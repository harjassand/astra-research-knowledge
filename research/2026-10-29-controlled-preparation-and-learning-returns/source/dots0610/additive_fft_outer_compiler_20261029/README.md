# Explicit additive-FFT outer CSS compiler
2026-10-29. New operational compiler construction, pending independent receiving review. Known classical additive FFT and quantum Reed–Solomon machinery are used; neither is claimed as a new invention.

## Completed finite construction
An explicit ancilla-free binary CNOT circuit now implements the full-field outer evaluation transform and its inverse. At B=2048 over GF(2^11), it uses22,528 data qubits and651,264 CNOTs per transform, not merely a gate upper bound. The generated circuit is stored in circuit_h11.npz. A separately generated all-to-all schedule uses115 nonempty disjoint CNOT layers per transform. Encoder plus inverse decoder therefore use1,302,528 CNOTs and230 such layers, plus initialization, Hadamards/readout, classical decoding, Pauli correction and storage. Circuit layer counts assume arbitrary all-to-all CNOT connectivity and do not supply a routing architecture.

This replaces the earlier sufficient dense transformation recipe. It does not reproduce the old B2047 block: full-field length is B=q=2048. Nearby policy calculations are supplied separately. The compiler benefits matching and conventional guards equally.

## Governing transform construction
Let beta_j be the polynomial field basis and W_j its first-j-dimensional binary span. Define s_j(x)=product_{w in W_j}(x-w), t_j=s_j/s_j(beta_j), and B_i(x)=product_j t_j(x)^{bit_j(i)}. The linearized recurrence s_{j+1}=s_j²+s_j(beta_j)s_j implies t_j is constant on cosets of W_j and t_j(alpha+beta_j)=t_j(alpha)+1. B_i has degree exactly i and nonzero leading coefficient, so its initial segments span exactly the usual bounded-degree polynomial spaces.

For f=f0+t_j f1 on a coset alpha+W_{j+1}, first form coefficient vectors a+c b and a+(c+1)b with c=t_j(alpha), then recursively evaluate them on alpha+W_j and alpha+beta_j+W_j. The implemented order is coefficient butterflies first, recursive evaluations second. Evaluating both lower polynomials on one coset before combining would generally be wrong in this recursion.

The in-place butterfly is a <- a+c b, followed by b <- b+a using the UPDATED a. Both are reversible field additions. There are exactly B h/2 butterflies. Multiplication by known c is a binary linear map, so a<-a+c b costs at most h² CNOTs between the two existing h-bit registers. The second update costs h. Thus one transform needs at most B h²(h+1)/2 CNOTs and no additional quantum ancillas. Reversing the CNOT list implements the inverse exactly. The actual h11 count is651264, below the bound1486848.

All butterflies at a recursion depth act on disjoint register pairs. For each constant multiplication, schedule control bit j to target bit k in layer(k-j mod h); each such layer is a matching. The final h bitwise additions form one more layer. This proves depth at most h(h+1) with all-to-all connectivity. parallel_schedule.py constructs the actual115-layer schedule and checks every layer has no repeated qubit.

## CSS encoder and complete syndrome interface
For B=q, the product of all differences at a field point is the derivative of x^q-x, equal to1 in characteristic2. Thus the full-field RS dual multipliers are all1. Let T have row i equal to the evaluations of B_i. Put s=2t, H=T[:s], C=T[:B-s], R=T[B-s:], and let the middle rows be logical coset representatives. Degree filtration gives C=RS(B,B-2t), H=C-perpendicular and H contained in C. The resulting CSS code is [[B,B-4t,2t+1]]_q.

Prepare the first2t coefficient registers in uniform plus states, put the logical payload in the middle B-4t registers, prepare the last2t in zero, and execute the FFT CNOT circuit. The output is the standard uniform CSS coset encoding. No basis-change between monomials and the new basis is needed for a freely chosen encoder: the code subspaces are unchanged, while the logical representatives and complement are chosen in this basis.

Apply the inverse circuit for decoding. For a q-ary Pauli error with X labels e and trace-pairing Z labels f, the decoded labels are e'=e T^-1 and f'=f T^T. Measure the first2t registers in the binary X basis and the last2t in binary Z. The first readout is binary phase data: convert it CLASSICALLY through the trace-dual basis to obtain f'[:2t]=H f^T. A bare tensor product of Hadamards is not silently identified with the field Fourier transform in an arbitrary polynomial basis. The last readout gives e'[-2t:], from which the X syndrome is (H R^T)e'[-2t:]^T. Dropping this H R^T conversion would be wrong for the chosen high-degree complement.

H R^T is invertible: H is orthogonal to C, R complements C, and the ambient field pairing is nondegenerate. Feed these two actual syndromes to the already-received total Berlekamp–Welch correction procedure. It operates on the same RS vector code, so its monomial interpolation representation does not require the quantum encoder to use monomial coefficient registers. Apply the resulting decoded logical Pauli corrections to the retained middle registers. Uncorrectable records receive the inherited total fallback.

## Why this corrects coherent errors
A nonzero vector in C has weight at least2t+1. Therefore two Pauli errors of weight at most t cannot share the same pair of stabilizer syndromes unless their difference acts trivially on the code. The syndrome measurement distinguishes the correctable error classes without learning the logical payload, and correction restores the same logical state in every class. By linearity of the error span and the Knill–Laflamme condition, this covers arbitrary coherent combinations of errors supported on at most t outer symbols, including environmental correlations. It is not restricted to a classical random Pauli model. This is established CSS/QEC machinery instantiated with the new transform, not a new correction principle.

## Executed evidence
additive_fft.py uses exact finite-field and binary arithmetic. For h3,4,5,6,8,11 it generates actual CNOT lists, checks three random forward/inverse bit circuits, and compares direct polynomial evaluation at all points for h<=6 and64 selected points per vector at larger h. It exhaustively checks every field coefficient basis vector against the full evaluation matrix for h<=5. This does not mean every basis vector was numerically enumerated at h11; the general correctness follows the recursive construction above.

Complete small-code syndrome and total-decoder checks cover548 correctable Pauli patterns for (B,t)=(8,1),(16,1),(16,3),(32,2),(32,5). They independently propagate binary Pauli labels through the actual inverse CNOT circuit, compare field labels, perform trace-dual readout conversion, verify both syndrome identities and invoke the actual inherited decoder. Exact small matrices verify invertibility and H C^T=0. No floating logical state amplitudes are needed for these Clifford/Pauli checks. No noisy hardware experiment is claimed.

## Updated nearby finite guard and remaining costs
nearby_B2048_policies.py retains the earlier R,b policy choices and re-evaluates them at J=22528, B2048. It does not relabel the old B2047 probabilities or re-optimize the policies. The source-known retained-memory calculation remains conditional on one learned history.

A sufficient illustrative composable error budget of1/256 for the1,302,528 encoder/decoder CNOTs would require each primitive's half-diamond deviation to be at most (1/256)/1302528, approximately3e-9, using a worst-case hybrid sum. This is NOT a necessary threshold, an achieved calibration, or a fault-tolerant implementation. Any per-gate guarantee must be composable on the actual complete interface, not only isolated average gate fidelities. Other gates, preparation, measurement, memory and routing errors need their own budget.

The previous policy guard already allocated1/128 to accepted source faults. Adding1/256 CNOT error yields3/256 before other errors, not a total1/128 certificate. The nearby file also lists the larger t needed to retune that guard to1/256, but spending the other1/256 entirely on CNOTs would leave no allowance for other operations. No complete physical1/128 budget has been closed.

The full large FFT circuit is compiled and executed on basis-bit data; the large B2048 classical total decoder has NOT been benchmarked end-to-end. Its inherited polynomial-time dense interpolation can be expensive. Trusted22,528-qubit buffers, source latency, physical interconnect and fault-tolerant endpoint operations remain substantial obligations. The compiler removes one dense quantum-transform cost, not all practical architecture costs.

## Primary sources and novelty boundary
Lin, Chung and Han, arXiv:1404.3458v1 (2014), SectionsII–III, defines normalized subspace-polynomial products and a fast invertible evaluation transform. The governing basis and recursion are established classical machinery. https://arxiv.org/html/1404.3458v1

Grassl, Geiselmann and Beth, Quantum Reed–Solomon Codes, arXiv:quant-ph/9910059v1 (1999), already presents quantum RS encoding/decoding using finite-field Fourier circuits and discusses dual binary bases. https://arxiv.org/html/quant-ph/9910059v1

These sources were actually read. The present deliverable is an explicit additive-transform implementation, syndrome/readout integration and concrete gate accounting for this guarded architecture. No first quantum RS encoder, first FFT encoder or historical novelty claim is made.

## Reproduction and immutable dependencies
Run additive_fft.py, parallel_schedule.py and nearby_B2048_policies.py. The last uses sibling guard_policy_optimization_20261029 data/module. received_grs_wrapper_v1.py is an unchanged copy of the reviewed earlier total GF/GRS decoder; field_certificates_received.json is an unchanged earlier field-certificate output. Python3.12.14 and NumPy2.3.5 were used. The manifest binds all new scientific files and exact received dependencies.
