# Same memory, same contacts, different protected logical operation

Author: `producer-workspace/architecture_challenge`, 29 October 2026 Australia/Brisbane.
Status: explicit construction and conventional comparator, with executed exact checks. Independent review is separate. No historical-priority or device-performance claim.

## 1. The matched question

Two schedules below have the same fourteen source qubits, one reusable bus qubit, the same multiset of twenty-eight controlled-Pauli contacts, the same ideal logical CZ, and the same source code and recovery. One corrects an arbitrary coherent fault process confined to one four-contact loop; the other admits a single bus Pauli fault that is an undetectable logical Z.

The decisive resource is which source information remains exposed to a live bus fault before a causal interaction closes. Maximum retained dimension and contact count alone do not determine that resource.

The mechanism is built from conventional qudit-bus commutator gates and Steane-code transversality. The purpose is to supply a strong actual-operation construction and a matched challenge for the new receiver fault calculus, not to rename those established ingredients as novel.

## 2. Supplied control interface and physical loop

The bus M is a true two-dimensional system, or a supplied representation on which the following exact Pauli identities hold on the entire admitted support. Each source qubit can control X_M or Z_M, and source Z labels are unchanged by the contact. No direct source-source gate is needed. With temporal order read left to right, the four contacts

\[
C_a(X_M),\ C_b(Z_M),\ C_a(X_M),\ C_b(Z_M)
\tag{1}
\]

have total unitary CZ_ab tensor I_M. On source basis bits a,b, the chronological product is Z^b X^a Z^b X^a = (-1)^(ab) I. Therefore the loop works on arbitrary initial bus states, including correlations with the source, external memory and a reference. Initialization or reset of M is not needed for this identity.

A compatible ideal Hamiltonian for one duration-tau contact is

\[
H_{j,P}=\frac{\pi\hbar}{2\tau}|1\rangle\langle1|_j\otimes(I-P_M),
\qquad P\in\{X,Z\}.
\tag{2}
\]

Its exponential is the declared controlled P, and its operator norm is pi hbar/tau. Equation (2) identifies the required coupling; it does not establish available bandwidth, capture, calibration, routing or leakage control in a device. These repeated source-bus contacts are a changed architecture, not extra source coupling silently granted to the earlier downstream-only receiver.

## 3. Code and useful target

Let H be the binary 3 by 7 matrix with columns 1,...,7 in binary, and C = rowspace H. Thus C has eight words, all weights zero or four, and is self-orthogonal. Put j=1111111. The Steane codewords are

\[
|a_L\rangle=2^{-3/2}\sum_{c\in C}|c+a j\rangle,\qquad a\in\{0,1\}.
\tag{3}
\]

The code is stabilized by X^h and Z^h for the three rows h of H. Each single physical Z has a different nonzero X-syndrome. Z^j is logical Z.

Use two blocks A and B. There are two different physical diagonal gates with the same logical action:

\[
G_{\rm local}=\prod_{i=1}^7CZ_{A_iB_i},
\qquad
G_{\rm dense}=\prod_{i,k=1}^7CZ_{A_iB_k}.
\tag{4}
\]

On computational support words x=c+a j and y=d+b j, self-orthogonality and even row weights give x dot y = ab mod 2. Also parity(x)=a and parity(y)=b. Consequently both gates multiply |a_L b_L> by (-1)^(ab): each is logical CZ.

### Local closed schedule

Perform (1) for (A_1,B_1), then for (A_2,B_2), through (A_7,B_7). This uses 28 contacts and implements G_local tensor I_M.

### Dense open schedule

Perform all seven C_Ai(X), then all seven C_Bi(Z), then all seven C_Ai(X), then all seven C_Bi(Z). The bus sees X controlled by the A parity and Z controlled by the B parity. The same commutator identity gives G_dense tensor I_M, again with 28 contacts.

The schedules use the same contact multiset. Under equal-duration, uniformly available ports they have the same interaction duration 28 tau and the same sum of contact norm-actions 28 pi hbar. Different spatial routing, simultaneous access, idle noise and pulse-shape costs can change a physical comparison; none is inferred from the count.

## 4. Arbitrary coherent one-loop faults in the local schedule

Allow arbitrary bus/external-memory evolution between completed loops, including correlations and non-Markovian memory. Each ideal closed loop is source CZ tensor identity on that memory, so these inter-loop memory operations cannot spread an existing error to later source pairs.

Inside at most one loop, allow an arbitrary bus-memory noise process, including many insertions or noise during finite contacts. The essential premise is that it acts on the bus/external memory and that the source contacts remain diagonal in their two source labels. The entire faulty loop has a controlled dilation

\[
\sum_{a,b}|ab\rangle\langle ab|\otimes D_{ab}
\]

with D_ab operators into the actual environment/output/record space. Remove the ideal CZ phase and expand the four source-label blocks by their binary Fourier transform. The result is

\[
\sum_{u,v\in\{0,1\}}Z_{A_i}^uZ_{B_i}^v\otimes A_{uv}.
\tag{5}
\]

This is an operator expansion, not a stochastic Pauli replacement. Coherent cross terms remain until the actual source syndrome is acquired. Arbitrary records emitted by the faulty process stay in the output environment; their fine outcomes are not replaced by latent fault labels.

Across an unknown faulty loop, the permitted source error space is

\[
\mathcal E_1=\operatorname{span}\{I,Z_{A_i},Z_{B_i},Z_{A_i}Z_{B_i}:1\leq i\leq7\}.
\tag{6}
\]

It has 22 distinct Pauli characters. The six measured X-stabilizer syndrome bits are respectively (i,0), (0,i), or (i,i), with three-bit i, and zero for I. These 22 syndromes are distinct. The usual correction applies Z at the syndrome's indicated position in each block.

For each actual instrument branch r and source syndrome s, the recovered Kraus operator on the logical code is exactly

\[
CZ_L\otimes A_{r,s}.
\tag{7}
\]

Equation (7) follows term by term from (5)-(6); terms with the same source character are combined coherently before syndrome measurement. Summing the actual fine records and syndrome outcomes is trace preserving, hence the operators A_r,s form a common instrument on the incoming bus/external memory. Therefore the complete logical/source/reference/actual-record output is logical CZ tensor this common instrument, including initially correlated logical data and memory. The logical-operation error is exactly zero for this contract, not just a sufficient low-order probability bound.

The argument also covers a coherent superposition of allowed one-loop fault locations when the whole process admits the error-space factorization (6). A probabilistic statement that each loop has a small marginal error does not imply that global support condition. Arbitrarily many bad loops are not corrected by it. Arbitrary memory-only noise between truly closed loops is harmless to the logical data, but a memory leakage state on which future controlled Pauli identities fail is outside the premise.

## 5. One fault defeats the dense schedule

Insert Z_M after the first fourteen dense contacts, between the first all-X/all-Z half and its reversal. Commuting that Z through the remaining all-X contacts adds Z^j on block A; commuting through all-Z adds nothing. The final operation is

\[
Z_A^j G_{\rm dense}\otimes Z_M
=Z_{L,A}CZ_L\otimes Z_M
\tag{8}
\]

on the encoded source. All six source X syndromes vanish because H j=0. The error is logical Z and cannot be corrected by the declared syndrome recovery. On logical |+>_A |0>_B it produces an orthogonal logical output: actual logical half-diamond error is exactly one for this deterministic fault.

The identical Z_M impulse after the fourteenth contact of the local schedule falls in its fourth loop. It adds only Z_A4, which its actual syndrome identifies and corrects. Both schedules use one bus and the same contact count. No noise-rate optimization or asymptotic approximation enters this comparison.

Two bad local loops can fail: Z_A1 and Z_A2 have syndrome 3, so the declared recovery applies Z_A3, leaving weight-three Z_A1 Z_A2 Z_A3, a logical Z. Thus the safe schedule does not imply unrestricted immunity. Its causal exposure distance is three for undetected logical Z patterns; the dense schedule has distance one. The fault count is a count of faulty open loops, not source Hamming weight or a probability.

## 6. Family and scope

The argument extends to any odd-length binary CSS [[n,1,d]] code built from a self-orthogonal even code C with C^perp = C + span{j}, j=all ones. Both pairwise transversal CZ and the all-to-all parity CZ give the same logical CZ. The local closed schedule uses 4n contacts and corrects arbitrary coherent faults in at most floor((d-1)/2) open loops, provided the induced source noise is phase-only as above. The dense schedule has a single bus fault producing logical Z. Concatenated Steane codes provide explicit such families; this is an existence/scaling statement, not a resource optimum.

The theorem does not certify errors in data preparation, syndrome extraction, data storage or source controls that flip labels; does not protect a leaked/lost bus with undefined later ports; and does not assign a total workload error. A bounded higher-order process tail can be added to (7) using an appropriate full-process norm. A stochastic probability of two or more bad loops and a coherent amplitude tail are different inputs to that calculation.

## 7. Essential acquisition, reuse and comparisons

- Two encoded data qubits occupy fourteen physical source qubits. A finite Clifford preparation is supplied by Gaussian elimination in `architecture_checks.py/json`; per block it uses six initially zero source ancillas, three Hadamards and 33 CNOT-equivalent gates (including the declared SWAP synthesis). It is not a fault-tolerant state-preparation certificate. Every source-source CNOT can be implemented with H on its target, the same four-contact bus CZ loop, then H on its target. Thus no extra direct source-source port is needed for this ideal netlist.
- Main interaction: one bus qubit, arbitrary admitted initial state, 28 controlled-Pauli contacts; no bus measurement or reset required between exact closed loops. Arbitrary bus reuse is justified only at those factorized boundaries.
- Phase recovery: six weight-four X checks. A direct ideal circuit uses six fresh |+> meter preparations, 24 meter-to-data CNOTs, six X readouts, and at most two classically controlled data Z corrections. The cheapest supplied-port implementation resets the main bus after the core and uses it as this meter: CNOT from bus to data equals H_data, native CZ_data,bus, H_data. This needs 24 additional controlled-bus contacts and six qualified reset/preparation/readout cycles, retaining all six actual bits. Reset is an acquired replacement/preparation independent of the current source and external memory; it is not inferred from a favorable measurement. Discarding the old bus after the core preserves the correctability proof. Fault-tolerant measurement/flag protocols are additional operations, not presumed by (7).
- Combining the unoptimized explicit encoder, the core and this syndrome implementation gives **316 controlled-bus contacts** (264 encoding, 28 core, 24 syndrome), **198 Hadamards** (138 encoding and 60 syndrome preparation/control/readout), twelve initially zero source ancillas, six bus reset/readout cycles and at most two data Z corrections. Peak controlled register width is fourteen source qubits plus the one bus. The admitted persistent external fault memory is not bounded by this count and is not supplied as a controlled computation resource; both schedules face the same external-memory allowance. Both schedules have the same full ideal interface counts. These counts end at recovered encoded logical blocks; returning two unencoded source output wires requires the inverse source encoders and the appropriate ancillary retirement, which are not included. If an independent syndrome meter is preferred and its source CNOTs are mediated by a separate bus loop, the count is 388 contacts with an extra meter. Neither ledger certifies noise inside source preparation, resets or syndrome circuits; the exact one-loop correction theorem concerns the declared computation core.
- The strongest direct-coupling comparator is the conventional seven physical transversal CZ gates on the same Steane blocks, with the same recovery. When such source-source couplings are allowed, it avoids the 28-contact bus synthesis. Nothing here beats it.
- Protecting the bus itself by conventional QEC is another allowed route; it preserves the source code rate but must acquire encoded bus preparation, fault-tolerant controlled source access and syndrome extraction. The present comparison does not claim that source protection is cheaper.
- The original finite field receiver can be valuable when direct repeated source access is unavailable. This bus construction uses a changed port contract and does not inherit the field compiler's physical certificate or its receiver-only lower bound.

## 8. Ancestry and exact evidence

Proctor, Dooley and Kendon, [1402.6674](https://arxiv.org/abs/1402.6674), Sections II B and III A--B, equations (21), (24)-(25), give state-independent qudit commutator gates and controlled displacement implementations. Cong et al., [Phys. Rev. X 12, 021049](https://doi.org/10.1103/PhysRevX.12.021049), Section IV A.3 equation (10), explicitly uses transversal logical CZ in the Steane code and treats physical fault propagation. These primary passages were read. Knill--Laflamme--Viola's graded interaction-algebra correction is the general coherent-error ancestry.

The matched same-contact example, exact fine-record factorization and explicit single-fault witness are derived here as an architectural test for the new causal error interface. `architecture_checks.py/json` independently executes the codewords, both full 28-contact sequences, every single bus-Pauli insertion, the actual source syndrome characters, and coherent-recovery operator identities with exact arithmetic. Its author receipt is not an independent review.
