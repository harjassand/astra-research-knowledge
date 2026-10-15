# Independent audit: strict log-concavity after Skellam convolution

This is an independently derived lemma, not a theorem attributed to Katkova–Vishnyakova. It concerns only the scalar class for which their theorem supplies a Poisson lattice multiplier. It makes no assertion about Diamond–Essén, arbitrary compact distributions, matrices, or higher dimensions.

## Statement and explicit constants

Let h, lambda, a > 0, set b=ah, and assume b <= 1/4. Let eta be the law of Y=h(N_+ - N_-), where N_+,N_- are independent Poisson(lambda) variables. Define

phi_R(z)=a[z asinh(z/R) - sqrt(R^2+z^2) + R],
kappa_R(z)=exp(-phi_R(z))/integral exp(-phi_R),
p_R=eta*kappa_R.

Set S0=2^(b+1) lambda,
C2=h^2(S0^2+S0),
C4=h^4(S0^4+6S0^3+7S0^2+S0).

It suffices to choose R satisfying all of

R >= 1,
R >= 2 C2(sqrt(2) a+4),
R >= 192 a C2,
R^3 >= 96 a C4.

Then p_R is an even, everywhere positive, smooth probability density, every derivative has every absolute exponential moment, and

(log p_R)''(x) <= -a/[6(R+|x|)] < 0  for every real x.

## Proof of the global curvature bound

Fix x and put t=R+|x|, u=t/R>=1, theta=phi_R'(x)=a asinh(x/R). Exponentially tilt eta by exp(theta Y), and denote expectation under this probability law by E_theta. The tilted law has independent Poisson rates r_+=lambda exp(h theta), r_-=lambda exp(-h theta). Their sum S satisfies

S <= 2 lambda exp(b|asinh(x/R)|) <= S0 u^b,

because exp(|asinh(v)|)=|v|+sqrt(1+v^2) <= 2(1+|v|). Comparing |N_+-N_-| with N_++N_- gives

M2:=E_theta Y^2 <= C2 u^(2b),
M4:=E_theta Y^4 <= C4 u^(4b).

Define the nonnegative Bregman remainder

D(Y)=phi_R(x-Y)-phi_R(x)+theta Y >= 0,
Z=E_theta exp(-D).

The posterior law appearing in differentiation of p_R is exactly exp(-D)/Z times the tilted law. Let A={|Y|<=t/2}. For every point z on the segment from x to x-Y, on A,

R+|z| >= t-|Y| >= t/2,
phi_R''(z)=a/sqrt(R^2+z^2) <= 2sqrt(2)a/t.

Consequently D<=sqrt(2)aY^2/t on A, and |phi_R'(x-Y)-theta|<=2sqrt(2)a|Y|/t there. Also P_theta(A^c)<=4M2/t^2. Thus

E_theta[exp(-D)1_A]
 >= 1 - sqrt(2)a M2/t - 4M2/t^2
 >= 1 - sqrt(2)a C2/R - 4C2/R^2
 >= 1/2.

Here 2b<=1 was used, and the displayed choice of R guarantees the last inequality. Since Z<=1, this proves both Z>=1/2 and posterior probability(A)>=1/2.

On A, sqrt(R^2+(x-Y)^2)<=R+|x-Y|<=3t/2. Therefore

E_post phi_R''(x-Y) >= a/(3t).

Variance is bounded by the second moment about any specified center. Globally phi_R' is a/R-Lipschitz. Hence

Var_post(phi_R'(x-Y))
 <= E_post[(phi_R'(x-Y)-theta)^2]
 <= 16a^2 M2/t^2 + 2a^2 E_theta[Y^2 1_(A^c)]/R^2
 <= 16a^2 M2/t^2 + 8a^2 M4/(R^2 t^2)
 <= (1/t)[16a^2 C2/R + 8a^2 C4/R^3]
 <= a/(6t).

The penultimate inequality uses u^(2b-1)<=1 and u^(4b-1)<=1; this is where b<=1/4 suffices. The final inequality follows by bounding each bracketed summand by a/12 using the choices of R.

Direct differentiation gives the exact identity

(log p_R)''(x) = Var_post(phi_R'(x-Y)) - E_post phi_R''(x-Y).

Combining the bounds proves the claim, uniformly on the entire real line.

## Analytic legitimacy and decay

The potential is even and smooth, with phi_R'=a asinh(z/R), phi_R''=a/sqrt(R^2+z^2), and phi_R(z)/|z| tending to infinity. Thus the normalizing integral is finite and positive. All derivatives of phi_R of order >=2 are bounded for fixed R. Repeated differentiation of exp(-phi_R) shows that every kappa_R derivative is bounded in absolute value by a constant times a power of 1+log(2+|z|) times exp(-phi_R(z)). Every derivative is therefore bounded and integrable against exp(c|z|) for every c>0.

Bounded derivatives justify differentiation under the eta integral to every order. The factors phi_R' kappa_R and ((phi_R')^2-phi_R'')kappa_R are bounded too, justifying the posterior curvature identity without any formal interchange. The tilted law is legitimate because the Skellam moment generating function is finite at every real argument.

Eta has every absolute exponential moment, by its explicit moment generating function exp(lambda(e^(hs)+e^(-hs)-2)). Tonelli's theorem and |y+z|<=|y|+|z| give, for each j and c>0,

integral exp(c|x|)|p_R^(j)(x)| dx
 <= [integral exp(c|y|) eta(dy)] [integral exp(c|z|)|kappa_R^(j)(z)| dz] < infinity.

Symmetry of eta and kappa_R gives evenness. Positivity of kappa_R and unit mass of eta give everywhere positivity and normalization.

## Consequence for the inspected scalar prior theorem

If the prior theorem supplies nu=law(hN), N Poisson(lambda), with q=f*nu>=0 for a nonzero integrable f with integral f>0, then eta=nu*reflected(nu). Therefore

f*p_R = q*reflected(nu)*kappa_R > 0 everywhere.

Indeed q*reflected(nu) is a finite nonnegative measure of positive mass, and kappa_R is everywhere positive. All associativity statements follow from f being integrable and the other factors being finite measures or integrable densities; the final convolution is well-defined pointwise because kappa_R is bounded. This strengthens the earlier Gaussian postprocessing overlap by adding strict log-concavity in precisely this admitted scalar class.
