# Actual correction cadence and acquisition-based selection

28 October2026. Author construction and simulated data; independent review pending. This extends the frozen clocked model under the **mandatory-channel/no-quantum-bypass** contract. It is not a general passive-memory lifetime result or a new code/selection algorithm.

## Physical policy family

Keep T mandatory native uses, with the same previously acquired onsite inverse after **every** native use. Apply the actual coherent-noisy/background-exposed flagged EC only after each r uses, for r in {1,2,4,8,16,32}. T is32 or64 and divisible by every r. Ancillas are freshly prepared locally for each EC; no ancilla carries information around a mandatory link.

The deterministic calculation propagates the actual physical five-qubit operator as

    (F N^r)^(T/r),

not as a powered decoded logical channel. Since native channels are independent across ports and stationary in time, N^r is computed by powering each local physical channel, without changing its meaning. The final ideal decoder is used only for the terminal metric. The EC map F is the actual clocked instrument with physical corrections, total fallback and both data/ancilla background noise.

Only the T/r EC windows actually scheduled are charged. Each has201 reference units and the specified integrated background strength; every native/inverse phase costs2. Thus elapsed time is

    2T + 201 T/r.

Across cadences, elapsed times differ because fewer local correction operations are executed. Within **each** policy comparison, the unencoded baseline uses exactly the same elapsed schedule and fixed acquired inverse. Its endpoint map is

    (D_window N_site^r)^(T/r),

not D_total N_site^T: the noncommuting order is preserved. This is fixed mandatory-use count with policy-dependent correction latency, not a fixed-wall-time comparison across policies. Five carrier exposures versus one per native use remain a separate resource cost.

Source-informed terminal full-CPTP oracle values and the separate all-adaptive single-carrier ceiling are diagnostics, not learner inputs. The latter uses the reviewed/being-reviewed concurrence statement in `clocked_flagged_storage_20261028/adaptive_single_carrier_bound_v1.md`:

    F_e(single carrier) <= [1+(399/401)^T exp(−(T/r)*integrated)]/2.

Its mandatory unmonitored native-phase and no-quantum-bypass assumptions remain essential. Equal-resource standard coding can implement the same pipeline; no algorithmic superiority follows from beating a single-carrier strategy.

## What cadence changes in this grid

AtT32 and integrated background.03 per EC window, r1 has F_e=.796645 and r2 improves to.824462. The r2 value exceeds its stronger one-carrier ceiling.763646. AtT64 the corresponding r2 fidelity is.687990, versus r1.64780.

At background.1, r1 fails badly (F_e=.368335); r4 improves to.561440, but its matched-schedule source-informed terminal oracle achieves up to.62527 and the all-adaptive ceiling is.691446. This is a partial absolute-quality rescue, **not** recovery of an advantage over the strong comparator, nor success at the predeclared.6 target.

At background.3, best-grid r8 gives F_e=.329672 atT32, still below the feasible classical measure/store/reprepare benchmark.5. Cadence is useful but does not remove the controller-noise obstruction.

The grid is a source-informed deterministic diagnostic. Its best r must not be described as operationally learned merely because the channel calculation reveals it.

## Separate counts-only policy selection

`HOLDOUT_PLAN_v1.json` was frozen before any fresh policy-selection or validation sampling. The computational grid had been generated but its r>1 scores were not inspected before the plan; earlier fixed-r1 results were known. This is an internal predeclared pilot, not an externally registered blind experiment.

The learner receives only2048 ordinary matched-logical-Pauli trial outcomes for each of the six policies. It chooses the fewest failures; ties choose larger r to reduce time. It receives no hidden background rate, channel matrix, oracle result or source parameters. A fresh independent8192-trial validation then tests the fixed target

    matched-state failure probability <=4/15,
    equivalently F_e >=3/5 under the trusted logical preparation/readout interface.

The one-sided binomial lower-tail decision uses exact integer arithmetic under rational null4/15 and alpha1/3000. Across three simulated contexts, family failure is at most1/1000 for the implemented record law. The52-bit floor-CDF sampling approximation contributes at most61440/2^52 relative to the supplied floating Born probabilities. The quantum-channel coefficients themselves are **not** outward-rounded; translating this to a physical quantum fidelity statement is conditional on the trusted logical interface and numerical model. No certified diamond bound follows.

The selected r values were2,4,8 for the three contexts, matching the post hoc best numerical grid values in this run. Only the first context passed the.6 target. The other two failures are retained; there is no reselection or extra sampling after failed validation. This is ordinary finite-policy selection, not a newly claimed learning algorithm. A strong equally informed conventional learner could use the same outcomes and policies.

## Full acquisition and interface cost

Each encoded trajectory atT32 consumes160 native carrier exposures. Selection and validation together use20480 trajectories per context, or3,276,800 native exposures. Across all three contexts the new pilot consumes **9,830,400 native exposures** and127,838,208 aggregate reference-time units, plus endpoint preparation/readout overhead not modeled here. These are simulated costs, not laboratory measurements. The earlier learned-frame acquisition is inherited, separately paid capital; its cost is not erased.

Selection and validation use ideal trusted logical preparation and terminal ideal decoded-Pauli readout, the same one-off boundary retained by prior packages. Demonstrating these with noisy hardware remains an independent obligation. The implementation retains raw setting/outcome counts, seeds, quantized CDFs, exact-tail digests, policy decisions and source-informed post hoc scores separately.

## Reproducibility and preservation

`cadence_sweep_v1.py` and its failure log are preserved: the numerical computation completed, but serialization failed on a NumPy Boolean. Version2 changes only that cast and output filename; it supplies the36 numerical policy/context/horizon results. The scientific grid was not changed. The original clocked and ideal-idle sources remain intact. `learn_cadence_holdout_v1.py` refuses to overwrite existing raw sampled counts.
