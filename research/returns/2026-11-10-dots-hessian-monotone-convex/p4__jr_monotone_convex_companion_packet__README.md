# J_r: a strictly monotone constitutive map and a globally convex quartic companion

This standalone mathematical package proves two reusable statements for every r>0. It does **not** prove full quasiconvexity of J_r and makes **no historical novelty claim**.

Put k=(2r+1)/3, ell=3k-1, n=k+1 and m=3k+1. For a real 2-by-2 matrix F, let u and v be its squared column norms, j=det F, and H=ku-v+2j. The original density and selector coefficient are

    J_k(F)=j^2+ell[H^2/(8n)+uv/4],
    lambda(F)=[3ell(ku-v)+24k j]/(2m).

Define R=(J_k-j^2)/ell, L=(lambda-2j)/ell and

    T(F)=DR(F)-L(F)cof F,
    Psi(F)=J_k(F)-lambda(F)det(F)/2.

## Proved scope

- T is globally strictly monotone on all real 2-by-2 matrices, with an exact finite sum-of-squares secant identity and the quartic remainder Psi(F1-F0)/ell.
- T is generally **not a gradient map**. Its exterior curvature is exactly -dL wedge dj.
- Psi is a globally convex quartic. The package gives an explicit strictly positive Hessian bound away from the zero matrix, using actual Hopf-coordinate identities.
- Its finite convex Bregman satisfies B_Psi(F+E;F)>=Psi(E)/3, sharply at F=-E/3.
- The statements are pointwise and integrate for L4 matrix fields. Their use in a spatial gradient problem does not remove that problem's compatibility or boundary terms.

The unresolved original energy is J_k=Psi+lambda j/2. The coefficient lambda depends on F, so the second term is not a null Lagrangian and cannot be discarded. No additional reserve may be counted twice.

## Read and reproduce

1. `sources/ALL_R_MONOTONE_CONSTITUTIVE_REMAINDER.md`: complete constitutive definitions, differential and finite identities, strictness, and the k=1 illustration.
2. `sources/CONVEX_RADIAL_POTENTIAL_AND_SIGNED_MINOR.md`: complete convexity proof, actual feature geometry, explicit Hessian bound, and remaining limitation.
3. `dependencies/ALL_R_FOUR_BILINEAR_SQUARES.md`: full selector definitions and analytic factorization used by both statements.
4. `independent_review/INDEPENDENT_SUBSTANTIVE_REVIEW.md`: source-bound independent reconstruction, strictness/function-space analysis, and reusable consequences.
5. Run `python reproduce.py` with Python 3.12 and SymPy 1.14.0. The wrapper verifies every packaged SHA-256 hash, then runs the separately written original-density checker. It installs nothing and makes no network requests.

The recorded independent check passed 19 exact polynomial identities in about 2.63 seconds of scientific execution, using no numerical samples or optimization. Timing depends on the machine. The Hopf strictness estimate was independently reconstructed analytically and is not mislabeled as an executed check. Original receipts, source snapshots and the exact checker are included.

## What is not claimed

This package is independent of the earlier adapted-Hessian archive. It is neither a proof of full J_r quasiconvexity, a historical-priority assessment, a physical validation, nor a solver-performance claim. It provides a monotone nonconservative constitutive map and a genuine convex companion while retaining the original signed weighted-minor problem.
