# Independent receipt — scalar inverse clearance clock

## Finding and accepted scope

**PASS, for the deterministic scalar ODE and expressly conditional deterministic lemmas only.**
Independent mathematical review and a separately implemented rational-endpoint replay establish

\[
1.106580521912579472\le s_*\le1.106580521912579663
\]

for the maximal solution of `e'=2(s+3e^2/4)^2`, `e(0)=0`. The underlying rational interval has width strictly less than `0.000000000000000189576600`; the two printed endpoints are outward-rounded, not point estimates.

The accepted numerical source is the eight-file `SCALAR_FREEZE.json` snapshot, manifest SHA-256 `11c22f296fadc36a5374c5bfab2c7b214a3c2a77ea27f3a5910055f93027b4a5`. In particular:

- `validated_clock.py`: `f7b3a0a64440042d1ce951d6acb072fca15c771ef8078bfec672e92ed65c5732`.
- `CERTIFICATE_FINE.json`: `ad0e3e581ed0a6d516c1cd56498fea073ff15f6d5411bd7ca009e9769c98fe21`.
- `PROOF.md`: `6de845b2f6ead2f511dec4fc5844b4ce2831f251d330d2be7cf2d9b0d8f7b237`.

The separate deterministic sup-primitive addendum, SHA-256 `7f3a88f030e5594e4b74e170192f4b1143104af77076d01b2c63b22cfb9a022c`, is also accepted on its stated domain. It does not alter the numerical freeze.

**Not accepted by this receipt:** a stochastic clearance-time theorem, a valid count-process inverse coordinate, a finite-jump generator corrector, an entrance/continuation/service bridge, a mesoscopic source theorem, or any claimed novelty/superiority. Context-source hashes do not turn those sources into reviewed dependencies. No external sources, downloads, installations, or publication were used.

## Independent mathematical checks

### 1. Startup and genuine blow-up

The forward field is a polynomial and is locally Lipschitz. Its solution is nonnegative and strictly increasing for positive time. While it exists, `e(s)>=2s^3/3`. If it reaches time 1, then `e(1)>=2/3` and `e'>=(9/8)e^4` forces blow-up by time 2. A finite maximal endpoint with bounded state would be extendible. Thus the finite maximal time is a genuine divergence endpoint, with `s_*<=2`.

The degree-78 startup polynomial has nonnegative coefficients. An independently implemented sparse-polynomial recurrence recomputed it and its full residual exactly. All residual coefficients below degree 78 vanish; all remaining ones are nonnegative. Thus `P` is a subsolution and `0<=R(s)<=R(1/2)` on `[0,1/2]`.

On `0<=s<=1/2`, `0<=e<=1/4`, the exact derivative bound is `f_e<=105/128=L`. With `delta=R(1/2)/(1-L/2)`, the polynomial-plus-line `U=P+delta*s` satisfies `U'-f(s,U)>=0`. The exact computed `U(1/2)<1/4`, and coefficient positivity keeps the whole barrier in the rectangle. Comparison bounds the true solution and rules out earlier blow-up. This is not a formal-series convergence assumption.

The upward dyadic rounding `a>=U(1/2)` and `e'(s)>=1/2` for `s>=1/2` imply
`1/2<=s(a)<=1/2+2(a-P(1/2))`. Existence to the hit is justified because a path cannot diverge without first crossing finite `a`. Both endpoints are rounded outward. The exact initial inverse width is `583509885/2^120`.

### 2. Directed arithmetic and Taylor remainder

The production integer interval operations correctly enclose addition, all sign combinations of multiplication, and reciprocal on either component away from zero. Python integer floor division, together with the explicit ceiling formula, supplies the claimed directions even for negative numerators. Reciprocal intervals containing zero are rejected.

The independent checker does **not import the constructor**: it stores `Fraction` endpoints and independently rounds exact endpoint products and reciprocals to the `2^-120` grid. Its startup uses a sparse polynomial representation rather than the production convolution arrays. Every replay decision uses integers or exact rational arithmetic.

For the inverse field `F(e,s)=1/[2(s+3e^2/4)^2]`, the reciprocal-series coefficient recurrence follows by multiplying formal series and extracting coefficients. Smooth ODE differentiation identifies those coefficients with `s^(j)/j!`; no assertion of convergence of an infinite Taylor series is needed. Natural interval evaluation therefore encloses the coefficient function over any rectangle with positive denominator.

For a center initial state `u`, the center trajectory lies in
`e in [a,a+h]`, `s in [u,u+h F(a,u)]`: it increases, and the field decreases in both coordinates. The implemented tube upper endpoint is rounded upward. The order-13 coefficient evaluated on this whole tube bounds the actual Lagrange remainder of the order-12 Taylor polynomial. The power is `h^13`; its factorial is already in the coefficient. This is a remainder proof, not merely computation of twelve derivatives.

As a distinct algebra check, the test suite computes exact coefficients from `2*w(h)^2*s'(h)=1` directly, without a reciprocal-series expansion. All 504 coefficient inclusions through order 13 at rational points in four rectangles pass. These finite tests supplement rather than replace the induction and Taylor theorem.

### 3. Nonexpansive global composition and error ledger

`F_s=-(s+3e^2/4)^-3<0`. Two inverse solutions beginning at the same level preserve order and their distance cannot increase. It is therefore valid to compute a center trajectory and then add the entire prior radius unchanged. No positive Gronwall multiplier is silently omitted.

A dyadic midpoint can require one additional width tick. For the fine replay the exact width decomposition is

- startup: `583509885/2^120`;
- summed local Taylor/rounding widths: `236682427985596251367/2^120`;
- midpoint-padding width: `560/2^120`.

The inverse-stage increment is consequently `236682427985596251927/2^120`, exactly the certificate's value. Each of the 18 saved checkpoints agrees with the independent replay. The coarse run has 237 midpoint-padding ticks and eight matching checkpoints.

### 4. The infinite tail is paid exactly

For `v>=E`, `0<F(v,s)<=8/(9v^4)`, so the inverse has a finite limit and `T0=8/(27E^3)` bounds its entire tail. If `s(E) in [L,H]`, then `L<=s(v)<=U=H+T0`. The inequalities

`1-2x <= (1+x)^(-2) <= 1-2x+3x^2`, for `x>=0`,

follow from exact nonnegative polynomial remainders. Substitution of `x=4s/(3v^2)`, monotonicity in `s`, and integration give exactly

`T_- = T0 - 64U/(135E^5)`,

`T_+ = T0 - 64L/(135E^5) + 128L^2/(189E^7)`.

The replay checks `0<T_-<=T_+<=T0` and `U<2` exactly. The baseline lower tail justified by `s_*<=2` is also valid. At `E=256`, the tail is of order `10^-8`, while its uncertainty is below `1.152*10^-17`: confusing those two sizes would invalidate the result.

The exact separation `s_star_lower - s_at_E_upper` is positive, as saved in `INDEPENDENT_TEST_RESULTS.json`. Thus omitting the tail gives an interval provably disjoint from the accepted enclosure, an explicit counterexample to treating the last finite-level value as the blow-up time.

### 5. Output decimals, floats, and costs

Both rational endpoints are independently converted to base-ten strings using integer floor/ceiling; the fine printed enclosure and the 24-digit upper bound on its width agree exactly. All 24 recomputed mathematical certificate fields match in both runs. Both saved JSON trees contain no floating-point value. The source has no float literal; its only timing path uses integer `monotonic_ns`, explicitly nonproof metadata.

The fine run uses degree 78 for startup, order 12 for inverse Taylor steps, fractional dyadic precision 120 bits, `E=256`, and 1,142 steps. “120 bits” is fractional grid precision, not a promise that every integer or temporary numerator has at most 120 bits.

Exactly reproduced interval-operation counts are:

| Run | Additions | Multiplications | Reciprocal calls |
|---|---:|---:|---:|
| Coarse, 507 steps | 128,778 | 149,058 | 11,661 |
| Fine, 1,142 steps | 401,984 | 454,516 | 30,834 |

For order `p>=3`, a separate count derivation gives per inverse step exactly `2p^2+5p+4` additions, `2p^2+8p+14` multiplications, and `2p+3` reciprocal calls. Thus the fine per-step counts are 352, 398, and 27; multiplying by 1,142 recovers the totals. The independent checker asserts these closed-form counts too.

As the frozen proof explicitly states, these counts exclude arithmetic self-tests and exact-fraction startup operations; they are not total bit-operation complexity or a hardware benchmark. Arbitrary-size integer arithmetic and the finite exact startup are still required. Counter resets make separate solver invocations comparable. No stochastic simulation cost follows from these deterministic counts.

## Separately accepted deterministic identities — no stochastic promotion

The frozen proof's conditional total-variation perturbation bound and forward time-shift comparison are valid under the displayed exact path identities, nonnegativity, and stopping/domain assumptions. Those assumptions are not proved for a count chain in this package.

For the remaining-time function `b(l,e)`, take `l>0,e>=0`, `w0=l-3e^2/4`, and solve the inverse equation from `(e,w0)`. Although `w0` may be negative, its denominator begins at `l>0` and increases. The tail is integrable. The initial-value sensitivity is

`J_inf=exp(-integral_e^infinity (u(v)+3v^2/4)^(-3) dv)`.

Smooth finite-level dependence and locally uniform integrable tail bounds justify the infinite-level derivatives. Initial-point differentiation gives the frozen formulas

`b_l=J_inf-1`,

`b_e=(3e/2)(1-J_inf)-J_inf/(2l^2)`.

They satisfy `(1+3l^2 e)b_l+2l^2 b_e=-1` by direct cancellation. They are accepted on this positive-denominator deterministic domain only. They do not justify substitution at `l=0`, a finite-jump Taylor remainder, or a stochastic corrector.

The separately frozen cumulative-residual addendum is valid even for measurable bounded `R`, provided the stated integral identity holds pointwise and the drift is integrable. Subtracting `R` gives an absolutely continuous `q`; monotonicity of the drift and the positive-part chain rule confine `q` between its two stated barriers. Both the symmetric bound `max(|delta0|,epsilon)+epsilon` and the asymmetric residual-oscillation bound follow. No finite-variation assumption is necessary.

A coefficient-one shortcut would be false even for this inverse field. Start matched paths in its positive domain, jump the residual from zero to `-epsilon`, evolve for a positive interval, then jump it to `+epsilon`. Strict inverse contraction places the state difference just before the second jump strictly between `-epsilon` and zero; just after it, the difference is strictly greater than `epsilon`. All denominators can be kept positive. This also explains why a martingale supremum does not become a one-for-one state error without the proved barrier argument.

## Reproducibility and negative controls

Run from the workspace root:

```sh
python audit_inverse_clock_certificate_20261101/verify_receipt.py
```

This checks frozen input/receipt bindings, independently replays both certificates, and runs the alternative-recurrence/rounding/mutation tests. The reviewer implementation is `independent_check.py`; its tests are `test_independent.py`. Source snapshots and exact replay outputs accompany this receipt.

Additional tests passed: 1,296 rational rounding pairs; four zero-containing reciprocal rejections; eight rejected certificate mutations (lower endpoint, upper endpoint, inward decimal, omitted tail, operation count, startup value, precision, first checkpoint). These checks are independent executable corroboration of the ordinary mathematical argument, not a proof-assistant/kernel formalization.

No blocking defect or counterexample to the stated scalar theorem or the separately scoped deterministic lemmas was found. Earlier float timing metadata and ambiguous operation-counter scope were corrected before the accepted freeze. Any change to a bound file requires fresh review/replay; this receipt does not authorize expanded stochastic claims.
