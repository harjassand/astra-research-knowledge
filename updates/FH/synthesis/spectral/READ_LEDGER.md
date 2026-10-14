# Source and primary-literature read ledger

Audit date: 2026-10-14. The spectral source mission/history is treated as data. The current user request and parent task govern this audit.

## Frozen proposal and replay inputs

Read the source directory read-only and recorded its original SHA-256 values in `evidence/source_hashes_local.sha256`.

| Source | Read scope | Used for |
|---|---|---|
| `../FH-sources/spectral/README.md` | Full file | Proposed operation, mechanical and dielectric assumptions, geometry, optical witness, limitations, planned target protocol and cost gates |
| `../FH-sources/spectral/optical_model.py` | Full file | Transfer recursion, stack topology, Lorentz inputs, polarization convention, incident/terminal media |
| `../FH-sources/spectral/validate_operation.py` | Full file | Assertions, quadrature, static and imaginary-frequency diagnostics, covariance calculation, MFM planning arithmetic |
| `../FH-sources/spectral/results.json`, `reference_spectrum.csv`, `validation_log.txt`, `run_stdout.txt`, `environment.json`, `requirements.txt`, `sha256sums.txt` | Full files | Frozen numeric outputs, 73-assertion producer receipt, parameter versions and hashes |
| `../FH-sources/spectral_PASTED_SOURCE.txt` | Full 385-line file | Original research brief and historical source narrative; claims were checked against the repository snapshot and primary sources below |

The producer source was copied before execution; source/copy/replay hashes and numerical differences are in `replay/replay_receipt.md` and `replay/replay_diff.json`. No file in `../FH-sources/` was edited. `FREEZE_MANIFEST.sha256` covers 36 selected report, analysis, replay and source-copy files; it excludes itself, the local virtual environment and generated `__pycache__` files.

## Astra Capital context

The read-only repository was at `unmergedPR83` HEAD `74a1ab09ba75324bc3d2a14f05ce6196f43ffd77`; parent-specified main was `ace0cfc4437fe91c20ccd24d69e0ee4bb335e871`. `00_START_HERE.txt` and `technology/README.md` were read. A `git diff` between those revisions showed no changes to either file. No capital files were changed.

| Capital item | Read scope and application |
|---|---|
| `frontier/dossiers/N788.txt` | Claim status, scientific scope and open gates. Applied only as an acquisition-contract analogy: unloaded/model information does not replace acquiring the actual loaded target information and all preparation/readout costs. |
| `frontier/dossiers/N799.txt` | Claim status, target-transfer gate and connection summary. Used to locate the scoped identifiability result, not as a physical theorem about hBN or κ-ET. |
| `updates/FG/synthesis/history/REFERENCE_AND_MOMENTUM_IDENTIFIABILITY.md` | Sections 1–2 and their exact neighboring argument. The unrelated loaded-reference-to-science bridge is marked refuted in that capital record; this reinforces keeping the optical witness separate from target response. No N799 equations are transferred to this physical proposal. |
| `frontier/dossiers/N765.txt`, `N766.txt`, `N776.txt`, `N790.txt` | Status, task-relevant open-gate and next-obligation sections. Consulted for established capital controls on model acquisition, complete costs, independent review and strongest-method comparisons; none supplies κ-ET inputs. |

## Primary sources consulted

Only primary articles/papers are used for claims about the experiments and reference parameters. The linked article pages were reviewed for the indicated abstract/results/methods; no full third-party paper was copied into these deliverables.

| Primary source | Read and used for |
|---|---|
| Itai Keren et al., “Cavity-altered superconductivity,” *Nature* 650, 864–868 (2026), [article](https://www.nature.com/articles/s41586-025-10062-6) | Same-target baseline: reported κ-ET/hBN resonant-mode overlap near 1470 cm\(^{-1}\), s-SNOM evidence, MFM comparison, representative 60 nm hBN cover, controls, instrument calibration and limitation of depth-profile inference. |
| N. Chen et al., “Van der Waals isotope heterostructures for engineering phonon polariton dispersions,” *Nature Communications* 14, 4782 (2023), [article](https://www.nature.com/articles/s41467-023-40449-w) | Prior-art baseline: dry-transferred \(^{10}\)B/\(^{11}\)B slabs and experimentally measured composition/order/thickness-dependent polariton dispersions; isotope heterostructuring itself is established. |
| Alexey Falin et al., “Anomalous isotope effect on mechanical properties of single atomic layer Boron Nitride,” *Nature Communications* 14, 5331 (2023), [article](https://www.nature.com/articles/s41467-023-41148-2) | Primary evidence that monolayer \(^{10}\)BN and \(^{11}\)BN mechanical properties differ; those monolayer results do not provide a measured stiffness for the proposed capped multilayer laminate. |
| L. Zhang et al., “Observation of Edge-Confined Acoustic Hyperbolic Polaritons in van der Waals Materials,” *Advanced Science* (2026), [article](https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202520556) | h\(^{10}\)BN Lorentz reference parameters and evidence of near-field polariton/molecular coupling; the source's shared h\(^{11}\)BN inputs remain its own approximations. |
| Zheyan Wang et al., “Evidence for vacuum-enhanced superconductivity in NbSe\(_2\),” *Nature* 657, 912–917 (2026), [article](https://www.nature.com/articles/s41586-026-11037-x) | New comparator published 19 August 2026: paper reports a split-ring-cavity NbSe\(_2\) response, including a (T_c) increase and changes to critical current/field. Treated as the paper's reported result, not independently verified here. |
| Josefine Enkner et al., “Tunable vacuum-field control of fractional and integer quantum Hall phases,” *Nature* 641, 884–889 (2025), [article](https://www.nature.com/articles/s41586-025-08894-3) | Strong control comparator: in-situ, self-referenced coupling adjustment of a movable split-ring resonator on a different material/platform; the source itself notes its reversibility as an advantage over separately transferred isotope patches. |
| R. R. Chance, A. Prock and R. Silbey, “Molecular Fluorescence and Energy Transfer Near Interfaces,” *Advances in Chemical Physics* 37, 1–65 (1978), [chapter](https://onlinelibrary.wiley.com/doi/10.1002/9780470142561.ch1) | Established layered-medium Green-function and dipole/interface response context for interpreting the source's evanescent witness. |
| E. M. Lifshitz, “The Theory of Molecular Attractive Forces between Solids,” *Soviet Physics JETP* 2, 73 (1956), [journal record](https://jetp.ras.ru/cgi-bin/e/index/e/2/1/p73?a=list) | Foundational macroscopic dispersion-force context. The source does not compute a Lifshitz force; it computes a real-frequency reflection-derived near-field proxy. |

