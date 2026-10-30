# Direct physical-leaf erasure: reviewed binding proof
2026-10-30. This accepts the direct-reset improvement over the reviewer's earlier reset/refresh construction.

Reset EVERY physical symbol of the consumed level-j block in parallel, using the accepted finite replacement target and counting all residual/noise locations. Classify a level-j erasure bad if at least k+1 child erasures are bad. There is no arbitrary-input refresh, inverse encoder, repreparation, or retained scratch circuit. This removes the prior refresh-work survivor concern entirely.

Let each incoming upper module coefficient have exceptional child supports S_a,S_b, each size at most r_res. Let S_bad contain at most k bad child erasures. Define T=S_a union S_b union S_bad, so |T|<=2r_res+k.

On children OUTSIDE T, the incoming lower-level modules are admitted and their erasures are good; the induction hypothesis contracts their old logical symbols to trace, leaving only syndrome/auxiliary coefficients. On children IN T, allow completely arbitrary action and retention, whether the incoming child was malformed or its erasure was bad. After the contractions, every dual retained-output matrix element is an arbitrary operator A_T supported on T of the upper-code child logical symbols, with arbitrary auxiliary coefficients. If

    2r_res+k < d_code,

code local indistinguishability gives V† A_T V=c(A_T) I. Thus the FULL retained output is independent of the old upper logical density matrix except for its trace. This proof does not illegitimately apply a good lower-level reset lemma to a malformed child. The same union already includes every exceptional child, so no extra r_res count is needed for this direct circuit.

The physical base case is literal replacement R tensor Id_retainedbath, not a unitary dilation retaining its reset reservoir. Recursive bad-cardinality sieves give the displayed y_j recursion jointly for disjoint erasure blocks. All count constants and the stronger code margin must be instantiated; the ordinary and erasure thresholds are both enforced.

Copy a protected outcome to an encoded ancilla, then apply this actual erasure to that ancilla. Good histories genuinely eliminate off-diagonal outcome terms in the FULL retained finite-bath channel. This supplies the missing hypothesis for the branch-dependent positive CP/TNI repair: its max-branch norm and direct comparison prove full-channel error <=2b, with b including erasure failures. No number-of-outcomes factor, ideal measurement of fault labels, or fictitious bath reset is used.

This is a scoped PASS for this erasure/instrument interface, not for a downstream native waiting-bank, teleportation or feedforward composition. Reservoir exclusion, finite CP-divisible scope and actual supplied resets remain essential.
