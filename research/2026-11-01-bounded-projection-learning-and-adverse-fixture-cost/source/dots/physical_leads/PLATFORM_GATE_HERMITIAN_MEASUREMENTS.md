# Hermitian-measurement spin interface: source earned conditionally; consequential-task gate still open

Root-selected interface assessment, 2026-11-01. No hardware actions. Verdict: unlike Gibbs mixing or dissipative time reversal, this candidate can honestly supply the stipulated scalar experiment using explicit preparation resources. Its easiest low-rank regime is exactly trivial for an ordinary learner. A genuinely consequential measurement-control task exists in the literature, but the present single infinite-temperature Pauli-return task does not certify that task, and its low dimension is not established.

## 1. Primitive and actual adjoint

On n qubits, D=2^n, assume each primitive has a FIXED generator

ℒ_a(X)=−(1/2)Σ_j [L_aj,[L_aj,X]], L_aj=L_aj†,
Φ_a=exp(t_a ℒ_a).

Use real Hermitian operator space and <X,Y>=Tr(XY)/D. Direct integration by parts gives ℒ_a†=ℒ_a and <X,ℒ_a X>=−(1/2D)Σ_j ||[L_aj,X]||²_HS≤0. Hence Φ_a is unital CPTP, self-adjoint and a contraction. The adjoint is the SAME physical primitive; no negative dissipation or inverse pulse is requested.

Purely Hermitian-jump Markovian dynamics is a physical premise, not a deduction from fitting returns. Coherent Hamiltonian drift, relaxation, leakage, asymmetric feedback, environment memory and uncalibrated ancillary gates can violate it. A time-varying succession of noncommuting measurement generators is NOT generally a self-adjoint primitive: expose its fixed blocks as separate labels and reverse their order for its adjoint. A construction using basis-change gates around a measurement must pay those gates and prove the complete noisy block has the advertised adjoint; ideal conjugation notation is insufficient.

## 2. Paid infinite-temperature preparation and measurement backaction

A route not requiring a cold pure reset is an independently randomized FULL local Pauli twirl. For arbitrary initial joint state ρ_SE, the ideal system-only twirl satisfies

4^(−n) Σ_{P∈{I,X,Y,Z}^⊗n} (P⊗I)ρ_SE(P†⊗I)=(I/D)⊗Tr_S ρ_SE.

It therefore both prepares the maximally mixed system and removes initial system–environment correlations in the averaged episode. It costs 2n fresh random bits and O(n) ideal local Pauli choices, with all physical pulse time, energy, error and control infrastructure paid. It does NOT reset the environment marginal: history-dependent bath drift still requires stabilization/reset or a justified fixed Markov source. Averaging is over fresh within-episode choices, not a claim about each chosen pure trajectory. Physical gates that also disturb the environment need their actual errors analyzed. Random X-only gates on an arbitrary initial state are NOT a full twirl.

An alternative, stronger reset route is to prepare each qubit in |0>, apply an X independently with probability 1/2, and average over fresh within-episode random choices. This yields I/D exactly in the ideal model, without thermal equilibration or an exponential-state sampler. It requires O(n) local reset/randomization operations, control access to the whole register, reproducible reset of the environment and preparation errors small enough for the source budget. It is not a one-port hardware service. Randomization is fresh and included inside the episode expectation conditional on the history before the episode.

Choose a nonidentity Pauli string f, f²=I, Tr f=0. A Lüders initial measurement gives s=±1 and state (I+s f)/D. This initial measurement must be nondestructive on the qubits subsequently evolved; alternatively explicitly prepare the corresponding signed ensemble with local basis preparation and random eigenvalues. The latter is possible for a Pauli product but its basis rotations, records and reset are paid. No implicit nondestructive detector is needed if that preparation alternative is used.

For Φ_w=Φ_{a_l}…Φ_{a_1}, execute chronological v followed by REVERSED u, then measure f with output t=±1. Since primitive adjoints equal themselves,

E[st]=Tr[f Φ_u† Φ_v(f)]/D=<Φ_u(f),Φ_v(f)>.

Only the final measurement may be destructive. There is no intermediate conditioning or measurement-record feedback in this experiment. Endpoints can be Pauli-product measurements with paid local rotations/readouts; the instruments must yield the signed ensemble and reported observable claimed above. Fresh episodes include device and bath reset, not merely fresh classical randomness.

Charge every reset, gate, random bit, measurement-coupling dwell, discarded readout, detector/ancilla reset, calibration, control history and computation. If preparation/readout bias is β and each elementary implemented operation has channel error at most η, an L-operation word can carry O(β+Lη) systematic return bias. This must fit the theorem's α budget or be explicitly included in a revised proof. Repetition does not erase it. No hardware error/time/energy rates are established here.

## 3. Exact kill of the straightforward stabilizer/Pauli regime

Suppose L_aj=√κ_aj P_aj with every P_aj a Pauli string. For any Pauli f,

P_aj f P_aj=χ_aj f, χ_aj∈{−1,+1},
ℒ_a(f)=−2[Σ_{j:χ_aj=−1}κ_aj]f,
Φ_a(f)=q_a f, 0<q_a≤1.

Thus EVERY reachable feature is a multiple of f. The task dimension is one and

F(w)=Π_{a in w}q_a, Γ(u,v)=Π_{a in u}q_a Π_{a in v}q_a.

The conjugation superoperators commute even when the Pauli jumps anticommute. Scheduling order therefore cannot change the result. Mandatory measurement budgets do not create a nontrivial order-selection problem in this regime. An ordinary retaining learner measures each q_a and multiplies; accuracy ε/H per primitive suffices for horizon H by telescoping. It receives exactly the same scalar data and needs neither tomography nor hidden coordinates. The general acquisition theorem is unnecessary here.

Sums or continuously rotated combinations of Pauli operators can escape this algebraic collapse, because their cross commutators mix Pauli directions. That escape does not imply small joint reachable width. Simple independent-qubit or collective-spin closures can remain small, but then ordinary low-dimensional identification is a direct comparator. No theorem says all low-rank Hermitian-measurement models are trivial; the rank-one negative result is specifically for Pauli-string jump channels and a Pauli seed.

## 4. A genuinely nontrivial important task, and the missing bridge

Measurement-only holonomic logical control is a serious task: rotate measured stabilizer observables around a nontrivial closed path to implement a target logical gate, then optimize the path/discretization at finite measurement strength. The required logical action prevents the trivial do-nothing memory solution. Unknown hardware measurement imperfections could motivate many held-out schedule predictions.

Primary theoretical proposal: Lanka, Garcia-Nila and Brun, “Continuous measurement-based holonomic quantum computation,” https://arxiv.org/abs/2510.06725 (v2, 7 July 2026). Its abstract describes logical operations from successions of rotated stabilizer measurements, finite-speed jumps and code/error-space handling. This is not an empirical demonstration of the proposed learning interface.

However the current return measures one infinite-temperature Pauli autocorrelation, not code-conditioned logical fidelity or a logical channel. A stabilizer code with k independent checks occupies fraction p=2^(−k) of the register Hilbert space. Uniform mixed preparation puts only p weight in it. If two block-preserving implementations differ only on that code, their normalized global Pauli-return difference can be bounded by 2p even when their code operations differ drastically. A bounded ±1 experiment near nonsaturated mean then requires order p^(−2) repetitions to resolve order-p differences. This example shows why code quality cannot be read from a global trace at fixed absolute precision.

One can instead prepare the code, postselect a syndrome, or use code-supported seeds/readouts, but those are additional paid resources and require a new source analysis. Normalizing a code-supported observable by p^(−1/2) forfeits the bounded binary-observation normalization; postselection generally pays order 1/p unless a better actual preparation exists. A common invariant code could define its own stationary trace source, but moving-code protocols do not automatically share that reference state.

Even outside this dilution issue, a single f-return does not establish preservation of conjugate logical observables, entanglement fidelity, correct logical gate action, or leakage bounds. Multi-seed/readout access must be explicitly earned. The finite alphabet also needs to include actual implemented measurement orientations; a continuous path optimization is not supplied for free.

The fault-tolerant extension, “Steering paths mid-flight for fault-tolerance in measurement-based holonomic gates,” https://arxiv.org/abs/2603.02552, uses decoded measurement records and real-time feedback according to its abstract. The fixed-word nonselective-return model does not supply those conditional record laws or the adjoints of feedback operations. Its successful scalar predictions therefore cannot certify that feedback protocol.

## 5. Strict verdict and comparator

The source earns a conditional PASS with an unusually explicit nonthermal preparation route, including the full local Pauli twirl that needs no cold pure reset. Generic non-Pauli Hermitian local jumps remain a legitimate conditional physical family even if their joint reachable dimension is large; lack of a low-rank or advantageous application does not negate the source construction. The straightforward Pauli/stabilizer low-rank application earns a decisive NO-ADVANTAGE verdict. Measurement-only holonomic control supplies a real nontrivial task, but its code-conditioned/record-conditioned outputs and low joint task width are UNESTABLISHED under the current interface. No major-enabling-operation claim follows.

Any comparison must give ordinary scalar system-ID/kernel/realization learners the identical endpoint records, preparation, labels, and retention rights, plus the same stated structural assumptions. If future work pays for code-conditioned source access, the ordinary baseline receives that too. The present useful result is a clean separation of (a) honestly available returns, (b) a trivial low-rank regime, and (c) a consequential task requiring additional operations—not another platform claim.

Sources: the two arXiv primary abstract pages above were opened successfully. No denied or inaccessible sources were bypassed. The physical-source algebra, Pauli factorization and code-dilution argument are direct derivations in this note; the cited papers support the existence and scope of the holonomic task, not these learning claims.

## 6. Root-proposed constructive repair: code-normalized, failure-inclusive instruments

This is a DIFFERENT explicitly paid source, not a property silently inherited by the infinite-temperature experiment. It removes the code-fraction objection if actual encoded preparation is available.

Let P be a code projector of rank d_C, and F a supported logical Hermitian Pauli with F²=P and Tr F=0. Prepare s uniformly in {±1}, then

ρ_s=(P+sF)/d_C.

These are normalized positive states, and E[sρ_s]=F/d_C. For a standard known stabilizer encoder, one possible implementation resets syndrome ancillas, prepares one signed logical Pauli eigenvalue, randomizes the other logical degrees of freedom, and applies the actual encoding circuit. Every reset, encoding gate, basis rotation, and their systematic errors are paid. This is not a free postselection from the maximally mixed register. It is a familiar logical process-tomography preparation service, not an oracle giving the dynamics.

Choose a specified measurement outcome whose actual ideal Kraus operator K_a is Hermitian and ||K_a||≤1 (a projector is sufficient). Define T_a(X)=K_a X K_a. This map is self-adjoint and HS-contractive: ||K_a X K_a||_HS≤||X||_HS. The Hilbert inner product is now Tr(XY)/d_C on the ambient operator space. F has norm one in that metric.

Execute chronological v followed by reversed u with fresh actual measurements. On ANY undesired outcome, report Z=0 and terminate that episode. On success of the whole word, measure the supported logical F, with any final out-of-code outcome assigned zero, and report Z=s times that outcome. Then

E Z=Tr[F T_u† T_v(F)]/d_C=Γ(u,v).

The expectation includes ALL failure episodes. There is no conditioning on success, division by success probability, or inverse-p weighting. The final supported F readout can use a paid decoder/syndrome check/logical measurement. Weak measurement implementations qualify only if their actual selected Kraus maps have the claimed form; generic noisy apparatus does not automatically qualify. Several Kraus operators for the reported outcome need a separately demonstrated self-adjoint contraction, not merely a Hermitian POVM effect.

The preparation source also works for seed P: prepare P/d_C, use sign +1 and final code projector output 0/1. For other logical Pauli seeds repeat their own paid preparations. The current theorem applies separately to each seed; shared-dictionary/multi-readout efficiency and arbitrary cross-seed logical channel reports are NOT claimed as proved.

### A consequential constrained objective actually reachable in a limited case

For one encoded qubit, let E_s be the unnormalized code-to-code branch map of a required measurement path s, with failures/leakage counted as errors. Independently acquire the four same-seed returns for P, X_L, Y_L, Z_L. The entanglement fidelity relative to logical identity is exactly

F_e(E_s,I)=[F_P(s)+F_X(s)+F_Y(s)+F_Z(s)]/4.

For target logical X, it is [F_P+F_X−F_Y−F_Z]/4. These are exact channel-fidelity identities for this trace-nonincreasing map, not an inference from a single Pauli. Four independently budgeted instances of the current theorem could therefore assess these specific full logical objectives. General target gates need cross terms or other explicitly earned resources and a corresponding theorem; a single seed cannot certify them.

The scheduling problem must impose a genuine external operation—e.g. a specified closed code-deformation path/required measurement workload or a nonidentity logical target—so doing nothing is not admissible. This does not by itself show that such a restricted objective is a bottleneck or that measurement-only realization beats available gates. Measurement-based holonomic protocols provide a possible setting, not an established application of this learner.

### Does the preparation service already give away the answer?

NO, not logically. It is the same service an ordinary logical tomography baseline receives, and for one logical qubit tomography of each COMPLETE candidate word is cheap in dimension. It still costs repeated shots for each new word. Moreover tomography of individual primitives compressed to the INITIAL code generally cannot be multiplied to predict a moving-code word: intermediate operators leave that fixed code, and repeated projection loses the excursions. Full ambient process tomography is a different and potentially much larger service.

This leaves a genuine possible amortization question: can a low-dimensional joint forward/reverse operator space learned from these branch-inclusive returns predict many unseen constrained paths more cheaply than repeated logical tomography or a retaining controlled-realization learner? Neither low width nor that advantage is currently established. If successful paths have tiny probability, their unnormalized fidelity is also tiny; one cannot resurrect a useful conditional gate by renormalizing the report. High success probability must be achieved and validated, not assumed from the ideal Zeno limit.

Updated boundary: the encoded-instrument construction is an HONEST CONDITIONAL LEAD, not killed by the infinite-temperature code dilution argument. It removes that specific obstruction by purchasing a stronger, explicit source. The unresolved decisive requirements remain joint task width, source bias at the required precision, total acquisition/solver cost, and comparison to strong ordinary retaining learners with the identical encoded preparation and instruments. No practical or major-enabling advantage is claimed.
