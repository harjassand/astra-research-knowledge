# A moving-fugacity dual repairs the finite-atlas obstruction

29 October 2026. Internal candidate proof, not independently reviewed or novelty-cleared. This is a two-unbounded-coordinate construction for one explicit non-complex-balanced weakly reversible network, not the general chemical recurrence conjecture. The parent independently proposed the simplified one-transition envelope used here.

## 1. Same exact network

The complexes are y0=(0,72), y1=(3,60), y2=(5,36), y3=(6,0), in a directed cycle with rates k=(2,1,1,1). See `FINITE_POISSON_ATLAS_OBSTRUCTION.md`: no finite minimum of rationally corrected fixed product-Poisson bases can provide an eventual global dual supersolution for this network.

Write populations as (a,b). Let g0=log(2)/14. Define a C1 nonincreasing function g on R by

    g(r)=g0,                         r<=20,
    g(r)=g0(1-3s^2+2s^3),           20<r<30, s=(r-20)/10,
    g(r)=0,                          r>=30.

Thus 0<=g<=g0 and its derivative is bounded. Define

    r(a,b)=log(a+2)/log(b+2),
    F(a,b)=b g(r(a,b)),
    mu(a,b)=2^a exp(F(a,b))/(a! b!).

This measure is strictly positive. It is summable, and sum mu(a,b) q(a,b)<infinity, because it is bounded above by 2^a exp(g0 b)/(a!b!), while every reaction rate is a fixed polynomial. The extra logarithmic dependence is essential: it is not a rational correction of one fixed Poisson base or a finite minimum of such bases.

## 2. Exact adjoint identity

For an incoming edge y_i -> y_j, put z=y_i-y_j. On states x=(a,b) with x>=y_j, factorial cancellation gives the exact contribution

    k_i 2^{z_A} exp[F(x+z)-F(x)] (x)_{y_j}.

If x is not above y_j, the incoming contribution vanishes. Hence

    L*mu(x)/mu(x)=sum_j D_j(x)(x)_{y_j},
    D_j(x)=k_{j-1}2^{y_{j-1,A}-y_{j,A}}
             exp[F(x+y_{j-1}-y_j)-F(x)]-k_j.        (1)

Expressions at invalid incoming points can be omitted because their falling factorial is zero. This formula has no diffusion approximation.

If g is constant equal to t throughout the relevant fixed shifts, the four coefficients are exactly

    d0(t)=64 exp(-72t)-2,
    d1(t)=exp(12t)/4-1,
    d2(t)=exp(24t)/4-1,
    d3(t)=exp(36t)/2-1.                            (2)

At t=g0 they are

    2^(6/7)-2 <0,
    2^(-8/7)-1 <0,
    2^(-2/7)-1 <0,
    2^(11/7)-1 >0.                                (3)

At t=0 they are (62,-3/4,-3/4,-1/2).

## 3. Uniform fixed-shift control in the transition region

Consider 19<=r(a,b)<=31 and b->infinity. Then a is between fixed-factor versions of b^19 and b^31. Every reaction shift is bounded by 6 in a and 72 in b. For sufficiently large b, the entire segment to each shifted point lies in a slightly wider fixed r-strip with a much larger than b.

Where derivatives are taken,

    partial_a F = b g'(r)/[(a+2)log(b+2)],
    partial_b F = g(r)
                  -[b/(b+2)] r g'(r)/log(b+2).

Bounded g' and bounded r on the strip give, uniformly over all reaction shifts z,

    F(x+z)-F(x)=z_B g(r(x))+O(1/log b).             (4)

The estimate also crosses the g-plateau endpoints, since g is C1 with a global bounded derivative. In particular D_j(x)=d_j(g(r(x)))+O(1/log b) uniformly. The crucial coefficient has a fixed negative margin throughout:

    d2(g(r)) <= 2^(-2/7)-1 =: -m0 <0.             (5)

## 4. Three regions prove eventual negativity

### Low region: r<=19

Outside a finite set, b is large and every relevant shifted point has r<20, so g is exactly g0 there. This uses the fixed margin between 19 and 20 and the fixed-shift logarithm estimate; bounded b together with r<=19 gives only finitely many a.

By (3), only the y3 monomial can contribute positively. If it is nonzero, its ratio to the negative y2 monomial is

    (a)_6 / [(a)_5 (b)_36] = (a-5)/(b)_36
      <= O(b^(-17)),

because a+2<=(b+2)^19. Thus the negative y2 term absorbs it for all sufficiently large b. Other nonzero terms are negative. This proves L*mu<0 throughout the low region outside a finite set.

### Middle region: 19<=r<=31

Here b->infinity outside finite sets and y2 is uniquely dominant. Uniformly in the region, the ratios of the other falling-factorial monomials to (a)_5(b)_36 satisfy

    (b)_72 / [(a)_5(b)_36] = O(b^(-59)),
    (a)_3(b)_60 / [(a)_5(b)_36] = O(b^(-14)),
    (a)_6 / [(a)_5(b)_36] = O(b^(-5)).

All D_j remain bounded by (4), and D2<=-m0/2 for sufficiently large b. Therefore (1) is strictly negative uniformly in this region.

### High region: r>=31

Outside a finite set, every relevant shifted point has r>30, so g is exactly zero. For b large the unit margin in logarithmic slope handles all bounded shifts. For bounded b, a->infinity eventually puts every shifted point above 30; the excluded points are still finite.

Only the y0 term has a positive coefficient. It is absorbed by the negative y3 term because a+2>=(b+2)^31:

    (b)_72/(a)_6 ->0

uniformly when b->infinity in this region; with bounded b, it vanishes relative to a^6 as a->infinity. If b<72 the positive term is already zero. Thus the adjoint is strictly negative outside a finite set in the high region as well.

Combining the regions proves

    L*mu(x)<0 outside a finite set K.               (6)

The argument gives effective finite cutoffs from the explicit g derivative bound, fixed shifts, coefficient margins and elementary falling-factorial estimates. No small, sharp or polynomial-bit cutoff is claimed. Enormous cutoff constants cannot be treated as an efficient algorithm or practical prediction horizon.

## 5. Recurrence consequence without assuming mixing

Let q(x) be the total nontrivial exit rate and nu(x)=mu(x)q(x). This is finite. Absorbing states are confined to a finite box (a<6,b<72). On nonabsorbing states the embedded chain P obeys

    nu P - nu = L*mu.

Take K large enough to contain all possible positive defects and all absorbing states. On C=K^c,

    nu_C >= nu_C P_CC + nu_K P_KC.

Iterating and summing bounds the expected number of embedded steps in excursions from K by the finite total mass of nu_C. Every closed irreducible class must meet K: a class disjoint from K would have a finite positive nu with strictly negative total invariance defect, impossible after summing nu P-nu over that class. The finite-set return criterion then gives positive recurrence of each embedded class. Weak reversibility ensures reachable communication classes are closed, because every enabled reaction has an enabled finite return path at fixed residual population.

An irreducible recurrent embedded chain returns infinitely often to a fixed state with finite exit rate, so the holding times there preclude explosion. Also every enabled mass-action reaction has rate at least min k_i=1, so mean holding times are at most 1; finite expected embedded return lengths imply finite expected continuous-time return durations. Hence every nonabsorbing communicating class is positive recurrent and the chain is nonexplosive. Absorbing singleton classes are trivial.

No invariant density, mixing time, spectral gap, finite-state truncation, or uniform adjacent-fiber overlap was assumed.

## What does not follow

This construction repairs one exact obstruction in two unbounded coordinates. It does not supply an atlas or moving-fugacity potential for arbitrary weakly reversible networks. Exposed faces containing neutral closed reaction linkages can require growing-shell internal dynamics; this proof avoids that case because one monomial has a uniform negative coefficient in the transition strip. External correctness, historical novelty, and relevance beyond this explicit family remain to be independently assessed.
