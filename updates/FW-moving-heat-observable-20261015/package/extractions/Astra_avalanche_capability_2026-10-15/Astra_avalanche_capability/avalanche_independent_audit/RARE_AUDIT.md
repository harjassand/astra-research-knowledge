# Rare-event bound audit

Verdict: the proposed physical-lifetime upper bound and its positive boundary DP are valid for the stated thermal equal-load-sharing model, conditional on the common-clock construction. Both compared numbers are upper bounds; neither is the actual physical CDF.

## Physical inequality and exact boundary

Let T_m be the internal time when the decreasing survivor count first falls below m. Since psi is increasing, the layer-cake identity is tau=sum_m (psi(m)-psi(m-1))*T_m. For j≤m, T_j≥T_m; retaining these terms gives tau≥psi(m)*T_m. Therefore P(tau≤t)≤P(K(t/psi(m))<m). The exponent sign in u=t*exp(F/(m*T)) is correct.

The boundary event is that every prefix count c satisfies c<m OR c*s_j≤F. Equivalently, for positive s_j its upper allowed count is max(m-1,floor(F/s_j)). The direct rational multiplication in the code also handles zero strengths without division. Equality is correctly included on the failure side. Checking absent-fiber positions cannot add a spurious exclusion because a count was attained at an earlier, stronger present position. The positive backward recurrence uses exp(-lambda*u) and -expm1(-lambda*u), avoiding catastrophic subtraction of the final probability from one.

The interval implementation correctly constructs exact rational strengths, F, T, and t before exponentiation. Its arithmetic depends on mpmath.iv's enclosure contract; it is not a formal verification of that library.

## Independent integer DP check

I recomputed each survivor probability at 90 interval decimal digits, converted its endpoints outward to multiples of 2^-384, and ran a separately written integer-only DP with directed division at every step. The boundary event is decreasing in each survivor probability, so lower probabilities plus upward DP rounding give an upper bound; upper probabilities plus downward rounding give a lower bound. This does not duplicate the producer's floating interval DP.

At n=400, m=166, F=70, T=3/20, t=1/10:
- Upper: 6.6723343061480519419386686845381717985738151459420993861512995397084795e-54.
- Integer bracket width: approximately 4.23836e-114.
- The bracket overlaps the producer's 70-digit interval.

At n=100, m=43, F=35/2, T=3/20, t=1/10:
- Upper: approximately 3.53225836221337906700176609934509419489663335420144e-14.
- The independent bracket also overlaps the producer's interval.

Exact rational upper numerators and denominators are saved in rare_result.json. Their decimal displays above are summaries, not substitutes for directed endpoint formatting.

## Refined birth-process comparison

The refined baseline is valid. After ell thermal deletions, closure of the initial set with those fibers removed equals the current state. Hence:
1. k≤n0-ell.
2. j_k-k≤ell: any fiber eligible at the current load could not have been mechanically deleted at an earlier, lower load.
3. k is at least the closure after removing the ell strongest original fibers, namely max{k:j_k-ell≥k}.

For a fixed feasible k, the maximum total thermal rate among possible surviving k-subsets of the eligibility prefix is obtained by its k weakest fibers. Maximizing that rate over the allowed counts gives a valid history-independent upper intensity R_ell. Also r*=max_k(j_k-k+1) thermal deletions are necessary for complete failure, since below that deletion count at least one feasible prefix must remain. Coupling consecutive waiting times to independent exponentials of rates R_ell yields the dominating pure-birth absorption probability used as the baseline.

I exhaustively checked all these count constraints and the componentwise weakest-fiber rate ordering on 1,073 deletion states from small tied rational fixtures. All passed.

The positive uniformization implementation is sound for the supplied inputs: R encloses all rates, transition probabilities are nonnegative, and the omitted Poisson terms are bounded by a geometric tail with ratio less than one. Adding the tail to both interval endpoints encloses the *computed upper-bound expression*. It should not be described as a two-sided enclosure of the pure-birth CDF itself, though its upper endpoint remains a valid upper bound. A 90-digit recomputation reproduced the approximately 8.492794723188767844842133e-46 bound for n400, t=.1.

## Scope

- These are new RandomState(0) fixed-strength instances under specified published-model-style parameters, not independently authenticated original experimental samples.
- The roughly eight-order improvement is an improvement over this particular valid analytic upper bound, not evidence of the true CDF, universal solver superiority, or novelty over reliability/boundary-crossing literature.
- The underlying source-model thermal hazard is exp((F/k-s_i)/T), with instantaneous removal when s_i≤F/k, as used by the independent model code inspected here. I did not execute downloaded author code or extend the claim to material experiments.
- The integer DP check still relies on interval-library exponential inputs; it independently audits probability propagation, exact mechanics, and monotonicity, rather than independently proving the transcendental implementation.

Reproduction: rare_check.py; results: rare_result.json.

## Stronger midpoint and strength-box audit

A standalone checker, rare_integer_check.py, imports no production routines. It regenerates the exact binary64 strengths, computes independent 140-decimal-digit interval exponential inputs, and propagates outward-rounded probabilities using 1024-bit fixed-point integer arithmetic. All four n400 integer upper endpoints lie strictly inside the corresponding producer intervals:

- f0=7/40, T=3/20, m166, t=.1: approximately 6.67233430614805194193866868453817e-54.
- Same fixture, t=.01: approximately 3.95437878914445179355437731770634e-119.
- f0=3/20, T=1/10, m142, t=.1: approximately 1.14593728296214034710830107405678e-110.
- Same midpoint fixture, t=.01: approximately 1.19943914291730411990352385621441e-200.

The midpoint t=.1 bracket's relative width is about 1.70e-137; the t=.01 bracket's relative width is about 6.59e-107. Thus the smallest bound has not been replaced by an absolute rounding floor. Full exact upper rationals are in rare_integer_1024_results.json. Conservative readable physical-CDF upper statements are respectively 6.67234e-54, 3.95438e-119, 1.14594e-110, and 1.19944e-200.

The strength-box coupling proof is valid. For coordinatewise larger strengths, use identical Exp(1) samples X_i and clocks E_i=X_i*exp(s_i/T). Higher strengths increase clocks (decrease intrinsic thermal rates) and enlarge the eligibility sets simultaneously. Consequently every surviving feasible subset at a lower-strength realization remains feasible at the higher-strength realization for each internal time. Hence K(u), and therefore the physical lifetime integral, increase pathwise. The physical failure probability is maximized at the all-lower corner. Applying any valid one-level upper bound at that corner gives a uniform upper bound throughout the box; the optimizing m need not be common to different boxes.

Inspected strength_uncertainty.py: exact rational eta, clipping at zero, recomputed deficit-maximizing m, and evaluation through the exact-boundary interval DP implement that argument correctly. I did not rerun all six box calculations. These boxes are hypothetical coordinatewise perturbation sets, not data-derived confidence regions.

Final remaining limits: dependence on interval exponential correctness, common-clock/source-model assumptions, and exact input provenance; no physical validation, CDF tightness certificate, optimizer/solver novelty claim, or exhaustive comparative performance result.
