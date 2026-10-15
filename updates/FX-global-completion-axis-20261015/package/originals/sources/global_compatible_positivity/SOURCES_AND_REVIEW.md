# Sources, reconstruction, and review boundary

## Incoming mathematical data

The user supplied `astra_compatible_heat_moving_kernel_20261015.zip` and its research report. The unchanged ZIP is retained under `inputs/previous_moving_kernel_package.zip`. `PREVIOUS_REPLAY.json` records its SHA-256, checks of every manifest payload, and freshly executed outputs from `verify_moving_acoustic.py`, `verify_structure.py`, and `reconstruct.py` in a temporary isolated directory.

The original input distinguishes transcribed N850 coefficient reconstruction from byte-for-byte verification of the original repository JSON. This investigation preserves that distinction. Hashes establish the supplied ZIP's bytes, not independently verified original repository bytes.

The N850 dossier was also read through the connected GitHub tool at:
https://github.com/harjassand/astra-research-knowledge/blob/main/frontier/dossiers/N850.txt

Its supplied proof routes include the exact compatible-heat proof, G rational certificate, and subsequent distortion-margin analysis. The new theorem does not use a current Sol result, a repository status label, or the original positive G Gram matrix as a premise. Its universal polynomial identities are checked directly.

## External mathematics

1. Giuseppe Bruno and Federico Pasqualotto, *Quasiconvexity for the Dacorogna–Marcellini Energy*, arXiv:2608.06367v1, submitted 6 August 2026.
   https://arxiv.org/html/2608.06367v1
   Inspected: theorem scope, Sections 2–3, and Appendix A. The paper gives the componentwise heat/exact-two-form method and the two-sided rotational quartic theorem. Appendix A adds the determinant-square term using polyconvexity separately. This work does not claim those methods or that addition as new, and does not substitute its one-sided result for the paper's stated two-sided theorem.

2. Rodrigo Banuelos and Prabhu Janakiraman, *Lp-bounds for the Beurling–Ahlfors transform*, Theorem 1.1.
   https://www.math.purdue.edu/~banuelos/Papers/Beur_Ahl.pdf
   Inspected: original PDF page 2, including a rendered screenshot of the theorem. The complex-valued bound is sqrt(2(p^2-p)); its p=4 specialization gives sqrt(24). This is the only external operator-norm bound used. No sharp Beurling-norm claim is imported.

3. A. P. Calderon, *A note on biquadratic forms*, Linear Algebra and its Applications 7 (1973), 175–177.
   DOI: 10.1016/0024-3795(73)90052-9.
   The original publisher page was attempted but was not reliably retrieved in the final source pass. Its two-dimensional-factor SOS theorem is also explicitly stated in the authored primary papers below. The original proof was not independently reconstructed. This theorem is used only for the contextual full-acoustic-cone representation, not for the new heat certificate or completion proof.

4. Yi Xu, Chunfeng Cui, and Liqun Qi, *Sum of Squares Decompositions for Structured Biquadratic Forms*, Communications on Applied Mathematics and Computation (2026).
   https://link.springer.com/article/10.1007/s42967-026-00586-7
   Inspected: primary article's historical statement of Calderon's m-by-2 biquadratic SOS theorem and its distinction from higher-dimensional PSD-not-SOS forms. Its newer results are not premises of the new construction.

5. Chunfeng Cui, Liqun Qi, and Yi Xu, *Positive Semi-Definite and Sum of Squares Biquadratic Polynomials*, Mathematics 13(14), 2294 (2025).
   https://www.mdpi.com/2227-7390/13/14/2294
   Inspected: primary article's corresponding background statement. No result about general four-by-six positive forms being SOS is assumed.

## What has and has not been checked

The new standalone verifier regenerates exact polynomial identities, closedness, primitives, matrix ranks, two quotient identities, the positive pivot formulas, acoustic necessary conditions, the coefficient decomposition, and an actual compatible Fourier heat-dissipation obstruction. It reads the exported JSON and does not call the discovery programs.

Universal positivity over both unbounded parameter components is justified by the explicit analytic Schur-complement argument in the report. The finitely many rational instances are cross-checks of this formula, not evidence replacing that argument.

The heat-to-quasiconvexity passage, density, elliptic estimate, and input-linear covariance are written in the report. They are not mechanically formalized. No external mathematician reviewed this package. Historical novelty, external correctness, and formal proof verification remain unresolved.

The literature search establishes relevant predecessors and method boundaries, not exhaustive priority clearance. In particular, the simple determinant-square heat obstruction could have prior appearances; no historical priority is claimed for it.
