# Exceptional face: exact ROC boundary and a blocked polynomial heat route

The all-ROC-implies-QC question at s=1/3 remains unresolved. This tranche establishes a complete, finite exact admission operation for its lower quadratic boundary, and an explicit nontranslation boundary polynomial which is globally rank-one convex but not polyconvex. For that same admitted polynomial, **no polynomial closed differential-form correction can make the ordinary heat density pointwise nonnegative**. This last statement obstructs a proof method; it is not a quasiconvexity counterexample.

Write

    z=(x,y)=(a+d,c-b),  w=(u,v)=(a-d,c+b),
    r=|z|², t=|w|²,  ν(w)=(u²-v²,2uv).

Multiplying the original polynomial by three makes its leading part

    F=t²+2rt=3 F_(1/3).

Every globally ROC polynomial with this leading part has, after a unique argument translation and deletion of affine terms, the form

    P=F+zᵀMν(w)+Q(z,w),                         (1)

where M is an arbitrary real 2×2 matrix and Q an arbitrary quadratic subject to the sharp condition below. Thus the four extra cubic modes become one ordinary 2×2 matrix, rather than an unspecified acoustic kernel.

For unit vectors a,b in R², put n=(b₁²-b₂²,2b₁b₂), e=(-n₂,n₁). Then (1) is globally ROC **if and only if**

    8Q(a,b) ≥ |Mn|² + 2(aᵀMe)²                 (2)

for every a,b. The acoustic matrix has constant rank three on all nonzero rank-one directions here, so this closed formula has no omitted singular-chart limits. Substituting rational circle parametrizations turns (2) into nonnegativity of an explicit polynomial of bidegree at most (4,8). `classify.py` decides this exactly by univariate projection, real-root isolation and Sturm counts, including weak boundaries. It handles general Q, not merely an isotropic stabilization. The proof explains why checking the finitely many open projection cells also covers the algebraic boundary fibers.

A particularly simple exact consequence is

    Q=αr+βt is admissible iff α+β ≥ (2σ₁²+σ₂²)/8,

where σ₁≥σ₂ are the singular values of M. For Q=λ(r+t), the threshold is λ=(2σ₁²+σ₂²)/16.

Taking M=I gives the explicit admitted polynomial

    P₀=t²+2rt+x(u²-v²)+2yuv+(3/16)(r+t).        (3)

Its quadratic coefficient is exactly at the ROC boundary. In the original task normalization, p₀=P₀/3 has leading part F_(1/3), cubic [x(u²-v²)+2yuv]/3, and quadratic |A|²/8.

At A₀=(z,w)=((-1/4,0),(0,-1/4)), a null rank-one direction forces the only possible polyconvex support multiplier for δ=r-t=4det A to be 1/16. At the rational matrix B₀=(z,w)=((-11/20,0),(0,-1/8)), the corresponding actual support gap is -3/20480. This proves non-polyconvexity without restricting the convex minor lift.

I then attacked QC of (3) by extending the supplied compatible heat primitive. The cubic has a compact rotational symmetry z→exp(2iθ)z, w→exp(iθ)w. Averaging makes the polynomial primitive class finite and exhaustive modulo exact gauges. All leading acoustic null conditions and all sharp-boundary null conditions can be solved exactly. Two necessary PSD tests then require simultaneously

    j≥-3/4,    j≤-19/24.

Consequently no polynomial closed two-form correction of any degree gives a nonnegative pointwise heat density for P₀. Higher degree corrections cannot evade this: their leading PSD density would vanish on every plane-wave Hessian, which spans the whole Hessian space, so their density is zero. An angular or other nonpolynomial primitive, or a different compatible proof, remains possible. No actual gradient energy violation has been obtained.

The cubic kernel dimension eight, the general rank-one Schur elimination, QC of the homogeneous F, and the generic translation theorem were supplied capital. The additions here are the exceptional conformal normal form, the explicit cost (2), its finite exact full-Q classifier, the sharp singular-value boundary, and the admitted non-polyconvex fixture with the exhaustive polynomial-heat obstruction. The heat method and homogeneous QC provenance remain Bruno–Pasqualotto, arXiv:2608.06367v1, Appendix A, as captured in the packet; the generic nonexceptional theorem is not applied at its exception. Historical priority and external independent review are unestablished.

Read `PROOF.md` for derivations. Run:

    python3 classify.py
    python3 verify_fixture.py
    python3 heat_obstruction.py

These exact replays passed locally using installed SymPy 1.14.0. The classifier tests the sharp boundary, a coefficient below it, an interior coefficient, a degenerate anisotropic quadratic boundary, translation normalization, and a general rational M with quadratic cross terms (projection degree 56). The fixture receiver reconstructs the support failure independently. The heat receiver reconstructs its whole finite coefficient system and contradictory PSD requirements. Exploratory scripts retain the initial fixed-primary-primitive failure and the numerical search which suggested the final exact heat obstruction.

The remaining scientific frontier is QC of (3), and then the universal compatible inequality for all M and all Q admitted by (2). Neither non-polyconvexity nor failure of every polynomial heat correction settles that frontier.
