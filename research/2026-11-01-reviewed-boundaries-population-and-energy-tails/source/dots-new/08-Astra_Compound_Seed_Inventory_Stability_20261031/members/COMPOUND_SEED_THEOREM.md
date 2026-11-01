# Acquired compound-seed inventories with an active-phase corrector

**Status: candidate ordinary proof; independent review pending.** Pure mathematics.
Accepted earlier artifacts are unchanged. This is a sufficient structural theorem,
not the general weak-reversibility conjecture, not the entire one-port conservative
class, and not a novelty claim. All rates below are arbitrary positive real numbers.
The executable interface separately restricts rates to exact positive rationals.

## 1. Raw family and finite acquisition of the inventory

There is one species A and n-1 satellites, n>=3. Only `0 <-> A` changes total count
N; its rates are lambda and mu. Every other nonnull channel is binary and has one
of the following forms, with the indicated reverse also present:

* `2A <-> H`, for every hub H;
* `A+X <-> H`, for selected satellite/hub pairs, covering every satellite X.

A hub is `X+Y` for two distinct satellites. Make the undirected graph whose vertices
are satellites occurring in hubs and whose edges are the hubs. Require each of its
k>=1 connected components to be complete bipartite. Thus hub pairs may overlap
extensively: a component may be any biclique, not merely one isolated edge. Satellites
outside this graph are free passengers. The reaction list itself discovers the graph,
its components, and the two shores of every component by deterministic two-coloring
and checking all cross-shore pairs. No grouping, siphon inventory, stationary fiber
law, or Lyapunov function is input. Channels with the same endpoints are combined.
Null channels can be discarded. No other nonnull channels are included here.

For component j let L_j and U_j be the total counts on its two shores. Set

    m = sum_j min(L_j,U_j),       R = A+m.

All the following claims are invariant under swapping the shores of any component.
The compiler checks the finite raw conditions; successful recognition is already a
qualitative recurrence/all-exponential-moments certificate by this theorem. A failed
recognition is UNKNOWN for stability. It does not exclude a different inventory.

### Inventory identities

Insertion or removal of a hub increases or decreases both of its shore totals by
one, so its contribution to m changes by exactly +1 or -1. In an arm reaction,
consuming one satellite can decrease its shore minimum by zero or one. It follows:

* `2A -> H` decreases R by one; `H -> 2A` increases R by one.
* `A+X -> H` changes R by zero or minus one.
* `H -> A+X` changes R by zero or plus one.
* Core immigration/death changes R by plus/minus one.

An internal decrease at R=1 is impossible: 2A needs A>=2; a decreasing arm needs
A>=1 and a positive shore minimum. Hence {R>=1} is internally invariant. R=0 means
A=0 and every shore minimum is zero, so every internal propensity is zero. This is
an **activity inventory**, not a conserved numerical quantity. A=0 alone does not
freeze the dynamics.

## 2. Rate summaries and the two physical mechanisms

Write b_h for the rate of `H -> 2A`, a for the sum of rates of `2A -> H`, and s_h for
the sum of all reverse-from-hub rates at hub h (including b_h). For each satellite
X let k_X be the sum of its forward arm rates `A+X -> H`. All k_X and b_h are positive.
Define

    k_- = min_X k_X,       k_+ = max_X k_X,
    K_f = a + 2 k_+,      beta = (min_h b_h)/(2k),
    sratio = max_h s_h/b_h.

Let r=R and j=A. Seed-decreasing internal rates are at most K_f j r. Indeed 2A has
rate a j(j-1), and a decreasing arm consumes from a shore whose total is no larger
than the opposite shore (at equality either shore may decrease). The total counts
on all such shores are at most 2m; their arm rates are at most 2 k_+ j m.

There is also a large family of **R-neutral, A-consuming** arm reactions. Every
satellite on a strictly larger shore is neutral, as is every free passenger. Their
aggregate rate is at least

    k_- j [sum_free X + sum_components |L_j-U_j|]
      = k_- j (N-2r+j).                                      (1)

The parenthesis is always nonnegative. For the polynomial estimates below, all
remaining seed-decreasing forward rates are at most K_f r^2; remaining neutral
forward reactions can be dropped because they only improve the correction drift.

Finally completeness of the acquired bipartite components gives the exact identity

    sum_h x_i x_j = sum_components L_j U_j >= sum_j min(L_j,U_j)^2 >= m^2/k.

Consequently, after reserving half of each b_h rate for the later phase correction,
seed amplification still has rate at least beta m^2. This is the earned quadratic
amplification; it is not an assumed independent success coin or a stationary law.

## 3. Acquiring a decreasing inventory profile, for each t>1

Fix any finite t>1. Put

    L=lambda(t-1),   epsilon=min(1,(lambda+beta)/2),
    c=4(L+epsilon)/beta,        K=max(2,ceil(2c)).

For integer r>=K set g_r=1+c/r. Construct r=K-1,...,1 backwards by

    g_r = [(lambda*t+beta*r^2)/(lambda+beta*r^2-epsilon)] g_(r+1).       (2)

Set g_0=2t g_1. Every denominator is strictly positive: epsilon<lambda+beta.
The multiplier in (2) is strictly larger than one, so g_r strictly decreases to 1.
All computations are finite. Define d_r=g_r-g_(r+1)>0 (r>=0). Then for all r>=1,

    lambda(t g_(r+1)-g_r) - beta r^2 d_r <= -epsilon g_r.              (3)

For r<K this is equality. For r>=K, c/r<=1/2, r/(r+1)>=1/2, and the left side is
at most L+L/2-beta*c/2 = -L/2-2epsilon <= -epsilon(1+c/r).

This finite recurrence joined to a certified rational tail is the only unbounded
inventory-profile acquisition. No infinite product is numerically evaluated.
The profile remains valid for every positive rate ratio and any requested t>1.
Costs can become very large; qualitative admission need not materialize them.

Let

    d_* = min( c, min_{1<=r<K} (r+1)^2 d_r ) > 0.                      (4)

The explicit tail shows (r+1)^2 d_r>=d_* for every r>=1.

## 4. Acquiring the active/latent phase correction

Let D=mu(1-1/t)>0 and

    J=max(K+1,2,ceil(4c(mu+K_f+beta)/D)).

For 1<=r<J evaluate

    E_r = mu(t^(-1)g_(r-1)-g_r) + K_f r d_(r-1) + 2 beta r d_r.       (5)

Acquire the single finite rational constant

    q = 1 + max_{1<=r<J} [4(r+1)^2 max(E_r,0)/k_-].                    (6)

For r>=J, both neighboring inventory terms are in the rational tail and

    E_r <= -D + 2c(mu+K_f+beta)/r <= -D/2.                            (7)

Here r/(r-1)<=2 is used. For the finite head, (6) earns the needed compensation;
there is no favorable-pivot or finite-layer LP oracle.

For N>=0 define f=A/(R+1)^2 and

    h(x)=g_R + q f/(N+1),             W(x)=t^N h(x).                  (8)

This is defined at R=0 too, since then A=0 and f=0. Always

    1 <= h <= H:=g_0+q/4,

because A<=R and R/(R+1)^2<=1/4. W is normlike and comparable to t^N.
The correction's amplitude is O(1/N) at a fixed inventory, but its drift through
fast A+bulk capture is order one. Dropping it is not an innocuous simplification.

## 5. Uniform finite-count generator bounds

Each internal jump has |Delta A|<=2 and |Delta R|<=1. For r>=1 direct subtraction
and A<=r give

    |Delta f| <= 11/(r+1)^2.                                        (9)

For a decrement, denominators are at least r, and
`2/r^2 + r(1/r^2-1/(r+1)^2) <= 11/(r+1)^2`; increments are smaller. The bound also
covers the allowed transition to r=0. A neutral A-consuming arm has exactly
Delta f=-1/(r+1)^2. Therefore the internal generator satisfies

    L_int f <= -k_- A(N-2r+A)/(r+1)^2
               + 11 K_f r^2/(r+1)^2
               + 11 sum_h s_h x_i x_j/(r+1)^2.                     (10)

Other neutral forward arms have nonpositive f drift and are discarded. The first
positive term bounds the seed-decreasing forward channels; the last bounds all
hub reverse channels. The base profile has

    L_int g_R <= K_f A r d_(r-1) - sum_h b_h x_i x_j d_r.             (11)

At r=1 the first term is a harmless overestimate (no internal decrease is enabled).
If

    N+1 >= 22 q sratio/d_*,                                         (12)

the last term of q L_int f/(N+1) is absorbed by half the negative hub term in (11).
The remaining half gives -beta(R-A)^2 d_r by Section 2.

For the core part of q t^N f/(N+1), elementary denominator subtraction gives the
uniform upper bound

    t^(-N) L_core[q t^N f/(N+1)] <= q(12lambda*t+12mu)/(N+1).         (13)

For clarity: birth is bounded by q lambda[11t+(t-1)/4]/(N+1). For a death at N>=1,
write its increment as
`t^(-1)(f'-f)/N + f[t^(-1)/N-1/(N+1)]`.
Use A/(r+1)^2<=1/4, (9), and 1/N<=2/(N+1), giving at most 6q mu/(N+1).
These deliberately enlarged constants retain all physical core costs; death at
A=1 is not replaced by a protected clock. At R=0 the separate computation below
handles the only enabled channel.

Let

    C_e=11K_f+12lambda*t+12mu,
    N_* = ceil max(1, 4J, q, 22q sratio/d_*, 2q C_e/epsilon).         (14)

No state up to N_* is enumerated. For N>=N_* and r>=1, combine (3), (5), and
`r^2-(r-A)^2<=2rA` to obtain

    t^(-N) LW <= -epsilon g_r + A E_r
          - q k_- A(N-2r+A)/[(N+1)(r+1)^2] + q C_e/(N+1).           (15)

If r<J, N>=4J implies (N-2r+A)/(N+1)>=1/4, and (6) cancels A E_r.
If r>=J, (7) is nonpositive and the correction's displayed negative term may be
dropped. Thus (15)<=-epsilon g_r+epsilon/2 <=-epsilon g_r/2.
Since N+1>=q, h<=g_r+1/4<=2g_r, yielding LW<=-epsilon W/4.

If r=0, all internals and death are off. Immigration gives exactly

    t^(-N) LW = lambda(t g_1-g_0) + q lambda*t/[4(N+2)]
              = -lambda g_0/2 + q lambda*t/[4(N+2)] <= -lambda g_0/4

for N>=N_* (use q/(N+2)<=1 and g_0>=2t). Therefore, with

    zeta=min(epsilon,lambda)/4,

we have LW<=-zeta W outside the finite set {N<N_*}.

## 6. Explicit finite exception, recurrence, and all exponential moments

Let S be the sum of all internal rate constants and retain the factored constant

    C_F = (zeta+lambda+mu N_*+S N_*^2) H t^(N_*+1).                  (16)

For N<N_*, each enabled internal propensity is at most its constant times N_*^2,
each destination has total count at most N_*+1, and h<=H. Hence

    LW <= -zeta W + C_F 1_{N<N_*}.                                  (17)

The exception contains binomial(N_*+n-1,n) lattice states; this is an accounting
quantity, not an executed enumeration. Powers in (16) may remain factored.

Nonexplosion is immediate from N(t)<=N(0)+Poisson(lambda t), since internal channels
conserve N and finite sublevels have finite bounded rates. The full graph is weakly
reversible. In fact this family is irreducible on the whole orthant: from zero,
immigrate twice, use 2A->H->A+X and kill A to reach any satellite singleton X; A is
reached directly. The reversed positive-rate paths also exist. Translation of these
finite enabled paths constructs or removes any requested count vector one singleton
at a time. There is no hidden irreducibility or stationary-fiber premise.

The ordinary countable-state Foster theorem applied to (17) gives positive
recurrence and a unique invariant probability pi. Standard stopped/localized Dynkin
and Fatou (or the invariant Foster moment theorem) gives

    pi(W) <= C_F/zeta,       pi(t^N) <= C_F/zeta.

Every step was for an arbitrary requested finite t>1. Recognition therefore earns
ALL finite exponential stationary total-count moments. Construction at a particular
t earns the corresponding numerical bound only; the universal statement rests on
the proof that acquisition terminates for every t, not on finitely many tests.

## 7. Why the additional information is genuinely used

The basic four-species example has hubs {C+D}, arms A+B,A+C,A+D, and 2A; take all
rates one except C+D->A+C at two. Complex balance would require a^2=cd, ab=cd,
ac=2cd, ad=cd, which is inconsistent. Pure B/C/D faces are inactive, defeating the
previous leading singleton-support certificate; the complexes have no common
species, defeating literal common-seed stripping.

At (0,n,1,1), R=1, and total internal exit rate is 5 independent of n. The chance
immigration precedes any other jump is lambda/(lambda+5), so first-core up-probability
cannot be O(1/N). A-zero occupation is not simply an immigration wait.

A stronger exact template obstruction holds in the present family. Suppose a
positive profile g_r made t^N g_R satisfy a strict geometric Foster inequality
outside a finite set. On pure-satellite rays R=0 forces g_0>t g_1. On A=1 plus a
large pure satellite, all fast arms preserve R, so the death contribution is
nonnegative and the birth inequality forces g_2<g_1/t. On A=2 plus that satellite,
all arms are again R-neutral and 2A->hubs has total rate 2a. Dropping positive birth
destinations gives a lower bound

    [2a(1-1/t)-lambda/t] g_1 > 0

whenever 2a(t-1)>lambda. Thus the profile-only geometric template is impossible
there. Our vanishing-amplitude active-phase correction supplies an order-one fast
capture drift. This is a representation result, not an instability result, and it
also holds at complex-balanced rate choices.

## 8. Exact boundary: why arbitrary hub matching is not silently included

For a general A-free hub graph one might try R=A+nu(x), where nu is the maximum
integer capacitated matching size. Hub insertion grows nu by at least one; the last
positive activity cannot be erased. But hub removal can decrease nu by TWO.
On the path 1--2--3--4 with all four counts M, nu=2M. Removing one copy each of
vertices 2 and 3 leaves nu=2M-2 (the middle-vertex cover proves the upper bound).
The reverse arm (2+3)->A+X for a free satellite X then DECREASES R by one at rate
kappa M^2 although A=0. This is outside the crucial A-dependent decrement bound.
The biclique condition is a sufficient acquired resource geometry, not a completeness
classification. A missing cross edge, odd cycle, absent amplification edge, uncovered
satellite, other internal reaction, or budget exhaustion means UNKNOWN, not instability.

Ordinary sampled-time/Foster, queueing, Petri-net/siphon, piecewise Lyapunov, and
product-form methods retain credit. The mechanism and code are not a priority claim;
primary comparisons are documented separately. No operational chemistry is provided.
