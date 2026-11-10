# Fixed-contact arbitrary-Hessian theorem for J_1

## What is proved

At **r=k=1**, at the **fixed affine mean A_1=[[0,1],[1,0]]**, every real periodic scalar potential psi in W^{2,4} satisfies

    average J_1(A_1+t diag(2,-4)D^2 psi) >= J_1(A_1)

for every real amplitude t. The inequality is strict if t and the Hessian are nonzero. The theorem covers all frequencies and their interactions; it does not assume separability, oddness, small amplitude or a sign of the Jacobian.

The equivalent vector perturbation is phi=diag(2,-4) grad psi. Thus its gradient is genuinely compatible. Compactly supported scalar potentials are also covered by periodization and approximation.

## What is not proved

- The affine mean is not arbitrary.
- The parameter is exactly r=k=1, where k=(2r+1)/3.
- The perturbations are transformed scalar Hessians, not all vector gradients.
- This is not the full J_r quasiconvexity result or a negative Jensen field.
- No historical novelty claim or exhaustive prior search is made.

## Contents

- THEOREM_AND_PROOF.md: standalone definitions, heat identities, exact constants, full quartic payment and function-space proof.
- INDEPENDENT_REVIEW.md: a separate reconstruction, including a second exact quartic payment and prior/scope assessment.
- check_exact.py: standard-library rational arithmetic for every displayed polynomial identity in the main proof and the positive Gram matrix.
- CHECK_RESULT.json: saved output from that checker. It does not replace the analytic proof.
- PROVENANCE.md: exact source bindings and delivery edits.
- MANIFEST.sha256: SHA256 checksums for all other packet files.

## Reproduce the finite algebra

With Python 3.9 or later, run:

    python check_exact.py

No third-party packages, numerical solvers, network connection or experimental data are required. The script checks the original J_1 expansion, the contact identity including the two null averages, the quartic remainder, the Gram identity, its exact positive principal minors, and the rational Schur bounds. A successful run prints JSON with status PASS. Heat convergence, compatibility and Sobolev density remain the analytic obligations proved in the text.

## Strong related primary reference

André Guerra, “Quasiconvexity of the Burkholder function on symmetric matrices,” arXiv:2608.23388v1: https://arxiv.org/html/2608.23388v1 . Its integrands and hypotheses should not be silently substituted for the distinct density and indefinite transformation here.
