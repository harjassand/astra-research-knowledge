# Local extraction faults can be correctable without a globally accurate inverse

28 October 2026. New scaling candidate; independent review pending. This preserves the actual colored three-reflection receiver, but changes its accuracy target. It does not assume a fault-tolerant encoder/decoder, a threshold theorem or a global error bound independent of system size.

## 1. Fixed local algebra, actual macro-gates and bounded schedule

There are n input qubits and n physical outputs on a line. A fixed unknown unitary V has Pauli algebras B_(i,j)=V sigma_(i,j)Vdagger, each supported in an interval S_i. Accepted local acquisition supplies an interval J_i containing S_i, of length at most W, and physical reflections Shat_(i,X/Z) supported on J_i satisfying

    ||Shat_(i,j)-B_(i,j)||op <= delta.

These are acquired operator certificates, not merely average Bell scores. The true algebras come from ONE global V and commute across i; independent locally valid triples are insufficient.

For each i, group its actual three-controlled-reflection extractor into one unitary macro-gate What_i on physical interval J_i and its own fresh receiver qubit A_i. Let W_i use the true B generators, on the SAME support envelope and ancilla. The actual gate construction gives

    ||What_i-W_i||op <= 2delta_Z+delta_X <=3delta,
    half||Ad_What_i-Ad_W_i||diamond <=3delta.                 (1)

Receiver qubits are independently initialized maximally mixed; their preparations and all controlled gates are paid. The comparison does not promote a noisy nonunitary hardware gate into an exact unitary: an additional actual patch-local diamond gate error can be added to the macro fault strength when its locality is certified.

Color the physical intervals J_i so overlapping intervals have different colors. At a given physical site x, all J_i containing x lie inside[x-W+1,x+W-1]. Hence all corresponding independent qubit algebras S_i lie in a region of at most2W-1 physical qubits. The commuting independent input factors generate a copy of M_(2^k) for k such inputs. Any faithful representation requires a Hilbert-space factor of dimension at least2^k, whereas this physical region has dimension at most2^(2W-1). Thus packing implies k<=2W-1. Interval-graph greedy coloring therefore gives

    chi <=2W-1.

Execute all macro-gates of each color in parallel, then the colors in a fixed order. This is macro-depth chi and controlled-reflection depth3chi. Ideal W_i commute across i and perform full extraction independent of this order; the learned What_i need not commute. The ACTUAL schedule, not an imagined commutative approximation, defines its lightcones.

## 2. Sort physical anchors and interleave known codes

Assign each receiver A_i the physical anchor ell_i=min(J_i) and sort input indices by ell_i, breaking ties by a fixed declared rule. This is a classical permutation learned from the support certificates. Let

    L=(2W-1)^2.

Take n=5m with m>=L. Encode m logical qubits by m known standard five-qubit codes, routing code b's five carriers into the input labels of sorted ranks

    b, b+m, b+2m, b+3m, b+4m.

The output receiver qubits are decoded with the matching permutation. This may require long-range encoding/routing and syndrome operations; their physical cost is NOT bounded by the local extraction schedule. They are separate whole-process error debits. Extra unused carriers or incomplete boundary groups require an explicitly specified layout; this statement uses exactly5m carriers.

A macro-gate fault begins on J_i plus A_i. Under the remaining at most chi layers, its physical interval expands by at most W-1 sites per side per layer. Its final interval has length at most W+2chi(W-1). Any affected receiver anchor lies in that interval. All true algebras with anchors in an interval of length h lie inside an interval of length at most h+W-1; packing bounds their number by h+W-1. Consequently one macro fault can affect at most

    2W-1+2chi(W-1) <= L

CONSECUTIVE sorted receiver indices. It can therefore touch at most ONE carrier of each interleaved five-qubit code, because two carriers of that code have rank gap m>=L.

This is a support bound for arbitrary coherent macro faults, not a claim of independent stochastic errors or a small-probability fault trajectory.

### Bounded output tiles instead of one global interleaving block

For n a multiple of5L, partition the sorted receiver ranks into consecutive tiles of5L. Within each tile encode L standard codes at offsets b,b+L,b+2L,b+3L,b+4L. The same single-fault rank-span bound proves correctability, including faults crossing a tile boundary: two carriers belonging to any one code still have rank gap L. The per-code bound below is unchanged.

Because the n true input algebras generate the FULL n-qubit output algebra, every physical output site belongs to some true support S_i; otherwise all generators would commute with a nontrivial local operator there. Thus the containing intervals J_i cover the physical line. Consecutive sorted left anchors cannot have a gap greater than W, since that would leave an uncovered site. A tile of5L receiver anchors therefore lies within a physical span of at most5LW sites. Output decoding and receiver routing can consequently stay within a bounded physical region at fixed W, rather than spanning the full growing array.

This does NOT automatically localize the input encoder: the current support promise permits an arbitrary permutation between input labels and output anchors. For bounded input-side routing, add an actual known input/output geometry condition, such as bounded displacement between each input port and its acquired output anchor, or pay the calibrated static quantum routing/permutation hardware. The tile observation removes an avoidable output-layout cost but does not create free long-distance input communication or a fault-tolerant encoding circuit.

## 3. Why every first-order macro fault is corrected

With all ideal macros, the full extraction unitary swaps the V-defined input algebra into the receiver qubits. The discarded physical outputs carry the transformed fresh mixed receiver register; because that register is I/2^n, the discarded register is exactly I/2^n and independent of payload and source reference.

Insert one arbitrary local CPTP macro replacement, leaving every other macro ideal. Conjugating its relative difference through the later IDEAL macro suffix gives a final fault supported within the lightcone above, possibly also acting on discarded physical workspace. After the ideal extraction, that workspace is independent. The induced CPTP operation may couple the one affected carrier of code b to other codes/workspace, but it acts on at most one carrier within b.

Expand its Kraus operators in the four Pauli operators on that carrier with operator coefficients on the spectator systems. The known five-qubit recovery eliminates cross Pauli syndromes and restores the logical b subsystem; trace preservation gives a CPTP spectator map. Thus, after discarding spectator outputs, logical b and every untouched external reference are exactly restored. The same argument holds jointly for any chosen set of logical codes: a single fault touches at most one carrier in each, and their product syndrome recovery corrects the whole joint error.

Likewise any one native single-input-qubit CPTP error before V is exactly corrected. Therefore first-order terms in an expansion by native input errors and local extraction macro replacements vanish for the protected logical output(s). This is not the false assertion that the entire learned extraction is globally within3delta of Vdagger; its uncoded global difference can still be order n delta.

## 4. Bound the number of relevant fault locations, not all n gates

Consider one logical output b after its known decoder; the other logical outputs are discarded. An arbitrary observable on its five receiver carriers has a backward lightcone that is the union of five intervals. For one carrier, after chi macro layers the physical interval length is at most

    h_b=1+2chi(W-1).

Every macro interval meeting that cone has its true algebra inside the cone expanded by W-1 on both sides, hence there are at most h_b+2(W-1)<=L relevant macro owners. Across the five carriers there are at most5L macro locations.

To pass through the black-box V, use its actual local algebra property: if S_i is disjoint from a physical region J then EVERY operator on J commutes with B_(i,X/Z). Its conjugate by Vdagger therefore acts as identity on input i. The reduced output on J depends only on inputs whose S_i intersect J. Those algebras lie in J expanded by W-1, so the same packing bound gives at most5L relevant native input sites. This reasoning also holds for operator-valued observables with arbitrary external reference; no microscopic V circuit is assumed.

All other TP fault locations are outside the ACTUAL/IDEAL union-support backward cone and cannot affect the selected logical output. Remove them before expanding. Suppose the actual native reduced channel is a product of single-input-qubit channels with half-diamond error at most p, and the actual macro replacement strength is at most e=3delta (plus any explicitly local implementation allowance). Complete CPTP contraction and cancellation of all first-order terms then give

    half||logical_b_map - ideal_trace_other_logicals||diamond
      <= min(1, (1/2)[(1+2p)^(5L)(1+2e)^(5L)
                            -1-10L p-10L e]).              (2)

The map domain includes all logical inputs and an arbitrary external reference; the output is logical b with that reference, while other processed logical outputs are traced. At fixed W, the bound is O((p+e)^2), independent of n. For any fixed k selected logical outputs, replace5L by5kL. A global all-logical-output guarantee can grow with k; no system-size-independent global diamond bound is claimed.

The strict product native-noise premise is material. Cross-input correlated noise not accounted for as bounded local fault locations can invalidate the expansion. Calibration/source memory correlations likewise need an actual conditional channel contract; reduced one-shot marginals alone do not suffice.

## 5. Accuracy, acquisition and implementation consequences

Choose local generator accuracy delta=O(p), not a global zeta/n. Every individual macro error is then a correctable first-order location, so (2) gives quadratic local logical error at fixed support width. Ordinary operator-certified acquisition has conservative O_tilde(delta^-2) source BLOCK cost at fixed local conditioning, with simultaneous confidence logarithms in n rather than an artificial n² precision factor. Physical exposure still costs n carriers per block, so this is not constant total experimentation as n grows. Positive-block fitting/arithmetic may remain expensive.

This statement changes the error budget supplied to the actual acquisition guards; it does not receive a new efficient estimator by assertion. Its finite caps, confidence failure beta, real input/readout/control errors and any dependence of conditioning on W remain. The code's encoder, long-range permutation/routing, decoder, storage and nonlocal hardware errors must be paid separately. To retain O(p²) final local error their total relevant complete-norm debit must also be O(p²), unless a separate fault-tolerant construction absorbs them. No such fault-tolerant construction is supplied here.

A dense or badly overlapping mixer can make W grow; then L and the packing/conditioning bounds deteriorate. A system with fewer than5L carriers does not fit this simple layout. Adjacent code carriers need not be safe: a single two-carrier correlated Pauli fault can be an uncorrectable first-order channel. The interleaving is an actual architectural requirement, not merely relabeling a physically fixed code at no routing cost.

Standard local-fault QEC and interleaving are the equally informed baseline. The candidate addition is a precise route from independently acquired local generator certificates to correctable extraction faults, without first demanding a globally accurate uncoded inverse. Historical novelty, an efficient complete processor and a threshold remain unestablished.

## 6. Exact scheduling fixture and source status

colored_extraction_lightcone_check_20261028.py constructs735 input/output modes and147 interleaved codes in three bounded output tiles with W=4. True input algebras occur in neighboring two-qubit blocks and accepted envelopes are expanded to width at most4. It greedily colors the ACTUAL envelopes, enumerates every single-macro forward cone and every logical-code backward cone as finite sets, and checks both correctability separation and native-input support packing. Actual macro depth is4 (the universal bound is7); the largest forward sorted-receiver span is6 (universal L=49); each logical backward cone has at most20 macro owners and42 native input sites (universal bounds245 each). These are exact support checks, not a735-qubit quantum simulation or evidence of feasible long-range encoding.

Dependencies: ordinary_local_inverse_coherent_memory_fallback_20261028.md for the literal extractor/operator telescope; positive_operator_clifford_acquisition_20261028.md and the ordinary local-support sources for physical local certificates; interleaved_patch_qec_absorbs_calibration_error_20261028.md for the standard code interface. This new lightcone-to-QEC composition requires its OWN substantive review. Its status is not inherited from any earlier local theorem.
