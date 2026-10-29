# Physical permutation twirling: protected-code orbit and memory-safe guard
2026-10-29. Independent constructive challenge; corrected proof draft v2, awaiting a separate review. Supersedes v1's inaccurate claim that a coarse bad branch can signal payload information to the source-memory marginal. No novelty claim.

## 1. Irreducible full-space channel twirl
Let H_P be the full n-qubit singlet sector, dimension d, carrying the irreducible permutation representation U_g of S_n. Let T be any CPTP map on P tensor M, with arbitrary memory output M'. Perform an actual uniform private permutation U_g before T, inverse U_g afterward, and retire g. The resulting joint channel is
Tbar=E_g (Ad_Ug* tensor id) T (Ad_Ug tensor id).
Its Choi matrix is invariant under U_g tensor conjugate(U_g) on the logical output/input-reference pair. The maximally entangled vector Omega_P is the UNIQUE invariant vector, since U is irreducible. Averaging kills its cross terms with the orthogonal complement. Positivity therefore gives an exact CP decomposition
Tbar = id_P tensor B_0 + T_bad.
This is a CP block decomposition, not a decomposition into individual unitary errors. The good Choi block is Omega_P tensor J(B_0); the bad Choi block has orthogonal logical-Choi support. Covariance and Schur's lemma on the input imply
T_bad^dagger(I_{P M'})=I_P tensor H_bad,
B_0^dagger(I)+H_bad=I_M.
For every memory state sigma, Tr(H_bad sigma)=1-Fe(T_sigma). Thus branch probabilities depend only on the memory marginal even when the current carrier and memory are correlated. Bad branches are NOT product maps, but their memory marginal is non-signalling from the carrier; they can create output-carrier–memory correlations. Explicitly, tracing the output carrier removes the inverse permutation, and averaging the input permutation gives I_P/d tensor Tr_P(X). Thus Tr_Pout Tbar(X)=B_total(Tr_P X). Subtracting the good branch gives Tr_Pout T_bad(X)=B_bad(Tr_P X), where B_bad is CP because it is the reduced bad output on I_P/d tensor sigma. This is valid on arbitrary correlated inputs and survives Q restriction and TP decoding.

For a memoryless TP logical map the same decomposition has weights F and1-F, each normalized branch TP by irreducibility. Its bad Choi state is orthogonal to Omega; the maximally entangled input distinguishes it perfectly from identity. Consequently half-diamond distance from identity is exactly1-Fe. This linear identity concerns the ACTUALLY twirled channel, not an untwirled source or a retained key.

## 2. Physical leakage and a proper power-of-two subcode
Use physical singlet encoder I_P and reset decoder D_P(X)=PXP+Tr((I-P)X)I_P/d. This decoder is covariant under all physical permutations. It extends an arbitrary physical source, including leakage and nonunitality, to the T above. Its Bell loss is bounded by C_full q, C_full=(n+2)/(n-1), from the reviewed matching-survival theorem.

Now select any fixed K-dimensional subcode Q of P, preferably K=2^k for the existing qubit/GRS architecture. It need not be permutation invariant. Encode into Q, physically permute the encoded state, invoke the same source, invert that permutation, and decode Q with maximally mixed replacement I_Q/K. The permutations take Q through its orbit; this is intentionally NOT the old fixed-code service.

Let E_Q be inclusion into P and D_Q be the TP reset decoder from P to Q. Then
(D_Q tensor id) Tbar (E_Q tensor id)
 = id_Q tensor B_0 + T_bad,Q,
with T_bad,Q CP and T_bad,Q^dagger(I)=I_Q tensor H_bad.
No d/K factor occurs. The full-space good identity block survives restriction and the bad branch's trace effect remains constant on Q. Physical direct reset to I_Q/K agrees with D_Q D_P, since D_Q(I_P/d)=I_Q/K. This equality is why the maximally mixed reset convention is specified.

The average source input after the physical permutation is P/d tensor sigma_M, even for a carrier-memory correlated state: irreducible group averaging is depolarization on P. A uniform matching test has the same averaged input. Exact input equality is helpful but not a replacement for the complete current-source boundary and private metadata requirement.

The per-history effects satisfy E_bad,service<=C_full E_fail,test on memory. The test need not know the physical permutation used on a service. Fresh independent matching and permutation settings, timing, routing and role metadata must be hidden until source action completes; keys must remain retired for the claimed output. Known acquired local frames conjugate both the singlet sector and the physical permutations and require the associated trusted rotations.

## 3. Sequential guard without product bad branches
Prepare the complete outer code, use one fresh service symbol per service call, and retain the secure-buffer and same-source assumptions of the existing guard. At every step the exact service CP instrument has good branch id_symbol tensor B_0 and bad branch T_bad,Q, with input effect I_symbol tensor H_bad. Condition on its virtual good/bad labels and observed prior tests, but NOT on retired keys. The full codeword can be correlated with source memory after a bad event; the coarse memory evolution nevertheless closes as a CP map of its prior marginal. Nevertheless the next event probabilities depend only on the current memory marginal, so uniformly for every conditional state
p(bad service | h)<=R p(test failure | h), R=C_full s/(1-s).
The existing bounded supermartingale proof therefore gives Pr(accept and >t bad services)<=epsilon_NB for EVERY initial joint payload-memory-reference input. Factorized latent Pauli histories are unnecessary for this probability bound.

On a branch with bad-service positions S, |S|<=t, all complete data-memory Kraus operators act only on those service symbols and memory; good service maps are identities on their data. Thus their operator expansion lies in the error space of arbitrary operators supported on at most t code blocks, tensored with memory operators. An actual outer quantum code correcting ALL such errors corrects that branch exactly, including coherent memory correlations. The Knill–Laflamme condition gives, after recovery with its syndrome retained, a branch map id_payload tensor B_h. A decoder that corrects only a stochastic Pauli model is insufficient; the existing distance-(2t+1) CSS/GRS quantum code does correct arbitrary t-block errors by linearity and its full quantum correction property.

## 4. Exact source-memory filter and retained-syndrome distinction
Let A_good be the accepted sum over <=t bad services after actual outer recovery, and A_bad the accepted remainder. Then A_good=id_payload tensor B_good. The uniform probability bound gives ||A_bad||diamond<=epsilon_NB on all initial joint inputs.

For the output consisting of recovered payload, source memory and permitted test/controller history, RETIRE outer-decoder syndrome/trash records. Each coarse step has exact CP memory closure; composition gives the actual accepted memory map B_acc=B_good+B_bad_acc. TP outer recovery cannot change that memory marginal. Both bad maps have norm at most epsilon_NB, so

(1/2)||A_acc-id_payload tensor B_acc||diamond <= epsilon_NB.

This ideal uses the SAME actual source-memory/test-history filter. On initially product payload-memory inputs actual acceptance is exactly independent of payload. On correlated inputs the memory filter can steer the logical marginal, as already allowed in the ideal target. Keys remain retired; conditioning on their values invalidates this channel.

If arbitrary outer-decoder syndrome/trash is retained as part of the allowed output, >t-error branches can place payload-dependent information there. Exact non-signalling to that enlarged environment is not established. A universally valid simulator instead fixes a dummy logical state tau and defines B_dummy(sigma)=Tr_payload[A_bad(tau tensor sigma)] including those extra records. Set B_acc_sim=B_good+B_dummy. It is CP and TNI because its trace is the actual acceptance probability on dummy payload; both A_bad and id tensor B_dummy have norm<=epsilon_NB. The same half-diamond bound follows, but the enlarged simulator filter is no longer claimed equal to the actual accepted marginal. These are two different output scopes, not interchangeable formulations.

## 5. Consequence and costs
Choosing s=1/(1+C_full) gives R=1 and the familiar b=0 bound2^(-t-1). The proper-subcode d/K localization penalty has been removed by physically moving the service code through its permutation orbit, not by strengthening the fixed-subcode witness. Logical Pauli compilation is replaced by known physical permutation control, but those routes, inverse routes, acquired-frame rotations, secret randomness, full initial encoding, output decoding and mixed reset are paid operations. On a line permutations still cost O(n^2) adjacent swaps per service in a straightforward implementation; no practical speedup follows automatically.

Ordinary random-unitary channel twirling, Schur's lemma and quantum authentication provide strong prior mechanisms. This proof does not claim a new general linear-diamond principle, arbitrary-noise positive capacity or superior total hardware architecture. The open obligation is independent review of the CP decomposition, arbitrary-error recovery and simulator composition, plus actual circuit/resource comparison.

## Additional direct physical refinement
The author's separate direct-Kraus proof can avoid the virtual maximally mixed full-P reset. The singlet permutation irrep occurs with multiplicity one in the full n-qubit physical space, so a group-averaged physical Kraus operator from P to that full space is exactly the inclusion tensor a memory operator. Subtract it to obtain a physical CP good/bad split; restriction to Q and ANY TP decoder exactly inverting Q preserves the good identity and the same bad effect. This stronger route permits a fixed pure-state leakage replacement as well. Its multiplicity-one premise is essential; it is not a theorem for an arbitrary repeated irrep without modification. The independently rerun orbit_instance.py exercises that route with full64-dimensional output, n=6,d=5,K=4 and pure logical0 reset.
