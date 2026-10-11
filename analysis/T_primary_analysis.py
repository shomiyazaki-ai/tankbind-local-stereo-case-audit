
from pathlib import Path
from itertools import permutations
import csv

import numpy as np
from rdkit import Chem
import rdkit

EPS = 0.00005

CENTERS = {
    "1MMV_3AR": [
        ("CA", 2, (1, 3, 5), 11, (12, 13, 10))
    ],
    "1Q1G_MTI": [
        ("C4'", 4, (3, 5, 8), 4, (3, 5, 19)),
        ("C2'", 6, (7, 8, 10), 17, (18, 19, 6)),
        ("C3'", 8, (4, 6, 9), 19, (4, 17, 20)),
        ("C1'", 10, (5, 6, 11), 6, (5, 17, 7))
    ]
}

def load(case, kind):
    path = Path("inputs") / f"{case}_{kind}.sdf"
    mol = Chem.SDMolSupplier(
        str(path), sanitize=False, removeHs=False
    )[0]
    if mol is None or mol.GetNumConformers() != 1:
        raise RuntimeError(f"Invalid input: {path}")
    return mol

def graph(mol):
    rw = Chem.RWMol()
    for atom in mol.GetAtoms():
        a = Chem.Atom(atom.GetAtomicNum())
        a.SetNoImplicit(True)
        rw.AddAtom(a)
    for bond in mol.GetBonds():
        rw.AddBond(
            bond.GetBeginAtomIdx(),
            bond.GetEndAtomIdx(),
            Chem.BondType.SINGLE
        )
    return rw.GetMol()

def bond_diff(c, p, match):
    return sum(
        b.GetBondType() != p.GetBondBetweenAtoms(
            match[b.GetBeginAtomIdx()],
            match[b.GetEndAtomIdx()]
        ).GetBondType()
        for b in c.GetBonds()
    )

def clear_and_assign(mol):
    Chem.RemoveStereochemistry(mol)
    for atom in mol.GetAtoms():
        for prop in ("_CIPCode", "_CIPRank"):
            if atom.HasProp(prop):
                atom.ClearProp(prop)
    mol.UpdatePropertyCache(strict=False)
    Chem.AssignStereochemistryFrom3D(
        mol, confId=0, replaceExistingTags=True
    )

def cip(mol, idx):
    atom = mol.GetAtomWithIdx(idx - 1)
    return atom.GetProp("_CIPCode") if atom.HasProp("_CIPCode") else None

def vectors(mol, center, neighbors):
    conf = mol.GetConformer()
    origin = np.array(conf.GetAtomPosition(center - 1))
    return np.array([
        np.array(conf.GetAtomPosition(i - 1)) - origin
        for i in neighbors
    ])

def mul(a, b):
    values = [x * y for x in a for y in b]
    return min(values), max(values)

def interval_det(v):
    intervals = [
        [(float(x) - 2*EPS, float(x) + 2*EPS) for x in row]
        for row in v
    ]
    result = (0.0, 0.0)

    for perm in permutations(range(3)):
        inversions = sum(
            perm[i] > perm[j]
            for i in range(3) for j in range(i+1, 3)
        )
        sign = -1 if inversions % 2 else 1
        term = (float(sign), float(sign))

        for i in range(3):
            term = mul(term, intervals[i][perm[i]])

        result = (result[0] + term[0], result[1] + term[1])

    return result

def stable_sign(bounds):
    if bounds[0] > 0:
        return 1
    if bounds[1] < 0:
        return -1
    return 0

rows = []

for case, entries in CENTERS.items():
    crystal = load(case, "crystal")
    predicted = load(case, "tankbind")

    matches = graph(predicted).GetSubstructMatches(
        graph(crystal),
        uniquify=False,
        useChirality=False,
        maxMatches=1000
    )

    if not matches:
        raise RuntimeError(f"No mapping: {case}")

    match = min(matches, key=lambda m: bond_diff(crystal, predicted, m))

    mapped = Chem.Mol(crystal)
    conf = mapped.GetConformer()
    pconf = predicted.GetConformer()

    for ci, pi in enumerate(match):
        conf.SetAtomPosition(ci, pconf.GetAtomPosition(pi))

    ref = Chem.Mol(crystal)
    clear_and_assign(ref)
    clear_and_assign(mapped)

    for name, ci, cn, pi, pn in entries:
        if match[ci - 1] != pi - 1:
            raise RuntimeError(f"Mapping mismatch: {case} {name}")
        if tuple(match[n-1] + 1 for n in cn) != pn:
            raise RuntimeError(f"Neighbor mapping mismatch: {case} {name}")

        vc = vectors(crystal, ci, cn)
        vp = vectors(mapped, ci, cn)

        dc = float(np.linalg.det(vc))
        dp = float(np.linalg.det(vp))
        ic = interval_det(vc)
        ip = interval_det(vp)
        sc = stable_sign(ic)
        sp = stable_sign(ip)

        geo = (
            "INDETERMINATE" if 0 in (sc, sp)
            else "PRESERVED" if sc == sp
            else "INVERTED"
        )

        ccip = cip(ref, ci)
        pcip = cip(mapped, ci)

        rdkit_result = (
            "UNDEFINED" if ccip not in ("R", "S") or pcip not in ("R", "S")
            else "PRESERVED" if ccip == pcip
            else "INVERTED"
        )

        rows.append({
            "case": case,
            "center": name,
            "crystal_index": ci,
            "tankbind_index": pi,
            "crystal_neighbors": ",".join(map(str, cn)),
            "tankbind_neighbors": ",".join(map(str, pn)),
            "crystal_det_A3": f"{dc:.10f}",
            "tankbind_det_A3": f"{dp:.10f}",
            "crystal_interval_lo": f"{ic[0]:.10f}",
            "crystal_interval_hi": f"{ic[1]:.10f}",
            "tankbind_interval_lo": f"{ip[0]:.10f}",
            "tankbind_interval_hi": f"{ip[1]:.10f}",
            "geometry_result": geo,
            "crystal_CIP": ccip or "",
            "tankbind_CIP": pcip or "",
            "rdkit_result": rdkit_result,
            "agreement": geo == rdkit_result and geo != "INDETERMINATE"
        })

out = Path("T_primary_results.csv")

with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

print("Python/RDKit/NumPy:", rdkit.__version__, np.__version__)
print("Output:", out.resolve())
print("Rows:", len(rows))

for row in rows:
    print(
        row["case"], row["center"],
        "Geometry:", row["geometry_result"],
        "RDKit:", row["rdkit_result"],
        "Agreement:", row["agreement"]
    )
