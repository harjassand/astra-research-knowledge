# Independent audit: stochastic control costs for refreshed private frames

Date: 2026-10-15. Mathematical audit of the proposed narrow extension. No canonical theorem files were edited and no external source execution was performed.

Reference inputs read:

- `../reference/DIRECT_FOURIER_INDEPENDENT_AUDIT.md`
- `../reference/SCHEDULED_MEMORY_COMPOSITION_GATE_AUDIT.md`

## Verdict

The proposed homogeneous marked-parent effect bound is valid under the full-process qualifications below:

`E(all i in S have a nonzero weak character OR a control-fault label) <= (p_weak + f_ctrl)^|S| I`.

Here `p_weak = min(1, a^2, m B(J,gamma,t))` is a uniform reference weak bound for the same complete global Fourier/Kraus family. A final homogeneous budget may be capped at one. Correlation between a parent's refresh path and its number of executed controls does not invalidate this result.

The original weak rate is retained in the primary proof because no-fault weights are dropped before the weak-clock average. A separately verified tilted-rate refinement is given below.

## 1. Required full-process hypotheses

At every executed control slot the actual full joint causal map, uniformly conditional on previous classical history, is

`R = (1-epsilon) R0 + epsilon R1`,

where both branch maps are CPTP, `R0` is exactly the intended joint ideal control in the common compiler, and the scalar branch weight is independent of the private initial seeds. The statement must concern the full joint memory/bath/controller process, not merely an individual reduced or marginal gate channel. Genuine quantum outcomes are retained in a dilation and summed without normalization.

The constant-weight version uses the same `epsilon` in every counted slot. Uniform upper bounds can be padded to a common contamination weight, producing a conservative declared-fault label. More general fixed slot weights require their corresponding no-fault product rather than the constant-weight formulas below.

The private proposal clocks and the number of counted deterministic boundary slots are exogenous. Faults do not change the count law, reservation endpoint, support, or scheduling rules used in the theorem. Boundary slots are padded/countable even when the intended operation is identity: skipping identity operations or implementing a variable-length final inverse requires separate count accounting.

After replacing any outside parent's control slots by their normalized fault branches, the same common reference/toggling representation must leave all selected all-good parents with the exact private additive weak interface. Outside branch maps and their dilations may depend on their own parents' fixed private parameters, but not on any remaining selected parent's private seeds or paths. This is a substantive deletion-stability requirement. Laboratory-level seed independence alone does not imply it after frame conjugations.

Ordinary internal records cannot be conditioned and normalized to manufacture this interface. The geometric record is still separate from the private internal streams.

## 2. Primary partition-and-domination proof

Write `C_i` for the event that parent i has a declared control fault, and `Q_i` for its nonzero weak Fourier character. Partition the joint event on S by the exact subset `F = {i in S : C_i}`; set `W = S \ F`.

For one partition term:

1. Sum all Fourier characters on F and on unselected parents. Parseval converts these sums into averages over their initial seeds.
2. Fix their exogenous paths and classical control-fault patterns. Their normalized branch maps become a selected-W-independent baseline. Sum genuine quantum/dilation outcomes.
3. Every W parent uses only `R0`. Its scalar no-fault branch weight is `q_i(path)` with `0 <= q_i <= 1`.
4. Remove the product of these weights at the positive-effect level, before averaging the W private clocks. Do not condition those clocks on the no-fault event.
5. Apply the weak theorem to the resulting reference process, uniformly in the outside background. This gives `p_weak^|W| I`.
6. Integrate the independent fault-parent path/coin distributions. Their masses contribute `product_(i in F) f_i`.

Consequently

`E_S <= sum_(F subset S) p_weak^|S\F| product_(i in F) f_i I`.

For homogeneous `f_i = f_ctrl` the sum is `(p_weak+f_ctrl)^|S| I`. There is no retained factor `1-f_ctrl` on the weak parents in this proof.

The scalar branch product is justified by trace preservation of every normalized causal branch. Marginal decompositions alone are insufficient: a common hidden coin could make all parents faulty with probability epsilon rather than epsilon raised to their number.

## 3. Poisson count and exact declared-fault probability

Use `mu = m gamma t` for the mean total number of proposed generator updates. For `N ~ Poisson(mu)` and c deterministic boundary slots,

`S0 = P(no control-fault label) = (1-epsilon)^c exp(-mu epsilon)`,

`f_ctrl = 1-S0`.

Thus the primary budget is `min(1, p_weak(gamma)+f_ctrl)`.

Notation warning: `exp(-lambda t epsilon)` is correct if `lambda=m gamma` denotes a rate. If lambda denotes the count mean `m gamma t`, the exponent is `-lambda epsilon`.

For deterministic time/type-dependent marking rates the Poisson no-fault exponent becomes minus the integral of clock intensity times the fault weight. Ordinal-slot-dependent weights generally require computing an expected product; they do not automatically give the same exponential.

## 4. Verified tilted-Poisson refinement

The scalar likelihood factor `(1-epsilon)^N` transforms each independent rate-gamma private clock into a rate-`gamma(1-epsilon)` Poisson clock. The joint normalizing mass, including boundaries, is S0. The initial fair seeds remain unchanged.

Therefore the unnormalized all-good weak effect on any selected W is at most

`[S0 q_tilt]^|W| I`,

where `q_tilt = min(1, a^2, m B(J,gamma(1-epsilon),t))`.

Repeating the fault-parent partition proves the sharper sufficient budget

`p_tilt = f_ctrl + S0 q_tilt`.

This explicitly uses the changed weak clock law. Multiplying `S0` by the original-rate `q_weak(gamma)` without a further argument would not be justified. One may take the smaller of the independently established homogeneous primary and tilted budgets.

## 5. Cap/overflow accounting

Let N be the complete latent proposal count. The following formula applies to the enlarged bad event

`{N > M} OR {at least one control-fault label}`.

On nonoverflow the actual capped and uncapped controls agree. On overflow the entire parent is charged bad, whatever the capped implementation subsequently does within its certified support.

The exact good mass is

`A_M = (1-epsilon)^c exp(-mu) sum_(n=0)^M [mu(1-epsilon)]^n/n!`,

and `f_M = 1-A_M`. Equivalently, with `T_M = P[Poisson(mu(1-epsilon)) <= M]`,

`A_M = S0 T_M`, and `f_M = 1-S0 T_M`.

Dropping all weak parents' no-fault weights and acceptance restrictions in the uncapped reference process gives the primary cap budget

`min(1, f_M + p_weak(gamma))`.

Under the tilted clock law, dropping only the acceptance restriction gives `S0 q_tilt` per weak parent. The independent acceptance mass also gives `S0 T_M`. The homogeneous minimum therefore proves

`p_M = f_M + S0 min(T_M, q_tilt)`.

This is at most one. Since the action-squared bound is uniform at every fixed path, a further valid good-term refinement is

`S0 min(T_M min(1,a^2), m B(J,gamma(1-epsilon),t))`.

These are homogeneous joint-subset minima, not an assertion of arbitrary heterogeneous hybrid minima.

If overflow is NOT itself declared bad, f_M is not the exact control-fault probability. For a protocol executing exactly `min(N,M)` updates that probability would instead be

`1-(1-epsilon)^c E[(1-epsilon)^min(N,M)]`.

The weak analysis of that character-only capped protocol is a different argument.

## 6. Deterministic fair-cell schedule

Partition the interval into M equal cells and choose each generator's frame value independently and fairly in every cell. Write the first value as the initial fair bit and use independent fair relative increments at the M-1 internal boundaries. This change of variables is a bijection over the bit strings.

For a selected witness generator, take its relative first-cell sign as +1. Its later relative cell values are independent fair signs. The averaged even correlation kernel is the indicator that every cell contains an even number of combined bra/ket insertions. It is nonnegative, so the direct Dyson majorization gives

`B_det = ( (cosh(2 J t/M))^M - 1 ) / 2`.

More generally, with uniform norm-action bounds a_k on individual cells, the scalar majorant is `[product_k cosh(2a_k)-1]/2`.

The physical flip count is `Binomial(m(M-1), 1/2)`. With constant epsilon and c padded deterministic boundary slots,

`f_det = 1-(1-epsilon)^c (1-epsilon/2)^[m(M-1)]`.

The primary proof yields the homogeneous budget

`min(1, min(1,a^2,m B_det) + f_det)`.

Dependence of flip count on the weak path is harmless because only fault-parent probabilities are retained, while the weak parents' no-fault weights are dropped.

For a tilted deterministic refinement, no-fault weighting biases each flip probability to `(1-epsilon)/(2-epsilon)`. The original iid-cell B_det cannot simply be multiplied by the no-fault mass; a new biased-sign weak bound would be needed.

## 7. Physical and support scope

An exact positive ideal-control component is a strong stochastic-noise premise. A distinct unitary over-rotation generally has no nonzero exact ideal-unitary mixture component, regardless of a small norm or diamond distance.

The effect theorem does not establish finite-width control equivalence, unchanged geometry, or completion-time support propagation of arbitrary control faults. Those require a certified time-aligned instrument, a full declared fault patch, and the existing support/locality hypotheses or a separate extension. In particular, instantaneous support at a faulty gate does not by itself prove that all descendants can be charged only at the original parent completion.

The result therefore qualifies the effect-budget substitution under explicit compiler and support premises. It does not independently qualify general noisy randomizers, noisy correction cores, or an autonomous continuous-noise memory.
