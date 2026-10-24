# A recurrent-controller event kernel obtained from occupation moments

New Pro3 construction. This is a proved obtaining algorithm with a newly
implemented binary specialization documented in Section 10. It removes the
single-opening requirement and allows the silent local generator to change
with a hidden recurrent controller. The tractable condition is commutation
of the two local killed generators. No global reaction or configuration
expansion is required by the acquisition algorithm.

The output is an unnormalized event-time-density operator with a relative
certificate valid for every supplied initial joint law, including correlated
positive mixtures and nonnegative tensor trains. Ordinary programmes and
existing inference methods may acquire and retain the same operator.

## 1. Source conditions and the scientific operation

Let C_t be an autonomous two-state continuous-time Markov chain with generator

    C=[[-lambda,lambda],[mu,-mu]],       lambda,mu>0.

Its switches leave the local physical states unchanged. Module i has a finite
state space, silent generator Q_i(c), and diagonal nonnegative recorded-event
killing D_i(c) in controller state c. Conditional on a controller path, the
modules evolve independently until the first recorded event. Set

    A_i(c)=Q_i(c)-D_i(c).

The total pre-event killing is additive. The selected final mark/reset
operator J is supplied as a finite positive sum of local tensor factors,
including a factor on the controller when necessary. Its row sums must be
consistent with the event intensities included in the killing. J can retain
or reset the controller and can have finitely many reset branches.

The essential algebraic condition is

    A_i(0) A_i(1)=A_i(1) A_i(0)          for every i.       (1)

For rational local source matrices, (1) is decided by exact local matrix
multiplication. No commutation between generators of different modules is
an additional requirement: their lifted actions already commute.
The finite controller/component decomposition and additive killing must be
supplied or obtained by checked structural analysis of the compact rule
source. Enumerating finite local states is allowed; a compact decomposition
for an arbitrary rule program is not assumed to exist or to be free to find.

Fix an observation lag t>0. The pre-event survival operator P_t retains the
controller endpoint and every local state. The desired marked density is

    K_t=P_t J.

For normalized input nu, the density of the selected first mark at t is
nu K_t 1 and its conditional output law is nu K_t/(nu K_t 1). Rows are not
normalized separately. No initial distribution, stationarity assumption or
strictly positive initial marginal is used in obtaining K_t.

## 2. Exact occupation reduction

Let S_t be the time the controller spends in state 1 during [0,t], and let

    mu_cd(ds)=Pr_c(S_t in ds, C_t=d),       c,d in {0,1}.

These are unnormalized positive measures of mass (exp(tC))_cd. Conditional
on a controller trajectory, (1) makes the ordered local product equal to

    H_i(s)=exp((t-s)A_i(0)+s A_i(1)).                    (2)

It depends on the occupation s, not the number or ordering of switches.
Consequently each controller block of the exact survival operator is

    (P_t)_cd=integral_[0,t] tensor_i H_i(s) mu_cd(ds).    (3)

This identity includes arbitrarily many controller switches. It is not a
finite-switch truncation. The controller occupation is marginalized in the
output; the controller endpoint is retained.

Examples satisfying (1) include A_i(c)=a_i(c) A_i with nonnegative clock
speeds a_i(c). Here both local silent kinetics and recorded turnover rates
are scaled by the controller. One phase may have zero local rates. More
general commuting killed generators are allowed. Common-clock reduction
and occupation-time methods are established primitives; their relative
operator acquisition below is the construction being developed.

## 3. Reachable support and a strictly positive local lower certificate

Neither phase needs to have strictly positive rates or an irreducible local
generator. Form the union of the positive off-diagonal graphs of Q_i(0)
and Q_i(1). Let R_i be its reachability relation, including diagonal pairs.
For every 0<s<t, the matrix in (2) has positive off-diagonal graph equal to
this union, so H_i(s)(x,y)>0 exactly for (x,y) in R_i. Outside R_i all
integrands and all acquired factors are exactly zero.

For s/t in [1/3,2/3], use the local reference generator

    Qbar_i=(Q_i(0)+Q_i(1))/3.

Choose the rational number

    v_i=max over x and p in {1/3,2/3} of
         [(1-p)(qout_i(0,x)+d_i(0,x))
          +p(qout_i(1,x)+d_i(1,x))-qbarout_i(x)].

It is nonnegative, and entrywise

    (1-p)A_i(0)+p A_i(1) >= Qbar_i-v_i I

throughout that interval. Positivity of matrix exponentials gives

    H_i(s) >= exp(-v_i t) exp(t Qbar_i).

Thus obtain any rational lower bound

    0<m_i<=min_(x,y in R_i)
                    exp(-v_i t) exp(t Qbar_i)(x,y).      (4)

This is a local computation. A positive graph path of length at most
|E_i|-1 gives one strictly positive uniformization-series term for each
reachable pair. Increasing precision and the positive-series cutoff
therefore eventually certify (4). Exact graph analysis identifies zeros.

Write m=product_i m_i. Although m can be exponentially small in the number
of modules, its representation and log(1/m)=sum_i log(1/m_i) are obtained
from local data. No exponentially large matrix is used to find it.

## 4. A controller occupation lower bound, including rare endpoint bridges

Every mu_cd has a continuous positive component on (0,t). Explicit paths
give a lower bound on its mass in the central interval [t/3,2t/3]. Put
nu=max(lambda,mu). Valid unnormalized lower bounds are

    g_01=lambda (t/3) exp(-nu t),
    g_10=mu     (t/3) exp(-nu t),
    g_00=g_11=lambda mu (t^2/144) exp(-nu t).             (5)

For unequal endpoints, restrict the one switch time to [t/3,2t/3]. For
equal endpoints, restrict the two switch times to [t/6,t/4] and
[3t/4,5t/6]. Both possible starting phases then spend between t/3 and 2t/3
in state 1. The path density is at least the product of the required rates
times exp(-nu t), and the indicated integration boxes give (5).

Let p_cd=(exp(tC))_cd. Obtain a common positive lower bound

    eta<=min_cd g_cd/p_cd.                              (6)

The simpler eta<=min_cd g_cd is valid because p_cd<=1. Certified lower
bounds on g_cd and upper bounds on p_cd give an obtainable rational eta.
If useful, a better occupation-probability calculation may improve (6);
the proof only needs one strictly positive valid bound.

For every supported local configuration pair x,y, (3)-(6) imply

    (P_t)_cd(x,y) >= p_cd eta m.                         (7)

The denominator is source-obtained. It is not the likelihood of a chosen
entrance or a particular future record. Define sigma=eta m>0.

## 5. Positive Gauss quadrature and an explicit all-input width bound

For each of the four measures mu_cd, take its q-node Gaussian quadrature:

    G_cd=sum_(ell=1)^q omega_(cd,ell)
                         tensor_i H_i(s_(cd,ell)).       (8)

All weights are positive and all nodes lie strictly between 0 and t. The
continuous component of mu_cd ensures its moment matrices are positive
definite and its orthogonal-polynomial roots are distinct. Endpoint atoms
from controller paths with no switch are included in these measures; they
are not dropped.

Set

    D=sum_i ||A_i(1)-A_i(0)||_infinity.

For a supported scalar entry f(s) of tensor_i H_i(s),

    |f^(r)(s)|<=D^r,             r>=0.                 (9)

To see this, the lifted generators commute by (1), and the derivative is
the substochastic product exponential multiplied by the rth power of the
lifted generator difference. Its infinity norm is at most D^r. Equivalently
the local product rule gives the same bound without forming a lifted matrix.

Let p_q be the monic degree-q orthogonal polynomial for mu_cd. The Gaussian
remainder theorem, valid also when the positive measure has endpoint atoms,
gives

    |integral f dmu_cd - G_cd(f)|
      <= [sup|f^(2q)|/(2q)!] integral p_q(s)^2 mu_cd(ds).

For completeness, interpolate f and its first derivative at the q Gaussian
nodes. Its degree-(2q-1) Hermite polynomial is integrated exactly; the pointwise
Hermite remainder has magnitude at most sup|f^(2q)| p_q(s)^2/(2q)!. Integrate
this bound. No density or smoothness of mu_cd is required.

The monic orthogonal polynomial minimizes its squared L2 norm among monic
degree-q polynomials. A scaled Chebyshev polynomial on [0,t] is monic with
supremum norm t^q/2^(2q-1). Therefore

    integral p_q^2 dmu_cd <= p_cd t^(2q)/2^(4q-2).

Combining this estimate with (7) and (9) proves, entrywise for every block,

    |P_t-G|<=delta_q P_t,
    delta_q=(4/sigma) (tD/4)^(2q)/(2q)!.                (10)

Structural zeros remain exactly zero. The factor p_cd cancels; no selected
input law appears in the relative certificate.

For any desired 0<delta_*<1, a sufficient integer q is

    q>=max(1, e tD/4, log(4/(sigma delta_*))/log 4),     (11)

rounding upward. Indeed (2q)!>=(2q/e)^(2q), and the second condition makes
the remaining power at most 4^(-q). One may replace e by the rational upper
bound 3 and use outward logarithm bounds for an explicit integer choice.
Searching (10) directly generally gives a sharper q. If D=0, the integrand
is constant and one node is exact, without the conservative choice (11).

The pre-event operator has at most 4q positive product terms, including the
controller matrix unit E_cd in each term. If the mark/reset has B positive
product branches, the event kernel has at most 4qB terms. Its local-factor
storage is O(qB sum_i |E_i|^2), plus the small controller factors and scalar
coefficients.

For fixed controller parameters, horizon, bounded local dimensions and
uniformly bounded local norms/lower-certificate costs, (11) gives

    q=O(n+log(1/delta_*)).

This is an explicit width bound, not merely a small arithmetic circuit that
may hide exponentially many positive summands. The local lower constants,
controller transition scales, horizon, coefficient bit lengths and moment
conditioning remain part of the obtaining cost. The statement is not a
uniform bit-complexity claim for arbitrarily stiff or nearly singular inputs.

## 6. Obtaining the Gaussian rules from a finite positive matrix calculation

The controller occupation moments are source quantities. With E=diag(0,1),

    E_c[exp(z S_t) 1_(C_t=d)]=(exp(t(C+zE)))_cd.        (12)

To obtain moments through degree r, form the block upper-bidiagonal matrix
B_S with r+1 copies of C on its diagonal and E on its first superdiagonal.
The (0,j) block of exp(t B_S) is the coefficient of z^j in (12), namely
E_c[S_t^j 1_(C_t=d)]/j!. Here the exponential is at time t. B_S-I is
substochastic, so exp(t B_S)=exp(t) exp(t(B_S-I)) can be evaluated by
positive uniformization and a known scalar factor.

For normalized occupation u=S_t/t, instead form B_u with diagonal blocks
tC and superdiagonal blocks E. The (0,j) block of exp(B_u) is
E_c[u^j 1_(C_t=d)]/j!. Here the exponential is at time ONE. Again B_u-I is
substochastic, and exp(B_u)=exp(1) exp(B_u-I). The two conventions must not
be mixed: normalized moments remove the powers of t, but the controller
diagonal blocks already contain t. Both constructions have nonnegative
off-diagonal entries and support certified positive uniformization.

A q-node rule needs moments through degree 2q-1, supplied by a matrix of
dimension 4q. For each c,d, solve the positive-definite moment system for
the monic orthogonal polynomial, isolate its q simple roots in (0,t), and
obtain the positive Gaussian weights. For example the weight at a root s is

    1 / (v(s)^T H^(-1) v(s)),

where v(s)=(1,s,...,s^(q-1))^T and H is the degree-(q-1) Hankel moment matrix.
Moment refinement, certified linear algebra and root isolation terminate
because the exact moment matrices are positive definite, the roots are
simple and the weights are positive. Their conditioning affects precision
and runtime; it is not assumed harmless.

This gives a finite obtaining procedure based on the small controller and
local matrix exponentials. It does not enumerate controller paths, switch
counts, global species or global configurations. The available binary
executor implements this procedure with certified moment intervals,
inverse-residual bounds for the orthogonal-polynomial coefficients, and
root intervals certified by sign changes. It uses the equivalent Gaussian
weight formula h_(q-1)/(p'_q(s) p_(q-1)(s)), where h_(q-1) is the squared
norm of the monic previous polynomial. General finite local blocks and
arbitrary finite reset-branch expansions remain broader mathematical scope
than this numerical specialization; Section 10 records what was executed.

## 7. Numerical evaluation, normalization and future conditioning

Suppose interval evaluation of the positive weights, nodes and local
exponentials produces a rational positive product operator L with

    L<=G<=C_num L,            C_num>=1.

On union-reachable local pairs the nodes lie in (0,t), so sufficiently fine
local enclosures eventually have positive lower endpoints. Unreachable
pairs are represented as exact zeros. The common coefficient multiplier
C_num is obtained by multiplying local upper/lower ratios within each
term and maximizing over terms. This handles node uncertainty as well as
local exponential and scalar-weight evaluation.

If delta_q<1, (10) gives

    a L<=P_t<=b L,
    a=1/(1+delta_q), b=C_num/(1-delta_q).                (13)

The same inequality holds after multiplication by the positive mark/reset J.
For every nonnegative joint input nu with nonzero output mass, the conditional
output-TV distance is at most

    (sqrt(b/a)-1)/(sqrt(b/a)+1).

For exact quadrature evaluation, setting delta_*=2 epsilon/(1+epsilon^2)
in (11) is sufficient for posterior TV at most epsilon. Numerical spread
uses an additional part of the error budget. Finite relative input error
multiplies the operator spread, and every repeated approximate application
incurs the operator's spread again. Exact later positive operations preserve
the already acquired spread regardless of record rarity.

This certificate covers the controller endpoint and all retained physical
local variables. Historical count labels can be included through identity
factors, as in the existing count-interface construction. A positive product
operator transforms only local physical indices of a nonnegative tensor
train, preserving its bonds per term. With the explicit 4qB-term bound,
applications and product-guard contractions on a supplied finite positive
mixture or tensor train have costs polynomial in q, the supplied ranks and
the local dimensions. Repeated applications may multiply mixture widths;
no indefinitely bounded representation has been proved.

Because the output retains the physical controller endpoint, it is a valid
entrance for the next recurrent-controller interval under the same source.
An external controller reset is not needed for this model. If the actual
protocol specifies a reset, that supplied positive operation is applied
explicitly. A stored numerical kernel is reusable at its admitted lag and
source parameters; different lags or parameters may require new acquisition.

The hidden occupation S_t has been integrated out. Quadrature labels are
representation indices, not a claimed joint-TV approximation to the physical
continuous occupation history. Queries about that unretained history need
an additional construction. The observed lag t is fixed, and absolute-time
protocols must retain whatever clock state they actually require.

## 8. Why commutation is substantive

Occupation time alone is insufficient for general changed local dynamics.
For a single binary module, take

    Q_0=[[-1,1],[0,0]],    Q_1=[[0,0],[1,-1]],

with no killing. Start the leaf in state 0 and let a controller trajectory
spend times a,b,c in phases 0,1,0. Its final active probability is

    1-exp(-c)+exp(-(b+c))-exp(-(a+b+c)).

Holding a+c and b fixed changes this probability when a changes. For example
two positive choices a=(a+c)/4 and a=3(a+c)/4 have equal occupation times,
equal starting and ending controller states, and different leaf laws.
Both path patterns have positive neighborhoods under a recurrent controller.
Thus the occupation reduction cannot simply be asserted for noncommuting
local generators. That broader source requires additional temporal
information; a separate positive splitting construction has a weaker
execution guarantee.

## 9. Relation to incumbents and status

Occupation distributions and Markov rewards are established computational
objects. Bruno Sericola, *Occupation Times in Markov Processes* (2000),
derives occupation distributions, joint occupation information and weighted
occupation rewards through uniformization and order statistics:
https://scispace.com/pdf/occupation-times-in-markov-processes-2gksbddev4.pdf
Bladt, Meini, Neuts and Sericola, *Distributions of Reward Functions on
Continuous-Time Markov Chains*, develop further reward-distribution
algorithms using uniformization, transform inversion and matrix convolution:
https://people.dm.unipi.it/meini/papers/BMNS-MAM4.html

Thomas Lux (2024), *Estimation of regime-switching diffusions via Fourier
transforms*, equation (15), Sections 2-3 and Appendix A, gives endpoint-
resolved positive occupation integrals including the no-switch atoms and
uses the transition laws in sequential hidden-state likelihoods:
https://link.springer.com/article/10.1007/s11222-024-10397-6
Thus occupation reduction, endpoint retention and sequential reuse are
direct antecedents. The proposed distinction is the source-checked local
support/relative-envelope calculation and explicit positive-product width.

Positive quadrature, Gaussian rules from moments, time changes and tensor
products are not claimed as new primitives. TTOP already treats structured
full propagators, and established componentwise matrix-exponential algorithms
already give relative entrywise certificates for explicit finite matrices.
Shao, Gao and Xue's positive Taylor/squaring and interval treatment is a
particularly relevant example:
https://webapps.cs.umu.se/uminf/reports/2012/004/part1.pdf

The candidate contribution is the compact-source width and relative
acquisition certificate: use the established occupation representation to
obtain an all-input reaction-event operator, bound its positive-product
width from local source data, and certify its application to correlated
entrances and later conditioning. The derivation above establishes its
mathematics and obtaining conditions, not historical priority or superiority
over every existing implementation. Incumbents receive the same compact
source, observations, tensor representations and retention rights.

## 10. Available implementation, retained operator and executed checks

`recurrent_occupation_kernel.py` is new scientific implementation. It uses
the available `source_interface_compiler.py` as a genuine dependency and
otherwise standard-library numerical/arithmetic facilities. It does not
claim to recover missing historical helpers.

The source pass checks a two-state autonomous bidirectional controller,
local additive recorded killing and the exact commutators of the killed
generators. Its local numerical exponentials currently support binary
modules. Multiple rules may share the observed mark when they have the
same owner and reset branch; their exact local hazards are summed. General
finite local blocks and arbitrary positive reset-branch families are not
claimed to have been implemented by this specialization.

The executed 24-module source has 146 rules, controller rates 7/10 and
11/10, and phase clock speeds 1/4 and 1. Both silent and marked local rates
are scaled by those clocks. The selected mark is reaction_0 at lag 1/2.
The physical state space has 33,554,432 configurations, including the
controller. The acquired operator in
`recurrent_occupation_kernel_24sites.json` has 34 Gaussian nodes per
controller endpoint pair and 136 positive product terms. Its all-input
and common-future-selection posterior-TV bound is less than 7.020921e-10.
The source proof permits a zero phase clock; that case is not claimed as
an additional executed 24-module calculation here.

The saved operator contains exact rational coefficients and local matrices,
controller input/output indices, exact multiplier/spread data and numerical
obtaining witnesses. It is an unnormalized event-density operator. The
source initial branch is not used to choose its all-input quadrature bound.
Runtime application accepts normalized positive mixtures with arbitrary
controller/leaf correlations represented by their component labels.

For the main acquisition, positive block-banded uniformization used 197
terms at 270 decimal digits. The finite moment block has dimension 136;
only two initial controller rows and its block bandwidth are propagated.
The reported maximum moment-tail bound is less than 6.63e-237. Numerical
inverse and root guesses are verified by interval residual and sign tests;
their apparent floating-point accuracy is not treated as a certificate.
Stored positive local factors are rational lower values with bounded
decimal length, and their evaluation spread is explicitly included.

`recurrent_occupation_kernel_results.json` also records an independent
two-leaf, eight-state expanded reference. It checks all input and output
controller states, 32 positive operator entries and 32 structural zeros
against evaluated outward operator bounds. Its positive-uniformization
tail is less than 2.148e-206. A deliberately altered source changes only
one phase's recorded killing and is rejected for noncommuting killed
generators even though the silent generators still commute.

The same small acquired kernel was actually applied twice to a correlated
two-component entrance, without an external controller reset. Exact
positive mixture width grows from 2 to 28 to 392; it is not held fixed by
an unproved compression. The two-event joint density is approximately
0.02999465250591614 and the final controller-one probability approximately
0.8738008187678451. The composed posterior-TV bound is less than
3.315910e-10, and an independent full reference contains the reported
likelihood/posterior quantities. These are executed application checks
reported in the results file; no separate serialized two-event posterior
is asserted here beyond the available applying code and retained kernel.

A targeted review checked the normalized occupation-moment convention,
uniformization tail factors, inverse-residual polynomial enclosure,
root/weight certification, local support and reset order, and exact
likelihood normalization during reuse. The review did not independently
rerun acquisition or the expanded calculations. The general theorem,
executed binary specialization, actual retained operator and numerical
comparison evidence are distinct claims.
