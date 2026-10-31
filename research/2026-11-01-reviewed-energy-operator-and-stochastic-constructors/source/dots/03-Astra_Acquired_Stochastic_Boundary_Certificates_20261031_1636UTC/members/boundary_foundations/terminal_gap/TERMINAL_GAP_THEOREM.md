# A finite, acquired terminal-gap certificate for stochastic recurrence

31 October 2026. Mathematical, non-operational count-process work only.

## Result and exact scope

The construction below takes a **finite raw reaction list**, not a supplied Lyapunov
function, grouping, face decomposition, or stationary distribution. It computes
strongly connected components, exact rational cone certificates, and an executable
finite-episode selector. A successful certificate proves nonexplosion and positive
recurrence on every nonabsorbing reachable class, for **every fixed positive rate
vector**. It also implies finite stationary mean total jump intensity.

This is a sufficient condition, not a complete recurrence algorithm. It rejects
some elementary complex-balanced stable networks. It does not solve general weak
reversibility, prove exponential moments, establish a mixing rate, give an efficient
finite exceptional-radius bound, or establish novelty. The statewise selector is
actually implemented; no generic finite-head/radius acquisition is claimed here.

The marked-target potential and its path recursion are closely based on Sections
3–7 of Alec Kriebel's August 2026 **unrefereed** preprint, version 1.2.4. Those
arguments are reconstructed below, rather than importing the preprint's claimed
whole theorem. Our additional sufficient condition is a finite, rate-independent,
boundary-sensitive cone test that ensures a rare terminal is reachable **inside the
currently carried linkage class**, including multiple linkage classes and arbitrary
finite molecularity. Historical priority for this condition is not established.

## 1. Input, notation, and the certificate

Let a finite reaction list consist of channels r: s_r -> u_r in N^d, with fixed
positive rates k_r. Drop channels s_r=u_r; they do not change the population CTMC.
For a state x, let

    (x)_s = product_i x_i!/(x_i-s_i)! if x>=s, and 0 otherwise,
    lambda_r(x)=k_r (x)_(s_r),
    Lambda(x)=sum_r lambda_r(x).

Parallel channels can be combined when BOTH endpoints agree. Distinct sources with
the same displacement must not be combined. The reaction graph must be weakly
reversible: each of its undirected components is strongly connected. Thus every
complex in the reduced graph is a source. Let C be its complexes, L its linkage
classes, and

    S = span_R {u_r-s_r}.

For every nonempty I subset {1,...,d}, put O=I^c. Call I *admissible* if

    there is v in S with v_i>=1 for i in I and v_i=0 for i in O.       (1)

The normalization 1 loses nothing: strict positivity on the finite set I can be
rescaled. Both feasibility and infeasibility of (1) have finite rational witnesses.
An infeasibility witness is an invariant ell annihilating every reaction vector,
with ell_i>=0 on I and sum_(i in I) ell_i>0; signs outside I are unrestricted.
Indeed ell.v would then be strictly positive, contradicting ell annihilating S.
The converse is the finite-dimensional theorem of alternatives.

For every admissible I and every linkage L, form the finite pair set

    P(I,L) = {(s,c): s in C, c in L, s_i<=c_i for every i in O}.       (2)

The source s need NOT belong to L. The terminal c MUST belong to L. Require
nonnegative rational coefficients alpha_(s,c) such that

    g_i := sum_((s,c) in P(I,L)) alpha_(s,c)(s_i-c_i) >= 1
    for every i in I.                                               (3)

A certificate consists of an excluding invariant for every inadmissible I, and
coefficients (3) for every linkage of every remaining I. A verifier checks only
raw endpoints, strongly connected components, exact sums, signs, and coverage of
all subsets. It does not call an LP solver or trust a numerical feasibility flag.

Equivalent dual obstruction: (3) is infeasible iff there is w_i>=0 on I,
sum_i w_i=1, with

    sum_(i in I) w_i(s_i-c_i)<=0 for every (s,c) in P(I,L).            (4)

This is a finite cone alternative, not a characterization of recurrence. A
rejection with (4) says only that this sufficient construction did not succeed.

### Acquired search and its cost

`exact_terminal_gap.py` computes SCCs and solves the rational systems by exhaustive
basis enumeration using `fractions.Fraction`. It uses no numerical solver. To
solve Bz=b,z>=0, it selects independent rows, enumerates rank(B)-column bases,
solves exactly, and checks the full equations and all signs. A feasible standard-
form system has such a basic feasible solution: its nonempty polyhedron contains
no line because z>=0. If b is outside the column span, the full-equation check
rejects every basis. Thus enumeration is complete for the finite LP being tested.

For (3), the columns are (s-c)_I and -e_i, and b is the all-ones vector. If there
are p pairs, at most binomial(p+|I|,|I|) bases are tested. There are at most
(2^d-1)*number_of_linkages such tests, plus admissibility/invariant tests. All
rational arithmetic and its actual bit growth are charged. No polynomial-time
claim in species number or graph size is made. The output records exact counts
of tested bases. The verifier is much cheaper than this deliberately simple
complete finder.

## 2. State communication and the marked process

An enabled reaction s->u from x=rho+s has a population return path. Choose a
directed complex path u=z_0 -> z_1 -> ... -> z_m=s in its linkage. The populations
rho+z_j realize it, because each designated source z_j is present. Therefore every
population transition can be reversed by an enabled finite path. Every reachable
set Gamma is a closed communicating class.

Finite nonabsorbing classes are trivially nonexplosive and positive recurrent;
absorbing singletons carry point masses. Fix an infinite nonabsorbing Gamma.
Construct the embedded jump chain first, independently of holding times, selecting
channel r with probability lambda_r(x)/Lambda(x). After a jump, retain its actual
target t. A marked state (x,t) always has x>=t. If s->u fires next,

    (x,t) -> (x-s+u,u).

The marked chain on all marked states obtainable within Gamma is irreducible.
Indeed any desired marked endpoint has a witnessing last channel and predecessor;
population irreducibility takes the current population to that predecessor, after
which the last channel supplies the desired mark. Every population in Gamma has a
reachable mark, by a positive-length return path.

Put rho=x-t and

    V(x,t)=sum_i log((x_i-t_i)!)=sum_i log(rho_i!).                   (5)

V is nonnegative and has finite sublevel sets. Direct factorial cancellation gives

    V(x-s+u,u)-V(x,t)=log[(x)_t/(x)_s].                             (6)

In particular, following a channel whose source is exactly the carried target has
zero increment. This exact identity does not require binary molecularity.

Let kbar_s be the sum of channel rates out of source s, and set

    p_x(s)=kbar_s (x)_s/Lambda(x).

At an enabled carried target t, the expected ordinary-jump reward is

    delta(x,t)=sum_s p_x(s) log[(x)_t/(x)_s]
              = log p_x(t) - sum_s p_x(s)log p_x(s)
                +sum_s p_x(s)log kbar_s-log kbar_t
              <= log p_x(t)+C0,                                  (7)

where C0=log|C|+log(max kbar/min kbar), and disabled sources contribute zero.

## 3. Finite episodes and propagation of rare-terminal drift

For each t,c in the same linkage, acquire a simple directed path

    t=y_0 -> y_1 -> ... -> y_m=c.

A (t,c)-episode follows the exact designated channel while it fires; it stops
immediately after any other channel. On reaching c it takes one ordinary jump and
stops. It uses between one and M=|C| genuine jumps. Along designated edges the
residual remains rho, and the populations are rho+y_j.

Write q_j=k_(y_j->y_(j+1))/kbar_(y_j)>0 and
p_j=p_(rho+y_j)(y_j). The expected remaining reward satisfies EXACTLY

    J_m=delta(rho+c,c),
    J_j=delta(rho+y_j,y_j)+q_j p_j J_(j+1).                         (8)

Continuation has probability q_j p_j; its immediate increment is zero by (6).
There is no discarded mismatch cost: the ordinary-jump delta includes it.

For a real upper bound H on J_(j+1), (7) bounds J_j by

    F_q(H)=sup_(0<p<=1) [log p+C0+qpH]
          = C0+qH,                    H>=-1/q,
          = C0-1-log(-qH),             H<-1/q.                      (9)

This follows by differentiation of a strictly concave scalar function. F_q is
nondecreasing and tends to -infinity when H does. Consequently, if for a sequence
of residuals p_(rho+c)(c)->0, the reward of the entire fixed path to c tends to
-infinity, whatever the intermediate probability scales do. Path length and all
rates are fixed in this statement. No uncharged lower bound on path success is
assumed.

## 4. Why the acquired cones supply the terminal

Suppose a sequence of marked states (x^(n),t^(n)) in the same marked communicating
class leaves every finite set. Extract a subsequence with fixed target t. Then
extract so that every coordinate of rho^(n)=x^(n)-t is either a fixed integer or
tends to infinity. Let I be the nonempty set of divergent coordinates.

I is admissible in (1). To see this without any reachability oracle, choose two
sufficiently separated points of the subsequence so that every I coordinate
strictly increases. Their difference lies in S, vanishes outside I, and is
strictly positive on I. Rescale it to obtain (1).

Set R_n=sum_(i in I) log(rho_i^(n)+1). After extracting again,

    w_i=lim log(rho_i^(n)+1)/R_n for i in I,
    w_i=0 for i outside I.

Thus w>=0 and sum_i w_i=1. A coordinate may diverge while w_i=0; it remains in I.
For any fixed enabled source s and fixed added complex c,

    log((rho^(n)+c)_s)=R_n w.s+o(R_n).                             (10)

This holds at arbitrary finite molecularity: every fixed number of falling
factors in a divergent coordinate contributes log(rho_i+1)+o(R_n), and each
enabled bounded coordinate contributes O(1).

Let L be the linkage of the fixed target t. By (3),

    sum_(s,c) alpha_(s,c) w.(s-c)=sum_(i in I) w_i g_i>=1.

Therefore at least one fixed pair (s,c) has w.(s-c)>0. The source s is eventually
enabled at rho^(n)+c: in I there are arbitrarily many particles, and outside I
(2) guarantees s_i<=c_i<=rho_i^(n)+c_i. The terminal c is always enabled there.
By (10),

    (rho^(n)+c)_s/(rho^(n)+c)_c -> infinity,
    p_(rho^(n)+c)(c) <= (kbar_c/kbar_s)
                         (rho^(n)+c)_c/(rho^(n)+c)_s -> 0.          (11)

Crucially c lies in L, so the acquired path from t to c exists. Equations (8)–(9)
now force this entire episode reward to tend to -infinity.

It follows that for every fixed B>0 the set

    K_B={(x,t) in marked Gamma: min_(c in linkage(t)) J_c(x,t)>-B}   (12)

is finite. Otherwise an escaping sequence in it would contradict (11). This is a
qualitative compactness argument, not an executed finite-radius bound.

## 5. An actual selector without an exceptional-set oracle

For positive RATIONAL rates, every episode reward is a rational linear combination
of logarithms of positive rational numbers, obtained by (6)–(8). It can be
computed to any prescribed absolute accuracy. No finite K_B is needed to operate
the selector: approximate every J_c to absolute error <=1/8, and choose a terminal
with smallest approximate value. Its true reward is at most min_c J_c+1/4.
Thus outside the finite K_1, its reward is <=-3/4, in particular <=-1/2.

`select_episode.py` implements this operation, not merely a call to an ideal log
oracle. For 1<=z<=2 and t=(z-1)/(z+1),

    log z = 2 sum_(j=0)^(N-1) t^(2j+1)/(2j+1) + R_N,
    0<=R_N<=2 t^(2N+1)/[(2N+1)(1-t^2)].                           (13)

Rational range reduction writes q=2^k z and uses the same formula for log 2.
The positive geometric remainder is evaluated exactly; signed multiplication by
k is interval-safe. Every phase delta interval has width at most 1/(8M), so
backwards recursion, whose multipliers lie in [0,1], gives episode width <=1/8.
The code rounds final intervals outward to denominator 2^24, retaining width
<=1/4, and chooses by their unrounded rational midpoints. All graph searches,
rate evaluations, series terms and actual rational bit growth are charged in its
output. The general theorem for arbitrary fixed positive real rates only needs
the mathematical minimizing selector; the effective implementation contract is
rational rates.

## 6. Embedded positive recurrence, nonexplosion, and physical time

Choose the implemented selector for rational rates, or a mathematical minimizer
for arbitrary positive rates. There is a finite nonempty K outside which the
selected episode drift is <=-1/2. Nonemptiness can also be assured by adding any
one marked state. Each episode uses <=M jumps and changes each coordinate by a
bounded amount. Stop the episode-endpoint chain Y at its first visit sigma to K.
Then

    V(Y_(n wedge sigma))+(n wedge sigma)/2

is a nonnegative supermartingale. All finite-n expectations are legitimate:
after at most nM jumps, every coordinate is bounded by its initial value plus a
fixed multiple of nM. Hence

    E_z sigma<=2V(z),
    E_z[number of original jumps until K is reached]<=2M V(z).     (14)

The endpoint chain need not be irreducible. We use irreducibility only of the
ORIGINAL marked chain. From a state of K take one ordinary jump. It has finitely
many successors, each with finite expected time back to K by (14). Therefore the
original marked chain's first-positive-return jump count to K has finite mean
from every k in K. Their maximum B_K is finite.

The trace of the original marked chain on finite K is irreducible: every finite
marked path between K states induces a trace path. Choose k_* in K. Finite
irreducibility supplies a common number of trace steps and a common positive
success probability to hit k_* from every trace state. Successive blocks give a
geometric bound on its positive trace return count T, so E T<infinity. By the
strong Markov property and Tonelli, expected original jump count for this return
is at most B_K E T. Thus the original marked embedded chain is positive
recurrent. Projection gives finite expected positive return count to the
population coordinate x_* of k_*.

Construct physical holding times now. The embedded chain returns to x_* infinitely
often almost surely. The holding times at successive such visits are independent
exponentials with the same finite positive rate Lambda(x_*). Their sum diverges
almost surely, ruling out explosion. Also every nonabsorbing state has an enabled
channel, whose integer falling-factorial factor is >=1. Thus

    Lambda(x)>=k_min:=min_r k_r>0.

The expected physical return time to x_* is at most its finite expected jump
return count divided by k_min. The minimal CTMC is therefore nonexplosive and
positive recurrent. Irreducibility gives the conclusion throughout Gamma.

### Finite stationary mean activity, and no stronger moment claim

Let mu be the embedded population chain's invariant probability and
Z=sum_x mu(x)/Lambda(x). Then 0<Z<=1/k_min, and

    pi(x)=mu(x)/(Z Lambda(x))

is the physical invariant probability (equivalently the regenerative occupation
formula). Consequently

    E_pi Lambda(X)=1/Z<infinity.                                  (15)

This is finite total stationary jump intensity, not a universal exponential
count-moment bound. The code does not compute pi or Z.

## 7. An interpretable binary corollary and its prior-art boundary

Suppose the network is bimolecular and EVERY linkage has stoichiometric span S,
the span of the entire network. Then the cone criterion succeeds.

Here is a self-contained proof. If it failed for an admissible I and linkage L,
(4) would give a normalized w. Apply the following binary top-complex argument
inside L. Set h(y)=w.y and let T be its maximizers.

* If all complexes have equal h, w annihilates the linkage span, hence S. This
  contradicts (1), because w.v>0.
* If a top complex has two particles in I, it is enabled over every terminal c
  outside T; it supplies the forbidden strict pair gap.
* Otherwise every top complex has exactly one I particle and possibly one
  outside-I companion. Let J be the I species appearing in top complexes. Each
  has weight h_max>0, no complex has two J particles, and top complexes are
  precisely those with one J particle. A unary top complex is enabled over every
  lower c and gives a strict gap. A binary top i+D is enabled over any lower c
  containing its outside-I companion D and also gives a strict gap. If neither
  case occurs, the signed functional

      ell(x)=sum_(i in J) x_i-sum_(D a top companion) x_D

  vanishes on every complex of L. It annihilates the linkage span S. But ell.v>0
  for v in (1), since companions are outside I, again a contradiction.

This exhausts binary complexes. The common-span graph condition is NOT new:
Gopalkrishnan–Miller–Shiu already use it as a sufficient condition for strong
endotacticity. Strong endotacticity by itself does not establish stochastic
recurrence. No priority claim is made for this stochastic corollary either.

## 8. Executed three-species, multiple-linkage, non-complex-balanced test

Use two directed cycles of abstract count symbols A,B,C:

    0 -> A+B -> A+C -> B+C -> 0,
    A -> B -> C -> 2A -> A.

All rates are 1 except 2A->A, whose rate is 2. The two linkage classes are disjoint
and each has stoichiometric span R^3. For the first, the three mixed complexes
are linearly independent (determinant -2). For the second, differences from A
include B-A, C-A, and A, which span R^3. Thus the corollary applies, and the raw
finder independently acquires all fourteen face/linkage certificates.

There is NO positive complex-balanced concentration. Complex balance on the first
unit-rate directed cycle forces ab=ac=bc=1, hence a=b=c=1. At this point the second
cycle has outgoing flux 2 from 2A but incoming flux 1 from C. Contradiction. This
is an algebraic non-complex-balance check, not simulation evidence.

This example is not double-full (2B and 2C are absent), has no unary outflow,
and has three species. These distinctions delimit comparison; they do not
establish historical novelty or practical advantage.

## 9. Exact architecture failure and an infinite-fiber repair

Consider the stable unit-rate network

    0 <-> A,     2A <-> A+B.                                      (16)

Its product-Poisson(1,1) law obeys detailed balance. The geometric finder correctly
REJECTS it: with I={A,B}, current linkage {2A,A+B}, and w=(1/2,1/2), every source
has total molecularity <=2 while both terminals have total molecularity 2.
Therefore every pair gap in (4) is nonpositive.

The failure is more than a loose proof estimate. Choose residual rho=(n,n), n>=1,
and carried target 2A. The only target-following phases are

    ((n+2,n),2A),      ((n+1,n+1),A+B).

For the ordered sources (0,A,2A,A+B), the exact factorial ratios in (6) are,
respectively, with a=n+2 in the first row and a=n+1 in the second,

    a(a-1), a-1, 1, (n+1)/n;
    a^2,    a,   a/(a-1), 1.

Every ratio is >=1. Designated jumps have reward zero, and every final ordinary
jump has positive expected reward. Hence EVERY finite target-following episode
confined to that current linkage has positive expected reward at these reachable
states, even if arbitrarily longer designated paths are allowed. The obstruction
is architectural, not an unstable process.

An explicit infinite-fiber correction repairs (16). Let N=a+b, let h(a)=H_(a-1)
for a>=1 and h(0)=0, and define

    W(a,b)=N-h(a)/2+(N/4)1{a=0}.                                (17)

Since H_(a-1)<=a-1, W>=N/2. The quadratic fast generator F obeys
Fh=N-2a for a>=2, by telescoping harmonic differences. Direct calculation gives

    LW=1-N/4,                                     a=0;
    LW=-(N+1)/4,                                  a=1;
    LW=1-N/2-1/(2a)+a/[2(a-1)] <=2-N/2,            a>=2.

Thus LW<=2-N/4 everywhere. The boundary spike at a=0 is essential: without it
the whole empty-A axis has positive drift 1. This is an explicit correction on an
unbounded conservative fast fiber, not a finite-state or stationary oracle.
It is useful evidence for a next mechanism, not a new recurrence result for a
network whose stationary law is already known.

## 10. Reproduction, evidence and limitations

Run in this directory:

    python exact_terminal_gap.py > results.json
    python select_episode.py > selector_results.json

The first run performs exact acquired cone certification, independent verification,
rejection/tamper checks, 1,024 exact factorial-ratio comparisons, and 4,225 exact
rational harmonic-generator identity checks. The generator identities above are
proved for all counts; the grid only checks code consistency. It also checks a
finite conservative class and the higher-molecularity example 0<->3A.

The second run executes five certified selectors on the non-CB three-species
network, including a 10^100 interior population and empty-coordinate boundaries.
It records real arithmetic work. The 10^100 case currently produces an interval
near -3.6841 with 23,318-bit intermediate final fractions before outward rounding;
it is NOT a claim that this is a smallest exceptional radius. Smaller interior
states can still have small or positive selected drift.

No source files were uploaded, no publication or outside communication occurred,
and no chemical/biological operation is implied. No denied Wisconsin full-PDF
source was retried or fetched through another transfer route. Search-visible
bibliographic context is separate from mathematical premises.

### Primary-source pointers

* Alec Kriebel, *Positive Recurrence for Single-Linkage Bimolecular Weakly
  Reversible Stochastic Reaction Networks*, unrefereed preprint v1.2.4:
  https://aleckriebel.com/research/positive-recurrence-bimolecular-reaction-networks/paper-v1.2.4.pdf
  — exact marked-target identity and finite path mechanism reconstructed above.
* Gopalkrishnan, Miller, Shiu, *A geometric approach to the Global Attractor
  Conjecture*, Corollary 3.19: common linkage span implies strong endotacticity;
  the geometric graph property is established prior work.
* Anderson, Cappelletti, Kim, Nguyen, *Tier structure of strongly endotactic
  reaction networks*, Stochastic Processes and their Applications 130 (2020),
  DOI 10.1016/j.spa.2020.07.012 — official abstract/search-visible Section 7 gives
  a more restricted binary stochastic recurrence criterion with all outflows;
  its previously inaccessible full PDF was not obtained here.
* ConStRAINeD project publications, https://constrained.polito.it/publications/:
  an all-two-species weak-reversibility recurrence result is announced as in
  preparation, not used here as an inspected proof or as a novelty baseline.
