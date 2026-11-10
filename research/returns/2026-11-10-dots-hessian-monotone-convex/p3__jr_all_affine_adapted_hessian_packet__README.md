# All-r, all-affine adapted-Hessian support for J_r

This is a reproducible mathematical proof package for a restricted, infinite-dimensional part of the original quasiconvexity question. It is **not a proof of full quasiconvexity for arbitrary vector gradients**, and makes **no historical novelty claim**.

## Result and exact scope

For every r>0, put k=(2r+1)/3, ell=3k-1, n=k+1 and m=3k+1. For a real 2-by-2 matrix F, set u=|F_1|^2, v=|F_2|^2 and j=det F. The original density is

    J_k(F) = ell/(8n) * (ku-v+2j)^2 + ell*uv/4 + j^2.

Let L_k=diag(2k,-m) and

    Lambda_k(A) = 2 det A
        + ell/m * [k|A_1|^2-|A_2|^2+(3n/2)det A].

For every real upper-triangular A and every real symmetric H,

    J_k(A+L_k H) >= J_k(A)+DJ_k(A):L_k H
                                  +Lambda_k(A)det(L_k H),

strictly if H is nonzero. A constant LEFT rotation R in SO(2) making R^T A upper triangular extends the result to every affine A, with its adapted matrix L_{k,A}=R L_k. There is no right/source rotation.

Consequently, for every real scalar periodic W^{2,4} potential psi on any rectangular torus,

    average J_k(A+L_{k,A}D^2 psi) >= J_k(A).

The statement includes all amplitudes, frequencies and determinant signs. Compactly supported W^{2,4} scalar potentials are included by periodization. The inequality is strict for a nonzero Hessian on a set of positive measure. A strictly positive coercive remainder exists for each fixed k, and uniformly on compact subintervals of k>1/3, but no numerical or endpoint-uniform constant is claimed.

## Start here

1. Read `quartic_all_k_endpoint_matched_support_20261109/ALL_R_ADAPTED_HESSIAN_THEOREM.md` for the complete theorem and proof.
2. Read `quartic_all_r_hessian_independent_review_20261110/INDEPENDENT_SUBSTANTIVE_REVIEW.md` for the independent disposition and precise limitations.
3. Run `python reproduce.py` from this directory. It verifies the package manifest, then runs both exact checkers. Python 3.12 and SymPy 1.14.0 reproduce the recorded environment. No floating solver, network request, parameter grid or optimization is used.

The reviewed author replay passed 1,272 exact gates. A separately written original-density, manifest, coordinate-boundary and literal-tail supplement passed 74 checks. Their original stdout, stderr, exit codes and timing receipts are included. Runtime is machine-dependent; the recorded mathematical checking took about nine seconds total.

## Contents and status

- The complete governing proof and all exact polynomial, matrix and rational Sturm certificates.
- A literal-original-density reconstruction and certificate-coverage replay.
- The independent report and separately written closure checker.
- The diagonal invariant Gram dependency, exact constructor sources and execution receipts.
- Preserved failed coefficient allocations, serialization/launcher failures and corrected replay history. These are transparently superseded, not omitted or counted as successes.
- A SHA-256 package manifest, pinned requirements and a one-command replay wrapper.

The proof source is kept byte-for-byte as submitted for review. Its historical wording says review was pending and no ZIP had yet been prepared. The independent report and this package record the later successful review; they do not retroactively edit the frozen source. The all-r extension supersedes the earlier r=k=1 adapted-class restriction, but does not settle the additional transverse component of a general compatible vector gradient.

## Remaining limitation

The admitted perturbation is an adapted **scalar Hessian**, not an arbitrary 2-by-2 compatible gradient. Variable rotations or variable reference means cannot be inserted without paying their force and compatibility terms. The result is not a physical validation, an algorithmic speed claim, or a novelty certification.
