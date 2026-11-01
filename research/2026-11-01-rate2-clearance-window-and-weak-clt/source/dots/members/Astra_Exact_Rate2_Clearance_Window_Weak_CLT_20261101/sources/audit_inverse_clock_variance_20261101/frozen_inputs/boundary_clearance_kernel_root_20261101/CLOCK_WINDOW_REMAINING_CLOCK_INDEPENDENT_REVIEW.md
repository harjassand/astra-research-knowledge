# Independent ordinary review: stopped window and remaining clock

Date: 2026-11-01. Reviewer: independent clock/window subagent. No external sources, publication, hardware work, stochastic CLT, actual-chain bridge, or scalar validated-solver acceptance is part of this review.

## Frozen inputs and result

- `STOPPED_CLOCK_WINDOW_CONSUMER.md`, SHA-256 `6e76a11da95461c91ad7ee708fd893b4752b661b342dd87289d7564907f01a94`.
- Original `REMAINING_CLOCK_OBSERVABLE.md`, now preserved exactly as `HISTORY_REMAINING_CLOCK_V1_f0ade880.md`, SHA-256 `f0ade8800f84315e818adabdf9a7fdf7f9773487aea19e139603a5d08b647067`.
- Repaired `REMAINING_CLOCK_OBSERVABLE.md`, SHA-256 `3738ec11751d5e094e70c5f32d7dedfe2ff978403cd7b4b6be18816bbf0cf555`. Its complete diff from the preserved original was inspected: only the candidate-variance introduction and final stochastic-scope paragraph changed.

**Stopped-window result: PASS as a conditional ordinary probability theorem.** Its signs, stopped endpoint use, Freedman radius, strict deadline comparison, simultaneous admission-failure convention, union-bound probability, and non-reachability argument are correct. It does not assume target attainment and does not establish its actual-chain premises.

**Repaired remaining-clock deterministic result: PASS**, including explosion, inverse representation, first derivatives, PDE, boundary extension of `|b_l|<=1`, and the stated origin-orbit variance-tail constant. The boundary justification is supplied below. No stochastic variance theorem is accepted. The original phrase “a justified diffusion limit ... its clock variance would be” needed narrowing to a candidate linear-fluctuation/small-noise clock variance, not a literal finite-noise diffusion assertion. The repaired hash above does this explicitly and is accepted in that deterministic/candidate-only scope. This clarification leaves the deterministic integral and tail unchanged.

## 1. Stopped-martingale window

Use a filtration with the usual conditions, actual stopping times `tau,sigma_adm`, and an actual càdlàg locally square-integrable Dynkin martingale `M`, with predictable bracket. The displayed identity implies `M_0=0`. All asserted jump, bracket, residual and endpoint bounds must hold for this stopped process itself, almost surely, with exit overshoots included. These are the standard intended meanings of the source, not new model acquisition.

Let `L=log(2/delta_M)` and `a=jL/3`. The chosen radius `m=a+sqrt(a²+2vL)` solves exactly

`m² = 2L(v+jm/3)`.

The one-sided bounded-jump martingale Bernstein/Freedman bound applied to `M` and `-M`, using `<M>_d<=v`, therefore gives

`P(sup_{t<=d}|M_t|>m)<=2exp(-L)=delta_M`.

If `j=v=0`, the martingale is zero and the same assertion is trivial; no division by zero in a tail exponent is required. A continuous martingale component is allowed if its predictable variation is included.

Write `B={sigma_adm<=min(tau,d)}` and `G=B^c intersect {sup_{t<=d}|M_t|<=m}`. On `G`:

- If `tau>d`, then `sigma_adm>d`, so `sigma=d`. The identity yields `d/T=q_0-q_d+I_d+M_d<=q_hi+c+r+m`, contradicting the strict deadline choice. Thus `tau<=d` without a reachability assumption.
- Consequently `sigma=tau`. Since `-c<=q_tau<=b_tail+c`, `|I_tau|<=r`, and `|M_tau|<=m`, the identity gives exactly

  `q_lo-b_tail-c-r-m <= tau/T <= q_hi+c+r+m`.

- Nonnegativity of `tau` gives the displayed clipped lower endpoint.

The probability is at least `1-delta_adm-delta_M` by a union bound, with no independence required. The convention charges simultaneous adverse exits, including the deadline. Counting a target at exactly `d` is harmless; only the contradiction for `tau>d` is needed.

An upper continuation statement should be read as a bound conditional on the actual `F_tau`, or be backed by the actual process's strong-Markov property and a uniform bound over its full exit state. A marginal or reset-state statement is insufficient. The source correctly keeps earlier-clearance exclusion separate from upper continuation.

### Necessary-condition checks

1. **Admission cannot be omitted.** Take a deterministic trajectory `q_t=1-min(t,1)`, `T=1`, `tau=infinity`, `sigma_adm=1`, `d=2`, `R=M=0`, `q_0=1`, `c=0`. All stopped bounds and the strict horizon condition hold, but the target is never reached. Its admission failure has probability one, exactly as the source requires charging.
2. **The lower endpoint needs the target upper bound.** With `q_t=1-t` until a deterministic target at `tau=1/2`, `b_tail=1/2`, and other error constants zero, the correct lower endpoint is `1/2`. Replacing the target upper bound by the domain lower bound would incorrectly give `tau>=1`.
3. **Stopping at a budget crossing is not itself a proof of the stopped budget.** For jump budgets, overshoot can survive stopping. The source's requirement that the bound hold for the stopped process, including one-step targets, is essential; a favorable-event or pre-exit bound cannot be substituted.

No counterexample to the theorem with its actual stated bounds was found.

## 2. Explosion and inverse construction

The polynomial vector field has a unique local solution; the nonnegative quadrant is forward invariant and the field is cooperative there. The origin solution satisfies `l(s)>=s`, `e(s)>=2s³/3`, and the exact identity

`l(s)=s+3e(s)²/4`.

If the origin solution survives to time one, then `e(1)>=2/3`. Thereafter `e'>=9e⁴/8`, which forces explosion within another `8/(27e(1)³)<=1` time unit. If it explodes before one the desired bound is immediate. Hence `s_*<=2`. Cooperative comparison gives `b(l,e)<=s_*` for every finite nonnegative initial state, while local existence gives `b(l,e)>0`.

For `l>0`, `e'=2l²>0` permits the inverse coordinate `v`. With `u(e)=w_0=l-3e²/4`,

`u'=1/(2L²)`, `L(v)=u(v)+3v²/4`, `L'=1/(2L²)+3v/2>0`.

Moreover `L(v)>=l+3(v²-e²)/4`. Thus the inverse solution exists for all finite `v>=e`, `u` is increasing, and its integral has a finite `v^-4` tail. Its limit is finite, `L(v)` tends to infinity, and actual elapsed time is `u(v)-w_0`. Therefore `b(l,e)=u(infinity)-w_0` is the actual deterministic remaining explosion time, not a stochastic oracle.

## 3. Derivatives and boundary scope

For `l>0`, parameter differentiation is legitimate on compact parameter neighborhoods: `L` is bounded away from zero initially and has a uniform quadratic lower bound in the tail. The relevant sensitivity is

`J(v)=exp(-integral_e^v L(z)^-3 dz)`, with `0<J_infinity<1`.

At fixed `e`, `partial_l u(v)=J(v)`, so `b_l=J_infinity-1`. When `e` moves at fixed `l`, both the initial value and initial coordinate move:

`partial_e u(v)=J(v)[-3e/2-1/(2l²)]`.

Subtracting `partial_e w_0=-3e/2` yields exactly the source's `b_e`. Substitution gives

`(1+3l²e)b_l+2l²b_e=-1`.

These formulas apply for `l>0,e>=0`; at `e=0` the derivative has its one-sided physical-domain meaning, or the local smooth extension meaning. They must not be evaluated by division by zero at `l=0`.

There is a short rigorous boundary extension argument. Fix a finite boundary state `x_0=(0,e_0)` and a sufficiently small deterministic `h>0` below its explosion time. The forward flow `Phi_h(x_0)` has positive `l` and `e`. By continuous dependence, a neighborhood of `x_0` also reaches a neighborhood of that interior point. On nearby nonnegative states,

`b(x)=h+b(Phi_h(x))`.

The right side is smooth by the interior inverse construction and the smooth finite-time flow. It gives a local smooth extension of `b` to the boundary. Differentiating along the original flow at `(0,e_0)` gives the stronger boundary identity `b_l(0,e_0)=-1`. Thus the non-strict bound `|b_l|<=1` extends correctly; the strict interior inequality does not extend to `l=0`. This local argument does not provide certified computational derivative suprema.

## 4. Deterministic variance candidate and exact tail

Along the origin orbit, `L(v)=s(v)+3v²/4>=3v²/4`. Therefore

`|b_l|=1-J_infinity<=integral_e^infinity L(v)^-3 dv<=64/(135e^5)`.

Also `dl/de=1/(2l²)+3e/2<=8/(9e^4)+3e/2`. Squaring the first bound and integrating the product gives exactly

`integral_{e>=E} b_l² dl <= (4096/18225)[(8/117)E^-13+(3/16)E^-8]`.

The constants are correct: the two antiderivatives contribute `1/13` and `1/8`, respectively. The restriction `E>=1` is sufficient; the inequality itself is valid for every `E>0` on this orbit. The compact initial segment is finite because `|b_l|<=1` and `l(E)<=2+3E²/4`. For example `E=1` gives the fully explicit deterministic bound

`Sigma² <= 23946071/8529300 < 2.807508`.

This bound is only for the displayed deterministic functional. It is not an actual-chain variance, distribution, finite-N error estimate, or algorithmic certificate.

**Scope counterexample:** the sensitivity tail bound is not uniform over arbitrary `(l,e)`. At fixed `e=1`, as `l` decreases to zero, `|b_l|` tends to one, while `64/135<1`. The frozen source correctly restricts this tail argument to the origin orbit.

### Stochastic wording repair

The repair described here is present in the accepted repaired hash above; this section records the reason it was needed, not an outstanding request.

For a literal finite-noise diffusion `dX=f(X)ds+sqrt(a(X)) e_l dW`, Itô's formula gives

`d[b(X_s)+s]=(a/2)b_ll(X_s)ds+sqrt(a)b_l(X_s)dW`.

It is therefore not enough merely to justify noise in the `l` coordinate with variance `a`: the integral is evaluated along a random path and the Itô drift is present. In fact, interior differentiation gives `b_ll=3J_infinity integral J(v)L(v)^-4dv>0`, so the correction is generally nonzero.

A precise replacement is: “For a justified linear Gaussian fluctuation limit about this deterministic orbit, with noise only in `l` and local covariance `a=1+3l²e`, the candidate first-order clock variance is the displayed deterministic integral, provided the clock delta method and terminal/tail passage are proved.” Differentiating `f dot grad b=-1` shows why the linearized drift cancels in `grad b(x(s)) dot Y(s)`. Neither that fluctuation limit nor the terminal passage is established here.

The final CDF warning is also correct: if `F` is continuous and `delta_a` is a point mass, their Kolmogorov distance is `max(F(a),1-F(a))>=1/2` (using the left-limit supremum). A deterministic clock and a finite-width high-probability window are not distributional solvers.

## 5. Separate conditional cone check requested by parent

This is new conditional deterministic material, not a broader acceptance of the frozen orbit-only claim. If `e>0`, `0<c<=3/4`, and `l>=c e²`, then

`L(v)>=l+(3/4)(v²-e²)>=c v²` for `v>=e`.

Consequently `|b_l|<=1/(5c³e^5)`. Also the exact interior second derivative above gives `0<b_ll<=3/(7c⁴e^7)`. Both proposed cone estimates are correct. No claim is made that an actual process remains in this cone or that these bounds cover its one-step targets.

## 6. Explicit non-acceptances

- No verification of the actual rate2 corrector cancellation, generator residual, jump/bracket, imbalance, preparation or admission probabilities.
- No acquisition or computational-cost certificate for `b`, its derivatives, or a validated scalar solver.
- No stochastic CLT, finite-N CDF, actual continuation to clearance, or favorable-conditioned martingale theorem.
- No competitive algorithm claim; source, precision, failure and complete runtime costs remain separate obligations.

`clock_window_remaining_symbolic_checks.py` records exact rational/symbolic consistency checks and input hashes. These checks support the algebra only; the arguments above supply the existence, stopping and scope reasoning. The first scripted hash-binding attempt correctly stopped when the parent concurrently repaired the main remaining-clock file; after inspecting the full diff and verifying the historical original, the script was rebound to all three exact inputs and rerun.
