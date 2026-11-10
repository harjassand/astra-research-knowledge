# J_1: all affine means, adapted scalar-Hessian perturbations

This packet proves and independently checks a restricted all-mean theorem. It materially extends a fixed-contact result, but it does not settle the full global quasiconvexity question.

**Proved:** k=r=1. For every affine matrix A, choose a left rotation R in SO(2) with R^T A upper triangular, and put L_A=R diag(2,-4). For every real periodic W^{2,4} scalar psi, at every amplitude,

    average J_1(A+L_A Hess psi) >= J_1(A).

The proof gives a pointwise determinant-translated support, strictness for nonzero Hessians, and a uniform quantitative remainder. It includes singular A, any rectangular torus and compactly supported scalar potentials.

**Not proved:** arbitrary W^{1,4} vector perturbations; a single fixed Hessian multiplier at every A; other values of r; historical novelty. The target rotation does not rotate the periodic source lattice.

Start with THEOREM_AND_PROOF.md. INDEPENDENT_REVIEW.md reconstructs all PSD, Gram, transformation and function-space steps. The exact checker verifies polynomial identities; it complements, rather than replaces, the analytic proof.

## Reproduce the exact checks

Use Python 3.12 and SymPy 1.14.0 (the tested versions). In an environment where SymPy is installed, run:

    python check_exact.py

It prints a JSON receipt. Success requires `status: pass` and all 16 checks true; the script also asserts these conditions. No floating-point optimization, external data, network access or field sampling is needed. CHECK_RESULT.json is the saved successful receipt; runtime can differ by machine.

requirements.txt records the dependency. MANIFEST.sha256 contains a hash for every other delivered file. PROVENANCE.md records source bindings, the standalone-proof edits and the preserved receipt-serialization correction.
