# Thermal-cluster example and the available resource boundary

[Return guide](README.md) · [Whole-channel compiler](whole-channel-compiler-and-classical-control.md) · [Complete visible response](P3_BOUNDED_FACTORIES_20261106_VISIBLE_COMPLETE.txt)

## A separate six-layer quantum data circuit

The explicit example is an open cluster chain `H_N=-sum_i J_i K_i`, with endpoint-adjusted `K_i=Z_(i-1) X_i Z_(i+1)` and `t_i=tanh(beta J_i)` in `(1/2,11/20]`. Its Gibbs state is `2^-N product_i(I+t_i K_i)`. For any crossing edge, the target violates the corresponding separable bound `E[K_i+K_(i+1)]<=1`, giving entanglement across every nontrivial bipartition. No stronger mixed-state multipartite classification is inferred.

The six physical data layers are reset, actual-root-controlled CNOT loading, Hadamard, two nearest-neighbor CZ matchings and local delivery. Outgoing data errors, unmatched-site idles and terminal noise count. The sufficient quantum condition is `p_Q<=1/3000`, with classical bit-flip rate `p_C<=min(p_Q,p_cl)` and history-erased root error `q_h<=10p_C`. The number `1/3000` certifies quantum positivity; the complete controller still requires its separate sufficient classical threshold `p_cl`.

Physical Clifford faults become bounded-support convolution in graph-basis labels. The input-label inverse has a signed transfer representation of at most sixteen link states. A signed expression alone is not a physical sampler: the proof supplies an invariant positive cone, with sufficient inequality `zeta<=1/(4R^2+2R)`.

At the certified endpoint, the reported rational evaluation gives `R=12.340233768...`, `zeta=0.0013337777119...` and bound `0.0015777699899...`. The strict inequality establishes positivity for every string and chain length, including odd and endpoint cases. It is an all-length argument rather than a finite-chain extrapolation.

Constant-width prefix contraction and absolute-error probability control provide an independent polynomial finite-bit sampler. Exponentially small prefix masses require `O(N+log(N/epsilon))` guard bits; direct arithmetic uses `O(N^2)` operations, or `O(N)` with cached suffixes, on fixed-size objects. Physical random bits and finite lazy-comparison tails are charged separately from arithmetic precision.

The excerpt retains a failure example: at the separately specified `p_Q=q=1/200`, `t_i=0.55`, the exact eight-site inverse has three negative entries, minimum about `-2.6064203784e-7`. This invalidates that route's input-label sampler at those settings; it does not rule out all bounded factories.

## Acquisition, full resource bill and remaining limits

Calibration compares the same positive source law, computed from an acquired parameter, through actual and estimated forward fault processes. Data processing and Pinsker bound output discrepancy by square-root relative entropy of `F` native faults plus `K` independent reference roots. History-erasure discrepancy is paid separately. No global inverse-condition-number amplification appears.

On a commissioned fixed positive-rate domain, `F,K=O(N)` and uniform root sensitivity give sufficient parameter accuracy `O(epsilon/sqrt N)` and assay count `O(N epsilon^-2 log(1/delta_acq))` at fixed visibility/domain constants. Near unidentified noise-support boundaries, the completed tail retains conservative `O(N^2 epsilon^-2 log(1/delta_acq))` coupling-based acquisition. The better bound keeps inverse-rate constants and commissioning costs; finite observations do not certify future stationarity.

The complete bill includes every quantum calibration/randomness probe in addition to the `O(N)` bounded quantum data stage, classical source generation, channel simulation, mixture solving, precision, protected copying/routing/synchronization, command-tree leaves, physical decoders, gate-library construction, wiring, startup, reset and record erasure. Classical preparation, calibration and random generation precede the bounded data stage. Energy/spacetime include storage, cooling and links; gate counts do not establish joule advantage.

For the general family, the inherited efficient source retains its original numerical convention. A separate rational positive-block-net/finite-convex-feasibility fallback closes finite-bit computability with potentially exponential work. The explicit cluster family has its own polynomial finite-bit source; its favorable six-layer/transfer constants do not transfer to arbitrary noncommuting chains.

The complete comparison credits ideal constant-depth block preparation, faster ideal all-temperature sampling, state precompensation, noisy probabilistic synthesis, graph-state noise tools, full FT/qLDPC interfaces and autonomous correction at their actual contracts. An equally informed ordinary preparer can adopt the same known-state compilation; no separation from that comparator or total-resource advantage is earned.

The endpoint is a known mixed state at release. Arbitrary unknown pure-state delivery, additional holding, apparatus drift/general leakage and practical total-cost advantage are not earned. Stationary independent finite-type noise, bounded ports and declared timing, known computable target and paid routing remain premises. The complete visible source is supplied as native prefix plus rendered overlap; the original package and standalone audit/check artifacts are now delivered unchanged. No Capital source execution or new scientific audit occurred.
