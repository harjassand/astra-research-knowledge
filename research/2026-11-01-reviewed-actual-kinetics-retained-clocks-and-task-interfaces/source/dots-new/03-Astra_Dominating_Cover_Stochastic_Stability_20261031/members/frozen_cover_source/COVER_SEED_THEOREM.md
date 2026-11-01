# Acquired cover inventories joining slow seed clocks and overlapping fast hubs

**Candidate ordinary mathematical proof; independent review pending.**
All work is mathematical and non-operational. Previously accepted artifacts are
unchanged. No claim of general weak-reversibility stability, arbitrary one-port
stability, historical novelty, efficient numerical constants, or source-process
clearance is made. No external source retrieval is used in this continuation.

## 1. Raw class and the earned graph condition

There are n=m+1 species, m>=2, with distinguished open species A. The only
nonconservative reactions are 0->A and A->0, with rates lambda,mu>0. Every other
nonnull channel joins an A-free square-free binary hub H=X+Y to either 2A or A+Z;
each included channel has its reverse. Each hub has the pair 2A<->H. Every
satellite Z has at least one A+Z<->H arm. No other nonnull channels are allowed.
Duplicate directed channels are summed. Validated null channels can be discarded.
All theorem rates are arbitrary strictly positive real numbers. Exact code uses
positive int/Fraction rates and a rational requested t>1.

Let G=(V,E) be the nonempty simple hub graph on ALL m satellite vertices, including
any satellites absent from hubs. Require:

(D) For every inclusion-minimal vertex cover C and every edge uv with u,v in C,
    each w outside C is adjacent to u or v.

This is acquired from the raw graph, not supplied as a decomposition oracle.
Equivalently, G has neither an induced triangle plus an isolated vertex nor an
induced four-vertex path plus an isolated vertex. To prove equivalence, the
complement I of a minimal cover is a maximal independent set. If uv in C fails
(D), choose w in I adjacent to neither endpoint. Minimality gives neighbors
b in I of u and c in I of v. A common neighbor makes the forbidden triangle;
otherwise, if either cross adjacency exists it also makes a triangle. With no
cross adjacency, b-u-v-c is an induced path. In either case w is isolated in the
indicated induced subgraph. Conversely extend the independent set consisting of
the isolated vertex and the triangle's third vertex, or the path's two endpoints,
to a maximal independent set. Its complementary minimal cover contains the
middle edge, which fails to dominate the isolated vertex.

The forbidden-pattern test is finite and polynomial in the explicit graph size:
inspect all 4- and 5-subsets. The code uses the exact induced degree patterns
[0,2,2,2] and [0,1,1,2,2], each with three edges. The latter is uniquely P4+K1.
This condition contains every disjoint union of bicliques, even with free vertices,
and every complete multipartite graph. It also admits P4 and C5. It is a sufficient
geometric condition here, not a classification of stable graphs or networks.
Ordinary vertex covers, maximal independent sets and graph domination are credited
as standard combinatorial tools; no novelty of their finite characterization is
claimed.

For satellite count vector x, acquire ALL inclusion-minimal structural covers by
explicitly scanning the 2^m subsets, retaining those that cover every edge and have
no removable vertex. Define

    tau(x)=min_C sum_(v in C) x_v,       R=A+tau(x),       N=A+sum_v x_v.

All covers may instead be used; minimal covers attain the same minimum because
weights are nonnegative. Qualitative recognition need not enumerate covers:
this proof is reusable mathematical capital. An explicitly evaluable quantitative
certificate does enumerate them, and charges that acquisition. No matching,
stationary-fiber, Lyapunov, or favorable-cover oracle is a premise.

## 2. Exact inventory geometry and two global combinatorial bounds

Every structural cover meets a hub in one or two vertices. Inserting a hub raises
tau by one or two; removing an enabled hub lowers it by one or two. Removing a
single satellite lowers tau by zero or one. Directly comparing every cover cost
shows that A+X->H changes R by -1,0,+1. The same is true for its reverse; 2A->H
changes R by -1 or 0, and H->2A by 0 or +1. Thus every internal |Delta R|<=1.
Core immigration/death changes R by exactly +1/-1. Always A<=R.

R=0 means A=0 and the satellite support is independent, so all internals are off.
An internal destination contains A or an enabled hub. Consequently {R>=1} is
internally invariant. This is an activity inventory, not a conserved quantity.

At a fixed state call an edge bad if some optimal inclusion-minimal cover contains
both endpoints; call the remaining edges good. Write Q_b,Q_g for the corresponding
sums x_u x_v, and Q=Q_b+Q_g. A good H->2A increases R by exactly one. A bad such
amplification leaves R unchanged. A reverse arm can decrease R only on a bad edge.
For this last assertion, an R-decrease requires tau to decrease by two. A
minimal destination-optimal cover must then have old cost tau, contain both hub
endpoints and omit the arm's returned satellite. If an optimal cover is initially
nonminimal, removing redundant vertices preserves optimality; enabled positive
hub endpoints cannot be removed without contradicting optimality.

Let B={v:x_v>R} and H_B=sum_(v in B)x_v. A vertex in B belongs to no optimal cover.
If H_B>0, condition (D) and any optimal minimal cover witnessing badness of uv give

    Q_g >= H_B min(x_u,x_v),
    x_u x_v <= R min(x_u,x_v),
    Q_b <= |E| R Q_g/H_B.                                      (1)

Indeed every heavy vertex is outside that cover and adjacent to u or v; all edges
incident to heavy vertices are good. The selected incident edges are distinct,
so summing their products proves the first inequality, without independent-event
or average-fiber reasoning. If a bad edge has zero product its bound is trivial.
All nonheavy counts are <=R, hence H_B>=N-nR. In particular, when R<=delta N and
0<delta<=1/(2n), H_B>=N/2 and

    Q_b <= 2|E| delta Q_g.                                      (2)

These bounds hold through cover switches and ties. They do NOT assert Q is always
fast. A P4 can have R=1,Q=1 while its total count diverges.

A second bound holds for every nonempty graph, without (D):

    Q >= tau^2/(4|E|).                                         (3)

Greedily remove pairs on enabled edges until the residual satellite support is
independent. Batch min(endpoint counts) pairs at each choice, so the procedure
terminates after finitely many vertex saturations. Let k_e be the pairs removed
on edge e and K=sum_e k_e. The fully saturated vertices form a cover of the
original graph, since both endpoints of any uncovered edge would retain particles.
Their original total count is <=2K, so tau<=2K. Each x_u x_v>=k_e^2. Cauchy's
inequality now gives Q>=sum k_e^2>=K^2/|E|>=tau^2/(4|E|). Zero-count vertices
cause no problem and can be included as saturated vertices.

The graph condition is sharp for this particular small-cone absorption mechanism,
not for stability. If an induced triangle plus isolate exists, put one particle at
each triangle vertex, N particles at the isolate, and zero elsewhere. Then A=0,
R=2, Q_b=3 and Q_g=0. If an induced P4 plus isolate exists, put one particle at
each path vertex and N at the isolate. Then R=2, Q_b=1 (the middle edge), Q_g=2.
Covers of either induced graph extend to full-graph covers by adding zero-weight
outside vertices; removing redundant vertices preserves the positive-weight
minimizers. Thus these exact values remain valid in any graph containing the
induced pattern. As N tends to infinity neither state permits a uniform bound
Q_b<=C(R/N)Q_g with fixed finite C. Unit-rate reversible networks on both graphs
remain ordinary detailed-balanced stable controls. This is a representation and
rate-comparison boundary, never a stability counterexample.

Finally, an arm consuming a heavy X has Delta R>=0. For any cover excluding X,
its weight rises at least one; for a cover including X, its old weight is at least
tau+1 and its change is nonnegative. Thus the new minimum is at least tau+1.
Such arms consume A while never decreasing R and have aggregate rate at least
k_- A H_B. An R-decreasing forward arm can only consume a nonheavy satellite;
its total rate, together with 2A->H, is bounded below in Section 3.

## 3. Raw rate summaries and a finite acquired profile

Write a=sum_H rate(2A->H); b_H=rate(H->2A); s_H=sum of all reverse-from-hub rates,
including b_H. Let k_X=sum_H rate(A+X->H). Set

    k_-=min_X k_X, k_+=max_X k_X, b_-=min_H b_H, s_+=max_H s_H,
    S=sum of all internal rate constants, F=2a+k_+,
    b0=min_H(s_H+b_H), K_f=a+m k_+, beta=b_-/(16|E|).

All are acquired by finite raw scans. R-decreasing forward channels have total
rate <=K_f A R: 2A gives a A(A-1)<=a A R, and every decreasing arm consumes a
satellite of count <=R, with at most m such types. Other forward channels have
nonpositive drift for any decreasing function of R. The same potentially adverse
forward set has rate <=K_f R^2.

Fix arbitrary t>1 and define

    L=lambda(t-1), epsilon0=min(1,(lambda+beta)/2),
    c=4(L+epsilon0)/beta, K=max(2,ceil(2c)).

For r>=K let g_r=1+c/r. For r=K-1,...,1 acquire backwards

    g_r=[(lambda*t+beta*r^2)/(lambda+beta*r^2-epsilon0)] g_(r+1),
    g_0=2t g_1.                                                (4)

Every denominator is positive; g decreases strictly to one. With d_r=g_r-g_(r+1),
for every r>=1,

    lambda(t g_(r+1)-g_r)-beta r^2 d_r <= -epsilon0 g_r.         (5)

For r<K it is equality. On the tail c/r<=1/2, r/(r+1)>=1/2 give an upper bound
L+L/2-beta*c/2=-L/2-2epsilon0<=-epsilon0(1+c/r).
The finite head and explicit tail also acquire

    d_*=min(c,min_(1<=r<K)(r+1)^2 d_r)>0,
    G_*=max(3,max_(1<=r<=K) d_(r-1)/d_r).                       (6)

Thus (r+1)^2 d_r>=d_* and d_(r-1)/d_r<=G_* for all r>=1. For r>=K+1 the ratio is
(r+1)/(r-1)<=3. This is the paid compatibility constant for overlap-induced bad
hub moves; it is not assumed rate-independent.

## 4. Oppositely signed phase corrections and acyclic acquisition

Put D=mu(1-1/t)>0 and choose

    epsilon=min(1/4, D/[4(F+D)], epsilon0/[4mu]),
    J=max(K+1,2,ceil(4c(mu+K_f+beta)/D)),
    E_r=mu(t^(-1)g_(r-1)-g_r)+K_f r d_(r-1)+2beta r d_r,
    q=1+max_(1<=r<J) 4(r+1)^2 max(E_r+epsilon(F+D),0)/k_-.      (7)

For r>=J, neighboring profile values lie in the rational tail and

    E_r <= -D+2c(mu+K_f+beta)/r <= -D/2,
    E_r+epsilon(F+D)<=-D/4.                                  (8)

The finite maximum in (7) handles every low-inventory extinction layer. Define

    delta=min(1/(2n),1/(2|E|),b_-/[8|E|s_+G_*]),
    C_core=12lambda*t+12mu, C_e=11K_f+C_core,
    C_int=2L+2mu+(2c+11)S/delta^2+C_core,
    kappa=min(D delta/4,epsilon b0 delta^2/(32|E|)),
    N_*=ceil max(1,q,K/delta,88q s_+/(b_-d_*),
                  4q C_e/epsilon0,(C_int+1)/kappa).            (9)

These definitions have no circular compatibility condition: raw graph/rates give
beta and profile; that gives d_*,G_*; then epsilon,J,q; then delta and N_*.
The potentially huge finite loop and rational arithmetic are charged. In particular,
there is no polynomial-bit numerical-acquisition assertion for this construction.

For every count state set

    f=A/(R+1)^2,
    h=g_R+q f/(N+1)-epsilon A/(N+1),      W=t^N h.              (10)

At R=0 both phase terms vanish. Always

    3/4<=h<=H:=g_0+q/4.                                      (11)

The positive correction rewards rapid capture when seeds are few; the negative
correction rewards activation when seeds form a macroscopic fraction. Neither is
a substitute for physical death, and they are not incorrectly combined into one
R-only function.

## 5. Exact generator estimates, including every last-copy death

Each internal jump has |Delta A|<=2 and |Delta R|<=1. For r=R>=1, A<=r and direct
subtraction yield

    |Delta f|<=11/(r+1)^2.                                   (12)

For a decrement use 2/r^2+r[1/r^2-1/(r+1)^2]<=11/(r+1)^2; increments are smaller.
The allowed core destination r=0 is also covered. A heavy-consuming arm decreases
f by at least 1/(r+1)^2. Every other forward arm with nondecreasing R has nonpositive
f drift. Therefore, whenever H_B is as defined above,

    L_int f <= -k_- A H_B/(r+1)^2
               +11K_f r^2/(r+1)^2+11s_+ Q/(r+1)^2.           (13)

The base profile satisfies

    L_int g_R <= K_f A r d_(r-1)+s_+ Q_b d_(r-1)-b_- Q_g d_r. (14)

Neutral amplification is dropped, adverse reverse arms are explicitly retained,
and all good amplifications are credited. No last-copy death is removed.

For the positive phase's whole physical core generator, direct denominator
subtraction gives the deliberately enlarged bound

    t^(-N)L_core[t^N q f/(N+1)]<=q C_core/(N+1).               (15)

Birth is bounded by q lambda[11t+(t-1)/4]/(N+1). For death at A>=1, N>=1,
write the scaled increment as t^(-1)(f'-f)/N+
 f[t^(-1)/N-1/(N+1)]. The first positive term is <=11q mu/(4N), using
A/(r+1)^2<=1/4; conversion to N+1 costs at most two. The second is at most
q mu A^2/[N(r+1)^2(N+1)]<=q mu/[4(N+1)] using A<=N. Thus a bound
6q mu/(N+1), and hence the displayed 12q mu/(N+1), is valid. Actual death
at A=1, including seed extinction, remains in this estimate and in the g term.

For the negative phase the exact internal A-generator is

    L_int A=-2a A(A-1)-A sum_X k_X x_X+sum_H(s_H+b_H)x_u x_v,

so

    L_int[-epsilon A/(N+1)]
       <=epsilon F A-epsilon b0 Q/(N+1).                    (16)

Birth's scaled negative-phase contribution is nonpositive. Death contributes
at most epsilon D A+epsilon mu: indeed
 A/(N+1)-(A-1)/N=(N+1-A)/[N(N+1)]<=1/N,
and multiply by A<=N. Hence the complete negative-phase contribution is at most

    epsilon(F+D)A+epsilon mu-epsilon b0 Q/(N+1).              (17)

This keeps the true D=mu(1-1/t) as t decreases to one and charges all positive
lambda(t-1) costs in the base profile. The estimates are uniform for every fixed
t>1 and every positive rate ratio.

## 6. Boundary cone: bad overlapping hubs are actually paid

Let N>=N_* and 1<=r<=delta N. By (1)-(2) and (9),

    Q_b<=Q_g,       s_+ Q_b d_(r-1)<=b_- Q_g d_r/4.

The reverse part of the positive phase obeys

    11q s_+ Q/[(N+1)(r+1)^2]
       <=22q s_+ Q_g/[(N+1)(r+1)^2]<=b_-Q_g d_r/4.

Thus at least b_-Q_g d_r/2 remains from (14). Since Q_g>=Q/2, (3) yields

    (b_-/2)Q_g d_r>=beta(r-A)^2 d_r.

Adding exact core drift of g, (5), (13), (15), (17), and
r^2-(r-A)^2<=2rA now gives

    t^(-N)LW <= -epsilon0 g_r+A[E_r+epsilon(F+D)]
        -q k_- A H_B/[(N+1)(r+1)^2]+q C_e/(N+1)+epsilon mu
        -epsilon b0 Q/(N+1).                                (18)

Here H_B>=N/2, so H_B/(N+1)>=1/4. If r<J, (7) pays the entire positive A term;
if r>=J, (8) lets it be dropped. The two constant errors are each <=epsilon0/4.
Therefore (18)<=-epsilon0 g_r/2. Because N+1>=q,
h<=g_r+1/4<=2g_r, and LW<=-epsilon0 W/4 on the whole boundary cone.

This is where the P4 obstruction is resolved: matching-loss events can occur at
small R, but their actual rate is absorbed by other good hubs, with the profile
slope ratio and all rate constants explicitly charged. No assumption that bad
loss requires large R, or that every active latent state has a fast clock, is used.

## 7. Interior: physical activation supplies linear restoration

Suppose N>=N_* and r>delta N. Then r>K and all r-1,r,r+1 profile values lie in the
rational tail. Thus every internal |Delta g|<=2c/r^2, so L_int g<=2c S/delta^2.
By (12), the positive phase's internal drift is <=11q S/[delta^2(N+1)]<=11S/delta^2.
Its core drift is <=C_core. For the base profile's core drift,

    lambda(tg_(r+1)-g_r)<=3L/2,
    mu A(t^(-1)g_(r-1)-g_r)<=-D A+mu/2,

since c/(r-1)<=c/K<=1/2. Combine these with (17),
epsilon(F+D)<=D/4 and epsilon<=1/4 to obtain the enlarged bound

    t^(-N)LW<=C_int-(D/2)A-epsilon b0 Q/(N+1).                (19)

If A>=r/2, death pays at least D delta N/4. Otherwise tau=r-A>delta N/2;
(3) and N^2/(N+1)>=N/2 imply the activation term pays at least
epsilon b0 delta^2 N/(32|E|). In either case (19)<=C_int-kappa N<=-1.
Here g_r<=3/2 and q/(N+1)<=1, so h<=7/4<2. Consequently LW<=-W/2.

If r=0, only immigration is enabled. Its exact scaled drift is

    lambda(tg_1-g_0)+q lambda*t/[4(N+2)]-epsilon lambda*t/(N+2)
       <=-lambda g_0/2+q lambda*t/[4(N+2)]<=-lambda g_0/4,

using N+1>=q and g_0>=2t. Since h=g_0, all three regions join to

    LW<=-zeta W outside {N<N_*},      zeta=min(epsilon0,lambda)/4. (20)

## 8. Finite head, nonexplosion, irreducibility and stationary receiving

Retain the factored constant

    C_F=(zeta+lambda+mu N_*+S N_*^2) H t^(N_*+1).              (21)

Every head state's total outgoing rate is bounded by lambda+mu N_*+S N_*^2,
and every destination has total count at most N_*+1. Equations (11),(20) give
LW<=-zeta W+C_F 1_{N<N_*}. No head enumeration or exponential power expansion
is needed to store this valid symbolic constant; neither operation is claimed cheap.
The number of head states is binomial(N_*+n-1,n), not an executed search.

N(s)<=N(0)+Poisson(lambda s) pathwise, so finite-time trajectories stay in finite
count sublevels and explosion is impossible. For each satellite an acquired arm
provides the reversible singleton path 0->A->2A->H->A+X->X. Nonnegative translated
paths preserve enabling, so the full orthant is irreducible. This is not a claimed
irreducibility of an uninspected finite fiber.

Localized integrating-factor Dynkin and Fatou give
E_x W(X_s)<=exp(-zeta s)W(x)+C_F/zeta. Finite-horizon integrability also follows
from W<=H t^N and the Poisson bound, including polynomial total propensities.
Normlikeness makes occupation averages tight; the usual finite-state localization
argument yields a unique invariant probability and positive recurrence. Fatou on
occupation averages gives pi(W)<=C_F/zeta and, using h>=3/4,

    pi(t^N)<=2 C_F/zeta.                                      (22)

Since construction succeeds mathematically for each finite t>1, all finite
exponential stationary total-count moments follow. Standard Foster/occupation
and finite-jump methods are components, not new claims in themselves.

## 9. Acquisition semantics, costs, and ordinary comparisons

Successful raw recognition of (D) already proves qualitative recurrence and all
finite exponential moments by this theorem. The qualitative interface does not
materialize covers, g, q, N_*, powers or a stationary law. This is a finite theorem
application, not an unexplained helpful-function oracle. Unsupported structure is
stability UNKNOWN; failed graph recognition is not evidence of instability.

For a requested explicit certificate, the implemented constructor charges 2^m
cover masks, K-1 backwards recurrence steps, J-1 finite compensation checks, and
all exact rational arithmetic. A budgeted refusal says UNKNOWN_NUMERICAL_BUDGET
while retaining the independent qualitative conclusion. These two loop budgets
are not a bit-cost, memory or hostile-input service cap. The implementation is a
trusted research API; same-implementation reconstruction is not an independent
validator. Powers stay factored; all constants may be enormous. No polynomial-bit
explicit quantitative claim from the earlier multipartite theorem transfers here.

The unit-rate reversible network is detailed-balanced at all species concentrations
one, so ordinary product form wins even on graphs excluded by (D). The diagnostic
P4 has hubs BC,CD,DE; amplification pairs to 2A; and arms AB<->BC, AC<->CD,
AD<->DE, AE<->CD. Rates are one except CD->AE has rate two. Its internal complex
graph is a tree, so complex balance forces edge-by-edge balance. Amplification
requires bc=cd=de=a^2. The AB,AC,AD leaves force b=c=d=a, hence e=a; the perturbed
AE leaf instead requires ae=2cd, a contradiction. This is a non-complex-balanced
fixture, not a proof that every strong ordinary theorem is inapplicable.

For the same P4, pure satellite faces fail leading singleton support; no literal
common species factor is shared by all complexes. At (A,B,C,D,E)=(0,M,1,1,M),
R=2 and the middle hub's reverse arm can decrease R, while endpoint hub activity
is order M. At (0,1,1,0,N), R=1,Q=1 and the latent clock is genuinely slow.
Both facts are retained, not erased by a parser extension. The present proof earns
how their different mechanisms fit, rather than assuming a uniform fast fiber.

The stronger ordinary recurrence literature retains the previously documented
bounded comparison and access limitations. No denied source is fetched or replaced
by another transfer; the prior source-process failure remains disclosed and
quarantined. No exhaustive novelty or general weak-reversibility conclusion follows.
