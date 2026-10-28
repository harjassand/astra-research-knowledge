# Independent receiving audit: direct full-decoder use of matrix GLS

**RECEIVED in the inherited ordinary-input, paid collective-receiver, one-payload scope.** 28 October 2026.

Source: `ordinary_generic_matrix_gls_direct_decoder_corollary_20261028.md`, SHA-256 `a9c040dc5884b3223400c24a46e857082d8ab509c91e816fa3c5d960b57d0067`.

The received parent construction and deterministic source cap remain unchanged at `a331566da59a07b7d9b679e4516368866fd38df20e44cff4f87f8496332d52ea` and `23a7d41b408007eb11c5616129cb2bc5253ba3bd44e92538659d2382cda3072c`. This reviewer checked the proposed direct-direction algebra before the manuscript was written and independently verified the complete corollary and constants after reading it; no new mechanism or proof correction was contributed to this corollary.

## 1. The whole Hilbert-space event is available

The received GLS event is a coefficient V-norm bound, and its block leverage is an operator inequality on the full real Hermitian space. It therefore applies directly to C, not only to rank-one projectors. The squared metric norm is exactly

    <C,K(U)C>=Tr(U C^2).

For a full CPTP decoder C>=0, C<=2I and Tr C=k. Thus C^2<=2C, and U<=3T+32eta I proves Tr(U C^2)<=6q+64k eta. This use of a nonlinear C^2 in the PROOF does not change the actual final affine decoder SDP. No decoder is chosen before the simultaneous event, and no exponential union bound is inserted.

The coefficient mesh finer by1/k bounds the operator rounding error by eta/(64k), hence its trace against C by eta/64. The main Loewner induction only becomes safer. This establishes the rounded bound(4), with its leading term independent of a spurious sqrt(k) factor.

## 2. Direct relative absorption and the finite decision gap

Writing K=ceil(sqrt(k)) gives

    |qhat-q|<=(3/64)sqrt(eta q)+(9K/64)eta.

Young's inequality with delta=gamma/16 costs9eta/(1024gamma). The proposed A=(eta/4)(gamma^-1+K) dominates both additive terms. An eta-accurate feasible affine minimization yields

    (1-delta)q_selected<=(1+delta)q_*+2A+eta.

The two exact comparisons

    (1+delta)/(1-delta)<=1+gamma/4,
    [(gamma^-1+K)/2+1]/(1-delta)<=2(gamma^-1+K)

hold for0<gamma<=1. They give(6) without clipping roots or discarding the relative structure. The original quadratic encoder-net comparator and interior decoder mixing remain applicable.

With the target scale in(7), the good-branch additive coefficient is at most18/1024, strictly below1/32. The original bad-history and whole-process finite implementation budgets therefore still prove the stated expected completed Bell-loss target against the original unrestricted full-CPTP optimum.

## 3. What changes in the paid schedule

Only the predetermined final scale/count J, the finer coefficient rounding, and the final solver accuracy change. The local bias restriction, m_i floors, every coarse/fine bank, support count, and horizon formula are unchanged as FUNCTIONS of that new J. Recompute the J-dependent median count and all displayed caps before data collection. Then eta_final^-1 is O((gamma^-1+sqrt(k))/epsilon), so the dominant source bill is

    O-tilde(k^4/(gamma epsilon)+k^(9/2)/epsilon).

The repeated chosen-x matrix-bank count remains O-tilde(k^2). The finer finite precision adds arithmetic/control bits, not an uncounted physical encoder grid or tomography bank. This does not remove the paid common frame, purification, collective receiver memory, or the one-use payload contract.

## 4. Independent evidence and boundary

The companion `_independent_check.py/.json` passes240 physical channel/full-CPTP-decoder directional cases, including20 perfect-isometry decoder fixtures, and600 exact rational relative-decision/comparator cases. The near-zero fixtures use exact dyadic/permutation isometries, avoiding an artificial floating-point logical-loss floor when eta is extremely small. Some fixtures saturate the direct metric bound; the maximum checked ratio is1.0. These diagnostics do not execute the local quantum query or a production solver.

No stronger matrix concentration, new tomography theorem, generic k^2 source rate, hardware advantage, or separation from an equally informed conventional learner is received. The improvement is a deterministic use of the same received second-moment coefficient event.
