# Predictive preparation from finite dissipation and private timing

The supplied construction acquires a reusable finite-horizon predictor of a retained locally dissipative **linear time-invariant plant**, without a hidden dimension or slowest-relaxation bound. It also gives an exact deterministic-preparation obstruction. Read the [complete report](package/predictive_preparation.md), [15-page PDF](package/predictive_preparation.pdf), [original ZIP](original/predictive_preparation_research_package.zip) and [complete captured return](P2_PREDICTIVE_PREPARATION_20261105_RETURN.txt). The ZIP arrived after capture; the prompt, full rendering/activity, native prefix and historical unavailable-download header are preserved verbatim. [Source metadata](SOURCES.json).

The [execution/cost page](execution-costs-and-scope.md) links the supplied exact digital certificates and distinguishes physical simulations. The [independent companion page](companion-constructions.md) retains module composition, sectorial oscillators and a finite-horizon noncoercive extension. The [structural join review](package/structural/random_window_structural_review.md) credits the constructed interfaces at their stated premises without establishing historical priority. No programme or new Capital audit was run; no practical acquisition advantage or realised civilisation-changing performance is inferred.

The later [equilibrium-inference law](../2026-11-05-p1-equilibrium-inference/README.md) concerns zero-state scalar-port trials with supplied rate bounds and independent sensor noise. Its [reset and reuse ledger](../2026-11-05-p1-equilibrium-inference/operation-and-costs.md) does not import retained-loaded-plant preparation here as free arbitrary-plant reset, and distinguishes transient age from full laboratory time. These interfaces and original results retain their separate scopes.

## Actual physical premises

For observed displacement x, velocity v and additive port force f, the complete causal well-posed LTI plant has a supplied storage function satisfying

```text
E(t)-E(s) <= integral_s^t f v - Gamma integral_s^t v^2,
E(t)>=mu x(t)^2/2,  Gamma,mu>0.
```

An actual local damper and permanently attached calibrated spring can supply these bounds; moving the spring centre applies f while its restoring term remains part of the **loaded plant**. It predicts that loaded plant, not a released unknown bare law. A known visible mass can additionally bound velocity. Local dissipation is stronger than bare passivity; storage, initial-energy bound, linearity/time invariance, finite sensors/actuators, private randomness, timing and reliable memory are substantive premises, not certified by a quiet trace.

The hidden environment may have arbitrarily many, slow, undamped or continuum modes within this physical class. Unbudgeted continuous thermal forcing and arbitrary nonlinear/active environments do not follow from a finite-initial-energy argument.

## Private random clock supplies the preparation operation

On a common passive off trajectory with initial energy at most E, `integral_0^infinity v_off^2<=E/Gamma`. Divide it into N disjoint slots of duration at most D; let Z_j be the maximum displacement range within slot j. Choose J uniformly **after the initial state is fixed**, using private randomness. Then

```text
Pr(Z_J>delta) <= ED/(Gamma N delta^2).
```

A power-of-two `N>=ED/(Gamma alpha delta^2)` gives failure at most alpha, maximum occupancy ND, expected start `(N-1)D/2` and exactly log2(N) random bits. The slot includes baseline readout, clearing, the whole future experiment, computation latency and guards.

This holds for every fixed admissible initial state over the fresh random choice. It does not recognize a safe future from a quiet prefix, give the guarantee conditional on every selected index, or permit an adversary to learn J before choosing the disturbance. Repeated physical use updates the energy ledger and draws fresh preparation randomness.

Time-varying off-force leakage xi_0 has the additional irreducible term `xi_0^2D^2/(Gamma^2delta^2)`; longer waiting alone cannot remove it. A fixed offset instead permits the stated shifted-storage budget. The operation charges actual force error/backaction rather than assuming a perfect off switch.

## Acquired response and arbitrary preprogrammed inputs

The mathematical zero-state unit-step displacement response S obeys `0<=S<=2/mu` and `|S(t)-S(s)|<=sqrt(|t-s|/(2Gamma mu))`. A supplied mass improves the modulus under its stated bound. The experiment never prepares the zero state or an instantaneous step: it uses a finite baseline, smooth force ramp/hold/return, finite averages and digitization. LTI superposition separates the small baseline-relative free drift from the forced response; ramp, boxes, interpolation, metrology, ADC, clocks and backaction are paid.

For acquired table error epsilon_S and a later bounded-variation programme with `W_f=|f(0+)|+TV(f)`, the visible return gives the complete prediction budget

```text
||x_f-x_tilde_f||_infinity <= delta_g+eta_g+W_f epsilon_S
 +(2q_bg+q_f)/sqrt(2Gamma mu)+epsilon_num.
```

One acquired event supports all admitted subsequently selected **preprogrammed** inputs, with planning inside the declared slot. Counterfactual queries reuse the table; a new physical run pays new preparation. Arbitrary future feedback requires another closed-loop comparison and is not silently supplied.

## Deterministic preparation has an exact obstruction

Even the known kernel `K(t)=B exp(-a t)` admits a conservative oscillator realization whose hidden initial force g has translation-invariant energy `integral(g'^2+a^2g^2)/(4Ba)`. Finite-energy opposite pulses can be placed after any deterministic preparation deadline while giving identical prior port records, including under local causal control. A deterministic stopping rule terminating on the zero-force record is similarly defeated.

For the stated normalized visible law, the attainable minimax future path radius is `R(E,T)=sqrt(2E)||h||_L2(0,T)`, with h the specified disturbance-to-displacement impulse response. The earlier preparation duration is absent. Known positive visible mass preserves the obstruction; finite-resolution oscillator/string realizations have their own material/precision costs. Private timing escapes because the disturbance state is fixed before the random start draw, and finite dissipation cannot spend substantial motion in every disjoint slot.

The earlier [nonlinear positive-relaxation acquisition theorem](../2026-11-05-p2-acquired-passive-environment/README.md), thermal simulator and quantum boundaries keep their different premises. The present return does not resolve weak-stream compression, arbitrary-feedback thermal prediction or generic hidden nonlinear model discovery. Established dissipativity, response-based control and initial-state-independent identification are credited in the captured comparison. Generated current retrieval was not rebuilt.
