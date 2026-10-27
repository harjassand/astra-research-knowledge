# Aligned filtered-seed value from an actual CQ reset dilation

Status: independently PASS; see `aligned_filtered_seed_cq_dilation_independent_audit.md`. This receives WHOLE VALUE, not a throughput-charged comparison to the unfiltered seed.

For nonnegative Schmidt weights h1,h2,h3 and diagonal A=diag(a1,a2,a3)>=0, let

X_low=|psi_h><psi_h|+I3 tensor A,
psi_h=sum_i sqrt(hi)|i,i>.

Then D(X_low)>=0. Equivalently, every qutrit-reset seed filtered by Z with[A,Z*Z]=0 has nonnegative homogeneous deficit, even though the filtered source is generally not TP. No inequality D(filtered)>=lambda_min(Z*Z)D(unfiltered) is asserted.

## Actual finite-dimensional source acquisition

Choose d>=max_i hi with d>0. On a six-dimensional reference with orthogonal low and high qutrit sectors, define the isometry

V|i>=sqrt(hi/d)|i,low>+sqrt(1-hi/d)|i,high>,
Y_M=A_low direct-sum M I_high, M>0.

The actual normalized Choi source is proportional to

X_M=3d Phi_V+I3 tensor Y_M.

Its trace is n_M=3d+3TrA+9M, and its physical input marginal is n_M I3/3. Thus it is an actual channel with pure reversible success, p=3d/n_M, and input-independent reset q tau with q tau=3Y_M/n_M.

For each physical output label i, a two-dimensional logical unitary rotates V|i> to |i> tensor a common pure logical success vector. This preserves physical output label i. It transforms diag(ai,M) into a positive two-dimensional logical bath T_i, without creating cross-physical reset coherences. Consequently the transformed channel is exactly the already received pure-success/physical-CQ mixed-reset class of `pure_success_arbitrary_cq_reset_bath_collapse_theorem.md`, not a mixture inference. That theorem gives D(X_M)>=0 for every finite M.

## Entropy limit

In the low/high reference split, the low diagonal block of X_M is exactly X_low, the high diagonal block is

X_high,M=M I9+|psi_(d-h)><psi_(d-h)|,

and the cross block is the bounded rank-one matrix |psi_h><psi_(d-h)|. The same reference split is respected by N and by the reference marginal.

First suppose A>0. The low blocks of X_M,NX_M and their reference marginal have a positive spectral lower bound independent of M. Their high blocks are M times positive identities plus bounded corrections. For any such two-scale block matrix [[L,C],[C*,M H+J]], with L,H>0 fixed and C,J bounded, the Schur determinant entropy formula bounds its difference from the block-pinched entropy by

O(integral_0^infinity 1/[(c+s)(c'M+s)] ds)
=O(log M/M).

Thus reference-block pinching changes the deficit by O(log M/M). The high reset-only source M I9 has deficit0 and zero first variation in every Hermitian direction: the input, output and reference-equilibrated states coincide there. The bounded high pure perturbation therefore contributes O(1/M) by the entropy Hessian. Hence

D(X_M)=D(X_low)+O(log M/M).

Taking M to infinity in the paid actual-source values proves D(X_low)>=0 for A>0. Arbitrary A>=0 follows by A+epsilon I and continuity of xlogx. Zero Schmidt weights are covered directly or by continuity. The all-zero h case is reset-only and has deficit0.

## Scope and relation to the large coherent attachment

This is a legitimate way to receive a non-TP filtered seed: it is the low-scale entropy limit of actual TP sources after homogeneous rescaling. The finite source is paid because the reset remains physical-CQ after the success-code rotation. If A does not commute with the Schmidt Gram, that rotation generally produces physical reset coherences and the CQ theorem no longer applies.

The result pays the filtered-seed term in the large-graph attachment coefficient whenever the filtered reset and main Schmidt Gram are simultaneously diagonalizable. It does not pay the difference from lambda_min(Z*Z) times the original value. Therefore the accepted-only GLS comparison remains separate.
