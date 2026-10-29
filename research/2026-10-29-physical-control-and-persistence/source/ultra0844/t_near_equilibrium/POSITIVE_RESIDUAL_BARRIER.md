# A moment-matched near-equilibrium source defeats scalar positive defects

29 October2026. Actual homogeneous3D hard spheres, angular measure normalized
to one, kernel |v-w|. This is a scoped obstruction to a specific cost-compression
mechanism. It is not a lower bound against all exact iid samplers, a denial of
spectral relaxation, or a new discovery that the usual linearized Boltzmann
operator is signed. Primary LVDSMC already makes that sign explicit.

## 1. Why this is the load-bearing interface

A tempting normalized shortcut would keep a known equilibrium reservoir and
simulate only a small positive residual:

    f_t = alpha(t) M +(1-alpha(t)) r_t,
    r_t>=0, int r_t=1.

If such a process were explicit, a near-equilibrium residual could replace
the full exponential-time ancestry. The reservoir's positivity cannot be
assumed from TV closeness, an L2 spectral gap, or signed deviational particles.
We test the tight available source share alpha(0)=1-delta, without an evolved
density oracle.

## 2. Source with fully acquired density, sampler and invariants

Let M(v)=(2pi)^(-3/2)exp(-|v|^2/2). Define B as uniform density on the ball
|v|<=2 and S as uniform density on the shell3/2<=|v|<=2. Put

    r=(41/189) B +(148/189) S,
    B=3/(32pi) on its ball,
    S=6/(37pi) on its shell.

These are explicit normalized densities. Their radial squared means are
12/5 and2343/740, so r has mean squared speed EXACTLY3. Spherical symmetry
gives mean zero and covariance I. The maximum density of r is33/(224pi).
Consequently

    r(v)/M(v) <= 33sqrt(2pi)exp(2)/112 <6,

using sqrt(2pi)<8/3 and exp(2)<15/2. Let

    f_delta=(1-delta) M+delta r, 0<delta<1.

It has exactly the same mass, momentum and energy as M, and

    ||f_delta/M-1||_infinity <=5delta.                    (1)

Thus delta can be arbitrarily small in a GLOBAL relative-density promise,
not merely a weak norm. Its density and sampler are supplied explicitly:
choose the mixture, sample M normally, or a uniform direction and radius
[r_in^3+U(r_out^3-r_in^3)]^(1/3). No future distribution, physical gas source
or fitted source parameter is granted. This is a qualified mathematical
source shared with every comparator.

## 3. Governing ordinary hard-sphere kernel

For a signed density g, the linearized operator at M is

    Lg=Q(M,g)+Q(g,M)
      =int [2K1(v,w)-K2(v,w)]g(w)dw -nu_M(v)g(v),
    K1(v,w)=exp[-(v dot n)^2/2]/[pi |v-w| sqrt(2pi)],
    K2(v,w)=|v-w| M(v), n=(v-w)/|v-w|.

These are the established hard-sphere Carleman/Hilbert kernels, e.g.
Radtke--Hadjiconstantinou--Wagner, 'Low Variance Particle Simulations ... VHS',
https://web.mit.edu/ngh/www/Radtke_RGD27.pdf, equations6--9, specialized to
beta=1, C_beta=1/(4pi), thermal variance1. The plane Gaussian integral is
(2pi)^(-1/2)exp[-(v dot n)^2/2]. This specialization pays our angular rate
normalization; it does not borrow the dimensional diameter prefactor.

Divide the off-diagonal kernel by M(v):

    [2K1-K2]/M(v) =4 exp(|v_perp|^2/2)/|v-w|-|v-w|,       (2)

where v_perp=v-(v dot n)n=w-(w dot n)n. In particular |v_perp|<=|w|.

## 4. Exact tangent obstruction on an open finite-velocity region

For |w|<=2 and |v|>=8, put z=|v-w|>=6. From (2),

    [2K1-K2]/M(v) <=4exp(2)/z-z
                  <30/6-6=-1.                          (3)

The bound is uniform over all source positions, not an angular quadrature
or one selected collision. Also r(v)=0 here. A collision of two velocities
of speed<=2 has outgoing squared speed<=8, so Q(r,r) is zero on |v|>=8.
Since Q(M,M)=0 and LM=0,

    Q(f_delta,f_delta)(v)
      =delta(1-delta)Lr(v)+delta^2 Q(r,r)(v)
      <=-delta(1-delta)M(v), |v|>=8.                     (4)

Take any nonzero smooth nonnegative test phi supported in8<|v|<9. Initially
int phi[f_delta-(1-delta)M]=0, while its right time derivative from (4) is
strictly negative. The cutoff hard-sphere weak/mild equation supplies this
initial tangent (our density has Gaussian decay and bounded compact parts).
Therefore for sufficiently small positive t,

    f_t-(1-delta)M is NOT a positive measure.             (5)

This avoids assuming pointwise differentiability at a shell boundary or an
unproved positivity-preserving linearized semigroup. The test is supported
far outside every source boundary. It excludes a fixed-share positive
normalized residual even with the unusually strong promise (1).

## 5. No finite scalar depletion speed from the tight share

The same argument is stronger than (5). For |v|>=V>2,

    Lr(v)/M(v) <= -c_V,
    c_V=(V-2)-4exp(2)/(V-2) ->infinity.

The quadratic gain remains zero for V>sqrt(8). If alpha is right
differentiable at0 with alpha(0)=1-delta and finite alpha'(0), then a
test supported outside a sufficiently large V has

    d/dt int phi[f_t-alpha(t)M]|_0
      <=[-delta(1-delta)c_V-alpha'(0)] int phi M <0.

Thus NO such finite-rate scalar reservoir depletion preserves positive
residuals on all velocities. In particular alpha(t)=(1-delta)exp(-gamma t)
with any finite gamma fails. This is an actual unbounded hard-rate/tail
interface, not a bad choice of one finite clock or a small numerical margin.

It does not exclude starting with a strictly smaller reservoir share,
a different-temperature or time-dependent reference, a nonsmooth instantaneous
depletion, correlated multi-particle representations, or a sampler not of
this convex-reservoir form. We do not infer inf_v f_t/M=0 for every t>0:
that stronger tail assertion needs a separate theorem and is NOT proved here.

## 6. Positive scalar gauge cannot repair the signed tangent

Conjugation by any positive velocity weight q(v) changes the linearized
off-diagonal kernel to q(v)[2K1-K2](v,w)/q(w). Its sign is unchanged.
In particular the conserved-currency q=h/c used by our exact hard-sphere
lineage cannot turn this defect operator into a one-velocity positive
Markov/branching generator. Its finite-time normalized sampler is correct;
the hoped-for equilibrium-compression consequence does not follow.

A related raw signed-query shortcut also lacks the Maxwell route's bounded
mark payment. In relative variables u=(f-M)/M its off-diagonal kernel is
Ktilde(v,w)=M(w)[2K1-K2](v,w)/M(v). Since LM=0,

    int Ktilde(v,w)dw=nu_M(v),
    int |Ktilde(v,w)|dw-nu_M(v)
        =2 int (-Ktilde(v,w))_+dw >0, |v|>=8.

Indeed the ball |w|<=2 alone gives a strictly positive lower bound by (3).
Thus sampling the absolute combined kernel with signs and treating nu_M as
the killing rate is not a substochastic one-particle estimator. This does
not refute spectral cancellation, a projected operator, correlated signs or
another representation. It prevents importing a norm-one direct-mark claim
from the earlier covariance/Maxwell construction into this raw hard kernel.

## 7. Ordinary comparison and the remaining opening

LVDSMC deliberately uses signed deviational particles and processes the
combined2K1-K2 creation/deletion kernel. It handles exactly the negative
tangent that defeats (5); its variance-reduction claims concern approximate
observable simulation, not an exact iid normalized full-law output. Wagner's
nonlinear deviational method is therefore a serious incumbent, not a failed
version of our proposed positive shortcut.

Constructive near-Maxwellian spectral estimates control relaxation in their
stated function spaces. They are not positivity or pointwise-minorization
theorems for this reservoir, and replacing the evolved law by M at an unpaid
tolerance does not meet exact output. CFTP for equilibrium Boltzmann weights
in statistical mechanics also does not directly sample a nonstationary
nonlinear kinetic f_t.

The exact faster-than-exponential iid hard-sphere target remains OPEN here.
The tested fixed-reference positive-defect mechanism is decisively excluded
at a source class where initial density, invariants, nearness and sampling
are all acquired. A new positive representation or a paid nonlocal cancellation
operation, rather than a freely normalized signed residual, is required.
