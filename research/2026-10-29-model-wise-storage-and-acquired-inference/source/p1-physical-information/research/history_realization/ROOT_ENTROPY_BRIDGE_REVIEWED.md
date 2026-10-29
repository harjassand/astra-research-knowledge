## 3. Why a finite observable inequality must exist

All finite tree tables lie in a compact product of finite simplices. Each
consistency equation involves finitely many entries. The full extension
exists if and only if every finite subsystem is feasible, by compactness.
Each finite subsystem is an ordinary linear feasibility problem.

If p fails the hierarchy, a finite subsystem has a Farkas separation
certificate. Its only supplied inputs are finitely many observed path
probabilities; structural matrix entries are rational. Strict separation
allows a certificate with rational coefficients. If the inputs involve
several time grids, shift them by stationarity into a common [0,T] and
take the union of their rational times. Each original probability is a
marginal of that larger word table. The dual inequality is exactly the
expectation of one bounded statistic F on this common grid, as in (1).

Finite separation alone follows already from closed convexity. The tree
contribution is an explicit complete family of finite LP/dual certificates,
without choosing a hidden-state count or a hidden rate parametrization.

Finite reversible models may be reducible because mixtures are allowed.
This does not change the closure if irreducibility is required: add an
epsilon-rate refresh to the stationary law. The new generator stays
reversible and becomes irreducible on positive-weight states. Coupling
until the first refresh bounds path TV change on [0,T] by 1-exp(-epsilon T).
Finite positive mixtures and their stationary weights are actual model
resources, not acquired initial preparations.

## 4. Entropy controls distance to the equilibrium class

Let Q be an all-even finite CTMC with strictly positive stationary law pi
on its supported states. Put Q*_(xy)=pi_y q_yx/pi_x and

    A=(Q+Q*)/2.

A is reversible for pi and has exactly Q's escape rates, since Q* does.
Take both stationary processes with the same initial pi. Their complete
path divergence on [0,T] is

    D(P_Q || P_A)=T sum_{x<y} B(f_xy,f_yx),
    B(f,g)=f log[2f/(f+g)]+g log[2g/(f+g)],                (6)
    f_xy=pi_x q_xy.

The usual conventions handle zero fluxes; if sigma is infinite the bounds
below are automatic. Otherwise reciprocal support holds. The all-even
stationary entropy rate is

    sigma=sum_{x<y}(f_xy-f_yx)log(f_xy/f_yx).

For f,g>0,

    B(f,g) <= (f-g)log(f/g)/4.                             (7)

One direct proof writes f+g=s and d=(f-g)/s. Both sides are even in d.
After division by s the difference, for d>=0, has derivative

    [d/(1-d^2)-atanh(d)]/2 >= 0,

and is zero at d=0. The nonnegativity follows by differentiating the
bracket. Thus

    D(P_Q || P_A) <= T sigma/4.                           (8)

Equation (7) uses an UNAVERAGED scalar flux-pair bracket. For normalized
probability distributions, the conventionally averaged Jensen-Shannon
divergence has the corresponding sharp local bound Jeffreys/8. These
normalizations must not be interchanged.

Observation and finite-time sampling contract KL. The observed law of A
belongs to E. If F has range L and violates (1) by gamma, the expectation
gap between Q and A is at least gamma. With TV defined as half the L1
distance, |E_Q F-E_A F| <= L TV. Pinsker and (8) give

    gamma <= L sqrt(T sigma/8),

which proves (2). No hidden dimension, spectral gap, clock bound or mixing
time appears in this valid inequality. Their absence is not a claim that
the needed observations can be obtained free of those resources.

### Reusing the stronger time-symmetric transfer

When the observed target itself is time-reversal symmetric, symmetrize F
with its reversed statistic on the union of the grid and its reflection.
The target and every equilibrium mean are unchanged; the range does not
increase. The previously developed geometric path comparison then gives
the stronger linear bound

    sigma >= 4 gamma/(T L).                              (9)

For completeness, let p,p* be the full path densities under Q,Q*, and a
the path density under A. Because Q and Q* have the same escape clocks,
the arithmetic/geometric mean inequality on every jump gives a>=sqrt(p p*)
pointwise. Also (p+p*)/2>=sqrt(p p*). Hence

    TV((P_Q+P_Q*)/2,P_A) <= 1-integral sqrt(p p*).

The scalar inequality (u-v)log(u/v)>=4(sqrt(u)-sqrt(v))^2, integrated on
path space, bounds this last deficit by T sigma/4. A symmetric statistic
has the same expectation under Q and (Q+Q*)/2 as PATH LAWS, proving (9).
This path mixture is not the Markov law of the arithmetic generator A;
the pointwise comparison is what connects them. The transfer mechanism
and its coefficient are reusable prior Astra capital, not a new numerical
bound claimed for this branch.

## 5. A convex information-distance form

For a finite observation grid G in [0,T], let p_G be its joint word law.
Let C_m(G) be any finite tree-hierarchy relaxation projected onto the
grid's word table. Include that grid as a path table and leave every OTHER
path table and every unobserved extension table variable. Do not fix other
paths to target statistics: that could exclude the comparison equilibrium
model and invalidate the bound. Every equilibrium grid law is in C_m(G).
Then (8) and data processing give

    sigma >= (4/T) min_{r in C_m(G)} D(p_G || r).          (10)

The right side is an ordinary convex optimization problem, not a new
optimization primitive. Rational Farkas witnesses plus Pinsker recover
(2). Enlarging finite subsystems tightens the admissible polytope. With
fixed G and an exhaustive hierarchy, their intersection is exactly the
projection of E onto G by compactness; KL lower semicontinuity then gives
convergence of the minima to the information distance from that set.

Taking all finite grids and levels is complete for positive detection:
if p is outside E, some finite grid and finite level have a positive
value. This does not make (10) the optimal numerical entropy bound, nor
does it give a finite acceptance certificate when p is in E.

## 6. Acquisition, certification and reuse

The preceding claims are about exact probability laws. A direct finite
acquisition contract for one witness is N independent preparations of
the same stationary source, each observed at its specified grid during
T native time units. With scores in an interval of length L, Hoeffding's
one-sided radius is

    epsilon_N = L sqrt(log(1/alpha)/(2N)).

If the empirical score is fbar, set gamma_cert=max(0,-fbar-epsilon_N).
With probability at least 1-alpha, (2) is valid with gamma_cert, and (9)
is valid when its extra symmetry condition is justified. Repeated or
data-selected witnesses require independent held-out validation or a
simultaneous confidence construction. A confidence region for p_G can
also be inserted directly into (10), minimizing jointly over admissible
data laws and over r; joint convexity preserves the ordinary convex form
when that confidence region is convex.

A countable enumeration of rational dual certificates with summable
failure budgets, and increasing independent validation, eventually detects
every fixed strict separation. There is no source-uniform finite level,
runtime or sample bound. The number of possible words and tree tables
can grow severely; enumeration is a completeness argument, not a practical
default. Existing model fits and established correlation or CP witnesses
should be used when they solve the task more cheaply.

The direct contract consumes N actual stationary preparations and N T
native observation time, plus all observations, storage, arithmetic and
timing precision. If samples instead come from one long trajectory,
dependence needs an acquired or justified mixing bound; stationarity alone
does not make them independent. Known sensor/timing TV error eta costs at
most L eta in the witness margin. Tree branches are mathematical extension
variables, not cloning operations, samples or available hidden-state resets.

Reuse is genuine but limited: acquired word records can test further
statistics measurable on the same grids, with valid simultaneous inference.
They do not supply new interventions, branch experiments, exact short-time
zeros or a prepared hidden simulator.

