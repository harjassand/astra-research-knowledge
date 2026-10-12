# CRAY: experimentally acquired flux coordinates for certified kinetic design

**Date:** 12 October 2026.  
**Status:** research candidate, not an independently verified or priority-cleared breakthrough.  
**Central task:** select simultaneous state-specific transition rates in an unknown kinetic network to maximise a bounded stationary output, acquiring only source indicators, that output, and labelled intervention-event counts.  
**Principal surviving construction:** a measured flux-response basis and a small global optimisation/certification problem.  
**Principal unresolved escalation:** acquiring a sufficiently informative basis and certifying the intervention structure for experimentally observable, heterogeneous states without learning the whole hidden system.

## 0. What this report does and does not establish

This note contains self-contained derivations of an exact measured-data control polytope; regenerative acquisition; a strength-independent event-count concentration bound; rate saturation; a finite-data outer LP and global-regret certificate; and a mixed-probe continuation that can remove a particular rare-calibration obstruction. Code executes the main acquisition-to-certificate workflow, rather than assuming its response matrix as an oracle.

These results are not a claim of new finite Markov response theory, a new occupation-measure LP, a new resetting principle, or a new general concept of control from data. Those ingredients have substantial prior art. The proposed contribution is their particular flux-calibrated interface, quantitative acquisition accounting, and certifiable composition. Whether this is a historically original and substantial contribution is unresolved. The comparison does not establish superiority to all structured or semi-Markov control methods.

The mathematical model is operational as a black-box simulation interface. No physical apparatus, real chemical system, hardware detector, or calibration procedure was tested. A source that is one state in the mathematics need not be one state in an experimental readout. Explicit five-state counterexamples show that this distinction can invalidate the desired scientific consequence even with unlimited isolated-control data.

The complete package is a local handoff, not a GitHub update. Previous Ising and Gaussian research is preserved separately and is not a premise. Astra HEAD read in this run was `5ab60ff49af6da752fe8452031996410a50f00b4`. Selective searches of Astra and `openai/math` supplied context, not mathematical premises. No archived theorem is assumed correct by inheritance.

## 1. Screening and the chosen obstruction

Four directions were compared at the mechanism level:

1. Goal-directed inverse inference: avoiding full reconstruction is already an established objective of goal-oriented experimental design. No new uniformly stable information acquisition theorem emerged here.
2. In-situ inverse design: physical adjoint/backpropagation measurements already exist in specialised systems; a new operation must overcome, not rename, reciprocity or experimental-access assumptions.
3. Certification of long-time stochastic predictions: generator/Poisson identities and sum-of-squares bounds are established tools; obtaining a useful global residual bound remains difficult for an unknown hidden network.
4. Joint kinetic intervention design: the stationary response is nonlinear in control rates, but linear in actual injected probability flux. This offers a concrete route from a small experimental table to a global design decision.

The chosen question is therefore: can a scientist optimise several simultaneous interventions without reconstructing hidden states, waiting for unassisted mixing, or estimating an extremely small occupation probability to high relative accuracy?

The answer derived here is positive for a precise resettable, state-selective interface, with acquisition costs explicitly depending on reset speed and probe informativeness. It is not a positive answer for arbitrary kinetic interventions.

## 2. Contract and notation

Use column-generator convention. The unknown finite-state system has

\[
Q(u)=Q_0+\sum_{j=1}^k u_j b_j e_{a_j}^{T},\qquad
b_j=\nu_j-e_{a_j},\qquad 0\le u_j\le U_j.
\]

Here `a_1,...,a_k` are distinct source states, `nu_j` are fixed destination probability laws, and all off-diagonal rates are nonnegative. The destination laws and the hidden generator are not supplied to inference. The same actuator must implement the same destination law under every control combination. Rates are additive in this microscopic sense, not merely independent settings on an instrument panel.

Assume all generators considered have a unique stationary probability law and a one-dimensional normalised stationary kernel. Irreducibility suffices. The common-reset assumption below also suffices even when some states are unreachable from the preparation.

Only the following are observed: source indicators `1_{X=a_i}`, a reward `f(X)` in `[0,1]`, and labels of added-transition events. No full state labels, microscopic transition matrix, mean first-passage matrix, or Poisson solution are given to the inference routine. Reward acquisition itself must be cheap enough for the intended application; it is not made free by the theorem.

The output is a rate vector and an interval certificate

\[
J(u_{\rm out})\ge L,\qquad \sup_{0\le u\le U}J(u)\le U_{\rm cert},
\quad J(u)=f^T\pi(u).
\]

Thus `U_cert-L` bounds global regret, not just a gradient or a fitted residual. Objectives that are linear combinations of several measured bounded outputs can reuse the experimental table. Average intervention-flux budgets add linear constraints. A budget on the sum of raw rate settings is generally not linear in the flux variables and is not included automatically.

For concrete acquisition assume

\[
Q_0=L_0+\rho(\nu\mathbf1^T-I),\quad \rho>0,
\]

where the background `L_0` has exit rate at most `Lambda_b`. The reset law `nu` must be reproducibly preparable and the reset remains in the target dynamics. It need not be explicitly reconstructed. Set

\[
\Lambda=\Lambda_b+\rho,\qquad \ell=\Lambda/\rho.
\]

For strength-independent event work additionally assume the **ejection condition**: every `nu_j` is supported outside the entire active source set `S={a_1,...,a_k}`. This condition is not needed for the exact polytope, but is load-bearing for the acquisition and saturation bounds stated below.

## 3. Exact single-probe compilation

Measure a baseline and, for each `j`, a probe with only rate `u_j=s_j>0` enabled. Let their laws be `pi^0` and `pi^j`. Record

\[
z_i^j=\pi^j(a_i),\quad w^j=f^T\pi^j,\quad
r_j=s_j\pi^j(a_j)>0.
\]

The last quantity is the mean labelled-event flux, not an assumed high-precision source population. Define

\[
F_{ij}=z_i^j-z_i^0,\qquad d_j=w^j-w^0.
\]

### Theorem 1: measured control polytope

The full achievable source/output set is represented exactly by

\[
\alpha\ge0,\quad z=z^0+F\alpha,\quad 0\le z\le1,
\qquad r_j\alpha_j\le U_j z_j,
\]

with output

\[
J=w^0+d^T\alpha.
\]

Recover an implementing control by

\[
u_j=r_j\alpha_j/z_j
\]

when `z_j>0`, and by `u_j=0` when `z_j=0`. The latter case forces `alpha_j=0`.

**Proof.** Let `h_j` be the zero-mass solution of `Q_0 h_j=-b_j`; these vectors are proof devices and are never supplied to the algorithm. Stationarity gives

\[
\pi^j-\pi^0=r_j h_j,
\qquad
\pi(u)-\pi^0=\sum_j u_j\pi(u)(a_j)h_j.
\]

Taking `alpha_j=u_j pi(u)(a_j)/r_j` proves the forward inclusion.

Conversely, given a feasible point, construct the possibly signed vector

\[
\widetilde\pi=\pi^0+\sum_j\alpha_j(\pi^j-\pi^0).
\]

It has mass one and its source coordinates are `z`. The recovered rates satisfy `u_j z_j=r_j alpha_j`, hence `Q(u) tilde_pi=0`. Uniqueness of the normalised stationary kernel forces `tilde_pi=pi(u)`, in particular nonnegativity of every unobserved coordinate. Thus no exponentially large collection of hidden positivity constraints is missing. This proves the converse and the output identity. □

Maximising the displayed linear objective is a global LP. It is not a local-response approximation. The theorem is closely related to existing finite perturbation identities and to elimination in occupation-measure control LPs; it is not an assertion that those underlying ideas are new.

## 4. Acquisition by independent finite episodes

For each probe, prepare `nu`, evolve under `L_0+sum u_j B_j`, and stop at an independent `T~Exp(rho)`. Record the endpoint source indicators, reward, and intervention counts `C_j` before stopping. Prepare a new independent episode and repeat.

The endpoint law is

\[
\rho\int_0^\infty e^{-\rho t}e^{(L_0+\sum u_jB_j)t}\nu\,dt=\pi(u).
\]

Multiplication by the resolvent verifies the stationary equation directly. Independent episodes therefore give independent stationary observations without burn-in. This is the established resetting/resolvent identity, not a novel resetting claim.

Also,

\[
\rho\mathbb E C_j
=\rho\int_0^\infty e^{-\rho t}u_j\Pr(X_t=a_j)\,dt
=u_j\pi(u)(a_j).
\]

Thus `rho` times mean tagged-event count directly estimates the required flux.

**Task boundary.** The endpoint law is stationary for the system *with this reset*. It is also a discounted occupation law for the unreset process. The procedure does not infer the unreset stationary law or arbitrarily long metastable kinetics. Making `rho` small lengthens the true experimental horizon and worsens the cost bounds.

### Why count events rather than infer their flux from rare occupancy?

For one probe at strength `s`, an endpoint estimator `s 1_{X=a}` has mean `r` and variance

\[
\operatorname{Var}(s1_{X=a})=sr-r^2.
\]

When `r` remains of ordinary size but `s` is huge, source endpoint observations become rare and this estimator becomes expensive. In contrast, tagged counts admit the uniform bound below. No claim is made that event counters or traffic measurements themselves were invented here; their role in the compiled acquisition contract is the point.

### Theorem 2: strength-independent count concentration

Under ejection, between successive controlled jumps there is at least one background jump. Consequently

\[
C_{\rm total}\le N_{\rm background}+1.
\]

Uniformising the background at rate `Lambda_b` and competing against the independent reset clock shows that the right-hand side is dominated by a positive geometric variable `G` of mean `ell=Lambda/rho`. This remains true when background uniformisation includes null events. In particular,

\[
\mathbb E C_j^m\le\mathbb E G^{\overline m}=m!\ell^m\quad(m\ge1).
\]

The rising-factorial identity follows by summing the geometric series. For `0<t<1/ell`, expansion of the exponential and `log(1+x)<=x` give

\[
\log\mathbb E e^{t(C_j-\mathbb EC_j)}
\le {t^2\ell^2\over1-t\ell}.
\]

For the lower tail, `e^{-x}<=1-x+x^2/2` for `x>=0` gives

\[
\log\mathbb E e^{-t(C_j-\mathbb EC_j)}\le t^2\ell^2.
\]

Chernoff optimisation yields, for `n` independent episodes and confidence parameter `t`,

\[
|\widehat r_j-r_j|
\le\Lambda\left(2\sqrt{t/n}+t/n\right)
\]

except with probability at most `2 exp(-t)`. Bounded endpoints satisfy Hoeffding radius `sqrt(t/(2n))`. For `k+1` single probes, take `t>=log(2D/delta)` with `D=(k+1)^2+k`; the union bound controls the whole acquired table. For arbitrary mixed probes replace the number of flux estimates by `k^2`.

Expected controlled-event work per episode is at most `ell`; expected background work is at most `Lambda_b/rho`; expected duration is exactly `1/rho`. The total stationary added flux is bounded by

\[
\sum_j u_j\pi(u)(a_j)\le\Lambda.
\]

This gives a useful extra linear inequality `sum r_j alpha_j<=Lambda` in the compiled LP.

## 5. Rate saturation and finite rate precision

### Theorem 3: uniform cap error

Let the sources be distinct and satisfy ejection, and let `v_j=min(u_j,K)`. Then for every `f` in `[0,1]`,

\[
|J(u)-J(v)|\le {\Lambda(1+\Lambda/\rho)\over K}.
\]

**Proof.** For the capped generator take a stationary Poisson solution

\[
Q(v)^T h=f-J(v)\mathbf1.
\]

Two copies of the process can couple at their next common reset. Therefore the oscillation of `h` is at most `1/rho`. At any source whose control has been capped, its local Poisson equation reads

\[
K(\nu_j^Th-h(a_j))+(Q_0^Th)(a_j)=f(a_j)-J(v).
\]

The baseline exit rate is at most `Lambda`, so

\[
|\nu_j^Th-h(a_j)|\le (1+\Lambda/\rho)/K.
\]

Pair the Poisson equation with `pi(u)` and use `Q(u)pi(u)=0`. The performance difference is bounded by the sum of these local differences weighted by `(u_j-K)pi(u)(a_j)` over capped channels. That weight sum is at most the total controlled flux, hence at most `Lambda`. □

This does not extend unchanged to multiple different actuators sharing the same source, where the local equation no longer isolates the capped channel. It also does not give strength-independent event work when controls jump directly between active sources.

For an error budget `epsilon_cap`, take

\[
K=\Lambda(1+\Lambda/\rho)/\epsilon_{\rm cap},
\]

and replace every bound by `min(U_j,K)`. Reading the binary input `U` still costs its input length, but numerical strength beyond the cap need not be implemented. The dependence on `rho^-1` and the other parameters is not removed.

For rate rounding, the same Poisson argument gives the conservative bound

\[
|J(u)-J(v)|\le {1\over\rho}\sum_j|u_j-v_j|.
\]

Rational rates within `epsilon_round rho/k` in each coordinate therefore suffice. Under distinct-source control the bound can be sharpened to an infinity-norm rate difference, but the implementation does not need that improvement.

## 6. Finite data, global upper bounds, and independent validation

Suppose every endpoint mean has error at most `eta`, every calibrated flux has error at most `eta_r`, and

\[
r_j^-=\widehat r_j-\eta_r>0.
\]

When this positivity is not certified, the implementation refuses the single-probe compilation. It does not substitute an arbitrary small denominator.

Let `A=sum alpha_j`. The following LP is an outer approximation of all true achievable designs in the capped box:

\[
\alpha\ge0,\quad0\le z\le1,
\]
\[
|z_i-\widehat z_i^0-\widehat F_{i\cdot}\alpha|
\le\eta(1+2A),
\]
\[
r_j^-\alpha_j\le K_jz_j,\qquad\sum_jr_j^-\alpha_j\le\Lambda.
\]

Its objective is the upper expression

\[
\widehat w^0+\widehat d^T\alpha+\eta(1+2A).
\]

Each absolute-value inequality is two linear inequalities. The factors account for the common baseline and the difference of two noisy probe means. Correlations in these differences are not assumed away; the simultaneous coordinate event suffices.

Solve this LP, propose an implementing rate using `min(K_j,hat_r_j alpha_j/z_j)`, and independently validate its actual output on fresh episodes. Add the cap allowance to the global upper bound. The difference between that upper bound and the validation lower bound is a global-regret certificate on the joint confidence event, regardless of whether the numerical proposal is especially good.

### A complete conservative sample-to-regret bound

For an exactly feasible outer-LP point with objective within `xi` of its optimum, define `A=sum alpha`. Let

\[
\widetilde\pi=\pi^0+\sum_j\alpha_j(\pi^j-\pi^0).
\]

Its source coordinates differ from the LP's `z` by at most `2 eta(1+2A)` each. The recovered rates satisfy

\[
\sum_j|u_jz_j-r_j\alpha_j|\le2\eta_r A.
\]

Hence the zero-mass stationary residual has total-variation norm at most

\[
\|Q(u)\widetilde\pi\|_{\rm TV}
\le 2kK\eta(1+2A)+2\eta_r A.
\]

The common-reset semigroup contracts zero-mass signed measures at rate `rho`, so its inverse on that space has norm at most `1/rho`. This proves

\[
J^*_{\rm capped}-J(u)
\le 2\eta(1+2A)(1+kK/\rho)+2\eta_r A/\rho+\xi.
\]

If the true minimum isolated calibration flux is `r_*>0` and `eta_r<=r_*/4`, then `A<=2 Lambda/r_*`. For `n>=t`, the count radius is at most `3 Lambda sqrt(t/n)`. Thus it is sufficient to choose `n` so that

\[
\left[2(1+4\Lambda/r_*)(1+kK/\rho)
+12\Lambda^2/(\rho r_*)\right]\sqrt{t/n}+\xi
\]

fits the design-error budget, as well as `n>=t(12 Lambda/r_*)^2` to resolve the fluxes. These are conservative polynomial resource bounds in the displayed numerical parameters, not a claim of practical optimality or a theorem polynomial in input bits alone. `r_*` can be exponentially small. Its lower bound is measured; the algorithm need not be supplied a magical value. Sequential doubling requires a summable allocation of failure probabilities across rounds.

### Exact arithmetic for the upper certificate

The primary integer benchmark builds the confidence LP directly from integer measurement counts and rational radii. A floating LP solver proposes multipliers. They are converted to nonnegative rational numbers and checked without trusting solver feasibility or optimality tolerances.

For `max c0+c^T x`, `A x<=b`, `0<=x<=M`, every `y>=0` gives the valid upper bound

\[
c_0+b^Ty+\sum_j M_j\max\{0,c_j-(A^Ty)_j\}.
\]

The last term repairs any dual residual exactly. The final upper, validation lower, and regret bound are also retained as fractions. In `rational_confidence.py`, a positive rational Taylor sum proves the chosen integer upper bound on the logarithm, and integer-square comparisons prove each square-root upper bound. This closes the numerical LP/radius arithmetic in the main benchmark; it does not certify a physical model.

## 7. Mixed probes: a different acquisition operation

The isolated protocol can be disastrously uninformative when one intervention exposes the source of another. Rather than treating this as an unavoidable denominator, use genuinely mixed calibration settings.

For `k` arbitrary probe vectors `u^(m)`, measure the entire flux vector

\[
R_{jm}=u_j^{(m)}\pi^{(m)}(a_j)
\]

and baseline-subtracted source/output changes `D` and `d`. If `H` contains the baseline source response columns and `g` the output response row, stationarity gives

\[
D=HR,\qquad d^T=gR.
\]

For an invertible measured flux basis, exact data give

\[
H=DR^{-1},\qquad g=d^TR^{-1}.
\]

Now optimise directly in physical fluxes `beta`:

\[
\beta\ge0,\quad z=z^0+H\beta,\quad0\le z\le1,
\quad\beta_j\le K_jz_j,\quad\mathbf1^T\beta\le\Lambda,
\]

with objective `w0+g beta`. Recover `u_j=beta_j/z_j`. The proof of converse feasibility is the same stationary-kernel argument as before. Mixture coefficients `R^-1 beta` may have either sign; treating them as nonnegative would be incorrect.

### Observable stability certificate

Under the reset assumption every entry of the true source/output response columns has magnitude at most `1/rho`, because

\[
h_j=(\rho I-L_0)^{-1}(\nu_j-e_{a_j}).
\]

Let the noisy measured flux matrix `hat_R` be invertible and define the observable quantity `kappa=||hat_R^-1||_1`. Set `hat_H=hat_D hat_R^-1`. Since

\[
\widehat D-H\widehat R=(\widehat D-D)-H(\widehat R-R),
\]

entrywise source/output coefficient error is bounded by

\[
\eta_H=(2\eta+k\eta_r/\rho)\kappa.
\]

This bound does not assume a supplied inverse or even that the true flux matrix was certified invertible. A badly conditioned measured matrix simply gives an uninformative error bound. A confidence LP follows by replacing source equalities with

\[
|z_i-\widehat z_i^0-\widehat H_{i\cdot}\beta|
\le\eta+\eta_H\mathbf1^T\beta
\]

and adding the same allowance to the objective. For an approximately optimal feasible point the conservative regret bound is

\[
2(\eta+\eta_H\Lambda)(1+kK/\rho)+\xi.
\]

This is a measured-data condition, not a free response oracle. However, finding well-conditioned and sufficiently precise mixed probes for every hidden network is not solved here. Fixed random probes, or an exponentially large search of all corners, must not be relabelled a polynomial acquisition theorem.

### A rare-pathway test

The extra fixture has two distinct microscopic source states. Background access from source 1 to source 2 is `2^-30`. Control 1 instead ejects to a bridge which reaches source 2 at rate 1; control 2 ejects to the output state. Reset rate is 1. Both controls therefore satisfy the precise source and ejection assumptions.

At rate 100, probing control 2 alone gives true flux approximately `9.2210e-10`, so 300,000 episodes contain only `0.0002766` expected tagged events. Probes `(100,0)` and `(100,100)` instead acquire

\[
\widehat R\approx
\begin{pmatrix}
0.9899633&0.9899133\\0&0.4899633
\end{pmatrix},\qquad
\|\widehat R^{-1}\|_1\approx4.08184.
\]

The mixed second-channel true flux is approximately `0.490148`. No source-preparation oracle or hidden generator was used for this acquisition. There were 900,000 total episodes including baseline.

The conservative coefficient error was about `0.1989`; the resulting global upper bound was 1. This is an explicit failure to obtain a useful certificate at that data budget, not a certified optimisation success. Twenty separately generated exact-data mixed-probe cases did match full-model LP optima, with maximum floating error about `2.082e-14`.

## 8. Resource accounting

Let `n` be calibration episodes per setting, `n_val` validation episodes, and `E=(k+1)n+n_val` for the isolated protocol.

- **Acquisition settings:** `k+1` plus independent validation. Mixed exploration may require more settings; all attempted settings must be charged.
- **Episodes:** the displayed Hoeffding/geometric bounds and the minimum observed isolated flux, or measured mixed-basis conditioning, determine precision cost. A few settings do not imply a few samples.
- **Physical time:** expectation `E/rho + E C_prep + C_cal` in a serial device, where preparation and calibration must be costed for the actual apparatus. Independent exponential episode durations have an Erlang tail, so high-probability serial horizon is also controlled. No hardware values for `C_prep` or `C_cal` are claimed.
- **Event work:** expected background events at most `E Lambda_b/rho`, controlled events at most `E Lambda/rho`. Reset/readout operations number `E`. Per-event detector bandwidth and processing are actual costs. Removing ejection can invalidate this bound.
- **Storage at inference:** `O(k^2)` accumulated statistics and the small LP, with counter bit lengths `O(log E)` on ordinary bounded-count or high-probability truncation events. Raw trajectories are not required. The hidden simulator or physical system still stores/embodies its hidden state.
- **LP and linear algebra:** polynomial arithmetic in `k` and rational input/data bit lengths; standard dense linear algebra uses cubic operations. No claim that every rational LP is solved by the prototype in strongly polynomial time is made.
- **Randomness and rate precision:** the rational simulator samples embedded competing clocks with unbiased integer draws. Each race uses a number of bits proportional to the binary encoding length of the relevant rational total rate. It does not enumerate a numerical number of null control events proportional to a huge rate. The benchmark uses seeded Python pseudorandom bits for reproducibility; exact distribution statements are under the usual independent-unbiased-bit model.
- **Continuous time:** the integer simulator does not need to generate an exponential waiting time to obtain endpoint and event-count laws. It records expected physical duration separately. The earlier floating simulator generated waiting times as diagnostics.
- **Output:** `k` rational control rates, reward bounds, and certificate fractions; at least `Omega(k)` writing cost. No full stationary vector is output.
- **Input acquisition:** rate settings, the reset clock, source-selective actuator semantics, and event labelling are specified by the assay interface. They are exact in the simulator, not inferred from a hidden transition matrix. A physical application still needs calibration/structural evidence for them. Unknown acquisition costs are not replaced by zero.

In particular, neither a slow reset nor a rarely activated calibration direction is hidden inside a nominal `poly(k)` assertion. No unconditional, hidden-state-count-independent polynomial physical-time theorem is claimed for arbitrary systems.

## 9. Executed evidence

### Exact-data algebra and comparator

`benchmark.py` generated 40 distinct hidden networks with 2–7 controls and 25–88 states. It checked 480 held-out control vectors against direct stationary solves. Maximum prediction discrepancy was `7.772e-16`; the reduced optimiser and the full occupation-measure LP differed by at most `8.394e-14`. Forty rate-cap comparisons passed their proved bounds. These are floating finite tests, not proof verification.

The known-model comparator is a full occupation-measure LP in `(pi,beta)`:

\[
(L_0-\rho I)\pi+B\beta=-\rho\nu,
\quad\beta_j\le U_j\pi(a_j),\quad\pi,\beta\ge0.
\]

It uses the hidden generator because it is a truth/comparison backend. The acquisition algorithm never calls it.

### Primary integer acquisition-to-certificate benchmark

Hidden seed `714032`, 160 states, 4 controls, background/reset rates both 1. Original rate bounds are `10^6` in each coordinate; all are capped at 600 with a proved objective allowance `0.01`.

Five settings used 800,000 episodes each; independent validation used 400,000. Total: **4,400,000 episodes**. The inferred rates were exactly `(600,0,600,0)`. The confidence budget was split into `0.005` for calibration and `0.005` for validation.

The rationally checked report gave:

| Quantity | Value |
|---|---:|
| Validation output mean | 0.402150 |
| Achieved-output lower bound | 0.399411387212 |
| Capped optimum upper bound | 0.42622375867738244 |
| Original optimum upper bound | 0.4362237586773824 |
| Global regret upper bound | 0.036812371465382424 |
| Known-model optimum, truth check | 0.40947512662712 |
| True value of proposed controls, truth check | 0.40088373713108943 |
| Actual regret, truth check | 0.008591389496030555 |

The rational regret bound is preserved as

`1863738001023519661778016174661577827 / 50628034186174068481327104000000000000`.

The confidence event was checked against hidden-model truth and held for this fixture. Nominal 99% confidence is conditional on the stated stochastic and actuator model, not a claim of 99% certainty about a real device.

The integer simulator used about 4.459 s for calibration and 0.506 s for validation on this run; the small LP took about 0.00255 s and the exact dual check about 0.000536 s. This is not a compute-matched superiority claim. The separate full-model LP benchmark took about 0.00573 s once the generator was supplied, much faster than experimental acquisition. The relevant potential advantage is access, not beating that solve on the toy model.

Expected accumulated physical duration is **4,400,000 time units**, not five time units. This exact backend did not sample a realised duration. It processed 4,397,869 background events and 1,098,768 controlled events; competing-race integers used at most 10 bits for these settings. Reset preparation/readout and real detector costs are additional.

The earlier floating simulator results are retained in `results.json`; an earlier integer run using float-proposed confidence radii is explicitly historical. The final main report is `integer_results.json`. Replaying the same seed with improved radius arithmetic is not a new independent experiment.

### Measurement comparison at huge rate

At rate `10^8`, 200,000 independent episodes yielded zero endpoint hits at the controlled source but 50,736 tagged intervention events. Endpoint-based flux estimation was 0; tagged-count estimation was 0.25368; hidden truth was 0.2552192709361038. The exact race integers needed 27 bits, not `10^8` event steps. At rates 1, 100, and 10,000 the same test records both estimates and event work. This is a diagnostic of the changed measurement statistic, not an optimal-estimator lower bound.

## 10. Falsification and limits of scientific transfer

### 10.1 A pooled source is not a microscopic source

Two hidden source states have different unforced exit rates, 0 and 3, to an output state. Reset rate is 1 into an equal mixture of the sources. A knob adds rate `theta` to both exits. Aggregate source occupancy is

\[
z(\theta)={1/2\over1+\theta}+{1/2\over4+\theta}.
\]

The one-source formula inferred at strengths 0 and 1 is wrong at strength 10 by approximately `0.0106043`. The control matrix has rank two, not one. No sampling error causes this failure.

### 10.2 Even every isolated experiment can be insufficient under affine controls

There are states `0,1,2,success,failure`, reset to 0 at rate 1. Control 1 changes the first hidden flag and control 2 the second. In model A:

- channel 1: `0->1`, `2->success`;
- channel 2: `0->2`, `1->success`.

Model B replaces `success` by `failure` on the second transition in each channel. A fixed output detector is 1 at success and 0 elsewhere. The two observable source sets are `{0,2}` and `{0,1}`; event labels are the same.

Both generators are affine sums of the controls. The entire observable path law under baseline or either control in isolation is identical in the two models, for every isolated strength: success and failure are both unreachable. Nevertheless, at equal joint rate `s`, model A has output

\[
1-{2\over1+s}+{1\over1+2s},
\]

while model B has output 0. At `s=100` the gap is approximately **0.985173**.

Therefore isolated-control data cannot certify the needed microscopic source structure. This counterexample is tiny; large hidden dimension is not required. Testing a few mixed settings can falsify a bad model, but does not establish an unrestricted uniform guarantee.

### 10.3 Instrument cross-talk

A hidden generator term `u1*u2*C` vanishes on all isolated probes. In the three-state fixture it changes the unit-rate joint output from `1/2` to `1/11` when its coefficient is 9. Physical additivity needs independent evidence; it does not follow from isolated fits.

### 10.4 Fast controlled loops

Two active states jumping directly to one another at rate `M`, with reset rate 1, generate `M` controlled events per episode in expectation. The claimed numerical-strength-independent event cost fails without ejection.

### 10.5 Truly rare calibration is not solved by counting alone

In the mixed-probe fixture, the isolated second channel is reached at probability of order `2^-30` per episode. Two possible second-channel destination laws differ only after such an event. A coupling then shows that `n` isolated episodes have distinguishability at most of order `n 2^-30`. Constant-confidence identification from those probes needs order `2^30` episodes. Tagged counts remove the small-occupation penalty of a *fast but frequently traversed* channel, not the cost of a genuinely rare visit. The mixed intervention changes the visit probability; that is a different operation.

### 10.6 Structural mismatch has a quantitative price, but the price must be acquired

Suppose an ideal model and actual model share the reset and differ by generators `E(u)`, with

\[
\sup_{u,x}{1\over2}\|E(u)e_x\|_1\le\zeta.
\]

A Poisson argument gives a uniform output difference at most `zeta/rho`. Thus an ideal global-regret certificate can transfer with an additional `2 zeta/rho` allowance, if its calibration data correspond to the ideal model or are separately debiased/bounded. This is not a way to assume `zeta`: obtaining a uniform, output-relevant structural error bound from the permitted physical observations is a central unsolved acquisition requirement. The note does not silently apply this target-transfer statement to noisy calibration of the actual model.

## 11. Priority and specialised comparisons

- Bao and Liang, *Nonlinear Response Identities and Bounds for Nonequilibrium Steady States*, arXiv:2412.19602v6, already derive exact finite-perturbation identities and model-free reconstruction of a full single-parameter response curve. The response algebra here is not a new substitute for their work.
- Guo and Song, *Discounted continuous-time constrained Markov decision processes in Polish spaces*, arXiv:1201.0089, develop occupation-measure LP methods in a much broader control setting. The full-model comparator uses this established type of optimisation. Our small LP eliminates hidden coordinates using acquired response/flux data; no general LP invention is claimed.
- Sutton, Precup, and Singh, *Between MDPs and semi-MDPs*, 1999, establish the options framework. Decision-node/first-passage reductions can also avoid representing every hidden transient state when richer event-path access is available. A separation from the strongest such methods has not been proved.
- Established data-driven control represents feasible system behaviour in experimental data coordinates; this predates the present work. The stationary flux parameterisation is a different contract from ordinary finite-horizon LTI data, but the high-level idea is not new.
- Resetting renewal identities and output-oriented inversion are also existing tools. Resetting a real process changes its target stationary law; it is not a universal shortcut to its original equilibrium.

The proper comparison is thus narrower than 'full reconstruction versus our new method'. The candidate seeks an endpoint-and-tagged-event acquisition interface with a global finite-data certificate, not a universal computational advantage over all existing control and inference methods.

## 12. Exact outstanding proof and capability gates

**P1 — Priority:** determine whether the measured stationary-flux LP, including finite-probe composition and its acquisition/certification analysis, already appears in Markov perturbation, event-based control, behavioural control, or structured MDP literature. Current searches are insufficient for a historical-originality claim.

**P2 — Informative experiments:** prove an adaptive mixed-intervention exploration theorem under an experimentally testable coverage condition. It must charge the work needed to obtain a stable flux basis, rather than assume an inverse or good smallest singular value. The rare-pathway fixture shows possible leverage, not a general theorem.

**P3 — Structural acquisition:** develop an operational test or physical intervention that makes a low-dimensional controlled-generator image valid for observable heterogeneous states, with a measured uniform residual. The affine five-state counterexample rules out deriving this from isolated data alone. Possible next attacks include mixed-control challenge design under bounded latent rank, or deliberate re-preparation of source ensembles with fully charged access; neither is established here.

**P4 — Nonvacuous robust certification:** tighten the mixed-probe uncertainty optimisation while preserving joint measurement dependence and acquired confidence. The initial mixed fixture has an uninformative upper bound of 1 despite obtaining an informative mean response. A small training error is not a substitute.

**P5 — Physical demonstration:** identify an actual resettable assay or computing service whose source, destination, reset, and counting operations match the stated interface, then measure calibration, bandwidth, preparation, energy, and wall-clock costs. Synthetic rate inputs do not discharge this gate.

**P6 — Independent validation:** external proof review or formalisation and compute/access-matched comparisons remain absent. Floating agreement and exact LP arithmetic are not general proof certification.

The strongest continuation is therefore not another constant improvement in the LP. It is acquisition of a certified useful intervention basis, especially for experimentally coarse states, and a proof that the resulting certificate is nonvacuous at a realistic sample and physical-time budget.

## Sources selectively read

Access date: 2026-10-12. URLs are retained for audit, not as endorsements of every claim in a source.

1. Attia, Alexanderian, Saibaba, goal-oriented experimental design: https://arxiv.org/abs/1802.06517
2. Bao and Liang, finite nonlinear Markov response, v6: https://arxiv.org/html/2412.19602v6
3. Lucarini, equation-free response: https://arxiv.org/html/2502.07908v2
4. Guo and Song, occupation-measure CTMDP LP: https://arxiv.org/abs/1201.0089
5. Sutton, Precup, Singh, semi-Markov options: https://www.sciencedirect.com/science/article/pii/S0004370299000521
6. Keidar et al., resetting framework and renewal identities: https://arxiv.org/html/2607.16474v1
7. Data-driven predictive control in a stochastic setting: https://www.sciencedirect.com/science/article/pii/S0005109823001139
8. System representation and optimal control in input-output data space: https://www.sciencedirect.com/science/article/abs/pii/S1474667017316105
9. Nilim and El Ghaoui, robust MDPs: https://people.eecs.berkeley.edu/~elghaoui/pubs_rob_mdp.html

These are context/comparison sources. Every mathematical assertion made specifically for the proposed interface is derived in this note; no broad theorem from a research-memory repository is silently imported.


## Additional finite rational audit and accounting notice

`exact_algebra_audit.py` executed 120 exact rational assertions across 12 five-state
fixtures. It checked the full-vector response identity, source/output identities,
and the LP-selected corner against all four two-control corners. For this
rank-one-per-source model, the objective as a function of one rate with other rates
fixed is fractional linear with a positive denominator; its derivative has fixed
sign or is zero. Replacing coordinates successively by an appropriate endpoint
therefore proves the existence of a corner optimum. These finite equalities do
not constitute a proof of the general theorem or an independent review.

For a physical device the energy budget must also include preparation/reset energy,
background operation, intervention events, readout, and control hardware. With
known per-operation upper costs the event/time bounds above translate to a total
energy bound. No such costs were measured here; no physical energy advantage is
claimed. The integer simulator's state memory and seeded random generator remain
resources of that simulator, not resources erased by the small inference LP.
