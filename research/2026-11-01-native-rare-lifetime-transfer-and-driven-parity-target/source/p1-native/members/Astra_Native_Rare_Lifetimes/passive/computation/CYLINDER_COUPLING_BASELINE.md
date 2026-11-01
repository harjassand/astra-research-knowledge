# Strong ordinary baseline: arbitrary rates near independent flips

The parent identified this stronger existing construction before retaining
the independent-flip cylinder as evidence of a new consequence. The
construction below independently verifies it. It solves that subcase with
ordinary graphical coupling and a small birth-death calculation, including
when the actual source is nonreversible and has an unknown nonproduct
stationary law. It must therefore be credited as a successful baseline.

## Contract

The state is x in {0,1}^n. Only single-bit flips occur. The actual flip
rate q_i(x) can depend arbitrarily on x, subject to

    c(1-eta)<=q_i(x)<=c(1+eta),  c>0, 0<=eta<1.

The target A fixes the first m bits to0; the other n-m coordinates are
unconstrained. Fixing an arbitrary bit pattern is equivalent after
flipping the corresponding coordinate labels. The reference has all
q_i(x)=c. Write pi for the actual stationary law, b=pi(A^c),
mu=E_pi tau_A and M=E_(pi(.|A^c)) tau_A=mu/b.

The rate box can be the output of the same passive confidence procedure
used elsewhere. No true stationary samples, known stationary density,
rare input state, or assumed monotonicity of the actual dynamics is added.

## A pathwise ordered coupling without actual attractiveness

Let L and U be independent-bit systems with rates

    L: 0->1 at c(1-eta), 1->0 at c(1+eta),
    U: 0->1 at c(1+eta), 1->0 at c(1-eta).

For each coordinate use the following independent Poisson clocks and
independent uniform marks for accepting actual extra moves:

1. At rate c(1-eta), set that coordinate in all three processes to1.
2. At rate c(1-eta), set that coordinate in all three processes to0.
3. At rate 2eta c, set U's coordinate to1 and, if X's coordinate is0,
   set it to1 with probability [q_i(X)-c(1-eta)]/(2eta c).
   L's coordinate is unchanged.
4. At rate 2eta c, set L's coordinate to0 and, if X's coordinate is1,
   set it to0 with probability [q_i(X)-c(1-eta)]/(2eta c).
   U's coordinate is unchanged.

For eta=0 only the first two clocks are needed. Each marginal generator
is exactly the stated generator; null settings do not count as physical
jumps. If L<=X<=U holds coordinatewise before any update, it holds after
that update. This is true for every accepted actual move, regardless of
how q_i(X) changes with the rest of X. Thus no attractiveness assumption
on X is needed.

The finite joint chain restricted to ordered triples has a stationary
distribution (for example, take a subsequential Cesaro limit). Its three
marginals are the unique stationary laws of L, X and U. Start from such
a stationary coupling. Since A is a down-set,

    tau_A(L)<=tau_A(X)<=tau_A(U) almost surely,
    mu_L<=mu<=mu_U,
    p_L>=p>=p_U,  b_L<=b<=b_U.                     (1)

Consequently the actual stationary-conditional mean satisfies

    mu_L/b_U <= M <= mu_U/b_L.                    (2)

One must not simply condition the ordered stationary coupling on each
process's different complement event. Such conditioning need not preserve
the required marginal order. Formula(2) handles the denominators safely.

## Exact small reference computations

For either bounding process, let a be its up-rate and d its down-rate.
The number J of1s among the m target coordinates is a birth-death chain
with upward rate a(m-j) and downward rate d j. Its stationary probabilities
are

    p_j=binom(m,j) r^j(1-r)^(m-j), r=a/(a+d).

The mean hitting time t_j of0 obeys t_0=0. For increments
Delta_j=t_j-t_(j-1), the exact backward recurrence is

    Delta_m=1/(dm),
    Delta_j=[1+a(m-j)Delta_(j+1)]/(dj),
    t_j=sum_(k=1)^j Delta_k,
    mu=sum_(j=1)^m p_j t_j, b=1-p_0.              (3)

This requires O(m) arithmetic operations after binomial weights are
available. Rational input gives a rational exact calculation; bit lengths
are polynomial in m and input precision. The long mean is represented
as a number rather than observed as a waiting time.

For the same reason, the unconditional survival curves S_L(t), S_U(t)
are those of two killed m-state birth-death matrices. The pathwise order
in(1) gives the full stationary-conditional CDF bracket

    max{0,1-S_U(t)/b_L} <= F_(actual|A^c)(t)
                        <= min{1,1-S_L(t)/b_U}.    (4)

Thus this baseline addresses deadline risk too, not merely a mean. A
separate high-precision small-matrix exponential or spectral evaluation
can evaluate(4); no such numerical deadline experiment is claimed here.

## Stronger consequence: pointwise stationary density for every target

The same coupling gives more than one cylinder estimate. Fix any pattern
z in {0,1}^n and relabel every bit by y_i=x_i XOR z_i. Actual flip rates
in the relabeled coordinates still lie in c(1+/-eta), even if they are
nonmonotone functions of all the bits. The singleton {z} becomes the
down-set {0^n}. Applying the stationary order to that singleton proves

    [(1-eta)/2]^n <= pi(z) <= [(1+eta)/2]^n

for every z, simultaneously as deterministic consequences of the rate box.
Relative to uniform pi0 this is the pointwise certificate

    (1-eta)^n <= pi(z)/pi0(z) <= (1+eta)^n,
    u_coupling=-n log(1-eta).                       (5)

There is no resolvent-bootstrap smallness condition in(5). The product
forcing bound from MISMATCH_AUDIT.md Section6 is consequently unnecessary
and weaker for the pure independent-flip reference. The pointwise result
also implies [(1-eta)/2]^r<=pi(cylinder pattern on r bits)<=
[(1+eta)/2]^r by applying the same construction only to those r coordinates.
It supplies inexpensive local-context mass lower bounds.

This result remains valid for unequal symmetric reference bit rates c_i,
using rate c_i in each coordinate's clocks. If relative widths are eta_i,
the density bounds become products of(1-eta_i) and(1+eta_i), with the
valid symmetric log certificate -sum_i log(1-eta_i).

Pointwise density comparison(5) can feed the ordinary symmetric/skew
inverse comparison in MISMATCH_AUDIT.md Section7 for ANY target, including
a nonmonotone affine code. Thus moving to a nonmonotone target defeats
the direct pathwise hitting order but does not defeat this stronger
equally informed ordinary route. Any claim of a new consequence must
compare against that combination too.

## Executed earlier comparison regime

The exact Fraction computation in cylinder_coupling_budget.py uses

    n=80, m=64, c=1/2,
    eta=0.000391378=195689/500000000.

It verifies every positive-state Poisson equation in(3) exactly. The
reference target probability is 2^-64, approximately5.4210108624e-20.
The reference conditional mean is approximately5.859216656491188e17.
For every actual source in the rate box, the resulting mean ratio obeys

    0.9756623015866811 <= M/M0 <= 1.0249550133275007.

The displayed decimals are floating presentations of exact rational
outputs. The script additionally proves the clean rational inequalities
M/M0>0.975 and M/M0<1.025 for its conservative endpoints. Absolute endpoints
are approximately5.716616808567211e17 and6.005433486242641e17. Results are
saved in cylinder_coupling_results.json. No trajectory is generated.

The parent later selected eta=9/20000=0.00045 for the main coded-target
certificate. That is a different budget from the executed cylinder
comparison above. Equation(5) gives, without another experiment,

    u<=80 eta/(1-eta)<181/5000,
    v<=81 eta/(1-eta)<367/10000.

The parent's subsequent mean and deadline calculations use these
conservative bounds. The source at rate c=1 has reference gap2; changing
c rescales means but does not change any mean ratio or density certificate.

## Consequence for the opening

This ordinary construction already converts the rate box into accurate
rare-output predictions for the product-reference cylinder. Its validity
does not depend on target visits, known actual stationary structure,
actual monotonicity, or a lumped actual count process. A general learned
flow certificate may be useful on that subcase, but cannot claim that
subcase as a previously missing consequence.

The order argument uses the down-set property of the target. For a
nonmonotone code target ker(H), coordinatewise L<=X<=U does not order
target membership or hitting times. However, the stationary pointwise
bound(5) still holds, and the general inverse comparison then controls its
mean. That combined ordinary construction is a successful stronger
comparator; a coded target needs an additional consequence or a broader
reference class to establish a missing operation.

General stochastic comparison of Markov processes has a long history;
one primary reference is W.A.Massey1987, Stochastic Orderings for Markov
Processes on Partially Ordered Spaces, Mathematics of Operations
Research12(2),350--367, DOI10.1287/moor.12.2.350. Only its publisher abstract
was retrieved here. The explicit coupling above supplies the needed proof
without attributing an unexamined theorem or sharp constant to that paper.
