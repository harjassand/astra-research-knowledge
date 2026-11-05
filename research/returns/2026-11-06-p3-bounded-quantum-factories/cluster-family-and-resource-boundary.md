# Thermal-cluster example and the available resource boundary

[Available-return guide](README.md) · [Whole-channel compiler](whole-channel-compiler-and-classical-control.md) · [Exact incomplete excerpt](P3_BOUNDED_FACTORIES_20261106_RETURN.txt)

## A separate six-layer quantum data circuit

The explicit example is an open cluster chain `H_N=-sum_i J_i K_i`, with endpoint-adjusted `K_i=Z_(i-1) X_i Z_(i+1)` and `t_i=tanh(beta J_i)` in `(1/2,11/20]`. Its Gibbs state is `2^-N product_i(I+t_i K_i)`. For any crossing edge, the target violates the corresponding separable bound `E[K_i+K_(i+1)]<=1`, giving entanglement across every nontrivial bipartition. No stronger mixed-state multipartite classification is inferred.

The six physical data layers are reset, actual-root-controlled CNOT loading, Hadamard, two nearest-neighbor CZ matchings and local delivery. Outgoing data errors, unmatched-site idles and terminal noise count. The sufficient quantum condition is `p_Q<=1/3000`, with classical bit-flip rate `p_C<=min(p_Q,p_cl)` and history-erased root error `q_h<=10p_C`. The number `1/3000` certifies quantum positivity; the complete controller still requires its separate sufficient classical threshold `p_cl`.

Physical Clifford faults become bounded-support convolution in graph-basis labels. The input-label inverse has a signed transfer representation of at most sixteen link states. A signed expression alone is not a physical sampler: the proof supplies an invariant positive cone, with sufficient inequality `zeta<=1/(4R^2+2R)`.

At the certified endpoint, the reported rational evaluation gives `R=12.340233768...`, `zeta=0.0013337777119...` and bound `0.0015777699899...`. The strict inequality establishes positivity for every string and chain length, including odd and endpoint cases. It is an all-length argument rather than a finite-chain extrapolation.

Constant-width prefix contraction and absolute-error probability control provide an independent polynomial finite-bit sampler. Exponentially small prefix masses require `O(N+log(N/epsilon))` guard bits; direct arithmetic uses `O(N^2)` operations, or `O(N)` with cached suffixes, on fixed-size objects. Physical random bits and finite lazy-comparison tails are charged separately from arithmetic precision.

The excerpt retains a failure example: at the separately specified `p_Q=q=1/200`, `t_i=0.55`, the exact eight-site inverse has three negative entries, minimum about `-2.6064203784e-7`. This invalidates that route's input-label sampler at those settings; it does not rule out all bounded factories.

## What the truncated acquisition section actually supplies

Calibration compares the same positive source law, computed from an acquired parameter, through actual and estimated forward fault processes. Data processing and Pinsker bound output discrepancy by square-root relative entropy of `F` native faults plus `K` independent reference roots. History-erasure discrepancy is paid separately. No global inverse-condition-number amplification appears.

On the stated fixed positive-rate domain, `F,K=O(N)` and uniform root sensitivity give sufficient parameter accuracy `O(epsilon/sqrt N)`. The excerpt displays assay shot scaling `O(N epsilon^-2 log(1/delta_acq))` and then **ends mid-sentence**. No uniform zero-rate endpoint, omitted remaining resources, final total bill, optimality result or missing theorem is inferred from that truncated tail.

The activity summary and available introduction explicitly state that noisy classical selection/delivery are paid and no total-resource advantage is earned. Generic block/library constants remain enormous; the explicit cluster route avoids those particular constants but does not establish an engineering or total-cost advantage. Calibration, protected classical randomness/computation, links, history-erasing trees and resets remain substantive resources.

The full visible response remains in the original producer chat, but Capital did not claim or reopen that tab. The complete response tail and original package are source-delivery dependencies. The archived excerpt is neither labelled complete nor used to reconstruct missing proof/audit/report files.
