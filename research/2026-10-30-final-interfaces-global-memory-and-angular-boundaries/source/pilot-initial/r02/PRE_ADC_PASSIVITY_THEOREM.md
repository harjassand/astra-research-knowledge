# Pre-ADC memory turns a passive-field energy budget into a finite-bit response certificate

The concrete result is a transduction theorem: a signed analog accumulator with one-bit feedback can estimate a fixed physical response at rate `sqrt(V_N)/N`, where `V_N` bounds total expected exposed old-field energy. For linear input-energy growth this is `N^(-1/2)`, with no relaxation-rate assumption and no inactive windows. It requires calibrated analog memory before the comparator. That memory's range and retention are charged below. This is a mathematical construction built from ordinary sigma-delta conversion, not a demonstrated device or a claim of advantage over ordinary methods with the same operations.

## 1. Source boundary and the first failed attack

The supplied `FACTS.txt`, `P1_RECOVERY_FINAL_VISIBLE_DOM.txt`, and `P1_RECOVERY_VISIBLE_ACTIVITY.txt` were read. Their weighted passivity and corrected fresh-sign chronology are inherited at their stated internal-review scope. Their separately attached proof/program files were unavailable and were not read. The new theorem and implementation here have not received an independent scientific review.

The first attack was dense, fixed-amplitude, forward-only correlation through a conditionally unbiased 257-level ADC. It fails because unbiased rounding estimates the clipped field. Let `u_t=alpha*xi_t`, `y_t=a*alpha*xi_t+h_t`, and `mu=alpha*a`, with `xi_t` a fresh sign and `h_t` fixed before that sign. The conditional mean of the demodulated clipped sample is

```
E[xi_t clip_R(h_t+xi_t mu) | history]
    = [clip_R(h_t+mu)-clip_R(h_t-mu)]/2.
```

Persistent input can replenish memory, so the set `|h_t|>R-|mu|` need not disappear at full activity. Retaining saturation flags does not make the above equal `mu`. The executable passive all-pass example makes this failure quantitative: after 262,144 windows the fixed-range ADC has gain error `0.1418001`, with 83,542 retained saturated reads. The mean of the exact conditional clipping bias on that path is `0.1423770`. Repeated runs and increasing prefixes preserve this bias. This numerical example is a failed estimator, not an impossibility theorem against all uses of its record.

The mechanism change is to multiply the physical output by the known sign and accumulate it in analog form before applying a one-bit comparator. Quantization then contributes an endpoint state, rather than a persistent clipping bias.

## 2. Observation and physical-resource assumptions

For `t=1,...,N`, a fixed scalar incremental response `a` obeys

```
u_t = alpha xi_t,
y_t = a alpha xi_t + h_t,
|a| <= A_max,  alpha>0,  R >= alpha A_max.
```

`h_t` is measurable before the fresh independent fair sign `xi_t`. More generally its conditional law may be independent of that sign and have the same second-moment bound. The filtration can include the complete unobserved physical past; the controller need not know it. There is no state-order, mixing, decay-rate, or finite-memory assumption. The gain `a` is fixed; a gain change induced by the current sign is outside this model.

There is a warranted, deterministic bound

```
sum_t E[h_t^2] <= V_N.
```

An energy-normalized observation can obtain this from a conditional passive balance. If `|h_t|^2 <= kappa e_t` and

```
e_t <= E_t - E[E_(t+1) | H_t] + S_t + J_t,
```

where `E_t>=0`, `E[E_1]<=E0`, `S_t` bounds supplied probe energy, and `J_t` accounts for other material or apparatus energy supplied to the specimen, then

```
V_N = kappa (E0 + sum_t S_t + sum_t J_t)
```

is valid after expectation and telescoping. The sample-to-energy calibration `kappa` and incident-energy bounds are real premises. Point samples of arbitrary bandwidth do not inherit such a calibration automatically. For `S_t=S`, this is the full-activity (`p=1`) consequence of the supplied conditional balance. A two-window source theorem must be converted to this per-observation contract with its actual waveform and readout calibration. The explicit specimen below satisfies the per-window contract directly.

Known continuing power is permitted by charging `sum J_t`. An unmeasured bath is not free. A linear bound `V_N=O(N)` still gives the rate below. Unknown `V_N`, non-exogenous old fields, or state-dependent current gain do not.

The additional readout operation is:

1. A sign-controlled polarity switch forms `z_t=xi_t*y_t` in analog form, without first clipping `y_t` to the comparator output range.
2. An initialized analog accumulator and a two-level feedback DAC implement

```
s_0 = 0,
p_t = s_(t-1) + z_t,
q_t = R sign(p_t),       sign(0)=+1,
s_t = p_t - q_t.
```

3. The controller sees only the bit `q_t/R` and any overload flag. It computes

```
a_hat = sum_t q_t / (alpha N).
```

No intermediate `y_t`, `h_t`, `s_t`, population gain, or hidden-state audit enters that estimator or its radius. The polarity switch, accurate addition, DAC pulses, loading and retention are supplied operations. The plant remains the same specimen. The apparatus accumulator is initialized once and is not the unknown plant state.

## 3. Finite-horizon theorem and proof

Fix `N` and `0<delta<1`. Set

```
L = sqrt(V_N/delta),
C = R + 2 L,
beta_N = (R + 3 L)/(alpha N).
```

With probability at least `1-delta`, simultaneously:

```
max_(t<=N) |s_t| <= C,
max_(t<=N) |p_t| <= C+R,
|a_hat-a| <= beta_N.
```

A device dimensioned for post-pulse range `C` and pre-pulse range `C+R` can abstain upon an overload flag. Correct completion without an overload then has probability at least `1-delta`. Merely observing no overload is not a claim that conditional error probability remains `delta`; the statement is the unconditional joint guarantee above.

**Proof.** Put `w_t=xi_t h_t` and `M_t=sum_(i<=t) w_i`. Freshness gives a square-integrable martingale with

```
E[M_N^2] = sum_t E[h_t^2] <= V_N.
```

The weak maximal inequality for the nonnegative submartingale `M_t^2` gives

```
P(max_(t<=N)|M_t| > L) <= V_N/L^2 = delta.
```

The deterministic state bound is

```
|s_t| <= R + 2 max_(k<=t) |M_k|.                 (1)
```

To see it, suppose `s_t>R` and let `k<t` be the last index with `s_k<=R`. At every step `i=k+1,...,t`, ending above `R` forces `q_i=+R`: if the pre-pulse value were negative, subtracting `-R` would leave a value at most `R`. Thus

```
s_t = s_k + (t-k)(mu-R) + M_t-M_k
    <= R + M_t-M_k
    <= R + 2 max_(j<=t)|M_j|,
```

because `mu<=R`. The negative excursion follows using `mu>=-R`; states inside `[-R,R]` already satisfy (1). There is no assumption that individual `z_t` are in range, and no assumption of independent quantization errors.

Telescoping the actual analog recurrence gives

```
sum_t q_t = N mu + M_N - s_N.
```

On the maximal event, the absolute estimation error is at most `(L+C)/(alpha N)=beta_N`. Also `p_t=s_t+q_t`, yielding the pre-pulse range. This proves all three claims on the same event. QED.

If `V_N=kappa(E0+(S+J)N)`, a sufficient horizon for gain tolerance `epsilon` is

```
N >= 2 R/(alpha epsilon),
N >= sqrt(72 kappa E0/(delta alpha^2 epsilon^2)),
N >= 72 kappa (S+J)/(delta alpha^2 epsilon^2).
```

These convenient constants follow by reserving `epsilon/2` for `R/(alpha N)` and splitting the two variance contributions. The exact inequality `beta_N<=epsilon` is tighter. This is a finite, predetermined number of physical windows with a confidence guarantee, not a deterministic guarantee of correct operation or a known last-warning time.

## 4. Explicit passive specimen and discriminating execution

Let `r^2+g^2=1`, and select one slot of a delay ring. Each window applies

```
[x_new, y]^T = [[r,g],[g,-r]] [x_old,u]^T.
```

The ring then advances. Its exact energy identity is

```
x_new^2+y^2 = x_old^2+u^2.
```

The incremental response is `a=-r` and the old field is `h=g*x_old`. Before the fresh sign is drawn the whole old state is fixed. Conditional averaging gives

```
E[E_(t+1)|H_t] = E_t - h_t^2 + g^2 alpha^2,
```

so `V_N<=E0+alpha^2 N` is warranted without knowing `r` or the ring length. A dark coordinate retains energy 9 throughout. The full initial stored-energy allowance is 16. No specimen state is reset.

A finite-waveform mathematical realization uses energy-normalized rectangular wave packets of duration `T_wave`, amplitude `u_t/sqrt(T_wave)`, in a lossless scattering junction with delay slots of length `T_wave+T_feedback`. Initial ring packets have the same shape and timing. During the packet a calibrated signed current transducer with gain `1/sqrt(T_wave)` adds charge `xi_t*y_t`; during the following gap a finite current pulse of amplitude `R/T_feedback` subtracts the selected feedback charge. Thus no infinitely narrow feedback impulse is needed. For constant packet currents the accumulator trajectory is linear during each subwindow, so its magnitude is bounded by its endpoint magnitudes. On the theorem event the polarity switch must handle signed field amplitude up to `C/sqrt(T_wave)`, the pre-pulse accumulator range is `C+R`, and each physical window lasts at least `T_wave+T_feedback`, plus any decision/switching overhead. The transducer is an additional calibrated instrument with its own loading and power supply; the passive junction identity does not certify its energy or noise. For arbitrary supplied waveforms, endpoint bounds alone do not control unmeasured intra-window transients, and a separately justified bandwidth/peak contract is required.

The executed main case used `r=1/sqrt(2)`, one ring slot, `alpha=.7`, `R=.75`, `delta=.02`, and 262,144 windows. All compared readouts received the same specimen outputs and sign sequence. The simulation assumes their stipulated ideal loading; their internal energy is separate from specimen energy.

| Quantity | Executed or certified value |
|---|---:|
| Physical forward windows, all active | 262,144 |
| Specimen resets / passive waiting windows | 0 / 0 |
| Sigma-delta output bits / feedback pulses | 262,144 / 262,144 |
| Incident specimen energy, normalized | 128,450.56 |
| Gain estimate | -0.7077189854 |
| Certified gain radius, failure allocation .02 | 0.0414387055 |
| Audited gain error, unavailable to controller | 0.0006122042 |
| Predetermined post-pulse accumulator range | 5,069.6071 |
| Predetermined pre-pulse accumulator range | 5,070.3571 |
| Actual maximum post-pulse magnitude, audit only | 1.8517117 |
| Overload encounters in this execution | 0 |

Eight additional seeds each were executed at 65,536 windows for ring length 1, ring length 257, and `r=.999999` with ring length 97. The largest audited gain error across these 24 runs was `0.00665153`; the common certified gain radius was `0.08290107`. No overload or certificate miss occurred in these finite tests. These counts do not establish the probability theorem; its proof is above. An exhaustive algebra check over 26,244 disturbance/signal strings found no last-crossing-bound violation and a maximum telescoping residual `3.56e-15`.

A further causal energy-balance fixture stores input energy in an unobserved port and releases a large old field at a fixed late window. It checks the theorem's broader predictable-memory contract and the accumulator range cost. It is not presented as a built device, a full physical realization of every hidden operation, or a lower bound. Exact executed values are in the JSON result.

## 5. Consequence for control and record reuse

For the scalar ridge task

```
u*(a) = a b/(a^2+lambda),
```

assume `|b|/(2 sqrt(lambda))<=U`, so this unconstrained optimum is permitted. Intersect the acquired gain interval with `[-A_max,A_max]`. Evaluating the above function at the interval endpoints and at any contained `a=+/-sqrt(lambda)` computes its exact image interval. The midpoint is a command and half its length is a certified distance to the true optimum. It uses only acquired bits and public constants.

The global derivative bound `|du*/da|<=|b|/lambda` also supplies a less fixture-sensitive bound. Choosing the clipped gain estimate as a plug-in command gives distance at most `(|b|/lambda)*beta_N`; the image-interval midpoint has no larger worst-case radius. Thus with `b=.4`, `lambda=.5`, `U=.7`, the 16,384-window prefix already supports a uniform command-radius guarantee `0.13276689<.15` for every permitted scalar gain. This uses 8,028.16 normalized incident specimen energy units, 16,384 bits and pulses, and predetermined post-pulse range 1,269.1474. The zero-experiment radius is `.28284271`.

At 262,144 windows the uniform command radius is `.03315096`. The exact image interval for this particular gain record gives radius `.000249724`; this stronger value exploits proximity to a stationary point of the ridge solution and is not the general construction's rate or the main scientific consequence.

Once the gain event holds, the interval remains valid for all later scalar targets `b` and regularizers selected from that record, subject to their declared feasibility and fixed specimen gain. No new plant-energy inference is needed just to compute these commands. A new physical receiving task or a changed gain still requires its own warranted operation and calibration.

For a `d`-input, `m`-output fixed matrix, probe each coordinate direction `K` times using fresh signs and maintain `m*d` analog accumulators. With total `N=dK` observations and `sum E||h_t||^2<=V_N`, the same argument plus the strong L2 maximal inequality yields

```
||A_hat-A||_F <= [R sqrt(md)+6 sqrt(V_N/delta)]/(alpha K)
```

with probability at least `1-delta`. In detail, summing the coordinate martingale maximal second moments gives at most `4V_N`; Markov gives a bound `4V_N/delta` for their sum. The scalar endpoint bound and the triangle inequality give the display. This supplies a general reusable operator certificate, at a cost of `m*d` analog states and `mN` output bits, with no claim of dimension-free learning. Individual matrix entries must satisfy `alpha|A_ij|<=R` and their physical observation norm must have the calibrated energy bound.

Given an operator-norm gain bound `L_A`, a Frobenius radius `beta` also bounds operator error. An ordinary constrained ridge optimizer on the acquired `A_hat` then obeys

```
||u*(A_hat)-u*(A)||
 <= beta * [(L_A+||A_hat||) U+||b||]/lambda.
```

This follows from strong monotonicity and the two variational optimality inequalities on the command ball. The matrix extension is proved algebraically here; the executed tests are scalar.

## 6. The crucial instrument obligations and their cost

The one-bit digital alphabet does not make the analog apparatus cheap or arbitrarily precise. For a horizon `N`, the proven required range is `O(sqrt(V_N/delta))`. A charge or voltage state with energy `W(s)=gamma*s^2/2` consequently needs rated stored energy at least `gamma*(C+R)^2/2` to cover the stipulated range. In the main normalization, `gamma=1` would give `12,854,260.41` units. `gamma` is an actual implementation parameter; this illustrative number is not joules or a complete apparatus-work bill.

Each read requires a signed switch, an analog accumulation, a comparator decision, and one `+/-R` feedback pulse. For an ideal capacitor with the above energy convention, subtracting the pulse changes energy by `gamma*(R^2-2R|p_t|)/2`; its positive supplied part is at most `gamma R^2/2` per pulse. The main run's corresponding bound is `73,728*gamma`. Input coupling, switch losses, comparator/DAC supplies, clocking, sensing load and dark-state control are additional costs. The mathematical construction counts their operations but has not calibrated their hardware energy or timing. Its physical duration is the actual duration of `N` fully instrumented windows, including switching and feedback time, not `N` free calls.

A tolerance extension makes the retention issue explicit. Suppose the implemented loop obeys

```
q_t = R sign(s_(t-1)+mu+w_t+nu_t),
s_t = s_(t-1)+mu+w_t-q_t+eta_t,
|nu_t|<=tau,  |eta_t|<=d0,  |mu|+d0<=R.
```

The same last-crossing proof, with boundary `B0=R+tau+d0`, gives, on the same martingale event,

```
max|s_t| <= B0+2L,
|a_hat-a| <= d0/alpha + [B0+3L]/(alpha N).
```

Indeed, a step ending above `B0` forces positive feedback, since negative feedback would require a pre-pulse value at most `tau` and would leave at most `R+tau+d0`. On such an excursion the drift `mu-R+eta_t` is nonpositive. The negative excursion is analogous. The exact sum identity has the extra `sum eta_t`, bounded by `N*d0`. No independence assumption is made about these bounded calibration errors.

Uncalibrated per-window integration or feedback error therefore produces a nonvanishing error floor. For target gain accuracy `epsilon`, a sufficient calibration allocation is `d0<=alpha*epsilon_cal`, leaving the remainder to the finite-sample term. Finite precision has not been assumed away.

For a leaky accumulator `p_t=(1-ell)s_(t-1)+z_t`, both `eta_t` and `nu_t` can be bounded by `ell*C_hardware` while in range. It must satisfy `alpha A_max+ell*C_hardware<=R`, the capacity inequality `C_hardware>=R+2ell*C_hardware+2L`, and the required calibration budget `ell*C_hardware/alpha<=epsilon_cal`. Because `C_hardware` grows like `sqrt(N)`, retention must improve when a longer horizon is purchased. The unknown specimen relaxation has been replaced by a specified, calibrated apparatus retention requirement, which is the unresolved physical enabling obligation. Equivalent gain, feedback-amplitude, leakage, timing and thermal-noise errors must actually be brought under this or another proved contract.

## 7. Strongest ordinary alternatives and exact contribution scope

An ordinary sigma-delta correlator using exactly this sign switch, integrator and feedback operation has exactly the same estimator and guarantee. This construction offers no advantage over it. Sigma-delta conversion is established engineering: the primary paper by Medina, Rombouts and Hernandez describes first-order integrator/comparator/feedback loops and input-range/overload limitations. The present mathematical step is the last-crossing energy-to-confidence bridge for unbounded individual predictable old fields, rather than a new converter architecture. External priority for that precise bridge has not been determined. [Medina et al., primary paper](https://arxiv.org/html/2311.06983v3)

Physical adjoint stochastic approximation is also established. Aarnoudse and Oomen obtain randomized gradient approximations through dedicated experiments, including waveform reversal in SISO and multichannel coding. Their model-free MIMO result prevents a claim that obtaining a physical gradient or using random signs is the discovery. The present forward-only identification route pays dimension-dependent acquisition costs instead of supplying a cheap new general adjoint. [Aarnoudse and Oomen, published primary source](https://pure.tue.nl/ws/files/193833656/Model_Free_Learning_for_Massive_MIMO_Systems_Stochastic_Approximation_Adjoint_Iterative_Learning_Control.pdf)

For the globally LTI contractive test specimen, a strong ordinary competitor is already better in its certificate: use a wider calibrated 257-level ADC, fresh stochastic rounding, and ordinary signed correlation. Passivity bounds the impulse-response squared sum by one. Independent Rademacher inputs then imply, by a sub-Gaussian tail and a union bound, that

```
R_wide = alpha A_max + sqrt(E0)
         + alpha sqrt(2 log(2N/delta_range))
```

covers every raw sample with probability at least `1-delta_range`. The initial-state response is bounded by `sqrt(E0)` and the randomized zero-state old response has variance proxy at most `alpha^2`. Let `Delta=2R_wide/256`. An ideal unbounded-grid stochastic rounding error is bounded by `Delta` and has the required complete conditional zero mean; on the no-clipping event it matches this ADC. A union of the no-clipping event, a second-moment bound on the signed old-field sum, and Azuma's bound on rounding errors gives

```
beta_wide = [sqrt(V_N/delta_memory)
             + Delta sqrt(2N log(2/delta_ADC))]/(alpha N).
```

The executed main comparison allocates `.005+.01+.005=.02`, uses range `8.954263` (11.94 times the sigma-delta feedback amplitude), and obtains gain radius `.02020813`, audited error `.000565861`, and no saturated reads. It pays 9 fixed-width bits per read and needs no sigma-delta accumulator. This demonstrates why the narrow clipping estimator is not the strongest ordinary competitor. The extra globally LTI premise supplies the concentration of raw output; the central theorem only needs predictable old fields and their total second moment.

More generally, finite-sample identification without mixing is established; Simchowitz et al. analyze ordinary least squares on observed linear-state trajectories under their excitation/noise premises. Their result is not the hidden-state passive finite-bit theorem proved here, but excludes the broad novelty claim of learning without mixing. [Simchowitz et al., primary paper](https://proceedings.mlr.press/v75/simchowitz18a/simchowitz18a.pdf)

The established opening is limited but concrete: a warranted passive-field energy budget can be transduced into a finite-horizon, finite-output-bit operator certificate by supplying calibrated analog accumulation before quantization, without waiting for specimen relaxation. The original fixed memoryless ADC interface has not gained this extra operation for free. A practical benefit, a complete apparatus energy advantage, hardware qualification, or civilisation-scale capability has not been established.

## 8. Actual passive indistinguishability and an initial-energy lower bound

This section specifies physical instances and operations, rather than treating arbitrary additive noise as a physical impossibility result. Both results use the same finite, lossless delay-ring scattering construction as Section 4, with delay exactly `N`. Consequently every initial coordinate is exposed once and no newly injected field returns within the `N`-window horizon. The allowed operation is one forward port observation per window, with `|u_t|<=alpha`, no reset, no internal-state access and no reverse-port operation. Arbitrary computation and full signed analog output are allowed. The bounds therefore also cover any digitization of that record. They do not prohibit an algorithm with extra physical access or a longer observation horizon.

### Exact pair against deterministic policies

Consider any deterministic adaptive policy. Let `u_t^0` be its commands along the all-zero analog observation history. Define

```
c = sqrt(E0/(E0+N alpha^2)),
a_plus = +c,   a_minus = -c,
g = sqrt(1-c^2),
r_plus = -a_plus,  r_minus = -a_minus,
x_t^plus = -a_plus u_t^0/g,
x_t^minus = -a_minus u_t^0/g.
```

These are two fixed preloaded physical states chosen before execution, not a state adjusted after each experiment. Each has energy

```
sum_t (x_t^plus)^2 = sum_t (x_t^minus)^2
    = [E0/(N alpha^2)] sum_t (u_t^0)^2 <= E0.
```

Induction on the policy history gives exactly the same observations in both instances:

```
y_t^plus = a_plus u_t^0+g x_t^plus = 0,
y_t^minus = a_minus u_t^0+g x_t^minus = 0.
```

Each exposed coordinate becomes `u_t^0/g`, identically in both instances. Energy conservation holds at every window. No deterministic estimate can have gain distance less than `c` on both instances. For the scalar ridge task its worst-case command radius is at least

```
c |b|/(c^2+lambda).
```

The executable concrete pair uses `N=64`, `alpha=.7`, `E0=16`. The gains are `+/-0.5812381937`, every hidden initial delay coordinate is respectively `-/+.5`, and all 64 full analog observations are exactly zero in floating-point execution as well as in the algebra. The two optimal commands are `+/-0.2774943635`. Both start with energy 16 and end with energy 47.36. The maximum numerical energy-identity residual is `1.43e-14`.

This obstruction excludes private fresh randomization: an admissible initial state cannot be preloaded to cancel a sign drawn independently after the state has been prepared. This is a specific operational reason why freshness can matter. It is not an impossibility result against the randomized construction in Section 3 or against all no-mixing identification.

### Statistical pair allowing arbitrary private randomized adaptive policies

Fix `N>=8`, `E0>0`, and define

```
Delta = min(1/2, sqrt(E0)/(8 alpha N)),
a_plus = +Delta/2,   a_minus = -Delta/2,
g = sqrt(1-Delta^2/4).
```

In each instance choose the initial delay coordinates from

```
x ~ Normal(0, E0/(4N) I_N), conditioned on ||x||^2<=E0.
```

Every resulting actual initial state satisfies the same deterministic energy allowance. An unobserved dark coordinate may fill the remaining energy to make total initial energy exactly `E0`; it does not change the observations. The two couplers have `r=-a` and the same `g`. This is a finite family of admissible passive specimens and states, with no continuously powered stochastic source. The distributions are statistical mixtures over fixed admissible initial states; exact deterministic transcript identity is asserted only for the preceding deterministic-policy pair.

Before conditioning, the observations of any randomized adaptive bounded-input policy satisfy

```
y_t = a u_t + g x_t,
g x_t are independent Normal(0, sigma^2),
sigma^2 = g^2 E0/(4N).
```

The controller's private coins can be included in the transcript. The same policy is used under both hypotheses, and the independent unused initial coordinate remains Gaussian conditional on that transcript's past. The chain rule for Gaussian likelihood ratios gives

```
KL(P_plus || P_minus)
   = [Delta^2/(2 sigma^2)] E_plus[sum_t u_t^2]
   <= 2 Delta^2 alpha^2 N^2/(g^2 E0).
```

Pinsker's inequality therefore bounds the total variation of the complete analog transcripts by `Delta alpha N/(g sqrt(E0))`. The removed initial-state prior mass is

```
eta = P(chi_square_N>4N)
    <= exp[-N(3-log(4))/2].
```

Conditioning changes each hypothesis transcript law by total variation at most `eta` (apply the same physical experiment to the conditioned prior). The triangle inequality yields the explicit admissible-instance bound

```
TV(P_plus_conditioned, P_minus_conditioned)
   <= Delta alpha N/(g sqrt(E0)) + 2 eta.        (2)
```

Any estimate achieving gain error strictly less than `Delta/2` supplies a correct sign test. Its average failure probability over the two physical priors is therefore at least `(1-TV)/2`. By averaging, at least one actual admissible fixed initial state in one of the two gain instances has that failure probability. For `N>=8`, (2) is below `.133`, giving failure at least `.433`; in particular a uniform `.98` confidence claim at such a radius is impossible. The order `sqrt(E0)/(alpha N)` of the positive theorem's initial-energy term cannot be removed in this operation class, although these constants and the dependence on `delta` are not a minimax match. No optimality claim is made for the separate `sqrt(S/N)` term, accumulator range, bit count, or full apparatus cost.

At the executed `N=64`, `E0=16`, `alpha=.7`, the gains are `+/-0.0055803571`. Formula (2) gives TV at most `.1250019464` and unavoidable average estimation failure at least `.4374990268` for radius below `.0055803571`. A full-analog likelihood-ratio test on 20,000 samples per instance had average error `.44995`, consistent with the unconditioned Gaussian exact value `.4502610`; the removed prior mass is bounded by `3.75e-23`. The passive energy identities were checked on those actual finite vectors. Numerical agreement is a discriminating check, while the uniform adaptive-policy claim follows from the likelihood proof.

## Artifacts

* `check_pre_adc_accumulation.py`: complete executable construction, matched alternatives, persistent-state fixtures, and algebra discrimination.
* `PRE_ADC_ACCUMULATION_RESULTS.json`: actual generated numerical outputs, including measured costs, audits, failures, and exact confidence constants.
* This file: theorem, proof, expanded operation contract, calibrated-error extension, generalization and primary-source comparison.
