# Read ledger

Audit date: 2026-10-14. All capital reads used the pinned clean checkout `work/astra-capital` at `4c47df1fda950e27e48295689dd642194bfac046`. The initial pin and incoming intake manifest were read before proof reuse. No capital files were written. Only this assigned directory was used for new files, copies, replays, and outputs.

## Supplied moving source

- Original: `/Users/harjas/Downloads/ASTRA_Moving_Compatibility/ADAPTIVE_AFFINE_STABILITY.md`.
- Preserved intake copy: `work/FK-sources/moving/ADAPTIVE_AFFINE_STABILITY.md`; audit copy: `work/FK-affine-audit/inputs/moving/ADAPTIVE_AFFINE_STABILITY.md`.
- Intake manifest: `work/FK-sources/INTAKE_MANIFEST.json`, moving entry reports 28,788 bytes, SHA256 `61a4c3a75967e07f8e5517f2a9d828b2074270cb2a4ceda8f8a3d6ba3344fe46`.
- Proof reviewed in full. Relevant sections: assumptions/theorem §§1–2, adaptive covariance fit §3, moving spectral/Finsler estimate §4, Schur complement §5, regressed cubic §6, full minimization §7, tangent counterexample §11, limits/prior-art §14.
- Producer script `verify_adaptive_affine.py` was inspected, copied to `replay/producer_moving/`, then run with the existing `work/FE-hidden-gate/venv/bin/python`. It imports SymPy, has no network or optimizer calls, and writes its JSON beside itself. All 11 exact-check groups passed. The original input copy was not modified.
- The supplied `adaptive_verification.json`, `verification.log`, `prior_replay.log`, README, manifest, and exploration files were retained as input copies. Exploratory optimizer code was inspected but not executed; it is not proof evidence.

## Original capital proofs and gates

- N806 dossier and current gate: `work/astra-capital/frontier/dossiers/N806.txt`, `frontier/gates/G-FJ-N806-REVIEW.json`; source proof `updates/FJ/package/quartic/CONTACT_COMPENSATION.md` (SHA256 `f47796d9088b9a4b75c43d31f93b05d36dbe025c4db9d6a8ec02dbd6d0a8ca28`) and `updates/FJ/synthesis/contact_audit/PROOF_RECONSTRUCTION.md` (SHA256 `51c00aabba38baee942dd1135acaa4d5661e09c478cd4b78e621984ec06dbbda`). Copied under `references/capital/N806/`. Read the fixed-contact compensation, contact-plane Jensen theorem, explicit open moving-Schur obligation, and scoped examples. Copied and replayed `verify_contact_compensation.py`: 9/9 exact groups passed.
- N803 dossier and current gate: `work/astra-capital/frontier/dossiers/N803.txt`, `frontier/gates/G-FI-N803-REVIEW.json`; source proof `updates/FI/package/quartic/ASTRA_POSITIVE_DEFINITE_BARRIER.md` (SHA256 `8f1ca7b237503d4fbf4ac6c3ccf5f7f2d8a90fcb86a4368829476f41cf7e7a21`). Copied under `references/capital/N803/`. Read the two-contact rigidity, tangent quartic (G), acoustic/covariance flatness, compatible concentration example, and exact scope limits. Copied and replayed `verify_positive_definite.py`: 12/12 exact groups passed.
- The two copied capital verifiers use self-contained SymPy calculations and write results beside the replay copies. They do not certify the analytic arguments or external correctness. No other FK worker output was read.

## Primary external sources

1. **T. J. Meijer et al., “A General Non-Strict Finsler’s Lemma,” arXiv:2403.10306v1 (15 Mar 2024).** Official arXiv HTML: <https://arxiv.org/html/2403.10306v1>. Read Lemma 2 and its stated indefinite-matrix hypothesis, HTML lines 75–91; also checked the distinction from arbitrary semidefinite constraint matrices in lines 64–75. The result directly supplies scalar feasibility for the indefinite determinant quadratic form. This is prior mathematics, not a new contribution of the moving note.

2. **Jan Kristensen, “On the non-locality of quasiconvexity,” Ann. Inst. H. Poincaré C 16 (1999), 1–13.** Official Numdam scan: <https://www.numdam.org/item/AIHPC_1999__16_1_1_0.pdf>. The full 14-page PDF text was opened. Read the definition of local quasiconvexity, PDF text lines 103–107; the strict Legendre–Hadamard discussion, lines 88–102; and Proposition 1, lines 148–156. Proposition 1 is the exact prior used here: $C^2$ plus strict Legendre–Hadamard positivity at every matrix implies local quasiconvexity. No claim was imported that it covers the degenerate transverse contact or the relative-moment/all-background inequality in this audit. The paper’s separate non-locality construction is for $n\ge3,m\ge2$, not a $2\times2$ counterexample.

3. **Giuseppe Bruno and Federico Pasqualotto, “Quasiconvexity for the Dacorogna–Marcellini Energy,” arXiv:2608.06367v1 (arXiv header 6 Aug 2026).** Official arXiv HTML: <https://arxiv.org/html/2608.06367v1>. Read the abstract and definitions, lines 27–53 and 68–82; Theorem 1, lines 88–95; and Theorem 2, lines 97–109. The primary source proves the Dacorogna–Marcellini family is quasiconvex through its rank-one-convex endpoint and gives the left-and-right-rotation-invariant quartic result. It does not establish the incoming result for arbitrary nonrotational quartics. The source’s page header and title-page date differ (6 Aug vs 24 Aug 2026); the version identifier is recorded exactly.

## Access and failure record

The official arXiv HTML pages and Numdam PDF text opened successfully. No access failure occurred. No literature search was treated as exhaustive and no historical-priority conclusion is made. The scientific scripts were executed only from the assigned copy-first replay paths with the pre-existing Python environment; no environment was installed and no optimization or physical experiment was run.

## Independent adversarial implementation

- Authored `work/FK-affine-audit/adversarial_check.py` independently of the producer verifier and capital proof checkers. It reconstructs the Dacorogna–Marcellini quartic and exact atomic-law moments in SymPy, then checks the singular line law, rare rank-one transverse spikes, nonzero determinant-normal covariance regression, the tangent balanced-law counterexample, an exact symbolic tangent scale family, and the zero law. The script passed six named groups with `work/FE-hidden-gate/venv/bin/python`; results are in `adversarial_results.json`. The tangent symbolic family has negative affine trial limit `-3/4` while both transverse ratios tend to zero, which is a moment-only boundary counterexample, not a compatible-gradient counterexample.
- `REPORT.md` contains the reconstructed theorem, proof and comparisons; claims are explicitly separated into incoming-source results, independent derivations, copy-first replays, and the new exact adversarial implementation. No producer exploratory optimizer or finite Fourier search was treated as proof.
- Final file integrity and scope are frozen in `work/FK-affine-audit/MANIFEST.json`. It covers every file under this assigned directory except itself; copied sources and references are tagged as inputs rather than audit-authored results. The manifest does not authenticate the cited external papers or establish theorem correctness beyond the stated checks.
