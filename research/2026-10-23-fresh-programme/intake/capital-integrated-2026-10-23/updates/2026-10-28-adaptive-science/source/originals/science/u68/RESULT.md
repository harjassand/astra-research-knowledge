# Result

The universal N687 polylogarithmic Gaussian-mean target remains **NOT ACHIEVED**. This run produced a legal positive five-query first correction with an implemented full-law bound, and a joint-source Stein gauge that removes the previous initial L2 inverse obstruction. A fresh independent helper audited both results without finding a substantive flaw. No novelty, external validation, practical advantage or general-learning breakthrough is claimed.

## Actual finite sampler

The governing proof is [FIVE_QUERY_POSITIVE_CORRECTION.md](FIVE_QUERY_POSITIVE_CORRECTION.md); executable floating diagnostics are [five_query_sampler.py](five_query_sampler.py) and [five_query_results.json](five_query_results.json).

For every globally λ-Lipschitz conservative g=grad F, F C1,1, let μ=E g(G), choose 0<a<1, b=sqrt(1-a²), and reserve η>0. The frozen source's two-value action factories compose in a fresh random order to give a four-value unbiased bounded action WΓ for Γ_b=sym(K_b Dh_b). Draw independent Gaussian vectors G,H,Z,W,V and T with density 2t on [0,1]. Return

```
C = T G + sqrt(1-T²) W,
Y = g(bG+aH) + Z - (1/2)WΓ(C;Z) + ηV.
```

This uses **at most five whole-vector g values on every execution**, O(d) surrounding real arithmetic/storage, and no mean, derivative, potential, VJP, conditional-mean or basis oracle. Its mean is exactly μ. With Cη=(sqrt(2)/2)log(1+η^(-2)),

```
TV(Law(Y), N(μ,(1+η²)I))
 <= min{1,
 Cη [b³λ³ sqrt(d)/sqrt(2) + b⁴λ⁴d/2]
 + sqrt(2)b⁴λ⁴d/(8η²) + aλ sqrt(d)/(2η)}.
```

The reserve is charged to the target variance. For physical target σ², run on g/τ and multiply by τ, where τ=σ/sqrt(1+η²). This is the supplied exact-Gaussian/exact-real oracle convention. Common rounding contracts the law bound; floating diagnostics do not supply a uniform machine-precision theorem for arbitrary oracle reals.

The proof charges the randomized correction's conditional variance through a Gaussian-smoothed Taylor estimate. It does not substitute an unbiased coefficient inside a nonlinear law. Its separate exact covariance receipt is

```
0 <= Cov(Y)-(1+η²)I <= [a²λ²+b⁴λ⁴/4]I.
```

For affine g(x)=c+Bx, B symmetric, the entire implemented law is exactly Gaussian with covariance `(1+η²)I+a²B²+(b⁴/4)B⁴`, checking the signs and normalization. This is not an advantage fixture: g(0) already gives an affine mean in one query.

## Foundational construction

[JOINT_GAUGE_THEOREM.md](JOINT_GAUGE_THEOREM.md) constructs a two-block kernel for every symmetric joint Gaussian L2 residual R(G,Z):

```
δG JG + δZ JZ=u,       E_Zu=0,
JG=-DGu,              sym[JZ+(DZu)^T]=-R,
||Du||2<=||R||2,      ||DGu||2<=||R||2/2,
||J||2<=sqrt(3)||R||2.
```

Constants are independent of dimension and Hermite degree. The source-adjoint block converts the full linearization's source term into `(K-Dh)DGu^T`. For X=h(G)+Z with Lip(h)=λ<1, a genuine initial L2 Neumann inverse follows with contraction at most λ, without higher source smoothness. This resolves the initial analytical source-derivative gate in the enlarged kernel class.

The stricter interface δZ JZ=u is genuinely obstructed: the helper proved sharp exponential inverse growth and a bounded smooth periodic residual with no strict L2 inverse. This is an interface obstruction, not a target lower bound. See [helper/HELPER_RESULT.md](helper/HELPER_RESULT.md).

The full Newton residual is exactly quadratic, but general L2 control only gives an L1 product and does not preserve the next inverse's coefficient gate. [SCALAR_CHAIN.md](SCALAR_CHAIN.md) gives a narrower scalar W1,4 chain for λ<1/(2sqrt(3)), with first-step residual at most `5λ⁴/[1-2sqrt(3)λ]²` in L2. Its separable extension assumes a supplied separable basis. Iteration and universal acquisition remain open.

## Additional legal acquisition

[RESOLVENT_DERIVATIVE_FACTORY.md](RESOLVENT_DERIVATIVE_FACTORY.md) acquires DK_b(y)[v]w exactly with **three g values**, including raw C1,1 conservative sources, with dimension-free Lp bounds of order sqrt(p)L||v||||w||. An eight-value antithetic version annihilates affine fields on every execution (four suffice in one dimension). It uses a chi3 chord, endpoints and one random interior value. It acquires a first tensor action, not a common realized tensor or the full coupled inverse.

## Verification and preserved failure

- Own Hermite code passed 48 polynomial identity/norm cases and scalar affine checks through source degree 100. The helper independently passed 180 exact-rational two-dimensional bichaos checks, including the sharp combined norm identity.
- Derivative-action diagnostics used 240,000 draws per case, frequencies through 64 and dimensions through 64. Means agreed with independent analytic quadrature at Monte Carlo accuracy; antithetic affine output vanished analytically and at floating cancellation scale numerically. This does not certify TV.
- The literal positive sampler records exactly five original queries per execution. Five-query independent averaging receives the same source and target noise. Bounded characteristic tests and moments do not certify TV; the theorem supplies its full-law bound.
- Unfiltered degree-64/80 Galerkin arithmetic failed: tiny spurious high-Hermite coefficients produced enormous fourth-moment residuals despite stable mean/variance. Preserve scalar_chain_diagnostic.py and scalar_chain_results.json as failures. A bounded-function OU-grid cross-check stabilized the λ=.12 quadratic residual near 4.786e-6 under refinement; its interpolation/quadrature errors remain uncertified. No theorem depends on that numerical calculation.

## Comparators and scientific decision

The matched five-query independent-average baseline has the frozen chi-square bound with proxy λ²I/5 and target noise 1+η². Its certificates are stronger on most recorded moderate-λ fixtures. The new bound improves powers of small λ in some dimension/noise regimes, which compares sufficient bounds rather than optimal errors or practical speed. The cosine fixture's mean is analytically known to an instance-aware competitor, so it is not an advantage benchmark. Antithetic/control-variate methods, fixed-positive-exponent compiler candidates, bounded-input FORS and Gaussian-cloud methods retain their actual contracts and remain competitors.

The decision changes precisely as follows: an initial positive value-only nonlinear correction with a proved implemented law now exists, and the initial ordinary-L2 inverse is repaired by an explicit full-source gauge. The hardest remaining obligation is an acquired **iterated** correction with dimension-controlled full-law error and a subcritical/every-execution polylogarithmic query budget. The five-query bound becomes vacuous at fixed λ as d grows. Formal iteration also loses product integrability and bounded coefficients. Those are real missing constructions.

Only supplied frozen science, owned files and the single authorized helper were used. No memory, other study trajectories, chats, goals, automations, external operations or shared edits were used. Governing frozen arguments were S3 sections 16–18 and S4 sections 8–12; S1/S2/S5/S6/S11/S12 supplied source/comparator context. No priority search was performed.
