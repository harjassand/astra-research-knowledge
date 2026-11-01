# Independent receipt — deterministic candidate inverse-clock variance

## Accepted result and boundary

**PASS.** For the deterministic origin orbit

`l'=1+3l²e`, `e'=2l²`, `l=s+3e²/4`,

and `J(e)=exp(-integral_e^infinity l(v)^(-3) dv)`, the functional

`Sigma²=integral_0^infinity (1-J(e))² dl(e)`

satisfies the rigorous outward enclosure

**`0.5677211094 <= Sigma² <= 0.5687113183`.**

The exact rational width is strictly less than `0.000990208879`, hence below `10^-3`. The finite calculation pays the singular-origin sensitivity, backward sensitivity tail, state and exponential rounding, both quadrature meshes, the startup join, and the final variance tail.

This acceptance is **only the deterministic candidate linear-fluctuation functional** from repaired root `3738ec11751d5e094e70c5f32d7dedfe2ff978403cd7b4b6be18816bbf0cf555`. It is not an actual-chain CLT, measured SSA variance, finite-noise Ito variance, finite-N timing distribution, or a proof of the stipulated noise covariance/linearization/terminal passage. The accepted `s_*` scalar freeze is preserved; this receipt does not expand its scope.

The numerical freeze reviewed is `VARIANCE_FREEZE.json`, SHA-256
`60636c65f720823168088f2b97760d5473f3fe5b51c6388369fedd1ada456129`, binding seven files. In particular:

- `validated_variance.py`: `166fdd045942000e7c849381d97e134795135137af1319c48894c47f0090331b`.
- `VARIANCE_CERTIFICATE.json`: `2d4e2c09d7213b8998b630d05624b8f6528ddd568e3d640dd0602d581b0ca806`.
- `PROOF.md`: `34a41c63df0dd25132fd15f0d2909c8d2d19d9bcb279b9a02778f2aec6829840`.

The reused scalar freeze remains `11c22f296fadc36a5374c5bfab2c7b214a3c2a77ea27f3a5910055f93027b4a5`, with solver hash `f7b3a0a64440042d1ce951d6acb072fca15c771ef8078bfec672e92ed65c5732`. Both packages and all declared source bindings were verified and copied to `frozen_inputs/`. No external source, installation, helper agent, or publication was used.

## 1. Positive-level orbit acquisition

The previously independently reviewed scalar method applies at order five as well as order twelve: its coefficient recurrence and whole-tube Taylor remainder proof are order-independent. The variance construction starts from the earned inverse state at `a>=e(1/2)` and uses two validated half-steps per interval. Hence each midpoint and endpoint encloses the same true orbit, with nonexpansive prior-error composition and all directed rounding retained.

At `E=8` the inverse state width is exactly
`167307339971037597677/332306998946228968225951765070086144`, below `5.04*10^-16`. The integration never substitutes an unproved inverse initial value at the singular corner.

## 2. Backward sensitivity, including infinity

For `L=s(e)+3e²/4`, `V=L'=1/(2L²)+3e/2`, direct differentiation gives

`L''=3/2-V/L³`,

`(L^-3)''=12V²/L^5+3V/L^7-(9/2)/L^4`.

The exact orbit has increasing `L`. On `[a,b]`, a certified positive `L_min` at the left endpoint therefore implies `V<=1/(2L_min²)+3b/2`. Taking absolute values termwise yields precisely the implemented curvature bound. The midpoint error is at most `M(b-a)^3/24`; this is the ordinary C² midpoint remainder, not a sampled-error estimate. The interval midpoint state contains the actual midpoint. Adding these interval integrals backward is valid without assuming independent node errors. Intersecting their lower endpoints with zero is safe since `L^-3>0`.

The global inverse-time tail gives `L_s<=s(e)<=U_s=H_s+8/(27E³)` for `e>=E`. The inequalities

`1-3x <= (1+x)^(-3) <= 1-3x+6x²`, `x>=0`,

have exact nonnegative polynomial remainders `6x²+8x³+3x⁴` and `10x³+15x⁴+6x⁵` after multiplication by `(1+x)^3`. Substitution and integration yield the implemented bounds

`H_tail_lower=64/(135E^5)-256U_s/(189E^7)`,

`H_tail_upper=64/(135E^5)-256L_s/(189E^7)+2048L_s²/(729E^9)`.

The bounds are positive and ordered. Backward accumulation from that interval, followed by an outward exponential, encloses every `J` node, including the effect of infinity.

The positive exponential algorithm is valid: scale until the argument is at most `1/8`, retain terms 0 through 18, and dominate the tail beginning at term 19 by `t19/(1-z/20)`. All successive ratios are bounded by `z/20`; the denominator remains positive. Repeated squaring and reciprocal preserve inclusion. Monotonicity reverses endpoints correctly for `exp(-z)`.

## 3. Singular-origin sensitivity and the startup join

The sparse degree-78 forward polynomial is independently recomputed. Its nonnegative residual coefficients vanish below degree 78, so on `[0,s0]`, `s0=1/2`,

`0<=R(s)<=R(s0)(s/s0)²`.

The cubic supersolution `P(s)+delta3*s³`, with
`delta3=R(s0)/[s0²(3-(105/128)s0)]`, stays below `1/4`; the derivative inequality proves it is a true barrier, not merely a formal-series approximation. Nonnegative polynomial coefficients and the endpoint check prove

`(2/3)s³ <= e(s) <= (84/125)s³`

throughout the segment.

For positive `s`, differentiation along the orbit gives

`d(log J)/ds=2/l=2/s-k(s)`.

The displayed regular `k(s)` is positive and lies between the stated rational multiples of `s^4`. Integrating gives

`J(s)=J(s0)(s/s0)² exp(integral_s^s0 k(u)du)`.

The regular exponential factor is bounded uniformly to zero, so this formula proves `J(0)=0`. The implementation uses that exact endpoint and never divides by zero. Bounding `k` by its two rational envelopes at every startup node is conservative and mathematically valid even though it is not a sharp Taylor quadrature.

Since `a>=e(s0)`, the omitted sensitivity segment obeys
`0<=integral_e(s0)^a l^-3 de <= 8(a-P(s0))`. Thus the lower multiplication by `1-8(a-P(s0))` and the unchanged upper endpoint rigorously recover `J(s0)` from `J(a)`. The actual variance join is nonnegative and at most its level length. The code charges the upper endpoint of `l(a)` minus the lower endpoint of `l(s0)`, exactly

`gap_variance_upper=620267879/2^120`.

The startup, join, and inverse regions meet at their true endpoints; no gap is silently removed and no independence of their interval errors is required.

## 4. Riemann–Stieltjes enclosure and final tail

`J` increases from zero to one and `l` increases; therefore `(1-J)²` decreases. The right endpoint gives a lower rectangle and the left endpoint an upper rectangle against `dl`. Clipping each true nonnegative level increment to

`[max(0,L_next-H_previous), H_next-L_previous]`

and each `1-J` enclosure to `[0,1]` preserves inclusion. Multiplication uses nonnegative endpoints, with outward rounding. Dependency between adjacent certified intervals can enlarge this bound but cannot invalidate it.

The terminal sensitivity estimate `1-J<=64/(135e^5)` and `dl/de<=8/(9e^4)+3e/2` give

`0<=V_tail<=(4096/18225)[(8/117)E^-13+(3/16)E^-8]`.

At `E=8`, the charged exact upper bound is `89857/35774477107200`, below `2.512*10^-9`. It is added rather than discarded.

The exact width ledger is

`startup_width + inverse_width + tail_and_gap_charged_width = total_width`.

The final tail/join rounding excess is exactly
`277523/2834346086112070738689610389812285748019200`, nonnegative and less than `2^-120`. All these values match independent recomputation. The singular sensitivity envelope and all rectangle errors are included in the first two widths.

## 5. Independent replay, negative controls, and costs

The independent variance implementation imports neither author solver. It reuses the **reviewer's** scalar recurrence, independently recomputes the startup with sparse polynomial products, and has a separately implemented directed-dyadic interval class. This class is cross-checked against exact rational endpoint arithmetic. The numerical method is deliberately replayed, not claimed to be a second unrelated theorem or proof-assistant formalization.

All **33 mathematical certificate fields** replay exactly, including the endpoints, every width contribution, origin/sensitivity quantities, state width, step counts, and operation counts. A separate execution of the frozen author code also matches every field except its expressly nonproof elapsed time. No certificate or independent proof value contains a float; source AST checks find no float literal.

Checks additionally passed:

- 1,296 directed-rounding comparisons against exact rational endpoints;
- four rejected reciprocals through zero;
- 20 exponential comparisons against independently bounded alternating rational series;
- symbolic verification of both tail-polynomial identities;
- four exact-integral tests of the monotone rectangle algorithm;
- nine rejected certificate mutations: endpoint, inward decimal, startup sensitivity, omitted sensitivity tail, omitted variance tail, omitted join, rectangle count, precision, and operation count.

An explicit counterexample confirms the essential rectangle direction: for `(1-l)^2` on `[0,1]`, the left rectangle is `1`, strictly above the integral `1/3`, and cannot be used as a lower bound. No counterexample or blocking defect was found in the frozen construction's actual inequalities.

The reproduced dynamic interval-operation ledger is:

| Quantity | Exact count |
|---|---:|
| Inverse intervals | 8,106 |
| Order-five validated half-steps | 16,212 |
| Startup rectangles | 1,024 |
| Interval additions | 1,546,668 |
| Interval multiplications | 2,438,711 |
| Interval reciprocal calls | 452,641 |

There are 8,107 inverse nodes and 1,025 startup nodes. These counts include the sensitivity/quadrature arithmetic after counter reset, but exclude exact-fraction startup/precomputation and are not total bit-operation complexity. The grid has 120 fractional bits; arbitrary-size intermediate integers and exact fractions remain required.

One separate frozen-code replay recorded `9,378,954,491` nanoseconds locally; a subsequent full-verifier execution recorded `11,749,590,008` nanoseconds. Thus the claimed roughly 8–10 seconds is a local diagnostic, not a stable upper cost: the two observed reviewer runs were about 9.38 and 11.75 seconds. This is neither a hardware guarantee nor an end-to-end stochastic simulation/CLT acquisition cost.

## Reproduction and disposition

From the workspace root:

```sh
python audit_inverse_clock_variance_20261101/verify_receipt.py
```

This verifies the bound snapshot and receipt artifacts, reruns the independent replay and tests, and freshly executes the frozen author solver in a temporary output directory. The receipt is backed by `RECEIPT_BINDINGS.json`, `INDEPENDENT_REPLAY.json`, `INDEPENDENT_TEST_RESULTS.json`, and `FINAL_VERIFICATION.json`.

**Accepted at the deterministic candidate-functional scope only.** No source repair was required. Changes to bound files, a different noise covariance, or promotion to an actual-chain/finite-noise variance claim require new review and the missing stochastic arguments.
