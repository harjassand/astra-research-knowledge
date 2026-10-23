# A source-scoped observation countermodel

This is an evaluator's algebraic identification argument, not a new chemistry model, physical counterexample, fit or trajectory. The starting observation contract comes from current Dots' `REPORT.md`, `photon_independent/matched_photon_proof.md` sections 5–6, and the supplied Wallace HTML: effective nitrite kinetics/power dependence and normalized nitrate agreement do not by themselves calibrate retained-original-N product.

## 1. Exact same observations, different retained product

Normalize the initial original-nitrogen inventory to one and suppose an independently established net-disappearance rate is `k(P,R)>0`. Grant the measured absolute aqueous nitrite curve, rather than weakening the baseline:

`x(t) = exp[-k(P,R)t]`.

For any `s` with `0<s<=1`, define

`y_s(t)=s[1-x(t)]`, `u_s(t)=(1-s)[1-x(t)]`.

Here `y` is retained-original-N nitrate; `u` is unobserved original N in other products/phases. The construction obeys

`x+y_s+u_s=1`,

`x'=-kx`, `y_s'=s kx`, `u_s'=(1-s)kx`.

All inventories and forward fluxes are nonnegative. This is a conservation-consistent abstract branching model. It does not claim that any chosen `s` is physically realized in the actual reaction network, that an unmeasured pool is a specified gas, or that the observed paper makes no additional measurements outside the read contract.

Normalize nitrate at the paper's comparison time `t_*>0`. Then

`y_s(t)/y_s(t_*) = [1-exp(-kt)]/[1-exp(-kt_*)]`,

which is independent of `s`. Every member therefore gives **identical absolute nitrite kinetics, identical normalized nitrate kinetics, identical power/radius scaling and the same fitted net-disappearance coefficient**. Nevertheless, for a measured delivered photon amount `q(t)>0`,

`retained nitrate per photon = s[1-exp(-kt)]/q(t)`.

The observation map is many-to-one and the target functional varies on its exact fiber. No number of noiseless replicates of those same observables identifies the absolute retained product. This is stronger than merely saying that a column is missing.

The countermodel also grants exact total original-N conservation, so a generic demand that a model conserve nitrogen does not resolve it. What is missing is an independently observed division of that nitrogen. Further detailed mechanistic assumptions might restrict `s`, but their support must come from evidence or a separate proved premise, not from the normalized curve itself.

### General observation-map form

The amplitude ambiguity does not depend on exponential kinetics. Suppose the independently measured remaining original nitrite fraction is `x(t)` and the measured nitrate curve is only `h(t)=y(t)/y(t_*)`, with `h(t_*)=1`. For any positive amplitude `a` satisfying

`a <= inf_{t:h(t)>0} [1-x(t)]/h(t)`,

the inventories `y_a(t)=a h(t)` and `u_a(t)=1-x(t)-a h(t)` are nonnegative and obey total-N conservation. If this infimum is positive, multiple amplitudes produce exactly the same observed curves and different product per dose. This is a sufficient explicit conservation-feasibility condition, not a claim it was checked for every raw experimental point. It need not give the same simple one-step forward reaction mechanism as the exponential example.

The supplied package does not contain a complete independently calibrated paired raw nitrite/nitrate amount series for the new source; external figure assets were not all bundled. Accordingly this review proves a structural ambiguity of the **stated normalized measurement interface** and an explicit conservation-consistent example. It does not claim a fitted counterkinetic model matching every unpublished or uninspected spectral datum. No exact source trajectory has been rerun or reverse-engineered.

The adjacent `empirical_observation_countermodel.py` checks two exact rational slices, using `exp(-kt)=2^-t` at integer times and `s=1/4` versus `s=3/4`. It does not integrate any differential equation or execute owner code. All normalized nitrate observations are identical, while absolute product differs by three. The algebra above, not the finite check, establishes the continuum family.

## 2. Product-per-initiation is a separate ambiguity

If the supplied `b=epsilon*phi` identifies only primary initiation, even the association with net disappearance must not be assumed. For any fixed `b>0`, the pairs `(epsilon,phi)=(b,1)` and `(2b,1/2)` have identical linear effective initiation. A recovered-product factor `g` per initiation is not fixed by that product. The useful quantity depends on `b*g` in the linear regime, along with finite inventory and all losses. The event-energy floor therefore becomes a nitrate-energy bound only after an admissible product factor or a net-disappearance interpretation is independently established.

This does not license arbitrary unbounded product in the measured finite inventory. Under the separate original-N and net-disappearance contract, conservation still imposes `y<=1-x`, giving a favorable lower cost bound. Unknown selectivity can destroy a putative advantage without invalidating that favorable screening lower bound. The two interpretations must not be mixed.

## 3. What this does and does not establish about the actual evidence

The proof applies to the exact normalized-observation interface just stated. It does not erase the earlier Meroni calibrated fixed-time nitrate rows. Those fix a conditional product quantity in their own apparatus, concentration, matrix and tracer/background contract. It does not prove all of the published Wallace mechanism is nonidentifiable under every possible external constraint. It shows that the measurement types used in the cited normalized comparison, even strengthened with absolute nitrite disappearance, do not determine absolute product under conservation alone.

Nor do high-concentration measurements determine the same property at dilute capture-liquid conditions without a transfer premise. A selectivity function can agree with every supplied measured concentration and differ elsewhere. A smooth interpolation can do this for finitely many measured concentrations; this is a transfer-identification issue, not evidence that the actual chemistry changes arbitrarily.

## 4. Minimum evidence is query-dependent

In the abstract family, **one independently calibrated original-N nitrate amount** at a positive time determines `s`. With the delivered photon dose independently measured, the scalar product-per-dose quotient is then identified. If provenance, background and foreign-N input are already controlled, a separate gas measurement is not logically required merely to compute this scalar.

Explicitly, if `a=y(t_*)` is that independent amplitude, then

`s=a/[1-exp(-kt_*)]`, and `J(t_*)=a/q(t_*)`.

The first conclusion uses this constant-branch-fraction model; the second needs **no kinetic model at all**. Directly observed net original-N product and delivered dose identify their quotient at the measured endpoint. One amplitude does not identify arbitrary time-dependent selectivity at every later time, nor transfer the quotient to a new concentration, geometry or operating regime.

With defensible nonnegative intervals `a in [a_-,a_+]` and `q in [q_-,q_+]`, where `q_->0`, the identified quotient lies in

`[a_-/q_+, a_+/q_-]`.

Two operations can be robustly ordered for this query if those correctly matched intervals are disjoint. Response calibration, backgrounds, initial nitrate, foreign-N contribution and delivery losses must be reflected in these intervals where relevant; machine precision is not their uncertainty. A stronger model may sharpen the interval, but unmeasured full gas composition is not an automatic prerequisite for the scalar comparison.

In contrast, even with `s` fixed, split the remaining original N as `g_h=h*u` and `l_h=(1-h)*u` for any `0<=h<=1`. These conserving models have identical measured nitrite, original-N nitrate and product-per-photon, but different emitted original-N inventory `g_h`. The scalar quotient therefore does not establish gas retention or zero emissions. Inferring `u=1-x-y` by an assumed conservation law is not an independent experimental closure check. Detailed gas speciation, pollutant limits, reagent reset and wall-plug/auxiliary energy create additional independent questions for a complete operation.

The exact calculation records one independent amplitude fixing `s=1/4` and product/dose `1/128` in its arbitrary normalization, while gas original-N can still be zero or `9/16`. An artificial interval example shows disjoint product/dose enclosures can decide this query. None of these values is an experimental or model prediction for Dots' chemistry.

Closure requirements are claim-specific. Validated aggregate total-N and retained-original-N measurements, with the appropriate provenance and boundary controls, can establish some total-retention queries without identifying every phase or species. Species-specific emissions, mechanistic branch attribution and exhaust-quality claims require observations or validated bounds that identify those particular quantities; a complete process additionally needs its relevant material, energy and reset balances. No single demand for complete phase/species accounting should be imposed on every retention or product-per-photon comparison. Conversely, a calibrated nitrate amount without controlled original-N provenance can still be insufficient for the exact *original*-N target. Nothing here establishes that the current experimental evidence satisfies any of these additional contracts.

The strategic lesson is not “demand every possible measurement.” It is to identify the **smallest independent observable that changes the current consequential decision**, and to distinguish it from requirements of stronger claims. Otherwise an appropriate skepticism can create an endlessly growing admission barrier, preserving correctness while never allowing a useful scoped result. The original-Dots preserved distinction between observed nitrate and whole-plant claims supports that narrower approach.

Historical novelty of this identification argument is not claimed. It is a standard mathematical nonidentifiability construction applied to Astra's actual source interface; its value is diagnosing what a future research method or additional reasoning can and cannot supply.
