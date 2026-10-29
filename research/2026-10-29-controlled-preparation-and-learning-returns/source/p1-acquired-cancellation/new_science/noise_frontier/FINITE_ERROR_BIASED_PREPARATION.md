# Finite-error biased preparation with a warranted density contract

29 October 2026. New complementary construction, not an independent re-audit
of the exact affine preparation theorem. No physical reset or acquisition was
performed. The chosen consequence is repeatable complete visible service after
an ACTUAL biased operation word, even when its hidden state retains memory.

## 1. A useful actual-operation class

Work in the acquired baseline Hilbert space H=L2(pi). The finite feature space
V contains1 and is exactly label-local, built by multiplying features by label
indicators. Let P be its orthogonal projection. Thus all visible multiplication
operators preserve V, irrespective of approximate dynamical closure.

Let W be an actually executable word of physical Markov kernels. Assume its
operations share the known reversible weight w(Y)>0, so they each preserve

    mu_*(dx)=g_*(x)pi(dx), g_*=w(Y)/pi(w).

The product W need NOT be reversible, but it preserves mu_*. This condition is
warranted by the actual-operation interface, not inferred from fitted outputs.
It requires no physical preparation of mu_* and no hidden convergence to mu_*.
Different kinetic prefactors among these operations are allowed. Their common
weight is substantive; an arbitrary cycle of differently biased operations does
not automatically satisfy this theorem.

Put R=sqrt(max w/min w). Markov contraction in L2(mu_*) and norm equivalence
give the global power bound

    ||W^n||_(L2(pi))<=R,  all n>=0.                         (1)

No full microscopic gap or mixing bound is used. Also ||g_*||_2<=R.

The true compression is B=P W|V. It preserves1. With ell=pi, P0 v=v-ell(v)1,
write

    A=P0 B|V0, b=ell B|V0, V0=V intersect ker ell.

Assume finite confidence/numerical bounds certify ||A||<=kappa<1 and an upper
bound on

    e=||(I-P)WP||.                                          (2)

B and e are acquired from K=<F,WF> and the Gram of WF, using actual weighted
adjoint words. For non-self-adjoint W the residual is

    <WF,WF>-K* G^-1 K,

not D-KG^-1K unless symmetry has separately been established. The existing
controlled-future-word construction can acquire this larger moment setting;
its word depth, preparations, weights and independent clocks are charged.

## 2. The affine prepared functional remains physically fixed under leakage

Because g_* is a visible function, g_* belongs to V. Consequently

    ell_*(Bf)=<g_*,P Wf>_pi=<g_*,Wf>_pi=<g_*,f>_pi,
    ell_*(f):=mu_*(f).

This holds even when e>0. The unique normalized invariant functional of B is
therefore the restriction of the GENUINE mu_* law. In affine coordinates,

    ell_*(f)=ell(f)+b(I-A)^-1 P0 f=mu_*(f).                  (3)

The right side is acquired from baseline visible weights and moment functionals.
Its positivity is supplied by the actual known weighted stationary measure,
not guessed from a signed inverse. There is no assertion that the physical
hidden distribution after finitely or infinitely many W calls equals mu_*.

This removes an avoidable functional-conditioning problem: when the invariant
weight is known, use (3)'s right side to specify the target. The affine inverse
can serve as a consistency check, while its finite numerical errors remain
accounted. A general word with no warranted common invariant weight lacks this
particular improvement.

## 3. Finite leakage produces a controlled preparation floor

Let the actual starting law have density g relative to pi, with a warranted
||g||_2<=K and pi(g)=1. Write

    H0=||P(g-g_*)||_2
       <=sqrt(K^2-1)+||g_*-1||_2.

Then the difference of prepared and target initial functionals on centered V
is bounded by

    d_m=H0 kappa^m
           +K R e (1-kappa^m)/(1-kappa).                    (4)

Proof. Let E=WP-PB, so E1=0 and ||E||=e. Discrete Duhamel gives

    W^m P-P B^m=sum_(j=0)^(m-1) W^(m-1-j) E B^j.

For f in V, the affine formula for B^j f has a constant part plus A^j P0 f.
E kills its constant part. Hence (1) yields

    ||(W^m-B^m)f||_2
       <=R e (1-kappa^m)/(1-kappa) ||P0 f||_2.              (5)

Pair with g and use ||g||<=K. The compressed difference from the invariant
functional is <g-g_*,A^m P0 f>, bounded by H0 kappa^m ||P0 f||. This proves
(4). For an event effect in V, ||P0 f||<=1/2, so its preparation error is at
most d_m/2. Neither exact closure nor an empirical exact zero was substituted.

The leakage term saturates instead of growing linearly with word count. The
reason is that every subsequent leakage insertion acts on the already contracting
centered predictive component. This is stronger than the coarse bound m e.
It does not remove the asymptotic floor K R e/(1-kappa).

Without the common-invariant-weight condition, a warranted bound on ||W^n||
can replace R in the sum. The elementary bound ||W||^n may grow exponentially
and can make preparation useless. A fitted quotient contraction alone does not
control the hidden power growth needed by (5).

## 4. Complete service and retained old records

Let E_dyn(T)=k^2 T D exp((k-1)JT) be the existing complete visible-path L1
bound against TRUE compressed service operators. The actual prepared density
g_m=(W*)^m g obeys ||g_m||<=R K. Comparing the two GENUINE service laws, one
from g_m and one from mu_*, through their signed compressed predictions gives

    L1 <= (R K+||g_*||_2) E_dyn(T)
                     + k d_m exp((k-1)JT).                 (6)

TV is half this bound, clipped at1. Numerical service, matrix and preparation
errors must be included through their previously proved operator/initial terms.
No positive reduced Markov realization is required for this triangle inequality;
its two endpoints are actual physical service laws.

For a retained old record Z, assume the actual JOINT density contract

    g_z=dP_(X|Z=z)/dpi,
    E_Z ||g_z||_2^2 <= K_joint^2.                            (7)

This is not implied by a bound on the unconditional starting density. Apply
(4)--(6) conditionally and integrate. Their same form holds with K_joint and

    H_joint=(E_Z ||P(g_z-g_*)||_2^2)^(1/2)
       <=sqrt(K_joint^2-1)+||g_*-1||_2.

The reference keeps the SAME marginal law of Z and permits the same policy
dependence on Z, but initializes service state from mu_*. The statement removes
only extra dependence carried by the physical source state. Reset outcomes,
realized random clocks, discarded reports or random seeds must not subsequently
be retained unless included in the joint instrument and its density analysis.
An averaged W cannot certify the conditional law given a retained clock seed.

No new microscopic reset is assumed. The guarantee is useful when the ACTUAL
source/preparation contract supplies (7), the acquired e is small compared with
1-kappa, and the retained complete-service error is acceptable. The old baseline
pi target differs from mu_* and must pay its separately acquired visible bias.

## 5. A bounded-density example shows an unavoidable nonzero floor

Take hidden H in{-1,+1} and visible Y in{-1,+1}. Choose 0<epsilon<1,
|beta|<1, and baseline full-support equilibrium

    pi(h,y)=(1+epsilon h y)/4.

The hidden H never changes. Baseline dynamics refreshes Y toward its conditional
mean epsilon H; for example its flip rate is (1-epsilon h y)/2. This is a
reversible bounded-rate physical chain. Its stationary law is not unique, and
no hidden mixing is claimed.

An actual biased operation uses visible weight w(y)=1+beta y. Its reversible
law mu_*=pi w has conditional visible mean

    m_h=(beta+epsilon h)/(1+beta epsilon h)=m0+m1 h,
    m0=beta(1-epsilon^2)/(1-beta^2 epsilon^2),
    m1=epsilon(1-beta^2)/(1-beta^2 epsilon^2).

Choose its flip rate (1-y m_h)/2. This is positive, <=1, and satisfies detailed
balance for mu_*. It is an ACTUAL operation with altered symmetric kinetics,
not an inference from the energy alone. For its independent exponential pulse
of rate alpha, set r=alpha/(alpha+1). The acquired kernel obeys

    W Y=rY+(1-r)(m0+m1 H).

For V=span{1,Y}, label closure is exact, and

    B Y=b+kappa Y,
    b=(1-r)m0,
    kappa=r+(1-r)m1 epsilon<1,
    e=(1-r)m1 sqrt(1-epsilon^2).

The affine limiting mean is b/(1-kappa)=beta, exactly mu_*(Y). Now take the
actual initial density g=1+aH relative to pi, with fixed |a|<1. It is uniformly
bounded, has K=sqrt(1+a^2), and requires no rare-state concentration. Since H
never changes,

    E_g[ Y after W^m ]
       =r^m a epsilon+(1-r^m)(m0+a m1).

Its limit differs from the predicted target beta by

    m1(a-beta epsilon).

For fixed nonzero a,beta and epsilon->0, this is of order e/(1-kappa), while
K stays bounded. The binary endpoint TV tends to half its absolute value.
Thus arbitrarily many calls do not eliminate a small but genuine leakage floor,
even with benign initial density. Hidden memory can remain weakly visible.

If an actual preparation record additionally reveals H, the unconditional
density can be exactly1 while the conditional densities are 2*1_{H=h}, with
K_joint=sqrt2. A guarantee using only the unconditional K would then miss the
retained-record dependence. This recording is a stated preparation interface,
not a claim that H can be read from passive visible data.

This example establishes necessity of retaining a leakage floor in the declared
source class, not a lower bound for every possible preparation operation. An
additional actual operation that changes H could improve preparation; it would
need its own acquisition and closure analysis.

## 6. A finite error target actually met by the synthetic construction

For the executable's epsilon=1/10, beta=1/2 and alpha=1, the exact quantities
are kappa=67/133 and e^2=99/70756. If the actual starting density contract is
K^2<=5/4, safe rational ceilings are K<=9/8, R<=7/4, e<=1/25 and
kappa<=51/100. Also ||g_*-1||=1/2 and H0<=1. Therefore the leakage floor in
(4) is at most9/56. After five actual independent-clock words, the immediate
visible binary output has TV from its biased equilibrium target at most

    (1/2)[9/56+(47/56)(51/100)^5] < 1/10.                  (8)

This is a useful finite tolerance despite a frozen hidden coordinate. It is a
mathematical synthetic certificate conditional on the stated density and source
contract, not an executed acquisition or a clock/metrology tolerance allowance.
If those errors are present, they must fit in the remaining error margin. The
subsequent complete-service guarantee remains (6), with its own horizon and
retained-record costs. The same example's persistent endpoint TV for a=1/2 is
9/532, showing why (8) must not be extrapolated to exact hidden reset.
