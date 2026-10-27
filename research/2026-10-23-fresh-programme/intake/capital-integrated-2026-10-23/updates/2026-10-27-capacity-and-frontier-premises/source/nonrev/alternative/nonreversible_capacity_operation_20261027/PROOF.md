# Certified rare excursions without detailed balance

Internal source-class extension, 2026-10-27. The operation accepts a supplied
finite, irreducible, local rational backward generator, an explicitly known
positive invariant law, and a valid lower bound on the gap of its symmetric
part. It produces a deterministic interval for the true exit-law probability
of reaching one state before returning to another. Reversibility is not a
premise. Executed examples use ordinary exact weighted GMRES. This is
neither a mathematical priority claim nor a new generic rarity complexity
class. See RESULTS.md for actual runs, failed lower degrees, and audits.

## 1. Conventions and the exact capacity identity

Let Q be a finite irreducible BACKWARD generator: Q(x,y) is the jump rate
from x to y for x != y, and Q(x,x) = -R_x. Suppose w > 0 is invariant,
w^T Q = 0, with w(a)=1, w(b)=rho in (0,1]. Put

    <f,h>_w = sum_x w(x) f(x) h(x), H=-Q,
    H*=diag(w)^(-1) H^T diag(w), S=(H+H*)/2,
    u=rho 1_a-1_b, Z=sum_x w(x).

Assume <f,Sf>_w >= g ||f||_w^2 on weighted-mean-zero functions, for
supplied g>0. Write H^# for the inverse of H on that subspace, extended by
zero on constants. This is the fundamental/group inverse, not an
unweighted Euclidean pseudoinverse.

Define p_exc as follows: start at a, leave according to q(a,y)/R_a, and
ask whether b is reached before a. Equivalently p_exc=P_a(T_b<T_a^+),
where T_a^+ includes the first departure. Let h(a)=1,h(b)=0 and let h be
Q-harmonic elsewhere. First-step equations give (Hh)(a)=R_a p_exc.
Invariance and harmonicity give (Hh)(b)=-R_a p_exc/rho. Hence

    Hh=(R_a p_exc/rho)u,
    I := <u,H^#u>_w/rho = (H^#u)(a)-(H^#u)(b)
       = rho/(R_a p_exc) > 0,
    p_exc=rho/(R_a I), stationary_capacity=rho/(Z I).

No detailed balance was used. The actual exit rate R_a is essential.

For P_t=exp(tQ), the symmetric-part gap implies contraction on weighted
mean-zero functions: differentiating ||P_t f||_w^2 gives a derivative at
most -2g||P_t f||_w^2. Thus H^#u=integral_0^infinity P_t u dt and

    I=integral_0^infinity f(t) dt,
    f(t)=<u,P_tu>_w/rho
        =rho P_t(a,a)+P_t(b,b)-P_t(a,b)-rho P_t(b,a).

The two cross terms cannot generally be merged. The integrand can be
negative at some times; tail bounds below are two-sided.

## 2. Primal/dual certificate and positive prior bound

For arbitrary real finite-support trial functions y,z, set

    r=u-Hy, s=u-H*z,
    I_hat=(<u,y>_w+<z,r>_w)/rho.

Both residuals have weighted mean zero. Constants in y,z cause no issue.
Writing x=H^#u and using H*z=u-s gives the exact error identity

    I-I_hat = <s,H^#r>_w/rho.

Coercivity and Cauchy-Schwarz give ||H^#r||_w <= ||r||_w/g. Consequently

    |I-I_hat| <= ||r||_w ||s||_w/(rho g).

This is a two-sided enclosure, not the reversible Dirichlet lower bound.
If its lower endpoint is nonpositive or the interval is too wide, the
requested relative target has not been met.

If R_x<=Rmax, write H=diag(R)-B, with B the off-diagonal rates.
Weighted Cauchy-Schwarz and invariance give

    sum_x w_x |(Bf)_x|^2
      <= Rmax sum_y f_y^2 sum_(x!=y) w_x q(x,y)
      = Rmax sum_y w_y R_y f_y^2 <= Rmax^2 ||f||_w^2.

Thus ||H||_w<=2Rmax. Since u=Hx and ||u||_w^2=rho(1+rho),

    rho I=<x,Sx>_w >= g||x||_w^2
          >= g||u||_w^2/(4Rmax^2),
    mu:=g(1+rho)/(4Rmax^2) <= I <= (1+rho)/g.

Intersect residual intervals with this positive prior and all previous
valid intervals. For 0<L<=I<=U, invert outward:

    rho/(R_a U) <= p_exc <= rho/(R_a L).

The probability endpoint ratio is U/L. The code stops only if U/L<=1+eps,
tested exactly as a rational inequality.

## 3. Actual overlapping local circulations

The state space is {0,1}^n. Fix rational theta in (0,1), gamma>0 and put

    w(x)=theta^|x|, a=0^n, b=1^n, rho=theta^n, Z=(1+theta)^n.

The base generator updates each spin by a unit-rate heat bath: 0->1 at
theta/(1+theta), 1->0 at 1/(1+theta). Its product eigenfunctions have
eigenvalues 0,1,...,n for the negative generator; the gap is exactly 1.

For EVERY adjacent pair (i,i+1), and each fixed outside configuration,
add the directed cycle

    00 -> 10 -> 11 -> 01 -> 00.

Its local weights are 1,theta,theta^2,theta. Give each directed edge the
constant local flow c=gamma theta^2: its rate is c/w_local at its source.
These rates are gamma theta^2,gamma theta,gamma,gamma theta in cycle
order. Multiplying by the outside weight shows that incoming and outgoing
stationary flow are equal at every cycle state. Each cycle therefore
preserves w, as does their overlapping sum. The adjoint reverses every
cycle and has the same diagonal exit rates.

For each stationary added generator C,

    <f,-Cf>_w=(1/2)sum_(x,y)w_x c(x,y)(f_y-f_x)^2 >=0.

Thus the symmetric part of the full H dominates the base Dirichlet form,
and g=1 is a valid GLOBAL lower bound without state-space enumeration.
The positive base rates imply irreducibility. Valid rate data are

    R_a=n theta/(1+theta)+(n-1) gamma theta^2,
    Rmax=n/(1+theta)+(n-1) gamma.

At the boundary edge 0^n -> (1,0,...,0), the unnormalised stationary net
current is gamma theta^2>0, so detailed balance fails. Its normalized
current is gamma theta^2/Z. Rates also depend on neighboring spins: the
rate flipping bit 0 from 0 to 1 is theta/(1+theta)+gamma theta^2 when
bit 1 is 0, but theta/(1+theta) when bit 1 is 1. These are interacting
nonequilibrium dynamics; the invariant Gibbs law itself has product form.
No nonproduct invariant law is claimed here.

The executed parameters are theta=1/4,gamma=1/2, giving a common rate
denominator D=160, circulation c=1/32 and symmetric-gap lower bound g=1.

## 4. Exact finite-support Krylov arithmetic

For theta=p/q in lowest terms, let W=q^n,N=p^n and integer weights
omega_x=W w_x=q^(n-|x|)p^|x|. Let A=D H and A*=D H*, with integer
entries. Start v0=Wu=N 1_a-W 1_b and separately compute

    v_j=A^j v0, d_j=(A*)^j v0, 0<=j<=k.

Choose alpha,beta by exact weighted least squares, minimizing

    ||v0-sum_(j<k)alpha_j v_(j+1)||_omega,
    ||v0-sum_(j<k)beta_j d_(j+1)||_omega.

These are ordinary weighted GMRES iterates in their respective Krylov
spaces, implemented using exact small normal equations. Exact arithmetic
avoids floating conditioning in those solves. Dependent bases cause an
explicit error; no singular inverse is silently accepted. Set

    Y=sum_(j<k)alpha_j v_j, Zt=sum_(j<k)beta_j d_j,
    R=v0-A Y, St=v0-A* Zt,
    y=(D/W)Y, z=(D/W)Zt.

If [.,.] denotes the integer-weight inner product, the certificate is

    I_hat=D([v0,Y]+[Zt,R])/(W^2 N),
    radius=sqrt([R,R][St,St])/(W^2 N g).

All Gram entries, coefficients and squared norms are exact. The square
root is rounded UP to a dyadic rational with 256 fractional bits, using
integer square root followed by an exact squared inequality check. JSON
stores the exact rational endpoints in hexadecimal; floats only describe
them. The small full-state controls also verify these scaling formulas.

Backward H is not forward-law multiplication. Scattering a supported
value at x into Hy requires all predecessor states y and the rates q(y,x).
The dual uses the weighted adjoint's predecessors. Both implementations
include the full neighbor closure, including rows outside trial support.
The independent large audit instead gathers outgoing differences at every
candidate row, using a separate literal semantic-cycle implementation.

Every transition flips exactly one bit. Powers through degree k therefore
live in the union of Hamming balls of radius k about a and b, containing
at most min(2^n,2 sum_(j=0)^k binomial(n,j)) states. This can grow
exponentially if k grows. No uniform low-degree theorem is claimed.
Source description, computation of rho, weight powers, bit operations,
dictionary storage, primal AND dual work, and independent audit costs all
remain part of the operation. The interval is for the supplied model;
finite local data cannot prove global stationarity, support or a gap for
an unknown physical system.

## 5. Equally informed ordinary Monte Carlo and finite-bit sampling

All ordinary methods receive the SAME generator, known invariant ratio,
gap promise and constructions above. Rarity alone is not a 1/p sampling
barrier under these premises.

A Markov-specific inequality is stronger than the Schur norm argument:

    ||Hf||_w^2
      <= Rmax sum_(x,y) w_x q(x,y)(f_x-f_y)^2
      =2Rmax <f,Sf>_w.

Applying this to H^#u proves the sharper positive prior

    mu1=(1+rho)/(2Rmax) <= I.

The executed certificate code conservatively uses the earlier, weaker
mu; its reported intervals are valid without changing those runs. The
stronger prior is available to every method and is used below.

The endpoint maximum principle gives another ordinary positive prior
if the actual exit R_b is known: I>=max(rho/R_a,1/R_b). For the harmonic
hit-b-before-a function h, with h(a)=0,h(b)=1, one has
Hh(b)=R_a p_exc/rho<=R_b, while p_exc<=1. The saved certificates and
conservative budgets below do not need this additional tightening.

Continuous-time version: |f(t)|<=(1+rho)exp(-gt) and the absolute tail
after T is at most (1+rho)exp(-gT)/g. For uniform t in [0,T], simulate
independent trajectories from a,b conditional on t and average

    Y=T[rho 1{Xa_t=a} -1{Xa_t=b} +1{Xb_t=b} -rho 1{Xb_t=a}].

Its expectation is the truncated integral and its range length is
2(1+rho)T. The truncation uncertainty is TWO-SIDED. This statement uses
the exact trajectory-law simulation premise.

There is also an exact rational discrete version that avoids continuous
random times. Set Lambda=2Rmax and P=I-H/Lambda. This is a lazy Markov
matrix preserving w. Expanding its squared weighted norm and using the
Markov inequality above gives, on mean-zero functions,

    ||Pf||_w^2 <= ||f||_w^2 - <f,Sf>_w/Lambda
                 <= (1-g/Lambda)||f||_w^2.

Consequently ||P||<=sqrt(1-g/Lambda)<=tau:=1-g/(2Lambda)<1. On this
subspace the absolutely convergent Neumann series gives

    I=(1/Lambda)sum_(k>=0) <u,P^k u>_w/rho,
    |tail after L| <= 2(1+rho)tau^(L+1)/g.

Choose eta=eps/16 and an integer L with this tail <=eta mu1. Sample k
uniformly from {0,...,L}, independently simulate k P-steps from a and b,
and average

    Y=(L+1)/Lambda * [rho 1{Xa_k=a} -1{Xa_k=b}
                     +1{Xb_k=b} -rho 1{Xb_k=a}].

The range length is 2(1+rho)(L+1)/Lambda. Hoeffding gives sampling error
at most eta mu1 with probability >=1-delta for

    samples N >= 2(1+rho)^2 (L+1)^2
                 /(Lambda^2 eta^2 mu1^2) * log(2/delta).

Together with truncation, [mean(Y)-2eta mu1,mean(Y)+2eta mu1] covers I
on that event. Intersect with I>=mu1 and invert positive endpoints. On
the covering event, endpoint ratio <=(1+4eta)/(1-4eta)<=1+eps for
0<eps<1. Thus this is a relative probability confidence interval.

For rational supplied rates and Lambda, P-steps are sampled using finite
integer cumulative weights. Rejection from a binary uniform integer has
expected fewer than two attempts. Index k is sampled the same way. With
efficiently evaluable rational local rates and represented weights,
expected bit cost is polynomial in input bit length, state size, L and N.
At most 2NL P-steps occur; local enumeration adds its actual size/bit cost.
One may choose L=O((Rmax/g)log(Rmax/(eta g))), and N is polynomial in
Rmax/g, 1/eps and log(1/delta), with no factor 1/p or 1/rho. This is an
expected random-bit cost statement, not a deterministic maximum number
of rejection bits. It does not acquire a physical source or stationary
weights, and a tiny gap remains expensive. The displayed conservative
budget can be enormous; no large Monte Carlo sample experiment is being
represented as executed. Statistical confidence differs from the exact
deterministic intervals actually executed here.

## 6. Adversarial control and primary antecedents

The independent three-state control in CONTROLS_SMALL.json has unit
invariant weights, clockwise rate 2 and counterclockwise rate 1. For
a=0,b=2, its exact values are R_a=3,p_exc=7/9,I=3/7 and symmetric gap
9/2. With y=z=(3/14)(1,0,-1), both residual squared norms are 1/14 and
I_hat=87/196 > 3/7. Radius 1/63 covers the error. Thus even this natural
choice gives an estimate ABOVE I; importing the reversible one-sided
lower-bound assertion would be false. A rational uniformisation kernel
also disproves merging the two cross terms. The parent supplied the
example; controls.py assembles it and verifies it independently.

Primary-source screen performed 2026-10-27 using public read-only web
retrieval. Firecrawl was not retried because its credits were exhausted.

- Gaudilliere and Landim, *A Dirichlet principle for non reversible Markov
  chains and some recurrence theorems*, arXiv:1111.2445 (2011), especially
  Section 2, Definition 2.1, Theorem 2.4 and Section 2.2. Their backward
  generator, stationary adjoint, escape-capacity relation, symmetric part,
  and divergence-free cycle flows directly precede this construction.
  The finite-state singleton capacity formula also uses the inverse's
  symmetric part. Our unnormalised w becomes their measure w/Z when
  reporting stationary capacity. Their work rules out presenting
  nonreversible capacity prediction itself as new.
  [Full primary text](https://arxiv.org/html/1111.2445).
- Saad and Schultz, *GMRES: A Generalized Minimal Residual Algorithm for
  Solving Nonsymmetric Linear Systems*, SIAM J. Sci. Stat. Comput. 7(3),
  856-869 (1986), DOI 10.1137/0907058. Residual minimization over Krylov
  spaces is the ordinary solver used here. A positive weighted inner
  product changes the norm, not this method's identity. Exact small normal
  equations are an implementation choice at the low degrees executed.
  [Publisher](https://epubs.siam.org/doi/10.1137/0907058),
  [Primary paper PDF](https://web.stanford.edu/class/cme324/saad-schultz.pdf).
- Becker and Rannacher, *An optimal control approach to a posteriori error
  estimation in finite element methods*, Acta Numerica 10, 1-102 (2001),
  DOI 10.1017/S0962492901000010. The publisher's abstract describes
  estimating a target functional using residuals and an approximately
  solved adjoint. This is a relevant primary antecedent for the
  primal/dual goal-error construction; this screen read the abstract,
  not the full article. The finite Markov identity and explicit coercivity
  bound used here are proved directly above.
  [Publisher abstract](https://www.cambridge.org/core/journals/acta-numerica/article/abs/an-optimal-control-approach-to-a-posteriori-error-estimation-in-finite-element-methods/5C67A03F528C6FA69F37A97DF5C3BE19).

This is a focused antecedent screen, not an exhaustive novelty audit. The
accepted scope is a proved and executed extension of this program's
source contract to known-law nonreversible local chains. Novel mathematics,
physical acquisition, robustness to arbitrary hidden shocks, empirical
validation, publication, and practical superiority remain unestablished.
