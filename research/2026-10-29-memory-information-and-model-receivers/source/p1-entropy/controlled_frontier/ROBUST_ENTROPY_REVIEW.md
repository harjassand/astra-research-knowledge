# Independent review: positive clock slack and one-tick entropy

29 October 2026, Brisbane. Scope: Sections 6--7 of root's
THERMODYNAMIC_PREDICTIVE_COMPLETION.md, including the new microscopic
path-measure use. The earlier exact boundary frontier is not re-audited.

**Conclusion:** the positive-slack inequality and its cut extension are
valid for the stated finite stationary CTMC, ordinary even-state reversal,
calibrated common weights, and a uniform hidden rate ceiling. The arguments
below independently establish the new bridge. They do not turn the bound
into a dissipation estimate for an unknown physical source, or make it
optimal away from the exact clock boundary.

## 1. Exact lower bound on one-tick excursion flux

Let mu be the unnormalized stationary microscopic excursion measure,
from a native departure at a port through zero or more hidden states to
the next port. Uniformize hidden evolution at rate Lambda only. Retain
the resulting virtual hidden self ticks as part of the augmented path.
Let N be its number of hidden ticks, with N=0 for a direct port jump.
The previously derived moment identities give

    integral N dmu = Lambda V,
    integral N(N-1) dmu = 2Lambda(Lambda c-V)=2Lambda delta.

Since N<=N(N-1) for each integer N>=2,

    h1=mu{N=1}
       =Lambda V-integral N 1{N>=2} dmu
       >=Lambda(V-2delta).

Nonnegativity of h1 gives h0=Lambda(V-2delta)_+ exactly as stated.
The positive-slack range h0>0 is c<3V/(2Lambda). No claim of a useful
positive bound outside that range follows from this argument.

## 2. Why the path-KL identity survives uniformization

For a microscopic excursion i,x1,...,xk,j with specified hidden holds,
its stationary intensity density is w_i times the first jump rate,
then each hidden survival factor and jump rate. Reversal begins with
w_j. The hidden survival factors cancel because each visited hidden
state has the same departure rate under stationary time reversal.
Stationary weights telescope, leaving the product of edge-flow ratios.
Integration counts each stationary native edge flux exactly once.
Thus D(mu||Rmu)=E, including the infinite case.

Uniformization adds hidden self jumps of rate Lambda-lambda_x. Their
forward/reverse likelihood ratio is one. Alternatively the conditional
Poisson decoration given the native hidden path is reversal covariant,
so it changes neither KL nor E. A common uniformization rate Lambda is
important for the stated one-tick formula.

This equality is for the FULL microscopic augmented excursion record,
used mathematically. A merely observed boundary waiting-time record has
in general only a data-processing lower bound; equality must not be
claimed for that observable record. No physical access to virtual ticks
is required to use this proof as a bound from an independently acquired
mean record and supplied clock ceiling.

## 3. Restriction to one-tick paths through one hidden state

Fix x, and write a_x=sum_i f_ix and b_x=sum_i f_xi, sums over ports.
The integrated flux of the augmented excursion i->x->j with exactly
one hidden tick is

    nu_x(i,j)=f_ix f_xj/(Lambda w_x).

It is NOT f_ix f_xj/(lambda_x w_x): the latter counts all native
single-hidden-state visits regardless of virtual ticks. With

    h_x=a_x b_x/(Lambda w_x),
    alpha_x(i)=f_ix/a_x, beta_x(i)=f_xi/b_x,

nu_x=h_x alpha_x tensor beta_x. Reversal transposes its two port labels.
The conditional hold density is the same exponential(Lambda) forward
and backward. Therefore the exact KL contribution is

    h_x[D(alpha_x||beta_x)+D(beta_x||alpha_x)]
      =h_x J(alpha_x,beta_x).

The subset indexed by N=1 and x is reversal invariant and hence has
equal forward/reverse mass. Its KL is nonnegative; so is the complement's.
Summing proves E>=sum_x h_x J. If a_x b_x=0 the subset has zero mass
and is omitted. If the endpoint supports fail to match, its entropy is
infinite, which is consistent with the bound.

## 4. Binary reduction and aggregation

For alpha=(p,1-p), beta=(q,1-q), let
r=pq+(1-p)(1-q), d=|p-q|. Then

    J=d log[(1-r+d)/(1-r-d)],
    d^2=1-2r+(p+q-1)^2.

When r<1/2, J increases with d at fixed r, so its minimum occurs at
p+q=1. This yields g(r)=4sqrt(1-2r)atanh(sqrt(1-2r)). For r>=1/2,
J>=0=g(r). The root's displayed derivatives are correct: g is convex
and nonincreasing, including the upward derivative jump from -8 to 0
at r=1/2.

The total one-tick self-return flux is sum_x h_x r_x. It is bounded
by total native self-return excursion flux, which is at most A. Thus

    E >= h1 g[(sum h_x r_x)/h1]
      >= h1 g(A/h1).

The perspective h g(A/h) is nondecreasing in h: where differentiable
its derivative is g(z)-z g'(z)>=0. This also holds through the threshold
and endpoint by continuity. With h1>=h0 the claimed result follows:

    E >= h0 g(A/h0),  h0>0.

If A=0 and h0>0, g(0)=infinity and no finite-entropy realization exists.
If h0=0, define this lower certificate as zero; do not evaluate 0*g(0/0).
The independent earlier argument that A=0,V>0 forces infinite entropy
can remain stronger outside the positive h0 range.

For a nontrivial port cut C,C^c, log-sum/data processing contracts each
Jeffreys divergence to the two endpoint groups. A same-group one-tick
excursion is either a self return or an excursion between distinct
ports in the same group. The first total is <=A; the second total is
bounded by the corresponding ordered off-diagonal trace flows F_ij,
which also include direct paths and longer hidden excursions. Therefore
B_C=A+sum_same_group,i!=j F_ij is a valid upper bound and

    E >= h0 g(B_C/h0).

The within-group sum is over ordered pairs, as the notation states.
No observed group equilibrium or isolated-module stationarity is needed.

## 5. Executable positive-slack controls

The checker builds four-state generators directly with port weights one
and hidden weights one. Hidden-to-boundary rate is kappa<1; around the
alternating cycle the clockwise flux is kappa(1-beta), reverse flux
kappa beta. A symmetric hidden-hidden edge of rate e is optional, with
kappa+e<=Lambda=1. A symmetric direct port edge is then chosen to make
each off-diagonal trace flow exactly one.

Exact elimination yields V=2 and c=2/kappa>V/Lambda. There are two
distinct slack mechanisms: e=0 gives virtual uniformization ticks;
e=1-kappa saturates the hidden native rate ceiling but yields actual
hidden-hidden ticks. The mean record remains fixed with respect to beta
within each kappa. Boundary flows remain balanced, and the direct
adjustment is nonnegative.

The full entropy is 4kappa(1-2beta)log[(1-beta)/beta]. The exact one-tick
mass is h1=2kappa^2, and its entropy is kappa times full E. The checker
constructs Q,L,G and the Schur record with rational arithmetic, verifies
all clock/budget identities, and compares the final entropy bounds with
rational outward bounds for logarithms and square roots. It also splits
one port into two to form genuine three-port cut checks, optionally
adding a symmetric within-group edge.

These are supplied mathematical controls with no acquired observations,
resets or physical device operation. The checker outputs its own exact
coefficients, interval certificates, case counts and source-call count.
It does not reuse the root's entropy implementation.

The saved run passes 120 supplied-generator controls: 40 binary cases
and 80 genuine three-port cut cases. All have c>V/Lambda. Sixty saturate
the hidden native rate ceiling and obtain slack through hidden-hidden
jumps; the other sixty use slower hidden clocks. There are 48 strictly
positive certified lower bounds and 30 explicit h0=0 controls. Logarithm
and square-root comparisons use exact rational outward intervals. The
run uses zero source observations or resets.
