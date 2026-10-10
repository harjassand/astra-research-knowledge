# Independent stress test of the inverse-variance chord form

Date: 2026-10-10. This document contains independent calculations, not a literature-priority claim or a proof of the universal conjecture. No claimed recent KLS theorem is used.

## 1. Definition and result summary

Let μ be a full-dimensional probability measure on Rⁿ, let U be uniform on Sⁿ⁻¹, and condition X on Y=P_{U⊥}X. Write T=U·X and σ²(Y,U)=Var(T|Y,U). For the examples below this is positive and finite for almost every fiber. Define

    Q_μ(f)=E_U E_Y[Var(f(X)|Y,U)/σ²(Y,U)].

The proposed inequality is

    Q_μ(f) ≥ c Var_μ(f)/(n ||Cov(μ)||op).                      (NC)

Results:

1. Every affine test has Q_μ(a·x+b)=|a|²/n, for any μ.
2. Every nondegenerate Gaussian satisfies (NC) for all L² tests with the sharp constant c=1, even with arbitrary covariance anisotropy.
3. The constant c=1 fails for a uniform ball in every dimension n≥2. An explicit test on the unit disk gives normalized quotient 373/385<1. A two-dimensional polynomial subspace has minimum about 0.946967 in dimension 5. These are fixed-factor failures, not counterexamples to a positive universal c.
4. Necessarily c≤1/4. This follows rigorously from the isotropic log-concave family Exp(1)×[-√3,√3]ⁿ⁻¹ and a small-chord limit. More generally, padding *any* fixed-dimensional measure with cube factors recovers its ordinary gradient Dirichlet form in the limit. Thus a uniform (NC) with constant c would imply the covariance Poincaré bound with constant exactly 1/c; the usual extra one-dimensional comparison constant is unnecessary for this implication.
5. The associated inverse-variance clock has infinite stationary mean rate for a square. This does not invalidate the analytic form, and does not by itself establish explosion. It does obstruct treating the form as an automatically finite-cost accelerated hit-and-run sampler.
6. No decisive counterexample to (NC) with some c>0, and no non-circular general proof, is obtained here.

## 2. Affine functions: exact and distribution-free

For f(x)=a·x+b and a fixed fiber, f(y+tu)=a·y+b+(a·u)t. Therefore

    Var(f|Y,u)/σ²(Y,u)=(a·u)².

Averaging gives Q_μ(f)=|a|²/n. Since Var_μ(f)=aᵀΣa, the normalized quotient

    n||Σ||op Q_μ(f)/Var_μ(f)=||Σ||op |a|²/(aᵀΣa)

is at least one, with equality on a maximal-covariance eigenvector. Affine tests alone therefore cannot expose any bottleneck.

## 3. Exact Gaussian proof

Let μ=N(m,Σ), Σ positive definite. Translation does not matter, so write X=Σ^{1/2}Z with Z standard Gaussian. For fixed u put

    r=uᵀΣ⁻¹u,
    v=Σ⁻¹/²u/√r.

A physical fiber parallel to u becomes a standard-Gaussian fiber parallel to the unit vector v. Its physical coordinate T has conditional variance 1/r. Thus, writing g(z)=f(Σ^{1/2}z),

    Q_μ(f)=E_u r ||g-E[g|P_{v⊥}Z]||²_{L²(γ_n)}.

Decompose g into orthogonal homogeneous Hermite chaoses. On chaos k≥1, identify a component with a symmetric k-tensor F, retaining the usual common k! norm factor. Conditional expectation onto P_{v⊥}Z is represented by P^{⊗k}, P=I-vvᵀ. Consequently its contribution to the conditional variance is

    k! <F,(I-P^{⊗k})F>.

Because the k coordinate-factor projections commute,

    I-P^{⊗k} ≥ (1/k) Σ_{j=1}^k (vvᵀ)_j.                  (1)

Indeed, on their simultaneous eigenspaces, if exactly m factors lie along v, the two eigenvalues are 1_{m≥1} and m/k. Also

    E_u[r vvᵀ]=Σ⁻¹/² E[uuᵀ] Σ⁻¹/²=Σ⁻¹/n.

Average (1), multiply by k!, and use λmin(Σ⁻¹)=1/||Σ||op:

    Q_k ≥ k! ||F||²/(n||Σ||op).

Sum over chaoses. Nonnegative orthogonal contributions justify passage to an arbitrary L² function by monotone convergence, even if Q is infinite. This proves

    Q_μ(f) ≥ Var_μ(f)/(n||Σ||op).

An affine test in a maximal-eigenvalue direction attains equality.

## 4. Uniform ball: the sharp Gaussian constant fails

Let μ be uniform on the ball B_R⊂Rⁿ. Its covariance is (R²/(n+2))I. For fixed u, a fiber has the form y+tu, |y|²=s, with t uniform on [-a,a], a²=R²-s. Its moments are

    E[t²]=a²/3, E[t⁴]=a⁴/5, E[t⁶]=a⁶/7.

The projected radial variable s/R² is Beta((n−1)/2,3/2). In particular,

    E[s]=(n−1)R²/(n+2),
    E[a²]=3R²/(n+2),
    E[s²]=(n−1)(n+1)R⁴/((n+2)(n+4)),
    E[sa²]=3(n−1)R⁴/((n+2)(n+4)),
    E[a⁴]=15R⁴/((n+2)(n+4)).

Consider f₁(x)=x₁ and f₃(x)=x₁|x|². They have mean zero. Their covariance matrix C and Q-bilinear matrix A are

    C₁₁=R²/(n+2),
    C₁₃=R⁴/(n+4),
    C₃₃=R⁶/(n+6),

    A₁₁=1/n,
    A₁₃=R²(n+4/5)/(n(n+2)),
    A₃₃=R⁴(35n²+154n+36)/(35n(n+2)(n+4)).       (2)

Derivation of the off-diagonal entry: on a fiber,

    f₁=y₁+u₁t,
    f₃=y₁s+u₁st+y₁t²+u₁t³,

so Cov(f₁,f₃)/Var(t)=u₁²(s+3a²/5). Averaging gives A₁₃. The same expansion gives

    Var(f₃)/Var(t)
      =u₁²(s²+(6/5)sa²+(3/7)a⁴)+(4/15)y₁²a²,

which yields A₃₃ from the listed radial moments and rotational symmetry.

Set D=nR²A/(n+2)−C. Then D₁₁=0 and

    D₁₃=4R⁴(n−1)/(5(n+2)²(n+4))>0              (n>1).

A positive semidefinite matrix with a zero diagonal entry must have the corresponding off-diagonal entries zero. Hence D is not positive semidefinite: c=1 fails for every n≥2.

### A completely explicit disk test

Take n=2, R=1 and f(x)=x₁(1−|x|²/2). Then

    Var(f)=11/96,
    Q(f)=373/1680,
    n||Σ||op=1/2,

and therefore

    n||Σ||op Q(f)/Var(f)=373/385≈0.96883117<1.

No numerical approximation is required for this counterexample to c=1.

For reference, the smallest generalized eigenvalue of (nR²A/(n+2), C) is

    n=2:    0.96691552
    n=3:    0.95347903
    n=4:    0.94831174
    n=5:    0.94696702
    n=10:   0.95463760
    n=20:   0.96979401
    n=50:   0.98565754
    n=100:  0.99241958.

These values concern only the displayed polynomial subspace; they are upper bounds on the full normalized spectral gap, not its exact values.

### Other quadratic checks

For f(x)=|x|²,

    Q(f)=4R²/(5(n+2)),
    Var(f)=4nR⁴/((n+2)²(n+4)),

so its normalized quotient is (n+4)/5.

For a trace-free symmetric A and f(x)=xᵀAx,

    Q(f)=4R² tr(A²)(5n+2)/(5n(n+2)²),
    Var(f)=2R⁴ tr(A²)/((n+2)(n+4)),

so its normalized quotient is

    2(n+4)(5n+2)/(5(n+2)²).

Neither quadratic sector alone approaches zero.

## 5. Rigorous small-chord padding limit

### One-coordinate version

Let ν be a nondegenerate log-concave probability law on R; in the application ν is Exp(1). More generally, the proof applies to a base density for which the product's conditional line variances are positive and finite on almost every relevant fiber. Mere existence of a possibly zero variance is insufficient, so discrete base laws are not included in this assertion. Set

    μ_n=ν⊗Unif[-a,a]^{⊗(n−1)}.

Let f:R→R be C¹ with bounded, uniformly continuous derivative, and consider F(x)=f(x₁). Then

    lim_{n→∞} n Q_{μ_n}(F)=∫ |f′|² dν.                  (3)

We prove this without using log-concavity, a Poincaré inequality, or a mixing theorem.

Couple all dimensions using independent G_i∼N(0,1), Z_i∼Unif[-a,a], i≥2, and X₁∼ν. Let u^{(n)}=G_{1:n}/|G_{1:n}|. Parameterize lines as X+sG rather than by physical arclength. The cube coordinates alone impose s∈[-A_n,B_n], where

    A_n=min_{2≤i≤n} backward_distance(Z_i, sign G_i)/|G_i|,
    B_n=min_{2≤i≤n} forward_distance(Z_i, sign G_i)/|G_i|.

For either sign of displacement, these are minima of identically distributed positive variables having positive probability in every interval (0,ε). Thus A_n→0 and B_n→0 almost surely. The entire first-coordinate diameter of the actual conditional fiber is bounded by

    δ_n=|G₁|(A_n+B_n)→0 almost surely.                   (4)

The factor ν can only shorten the fiber's support; it cannot enlarge that bound.

Let M=||f′||∞ and let ω be the modulus of continuity of f′. On a fiber, use two independent conditional points S,T. The variance ratio is a weighted average of squared divided differences:

    Var(F|fiber)/Var(physical T|fiber)
       =u₁² E[(z−z′)² ((f(z)−f(z′))/(z−z′))²]
                    /E[(z−z′)²],                      (5)

with z,z′ the first coordinates; the u₁=0 case is zero. Every divided difference in (5) differs from f′ at any point of that fiber by at most ω(δ_n). Both magnitudes are at most M. Hence, using the sampled X as that point,

    |Var(F|fiber)/σ² − u₁² f′(X₁)²|
       ≤2M u₁² ω(δ_n).                                (6)

Conditional averaging of the right comparison term, followed by global averaging, is legitimate since (6) holds at every point in the fiber. Now

    W_n=n(u₁^{(n)})²→G₁² almost surely,
    E[W_n²]=3n/(n+2)≤3.

Thus W_n is uniformly integrable. Since ω(δ_n)→0 and is bounded by 2M, the expectation of n times the right side of (6) tends to zero. Finally, the direction is independent of X₁ and E[n u₁²]=1. This proves (3).

### Consequence: no universal constant greater than 1/4

Take a=√3 and ν=Exp(1). All covariance eigenvalues of μ_n equal one, so (NC) would give

    nQ_{μ_n}(f(X₁)) ≥ c Var_ν(f).

Pass to the limit in (3). It follows that

    ∫|f′|²dν ≥ c Var_ν(f).                              (7)

For 0<α<1/2 let f(x)=e^{αx} on x≥0. Direct integration gives

    Var_ν(f)=α²/((1−2α)(1−α)²),
    ∫|f′|²dν=α²/(1−2α),

so the quotient is (1−α)². To stay strictly within the hypotheses of (3), first replace f by smooth truncations f_R with bounded uniformly continuous derivatives. For example choose a smooth 0≤χ≤1 equal to one on [0,1] and zero on [2,∞), and put, for x≥0,

    f_R(x)=1+∫₀ˣ αe^{αt}χ(t/R)dt.

Extend smoothly to x<0. For each fixed R the hypotheses hold. As R→∞, dominated convergence gives convergence of f_R in L²(ν) to e^{αx}, and of f_R′ in L²(ν) to αe^{αx}. Applying (7) first to each R then passing R→∞ shows

    c≤(1−α)².

Let α↑1/2. Necessarily c≤1/4.

The order of limits is fixed R, then n→∞, then R→∞, then α↑1/2. No unjustified simultaneous limit is needed.

### Fixed-dimensional base: the local obstruction is retained exactly

The same argument applies to a fixed full-dimensional log-concave measure ν on Rᵈ, padded with n−d cube factors, and F(x)=f(x₁,…,x_d) for C¹ f with bounded uniformly continuous gradient. More general densities require the positive-finite conditional-variance qualification above. Replace |G₁| by |G_{1:d}| and u₁² by |u_{1:d}|² in the error bound. The exact spherical second-moment identity gives

    lim_{n→∞} nQ_{ν⊗cube^{n−d}}(F)=∫|∇f|²dν.          (8)

Here E[(n|u_{1:d}|²)²]=n d(d+2)/(n+2)≤d(d+2), giving the same uniform-integrability argument. If ν is full-dimensional log-concave with covariance Σ, choose each cube coordinate to have variance ||Σ||op. The product covariance operator norm remains ||Σ||op. Therefore a universal (NC) would imply

    Var_ν(f)≤(||Σ||op/c)∫|∇f|²dν

for every such smooth test. This is a direct, constant-preserving implication. It is not a converse proof, and it does not show that the chord form is easier to estimate than the ordinary Dirichlet form.

## 6. Infinite stationary mean clock rate on a square

For uniform measure on a convex body, a chord of length ℓ has variance ℓ²/12, and the projected marginal density is ℓ/Vol(K). Thus the stationary mean rate in a fixed direction is

    E_Y[1/σ²(Y,u)] = (12/Vol(K)) ∫_{P_{u⊥}K} dy/ℓ(y,u). (9)

For a square in R² and any direction not parallel to a side, a support line perpendicular to the projection direction touches a vertex. At projected distance h from that extremum, the small chord has length ℓ(h)=C(u)h for all sufficiently small h, with C(u)>0. The contribution of (9) is a constant times

    ∫₀^ε dh/h=∞.

The exceptional axis-parallel directions have zero spherical measure, so averaging over directions does not repair this divergence.

Interpretation must be narrow and precise:

- This proves infinite stationary expected jump rate for the naive inverse-variance clock.
- It does not prove that the associated closed Dirichlet form fails to exist.
- It does not prove pathwise explosion or preclude a different simulation scheme.
- Smooth/Lipschitz test functions may have finite Q because their squared increments cancel the short-chord singularity.
- In particular, an analytic proof of (NC) would not by itself establish a finite-work, dimension-free sampling algorithm.

## 7. Numerical files and limitations

`ball_exact_tests.py` reproduces the exact-moment polynomial diagnostics above.

`product_exponential_test.py` is an exploratory importance-sampled quadrature calculation for Exp(1)ⁿ. Its original low-dimensional implementation suffered overflows for long, steeply tilted fibers, so low-dimensional output is not trustworthy. It is not evidence for a theorem and is not used anywhere in this analysis. The proof in Section 5 supersedes the exploratory motivation and establishes the constant ceiling cleanly using cube padding.

Scope closure: the mechanism survives the stated tests for a sufficiently small universal constant, but remains an unproved analytic inequality. The Gaussian result and ball obstruction are exact; the 1/4 ceiling is rigorous; the jump-rate issue blocks any automatic claim of a new sampling capability.
