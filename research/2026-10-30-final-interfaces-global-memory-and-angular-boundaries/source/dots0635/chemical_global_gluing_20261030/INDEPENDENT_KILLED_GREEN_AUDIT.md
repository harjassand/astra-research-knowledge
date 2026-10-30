# Independent audit: killed-shell neighboring Green comparison

Reviewer: finite_phase_drift_challenge, 2026-10-30. Internal mathematical review; not external novelty certification.

## Verdict

Both neighboring-shell comparisons pass. The Schur complements, matching supports after one new killing insertion, monotone rate ratios, positive forest bounds, and Sherman–Morrison estimate are valid. The proof obtains genuine entrywise estimates rather than converting a norm bound into an unjustified Harnack bound. It remains specific to this birth–death shell and does not settle connector feedback or recurrence.

## 1. Killed chain and coarse norm

For N≥4, all adjacent birth/death edges on 0,...,N are enabled. States a≥3 have immediate killing; a=0,1,2 can reach a=3 by at most three increasing steps. Each prescribed nonzero rate is at least a positive constant, total rates are at most C N³, and the complete path including killing has at most four steps. Thus the block absorption probability is at least c N^−12. The standard repeated-block argument and a fixed upper bound on mean active holding times give ||G_N||_infinity≤C N^12. This uses neither mixing nor stationary-shell estimates.

## 2. Adding C: exact Schur complement

At the new top endpoint a=N+1 of shell N+1, death=(N+1)_3 and killing=(N+1)_3. Its only internal neighbor is a=N. The Schur complement on old indices removes the transition to this endpoint and returns half its rate as a diagonal correction, leaving extra killing b_(N+1)(N)/2=7N(N−1)/2. Internal transitions among old states retain their shell-(N+1) rates. In particular the removed endpoint transition is not retained as an extra internal birth at old a=N.

For old a<N the birth ratio is ((c+1)/c) times P_(N+1)(a)/P_N(a), c=N−a. At a≥1 the death ratio is Q_(N+1)(a−1)/Q_N(a−1). All these ratios are at least one, and their quadratic ratios are at most 1+C/N by the prior bounds. At old N, the killing ratio is exactly 1+7/[2(N−2)]; all other killing rates and all killing zeros are unchanged.

A denominator forest uses one outgoing transition or cemetery edge per state; a Green-cofactor forest uses at most one. Because supports agree, each weight ratio is between one and a product of per-vertex upper bounds. The potentially nonuniform birth factors multiply to

    product_(c=1)^N (c+1)/c = N+1,

and all remaining factors multiply to a fixed constant via (1+C/N)^(N+1). Both numerator and denominator ratios therefore lie in [1,C(N+1)]. Their quotient lies in [1/(C(N+1)),C(N+1)]. The upper-left Green block of the original chain is exactly the inverse Schur complement, so this is the claimed comparison for G_(N+1)(a,b).

## 3. Adding A: precise shifted rate checks

The eliminated a=0 endpoint of shell N+1 has positive birth and no killing. Its only neighbor is a=1. The Schur complement returns its entire excursion rate to the diagonal at a=1, canceling that state's death-to-zero loss. Thus shifted old index zero has no death, matching shell N, and there is no extra killing from this elimination.

Let old a+c=N. For births at a<N, the shifted quadratic factor minus the old one is

    (c−1)+14a ≥0.

For deaths at a≥1, write the old quadratic factor as

    12c(c−1)+(a−1)c+(a−1)(a−2).

The shifted factor exceeds it by c+2(a−1)≥0, while its leading linear prefactor changes from a to a+1. The same lower bound (N−2)²/2 on these quadratics gives relative factor 1+O(1/N), uniformly over relevant indices. Existing killing ratios at a≥3 are exactly (a+1)/(a−2). The shifted kill at a=2 is 6; old a=0,1 remain unkilled. Adding rate 6 at old a=2 therefore makes the supports exactly equal.

After this insertion, all rate ratios are at least one. The nonconstant per-vertex factors satisfy

    product_(a=1)^N (a+1)/a = N+1,
    product_(a=3)^N (a+1)/(a−2) = (N+1)N(N−1)/6.

Multiplying both families is a valid coarse bound even though each forest vertex chooses at most one outgoing edge. Quadratic ratios contribute only a fixed constant. Hence every forest weight ratio is in [1,CN^4], and the shifted Green kernel compared with the newly killed old kernel has entrywise ratios in [1/(CN^4),CN^4].

## 4. New killing and Green inequality

For the original killed chain and i=2,

    G(a,i)=P_a(T_i<kill)G(i,i),
    G(a,b)≥P_a(T_i<kill)G(i,b),

where T_i includes time zero when a=i. Therefore G(a,i)G(i,b)≤G(a,b)G(i,i). The inequality includes endpoints and repeated indices.

Adding killing theta at i replaces G by

    G'=G−theta G_:i G_i:/(1+theta G_ii).

The entrywise bounds are G/(1+theta G_ii)≤G'≤G. Setting theta=6 and using G_ii≤C N^12 proves the claimed polynomial loss. Combined with the previous forest estimate, one may take the explicit coarse exponents

    c N^−16 ≤ G_(N+1)(a+1,b+1)/G_N(a,b) ≤ C N^4,

and hence the symmetric statement with D=16 after adjusting constants. No claim that these exponents are sharp is warranted.

## 5. Why positivity is legitimate here

The relevant positive expansions are directed spanning-forest formulas for a killed generator expressed in its transition and killing rates. The determinant is the sum over cemetery-rooted trees/forests; an inverse-entry numerator uses two-root forests with the appropriate source in the destination's tree. All weights have positive coefficients and at most one outgoing choice per vertex. This is stronger than mere positivity of the final determinant, and is valid for these exact killed Markov generators after the Schur operations. It would not automatically hold for an arbitrary tilted Metzler matrix expressed in its original reaction parameters.

## Scope retained

The proof compares prescribed neighboring shell entries without requiring a uniform spectral gap. The original inverse-norm bound is used only to control the single new killing perturbation. Full connector forcing, radial/B-envelope design, and multidimensional conservative faces remain outside this result.

Reviewed source SHA-256: `5359c5d9f4ca41fe4e81cc716b72c31819fc14fc2b6460e5b51d3afce180a5f3`.
