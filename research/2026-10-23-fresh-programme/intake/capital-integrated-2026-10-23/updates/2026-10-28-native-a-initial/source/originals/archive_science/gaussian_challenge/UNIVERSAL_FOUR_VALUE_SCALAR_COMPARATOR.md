# A universal four-value scalar positive correction

27 October 2026. This is an ordinary transported Edgeworth-type comparator, reconstructed and proved here to avoid mistaking the more elaborate source-dependent scalar correction for a practical advantage. Historical novelty is not claimed. It works for every scalar globally Lipschitz source, with no fitted coefficient, mean oracle, derivative oracle, or Stein-kernel acquisition.

## 1. The implemented channel

Let h:R->R be globally ell-Lipschitz, let `mu=E h(G)`, and take a>0. Draw independent standard Gaussians `G0,G1,G2,G3,Z,W`. Query exactly the four values `V_i=h(G_i)`. Form

`vhat=(V1-V2)^2/2`,

`mhat=(V1-V2)^2(V1-V3)`,

and output

`Y=V0+(1-vhat/2)Z-(mhat/6)(Z^2-1)+aW`.              (1)

This is a positive pushforward on every execution, even when the random coefficient of Z is negative. Positivity of a density is not being inferred from a truncated signed series. The cost is exactly FOUR original value queries, six scalar Gaussian draws, and constant scalar arithmetic/storage. Its unknown constant offset cancels from both empirical coefficients. The mathematical statement uses exact Gaussian seeds and real arithmetic; finite precision needs a commonly rounded target and primitive-error budget.

The target is `N(mu,1+a^2)`. The reserve aW is paid noise, not free smoothing.

## 2. Exact unbiased coefficients and second moments

Write `H_i=V_i-mu`, `v=E H_i^2`, and `m3=E H_i^3`. Independence and centering give

`E vhat=v`, `E mhat=m3`.

The latter follows by expanding `(H1-H2)^2(H1-H3)`: only H1^3 has nonzero expectation. Since both Gaussian polynomials in the correction are centered,

`E Y=mu` exactly.

The coefficients are independent of H0,Z,W. Set

`U=-(vhat/2)Z-(mhat/6)(Z^2-1)`.

Orthogonality of the first two Gaussian Hermite polynomials gives

`E U^2=E vhat^2/4+E mhat^2/18`.

Pointwise Lipschitz differences and Gaussian moments yield

`E vhat^2 <=3 ell^4`,

`E mhat^2 <=48 ell^6`.

Indeed `E(G1-G2)^4=12`, and, for the correlated Gaussian differences P=G1-G2 and Q=G1-G3, `Var P=Var Q=2`, `Cov(P,Q)=1`, and `E P^4 Q^2=48`. Therefore

`E U^2 <=(3/4)ell^4+(8/3)ell^6`.                    (2)

These are unconditional moments of the actual random correction. No plug-in coefficient is treated as exact inside a nonlinear output law.

## 3. A full-law bound for every scalar Lipschitz source

Let phi be the standard Gaussian density, put

`rminus=sqrt(3-sqrt(6))`, `rplus=sqrt(3+sqrt(6))`,

`D4=(1/2)||phi''''||_1`

`  =2sqrt(6)[rminus phi(rminus)+rplus phi(rplus)]`.

The actual output satisfies

`TV(Law(Y),N(mu,1+a^2))`

` <= min(1, [19 D4/(24(1+a^2)^2)]ell^4`

`             +[phi(1)/a^2][(3/4)ell^4+(8/3)ell^6]).` (3)

A simpler slightly weaker bound replaces D4 by sqrt(6).

### Proof

Fix an arbitrary Borel event A and let `F=1_A*phi_a`. Expand once in the actual random correction U around `mu+Z+H0`. The absolute Taylor remainder is at most

`(1/2)||F''||infinity E U^2 <=phi(1)E U^2/a^2`,       (4)

because the derivative of a smoothed event is bounded by half the L1 norm of the corresponding Gaussian density derivative, and `||phi_a''||_1=4phi(1)/a^2`.

Independence of the empirical coefficients gives

`E[U F'(mu+Z+H0)]`

` =-(v/2)E F''(mu+Z+H0)-(m3/6)E F'''(mu+Z+H0)`,      (5)

using exact Gaussian integration by parts in Z. Both the variance and third-moment first-order contributions are therefore retained with their correct source correlations.

Now integrate the base Z. Define `q(x)=E_Z F(mu+Z+x)`. This is an event smoothed at standard deviation `sqrt(1+a^2)`, so

`||q''''||infinity <=D4/(1+a^2)^2`.

Taylor expansion in the centered H0 gives

`|E q(H0)-q(0)-(v/2)q''(0)-(m3/6)q'''(0)|`

` <=E H0^4 ||q''''||infinity/24`.

Furthermore,

`|E q''(H0)-q''(0)| <=(v/2)||q''''||infinity`,

`|E q'''(H0)-q'''(0)| <=sqrt(v)||q''''||infinity`.

Combining these estimates with (5), the uncancelled part is bounded by

`[E H0^4/24+v^2/4+|m3|sqrt(v)/6] ||q''''||infinity`. (6)

Gaussian Poincare gives `v<=ell^2` and

`Var(H0^2)<=4ell^2 v`,

so `E H0^4<=v^2+4ell^2v`. Cauchy–Schwarz additionally gives

`|m3|=|Cov(H0,H0^2)|<=2ell v`.

The bracket in (6) is therefore at most `(19/24)ell^4`. Insert (2), (4), and the fourth-derivative bound, then take the supremum over all Borel A. This proves (3). The claim is about the full implemented law; finite-moment tests play no role in its certification.

The formula for D4 follows by splitting the fourth Gaussian derivative at the four roots of `z^4-6z^2+3`. The bound `D4<=sqrt(6)` follows from Cauchy–Schwarz and `E He_4(Z)^2=4!`, with the same factor one-half for event indicators.

## 4. Arbitrary physical noise units

If the desired target has variance `sigma^2=b^2+a^2` with b,a>0, replace (1) by

`Y=V0+(b-vhat/(2b))Z-[mhat/(6b^2)](Z^2-1)+aW`.

For an L-Lipschitz source, the same proof gives

`TV <= [19 D4/24](L/sigma)^4`

`       +[phi(1)/a^2][3L^4/(4b^2)+8L^6/(3b^4)]`,

clipped at one. This is a small-L/noise-ratio quartic guarantee, not arbitrary-accuracy polylogarithmic sampling at a fixed ratio.

## 5. Why this scalar comparator does not complete N687

No claim follows for a high-dimensional vector merely by applying coordinatewise moment corrections: cross-coordinate cumulants and covariance remain. A direct vector covariance estimator from one difference Delta has

`Vhat=Delta Delta^T/2`.

Its Gaussian correction contributes `E||Vhat Z/2||^2=E||Delta||^4/16`. Already for the legitimate conservative affine source `g(x)=ell x`, this equals

`ell^4 d(d+2)/4`.

Thus the straightforward random covariance correction pays a quadratic dimension factor in its second-moment budget. That calculation is a failure of the desired dimension-free proof/interface, not a claimed target lower bound or a proof of TV from a covariance statistic. It is exactly where the main problem requires additional source geometry or a different representation.

For the explicitly known rational source family in the other note, reference subtraction still gives an even stronger one-query exact sampler. For a general unknown scalar source, (1) is a stronger ordinary comparison than assuming a useful S can be fitted for free. Bounded-input FORS under its full contract and the packet's other end-to-end samplers remain relevant competitors. No historical novelty or practical advantage is claimed.

## 6. Preserved executed checks

`check_universal_scalar_comparator.py` checks the coefficient identities and correlated-Gaussian moments exactly using rational polynomial arithmetic, evaluates (3), and executes (1) with a counting oracle. Floating moment outputs are consistency checks, never total-variation certification. Every execution uses four source calls; no fitted coefficient, source mean, derivative, K value, or conditional expectation is provided.
