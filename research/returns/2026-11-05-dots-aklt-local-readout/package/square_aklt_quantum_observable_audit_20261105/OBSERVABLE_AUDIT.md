# Quantum observables from exact square-AKLT loop samples

## Acquired scope and boundary state

The sampled positive loop gas is the coherent-state norm of the open-rectangle spin-2 AKLT PEPS with identity on its dangling virtual boundary:

sigma_R = V_R I_virtual V_R^dagger / Tr(V_R I_virtual V_R^dagger).

This is a specified ground-state ensemble, not the maximally mixed physical ground-space projector and not a thermal state at positive temperature. Equivalently attach one spin-1/2 leaf for each missing boundary bond, form the decorated graph VBS, and trace the leaves. Integrating their spheres removes each leaf factor. Every core remains spin2, including boundary cores. Without this convention, a natural graph VBS has spin degree/2 at its boundary and different observable coefficients.

The ensemble is SU(2)-invariant. Thus onsite <S_i^2>=6, <S_iz^2>=2, and <(S_iz^2-2)^2>=14/5, including boundary cores.

Exact sampling removes finite-volume burn-in and autocorrelation bias. It does not make a finite sample mean equal its expectation, prepare a quantum state, certify a spectral gap, or remove arbitrary observable sign cancellations.

## 1. Coherent-state conversion

With normalized sphere measure and spin-S coherent states, the exact contravariant symbols are

S^a <-> (S+1)n_a,
(S^z)^2 <-> ((S+1)(2S+3)/2)n_z^2 - (S+1)/2.

For spin2, set Q_i=(S_i^z)^2-2. Its symbol is (21/2)(n_iz^2-1/3). These identities are operator identities under the coherent resolution of identity, not the covariant expectation <n|S|n>=S n. Confusing the two gives the wrong factor4 instead of9 in distinct-site spin correlations.

The local beta-integral check is exact: normalized diagonal coherent integration gives integral(n_z^2 |m>)=(2m^2+3)/21, so multiplying by21/2 and subtracting3/2 gives m^2 for every spin2 m.

After the bipartite change n_i -> eta_i n_i, the classical norm is integral product_edges(1+n_i dot n_j). The routed-loop activity is w_gamma=3^(1-L_gamma)(3/5)^r_gamma, with hard edge overlap and factor3/5 per shared vertex otherwise.

## 2. Dipolar correlations via an open-path insertion

For distinct cores i,j, let G_ij be the positive staggered classical correlation. Add a distinguished auxiliary factor1+t n_i dot n_j to the classical norm. The coefficient of t consists of loops containing that auxiliary edge. Removing it gives exactly one routed edge-simple path p oriented i to j. This is a separate parallel edge when i,j are neighbors.

The resulting identity is

<S_i dot S_j> = 9 eta_i eta_j G_ij,
G_ij = sum_(p:i->j) 3^(-L_p)(3/5)^r_p E_loop[product_gamma delta(p,gamma)].

Here r_p includes degree3 physical endpoints, which become degree4 after adding the auxiliary edge. Internal degree4 contacts also count. There is no factor2L: the source edge fixes the path orientation and rooting. Its loop color factor3 cancels the extra factor1/3 from the auxiliary edge, leaving3^(-L_p). The source-free partition function is exactly the denominator already sampled, so no ratio of uncertain Monte Carlo normalizers is needed.

This identity was independently audited against the constructor's derivation. The separate observable-join lane has exhaustive direct-VBS checks, including endpoint revisits; its artifacts should accompany implementation claims.

Suppose an exact proposal oracle has known normalizer C and its accepted path intensity equals the path activity above. An independent exact closed-loop sample gives

X = 9 eta_i eta_j C * 1_valid_path * product_gamma delta(p,gamma).

It is unbiased, real, and bounded in absolute value by9C, with one deterministic parity sign. Keeping the product is preferable to adding another acceptance coin. If it is Bernoulli-thinned, Var(X)=81(C G_ij-G_ij^2), at most81 C^2/4. The unthinned product has no greater variance.

The supplied pair normalizers are approximately C_(1,0)=0.602448, C_(1,1)=0.440631, C_(2,0)=0.347172, C_(3,0)=0.220916. Their exact implementation is owned by the observable-join lane. For an all-endpoint oracle with B approximately65.8844, an unbiased equal-time staggered correlation-sum estimator is6+9B times its success variable. Its range width is about593: volume-independent amplitude is not the same as a small variance. Far-separated relative accuracy remains a rare-event problem, with Bernoulli relative variance C/G_ij-1.

One can amortize a closed-loop sample across many independent path proposals, then treat each averaged loop sample as an independent batch. This reduces auxiliary proposal noise without pretending all within-batch observations are independent.

## 3. Direct closed-loop quadrupolar estimator

This family needs no open-path proposal. In a routed loop sample let d_i be occupied degree, in{0,2,4}, and m_iell in{0,1,2} count visits of loop ell to i. Thus sum_ell m_iell=d_i/2.

For distinct i,j,

Y_ij = 98 * sum_ell m_iell m_jell / ((d_i+3)(d_j+3))

is an unbiased estimator of <Q_i Q_j>. It is nonnegative and at most8.

Derivation: temporarily color each loop independently and uniformly by one of three Cartesian colors. At a vertex with d original legs, inserting n_z^2 changes its spherical moment by the exact factor(1+2m_z)/(d+3). In the pairing expansion, the two added z legs either pair together, or attach in two orders to one original paired visit. Since both inserted indices are z, the latter forces that original pair's color to z without changing the underlying routed loops. This local reduction is valid independently at distinct insertion sites.

The spin2 symbol consequently gives

Q_i conditional estimator = 21/(d_i+3) * sum_ell m_iell (1_(color_ell=z)-1/3).

Independent loop colors have centered covariance2/9 when their loop labels coincide and zero otherwise. Integrating colors yields exactly the coefficient98 above. Shared-core separate loops and self-contacting single loops must remain distinguished; the multiplicity m_iell is essential.

The bound follows from sum_ell m_iell m_jell <= (d_i/2)(d_j/2), maximized at d_i=d_j=4. Thus Var(Y)<=16, and also Var(Y)<=8 E[Y]-(E[Y])^2. Hoeffding gives absolute-error epsilon with failure delta after n>=32 epsilon^(-2) log(2/delta) iid samples. This bound is valid but often very conservative. Small distant correlations still have rare-event relative-error cost.

A product of distinct-site S_iz^2 operators also has a direct colored-loop estimator: multiply F_i=(21/2)(1+2m_z(i))/(d_i+3)-3/2. Each F_i lies in[0,6]. General k-site products therefore have a6^k range bound, not an efficient universal measurement sampler.

By SU(2) invariance, the contracted rank2 tensor correlation is(15/2) E[Y_ij]. For Q_i^{ab}={S_i^a,S_i^b}/2-2 delta_ab,

Q_i:Q_j = (S_i dot S_j)^2 + (S_i dot S_j)/2 -12.

Combining the dipolar and quadrupolar estimators therefore gives normalized biquadratic correlations as well. Fixed-sublattice sign and ordinary subtraction appear, but no fluctuating partition-function sign denominator is introduced for these observables.

## 4. Structure factors and observable cost

For Qzz define u_iell=m_iell/(d_i+3). The per-site structure-factor estimator is

14/5 + (98/N) sum_ell [ |sum_i exp(ik dot r_i) u_iell|^2 - sum_i u_iell^2 ].

The onsite14/5 must be inserted explicitly; squaring a contravariant symbol at the same site is invalid. Each wavevector costs linear work in the occupied loop visits, rather than enumerating all site pairs. At k=0 the offsite contribution is nonnegative. Arbitrary momenta introduce real cancellations, not a Boltzmann sign problem. A loop configuration can likewise produce all chosen translation-averaged pair separations cheaply.

`verify_quadrupole_identity.py` compares exact rational coherent monomial integrals to the complete routed-loop measures on a square and two touching squares. The square gives<Q_iQ_j>=7/50; touching squares give7/50 for center/outer and1/500 for opposite outer sites. The latter tests the crossed single-loop contributions. All identities pass exactly.

## 5. Strongest baseline and realistic payoff

AKLT ground-state observables were already accessible to sign-free valence-bond Monte Carlo. Wierschem and Beach (2016), arXiv1603.03444, use local flavor permutations and faster combined bond-spin updates. Their standard spin-half-flavor loop-connectivity estimator has coefficient3/4, and summed loop lengths give staggered magnetization. They also evaluate biquadratic and four-spin correlations. This is a different loop representation, so its connectivity formula must not be copied into the present O(3) routed gas.

Source: https://arxiv.org/abs/1603.03444 . The separate baseline auditor is examining the earlier worm implementation. No matched speed superiority over these mature methods has been established.

The acquired advantage is an exact finite-volume iid law with a known boundary convention and bounded unbiased estimators. It supports independent reference data and finite-sample guarantees without assuming a burn-in duration or integrated autocorrelation time. Existing MCMC can still be faster per useful accuracy, especially for large volumes, rare correlations, and extensive collections of observables.

Current constructor benchmarks for the closure-aware exact sampler are approximately0.067 seconds per32x32 sample,0.48 per64x64,2.39 per128x128, and11.8 per256x256, with few samples at the largest size. These are prototype measurements, not complexity guarantees or optimized comparisons. The worst-case Hoeffding bound for one Qzz pair at absolute error0.01 and95% confidence requires about1.18 million samples, illustrating why exactness alone is not a practical high-precision speedup. Translation averaging, color integration, and batching path proposals can reduce observed variance substantially; any reported errors must distinguish observed standard errors from rigorous confidence bounds.

Nothing here establishes a sign-free spectral-function or excitation-gap algorithm. Generic observable symbols, large-support products, nonbipartite loops, and imaginary-time Hamiltonian projections can reintroduce cancellations or genuine sign problems.

## 6. Additional exact checks and uniform equal-time bound

Two independent direct PEPS/VBS contractions confirmed all six2x2 core-pair quadrupole values7/50. The implementation now accumulates pair-estimator numerators as integers: every nonzero Y value is a multiple of1/25, so translation sums require only one final division.

A100-sample32x32 benchmark took6.9566seconds, of which0.0228seconds evaluated four horizontal translation-averaged separations. At distances1,2,4 the sample means were0.353954,0.0601775,0.00295625 and empirical standard errors0.005812,0.002581,0.000589. These are not rigorous confidence intervals. No distance8 event occurred; the resulting zero empirical variance is not evidence of exact zero correlation or zero uncertainty.

The positive repulsive gas has loop occupation probability at most its activity. Let S2,T2,M4 be the certified length-weighted root masses for degree-two straight, degree-two turning, and degree-four loops. Exact enumeration through length12 gives unweighted lower bounds U2=382856/1476225 and U4=2884/1476225. For a fixed core i, subtracting j=i and using denominator5 for a degree-two root and7 for a degree-four root yields

sum_j <Q_i Q_j> <=14/5 +(98/25)(S2+T2-U2)+(28/5)(M4-2U4) <10.701424.

To justify the subtraction at boundaries, first extend the finite-box nonnegative weighted(L-1) and(L-2) sums to the infinite lattice, then subtract its exact unweighted lower bounds. One must not pretend those infinite-lattice lower bounds hold inside every finite box. The resulting inequality is uniform in the finite box and its virtual-identity boundary ensemble. It is an equal-time fluctuation bound, not a static/Kubo susceptibility bound. The exact conservative rational evaluation is in quadrupole_uniform_bound.json.

## 7. Explicit clustering certificates and prior-art limit

The independent trail witness reconstructs a rooted all-endpoint generating mass C<97.968 at tilt tau0.06. Since path dressing is at most1, it gives the quantitative bound |<S_i dot S_j>| <=881.712 exp(-0.06 dist(i,j)). For the direct quadrupole estimator, occupation<=activity, every connecting loop has length at least2dist, and rooted counting gives sum_gamma m_i w_gamma exp(tau L) <=(3/2)C. Hence <Q_i Q_j> <=822.9312 exp(-0.12 dist(i,j)). These are loose supporting bounds for the specified boundary ensemble.

Exponential spin two-point decay of square-lattice spin2 AKLT is not new: Kennedy, Lieb and Tasaki, Journal of Statistical Physics53,383–415(1988), DOI10.1007/BF01011563, already established it for periodic boundaries. The present numerical constants and finite-boundary bookkeeping must not be sold as a newly available physical phenomenon or a gap proof. Primary publication metadata: https://experts.arizona.edu/en/publications/a-two-dimensional-isotropic-quantum-antiferromagnet-with-unique-d/ .
