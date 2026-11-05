# Backward construction: learning every equilibrium intervention

## Decision for the parent

**A complete conditional capability is constructed below, including an exact arithmetic certificate and an executable example. It should not be selected as the civilisation-changing result.** The central sparse-network identification mechanism has a direct predecessor: Hayden, Chang, Goncalves and Tomlin, *Compressed Sensing for Network Reconstruction* (2014), subsequently *Sparse network identifiability via Compressed Sensing*, Automatica 68 (2016), 9–17, DOI [10.1016/j.automatica.2016.01.008](https://doi.org/10.1016/j.automatica.2016.01.008). Their problem is already sparse recovery from experimentally determined sensing matrices, with rank conditions, experiment design, and limitations of convex relaxations. [Primary preprint](https://arxiv.org/abs/1411.4095).

What this attempt earns is a sharp logical distinction: smooth stability alone cannot support cheap uniform learning of all interventions; a sparse quadratic constitutive class supports a complete, data-certified operation. The latter certificate establishes conditioning and ambiguity *within that class*. It does not experimentally establish that the class describes nature globally. No novelty claim is made for either the general obstruction or the sparse identification mechanism. The constants and exact certificate below are an explicit construction, not evidence of a fundamental new discovery.

## 1. Precise desired capability

Let a physical system have energy U on R^d. Applying a constant control h adds work term −h·x. Its equilibrium response is

    G_U(h) = argmin_x [U(x) − h·x].

The intended capability is to acquire a finite experimental model and then predict **every** allowed intervention h in B_2(0,R), with one simultaneous error guarantee

    P_U{sup_{||h||≤R} ||Ghat(h) − G_U(h)||_2 ≤ ε} ≥ 1−δ,

for every admitted physical law U. This is stronger than an average prediction guarantee, or answering one requested intervention with additional experiments. Exact full-state equilibrium observations are initially allowed, computation is unrestricted, and experiments may be chosen adaptively anywhere in R^d. Units are fixed by the energy-curvature bounds; ε/R is the meaningful dimensionless accuracy in the obstruction.

The theory concerns deterministic equilibrium. Finite-temperature Gibbs means, hidden variables, finite observation bandwidth, hysteresis, phase transitions, and quantum measurement costs are not included.

## 2. A generic obstruction that survives strong stability

Admit every C^2 energy satisfying

    (1/2)I ≤ ∇²U(x) ≤ (3/2)I  for all x.

There is a unique equilibrium, no metastability, and the inverse-gradient response has Lipschitz constant at most 2. Nevertheless, any uniformly successful algorithm must use exponentially many equilibrium experiments in the worst case.

### Explicit indistinguishable alternatives

Take U_0(x)=||x||²/2. Choose centers c_j in B_2(0,R), separated by at least 2r. A maximal packing has

    N ≥ (R/(2r))^d,

because the balls of radius 2r around its centers cover B_2(0,R). The perturbation supports may extend outside the intervention domain; this causes no problem.

Define, for ||z||<1,

    ψ(z) = z_1(1−||z||²)^3,

and set ψ=0 outside the unit ball. This function is C^2, including at the boundary. Do not upgrade this assertion to analyticity or C-infinity.

Its gradient and Hessian, writing s=||z||², are

    ∇ψ = e_1(1−s)^3 − 6z_1(1−s)^2 z,
    ∇²ψ = −6(1−s)^2(e_1 zᵀ + z e_1ᵀ + z_1 I)
           +24z_1(1−s)zzᵀ.

The dimension-independent bound ||∇²ψ||_op <4 is proved in Appendix A. Therefore

    U_j(x) = ||x||²/2 + (r²/8)ψ((x−c_j)/r)

belongs to the admitted energy class. If h lies outside the open ball B(c_j,r), then x=h solves ∇U_j(x)=h. Strong convexity makes it the unique solution, so G_j(h)=h=G_0(h). An experiment outside that support reveals nothing about this alternative, even with exact, noiseless, full-state readout.

At h=c_j the force mismatch at x=c_j is (r/8)e_1. Since the gradient is 3/2-Lipschitz,

    ||G_j(c_j)−c_j|| ≥ (r/8)/(3/2) = r/12.

Choose r=25ε. The two response laws then differ by more than 2ε at the allowed intervention c_j.

### Adaptive randomized lower bound

Couple an algorithm under U_0 and U_j with the same random seed. Their transcripts coincide until its first query in B(c_j,r). Let p_j be that hitting probability under U_0. On the no-hit event a common output cannot be within ε of both response laws uniformly, so two failure probabilities at most δ imply

    p_j ≥ 1−2δ.

The supports are disjoint. Consequently the expected number T of experiments under the base system obeys

    E_0 T ≥ Σ_j p_j ≥ (1−2δ)N
          ≥ (1−2δ)(R/(50ε))^d.                 (1)

This holds for δ<1/2 and for finite expected stopping times. It is nontrivial as an exponential-in-d bound when ε<R/50. For example, ε=R/100 gives a lower bound (1−2δ)2^d. This is an information bound; extra computation, learned priors absent from the stated class, and adaptive experiment selection cannot remove it.

### Gaussian observation noise

Suppose the equilibrium oracle returns G_U(h)+ξ, where ξ has independent N(0,σ²) coordinates. The gradient bound

    ||∇ψ(z)|| ≤ (1−s)^2(1+5s) ≤ 32/25

implies ||G_j(h)−h||≤4r/25=4ε everywhere, with zero difference off its support. The conditional Gaussian KL divergence at a query in that support is at most 8ε²/σ². The adaptive likelihood chain rule and data processing for the event that Ghat is uniformly close to G_0 give

    (8ε²/σ²) E_0 N_j ≥ kl(1−δ,δ),

where kl(1−δ,δ)=(1−2δ) log((1−δ)/δ). Thus

    E_0 T ≥ N max{1−2δ, (σ²/(8ε²)) kl(1−δ,δ)}. (2)

For random stopping, apply the chain rule to stopped transcripts under the usual finite-expectation conditions, or first truncate and take the limit. The change-of-measure step is standard; a primary source on this adaptive lower-bound method is Kaufmann, Cappé and Garivier, [*On the Complexity of Best Arm Identification in Multi-Armed Bandit Models*](https://arxiv.org/abs/1407.4443), JMLR 17 (2016), especially their change-of-measure lemma. The present equilibrium specialization is derived above rather than attributed to that paper.

### Complete ordinary upper procedure

Strong monotonicity implies G is 1/m-Lipschitz, with m=1/2 here. Sample a ρ-net of the intervention ball, store each response to accuracy η, and use the closest stored response. The uniform error is at most ρ/m+η.

For exact observations choose ρ=ε/2. A volumetric cover exists with at most (1+4R/ε)^d points. For noisy observations choose ρ=ε/4 and η=ε/2, giving at most (1+8R/ε)^d points. Average M independent measurements per point, with

    M ≥ (4σ²/ε²)(sqrt(d)+sqrt(2 log(N/δ)))².

A Gaussian norm tail bound and a union bound certify all stored responses simultaneously. The total experimental cost is NM and storage Nd scalars. A fully explicit bounding-box grid is also valid: spacing ρ/sqrt(d) gives no worse than (1+2R sqrt(d)/ρ)^d grid points, with an explicit rounding convention. This constructive grid has an extra dimension factor in the cover; no efficient optimal-net construction is assumed.

This is the familiar information-complexity curse. Hinrichs, Novak, Ullrich and Woźniakowski prove related exponential information requirements for smooth numerical integration in [*The Curse of Dimensionality for Numerical Integration of Smooth Functions*](https://arxiv.org/abs/1211.0871), Mathematics of Computation 83 (2014), 2853–2863. That source is related prior methodology, not a claim that its theorem already has exactly our equilibrium oracle or constants.

## 3. Stronger positive question: can locality be made into a complete operation?

Impose the physical constitutive structure

    U(x) = (1/2)xᵀKx,
    K=Kᵀ,  mI≤K≤LI,
    each row of K has at most s nonzero entries.

The interaction graph and coefficients are unknown. The zero-equilibrium reference, degree bound s, and curvature bounds m,L are supplied. Full independent control of every coordinate and full state readout are supplied. These are indispensable experimental resources, not free consequences of observing a network.

With q equilibrium experiments, arrange the applied controls and responses as d-by-q matrices H and X. The exact physical equation is

    KX=H.

The entire unknown local law is therefore recoverable if the measured X separates every possible difference of two s-sparse rows.

### The indispensable operation and its earned certificate

Set A=Xᵀ/sqrt(q), k=min(2s,d), and define

    α = min_{S⊂{1,…,d}, |S|=k} σ_min(A_S).      (3)

When q≥k and α>0, every smaller support is also bounded below by α. This number is computed from the actual acquired data. It does not rely on trusting a nominal random-design claim.

For each row i, enumerate all supports of size at most s, solve least squares on each support, and retain the best fit to y_i=H_iᵀ/sqrt(q). Exact-size-s supports suffice by padding smaller ones. Exact data and α>0 give exact recovery of every row of K. This is a complete finite algorithm.

For measured data Ahat and an actual s-sparse physical row k_i, suppose

    ||Ahat k_i−y_i||≤η.

If a candidate s-sparse row khat_i has measured residual r_i, then its difference from the true row is 2s-sparse and

    ||khat_i−k_i||≤(r_i+η)/αhat.              (4)

A support minimizer has r_i≤η. Hence a common valid row error bound is τ=2η/αhat. An approximate solver is also allowed if its actually checked residual is used in (4). A solver's unsupported declaration of convergence is not a certificate.

### Exact arithmetic implementation of the certificate

The stored measurement matrix consists of rational numbers; a binary64 value is an exact dyadic rational once stored. To certify a proposed rational lower bound a_0>0, check positive definiteness of

    Xhat_S Xhat_Sᵀ/q − a_0² I

for every support S of size k. Clear denominators and use Sylvester's criterion with fraction-free Bareiss elimination. Every division is exact. All positive leading principal determinants certify αhat>a_0 without trusting floating singular values. Fitted-row residuals are checked by exact rational squared norms. If a bound fails, reduce a_0 or acquire more experiments. An exactly rank-deficient support can be detected directly.

The operation is computationally expensive, but finite and implemented in `exact_certificate.py`. It establishes conditioning for the recorded data. Physical noise bounds and the sparsity/quadratic hypotheses remain separate assumptions.

### Why a logarithmic number of random experiments can suffice

Take the q control vectors independently N(0,I_d), with the unknown K fixed before their random selection. For every fixed support S, write K^{-1}P_S=Q_SB_S with Q_S orthonormal. The matrix HᵀQ_S/sqrt(q) is a q-by-k Gaussian matrix, and σ_min(B_S)≥1/L.

A 1/4-net of the k-dimensional unit sphere has size at most 9^k. For each net point the χ² concentration inequality gives

    P{| ||HᵀQ_Sv||²/q −1 |>1/4} ≤ 2 exp(−q/128).

Union over the net and all binomial(d,k) supports. The quadratic-form net inequality upgrades this to operator covariance error at most 1/2. Therefore if

    q ≥ 128[log(2/δ)+log binomial(d,k)+k log 9], (5)

then α≥1/(sqrt(2)L), in particular α≥1/(2L), with probability at least 1−δ. This is O(s log(d/s)+log(1/δ)) experiments when 2s≤d. Constants are deliberately conservative. Actual measured certificates can pass at much smaller q.

For exact noiseless data q=k already gives α>0 almost surely, because each of finitely many support submatrices has full rank. This statement relies on arbitrarily fine precision; it promises no practically useful margin against noise.

### Measurement errors, missing weak edges, and all-intervention prediction

Suppose each recorded state coordinate has absolute error at most ν. Since every physical row satisfies ||k_i||_1≤sqrt(s)L, the true-row residual in normalized data obeys

    η=ν sqrt(s)L.                            (6)

Known control error bounded by β per coordinate adds β to η. If the original random design has α≥1/(2L), then

    αhat ≥ α−ν sqrt(k) ≥ 1/(4L)

provided ν≤1/(4L sqrt(k)). One can instead use the stronger measured exact certificate a_0.

To obtain an operator guarantee independent of d, threshold the reconstructed rows: discard every coefficient of magnitude at most τ. A truly zero coefficient is always discarded. A discarded true coefficient has magnitude at most 2τ. Symmetrize the thresholded matrix to obtain Ktilde. Its support remains inside the true symmetric graph, and each entry error is at most 2τ. Thus

    ||Ktilde−K||_op ≤ Δ := 2sτ.               (7)

No lower bound on the smallest nonzero interaction is needed. Weak edges may be omitted, with their error included in Δ.

If Δ<m, Ktilde remains positive definite. The resolvent identity then gives, simultaneously for every h,

    ||Ktilde^{-1}h−K^{-1}h||
       ≤ [Δ/(m(m−Δ))] ||h||.                 (8)

On ||h||≤R this is at most ε when Δ≤m²ε/(R+mε). Combining the conservative random-design bounds yields Δ≤16ν s^{3/2}L². A sufficient precision is therefore

    ν ≤ [m²ε/(R+mε)]/[16s^{3/2}L²],

together with the injectivity noise limit above. If independent per-coordinate observation noise has variance σ², averaging

    M ≥ (2σ²/ν²) log(2dq/δ_noise)

replicates at each control gives the required coordinate bound by a Gaussian union bound. Allocate probability separately between random-design failure and measurement noise. Deterministic settling errors must be included in the same ν budget.

## 4. Executed example and exact certificates

`verify_boundary.py` builds a sixteen-variable symmetric ring with three nonzeros per row, including the diagonal. Ten Gaussian controls produce 160 scalar state outputs. It enumerates 560 candidate supports per fitted row and all 8,008 six-coordinate supports for the ambiguity certificate.

The exact-data reconstruction has maximum coefficient error 2.67e−15 in floating arithmetic. With coordinate perturbations bounded by approximately 1e−6 in the generated example, the floating minimum restricted singular value is 0.02470899. The **formal certificate does not use this floating estimate**: exact integer arithmetic proves αhat>1/64 on every six-coordinate support.

Using L=5/2 and η²=3(5/2)²(10−6)², all sixteen fitted-row residuals pass exact rational checks; the largest squared residual uses 8.23% of its budget. The generating true rows also pass an exact residual check, using 10.76% of the budget. This latter check uses knowledge of the simulated ground truth and is not an operation available to an experimenter with unknown K. Exact integer positive-definiteness checks separately confirm m=3/2 and L=5/2 for the simulated physical matrix.

The rational output matrix uses exact threshold comparisons and exact symmetrization. For it, the certified response-operator error is at most 0.001481301. Thus the output law predicts **every** control ||h||≤1 to that error, conditional on the constitutive assumptions and the true residual budget. The observed floating operator error is about 4.68e−7; this tighter numerical observation is not substituted for the theorem's certificate.

Repeated identical controls yield a zero restricted singular value, correctly failing the certificate. The energy-bump check locates its Hessian maximum at approximately 3.952588797 and its center response separation at 2.7835ε, consistent with the analytic lower bound 25ε/12.

The inputs, raw fitted coefficients, rational final matrix, and certificate parameters are in `certified_network.json`; numerical results are in `verification_results.json`. The exact arithmetic routines verify the hard inequalities rather than merely retesting the same floating estimator.

## 5. Costs and the strongest ordinary alternatives

The sparse operation uses q equilibrations, but reads dq real values and applies q controls with d independently chosen components. Gaussian controls have expected squared Euclidean norm d. Experiment count alone is not the full resource bill. If total available control norm is fixed independently of d, scale the controls down by order 1/sqrt(d); the injectivity margin scales down too, and the required averaging can grow by order d. A fixed bound per actuator instead introduces only logarithmic normalization losses, while total control energy still grows with d.

Support fitting costs d binomial(d,s) least-squares solves. Exact certificate construction checks binomial(d,2s) small Gram matrices. Both are exponential in local degree. This is not an efficient unrestricted algorithm. Sparse solvers such as basis pursuit or Lasso are the ordinary computational alternative when appropriate recovery conditions can be justified; the nearest primary network paper already studies the experimental sparse-recovery formulation and the limits of convex relaxation.

Without sparsity, d independent controls can recover the dense linear response and then its inverse, with polynomial linear algebra. For moderate d and cheap experiments that may be preferable to an exhaustive sparse certificate. There is no claim that the presented construction dominates it.

For one desired intervention in a general strongly convex system, ordinary iterative solution is much cheaper than building a universal surrogate. With a force oracle, the iteration

    x_{t+1}=x_t−[2/(L+m)](∇U(x_t)−h)

contracts distance to equilibrium by (L−m)/(L+m). For m=1/2,L=3/2 that is 1/2 per iteration. A measured force residual rhat with bounded error η_f certifies

    ||x−G_U(h)|| ≤ (||rhat||+η_f)/m.

A proposed state can therefore be certified for its current control with one additional residual measurement, assuming the global curvature bound is known. The offline exponential obstruction does not prohibit this targeted operation.

Equilibrium control itself can emulate an imposed-state force experiment. To find h*=∇U(x_target), iterate

    h_{t+1}=h_t+[2mL/(m+L)](x_target−G_U(h_t)).

The inverse-gradient Jacobian has eigenvalues between 1/L and 1/m, so this is a contraction with the same factor (L−m)/(L+m). Once ||G_U(h_t)−x_target||≤ζ, the inferred force differs from ∇U(x_target) by at most Lζ. This operation requires full control and suitable available control range. It is a standard inverse-gradient fixed-point construction, not a newly discovered physical capability.

## 6. What the attempt establishes, and what it cannot claim

The negative and positive constructions are compatible. Generic smooth stability leaves exponentially many localized changes unobserved. The sparse quadratic class excludes those changes by assumption. Acquired-data rank certificates can establish identifiability and robustness inside that restricted class. They cannot establish that all omitted nonlinear changes are physically absent: a perturbation supported away from every observed intervention produces identical data while violating the global quadratic hypothesis.

Consequently this is an honest complete boundary attempt, but its successful mechanism is established sparse identification, and its indispensable constitutive structure was supplied rather than derived from physics. It fails the user's requested scale of conceptual novelty. It should be retained as a concrete rejected candidate and as a warning against claiming that a model-class conditioning certificate validates universal scientific understanding.

## Appendix A: the dimension-independent bump bound

Put z=sqrt(s)u and q=|e_1·u|. On span{u,e_1}, the Hessian equals 6sqrt(s)(1−s) times the symmetric matrix

    [ q(7s−3)       −(1−s)sqrt(1−q²) ]
    [ −(1−s)sqrt(1−q²)   −q(1−s)    ].

Every remaining eigenvalue is −6sqrt(s)q(1−s)², bounded by the norm of the displayed block. The block norm divided by its prefactor is

    f(s,q)=2q|2s−1|+sqrt((1−s)²+4q²s(2s−1)).

Maximization over q in [0,1] gives three ranges:

- For 0≤s≤1/5: 6sqrt(s)(1−s)(3−7s). Its maximum occurs at s*=(15−2sqrt(30))/35 and equals approximately 3.952588797. A rational enclosure 0.115<s*<0.116 gives the rigorous bound 6(0.341)(0.885)(2.195)=3.97450845<4.
- For 1/5<s<1/2: 6(1−s)^(5/2), at most 6(4/5)^(5/2)<4.
- For 1/2≤s≤1: 6sqrt(s)(1−s)(7s−3), at most 6 max_s (1−s)(7s−3)=24/7<4.

The d=1 case is the q=1 restriction; s=0 follows directly. Thus every dimension has ||∇²ψ||<4, which completes the strong-convexity check in the lower-bound construction.
