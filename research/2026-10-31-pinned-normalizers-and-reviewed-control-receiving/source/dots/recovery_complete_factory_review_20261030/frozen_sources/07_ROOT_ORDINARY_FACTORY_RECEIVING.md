# Receiving an ordinary protected encoder and noisy output decoder into native Tanner memory
30 October 2026. Root conditional construction candidate. The actual protected top-down decoder is a separate unfinished obligation; this note does not replace it by an ideal decoder.

## Intended capability and why this alternative matters
A known stabilizer state, including a Tanner encoded Bell resource, has a polynomial-size Clifford encoder obtained by finite symplectic/Gaussian elimination on the given stabilizer generators. Execute that ordinary encoder on temporary concatenated-code logical qubits using the accepted scheduled fault-tolerance construction. Then physically de-encode each output block in parallel, tolerating a fixed sufficiently small local output-noise floor. Prepare the native memory's known ready apparatus during the final scheduled handoff and enable its already-supplied correction dynamics.

This avoids the alternating-Tanner graph's random raw measurement records, delayed global Pauli frame and protected classical-record factory, by paying polynomial protected preparation time and temporary encoding space. It is an informed conventional alternative, not a claim that ordinary fault-tolerant state preparation is new or faster. The native target code and its decoder/corrector interfaces remain the same.

The missing actual decoder must preserve arbitrary quantum coherence, not merely reproduce the classical labels of ABO's physical recursive-majority output. A promising implementation is top-down protected recovery+inverse encoding, shrinking one concatenation level per stage, with every nonterminal stage executed fault-tolerantly on its child blocks and a final constant-size physical quantum decoder. Its exact module receiving is separate.

## 1. Sufficient joint output interface
Let M<=c_0 N denote target DATA outputs plus physical native-apparatus sites. The ideal target is the intended Tanner logical module with strong-ready product apparatus. Suppose the full physical encoder/decoder/reset circuit has an exact signed expansion indexed by physical fault sets.

Let C_bad be the event that the protected encoder computation has a bad top-level rectangle. Its complete map sum has norm at most epsilon_comp. Let O_j be the decoder/reset failure predicate for output region j. The proposed output decoder supplies, jointly for every selected region set S,

 ||sum_(faults satisfying all O_j,j in S) E_faults||_diamond <=p^|S|.

Since computation locations and all decoder/reset locations are disjoint in time/location space, the SAME inclusive-sieve calculation should also supply

 ||sum_(C_bad and all O_j,j in S) E_faults||_diamond
 <=epsilon_comp p^|S|.                                 (OF1)

This is not inferred from two marginal bounds. It follows only if both predicates have the exact disjoint-location sieve expansions with the stated coefficient budgets. Shared-bath correlations are already allowed by the underlying inclusive norm law.

Restricting to computation-good paths gives a signed output family G_D with inclusive norm

 ||sum_(D contains S)G_D||_diamond <=(1+epsilon_comp)p^|S|.  (OF2)

The common good-module intertwiner of the actual output decoder must ensure that each G_D acts, on the ideal Tanner source, within the operator-error span supported on the output regions D. It need not be CP. An output region must have a bounded physical footprint; the actual decoder's temporary space is not charged as output support after its correctly specified de-encoding map.

## 2. Large-output-support bound directly from inclusive norms
For integer K, the exact threshold sieve used in the accepted circuit bridge gives

 ||sum_(|D|>=K)G_D||_diamond
 <=(1+epsilon_comp) binom(M,K)p^K(1+p)^(M-K).           (OF3)

Let P be the common native logical-module span reached from the ideal source by errors in fewer than K output regions, including arbitrary bath coefficients and dirty apparatus within those footprints. All computation-good terms with |D|<K have zero (I-P) compression. Positivity of the ACTUAL final state therefore gives

 Tr[(I-P)rho_actual] <=epsilon_comp
 +(1+epsilon_comp) binom(M,K)p^K(1+p)^(M-K).           (OF4)

For K=delta N with delta fixed, sufficiently small fixed p makes the second term exp(-cN). Choose epsilon_comp<=exp(-c' N). A gentle projection then gives a positive, subnormalized source supported in P within trace norm at most twice the square root of the right side. No signed path was called a positive probability, and no noise independence was assumed.

## 3. Native source warmth is paid by actual output footprints
Use the real bounded-ownership/forest constants of READ_OFF_WARM_COMPLETION.md, not a generic assertion that all sparse scratch is harmless. A fault in one output region affects at most c_act native owner predicates and f-sized prefix footprints. Starting with strong-ready apparatus, fewer than K region faults therefore imply

 canonical BOTH-sector radius <= C_rad K,
 BUSY and dirty-owner count <=C_busy K,
 E_native <=C_E K,

with fixed actual hardware constants. Baseline b=0 is hard-coded in the comparator and target module; there is no random acquired reference to retain. If a different known reference is used, its true baseline discrepancy must be paid explicitly.

Choose delta so these bounds lie strictly inside all original native basin, radius and BUSY allowances. On this common source subspace the actual positive Lyapunov envelope obeys its received finite-footprint upper bound

 P F_native P <= exp[(g+s C_E delta)N] P.

This inequality must be read through the exact canonical/pullback source envelope; it is not an operator-Jensen step. It supplies a valid warm coefficient below the native escape barrier when delta and existing proof parameters have the required margin. The positive support cut need not be a physical operation. Native correction then protects the original logical module using its already-reviewed continuous operator theorem.

This common-span route avoids trying to infer a joint exponential moment from separate positive marginal fault probabilities. It does require the real output-region/coherent-module guarantee of section1 and the same native bounded-footprint geometry used by the earlier source receiver.

## 4. Actual resource accounting
If the ideal stabilizer encoder has L_enc=poly(N) locations, ordinary scheduled FT uses L_enc polylog(L_enc/epsilon_comp) physical locations and a corresponding polylog factor in space/depth (with the actual unoptimized code constants). For epsilon_comp=exp(-cN), log(L_enc/epsilon_comp)=Theta(N), so this overhead is polynomial in N, NOT merely polylogarithmic in N. It may be a very large polynomial.

All output blocks can follow the same shrinking decoder schedule and emerge together. This avoids leaving already decoded physical target qubits unprotected for a long serial decoder. Native apparatus preparation and the final switch must fit the actual fixed-duration last handoff window; idles and noise throughout are counted. Dirty ancillas are prepared with the accepted finite-reset/approximate-target cavity construction, not assumed initially pure.

This alternative trades away the ATG's short source depth and may have substantially worse work/space. It has no unproved expensive global Pauli-frame computation and no unknown input-latch requirement because the desired resource is KNOWN. It does not yield an autonomous scheduler, an external detector, a practical advantage, or a new universal-fault-tolerance theorem.

## Current status
Equations OF1-OF4 and the native receiving conditions isolate the required decoder contract and an exact path to a physical factory. They are not a claim that the top-down decoder and all source-handoff contracts are already established. Preserve that distinction until the actual decoder construction and whole transfer are independently reviewed.
