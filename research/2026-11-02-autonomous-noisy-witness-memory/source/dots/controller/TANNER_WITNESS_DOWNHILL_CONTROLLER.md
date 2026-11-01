# Finite witness-register downhill controller: construction and proof gate

## Result first

There is a concrete way to turn the Tanner mismatch decoder into a fixed local syndrome-conditioned controller WITHOUT a clock, stored syndrome history, clean classical processor, or trusted input encoder. Add constant-size noisy witness registers to each check view and make their inconsistency an energetic penalty. The elementary construction below supplies an extensive downhill-move bound, conditional only on the explicit small-decomposition theorem of the chosen Tanner family. This is a new derived construction here, not a claim that its full quantum-memory theorem or implementation has been established.

## Primary receipt / exact imported facts

Leverrier–Zémor, https://arxiv.org/pdf/2208.05537, v3: local dual-tensor codewords split into row/column codewords transferable across adjacent views (§4); Theorem12 guarantees fast mismatch reduction for sufficiently small decomposition norm; Lemma18's proof partitions the original mismatch into removed subsets, with at least half covered by high-overlap increments. Gu–Pattison–Tang, https://arxiv.org/pdf/2206.06557, supplies a different physical-syndrome potential and linear-radius sequential decoder, but not the extensive-move statement imported here. The construction below uses LZ witnesses, not an unjustified identification of their mismatch with GPT's potential.

## 1. One CSS sector: explicit registers and potential

Use the appropriate pair of check-view classes for this error sector, denoted C_0,C_1. Their local views each partition the physical qubits; every qubit belongs to exactly one view in each class. Let d0=Delta^2 be a view size. At each check-view vertex v store a binary vector a_v of length d0. All these bits are PHYSICAL noisy registers, not reliable classical oracles.

Let s_v be the actual commuting stabilizer syndrome in that local view, and H_v its local parity-check map. Set

j = #{v: H_v a_v != s_v},
Z = XOR_v a_v (embedded on physical-qubit positions), z=|Z|,
W = M j + z, with M=d0+1.

Thus Z is exactly disagreement between the two stored copies associated with each qubit. j counts violated local compatibility blocks, not individual syndrome bits. Each term is a bounded-support function of commuting physical stabilizers and register Z operators. W is an actual diagonal observable on the enlarged system.

## 2. Local moves

(A) Compatibility repair at v: when H_v a_v != s_v, choose a fixed deterministic minimum-weight b_v solving H_v b_v=s_v+H_v a_v; update a_v <- a_v+b_v. Only that compatibility block changes, and |Delta Z|<=d0. Therefore Delta W <= -M+d0=-1. There is one such available move per violated block. Deciding and implementing it requires only this constant-sized local syndrome and witness vector.

(B) Mismatch reduction at any square-complex vertex u: choose a local dual-tensor codeword x=c+r supported in Q(u) with |Z+x|<|Z| (one can use the stronger >|x|/2 reduction rule).
- If u is a check-view vertex, add x directly to a_u.
- If u is in the other vertex pair, distribute the column words of c and row words of r to their adjacent check views sharing those strips. Each strip belongs to that view's local dual-tensor code, so all H_v a_v remain unchanged. Their total XOR contribution is x.
This move changes z exactly as prescribed and leaves EVERY compatibility indicator invariant, even if the input is already incompatible.

Every update is bounded support and bounded incidence for fixed Delta. The distributed version touches at most 2d0 witness bits before cancellations, and a constant number of neighboring views. Store a fixed local truth table choosing one improving move; no maintained decomposition, global minimum search, or sequential program is needed. Exponential dependence of that table on Delta is a large FIXED hardware constant, not free computation.

For each selected local pattern, use the ideal jump J=sqrt(kappa) T Pi, where Pi projects onto its local commuting syndrome/register condition and T applies the specified register flips. This defines a finite fixed local Lindbladian on the Tanner interaction graph. A physical implementation of these jumps remains a separate engineering/control-cost problem.

## 3. Static extensive mismatch moves (derived from the primary proof)

Assume Z admits a terminating sequence x_1,...,x_m of local increments satisfying
|Z_{i-1}|-|Z_i| >= (1-epsilon)|x_i|, epsilon<1/6.

Partition the ORIGINAL support of Z into the disjoint sets x'_i first removed by increment i. The accounting of added coordinates gives a subset G such that the union of x'_i for i in G covers at least |Z|/2 and |x'_i|>(1-3epsilon/2)|x_i|. Hence every such x_i is already improving at the INITIAL Z:

|Z|-|Z+x_i| >= 2|x'_i|-|x_i| > (1-3epsilon)|x_i| > |x_i|/2.

For a fixed vertex u, all disjoint x'_i belonging to increments supported at u lie in its d0-coordinate view. They can cover at most d0 original coordinates. Therefore at least |Z|/(2d0) DISTINCT vertices have an initially improving move. This is a static rate bound; no parallel round or clock is used.

Why the fast sequence exists in a basin: Theorem12 supplies an increment whenever the minimum decomposition has sufficiently few active vertices. Starting with decomposition norm r_Z, the whole fast sequence changes that norm by at most a constant times |Z|, because each step's codeword norm is bounded by its weight divided by a fixed robustness constant. Also |Z| is bounded by a fixed constant times r_Z. Thus taking r_Z below a suitably reduced linear threshold preserves the theorem's hypothesis to termination. This is the same norm-budget argument used in the source, with its constants retained as fixed family constants.

## 4. Basin admission from physical plus witness errors

Fix a zero-energy gauge frame A0: its two witness copies agree and its physical syndrome equals syndrome(A0). Relative to it, let physical Pauli error be e in the sector and witness bit errors be b_v. When compatible,

c_v=b_v+e|Q(v) is a local dual-tensor codeword,
Z= XOR_v c_v,

since each physical error coordinate occurs in exactly two views and cancels in the XOR. Only views touched by e or b can have nonzero c_v. Each such local word has a bounded row/column decomposition norm. Consequently minimum decomposition norm of Z is at most C times the total number of physical/witness error locations, for a fixed C. This supplies the small-decomposition hypothesis inside a linear-radius joint error basin. One may choose a minimum representative modulo the enlarged stabilizer/gauge operators; existence of that representative is an analysis device, not a controller computation.

## 5. Incompatibilities do not destroy extensive drift

For an arbitrary state in a sufficiently smaller joint basin, virtually perform all j compatibility repairs, obtaining witnesses a' and mismatch Z'. These virtual repairs change at most d0*j mismatch coordinates and enlarge joint error weight by at most d0*j, so the compatible-state theorem still applies after reducing the basin constant.

Let z'=|Z'|. Then z'>=z-d0*j. There are at least z'/(2d0) improving vertices for Z'. Each changed coordinate belongs to four square-complex vertex views, so at most 4d0*j candidate vertices can distinguish Z from Z'. All remaining improving moves are also available in the original state. Thus

N_mismatch >= max(0, z/(2d0) - C0*j), C0=1/2+4d0.

Together with N_repair=j,

W=M*j+z <= K*(N_repair+N_mismatch),
K=max(M+2d0*C0,2d0)=8d0^2+2d0+1.

Every counted move lowers W by at least 1. With each local move type offered at rate kappa, for F=exp(aW),

L_cool^*(F) <= -kappa*(1-exp(-a))*W*F/K

throughout that joint basin, as an operator inequality on its diagonal syndrome/register sectors. No Gibbs state, stationarity, Zeno limit, or stochastic replacement of coherent noise is used for this identity. Counts are distinct vertex/type locations, not exponentially many enabled choices each secretly assigned a full hardware rate.

## 6. Ground space and logical frame: what is and is not established

At W=0, witness copies agree on a global A and compatibility gives syndrome(A)=physical syndrome. A controlled Pauli frame removal maps this ground sector to the original codespace. For both CSS sectors, use separate witness registers and a fixed ordering of controlled X and Z frame removals. These are bounded-degree local controlled gates on the Tanner graph; phase conventions must be fixed consistently. Witness phase errors are gauge degrees of freedom rather than classical bit flips in W, but general coherent errors are not dismissed: the parent's operator drift argument must cover them.

A complete enlarged-system logical subsystem and minimum-distance statement should be written using that controlled-frame unitary, rather than treating W=0 as the physical codespace with no auxiliary information. The controller changes witnesses, not necessarily the physical data: the stored Pauli frame is part of the actual memory. Final readout/correction must access it through those local controlled operations.

There is a standard conditional barrier deduction worth making explicit. If every nonzero W state within reduced radius R has a <=b-support downhill move, then a descent from reduced weight r<=R/2 and W<r/b would use fewer than r/b steps and stay below R. It would reach a ground state with a correction of weight <r. If total path plus initial error is below the enlarged logical distance, that contradicts minimality of r modulo gauge/stabilizers. Thus W>=r/b in this smaller basin. This deduction requires the precise enlarged logical distance and gauge definition; it is not a substitute for them. It also does not give the parent's censored-dynamics/boundary leakage theorem by itself.

## 7. Costs, comparator, status

Per CSS sector there are two witness bits per data qubit; both sectors add four physical witness qubits/bits per original qubit, plus local controller ancillas and resets. All are noisy and must be included in V or other physical fault generators. Delta may be very large. Local truth tables, jump support, check extraction/coupling time, and per-site total rate have Delta-dependent constants. The graph has bounded degree but is an expander: Euclidean constant-range locality is NOT obtained. Long-range links, routing, propagation delays, and their noise must be charged or the statement remains graph-local.

The strongest ordinary competitor is active Tanner/LDPC memory using the identical checks, witnesses, long-range interactions, noisy ancillas, and rates; the underlying decoder and code are prior machinery. The potential new capability is a fixed time-independent controller whose joint quantum/classical dynamics admits robust quantum drift at fixed local noise/control ratio. No hardware-level or lifetime advantage is yet established.

Status: explicit finite witness controller and extensive local drift derivation above; outstanding independent audit of the enlarged quantum logical subsystem/distance, all source constants and orientation conventions, actual noisy jump realization, and the parent’s coherent-noise/censored-boundary consumer. This is substantially more than a decoder-oracle assumption, but not a finished scalable autonomous memory theorem.

## 8. Enlarged logical subsystem and distance: explicit completion

For each original data qubit q, there are two X-sector witness bits and two Z-sector witness bits. Choose the copy from one fixed check partition in each sector, denoted a_X(q),a_Z(q). Let U be the product, over q, of a controlled-X from a_X(q) to data q and a controlled-Z from a_Z(q) to data q, in a fixed order. This is a Clifford unitary consisting of disjoint five-qubit blocks and two gate layers. It uses only the incident witness/data connections.

Let K_aux be the simultaneous +1 space of the two copy-agreement operators per data qubit, Z_X,0 Z_X,1 and Z_Z,0 Z_Z,1. Each pair has one free gauge qubit. The exact W=0 space is

U(C_original tensor K_aux).

Proof: agreement fixes two equal copies in each sector. Conjugating a physical stabilizer by U attaches exactly the chosen witness-parity factor for the corresponding error sector. On the agreement subspace this chosen-copy parity equals the parity of a_v in every relevant local view. Therefore compatibility is precisely the original stabilizer constraint after conjugation. This holds as a subspace identity, including coherent superpositions of witness values, not merely for classical mixtures.

Define logical observables by U(L_original tensor I_aux)U†; the auxiliary pair logicals are gauge, not protected information. Any Pauli on w enlarged physical qubits conjugates under U to a Pauli supported on at most 5w qubits (the conservative block-size bound suffices). If it is a dressed nontrivial logical of the enlarged subsystem, its original-data component is a nontrivial logical of the original code, hence 5w>=d_original. Thus

d_enlarged >= d_original/5.

This closes the linear-distance point at the abstract local-channel level. In particular, witness phase faults are genuine gauge operators after decoding; they are not silently treated as absent. General Hamiltonian combinations involving witness flips remain physical noise and must be included in the operator relative-form bound.

Combining this distance with section 6's descent argument gives a linear barrier in a sufficiently smaller basin, using b<=2d0 for the witness updates (or any conservative fixed upper bound on their actual support). The separate task of defining the correct censored quantum generator and controlling logical boundary leakage remains with the parent; no lifetime estimate is asserted here.

## 9. An explicit conservative basin constant

Write kappa_rob for the source's tensor robustness constant, to distinguish it from the physical controller rate. Let epsilon=1/12 and d0=Delta^2. Let r count the weight of a chosen joint Pauli representative modulo gauge. In one sector, at most 2r compatibility views are touched. After virtual repairs their added witness weight is at most 2d0*r, so a representative of weight r' <= (1+2d0)r suffices. At most 2r' local codewords c_v are nonzero, each admitting a row/column decomposition using at most 2Delta words. Therefore

||Z'|| <= 4Delta(1+2d0)r.

A fast sequential move obeys ||x|| <= |x|/(kappa_rob*Delta), and its total weight over the full path is bounded by |Z'|/(1-epsilon). Since |Z'|<=Delta*||Z'||, every intermediate minimum decomposition norm is at most

A ||Z'||,  A=1+1/[kappa_rob(1-epsilon)].

Theorem12's sufficient active-vertex bound is 2^(-12)*delta^2*epsilon^3*kappa_rob*|V00|. Since |V00|=n/Delta^2, it is enough to take

r < R_n := [2^(-12)*delta^2*epsilon^3*kappa_rob /
             (4*A*Delta^3*(1+2Delta^2))] n.

Use the smaller constant for the two CSS sectors, and additionally reduce R_n below a fixed fraction of d_enlarged. This conservative expression is not optimized. It demonstrates that all basin reductions are FIXED constants, not shrinking with n. Strict inequalities can be protected with an extra factor 1/2. An independent source-notation audit remains sensible before treating the numerical prefactor as certified.

### Initialization/readout and physical scope

The storage construction starts from an encoded original logical state with witness pairs initialized to zero, or from a separately proved correctable preparation distribution. It does not provide a fault-tolerant encoder for arbitrary fresh unknown quantum input for free. Initial encoding, witness preparation, local jump ancillas/reset, and final controlled-frame removal plus residual decoding have finite costs that must be matched in the active comparator. In the exact ground space, the two-layer controlled-frame unitary recovers the protected original-code state even when witnesses are coherent/entangled gauge states; one must not replace that coherent recovery by an unjustified assumption that all witness registers are already classical.

All claims here concern a bounded-degree interaction graph with fixed finite-support ideal Lindblad channels plus separately modeled local perturbations. Synthesizing those channels from bounded-arity Hamiltonian couplings, finite-temperature meters, and imperfect controllers is not supplied. In particular, noisy internal hardware that generates correlated or growing-support effective faults is outside the stated local perturbation model until derived.
