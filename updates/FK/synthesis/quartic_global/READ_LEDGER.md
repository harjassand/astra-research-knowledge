# Read ledger — FK quartic global compatibility

Research date: 2026-10-14. Scope: assigned investigation of global compatible quartic profiles beyond the moving near-line theorem. All owned output is under `work/FK-quartic-global/`.

## Pinned/local inputs

| Source | Version/hash | Access depth and use |
|---|---|---|
| `work/FK_WORKER_CONTRACT.txt` | As present in the calling workspace | Read in full before work; honored the assigned-directory, pinned-source, no-cross-worker-output, and freeze requirements. |
| `work/FK_PIN.json` | SHA256 `828d12ae103d0714e4372b8d2ceba3e0bb0c83aadf4f762fdcd911837c8408d8` | Read in full. The clean capital checkout is pinned at `4c47df1fda950e27e48295689dd642194bfac046`. |
| `work/FK-sources/INTAKE_MANIFEST.json` | SHA256 `aa811a894c5bf820eb6187b768fe462fab39239c2883408021cdffa054351b67` | Read in full to verify supplied payload paths and source hashes. |
| `work/FK-sources/moving/ADAPTIVE_AFFINE_STABILITY.md` | 28,788 bytes; SHA256 `61a4c3a75967e07f8e5517f2a9d828b2074270cb2a4ceda8f8a3d6ba3344fe46` | Read Sections 1–7, 10–13 (file lines 17–34, 57–82, 86–117, 142–230, 235–334, 424–510). Used the exact optimized-gap formula, transverse theorem hypotheses, tangent/contact gap, resonant profiles, and stated missing operation. |
| `work/astra-capital` | Git HEAD `4c47df1fda950e27e48295689dd642194bfac046`; `git status --short` empty | Confirmed read-only clean pinned checkout. Read only the targeted N794/N797/N800/N803/N806 source mechanisms listed below; no archive was preloaded and no capital file was written. |

## Targeted capital mechanisms

| Mechanism source | SHA256 | Lines read and use |
|---|---|---|
| N794 `updates/FE/package/quartic/ASTRA_META_GENESIS_Morrey_quartics.md` | `7c88a08aa6aef88786751fde9671b7568e97676c516824028c3aac9d9859725b` | Lines 154–263: nine-coefficient left-SO(2) basis and exact 8×8 acoustic Gram interface. Lines 340–389: exact finite moment-completion equivalence and the unresolved gradient-compatibility-to-PSD-completion step. |
| N794 checker `updates/FE/package/quartic/verify_morrey_quartics.py` | SHA256 `b4f7d24e70562576bdffddab0a75bcdcd1984de91e0c66aa068675e862420ef7` | Read lines 1–130 to reconstruct the coefficient/acoustic basis for context; did not run or copy this checker. |
| N797 `updates/FG/package/quartic/ASTRA_SHARP_QUARTIC_THEOREM.md` | `6cd5cd449f07ecefb2956bb37ef42fba74795334e8ef058522b8a1af9e4dcd79` | Read status/scope and compatible-jet theorem, including lines 1–20, 210–271, 578–604. Used to keep its exact slice separate from the full left-SO(2) cone. |
| N797 `updates/FG/synthesis/quartic/ADJACENT_THEOREM.md` | `35a88dd514f635761f634521ed137e488b1ce1671e6874727a48a149ff8a4d08` | Read lines 1–60 for the sharp adjacent family, tensor certificate, scalar-representation limitation, and explicit scope boundary. |
| N800 `updates/FH/package/quartic/ASTRA_FULL_CONE_RIGIDITY.md` | `9a5142d0ca9b221b56543242276e298799e51ef1d2bb82edaf8af43d6bd8271d` | Read lines 5–14, 109–152, 300–390, and 488–512. Used the all-35 one-quadric nullspace closure, nine-coefficient singular-face Jensen theorem, and explicit positive-definite-sector gap. |
| N803 `updates/FI/package/quartic/ASTRA_POSITIVE_DEFINITE_BARRIER.md` | `8f1ca7b237503d4fbf4ac6c3ccf5f7f2d8a90fcb86a4368829476f41cf7e7a21` | Read lines 5–15, 294–381, 538–590, 640–646. Used the exact contact shear limitation, disjoint-profile superadditivity/defect formula, and the no-general-profile-decomposition boundary. |
| N806 `updates/FJ/package/quartic/CONTACT_COMPENSATION.md` | `f47796d9088b9a4b75c43d31f93b05d36dbe025c4db9d6a8ec02dbd6d0a8ca28` | Read lines 5–20, 253–287, 364–387, 442–497. Used the contact compensation theorem, exact nonzero three-wave resonance, shear limitation, and full reduced-Schur missing estimate. |
| N806 `updates/FJ/synthesis/contact_global/REPORT.md` | `78f0d995189ec361b526378aaef4db00d9ef445d16c4f35f5fd46666edaffe4b` | Read Sections 1–6 (lines 3–244), including exact all-background reduction, rotating-background controls, resonant anisotropic family, and concentration limitation. |

## Primary external sources

| Source/version | Accessed material and use | Access limitations |
|---|---|---|
| Pablo Pedregal, *Morrey's conjecture: rank-one convexity implies quasi-convexity for two-dimensional, two-component maps*, arXiv:1905.06571v5, submitted version dated 2026-06-18. [Abstract/version page](https://arxiv.org/abs/1905.06571v5); [HTML](https://arxiv.org/html/1905.06571v5). | Read the official arXiv abstract and HTML Introduction through Theorem 1.1, Section 6 fixed-point setup, Section 7 Proposition 7.1 proof, and conclusion. The paper claims every discrete two-component planar gradient measure is a laminate. The report records the precise feasibility step that needs an independent proof before using this sweeping claim: constrained-map rank and global segment/weight feasibility are inferred from a dimension/neighborhood argument in lines 752–786. | Only the arXiv preprint HTML/metadata was accessed; the PDF/TeX source and independent review/publication status were not checked. This is recorded as a primary-source claim, not an established theorem for this task. No failed access. |
| Giuseppe Bruno and Federico Pasqualotto, *Quasiconvexity for the Dacorogna–Marcellini Energy*, arXiv:2608.06367v1, submitted 2026-08-06. [Official version page](https://arxiv.org/abs/2608.06367). | Read arXiv metadata and abstract only. Used the authors' stated scope: Dacorogna–Marcellini energy, with a corollary for quartics invariant under both left and right rotations. | Full text/proof was not accessed in this subtask; no claim about proof validity is made. No failed access. |

## Independent exact check authored here

`exact_resonant_profile.py` was written in this owned directory without importing or copying any capital script. It computes Laurent coefficients directly for the exact three-frequency potential in the report and outputs all rational moments, the averaged Hessian, its leading principal minors, and the fully minimized gap to `exact_resonant_profile.json`.

Command: `work/FE-hidden-gate/venv/bin/python work/FK-quartic-global/exact_resonant_profile.py` from the workspace root. Runtime: Python 3.14.3, SymPy 1.14.0. The command exited 0 and generated the retained JSON. Scope is one finite compatible profile; this does not test or prove a global inequality. No external package was installed, and no code was run from another worker's directory.

## Access failures and exclusions

No local read/access failure occurred. No other `work/FK-*` output was read. No external messages or chats were sent. No source paper was copied into the owned directory. The only generated artifacts are the report, this ledger, the standalone exact-check script, and its rational output JSON.
