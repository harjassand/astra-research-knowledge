# Strong conventional comparator and priority audit
2026-10-29. Independent challenge of the actual guarded clock, two-site lease, and 480-level recovery hub. This is an explicit mathematical comparator, not a claim that every combined formula already appeared in print.

## Verdict

The strongest comparator is **Stinespring dilation + Feynman history propagation + a terminal reset**, with local finite-state mutual exclusion for overlapping transactions. It matches exact finite-rate completed-channel semantics without adiabatic elimination. The full recovery hub supplied here is itself precisely this comparator, rather than evidence against it.

The constructive contribution can still be useful: explicit compatible local controller alphabets, a clean exact intertwiner, and controller-specific defect/progress estimates. But the materials do not yet establish a decisive interface unavailable to equally informed conventional synthesis, nor a single two-site-qudit noisy compiler satisfying the entire advertised bundle. The guarded model has the proved commuting defect sparsity estimate but many-body guards; the two-site lease has the two-site clean compiler but unproved noisy repair; the full recovery hub has full-space regeneration but no overlapping-cell scheduling or fault-tolerant data architecture. Keep those quantifiers separate.

## Explicit ordinary construction matching the hub

Let Phi be any fixed finite-support CPTP update. Choose a finite environment E, initial |0>_E, and a Stinespring unitary U with K_s=<s|U|0>. Compile U into a finite circuit U_(L-1)...U_0. Store E and a clock 0,...,L in a finite-dimensional hub, and compile each U_t into hub-only or hub–one-leaf operations (a hub can act as a bus). For a bounded support and fixed update family all dimensions, path lengths, and geometric ranges are fixed constants. Define

H = g sum_(t=0)^(L-1) [U_t ⊗ |t+1><t| + h.c.],
J_s = sqrt(kappa) I_D ⊗ |0_E,0_clock><s_E,L_clock|.

Every H term is at most two physical-qudit sites; every J_s is one hub-site. This uses the same physical-site convention as the proposed 480-dimensional hub, not elementary two-qubit locality.

Put G_t=U_(t-1)...U_0 and Q=sum_t G_t⊗|t><t|. Then Q†HQ=I_DE⊗g A_path and Q†(sum_s J_s†J_s)Q=kappa I_DE⊗|L><L|. Thus no-jump propagation from the ready hub has scalar clock amplitudes f_t(t). A first terminal jump with label s produces exactly sqrt(kappa) f_L(t) K_s on data and resets the hub. Summing s gives Phi, independent of the random completion time and valid with an external reference. The endpoint-damped finite path has no undamped eigenvector: zero terminal amplitude recursively forces all amplitudes zero. Hence every dirty hub state regenerates with an exponential tail. A Lyapunov certificate and local Duhamel robustness estimate give exactly the type of fixed-module noisy-reset bound in EXPLICIT_QUANTUM_RECOVERY_CELL.md.

This derivation is independent of any adiabatic limit. It is an ordinary circuit-to-Hamiltonian gauge calculation, and it reproduces the proposed 29-gate hub verbatim in structure. It does not solve overlapping-module arbitration; neither does that hub.

## Matching the lease without claiming a historical first

For a two-site Phi, the shortest history edge is its isometry V=sum_s K_s⊗|s>. A reversible local transaction reserves both endpoint clock alphabets, applies V during RR↔C_sP, commits by the owner's one-site C_s→D emission, releases the partner via DP↔TR, and releases the owner via T→R. This is precisely the supplied lease. An equally informed conventional designer permitted arbitrary fixed two-qudit matrix elements can implement those finite-state transitions directly; no stronger primitive than the proposed construction is needed.

The nontrivial correctness condition is that all pending transactions form a matching. It yields the same direct-sum history isometry and ensures reverse coherent propagation undoes only uncommitted work. The release phase prevents a completed channel from being undone. This is a concrete asynchronous controller construction, not a generic appeal to universality. It demonstrates equivalence of synthesis resources, not bibliographic priority of the exact alphabet. The defect-repair terms require a further proof for an operational noisy advantage.

## The interface actually removed, and the interface substituted

Relative to an adiabatically eliminated damped-ancilla simulator, the construction removes **finite-rate error in the map conditional on a completed event**. That is a real mathematical benefit. It does not remove finite-rate error in simulation of a specified Lindblad semigroup on physical data at every time.

For an isolated ready clock H=g(V+V†), short-time excited probability is g²t²+O(t³), so first-emission probability is kappa g²t³/3+O(t⁴). A desired Poisson update process at positive rate lambda has event probability lambda t+O(t²). These cannot agree. Interacting exclusions further correlate clocks. Physical reduced data also contain pending Stinespring work between events. The contract is therefore event-semantic, with correlated random durations and a pending-update frame; it is not exact implementation of sum_x lambda_x(Phi_x-I).

This matters for 2601.20818: its direct CPTP-jump realization has independent Poisson attempts. A new delay/fault composition theorem is required to replace that realization by these clocks. Equal-time sparse bad boxes do not establish sparse space-time faults. Their healing also does not reverse data damage. The current results carefully acknowledge this, and the comparison should not erase the acknowledgment.

## Primary-source comparison (checked 2026-10-29)

* [Nagaj–Wocjan, Hamiltonian Quantum Cellular Automata in 1D](https://arxiv.org/abs/0802.0886): autonomous universal dynamics with nearest-neighbor 10-dimensional qudits and prepared program/input. Establishes strong two-qudit Hamiltonian prior art, not noisy reset-mediated correction.
* [Breuckmann–Terhal, Space-Time Circuit-to-Hamiltonian Construction](https://arxiv.org/abs/1311.6101): separate clocks for interacting qubits encode causal circuit structure. Local clocks and legal-history sectors are established; the present reusable reset/lease semantics are a narrower comparison.
* [Verstraete–Wolf–Cirac, dissipative computation](https://arxiv.org/abs/0803.1447): time-independent local dissipation supports universal computation. It is not enough to identify autonomous computation plus dissipation as the new ingredient.
* [Paz–Zurek, Continuous Error Correction](https://arxiv.org/abs/quant-ph/9707049): stabilizer recovery operations already enter continuous-time master equations. This does not itself supply the specified one-site-reset/two-site-Hamiltonian compiler.
* [Kastoryano–Wolf–Eisert, Precisely timing dissipative quantum information processing](https://arxiv.org/pdf/1205.0985): autonomous triggering and sequencing are explicit prior art. The supplementary discussion also identifies noisy gadgets and interfacing protected classical control with qubits as obstacles; the present controller claims should be compared to that concrete interface, not only to the paper's abstract.
* [Kashyap et al., 2404.11081v2 / PRX 15, 021017](https://arxiv.org/html/2404.11081v2): Eq. (2) couples target jump operators to damped auxiliary qubits; finite coupling gives approximate reduced-state simulation, with local-observable guarantees uniform in volume. The proposed exact event semantics changes the target contract rather than improving every-time simulation accuracy at the same contract. Its supplied Kraus channels can package complete updates instead of isolated target jump operators.
* [Dünnweber–Styliaris–Trivedi, 2601.20818v3](https://arxiv.org/html/2601.20818v3): discrete-time threshold and hierarchical noisy controller architecture are much stronger data-protection results than a finite recovery cell. Section VII explicitly presents continuous time as an outline, not a fully formal proof; its direct local CPTP jumps give independent Poisson attempts. It excludes nonunitary imperfections of engineered update jumps. The proposed compiler targets a useful hardware interface, but cannot import the threshold without controlling its changed timing and controller failures.
* [Harley et al., Going beyond gadgets](https://arxiv.org/html/2306.13739), [journal DOI](https://doi.org/10.1038/s41467-024-50744-9): the resource comparison concerns composable Hamiltonian locality reduction/encodings and energy scaling. Its own dissipative Zeno construction already uses nonunitarity, so merely saying “channels evade the no-go” is not a distinction. The present construction uses large fixed local qudits, a nontrivial history encoding, engineered reset, and event-semantic rather than arbitrary-time Hamiltonian simulation. Those changed assumptions prevent a direct application of the no-go; they do not prove a stronger simulator satisfying its original specification. Binary compilation of a 480-level hub is particularly not supplied.

## Defensible priority language and next falsifiable test

Defensible: “We give explicit finite-resource reset-mediated channel clocks, prove exact completed-update semantics, and derive controller-specific bounds under stated locality/noise assumptions.” Not defensible yet: “first autonomous quantum computer,” “solves the hardware bridge to the 2026 threshold,” “evades Hamiltonian simulation no-go at unchanged resources,” or “a fully robust two-body compiler.” No absence of search hits proves priority.

The strongest next comparison is a single specification table for BOTH the proposed mechanism and the conventional hub/lease compiler: local dimension; primitive matrix-element control; reset entropy source; supported overlapping updates; event versus laboratory-time output contract; dirty-controller regeneration; joint space-time fault strength; readout. A genuine separation would require a proved improvement in one of those interfaces at matched others. At present, controller product-defect sparsity and explicit volume-uniform progress are the most plausible new technical lemmas, but they do not yet coexist with all the two-site claims in one proved architecture.
