# Rare conductance without computing the fiber partition function

Status: ROOT candidate, UNREVIEWED. This is a distinct consequence of conditional transport, not an executed extension of the accepted Gaussian program. All work is abstract diffusion mathematics. No physical, novelty, general complexity-hardness or arbitrary-start passage-time claim is made.

## 1. Task and actual model

In physical orthogonal coordinates x=(y,z), z in R^m, let

  F(y,z)=v(y) U(z),   v(y)=1+kappa(1-y^2)^2, kappa>0.

U is a smooth positive homogeneous polynomial of even degree p>=2, with an ACQUIRED global coercivity certificate

  U(z)>=a ||z||^p,  a>0.

No convexity, independent coordinates, Gaussian fibers, rapid conditional mixing or evaluable fiber partition function is assumed. Require 4m>p. The full process is isotropic overdamped diffusion dX=-grad F dt+sqrt(2/beta)dW, beta>0. Basins are full fibers y<=-1/2 and y>=1/2. The output is cap_mu(A,B)/mu(A), not an arbitrary-state mean passage time or a complete sampler.

A raw-input acquirer still has to earn the coordinate, full identity and coercivity. A simple sparse, explicitly verifiable quartic family is given below; generic positive-form recognition is not granted for free.

## 2. Exact cancellation of the unknown internal partition function

Let Z_U=integral exp(-U(z))dz, finite by coercivity. Homogeneity and a change of variables give

  integral exp[-beta v(y) U(z)]dz=(beta v(y))^(-m/p) Z_U.

Thus the unnormalized y marginal can be taken to be

  q(y)=v(y)^(-m/p).

Z_U cancels from the normalized marginal and from capacity divided by basin mass. It need not be numerically evaluated or sampled. This is an exact algebraic consequence of the actual potential, not a supplied normalization oracle.

The full projected process is generally not Markov: its y drift is -v'(y)U(z), which depends on the retained fiber state. No replacement of that drift by its equilibrium average is made.

## 3. Exact conditional transport and an acquired moment bound

The conditional density is proportional to exp[-beta v(y)U(z)]. Scaling its coordinates gives the exact continuity field

  w_y(z)=-(v'(y)/(p v(y))) z.

Indeed homogeneity z.grad U=pU makes partial_y rho+div_z(rho w)=0. Although the normalized density/current has an unknown common constant Z_U, it is an analytical proof object, not an operation the algorithm must implement. All scalar quantities needed for the bound below are acquired without that constant.

Scaling, or integration by parts, gives the exact virial identity

  E_y U = m/(p beta v(y)).

By coercivity and Jensen (2/p<=1),

  E_y ||z||^2 <= [m/(p beta a v(y))]^(2/p).

The conditional transport cost K=E_y||w_y||^2 therefore satisfies

  K(y)<= m^(2/p) v'(y)^2 /
              [p^(2+2/p) (beta a)^(2/p) v(y)^(2+2/p)].   (1)

This does not assume any knowledge of the angular Gibbs law or of its relaxation time.

## 4. Dimension-separated integrated resistance

Set b=1/2, W=1/q=v^(m/p), s=1+2/p, and

  C_m = m^(2/p-1)/[p^(1+2/p)(beta a)^(2/p)],
  v_min=1+9 kappa/16,
  D=4 kappa/v_min^s + s*(9 kappa^2/4)/v_min^(s+1).

On [0,b], v'<=0 and -W'/W=(m/p)(-v'/v). Dividing (1) by this derivative (or taking its continuous endpoint limit) gives

  K W <= C_m f(y)(-W'),   f=(-v')v^(-s), f(0)=0.

Here

  f'=-v'' v^(-s)+s v'^2 v^(-s-1) <=D,

because -v''<=4kappa and |v'|<=3kappa/2 in the slab. Integration by parts retains the favorable boundary term:

  integral_0^b K W
    <=C_m[-f(b)W(b)+integral_0^b f'W]
    <=C_m D integral_0^b W.

Evenness gives R1<= (1+C_m D)R0, where

  R0=integral_-b^b 1/q,
  R1=integral_-b^b (1+K)/q,
  MA=integral_b^infinity q.

The ordinary full-diffusion conditional-transport/Dirichlet sandwich now yields

  k_free/(1+C_m D) <= cap_mu(A,B)/mu(A) <= k_free,
  k_free=1/(beta MA R0).                                (2)

Thus an exponentially small conductance may be enclosed by two scalar integrals and acquired coercivity, without computing the high-dimensional internal partition function. No claim that that partition function is formally hard for every U is needed or proved.

The conditioning in a is real. For fixed a and p>=2, C_m does not grow with m, but extensive models may have a depending on dimension. That dependence must be retained, not called dimension-free by hiding it.

## 5. A directly recognizable coupled quartic family

Take p=4 and, in the actual physical fiber axes,

  U(z)=sum_i d_i z_i^4 + sum_(i<j) J_ij z_i^2 z_j^2,
  d_i>=d_min>0, J_ij>=0.

The couplings may form any finite graph and can be arbitrarily large. Reading every coefficient, verifying the monomial types and signs, and taking d_min acquires

  U>=d_min sum_i z_i^4>= (d_min/m)||z||^4.

So a=d_min/m and

  C_m=1/[8 sqrt(beta d_min)],

independent of the number of fibers and the nonnegative interaction weights. Convexity is not assumed; positive mixed quartics need not have positive Hessian everywhere. The angular conditional law may be complicated. Its partition constant cancels exactly; its effect on the full dynamics is retained within the transport resistance bound.

For beta=d_min=kappa=1, using the deliberately coarser v_min>=1 bound gives D<=59/8, hence

  k_free/(123/64) <= cap_mu(A,B)/mu(A) <= k_free.           (3)

The sharper D above improves this factor further. At m divisible by4, q=v^(-m/4) is rational at rational y; otherwise exact outward p-th-root arithmetic is sufficient. No Gaussian determinant or fiber sampler is needed.

This is an available raw grammar, not an assumption that arbitrary rotated quartics are already decomposed into this form. A prototype can acquire an aligned reaction coordinate by the unique absent direction of the lowest homogeneous term, then verify ALL coefficients of F=v U. More generally, the translation-invariant direction of the lowest homogeneous polynomial can be acquired by solving the finite linear equations ell.grad(F_p)=0; coercivity ensures its kernel is one-dimensional for an actual family member. Euclidean normalization, a global transverse coercivity certificate, and full input identity still have to be earned. A generic rotated positive quartic may return UNKNOWN under a limited sufficient finder.

## 6. Global diffusion and tail receiving

Coercivity makes Z_U finite. For |y|>=T>1,

  q(y)<=kappa^(-m/p)(y^2-1)^(-2m/p),

and its tail has the explicit upper bound

  integral_T^infinity q <= kappa^(-m/p)
       (1-1/T^2)^(-2m/p) T^(1-4m/p)/(4m/p-1).           (4)

Thus the full Gibbs density is normalizable precisely within the stated sufficient tail condition 4m>p.

For nonexplosion, take V=1+y^2+K0||z||^2, with K0=1+kappa/p. Euler homogeneity gives

  grad V.grad F = 2[y v'(y)+K0 p v(y)]U(z).

Since y v'=4kappa y^2(y^2-1)>=-kappa and v>=1, the bracket is at least p. Therefore the full generator satisfies

  L V <=2(1+K0 m)/beta.

The usual stopped Lyapunov argument proves nonexplosion. Smoothness, nondegenerate diffusion and the finite Gibbs law give the conservative reversible process used in the capacity principle. No artificial reflecting fiber boundary or uncharged truncated tail is inserted.

## 7. Remaining construction and comparison obligations

A full producer/verifier, exact input/task binding, numerical/tail arithmetic, finite budgets, bit-growth accounting, adversarial tests and independent review remain to be completed. The accepted Gaussian program cannot receive this potential by a filename change. In particular the physical dimension m, homogeneous degree p and exponent m/p are distinct from polynomial degrees in a determinant backend.

Homogeneous scaling, virial identities, conditional transport and Thomson/Dirichlet principles are conventional tools. The proposed contribution is the assembled finite-rate conductance certificate and an explicit raw coupled-polynomial consumer that avoids acquiring Z_U. Located prior results must be distinguished from ordinary methods augmented with this newly derived bound. Historical originality, practical performance and any complexity separation remain open.
