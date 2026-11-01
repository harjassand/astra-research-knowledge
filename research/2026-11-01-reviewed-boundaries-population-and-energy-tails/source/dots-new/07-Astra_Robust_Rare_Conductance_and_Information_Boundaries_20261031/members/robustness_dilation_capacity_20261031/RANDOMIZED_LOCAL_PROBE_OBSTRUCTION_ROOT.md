# Randomized local probes: a fixed hidden barrier

Status: new root construction, not yet independently reviewed. This is a generic
information obstruction, not a novelty claim or a lower bound for bounded-degree
symbolic input. It does not challenge the declared full-coefficient receiver.

Fix an admitted nominal potential F0 and a finite constant mobility diag(1,M),
with M positive definite. An oracle returns values and arbitrary finite jets at queried points.
An adaptive randomized procedure terminates almost surely on F0. Suppose it
reports a strictly positive conductance lower bound with probability q>0.
For every epsilon>0 there is a fixed smooth alternative F1, agreeing with F0
outside a compact subinterval of the slab, on which its reported lower bound is
false with probability at least q-epsilon. Thus no uniform positive lower-bound
certification can follow from finitely many unrestricted local probes alone.

Proof. Couple all algorithm randomness on F0. Choose K so the probability that
the number of queries exceeds K is below epsilon/3. For missing queries pad by
a fixed point outside the slab. Choose L>0 so the probability of reporting a
lower bound at least L is at least q-epsilon/3. Inside a fixed compact open slab
interval J choose a uniformly translated interval I of sufficiently small length.
For every possible query coordinate y, the fraction of translations whose I
contains y is at most |I| divided by the permitted translation range. A union
bound for the first K queries, then averaging over translations, yields one
FIXED interval I for which P(any of these queries hits I) < epsilon/3. No query
density or independence assumption is needed. Shrink permissible translations
to keep the closure of I inside J.

Take a smooth nonnegative bump b supported inside I and at least one on a
subinterval I0 of positive length. Set F_A=F0+A b(y). Under the same algorithm
randomness, every oracle response (including finite derivatives) is identical
until a query enters I. On the event of at most K nominal queries and no hit,
the entire stopped transcript and reported number therefore coincide. The
probability of such coincidence together with a reported bound at least L is
at least q-epsilon, uniformly in A.

The unnormalized basin mass M_A is unchanged. A scalar trial function that
changes only across I0 has capacity at most

  exp(-beta A)/(beta |I0|^2) * integral_{I0 x R^m} exp(-beta F0).

Consequently its equilibrium conductance tends to zero. Select a fixed finite
A making that conductance below L. This F_A is fixed independently of the
algorithm's realized randomness. Its false lower-bound probability is at least
q-epsilon, as claimed.

Global receiving. F_A>=F0 gives finite Gibbs mass. For the nominal coercive
quadratic Lyapunov V=1+y^2+K z^T M^{-1}z, the additional generator term is
-2 A y b'(y), bounded above on the compact bump support, independent of z.
The nominal bound LV<=C thus becomes LV<=C+C_A, proving nonexplosion of each
fixed actual smooth diffusion. Basins and noise/mobility are unchanged. The
ordinary reversible Dirichlet capacity used above is therefore a legitimate
output of the received global process.

Restrictions. The argument allows arbitrarily narrow/high smooth barriers, so
it does not apply under fixed derivative bounds, fixed polynomial degree, a
known finite-dimensional parametric class, interval-enclosure oracles, or actual
global radial-envelope certificates. It concerns local value/derivative queries,
not trajectory observations, equilibrium sampling, or other richer interfaces.
Finite almost-sure termination on F0 is enough; no uniform expected query bound
is assumed. A procedure which reports UNKNOWN instead of a positive bound is
not contradicted.
