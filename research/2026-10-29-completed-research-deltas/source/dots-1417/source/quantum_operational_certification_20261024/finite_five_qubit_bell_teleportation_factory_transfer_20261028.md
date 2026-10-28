# An actual finite five-qubit Bell-resource transfer circuit

28 October 2026. Author construction/check; contributor evidence for the separately drafted finite two-way factory, **not an independent receipt of that factory**. The stabilizer code, recurrence and teleportation are established ingredients. This note supplies explicit gates, orientations, recovery records and a complete-channel composition. It makes no efficient-hashing assumption and no new quantum advantage claim.

## 1. Precisely scoped input and conclusion

Condition on a fixed allowed common-frame parameter and pre-factory history. Suppose the supplied resource pairs are independent with state

    sigma_q = sum_(e in {I,X,Y,Z}) q_e (I tensor e) Phi_2 (I tensor e),
    p = 1-q_I.

The pairs need not be isotropic. They are independent of the future input conditional on this history; that input may be arbitrarily entangled with untouched systems. No purification of the resource or discarded private twirl keys is an exported output. The sender and receiver have trusted known local controls and charged classical communication. The underlying factory must separately pay for every pair, including its discarded/failed attempts.

The circuit below consumes five pairs to transfer one input qubit, with induced Pauli error probability

    p' <= 1-(1-p)^5-5p(1-p)^4 <= 10p^2.              (1)

It is a deterministic LOCC circuit, not a postselected logical channel. Encoding half of a locally prepared Bell pair instead produces a shared pair with the same logical Pauli law. Arbitrary XYZ bias is allowed. The precise instrument including all teleportation and syndrome records is given in Section 5.

The prior received stabilizer enumeration is `bootstrap_five_qubit_pauli_independent_receipt_20261027.md` (SHA256 `00049ed8a3b98e62878540d64ab14bfafee0136ff0633ed36eed810641b4b648`). The present construction independently gives an actual circuit implementing its channel, rather than invoking a coding/distillation equivalence by name. The standard five-qubit code was introduced by [Laflamme et al.](https://arxiv.org/abs/quant-ph/9602019); the operational calculation below is self-contained.

## 2. Explicit encoder, decoder and syndrome table

Number the five qubits 0,1,2,3,4; qubit 4 is the logical input and qubits 0–3 start in zero. Define the stabilizer and logical operators

    g1=XZZXI, g2=IXZZX, g3=XIXZZ, g4=ZXIXZ,
    X_L=XXXXX, Z_L=ZZZZZ.

Here is the chronological gate list for a unitary **decoder** Q. `CX(c,t)` denotes controlled-X with control c; `SD` is S-dagger. Gates on a line are still applied left to right.

    H(0), H(3), CX(1,0), CX(2,0), CX(3,0),
    H(1), H(3), H(4), CX(2,1), CX(3,1), CX(4,1),
    SD(2), H(2), SD(3), H(3), H(4), CX(3,2), CX(4,2),
    SD(4), H(4), CX(4,3), H(4), SD(4),
    CZ(4,0), CZ(4,1), CZ(4,2), CZ(4,3).

There are 27 known Clifford gates. The **encoder** is U=Q-dagger: reverse the list and replace each SD with S. The other listed gates are self-inverse. Exact signed-Pauli conjugation gives

    Q g1 Q† = ZIIII,       Q g2 Q† = IZIII,
    Q g3 Q† = ZIZII,       Q g4 Q† = IZIZI,
    Q X_L Q† = IIIIX,      Q Z_L Q† = IIIIZ.            (2)

Thus U(|0000> tensor |psi>) is a codeword with logical state |psi>. For every physical Pauli E, Clifford conjugation writes

    Q E Q† = phase(E) (A_0 tensor ... tensor A_3 tensor L_E).

After Q, measuring the first four qubits in Z gives the deterministic string s(E), whose i-th bit is one exactly when A_i is X or Y. Their phases multiply the entire logical branch by a scalar; the remaining qubit is L_E|psi>. The following recovery table lists the unique weight-at-most-one representative and the Pauli to apply to the remaining logical qubit:

| Measured s | Representative | Logical correction |
|---|---|---|
|0000|IIIII|I|
|0001|XIIII|X|
|0010|IIZII|Z|
|0011|IIIIX|X|
|0100|IZIII|Z|
|0101|IIIIZ|Z|
|0110|IIIIY|Y|
|0111|IIIXI|X|
|1000|ZIIII|Z|
|1001|YIIII|Y|
|1010|IXIII|X|
|1011|IIIZI|Z|
|1100|IIIYI|Y|
|1101|IIYII|Y|
|1110|IYIII|Y|
|1111|IIXII|X|

These are the measured decoder-coordinate syndromes, not an unlabelled reuse of the four original-generator syndromes: (2) specifies their relation. Let c_s be the final column. For every E, the residual logical Pauli is c_(s(E)) L_E, modulo its irrelevant phase. In particular every error of weight zero or one has residual I. No inference about correction of arbitrary weight-two errors is needed for (1).

The check enumerates all 1024 physical Pauli patterns using exact signed-Pauli algebra. The numbers with residual I by physical weight 0,...,5 are (1,15,0,60,135,45). Each of the other three logical classes has counts (0,0,30,70,90,66). A separate 32-by-32 matrix calculation checks the displayed circuit on both logical basis vectors for every pattern.

## 3. Actual Bell teleportation, including outcome law

Let C be the carrier, and A,B the sender/receiver resource halves. The sender applies CX(C,A), then H(C), measures C,A in Z to obtain a,b, and sends these two bits. The receiver applies Z^a X^b. For resource error e, the corrected C-to-B Kraus matrix is

    K_(a,b,e) = phase(a,b,e) e/2.                      (3)

This follows by contracting the resource vector (I tensor e)|Phi> against the Bell measurement vector. Equivalently, if the measurement Bell vector is (I tensor P_m)|Phi>, the uncorrected matrix is e P_m* /2 and correction P_m^T conjugates e to itself up to phase. In particular K†K=I/4. All four outcomes are uniform, independent of both e and the carrier input, including its reference. Equation (3) is an operator identity, not just a computational-basis probability check.

For five disjoint resources, the complete corrected teleportation instrument is the product of (3), even on an entangled encoded carrier. Consequently the sender can:

1. append four zero ancillas and apply U to the actual input qubit;
2. teleport all five physical carriers using five distinct resource pairs and ten classical bits;
3. let the receiver apply Q, measure qubits 0–3, and apply c_s to qubit 4.

The input qubit is consumed, not bypassed. No source call occurs during this phase; all source calls were spent making the resource pairs. The physical error pattern E has probability product_i q_(E_i). Its corrected logical class is the one in Section 2. This proves the exact Pauli channel and (1), since two or more physical errors imply that at least one of the ten pairs of locations both erred.

## 4. Optional direct bilateral realization: orientation is fixed

For completeness, the same one-level conversion can be done directly on five Bell pairs without preparing/teleporting a separate codeword. Alice applies **Q*** to her five halves; Bob applies **Q** to his. This is conjugation, not the same orientation on both sides and not Q-dagger on Bob. The identity

    (Q* tensor Q)|Phi_32> = |Phi_32>

transforms a Bob-side physical error E into Q E Q† on Bob's side. Since Q is Clifford, the state is a product of five Pauli-labelled Bell states. Both parties measure their first four halves in Z. Alice's four-bit string a is uniform; Bob's string is b=a XOR s(E). Alice sends a, Bob computes s and applies c_s to his retained logical half. The retained pair has residual logical label c_s L_E, exactly as in Section 3. The measured ancillary phases have no effect on the retained pair. Retaining a,b gives an input-free classical record; discarding either does not change the pair law.

This direct circuit consumes five pairs and sends four syndrome bits from Alice to Bob; bidirectional communication is not needed for this final code step. The earlier recurrence does use comparison/retention communication. The code-teleportation route is the primary reference-transfer implementation because it makes arbitrary untouched input references explicit.

## 5. Full classical-record and reference contract

Let t include the teleport outcomes and measured code syndromes. For a fixed input-independent resource law, define w_(t,l) as the probability of t and corrected logical label l, with pi_t=sum_l w_(t,l). The actual complete instrument is

    Gamma(rho)=sum_t |t><t| tensor sum_l w_(t,l) l rho l,

and compare it with the ideal identity instrument having **the same actual record law**,

    Gamma_id(rho)=sum_t pi_t |t><t| tensor rho.

The record law is independent of the logical input. It need not be independent of the residual error, and no small conditional error for every revealed syndrome is asserted. Nevertheless

    ||Gamma-Gamma_id||_diamond = 2 sum_(t,l!=I) w_(t,l)
                             = 2p'.                  (4)

For the upper bound, use the triangle inequality within each orthogonal classical block and ||Ad_l-id||_diamond<=2. A Bell input attains the bound: the erroneous Bell states are orthogonal to the identity Bell state in each classical block. This proves (4) for arbitrary outside references and also shows that discarding these records cannot worsen the error. It is stronger than a marginal Bell-fidelity statement, but it is **not** an assertion of linear-in-p decoupling from an exported purification of the resources. Such an environment or discarded twirl key is outside this claim.

At each concatenation level, disjoint groups are independent conditional on the fixed latent common frame/history; the next-level Pauli bias can change. Hence, for p_0<=1/40,

    p_(j+1)<=10 p_j^2,
    p_L <= (10p_0)^(2^L)/10 <= 4^(-2^L)/10.           (5)

The full inner syndrome trees are still input-independent classical records and the residual Pauli law remains exact. Equation (4) applies with p_L. For M transfers using disjoint resource blocks, the complete joint-output discrepancy is at most 2M p_L, including entangled inputs, untouched systems, and any later operations by contractivity. A causal hybrid gives the same bound if later permitted inputs are selected using previous classical records. One must average the fixed latent history **after** this complete bound; a product of averaged channels is generally the wrong law.

An upstream bad-history/shortage event of probability beta costs at most 2beta for the total CPTP replacement-on-abort protocol, not M times. A single whole-process finite implementation discrepancy nu is then added. No normalized accepted-branch claim follows without its own acceptance bound.

## 6. Verification of the finite-factory recurrence interface

This section checks Sections 3–5 of the parent's candidate `two_way_learned_reference_factory_20261028/FINITE_TWO_WAY_LEARNED_REFERENCE_FACTORY.md` as read at SHA256 `af2a155f109c33987f13f87511a5758315e605643f1bdf1938686a731283e1c8`. It is contributor verification; the warm learner, frame compiler and entire factory cap are not independently received here.

Write a Bell label as (x,z), corresponding to X^x Z^z modulo phase. Bilateral CX from the first pair to the second sends

    (x1,z1),(x2,z2) -> (x1,z1+z2),(x1+x2,z2).

Measuring the second pair's two halves gives equal bits iff x1=x2. Conditional on a fixed label pair the two allowed fine bit strings are equiprobable. For isotropic input with weights F,(1-F)/3,(1-F)/3,(1-F)/3, direct summation gives

    P(F)=(8F^2-4F+5)/9,
    R(F)=(10F^2-2F+1)/(8F^2-4F+5).                  (6)

On F>=1/2, P(F)>=5/9. The retained state is not generally isotropic before a NEW independent bilateral twirl; that twirl preserves its Bell fraction R(F). Its key is then discarded.

For a fixed F, each attempt is a tensor instrument with an input-free success probability P and the SAME normalized success state sigma_(R(F)). Consequently, conditional on any coarse pass/fail pattern, all successful outputs are independent copies of that state. Taking the first fixed N successes therefore retains its N-fold tensor power, independently of the coarse pattern. This remains true conditional on a previous coarse history by induction, because each previous stage already supplies a tensor power. Conditioning on private twirl keys instead is not allowed in this isotropic reference law.

The exact circuit check covers all 16 input Bell-label pairs and every fine measurement outcome. It also checks (6) at six rational fidelities, the first-two-success product law for every nonzero four-attempt coarse pattern at those fidelities, and the exact rational inequality R^9(3/4)>39/40 (value approximately 0.981485375906). The displayed product law is a tensor-factorization proof; the finite patterns are diagnostics, not a proof for arbitrary reservoir size. This is the established recurrence of [Bennett–DiVincenzo–Smolin–Wootters](https://arxiv.org/pdf/quant-ph/9604024), here checked in the actual Phi-label convention.

## 7. Deterministic local cost and finite implementation

A level-L transfer consumes exactly 5^L pre-existing noisy resource pairs and sends 2*5^L teleport bits. Its encoder and receiver decoder each use the 27-gate circuit at (5^L-1)/4 internal nodes, with four syndrome measurements and a known one-qubit Pauli correction per decoder node. If Pauli gates X,Z are the primitives, at most two gates implement each correction. The sender can create a new high-quality remote pair by starting with one additional local H/CX Bell preparation and applying the transfer to its second half.

All gates are fixed finite Clifford controls; no unknown inverse, programmable reference, uncounted protected quantum link, or arbitrary efficient hashing decoder appears. Memory and classical messages are real resources. The code does not correct unmodelled local-control/storage faults by squaring them into p: these are paid in the whole-process discrepancy nu. Given a deterministic count G_tot of local quantum/classical instrument operations, allocate each implementation unhalved diamond error at most nu/G_tot and use a telescoping channel bound, including records. The resources' creation and any finite bilateral-twirl sampler are separately included in the parent's upstream cap. A cap-exhaustion branch produces fixed replacements; it does not request an unbounded retry.

## Evidence and status

The companion `_check.py`, `_check.json`, and `_author_replay.log` give the synthesized 27-gate list; exact signed-Pauli and syndrome table; 1024 error-pattern checks; 16 teleport Kraus cases; 16 recurrence label pairs; 165 rational biased Pauli laws; three exact biased concatenation levels; and three kept-syndrome cq trace-norm checks. The dense-matrix residual is numerical evidence supplementing, not replacing, exact Pauli algebra and the operator proofs. This is a proved ideal finite circuit with a paid finite-control interface, not hardware execution or an independently received full factory.
