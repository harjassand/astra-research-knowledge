# Stage 2 adversarial audit and attribution correction

No stage1 files were changed. This document qualifies the preserved stage1 result rather than rewriting its history.

## 1. Strongest competing explanation: ordinary optimal design

The ladder optimization is exactly a classical generalized-least-squares (GLS) mean-estimation problem after the coordinate change x_k=log S_k. Suppose observations satisfy Y_k=mu+epsilon_k with known covariance

    K_ij=exp(-|x_i-x_j|).

An unbiased linear estimator with weights w has sum w=1 and variance w^T K w. Its GLS optimum is w=K^(-1)1/(1^T K^(-1)1), with variance 1/(1^T K^(-1)1). Stage1's normalized thermal edge-delay contributions a_k/tau are exactly those estimator weights. Fixing C_total/C_s fixes the observation-domain length log R, and choosing capacities is choosing the interior sample positions.

Thus the entire ladder optimization, including equidistant log-cumulative capacities, can be obtained by conventional OU optimal design without copying a newly revealed thermal algorithm. The already published primary paper by Kiselak and Stehlik, [*Equidistant and D-optimal designs for parameters of Ornstein--Uhlenbeck process* (2008), DOI 10.1016/j.spl.2007.12.012](https://www.sciencedirect.com/science/article/abs/pii/S0167715207004208), explicitly establishes n-point equidistant optimality for the trend parameter. The [authors' institution record](https://research.jku.at/en/publications/equidistant-and-d-optimal-designs-for-parameters-of-ornstein-uhle-2/) corroborates the publication. Only its primary abstract and accessible indexed statements were available; no inaccessible theorem text is quoted or invented.

The algebraic equivalence itself is proved above and in the preserved stage1 proof. The exact-arithmetic code independently computes GLS weights and verifies they equal the thermal attaining weights in 22 designs. This strengthens the novelty correction: **the kernel optimization/equidistance principle is established mathematics.** The heat-capacity interpretation and tree branch-collapse consequence may still have a distinct application-level provenance, but no verified priority for those is established here. A new general optimization principle must not be claimed.

## 2. Full-domain proof audit

The stage1 finite-tree theorem survives the following explicit audit of its real-parameter domain.

* A finite connected positive-conductance tree with a Dirichlet bath has positive-definite L. Normalized node energies form a positive killed linear system; all energy reaches the bath, so the release density is normalized without a favorable postselection fraction.
* Backward mean and second moments solve Lh=c and Lh2=2 diag(c)h for arbitrary positive real capacities. The tree Green function is the shared root-path resistance, including source-interior configurations.
* Nodes in other branches of the bath are never visited before absorption from the source. Their capacities are irrelevant to the moments. Counting them in C_total only weakens the stated bound; they cannot create a counterexample.
* In a source-connected off-path branch, replacing the branch with its total capacity at its attachment preserves the mean exactly. The excess second moment is 2 sum_k R_k sum_{i,j in B_k} C_i C_j H_ij with every term nonnegative. This is algebra over arbitrary positive real parameters, not a sampled-graph inference.
* For arbitrary positive ladder capacities, the inverse-kernel row sums are positive. An interior row sum is (1-rho_left*rho_right)/[(1+rho_left)(1+rho_right)]>0. The unconstrained GLS solution therefore never requires a negative resistance.
* The positive log increments sum to log R. Strict concavity of tanh gives the global equally spaced optimum for all R>1, not merely the geometric integer examples. Monotonicity in node count and capacity ratio completes the branch-collapse comparison.

No logical counterexample to that precisely scoped theorem was found. The independent withheld fixtures are supporting checks of the implementation and algebra:

| Storage nodes | Every labelled tree topology tested |
|---:|---:|
| 2 | 3 |
| 3 | 16 |
| 4 | 125 |
| 5 | 1296 |

Each of the 1440 topologies received a new positive rational capacity/conductance fixture. Means, variance differences, branch penalties and fixed-capacity covariance bounds were evaluated with exact Fractions. All assertions passed. There were 1121 strictly positive branch penalties and 740 cases with irrelevant bath branches. Exact equality was also checked for N=2..12 at cumulative ratios q=2 and q=3, including positive GLS/thermal weights and prescribed mean one. See exact_stress.py and exact_stress_results.json. One rational point per topology is not exhaustive real-parameter testing; the all-real quantifier rests on the governing argument above.

## 3. A physical compatibility qualification to the continuum example

The ideal one-dimensional tapered rod in stage1 has

    ell=sqrt(alpha*tau/(log R+2)),
    A(x)=C_s/(c_v ell)*exp(x/ell),
    length=ell*log R.

For a circular cross section, its largest radius a_max satisfies

    chi := a_max/ell = sqrt[C_total/(pi*c_v*ell^3)].

The taper slope at that end is a_max/(2 ell)=chi/2. Transverse diffusion time divided by the axial scale kappa=tau/(log R+2) is chi squared. A sufficient asymptotic regime for a slowly varying slender one-dimensional approximation is chi much smaller than one. With a specified tolerance chi<=eta_g, this requires

    tau >= (log R+2)/alpha
           *[C_total/(pi*eta_g^2*c_v)]^(2/3).            (1)

This is a compatibility condition, not a new material measurement or a universal lower bound on all rod geometries. It follows directly from the proposed geometry and the ordinary diffusion-time scaling. At fixed material, C_s,R and tau, it cannot be made true just by declaring the rod slender. Geometrically similar rescaling preserves chi when capacity scales as length cubed and diffusion time as length squared.

Accordingly stage1's suggestion that a geometrically similar shape can approach the one-dimensional regime needs this condition. The continuum PDE construction is a conditional idealization, not an unconditional device realization at every prescribed budget. This qualification leaves the finite-tree theorem and its abstract positive-component optimum intact.

## 4. Stronger positive mechanism attempted

The linear-tree blocker does not rule out temperature-dependent conductance. A source reservoir can cool slowly through an OFF link, then close a thermal contact when its own temperature falls through a threshold and discharge quickly. Cold-closing passive switches are demonstrated operations; this does not require inventing a selective detector. The actual integrated response still cannot be inferred from endpoint conductance values.

SWITCH_PROOF.md completes a stronger mathematical representation. For any memoryless G(T) between g_min and g_max, with constant reservoir capacity, it proves the exact global optimum over **all measurable conductance curves**, not just over one favorable step fixture. A functional linear certificate plus Cauchy--Schwarz proves that a single self-temperature threshold is optimal. All leakage is included. Its contrast/precision frontier is

    2[atanh(v)-v]=-log(1-1/K)-1/K,   K=g_max/g_min,
    v=minimum CV squared.

This supplies a usable necessary contrast requirement and an ideal attaining response. It is a mathematical relaxation of ordinary thermal-switch storage, not a physical invention. The ordinary scalar optimizer matches it; a conventional smooth-switch designer was allowed to retune its threshold.

The source/regime obstacle is concrete. The [Dietrich et al. primary manuscript, arXiv:1307.6367v2](https://arxiv.org/html/1307.6367v2) uses a two-temperature assembly and reports full ON performance well below the closure transition. Its endpoint ratio is not a measured local sharp G(T) response during reservoir self-cooling. We did not combine incompatible temperatures into an ideal gate. No actor heat capacity, threshold jitter, response time, charging energy or reset time was invented.

## 5. Actual surviving conclusion

The fixed linear-tree resource law and an ideal nonlinear contrast frontier are supported mathematical objects. The first contains established OU optimal-design mathematics; priority of the thermal consequences is unresolved. The second quantifies the stronger conventional switching route but leaves an integrated calibrated operation unsupplied. Neither establishes a new practical capability or the mission-level advance.
