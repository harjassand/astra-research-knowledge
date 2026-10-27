# Exact polyconvex obstruction to the elliptope beta bridge

25 October 2026. This rejects the proposed nonhomothetic beta marginal path. It is not a counterexample to Morrey, does not exclude a positive null stress from delta_0 to the actual cosine law, and does not resolve the full 2x2 conjecture.

## Bridge, domain, and actual endpoint

Let

    F(u,v,w)=1-u^2-v^2-w^2+2uvw,
    q(u,v,w)=uv+uw+vw,       s=u+v+w,
    J=(ee^T-I)/2,           e=(1,1,1).

The domain is the interior K of the 3-by-3 correlation elliptope, not the entire set F>0 in R^3:

    -1<u,v<1,
    |w-uv|<sqrt((1-u^2)(1-v^2)).

For eta>0 let mu_eta have density proportional to F^(eta-1) on K, with normalizing integral

    B(1/2,eta) B(1/2,eta+1/2)^2.

Use the increasing parameter t=1/(eta+1), and write nu_t=mu_(1/t-1). The change of variables

    w=uv+sqrt((1-u^2)(1-v^2)) R

makes u and v independent with densities proportional to (1-u^2)^(eta-1/2), and R independent with density proportional to (1-R^2)^(eta-1). This follows directly from

    F=(1-u^2)(1-v^2)-(w-uv)^2

and its Jacobian. As t tends to 1, u and v tend to independent arcsine variables and R tends to symmetric mass on {-1,1}. Therefore nu_1 is exactly the correlated law

    (cos x, cos y, cos(x+y))

for independent Haar phases, NOT three independent cosines. As t tends to 0, E|Z|^2=3t/2 implies nu_t tends to delta_0.

The proposed path has zero mean and E q=0 at every time. These necessary low-order identities do not make it a null-martingale path.

## Exact higher-moment diagnostic

Set

    H(z)=q(z)-s(z).

Under nu_t, the following moments are exact:

    E H = 0,
    E H^2 = 3t(2-t)/4,
    E H^3 = 3t^2(4-t^2) / [4(1+t)^2].

Here is a short direct derivation, sufficient to check the higher moment independently. The distribution is invariant under changing the signs of any pair of u,v,w. A monomial can therefore have nonzero expectation only when its three exponents have the same parity. The conditional-beta representation gives

    E u^2 = t/2,
    E u^4 = 3t^2/[4(1+t)],
    E uvw = E u^2v^2 = t^2/4,
    E u^3vw = 3t^3/[8(1+t)],
    E u^2v^2w^2 = t^3(4t+1)/[8(1+t)^2].

For the last identity, condition on u,v and use E R^2=t/(2-t). Consequently,

    E H^2 = 3 E u^2v^2 - 6 E uvw + 3 E u^2,
    E H^3 = 6 E u^2v^2w^2 - 18 E u^3vw
             + 18 E u^2v^2 - 6 E uvw,

which yield the displayed formulas.

At the endpoint,

    (d/dt) E H^2 |_(t=1)=0,
    (d/dt) E H^3 |_(t=1)=3/16.

These two facts are already incompatible with a bounded martingale H(Z_t).

## Martingale obstruction

If Z_t is a continuous martingale and its matrix bracket obeys

    J:d<Z>_t=0

as a signed time-measure identity, Ito's formula makes q(Z_t), and hence H(Z_t), a martingale. This does not assume a Markov generator or an absolutely continuous bracket.

Every nu_t is supported in [-1,1]^3. Since H is multi-affine, its cube extrema occur at vertices and its range on that cube is [-2,6]. Thus H(Z_t) is bounded. If the path is originally defined only for t<1, the bounded martingale has an endpoint limit, whose law is fixed by the weak limit nu_1.

For t<1, a martingale coupling from t to 1 would give

    E(H_1-H_t)^2 = E H_1^2-E H_t^2 = (3/4)(1-t)^2.

Taylor's formula for x^3 on [-2,6], with the martingale cancellation of its linear term, gives

    |E H_1^3-E H_t^3| <= 18 E(H_1-H_t)^2
                       = (27/2)(1-t)^2.

But the exact third moment has a nonzero first-order endpoint change, namely (3/16)(1-t)+O((1-t)^2). Contradiction. Therefore the whole beta bridge cannot be a determinant-null martingale marginal path.

This is not merely a failure of the proposed low-degree covariance: no covariance, state dependence, hidden variables, singular clock, or non-Markovian choice can realize all these marginals while retaining the null-martingale property.

## Explicit global polyconvex separator

The obstruction can be made into one exact late-transition certificate. Define the globally C^2 convex function

    psi(x)=18x^2-x^3,       x<=6,
    psi(x)=108x-216,        x>=6.

The branches match in value, first derivative, and second derivative at 6; psi''=36-6x>=0 on the first branch and zero on the second.

On all 2-by-2 real matrices define

    h(A)=det A-tr A+(A_12+A_21)/2,
    f(A)=psi(h(A)).

This f is globally polyconvex: it is the restriction of the convex function

    (A,d) -> psi(d-tr A+(A_12+A_21)/2)

to d=det A. In particular it is globally rank-one convex. For the physical source map

    B(u,v,w)=[[u+w,w],[w,v+w]],

one has h(B(z))=H(z). Therefore its expectations on the beta family are

    P(t)=E f(B(Z_t))
        =(27/2)t(2-t)-3t^2(4-t^2)/[4(1+t)^2].

At t0=99/100, corresponding to eta=1/99,

    P(1)-P(99/100) = -942849/1584040000 < 0.

Thus the transition from nu_(99/100) to the ACTUAL terminal cosine law is blocked even by a global polyconvex function. No determinant-null martingale transition, laminate transition, or finite positive determinant-null stress transition can have these two marginals.

The failure also occurs between strictly interior beta laws. For example,

    P(999/1000)-P(99/100)
      = -266178585850551/632982542404000000 < 0.

So excluding the limiting surface time does not rescue the path.

## Why finite positive stresses cannot evade this separator

In coefficient coordinates let g(z)=psi(H(z)). Direct differentiation gives

    D^2g = psi''(H) grad H tensor grad H + 2 psi'(H) J.

For every PSD matrix measure S with J:S=0,

    D^2g:S = psi''(H) (grad H)^T S grad H >= 0.

To avoid any unbounded-test or assumed-support issue for a finite-activity stress, use a bounded-slope convex extension with exactly the same source values. Replace the lower part of psi by

    psi_hat(x) = -108x-144,                         x<=-3,
    psi_hat(x) = 8(x+3)^3-108(x+3)+180,             -3<=x<=-2,
    psi_hat(x) = 18x^2-x^3,                        -2<=x<=6,
    psi_hat(x) = 108x-216,                         x>=6.

The pieces match through second derivative. Their second derivatives are respectively 0, 48(x+3), 36-6x, and 0, all nonnegative on the corresponding intervals. Moreover |psi_hat'|<=108. All source values are unchanged because H lies in [-2,6].

Set g_hat=psi_hat(H). Then g_hat=O(1+|z|^2), grad g_hat=O(1+|z|), and

    D^2g_hat:S=psi_hat''(H) (grad H)^T S grad H >=0.

Test the stress equation with chi(z/R)g_hat, where chi is a fixed nonnegative compact cutoff equal to 1 on the unit ball. For large R its source integral is exactly the negative expectation gap above. The main Hessian term chi D^2g_hat:S is nonnegative. All other product-rule terms are supported in R<=|z|<=2R and bounded in absolute value by a fixed constant times the trace mass of S in that annulus: the derivatives of chi supply 1/R and 1/R^2, which cancel the stated gradient and value growth. Since S has finite trace mass, these errors tend to zero. A negative source integral is impossible. C^2 tests are justified by local smooth approximation on each compact support.

This excludes every finite positive J-null stress with DivDiv S=nu_1-nu_(99/100), without imposing its support in advance. Exactly the same proof applies to (1/2)DivDiv C=nu_1-nu_(99/100), with C=2S. It applies equally to the explicitly negative strictly interior transition above.

## Normalizations and scope

For each beta marginal, E|B(Z_t)|_F^2=3t. A hypothetical transition stress from time a to b would therefore have physical trace mass

    (3/2)(b-a) for DivDiv S=nu_b-nu_a,
    3(b-a) for (1/2)DivDiv C=nu_b-nu_a.

The distinction does not alter the obstruction.

This is NOT a counterexample to rank-one-convex implies quasiconvex. The function f is polyconvex, and every individual centered beta marginal has E f>=f(0) because E H=0 and scalar Jensen applies. The contradiction concerns ordering two nontrivial proposed intermediate laws, not Jensen from delta_0. A different nonhomothetic path, or a direct positive endpoint stress, remains possible.

## Provenance and verification

The parent supplied the proposed beta density, conditional representation, time parameter, and a low-degree covariance candidate explicitly marked unqualified. The argument above does not assume that covariance is PSD or solves the equation and does not retune it. It rejects the whole marginal path using exact higher moments.

The separate surface-Stein obstruction packet is preserved unchanged. No stopped localization, old map/SOS search, simulation, or expensive prefix certification was run. check_exact_beta_moments.py reproduces the moments and separator with exact SymPy arithmetic; exact_beta_receipt.json records the actual check. INDEPENDENT_CHECK.md contains a separate mathematical audit. The full Morrey conjecture remains unresolved.
