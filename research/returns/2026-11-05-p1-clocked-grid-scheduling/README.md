# Energy scheduling for clock-driven grid disturbances

The supplied construction assigns phases to indivisible recurring tasks while preserving their service cadence, then certifies cumulative event-energy imbalance and its effect under a **separately supplied** dynamic response model. It is motivated by published minute-locked grid disturbances and an incomplete firmware mitigation. The physical source mechanism and proposals to desynchronize tasks are already in the empirical literature; this return supplies a conditional scheduling/resource construction, exact rational software certificates and scoped public-data reanalysis.

| Distinct result | Direct route |
|---|---|
| Weighted energy schedule, jitter law, whole-response bound and finite execution | This page and [complete proof](package/theorem_energy.txt) |
| Arbitrary heterogeneous waveform scheduling for selected harmonics | [Independent harmonic construction and error/deadline limits](harmonic-scheduling.md) |
| Published measurements, phase-locking calculation and replay limits | [Evidence and data page](measurements-and-evidence.md) |
| Original material | [ZIP](original/clocked_grid_research.zip), [complete captured return](P1_CLOCKED_GRID_20261105_RETURN.txt), [provenance and hashes](SOURCES.json) |

This is not a new physical mechanism, historical-priority finding, deployed UPS controller, field experiment or demonstrated civilisation-changing capability. Firmware access, complete waveform metrology and an applicable grid response remain unacquired for a deployment. Capital performs no scientific rerun or new audit.

## Recurring physical model and exact schedule

Each device i in class c executes a causal signed grid-facing waveform `e_i h_c` once every period T, with `e_i>0` and `integral |h_c|=1`. The response includes the full diagnostic, recharge and operating-state effects at the actual interface; net energy alone need not equal its L1 energy. Changing the start phase must leave that response valid within declared errors. No pulse-amplitude actuator, shortened diagnostic, removed task or new control access is granted.

For class energy `E_c=sum_i e_i`, choose weighted midpoint phases

```text
phi_i=T (sum_(j before i)e_j+e_i/2)/E_c.
```

The weighted event train minus its uniform mean has a primitive that jumps from `-e_i/2` to `+e_i/2` at event i and declines linearly between events. Its oscillation is exactly the largest event energy `e_max,c`. Every phase schedule has a jump at least that size, so this is optimal for the **cumulative event-energy metric**. It is not an optimality theorem for every waveform peak, grid response or heterogeneous multi-class objective.

When every event may move independently by at most delta, the one-class long-horizon minimax primitive oscillation is exactly `e_max+2(E/T)delta`. The lower bound uses adversarial per-event errors and well-separated extrema over a sufficiently long schedule. It is not assigned to one fixed offset per device, short horizons or all error-correlation structures.

Convolution with the signed unit-L1 kernel preserves the centered primitive bound. For fixed repeated per-device waveform residuals of L1 size at most `eta_i`, a sufficient full budget is

```text
B=sum_c[e_max,c+2 E_c delta_c/T]
  +sum_i[(1+2 delta_i/T)eta_i].
```

The residual's timing effect is included. Arbitrary changes on every cycle need an additional cumulative-energy contract; a stationary repeated-waveform bound cannot be assumed for them.

For a supplied stable causal bounded-variation response kernel g, peak incremental output frequency is bounded by `(B/2)(|g(0+)|+TV(g))`. For `M f_dot+D f=-u`, `M,D>0`, this becomes `B/M`. Initial response and uncontrolled disturbances remain separate. A measured static power–frequency slope does not identify the dynamic kernel, and different injection locations need compatible response classes or a network model. Energy imbalance alone does not control instantaneous power, RoCoF or nonlinear grid stability. The full proof separately gives power bounds under the required bounded-variation waveform assumptions.

## Finite compiler, commissioning and retained state

The midpoint construction needs `O(N)` arithmetic. The supplied [compiler](package/compile_schedule.py) uses exact rational arithmetic, rounds to actual timer ticks and checks primitive extrema at event boundaries rather than temporal samples. [Synthetic fleet input](package/fleet_input.json) and [compiled schedule/certificate](package/fleet_schedule.json) make its result reviewable; they do not operate grid equipment.

Deployment needs manufacturer-supported timing control preserving diagnostic validity and recovery deadlines. Commissioning advances tasks using shorter permitted intervals until their new phase is reached. The old nominal phase is explicit, with minimum recovery and maximum deadline checked using `2delta` guards. Total advance is less than one period and can bring at most one nominal additional execution per device into the transition window. Its energy and aggregate transient still need reserve; the steady-state bound is not claimed during migration. If exact spacing T is immutable and neither early nor late tests are allowed, phase migration is impossible under that interface.

Each endpoint retains phase, period, schedule version and executed-event state across reboot. Catch-up bursts or mandatory simultaneous restart tests need separate load budgets. Membership changes require recompilation or an explicit dropout allowance. No per-cycle central message is required after valid commissioning; clock maintenance, communication for calibration/assignment and local execution remain real work. The mean power demand is not removed.

With `Q=T/q` timer slots, midpoint rounding gives span at most `e_max+E/Q` before other errors; some slot must carry at least `E/Q` energy. Fixed timer precision does not guarantee fixed absolute error as a fleet grows on the same grid. Worst-case differential waveform/calibration errors also accumulate. Constant common clock offsets only shift the schedule, and common positive class gain rescales it; the adversarial floor is not a universal statement about shared errors or grids whose response changes with scale. High-frequency smoothing must be measured, not inferred from unresolved samples.

## Supplied numerical evidence and ordinary alternatives

Synthetic integer-weight fleets of 16 through 4096 devices use energies 5–100 J, period 60 s and a 1 ms timer. At N=4096, the recorded event spans are 213849 J aligned, 6335.321 J for **one** random assignment and 103.3783 J for the midpoint schedule, versus ideal exact largest-event bound 100 J before timer rounding. These are mathematical examples, not UPS measurements, random-phase percentiles or measured grid improvements. [Recorded results](package/results.json), [original program](package/reproduce.py), [supplied figure](package/evidence_and_construction.png).

Independent random phases may already be operationally adequate. Converter interleaving, DESYNC, weighted fair queuing, network-calculus jitter bounds and Shapley–Folkman aggregation are established machinery. The harmonic companion retains the stronger ordinary common-template interleaving comparison. No exclusive mitigation or practical superiority over these alternatives is established. [Evidence audit](package/evidence_note.txt), [lattice calculation](package/lattice_randomization.txt), [original harmonic proof](package/math_note_harmonic.txt).

The observational/data results and licensing are [separately navigable](measurements-and-evidence.md). The supplied Astra retrieval record uses prior certificate/response-metrology distinctions without importing an unrelated signing theorem or a thermal-RC response model into the grid. [Immutable retrieval provenance](package/astra_retrieval.txt). Original proof, source data, programs, outputs and attribution are retained without scientific execution. Generated current retrieval has not been rebuilt; these scientific pages and complete package are directly available on GitHub.
