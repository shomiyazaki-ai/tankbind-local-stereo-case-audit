# Input manifest, fixed atom correspondence and prior-art comparison

## Origin and frozen checksums

The four SDFs come from the **PoseBusters** `tests/conftest` fixtures at commit `1dd61e568d4507b5ab5579e161806447bca3b859`. The CIF files are RCSB Chemical Component Dictionary snapshots checked on 2026-10-11. Place **only the four SDFs** under `inputs/` for the two included Python scripts. The CIF files are provenance/CCD reference evidence, **not** runtime dependencies of the frozen scripts.

| File | Source download URL | SHA-256 |
|---|---|---|
| `1MMV_3AR_crystal.sdf` | [download](https://raw.githubusercontent.com/maabuu/posebusters/1dd61e568d4507b5ab5579e161806447bca3b859/tests/conftest/1MMV_3AR/1MMV_3AR_crystal.sdf) | `4e1fc699f0288596ab59b22ae4d2f7d168fbcb58a9c808a3a6ff3dbf6b297bc9` |
| `1MMV_3AR_tankbind.sdf` | [download](https://raw.githubusercontent.com/maabuu/posebusters/1dd61e568d4507b5ab5579e161806447bca3b859/tests/conftest/1MMV_3AR/1MMV_3AR_tankbind.sdf) | `163ff81187ca67f0e39925a6dd9710250e74d8ccd88b898b7f9731a0c463bf0f` |
| `1Q1G_MTI_crystal.sdf` | [download](https://raw.githubusercontent.com/maabuu/posebusters/1dd61e568d4507b5ab5579e161806447bca3b859/tests/conftest/1Q1G_MTI/1Q1G_MTI_crystal.sdf) | `9fa835f282fbaa034d372dd37139d3c0d27c9aae7daaeab7ae410e3fee9de3aa` |
| `1Q1G_MTI_tankbind.sdf` | [download](https://raw.githubusercontent.com/maabuu/posebusters/1dd61e568d4507b5ab5579e161806447bca3b859/tests/conftest/1Q1G_MTI/1Q1G_MTI_tankbind.sdf) | `fdb5ed3f4002c8c6241520010664f94778725137c2d466b92c4df9f657f7f356` |
| `3AR.cif` | [download](https://files.rcsb.org/ligands/download/3AR.cif) | `f9682688c906eed03b0cc4300472b707f1f9ebc921edf9dbc264fc836618905b` |
| `MTI.cif` | [download](https://files.rcsb.org/ligands/download/MTI.cif) | `0f9603f8a5d7af4b0e0dcb088e98fcb5b09ef7eb0cfca115cf119c1f6d88ae33` |

The six user-provided files matched these hashes and the independently fetched public files byte-for-byte in the 2026-10-11 Work audit. **The CCD hashes identify the retrieved snapshots; they are not historical CCD version identifiers.** Public CCD endpoints may evolve. File hashes, rather than the current endpoint alone, identify the audited bytes. If the current file does not match the listed hash, do not silently substitute it.

For POSIX environments, run `sha256sum inputs/*.sdf` (and `sha256sum 3AR.cif MTI.cif` if separately downloading CCD snapshots). On Windows PowerShell, `Get-FileHash -Algorithm SHA256 inputs\*.sdf` is an equivalent way to inspect hashes. Compare the outputs to the table; the scripts themselves do not enforce hash pinning.

## Ordered correspondence for the five preselected carbon centers

Indices below are **1-based SDF atom numbers**. The order of the three neighboring heavy atoms is part of the fixed signed-determinant convention. The same fixed correspondence is used for crystal and predicted coordinates.

| Case / center | Crystal center (ordered neighbors) | Predicted center (ordered neighbors) | CCD neighbor labels (ordered); implicit H |
|---|---|---|---|
| `1MMV_3AR` CA | `2 (1,3,5)` | `11 (12,13,10)` | N, C, CB; HA |
| `1Q1G_MTI` C4′ | `4 (3,5,8)` | `4 (3,5,19)` | C5′, N4′, C3′; H4′ |
| `1Q1G_MTI` C2′ | `6 (7,8,10)` | `17 (18,19,6)` | O2′, C3′, C1′; H1 |
| `1Q1G_MTI` C3′ | `8 (4,6,9)` | `19 (4,17,20)` | C4′, C2′, O3′; H3′ |
| `1Q1G_MTI` C1′ | `10 (5,6,11)` | `6 (5,17,7)` | N4′, C2′, C9; H1′ |

All-graph heavy-atom correspondence (element and connectivity, without stereochemical labels or geometry) yielded **two** candidate matches for 3AR and **one** for MTI. The 3AR whole-graph ambiguity exchanges terminal O/OXT labels; the prescribed 3AR center and its ordered local neighbors are the same under both matches. For the 3AR mapping used in the analysis, bond-order differences across crystal and raw prediction are zero; the other mapping has two. No mapping was chosen by maximizing stereochemical agreement. Four MTI centers have unique local correspondences.

## Chemical representation differences in the original SDFs

**Mapping here does not imply full chemical identity.** Under the selected element/connectivity correspondence:

- `1MMV_3AR`: zero mapped bond-order differences; two mapped N atoms have differing formal charges (crystal N indices 1 and 11 vs predicted N indices 12 and 6, respectively).
- `1Q1G_MTI`: six mapped bond orders differ (crystal bond atom pairs `(14,15)`, `(15,16)`, `(17,18)`, `(18,19)`, `(14,20)`, `(19,20)`); two mapped N atoms differ in formal charge (crystal N indices 5 and 13 vs predicted N indices 5 and 9).

The main analysis **copies the crystal chemical graph and transfers predicted coordinates** via the fixed mapping. Thus its local geometry/CIP comparison is conditional on the crystal graph. It does not evaluate the raw predicted SDF's original bond-order/charge description as a whole-molecule identity verdict.

## Published result comparison: provenance, not a bug claim

Source: [PoseBusters original paper-results CSV](https://zenodo.org/records/8278563/files/posebusters_paper_results.csv?download=1) from [Zenodo record 8278563](https://zenodo.org/records/8278563). Work audit download SHA-256: `613f941c5f9beca14497acb16d6bb601ddd4e7aa94aafed8852b48038ea11efb`.

Exact row selection in the publication results CSV: `dataset=astex`, `method=tankbind`, `post-processing=none`, and `(pdb_id,ccd_id)` equals `(1MMV,3AR)` or `(1Q1G,MTI)`.

| Selected row | Published `sp3_stereochemistry_preserved` | Here, **fixed local carbon center(s)** |
|---|---|---|
| `1MMV_3AR` | `False` | CA: `PRESERVED` on mapped crystal graph |
| `1Q1G_MTI` | `True` | C4′, C2′, C3′, C1′: `PRESERVED` on mapped crystal graph |

This is a **non-equivalent comparison**, not an established contradiction. We have **not** verified byte identity of the archived SDFs underlying the published results and the later frozen test fixtures. Nor did this work execute the original end-to-end PoseBusters procedure on the raw SDFs. The differing 3AR entries have **no established cause** and must not be reported as an error or an identified general failure boundary.

Sources for context: Buttenschoen M, Morris GM, Deane CM, *Chemical Science* (2024), DOI [10.1039/D3SC04185A](https://doi.org/10.1039/D3SC04185A); [fixed repository](https://github.com/maabuu/posebusters/tree/1dd61e568d4507b5ab5579e161806447bca3b859).
