# Exact graph boundary for uniformly fast latent activity

Separate ordinary graph/CTMC scope lemma, not a new general stability theorem.
No external retrieval. The graph equivalence is elementary and is proved here;
no historical novelty is claimed. Existing frozen main sources are unchanged.

Let G be a finite simple graph with AT LEAST ONE EDGE, including any isolated
vertices in its vertex set. For integer capacities x>=0 write

    S(x)=sum_v x_v,     Q_G(x)=sum_{uv in E(G)} x_u x_v.

Call x active if Q_G(x)>0. The nonempty-edge assumption is essential: for an empty
graph the activity implications below are vacuous.

## Theorem

The following are equivalent:

1. G is complete multipartite, with at least two independent parts and no omitted
   vertices (hence no isolated vertices).
2. G has no induced three-vertex graph consisting of one edge and an isolated vertex.
3. For every integer x with Q_G(x)>0, Q_G(x)>=S(x)-1.
4. There exist c>0 and S0<infinity such that Q_G(x)>=c S(x) for every active integer
   x with S(x)>=S0.

**1 implies3.** Let z_j be the total on each part and M=max z_j. Activity implies
1<=M<=S-1. Completeness gives Q=Σ_{i<j}z_i z_j>=M(S-M)>=S-1; the last inequality
is equivalent to (M-1)(S-M-1)>=0. Integrality is used at this last step.

**3 implies4.** Take c=1/2,S0=2.

**4 implies2.** If uv is an edge and w is adjacent to neither endpoint, put x_u=x_v=1,
x_w=N and all other counts zero. Then Q=1 and S=N+2, contradicting4 as N diverges.
This is an exact integer witness, not a numerical limit-law argument.

**2 implies1.** Define u~v if u=v or uv is not an edge. This relation is reflexive
and symmetric. If u~v,v~w but uw is an edge, the three vertices induce precisely
the forbidden edge-plus-isolate, so ~ is transitive. Its equivalence classes are
independent, and every pair from distinct classes is adjacent. The graph is complete
multipartite. Since an edge exists there are at least two classes.

## Exact stochastic consequence, and what it does NOT say

Consider the raw hub architecture of the multipartite candidate, but now allow ANY
nonempty square-free hub graph: only0<->A changes total count, and all internals
join A-free hubs to2A or A+X. Let s_h be the sum of all rates leaving hub h.
At A=0 the total internal exit rate is exactly

    sum_h s_h x_u x_v.

If G is complete multipartite, this is at least s_min(N-1) at every active latent
state. Every such departure creates A. Thus uniformly linear latent activation
rate is a genuine acquired graph property, not a stationary-fiber premise.

If G is not complete multipartite, the graph theorem supplies uv,w. At
A=0,x_u=x_v=1,x_w=N, all other counts zero, the ONLY active hub is uv. Internal
exit rate is s_uv, independent of N; death is off and immigration is lambda.
Consequently

    P(immigration precedes every internal jump)=lambda/(lambda+s_uv)>0.

This is included in a first-core up event. A uniform O(1/N), or any vanishing,
first-core up bound over all positive-inventory states is therefore impossible
for that architecture. No alternate sampling rule or joint Lyapunov construction
is excluded. In particular this is NOT a transience result, an obstruction to
all exponential moments, or a claim about networks with additional internal
channel types. Ordinary unit-rate detailed-balanced examples lie on both sides.

The converse clock claim is deliberately limited: the linear internal-exit bound
alone does not prove recurrence or an O(1/N) first-core up bound. The separate
multipartite proof earns stability with a weighted inverse boundary energy plus
an interior A-activation correction, retaining real seed loss and physical time.

## Relation to the earlier inventory boundary

The earlier complete-BIPARTITE-COMPONENTS theorem classifies a different universal
property: every enabled hub removal lowers maximum capacitated matching by exactly
one. That geometry can include isolated free passengers and disconnected components,
so it can have a constant latent clock; its acquired unbounded inventory profile
pays that clock. The current complete-MULTIPARTITE graph property removes those
slow latent configurations but permits matching drop-two, repaired by a different
joint energy. Neither property classifies stable networks. Their two concrete
obstructions identify why a general hub-graph theorem needs a genuinely new join.
