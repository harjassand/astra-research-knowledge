# Astra Pro3 — Acquire a causal memory law from a reconfigurable boundary instrument

27 October 2026. New conditional mathematics, original source-to-experiment integrations, exact-rational executable controls, and decisive indistinguishability counterexamples. This continues the supplied `ASTRA_PRO3_CODRIFT_EXPERIMENT_SYNTHESIS.md` and the self-calibrating active-interface construction. It does not replace their proofs and does not claim new mathematical priority. **Source assumptions and source-acquired knowledge are always separated.**

## 1. The problem and the physically charged observation interface

The preceding experiments acquired one-step intervention carryover, assuming a specific linear dependence on the immediately preceding shunt. That model transfers poorly to an unforeseen *sequence* of interventions. The new target is to retain a finite causal response representation which, once acquired, can execute a new sequence or digital control algorithm after the source becomes unavailable.

The physical native instrument is still a configured scalar Schur boundary reaction, not direct access to a hidden Hessian. For a positive 2-port hidden inverse stiffness `H_t=diag(q_t,3/5)`, unknown positive inverse gain `h_t`, and applied shunt strength `lambda_t=1+u_t`, the full augmented stiffness is

`S=diag([[2,1],[1,2]],H_t^{-1}) +(lambda_t/h_t)(e0-e2)(e0-e2)^T`.

The native output is `R_t = S_00 - S_0,I S_I,I^{-1} S_I,0`. Whole-matrix Schur elimination, **not** an invented direct-response oracle, is performed in `causal_memory_primitives.py`. It yields

\[
 R_t=\frac32+\frac{1}{q_t+h_t/\lambda_t},\qquad
 z_t=\frac{1}{R_t-3/2}=q_t+\frac{h_t}{\lambda_t}.\tag{1}
\]

The boundary baseline `3/2` and ability to issue positive strength commands are supplied. The native reaction includes the physical source, shunt, and instrument gain. A raw reaction error must be converted into reciprocal error before any later bound is applied. For `z<=Z` and raw absolute error `eta` with `eta Z<1`, a conservative conversion is `eta Z^2/(1-eta Z)`.

**Causal intervention model.** Let `u_t=lambda_t-1 in [-1/5,1/5]`. The hidden response for the first construction is

\[
 q_t=q_t^{(0)}+\sum_{j=0}^{t-1}g_j u_{t-1-j}.\tag{2}
\]

The nuisance `q_t^(0)` and `h_t` may vary *arbitrarily* with time; unlike the previous co-drift theorem neither is promised affine. However, sham and treated trials must be reproducible at corresponding elapsed times: same baseline, gain, boundary baseline and initial state, apart from their commanded intervention history. The physical source, memory, and instrument must remain in the source's declared operating domain. The hidden causal kernel is time invariant and additive in the intervention departures—another **supplied contract**. There is no learned guarantee of unrestricted physical stationarity or perfect reset.

### Matched-pulse difference identifies causal impulse values

In two synchronized trials, use one pulse `u_0=delta=1/5` versus no pulse, followed by the same strength `lambda_t=1` at each time `t>=1`. Measure each trial at times `1,2,...,N`. Then for every `j=0,...,N-1`,

\[
 \boxed{g_j=\frac{z_{j+1}^{pulse}-z_{j+1}^{sham}}{\delta}.}\tag{3}
\]

This cancels *both* `q^(0)_(j+1)` and `h_(j+1)` without fitting or assuming either time trajectory. It also eliminates the current nominal shunt contribution because the current setting is identical in both trials. Each `g_j` costs two scalar readouts, but successive values are sampled during **two continuous experimental runs**, not `2N` separately reset experiments. The initial intervention and one state reset are still physically charged. A finite record cannot itself establish reproducibility of the reset.

## 2. Conditional all-future theorem for finite-dimensional causal memory

**Supplied source class.** Assume `g_k=c^T A^k b` for a real stable state matrix with minimal reachable/observable dimension `r`. For a single-input single-output minimal realization, the `r x r` Hankel matrix `H_r=(g_{i+j})_(0<=i,j<r)` is nonsingular: it factors as the product of the `r`-step observability and controllability matrices. No state coordinates or individual eigenmodes are supplied to the learner.

**Theorem (finite acquisition of an infinite causal kernel).** The `2r` exact Markov coefficients `g_0,...,g_(2r-1)` determine the whole infinite sequence. Solve

\[
 H_r\alpha=(g_r,...,g_{2r-1})^T.\tag{4}
\]

Cayley–Hamilton gives the recurrence

\[
 \boxed{g_{k+r}=\sum_{j=0}^{r-1}\alpha_jg_{k+j}\quad(k\ge0).}\tag{5}
\]

The recurrence uniquely determines every later `g_k`, which compiles the differential response to any later command sequence as the causal convolution in (2). The result also supports specified *digital* feedback programmes whose actions depend on earlier **differential** responses, with an explicit actuator resolution. It does not predict the unknown absolute raw reaction or the physical kinetics of a controller not in this discrete-time source contract.

**Why this is not just a numerical fit.** The proof uses the exact Hankel factorization and the source dimension contract. If the retained Hankel is singular or measurement errors are nonzero, (4) is not silently promoted to an exact theorem. A fixed minimal order is not inferred from six numerical values.

**Generic minimum.** A generic real SISO `r`-mode impulse law with distinct poles and nonzero residues has `2r` independent local real parameters. Its first `2r` Markov coefficients have Jacobian equal to a confluent Vandermonde-type matrix of nonzero determinant. With fewer scalar impulse constraints, generic distinct source parameters remain compatible with an adaptive transcript; a changed future response separates them. Therefore `2r` independent scalar impulse values are generically necessary for *complete* impulse-law identification in this class. This is **not** a minimum theorem about number of physical trials, bits returned, arbitrary future individual scalar tasks, stronger source promises, or native hardware interfaces.

**Executed source.** A synthetic three-mode response has poles `(3/4,1/4,-1/2)` and residues `(1/10,1/12,1/15)`; these parameters are available to the independent checker, **not** to the acquisition recurrence solver. The six acquired coefficients were

`(1/4,1/16,5/64,9/256,37/1024,89/4096)`.

The observed Hankel determinant was `1/8192`, and the independently calculated six-parameter Prony Jacobian determinant was `225/8388608`. The learner obtained

\[
 \boxed{g_{k+3}=-\frac{3}{32}g_k+\frac{5}{16}g_{k+1}+\frac12g_{k+2}.}\tag{6}
\]

Twelve raw native Schur reaction readings were made over two matched trial histories, with six identical-time comparisons. A separately implemented latent-state checker agreed *exactly* on two unseen 48-step intervention sequences. A new 36-step specified digital-feedback programme driven by differential reaction feedback agreed exactly. Its controller is a known software update rule, not an inferred physical controller. Selected native Schur checker evaluations verified that the differential outputs agree with the independent latent-state checker. New learner acquisition calls for these later tasks: **zero**.

## 3. Precision-aware transfer without inventing a noise-free recurrence

Suppose the two reciprocal readings at each elapsed time are each known within deterministic absolute error `epsilon` (errors may be adversarial and correlated). Then acquired impulse centers obey

\[
 |\widehat g_j-g_j|\le\delta_g=2\epsilon/|\delta|.\tag{7}
\]

Write `Hhat` for the first `r x r` measured Hankel and `bhat` for the measured continuation. Put `L=||Hhat^{-1}||_infty`. If

\[
 \theta=r\delta_gL<1,\tag{8}
\]

then **every compatible true Hankel is invertible**, with `||H^{-1}||_infty <= L/(1-theta)`. Let `alphahat=Hhat^{-1} bhat`. Directly from the perturbed linear system,

\[
 \boxed{||\alpha-\widehat\alpha||_\infty\le
 \frac{L\delta_g(1+||\widehat\alpha||_1)}{1-r\delta_gL}=\Delta_\alpha.}\tag{9}
\]

This is a valid coefficient enclosure even for correlated sensor errors. It is not asserted sharp for the full nonlinear rank-constrained consistency family.

If there is also an independently justified stable envelope `|g_k|<=M rho^k`, the following recurrence propagates certified future impulse uncertainty, with initial center errors at most `delta_g`:

\[
 E_{k+r}\le\sum_{j=0}^{r-1}|\widehat\alpha_j|E_{k+j}
       +\Delta_\alpha M\sum_{j=0}^{r-1}\rho^{k+j}.\tag{10}
\]

Each generated interval is intersected with both the public stability envelope and, where available, **all directly retained six noisy impulse reading intervals**. That intersection is important: the latter three observations used to estimate the recurrence are not thrown away after fitting. Interval convolution gives sound future differential-response bounds for any later input sequence, without pretending each impulse uncertainty is independent or claiming that these outer intervals are jointly sharp.

**Executed noisy control.** Bound reciprocal-reading error at `10^-9` for each of the twelve original reports; impose public `M=1/3` and `rho=4/5`, both valid for the test source but not learned from six readings. Exact rational interval propagation enclosed all independent latent-state outputs of the later sequences. The mean-width improvements over the prior-only stable-kernel envelope were approximately `25,467x` (three-pulse 48-step task) and `36,851x` (dense 48-step task). These are *certified upper-bound comparisons for these two workloads*, not a universal improvement factor or a minimax theorem.

**Sharp small-excitation information floor.** With an unknown common baseline for one sham/pulse pair, two source-response values differing by `4 epsilon/|delta|` can produce the same permitted noisy readings; thus no decoder can universally certify a coefficient radius below `2 epsilon/|delta|` for that one-lag class. The saved exact-rational source pair attains this floor. No amount of algebra compensates for a vanishing intervention pulse.

## 4. A decisive finite-memory failure

The same first six impulse readings can also be produced by a source whose true kernel has a seventh-state delayed mode. Construct a nilpotent shift of dimension seven, with norm `rho=1/2`, one input at the first state and one output at the seventh. Its contribution is exactly zero for impulse lags `0,...,5`, but nonzero at lag six by

\[
 \Delta g_6=\frac1{20}\left(\frac12\right)^6=\frac1{1280}.\tag{11}
\]

The alternative remains stable. Therefore finite agreement, even with a stable hidden realization, cannot establish the original three-state dimension bound without an additional promise or source experiments. In the absence of synchronized reproducible resets, a changed physical baseline in the pulsed trial can similarly disguise a changed three-mode impulse kernel at **every** acquired lag. These are separate identifiability obstructions.

## 5. Next useful attack: unknown interactions between interventions

Isolated-pulse experiments do not identify response to pulse *combinations*. Allow a supplied quadratic off-diagonal five-lag extension:

\[
 q_t=q_t^{(0)}+\sum_{j\ge0}g_ju_{t-1-j}
       +\sum_{0\le i<j<5}\beta_{ij}u_{t-1-i}u_{t-1-j}.\tag{12}
\]

The earlier two matched acquisition runs remain valid because every quadratic term vanishes on a history containing only one pulse. Ten pair coefficients `beta_ij` remain unknown. At a new target epoch `T`, the physical baseline and instrument gain together contribute **one new unknown nuisance scalar `B_T`**. Measure one all-zero history and then each two-pulse history with known amplitude `delta`. By reusing the learned `g`,

\[
 \boxed{\beta_{ij}=
 \frac{z_T(i,j)-z_T(\emptyset)-\delta(g_i+g_j)}{\delta^2}.}\tag{13}
\]

This acquires ten previously unknown pair interactions using **eleven** new native scalar Schur readings at one epoch. The new programme needs eleven separately prepared/reset trial histories and 20 active pulse departures in those ten pair experiments, plus waiting/idle settings; there are no free native calls. The exact observation design for unknown `(B_T, ten beta_ij)` has determinant `delta^20`, and an open eleven-dimensional family cannot be identified by ten scalar reactions, even adaptively, under this interface. The lower bound is for the *full ten-coefficient transfer target with unknown epoch nuisance*, not any single later question.

**Executed:** all ten coefficients were recovered as exact rationals. Three new 36-step multi-pulse sequences, including signed pulses never used in the pair acquisitions, matched an independent nonlinear native source after translating to differential reciprocal reactions; **zero later learner calls**. The mathematical contract is a five-lag quadratic pair term, with no unknown diagonal terms or interactions beyond the specified pair library. It is not discovered merely because training pairs fit.

### A third-order source with an identical old experimental record

Add `gamma u_(t-1)u_(t-2)u_(t-3)` to (12), `gamma=1/4`. This hidden term vanishes on **every** sham, singleton, and pair history, including all eleven interaction-acquisition reports. It changes a newly specified triple-pulse reaction at the same epoch by

\[
 \Delta z_T=\gamma\delta^3=\frac1{500}.\tag{14}
\]

One properly chosen, separately charged triple-pulse native experiment identifies `gamma` under this **restricted one-parameter cubic extension**. The amended programme then reproduced 99 new late-time nonlinear source contrasts exactly. This is a concrete model-falsification and repair sequence, not proof of a universal causal learner.

## 6. Fresh guards for the acquired interaction model

After the quadratic candidate was frozen, eight independent fresh intervention-history patterns were drawn from an eleven-level rational strength grid, within the physical range `[-1/5,1/5]`. A single same-epoch sham reaction was retained; eight new native reactions gave their exact differential responses. The wrong quadratic candidate was rejected by the **first** fresh pattern. The amended cubic candidate agreed with all eight source reactions.

If the true differential source function at that epoch is promised to be a polynomial of total degree at most three on the five most recent intervention amplitudes, the candidate is frozen *before* fresh tests, and readings are exact, Schwartz–Zippel yields the joint bad-acceptance bound

\[
 \Pr[\hbox{all eight match AND frozen candidate is not the true polynomial}]
 \le (3/11)^8=6561/214358881\approx3.06\cdot10^{-5}.\tag{15}
\]

This is a **joint** bad-acceptance probability over fresh independent test draws, not a conditional-on-acceptance guarantee without a yield estimate. Source invariance between acquisition and guard epochs remains supplied. An explicit degree-eleven polynomial `P(u)=prod_(a in grid)(u-a)` vanishes on every value of the entire validation grid but is nonzero at the **physically admissible** new amplitude `u=1/50`. Thus passing all these tests does not establish an unrestricted analytic or physical model class.

## 7. Alternative physical acquisition when resets are unavailable

The matched-pulse method genuinely needs reproducible resets. If instead the physical baseline and inverse instrument gain can be independently promised affine over the experiment and the memory is promised to have **four FIR taps**, a single continuous run can fit all unknowns:

\[
 z_t=q_0+q_1t+\frac{h_0+h_1t}{1+u_t}
          +\sum_{j=0}^{3}a_ju_{t-1-j}.\tag{16}
\]

There are eight unknown scalar coefficients. Each native reciprocal reaction is one linear equation in `[1,t,(1+u_t)^-1,t(1+u_t)^-1,u_(t-1),...,u_(t-4)]`. A full-rank eight-row design is sufficient and, on an interior eight-parameter source class, seven readings cannot identify *all eight* coefficients along a fixed adaptive transcript.

**Executed with native Schur reactions:** twelve sequential positive shunt commands, the first four furnishing pulse history but **not** reports; eight later scalar reactions at different times made a matrix with determinant `-8399/21780000`. The learner recovered the entire physical baseline, instrument gain, and four tap coefficients exactly:

`(q0,q1,h0,h1,a0,a1,a2,a3)=(3/5,1/1000,4/5,1/2000,1/8,-1/12,1/15,1/20)`.

Once acquired, **24 future open-loop reactions** and **24 steps of a newly specified raw-reaction-driven digital feedback** were executed correctly with zero new learner source calls. To avoid unwarranted arithmetic explosion, the feedback actuator is explicitly quantized to `1/10000`: both the experiment and predictor use the same physical command, rather than concealing a rounding discrepancy.

An analytic nonaffine-baseline alternative agrees with every one of the eight historical reactions but changes the next physical baseline by exactly `1/100` at previously unobserved time 12, producing a different native boundary reaction. The source remains positive on its operating horizon. This construction therefore **exchanges the reset requirement for a substantially stronger nuisance-drift and FIR contract**; it does not dominate the matched-reset method without comparing physical reset, actuation, timing and sensor costs.

## 8. Strong equally informed comparators and scientific status

- **Ho–Kalman/Prony realization:** the Hankel recurrence and minimality calculations are classical realization theory. An equally informed system-identification algorithm can perform the same exact computations and tie the future transfer. A relevant primary discussion is `Minimal state-space realization in linear system theory: an overview`, https://doi.org/10.1016/S0377-0427(00)00341-1.
- **Willems' fundamental lemma / behavioral data-driven control:** persistently exciting trajectories can represent future LTI trajectories. They are legitimate alternatives, not inferior competitors by default: https://doi.org/10.1016/j.sysconle.2004.09.003.
- **Factorial design, Volterra/polynomial response, and polynomial identity testing:** pair and triple differences, coefficient counting and fresh guards have established ancestry. The source-to-experiment composition and explicit scope management are this investigation's contributions; mathematical historical priority is not established.
- **Same information and costs:** the synthetic experiments do not demonstrate better total runtime or hardware performance than a retaining algorithm allowed to use the same model class, exact readings, calibration, resets, and code. Native interface settings, resets, returned scalar width, source-aware checker calls and exact rational arithmetic remain charged separately. Dense long-horizon rational coefficients grow; the bounded-resolution digital actuator is part of the protocol.

**What has genuinely been acquired:** an exact recurrence describing future causal differential responses under a three-state LTI contract; ten later pair interaction coefficients and one third-order coefficient when the specified mechanism library was expanded; a finite-noise outer predictor that refuses unsupported exactness; and, under an alternative stricter contract, a reset-free model predicting future **raw** reactions and digital feedback. All acquisition uses actual configured Schur source readings. What remains **supplied**, not learned, is the source mechanism class, matched-reset reproducibility or affine nuisance law, physical stability/decay bounds, a stable baseline, ability to configure interventions, and exact or bounded sensor errors.

**Decisive failures retained:** stable delayed impulse echo with identical first six values; nonreproducible baselines masking even a three-mode response; sharp weak-excitation noise floor; unobserved third-order interaction invisible to all pair histories; higher-degree source invisible to the entire finite validation grid; nonaffine source drift matching every reset-free training reading. The strongest research frontier is to acquire a causally useful *mechanism class* and reset/recovery guarantees from real intervention histories with finite precision, rather than infer them from short successful fits.

## 9. Reproducible producer and independent checks

The actual saved programme and result files in this directory are:

1. `causal_memory_primitives.py` — the independent native four-port Schur source.
2. `causal_hankel_acquisition.py` and `causal_hankel_results.json` — two matched runs, six Markov coefficients, all-future recurrence, unseen programmes.
3. `noisy_memory_and_obstructions.py` and `noisy_memory_and_obstructions_results.json` — outer precision bounds, source-twin counterexamples, delayed stable mode and noise floor.
4. `nonlinear_causal_interaction_learning.py` and `nonlinear_causal_interaction_results.json` — ten off-diagonal interactions, unseen multi-pulse transfer and one extra triple-pulse probe.
5. `fresh_causal_model_guards.py` and `fresh_causal_model_guards_results.json` — fresh held-out causal mechanism validation, wrong-source detection and degree-class no-go.
6. `reset_free_fir_acquisition.py` and `reset_free_fir_results.json` — alternative single-run, full raw-reaction transfer; explicit quantized feedback.
7. `verify_causal_research.py` and `independent_verification_results.json` — independent reconstruction of rational acquisition, coefficient and source-witness results without importing producer algorithms.
8. `clean_replay.py` / `clean_replay_results.json` and `SHA256_MANIFEST.json` — execution from an isolated working directory and preserved file hashes.

No historical sandbox path is presumed to exist in this workspace. These are finite synthetic scientific source controls, not physical device experiments, and this turn does not mutate the Astra GitHub repository.
