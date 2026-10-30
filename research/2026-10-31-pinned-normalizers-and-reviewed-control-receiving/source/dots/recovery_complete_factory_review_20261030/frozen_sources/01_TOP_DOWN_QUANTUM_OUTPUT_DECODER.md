# Actual top-down quantum output from scheduled concatenated computation
30 October2026. New receiving construction using the reviewed scheduled-FT interface, not ABO's classical de-encoding and not an autonomous construction. Independent review requested.

## Result and received foundation
An actual noisy quantum-output decoder can have a fixed small inclusive output-error strength O(x_0), uniformly in concatenation depth. Shrink the code top-down, using protected lower-level gates before each shrink. Do not decode all children to unprotected qubits and wait, and do not silently replace the final hardware by an ideal decoder.

Received: producer-workspace/INDEPENDENT_REVIEW.md and its frozen STANDARD_FT_SUPEROPERATOR_RECEIVING.md (SHA751b5452...). It supplies disjoint scheduled rectangles, inclusive complete strengths x_j, actual finite reset reception, and the common hierarchical sparse-error module proof. Its arbitrary-input correction assertion is essential here. The actual computation-code and routing/idle resources remain paid.

## 1. Fixed code and genuine coherent recovery
Let the chosen qubit computation code have fixed block size m, correct d_c arbitrary errors, and actual correction-plus-gate spread ell, with k ell<=d_c. All constants below depend on this fixed code. A conservative strict margin k ell<=d_c/2 may be chosen.

There is a constant-size circuit D_0=(E_0^dagger tensor I_work) R_0, where R_0 is a coherent full-syndrome recovery followed by the inverse UNITARY stabilizer encoder E_0^dagger. It acts on m DATA symbols and a fixed number of ancillas. Compute all stabilizer syndromes, reversibly select a Pauli representative for each syndrome (minimum-weight on correctable syndromes), apply its inverse, and retain the syndrome work. The code is fixed, so its full lookup table is finite and compiles into a fixed reversible circuit. Then apply inverse Clifford encoding, retain the one logical output and discard/retain the other DATA and work as garbage.

For every admitted correctable E and every unknown logical state,

 D_0 E V|psi>
       = |psi>_out tensor |s_E>_garbage,                  (1)

Thus recovery executes BEFORE inverse encoding. The clean recovery also maps arbitrary incoming words into the code module, possibly with arbitrary logical content. No logical-value copy is left in discarded garbage for inputs in the correctable module.

This is NOT the classical procedure of ABO §4.9. That procedure permits logical-label-dependent garbage and is unsuitable for unknown quantum output. Here the finite actual coherent stabilizer circuit is explicitly used. Its syndrome/conditional correction gates belong to the supplied finite universal gate set; for qubit stabilizer codes the Clifford inverse encoder is exact.

## 2. Actual shrinking protocol D_l
Input: an l-level block in the full hierarchical sparse-error span admitted at an actual computation working-period boundary, including arbitrary bath correlations and preexisting malformed child blocks. There may be up to d_c exceptional children at the top, not merely a clean concatenated codeword.

For l>=2:
1. Apply an ACTUAL (l-1)-level correction/identity refresh separately to every child block, padded as a full child identity rectangle so the accepted totalization and good-rectangle bounds apply. On good children it preserves their logical state. The received arbitrary-input correction property puts exceptional children into a child code module with arbitrary logical symbols and sparse residuals. These operations are physical gadgets, not analysis decoders.
2. Execute the finite logical circuit R_0 then E_0^dagger on the child logical symbols, implementing EVERY gate with the actual (l-1)-level fault-tolerant rectangle. Include fresh-ancilla preparations, their finite reset time, discarded work, idles and routing.
3. Keep the selected one child block containing the quantum output; discard or retain the other children as garbage. Recurse D_(l-1) only on that child.

At l=1 execute the same finite coherent recovery/inverse encoder using actual physical gates. Declare this terminal stage bad if ANY of its elementary locations is faulty. There is no promise of arbitrarily accurate unencoded output at fixed nonzero noise.

Run one such shrinking schedule for EACH desired physical output, in parallel and padded to a common end time. No inter-output decoder gates are needed. Every physical system leg and idle interval remains within the full actual cavity model; the bath may be shared.

Let B be a constant upper bound on the number of child-level rectangles in a complete shrinking stage, including the m initial totalizing refreshes and the level-one physical stage. Different stages occupy disjoint time intervals. Different output decoders occupy disjoint circuit modules. A large fixed B is allowed; no favorable numerical threshold is claimed.

## 3. Deterministic receiving: preexisting residuals and cross terms
Declare an l-stage good if ALL its (l-1)-level constituent rectangles are good. This is deliberately stricter than allowing several new child-level logical failures during decoding.

After the first actual child refresh, every child lies in its lower-level code/error module. Good children have unchanged logical states. At most d_c exceptional children may have arbitrary logical operators, correlated with garbage/bath. Thus the upper-level error family is still supported on at most d_c logical symbols. The clean logical R_0 corrects this entire operator family, including its two-sided cross terms, by the same Knill–Laflamme recovery. E_0^dagger then puts the recovered unknown logical state in the retained child.

Because all lower-level gate rectangles in this stage are good, the accepted common-decoder theorem moves their common analysis decoders through the ACTUAL simulated R_0/E_0^dagger circuit. The retained child ends in its admitted lower-level sparse module. All errors left by good microscopic rectangles are at that lower level; no new upper logical exception is being tolerated without charge. The arbitrary-input totalizing refresh is what prevents a malformed exceptional child from being mistaken for an encoded logical symbol before this argument.

Induct on l. At the last level no physical fault is allowed in a good stage, and the actual circuit (1) corrects all remaining preexisting base-code errors. Therefore every all-good complete decoder history H satisfies

 H E_sparse V_l = I_logical tensor |s_(H,E)>              (2)

on the entire admitted hierarchical error span. The FINAL output in (2) is the actual physical qubit; intermediate analysis decoders have disappeared through induction. The garbage may retain every syndrome, discarded block and environment. The factor is common for all sparse supports and all ket/bra histories, so arbitrary bath operator coefficients may be attached without estimating their individual norms.

This uses precisely the received arbitrary-input sparse correction property. If a different gadget family lacks that range property or only has a classical correctness statement, this construction is NOT earned for that family. Strict residue margin alone is not a substitute for that property.

## 4. Joint inclusive decoder strength
From the accepted threshold recursion, x_j<=x_* r^(s^j), r=x_0/x_*<1, s=k+1>=2. Define

 p_dec = product_(j=0..l-1)(1+x_j)^B - 1.

Each output is bad iff some stage contains a bad child rectangle. Selected child rectangles from different shrinking stages or outputs are disjoint physical spacetime subcircuits (a prefix-free mixed-level family). Apply the same exact nested threshold sieves inside each selected rectangle; their supports are disjoint, so the inclusive bound is the product of their x_j strengths. No shared-bath independence is used.

Expand the exact OR indicator for each selected output. Taking absolute values only of its finite indicator coefficients gives, JOINTLY for every selected output set S,

 ||sum_(decoder paths bad on every i in S) E_F||_diamond
       <= p_dec^|S|.                                    (3)

The same statement applies with selected computation bad events by the full-circuit disjoint expansion. In particular it does not presume that a good computation map is positive.

Since s^j>=j+1,

 sum_j x_j <= x_0/(1-r),
 p_dec <= exp[B x_0/(1-r)]-1 = O(x_0),                  (4)

uniformly in l. The floor arises at the final physical stage. There is NO l*x_0 cost: the stage performed with level j gates costs x_j, not x_0. There is also no need to claim the bottom-up recurrence p_next<=Bx_0+A p_child^(d_c+1).

## 5. Global computation and outer-code support
Let q denote the number of desired physical output qubits, and let epsilon_comp bound the complete bad-computation map for preparing the target on q concatenated logical qubits. Split using the ONE full-circuit fault expansion. Computation and decoder physical locations are disjoint. The mixed inclusive bound for decoder-bad S AND computation-bad is <=epsilon_comp p_dec^|S| (with epsilon_comp defined by the accepted computation OR majorant). Hence restricting decoder maps to computation-good costs at most(1+epsilon_comp), not positive conditioning.

On computation-good and with at most t bad output decoders, (2) shows that the actual output lies in the common span of arbitrary operators supported on at most t physical output qubits applied to the target. This includes cross terms and entangled operator coefficients across the bad outputs.

The exact cardinality sieve gives for K=t+1

 b_out <= binom(q,K) p_dec^K (1+p_dec)^(q-K).

A valid total bad-map bound is

 b_total <= epsilon_comp +(1+epsilon_comp)b_out.          (5)

For a linear-distance outer Tanner code, choose t=theta q inside its common correctable radius. At sufficiently small FIXED x_0, b_out=exp(-Omega(q)). Choose epsilon_comp equally small. The actual state is positive even though the grouped maps need not be; an actual output projector onto the common target-Pauli span annihilates all good histories, so its bad population is <=b_total, and gentle projection gives a source support error <=2sqrt(b_total). A native receiving apparatus still requires its real warm-input/moment interface; no native clock/reset module is manufactured by (5).

## 6. Fixed-schedule Tanner target factory and honest cost
Compute a polynomial-size stabilizer encoder for the desired known Tanner logical state or encoded Bell state by binary symplectic Gaussian elimination. Prepare its q known input bits/Bell pairs and run that fixed Clifford circuit on q temporary concatenated-code logical qubits using the reviewed FT construction. All syndrome work is quantum/reversible inside that schedule; no random ATG record, global measured Pauli frame, or late classical minimum-weight frame computation is needed. The classical compilation is offline on a known target, not a decoder acting on unknown quantum data.

Let L count the complete padded ideal target circuit, preparations and required routing; L=poly(q) with the declared connectivity. Choose l=O(log log(L/epsilon_comp)). Temporary space is

 q * polylog(L/epsilon_comp),

and computation locations are L*polylog(L/epsilon_comp). The shrinking decoder adds O(q A^l) locations and O(D_g^l) times a fixed stage-depth factor; these are of the same polylogarithmic-overhead form. Idles and discarded-block handling must be included in the declared schedule.

For the desired epsilon_comp=exp(-c q), log(L/epsilon_comp)=Theta(q). Thus temporary space and physical time are POLYNOMIAL in q, potentially with enormous exponents—not q*polylog(q). The original ATG source has far better constant-depth/O(q^2) ordinary preparation costs under its own resource model. This construction's different advantage is eliminating the random-frame storage/interface, not asymptotic or practical superiority.

## Scope
Earned only if reviewed: an actual fixed-schedule quantum-output source with a small local output-noise floor and exponentially small outer-code support failure, using the accepted actual gate/reset/cavity resources and totalizing quantum correction. Not an ideal output decoder, not arbitrary-accuracy single-qubit delivery, not an autonomous source, not a new FT principle, and not yet a full native warm-apparatus theorem.
