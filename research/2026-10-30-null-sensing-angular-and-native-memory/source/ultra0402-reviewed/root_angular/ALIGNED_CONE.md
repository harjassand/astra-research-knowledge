# Extending the positive seed while reusing the strongest acquired predecessor

30 October 2026. Root construction. This theorem uses the qualified
angular seed F* from `../b_angular_repair/PROOF.md`; until that seed's
whole mathematical intake is complete, the QC conclusions here are
conditional on it. The decompositions and convex endpoint are exact.
The prior-reuse section gives a stronger coverage envelope than the
simple endpoint chord below.

For real 2×2 matrices use T=|A|², X=a²+c²−b²−d²,
Y=2(ab+cd), Z=2det A, and

    F_(beta,r)=X²+Y²+2 beta XZ+r Z²
              =T²+4 beta qX+4(r−1)q².

Let b=|beta|<=1. Then EVERY

    r >= 1/2+(7/2)b                                      (1)

is quasiconvex. For b<1 it obeys the quantitative inequality

    integral_Omega [F_(beta,r)(A+Dphi)−F_(beta,r)(A)]
       >= (1−b)/6 integral_Omega |Dphi|⁴.                 (2)

The modulus in (2) multiplies |Dphi|⁴ ONLY; a weighted
|A|²|Dphi|² term is not asserted on the boundary in (1).

## The convex endpoint and the exact identity

Set

    C(A)=T²−2q²=Tr[(A^T A)²].

Writing S=A^T A and Delta=A^T H+H^T A gives

    D²C(A)[H,H]=2 Tr(Delta²)+4 Tr(S H^T H) >= 0.

Both terms are nonnegative: Delta is symmetric, and S,H^TH are positive
semidefinite. This proves ordinary convexity without a norm oracle or
a sampled Hessian. Also C(H)>=|H|⁴/2 by its two nonnegative eigenvalues.

Let F*_+ be the angular seed T²+12q²+4qX, and
F*_−=T²+12q²−4qX its orthogonal column-reflection transport. QC is
preserved by that invertible domain change. With either sign for beta=0,
the literal identity is

    F_(beta,r)
       = b F*_(sign beta)+(1−b)C
          +4[r−(1/2+7b/2)]q².                           (3)

Each coefficient in (3) is nonnegative under (1). The first summand is
QC by the seed, C is convex, and q² is polyconvex. In particular,
integral q(A+Dphi)=|Omega|q(A) and scalar Jensen prove the required
q² inequality directly. The determinant term need not dissipate the
ordinary heat flow, and (3) does not claim a single heat correction
for all its summands.

## A useful general convex-quartic Bregman inequality

For ANY convex homogeneous quartic C that is positive off zero,

    C(A+H)−C(A)−DC(A):H >= C(H)/3.                       (4)

For H!=0 write C(A+tH)=c0+c1 t+c2 t²+c3 t³+c4 t⁴,
where c4=C(H)>0. Convexity on the whole line requires

    2c2+6c3 t+12c4 t²>=0 for all real t,
    c2>=3c3²/(8c4).

Hence

    c2+c3+c4 >= (3/(8c4))(c3+4c4/3)²+c4/3.

This proves (4); H=0 is equality. Apply it to the explicit C above,
integrate, and use integral DC(A):Dphi=0. Equation (3) then gives (2).
This is an analytic all-parameter result, not a parameter grid.

## Reuse of the already established anisotropic seed

The current programme ALREADY proved QC for

    Q=F_(99/100,88/25)
      =T²+(252/25)q²+(99/25)qX,
    integral[Q(A+Dphi)−Q(A)]>=(1/900000)integral|Dphi|⁴.

The governing construction is
`../../sol25_capability_frontiers_20261030/a_independent/heat_form/PROOF.md`;
its full substantive acceptance is in
`../../sol25_capability_frontiers_20261030/t_angular_challenge/REVIEW.md`.
Its original frozen proof header was not rewritten to assert acceptance;
the completed independent review governs. Root read the actual statement
and review, rather than inferring that every previously studied parameter
below r=4 was still open. The negative-beta reflection has the same bound.

Taking the convex hull in (b,r) of C=(0,1/2), Q=(99/100,88/25), and
the NEW seed F*=(1,4) gives the stronger sufficient threshold

    U(b)=1/2+(302/99)b,                  0<=b<=99/100,
    U(b)=48b−44,                        99/100<=b<=1.     (5)

EVERY |beta|<=1, r>=U(|beta|) is therefore QC. Below the middle vertex,
put lambda=100b/99. The exact identity is

    F_(beta,U(b))=lambda Q_(sign beta)+(1−lambda)C.

Above it, put lambda=100(1−b). Then

    F_(beta,U(b))=lambda Q_(sign beta)
                             +(100b−99)F*_(sign beta).

The weights are nonnegative and sum to1. For any r>=U(b), add the
polyconvex term 4[r−U(b)]q². No new profile, optimizer or parameter-case
experiment is needed. The explicit L4-only strong-QC modulus is at least

    lambda/900000+(1−lambda)/6,          0<=b<=99/100,
    (1−b)/9000,                         99/100<=b<1.     (6)

The formulas agree at b=99/100. No positive endpoint modulus is claimed
at b=1. These bounds need not be optimal, and alternative decompositions
such as (3) remain usable whenever their hypotheses hold.

The lower branch of (5) is prior reuse and ordinary convex composition;
it is not presented as a newly acquired QC seed. The new F* theorem adds
the high-beta segment through the extreme endpoint. This is the precise
added capability beyond the previously accepted strict seed.

## Consequence and boundaries

Using only the norm-four convex endpoint would give the smaller region
r>=1+3b. Using only B's first nonnegative-norm-four/PC export would give
r>=4. The ordinary convex Schatten-four endpoint in (3) gives the
strictly larger region (1), reaching the known ROC boundary at b=0
and at b=1. This is a positive extension below r=4; it does not classify
the curved rank-one-convex boundary between those endpoints.

The earlier explicit family r=4,
beta_m=(m²−1)/(m²+1), m>=197, is included. Its stronger bound using the
direct norm-four decomposition, 2/[3(m²+1)] times integral|Dphi|⁴,
remains admitted; (2) is not presented as its optimal modulus.

The exact ROC threshold from the accepted `sol9_frontier_20261028/hopf`
calculation is

    R(b)=1/2+2b²,                      0<=b<=1/2,
    R(b)=4−2 sqrt(3(1−b²)),             1/2<=b<=1.

The region R(b)<=r<U(b) is not classified by these decompositions and is
not silently promoted to QC. Other previously proved pieces remain
available. No generic Morrey result, physical material, measured speed
advantage or historical-priority claim is made. Convexity, determinant
Jensen and cone transport are ordinary methods explicitly credited by
their use here; the nontrivial input is the exact anisotropic seed.
