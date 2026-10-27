# Independent audit: finite-direction collapse of the actual cosine law

25 October 2026. This report concerns exact conditional-barycenter contractions, not midpoint substitutions, independently sampled coordinates, or an asserted gradient realization. All claims below are mathematical identities or necessary/sufficient criteria proved here. The construction of the actual first and second contractions, including the stated certificate for the second cubic moment, is input from the preceding nonlinear-chord audit. Full collapse and the full Morrey problem remain open.

## 1. Setup and scope

Let Z=(cos x, cos y, cos(x+y)), with independent uniform phases, and let μ be its law. Write

- q(u,v,w)=uv+uw+vw=zᵀJz, where J=(11ᵀ−I)/2;
- K={z: [[1,u,v],[u,1,w],[v,w,1]] is positive semidefinite};
- d1=(−1,2,2), d2=(2,−1,2), d3=(2,2,−1);
- e1,e2,e3 for the coordinate directions.

The source is supported on K⊂[−1,1]³, has E Z=0 and Cov(Z)=I/2, and its sole nonzero cubic monomial moment is E[uvw]=1/4. All six displayed directions are q-null. Also di·dj=9 δij.

For a nonzero direction d let P_d be orthogonal projection onto d⊥. The exact operation is

    C_d Z = E[Z | P_d Z].

It is a deterministic function of Z, preserves P_d Z pointwise, keeps the law in K, and preserves the expectation of every function affine on d-lines. In particular, it preserves the mean and E q=0.

Let ν1=C_d1 μ, ν2=C_e1 ν1. Define the strictly positive scalar variance losses s,r by

    Cov(ν1)=I/2−s d1d1ᵀ,
    Cov(ν2)=I/2−s d1d1ᵀ−r e1e1ᵀ.

Thus s is the conditional variance of (d1·Z)/9 in the first operation, whereas r is the conditional variance of u in the second. Their energy losses are 9s and r, respectively. The preceding audit gives 0<s<1/18 and r>0. We use as input the certified actual-law bound

    26/125 < m2 := E_ν2[uvw] < 47/200.

Every subsequent statement identifying ν1 or ν2 refers to these exact correlated measures.

## 2. Positive global theorem: every schedule has an L² limit

Choose any deterministic sequence of directions and realize every contraction on the original probability space:

    Z_(n+1)=E[Z_n | P_dn Z_n],   F_n=σ(Z_n).

Then F_(n+1)=σ(P_dn Z_n)⊂F_n. Indeed Z_(n+1) is a function of P_dn Z_n, and P_dn Z_(n+1)=P_dn Z_n. Induction and the tower property give

    Z_n=E[Z_0 | F_n].

Therefore the reverse-martingale convergence theorem yields

    Z_n → Z_∞=E[Z_0 | F_∞] almost surely and in L²,
    F_∞=intersection of the completed F_n.

This proves convergence of the iterates, not collapse to zero. The same conclusion holds for a fixed law-dependent choice of direction, since the chosen directions are deterministic once the initial law and selection rule are fixed. A direction selected differently for individual points is a different operation and is not covered by this formulation.

Set Δ_n=Z_n−Z_(n+1). These increments are orthogonal in L², including their cross-coordinate matrix moments. For n<m, Δ_m is F_(n+1)-measurable while E[Δ_n | F_(n+1)]=0. Consequently

    Cov(Z_0)−Cov(Z_∞)=sum_n E[Δ_n Δ_nᵀ],
    E|Z_0|²−E|Z_∞|²=sum_n E|Δ_n|².

For a step in direction d, Δ_n=a_n d and E[Δ_nΔ_nᵀ]=α_n ddᵀ with α_n=E[a_n²]≥0.

With zero mean, the following conditions are exactly equivalent for the specified schedule:

1. The laws converge to δ0.
2. Z_∞=0 almost surely.
3. E[Z_0 | F_∞]=0.
4. The scalar variance budget is exhausted: sum E|Δ_n|²=E|Z_0|².
5. The matrix covariance budget is exhausted: sum α_n d_n d_nᵀ=Cov(Z_0).

No independence assumption is used. Vanishing per-step losses holds for every schedule by summability and is not a collapse criterion. A fair or cyclic schedule is not, by itself, a collapse theorem.

The associated positive null stresses also have summable trace mass. Their total trace is half the dissipated energy, so their sum realizes μ−ν∞, not automatically μ−δ0.

## 3. Actual-law obstruction: only d1 and e1

Both directions have equal second and third components, so v−w is preserved pointwise at every step. For μ, E(v−w)²=1; hence the same identity holds for ν1, ν2, and all descendants using only {d1,e1}.

The elementary bound E|Z|²≥1/2 is valid, but the preserved null-quadratic moment gives the stronger exact bound

    |z|²−(3/4)(v−w)²−q(z)=(1/4)(2u−v−w)²≥0,
    E|Z|²≥3/4.

Thus no schedule using only these directions collapses the actual law, regardless of how many times each direction is revisited.

## 4. Actual-law obstruction: the coordinate axes

The polynomial uvw is affine separately in each coordinate, so every axis contraction preserves E[uvw]. In particular, all axis-only descendants of ν2 have cubic moment m2>26/125 and cannot converge to zero.

Since support stays in the cube,

    |uvw|≤(|u|²+|v|²+|w|²)/3.

For example, use |uvw|≤(|z|²/3)^(3/2) and |z|≤√3. Hence

    E|Z|²≥3m2>78/125

for every axis-only descendant of ν2. Starting directly from μ gives E|Z|²≥3/4. No assertion is made that this lower bound is attained by an actual axis schedule.

## 5. Actual-law obstruction: the three cyclic nonaxis directions

Define

    P_D(z)=(d1·z)(d2·z)(d3·z).

Because the di are mutually orthogonal, this polynomial is affine along each di-line. Its expansion is

    −4(u³+v³+w³)
    +6(u²v+u²w+uv²+uw²+v²w+vw²)+3uvw.

Thus E_μ P_D=3/4, and the first d1 contraction preserves this value. Every schedule using only {d1,d2,d3}, starting from ν1 or μ, retains the same nonzero invariant and cannot collapse.

The covariance feasibility test alone misses this obstruction, since

    sum_i di diᵀ=9I.

For an explicit residual-energy bound let a_i=(di·z)/3. Orthogonality gives |a|=|z|, and therefore

    |P_D(z)|=27|a1a2a3|≤3√3 |z|³≤9|z|² on K.

It follows that every such descendant satisfies E|Z|²≥1/12. This is a convenient certified lower bound, not a claim of optimality.

## 6. Stronger ν2 obstruction: cyclic directions plus the same e1

Suppose future directions are restricted to {d1,d2,d3,e1}. Use orthonormal coordinates a_i=(di·z)/3. The orthogonal map U with rows di/3 fixes the all-ones vector and negates its perpendicular plane, so q(Uz)=q(z).

The first d1 loss is diagonal in a-coordinates. The second e1 loss has direction

    b=Ue1=(−1,2,2)/3,

and therefore E_ν2[a2a3]=−4r/9. Future cyclic-direction losses are diagonal in these coordinates; future e1 losses only decrease this off-diagonal covariance. Hence

    E[a2a3]≤−4r/9.

Using

    |a|²+4a2a3−2q(a)=(a1−a2−a3)²≥0

gives the quantitative obstruction

    E|Z|²≥16r/9>0.

Equivalently, in this orthonormal basis no nonnegative combination of diagonal cyclic-direction covariance losses can cancel the nonzero off-diagonal pattern already contributed by e1. Merely adding e1 to the cyclic set does not repair collapse after the actual second contraction.

## 7. Five directions eliminate smooth invariants but still fail

Let D5={e1,e2,e3,d1,d2}.

### 7.1 Correct invariant classification

The five matrices ddᵀ span J⊥ in the six-dimensional symmetric-matrix space. Equivalently, a common C² direction-affine function has Hessian proportional to J. The proportionality cannot depend on z.

A direct C² proof avoids any extra smoothness assumption. The three axis conditions imply that, locally on boxes, f is a multiaffine polynomial:

    f=A+linear+a uv+b uw+c vw+h uvw.

The d1 condition forces h=0 and a+b=2c; the d2 condition forces a+c=2b. Hence a=b=c. On a connected open domain these local polynomial coefficients patch, yielding exactly

    f=A+linear+c q.

Thus D5 has no additional global C² direction-affine invariant. This algebraic statement is correct.

### 7.2 Nevertheless D5 cannot collapse ν1 or ν2

For every available direction, d_u d_v≤0: it is zero for axes and −2 for d1,d2. Consequently E[uv] is nondecreasing under the allowed contractions. Both ν1 and ν2 have E[uv]=2s>0.

Moreover,

    |z|²−(9/4)uv+(1/2)q(z)
      =(15/16)(u−v)²+(1/16)(u+v+4w)²≥0.

Every D5 descendant therefore satisfies

    E|Z|²≥(9/4)E[uv]≥(9/2)s>0.

In covariance-cone language, representing Cov(ν2) by nonnegative combinations of the five allowed dyads would force the future d1 coefficient to equal −s and the future d2 coefficient to equal zero. The axis decrement r changes no off-diagonal entries and cannot help.

In fact no D5 schedule collapses μ itself. If it ever has positive d1 or d2 activity, E[uv] becomes strictly positive forever. If all nonaxis steps have zero activity, the process is effectively axis-only and retains E[uvw]=1/4. This is an actual-law no-go result, not a generic fixed-point example.

The lesson is that linear spanning of J⊥ must not be confused with membership in the positive cone generated by the direction dyads.

## 8. Six-direction candidate: exact remaining covariance gate

Let D6={e1,e2,e3,d1,d2,d3}. This set removes the preceding D5 cone failure and the cyclic cubic invariant at the ambient-function level. It still does not automatically contain the covariance of ν2 in its positive dyad cone.

If a_i≥0 and b_i≥0 are future total coefficients for the axes and cyclic directions, respectively, covariance exhaustion from ν2 requires

    Cov(ν2)=sum_i a_i e_i e_iᵀ+sum_i b_i di diᵀ.

Solving all six entries gives a single parameter t:

    b1=t−s,  b2=b3=t,
    a1=1/2−r−9t,  a2=a3=1/2−9t.

Therefore this covariance representation exists if and only if

    s≤t≤(1/2−r)/9,
    equivalently r≤1/2−9s.

Since E_ν2|Z|²=3/2−9s−r, the same gate is E_ν2|Z|²≥1. Its truth for the actual ν2 requires a bound on the actual s,r; it is not implied merely by Cov(ν2)≥0. If this gate fails, D6 is ruled out already. If it holds, the coefficients are only algebraically feasible budgets, not proof that actual conditional variances will realize them.

For a schedule starting from μ, exhaustion requires the cumulative coefficients of the three di to be equal, and the cumulative coefficients of the three axes to be equal. The initial s and r must be included in those totals.

## 9. Exact fixed-point counterexample for D6, with the source cubic moments

There is an explicit finite atomic law supported on the ORIGINAL cosine surface, with exactly the same moments as μ through degree three, that is fixed by every direction in D6.

Choose angles α,β satisfying

    cosα=3/5, sinα=4/5,
    cosβ=5/13, sinβ=12/13.

Sample k,l independently and uniformly from {0,1,2,3}, set x=α+kπ/2 and y=β+lπ/2, and form Z=(cos x,cos y,cos(x+y)). Call this 16-atom law ρ.

Each coordinate of 65Z is an integer. Its u-values are {39,−52,−39,52}, its v-values are {25,−60,−25,60}, and its w-values are {−56,−33,33,56}. Each fixed k or fixed l sees all four distinct w-values, so every coordinate-axis projection is injective on the 16-point support.

The possible absolute nonzero u-differences, multiplied by 65, are

    {13,26,78,91,104},

while the v-differences are

    {35,50,85,120}.

These sets rule out Δv=−2Δu, Δu=−2Δv, and Δu=Δv, respectively. Hence no pair lies on a line parallel to d1, d2, or d3 either. Every D6 fiber contains at most one atom, so every conditional-barycenter operation is exactly the identity on ρ.

Uniform four-point phase quadrature annihilates every nonzero phase frequency of absolute value at most three. Every degree-at-most-three coordinate monomial has phase frequencies in that range. Therefore ρ has exactly the same moments as μ through degree three:

    E_ρ Z=0,  Cov_ρ(Z)=I/2,  E_ρ[uvw]=1/4,
    every other cubic monomial moment is zero.

In particular, E_ρ|Z|²=3/2, yet every D6 conditional variance vanishes. The supplied exact-rational verification checks all 120 unordered pairs for all six directions and every monomial through degree three.

This counterexample is relevant but LIMITED: it rules out a universal D6 dissipation/coercivity theorem based only on K support and the source moments through cubic order. It does not show that ρ is reachable from μ, ν1, or ν2 by the allowed operations, and it does not settle collapse of those actual laws.

The distinction cannot be removed by assuming only weak or W2 closeness to μ. In fact, let D be ANY fixed finite set of nonzero directions. For an N×N uniform phase grid with N≥4, generic phase shifts avoid all finitely many pair-direction coincidences. Here is a proof that the excluded analytic equations are genuinely nonidentical, including for directions with zero components.

For a distinct index pair (k,l),(k′,l′), the coordinate differences have Fourier supports respectively {±(1,0)}, {±(0,1)}, and {±(1,1)} in the phase offsets (α,β). The first is nonzero exactly when k≠k′ modulo N, the second when l≠l′, and the third when k+l≠k′+l′. At least two coordinate differences are nonzero. Their disjoint Fourier supports prevent them from being constant multiples. Thus the difference vector cannot lie identically in any one fixed line. At least one component of its cross product with any prescribed d is a nonzero analytic function. Its zero set has measure zero; a finite union over pairs and directions still has measure zero.

These generic-grid laws are therefore D-fixed, match all source monomials of degree less than N, and converge to μ in W2 as N→∞. Convergence holds for arbitrary choices of the offsets since the phase mesh tends uniformly to zero. In particular every N≥4 exactly matches all cubic moments. Thus even arbitrarily accurate moments and quadrature approximations cannot stand in for the actual fiber structure. These approximants are NOT asserted reachable by positive contractions of μ.

## 10. Conditional variance is not continuous in the required direction

For a unit direction d define

    δ_d(ν)=E_ν |Z−E_ν[Z | P_d Z]|².

It is zero exactly when ν is concentrated, up to null sets, on a measurable graph over d⊥. It is not lower semicontinuous under W2 convergence. For example, two atoms at (1,ε,0) and (−1,−ε,0) have injective e1 projection and δ_e1=0, whereas their limit at (±1,0,0) has δ_e1=1.

More generally, δ_d is the infimum over bounded continuous regression functions of the corresponding continuous squared-error integrals (with harmless moment control). Thus it is upper, not lower, semicontinuous. The exact quadrature example above shows this discontinuity directly at the actual cosine law: finite D6-fixed laws converge to μ, although μ has positive d1 activity.

Consequently, from Z_n→Z∞ in L² and δ_dn(ν_n)→0 one cannot infer, just by passing to a limit, that ν∞ is fixed for every infinitely recurring direction. A separate argument using additional reachable-law regularity would be needed. No such continuity or regularity theorem is asserted here.

## 11. What would actually establish collapse

For the actual reachable class, a valid positive theorem could take one of these forms:

- A proof that the terminal reverse-martingale barycenter E[Z0 | F∞] is zero.
- An exact proof that the cumulative actual conditional-variance matrix exhausts Cov(Z0).
- A quantitative reachable-class bound max_(d∈D) δ_d(ν)≥c E_ν|Z|², with c>0, together with a greedy schedule. This yields geometric energy decay.
- More weakly, for each ε>0, a positive lower bound on max δ_d over the actual reachable laws with energy at least ε. A greedy schedule then cannot retain positive limiting energy.
- For a specified cyclic schedule, the analogous positive lower bound on total energy lost across one complete direction cycle, restricted to its reachable laws.

The last three are substantive analytic gates, not consequences of moment matching, ambient invariant classification, fairness, or covariance-cone feasibility. The explicit common fixed laws show why a reachable-class hypothesis is essential.

## 12. Audit conclusion

Verified for the actual correlated laws:

1. Every exact schedule converges in L², but not necessarily to zero.
2. {d1,e1}, the coordinate axes after ν2, and the cyclic triple after ν1 all have rigorous noncollapse obstructions.
3. Adding only e1 to the cyclic triple still cannot collapse ν2.
4. D5 eliminates extra smooth direction-affine invariants but cannot collapse μ, ν1, or ν2.
5. D6 has an explicit necessary-and-sufficient covariance-cone gate for ν2, r≤1/2−9s. Passing it is not a convergence proof.
6. Even exact source moments through degree three and source-surface support admit a positive-energy common D6 fixed law. This is not claimed reachable from the actual cosine law.

What remains open is an actual-law convergence mechanism beyond these gates. No full null-stress completion, laminate representation, new gradient realization, or resolution of the full Morrey problem follows from this audit.

Reproducibility: run `python check_finite_directions.py`. Its exact symbolic and rational assertions produce `EXACT_CHECKS.json`.
