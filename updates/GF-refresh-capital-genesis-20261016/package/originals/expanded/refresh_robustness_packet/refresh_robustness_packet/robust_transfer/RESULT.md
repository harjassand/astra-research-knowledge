# Robust refresh transfer: result

16 October 2026. Conditional theorem, no physical-device or lifetime qualification.

## Main result

Let f_i be the existing ideal parent tester bound, including the exact one-node general-Schur value when applicable. Let each actual imperfect slot N_ik be a CPTP operation on its own full reservation D_i plus the complete persistent shared bath B, identity on other active reservations. Compare it to its ideal reference T_ik on this FULL joint boundary:

    epsilon_ik = (1/2)||N_ik-T_ik||_diamond.

Keep the fixed schedule, disjoint active full reservations, uniform action envelopes, and actual exact trusted entry/final syndrome instruments. Then for every subset R,

    F_R <= product_(i in R) min{1, f_i+sum_k epsilon_ik} I.

This remains valid with arbitrary shared bath, initially correlated input, staggered entry/retirement, and later patch reuse. It does not require independent actual fault probabilities. First-fault expansion within each parent prevents either a global additive error or an unnecessary product of (1+epsilon) factors.

## Why the bound works, and what it does not imply

The channel-distance SDP gives exactly

    N <=_CP T + epsilon E

for some normalized channel E on the same local boundary. This is a positive upper comparison. It is NOT an actual decomposition N=(1-epsilon)T+epsilon E. At the first comparison-error branch, remove that parent's acceptance test and give its physical system/controller to the prover. Remaining ideal testers retain their product bound.

A genuine mixture gives the sharper local factor (1-r)f+r and a true latent fault branch. Generic diamond closeness supplies neither that mixture nor a large exact ideal CP subchannel.

## Correctable support can survive coherent imperfections

There is a positive support route without stochastic flags. Enlarge the old weak footprint to C_i containing ALL actual propagated noisy refresh/control footprints, and check

    Pauli(C_i) intersect Centralizer(G_i) subset phase times S_code.

Every actual node must have a Kraus expansion on C_i plus bath, up to admitted exact stabilizer-algebra factors. The actual exact endpoint projections then force every endpoint-good net Pauli into the stabilizer group. Actual endpoint-good records therefore still define the genuine common-decoder-good CP subchannel. The proof keeps bath coefficients chronological. Recompute patch support/geometry/resource charges if C_i grew; containment in the old reservation alone is insufficient.

## Exact obstructions

- Marginal calibration: one shared rare bath trigger flips every parent. Each reduced channel is epsilon-close, but all fail with probability epsilon rather than epsilon^n. The full joint distance is 1.
- Missing influence locality: one full-joint epsilon fault touching n active reservations also makes all fail with probability epsilon.
- Missing enlarged-footprint condition: an arbitrarily small coherent logical rotation has zero syndrome mismatches. Its nonidentity rank-one Choi ray contains no nonzero identity CP subchannel, so diamond closeness cannot manufacture a rare actual fault flag.
- Uncharged compiled-pulse baseline: the independently checked fully finite two-qubit example has original odd action zero but private averaged endpoint failure 2/9. Path-noncommuting drift must be included in the actual error action.

## Physical gate

Qualify the complete local/portwise process, persistent controller/bath inventory, propagated error footprint, trusted endpoints, and total reset-complete reservation. A finite-pulse residual action bounds half-diamond error by sin(min(delta,pi/2)) only on a justified complete boundary. Concurrent-window compression can spread influence; use a separately proved local primitive/portwise interface. PROOF.md gives a narrow sufficient local-control-frame model and explicitly excludes arbitrary compiled windows.

Files: PROOF.md contains the theorem and full derivations. check_exact.py and check_results.json give exact SymPy checks of CP-majorant constants, coherent no-minorant, bath/cross-parent counterexamples, support example, and the 4/9 pulse branch / 2/9 private average. All checks pass.
