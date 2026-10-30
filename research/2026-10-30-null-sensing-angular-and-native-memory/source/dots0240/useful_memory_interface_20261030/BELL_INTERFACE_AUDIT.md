# Independent audit: encoded Bell interface through paired DATA columns
2026-10-30. Additive audit. No source manuscript changed.

## Verdict

**Scoped PASS for a controlled encoded Bell measurement and entanglement-swapping interface, under the already explicit controlled-terminal-stage and classical-reliability premises.** The initially proposed two-layer contraction can be replaced by an exact onsite-column argument. No encoded Bell-resource preparation, autonomous mode switching, arbitrary bare quantum retrieval, or continuous-coherent terminal-gate theorem is obtained.

The operational output is an encoded remote Bell pair plus a classical Pauli frame. The remote memories need not be decoded while the Bell labels are calculated. Their entire waiting time remains charged to their native memory histories; no conditional restart theorem is used.

## Sources read

- `producer-workspace/EXPLICIT_GPT_TRANSACTION_CIRCUIT.md`, terminal D0-only suffix and scope.
- `producer-workspace/INTEGER_ENERGY_D0_D1.md`.
- `producer-workspace/DESTRUCTIVE_CSS_READOUT_CANDIDATE.md`.
- `producer-workspace/DESTRUCTIVE_CSS_READOUT_REVIEW.md`.
- `producer-workspace/SPACETIME_CPTP_MEMORY.md`, one-chain argument and component-rooting requirement.

The single-block destructive measurement is already reviewed; this document does not present it as a new result.

## 1. The exact geometry repair

Let A and B be identical CSS code blocks with matched coordinate i. Regard the pair `(A_i,B_i)` as one DATA column of fixed dimension four. The column graph is the union of the two layer graphs, plus every declared projected primitive/readout support clique. Its degree remains bounded. Pairwise CNOT requires the corresponding matching interaction; physical geometric routing is not supplied by this identification.

In the X sector a Pauli label is the column vector `(x_A,x_B)`, and transversal CNOT A to B acts by

    (x_A,x_B) -> (x_A, x_A XOR x_B).

In the Z sector it acts by

    (z_A,z_B) -> (z_A XOR z_B, z_B).

Both maps are invertible on each column. Consequently a column is occupied before the gate if and only if it is occupied afterward, separately in each CSS sector. There is no support expansion, no quotient that can disconnect a witness, and no new macroscopic root made out of the supports of the nominal gates.

The product code has column distance at least the single-block distance d: a nontrivial product-code logical Pauli has a nontrivial logical component in at least one layer, whose support already contains at least d distinct columns.

Use independently minimum PHYSICAL-weight syndrome representatives in each layer. Do not replace these with an unproved minimum-column-weight decoder. If E^o denotes their union of occupied columns, then

    |E^o| <= |E_A|+|E_B| <= 2|E^o|.

Each layer restriction to a column component is stabilizer-reduced. Component sizes below the single-block correction radius therefore suffice for both layers.

## 2. Product-code D0/D1 with explicit constant bounds

Use U_sum=U_A+U_B. On a small column component C,

    h |E^o intersect C| <= U_sum(E restricted C)
       <= 4 |E^o intersect C|.

An accepted move in one layer decreases this nonnegative integer potential by at least one and touches at most w columns. A bad Pauli on q columns can touch at most 2q layer qubits, hence changes U_sum by at most 4q. Full raw-syndrome dependency cliques still provide locality and additivity. The two-layer hub count only changes fixed packing/incidence constants.

For example, with Q the column-support mass including multiplicity, the packed-candidate argument gives

    kappa_p' U_start <= C_res D_U + 2d Q + M,
    U_end <= U_start - D_U + 4Q,

where C_res=dw+1 can still be used after adjusting the packing constant. Thus D1 has the same form with a'=kappa_p'/C_res, A'=4+2d/C_res, B'=1/C_res. All coefficients remain independent of blocklength.

For unconditional D0, the number of accepted moves on any localized execution component is at most

    U_in+4Q <= 4(|E_in^o|+Q).

Its execution-column footprint is at most `(1+4w)(|E_in^o|+Q)`. Appending the two independently minimum physical-weight representatives enlarges this footprint by at most a factor three: their combined physical weight on a final component is at most the actual combined physical output weight, which is at most twice its execution-column size. A safe explicit constant is therefore

    C_seed' = 3(1+4w),
    |K| <= C_seed' [|E_in^o intersect K|+Q(K)].       (D0-col)

The same-syndrome replacement is local to an enlarged column component because every check support is a clique. Per-layer global minimum physical weight implies the required componentwise comparison. No column-weight minimality is used.

The source D1 proof then transfers literally with its numerical constants replaced: use U_sum, column supports, the inequalities above, and separately reduced layer representatives. Choose the fixed physical block length so c_R'/(2C_seed')>1. The ancestry slices are all column sets; every earlier component meets its actual target column. Thus the original connected-spacetime-animal proof remains available.

The fixed-set physical fault/service moment bounds are queried on at most 2|W| layer DATA sites for a column set W. This increases their fixed incidence/moment constants but does not require independence between layers, their baths, or their controllers.

## 3. The controlled nominal instrument must be exact

The nominal terminal instrument on A and B is

    U_pointer,(X on A,Z on B) · CNOT_transversal · (F_A^dagger F_B^dagger),

followed by ideal terminal pointer observations and disposal of A/B DATA. It must be implemented on the actual full-Hilbert controllers/workspaces. The transition into this mode, gates, and pointer preparation/write operations have a total duration bounded independently of N.

**Every incompatible native term must be suppressed or incorporated in that prescribed nominal instrument.** Merely switching off visibly DATA-affecting terms is not enough if uncontrolled controller motion changes the frame during F^dagger. No dissipative evolution is inverted by a frame convention.

Every modeled error during this stage is a declared bounded-range/bounded-incidence Poisson CPTP kick, including preparation/write noise. By unitary conjugation through the bounded-depth nominal circuit, the faults can be relocated to bounded supports adjacent to the ideal gate/measurement. Pointer Pauli flips become bounded effective measured-bit masks exactly as in the reviewed destructive-readout proof. A common retained bath is allowed; formal Pauli terms are not assigned probabilities.

## 4. One D0-only root, including CNOT

Before the terminal gate, virtual representatives E_A,E_B are separately minimum physical-weight representatives on every earlier safe history. CNOT maps their stabilizer equivalences to stabilizer equivalences of the product code, because transversal CNOT normalizes that code. Their occupied-column support is exactly preserved.

The entire noisy terminal stage plus both complete noiseless GPT computations forms ONE analysis suffix. Its D0 input column set is precisely the pre-gate occupied-column set. D0 is unconditional, so the fact that the post-CNOT error is not separately minimum-weight is harmless. It obeys (D0-col), with Q_ro the relocated effective terminal-fault mass.

If all enlarged suffix components are below the common cutoff, componentwise progress forces every terminal relevant-sector syndrome to vanish. The resulting correction implements the desired logical CNOT followed by logical X_A and Z_B observations. Otherwise a cutoff-bad root K has either dense Q_ro or a target

    S=E_pre^o intersect K,
    |S| >= |K|/(2C_seed').

This is an actual subset of the preceding native-memory reduced representatives. It attaches to the same columns of K; the gate introduces no spatial contraction. The existing backward chain proceeds through genuine preceding memory blocks only. No service guarantee or small missed-opportunity parameter is asserted during the terminal gate/measurement.

A direct Poisson terminal-tail bound and the native actual-record moment bound therefore yield, after recomputing fixed graph/counting constants,

    delta_Bell <= C N(1+t) exp(-cN)

for a sufficiently small fixed kick rate and observation at a native analysis-block boundary. A non-boundary final partial interval can instead be put in the root, but its marked/direct fault moment must be included; a pure readout Poisson formula alone is not enough.

## 5. Measurement-compatible span and the Bell instrument

Choose matched logical symplectic bases. Transversal physical CNOT is a parallel logical CNOT in those bases. Let raw outcomes be x on A in X and z on B in Z. Apply the ordinary relevant-sector classical GPT decoder to each raw string and output

    a = decoded logical-X(A) string,
    b = decoded logical-Z(B) string.

Inserting the unused ideal syndrome sector/recovery does not change either output POVM, by the same commutation argument as the reviewed CSS readout. Their joint ideal POVM before CNOT is the rank-one logical Bell measurement with vectors

    |beta_(a,b)> = (I tensor X^b Z^a)|Phi_(2^k)>.

On a common safe physical record, every compatible Pauli-expanded term giving a fine pointer result y annihilates all logical Bell vectors except the one indexed by the decoded `(a,b)`. Therefore, after encoded restriction,

    K_y Enc_AB = B_y <beta_(a,b)|.

The form survives coherent summation. The good effects are `a_(a,b) |beta_(a,b)><beta_(a,b)|`; they need not have equal coefficients. A uniform bad-record effect <=delta_Bell I and trace preservation yield the same positive-completion argument as before. Thus the complete classical Bell-output channel, including its action on any untouched reference, is within `2 delta_Bell` diamond distance of the ideal logical Bell measurement. A certified total classical failure probability p_cl contributes at most 2p_cl.

## 6. Encoded entanglement swapping and delayed classical processing

For supplied encoded links Phi_RA and Phi_BS, the ideal Bell instrument on A/B leaves R/S in an encoded Bell pair with known logical Pauli frame X^b Z^a on S (up to an irrelevant phase/convention). Store that frame classically; no physical high-weight Pauli correction is necessary. The remote recipients remain encoded.

If R/S are abstract untouched references, the preceding Bell-channel diamond bound already proves this statement exactly, including conditional remote states.

If R/S are actual noisy autonomous memories, their errors during the entire latency must also be charged. Use their original global initialization and native histories through the final requested time T, together with the A/B Bell-root history. On the intersection of the four-block safe record certificates, native R/S Pauli terms act trivially on their decoded logical factors, while A/B terms have the Bell-bra form above. This gives the intended joint logical channel term by term; the bad events are union-bounded UNCONDITIONALLY. In particular, do not restart the native theorem on a measurement-conditioned remote controller/bath state.

The resulting decoded joint statement has an error bound of the form

    2 delta_Bell(t) + 2 delta_RS(T) + 2 p_cl.

The required fixed-record moments must hold on the jointly initialized devices with their declared bounded-incidence primitive support families; this is the same uniform-positive-initial-state use as the native proof, not an independence premise. Classical processing can take polynomial time without exposing a bare remote output, but T includes that time. The protocol does not supply a free reliable classical processor.

## 7. Scope and ordinary alternatives

The encoded Bell links are resources, not a preparation theorem. No claim is made that single-shot Tanner QEC prepares them from arbitrary product-state projections; its low-reduced-weight premise would need a separate argument. Nor is the externally controlled terminal mode constructed by the autonomous memory theorem.

A conventional actively corrected CSS memory with the same encoded links and the same terminal circuit performs the same entanglement swap. The operational advantage attributable to the proposed autonomous device is specifically its certified unscheduled waiting protection, not a new teleportation primitive, a magic-state source, or superiority over the strongest scheduled FT comparator.

The bridge is useful and nontrivial as a scope result: quantum output can remain encoded and protected while classical Bell decoding occurs, avoiding the bare-output last-fault bottleneck. It does not close quantum loading or promise a complete autonomous repeater.
