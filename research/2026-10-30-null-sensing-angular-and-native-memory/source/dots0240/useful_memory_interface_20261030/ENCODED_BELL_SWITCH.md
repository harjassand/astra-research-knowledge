# An encoded Bell switch: a quantum recipient without bare decoding
2026-10-30. Independently scoped construction; see BELL_INTERFACE_AUDIT.md. It extends the already-written controlled destructive CSS readout; it does **not** claim a new autonomous readout primitive or a solution to encoded-state preparation.

## Useful result first
Two stored encoded Bell links R--A and B--S can be joined into an encoded Bell link R--S by a bounded-depth noisy terminal operation on A,B. Only a classical Pauli frame must reach R,S; the receiving memories need never be decoded to bare qubits, and they can continue protecting their states while the classical decoder runs. For a constant number of identical Tanner blocks, the same positive-record/D0 proof gives an exponentially small decoded switching error under the native Poisson-CPTP noise model, with changed fixed constants.

The resource genuinely supplied is asynchronous **waiting** for a matching quantum link followed by an encoded Clifford switch, not a universal quantum processor. Encoded incoming Bell links, one controlled terminal mode, and a classical reliability budget remain explicit interfaces. Neither Bell-resource generation nor a noise-free physical endpoint is silently imported.

## 1. Exact resource and physical endpoint
Use identical [[N,k,d]] CSS codes, k=Theta(N), d=Theta(N), with a fixed paired logical X/Z basis. The four logical blocks are initially

    |Phi_k>_{R,A} tensor |Phi_k>_{B,S}.

This fits the memory theorem's arbitrary encoded logical/reference initialization; it does not explain how the links were produced. R and S remain encoded in their own protected memories. Their noise and their total storage time, including classical-latency time, must be charged. A fixed number of blocks preserves constant rate and linear distance up to constants.

Choose a native analysis-block boundary as the switching time. (A non-boundary partial interval may instead join the root, but requires its marked/direct fault-mass moment, not just the terminal Poisson tail.) Apply to A,B exactly this nominal terminal sequence:

1. Enter the controlled terminal mode from DESTRUCTIVE_CSS_READOUT_CANDIDATE.md, suppressing or explicitly incorporating ALL incompatible native dynamics throughout the endpoint quantum stage, including controller motion that could change the frame during F^dagger. Switching off visibly DATA-affecting terms alone is not enough.
2. Apply the actual full-Hilbert inverse frames F_A^dagger and F_B^dagger on DATA and controllers/workspaces/locks. No assumption that all transactions finished is made.
3. Apply parallel physical CNOT gates A_i -> B_i, i=1,...,N.
4. Destructively measure A in physical X and B in physical Z, using the declared local pointer/dilation implementation.
5. Compute each relevant check syndrome and run the fixed deterministic GPT classical correction. Output the k logical X results x of A and k logical Z results z of B.

An identical CSS code admits transversal CNOT: X_A(v) maps to X_A(v)X_B(v), Z_B(w) maps to Z_A(w)Z_B(w), while Z_A and X_B remain unchanged. This preserves the product stabilizer group and implements paired logical CNOT. Thus measuring logical X_A and logical Z_B after this gate measures the commuting logical Bell observables X_A X_B and Z_A Z_B before it. No logical Hadamard gate or magic state is needed.

All gate durations, inverse-frame operations, pointer faults, and local switching noise are part of one bounded-depth finite-duration endpoint instrument. Perfect suppression/scheduling in its nominal specification is the *same extra endpoint assumption already present in the earlier readout*, not a consequence of time-independent memory. Arbitrary unmodeled detector failures remain excluded. Subsequent classical failures have a separately certified budget p_cl.

## 2. Column grouping removes a hidden spread problem
A tempting but incomplete argument is to invoke each memory's terminal decoder separately and then insert a CNOT: two individually harmless residual clusters can join after propagation. Instead redo the deterministic certificate on matched **columns** (A_i,B_i), each a fixed-dimensional site.

Let G_col contain the union of both memory interaction graphs after identifying A_i with B_i. Include all enlarged frame/readout/fault support cliques. It has bounded degree and O(N) columns. Each transversal CNOT is now an onsite operation, and conjugation maps a nonidentity two-qubit Pauli to a nonidentity two-qubit Pauli. Hence its column support is **exactly preserved**.

Use E_A and E_B that separately minimize physical Pauli weight modulo the relevant stabilizers. Do not silently substitute a minimum-column-weight representative. Write w_phys=|E_A|+|E_B| and w_col=|supp(E_A) union supp(E_B)|. Then

    w_col <= w_phys <= 2 w_col.

For the product energy U=U_A+U_B, U<=2 w_phys<=4 w_col. On each small column component C, both restrictions are reduced, both are below the original correction radius, and confinement gives U(C)>=h w_phys(C)>=h w_col(C). Activity counts add across layers; each physical check/hub remains local in G_col. Packed-candidate incidence constants at most change by fixed factors. The product code's nontrivial logical Pauli has column weight at least d, since one of its two factors is a nontrivial logical Pauli of its original block.

Therefore the integer-energy D0/D1 proof applies verbatim with safe changed constants, e.g. doubling weight-conversion constants where required. Adding cross-layer column adjacency merely merges components; it does not change check identities, raw-syndrome persistence, or the fact that each full read footprint lies in one component. A branch's total physical fault mass is bounded by a fixed multiple of its column fault mass.

## 3. One D0-only terminal root, not fictitious service
After the inverse frames, push endpoint local CPTP faults through the bounded-depth nominal circuit as in the existing readout construction. Their dressed supports remain bounded in G_col; retained common bath action stays in their coefficients. Expand only as a linear Pauli/matrix-coefficient expansion, never as an invented stochastic Pauli distribution.

The terminal CNOT exactly preserves column support and maps the product code to itself. The subsequent complete ideal classical GPT computations are one formal terminal suffix. The unconditional finite-work argument gives

    |K| <= C_tail [ |R_in intersect K| + Q_ro(K) ],       (1)

for every enlarged root component K, using column support and a fixed enlarged C_tail. This is proved by applying the ordinary finite-work bound to the post-CNOT representatives; the pre/post representatives have identical column support. Every component remains rooted, so no uncharged disconnected correction component appears. The input need not be a minimum-weight post-CNOT representative: D0's first finite-work estimate is unconditional, and its endpoint reduction is the same-syndrome minimization already used in the source proof.

If all such components have size below the cutoff, the no-improvement terminal condition and activity/confinement imply zero remaining relevant syndrome. The corresponding logical Bell measurement is correct. Failure therefore implies a large component in this suffix or earlier memory history.

For a large terminal component, either Q_ro is dense and a fixed-set Poisson tail pays directly, or R_in is dense and starts the usual backward chain in the genuine earlier memory blocks. The constant C_tail affects the chain's root-volume comparison but not its geometric expansion thereafter. There is NO D1/service assumption during the quantum terminal stage and NO quantum latency charged for offline A/B processing, since A,B were destroyed.

The marked-controller ancestry and fresh-service hypotheses are the original physical-record hypotheses for the two independent native controller sets, evaluated on the enlarged bounded-degree column geometry. Common retained-bath correlations are allowed. Constants may deteriorate severely. The theorem is a finite-block extension, not an arbitrary large switching-network theorem with uniform constants.

## 4. Quantum, not merely classical, correctness
For every safe physical record, every compatible Pauli coefficient history implements the same logical Bell outcome rule after the terminal classical corrections. For a fine pointer result y decoding to b=(x,z), the Kraus restriction has the form

    K_y Enc_{AB} = B_y <Bell_b|_{AB}.

This rank-one logical factor survives coherent sums. It establishes the measurement channel including an arbitrary quantum reference, not merely the distribution of classical Bell labels. The good instrument need not have an input-independent distribution of b; its effects are a_b |Bell_b><Bell_b|. As in the earlier readout proof, a uniform bad-record CP norm delta implies measurement-channel diamond error <=2 delta.

Apply the channel to the two logical Bell links. Each outcome leaves R,S in |Phi_k> up to the known logical Pauli X^z Z^x on one side (transpose/convention phases are physically irrelevant; fix the agreed logical Bell convention once). No physical Pauli pulse is necessary: retain the frame as classical metadata and modify later logical observable/Bell outcome interpretation. Logical Paulis have zero syndrome, so leaving the frame unapplied does not disable autonomous correction.

At a subsequent use time T, analyze R,S with their continued memory protection and A,B with the terminal root. Equivalently use a constant-size product-code history and the reference-complete Bell instrument. The resulting decoded encoded-link instrument differs from ideal swapping by

    error <= C N (1+T) exp(-cN) + 2 p_cl,              (2)

for sufficiently small fixed endpoint/storage kick rates and changed positive constants. Equation (2) describes **encoded output**: it is not a claim that the bare physical R,S data are trace-close to a codeword. Their residual correctable errors and their live controller frames remain present, and eventual recipients must use an allowed encoded interface.

## 5. Preparation and use ledger
What is closed:
- Quantum recipient: R,S remain protected and encoded.
- Operation: entanglement swapping / logical Bell measurement, a nontrivial Clifford primitive.
- Actual local frame: F_A^dagger F_B^dagger, including malformed controller sectors.
- Noise during endpoint: bounded-depth same-model CPTP kicks, one D0-only root.
- Classical latency: remote encoded memory continues; no bare coherent output waits.
- Quantum output correction: classical logical Pauli frame only.

What is not closed:
- Generation/loading of the encoded Bell links or arbitrary source states.
- A physical controlled-mode switch from the static memory Hamiltonian, beyond the earlier explicit endpoint assumption.
- Reliability of the classical decoder/storage; this is p_cl, not zero by fiat.
- Repeated programmable gates with a size-independent circuit threshold.
- Continuously coherent-noisy finite-duration endpoint control, or geometric routing beyond the bounded-degree graph.

Known logical |+> and |0> blocks plus the same transversal CNOT would create a Bell resource, but that merely moves the preparation burden to those encoded stabilizer states. Single-shot Tanner QEC starts near an encoded state and does not by itself certify preparation from a product state with a uniformly random syndrome.

## 6. Strong ordinary alternatives with equal access
Give an ordinary scheduled fault-tolerant CSS/qLDPC memory the same encoded Bell links, transversal matching gates, pointer measurements, reliable classical budget, and graph connectivity. It implements exactly the same switch, with the same logical circuit and Pauli-frame technique. A surface-code repeater likewise performs encoded Bell swapping with different space/routing costs. These are constructive alternatives, not weaker classical strawmen.

Thus neither teleportation nor entanglement swapping is novel. The candidate additional capability is retaining Theta(N) link qubits during exponentially long *unscheduled noisy-controller waiting* before this controlled one-shot switch. There is no demonstrated numerical threshold, rate, latency, energy, or hardware advantage over conventional repeaters.

A classical store cannot retain arbitrary logical entanglement: every measure-and-prepare replacement is entanglement breaking. That certifies the quantum nature of the workload, but not superiority over other quantum memories. See DELAYED_BASIS_GAME.md for a stronger measure-first comparator that even grants arbitrary global quantum measurement before the waiting interval and unlimited perfect classical processing afterward.
