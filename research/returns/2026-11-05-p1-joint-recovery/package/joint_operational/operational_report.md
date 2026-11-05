# Independent operational construction and exact control formulation

## Status and relation to the root diagnostic

The proposed root diagnostic (alternating SDPs for nonselective maps M⊗E→M using a backward Bell cost) does not duplicate any numerical optimization implemented here. I independently formulated an exact finite-horizon optimization that includes measurements and classical feedback; I have not implemented its optimization. A nonselective alternating SDP is a useful restricted diagnostic but does not optimize arbitrary feedback instruments, and alternating optimization is not a global certificate.

I have a complete executable, locally routed version of the accepted inverse decoder, including its resource bill. I also have an exact finite-dimensional characterization of the general feedback receiver problem, with a finite classical branching bound. Neither establishes a new weak-angle optimal memory asymptotic. The unrestricted joint asymptotic endpoint remains unresolved; the accepted fixed-angle converse must not be promoted to a weak-angle theorem.

## 1. Physical line decoder with routing included

Write c=cos θ, s=sin θ, and r=1−s⁴. Select a number K≤N of outputs to use. Store the first K output qubits in chronological order along a line, E₁,…,E_K, with a fresh maximally mixed dummy D immediately to their right. A simple faithful implementation allocates K storage sites in advance and loads each arriving qubit into its designated site. The interconnect needed for that loading must be stated separately; this construction does not claim that arbitrary addressed loading is free.

For j=K,K−1,…,1, apply the following nearest-neighbor gate to the physical sites currently holding E_j and the logical dummy:

    Wθ = SWAP Uθ† = c SWAP − i s I = −i U_(π/2−θ).

After this gate, the logical dummy occupies the left site and the spent bath carrier occupies the right site. Release or reset the right site, then continue one site to the left. Consequently the gate sequence implements exactly the accepted reverse-ordered inverse-collision decoder, while moving the dummy through the stored chain. At the end the recovered output occupies the oldest carrier's site.

This equality holds as a channel, including an arbitrary inaccessible reference. It does not require bath purification, bath preparation labels, or access to S. The only initialized dummy is independent of the source. A fair classical bit followed by preparation of |0⟩ or |1⟩ prepares it, and that bit need not be retained.

The resulting channel is depolarizing with Bloch visibility 1−r^K. Its half diamond error is exactly

    εideal(K,θ) = (3/4)r^K.

For 0<εideal<3/4, choose

    K = ceil{ log[3/(4εideal)] / [−log(1−sin⁴θ)] }.

Once the first K carriers have been collected, later source interactions cannot change their reduced state. Discarding later arrivals therefore leaves the same guarantee. This makes the achievable memory a function of the useful prefix K, not of an unnecessarily larger N.

### Validation

The independent script `verify_routed.py` explicitly evolves the reference, source, bath outputs, and mixed dummy as a density matrix, performs the physical adjacent W gates, and traces all but the reference and leftmost output. For K=1,…,4 and θ∈{0.07,0.3,0.8,1.4}, it agrees with the full predicted depolarizing Choi matrix to numerical precision (maximum entry residual below 10⁻¹²). `routed_verification.json` contains all sixteen comparisons.

### Logical resources

- K stored carriers plus one decoding dummy at peak, excluding any incoming-loading device not specified by the source interface.
- K local two-qubit inverse-and-move gates, in a necessarily ordered sweep.
- One independent mixed-qubit preparation.
- K carrier-release operations, if physically necessary rather than simply leaving spent sites unused.
- Output appears at the oldest end. If the required output port is the newest end, a return path or K additional local swaps must be charged.

The combined gate is close to a full SWAP when θ is small. Its physical duration cannot be declared O(θ) merely because the source's collision is weak. With an exchange interaction of bounded strength J_R implementing Uφ in time |φ|/J_R, the sweep duration is K(π/2−θ)/J_R, before any final routing.

### A completely local fixed-port loader

If all arrivals enter one fixed port, the line construction alone has not paid for distributing them. One explicit nearest-neighbor implementation uses two rows A₁,…,A_K and B₁,…,B_K, plus the decoding dummy. B is reset and serves as an expressly counted routing buffer. At arrival k, the old k−1 carriers occupy A_(K−k+2),…,A_K. Before loading the new carrier into A_K, perform two parallel layers:

1. SWAP each occupied A_i with its empty B_(i−1).
2. SWAP those B_(i−1) with the now-empty A_(i−1).

The chronological data shift one site left, all used B sites return to the fixed reset state, and A_K is free for the new carrier. The links A_i—B_(i−1), B_i—A_i, and A_i—A_(i+1) form a local ladder/triangular array. The source only supplies the arriving carrier; no return is used.

This loader uses K(K−1) local routing SWAPs in total, plus K loading operations, but only two routing layers per arrival. Its physical footprint is 2K+1 resident qubits, plus the transient incoming carrier if the interface uses a separate loading qubit. It requires an arrival interval accommodating the two layers and loading, or else a further queue whose size must be counted. The reverse sweep is then carried out on row A by the W gates already specified. This is an explicit attainable fixed-port construction, not a claim that the quadratic routing gate count is optimal. With one row and one moving vacancy the same shift takes k−1 sequential SWAPs at arrival k, saving the extra row but worsening throughput.

A different routing architecture, e.g. an addressed tree, can change these costs. This is why an addressed-gate count and a fully local fixed-port gate count are distinct resource statements. In the ladder construction the sufficient per-gate implementation-error allocation becomes O(ε/K²) rather than O(ε/K), because loading and routing contribute O(K²) gates.

### Storage-time and error budget

Let arrivals be separated by Δ, local sweep gates take τ_g, and assume loading is feasible at that rate without an extra queue. Between arrivals, the number of stored received qubits grows from zero to K. If spent carriers are released during the sweep, the total vulnerable logical-qubit time is approximately

    Vtime = Δ K(K−1)/2 + τ_g K(K+3)/2,

when the dummy is prepared at the start of the sweep, not counting initialization, loading, endpoint conventions, and output delivery. Each sweep gate has the remaining carriers plus the dummy live, so the sweep occupancy is K+1,K,…,2. This is the time over which unknown quantum information must be protected; a preallocated physical array also has its fixed hardware footprint even while some sites are empty. Allocate error as

    εideal + εloading + εgates + εstorage + εpreparation + εdelivery ≤ ε.

The channel trace/diamond norm telescoping bound gives εgates≤Kδ for a bound δ on each gate's half diamond implementation error, with analogous additions for loading and delivery. A safe choice is δ=O(ε/K). If an angle is directly controlled to absolute error O(δ), this requires O(log(K/ε)) control bits. This is a sufficient worst-case precision budget, not a lower bound.

The decoder's use of θ and its chosen K also depends continuously on the calibrated source angle. A uniform worst-case bound for a source/decoder sequence with angle error η is O(K|η|), so η=O(ε/K) is sufficient without relying on cancellation. A more favorable calibration law would need an explicit perturbation analysis or stochastic calibration model.

For small θ, K=Θ(θ⁻⁴ log(1/εideal)). At fixed Δ and τ_g, Vtime=Θ(θ⁻⁸ log²(1/εideal)). If the source step duration is explicitly Δ=θ/J_S, the filling contribution is Θ(θ⁻⁷ log²(1/εideal)/J_S); the receiver's near-SWAP sweep contribution can still scale as θ⁻⁸. These alternatives show why a collision-count theorem is not automatically a physical-time theorem.

Protection has no universal bill in the stated ideal CPTP model. Under a separately stipulated below-threshold local noise model and a particular error-correcting architecture, the above gate count, depth, and storage-time volume can be converted into physical qubits, cycles, preparation overhead, and code distance. For example, a model with logical error per relevant location bounded by A exp(−αd) permits d≥α⁻¹log(AV/εstorage). A surface-code-like architecture then uses O(Kd²) physical memory sites. These are conditional engineering estimates, not consequences of the partial-SWAP specification.

## 2. Exact finite-horizon optimization including arbitrary feedback

Here memory dimension m denotes the coherent system carried between arrivals. A physical implementation may require the current carrier and a measured ancillary qubit in addition to that memory; these are explicitly charged below. If a different peak-memory convention is used, shift the allowed dimension accordingly.

Let ω be an unnormalized positive operator on R⊗S⊗M, with dim R=dim S=2 and dim M=m. It is a planning state; the receiver does not gain physical access to R or S. One source step is the fixed map

    Ξθ(ω) = U_SE (ω⊗I_E/2) U_SE†.

Every receiver instrument can be refined to have one Kraus operator K_y per classical outcome. Retaining the refined outcome is allowed and never decreases achievable performance. Each K_y maps M⊗E to M and satisfies

    Σ_y K_y†K_y = I_(2m).

Its branch state is

    ω_y = (I_RS⊗K_y) Ξθ(ω) (I_RS⊗K_y†).

Define the terminal reward

    V₀(ω) = max_(D:M→Q CPTP) ⟨Φ_RQ| (id_R⊗D)(Tr_S ω) |Φ_RQ⟩.

This is a semidefinite program in the final decoder's Choi operator. Then the exact Bell-fidelity recursion is

    V_n(ω) = sup_{instruments {K_y}} Σ_y V_(n−1)(ω_y).

The initial state is Φ_RS⊗|0⟩⟨0|_M. An initially mixed memory does not improve the optimum: it is a mixture of pure preparations, whose classical preparation label could also be retained, and the objective is linear before optimizing. Padding smaller memories embeds every admissible strategy into dimension m.

This recursion describes all causal instruments, not only nonselective CPTP maps. Its dependence on a conditional ω corresponds to a policy depending on the observed classical history, with those planning states calculated offline. No forbidden state measurement on S or R is performed.

### Exact reduction from diamond error to Bell fidelity

The emission channel is SU(2)-covariant because the bath is tracial and partial SWAP commutes with a common rotation on both qubits. For any causal receiver, pick one random single-qubit Clifford g at initialization, apply the same g to each incoming carrier before the receiver, and apply g† to its output. Retain g only as a classical label.

Averaging over the finite Clifford group twirls the resulting qubit channel to a depolarizing channel and preserves its entanglement fidelity. Its half diamond distance from identity is exactly 1−F_e. For an arbitrary untwirled qubit channel, the Bell-input test gives half diamond error at least 1−F_e. Therefore the minimum half diamond error over allowed dimension-m receivers is exactly

    e_N(m,θ) = 1 − V_N(Φ_RS⊗|0⟩⟨0|_M).

The random twirl does not increase between-arrival quantum memory. Its gates, classical label, calibration, and service duration still count in a physical implementation.

### Finite outcome bound despite unlimited classical records

Put d=2m. At any node, choose a nonzero one-Kraus outcome K and its full continuation strategy π. Write K=√t L with t=Tr(K†K), Tr(L†L)=1. Associate the real vector

    x(L,π) = (L†L, reward after L followed by π).

It lies in Hermitian(d)⊕R, a real vector space of dimension d²+1. The instrument completeness equation and its total attained reward are together

    Σ_y t_y x(L_y,π_y) = (I_d, total reward).

Conic Carathéodory therefore replaces this sum or integral by at most d²+1 terms while preserving both completeness and the exact reward. The replacement may select a different continuation for each retained outcome; that is precisely the allowed feedback model.

Induct on the remaining horizon. The terminal CPTP set is compact. Given compact finite-branch continuation strategy sets, the normalized-L/continuation vector set is compact, its convex hull is compact, and Σt_y=d bounds all weights. Thus the optimum is attained within a tree with at most

    L_m = 4m²+1

outcomes per arrival node. No infinite classical outcome alphabet is necessary. The full tree still has up to L_m^N leaves and is generally enormous.

This establishes an exact finite-dimensional polynomial optimization for each fixed N and m. Using real and imaginary parts of the Kraus matrices, completeness is polynomial and the Bell reward is polynomial. Terminal channels may be parameterized by at most 2m Kraus matrices of size 2×m. For algebraic c and s, real-algebraic quantifier elimination can in principle decide the threshold e_N(m,θ)≤ε and produce a policy. For general known real θ, finite-precision numerical synthesis requires a strict accuracy margin and does not certify a decision exactly on a threshold.

Enumerating m up to the accepted passive-buffer bound characterizes the exact optimal finite-horizon memory. This is an algorithmic characterization, not a closed joint asymptotic law and not an efficient decoder. It must not be advertised as resolving the requested weak-angle scaling.

### Physical implementation of the finite instruments

A finite one-Kraus instrument on a d-dimensional input can be implemented as a binary measurement tree without keeping its whole outcome alphabet coherent. For a group A of outcomes, let P_A=Σ_(y∈A)K_y†K_y. After a group J has been reached with cumulative operator √P_J, the two child operations can be chosen as √P_A P_J^(−1/2) and √P_B P_J^(−1/2) on the support of P_J, with arbitrary trace-preserving extension on its unreachable null space. Their products with √P_J are √P_A and √P_B. At a leaf, apply the polar isometry taking √(K_y†K_y) to K_y.

A single measured ancillary qubit realizes each binary split. The d=2m-dimensional current memory-plus-carrier register remains present until the selected branch has been compressed back to m dimensions. Consequently, for m=2^q, the operation can use q+2 live qubits at peak: q retained-memory qubits, the current carrier, and one ancilla, with classical branch bits external. The final rank-at-most-m branch is mapped to M plus a fixed carrier state and the carrier can then be released. This is an actual physical erasure/compression step justified by the branch rank, rather than a formal tensor truncation.

Balanced branching takes O(log L_m)=O(log m) measured splits on the realized path. Generic dense unitary synthesis on O(log m) qubits has O(m² polylog m) elementary-gate cost per split, before gate-set precision overhead; classical storage for the full policy can be exponential in N. Approximate instruments must be approximated as complete quantum-classical channels. If each realized stage has half diamond error ≤δ, adaptivity still permits the telescoping bound Nδ; δ=O(ε/N) suffices when the ideal synthesis leaves a margin.

Crucially, this implementation is not automatically fast enough to service a fixed-rate stream. If its per-arrival service time exceeds Δ, the resulting queue is quantum memory and must be added. Nothing in the finite-dimensional optimization licenses an arbitrarily fast dense unitary or an uncounted queue.

## 3. What is and is not established

The routed passive decoder gives a valid joint upper bound using the useful prefix K. The accepted global-decoder obstruction gives the necessary carrier count

    (3/4)[1−sqrt(1−r^N)] ≤ ε.

For 0<ε<3/4 this implies r^N≤(8ε/3−16ε²/9). Together with the passive upper bound it fixes carrier-count scaling Θ(θ⁻⁴ log(1/ε)) in the usual small-error, weak-angle regime.

It does not fix receiver-memory scaling. The older general prefix converse, and its fixed-angle Ω(N/log N) consequence, leave a weak-angle fixed-error gap. The exact finite-memory control recursion above neither closes that gap nor bypasses it. The large finite policy synthesis gives an operational definition of the optimum that includes arbitrary measurements; it is not evidence of a small memory optimum.

An optimal law including physical protection, routing, preparation time, and control cost also cannot be unique without specifying architecture, gate set, arrival timing, noise, and output-port requirements. The same ideal CPTP map can be given different physical costs under different valid implementations. The honest endpoint is therefore: a completely costed attainable benchmark and an exact general optimization formulation, with the joint memory asymptotic still open.

## Primary background reference

A. Bisio, G. M. D'Ariano, P. Perinotti, and M. Sedlák, “Memory cost of quantum protocols,” Physical Review A 85, 032333 (2012), https://arxiv.org/abs/1112.3853 and https://doi.org/10.1103/PhysRevA.85.032333. This work treats quantum-memory minimization with classical memory and emphasizes the global nature of the problem. It is relevant methodological background, not a proof of any partial-SWAP-specific scaling claimed here.
