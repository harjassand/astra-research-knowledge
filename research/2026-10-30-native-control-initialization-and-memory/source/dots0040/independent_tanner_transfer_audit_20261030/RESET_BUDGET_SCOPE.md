# Reset-budget comparison: scope, not an optimality claim
2026-10-30.

Primary comparison: [Baumann–Stein–Linnhoff-Popien, The Fundamental Memory Ceiling of Noisy Quantum Reservoirs](https://arxiv.org/html/2610.26228), dated 19 October 2026.

Its ceiling concerns discrete-time Markovian reservoirs with a fixed local depolarizing layer, charged entropy sinks, and no classical feedback. The relevant memory notion is echo-state memory after initialization washout. Its reset-budget formulation bounds entropy removal through E(I)<=2^b I; fresh reset qubits are a special case. Exponential dependence on reset budget is achievable in that setting.

Those hypotheses do not automatically cover an arbitrary initially encoded quantum state, a retained non-Markovian bath, or our continuous-time coherent-noise model. A discrete fixed-depolarization theorem cannot simply be Trotterized while keeping its constants. Consequently exp(cN) at O(N) reset capacity is consistent with the reported scaling, but is NOT a proved universal optimum for the Tanner-memory theorem here.

Our separate accounting: fixed-degree local atomic instruments number O(N), each admits a bounded-size local dilation and is attempted at constant rate. Thus supplied workspace-reset CAPACITY is O(N) per unit physical time. This is neither actual entropy production in a quiet trajectory nor a Landauer heat estimate. A physical controller or entropy sink must still be specified to turn that capacity accounting into hardware resources.
