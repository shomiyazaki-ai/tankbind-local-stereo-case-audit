"""Milestone 7 controls reconstructed from the execution-chat code.
NOT the original Windows-executed script; this consolidated version has NOT
been rerun on the user's Windows environment. Run from TankBind_T directory.
"""
from pathlib import Path
import numpy as np
from rdkit import Chem
from rdkit.Geometry import Point3D

CENTERS = {
    '1MMV_3AR': [('CA',2,(1,3,5))],
    '1Q1G_MTI': [("C4'",4,(3,5,8)),("C2'",6,(7,8,10)),
                 ("C3'",8,(4,6,9)),("C1'",10,(5,6,11))],
}

def det(mol, ci, neighbors):
    conf=mol.GetConformer()
    origin=np.array(conf.GetAtomPosition(ci-1))
    vectors=np.array([np.array(conf.GetAtomPosition(n-1))-origin for n in neighbors])
    return float(np.linalg.det(vectors))

def assign(mol):
    m=Chem.Mol(mol)
    Chem.RemoveStereochemistry(m)
    for atom in m.GetAtoms():
        for prop in ('_CIPCode','_CIPRank'):
            if atom.HasProp(prop): atom.ClearProp(prop)
    m.UpdatePropertyCache(strict=False)
    Chem.AssignStereochemistryFrom3D(m,confId=0,replaceExistingTags=True)
    return m

def cip(mol, ci):
    a=mol.GetAtomWithIdx(ci-1)
    return a.GetProp('_CIPCode') if a.HasProp('_CIPCode') else None

def transform(mol, matrix, translation):
    result=Chem.Mol(mol)
    conf=result.GetConformer()
    for i in range(result.GetNumAtoms()):
        p=matrix@np.array(conf.GetAtomPosition(i))+translation
        conf.SetAtomPosition(i,Point3D(*map(float,p)))
    return result

def run():
    outcomes={}
    R=np.array([[0.,-1.,0.],[1.,0.,0.],[0.,0.,1.]])
    reflection=np.diag([-1.,1.,1.])
    assert np.isclose(np.linalg.det(R),1.0)
    assert np.isclose(np.linalg.det(reflection),-1.0)
    for title in ('Crystal-Crystal','Rigid transformation','Atom-order permutation','Reflection'):
        passed_all=True
        print('\n===',title,'===')
        for case,entries in CENTERS.items():
            path=Path('inputs')/f'{case}_crystal.sdf'
            mol=Chem.SDMolSupplier(str(path),sanitize=False,removeHs=False)[0]
            if mol is None: raise RuntimeError(f'Cannot load {path}')
            if title=='Crystal-Crystal':
                other=Chem.Mol(mol)
                renumber=None
            elif title=='Rigid transformation':
                other=transform(mol,R,np.array([10.,-7.,3.]))
                renumber=None
            elif title=='Reflection':
                other=transform(mol,reflection,np.zeros(3))
                renumber=None
            else:
                permutation=list(reversed(range(mol.GetNumAtoms())))
                old_to_new={old:new for new,old in enumerate(permutation)}
                other=Chem.RenumberAtoms(mol,permutation)
                renumber=old_to_new
            a0,a1=assign(mol),assign(other)
            for name,ci,ns in entries:
                ci1=renumber[ci-1]+1 if renumber is not None else ci
                ns1=tuple(renumber[n-1]+1 for n in ns) if renumber is not None else ns
                d0,d1=det(mol,ci,ns),det(other,ci1,ns1)
                c0,c1=cip(a0,ci),cip(a1,ci1)
                if title=='Reflection':
                    geo=abs(d0)>1e-6 and np.isclose(d1,-d0,rtol=1e-10,atol=1e-10)
                    stereo=c0 in ('R','S') and c1 in ('R','S') and c0!=c1
                elif title=='Rigid transformation' or title=='Atom-order permutation':
                    geo=abs(d0)>1e-6 and np.isclose(d0,d1,rtol=1e-10,atol=1e-10)
                    stereo=c0 in ('R','S') and c0==c1
                else:
                    geo=abs(d0)>1e-6 and abs(d1)>1e-6 and np.sign(d0)==np.sign(d1)
                    stereo=c0 in ('R','S') and c0==c1
                passed=bool(geo and stereo)
                passed_all &= passed
                print(f'{case} {name}: geometry={"PASS" if geo else "FAIL"}, RDKit={c0}/{c1}, STATUS={"PASS" if passed else "FAIL"}')
        print(f'{title} control: {"PASS" if passed_all else "FAIL"}')
        outcomes[title]=passed_all
    if not all(outcomes.values()): raise SystemExit('FAIL: one or more controls')
if __name__=='__main__':run()
