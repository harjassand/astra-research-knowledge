# Costs and operational contract

Worker: gd_physical_operation. Date: 16 October 2026. Overall physical status: NOT_ACQUIRED. This means no acquired same-apparatus demonstration supplies the structured catalog, positive floors, completed pair correctors, locality and a useful common rate margin together. It does not mean these components are physically impossible.

## Intended useful operation and the selected route

The useful output is preservation of an arbitrary unknown quantum state, including entanglement with a reference, for longer than the strongest equally informed operation on the same apparatus at matched elapsed time and total resources.

The selected realistic experimental route is a coherent syndrome predicate mapped to an ancilla, a conditional one-face Pauli, and explicit ancilla entropy export/reset. Begin with an isolated two-check gadget and then an actual eleven-data-qubit pair patch. A fixed deliberate physical Pauli-dephasing floor is a separate control operation. This is the closest obtainable implementation of the source interface; its ingredients are established, while their required joint regime is missing.

Two implementations must be distinguished:

| Operation | Explicit ideal implementation | Main cost |
| --- | --- | --- |
| Exact supplied C_pair | Extract two check bits coherently, compute AND, uncompute both bits, conditionally write one face, reset only the flag | Three ancillas, 31 conventional two-qubit gates in the displayed construction, basis rotations, wiring and flag reset |
| Finer C_fine | Measure the two commuting checks and conditionally write the face; reset both measurement registers | Two ancillas, 12 parity-extraction CNOTs plus conditional control, readout/feedback or coherent classical logic, two resets |
| Active jump D[Q Pi] | Continuous conditional pumping without the inactive completion | A different generator; its Pauli-noise statement does not acquire the completed model's coherent robustness |
| Sparse physical floor | Independent real Pauli phase kicks or a justified engineered reservoir | Actual pulse/reservoir duration, amplitude/bandwidth error, cross-talk and additional entropy/noise |

All counts are constructions, not demonstrated fidelities or lower bounds. Full two-check measurement is often the easier experimental route, but its inactive coherences differ by order one from the exact source channel. LOCAL_OPERATION_LEMMAS.md proves both the distinction and a conditional quantum-span extension for the finer version.

The mathematical noise proposal channels need not be separately implemented at their inferred proposal clocks. They are a positive representation of an already present floor plus actual generator error. By contrast, implementing the ideal correction channels with finite gate sequences requires an apparatus-to-generator transfer argument.

## Costs that must be acquired on the same patch

| Boundary | Charged quantity and present evidence |
| --- | --- |
| Input state | Preparation time, entropy and errors for a reference-entangled encoded state, together with a fixed recovery convention. Source assumes exact encoding and final decoding. No matching physical acquisition. |
| Noise catalog | Known Hermitian Pauli labels, all allowed coefficient positions, M_ab and u_p with units, confidence and validity period; plus an out-of-catalog remainder. No such bounds acquired for an eleven-qubit pair gadget. A sparse best fit is insufficient. |
| Natural relaxation | Measure T1, excitation, leakage and reset-induced loss during every substep. A qubit T1 does not determine the entire local GKSL matrix or independence. |
| Deliberate floors | Every gamma_p, support diameter, incident count and pulse/reservoir implementation. The fixed-design compiler charges row sums and product directions, not only original local noise labels. No positive uniform lower floor bound acquired. |
| Coherent controls | Pulse shape, calibrated Hamiltonian, duration, bandwidth, amplitude/phase stability, drive power and stochastic record. Software frame bookkeeping alone is not physical dephasing of an idle data state. |
| Multi-check correction | Full eleven-qubit conditional channel or a separately declared refinement; population pumping and a high average fidelity alone do not specify it. No same-patch instrument acquired. |
| Control errors | Per-operation diamond bounds or a justified probabilistic/structured model, coherent accumulation, propagation through parity gadgets, leakage, cross-talk and pulse overlap. No inference of rare CPTP faults from gate fidelity alone. |
| Reset | Complete state reset, delay, residual excitation, action on spectator data, cavity/motional memory, emitted photons and heating. A reported reset-drive duration is not the full reset-cycle duration. |
| Entropy export | Coarse predicate flag has dimension two; full separate syndrome registers have dimension four. Work ancillas return pure only for the ideal uncomputation. Actual discarded entropy, bath state and reset reliability remain unknown. |
| Energy | Integrals of delivered/control-line powers, reset emission, readout amplification, refrigeration/laser/vacuum overhead and reuse amortization. No joule or economic advantage was acquired. A gate count is not energy. |
| Timing | Entire gadget duration tau, idle interval, repeated-cycle schedule, queueing/serialization and late events. Independent instantaneous Poisson evolution is a model premise, not a conclusion from a working circuit. |
| Classical control | Calibration/optimization runs, waveform memory, random bits, trigger timestamp precision, record storage, readout, and feedback/frame adaptations. Measurement-free recovery still needs programmed drives and a reset environment. |
| Locality | Body count and geometric diameter are separate. Source requires a periodic four-dimensional local graph and bounded incident fault supports. No bounded-density three-dimensional realization with fixed range was acquired. |
| Reliability | Drift periods, rejected data, calibration uptime, rare bursts and controls enabled during characterization. No all-time catalog guarantee or useful numerical memory threshold acquired. |
| Output | Compare unconditional channel error at fixed wall time or useful lifetime at a declared infidelity, with identical encoding/readout and no selective record discard. No matched apparatus trial was executed. |

A continuous-reservoir route could avoid circuit start collisions. It would instead require a microscopic coupling, finite reservoir memory and a controlled elimination approximation on the eleven-qubit patch, including its error over storage time. No such paid construction was acquired here.

## Exact rate budget and finite-duration charge

For the source's signed catalog,

    E = sum_ab C_ab(P_a rho P_b - {P_b P_a,rho}/2) - i[sum_p h_p P_p,rho],
    |C_ab| <= M_ab, |h_p| <= u_p,

the fixed floor and ceiling are

    F = sum_p (r_p + beta_p) D[P_p],
    r_p = sum_q M_pq,
    beta_p = (1/2) sum_(a!=b: product label p) M_ab + u_p,
    Lambda <= 2 sum_ab M_ab + 2 sum_p u_p.

The ordered coefficient sum counts an off-diagonal edge twice. Product floors and proposal supports occupy the union of the two Pauli supports. Per-cell or per-guard incident totals are the operative budget. Dividing a large patch into arbitrary names cannot reduce physical incidence.

For a single drift mode |h|<=u, gamma=u minimizes the modewise worst-case proposal rate 2u. Installing gamma also produces an actual coherence decay rate 2u. The floor is not an error-correction mechanism in isolation.

An illustrative 100 Hz residual detuning bound means h<=pi*100 per second, a floor of 314.2/s, and a compiled rate of 628.3/s on each data qubit. With six data modes owned by a fine cell this becomes 3,769.9/s. This example supplies no measured residual bound.

The source needs twelve correction streams per fine cell, each with rate kappa, and twenty-two correction support incidences per data qubit. The direct independent-start gate route has at least one-qubit collision probability 1-exp(-21 kappa tau). For a hypothetical one-microsecond entire gadget and a chosen one-percent contention tolerance, kappa<=478.6/s. At five microseconds it is <=95.72/s. These are route-specific scheduling arithmetic; the source gives no numerical acceptable noise fraction. Even a very good measured gadget cannot be assumed to instantiate its independent clocks.

For a digital instantaneous noisy channel C_actual, the generator difference kappa(C_actual-C_ideal) is a signed local map. A small circuit diamond error gives a norm bound but not automatically the sparse coefficient promise. A near-identity unitary cannot be a nontrivial convex mixture of Id and a rare faulty channel. This exact obstruction is proved in LOCAL_OPERATION_LEMMAS.md. Treating all coherent gate errors as independent stochastic Pauli faults is an additional physical intervention/model assumption.

## Acquisition and calibration cost

Published noise-learning experiments demonstrate useful practical fits; they do not furnish the catalog for this gadget. A full eleven-qubit process has exponentially many parameters, while the sparse route reduces this only if the sparse physical interface is justified. The apparatus must supply sufficient independent preparations, control settings and measurements to bound allowed coefficients and residuals, including SPAM uncertainty.

For a fixed scalar Ramsey observable bounded in [-1,1], independent-shot estimation within additive delta with failure probability alpha can use

    n >= 2 delta^(-2) log(2/alpha)

by Hoeffding's inequality. Estimating m observables with a simple union bound replaces alpha by alpha/m. This is only an elementary shot budget; converting these observables into generator bounds, handling correlated shots and controlling drift is a separate acquisition problem. The cost must include calibration refresh and failed models, not just the final fit.

The decisive measurements must occur with the same correction/reset/floor drives enabled. A quiet idle Ramsey scan is not a certificate for gated, measured and reset operation.

## Strong equally informed alternatives

| Alternative | Same-information comparison and accounting |
| --- | --- |
| Retain continuous drift and ordinary quantum trajectories | Models the original amplitude damping/Hamiltonian without installing a floor. Pays continuous propagation and state-dependent jump simulation. It does not prove the source's common good-schedule event. |
| Calibrate phase and use echo/DD | For static one-Pauli drift, ideal echo cancels the drift without adding dephasing. Pays pulse width, pulse error and calibration/spectral characterization. DD can fail for white Markov noise and can disturb a correction circuit unless controls and frames are adapted. |
| Periodic coherent recovery plus reset | Directly uses demonstrated channel-simulation/QEC operations. Pays finite recovery error, ancilla reset and an optimized repetition period. It is the closest operational incumbent and requires fewer unsupported clock assumptions. |
| Conventional repeated measurement QEC | Pays ancillas, syndrome readout, leakage removal and real-time or final decoding. It already has published below-threshold quantum-memory evidence under its own architecture. It is not equivalent to the asynchronous 4D model. |
| Small autonomous bosonic/qudit QEC | Existing experiments already exchange syndrome entropy with ancillas/reservoirs. These are strong local primitive precedents, but their code/noise/locality differs and their physical lifetimes cannot be transferred to the toric construction. |

No experimental winner between the proposed joint model and these alternatives was acquired. For the isolated constant-drift subproblem the ideal floor strategy loses to an ideal equally informed echo by adding avoidable dephasing. That falsifies a claim that the compiler itself supplies superior local noise suppression; it does not rule out a proof benefit for a noisy many-qubit memory.

## Decision

The available physical operation is standard coherent syndrome recovery with paid reset. The exact added contribution supplied by the compiler is an algebraic positive schedule representation under a qualified error interface. There is no acquired regime in which its full structured-noise assumptions, physical floors and eleven-qubit correctors coexist below a demonstrated useful rate ceiling.

Required status for that joint regime: NOT_ACQUIRED. Required status for practical advantage: NOT_ESTABLISHED. Further publication of this handoff should preserve the active/completed/finer/regularized generator distinctions and all unknown costs.
