# Independent affine-program realization review

## Source-bound verdict

**PASS as a mathematical acquisition construction for the declared classical-process task.** I read the complete `AFFINE_PROGRAM_REALIZATION_SPECIFICATION.md`, 11,689 bytes, SHA-256 `9e810f64f08ead6182627693747d71dc34f767fdf0797d8d00df3f9628340f0e`, checked the finite-field construction and quantum/classical orientation, and ran independent small exact/dense diagnostics. No source correction was required.

This receipt does not certify an implemented polynomial affine compiler. It does not permit replacing an arbitrary originally supplied quantum dilation, coherent source controls, exposed random tape or environment records. It binds only a known controllable binary affine state program with fresh private fair random bits, and the outcome-retaining diagonal-process consumer stated in the source. Existing whole simulation and sparse-Pauli receiving theorems remain separate dependencies, not newly proved here.

## 1. Classical law and reverse fibres

Compressing redundant random bits to a basis of im G preserves their uniform image exactly. Controllability forces rank[F G]=n, so uniform input state together with uniform independent random bits gives uniform output state. Iterating n times makes the accumulated random image all of GF(2)^n; hence the forward stochastic matrix has nth power equal to uniform reset, including every affine offset and every initial state.

For a quotient R with kernel im G, H=RF has independent rows. A row annihilating H would give a row of the original state space annihilating both F and G, contradicting rank[F G]=n. Therefore H admits the stated right-inverse construction and ker H has dimension g.

The solutions of Hx=R(y+b) are exactly x=A0 y+Bz+A0 b, with z uniform and unique after choosing B as a basis of ker H. Under uniform stationarity this is the reverse conditional law. Adding BL to A0 changes only the private choice of representative within each fibre. It does not change that reverse conditional distribution. The reverse matrix is the transpose of the forward stochastic matrix; its nth power is again uniform reset. Its affine random-support formula therefore proves controllability of (A0,B), without importing an asymptotic or spectral mixing assertion.

## 2. Feedback over GF(2) is actually proved

The finite candidate list 0,e1,...,eg suffices in each cyclic-reduction step. If every candidate A0 v_i+B u stayed in the current span, the zero candidate and its differences would put A0 v_i and every B column in that span. The earlier recurrence relations would then put A0 v_j there for all previous basis vectors. This would produce a proper A0-invariant subspace containing im B, contrary to controllability. Thus the construction reaches a basis T in at most n steps using polynomially many binary rank tests.

For A1=A0+B L0 the vectors in T are consecutive powers of A1 applied to b1. With w=e_n^T T^{-1}, the observation matrix O has an anti-triangular product OT with ones on its anti-diagonal, so O is invertible over GF(2). For j<n-1, w A1^j b1=0; for j=n-1 it is one. Consequently A=A1+b1(w A1^n) shifts the rows of O and annihilates the last row, since addition equals subtraction in characteristic two. Thus OAO^{-1} is a nilpotent shift and A^n=0. Also HA=R is preserved by every feedback term because HB=0.

This is a direct finite-field argument. It does not rely on transferring a real-field distinct-pole proof or assuming an infinite choice set. Matrix inversion, rank tests and multiplication are polynomial in the explicit binary dimensions.

## 3. Reversible completion has the correct forward orientation

The columns of [A B] span the state space: under H the A columns map onto the quotient through R, while B spans ker H. Equivalently its n rows are independent. Extending them to an invertible (n+g)-square binary matrix and adding the fixed translation gives an explicitly synthesizable affine reversible circuit.

Its inverse U is the physical forward circuit. For fixed input x, every y satisfying y in Fx+b+im G determines exactly one z through the reverse-fibre equation. The remaining input register r_new is then uniquely determined by the completed invertible map. Distinct such y cannot share the same r_new, since that would give two outputs for a single input of U. There are exactly 2^g allowed y, so uniform input r_new gives the original forward transition with the correct probability, not the reverse chain. The choice of completion rows changes only private environment conventions.

## 4. Full-reference quantum reset, not only diagonal mixing

With g actual Hadamards preparing the fresh environment, the Kraus matrix indexed by its discarded output z has one entry 2^{-g/2} in each row, at column f_z(y)=Ay+Bz+Ab. This formula is valid even when f_z is noninjective. Products of these matrices compose the deterministic row maps; no unintended path multiplicity appears. After n steps every composed map has linear part A^n=0. Each Kraus word therefore has rank one and common output vector proportional to the uniform superposition.

Trace preservation of the complete Kraus family then forces the exact reference-preserving reset channel. One need not separately assume a normalized or uniform root distribution. Because the entire affine circuit is a computational-basis permutation with positive entries, it fixes the uniform superposition on all source and environment bits. Thus W psi=psi tensor |+>^g holds with the actual circuit phase, supplying explicit c, source preparation and reflection. The return certificate m=n applies to all quantum source/reference inputs of this NEW realization.

Running the separately reviewed Clifford finder on an eventually emitted gate program is an additional check, not a substitute for this proof and not an execution claimed by the present mathematical source.

## 5. Controlled classical receiving and its boundary

For a diagonal observable, each Kraus row selects only one input column; hence the adjoint output is diagonal and equals the original forward affine expectation. The argument also holds for system-operator-valued diagonal entries. Source-label-controlled Hamiltonians preserve this algebra under commutators, even when different system couplings do not commute. Backward composition with outcome-retaining prescribed interventions whose adjoints preserve the same algebra therefore gives the original system process and public label statistics from any supplied classical initial law.

This is not a claim that the newly synthesized quantum channel equals a naive previous dilation on off-diagonal source observables. The one-bit uniform-reset example correctly separates a random-X quantum channel retaining X information from an actual |+> reset realization with the same classical kernel. Disclosing original private random bits, arbitrary coherent source interventions, or simulator emission/time records would change the receiving task and is excluded.

Future coupling/centering and nontrivial mean-Hamiltonian costs remain acquired and paid. In particular, an arbitrary succinct Boolean output's uniform mean is not supplied by the construction. Ordinary diagonal-process equality does not remove those costs or imply a practical advantage.

## 6. Independent diagnostic evidence

`check_affine_realization_independent.py`, 4,646 bytes, SHA-256 `cdd31c03e0d19a0034db62bb5acec187ec3fc7ca47bc7c1b37d9b8b3af7a449c`, completed successfully. Its result `affine_independent_checks.json`, 280 bytes, SHA-256 `dad930249351be95732179af12e776efa0807866f5391eee1b81b08020826ae3`, records:

- exhaustive examination of 3,634 single-input (F,G) pairs through n=3;
- all 1,370 controllable pairs passed the feedback identities HA=R, full row rank of [A B], and A^n=0;
- 100 selected single-input cases and 96 random multi-input/redundant-input cases passed every affine offset;
- those dense checks compared the original forward kernel to both the Kraus diagonal action and an independently completed affine permutation, verified Kraus completeness, and compared the entire n-step superoperator with pure reset, not merely its diagonal restriction.

The diagnostic deliberately uses small brute-force solves and dense matrices. It is NOT an implemented polynomial compiler or proof of large-instance performance. The polynomial acquisition claim rests on the explicit elimination/rank construction above.

## 7. Ordinary ingredients and source limits

I inspected the accessible primary Heymann correspondence, which explicitly gives the controllable multi-input to cyclic single-input feedback lemma and a constructive real-matrix pole-assignment method: https://csaws.cs.technion.ac.il/~heymann/Heymann%27s%20papers/Pole%20Assignment%20in%20Multi-Input%20Linear%20Systems.pdf . The present finite-field proof is checked directly rather than inferred from its real spectral setting. Gaussian elimination, reversible affine circuits and stabilizer processing are ordinary ingredients. The denied NASA record was not retried or used as theorem evidence.

The accepted operation is a precisely scoped realization-synthesis construction for a known classical affine source: choose hidden coherence differently while retaining the declared classical controlled law and earning a pure-return certificate. No novelty, unrestricted representation learning, nonlinear-source completeness, classical hardness, whole-compiler implementation or practical superiority is asserted.
