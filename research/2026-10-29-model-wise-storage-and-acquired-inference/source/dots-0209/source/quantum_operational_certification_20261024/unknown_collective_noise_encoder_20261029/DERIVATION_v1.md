# Unknown locally twisted collective noise: encoder acquisition from pair probes
2026-10-29. New proposed theorem, not yet independently reviewed. Historical novelty not established.

## Actual interfaces and claim
An even n-qubit array has fixed unknown V_i in SU(2). During training, each independently reset source call applies the random unitary tensor_i V_i U_z V_i†, with z independently distributed according to an unknown stationary distribution. Ordinary calibrated local Pauli eigenstate preparation/readout is available, including individual site addressing. Define O_i=Ad(V_i) in SO(3). Promise: the common commutant of supported adjoint rotations R_z on real 3-space consists of scalar matrices. This is weaker than generating all SO(3), and is the exact necessary one-dimensional-fixed-space condition below. Let g>0 be the smallest nonzero singular value of I−E_z[R_z tensor R_z]. A known lower bound g0≤g is needed for the stated predetermined sample count; alternatively a statistical singular-value bound may provide an a posteriori stopping rule, but cannot certify the model promise.

Deployment need NOT be stationary or reset: all full data–bath operations, including any retained bath, must stay in the SAME conjugated collective SU(2) operator algebra tensored with arbitrary bath operators. This global structural promise is NOT inferred from finite pair data. No intermediate misaligned controls are allowed in the storage theorem. Input preparation and final decoder are calibrated and priced separately. The logical input is fresh, initially independent of training records/bath except for arbitrary external reference entanglement.

Then physical product probes discover relative frames, sufficient to compile a deterministic singlet-sector encoder storing floor(log2 Catalan(n/2)) = n−(3/2)log2 n−O(1) logical qubits. No supplied logical preparations, environment tomography, entangled training inputs, or postselected singlet sampling is required. Polynomial-cost trusted Schur synthesis is still required.

## Pair acquisition and exact identification
For pair i,j, a correlation matrix C transforms as
T_ij(C)=E_z[(O_i R_z O_i^T) C (O_j R_z^T O_j^T)].
Row-major vec gives matrix E_z[(O_i R_z O_i^T) tensor (O_j R_z O_j^T)]. The right unit fixed vector is vec(O_i O_j^T)/sqrt(3).

If T x=x, each orthogonal realization K_z has ||K_z x||=||x||. Since E||K_zx−x||²=2||x||²−2<x,Tx>=0, K_zx=x almost surely. Thus the fixed space is exactly the common fixed space, and under the scalar-commutant promise it is one-dimensional. A nonnormal eigenvalue gap is not a replacement for the singular gap of I−T.

To measure entry T[(a,b),(c,d)], prepare +1 eigenstates of Pauli c,d at the pair, arbitrary product states elsewhere, pass one full array through source, and measure Pauli a,b. The product of the two ±1 outcomes has mean exactly this entry: conjugated product unitaries preserve Pauli degree and no identity/single-body contamination appears. Use 81 settings and m independent calls each per star edge (i,1). This explicit nonparallel schedule costs N=81(n−1)m full n-qubit calls, O(nN) physical qubit traffic/preparation, O(N) measured pairs, and O(n) stored 9×9 estimates. Individual-shot storage can be replaced by counters.

Hoeffding and a union bound give all 81(n−1) entry errors ≤η with probability ≥1−δ when
m≥2 η^(−2) log[162(n−1)/δ].
Then every block operator error e≤9η.

## Robust SO(3) rounding
Let A=I−T and Ahat=I−That, with ||Ahat−A||≤e. Choose unit right smallest-singular-vector vhat. Its residual satisfies ||A vhat||≤2e since min||Ahat v||≤e. Writing true unit kernel vector v, the orthogonal part is ≤2e/g. After sign alignment,
||vhat−v||≤2 sqrt(2)e/g.
Hence M=sqrt(3)reshape(vhat) is within d=2 sqrt(6)e/g of either C or −C. Choose the closest rotation among the polar SO(3) projections of M and −M, together with the corresponding sign. Because distance(SO(3),−SO(3))=2 in Frobenius norm, d<1 guarantees correct branch selection. Nearest-rotation projection gives
||Chat−C||_F≤2d=4 sqrt(6)e/g.
Set estimated O_1=I, O_i=Chat_i1. The exact comparable gauge is W_i=O_i O_1^T. A global common rotation changes no singlet code.

SU(2) lifts can be selected up to irrelevant local signs, with
||Vhat_i−Wlift_i||op≤(1/2)||Ohat_i−W_i||F.
Proof: rotation discrepancy θ∈[0,π] gives SU norm 2sin(θ/4) and SO Frobenius norm 2sqrt(2)sin(θ/2); their ratio ≤1/2. Tensor telescoping yields total basis-unitary discrepancy α≤2sqrt(6)(n−1)e/g.

## Storage bound, including quantum bath memory
Let E embed the chosen logical space in the total-spin-zero sector. The exact aligned collective algebra acts as identity on this sector, so any sequence of full data–bath operations in that algebra leaves E's logical state intact. Compare the learned physical encoder Vhat E to exact V E: their induced channels differ by ≤2α in diamond norm. Compare final learned decoder (Vhat† then Schur inverse, with arbitrary fixed leakage replacement) to exact decoder: also ≤2α. Contractivity around the WHOLE intervening data–bath process gives
||LearnedService_T−id||diamond ≤4α ≤8sqrt(6)(n−1)e/g ≤72sqrt(6)(n−1)η/g,
for every horizon T. This is a uniform bound, NOT a statement that measured error is constant in time. Small frame mismatch acts at two boundaries and cannot be charged per storage step under the fixed algebra promise. Add actual encoder/decoder diamond implementation errors separately. Symmetry-breaking deployment noise instead accumulates with its own whole-process bound and is not covered.

For target ε≤1, choose η=ε g0/[200(n−1)]. This ensures both the sign separation condition and ≤ε service diamond error. The deliberately conservative schedule has O(n³ g0^(−2) ε^(−2) log(n/δ)) full-array calls and O(n⁴ ...) physical qubit traffic. Classical processing is n constant-size SVDs and rotations. Schur encoding/decoding is poly(n,log(1/precision)) for local d=2; local rotations add O(n) synthesis. This is a polynomial existence construction, not a competitive sample-optimal architecture.

## Failure and scope checks
* Identity training: 9-dimensional pair fixed space, no relative frames identifiable; actual identity noise is harmless. Identifiability failure does not prove impossibility of memory.
* Single-axis generic rotation: fixed dimension 3; an axial gauge remains. A different dephasing-adapted code may work, but this full-frame algorithm is not certified.
* Rare excitation: g tends to zero as training approaches identity; no gap-free finite sample bound asserted.
* Pairwise tomography under unrelated noise can fit some relative frames without certifying a common global data–bath algebra. A later symmetry-breaking operation defeats the storage claim. Even every one-time reduced marginal is insufficient to license arbitrary retained-memory composition.
* Determinant sign: using an arbitrary SVD eigenvector as a frame without ±SO(3) selection is wrong.
* Global frame is unidentifiable but irrelevant. Relative frames require no pre-existing logical encoder.
* Bath memory during training is excluded in v1. Full-memory deployment is allowed only by the separate fixed algebra promise.

## Reproducible first check
`check_v1.py` uses n=4, independent unknown local frames, four collective rotations, physical-product-probe Bernoulli statistics, and SVD/polar reconstruction. The deployment is a coherent system–bath Hamiltonian sum_a V J_a V† tensor sigma_a, with one retained bath qubit (not fresh iid reduced noise). It prepares a logical Bell pair through the inferred two-dimensional singlet encoder and measures entanglement fidelity including leakage over t=0,1,10,100,1000. Exact-block acquisition is a diagnostic baseline, not a zero-call physical algorithm. Finite samples cost the listed 243m full-array calls. At m=100000, observed fidelities exceed 0.99954 over these five horizons. This is a small numerical sanity check, not a proof or hardware result; values above one by 1e−13 are floating-point artifacts. Identity and axial fixed dimensions are checked as 9 and 3.

## Conventional comparator and sources
This is standard DFS/noiseless-subsystem and Schur machinery after learning frames. No novelty is claimed for noise commutants, noiseless subsystems, or efficient Schur encoding. The proposed distinct interface is dimension-9 pair acquisition of unknown local conjugations with finite-shot costs and a full-memory boundary-mismatch guarantee. A strongest equally informed conventional alternative can use the SAME pair symmetry and Schur mechanism; no advantage over that alternative is established. General full-channel commutant tomography is not the sole baseline.

Primary sources checked 2026-10-29 (abstract-level navigation so far, not load-bearing new transfers):
* Choi–Kribs, A method to find quantum noiseless subsystems, PRL96 050501 (2006), https://arxiv.org/abs/quant-ph/0507213 ; general operations/commutant methods.
* Holbrook–Kribs–Laflamme, Noiseless subsystems and the structure of the commutant in quantum error correction, QIP2 (2004)381, https://arxiv.org/abs/quant-ph/0402056 ; unital commutant computation.
* Bacon–Chuang–Harrow, Efficient Quantum Circuits for Schur and Clebsch-Gordan Transforms, PRL97 170502 (2006), https://arxiv.org/abs/quant-ph/0407082 ; poly(n,d,log1/ε) synthesis, d=2 here.

Astra plugin first search on 2026-10-29 found current N1144 and N1143. Both N1144 capsule pages read at revision ad7ff1b9d15a774d4b4d8362314c7070cac030e5, input 5788b3479627421d3a67e1e6fced19f66323e94e01ccdaf4bf094a14547aa8b9. N1144 assumes logical preparation/readout, known physical geometry/width, common logical algebra, reset, contrast, separate global identity dominance. This construction uses none of its proofs as premises and does not inherit its acceptance. Its distinction is discovering the encoder using physical inputs. Source corrections/current on-site freeze successors remain relevant navigation, not a transfer proof.
