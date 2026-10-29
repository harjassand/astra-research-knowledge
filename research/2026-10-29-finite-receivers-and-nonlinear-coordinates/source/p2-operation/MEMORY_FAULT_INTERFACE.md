# From retained-qubit faults to an exact source-operation error

Author `/root`, 29 October 2026 Australia/Brisbane. New construction; executed evidence and actual independent review are separate. Physical memory noise is not assumed automatically Pauli.

## 1. Consequence and contract

The finite receiver protects a specified matrix factor. Its usefulness for computing depends on how faults of that factor change the source operation. The retained Pauli frames give an explicit answer including every actual receiver record, and an exact error for the noise class below.

There are n source qubits with the full binary label space. The source dilation and target G are diagonal in that basis. At cut t the compiled source branches act through ordered words in fixed Hermitian Pauli operators P_i^(t) on r_t retained qubits; scalar phases are in the actual classical history. The later receiver exactly erases that remaining family, or approximates its complete operation with uniform compiler allowance epsilon_c.

At each storage boundary insert a Pauli Q_t on the retained register. A fault path f=(Q_1,...,Q_(T-1)) has a classical joint probability p_f independent of the initial source, field and reference. Arbitrary time correlations are allowed; the law need not factorize, and the field need not be freshly prepared. The matrices and schedule are fixed, so each cut has the same known P_i on every actual history.

This premise is an actual state-independent Pauli noise process. It is not obtained by expanding arbitrary Kraus operators in the Pauli basis, quoting mean infidelity, or twirling a marginal while retaining hidden control/environment dependence. Faults during extraction, readout or source contact need separate compatible contracts.

If a memory error-correction instrument supplies an input-independent joint law of logical Pauli faults and observed syndrome h, include h in the path and the actual receiver record. A chosen syndrome-dependent source phase correction can be incorporated below. Its state-independent logical instrument, preparation, control and syndrome acquisition must be supplied; this theorem does not certify them.

## 2. The fault character is determined by the causal algebra

Define chi_t(Q) by Q P_i=(-1)^chi_i P_i Q. In binary Pauli coordinates,

\[
\chi_t(Q)_i=x_Q\cdot z_i+z_Q\cdot x_i\pmod2.
\tag{1}
\]

For P_x=product_i P_i^x_i in the declared order,

\[
Q P_x=(-1)^{x\cdot\chi_t(Q)}P_x Q.\tag{2}
\]

Moving a memory fault through the controlled source branch therefore adds exactly source Z^chi_t(Q). Fixed Pauli-frame phases cancel in this commutator but must still be implemented in receiver queries.

Let F_t be the n by 2r_t binary matrix of retained Pauli coordinates and J the nonsingular symplectic form. The prefix commutation matrix is B_t=F_t J F_t^T and chi_t(Q)=F_t J q. The rank-minimal factor has rank F_t=2r_t. Hence

\[
\operatorname{Im}\chi_t=\operatorname{Im}B_t,
\qquad\ker\chi_t=\{0\}\quad\text{on Pauli labels modulo phase}.
\tag{3}
\]

The same matrix that fixes coherent memory dimension also fixes the possible source phase-error patterns. Every nontrivial Pauli on the minimal retained factor affects some admitted source coherence. These patterns can have high source Hamming weight; a small receiver register does not imply local source errors. Discarded multiplicity, an encoded larger physical memory and a restricted source alphabet are outside this injectivity statement.

For a path, chi(f)=xor_t chi_t(Q_t). Source Z errors commute with the declared interactions and later phase feedback, so the characters add. If a chosen syndrome correction is Z^hat_chi(h), use residual chi(f) xor hat_chi(h). This describes that protocol, not an optimum over all fault-aware or receiver-record-dependent recovery.

## 3. Complete-instrument normal form and exact actual error

For each fixed path let R_f be the complete actual receiver instrument on the common input, including that path's memory faults and every actual phase, syndrome and final measurement record. After summing its outcomes it is trace preserving. It can depend on f and preserve correlations between its records and the original input.

Repeated use of (2) and exact erasure, after removing G, gives

\[
\mathcal I(\rho)=\sum_f p_f
(\operatorname{Ad}_{Z^{\chi(f)}}\otimes\mathcal R_f)(\rho),
\qquad
\mathcal B(\rho)=\sum_f p_f
(\operatorname{id}_S\otimes\mathcal R_f)(\rho).
\tag{4}
\]

B is the same noisy receiver on the common input. References are identity-extended. A latent fault path is a mathematical mixture, not an unreported physical measurement; any actually observed fault information belongs to the retained record. Equation (4) does not factor that real record law into an independent source channel and one record distribution.

For p_0=Pr[chi(f)=0], the actual complete-instrument half-diamond distance is

\[
\tfrac12\|\mathcal I-\mathcal B\|_\diamond=1-p_0.
\tag{5}
\]

Good paths have identical channels. Every other pair of channels differs by at most two in diamond norm, so convexity gives the upper bound, including arbitrary correlated inputs and references. For equality, choose the permitted product input |+>^tensor n on the source and any normal environment state. Discarding records leaves the source mixture of Z^chi(f)|+>^tensor n. These are orthogonal for distinct characters, giving trace distance 1-p_0 from the ideal source |+>^tensor n. Discarding records cannot increase distinguishability; this proves the matching complete-record lower bound.

The source-only channel is exactly the corresponding Z mixture for arbitrary initially correlated inputs, since every R_f is trace preserving. Although the full-record channel need not factor, its worst-case error equals the source error for this particular fault structure. The earlier square-root source/full-record examples concern a different structure and remain valid.

At one location, injectivity implies p_0=Pr[Q=I] modulo scalar phase. Across locations, nontrivial faults can cancel. For example, with identical retained frames at two cuts, paths (I,I), (Z,Z), (X,I) with probabilities 1/2,1/4,1/4 have actual error 1/4, although the probability of at least one nontrivial fault is 1/2. These are exogenous correlated fault paths; cancellation is not a generic independence assumption.

## 4. Finite compiler and physical discrepancies

The finite circuit's intertwining allowance is uniform over all admitted inputs and pre-cut histories. Insert a fixed Pauli fault path into both comparison circuits. Unitary faults preserve norms; subsequent channels contract them. The same stage telescoping gives epsilon_c between the actual circuit and (4), using R_f of the same actual finite receiver. Averaging paths preserves the allowance.

Consequently,

\[
\max(0,1-p_0-\epsilon_c)\leq\epsilon_{\rm actual}
\leq\min(1,1-p_0+\epsilon_c).
\tag{6}
\]

The compiler allowance is paid once: (4) already uses the same actual receiver. Replacing both endpoints by a different physical receiver model can separately require two implementation allowances. Non-Pauli memory noise, extraction faults and source-control errors still need their actual compatible channels.

This provides an interface to conventional quantum-memory protection: an acquired logical-memory Pauli instrument and residual law determine a calculable source error. It does not supply a memory code, threshold, low-cost schedule or total workload advantage. In particular the dense error patterns in Im B_t must be propagated into any source error-correction design.

## 5. A coherent fault rejects a false quadratic prediction

Use two arrival qubits and two source bits x,z, with the actual branch

\[
(X_1^x Z_1^z)\otimes(X_2^x Z_2^z).
\]

The receiver retains the first arrival qubit, then Bell-measures X_1X_2 and Z_1Z_2 and corrects their source phases. Insert a coherent storage fault E=cI-isZ_1 with c=4/5,s=3/5. On the permitted common environment input |00>, only the two Phi Bell records occur, each with probability 1/2. After feedback each branch has the same source unitary

\[
\operatorname{diag}(c-is,c+is)
\]

on source bit x, with identity on z. The same fault on the common baseline changes |00> only by a scalar phase. For source |+> the actual source and full-record errors on this input are 3/5.

A false Pauli-mixture replacement would assign Z probability s^2=9/25 and predict error 9/25. These are different channels: the coherent off-diagonal multiplier is (7-24i)/25, whereas the mixture gives 7/25. This is an explicit failure of the replacement, not a failure of (5), whose state-independent classical Pauli-path premise is absent.

## 6. Evidence and scope

`memory_fault_checks.py/json` verifies the exact complete Bell-branch fault identity over all Pauli faults and source words, computes path-character cancellation with rational weights, checks the causal-algebra image relation on emitted retained frames, and verifies the coherent counterexample in exact rational complex arithmetic. No interval solver or bosonic truncation is used.

The Pauli commutation and fault propagation ingredients are conventional. The bridge established here is a complete-record causal receiver normal form with an exact actual operation metric, compatible with the finite compiler and its independently reviewed interface. The scalar character law is an explicit acquired noise contract, not a universal consequence of randomized compiling. The read primary comparison in Winick et al., [2212.07500](https://arxiv.org/abs/2212.07500), Sections III B–C, retains persistent-memory and leaked-control qualifications.
