# A Local Stereochemistry Audit of Two Public TankBind Test Cases

**A fixed-case technical record, not a general benchmark or a new stereochemistry method.**

This record checks whether five preselected tetrahedral carbon centers in two public PoseBusters test fixtures retain their local orientation when coordinates from the `tankbind` SDFs are compared with the corresponding crystal SDFs **on the same crystal-derived molecular graph and with predetermined atom mappings**. It uses a signed determinant of three ordered heavy-atom neighbor vectors, checks the sign against an SDF text-coordinate rounding envelope, and compares the classifications with RDKit's 3D-based stereochemistry assignment. All five selected centers are **PRESERVED** in both comparisons. These are two fixed cases, not independent statistical samples; no general inference about TankBind's stereochemical accuracy is warranted.

**Record type:** reproducible fixed-case software/technical record · **Version:** `v1.0.0` · **Author:** Sho Miyazaki · **Affiliation:** Independent researcher, Tokyo, Japan. This repository is not a peer-reviewed research article.

## Scope and results

| Public fixture | Preselected carbon centers | Geometric classification | RDKit CIP (crystal → mapped prediction) |
| --- | --- | --- | --- |
| `1MMV_3AR` | `CA` | `PRESERVED` | S → S |
| `1Q1G_MTI` | `C4′`, `C2′`, `C3′`, `C1′` | `PRESERVED` (4/4) | S → S, S → S, R → R, S → S |

For all five centers, the signed determinant and RDKit classifications agree and the **ten** conservative determinant intervals (five crystal and five mapped predicted structures) exclude zero when each input coordinate component is assigned an SDF-text rounding allowance of ±0.00005 Å. The intervals address **text rounding only**, not physical uncertainty or experimental positional error. Full decimal values, intervals, atom indices and comparisons are in [`results/T_primary_results.csv`](results/T_primary_results.csv).

## Relationship to the published PoseBusters results

The [PoseBusters paper's published results table](https://zenodo.org/records/8278563/files/posebusters_paper_results.csv?download=1), when filtered to `dataset=astex`, `method=tankbind`, `post-processing=none`, reports `sp3_stereochemistry_preserved=False` for `1MMV_3AR` and `True` for `1Q1G_MTI`. Here, the **specific 3AR CA center** is classified as locally `PRESERVED` after mapping TankBind coordinates onto the crystal-derived graph. **These are not demonstrated to be the same measurement.** The published table's underlying result-generating SDF files have not been shown to be byte-identical to the fixed test fixtures, nor has the original PoseBusters verdict been rerun. The original SDFs also differ in some formal-charge and/or bond-order assignments. The reason for the different 3AR labels remains **undetermined**. **We do not claim a PoseBusters error, a TankBind bug, or resolution of a discrepancy.** See [`provenance/inputs_manifest.md`](provenance/inputs_manifest.md) for the exact filters, data provenance, chemical-graph differences and atom mapping.

## Reproduce this fixed case

The four input SDFs are **not redistributed** here. Retrieve their exact files from the immutable PoseBusters commit and verify SHA-256 hashes using the source URLs and checksum table in [`provenance/inputs_manifest.md`](provenance/inputs_manifest.md). Two RCSB CCD CIF snapshots were consulted to validate chemical labels; the analysis scripts themselves need only the four SDFs. CCD downloads and audited snapshot hashes are also recorded there.

Recommended verified environment for reproducing the archived result: **Python 3.13.5, RDKit 2025.09.4, NumPy 2.3.5** (Linux; another verified Work environment used Python 3.12.14, RDKit 2026.09.1, NumPy 2.3.5). The original Windows run used Python 3.13.1, RDKit 2026.09.1 and NumPy 2.5.3. This is not a promise of compatibility across arbitrary versions.

```bash
python -m pip install -r requirements.txt
mkdir -p inputs
# Download the four exact .sdf files into inputs/ using provenance/inputs_manifest.md.
# Verify their SHA-256 checksums BEFORE running the scripts.
python analysis/T_primary_analysis.py
python analysis/m7_controls_reconstructed.py
```

**Important:** Run both scripts from the repository **root**. The unchanged primary script expects `inputs/<case>_<kind>.sdf` relative to the working directory, and **writes `T_primary_results.csv` to the current working directory**, not to `results/`. Compare that newly generated CSV byte-for-byte against the frozen [`results/T_primary_results.csv`](results/T_primary_results.csv), without overwriting the archived reference file. For example:

```bash
sha256sum T_primary_results.csv results/T_primary_results.csv
# Expected SHA-256 for BOTH: ba1040997929f83c2b9f9f2f9ee95948a865a9893856bf4a17ba9a771bc810cf
```

On Windows PowerShell, use `Get-FileHash -Algorithm SHA256` instead of `sha256sum`. Check the *output file itself*; the script's final `Python/RDKit/NumPy:` log label currently prints RDKit and NumPy versions, **not the Python version**. The primary script and archived result CSV have been copied without changes; their hashes are in [`provenance/validation.md`](provenance/validation.md).

The Milestone 7 control script is **a later consolidated reconstruction**, not the original set of Windows-executed scripts. Its four checks use the crystal inputs: crystal self-comparison, a tracked atom-order permutation, proper rigid rotation plus translation, and reflection. Passing those controls does not itself establish the correctness of cross-file atom mapping, coordinate transfer, or the determinant rounding envelope. See [`provenance/validation.md`](provenance/validation.md).

## Interpretation and limits

- All results concern **two fixed cases, five selected centers, fixed local mapping and a common crystal-derived graph**; they do not evaluate all stereocenters in all predictions or the model's error rate.
- The raw crystal and TankBind SDFs are not identical in their original chemical representations. The analysis intentionally preserves the crystal **graph** while substituting mapped predicted **coordinates**; it does **not** reproduce the original PoseBusters chemical-identity or whole-molecule verdict.
- RDKit and signed-determinant checks share the same coordinates, local mapping and reference graph. They are two computational cross-checks, **not independent chemical experiments**.
- The floating-point interval implementation in the original script is not a general-purpose rigorously outward-rounded interval package. For **these fixed coordinates**, a separate decimal-arithmetic audit verified sign stability.
- No cause analysis of the published 3AR `False` entry, new docking predictions, further cases, or general claims are made.

## Sources, attribution, validation and reuse

- [PoseBusters fixed-source repository](https://github.com/maabuu/posebusters/tree/1dd61e568d4507b5ab5579e161806447bca3b859) (see its own LICENSE and source notices).
- Buttenschoen M, Morris GM, Deane CM. *PoseBusters: AI-based docking methods fail to generate physically valid poses or generalise to novel sequences*. **Chemical Science** (2024), DOI: [10.1039/D3SC04185A](https://doi.org/10.1039/D3SC04185A).
- [PoseBusters paper data record](https://zenodo.org/records/8278563) and [RCSB Chemical Component Dictionary](https://www.rcsb.org/).
- [RDKit documentation](https://www.rdkit.org/docs/source/rdkit.Chem.rdmolops.html).

[`provenance/inputs_manifest.md`](provenance/inputs_manifest.md) records the precise upstream inputs and matching rules. [`provenance/validation.md`](provenance/validation.md) documents the historical vs. later reconstructed controls, computational reruns, evidence levels and limitations. The external source data are **not relicensed** by this repository's MIT license. This record includes AI-assisted code analysis, checking and preparation; the named author remains responsible for the presentation and claims. AI-led checks do not constitute independent human peer review.

**Citation:** See [`CITATION.cff`](CITATION.cff). The Zenodo DOI, once assigned, identifies the frozen release and does not certify peer review or novelty. No DOI is asserted before issuance.
