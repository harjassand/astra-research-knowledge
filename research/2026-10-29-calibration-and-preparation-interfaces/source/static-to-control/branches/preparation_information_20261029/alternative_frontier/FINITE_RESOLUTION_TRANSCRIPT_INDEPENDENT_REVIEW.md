# Independent review of finite-resolution transcript theorems

29 October 2026. Reviewer: producer-workspace/different_consequential_opening.

Reviewed source:
causal_frontier/FINITE_RESOLUTION_TRANSCRIPT_THEOREMS.md
SHA256: f3c49ad02d723f9e043b54abc5a838c483449448b1e0450c1d337cc42bccf353.

Scope: ordinary proof review of the new adaptive likelihood, feedback,
convolution, point-sampling, continuous-meter and quantization arguments.
No older projection or compact-native-repair theorem was re-audited.

## Finding

The main adaptive Gaussian transcript bounds (8)--(9), general adaptive-point
bound (12), continuous-meter bound (14), and finite-tree quantization bound
(16) are correct under their declared access and well-posedness contracts.
The common-history latent comparison is sound; it does not assume that
independently realized feedback histories agree.

One scope correction is needed in Section 5's deterministic-time shortcut:
deterministic observation TIMES do not by themselves permit a deterministic
variance bound to be multiplied by HISTORY-SELECTED precisions. The claimed
V_n sum eta_i^(-2)/2 formula is valid for deterministic precisions, or after
replacing each precision by a deterministic per-query ceiling. The main
adaptive-point theorem already avoids this issue.

Two clarifications should also remain explicit:
- the stationary-preparation latent variable must include the forcing
  prehistory or its necessary initial filtered-force state;
- exact no-information-gain equivalence with passive observation applies
  to the stated translation-compatible sensors. For a general nonlinear
  phase sensor, the coupling bound remains valid, but it does not prove
  that a particular feedback choice cannot improve finite-n information.

No actual noise calibration, sensor law, force preparation or microscopic
observation has been acquired by these mathematical arguments.

## 1. Common-history augmented likelihood

Fix an exogenous latent variable xi with the SAME prior in both experiments.
It includes the required initial variables, Brownian drivers and policy seed,
but excludes each report's fresh noise. For stationary preparation it must
also include the needed x/v forcing prehistory (or the equivalent initial
filtered-force variable). The comparison model may ignore that extra latent
variable; its inclusion does not reveal it to the experimenter.

For each possible past report history, both models select the same next
time, settings, command protocol and positive Gaussian covariance.
Conditional on xi and that common history, each model has its own correct
Gaussian report mean. Therefore the conditional likelihood increment is
exactly the squared difference of those means in the common covariance
metric, divided by two.

The chain rule then gives (3) exactly on the augmented space. Its expectation
is under the SOURCE augmented law. Both augmented laws retain the original
xi marginal, because the report-generation kernels integrate to one for
every xi. Thus a pathwise bound in xi alone can be averaged under the
original common driver law despite feedback and adaptive timing.

Times, settings, commands and stop decisions are functions of the past
reports and the seed, so they create no omitted likelihood factor. Padding
with a common dummy outcome handles stopping. This reasoning includes the
entire record and all success/failure flags; conditioning on a selected
branch would require a separate normalization analysis.

Fresh Gaussian errors must have positive variances (or the displayed formulas
be read in the appropriate extended/singular covariance form). Repeated
readings of one continuous noisy meter are not fresh independent errors;
the note correctly separates that interface.

## 2. Additive report-driven forcing

At one common history, the realized additive waveform u is the same in
both equations. Subtraction therefore leaves delta w=Y and
delta y=integral Y. These identities are independent of the gain of the
map from reports to u. They require u to be a well-posed causal waveform
based only on the declared records and known external inputs.

The moment bounds follow pathwise from

    sup_t |integral_0^t Y|^2 <= h integral_0^h Y^2,
    integral_0^h |delta w|^2 = integral_0^h Y^2.

Averaging gives (5). No independence between an adaptive history and Y is
needed, because these bounds are uniform over common histories.

For finite sequential linear or translation-equivariant reports, subtraction
of the known controlled shifts A_u and B_u is genuinely causal and invertible.
At query j the required shift is determined by already reconstructed earlier
reports. One can reconstruct the original report by adding that shift, then
reconstruct the next settings and commands. The passive transformed policy
may be adaptive; it is not a claim of equivalence to a fixed passive schedule.

For wrapped-position reports, subtraction modulo the torus respects wrapped
Gaussian noise. For general nonlinear phi(q), however, subtracting B_u from
the output is not generally a valid operation. The source correctly limits
the exact equivalence to translation-compatible readouts. Its section title
should not be interpreted as an unrestricted claim that nonlinear feedback
can never improve information: only the uniform resource bound is established
for those more general sensors.

The passive-equivalence statement is clearest for finite report sequences.
For continuous feedback, any exact inverse transcript transformation would
also need the corresponding causal Volterra inversion/uniqueness condition.
The separate continuous-meter KL theorem does not need such an equivalence.

## 3. Native state feedback receiving

For the stated uniformly K-Lipschitz state-feedback family, freeze the common
report history and write delta w=Y+Z. Then

    Z'=-gamma Z+delta u,
    delta y'=Y+Z,
    |delta u|<=K(|delta y|+|Y|+|Z|).

Starting from Z(0)=delta y(0)=0, the sum |delta y|+|Z| is bounded by
C_h integral_0^h |Y| with the source's conservative
C_h=(1+K)exp[(1+gamma+K)h]. This proves (6), including the momentum-energy
factor 2(1+C_h^2 h^2). History-selected members of the same uniformly
Lipschitz family satisfy this at every common history.

An actual continuously reported state-feedback command could itself disclose
unobserved state. Those values are not automatically a free deterministic
part of the transcript; the source's explicit warning is necessary.

## 4. Position and convolution readouts

For each history and latent driver,

    sum position signal^2/noise_variance
      <= J_q sup_t |delta y(t)|^2,

and by Cauchy--Schwarz,

    sum convolution signal^2/noise_variance
      <= J_p integral_0^h |delta w(t)|^2 dt.

The deterministic all-histories budget ceilings are load bearing. They
permit the entire adaptive sum to be bounded before averaging. This is why
there is no hidden independence assumption involving adaptive kernels,
precisions, gains or stopping times in (8).

The same deterministic receiving bounds under native state feedback give (9).
Pinsker's factor in (8) and the necessary precision/bandwidth inequality (10)
are correct. The bound is necessary, not sufficient or a sharp sample theorem.

The boxcar L2 norm and continuous-noise variance accounting are correct.
Overlapping samples of one physical meter need their actual covariance or
the continuous theorem; treating them as independent would invalidate the
likelihood calculation.

## 5. Deterministic-time precision correction and adaptive point samples

For fixed times t_i and fixed positive precisions c_i=eta_i^(-2),

    E sum_i c_i Y(t_i)^2 <= V_n sum_i c_i.

The same formula with sum_i bar c_i is valid when c_i(history)<=bar c_i
for specified deterministic per-query ceilings.

But if precisions are selected from previous reports, c_i can be correlated
with the latent signal at the deterministic time t_i. In general,

    E[c_i Y(t_i)^2] != E[c_i] E[Y(t_i)^2],

and a deterministic-time marginal moment bound does not justify that
factorization. A single total precision ceiling J_point is not by itself
a per-query deterministic factorization.

Suggested replacement for Section 5's opening paragraph:

    "For deterministic observation times and deterministic precisions
    c_i, noisy momentum samples add at most (V_n/2) sum_i c_i to the
    augmented KL. More generally use deterministic per-query ceilings
    c_i(history)<=bar c_i and replace the sum by sum_i bar c_i.
    Arbitrary history-selected precisions under only the total budget
    J_point are covered by the adaptive-point bound below."

For at most N points in a fixed deterministic schedule, an alternative valid
total-budget bound is

    (J_point/2) min(R_n,N V_n),

because E max_i Y(t_i)^2<=N V_n and also <=E sup_t Y(t)^2<=R_n.
This is a secondary bound, not required for the main result.

The adaptive-time grid argument itself is correct. Since |Y'|<=2a,

    E sup |Y|^2 <= 2(h/Delta+2)V_n+8a^2 Delta^2.

The choice Delta=(hV_n/(8a^2))^(1/3) gives exactly
R_n=4V_n+6(ahV_n)^(2/3). The endpoint-inclusive grid makes the bound valid
even if Delta>h. The a=0 case must indeed be handled directly.

The full adaptive precision sum is bounded PATHWISE by
J_point sup_t |Y(t)|^2. Hence (12) is sound for both adaptive times and
adaptive precisions. The native-state-feedback correction follows from
delta w=Y+Z and the previously established bound on Z.

## 6. Continuous Gaussian meter

Conditioning on all exogenous physical drivers does not condition on sensor
Brownian motion: the latter is independently generated. The observation drift
is then a predictable functional of the possible observation history and a
fixed latent parameter xi. It need not be a Gaussian process after nonlinear
feedback; Girsanov, rather than a Gaussian-process assertion, is the correct
tool.

At each common history the momentum mean difference is Y and the phase mean
difference is at most L_q |integral_0^t Y|. Both differences are bounded on
the finite horizon. The likelihood-changing exponential therefore satisfies
Novikov for this difference drift. Strong/weak uniqueness for the closed-loop
observation equation identifies the changed measure with the intended
comparison law; the note correctly retains well-posedness and local signal
integrability rather than claiming those for arbitrary formal feedback.

Conditional path KL is half the integrated normalized drift difference.
Marginalizing xi and using E Y(t)^2<=V_n yields the momentum term h V_n.
For position,

    E|integral_0^t Y|^2<=t^2 V_n,

and integration gives h^3 V_n/3. Thus every factor in (14) checks.

The fixed causal convolution extension follows from Young's L1-to-L2 bound
with zero filter initialization. A general adaptively changing filter would
need its actual uniform operator bound; the displayed fixed-convolution
calculation alone would not justify it. The note's prehistory warning is
appropriate.

Any adaptive processing of an already acquired complete meter record is
then covered by data processing. Changing the physical meter or adding a
fresh independent-noise sensor is a different acquisition interface.

## 7. Passive and adaptive quantization

For passive fixed-time bins, condition on every driver except the initial
uniform y phase. The displacement delta y is independent of that phase,
and the comparison y position is phase plus a fixed shift. The mismatch
set is contained in K boundary strips of total normalized length at most
K|delta y|/(2pi), truncated at one. Union and Cauchy--Schwarz give (15).

Conditioning on previous bins would generally destroy uniformity, so that
argument cannot simply be iterated conditionally. The source instead unions
over the entire finite decision tree before conditioning on the realized
history. This repairs the issue.

With the non-phase drivers and policy seed fixed, each of at most
(K^N-1)/(K-1) nodes fixes its query time, grid and additive command. At a
node the free coordinate is still phase plus a fixed shift, and its source
difference is uniformly bounded by sup_t|delta y|. If two actual transcripts
first diverge at that node, their initial phase lies in its mismatch set.
Union over all nodes therefore bounds the coupling failure probability.
Finally E sup_t|delta y|<=h sqrt(V_n), proving (16).

The finite-tree count requires the stated finite alphabet and no extra
continuous observation depending on the initial phase. Stopping and continuous
choices of settings based on finite previous reports cause no problem:
once a node and seed are fixed, those choices are fixed. State-dependent
unrecorded threshold triggers would be a different interface.

The exponential node factor is retained. It does not establish the Gaussian
Omega(n) budget bound for noiseless adaptive quantizers.

## 8. Physical interpretation and final scope

sigma_n is the UNCONTROLLED stationary shear's entropy rate, or its comparison
variance parameter in the common-Maxwell preparation. Arbitrary additive
feedback can supply additional work and entropy. These transcript bounds
do not assert that the controlled experiment's total physical entropy equals
sigma_n or tends to zero. The source explicitly leaves command work outside
its information bound; this distinction must survive synthesis.

The scientific addition is a complete experiment-law conclusion for a declared
finite-resolution interface, not a new Gaussian likelihood identity or a
free acquisition of native resolution. Positive Gaussian noise power, gain,
filter norm, query count, physical horizon and hidden preparation all remain
attached to the claimed consequence.

Subject to the deterministic-time precision qualification above, the main
transcript theorems pass this substantive review.

