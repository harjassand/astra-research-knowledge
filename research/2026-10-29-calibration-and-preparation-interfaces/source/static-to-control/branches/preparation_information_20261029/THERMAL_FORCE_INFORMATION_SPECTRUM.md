# Dissipation and force explanation measure different spatial norms

29 October 2026. Root construction following the native thermal counterexample.
The point is an infinite-dimensional source-class principle and a sharp
regularity/consequence relation, not another fitted example or entropy estimator.

## 1. General shear source and exact information spectrum

Retain the two-torus kinetic thermostat with unit masses, damping gamma>0 and
temperature tau>0, but replace a sin(nx) by ANY real bounded periodic f(x).
Assume sufficient regularity for the stated physical force model; continuous
bounded f already defines the triangular SDE by its explicit integral solution.
The applied work force is (0,f(x)) relative to the stationary bath. Its Fourier
coefficients use normalized Haar measure dx/(2pi):

    f(x)=sum_(m in Z) fhat_m exp(imx),
    ||f||_2^2=sum_m |fhat_m|^2.

The same stationary Gaussian driver and independent uniform phases give

    C_f(t)=E[f(x_t)f(x_0)]
       =sum_m |fhat_m|^2
          exp[-m^2 tau/gamma^2 (gamma t-1+exp(-gamma t))]. (1)

The Fourier diagonalization is exact: uniform phase removes unequal modes,
and the integrated OU displacement supplies the characteristic function.
All summands are nonnegative. Parseval and Tonelli justify the formula for
bounded L2 forces by approximation. In particular C_f(t)>=0, even when f
itself changes sign.

Define the positive multipliers

    I_m=integral_0^infinity exp[-gamma t
                  -m^2 tau/gamma^2 (gamma t-1+exp(-gamma t))]dt.

Then the stationary physical entropy-production rate is EXACTLY

    sigma[f]=(1/tau) sum_m |fhat_m|^2 I_m.                (2)

I_0=1/gamma; I_m is strictly decreasing in |m|>0; and

    |m| I_m -> sqrt(pi/2)/sqrt(tau).                     (3)

The best equilibrium path model WITH THE SAME conventional bath and a
conservative position-only force is free equilibrium. Its stationary KL RATE is

    I_native[f]=||f||_2^2/(4gamma tau).                  (4)

This includes nonzero mean f: a constant transverse force is also orthogonal
to every periodic gradient. The exact full-horizon projection is

    inf_U D(P_f^rho_f[0,h]||P_U^nu_U[0,h])
         = D(rho_f||mu_0)+h I_native[f],
    D(rho_f||mu_0)<=sigma[f]/(2gamma).                   (5)

To see the initial minimization, uniform position gives
D(rho_f||nu_U)=D(rho_f||mu_0)+D(uniform_q||nu_U,q).
The rate minimization follows by force/gradient orthogonality. Hence both
terms are independently minimized by constant U. For the common free-Gibbs
initial preparation, the exact minimum is simply h I_native[f].

The fact that a shear SDE is exactly solvable, and its integrated-OU Fourier
kernel, are established inertial-transport machinery. See Boi--Mazzino--
Muratore-Ginanneschi, arXiv:1611.02747, equations (3)--(9). Their eddy-diffusion
observable uses a different time weighting. The proposed use here is the
comparison of physical entropy with complete same-bath equilibrium explanation
and its observation/preparation resources, not invention of that kernel.

## 2. A negative-half-derivative norm

Let w_m=gamma+|m|sqrt(tau). Uniformly in m,

    exp(-3/2)/w_m <= I_m <= 5/w_m.                       (6)

For the lower bound, g(u)=u-1+exp(-u)<=u^2/2. Integrate only over
0<=t<=1/w_m; the exponent gamma t+m^2 tau t^2/2 is at most 3/2.

For the upper bound set alpha=|m|sqrt(tau)/gamma. If alpha<=1, I_m<=1/gamma
<=2/w_m. If alpha>=1, use g(u)>=u^2/4 on [0,1] and g(u)>=u/4 for u>=1.
The first inequality follows from 1-exp(-u)>=u/(1+u), integration, and
u-log(1+u)>=u^2/[2(1+u)]. Then

    gamma I_m <= sqrt(pi)/alpha
                    +exp[-1-alpha^2/4]/(1+alpha^2/4)
                <= (sqrt(pi)+exp(-1))/alpha
                < 5/(1+alpha).

The penultimate bound uses alpha<=1+alpha^2/4. The final bound uses
1/alpha<=2/(1+alpha) and 2(sqrt(pi)+exp(-1))<5.

Thus sigma is equivalent, with explicit constants, to

    (1/tau) sum_m |fhat_m|^2/(gamma+|m|sqrt(tau)),        (7)

an inhomogeneous Sobolev norm of order -1/2 squared. In contrast, native
equilibrium path-KL cost is the ordinary L2 force norm squared. These are
distinct physical questions: high spatial frequencies are suppressed in
dissipation by inertial averaging while they remain visible to fully resolved
acceleration/force likelihoods.

This norm statement is restricted to the triangular shear source. It is not
a claimed universal formula for arbitrary multidimensional nonconservative
forces or interacting hidden systems.

## 3. Exact bandwidth repair

If physical information warrants fhat_m=0 for |m|>N, then

    I_native[f] <= sigma[f]/(4gamma I_N).                (8)

This coefficient is optimal in this source class: equality holds in the
rate inequality for a pure real sine/cosine at frequency N (and for a
constant at N=0). Combining with (5) gives

    inf_U D(P_f^rho_f||P_U^nu_U)
       <= sigma[f] [1/(2gamma)+h/(4gamma I_N)].          (9)

For large N, 1/(4gamma I_N) grows asymptotically as
N sqrt(tau)/(4gamma sqrt(pi/2)). Bandwidth therefore enters a necessary
physical cost; an amplitude bound alone cannot replace it. The bandlimit
is a warranted source constraint here, not something certified from finitely
many samples without an additional regularity/acquisition argument.

## 4. Sharp Sobolev regularity repair

For any s>0 suppose a warranted weighted regularity budget is

    B_s=sum_m w_m^(2s)|fhat_m|^2 <= R_s^2.

Let A_-=sum_m |fhat_m|^2/w_m. Holder interpolation gives exactly

    ||f||_2^2 <= A_-^(2s/(2s+1)) B_s^(1/(2s+1)).         (10)

This follows by writing each |fhat_m|^2 as the product of powers of
|fhat_m|^2/w_m and w_m^(2s)|fhat_m|^2 with exponents
2s/(2s+1) and 1/(2s+1). Equation (6) supplies A_-<=tau sigma/c,
c=exp(-3/2). Therefore

    I_native[f] <= (1/(4gamma tau))
        (tau sigma[f]/c)^(2s/(2s+1)) R_s^(2/(2s+1)).     (11)

The exponent is optimal as a uniform small-sigma power under this budget.
Take f_n(x)=b n^(-s)sin(nx) with fixed b. Its B_s stays bounded, whereas

    sigma[f_n] is asymptotic to a positive constant times n^(-2s-1),
    I_native[f_n]=b^2 n^(-2s)/(8gamma tau).

No larger power of sigma can bound (4) uniformly with a fixed finite
coefficient. For s=1 the sharp rate exponent is 2/3. A known amplitude
bound ||f||_infinity<=a and Lipschitz bound L imply
B_1<=2gamma^2 a^2+2tau L^2, making (11) a concrete quantitative version
of the broader compactness theorem in physical_frontier/.

The full stationary path-KL bound adds sigma/(2gamma); Pinsker then gives
a total-variation upper bound. Sharpness above concerns the KL-rate exponent,
not an asserted optimal TV exponent or sample complexity.

## 5. Preparation and prediction reuse

Every C_f in (1) is nonnegative. Thus the common thermal preparation proof,
finite-horizon work bound W(h)<=tau h sigma[f], final-state KL bound,
force-off recovery and synchronous coupling all extend from a single sine
to this whole shear class. The free model predicts the declared
position-sup/momentum-L2 consequences with error proportional to sqrt(sigma).

This is a strong equally informed conventional comparator: free equilibrium
is not merely convenient but is the exact native equilibrium KL projection.
It is already the preferred predictor for these low-resolution tasks. The
new scientific addition is the explicit relation between the consequence,
spatial regularity and physical information needed to justify that reuse.
There is no claim of faster computation or historical priority.
