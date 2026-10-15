# Native computation: amplification, its physical contract, and a nonlinear information barrier

15 October 2026. **Status: no qualifying new scientific capability established.**

This independent lane tested two representation changes. The first—letting an unknown transport medium expose its internal response through finite localized load changes—is already covered closely by Virtual VNA, differential scattering, and physical adjoint methods. It was stopped. The second—letting an unknown specimen amplify an unstable mode instead of reconstructing its operator—has a clean conditional computation contract. Its underlying mechanism is established threshold/eigenmode physics. The original derivation here is a nonlinear information bound: a fixed negative local curvature does not provide a uniform finite-cost instability measurement, even with full continuous observation, nonzero thermal coupling, exact reset, and bounded adaptive forcing.

No experiment was performed. The calculation script checks algebra and numerical consequences of explicit models. It does not validate an apparatus, establish historical priority, or independently verify the universal proofs.

## 1. Question, native input, and decision

The physical input is an existing unknown coupled specimen, rather than a digitally supplied matrix. The proposed output is one bit: does its calibrated small-signal drift have an eigenvalue at least +a, or are all eigenvalues at most −a? The band between −a and +a is deliberately outside the promise. A possible scientific use is screening a native resonator or mechanical array for an unsafe growing mode before using it, or locating the uniform trapping strength at which a mode becomes unstable.

The representation change is to retain the operator in the specimen and convert a spectral property into native growth and then a threshold count. There is no QRAM, Hamiltonian oracle, uncharged matrix-loading step, or claimed reconstruction of the microscopic specimen. Fabricating or preparing the specimen, qualifying its control/noise/readout interfaces, and resetting it are part of the cost.

The strongest comparator receives the same specimen, access, pump, noise, reset and readout budget. It may use established threshold spectroscopy, stochastic drift estimation, active force/displacement measurements, or the very statistic derived below. No advantage over that comparator is proved.

## 2. Capital examined, and why its premises are not imported

Capital was read at Git revision **846f185763ed3a27310fad4ce9471ba324d1e5f4**, beginning with AGENTS.md and 00_START_HERE.txt. Selective dossier inspection covered N791 (local reset echo), N798 (full-source response), N799 (parked molecular history), N786 (finite-order spectral information), N772 (source-word representation), and N585/N736 as route screens. They remain scoped, unreviewed material. The potentially relevant inherited lessons are:

- N791's rare spectral-weight cost is tied to its specific null-readout and reset/twirl interface. An actively growing classical system is a different experiment, so its dimension cost cannot simply be transferred either way.
- N798 does not acquire global source/operator envelopes from finite local measurements. Native dynamics do not automatically supply those envelopes.
- N799's loaded-reference calibration need not transfer to a science-correlated state. A threshold in a reference device does not certify the target specimen's drift, gain coupling, or nonlinear radius.
- N786's finite-order information obstruction uses high-order terms, while a known low body-order plus complete labelled operator data changes the contract. The countermodel below instead uses just one coordinate and a quartic potential; it is not a reuse or strengthening of the N786 theorem.

No Capital theorem is a proof premise in the derivations below, and no Capital files were changed.

## 3. Failed first route: a task-native internal port

I initially considered finite boundary-response differences under a local rank-one perturbation. For an invertible linear operator L and perturbation αbbᵀ, the directly derived resolvent identity is

    Bᵀ(L+αbbᵀ)⁻¹B − BᵀL⁻¹B
      = −α vvᵀ/(1+αr),
    v=BᵀL⁻¹b,   r=bᵀL⁻¹b.

Ratios at distinct known strengths can expose r and vvᵀ without reconstructing L. This is not a surviving novelty claim.

[Frozen Differential Scattering, del Hougne (2026)](https://doi.org/10.1002/lpor.202502660), inspected in full-text sections 2.2.2, 4.2, 6 and 7, already gives an exact finite local-load factorization for arbitrary complex media, including nonreciprocal ones. It proposes toggled scalar matched filtering and discusses multi-perturber rank bounds. Our initial physical interface lies inside that contract.

[Virtual VNA (2025)](https://doi.org/10.1109/TIM.2025.3551897), with the [author preprint](https://arxiv.org/abs/2403.08074), uses at least three known loads per inaccessible port and estimates hidden scattering parameters up to specified sign ambiguities. Its low-noise calibration upper count is 1+2Ns+Ns(Ns−1)/2 for Na>1. [Virtual VNA 3.0](https://arxiv.org/abs/2503.07239) uses tunable and coupled loads to remove ambiguities for nonreciprocal devices. Thus merely dropping reciprocity or lifting the sign ambiguity would not establish a new interface.

[Guillamon et al., physical adjoint computing (2025)](https://www.nature.com/articles/s41467-025-66385-5), inspected through the principles and implementation sections, physically obtains gradients using forward and adjoint propagations, local fields and local actuator derivatives. Its demonstrated functionalities include target transfer, absorption and camouflage. Native execution of an unknown transport operator is already an established capability; it is not enough to rename it as a new representation operation.

Disposition: **stop this route unless a concrete task and measured interface fall outside these methods and beat their full-cost comparison.**

## 4. Conditional construction: scalar readout of a native unstable mode

### Exact linear-noise contract

Let X(t)∈Rᵈ satisfy

    dX = A X dt + sqrt(2D) dW,      X(0)=0,

where A is an unknown real symmetric matrix, D>0 is known isotropic diffusion, and W is standard d-dimensional Brownian motion. The model and apparatus supply:

1. exact reset to zero, or an independently bounded replacement error;
2. the stated linear law over the complete interrogation range and time;
3. symmetric drift in the readout coordinates, isotropic noise, and calibrated time;
4. a scalar readout S=||X(T)||² with a declared absolute error;
5. one of Hs: λmax(A)≤−a, or Hu: λmax(A)≥a, for a>0.

No eigenvector, matrix entry or factorization of A is supplied to the decision procedure.

For a mode with eigenvalue λ, the variance is

    qλ(T) = D (exp(2λT)−1)/λ,

with the continuous value 2DT at λ=0. Under Hs,

    E S ≤ dD/a.

Under Hu an unstable eigenvector has Gaussian projection with variance at least

    q+(T) = D (exp(2aT)−1)/a.

For 0<δ<1/2, choose

    h = dD/(aδ),
    T ≥ log(1+2d/(πδ³))/(2a).

Declare Hu if S≥h and Hs otherwise. Markov's inequality gives

    Pr_Hs(S≥h) ≤ δ.

For Z∼N(0,1), Pr(|Z|<z)≤sqrt(2/π)z. Retaining one unstable projection therefore gives

    Pr_Hu(S<h) ≤ sqrt(2h/(πq+(T))) ≤ δ.

This proves the conditional binary test. The interrogation time grows logarithmically in d and inverse confidence, while the required threshold h grows linearly in d. These are sufficient bounds for this procedure, not lower bounds for all procedures. The unknown operator is physically executed; the digital work is one threshold comparison and arithmetic on d,D,a,δ. The theorem does not certify its own physical promises.

With a deterministic absolute readout error e≥0, use the reported threshold h+e. A stable false positive still requires true S≥h; an unstable false negative can occur only if true S<h+2e. It suffices to replace the time condition by

    exp(2aT)−1 ≥ 2a(h+2e)/(πδ²D).

Acquiring a uniform e on the actual specimen is a separate task.

### What is already established, and what is new here

The mechanism is continuous-time spectral amplification, closely related to power iteration and the selection of a largest-growth mode at laser/OPO threshold. [Roy et al., Spectral Phase Transitions in Optical Parametric Oscillators (2021)](https://www.nature.com/articles/s41467-021-21048-z), inspected through its linear-stability model, experimental characterization and discussion, explicitly connects the largest growth eigenvalue to threshold and experimentally studies spectral mode selection. It also identifies critical slowing near the transition. The present Gaussian threshold inequality is an internal, original calculation on a simpler promised model; it does not establish a new threshold device or superiority over that literature.

The useful distinction is that a passive rare-overlap measurement and an actively growing native system are different interfaces. The latter can trade elapsed time for physical amplitude, energy injection and nonlinear range. It does not erase those costs.

### Complete cost contract

| Item | Required resource or evidence |
|---|---|
| Physical input/loading | Existing specimen containing native A. Preparing/fabricating a new programmable A would require its full loading/fabrication cost; none is omitted by treating an existing specimen as input. |
| Preparation/reset | Bring all relevant coordinates to the declared initial distribution. Exact X(0)=0 is ideal; actual reset error and reset duration must be acquired. |
| Noise | A strictly positive, isotropic diffusion D on every potentially growing mode. The quadratic-variation trace is 2Dd per unit time. The Itô injection term for the diagnostic κ||X||²/2 is κDd per unit time; this is a coordinate-normalized model ledger, not measured heat, pump efficiency, or a thermodynamic lower bound. |
| Gain/control | If a tunable uniform gain or negative stiffness is needed to shift the spectrum, demonstrate its actual coupling in these same coordinates. A pump label or actuator voltage does not supply aI. Pump energy, loss, bandwidth and calibration remain paid. |
| Evolution | At least T above, plus physical settling/control time. Linear range must cover the attempted experiment; saturation cannot be silently treated as a faithful flag. |
| Output/dynamic range | Resolve h and the absolute readout error e. With a common scale κ, h corresponds to κh/2 of probe energy. h is O(dD/(aδ)); it is not a dimension-free macroscopic output guarantee. |
| Readout | A calibrated positive-definite all-mode quadratic readout. Measuring d coordinates costs d channels/samples unless a qualified native aggregator exists. A detector that sums a different quantity needs a new norm-equivalence proof. |
| Computation/storage | O(1) scalar statistics after a qualified native aggregator; otherwise O(d) readout processing. Coefficient reconstruction and storage are unnecessary for the conditional test. |
| Calibration/model validation | Symmetry or the correct similarity metric, diffusion support, mobility/rate bounds, nonlinear range, uniform sensor error and reset validity. Generic finite port data do not provide all-state guarantees. Cost UNKNOWN for an unspecified specimen. |
| Errors | Threshold error ≤δ per promised hypothesis only under the exact model; the gap region returns no warranted classification. Model discrepancy is an additional acquired budget. |
| Energy/fabrication/lifetime | Numerical values UNKNOWN. Sample survival and repeatability after growth/reset must be measured. No inference-energy telemetry was available. |

## 5. Adversarial tests of the construction

### Noise support is essential

Let the diffusion excite only coordinate 1, let X(0)=0, and compare

    As=diag(−a,−a),       Au=diag(−a,+a).

Coordinate 2 remains exactly zero. Every full trajectory is identical in the two models although Au has an unstable eigenvalue. Nonzero total thermal or injected noise does not establish every-mode support. This is an exact countermodel, not a claim that an actual specimen has zero mobility.

### Stable nonnormal dynamics can show large native growth

For

    A = [[−a, K], [0,−a]],
    exp(At)=exp(−at) [[1,Kt],[0,1]],

both eigenvalues are negative, yet a seed in coordinate 2 produces arbitrarily large transient norm as K increases. Symmetry, a justified energy metric, or a quantitative nonnormal bound is necessary. Observing a large transient alone does not determine an unstable eigenvalue.

For overdamped mechanics A=−MK, with positive mobility M and Hessian K, similarity to −M^(1/2)KM^(1/2) preserves the sign of unstable directions. It does not give a lower growth rate from the Hessian alone if mobility is unknown or arbitrarily small. Nor does it supply the proper scalar readout metric or isotropic-noise coordinates.

### Local negative curvature need not yield an observable flag

Consider the two one-coordinate potentials

    Us(y)=b y⁴/4 + γ y²/2,
    Uu(y)=b y⁴/4 − γ y²/2,

with b,γ>0. Their Hessians at zero are +γ and −γ, respectively. Uu has minima at ±sqrt(γ/b), and the energy released from zero to either minimum is γ²/(4b). Both the output displacement and released energy can vanish while the negative curvature remains fixed. A detector cannot be assigned a macroscopic instability flag from the curvature premise alone.

The next section makes this information-theoretic, including thermal motion and adaptive controls. It is stronger than merely noting saturation.

## 6. Original bounded-control indistinguishability theorem

### Input/output and allowed interventions

The unknown specimen is Us or Uu above. For this lower bound, b and γ may even be supplied exactly; only the sign label is unknown. Grant the investigator exact reset Y(0)=0, known mobility μ>0, known inverse temperature β>0, and perfect continuous observation of the entire real-valued coordinate. The investigator may use any common admissible causal randomized policy, independent of the unknown model label, with predictable gain g_t and force f_t satisfying

    |g_t|≤G,       |f_t|≤F,

for fixed finite G,F. Under θ=−1 (stable) or θ=+1 (unstable),

    dY = μ[(g_t+θγ)Y − bY³ + f_t]dt + sqrt(2μ/β)dW.

The same policy means the same function of the observed past and investigator randomness under both hypotheses. Admissibility requires a nonexplosive controlled SDE that is unique in law; the bound applies to every such policy. It need not be an open-loop waveform. The allowed gain can attempt the proposed self-amplification, and the force can actively probe the coordinate. The result does not cover unbounded force/gain, noiseless force readout, a nonzero hard clamp, changes in temperature/mobility, or direct observation of the force law.

### Moment bound

Choose any η>0 with stiffness units, and define

    C=G+γ+η/2,
    H=1/β+F²/(2η),
    s*= [C+sqrt(C²+4bH)]/(2b).

Let s(t)=E[Y(t)²]. Itô's formula, Jensen's inequality, and

    E[f_tY] ≤ F sqrt(s) ≤ ηs/2+F²/(2η)

give

    s'(t) ≤ 2μ[Cs(t) − b s(t)² + H].

Starting at zero, scalar comparison with the positive root yields s(t)≤s* for every t, under either model and every allowed policy. The quartic restoring drift supplies nonexplosion and finite moments; the bound is uniform in the policy.

With no controls, the sharper constants are C=γ,H=1/β. In particular

    s* = [γ+sqrt(γ²+4b/β)]/(2b).

### Path-information bound

Conditional on the investigator's independent random seed, the two drifts differ by exactly 2μγY. Their controls are identical as functions on a given observed path, even when feedback is adaptive. The standard Girsanov identity on the augmented path/seed record, followed by marginalization if the seed is omitted, gives

    KL(Pu[0,T] || Ps[0,T])
      ≤ μβγ² E_u ∫₀ᵀ Y(t)² dt
      ≤ μβγ² T s*.

For completeness, one localization proof uses the same exit functional τR=inf{t:|Y(t)|≥R} under both laws and the frozen path record Y(t∧τR). Their entropy is bounded by μβγ² E_u∫₀^(T∧τR)Y(t)²dt, which is at most the unstopped bound μβγ²Ts*. No uniform moment bound on a frozen-at-R process is used. Nonexplosion makes frozen records converge to full records as R→∞; lower semicontinuity of relative entropy preserves the upper bound.

An independent same-team audit also supplied a direct global check. Under the stable law, for any c>0 let V(y)=exp(cy²). Its controlled generator obeys

    L_t V/V ≤ −2cμb y⁴
               + [2cμ(G−γ)+4c²μ/β] y²
               + 2cμF|y| + 2cμ/β.

For every finite λ>0, adding λy² still leaves a polynomial with a negative quartic leading term, hence (L_t+λy²)V≤Kλ V for a finite uniform Kλ. Stopped Itô and Fatou give E_s exp(λ∫₀ᵀY²dt)≤exp(KλT). Taking λ=μβγ² verifies Novikov for the drift-change stochastic exponential. Thus the entropy step is also available directly, without assuming a global Novikov condition that has not been proved. This is an internal audit of the stated model, not external theorem validation.

The drift-relative-entropy relation is established mathematics; see [Opper (2017)](https://doi.org/10.1016/j.jcp.2016.11.021), whose primary article preview was inspected. The original contribution of this report is its application with a uniform controlled moment bound to the opposite-curvature pair, not the Girsanov identity itself.

A closer active-inference comparator is [Hooker, Lin and Rogers, Control Theory and Experimental Design in Diffusion Processes, v3 (2014)](https://arxiv.org/html/1210.3739v3), inspected in sections 2 and 4. It optimizes full-path Fisher information by feedback and studies a double-well particle with bounded additive forcing. Its example has a quartic well plus a Gaussian barrier and uses numerical control/estimation. Active feedback to visit informative regions is therefore established. Our all-policy opposite-curvature KL upper bound addresses a different parameter family and uniform resource question; no priority claim follows from that distinction.

For fixed μ,β,γ,G,F,η,T,

    s* = O(b^(−1/2)),
    KL(Pu || Ps) = O(T b^(−1/2)).

Hence the entire path laws become arbitrarily close as b grows, despite a fixed local drift-growth rate μγ under Uu at zero. Every readout or representation computed from those paths obeys data processing. Infinite sampling bandwidth and a perfect scalar sensor cannot evade this bound.

### Decision lower bound and reset accounting

Pinsker's inequality gives equal-prior optimal error at least

    [1 − sqrt(μβγ²T s*/2)]/2,

clipped below at zero. More sharply for a test whose error is at most δ<1/2 under each hypothesis, binary data processing requires

    μβγ²T s* ≥ (1−2δ) log((1−δ)/δ).

Consequently a necessary total observation time is

    T ≥ (1−2δ) log((1−δ)/δ) / (μβγ²s*) = Ω(sqrt(b)).

For finitely many exactly reset trials with deterministic per-trial horizons T1,...,Tm and total interrogation budget Ttotal=sum Ti, conditional application on each fresh zero state and the KL chain rule replace T by Ttotal. Later policies may depend on earlier records. Declared deterministic caps work by the same argument. Arbitrary sampling, control computation and pooled representations of those records do not remove this bound. No bound in terms of an unqualified expected stopping time is asserted. The theorem grants ideal resets; their real time/energy only increase total cost. It is not a lower bound on every conceivable intervention or every material class.

### Numerical consequence, explicitly model arithmetic

Set μ=β=γ=1 and use no controls. For b=10¹² and Ttotal=100, the displayed bound gives KL≤0.00010000005..., so equal-prior error is at least approximately 0.496464. A 5% error under each model requires at least about 2.65 million model-time units by the necessary bound. These are dimensionless model calculations, not laboratory times or calibrated specimen properties. RESULTS.json contains the generated values.

This is a different obstruction from a rare hidden state or a disconnected bath. There is only one fully observed noisy coordinate. Strong nonlinear confinement makes the force difference that the trajectory visits too small to accumulate information quickly.

At fixed γ the minima coalesce and the barrier γ²/(4b) vanishes as b grows. The relevant limit is strong confinement with a fixed curvature margin. Increasing γ with b to retain a fixed barrier changes the information bound and its asymptotic conclusion.

## 7. What could escape the bound, and why it is not acquired here

The active-interface change would have to include at least one quantified resource that the theorem holds fixed: an upper bound on b/nonlinear curvature growth, a minimum linear/energy-release radius, force or gain increasing with b, a calibrated clamp that measures force at imposed displacement, lower temperature, a changed mobility/noise regime, or a new sensor directly observing the relevant force difference.

For example, to hold a fixed nonzero displacement y0 as b grows requires force of order b y0³. A calibrated force clamp may then compare the forces of the two potentials; their difference is 2γy0. That is a real change in intervention/input information and pays an increasing force budget. It is not free amplification of the original thermal record. Direct force-displacement metrology is a strong incumbent for this task, not an excluded baseline.

Likewise, reducing thermal energy below the double-well scale requires βγ²/b to become large. Refrigeration, preparation and the persistence of that temperature on every degree of freedom must be included. Changing the hypothesis class to globally linear dynamics also avoids the quartic countermodel, but must be justified for the specimen rather than inferred from its early response.

## 8. Disposition and precise follow-up

**Do not promote either tested mechanism as a new capability.** The port operation is covered closely by existing work. Native instability amplification is a conditional established mechanism, and its proposed generic transfer from a local curvature margin is refuted by an explicit quartic thermal model, including bounded adaptive control.

The useful research capital is the exact operational boundary and the controlled path-information inequality. Historical priority of this particular inequality is UNKNOWN; a targeted search did not find an exact match, which is insufficient for novelty clearance. Its proof has been internally derived, not externally reviewed or formally verified.

A justified follow-up, if root allocates one, is a single independently specified native specimen whose linear radius, mobility/noise support, gain coupling and all-mode readout can actually be acquired. Freeze a matched threshold-spectroscopy/force-metrology comparator, then measure total preparation, calibration, force/pump, readout, reset and damage costs. First ask whether successful testing changes a consequential control decision; do not spend another round merely improving the logarithmic ideal-model bound. No such specimen or apparatus evidence was obtained in this lane.

## 9. Artifacts and provenance

- `verify_bounds.py`: standard-library numerical checks of the exact algebraic bounds and nonnormal countermodel; no stochastic time stepping.
- `RESULTS.json`: fresh script output, with model status and units.
- `SOURCES.json`: primary URLs, inspected source scopes, and limitations.
- [Independent same-team nonlinear audit](../nonlinear_audit/REPORT.md): confirms the scalar moment, Novikov, adaptive common-policy KL, testing constant and deterministic multi-trial scopes; historical priority and physical capability remain unestablished.

The memory registry was used only for the workflow rule to audit acquisition and the closest method before deep derivation; the live Capital entry point and current primary sources were then inspected. No memory-derived scientific result is used as a proof premise. No Capital mutation, publication, external message, purchase or laboratory action was performed.
