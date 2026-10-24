# Relative entrance acquisition without equilibrium initialization

New mathematical and computational work in this Pro3 continuation. This file
removes the stationary and strictly positive initial-marginal assumptions
from the one-opening entrance construction when opening leaves the silent
generator unchanged. It preserves the substantive source, reset and support
conditions. The binary implementation and its numerical output are new files;
the earlier stationary executor and its results are preserved.

## 1. Local source and the correct temporal ordering

Let Q be a finite generator and D=diag(d) a nonnegative diagonal matrix of
recorded-event killing rates. Write

    A=Q-D,
    d_min=min_x d(x), d_max=max_x d(x).

Fix a horizon t>0 and any probability row mu, including a point mass. A
controller opens at time t-u, after which the local recorded-event hazards
are enabled. The silent generator is exactly Q before and after opening.
The unnormalized local row at time t, with no recorded event after opening,
is

    v(u)=mu exp(Q(t-u)) exp(Au),       0<=u<=t.            (1)

The order in (1) matters. One must evolve the possibly nonstationary initial
law for the pre-opening interval before applying killed open-phase dynamics.
Replacing (1) by mu exp(Au) is valid only with an additional invariant-law
argument, such as mu Q=0.

### Theorem 1: monotonicity and fixed reachable support

For every probability row mu,

    v'(u)=-mu exp(Q(t-u)) D exp(Au),
    -d_max v(u) <= v'(u) <= -d_min v(u),                 (2)

componentwise. In particular v is componentwise nonincreasing in the
activated duration u. Let q=mu exp(Qt). Then

    exp(-d_max u) q <= v(u) <= exp(-d_min u) q.           (3)

Consequently v(u) has the same support as q for every u in [0,t]. Neither
stationarity nor positive mass at every initial local state is required.

**Proof of (2).** Differentiate (1). Q commutes with its own exponential,
and A commutes with its own exponential, yielding

    v'(u)=mu exp(Q(t-u))(-Q+A) exp(Au).

Since -Q+A=-D, this proves the identity. The row mu exp(Q(t-u)) and the
matrix exp(Au) are nonnegative. Multiplying
d_min I<=D<=d_max I by them gives the inequalities. QED.

**Proof of (3).** Starting from v(0)=q, integrate the scalar differential
inequalities (2) coordinatewise. Equivalently, compare the positive killed
semigroup with exp(-d_max u)exp(Qu) and exp(-d_min u)exp(Qu), and multiply
on the left by mu exp(Q(t-u)). The lower and upper factors are strictly
positive for finite u, so support agrees. QED.

There is also a direct path interpretation. Use the same silent Q path
throughout [0,t]. Increasing u exposes a longer terminal part of that path
to killing. The extra survival factor is between the corresponding
exponentials of d_max and d_min. Conditioning on an endpoint and summing
paths preserves these inequalities.

This result supersedes any earlier blanket statement in the retained packet
that nonstationary initialization destroys componentwise monotonicity. That
warning is too broad for the same-Q construction (1). If opening changes the
silent generator, the derivative instead contains the difference of the two
silent generators and (2) does not follow. No general changed-Q extension is
claimed here.

## 2. Reachable support is locally obtainable

Assume Q, mu and t are rational inputs, t>0. Let S be the states reachable
from the positive support of mu using positive off-diagonal Q edges,
including the starting states themselves. Graph reachability obtains S
without enumerating another module's states.

For every x in S choose a positive initial state y and a simple positive
path y=x_0,...,x_ell=x, with ell<=|E|-1. Choose rational Lambda>0 at least
the largest exit rate, and set P=I+Q/Lambda. The uniformization series gives

    q(x) >= exp(-Lambda t) (Lambda t)^ell/ell!
            * mu(y) product_{j<ell} P(x_j,x_(j+1)) > 0.  (4)

For ell=0 the empty product is one. Unreachable x have q(x)=0 exactly.
The remaining exponential can be enclosed to any desired precision. An
explicit rational lower bound is also available: with m=ceil(Lambda t),
exp(-Lambda t)>=3^(-m), using e<3. This may be conservative, but proves
effective positivity with no numerical sign guess.

Thus q_min=min_{x in S}q(x)>0 has a finite locally obtained positive lower
certificate. Restricting Q and D to S is valid because S is closed under
positive Q transitions and D is diagonal. All supported v(u) coordinates
then have the uniform positive floor exp(-d_max t)q_min by (3).

This gives an obtaining procedure, rather than an assumption that a
positive global-state minimum is available. A sufficiently accurate positive
local semigroup enclosure will eventually resolve the supported entries.
Very small probabilities, large rates or long horizons can require substantial
arithmetic precision and work; no uniform bit-cost bound is asserted.

## 3. Product mixtures and finitely branched marked resets

There are n local modules with fixed silent generators Q_i and diagonal
recorded-event killing matrices D_i. The global no-recorded-event generator
after opening is the Kronecker sum of A_i=Q_i-D_i. In particular the total
recorded hazard is additive across the admitted modules. This is a source
condition, not a conclusion drawn from low rank alone.

The autonomous controller starts closed and opens irreversibly at rate
gamma>0. It does not change the Q_i. The observed datum is the first
recorded event at the exact time t, with a specified mark. Its nonnegative
marked-event/reset operator has a supplied finite factorization

    J = sum_{b=1}^B beta_b tensor_i J_(b,i),
    beta_b>=0.

This includes a local hazard with a product reset, or a finite mixture of
product reset branches. The source's event operators and total killing must
be mutually consistent. The finite factorization of J is not assumed for
arbitrary rules. The known post-event public phase or controller state must
be included in the interface; an unobserved reset state cannot be omitted.

Initialize the leaves with a finite positive product mixture

    mu = sum_{r=1}^R w_r tensor_i mu_(r,i),
    w_r>=0, sum_r w_r=1.

Each local mu_(r,i) may have zeros and may be deterministic. The exact
unnormalized post-event density is

    M = integral_0^t gamma exp(-gamma(t-u))
          sum_{r,b} w_r beta_b tensor_i
          [mu_(r,i) exp(Q_i(t-u)) exp(A_i u) J_(b,i)] du. (5)

The integration variable u is the duration for which the controller has
been open. Before opening no recorded event is possible; after opening the
killed semigroups enforce the absence of earlier recorded events. J supplies
the final selected mark and reset. A positive event density is required for
normalization.

For each r,i the support of its pre-reset local row is the reachability
support S_(r,i) from Section 2. Its post-reset branch support is

    T_(r,b,i)={y: J_(b,i)(x,y)>0 for some x in S_(r,i)}.

This support is independent of u. Different r,b branches may have different
supports. A branch with an empty local support contributes zero and can be
dropped. The complete output support is their union of product supports.
There is no requirement that every branch be positive on the same ambient
space. Shared structural zeros are handled branchwise, without a global
configuration enumeration.

Positive multiplication by J_(b,i), positive tensor products, and positive
summation preserve the derivative order in (2). Put

    d_- = sum_i min_x D_i(x,x),
    d_+ = sum_i max_x D_i(x,x).

For the full integrand F(u) in (5), on every positive output coordinate,

    (gamma-d_+) F(u) <= F'(u) <= (gamma-d_-) F(u).        (6)

This can be proved for each product branch by the product rule, then summed.
A valid absolute log-variation constant is

    L=max(|gamma-d_+|,|gamma-d_-|),

or the more conservative gamma+d_+. These bounds contain no silent
transition rates and require no stationary initialization.

## 4. A constructive relative midpoint compiler

Partition [0,t] into cells of maximum width h. For midpoint u_c and cell
width h_c, form the exact positive midpoint sum

    Q_mid = sum_c h_c F(u_c).

By (6), F(u)/F(u_c) lies between exp(-L|u-u_c|) and
exp(L|u-u_c|) on every supported coordinate. The simple pointwise bound gives

    exp(-Lh/2) Q_mid <= M <= exp(Lh/2) Q_mid.

Hence its projective spread is at most exp(Lh), and normalized output TV
is at most tanh(Lh/4). This recovers the earlier compactness bound without
its stationary or strictly positive initialization restriction.

A slightly sharper bound integrates those envelopes over the cell. Define

    a_h=(1-exp(-Lh/2))/(Lh/2),
    b_h=(exp(Lh/2)-1)/(Lh/2),

with a_h=b_h=1 when Lh=0. Integration gives

    a_h Q_mid <= M <= b_h Q_mid,
    b_h/a_h=exp(Lh/2).                                  (7)

For cells narrower than h, the local lower multiplier is larger and the
upper multiplier smaller, so the same constants apply to their sum. Thus
uniform N-cell midpoint quadrature gives posterior-TV at most tanh(Lt/(8N)).
For 0<epsilon<1, it suffices to take

    N >= max(1, ceil(Lt/(8 atanh(epsilon)))).

These statements concern exact node evaluations. A certified positive
finite numerical evaluation with additional spread C_num multiplies the
spread in (7). It must be budgeted separately.

The resulting product-mixture representation contains at most R B N
components. Each is obtained by local propagation and a local reset at one
node. The bound is independent of the number of global product states.
Its scalar node-count bound does not contain silent-rate magnitudes, but
local propagator evaluation, integer bit lengths, and source acquisition
costs remain explicit.

### Removing a known common exponential from the quadrature bound

The opening density and the common part of the killing can be integrated
into positive quadrature weights. Set

    c=gamma-(d_++d_-)/2,
    rho=(d_+-d_-)/2,
    H(u)=exp(-cu)F(u).

By (6), |H'(u)|<=rho H(u) coordinatewise. Use

    Q_weighted=sum_c omega_c H(u_c),
    omega_c=integral_cell exp(cu)du > 0.

The scalar weights are explicit exponentials, with the continuous c=0 limit
equal to the cell width. The pointwise envelope proves

    exp(-rho h/2) Q_weighted <= M
                              <= exp(rho h/2) Q_weighted.

Its spread is at most exp(rho h). Consequently a sufficient uniform node
count is

    N >= max(1, ceil((d_+-d_-)t/(8 atanh(epsilon)))).       (8)

This bound depends on hazard contrast, and not on gamma or the silent
transition rates. If d_+=d_-, H is constant and the exact exponentially
weighted rule needs one node. The positive scalar weights must themselves
be numerically enclosed; rare source densities and large exponents can still
affect bit costs. This is a proved obtaining alternative, not a claim that
the new Gauss script implements these midpoint rules.

## 5. Obtainable higher relative derivatives

For the local row (1), define rational matrices

    C_0=I,
    C_(m+1)=-Q C_m+C_m A.

Then

    v^(m)(u)=mu exp(Q(t-u)) C_m exp(Au).                  (9)

**Proof.** Differentiate the expression in (9), using the commutation of Q
and A with their respective exponentials. The next inserted matrix is
-Q C_m+C_m A, proving the recurrence by induction. QED.

In particular C_1=-D and C_2=QD-DQ+D^2; the matrices generally do not commute.
Let ||C||_infinity=max_x sum_y |C(x,y)|. The left row mu exp(Q(t-u)) is a
probability row, and exp(Au) is substochastic. Therefore

    |v^(m)(u)(x)| <= ||C_m||_infinity.

On the locally reachable support, (3) implies

    |v^(m)(u)(x)| <= b_m v(u)(x),
    b_0=1, b_1=d_max,
    b_m=||C_m||_infinity exp(d_max t)/q_min,   m>=2.      (10)

Certified upper bounds on exp(d_max t) and certified lower bounds on q_min
make every b_m obtainable by local rational and interval calculations.
After multiplication by a fixed nonnegative local reset matrix, (10) still
holds because |v^(m)J|<=|v^(m)|J. Unreachable coordinates and zero reset
coordinates remain structural zeros of every derivative.

For a product integrand including gamma exp(-gamma(t-u)), the generalized
product rule gives a relative derivative bound of order m:

    B_m = sum_{k_0+...+k_n=m}
           m!/(k_0!...k_n!) gamma^(k_0) product_i b_(i,k_i).

Equivalently, B_m is m! times the degree-m coefficient of
exp(gamma z) product_i sum_{k=0}^m b_(i,k)z^k/k!.
Truncated coefficient convolution obtains it without enumerating global
states. For several initial mixture branches, use their maximum B_m;
positive summation and reset branching preserve the bound. Unlike the
midpoint mesh bound, these conservative higher-derivative bounds can depend
substantially on silent rates through the commutators.

For four-point Gauss quadrature on cells of maximum width h, the positive
Peano remainder yields

    |M-G| <= delta M,
    delta=C_4 h^8 B_8 exp(Lh),
    C_4=1/1778112000.                                    (11)

The per-cell absolute remainder is at most C_4 h_c^9 sup|F^(8)|.
Using |F^(8)|<=B_8F and sup_cell F<=exp(Lh_c) average_cell F proves (11)
after summation. This is the relative argument detailed in
`relative_gauss_entrance_proof.md`, now with arbitrary initial rows.

If the retained positive lower-node law L_node satisfies

    L_node<=G<=C_num L_node,

and delta<1, then

    L_node/(1+delta) <= M <= C_num L_node/(1-delta).       (12)

This is the unnormalized source certificate. Its spread is
C_num(1+delta)/(1-delta), and the usual sharp projective-TV conversion gives
the all-future normalized guarantee. If the supplied initial entrance was
itself certified with spread R_init, the full spread is multiplied by
R_init. The composition compares the same source operation on both inputs.

## 6. Positive tensor entrances can also be reused

The midpoint order argument does not intrinsically require an initial product
mixture. For any supplied nonnegative global entrance row, use the same
derivative identity with Q=sum_i Q_i and D=sum_i D_i. Its pointwise log
variation is still bounded by (6). Compact execution requires a representation
that admits the local node operators.

In particular, applying
tensor_i[exp(Q_i(t-u))exp(A_i u)J_(b,i)] to a positive tensor train changes
only its physical indices. Each node/reset branch preserves the train's
bond dimensions. Summing N nodes and B reset branches yields a positive
mixture of at most NB such trains per initial tensor component. The count
interface in `unresolved_count_interface_proof.md` is one possible input.

This is a representation-level closure theorem. A general positive-TT
opening executor is not claimed to be implemented by the binary
product-initialization script. Local entrywise propagator certificates can
be obtained using the reachable-support argument for each local basis
initial state; no global minimum probability is necessary for the midpoint
certificate. Any proposed numerical TT compression would need an additional
relative certificate.

## 7. Implemented deterministic initialization and targeted review

The new `nonstationary_gauss_entrance.py` introduces a checked source adapter
for one initially closed irreversible controller and binary modules whose
silent generators are unchanged by opening. It accepts arbitrary exact local
probability rows, including zeros. The numerical adapter requires positive
binary on/off rates, so its t>0 local reachable support is the whole binary
space. The more general finite/reducible support theorem above is proved,
not claimed as implemented by this adapter.

The demonstrated source starts all 24 leaves deterministically off. Its
first specified reaction is observed at t=3/2 and resets its firing site to
zero. The source is obtained through the general source compiler's new
product-mixture initialization route. The previous stationary adapter is
unchanged.

The completed execution in `nonstationary_gauss_entrance_results.json`
records 128 time cells, 512 positive product components, and the source
entrance-density interval

    [0.00926179861912889841598728015009658300218322409,
     0.00926179864897264376407472299929130487123208701].

Its all-common-future-operation posterior-TV upper bound is

    8.05560197518429609579296931006334866426137634e-10.

The exact rational law is saved as
`nonstationary_correlated_entrance_24sites.json` and accepted by the existing
reusable entrance loader. The reported four-point quadrature relative error
is approximately 1.611120395e-9; the node-rounding spread minus one is
3.09e-42. These are separate from the sharp normalized TV conversion.

Targeted independent code inspection confirmed the following mathematical
and arithmetic points: the silent pre-opening row is computed first and
multiplied on the right by the killed exponential; the C recurrence uses the
previous C consistently; q_min is replaced by a positive LOWER enclosure;
exp(d_max t) is replaced by an UPPER enclosure; b_0=1 and b_1=d_max are
correct; and the source adapter explicitly checks equality of the two
silent generators. Initial-row positivity is not used or required.

The completed separate three-leaf comparison uses a 16-state expanded killed
reference and rational positive uniformization. All four positive post-reset
coordinate enclosures lie inside the acquired relative sandwich, and four
structural-zero coordinates are checked. Its reported Poisson-tail upper
bound is 1.34556900712742475173284895147163561550160513e-51. This is a small
implementation check; the general guarantee is the local proof and enclosure
construction. Neither source acquisition nor this full computation was
rerun for the targeted review described here.

## 8. Scope of the extension

The removed restrictions are equilibrium initialization and initial positive
mass at every state. The retained restrictions include unchanged silent Q
across opening; finite locally obtainable modules; an autonomous single
irreversible opening with known rate; additive nonnegative recorded-event
killing; a specified initialization representation; and an obtainable finite
positive marked-reset factorization. State-dependent opening, changed silent
kinetics, arbitrary hidden common resets and arbitrary nonlinear observation
interfaces require new obtaining arguments.

The latent opening time is marginalized. The retained post-event physical
state and known public information must suffice for future dynamics.
Retrospective opening-history questions are not covered by a state-only
certificate. Subsequent approximate operators consume their own relative
error budgets, while exact common positive operations preserve the retained
spread, as proved in `conditioning_stable_entrance.md`.

The underlying killed-semigroup algebra, positive quadrature and projective
filtering are established mathematical tools. The extension here establishes
the enlarged obtaining conditions and their reusable composition. It is not
an identification claim about unknown biology or a claim that a special
retaining architecture is necessary.
