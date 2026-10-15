# Certified precision audit for event-conditioned Bernoulli labels

Run `python /workspace/shared/conditional_precision/audit.py`. Standard library only; no NumPy dependency. It decodes the existing NPY binary64 arrays from the NPZ ZIP with `struct`, then performs every certificate operation with exact fractions or integers. The final runtime and human-readable decimal summaries are not themselves proof objects; integer endpoints and exact rational bounds in `results.json` are.

## Explicit model pin

This is a **new exact model**, not an assertion about the law implemented by the original floating-point simulation. Each rate and interaction coefficient is the exact rational decimal `repr` of the stored binary64 value in the SHA256-pinned fixture. Time is exactly 1/200. `model_pin.json` stores the rate decimals and fixture hash, and describes how all interaction coefficients are pinned. The audit verifies all 160,000 interactions satisfy 0 ≤ W_ij ≤ 1/200 and W_ii=0. Thus n=400, k=20 and beta=2 imply

C = product from j=0 to 19 of (1 + j/200) < 2.510662313729247.

The pin does not quantify model perturbation relative to any hypothetical real parameters used before the fixture was stored. It also does not certify the RNG or the original NumPy sampling code.

## Enclosure construction

Let p_i = 1 - exp(-lambda_i T). All lambda_i T lie strictly between zero and one. Alternating Taylor partial sums of exp(-x) give exact lower (odd) and upper (even) bounds. Continue until their difference is at most 2^(-b-16), then round the corresponding p_i enclosure outward to the grid S=2^b.

Represent [a/S, b/S] by integer pair (a,b). Nonnegative multiplication rounds the lower product down and upper product up; addition is exact on the grid. Complements reverse endpoints. Intersecting with [0,1] is valid for probabilities.

Define H_i(r) = P(sum of labels from i through n-1 ≥ r). Set H_i(0)=1, H_n(r)=0 for positive r and H_i(r)=0 when r>n-i. The suffix recursion is

H_i(r) = (1-p_i) H_(i+1)(r) + p_i H_(i+1)(r-1).

Induction proves enclosure at every cell. Dependence among terms can widen the enclosure but cannot invalidate it. H_0(k) encloses p0.

For a current unmet count r>0, the event-conditioned coin is

q_i(r) = p_i H_(i+1)(r-1) / H_i(r).

A positive-denominator interval quotient is bounded using numerator-lower/denominator-upper and numerator-upper/denominator-lower, with outward grid rounding. All relevant lower denominators are explicitly checked positive. When r=n-i the coin is exactly one, avoiding a needless ill-conditioned division. When r=0, the threshold is already satisfied and the coin is p_i. States with r>n-i are unreachable.

The reachable states are max(0,k-i) ≤ r ≤ min(k,n-i), with r=0 amalgamating histories that have already attained the event. All rates have 0<p_i<1, so these are exactly the possible states for an event-conditioned path before its next coin. There are 8,000 such states for this fixture.

## Finite-bit sampler and coupling certificate

A concrete sampler compatible with the audit chooses threshold M_i(r) = floor((q_lower_integer+q_upper_integer)/2), draws an independent exactly uniform b-bit integer U, and selects a failure label iff U < M_i(r). Its coin probability is exactly M_i(r)/S, inside the certified interval. Consequently its per-state error is at most the interval width. The reported bound conservatively adds 1/S at each step, also covering floor rounding of an arbitrary chosen real threshold in that interval.

Let d_i be the maximum interval width across reachable states at step i, plus 1/S. Couple ideal and approximate coins with common uniform random variables until the first disagreement. Conditional on no earlier disagreement they have the same reachable state, hence disagreement probability at step i is at most d_i. Thus

TV(ideal label law, approximate label law) ≤ sum_i d_i.

This uses TV = sup_A |P(A)-Q(A)|. It is a certificate of the described finite-bit distribution assuming independent uniform random bits; the audit does not generate samples or validate a pseudorandom generator.

If labels are then passed through the **same exact continuous conditional-time kernel** in both laws, total variation cannot increase. With stopped likelihood 0≤L≤C, the normalized expectation error |E_approx L - E_ideal L| is at most C TV. Because facilitating interactions imply p≥p0, the induced relative error in p=p0 E L is also at most C TV. This bound is conditional on exact time sampling and exact likelihood integration/evaluation, not on the existing floating implementation.

If p0 is replaced by any point in its certified interval, let epsilon_h be interval width divided by its lower endpoint. A combined relative-error bound from the p0 representation and label law alone is C[epsilon_h+(1+epsilon_h)TV]. Continuous-time and likelihood numerical errors remain to be added separately.

## Results

At b=256:
- p0 ≈ 5.10418718710409704415043333108e-14.
- Exact endpoint relative width ≤ 1.281e-61.
- Maximum conditional coin width ≤ 2.045e-32, at i=379 and r=20 (zero-based i).
- Summed label TV bound ≤ 2.373e-32.
- C times TV ≤ 5.956e-32.
- Maximum exponential Taylor depth: 26 terms after the constant.

At b=512:
- p0 exact endpoint relative width ≤ 1.112e-138.
- Maximum conditional coin width ≤ 1.766e-109.
- Summed label TV ≤ 2.049e-109.
- C times TV ≤ 5.144e-109.
- Maximum exponential Taylor depth: 47 terms after the constant.

The displayed 30-digit decimal p0 endpoints are deliberately coarser than the stored exact dyadic endpoints. Relative-width claims are calculated from the exact integer endpoints, not by subtracting the printed decimal strings.

Both audits complete in approximately 1.4 seconds together on this environment. Runtime is incidental and not a complexity certificate. This demonstrates sufficient precision at this fixed instance; it does not establish a universal bit-complexity theorem.

## Remaining gap: continuous failure times and likelihood evaluation

A distribution supported on floating-point time vectors is singular relative to the exact continuous conditional-time law: their TV distance is one. **Do not combine the label TV certificate with a claim that rounded times have small TV distance.** Likewise the pre-existing 3,000 floating-point likelihood values cannot retroactively inherit an exact iid empirical-Bernstein certificate from this audit.

One possible rigorous continuation is to generate each conditional time from an infinite random-bit uniform U using

t_i = -log(1 - U p_i)/lambda_i,

maintain nested dyadic cells for U, certify log/exponential and arithmetic intervals, and refine until the first k times are unambiguously ordered and each stopped likelihood enclosure is narrower than a declared absolute tolerance. Distinct times occur almost surely, so ordering can resolve almost surely; an explicit finite worst-case resource cap is a different claim. A bounded-time implementation could instead return an unresolved status on rare close cases, and any omission or fallback would require its own bias bound. The endpoints U=1 and equality of times have probability zero under ideal independent infinite-bit uniforms.

If every exact likelihood is enclosed within a chosen tolerance, concentration bounds can be conservatively widened using those per-sample intervals. This requires a new validated sampling/evaluation pipeline or retained randomness sufficient to replay existing samples; the current audit does not implement it.

These are standard interval arithmetic, conditional Bernoulli sampling, and coupling arguments. No novelty is claimed for these components.
