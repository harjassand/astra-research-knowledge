# Independent receiving: automatic validated row fast path

28 October 2026. **PASS for the composition with the bound resource-event implementation clarification.**

Source: `AUTOMATIC_VALIDATED_ROW_FAST_PATH.md`, SHA-256 `69b012d669b6e8a32a587b804768acf2bc3155906ea2598727275c357a89fd05`.

Required clarification: `FAST_PATH_RESOURCE_EVENT_IMPLEMENTATION_CLARIFICATION.md`, SHA-256 `cea657a43f9b6fac5a9567a285de21676e523b0cb54b1b2f768332896f74d3b0`. Its automatic-schedule resource-event interpretation is received by this review. The author sources and previously received modules were not edited.

## Accepted modules and scope

The acquired-anchor construction and positive residual-validation/fallback construction are now received imports, bound by `acquired_anchor_independent_receipt.json` and `row_residual_validation_independent_receipt.json`. I reverified all 11 and 15 entries of those receipts, respectively. Their matrix estimator, physical decoder and generic fallback primitives are not re-audited here.

The new obligations are the universal geometric balance floor, finite dyadic schedule, confidence redistribution over reached histories, instance-sensitive early-completion count, and its actual finite-control probability. The actual known physical output basis and fixed four-real-coordinate encoder remain. No approximate-row theorem is imported.

## 1. Universal balance floor

For a uniform real point on S^3, slicing at first coordinate t gives surface measure proportional to `sqrt(1-t^2) dt`: the S^2 slice area is `4pi(1-t^2)` and the surface Jacobian contributes `1/sqrt(1-t^2)`. Dividing by the S^3 area `2pi^2` gives density `(2/pi)sqrt(1-t^2)`. Hence the probability of `|u^T x|<a` is at most `4a/pi` for every unit real u.

There are at most d nonzero row directions, so at `a=1/(4d)` the union has probability at most `1/pi<1`. A point outside the union has every squared overlap at least `1/(16d^2)`. The finite minimum is continuous on a compact sphere, so its maximum kappa_* exists. Normalization gives `1=sum_i lambda_i |u_i^T x|^2` and `sum_i lambda_i=4`, proving the upper bound kappa_*<=1/4. No stochastic sampling of this sphere is required by the algorithm; it is a mathematical existence bound only.

This step does not provide an acquired anchor or a good logical code. Its dimension loss is retained: the universal value is only of order d^-2.

## 2. Schedule and confidence parameters are finite

Compute J as the smallest integer with `2^J>=4d^2`, avoiding an unresolved numerical comparison with an irrational logarithm. Then `1/(32d^2)<2^(-J-2)<=1/(16d^2)`, and every kappa_j is rational. The count thresholds, anchor tests and validation thresholds are therefore exact rational comparisons.

The acquired-anchor pilot concentration proof accepts any confidence input through `L>=log(64d/beta_t,j)`. Likewise each residual test's proof applies at any declared beta_0,j via its sample logarithm. Reducing these budgets to the displayed values changes only logarithmic factors and finite precision, not the signal thresholds or the relative-risk target. Conservative integer upper logarithms, such as outward base-two bounds, give an explicit finite cap without having to decide whether a transcendental logarithm is exactly an integer. Their constant-factor overestimate leaves the claimed order unchanged.

Each reached stage uses fresh pilot and validation data. Conditional on its preceding history, the actual source is the same stationary reset source in the known physical basis. The module's uniform conditional validation statements therefore apply at that stage. No confidence statement is conditioned on eventual success and no bank is shared as though it remained independent after an adaptive rejection.

## 3. Arbitrary-source risk under first acceptance

At every reached stage, each of the two tests has false-acceptance mass at most beta_0,j conditional on all prior records. Multiplying by its reach probability and summing is bounded by the unconditional schedule sum. Thus

`Pr(false accepted residual bound)<=2 sum_j beta_0,j=epsilon/4096`.

The single subsequently acquired actual anchor bank has failure mass at most epsilon/512 after averaging its uniform conditional guarantee. There is no bank per rejected stage. If every stage rejects, the generic learner is acquired on fresh calls after that entire decision record, so its expected guarantee can be weighted by the probability of rejection. The identity known-frame specialization with trivial valid Choi-rank bound 2k is explicit in this source.

Combining the accepted and fallback branches gives exactly the stated additive budget

`epsilon/512+epsilon/4096+epsilon/512=17epsilon/4096`.

All bad selected policies remain physical and cost at most one Bell loss. One private-framed payload and one whole-process implementation debit epsilon/2 fit the final complete-error target with substantial slack. The proof supplies averaged risk, not a public record-dependent or rare-acceptance conditional certificate.

## 4. Instance-sensitive call count and worst-case cap

On an exact-row source, let j_* be the first index with kappa_j<=kappa_*. Existence of the universal floor ensures j_*<=J; the dyadic spacing gives kappa_j*>=kappa_*/2. If an earlier stage accepts, even erroneously, it already uses no more source calls than the corresponding prefix ending at j_*. Correctness is separately controlled by the false-acceptance budget.

Conditional on actually reaching j_*, the new pilot has its stated good-event probability. The true balance promise at that value then makes its anchor search succeed and provides the module's residual completeness bounds. The two fresh validation tests reject with total probability at most 2beta_0,j*. Therefore the ideal probability of no acceptance by j_* is at most beta_t,j*+2beta_0,j*, strictly below epsilon/512. Earlier pilot events need not all be good and no union over all of them is required for this specific completion event.

For the call sum, `sum_{j<=j*}1/kappa_j<2/kappa_j*<=4/kappa_*`. Pilot and row-kernel banks therefore sum geometrically. The discarded-mass test has a stage-independent price, but that price is bounded by the row-kernel test price at every stage, so it does not create a hidden polynomial stage multiplier. Integer ceilings contribute at most a geometric-order amount; the leading calls are already at least one per stage. The single anchor bank is no larger than the bank for j_*. This proves the stated instance-sensitive order with logarithmic confidence factors.

At the final possible stage, `1/kappa_J<32d^2` and r<=d, so the bank plus all preceding acquisition is `O_tilde(d^4/(gamma epsilon))`. Adding the independently received generic fallback preserves that worst-case order. This maximum, along with every known-control and memory cap, is declared before data. Early exit does not retroactively reduce numerical precision or the allowed process-error ledger. The theorem is not a smaller universal deterministic cap or an expected-stopping-time claim.

## 5. Actual resource-event probability

The original statistical completion probability concerns the ideal reference experiment. The bound clarification allocates `nu_pre<=epsilon/1024` to the ENTIRE predecision adaptive instrument, including its classical branch record, inside the already allowed total epsilon/2 process discrepancy. This is one allowance over all stages, not a fresh allowance at each stage. Choosing sampler bits and known-control precision against the maximum horizon implements that allocation without new source calls.

The actual event probability differs by at most nu_pre. Consequently actual failure to stop by j_* is below `epsilon/512+epsilon/1024=3epsilon/1024<epsilon/256`. This is the probability to use when stating the high-probability ACTUAL call bound. It does not add another epsilon/1024 to final channel error outside the existing epsilon/2 budget. A complete-error bound after discarding the branch record alone would not prove the resource-event claim; the predecision record must be retained in the comparison as specified.

## Independent evidence

`automatic_row_schedule_independent_checks.py/.json/.log` is new, source-disabled reviewer evidence: 256 exact dimension schedules, 11,912 intrinsic-balance index cases, 456 finite source-cap cases, and 96 exact adaptive first-accept/fallback risk histories. It checks integer stopping, rational threshold geometry, ceiling costs, one-bank prefixes, false-acceptance sums and the implementation probability debit. Both received module manifests, 26 entries in total, were reverified.

There were zero RNG draws, source calls, sampled trial outcomes, aggregate count simulations, acquisition circuit executions or production optimizations. The checks are deterministic rational composition evidence, not practical or hardware validation. The sphere density and complete-process arguments are independently proved above rather than inferred from simulations.

## Accepted conclusion

This is a parameter-free ordinary fast path with the existing generic k^4 worst-case cap. It automatically attains a faster high-probability source count on the exact-row subclass in terms of the unknown intrinsic balance, with no supplied anchor, balance value or useful logical seed. The actual known receiver basis, reset interface, ordinary input restriction and full coherent CPTP comparator remain. Generic fast acceptance, an arbitrary-basis guarantee, a universal k^2 rate, or an advantage over an equally informed conventional learner is not received.
