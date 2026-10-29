# Clock-to-data bridge result, 2026-10-29

1. **Proved: actual physical-time inclusive fault-insertion bound.** `PHYSICAL_TIME_FAULT_INSERTIONS.md` proves ||F(S)||_diamond <= (eta T)^|S| for deterministic noise cells, retaining the common bath and the actual reset-record instrument. Covers bounded local Hamiltonians and added bounded Lindblad terms whose independent strength interpolation remains CPTP. Does not require independent clocks or stationary states. This is a genuine replacement for a marginal-error argument, but it does not establish autonomous data-error correction.

2. **Proved: update-index interval-noise transfer fails.** `DATA_EXPOSURE_COUNTEREXAMPLE.md` gives specified update intervals in the independent-Poisson marching-soldier comparator with large simultaneous physical data exposure under arbitrarily weak bounded local nonunitary noise. Includes an operational completed-measurement-output variant using actual Kraus-label records. The reset-erasure caveat is explicit: discarded-output reset maps can erase the damage, so do not claim their reduced-data completed channels are faulty.

3. **Not proved:** a threshold for the guarded-clock architecture; a bounded spread/cluster decoding theorem for controller faults; a direct transfer of independent Poisson timing to finite-kappa clocks; a threshold for a two-site lease implementation; arbitrary signed generator perturbations under the interpolation theorem. No such claims should be inferred.

The remaining exact action is to prove a data-correction/cluster semantics theorem for the physical-time fault model plus the actual clock instrument, or redesign the maintenance schedule to prevent large uncharged idle exposure. Controller liveness and equal-time defect sparsity do not supply that theorem.
