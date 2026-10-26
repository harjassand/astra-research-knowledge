# ASTRA Pro3 — Self-calibrating active experimental interfaces and task-specific acquisition

**Date:** 27 October 2026. Original conditional construction and executed exact-rational controls. Continue from `ASTRA_PRO3_ACQUIRED_PORT_ELIMINATION_AND_ACTIVE_INTERFACES.md` (previous local handoff). The scripts in this directory are the actual producers of the results; independent verification and isolated replay are separately executable. There is no physical apparatus.

## 1. Why the next attack matters

The preceding active one-port experiment turned a hidden positive-definite block into measurable quadratic forms by changing a known shunt. But **knowing the actual shunt gain** was a strong, previously unacquired instrument contract. If the gain is wrong, applying the previous inverse formula is wrong. The present attack both weakens that interface assumption and exposes tasks that do not need gain calibration at all.

The source is fixed real symmetric positive definite, with hidden `r×r` stiffness `T` and `I <= T <= 3I`. Equivalently `H=T^{-1}` obeys `(1/3)I <= H <= I`. The original known observed-port block is `B=[[2,1],[1,2]]`, whose unloaded single-port boundary reaction is `b=3/2`. A configured native shunt is `J_v = κ λ(e_0-v)(e_0-v)^T`, where `λ>0` is the **nominal** commanded strength and `κ>0` is an *unknown physical gain shared by all experiments in the fixed-gain contract*. The measurement clamps the boundary port and returns **one scalar**. The known `B`, linearity, passivity, spectra, ability to configure the rank-one shunt, and gain stability are supplied premises; the native scalar reaction is independently charged every time.

Schur elimination, not access to hidden internal coordinates, gives the true response

\[
y_\lambda(v)=b+\frac{\kappa\lambda}{1+\kappa\lambda v^\top H v}.\tag{1}\]

Let `h=1/κ`, `x=1/λ`, and `z=1/(y-b)`. Because the native reaction is strictly above `b` under the contract,

\[
 z(v,x)=v^\top H v+h x.\tag{2}
\]

**This is the acquired operation language**: every configured scalar reaction is one *linear* functional of the shared unknown `(H,h)`, after the observable reciprocal transformation. This does not assume access to an imaginary native matrix-vector oracle. Formula (1) was independently checked against native Schur reductions in the producer programs.

## 2. Self-calibration theorem and exact calls

Let `d=r(r+1)/2`. With known baseline `b`, take the same nonzero `v` at distinct strengths `λ_1, λ_2`. Then

\[
 h=\frac{z_1-z_2}{1/\lambda_1-1/\lambda_2},\quad
 q(v)=z_1-h/\lambda_1.\tag{3}
\]

One additional scalar experiment along each of the remaining `d-1` basis/pair-sum quadratic-form directions identifies all entries of `H` by polarization. Total **`d+1` scalar calls**. A grounded reference `v=0`, when physically supported, is an alternative gain calibration; it yields `z=h/λ` without probing the hidden block.

**Exact optimality, deterministic adaptive experiments included.** Along any fixed exact transcript, subsequent chosen `v_i,λ_i` are fixed. Write `θ=(vech(H),h)` of dimension `d+1` and observation rows `a_i=(vech_sym(v_iv_i^T),1/λ_i)`. Fewer than `d+1` scalar reports leave a nonzero affine null direction `δθ`. At an interior source and gain, small positive and negative perturbations along `δθ` preserve every observed `z_i`, every native reaction, the spectral/source contract, and the adaptive continuation. The null vector cannot have `δH=0`, since all `1/λ_i>0`. Therefore even identification of `H` alone is impossible from `d` readings in general. The canonical `d+1` programme is query-optimal for the declared native interface. In its executed form, the pair-sum coupling vectors have norm `sqrt(2)`, while coordinate couplings have norm one; a unit-norm cap can instead use rescaled pair sums at the **same number** of calls with a larger finite-noise error. That additional executed resource trade-off is recorded in Section 5.

If the baseline `b` is also unknown but stable, three strengths at the **same nonzero vector** identify `b,h,q(v)` before the other `d-1` quadratic-form probes. Let `x_i=1/λ_i`, `y_i` be three distinct reaction values and set

\[
 A=(y_2-y_1)(x_2-x_3),\quad B=(y_3-y_2)(x_1-x_2),\quad
 b=\frac{B y_1-A y_3}{B-A}.\tag{4}
\]

The denominator is nonzero in the positive-gain, distinct-strength regime. Equations (3) then recover `h,q(v)`. This costs **`d+2` scalar calls**. Joint recovery of the `d` source coefficients, gain and baseline cannot be universal with fewer observations: for `k<=d`, the linear reciprocal constraints at fixed `b` have a nonzero source/instrument kernel; for `k=d+1`, either that kernel survives or full-row-rank linear reciprocal equations admit nearby solutions as `b` varies. The latter generically change `H`, and in all cases prevent full source-and-interface identification. A separate exact one-hidden-port/two-reading source pair demonstrates the lower limit concretely. The unknown baseline is genuinely an independent unknown of the source/instrument; no old known calibration call is silently free.

**Executed acquisition:** for `r=2,3,5`, the known-baseline unknown-gain plans required **4,7,16** native scalar configured measurements; unknown baseline and gain required **5,8,17**. All six reconstruct `H`, `T`, `κ`, and (when unknown) `b` exactly. Each programme then predicted eight newly specified shunt configurations plus a later nonsymmetric hidden controller without learner source calls. There are 57 total acquired scalar reports across the six alternative tests and 48 independent *checker-only* future shunt evaluations. They are not a single 57-call physical history.

## 3. Stronger task-specific theorem: indefinite questions need no calibration

Suppose a later task, known when selecting its next experiments, requests the linear scalar `L_C=tr(C H)` for an arbitrary real symmetric matrix `C`. Baseline `b` is known, gain `κ` is unknown but common, and the probe vectors may have arbitrary real amplitudes of Euclidean norm `<=1` (including `0` where allowed), with positive nominal strengths. The task can be recovered exactly iff its coefficient row `(C,0)` lies in the span of measured rows `(v_i v_i^T,1/λ_i)`, because the source/gain class contains an open parameter neighbourhood.

Let `s=rank(C)`. The exact minimum number of scalar native reactions for one nonzero task is

\[
N^*(C)=\begin{cases}
s, & C\text{ indefinite},\\
s+1, & C\text{ positive or negative semidefinite}.
\end{cases}\tag{5}
\]

For `C=0`, no calls are needed.

**Proof of lower bounds.** If `C=∑_{i=1}^k α_i v_i v_i^T`, then `s<=k`, regardless of adaptivity, by source ambiguity along a fixed transcript. The nuisance coefficient additionally requires `∑ α_i/λ_i=0`. If `k=s` and `C` is nonzero semidefinite, the `s` nonzero `v_i` must be linearly independent. Sylvester's law of inertia then forces all `α_i` to share the same sign. Since `λ_i>0`, the nuisance sum cannot vanish. Thus `s+1` calls are necessary. For indefinite `C`, the rank lower bound `s` remains.

**Attainability.** Spectrally decompose `C` into `p>0` positive and `q>0` negative rank-one eigenpieces. Choose a sufficiently large `L>0`, scale each positive eigenvector probe so its decoding weight is `qL`, and each negative probe so its weight is `-pL`. Probe norms may all be `<=1` and the weights sum to `pqL-qpL=0`. One fixed nominal strength suffices. For semidefinite `C`, use `s` spectral probes and one `v=0` gain-reference probe, or replace the latter by a different amplitude on one already used nonzero probe. Spectral probes may be irrational for generic rational `C`: the exact theorem assumes real probes; executable rational tasks use rational probes and weights. Any finite-precision approximation needs a separate error certificate.

**Executed rational task controls:** for `r=4`, indefinites of inertias `(1,1),(2,1),(1,2),(2,2)` required respectively `2,3,3,4` calls, while semidefinites with ranks `1,3,2` required respectively `2,4,3`. All seven returned exact task values with a stable unknown physical gain. A separate hidden two-port control computed `H_12` from just two **rational unit vectors** `(3/5,+4/5)` and `(3/5,-4/5)`:

\[
 H_{12}=\frac{25}{48}\left[z(3/5,4/5)-z(3/5,-4/5)\right].\tag{6}
\]

No calibration is needed because the unknown `h` cancels. For 0.001-bounded native noise, this two-reading procedure certified `H_12 ∈ [-0.05290052,-0.04968468]`, containing the actual `-4/79`.

**Crucial scope:** task-specific procedures above require the ability to perform their two-or-more measurements *when the task is selected*, or must have pre-acquired those probe forms. They are not zero-new-call predictions from an already expired instrument. If only nonnegative fixed-dose or only unit-norm probes are allowed, formula (5) does not automatically apply. Full calibrated tomography, once acquired and retained, supports entirely unknown later tasks with no more calls. An equally informed retaining optimizer achieves the same optimal call counts.

## 4. A hidden calibration gauge, and a decisive unstable-gain failure

If every permitted probe has `||v||=1` at one fixed nominal `λ`, then

\[
 (H,h)\mapsto(H+\delta I,h-\lambda\delta)\tag{7}
\]

preserves **every possible reading**, for small `δ` within the strict spectral/gain interior. An executed two-source pair shares four representative unit-probe reports and differs in `tr(H)`; equation (7) proves indistinguishability across the *entire* unit-sphere query interface, not merely those four samples. An anisotropy or off-diagonal contrast survives the gauge, but absolute isotropic response does not. Changing probe amplitude or nominal strength breaks it.

A stronger failure occurs if the inverse hardware gain can vary arbitrarily with the experiment. Fix `H` and `H'=H+ε I`; for any allowed configuration `(v,λ)`, choose

\[
 h'(v,\lambda)=h-\lambda\epsilon\|v\|^2.\tag{8}
\]

Then `v^T H'v+h'/λ=v^T Hv+h/λ` identically. In the executed counterexample, `ε=1/100`, `1/4<=λ<=4`, `||v||^2<=2`, and `h=4/5`. Every changed inverse gain stays in `[0.72,0.8]`, hence within the declared per-reading admissible range `[2/3,5/4]`. Both `H` and `H'` remain within `[I/3,I]`. Thus **even infinitely many adaptively chosen configurations cannot distinguish the two sources under an unconstrained per-configuration gain**, because the instrument can hide source changes in its gain changes. The script executes fifteen exact matching controls; the identity proves all configurations in the declared domain.

This prevents treating gain stability as an experimentally acquired fact merely because a finite calibration record fits.

## 5. Exact noisy joint history, future procedures, and design

Assume an absolute bounded error `|ŷ_i-y_i|<=η`, known baseline `b`, and `ŷ_i-b>η`. The exact transformed observation band is

\[
 \ell_i=\frac1{\hat y_i-b+\eta}
 \le v_i^T H v_i+h/\lambda_i
 \le\frac1{\hat y_i-b-\eta}=u_i.\tag{9}
\]

Together with `I/3<=H<=I` and `h∈[h_min,h_max]`, these constraints are an **exact spectrahedral consistency family** for the entire noisy history, not separate fitted source estimates. A future reaction remains the decreasing reciprocal transform of the positive linear functional `v^THv+h/λ`; optimising this functional over the shared feasible set yields its sharp endpoint interval. A future nonlinear controller remains coupled through the same `(H,h)` and may require an additional certified optimization.

A simpler implemented compiler linearly inverts four independent transformed readings, propagates the full observation box with correct coefficient signs, and checks spectral feasibility. In all three two-port noise experiments, **all 16 corners of the reciprocal-data box** meet the spectral and gain contracts. By convexity every point in the box is feasible. Accordingly, in these particular fixtures the interval propagation is not just sound: for each of 24 subsequently specified scalar reaction predictions, the compiler constructs an attainable consistent source/gain witness at **each endpoint**. The 16-corner property is checked, not assumed for arbitrary sources. The three later skew-controller estimates use conservative norm-error bounds and are not claimed sharp.

**A genuinely different physical amplitude constraint.** The preceding four-reaction programmes allow one pair-sum coupling vector of norm `sqrt(2)`. A separate executed control limits **every** hidden coupling vector to norm at most one by replacing `e_1+e_2` with `(e_1+e_2)/2`, without increasing the four-call budget. All 16 transformed box corners remain compatible, hence the later reaction intervals are still sharp, but weakened excitation enlarges their mean widths. For the selected, extreme, and close strength designs the ratios of constrained to original interval width are respectively **2.488**, **2.646**, and **3.398**. This is a real distinction between algebraic sufficiency and resource-bounded useful precision, not a free normalisation of hardware inputs.

### Source-oblivious hardware precision design

For `v=e_1`, the source spectral contract gives `q=v^T Hv<=1`; gain contract `4/5<=κ<=3/2` gives `h<=5/4`. Set `x=1/λ`, `Z(x)=1+(5/4)x` and require `η Z(x)<1`. With `\hat z=1/(\hat y-b)` and actual `z=q+hx`, every admissible measurement obeys

\[
 |\hat z-z|\le E(x):=\frac{\eta Z(x)^2}{1-\eta Z(x)}.\tag{10}
\]

This follows from the reciprocal identity and the worst permitted source/gain; it does **not** use the checker-hidden `T` or `κ`. For two strengths with `x_1>x_2`, the affine-intercept estimate of `q` has the certified bound

\[
 |\hat q-q|\le
 \frac{x_2 E(x_1)+x_1E(x_2)}{x_1-x_2}.\tag{11}
\]

Over the 120 strength pairs drawn from `λ=j/4`, `j=1,...,16`, an exact rational exhaustive comparison of **this bound** chooses `(λ_1,λ_2)=(1/2,4)` with worst-case error bound **0.00372748**. The extreme-range pair `(1/4,4)` has bound **0.00425440**, and the nearby pair `(1,5/4)` has bound **0.04033575**. This is catalogue-optimal for the specified certified bound, not globally minimax under the raw observation model. Lower nominal strength increases reciprocal-noise amplification; the widest separation alone is not the right engineering objective.

After adding the same two other hidden-form readings, each four-scalar native plan was executed with actual signed deterministic sensor perturbations inside `±0.001`. The resulting mean widths for eight later scalar reactions were respectively **0.00629180**, **0.00724379**, and **0.01703863** for the selected, extreme-range, and nearby plans. All are **sharp** over their corresponding exact full noisy histories by the 16-corner test. The independent source-aware validator made 24 later checks; the learner made no calls for those requests.

### Falsifying a claimed fixed-gain interface

At one fixed `v`, `z=1/(y-b)` must be affine in `x=1/λ`. Three distinct strengths permit a source-free collinearity test. An intentionally perturbed three-reading record has disjoint inverse-noise bands from every affine line through its two endpoint bands; the exact rational nonoverlap margin is approximately **0.0296153**. Therefore no stable common gain and response coefficient can explain those reports under the stated error allowance. Passing such a finite test cannot *prove* global gain stability; it can only reject a contract when violated at observed configurations.

## 6. Repair when instrument gain drifts with time

A meaningful intermediate contract is `|h(t)-h(s)|<=ν|t-s|` for the **inverse gain** `h=1/κ`, while the hidden `H` remains fixed. A grounded reference experiment `v=0` at time `s` reports `y-b=κ(s)λ`, hence obtains `h(s)=λ/(y-b)` exactly in the idealized noiseless sensor. If a known nonzero reference form was already calibrated, it can replace grounding.

Given charged reference times `s_j` and readings `h(s_j)`, every unmeasured gain obeys the complete Lipschitz point interval

\[
\max_j[h(s_j)-\nu|t-s_j|]\le h(t)\le
\min_j[h(s_j)+\nu|t-s_j|].\tag{12}
\]

For a science reading `z(v,t)=v^THv+h(t)/λ`, subtract the right and left gain bounds to obtain sound bounds on the required hidden quadratic form. The upper and lower scalar Lipschitz envelopes are attained by compatible time-varying gains. A subsequent common-`H` matrix reconstruction may further tighten these bounds; the implemented interval arithmetic is sound but not generally sharp for multi-form tasks.

**Executed drift control:** `h(t)=4/5+(1/25)t(1-t)`, satisfying the supplied rate `ν=1/25`. Three hidden science measurements occur at times `1/4,1/2,3/4`. With reference readings at times `0,1`, a later unforeseen `H_12` question has a certified interval width **0.04**. Adding a third reference at time `1/2`, with no repeated science calls, reduces its width to **0.01**. The reference costs are **2 versus 3 scalar calls**; both programmes have **three** science scalar calls. The physical ability to perform two configurations in the same idealized time epoch is stipulated; hardware switching delay would consume additional drift budget.

**Matching sharp floor:** If endpoint inverse gains are identical and the only science observation is at midpoint, two gain histories `h_±(t)=h_0±ν min(t,1-t)` obey the same reference readings. Two source inverse blocks differing by `±(ν/2)e_1e_1^T` then produce the same midpoint science report (with opposite gain tents) but disagree on `H_11` by `ν`. The worst-case error radius is at least **ν/2 = 0.02** in the executed rate contract. The script reconstructs both SPD source witnesses and native identical responses. Historical reference density cannot beat this floor without a closer calibration time or a stronger drift premise.

## 7. Equally informed alternatives, limits, and highest-value next attack

A strong ordinary system-identification method supplied the same native readings, gain-stability class, spectral bounds, allowed configurations, and retention rights can apply the same reciprocal transformation and tie every theorem. Classical optimal experimental design, reciprocity, impedance shunt calibration, polarization, signed measurements, spectral matrix completion and Lipschitz time interpolation have substantial antecedents. **No priority, architecture superiority, working hardware, measured physical law, or civilization-level discovery is established.** Actual configurable shunts may perturb the supposedly fixed source, violate linearity, inject unmodelled hysteresis, or exceed hardware energy/bandwidth budgets. Those are unacquired interfaces, not an excuse to omit them from cost.

The previous known-gain acquisition required `d` native scalar readings. Learning an unknown common gain costs exactly **one** additional reading; learning the baseline too costs **two**. But the better compiler sometimes **does not calibrate anything**: indefinite scientific contrasts admit exact `rank(C)`-call gain-free procedures. Noisy joint consistency is an explicit spectrahedron, and three-strength repetitions can falsify one false hardware assumption. Under drift, bracketing reference measurements supply precision with a matching time-dependent information limit.

The next research target is physical-source and shunt **co-drift**, where calibration actions themselves perturb source parameters. A useful result would identify an experimentally enforceable common-source contract or a task-specific invariant surviving both drifts, under explicit intervention cost. The current evidence does not solve this.

## 8. Reproducible experiments and primary contextual sources

Producer scripts and their corresponding actual JSON outputs:

1. `active_shunt_self_calibration.py` / `active_shunt_self_calibration_results.json`: six exact acquisitions, unknown-baseline indistinguishability, late shunt and controller operations.
2. `task_specific_gain_quotient.py` / `task_specific_gain_quotient_results.json`: calibration-free tasks, intrinsic gauge, bounded-noise two-reading contrast, arbitrary-gain-drift unidentifiability.
3. `noisy_self_calibrating_design.py` / `noisy_self_calibrating_design_results.json`: 120-pair public design selection, exact noisy joint boxes, 48 attaining endpoint witnesses, late tasks and contract-falsifying record.
4. `time_bracketed_gain_drift.py` / `time_bracketed_gain_drift_results.json`: time-coherent reference calibration, retained later coupling, matching drift floor.
5. `gain_free_rank_procedures.py` / `gain_free_rank_procedures_results.json`: seven exact-rational rank-inertia task procedures.
6. `unit_amplitude_control.py` / `unit_amplitude_control_results.json`: norm-one native coupling constraints, same call counts and reduced excitation, with 48 further endpoint source witnesses in three exact noisy histories.

`verify_research.py` independently reconstructs the saved identities, full-source alternatives, observation bands, source-attaining extrema, and the public design search without importing the experiment producer scripts. `clean_replay.py` executes the six producers in an isolated workspace with their fixed primary helper and checks the JSON files byte-for-byte. Their results and hashes are retained alongside this note.

Relevant antecedents/context: the previous user-provided primary note `ASTRA_PRO3_ACQUIRED_PORT_ELIMINATION_AND_ACTIVE_INTERFACES.md`, Sherman–Morrison and Schur complement, classical polarisation and linear inverse problems, and literature on source calibration and optimal impedance experiment design, e.g. Ciucci et al. (2011), *Electrochimica Acta* 56, 5416–5434, DOI `10.1016/j.electacta.2011.02.098`, and Orazem & Tribollet (2017), *Electrochemical Impedance Spectroscopy*, experimental design chapter. The present result claims no historical priority over those or other instrumentation literature.
