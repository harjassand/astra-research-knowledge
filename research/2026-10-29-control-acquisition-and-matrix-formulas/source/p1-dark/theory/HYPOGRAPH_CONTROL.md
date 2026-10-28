# Acquired inner and outer hypographs for continuous compliance control

28 October 2026. Ordinary proof and scoped review of the proposed construction.
The root implementation was pending when this argument was written. This
document proves its mathematical interface; it does not certify code not yet
read or claim an independent whole-proof audit.

## 1. Acquired input and objective

Let the original physical domain be the dose simplex

    D={u in R^n: u>=0, sum_i u_i<=delta}.

The warranted fixed source has positive concave effective conductance J(u),
native response R(u)=r0+J(u), and compliance Z(u)=1/J(u). For the present
rank-one positive quadratic-form source,

    J(u)=c0+min_y [||y||^2+sum_i u_i(g_i+b_i^T y)^2],
    |g_i|<=G, ||b_i||^2<=kappa, c0>=cmin>0.

Concavity follows because an infimum of affine functions of u is concave.
All coordinates are nondecreasing, since increasing a dose increases every
quadratic energy before minimization. Thus a positive acquired baseline
lower bound cL<=J(0) is also a global lower bound. A warranted positive cmin
can be used if the observed baseline interval alone does not resolve it.

For degree k, the already acquired lattice is

    u_alpha=(delta/k)(alpha_1,...,alpha_n),
    alpha_i>=0 integer, sum_(i=0)^n alpha_i=k,
    M=binom(n+k,k).

Its convex hull is exactly D. The alpha_0 category represents unused dose.
At each node acquire simultaneous bounds

    0<cL<=ell_alpha<=J(u_alpha)<=h_alpha.

If necessary replace a raw lower bound by its maximum with the warranted
cL. These inequalities concern the exact nominal commands. The original
acquisition must already pay calibration, raw error, ADC and nominal-command
actuation allowances; finite successful interpolation does not prove the
source class or source stability. No independence of the errors is assumed.

For a later linear price vector c, consider

    V(u)=phi(J(u))-c.u,

where phi is increasing and concave on the positive conductance range. The
original compliance-reduction objective is phi(j)=-1/j: adding the unknown
constant Z(0) leaves every optimality gap unchanged. This construction
therefore preserves the earlier physical objective at nonzero prices.

## 2. Inner hypograph from acquired lower node values

For any u in D define

    L(u)=max {sum_alpha lambda_alpha ell_alpha:
              lambda>=0, sum lambda=1,
              sum_alpha lambda_alpha u_alpha=u}.           (1)

The feasible set is a nonempty compact polytope, so the maximum exists.
L is concave: mixing feasible maximizing combinations for two commands
gives a feasible combination at their convex mixture. For every feasible
lambda, source concavity gives

    J(u)>=sum_alpha lambda_alpha J(u_alpha)
        >=sum_alpha lambda_alpha ell_alpha.

Consequently L(u)<=J(u). The convex hull of the lower node points, with
vertical downward rays added, is an inner approximation to the true
hypograph. This is a lower model even though (1) takes a MAXIMUM over node
mixtures. Calling it an ordinary interpolation simplex would conceal this
important freedom to choose a representation of u.

No hidden g, B, rank, individual coupling or source gradient is used.

## 3. Two valid outer hypographs

### 3.1 Acquired interpolant coefficients

Suppose the acquired degree-k interpolant p has the uniform proved error

    |J(u)-p(u)|<=E,
    p(u)=sum_alpha B_alpha(u)b_alpha.

Here B_alpha are degree-k simplex Bernstein weights. They are nonnegative,
sum to one, and reproduce the physical command:

    sum_alpha B_alpha(u)u_alpha=u.                         (2)

The coefficients b_alpha are obtained from the acquired nodal reports;
they are not hidden source Taylor coefficients. If interpolation was
performed on R, subtract r0 from every coefficient to obtain J coefficients.
The error E includes both model-comparator bias and acquired node error.

Set a_alpha=b_alpha+E. Then

    J(u)<=sum_alpha B_alpha(u)a_alpha.

The concave envelope of these upper control points,

    U_I(u)=max {sum_alpha lambda_alpha a_alpha:
                lambda>=0, sum lambda=1, sum lambda u_alpha=u},       (3)

satisfies J(u)<=U_I(u), because the particular weights B_alpha(u) are
feasible. If any a_alpha<cL, replacing it by max(a_alpha,cL) only raises
(3) and preserves the upper bound while making phi's domain positive.

This positivity repair is an UPWARD change. Arbitrarily clipping an upper
coefficient downward, even using a global physical maximum, need not
preserve the coefficientwise Bernstein construction.

### 3.2 Positive Bernstein approximation

The proved source-specific bias is

    0<=J(u)-sum_alpha B_alpha(u)J(u_alpha)<=C,
    C=delta^2*kappa*G^2/k.                                (4)

Thus upper points a_alpha=h_alpha+C give a second outer envelope U_B by
the same definition (3). Every upper point is already positive. This
construction needs no interpolation coefficient transform and works for
all finite q=delta*kappa, including singular B and exactly dark controls.

The upper concave envelope of mere node upper bounds h_alpha, WITHOUT
the proved bias C or another whole-domain argument, is not generally an
upper bound on a concave source between nodes. The Bernstein identity and
its bias proof are essential.

Both U_I and U_B enclose J. One may take the smaller of their separately
certified global objective upper bounds. Taking coordinatewise minima of
their two lists of upper coefficients is NOT justified: two upper weighted
sums do not in general imply that the weighted sum of pointwise minima is
an upper bound. Their pointwise function minimum is a valid outer envelope,
but optimizing the intersection requires its own calculation.

## 4. Every later task reduces to a planar lower cost hull

For any of the envelope point lists a_alpha, let

    C_alpha=c.u_alpha,
    P_a=conv{(a_alpha,C_alpha): alpha in the lattice}.

Because phi is increasing,

    max_(u in D) [phi(U_a(u))-c.u]
      = max_(lambda in probability simplex)
          [phi(sum lambda a_alpha)-sum lambda C_alpha]
      = max_((j,t) in P_a) [phi(j)-t].                    (5)

The first equality follows in both directions: any lambda gives a command
u and a height at most U_a(u), while a maximizing lambda in the definition
of U_a realizes that height. The same statement with a=ell gives exactly
the optimum of the inner model phi(L(u))-c.u.

At a fixed j the objective strictly decreases with cost t. Therefore only
the lower boundary of P_a matters. It is the graph of a convex piecewise
affine function of j between the smallest and largest conductance values.
Every point on this lower chain belongs to either a vertex or one segment
between two retained node points. An optimum of (5) therefore has a
representation using AT MOST TWO original lattice nodes. This is a planar
boundary fact, stronger here than the generic three-point planar
Caratheodory bound. Vertical duplicate-j points can be reduced to the one
with least cost; dominated duplicates are never useful for (5).

The chosen command is the deterministic simultaneous mixture

    u=(1-theta)u_alpha+theta*u_beta,  0<=theta<=1.       (6)

It is not randomized execution or alternation between two source experiments.
It is feasible because D is convex. Since each acquisition node activates
at most k controls, (6) activates at most min(n,2k) controls before finite
preparation. The true physical optimum need not have this support bound;
the statement concerns the acquired inner/outer envelope optimizers.

Only the price projection changes between tasks. An exact rational lower
chain can be built by sorting j, removing duplicate-j higher costs, and
using rational cross-product orientation tests to retain increasing slopes.
No n-dimensional hypograph hull need be explicitly constructed. The
conceptual high-dimensional hypographs establish the proof; their price
projections provide the algorithm.

## 5. Compliance utility: exact segment solution and outward radicals

On a lower-chain segment with positive j in[jA,jB], jA<jB, write cost as

    t=s*j+b.

For phi(j)=-1/j the segment objective is

    f(j)=-1/j-s*j-b,
    f'(j)=1/j^2-s,  f''(j)=-2/j^3<0.

If s<=0, the optimum is the right endpoint. If s>0, the only interior
stationary point is j*=1/sqrt(s). Its membership can be tested without
floating-point arithmetic:

    s*jA^2<=1<=s*jB^2.

Otherwise choose the endpoint indicated by the derivative sign. If the
stationary point is inside, its exact optimal value is

    f(j*)=-2*sqrt(s)-b.                               (7)

For an outward rational root enclosure rL<=sqrt(s)<=rU, equation (7) lies
in[-2*rU-b,-2*rL-b]. Thus the UPPER certificate uses the LOWER square-root
endpoint. Endpoints use ordinary exact rational evaluation. Taking the
largest upper endpoint over all segments/vertices certifies the global
envelope maximum. A one-point hull or all-equal-j case is handled directly.

For an implementable candidate, enclose sqrt(1/s) outward, choose any
rational j inside the segment close to that enclosure, and form
theta=(j-jA)/(jB-jA). There is no need to pretend the irrational optimum
can be commanded exactly. The final candidate is certified on its actual
finite prepared coordinates. Candidate root precision affects the achieved
gap, but cannot invalidate a correctly computed upper/lower gap.

The same geometric reduction holds for any increasing concave phi. Its
one-dimensional segment optimizer may require a different certified scalar
procedure; closed form (7) is specific to compliance utility.

## 6. Finite preparation and the actual candidate lower bound

Suppose the chosen mixture has acquired lower height

    j_mix=(1-theta)ell_alpha+theta*ell_beta<=J(u).

Prepare an actual finite command uhat in D, for example by rounding every
nonnegative coordinate inward to the hardware grid. Let

    e_u=||uhat-u||_1.

A warranted global coordinate Lipschitz bound L_J gives

    J(uhat)>=max(cL,j_mix-L_J*e_u)=:j_candidate>0.     (8)

For this source one sufficient bound is

    L_J=G^2*(1+sqrt(delta*kappa)/2)^2.                (9)

Indeed the energy minimizer is y*=-(I+XX^T)^-1 X sqrt(U)g with
X=[sqrt(u_i)b_i]. The singular-value inequality
sigma/(1+sigma^2)<=1/2 gives ||y*||<=G*sqrt(delta)/2. Hence
partial_i J=(g_i+b_i^T y*)^2<=L_J. The looser existing physical-oracle
bound G^2*(1+sqrt(delta*kappa))^2 is also sufficient. Use outward square
roots, not uncertified floating estimates, when evaluating either bound.

The actual candidate objective lower bound is

    LB=phi(j_candidate)-c.uhat.                       (10)

Recompute the linear cost at the actual command. A price vector need not
have a sign that makes inward rounding beneficial. Do not substitute the
ideal mixture's cost or utility. A tighter compiled prediction or another
valid acquired lower bound at uhat may replace (8).

Let UB_I and UB_B be the separately certified outer-envelope maxima. Then

    sup_(u in D)[V(u)-V(uhat)]
       <=max(0,min(UB_I,UB_B)-LB).                   (11)

For the original objective Z(0)-Z(u)-c.u, the same inequality holds because
Z(0) cancels. No new source reaction is required to compute (11). Any later
physical verification or deployment is a separate paid and authorized
action; none is executed by this proof.

## 7. A uniform a priori gap survives the hull reduction

Let w=max_alpha(h_alpha-ell_alpha). The positive-Bernstein upper point
heights differ from the lower point heights by at most d=w+C. For every u,

    L(u)<=J(u)<=U_B(u)<=L(u)+d.                      (12)

The last inequality follows by applying a_alpha<=ell_alpha+d to EVERY
feasible lambda before taking the maximum. If phi has Lipschitz constant
K_phi on [cL,infinity), then

    max_u[phi(U_B(u))-c.u]-max_u[phi(L(u))-c.u]
       <=K_phi*d.                                   (13)

For phi(j)=-1/j, take K_phi=1/cL^2. An exact inner-model maximizing mixture
therefore has true global regret at most (w+C)/cL^2. Finite candidate/root
selection and preparation add their explicitly computed losses. A simple
preparation allowance is K_phi*L_J*e_u+|c.(uhat-u)|. The actual reported
certificate (11) is preferable because it accounts for the chosen finite
command directly and may be tighter.

This proves that converting to hypographs does not throw away the positive
approximation's dimension-independent error bound. It does not make the
binomial physical acquisition cost small: k may need to be large for a
small target tolerance, and M=binom(n+k,k) remains explicit.

## 8. Costs, conventional comparator, and scope

The initial record costs M native reactions plus its calibration readings,
all attempted/failed settings, preparation, settling, integration and reset.
The acquired table is reusable for every later price vector and the declared
class of increasing concave utilities within the same source/stability epoch.

For one price vector, node cost projection takes O(M*min(n,k)) arithmetic
if node supports are stored sparsely. A planar hull takes O(M log M)
comparison/arithmetic operations and O(M) working storage; because all
conductance coordinates are task-independent, their order can alternatively
be precomputed once. The segment scan is O(M), plus rational bit and outward
root costs. Dense storage of all node vectors costs O(Mn); sparse or implicit
node encoding is an implementation choice and must not be claimed before
it is actually used. Bernstein coefficient transformation is an additional
one-time cost for U_I; U_B does not need it. The final two-node mixture needs
at most min(n,2k) nonzero coordinate settings, with its finite DAC allowance
and use/reset costs retained.

Convex/concave envelopes, lifted-point convex hulls, and planar lower hull
optimization are conventional convex-analysis tools. Boyd and Vandenberghe,
*Convex Optimization*, exercise 3.30, formulates convex envelopes through the
convex hull of the epigraph; changing sign gives the concave formulation.
Primary author-hosted source:
https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf .

Existing implementations include SciPy's Qhull-backed `ConvexHull`:
https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.ConvexHull.html .
Its documented input/output uses floating-point coordinates and notes
degeneracy/precision issues. The proposed certificate therefore uses exact
rational planar comparisons and outward root enclosures rather than treating
an unverified floating hull as exact. Qhull's own precision discussion is
https://www.qhull.org/html/qh-impre.htm .

An equally informed conventional concave-envelope/robust-control solver
can use the identical acquired node intervals, source-specific whole-law
bias, hull reduction and finite-preparation checks, and tie this cost.
The consequential closure is from a charged, noisy, dark-tolerant value
record to continuous original compliance control without identifying each
coupling, acquiring full rank, or relying on nonconvex polynomial optimizer
convergence. It is not a new convex-hull algorithm, a universal performance
advantage, a photon/statistical lower bound, or evidence of an operated
device.
