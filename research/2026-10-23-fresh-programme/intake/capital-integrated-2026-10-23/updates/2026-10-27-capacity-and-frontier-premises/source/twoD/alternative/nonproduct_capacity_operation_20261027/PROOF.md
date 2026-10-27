# Exact nonproduct two-dimensional rare-excursion certificate

This is an executed application of ordinary finite reversible potential
theory and exact Galerkin residual bounds. The new scope within this local
research branch is an explicitly nonproduct, non-count-lumpable
two-dimensional Gibbs source. There is no priority, new complexity class,
physical validation, or computational superiority claim.

## 1. Exact source and output

Let G be the simple nearest-neighbor square graph on (Z/8Z)^2. It has 64
vertices and 128 undirected edges. A state x assigns one bit x_i to each
vertex. Write n(x)=sum_i x_i and e(x)=sum_{ij in E} x_i x_j. Set

    theta=1/4, kappa=9/8,
    w(x)=theta^n(x) * kappa^e(x),
    a=all zero, b=all one,
    rho=w(b)/w(a)=9^128/2^512.

Every site has an independent rate-one resampling clock. Given k occupied
neighbors, its new bit is Bernoulli(p_k), where

    r_k=theta*kappa^k=9^k/(4*8^k),
    p_k=r_k/(1+r_k)=9^k/(4*8^k+9^k),  k=0,...,4.

Thus q(x,x^i)=p_k if x_i=0 and 1-p_k if x_i=1; x^i flips only i.
The BACKWARD generator is

    (Qf)(x)=sum_i q(x,x^i)*(f(x^i)-f(x)),  H=-Q.

All flip rates are positive, so this finite chain is irreducible on all
2^64 states. Flipping 0 to 1 multiplies w by r_k and satisfies

    w(x)*p_k=w(x^i)*(1-p_k).

Therefore w is an invariant reversible weight. No partition function is
needed for the output below. The clock convention is continuous time with
one clock per site; a discrete chain with one randomly chosen site per
step has a different time normalization.

Let sigma_a be the first actual exit time from a, and tau_a^+ the first
return to a after sigma_a. The certified quantity is the TRUE exit-law
probability

    p_exc=P_a(tau_b < tau_a^+).

Here R_a=sum_y q(a,y)=64/5; the exit distribution is uniform over the 64
single occupied-site states. The normalization R_a must be retained.

The spin substitution x_i=(1+s_i)/2 rewrites log w, up to a constant, as

    J*sum_edges s_i*s_j + h*sum_i s_i,
    J=(log kappa)/4 > 0, h=(log theta)/2+log kappa=log(9/16) != 0.

This is a square-lattice Gibbs/heatbath source with interactions and
nonzero field. This work supplies no Gaussian or free-fermion reduction
and uses none. The exclusions proved next concern the natural site-bit
product structure and the indicated lumpings; they do not assert that
every possible hidden representation has been ruled out.

## 2. Explicit nonproduct and non-lumpability witnesses

Fix every bit outside an adjacent pair i,j to zero. Its conditional
unnormalized weights are 1, theta, theta, theta^2*kappa. Their cross ratio
is

    w11*w00/(w10*w01)=kappa=9/8 != 1.

A positive product measure has cross ratio one on every such pair.
Consequently this Gibbs measure is not a product over its site bits.

For total-count lumpability, compare two occupied adjacent sites with two
occupied well-separated sites. Both have n=2. The total rate into n=1 is

    adjacent: 2/(1+theta*kappa)=64/41,
    separated: 2/(1+theta)=8/5.

The rates differ, violating the necessary equal aggregate-row-rate
condition for a strongly lumpable count chain.

Even (n,e) is insufficient. Three occupied sites at coordinates
(0,0),(1,0),(2,0) form a line; (0,0),(1,0),(0,1) form an L. Both have
(n,e)=(3,2). The line has no empty site with two occupied neighbors, while
the L has one at (1,1). Hence their rates into (n,e)=(4,4) are respectively
0 and p_2=81/337. This also violates strong lumpability. The birth-rate
second difference p_2-2p_1+p_0=92/69085 is nonzero.

The independent source checker evaluates all these weights and aggregate
rates as exact Fractions, separately from the production operator.

## 3. Exact positive spectral-gap proof

The five conditional probabilities are

    (p_0,...,p_4)=(1/5,9/41,81/337,729/2777,6561/22945).

Changing one neighbor changes this Bernoulli law by at most

    c=max_{k=0,...,3}(p_(k+1)-p_k)
     =1492992/63718265,
    g=1-4*c=57746297/63718265 > 0.

For completeness this bound is derived here in the actual clock units.
Use the same rate-one site clocks and the same uniform variable U for two
chains; at an update of i set each bit to 1 iff U<=p_k for its own
neighbor context. If D(x,y)=sum_i |x_i-y_i|, an i update creates a bit
discrepancy with conditional probability at most

    c*sum_{j adjacent i}|x_j-y_j|.

Summing its drift over i and using the square graph's degree four gives

    coupling_generator D <= -(1-4*c)*D,
    E[D(X_t,Y_t)] <= exp(-g*t)*D(X_0,Y_0).

To obtain a gap bound, let f be a nonconstant eigenfunction of H with
positive eigenvalue lambda. On this finite configuration hypercube let
Lip(f) be the maximum absolute difference over adjacent configurations;
it is positive. Coupling gives Lip(P_t f)<=exp(-g*t)*Lip(f), whereas the
eigenfunction identity gives Lip(P_t f)=exp(-lambda*t)*Lip(f). Thus every
positive eigenvalue is at least g. Reversibility makes this exactly the
spectral-gap statement needed below. This is a global analytic source
proof, not an inference from the finitely visited states.

## 4. Potential identity and deterministic residual bound

Use the unnormalized inner product <f,h>_w=sum_x w(x) f(x) h(x). Define

    u=rho*1_a-1_b,
    I=<u,H^+u>_w/rho.

We have <1,u>_w=0. The pseudoinverse acts on this mean-zero subspace.
One direct derivation of the excursion identity uses
h(x)=P_x(tau_b<tau_a), with h(a)=0,h(b)=1. Then Hh is zero in the
interior, Hh(a)=-R_a*p_exc, and weighted stationarity implies
Hh(b)=R_a*p_exc/rho. Therefore

    Hh=-(R_a*p_exc/rho)*u,
    H*(-rho*h/(R_a*p_exc))=u,
    I=rho/(R_a*p_exc),
    p_exc=rho/(R_a*I).

The associated unnormalized capacity is R_a*p_exc=rho/I. Normalized
stationary capacity would be rho/(Z*I), where Z=sum_x w(x); Z is not
computed or claimed here. These identities are established reversible
potential theory; see the primary antecedents below.

For any finite-support y define r=u-Hy and

    L=(2<u,y>_w-<y,Hy>_w)/rho.

Writing f=H^+u and completing the square gives

    I-L=<f-y,H(f-y)>_w/rho=<r,H^+r>_w/rho.

The constant part of y causes no problem, and <1,r>_w=0. Since the gap
is at least g,

    L <= I <= L+<r,r>_w/(rho*g).

Every term is an exact finite sum when the complete support of Hy is
included. Positive I bounds invert to probability bounds in the opposite
order. A wide interval remains a valid unresolved-width result.

## 5. Local, exact integer-scaled operation

The common positive rate denominator and invariant weight scale are

    D=lcm(5,41,337,2777,22945)=880395267505  (40 bits),
    B=4^64*8^128=2^512                   (513 bits),
    N=B*rho=9^128,
    W(x)=B*w(x)=2^(512-2*n(x)-3*e(x))*9^e(x),
    A=D*H,  v_0=B*u=N*1_a-B*1_b,  v_j=A^j*v_0.

All W(x) are positive integers: 2*n+3*e<=512. Production weight
propagation across an edge uses exact detailed balance
W(y)=W(x)*[D*q(x,y)]/[D*q(y,x)] and checks exact division and consistency.

Each v_j is supported on Hamming balls of radius j around a and b.
For j<=3 they are disjoint and contain

    2*sum_(l=0)^j binomial(64,l)

states. No outside contribution is discarded: v_j is the FULL power on
that support. In particular a degree-three trial uses v_0,v_1,v_2, and
its entire residual uses v_0,...,v_3. "Local" refers here to state-graph
balls; every spatial site is included in each source row evaluated.

For <v,z>_W=sum_x W(x)v(x)z(x), solve the k-by-k exact Galerkin system

    S_ij=<v_i,A*v_j>_W,  t_i=<v_i,v_0>_W,
    S*alpha=t,  i,j=0,...,k-1.

The trial is y=(D/B)*sum_j alpha_j v_j. Let
E=t^T alpha, beta=(1,-alpha_0,...,-alpha_(k-1)), and
G_ij=<v_i,v_j>_W for 0<=i,j<=k. Then

    L=D*E/(B^2*N),
    U=L+(beta^T*G*beta)/(B^2*N*g).

The script also intersects with the generic spectral enclosure
(1+rho)/(2*64)<=I<=(1+rho)/g and all earlier valid enclosures. A dependent
Krylov basis raises an explicit exact singular-system error; this fixture
has independent vectors through the executed degree three.

Operator orientation matters. For sparse column propagation from a
supported state x, the contribution at neighbor y is
-D*q(y,x)*v(x), using the BACKWARD predecessor rate, not q(x,y).
Independent verification instead evaluates each complete backward row at
a separately generated candidate state, so this particular error cannot
be concealed by duplicating the propagation rule.

## 6. Ordinary comparators under the same promises

The exact operation above IS an ordinary Galerkin/Krylov method. An
equally informed ordinary solver receives the same source, gap, rho,
local weights, exact arithmetic and residual support; it can run the
identical operation and obtains the same certificate. No timing
leaderboard or superiority comparison is inferred from this experiment.

There is also no justified generic 1/p Monte Carlo lower bound here.
With P_t(x,y) denoting start x, end y, the positive-gap potential kernel
satisfies

    f(t)=<u,exp(-t*H)u>_w/rho
        =rho*P_t(a,a)+P_t(b,b)-2*rho*P_t(b,a) >= 0,
    I=integral_0^infinity f(t)dt,
    mu=(1+rho)/(2*Rstar)<=I, Rstar=64,
    integral_T^infinity f <= (1+rho)*exp(-g*T)/g.

Choose uniform t in [0,T] and independent exact-law trajectories from a
and b. The sample

    Y=T*(rho*1{Xa_t=a}+1{Xb_t=b}-2*rho*1{Xb_t=a})

has the truncated integral as its expectation and range length at most
(1+3*rho)*T. Independent replicate averages have additive error eta*mu
with failure probability at most delta when

    samples >= (1+3*rho)^2*T^2*log(2/delta)/(2*eta^2*mu^2).

If the tail is at most eta*mu, intersecting the integral interval with
I>=mu gives relative interval width at most 3*eta on this event. Invert
as above. With epsilon=1/1000, eta=1/4000, delta=1/20 and T=15, exact
positive Taylor lower polynomials verify the tail condition and
log(40)<4. The conservative sufficient count is 117964800000001
replicates, with two trajectories each. Uniformization at Rstar yields
expected event count at most 226492416000001920 using the conservative
horizon bound. This loose analytic bound is NOT an executed or optimal
Monte Carlo cost, and is not evidence of superiority over it.

For bounded local rates and polynomial inverse gap, this sample/event
bound is polynomial in source size and inverse tolerance, with no 1/p.
It assumes exact-law finite-time simulation and independent randomness;
it is not a full exact finite-bit simulator theorem. Computational
initialization at b is also not physical preparation of b.

## 7. Primary antecedents read for this construction

- [Aldous and Fill, continuous-time occupation and hitting identities,
  section 2.2.3](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch2.S2.html)
  and [Dirichlet/capacity principles, section 3.7](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch3.S7.html).
  The latter explicitly includes the continuous-time exit-rate factor.
- [Hestenes and Stiefel, Methods of Conjugate Gradients for Solving Linear
  Systems, 1952](https://math.nist.gov/mcsd/Reports/2002/hestenes-steifel-52.pdf).
  The original exact linear-system iteration is longstanding.
- [Golub and Meurant, Matrices, Moments and Quadrature, 1994 report](https://web.stanford.edu/class/cme335/sccm93-07.pdf)
  studies bounds for matrix-function bilinear forms, including inverse
  entries, through Lanczos/quadrature. The opening page of
  [Matrices, Moments and Quadrature II](https://www.gerard-meurant.fr/cgestbit_1997.pdf)
  explicitly gives e=A^-1*r and ||e||_A^2=r^T*A^-1*r and develops CG
  error bounds. These directly rule out treating the residual identity
  or inverse-quadratic-form operation as new here.
- [Benzi and Razouk, Emory TR-2007-003](https://www.cs.emory.edu/technical-reports/techrep-00021.pdf)
  develops sparse-matrix function localization and polynomial
  approximation. Its matrix dimension is not the number of lattice
  sites; no linear-in-64 consequence of that paper is assumed here.
- [Hayes, A simple condition implying rapid mixing of single-site
  dynamics on spin systems, FOCS 2006](https://www.cs.unm.edu/~hayes/papers/EigenvalueDobrushin/EigenvalueDobrushin-FOCS06.pdf)
  defines heatbath single-site dynamics and influence conditions. The
  exact continuous-time gap required here was proved directly above.

This is a focused antecedent check, not a comprehensive novelty audit.

## 8. Scope of the achieved extension

The construction certifies the supplied exact 64-site nonproduct model.
It goes beyond the earlier Gaussian-reference and product-conditioned
one-dimensional fixtures in SOURCE CLASS, using the same ordinary
residual method. Degree three happens to resolve this fixture; this is
not a theorem of uniform low degree for all two-dimensional sources or
parameters. State-ball growth and rational bit growth remain real
costs. The input gap, locality, reversibility and invariant ratio must
come from valid structural knowledge; finite observations do not acquire
them. No empirical kinetics, hardware behavior, practical advantage,
publication, or priority is established by this calculation.
