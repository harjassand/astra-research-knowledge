# Correcting causal memory faults while retaining a quantum receiver advantage

Author `/root`, 29 October 2026 Australia/Brisbane. Authored construction; independent review is separate. Previous accepted proofs and comparisons remain unchanged.

## 1. Fixed operation

There are L source pairs (x_j,z_j) and L field pairs (A_j,B_j). The source interaction is

\[
U=\sum_{x,z}|x,z\rangle\langle x,z|\otimes
\bigotimes_{j=1}^L (X_{A_j}^{x_j}Z_{A_j}^{z_j})(X_{B_j}^{x_j}Z_{B_j}^{z_j}). \tag{1}
\]

Fields arrive after their contacts in order A1,B1,A2,B2,... . Common field states, inter-arrival correlations and correlations with the encoded source/reference are arbitrary. No known Bell/vacuum preparation or preparation-side information is supplied. The task is deterministic erasure of this specified contact while preserving unknown encoded data. This is a recovery primitive, not a free computing gate. If the contact can simply be avoided, avoiding it is a strong alternative.

The exact receiver retains one controlled qubit across each A_j-to-B_j gap, measures X_A X_B and Z_A Z_B when B arrives, retains both actual Bell bits and applies the prescribed source Z phases. This is the finite Pauli receiver; there is no phase-estimation cutoff or numerical solver. A memory Pauli Q with QX=(-1)^a XQ and QZ=(-1)^b ZQ induces source phase character Z_x^a Z_z^b.

Let E_t consist of length-2L binary vectors with nonzero two-bit blocks at at most t locations. Its size is

\[
V_4(L,t)=\sum_{j=0}^t\binom Lj3^j. \tag{2}
\]

A returning quantum fault bath is additional physical quantum memory and must be included in a total cut-dimension budget. The one-qubit resource separation already holds for the included subclass with local/discarded environments or no returning noise bath. The same code extends robustness to persistent adversarial baths without counting them as free memory or as an acquired computational resource.

The noise assumption is a completed amplitude contract: each supported fault path in a source-independent causal dilation acts at no more than t retained-register locations. Coherent superpositions of allowed locations and a persistent quantum fault bath are allowed. The bath must not directly access the source or future source-imprinted fields outside the declared interfaces. Instantaneous locality alone is insufficient; a bath visiting all locations generally creates higher-order paths.

## 2. Actual source correction and complete record

The theorem in `../protected_algebra/COHERENT_FAULT_TRANSMUTATION.md` gives complete receiver Kraus operators, after its prescribed feedback,

\[
K_{y,\alpha}=\sum_{e\in E_t}Z^e\otimes A_{e,y,\alpha}. \tag{3}
\]

The A operators retain the field/bath dependence; y is the actual receiver record and alpha an unobserved index. This is a coherent sum, not a Pauli mixture. It holds for all initially correlated encoded source/field/reference inputs.

Choose a binary b-by-2L matrix H separating E_t: He differs from Hf for every distinct e,f in E_t. The source code is the +1 eigenspace of X^{h_i}, for independent rows h_i of H. It encodes 2L-rank(H) qubits. Measure these actual checks after the receiver, infer e from syndrome s=He, and apply Z^e. If V is the code isometry and P_s the syndrome projector, then

\[
V^\dagger Z^eP_{He}K_{y,\alpha}V=I_{\rm logical}\otimes A_{e,y,\alpha}. \tag{4}
\]

Thus the corrected full instrument, including Bell bits, actual source syndrome and all retained common outputs, is id_logical tensor R_C. It is trace preserving because the circuit is. R_C is a **code-dependent common instrument**, generally different from the previous same-noisy-receiver record law. No mathematical fault label was physically measured to derive (3); only the implemented source syndrome was measured.

A diagonal target G commutes with the phase errors, but changes the output code to GC. A compatible decoder must be supplied: if G preserves C and a declared logical action, the same checks suffice; otherwise G-conjugated checks or a separately constructed decoder must be paid. This file proves the identity/erasure operation, not an arbitrary nontrivial G.

## 3. Exact finite construction

Use GF(4)={0,1,w,1+w}, w^2=w+1. The quaternary parity-check matrix has the five projective columns of GF(4)^2, normalized to first nonzero entry 1. Expanding multiplication in basis (1,w) gives four binary X checks on ten source qubits. The 1+3*5=16 zero-or-one-location characters have all sixteen distinct four-bit syndromes.

This is the ordinary quaternary [5,3,3] Hamming/MDS construction, used as a phase-error source code. It encodes **six logical qubits**, corrects one arbitrary completed coherent faulty storage location, and uses one receiver qubit across each of five gaps. Known coding theory is credited; the constructed bridge is its actual causal receiver and record interface.

`exposure_codes.py` emits both matrices, the syndrome table, a source CNOT/SWAP encoder and inverse-decoder prescription. Exact integer checks verify 65,536 syndrome/amplitude identities, 16,384 diagonal codeword KL identities (cross-codeword terms vanish by disjoint support), all 1,024 encoder basis inputs and all 90 two-location phase errors. A two-location failure is preserved: the single-location decoder leaves a nontrivial logical phase. Two-fault protection is not claimed.

| Resource | Emitted circuit |
|---|---:|
| Physical source / logical qubits | 10 / 6 |
| Fresh plus-state gauge inputs | 4 |
| Controlled receiver qubits held across each gap | 1 |
| Arriving field qubits | 10 |
| Source-to-field controlled Pauli contacts | 20 |
| Bell CNOT / Hadamard / readout | 5 / 5 / 10 |
| Source encoder | 44 CNOT + 1 SWAP |
| Source decoder | inverse encoder |
| Source syndrome controlled-X contacts | 18 |
| Actual source syndrome bits / Bell bits | 4 / 10 |

This transparent Gaussian-elimination encoder is not gate-count optimal. A SWAP can be decomposed into three CNOTs. Two field/receiver qubits coexist during Bell analysis: across-gap memory is not processing peak. Syndrome extraction can reuse one prepared/reset ancilla; preparation, H gates, measurement, reset, source holding, readout fidelity and feed-forward delay are additional costs. Source correction adds at most two Z operators in these coordinates, besides receiver phase feedback.

Capture, controlled access and source gates must be supplied. Memory loss fits only if a declared loss/replacement instrument returns the qubit interface with its record. Uncontrolled leakage with later return is not automatically a qubit error. Source X/Y noise, contact faults, analyzer faults and syndrome faults need their own acquired channels. Zero ideal logical error is not a device error rate.

## 4. A comparator granted arbitrary encoding and final recovery

The independently constructed `../classical_capacity/CAUSAL_CODE_CAPACITY.md` allows any K-dimensional source code and arbitrary final source CPTP recovery using every actual receiver record. For any receiver classical at all L specified gaps,

\[
F_e\le\min(1,2^L/K),\qquad
\epsilon_{\diamond/2}\ge\max(0,1-2^L/K). \tag{5}
\]

Its legal test input has maximally mixed common field and a maximally entangled encoded logical/reference pair. Actual receiver effects determine a Bell posterior; a coding-and-decoding fidelity inequality yields (5). It does not restrict codes to stabilizers or recovery to phase correction. Joint quantum processing between specified gaps is allowed. All coherent buffers crossing a designated gap must be counted.

For L=5 and K=64 every classical-at-gaps receiver has actual logical half-diamond error at least **1/2**. The constructed quantum receiver/code has zero logical error under the exact one-location fault contract. The classical comparator can perfectly preserve five logical qubits. It receives unlimited classical memory, code knowledge and decoder freedom, but no undeclared cross-gap quantum register, entangled supply or extra source-to-field contact.

If q gaps permit quantum passage and the rest are classical, exact preservation obeys k<=L+q, attained with one qubit at each selected gap. For actual quantum cut dimensions D_j the general bound is k<=L+sum_j log2(D_j). Thus peak memory misses the number of boundaries over which coherence survives. This discrete budget is not a duration, energy, query-count or loss bound.

### Scoped finite-code optimality

Six logical qubits is optimal for the prescribed Bell receiver/feedback plus arbitrary final source decoder against one unknown Pauli memory fault among the five intervals. On maximally mixed field, every Bell record is uniform and independent of source and chosen Pauli fault. Averaging record-conditioned recovery gives a decoder for the unflagged error set E_1. KL products contain the entire diagonal Pauli algebra on any two source pairs, i.e. four bits. Each joint-character projector Pi has rank 2^(10-4)=64. KL gives V^dagger Pi V=c_i I_K. Some c_i>0, hence K<=rank(Pi)=64.

Only the Pauli subfamily is needed for necessity; coherent faults generally do not yield an independent record. Optimality here does not include redesigned receivers, additional fault observations, new source contacts or active receiver-memory protection.

A known independent Phi+ field pair is a +1 eigenstate of both branch generators and needs no receiver. Its acquisition changes the common-field contract. Conventional protected receiver memory and closed bus loops may also be cheaper. Equation (5) is not hardware superiority against these different supplied interfaces.

## 5. Explicit family and positive fault-density existence

The projective GF(4)^m Hamming construction, m>=2, gives

\[
L=(4^m-1)/3,\quad n=2L,\quad k=2L-2m. \tag{6}
\]

It corrects one arbitrary bad gap with O(L) syndrome lookup and polynomial-size source Clifford compilation. The tested (L,k)=(5,6),(21,36),(85,162) give classical fidelity ceilings 2^-1, 2^-15, 2^-77. This family alone does not tolerate a constant density of arbitrary faulty intervals.

For general t, a random binary b-by-2L H sends each nonzero v to zero with probability 2^-b. Distinct E_t errors differ by an element of E_(2t) excluding zero. The union bound guarantees a separating H when

\[
2^b>V_4(L,2t)-1. \tag{7}
\]

Dependent rows can be removed or completed to independent ones without losing separation. This is finite verifiable search, with no efficient-decoding claim at extensive t.

For L divisible by 16 set t=L/16, b=3L/4. Then

\[
V_4(L,L/8)\le4^{L H_4(1/8)}<2^{3L/4},\qquad
H_4(p)=[h_2(p)+p\log_2 3]/2. \tag{8}
\]

The strict entropy inequality H_4(1/8)<3/8 is exactly 3*2^18<7^7 (786432<823543). To prove the ball bound, assign each word of weight j probability (p/3)^j(1-p)^(L-j). For p<3/4 and j<=pL it is at least 4^[-L H_4(p)]. The total probability is at most one. No numerical optimizer enters this argument.

Therefore a code exists with

\[
k\ge5L/4,\quad t=L/16,\quad
\epsilon_{\rm classical}\ge1-2^{-L/4}. \tag{9}
\]

One controlled receiver qubit reused over L gaps and this source code exactly preserves the logical state for the completed coherent t-location fault class. The classical comparator fails with error approaching one despite arbitrary source encoding/recovery. This is an operational separation at a positive **allowed fault density**, not a hardware threshold or efficient scalable computer. Syndrome search may be expensive, checks dense, and source storage/control costs substantial.

## 6. Ancestry, reach and limitations

Knill–Laflamme–Viola [quant-ph/9908066](https://arxiv.org/abs/quant-ph/9908066) already establish graded interaction-space correction for coherent correlated general noise. Quaternary Hamming codes, phase-error stabilizers, KL recovery and Bell/LOCC discrimination limits are known. The bridge constructed here combines them with the causal memory character map and an implemented complete-record decoder, then compares against all source codes and final decoders in the classical receiver class.

It permits correction to move from the receiver register into source redundancy while retaining a strict causal quantum-information advantage. The separate cumulative cut-dimension bound identifies a resource omitted by peak memory. This is foundational information-processing scope, without historical priority, a working device or a total workload advantage claim.

Current Astra N1063 governing source and actual curator review were read and saved. Their completed-access condition, syndrome-dependent bath backaction, sequential-contact warning and physical gaps remain attached. Missing producer numerical archives were neither reconstructed nor imported. The present exact code evidence is its own. `../FAULT_TAIL_AND_REUSE.md` treats a distinct approximate coherent model; its sufficient bound is not an exact performance calculation.
