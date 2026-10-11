# Validation record and evidence limits

This is a public, concise **provenance summary** of an existing, bounded analysis, not the complete private research diary or a human peer-review report. The primary code, final result CSV and later reconstructed controls are preserved **without modification** in this release.

## Fixed artifacts

| File | SHA-256 | Status |
|---|---|---|
| `analysis/T_primary_analysis.py` | `8a70c65cbc62c58745368c6f2287df06c2ae3366042eecf4117d4db92ad26578` | Original saved fixed-case primary implementation, unchanged |
| `results/T_primary_results.csv` | `ba1040997929f83c2b9f9f2f9ee95948a865a9893856bf4a17ba9a771bc810cf` | Original saved five-row result CSV (981 bytes), unchanged |

The original Windows execution reported byte-identical regeneration of the final CSV from an earlier frozen M8 copy in the same environment; that historical run is a **user-reported record**, not authenticated by inclusion of the M8 protected copy in this package. The CSV was subsequently regenerated from supplied fixed files and compared byte-for-byte in a separate Work audit.

## Independent computational rechecks of frozen data

- The Work audit on 2026-10-11 (Linux; Python **3.12.14**, RDKit **2026.09.1**, NumPy **2.3.5**, gemmi **0.7.5**) confirmed the 6 fixed-input hashes, enumerated heavy-atom graph correspondences without RDKit stereochemical assignment, recomputed exact-decimal determinant/rounding bounds, verified the 5 local RDKit assignments, ran later reconstructed transformation controls, and reproduced the CSV byte-for-byte.
- A subsequent computational recheck in a separate ChatGPT execution environment (Linux; Python **3.13.5**, RDKit **2025.09.4**, NumPy **2.3.5**, gemmi **0.7.4**) also reproduced the fixed CSV and control classifications and independently audited the same case-level calculations. These computational checks are **not human peer review or independent experimental replication**. Both share fixed study-design assumptions, reference graph and input fixtures.
- Original Windows run: Windows 11 Pro, Python **3.13.1**, RDKit **2026.09.1**, NumPy **2.5.3** (historical user-reported execution).

## Primary analysis

- For each predeclared center, compute the signed determinant of vectors from the carbon center to its **three ordered heavy-atom neighbors** on crystal and mapped predicted coordinates.
- The SDF textual coordinates have four decimals. A ±0.00005 Å allowance per coordinate component leads to ±0.00010 Å for vector components in a conservative interval bound. **All ten** determinant intervals avoid zero for these fixed inputs.
- The primary script's interval arithmetic uses standard floating-point values and does **not** promise generally rigorous directed outward rounding. A separate decimal-arithmetic Work recheck confirmed that its sign classifications hold **for these frozen inputs**; neither technique assesses experimental coordinate uncertainty.
- RDKit: remove existing stereo assignments and `_CIPCode`/`_CIPRank` properties, assign from 3D coordinates on the shared **crystal** chemical graph. The resulting five-center CIP sequence is S, S, S, R, S for both crystal and predicted coordinates.
- Geometry and RDKit share input coordinates, atom mapping and graph and must not be presented as two fully independent sources of chemical truth.

## Milestone 7 controls — historical versus reconstructed

`analysis/m7_controls_reconstructed.py` consolidates procedures originally tested separately in the research chat. **It is not the byte-identical script originally executed on the user's Windows device.** Its fixed crystal-fixture controls are:

| Control | Reconstructed-code result for five centers | Main detectable error class | Not independently established |
|---|---|---|---|
| Crystal self-comparison | 5/5 preserved | Baseline comparison inconsistency | Correct crystal–prediction atom mapping |
| Tracked atom-order permutation | 5/5 preserved | Hidden dependence on atom indices | Correct cross-file correspondence |
| Proper rigid rotation and translation | 5/5 preserved | Incorrect dependence on origin or axes | Predicted-coordinate transfer correctness |
| Mirror reflection (`x→−x`) | 5/5 inverted, RDKit R↔S | Failure to respond to chirality inversion | Real-world stereochemistry validity |

The reconstructed script passed all four controls in the Work audit and later execution environment. It does not test the primary script's full graph matching, transfer, or rounding path. Those were checked separately in the Work audit. Do not multiply these checks into a larger number of independent molecular observations.

## Limitations and incompletely verified provenance

- Original M7 scripts and historical protected M8 copy are unavailable in this public package.
- The original PoseBusters result row for 3AR reports `False`, but the exact underlying archived SDF-vs-fixed-fixture identity and cause of the different conditional local classification have **not** been established. The original raw PoseBusters verdict was **not** rerun here.
- The full PoseBusters paper SI was not verified in the Work audit. Absence of another equivalent record in the world is **not** claimed.
- The SDF/CIF upstream files are **not redistributed**. Reproduction requires retrieval of the exact fixed files and matching checksums; CCD source content may change in the future.
- No independent human review or third-party adoption is claimed, and the study does not estimate general model reliability.

## Transparency and attribution

The author used ChatGPT assistance in designing, implementing, interpreting, independently checking and documenting the fixed-case workflow, under the author's responsibility. Statements of computational rechecks are limited to the recorded runs; they are **not** presented as independent human expert verification or peer review. Related original work and sources are cited in the README and [`inputs_manifest.md`](inputs_manifest.md).
