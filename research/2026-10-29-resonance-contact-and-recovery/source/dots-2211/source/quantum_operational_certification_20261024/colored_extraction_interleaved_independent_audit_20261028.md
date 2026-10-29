# Independent hard review: colored extraction faults and interleaved local logical precision

28 October2026. PASS_SCOPED_PER_LOGICAL_LOCAL_FAULT_COMPOSITION, after explicit hardware-composition correction. Governing source SHA998cd7d4c688174db2a7d8e03a171e2e9a1c7cf6fd2a46a01ab41d6ea60d7002. This is a per-logical complete-reference theorem, not a global threshold or whole-array diamond theorem. Original pre-correction source is retained by author.

## Geometry and actual schedule

The packing argument uses more than interval cardinalities: k distinct globally compatible input factors generate a faithful copy of M_(2^k). If all act on h physical qubits, a faithful representation requires k<=h. At any physical point, all width-W containing envelopes lie in a2W−1-site region; their underlying factors therefore number at most2W−1. Interval-graph coloring yields chi<=2W−1. Arbitrary independently fitted triples would not justify this argument; ONE common V is indispensable and stated.

A fault's forward physical span begins at length<=W and expands by<=W−1 at each end per remaining color. Every receiver reached has its anchor inside this span. All anchors between the extreme reached anchors count toward rank span, and their true factors fit in that span expanded right byW−1. Thus the consecutive sorted-rank span is bounded by2W−1+2chi(W−1)<=L=(2W−1)^2. This is stronger than merely counting reached receivers and is the property interleaving needs. Code positions separated by at leastL cannot both lie in a rank span of length<=L.

For backward cones, begin each receiver at its anchor as a conservative physical overapproximation. Across chi layers the physical span is<=1+2chi(W−1); relevant macro owners' true supports lie in its two-sidedW−1 expansion, totaling<=L factors. Five carrier cones therefore involve<=5L macro locations. The separate native-input bound is not inferred from a circuit for V: if S_i misses the physical cone, every observable there commutes with both B_i,X and B_i,Z, so conjugation byV† lies in the commutant of the full input-i matrix algebra and acts identically there. The same packing bounds relevant native sites by5L. Operator-valued reference coefficients do not change this commutant conclusion.

The bounded-output tile modification is valid. Completeness of the n input factors forces their containing intervals to cover every output site; otherwise the generated full output algebra would commute with an unused site's nontrivial operator. Consecutive anchor gaps are therefore<=W. Five-L-rank tiles have bounded physical output span<=5LW. This DOES NOT bound input-port permutation/routing: the source explicitly charges it or requires extra geometry.

## Why a single arbitrary coherent fault is actually correctable

The true macro is the swap between A_i and the V-defined factor, equivalently the SWAP polynomial(I+sum_j B_i,j sigma_Ai,j)/2. Across i these ideal swaps commute because the factors and receivers are distinct. Their product is(V⊗I) SWAP_(P,A) (V†⊗I). With fresh maximally mixed receiver input it extracts the original full input and leaves the discarded physical workspace maximally mixed and independent of that input/reference.

For one actual local CPTP replacement F_i, define its relative map F_i composed Ad_(W_i†), which is still CPTP and local to J_i,A_i. Conjugating through the IDEAL suffix gives a final CPTP fault on the forward cone. It can affect at most one carrier per selected code, though it may coherently couple that carrier to other codes and workspace. This is not independent stochastic noise.

The standard five-qubit code has V_code† E_a†E_b V_code=delta_ab I for its16 identity/single-carrier Pauli errors. Expanding an arbitrary joint fault Kraus operator as sum_a E_a⊗F_a, syndrome recovery removes cross syndromes and acts as identity on the protected logical subsystem tensor a TP spectator map. This holds on arbitrary encoded inputs entangled with other logicals and an external reference. Tracing processed spectators therefore gives exactly the desired reduced logical/reference channel. Tensor-product recovery corrects a single fault touching one carrier of each selected code jointly. A single native input-qubit error beforeV is corrected for the same reason.

This reasoning establishes first-order cancellation; finite support enumeration alone would not establish it. Independent code checks construct the actual standard stabilizer encoding, verify all256 Knill–Laflamme pairs and the complete32-dimensional syndrome basis using exact bounded integer-complex arithmetic.

## Fault expansion and scope correction

Outside the ACTUAL/IDEAL union-support backward cone, TP local maps cannot change the chosen output observable, even for entangled inputs. Remove those locations before expanding. For each remaining native input location ||N_i−id||diamond<=2p; for each macro ||F_i−Ad_Wi||diamond<=2e. All zero- and first-order protected terms are the ideal logical map or zero difference. Submultiplicativity across intervening CPTP maps bounds the remaining signed sum by

 (1/2)[(1+2p)^(5L)(1+2e)^(5L)−1−10Lp−10Le],

clipped at1. Replacing5L by5kL handles any fixed k selected codes. This is valid on the full logical-input domain with arbitrary external reference, while unselected processed logical outputs are discarded. It does not control the joint error of an unbounded number of logical outputs independently ofn.

An important scope gap was challenged and corrected before receipt. Per-gate reduced local/diamond-close marginals DO NOT imply this ordered local CPTP composition when a bath retains correlations across locations. The revised source requires the actual fixed composition (nominal learned unitary macros already satisfy it); unresolved shared bath is a separate whole-process discrepancy. Extending explicit memory wires would require a new causal/norm proof. The native channel also retains its actual product-input-site premise.

Independent negative control: one shared bad coin appliesX to all five code carriers with probabilityh. Every single-site marginal is h-close to identity, but XXXXX is logicalX and total logical error ish. At h=1/100 this exceeds the falsely substituted quadratic five-location bound. The exact fixture verifies this logical action. Hence the new hardware wording is load-bearing, not cosmetic.

## Resource consequences and independent evidence

With fixedW and conditioning, choosing delta=O(p) gives e=O(p) and a quadratic LOCAL logical bound. This removes an unnecessary delta~1/n target for this particular encoded objective. It does not invent a new acquisition estimator; the inherited finite operator-certificate mechanisms, simultaneous confidence, source exposure ofn carriers per block, conditioning, finite caps and synthesis remain charged. Encoder, input routing, syndrome recovery and other unabsorbed operations need total relevant complete-norm debitO(p²) to preserve that scaling. No fault-tolerant construction for them is supplied.

Reran author's735-mode/147-code support fixture. Independent ten faithful block-algebra layouts coverW1..5, multiple expanded-envelope geometries and actual color depths up to2W−1; every forward rank-span and per-code backward/native bound passes. These corroborate the general packing proof, not replace it. Exact code algebra and shared-bad-coin boundary are in `colored_extraction_independent_qec_check_20261028.py/.json`.

No further mathematical gap found at the corrected scope. Received neither global diamond scaling independent of system size, code threshold, arbitrary shared-bath service, physically free input permutation, practical budgets nor historical novelty of interleaving/QEC. The source correctly treats standard local-fault QEC as the equally informed conventional baseline.
