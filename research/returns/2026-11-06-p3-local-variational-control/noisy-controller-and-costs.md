# Ring certificate, noisy interface and paid commissioning

The [complete P3 source](P3_LOCAL_VARIATIONAL_CONTROL_20261106_RETURN.txt) reports an eleven-bit local controller for a homogeneous binary ring. `0→1` admits a job, `1→0` completes it; selectable rates lie in `[0.05,1]`. Reward counts completions minus `0.08` per jump, `0.01` per site-time and neighbouring-occupancy congestion. Useful-work semantics belong to this supplied model, not an independently established physical output interface.

The 2,048-entry endpoint-command table has 29 binary decision nodes and a 98-Boolean-gate realization. Separate exact certificates bound every ring length `n≥11`, using temporal potentials for endpoint transients and spatial differences that telescope around the ring. The de Bruijn maximum-cycle-mean characterization supports finite-window spatial inequalities. The all-length claim is reported as a theorem, not extrapolation from simulations. The independent integer verifier reportedly reconstructs full generators for lengths11/12 and checks all circuit words; those finite checks and files have not been delivered to Capital. An upper Bellman approximation alone does not certify its greedy policy: the selected policy has a separate lower certificate, with finite-block convergence as fallback.

| Ideal source-model quantity, per component per plant-time | Reported bound |
|---|---:|
| Delivered policy reward, long-run lower | 0.218607767932699 |
| Every admissible global controller reward, upper | 0.220642351774732 |
| Certified gap | 0.002034583842033 |
| Delivered completed-work lower | 0.291070773877436 |

Safe rounded finite-time bounds are `0.21860776−1.10795072/T ≤ E Rlocal/(nT) ≤ supπ E Rπ/(nT) ≤ 0.22064236+2.03700893/T`, from every initial state.

The noisy apparatus contract is narrower than the general theorem: two stationary primitive rates per component in `[0.04,1.01]`, state-independent while held; noninvasive reads; faulty commands select a primitive without adding an unbounded transition channel. The instance has64 components, raw-read fault probability `10⁻⁵`, logic/wire/latch and pin-write probabilities `10⁻⁶`, update interval `0.0005`, latency bound `10⁻⁵` plant-time,284 vulnerable locations per call and calibration failure budget0.01. These are **declared model parameters**, not hardware measurements.

For a constant rate `r`, parity of two reads separated by `Δ` has probability `(1−exp(−2rΔ))/2`. The unknown initial bit cancels, so this assay needs neither reset nor equilibrium. The inference program is reported to consume observed counts/uncertainty bounds, not synthetic true rates, with finite-bit rational enclosures for transcendental bounds. Aggregate calibration needs independent packets; a separate simultaneous-interval fallback has weaker dependence assumptions and looser bounds, with distinct confidence events. The supplied **synthetic** record reportedly gives mean endpoint discrepancy `η≤0.005201388` at confidence≥0.99.

On that calibration-coverage event, expectations over subsequent plant/apparatus noise obey:

- Reward lower: `E Ractual/(64T)≥0.20424123−1.10796330/T`.
- Ideal global comparator upper: `supπ E Rπ/(64T)≤0.22740447+2.03700893/T`.
- Completed-work lower: `E Wactual/(64T)≥0.27968905−3.11053900/T`.

These include calibration discrepancy, read/logic/final-latch error, stale observations and latency, **before separate digital/infrastructure overhead**. The comparator has perfect state access, global history and instantaneous commands; this supplies an upper bound, not a matched physical advantage. An ordinary equally informed factored-control implementation can use the same certificate/circuit. Physical useful completion and a paid output meter still need a real source contract.

| Resource | Reported sufficient cost for64 components |
|---|---:|
| Calibration parity packets / raw readings / pin writes | 256million /512million /256million |
| Parallel commissioning duration bound | 1,600,048 plant-time units |
| Online reads per component per plant-time | 22,000 |
| Online circuit-location uses per component per plant-time | 568,000 |
| Controller calls per component per plant-time | 2,000 |
| Streaming calibration storage | `O(n log K)` bits |
| Retaining every packet | `O(nK)` bits plus I/O |

Paid fabrication, programming, reliable offline computation, calibration electronics, routing, synchronization, cooling, deployment, memory reset and final-state handling remain. In reward units, running overhead is conservatively `cctl=(11cread+284cloc+cclock)/0.0005+croute+pstandby`. Nominal workload event costs do not automatically pay it.

For commissioning duration `Tc` and other one-time cost `C₀`, the source's campaign lower bound is

`E Rnet/[n(Tc+T)] ≥ [−1.0908Tc+(0.20424123−cctl)T−1.10796330−C₀/n]/(Tc+T)`.

Even setting extra digital overhead and other one-time costs to zero leaves a conservative break-even operation of roughly **8.5million plant-time units**. There is no conversion to seconds/joules without a physical source, and calibration reuse requires stationarity or proved drift allowance. Symbolic prices/synthetic calibration are not fabrication feasibility or resource superiority.

The original ZIP is held after one failed transfer; report/code/record/checker claims above come from the complete visible return. Capital performed no replay, simulation, circuit or proof check. Earlier quantum, preparation, reconstruction, sensing and first-event results retain their scopes without an assumed physical reduction.
