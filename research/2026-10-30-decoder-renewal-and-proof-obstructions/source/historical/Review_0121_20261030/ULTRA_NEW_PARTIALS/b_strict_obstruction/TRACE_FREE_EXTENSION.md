# Governing strengthening: the outer operator needs no trace condition

This supplements the complete proof in `PROOF.md`. Its larger outer cone
has its OWN unevaluated positive distance. No numerical radius from the
main proof is silently reused.

Let H0 be the set of homogeneous quartic polynomials F∈K for which there
exist ANY real constant matrices L11,L12,L22 satisfying

    sum ||Lij||_F²=1,

and a closed quadratic-coefficient 2-form Omega such that

    C_F,L(A)+W(Omega(A))>=0 for every A.                 (E1)

There is no mean-convergence, trace, symmetry or parabolicity assumption
on L in this OUTER class. The separate requirement F∈K is retained.
We do not claim that H0 consists of valid QC/heat proofs. In particular
an arbitrary unstable flow does not automatically prove QC.

The nonzero normalization is essential: admitting L=0 and Omega=0 would
trivially admit every F and would be no proof operation at all.

Every actual origin-regular mean-converging heat part belongs to H0 by
the Taylor reduction and Lyapunov argument of PROOF Sections1/4. H0 is
a closed, possibly nonconvex cone by exactly the coefficient bound (8)
and compact normalized L sphere; the removed trace condition was not
needed for witness boundedness or closure. H0⊂K holds by its definition.

## Endpoint exclusion without a trace hypothesis

Suppose F*∈H0. Average (E1) over the same compact symmetries of F*.
The averaged symbol is

    ell0 |xi|² I+2nu xi1xi2 J,

now with ell0 an arbitrary REAL number. The exact determinant (11) in
PROOF has t² coefficient −256nu², so nu=0 regardless of ell0's sign.
At A=E11 and every nonzero xi, the acoustic B in (13) is positive
definite. The averaged acoustic inequality is therefore

    ell0 |xi|² B>=0,

which itself forces ell0>=0. No trace hypothesis has been used.

The two remaining cases are exactly those already proved:

* ell0>0 produces the impossible ordinary-heat closed quadratic
  completion of F*;
* ell0=0 makes the averaged positive density a pure wedge and hence
  zero. Positivity and continuity force the ORIGINAL density zero.
  Its rotation-orbit acoustic identities force L(xi)=0 for every xi,
  contradicting normalization.

Thus F*∉H0. In particular F* has no origin-C² exact-form completion for
ANY nonzero real constant second-order operator, whether or not it
converges. This remains a restricted-regularity statement: the full
angular/rational class is not excluded.

## Strict/open combined obstruction

Let

    S0=P+conic_hull(H0).

By the explicit positive ROC base, closed H0 and closed P have compact
bases. The same35-dimensional Caratheodory argument proves S0 a closed
convex cone. Endpoint ROC extremality and non-PC give F*∉S0. Consequently

    delta0=dist_inf(F*,S0)>0.                            (E2)

This is a NEW existence constant; it is not evaluated. For every
0<epsilon<delta0/4, F*+epsilon T² is outside S0 and obeys the strict
quartic LH bound4epsilon |A|²|R|². Its coefficient ball of radius

    r<min(delta0/4,epsilon/840)

is disjoint from S0 and has LH bound2epsilon |A|²|R|².

This excludes finite decompositions into PC quartic polynomials and
ROC quartic polynomials possessing origin-regular exact-form completions,
even if the latter are granted ANY nonzero constant flow. It therefore
includes the entire intended mean-converging proof class with arbitrarily
many different flows. It does not assert closure/convexity of that actual
flow union, nor impose a numerical source supplier for delta0.
