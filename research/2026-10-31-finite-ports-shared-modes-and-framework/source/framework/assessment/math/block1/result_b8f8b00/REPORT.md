# Sharp compatible QC for rank-one exceptional modes

The full exceptional face remains unresolved. This continuation constructs a positive compatible certificate which **reaches the exact ROC threshold for every rank-one nontranslation matrix M with an isotropic lower quadratic**. It also gives an explicit quasiconvexity region for all M and general Q, and improves that region for the checkpoint's conformal cubic.

Use the checkpoint coordinates and normalization

    F=t²+2rt,  C=zᵀMν(w),  P=F+C+Q.

For Q=αr+βt, the supplied exact ROC threshold is

    α+β ≥ (2σ₁(M)²+σ₂(M)²)/8.

The new compatible construction proves QC whenever

    α+β ≥ (σ₁(M)²+σ₂(M)²)/4.

These coincide when rank M≤1. Thus the entire isotropic-quadratic rank-one exceptional subfamily, including its sharp weak boundary and determinant lineality, is resolved positively. This includes genuine nontranslation cubics; it is not the generic translation theorem applied at its exception.

For arbitrary Q the sufficient condition is

    Q(a,b) ≥ ||M||_F²/4 for every |a|=|b|=1.

It follows by adding a QC rank-one convex quadratic to the constructed member. This is a sufficient region, not a replacement for the checkpoint's sharper full ROC admission criterion.

The hardest step is an exact three-complex-square identity for the corrected compatible heat density. After actual output/domain rotations, write C=a Re(bar(z)w²)+b Re(zw²). With complex Hessian components A,B,C, that identity is

    B_P = |zB+2wA+b bar(C)|²
          +2|bar(z)A+bar(w)B+w bar(C)|²
          +|z bar(B)+2bar(w)B+aC|²

at quadratic coefficient λ=(a²+b²)/4. The correction is the pullback of an explicitly given polynomial exact two-form. Stokes and actual componentwise heat flow prove the QC inequality for every background and every compatible gradient test. No matrix distribution or correction-selector oracle is used.

A tunable positive-definite 3×3 Gram matrix improves the bound. For the conformal M=I cubic it proves QC at

    λ_H=(3+sqrt(3))/24 ≈ 0.197168783648,

while ROC begins at λ=3/16=0.1875. The original boundary P₀ remains unresolved. The one-parameter bound for all M is explicit in PROOF.md; no optimality among all possible QC proofs is claimed.

`verify_certificate.py` reconstructs and checks the universal identity with symbolic cubic coefficients, the rank-one specialization, the tunable leading and cubic identities, and the radical improved certificate. All exact checks pass using installed SymPy. Run:

    python3 verify_certificate.py

`PROOF.md` contains the derivation, the compatibility argument, source credits, and exact limitations. `fourier_search.py` preserves a failed search with actual trigonometric potentials: no negative energy or integrated-heat witness was found. A coarse supporting-minor probe was also inconclusive; it is not used as a theorem.

The new positive result does not settle arbitrary admitted Q even for rank-one M, or the full-rank sharp boundary. Homogeneous QC and the heat/Stokes mechanism retain the Bruno--Pasqualotto Appendix A credit from the frozen packet. The checkpoint's full ROC classifier and its boundary polynomial heat obstruction are respected rather than repeated.
