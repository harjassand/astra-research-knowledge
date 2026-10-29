# Radially thickened positive-probe oracle theorem — v2
2026-10-29. Proposed theorem at an EXACT convex-body oracle scope. This replaces the draft's affine-measure extension by a full-dimensional construction. It does NOT replace the previously accepted finite signed-feedback algorithm: finite-precision sampling/conditioning remains unresolved.

## Setup
Fix a star edge. At time t, conditional on the actual prior history, the physical Bell-sign probe has Bernoulli outcome Y with mean q_t(C)=vec(C)^T H_t vec(C), C in SO(3), H_t positive semidefinite. Current settings are private and the source is nonanticipating. A fixed C* has H_t vec(C*)=0 for every realized history under the common-algebra promise. No excitation lower bound is imposed. The preceding draft derives the actual one-source-call sign probe; numerical nonunital and arbitrary-channel checks are supplied separately.

Use quadratic features phi(C)=vec(C)vec(C)^T, represented in their actual35-dimensional linear span. The ordinary hull has affine dimension34 because trace(phi)=3. Define instead
 A={alpha phi(C): C in A_grid, alpha in[1/2,1]},
 K=conv A=conv{phi(C)/2,phi(C): C in A_grid}.
Universally, the45 symmetric quadratic coordinates satisfy ten independent homogeneous identities: three off-diagonal row inner products, three off-diagonal column inner products, two row-norm differences and two column-norm differences. The six off-diagonal relations have disjoint monomial supports; the four diagonal-square relations are independent row/column-sum differences and are disjoint from those six. Thus the linear span is at most35 for EVERY rotation, not merely the sampled grid. Include the supplied fixed rational anchor grid, whose nonzero35-by35 minor proves the matching lower bound. Radial thickening makes K full-dimensional in that35-dimensional span and excludes zero. No nonexistent free zero-loss physical action is added.

For any x in K, alpha(x)=Tr(x)/3 lies in[1/2,1] and x/alpha(x) belongs to conv{phi(C)}. Solve a finite LP for its convex decomposition and sample a genuine rotation C from it. This is exact unbiased feature rounding. Report the bounded scalar Z=alpha(x)Y, NOT the exact unknown mean q_t(C). Then
 E[Z|history,x]=ell_t dot x, 0<=Z<=1, Z²<=Z.
The expected physical failure probability is at most twice the expected reported loss. The scaled action alpha(x)phi(C) belongs to A; its conditional mean equals x. Linear optimization over A uses only alpha endpoints and enumeration over the rotation grid.

## Bernoulli/scaled-Bernoulli extension of the potential argument
Use the m=0 exponential-density/truncated-covariance algorithm from Ito–Hirahara–Soma–Yoshida (NeurIPS2020), Theorem1/Appendix B, on K. Let S_t be the exact uncentered second moment of its truncated distribution and use ghat_t=Z_t S_t^-1 x_t. Conditional unbiasedness follows from E[Z|x]=ell_t dot x. The deterministic potential argument depends on the scalar observation only through its bound and square; substitute Z everywhere. All translations back to true predictable loss use conditional unbiasedness. Appendix B's truncation and covariance-comparison steps concern the sampler geometry, unchanged here. The full-dimensional K removes the volume ambiguity of the unthickened feature hull.

For T>=2, d=35, gamma=4log(10dT), eta=1/(8d gamma²), the step-size condition holds. Let X=E sum_t Z_t and L*=E sum_t ell_t dot a*. The resulting inequality is
 X-L* <= X/2+8d²gamma²logT+3,
 so X<=2L*+16d²gamma²logT+6.
Therefore the PHYSICAL cumulative failure probability satisfies
 E sum_t q_t(C_t) <=4L*+32d²gamma²logT+12.
This is an expected predictable-loss statement, not a simultaneous confidence sequence or a hardware performance guarantee.

## Finite rational rotation net and comparator
Haar orthogonality and q_t(C)<=1 imply Tr H_t<=3. Since H_t vec(C*)=0, q_t(C)<=3||C-C*||F².

Use rational stereographic quaternions
 q(u)=(2u_1,2u_2,2u_3,1-||u||²)/(1+||u||²), u in[-1,1]^3.
Every rotation has a unit quaternion representative with last coordinate nonnegative, whose preimage has ||u||<=1. The stereographic map is2-Lipschitz, and ||R(q)-R(p)||F<=2sqrt2||q-p||. Thus a cubic grid of mesh Delta<=epsilon/(2sqrt6) is an epsilon Frobenius net. Every quaternion and rotation is rational when u is rational. The grid has O(epsilon^-3) points; union with a fixed anchor grid does not change this order.

For epsilon<=T^-1/2, one fixed grid rotation C_j* satisfies q_t(C_j*)<=3epsilon² on every adaptive history. Choose comparator a*=phi(C_j*)/2, so L*<=1.5T epsilon². Hence
 E sum_t q_t(C_t) <=6T epsilon²+32d²gamma²logT+12.
At epsilon=T^-1/2 the bound is O(d²log³T), rather than square-root T. The enumerated grid has O(T^(3/2)) actions, but the regret pays feature dimension35, not the grid cardinality. Enumeration, LP and exact rank reduction are explicit mathematical operations; their enormous cost is not hidden.

## One physical edge query per global round
For m star edges, run m controllers with independent current randomization. Every controller samples its current candidate each global round, for potential use in service/validation. Independently choose learning role with probability p and then one uniform edge. Controller i receives
 Z_i=alpha_i * 1[learning role and selected edge i] * Y_i,
 and receives0 otherwise. This zero is MASKED feedback, not a claim to have measured its unqueried physical loss. Conditional mean is p_edge ell_i dot x_i, with p_edge=p/m, and Z_i²<=Z_i. Each controller's theorem applies to this scaled predictable loss.

For the same epsilon net, summing the bounds and converting back to physical edge risks gives
 sum_t sum_i E q_(i,t)(C_(i,t)) <=6m T epsilon² + (m/p_edge)(32d²gamma²logT+12).
Thus the dimension-free-in-T term becomes O(m² d²log³T/p). The source-call cost is still one full-array use per learning event, not m simultaneous edge observations. Conversion from summed edge loss to protected information, three-role readiness and complete source/control budgets requires the previously established separate transfer/guard arguments. This note does not independently close that integration.

## Explicit oracle and implementation boundary
The theorem assumes exact sampling of the exponentially tilted convex-body law and its prescribed truncation, and exact truncated second moments. The physical response itself is an actual shot; it is NOT an exact-loss oracle. These two facts must not be conflated.

The rational grid and rank certificate provide finite action optimization and finite LP rounding. They do not yet provide a numerically certified adaptive sampler/moment inverse. Approximate covariance conditioning, integration/sampling error, bit precision and runtime have NOT been supplied. A discrete quadrature law cannot be total-variation-close to the continuous law; any proposed discretization must use cell-mass/quantization coupling and moment/potential errors instead. Fixed dimension alone does not make exponentially fine grids polynomial-time. The primary paper's discussion of approximate convex sampling is not silently imported as a proved implementation for this new feedback interface.

Consequently this is a valuable oracle-relative gap-free first-order bridge, not a finished practical controller. The previous finite signed-feedback construction remains the implemented fallback. No claim of a physical speedup, small usable constants, identification of an unexcited frame, novelty of small-loss bandits, or general recovery without a common algebra is made.

## Primary premise
Ito, Hirahara, Soma and Yoshida, Tight First- and Second-Order Regret Bounds for Adversarial Linear Bandits, NeurIPS2020, Theorem1 and Appendix B. Main paper and complete appendix were read. The new obligation checked here is replacement of exact scalar feedback by bounded unbiased physical feedback; the published first-order theorem is not quoted as if it directly specified quantum shot noise.
https://proceedings.neurips.cc/paper/2020/file/15bb63b28926cd083b15e3b97567bbea-Supplemental.pdf
