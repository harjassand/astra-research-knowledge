# Partition-free conductance from parallel frozen-fiber channels

Status: NEW UNREVIEWED construction, separate from the frozen radial consumer.
It is a stronger retaining use of ordinary weighted Cauchy/Dirichlet machinery,
not a claim of historical originality. No frozen source is modified.

## 1. Same task, less kinetic conditioning

Let F(y,z)=v(y)U(z), v=1+kappa(1-y^2)^2, kappa>0, z in R^m. Let U be positive
homogeneous degree p>0, with finite positive Z_U=integral exp(-U)dz, and enough
smoothness/coercivity to define the conservative reversible isotropic diffusion.
The earlier polynomial Lyapunov proof applies to the received quartic grammar.
Assume4m>p so the full Gibbs law is finite. Put alpha=m/p>0, b=1/2,
A={y<=-b}, B={y>=b}, q=v^(-alpha), MA=integral_b^infinity q,
R0=integral_-b^b v^alpha and k_free=1/(beta MA R0).

For every admitted model,

  k_free / C_parallel <= cap_mu(A,B)/mu(A) <= k_free,
  C_parallel = sqrt((16+23 kappa)/(14(1+kappa))).            (P)

In particular C_parallel=sqrt(39/28), about1.1802, for unit kappa, independently
of m,p,beta,d_min, interaction graph and weights. For all positive kappa,
C_parallel<=sqrt(23/14), about1.2818. Coercivity/finite partition is still acquired
for model existence; its numeric constant no longer enters the kinetic factor.

The previous radial proof remains valid, but this is a stronger ordinary
retaining construction in unit parameters and whenever radial conditioning is
worse. This is not a claim that older literature already contained(P).

## 2. Parallel-channel lower bound by direct one-dimensional Cauchy

For any admissible h=1 on A, h=0 on B and each fixed z,

  integral_-b^b partial_y h(y,z)dy = -1.

Weighted Cauchy therefore yields

  integral_-b^b |partial_y h|^2 exp[-beta v(y)U(z)]dy
    >= 1 / integral_-b^b exp[beta v(y)U(z)]dy.

Discard the nonnegative fiber-gradient energy and integrate this inequality over
z. The full Dirichlet infimum has the lower bound

  cap_mu(A,B)>= (1/(beta Z)) integral_R^m 1/R(beta U(z))dz,
  R(t)=integral_-b^b exp[v(y)t]dy,

where Z is the full unnormalized Gibbs integral. All integrals are finite:
1/R(beta U)<=exp[-beta v_min U], since the slab length2b=1. This is equivalent
to optimizing a unit Thomson current with no transverse component, but neither
that current nor its normalization needs to be computed. No fiber mixing or
moment estimate was used. Sobolev/Fubini approximation extends the smooth core.

Homogeneity gives the radial energy measure

  integral f(beta U(z))dz
    = (Z_U beta^(-alpha)/Gamma(alpha))
       integral_0^infinity t^(alpha-1) f(t)dt.              (1)

For example this follows from vol{U<=r}=r^alpha vol{U<=1} and
Z_U=Gamma(alpha+1)vol{U<=1}. It holds for positive integrable f by pushforward,
without an angular chart, partition oracle or convexity.

As Z mu(A)=Z_U beta^(-alpha) MA, the lower rate is

  k_parallel = 1/(beta MA Gamma(alpha))
                 integral_0^infinity t^(alpha-1)/R(t)dt.  (2)

Unknown angular volume and partition factors cancel exactly. Equation(2) is a
proof object; the actual algorithm below will not perform this second integral
or evaluate Gamma.

## 3. Gamma expectation and Jensen remove that extra integral

Write a=1+kappa, Delta(y)=a-v(y)=kappa y^2(2-y^2)>=0 on the slab,
d=max Delta/a=7kappa/[16(1+kappa)]<1. Let T have the Gamma(shape alpha,rate a)
law and S(t)=integral_-b^b exp[-t Delta(y)]dy. Then R(t)=exp(at)S(t), and

  k_parallel/k_free = I_minus E[1/S(T)],
  I_minus=integral_-b^b (1-Delta/a)^alpha dy.

Since S(T)>0, Jensen gives E[1/S]>=1/E[S]. The Gamma Laplace identity and Tonelli
give

  E[S(T)]=I_plus=integral_-b^b (1+Delta/a)^(-alpha)dy,

so k_parallel/k_free>=I_minus/I_plus. Positivity and integrability justify these
operations. E[1/S] is finite because1/S(t)<=exp(t max Delta) and max Delta<a.

## 4. A physical slab contraction proves a finite uniform ratio

Choose eta^2=7/[8(1+d)], so0<eta<1. For |y|<=1/2,

  Delta(eta y)/Delta(y)
    = eta^2 (2-eta^2 y^2)/(2-y^2)
    <= (8/7)eta^2 = 1/(1+d)
    <= 1/(1+Delta(y)/a).

At y=0 take the continuous inequality. Hence

  1-Delta(eta y)/a >= 1/(1+Delta(y)/a).

Raise to alpha>0 and integrate. Restriction to the smaller slab is legitimate
because the integrand is nonnegative:

  I_minus >= integral_-eta b^eta b (1-Delta(y)/a)^alpha dy
          = eta integral_-b^b (1-Delta(eta y)/a)^alpha dy
          >= eta I_plus.

Thus k_parallel>=eta k_free and(P) follows since

  eta^(-2)=(8/7)(1+d)=(16+23kappa)/(14(1+kappa)).

This proof does not rely on the earlier radial field, integration-by-parts
curvature constants, angular equilibrium along trajectories, or a computable
conditional density. Homogeneity and the full-fiber boundary condition are the
critical acquired structure; finite fiber partition and global process existence
remain required. No kinetic claim for other basins, MFPTs, transient preparation,
angular relaxation or time-dependent changes follows.

## 5. Receiving and scientific interpretation

The same acquired raw quartic grammar and exact q/MA/R0 integrator can receive(P)
by replacing the structural factor with an outward square root of the explicit
rational eta^(-2). All beta/task/input/model checks must still be paid. No need
to evaluate the high-dimensional partition, Gamma functions, a two-dimensional
quadrature or current fields. The old source freeze is not silently relabeled.
A separately reviewed wrapper or new consumer version is still needed.

For fixed m,p,kappa,beta, all admitted homogeneous angular models have the same
k_free, and any two full-fiber conductances differ by at most C_parallel even if
coercivity constants and angular laws differ. In particular small d_min cannot
create an arbitrarily large slowdown of this observable within this family.
The frozen-fiber lower bound explains why: the equilibrium reservoir populates
parallel channels that already carry sufficient conductance. Arbitrary-start
kinetics and equilibration of those reservoirs are different questions.
