# Aggregate resources and uniform receiving effect
30 October 2026. Scope clarification for the reviewed classical capture theorem. No new quantum-consumer claim.

Use R for the number of records and b for each record block size, to avoid confusing them with the norm constant M.

- Physical classical storage: O(R b) two-level sites, with fixed bounded degree/body and fixed rates. Hardware constants can be enormous and the admitted fixed noise tolerance can be very small.
- Scheduled capture: O(R b) site-time and O(log b) parallel stage depth/wall time, once fixed seed/reset/stage constants are included. This is a declared scheduled architecture, not an autonomous one.
- Final retention to horizon H with per-record permanent-mark contribution at most epsilon: b=O(log(H/epsilon)) with a sufficiently large fixed coefficient. This gives exponential lifetime in the PER-RECORD block size b, not in total device volume R b.
- Actual fixed root ports and bounded read fanout are included. The optional terminal reset/CNOT copy-out adds O(R) output sites and fixed parallel time. An external detector's noise contract remains separate.
- The theorem earns a small constant physical-port error parameter, not perfect simultaneous correctness of every record. If a user needs all R ports correct with failure at most epsilon_total, a union bound pays R p_port, and the architecture/parameters or another error-correcting consumer must meet that distinct target. Increasing b alone removes phase escapes but does not remove the stationary local-port floor M/(1+K v0).

For the contemplated ATG source with code size N and temporal depth T~N, retaining every raw outcome means R=O(NT)=O(N^2). If the desired horizon is H=exp(cN), then b=O(N) and classical storage is O(N^3). Retaining only O(N) boundary records would instead cost O(N^2), but discarding/releasing bulk records requires a supplied actual decoding/processing interface. It is not implied by the port theorem. No constant-overhead source or lifetime exponential in the total physical device has been proved.

## Uniform effect form
For each supplied genuine historical m, capture is a physical CPTP map T_m on arbitrary conditional Q/bath input, with the raw |m> input and actual target-reset routine included. The proof is uniform for every positive input and retained reference. Therefore its final port conclusion is equivalently

 T_m^*(E_S)<=p_port^|S| I,

where E_S is the product of actual final port-error projectors relative to m. This immediately gives the valid SEQUENTIAL bound

 Tr[E_S T_m(P rho P)]<=p_port^|S| Tr(P rho)

for any source-side positive corner P rho P in that input space. It does NOT identify a source's coherent defect projectors with classical trajectories, make those projectors commute with a different instrument, or establish a combined source/capture common-span certificate. The precise source instrument and quantum receiving argument remain necessary.
