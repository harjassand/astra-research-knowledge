# Private-terminal discovery of a common Pauli-protected subsystem
2026-10-29. Root-proposed construction, derived and finite-tested by compilation branch. Status: independent audit pending. Governing correction: this is a common-algebra promise, NOT generic unknown-noise capacity, arbitrary unknown frame, or an iid approximation to quantum memory.

## Promise and resource target
There are n physical source-input/output qubits B, arbitrary retained source memory M, and a fixed unknown Pauli label subspace S* of F_2^(2n). Its restricted symplectic rank is2a*, radical dimension b*, and cost a*+b*<=g=n-k0, with known1<=k0<=n. Each actual conditional joint source interaction, including history/time-dependent interactions, has Kraus expansion

  V_{r,t}=sum_{s in S*} P_s tensor A_{r,s,t}

on B and source memory. The A operators can change memory dimension and need not commute. Source evolution and memory initial state are otherwise unrestricted. This support promise must apply to every interaction on the actual protocol histories, not merely an average channel fitted from data. Private reference registers and controls are not accessible to the source. Source call timing and all source-visible control side channels must not reveal the private terminal/probe role.

Goal: produce k0 ebits with small **expected Bell infidelity**, then teleport fresh payloads through those ebits. It is not a promise that a fitted code works for later unobserved calls.

## Physical protocol
Before starting privately choose T uniform in{1,...,N}, independent of source. For t=1,...,T:
1. Let S_t be the binary span of all Bell labels from rounds before t. Initially S_1={0}. Compile its Pauli algebra using v1 H/S/CNOT/SWAP elimination. Its cost is at mostg. Pad the gauge subsystem to exactlyg qubits and retain k0 logical qubits. Write C_t=U_t† for the resulting actual encoding Clifford.
2. Prepare n trusted fresh Bell pairs R:B. Apply C_t to B, then submit B through the source interaction. The retained memory M may be arbitrarily correlated with the past.
3. If t<T, apply C_t* (entrywise complex conjugate in the computational basis) on the private reference R. Measure R:B in the n-pair Bell basis, obtaining label v_t. Update S_{t+1}=span(S_t,v_t).
4. If t=T, instead apply C_t† to B, discard theg gauge qubits from each of R and B, and retain the k0 logical Bell-pair resource. No Bell measurement is performed in this terminal branch.

The reference conjugate has an explicit gate implementation: H,CNOT,SWAP are real, S conjugates to S†. Reverse/inverse/conjugate order must follow the emitted circuit convention; no dense-unitary oracle is required. Both roles have identical source-side preparation C_t and timing until the source call finishes. Role-dependent operations occur only afterwards on private/returned systems. All B inputs have marginal I/2^n. T is not revealed before the terminal call; source behavior on probe prefixes matches a conceptual all-probe run.

## Probe identity including retained memory
Condition on any probe-prefix history and its resulting memory state. The Bell identity

  (C_t* tensor C_t)|Phi_d>=|Phi_d>

holds exactly. C_t* on private R commutes with the source's joint operation on B,M. Therefore the physical probe state/instrument equals one obtained by applying the joint source directly to an unencoded Bell pair. In particular its Bell probabilities are the diagonal process coefficients p_t(v) of the conditional physical channel, and v lies in S* surely. The resulting memory instrument is also the same, not only its outcome distribution. This is why future source memory is not replaced with an iid state in the argument.

For a joint unitary V=sum_v P_v tensor A_v, the physical conditional instrument on memory is rho_M -> A_v rho_M A_v†. General Kraus sources sum this expression over Kraus index. These formulas can be used for exact simulation without constructing an exponentially large reference density matrix; the finite fixture separately verifies the actual reference controls.

## Terminal identity and innovation accounting
The terminal state before gauge discard is Choi(C_t† o E_t o C_t), with the same conditional E_t as the probe counterpart. Tracing the gauge on both R and B makes the logical state exactly the Choi state of the mixed-gauge encoder and discard decoder. By COHERENT_MIXED_GAUGE_BRIDGE_v2.md its Bell fidelity is

  F_t=sum_{v in G_t} p_t(v),

where G_t is the full Pauli subspace acting only on the chosen g gauge qubits in compiled coordinates. S_t is contained in G_t, hence

  1-F_t <= Pr[v_t notin S_t | prefix].

On every conceptual all-probe path, the sum of indicators1[v_t notin S_t] is the number of binary rank increments, at most dimS*=2a*+b*<=2g. The cost bound needed for compilation follows from monotonicity: when adding one independent row, the restricted alternating-form rank rises by0or2, so dimS−rank(S)/2 rises by1or0. Since S_t⊆S*, its cost cannot exceedg.

Taking expectations, and then averaging the independent uniform terminal time, gives

  E[1-F_terminal] <= dimS*/N <= 2g/N.                     (A)

The equality relating terminal and conceptual all-probe prefix laws uses private role hiding and identical controls before each call. No distribution stationarity, mixing, spectral/excitation gap, or lower bound on rare errors is used. The algorithm need not ever discover all of S*: errors that are never excited cost no innovations or terminal fidelity. This is an expectation guarantee over the private terminal/probe record, not a recordwise high-probability confidence claim. A Markov conversion costs the usual1/delta. Ifg=0 the promise implies only identity Pauli support and the resource is exact; no discovery is necessary.

With N=ceil(2g/epsilon), (A) yields expected Bell infidelity<=epsilon. The source may continue to hold a purification of the resource. Standard teleportation with trusted Bell measurements, classical communication and Pauli corrections maps the reduced resource to a Pauli channel with identity probability F_terminal. Its reduced half-diamond error, averaged over the actual procedure, is at mostepsilon. This describes reliable transfer of a *fresh* payload using a prepared resource. It does not assert a decoupling rate linear in epsilon for the joint environment, nor an unrandomized worst-case logical channel guarantee for new source calls.

## Implementation budget and comparison
There are at mostN source calls, expected(T)=(N+1)/2. Each call uses n trusted Bell pairs, O(n²) compiled Clifford gates before source access, and either O(n²)+O(n) probe controls/readout or O(n²) terminal decoder controls. Binary span storage and emitted gate lists are polynomial n; recompilation can be cached or updated. The common error algebra may contain2^Theta(n) Pauli errors; no distribution or environment model of that size is learned. No full-reference recovery-row block encoding occurs: logical tensor-factor extraction replaces it.

Control/probe errors, calibration, connectivity/routing and storage must be included in any practical claim. An incorrect Bell label may violate S_t⊆S* permanently; naive rank updates are not robust to noisy acquisition. A conservative hybrid bound sums implementation diamond errors over actual rounds; fixed per-gate error is not silently scalable. If empirical cost ever exceedsg, the promise or acquisition model has failed; no guarantee then follows, and a physical implementation must abort or use a separately certified fallback. Source-side leakage of terminal role destroys the proof. The common Pauli basis and trusted Clifford controls remain load-bearing.

The algebraic decoder and Bell sampling are conventional. An equally informed stabilizer/noiseless-subsystem learner can use exactly the same innovation accounting and terminal protocol. The useful advance relative to the earlier Astra bridge is the **acquisition-to-actual-encoder mechanism under retained quantum memory**, with1/epsilon rather than a generic regret1/epsilon² sample dependence, under a much stronger common-algebra promise. No comparative novelty claim has been cleared. This does not supersede the generic compact-flag oracle-comparator theorem, which applies to a different source class.

## Finite evidence
`memory_algebra_discovery_v1.py` simulates n=2,k0=1, a hidden noncommuting dimension2 Pauli subspace, and a genuine retained2-dimensional quantum memory. Its joint unitary has noncommuting X⊗X and Z⊗Z interactions, a gauge Y field, and a memory Y field. The memory is updated by its actual Bell instruments. All histories are summed exactly by unnormalized memory operators grouped by learned span (valid because future controls depend only on the span in this fixture). This is not an iid resampling or a classical flag replacement.

The full R:B:M physical circuit is separately checked on prefixes through round3: probe label probabilities match the source instrument to4e-16, and terminal logical Bell fidelity matches the mixed-gauge expression to1.3e-15. At N=64 expected private-terminal loss is0.015625 (bound0.03125); at N=256 it is0.00390625 (bound0.0078125). The summed expected innovations approach2 as required. These small numerical checks support implementation consistency, not the general theorem.
