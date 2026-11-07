# Local noise absorption and repeatable physical-state restoration

**Latest lifecycle and availability, 7 November Brisbane:** P1e61f06c8 and P3031cfb9a completed. P1 reports a completed restricted structural-inference question; its ZIP transfer is unconfirmed and held, with no retry. P3 supplies its noise-absorption original; the broader many-body state-control programme remains unfinished. Both matching expanded user-visible traces are now staged with prior captures preserved. No new assessment or successor-post/start receipt was supplied for these returns. P2e0144bad work is undisturbed. Earlier all-three-started snapshots are history. Stickies closure UNKNOWN is cleanup only. Capital does not select/dispatch science or recover held originals; Sol/Dots/N1683/team/resource limits remain.


This return supplies a model-relative positive completion of known local noise, a rapid many-body restoration regime and decisions for an actually supplied native-control menu. **The broader programme remains unfinished:** native interfaces, acquired calibration and affordable holding costs for wider targets are not established. No new coordinator assessment or impact score was supplied with this intake.

Read the [full proofs and contracts](package/P3_NOISE_ABSORPTION_20261107_RETURN.txt), [packet guide](package/README.txt), [source-access notes](package/SOURCE_ACCESS_NOTES.txt), and [original25-member ZIP](original/P3_NOISE_ABSORPTION_20261107_PACKAGE.zip). The [actual prompt/full response/recovered activity](P3_NOISE_ABSORPTION_20261107_RETURN.txt), [separate visible trace](activity/p3_noise_absorption_20261107_return.visible-activity.txt), and [pre-recovery capture](P3_NOISE_ABSORPTION_20261107_RETURN.pre-recovery.txt) are distinct from the longer internal report. [Provenance](SOURCES.json) records all byte identities.

## Known modeled noise versus residual uncertainty

The construction incorporates a **supplied** Markovian noise generator into intended dynamics by adding positive control processes. A fixed nonzero modeled rate may remain as N grows. Unmodeled drift, synthesis, idle storage, reset, selection and control errors still consume a residual-error budget. This is not an experimentally acquired apparatus, arbitrary unknown noise correction, decoded-only guarantee or generic constant hardware threshold.

For full-rank sigma and jump F, modular partner `J=sigma^(1/2) F† sigma^(-1/2)` plus the supplied coherent correction gives a Lindblad completion stationary at sigma. Established KMS/GKSL/coherent-correction machinery is credited. For commuting local Gibbs Hamiltonians, only terms noncommuting with F enter the finite-neighbourhood completion, giving local **stationarity** without a global partition-function oracle. This does not give rapid mixing throughout the phase diagram or evade the earlier bottlenecks.

## Reset embedding and rapid physical-output regime

The stronger demand `N+C=kappa(R_omega-id)` has exact projected-Choi condition `kappa A-B>=0`. Full-rank omega gives the largest generalized-eigenvalue optimum; rank-deficient targets need the stated kernel inclusion. Optimality concerns this **reset embedding**, not minimum power/activity/time over all stabilizing dynamics. A sufficient positive-factorization construction supplies extra jumps and a compensating Hamiltonian, without an inverse noise channel. The generic emitter uses that sufficient construction and reports the optimal projected rate separately.

Rapid restoration requires a supplied bounded-depth local circuit `sigma=U(tensor_i tau_i)U†`, full-rank local factors, supplied local noise and available/checked bounded-support controls. Circuit light cones and local matrix work are paid; generic block costs are exponential in block size. Deep circuits, nearly pure factors and generic collective Gibbs states need not lie in the fixed-parameter economical regime.

Completed product-representation block resets commute even when blocks overlap. If `r_i=sum_(B contains i)kappa_B` and `r=min r_i>0`, the physical replacement-channel guarantee is

```text
half-diamond distance(e^(t L0), R_sigma)
    <= min(1,sum_i exp(-r_i t)) <= min(1,N exp(-r t)).
```

It covers arbitrary initial states and arbitrary untouched references, with exact target stationarity in the supplied generator model and no unfinished clock weight. At fixed local parameters/native costs: O(N) descriptions/local calculations, O(log(N/epsilon)) parallel restoration time, O(N log(N/epsilon)) restoration activity and O(Nh) holding activity. These are conditional model units, not calibrated seconds, device cycles or joules. Extracted/stored outputs and repeated operation still pay reset, storage and continuing resources.

## Native menus and actuator-generated noise

A positive computed generator is not automatically native. [native_menu.py](package/native_menu.py) accepts an actually supplied finite affine generator menu, joint control-dependent noise law, caps, capacity and costs. Sparse tensor coefficients yield a stationarity LP allowing cancellation across overlapping terms, or a stronger full-reset-equality LP earning the coverage theorem. A failed reset embedding is not general stationarity impossibility: the exact example has reset feasible with downward cap7, reset infeasible but stationarity feasible with cap5, and both infeasible with cap2. Bounds/negative conclusions remain within that menu.

The separate native family includes actuator noise:

```text
L_i(a_i)=lambda_i D[X]+a_i(D[lowering]+e_i D[X]).
a_i=lambda_i(1-2p_i)/(p_i(1+2e_i)-e_i).
```

The supplied joint affine/alignment law, after the same U dressing, is substantive. Attainment needs a positive denominator and the rate cap; the infinite-rate population floor is `p_i>e_i/(1+2e_i)`. Increasing activity cannot remove that floor. With `g=min_i a_i/2`, complete error is bounded by `min(1,2N exp(-g t))`. The exact example `p=1/5,lambda=1,e=1/10` gives `a=30/7,g=15/7`, floor1/12; cap5 works, cap4 does not. This known-model e=0.1 is **not a universal10% hardware threshold**. Million-factor time/activity figures are conditional formulas, not measurements.

## Calibration and error costs

Arbitrary time-dependent residual half-diamond generator error eta gives continuing physical/reference error at most `min(1,N exp(-r t))+2 eta(1+log N)/r`. Summing local residuals can require per-term precision of order`epsilon r/(N log N)`. Modeled noise can remain nonzero while this sufficient uncertainty budget shrinks. A separate fixed-local-observable estimate must not be substituted for whole-state accuracy.

Structured noisy-actuator parameter boxes give population intervals and an exact rational squared global-error bound, with sufficient population precision of order`epsilon/sqrt(N)` away from boundaries. [The million-factor certificate](package/EXACT_GLOBAL_PARAMETER_CERTIFICATE.json) gives error below0.005796 for **supplied** simultaneous parameter radii1e-5. Those intervals were not acquired experimentally.

Finite-time population inversion within the warranted native model is constructed, with conditioning/confidence costs. It requires paid preparations/readout/reset/timing and model validity. Population records alone establish neither coherence behaviour nor absence of environmental memory. Independent-site global calibration can require O(N²/epsilon²) scalar outcomes, with confidence factors; simultaneous readout does not erase per-trial costs. The [synthetic finite-time audit](package/FINITE_TIME_ACQUISITION_AUDIT.json) at probability error0.001 does not acquire the much tighter boxes in the million-factor certificate.

## Limits and producer evidence

An unmonitored noise jump carrying a pure physical state out of its support cannot be canceled by added positive dissipators, even with arbitrary auxiliaries. Fixed local error also need not give fixed global error: in the declared product example, one-factor error0.002 coexists with whole-state distance near0.9874 at a million factors. Common unitary dressing preserves that distance.

The producer's complex/locality/graph-state/reference/overlapping-menu audits are small mathematical fixtures. The graph-state full-generator residual near1.81e-14 is a binary64 diagnostic; its analytic complete-error bound0.0050613 and attained reference-input error0.0031292 have separate scopes. [Exact rational certificates](package/EXACT_RATIONAL_CERTIFICATES.json) are separately labeled. [GRAPH_STATE_CONTROLLER_BINARY64.json](package/GRAPH_STATE_CONTROLLER_BINARY64.json) is logical-generator data, not native hardware commands or rigorous interval synthesis. No physical experiment, new Capital replay, independent scientist audit or generic native commissioning is established.

Earlier state-preparation/local-restoration, exact hard-window, physical-output, bottleneck and source/interface limits remain unchanged. Classical GKSL/KMS, optimization, reset, synthesis and statistical credit is retained. The operation resolves a supplied-model noise-completion/native-menu regime inside the unfinished many-body control programme; affordable broader native access/calibration/holding remains open.

The [access notes](package/SOURCE_ACCESS_NOTES.txt) retain all prior holds and add three unavailable originals: arXiv2604.19973v1 HTML, the Wolf institutional PDF and the Cubitt-et-al. stability PDF. No alternate/mirror recovery is allowed or performed. Successful Ding–Li–Lin v5 and other scope reads are distinct from those held originals. No governing new Zenodo payload or live peer construction was adopted. P1's separate new ZIP remains held. Sol is closed/held, Dots protected/unmessaged and team/resource limits remain; source code is published without execution and the full generated index is not rebuilt.
