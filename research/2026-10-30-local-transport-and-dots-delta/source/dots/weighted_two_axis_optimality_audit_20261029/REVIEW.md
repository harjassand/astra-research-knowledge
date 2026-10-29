# Receiving review: weighted two-axis recovery optimum
2026-10-29. Reviewer: producer-workspace/sharpen_noreset_acquisition_certificate.

ACCEPT the frozen author's analytic sufficiency lemma. The response decomposition is a supplied mathematical premise, not an acquired/implemented decoder. Unknown background is allowed only subject to the complete channel being CPTP. No source inverse, approximate-central repair bound, acquisition guarantee, or physical unknown-matrix operation is supplied by this lemma.

## Choi orientation and all-recovery upper bound
For recovery Kraus matrices K_l:C^(2m)→C², define v_l in test-qubit⊗physical-output order by (v_l)_(a,b)=conjugate((K_l)_(a,b)); equivalently this is column-vectorization of K_l† with input-test column index first. Put Q=sum_l v_l v_l†. Then Q≥0 and Tr_test Q=I_(2m), since recovery is TP. Direct index contraction gives
 Tr[(sigma^T⊗Delta)Q]=Tr[sigma R(Delta)].
Thus the author's L=sum sigma^T⊗Delta has precisely the required objective orientation; it is not an unjustified transpose convention. The independent exact check tests 64 matrix-unit identities for a complex-valued TP recovery.

The adjoint/Pauli expansion fixes the identity contribution globally:
 Fe=1/4+(1/8)Tr[LQ].
With Y0=I2⊗[(a+b)W+J], positivity of I_test⊗Y0−L gives Tr[LQ]≤Tr[Y0]=2[(a+b)Tr W+Tr J]. No assumption that Y0 commutes with L or that W commutes with J is used.

## Bell-valued slack
In Bell order (Phi+,Psi+,Psi−,Phi−), the junk-valued diagonal blocks are exactly
 0, 2(bW+J), 2(aW+J), 2(a+b)W.
These are PSD because W≥0, a≥b≥0 and J+bW≥0. The source lists the same blocks in another order. The change of basis diagonalizes only the TWO known qubit tensor factors; it is an operator identity even for noncommuting junk matrices.

Extraction has Q_ext=2|Phi+><Phi+|⊗I_m, so it lies in the slack kernel and saturates the bound. Consequently
 Fopt=1/4+[(a+b)Tr W+Tr J]/4.
For direct sums, dephase the output block label and extract the respective qubit. Every arbitrary recovery restricts to a TP recovery on each block, and the dual is the direct sum of the displayed Y0. Offdiagonal block coherences of the input-independent background cannot change the fixed TP baseline. The baseline remains ONE global 1/4.

## Degenerate and noncommuting cases
The argument covers b=0, a=b, singular W, and W=0. No inverse of W occurs. A proposed analysis-only repair using W^(1/2) does not establish how much the repair moves the true responses, and is not received as an implemented operation. Fullrank or singular background is immaterial to this objective but can matter to other tasks.

## Executed evidence
The 60 author CPTP diagnostic cases were replayed exactly, with byte-equivalent JSON values. Independent exact SymPy checks include three actual CPTP channels with singular noncommuting W/J, fullrank noncommuting W/J, and W=0; exact Bell block identities; exact extraction/dual equality; and the complex Choi-orientation tests. The channels use a small rational response scaling and fullrank replacer background, verified TP and positive definite by exact leading principal minors. None of these diagnostics acquires an unknown decomposition or executes the proposed approximate streaming algorithm.

A separate reviewer-originated necessity statement and its counterexample are preserved in NECESSITY_ADDENDUM_CANDIDATE.md. They are not silently included as an author-source receiving claim.
