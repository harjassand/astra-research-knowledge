# A finite circuit compiler for causal binary projective information

Author: `/root`. 29 October 2026 Australia/Brisbane. Status at creation: analytic construction, with executable checks and independent review recorded separately. This builds on the reviewed finite-algebra theorem and the explicit two-unitary extractor. It is not a claim of hardware advantage or historical priority.

## 1. The operation being compiled

An acquired source dilation has a finite source alphabet and ordered branches

\[
V_x=\prod_{i=1}^n V_i^{x_i},\qquad
V_i=\bigotimes_{t=1}^T U_{i,t},\qquad x_i\in\{0,1\}.
\]

A known source unitary G, diagonal in the source-label basis and including actual ordered-product cocycles, is to be preserved. Batch generators obey the exact bounded-unitary relations

\[
U_{i,t}U_{j,t}=(-1)^{C_{t,ij}}U_{j,t}U_{i,t},\qquad
B_t=\sum_{s\leq t}C_s\pmod2.
\]

Let rank(B_t)=2r_t and assume B_T=0. The original source, all batches and a reference may be arbitrarily correlated. A receiver may control the actual U_{i,t} with a qubit; it has finite qubit gates, preparation and readout. It may retire processed field systems, but every quantum system crossing an arrival cut counts as memory. It does not gain a new source coupling.

The construction below retains **r_t qubits after batch t**, emits only finite actual records, and approximates the complete corrected source/reference/record instrument by G followed by the **same actual receiver on the common input**. No exact Zak transform, sign-observable oracle, central spectral measurement or GKP codeword is supplied.

The reviewed exact lower bound still says r_t qubits are necessary for zero error. This document does not claim that they minimize memory at every nonzero error. The separate two-generator operation-error converse establishes a nonzero-error separation in its stated case.

## 2. Local compilation problem and finite center instrument

At a cut the previous retained generators can be fixed Hermitian Pauli words P_i on r_(t-1) qubits, with all scalar phases in the actual classical record. Combine them with the new batch:

\[
A_i=P_i\otimes U_{i,t},\qquad A_iA_j=(-1)^{B_{t,ij}}A_jA_i.
\]

Fix one cut and write B=B_t, r=r_t. Every A_i^2 commutes with every A_j. Perform the actual finite sine phase instrument of `extractor_circuit/FINITE_QUBIT_EXTRACTOR.md` separately on all A_i^2. For M=2^m it uses weights

\[
w_k=\sqrt{2/M}\sin((k+1)\pi/M),\quad 0\leq k\leq M-2,
\quad w_{M-1}=0.
\]

All n measured indices y=(j_1,...,j_n) are retained. Set phi_i=2pi j_i/M, and let K_y be the product of the actual commuting phase Kraus operators. Define, for this actual outcome,

\[
\widehat A_i(y)=e^{-i\phi_i/2}A_i,\quad C_i(y)=\widehat A_i(y)^2,
\quad r_M=2\sin(\pi/(2M)).
\]

The exact phase identity gives

\[
\sum_y K_y^*(C_i-I)^*(C_i-I)K_y=r_M^2 I.                 \tag{1}
\]

No condition on the unknown spectrum or a favorable estimation event is imposed.

### A comparison lemma, not an additional control

For the proof alone choose the bounded Borel square root

\[
R_i(y)=\exp\{\tfrac i2\operatorname{Arg} C_i(y)\},\qquad
J_i(y)=\widehat A_i(y)R_i(y)^*,
\]

where Arg takes values in [-pi,pi). These are measurable central functions. Then J_i are Hermitian involutions, with exactly the same pairwise signs B. For every unit-circle value c,

\[
|1-\sqrt c|\leq |1-c|/\sqrt2.
\]

Consequently, for the coherent version F of the actual phase instrument,

\[
\|(\widehat A_i-J_i)F\|\leq e_M:=r_M/\sqrt2.           \tag{2}
\]

The notation in (2) means the record-controlled operator in the corresponding direct sum. This inequality includes the branch cut. J_i is never measured or implemented. Approximation of a fixed discontinuous sign function in unrestricted operator norm is neither asserted nor required. The error is weighted by the **actual finite record instrument**, and both endpoints of the later encoder comparison are charged.

Equation (2) remains valid after any sequence of controlled words in the A_i, J_i and gates on the other finite qubits, with the phase records only used as controls and never coherently mixed after F. All these operations commute with the record-dependent positive central error operators. Inserting a control projector can only decrease the squared norm. This is the actual circuit's gate class, and it justifies the telescoping below even with entangled references and adaptive phase frames. It does not license an arbitrary coherent rewrite of the phase record.

## 3. Symplectic word reduction is finite and constructive

Find an invertible binary matrix R with

\[
R^TBR=\bigoplus_{k=1}^r\begin{pmatrix}0&1\\1&0\end{pmatrix}
\oplus 0_{n-2r}.
\]

Symplectic elimination over F_2 constructs R: select a nonzero pairing u,v, replace each remaining w by w+B(w,v)u+B(w,u)v, then repeat on the orthogonal remainder. Let h_j be the Hamming weight of column j and L=sum_j h_j<=n^2.

For column j define q_j=sum_(i<k) R_ij R_kj B_ik modulo 2 and the ordered words

\[
H_j(J)=i^{q_j}\prod_iJ_i^{R_{ij}},\qquad
H_j(\widehat A)=i^{q_j}\prod_i\widehat A_i^{R_{ij}}.    \tag{3}
\]

The H_j(J) are Hermitian involutions. Each successive pair anticommutes; different pairs and the final n-2r radical generators commute. The actual H_j(widehat A) have the same signs, but need not be involutions. All the phases in (3) are computable finite constants.

The inverse matrix R^-1 reconstructs each J_i as a product of canonical H_j(J), with a known power of i. Obtain that phase by multiplying the finite binary words in their fixed order; it must not be discarded. This also constructs the output Pauli words below.

## 4. The actual circuit

For each canonical pair use the two-query isometry

\[
W(A,B)=|0\rangle(I+B)/2+|1\rangle A(I-B)/2,
\]

with A=H_(2k-1)(widehat A), B=H_(2k)(widehat A). It is the circuit H, controlled-B, H, controlled-A on a fresh output qubit, and is exactly isometric for **any** unitary A,B. Retain this qubit.

For each radical H_j(widehat A), prepare one qubit, apply H, controlled-H_j, H and measure in the computational basis. This has isometry

\[
L(H_j)=|0\rangle(I+H_j)/2+|1\rangle(I-H_j)/2.
\]

Retain the actual binary outcome and reset or replace this temporary qubit. The radical outcomes are not hidden finer measurements. Trace the remaining field and previous memory only after all of these steps.

Let T_A(y) denote the isometry before radical records are dephased, and T_J(y) the comparison-only circuit with each widehat A replaced by J. Every canonical word appears in one controlled query; their implementation uses **L controlled original generators**, with known control phases. Elementary circuit telescoping and (2) give

\[
\|(T_A-T_J)F\|\leq L e_M.                              \tag{4}
\]

For exact involutions the pair circuit transfers A to X and B to Z on its output qubit. The radical circuit transfers H_j to Z on its readout qubit. Different canonical generators commute, so all these transfers coexist in the same circuit. Thus

\[
T_JJ_i=\Gamma_iT_J,                                   \tag{5}
\]

where Gamma_i is the fixed finite Pauli word obtained by the inverse word calculation in Section 3. On radical qubits it uses only Z, so after measurement it is a known scalar sign times a Hermitian Pauli word on the r retained qubits. These r-qubit words can be chosen once per B; only the scalar sign and center phase depend on actual records.

## 5. Same-receiver intertwining, with both endpoint errors

For the actual encoder E=T_A F, subtract its response to A_i from the corresponding output Pauli/record-phase response. After removing e^(i phi_i/2), insert (5):

\[
T_A\widehat A_i-\Gamma_iT_A
=(T_A-T_J)\widehat A_i+T_J(\widehat A_i-J_i)
+\Gamma_i(T_J-T_A).
\]

The first term in (4) is still bounded by L e_M after widehat A_i, since it commutes with the central errors. Therefore

\[
\|EA_i-\widetilde P_iE\|\leq(2L+1)e_M,\qquad
\widetilde P_i=e^{i\phi_i/2}\Gamma_i.                    \tag{6}
\]

The two copies of L in (6) are essential: one changes the source-acted endpoint, the other returns the common-input endpoint to the actual receiver. Output-state closeness to T_J alone would not give the required contract.

For an ordered source branch with at most w active generators, telescoping the unitary words gives

\[
\|EV_x-\widetilde P_xE\|
\leq w(2L+1)r_M/\sqrt2.                                \tag{7}
\]

For a controlled superposition of source labels take the maximum w, not the number of labels: the source-label blocks are orthogonal. Copying/dephasing all actual records, applying their source phase feedback and tracing retired systems are common channels. Hence (7) bounds the half trace distance of the complete outputs for arbitrary initial correlations and references.

## 6. Causal composition and resource ledger

At the next cut use the fixed retained Pauli words from the previous cut and the next actual U_i,t. The construction applies with B_(t+1). Its scalar phases are appended to the actual history. The bounds are uniform over every pre-cut history and every admitted input, with the current phase outcomes summed in the actual instrument. They are not uniform after conditioning on an arbitrarily bad current phase-estimation outcome. The complete stage errors therefore telescope. At the final cut B_T=0 all generators have become actual record phases, which source feedback removes. The complete-instrument error obeys

\[
\epsilon_{\rm complete}\leq
\min\left\{1,\sum_{t=1}^T w_t(2L_t+1)
                 \frac{2\sin(\pi/(2M_t))}{\sqrt2}\right\}.\tag{8}
\]

For binary labels w_t<=n, L_t<=n^2. Thus a sufficient finite choice with sum_t n(2n^2+1)pi/(sqrt2 M_t)<=epsilon exists for every positive epsilon. This is a conservative compilation bound; the specialized two-unitary proof is much tighter and should be used for that operation.

| Per-cut resource | Explicit allowance |
|---|---|
| Quantum memory after extraction | r_t=rank(B_t)/2 qubits |
| Actual phase records | n log2(M_t) bits |
| Actual radical records | n-2r_t bits |
| Actual controlled U_i,t calls | At most 2n(M_t-1)+L_t |
| Center preparations / QFTs | n deterministic sine preparations / 2n QFTs |
| Temporary finite qubits | Conservatively m_t+r_(t-1)+r_t+1 |
| Source feedback | Recorded diagonal phases, after the declared source interaction |

The center query count uses A_i^2=I on the old Pauli factor tensor U_i,t^2, so no old-memory query is needed for those squared powers. Each remaining controlled A_i combines a controlled old Pauli word with one controlled U_i,t. Pauli synthesis, qubit connectivity, source storage and feedback latency are additional costs. The temporary width bound is deliberately conservative; known streaming sine-phase algorithms may reduce it, without changing the between-arrival memory theorem.

Register reset uses actual retained readout bits and ideal conditional X gates, or fresh registers. This does not erase entropy or pay for preparation/readout faults. Each arriving field must remain captured during its phase and extraction processing. Buffering when arrivals overlap increases the actual retained quantum resource. Retired field energy, field loss, memory decoherence, powered-query duration and finite control accuracy remain real costs. In a bosonic implementation the prior number-moment/control machinery is needed for physical model and calibration errors; arbitrary-energy small-parameter continuity is not assumed.

An implemented receiver discrepancy eta_R costs up to 2 eta_R when both the actual operation and its common-input baseline use that implemented receiver. Source-coupling and source-feedback errors are separate. Approximation (8), solver diagnostics, physical noise and total workload error remain distinct.

## 7. What this adds, and the strongest alternatives

The exact algebra theorem supplied a normal-form extractor as an operation. This compiler constructs that role, to any positive complete-operation accuracy, from controlled actual source unitaries and finite ancillary gates/readout. It applies to every binary projective rank walk at once, including increases, decreases and final retirement of memory; it is not a collection of separately optimal incompatible cut encodings.

Conventional symplectic reduction, Pauli/SWAP extraction and sine phase estimation are the ingredients. The new bridge established here is their finite actual-record, all-input, same-receiver causal operation contract. No claim is made to invent finite-dimensional Pauli subalgebras or optimal phase states. Recent oscillator Pauli constructions using discontinuous bounded functional calculus are relevant mathematical ancestry; this circuit does not assume physical access to those discontinuous functions. They enter only a comparison proof and both endpoint differences are paid.

A Gaussian receiver that retains a suitable oscillator and performs the final commuting quadrature measurement can be substantially simpler when that memory is available. A prepared known vacuum can also allow stronger record-conditioned recovery than the all-input contract. Neither is weakened for this comparison. The compiler establishes how to replace continuous quantum information by finite coherent factors and finite records under explicit stronger controlled-unitary access. It does not establish that this replacement is cheaper, faster or more fault tolerant in a particular device.

The exact binary relation is a premise here. `robust_extractor/NEAR_ANTICOMMUTING_EXTRACTOR.md` separately constructs an imperfect-relation two-generator bridge using the actual operators. General near-projective compilation with uniform costs is not established by (8).

## 8. Evidence and ordinary failures preserved

`projective_compiler_checks.py/json` checks binary symplectic reduction, all cocycle signs, exact multigenerator isometry/Pauli transfer, and finite-phase whole-encoder comparisons. Exact rational checks and floating diagnostics are reported separately. Finite matrices test the algebra and implementation; they do not certify the infinite-dimensional analytic theorem by truncation.

The first possible shortcut—replacing the actual encoder by an ideal involution extractor and paying only its source-acted error—fails to control the common-input baseline. Equation (6) keeps the missing endpoint. A second shortcut—treating normalized unitaries as exact involutions after finite phase estimation—is false. The actual circuit stays isometric, while (1)-(2) explicitly pay the squared-unitary defect. No hidden exact phase record is used.

### Primary reading and dependency scope

- Berry–Wiseman, [quant-ph/0009117](https://arxiv.org/abs/quant-ph/0009117), canonical phase measurement and sine-state equations: ancestry of the finite phase instrument, not a new optimum claimed here.
- Babbush et al., [1805.03662](https://arxiv.org/abs/1805.03662), Section II B, equations (17)-(20): efficient deterministic sine preparation already exists. Root read this construction; its different window is not substituted into (1).
- Najafi–Costa–Berry, [2303.12503](https://arxiv.org/abs/2303.12503), Sections II and IV: two-control streaming phase estimation is a strong temporary-workspace alternative. Root read the relevant preparation recursion/circuit; equivalence to the exact zero-edge instrument here has not been certified and is not a premise.
- Sorella, [2610.23264v2](https://arxiv.org/abs/2610.23264), Sections 1-4: exact oscillator Pauli algebras from anticommuting displacements and discontinuous bounded functional calculus. Root successfully read these full-source passages after a contributor's retrieval failed. Only the algebraic ancestry is used; the singlet-overlap calculation and hardware synthesis are not imported.

The exact finite-algebra lower bound, explicit finite phase/extraction identities and their actual internal reviews are preserved in the adjacent packages. New compiler evidence is scoped separately. Reviewer clarifications are incorporated: G is diagonal in the source-label basis; stage uniformity means a pre-cut history with the current actual phase outcomes summed; subsequent gates never coherently mix the phase records. No arbitrarily postselected phase branch inherits the average bound.
