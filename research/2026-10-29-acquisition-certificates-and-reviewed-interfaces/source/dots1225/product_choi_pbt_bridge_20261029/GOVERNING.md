# Deterministic many-use unknown-frame processing from product Choi programs

2026-10-29. Author derivation and finite dense execution; independent review requested. This is an established port-based-teleportation (PBT) comparator, not a new programmable-processor invention. It removes the exponential multiplication of identity-Bell herald probabilities, at a substantial paid program/control cost. Program acquisition remains a separate conditional interface.

## 1. Explicit deterministic product-resource processor

Let Phi=|Phi_d><Phi_d| be the normalized maximally entangled state. Supply N independent normalized Choi programs J(E)=(id⊗E)(Phi), each on A_i B_i, independently of the payload/reference. First take E=id. On input C and A_1...A_N define

P_i=Phi_(C A_i)⊗I_(other A), S=sum_i P_i,
M_i=S^(-1/2) P_i S^(-1/2)+(I−Pi_supp(S))/N.

Inverse powers mean the Moore–Penrose inverse on the support. These positive effects sum to I. Implement the known measurement {M_i}; retain B_i selected by the classical result and discard all other ports. Every result is used: there is no failure herald. This is a deterministic approximate channel T_N, not an exact gate conditioned on a1/4 event. A known Naimark isometry is W=sum_i |i>⊗sqrt(M_i); extending it to a unitary, measuring i and routing B_i explicitly specifies a finite physical operation. All measurement synthesis, ancillas, routing and protected storage are required.

The processor depends only on d,N, not E or an unknown frame. Using J(U)^tensorN instead of EPR pairs gives U∘T_N, because U acts only on B halves and commutes through Alice's measurement; tracing unused ports removes their local unitaries. There is no call to U, controlled-U, U inverse, bath inverse or classical reconstruction in the processor. The simulation's use of U to *generate test resource matrices* is evaluator-side only.

## 2. Self-contained finite bound for this product-resource protocol

Put r=d^(N−1), sigma_i=P_i/r and rho=sum_i sigma_i. Standard Bell contraction gives entanglement fidelity

F_e(T_N)=(1/d²)sum_i Tr[rho^(-1/2) sigma_i rho^(-1/2) sigma_i].

The kernel completion in M_i contributes zero to this expression. On im(P_i), Hilbert–Schmidt Cauchy–Schwarz gives

Tr[(P_i rho^(-1/2) P_i)^2]≥Tr[P_i rho^(-1/2)]²/r.

Apply scalar Jensen to the spectral distribution of rho in density P_i/r, using convex x^(−1/2):

Tr[P_i rho^(-1/2)]/r ≥ (Tr[P_i rho]/r)^(−1/2).

There is no zero-eigenvalue contribution because im(P_i)⊂supp(rho). Combining the two inequalities,

Tr[rho^(-1/2) sigma_i rho^(-1/2) sigma_i] ≥1/Tr[P_i rho].

Bell-projector overlaps are Tr(P_i²)=r and Tr(P_i P_j)=r/d² for i≠j. Hence Tr[P_i rho]=1+(N−1)/d² and

**F_e(T_N)≥N/(N+d²−1).**

The protocol is covariant under every input unitary: P_i is invariant under U_C⊗conj(U)_(all A), and EPR pairs relate conjugate A rotations to U rotations on B. The kernel completion is covariant too. Therefore T_N is depolarizing. For a depolarizing channel with entanglement fidelity F_e, its Weyl-channel decomposition has identity weight F_e and total nonidentity weight1−F_e. The triangle inequality gives half-diamond distance≤1−F_e; a maximally entangled input attains equality because the Weyl Choi states are orthogonal. Thus

**e_N := (1/2)||T_N−id||_diamond =1−F_e(T_N)≤(d²−1)/(N+d²−1).**

This is a nonsharp finite sufficient bound for the product-resource PGM, not an optimality theorem over all processors. No optimized correlated PBT resource is smuggled in.

## 3. Product Choi noise is applied once, not once per port

More generally, supply exactly J(E)^tensorN for any CPTP E. The entire resource is obtained by applying E on each B half of EPR pairs. These maps commute through the measurement on C,A. For outcome i, tracing all B_j with j≠i eliminates their trace-preserving maps. Therefore the implemented channel is **exactly E∘T_N**. If E=Lambda∘U, the port noise Lambda appears once on the retained output, despite N noisy programs. In particular

(1/2)||E∘T_N−U||_diamond ≤ e_N + (1/2)||E−U||_diamond.

For nonidentical but independent valid-Choi ports J(E_i), write {T_i} for the ideal PBT trace-nonincreasing subchannels. The actual map is sum_i E_i∘T_i. If every half-diamond(E_i,U)≤nu, then positivity and sum_i Tr(T_i(input))=1 bound the additional error by nu, not N nu. This includes input/reference entanglement.

If an IID noisy program state tau has maximally mixed A marginal, it is J(E) for a CPTP E. If its trace distance to J(U) is at most eta, the usual Choi-to-diamond inequality gives half-diamond(E,U)≤d eta: every pure input/reference state can be written (I⊗A)|Phi_d> with ||A||²≤d. Hence this directly supplies e_N+d eta, without N eta.

These conclusions do **not** follow from arbitrary noisy single-program marginals alone. Product/freshness, valid Choi normalization, and independence from the payload/reference are stated interfaces. For a general correlated bank, a separately supplied joint trace-distance bound eta_bank to the ideal product bank decoupled from external systems instead gives processor error≤e_N+eta_bank by contractivity. Treating merely close marginals as a close product bank would be invalid. Shared noise with explicit non-signalling single-port channel marginals admits a further extension, but is not required or assumed here.

## 4. Many gates without exponentially small heralded success

For M uses, allocate a fresh N-port bank to each use. Gates may act on entangled payloads and be interspersed with arbitrary common CPTP processing. The hybrid/channel-composition inequality gives total half-diamond error at most

sum_(j=1)^M [e_(N_j)+nu_j+epsilon_control,j],

plus any separately justified joint resource-bank error. With ideal exact programs and controls, equal N and qubits, this is≤3M/(N+3). Thus N≥ceil(3M/epsilon−3), with N≥1, suffices for total error epsilon, consuming MN Choi programs. There is no factor(1/4)^M. This is a sufficient construction, not a proof that MN is necessary or optimal; recycling/multiport schemes are stronger comparator directions that need their own operational bounds, especially for adaptive gates.

Examples with epsilon=0.01, ignoring control/program noise: M=1 needs N=297 ports; M=10 needs N=2997 and29970 total programs; M=100 needs N=29997 and2999700 programs. One bank needs2N program qubits before workspace for qubit ports; preparing all banks before admitting an unknown payload uses2MN program qubits. Streaming banks instead requires paid protected payload storage during later acquisition. These numbers are conservative bounds, not hardware forecasts.

Astra's accepted pure kernel-program and quaternion conversion interfaces can supply exact J(U) states without U queries; every successful pure output is decoupled, making product banks possible. Success probabilities and source-call caps must still be paid before calling the bank supplied. For arbitrary causal sources there may never be enough programs. For noisy outputs, retaining multiple outputs of one conversion does not automatically give independent ports: use a proved product/joint-state interface or separately generated independent batches. No unavailable source inverse is introduced.

Deterministic processing removes *online herald failures*, not approximation error. It also does not itself protect an unknown source-stored state or acquire the microscopic gate compatibility required by a physical DFS architecture. The target here is execution of supplied unknown-frame operations inside the trusted controller.

## 5. Known-control compilation and primary comparison

Ishizaka–Hiroshima introduced this product-resource programmable-processor use of PBT: https://arxiv.org/abs/0807.4568 . The explicit PGM above is standard. Wills–Hsieh–Strelchuk's primary qubit construction (TableI and measurement construction) gives Clifford+T gate count O-tilde(N^(3/2)) polylog(1/epsilon_synth) using O(N log N) ancillas; an alternative trades slower gates for O(log N) *ancillas*, not total port storage: https://arxiv.org/pdf/2311.12012 . These are cited circuit families, not native gates executed by this packet. Naimark synthesis error must be converted to a joint channel budget.

A fresh primary alternative, Anshu–Nguyen(22Oct2026), constructs product-EPR PBT using a support reflection and known antisymmetric encoding, commuting swap-sum eigenvalue extraction, a phase and uncomputation. For d|N it states full diamond error≤2(d²−1)/N+delta, polylog(Nd/delta) depth and polynomial width. Its proof and appendices were read: https://arxiv.org/html/2610.30761v1 . It assumes arbitrary-angle one/two-qubit gates, unrestricted connectivity and clean ancillas. The low depth uses large parallel width; it is not a small device, a source inverse, or a free unknown-unitary preparation oracle. Its *state-preparation* corollary does not acquire Astra's unknown programs. This packet's sharper finite error expression concerns the exact PGM, not that different reflection circuit; do not combine them silently.

Optimized-resource PBT's stronger asymptotic error and optimal unitary-query storage protocols generally assume resources or query access not supplied by independent Choi copies. Their applicability would require an explicit paid conversion. Likewise, no historical novelty or advantage over an equally informed conventional quantum processor is asserted: the point is precisely to adopt the strong known alternative rather than compound a weak1/4 postselection baseline.

## 6. Executed evidence and remaining obligations

`check_product_pbt.py` constructs actual PGM effects, their square roots, product resource states, all measurement branches and partial traces. It checks qubits N1–5 and qutrits N1–2. Observed unitary-resource covariance residual≤1.11e−15; a genuinely mixed amplitude-damping Choi product at N3 agrees with E∘T_N within2.01e−16. These finite floating diagnostics support the exact derivation; they are not scalable hardware implementation or interval-certified numerical fidelities. The reported half-diamond values use the proved depolarizing identity, not an unperformed generic SDP.

Remaining: independent review of this derivation and transfer; complete concrete native gate/routing/error budgets; acquired program availability; noisy-bank independence and valid-Choi structure; stronger many-use resource optimizations. Established PBT mathematics is not claimed as a new Astra discovery.
