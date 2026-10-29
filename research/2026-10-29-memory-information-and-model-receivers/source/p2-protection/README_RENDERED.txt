Readme
Astra P2: protecting the quantum information that a causal operation needs

Research completed 29 October 2026. Six scoped components have independent internal reviews, with separate implementations and pinned evidence. Earlier receiver, record-compiler, algebra-separation and fault-interface packages remain unchanged.

Result and consequence

This tranche constructs a bridge from the quantum information a receiver must retain to a source code that corrects the errors that retained information can cause. It proves a strict separation from receivers that turn everything into classical records at the required time boundaries, even when those receivers receive arbitrary source encoding and final decoding. The separation survives weak coherent noise at every storage interval under the declared completed-interaction contract.

The resulting design principle has two parts. Count the time boundaries across which quantum information must pass, not just the largest register. Then design the source code and interaction schedule for the errors that each open interaction can spread. A useful entangling-gate example shows that this second part can change correctability while keeping the same bus, core contacts and intended logical operation.

The contribution is a conditional information-processing construction and resource comparison. It does not establish a new circuit-level threshold, an efficient decoder for the extensive-error family, or a practical advantage over conventional fault-tolerant quantum computing. Known QEC, Bell-measurement, quaternary-code and mediated-gate ingredients are credited below. Historical priority is not claimed.

1. From retained noise to source correction

At a declared causal cut, the source-controlled retained frame converts a memory Pauli into a source phase character. For location j, let W_j be the binary subspace of possible characters. The relevant fault family is

𝐸
𝑡
=
⋃
∣
𝐽
∣
≤
𝑡
∑
𝑗
∈
𝐽
𝑊
𝑗
.
E
t
	​

=
∣J∣≤t
⋃
	​

j∈J
∑
	​

W
j
	​

.

This family records which completed interactions can be faulty. A single character may touch many source qubits; small source Hamming weight is not required. A bath visiting additional interfaces cannot be omitted by calling its instantaneous coupling local.

Inserted noise acts on the retained register and its declared bath. Additional direct contact with the source or unprocessed source-imprinted fields must be included in the acquired response interface, or must commute with all remaining source branches.

The reviewed transmutation theorem retains coherent sums and operator-valued coefficients on a persistent bath. After the receiver's actual feedback its Kraus operators have the form

𝐾
𝑦
,
𝛼
=
∑
𝑒
∈
𝐸
𝑡
𝑍
𝑒
⊗
𝐴
𝑒
,
𝑦
,
𝛼
.
K
y,α
	​

=
e∈E
t
	​

∑
	​

Z
e
⊗A
e,y,α
	​

.

The actual receiver record y remains present. This is not a stochastic Pauli replacement. A source code correcting this error space yields a complete corrected instrument equal to the desired logical channel tensored with a code-dependent common instrument. The latter includes the actual source syndrome, field/bath outputs and receiver records. It need not have the old unencoded receiver's probability law: an exact example preserves the logical state while changing that law by total variation 12/25.

For a binary check matrix H that separates E_t, the source code uses X checks with rows of H. Measuring the actual syndrome He and applying the inferred Z phase implements the correction. Arbitrary initial correlations with the logical reference and admitted field/bath are included. A useful target gate also needs a compatible output code and decoder; commutation with the phase errors alone does not supply those controls.

Proof and executable evidence: 
COHERENT_FAULT_TRANSMUTATION.md, with its separate 
review.

2. A coded operation that classical records cannot replace

The fixed test operation has L field pairs arriving as A1,B1,A2,B2,... and 2L source qubits. Each source pair controls the same X and Z words on both field halves. The task is to erase this acquired interaction and preserve unknown encoded data, for arbitrary allowed common field states. A receiver retains one controlled qubit between A_j and B_j, performs the Bell measurement, retains both actual bits and applies source phase feedback.

The classical comparator is strong: any source code, unlimited classical memory and adaptation, joint quantum processing between the designated gaps, and arbitrary final CPTP source decoding using every actual record. It has no extra source-field contact, protected encoder-to-decoder bypass, source wire acting as receiver storage, or uncounted quantum resource crossing a gap.

For logical dimension K and actual quantum cut dimensions D_j, the converse gives

𝐹
𝑒
≤
min
⁡
(
1
,
2
𝐿
∏
𝑗
𝐷
𝑗
𝐾
)
.
F
e
	​

≤min(1,
K
2
L
∏
j
	​

D
j
	​

	​

).

Thus exact preservation requires k <= L + sum_j log2(D_j), as well as the ordinary k <= 2L source-dimension limit. If precisely q gaps allow quantum passage and the others are classical, the exact maximum is L+q logical qubits. One qubit at each selected gap attains it. This is a discrete coherent-transfer budget, not an elapsed-time, energy or query-count bound.

The lower bound uses an allowed independent maximally mixed field, without supplied preparation labels or purification. Merely fixing the field marginal is insufficient: known classical preparation labels can enable complete erasure with local measurements. A supplied known Bell field is another easier task and can make the receiver unnecessary. Avoiding an optional contact is also a stronger alternative when allowed.

The explicit source code uses the ordinary GF(4) [5,3,3] Hamming/MDS construction as four binary X checks. It stores six logical qubits in ten source qubits and corrects one arbitrary completed coherent faulty storage location among five. A classical-at-all-gaps receiver can preserve at most five logical qubits exactly; for a six-qubit input its logical half-diamond error is at least 1/2, even with arbitrary encoding and final decoding. The constructed quantum receiver and source decoder have exact zero logical error under the one-location contract.

This does not hide the interface cost. The emitted encoder uses 44 CNOTs and one SWAP, four fresh plus inputs, and its inverse for decoding. The receiver needs ten field arrivals, twenty source-field controlled-Pauli contacts, five Bell CNOTs, five Bell Hadamards and ten readouts. Source syndrome extraction uses eighteen controlled-X contacts and four recorded bits, with ancilla preparation, readout, reset and holding costs additional. Two field/receiver qubits coexist during Bell processing. Loss and leakage require a specified continuation on the admitted interface; source, contact, analyzer and syndrome faults need separate channels.

The six-qubit optimum is proved for this prescribed Bell receiver and feedback against one unknown memory fault, with arbitrary final source decoding. It is not an optimum over redesigned receivers or extra fault observations.

Proofs: 
CAUSAL_CODE_CAPACITY.md, 
CODED_CAUSAL_ERASURE.md. Both have separate independent reviews.

3. Weak noise at every interval: a normalized full-record theorem

The stronger result removes the hard promise that only t intervals are faulty. Write each completed noise dilation as its declared bath-only baseline plus F_j, with operator norm at most eta_j. The exact fault-subset expansion has paths W_J satisfying ||W_J|| <= product_(j in J) eta_j. No independence of the noise and no Pauli twirl are assumed.

Let Phi be the actual corrected channel, with all actual classical records and admitted common quantum outputs. Define the normalized comparison instrument

𝑅
m
i
x
(
𝜎
)
=
Tr
⁡
𝐿
Φ
(
𝐼
𝐾
/
𝐾
⊗
𝜎
)
.
R
mix
	​

(σ)=Tr
L
	​

Φ(I
K
	​

/K⊗σ).

It is CPTP. Its definition is mathematical; the real protocol does not need to prepare a maximally mixed logical state. The projection Phi -> id_L tensor R_mix is diamond-norm contractive.

The decisive cancellation is at the channel level. Actual syndrome measurement removes every cross term whose two phase characters have different syndromes. If the combined fault-subset degree is below 2t+1, equal syndromes imply equal characters, and that character is corrected. This identity holds record by record with arbitrary noncommuting bath coefficients. Consequently,

1
2
∥
Φ
−
id
⁡
𝐿
⊗
𝑅
m
i
x
∥
⋄
≤
min
⁡
(
1
,
∑
∣
𝐽
∣
+
∣
𝑄
∣
≥
2
𝑡
+
1
∏
𝑗
∈
𝐽
𝜂
𝑗
∏
𝑞
∈
𝑄
𝜂
𝑞
)
.
2
1
	​

∥Φ−id
L
	​

⊗R
mix
	​

∥
⋄
	​

≤min
	​

1,
∣J∣+∣Q∣≥2t+1
∑
	​

j∈J
∏
	​

η
j
	​

q∈Q
∏
	​

η
q
	​

	​

.

The sum is the degree >=2t+1 tail of product_j(1+eta_j z)^2. It has no error-basis coefficient-count penalty. For general exposure spaces, E_p+E_q=E_(p+q), so the same argument applies to overlapping and dense source-error characters. The comparison remains valid on correlated logical/bath/reference inputs.

For L divisible by 16, a binary-check existence argument supplies k >= 5L/4 and t=L/16. If every completed interval satisfies eta_j <= 1/128, then

𝜖
q
u
a
n
t
u
m
≤
1
8
[
(
17
/
16
)
16
8
]
𝐿
/
8
⟶
0
,
𝜖
c
l
a
s
s
i
c
a
l
≥
1
−
2
−
𝐿
/
4
⟶
1.
ϵ
quantum
	​

≤
8
1
	​

[
8
(17/16)
16
	​

]
L/8
⟶0,ϵ
classical
	​

≥1−2
−L/4
⟶1.

This is a robust coded-operation separation. The constant 1/128 is a conservative sufficient interaction norm, not a fault probability or necessary physical limit. Extensive-distance code search and decoding may be expensive; checks can be dense. Source preparation, storage and correction operations are ideal or separately bounded. One controlled receiver qubit does not include a returning quantum bath. The total-one-qubit subclass has no returning bath; the theorem's persistent-bath robustness counts that bath as additional physical memory.

The independent review constructed a different phase code and a two-qubit noncommuting persistent bath. Exact arithmetic checks 5,632 low-degree record/logical/bath matrix-unit blocks and the whole comparison identity. Its useful negative control is essential: keeping the syndrome coherent allows a lower-degree logical cross term. Making the syndrome an actual classical record removes it. A coherently returned purification of that measurement is a different output contract. All comparisons here concern completed calls; new external interventions inside a call require a causal-comb argument.

Proof: 
CHANNEL_ORDER_AND_ROBUST_CAPACITY.md. Review: 
INDEPENDENT_REVIEW.md. The separate 
FAULT_TAIL_AND_REUSE.md gives a more general normalized amplitude-tail bound when this stronger measured-syndrome structure is unavailable.

4. Schedule closure changes a useful operation

A second construction supplies an actual logical CZ rather than only erasure. Two seven-qubit Steane blocks interact with a controlled bus through declared source-controlled X and Z ports. Four contacts on a source pair make a CZ and return the bus identically for every admitted bus state, including initial correlations. Seven local closed loops implement transversal logical CZ.

A dense ordering of the same twenty-eight core contacts also implements logical CZ on these codes. It has the same bus and core contact-time budget. Yet a bus Z fault after the fourteenth contact induces an undetected logical Z in the dense schedule, with actual logical error one on a specified input. In the local-loop schedule that impulse is correctable. More generally, one arbitrary coherent bad open loop, including admitted noise during a finite controlled contact, exposes only its two source labels and is exactly correctable by the actual source syndrome.

This makes the causal exposure family operational: closing an interaction can prevent a small bus fault from becoming a large uncorrectable source fault. The result includes an explicit whole-support port assumption; leakage outside that support has an independently tested failure. Multiple bad loops, source faults and noisy syndrome extraction are not protected by this finite theorem.

The supplied ideal implementation, including block encoding and correction, uses 316 controlled bus contacts, 198 Hadamards, twelve zero-state source ancillas and six bus reset/readout cycles, ending at recovered encoded outputs. Decoding is additional. Fifteen controlled qubits excludes external fault memory. The 28-contact core is not the full operation cost. If direct transversal source-source CZ gates are available, seven such gates are the stronger conventional alternative.

Proof and ledger: 
CLOSED_LOOP_LOGICAL_CZ.md, with its separate 
review.

5. Useful failures, ancestry and actual review

Protecting the entire diagonal error algebra was not a route to an automatic quantum advantage. In the acquired code-preserving setting, a code correcting that whole algebra has a passive character sector carrying the same logical operation. Its active construction can be replaced by a classical causal receiver on that sector. This scoped failure motivated protection of graded exposure families and redesign of open interactions. It is preserved in the coherent-transmutation proof and the architecture comparison; it is not a universal no-go for record-assisted correction.

Other preserved corrections concern supplied preparation labels, returning bath memory, encoded output boundaries, and literal F_j degree versus Pauli weight. A truncated low-order CP map need not be trace-nonincreasing. The generic tail proof now uses an explicit polar normalization and confines reuse to completed-call boundaries. Author and reviewer development failures remain in the relevant history directories.

The work builds on Knill–Laflamme–Viola's general-noise grading, coherent-error distance-order suppression, separable Bell-discrimination bounds, and state-independent mediated phase gates. Current qLDPC coherent-noise results are a strong conventional comparator under their bounded-support, fixed-depth noise and ideal-syndrome premises. Their fresh-environment local-CPTP extension is not imported for an arbitrary persistent returning bath.

Current Astra N1063, its governing completed-access argument and actual curator review were read with their corrections. N1041 informed the architecture control challenge. Missing producer archives were not reconstructed or imported. The accepted quantum-channel undecidability foundations and older bath-representation certificates remain at their prior scope; neither is reopened or repurposed as a device-error premise here.

Component	Author	Independent reviewer	Disposition
Coherent fault transmutation	protected_algebra	classical_capacity	Accepted at declared interfaces
Arbitrary-code causal capacity	classical_capacity	protected_algebra	Accepted with preparation-label clarification
Explicit exposure code and family	root	architecture_challenge	Accepted with returning-memory accounting
Closed-loop logical CZ	architecture_challenge	protected_algebra	Accepted with output/support/resource boundaries
Normalized amplitude tail and reuse	root	classical_capacity	Accepted after recorded grading and scope corrections
Full-record channel order and robust separation	root	architecture_challenge	Accepted, including general exposure spaces

These are scoped internal mathematical and executable reviews, not external peer review or physical validation. Independent implementations are distinct from byte-identical author replays. Finite exact checks support the all-input derivations; no numerical diamond optimizer or device calibration is substituted for a proof assumption.

Reproduction and continuation boundary

REPRODUCE.md gives executable commands and evidence scopes. 
ROOT_AUTHOR_RECEIPT.json, the six review receipts, source read ledgers and 
MANIFEST.json preserve authorship, provenance and byte integrity. No duplicate export is needed.

This construction makes source redundancy and interaction closure available as deliberate substitutes for protecting every retained degree of freedom. A consequential implementation still needs to protect the source/control and actual record-conversion interfaces, with efficient decoding and compatible capture, loss and reset behavior. Those are physical and algorithmic frontiers exposed by the result; the present normalized bound is a sufficient completed-operation comparison, not total workload performance.