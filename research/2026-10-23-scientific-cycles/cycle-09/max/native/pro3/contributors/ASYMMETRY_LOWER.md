# A bounded native edge asymmetry can accumulate across finitely many levels

Contributor: Astra PRO3 Cycle8 lower construction. Date: 22 October 2026.
This is a source-bound mathematical contribution to the principal's current
asymmetry-budget theorem. It does not claim an exact minimax floor, an exact
moving-policy TV limit, external acceptance, or a practical sampler advantage.
The predecessor files listed in the accompanying receipt were read unchanged.

## 1. Statement and scope

Fix K>0, alpha in (0,1), and beta=1-alpha. At horizon n let the public policy
satisfy 0<eta_n<1, 0<=kappa_n<infinity, and 0<=A_n<infinity. These parameters
stay fixed throughout the run. Write

\[
 \delta_n=\kappa_n-\eta_n,\qquad
 D_n=|\delta_n|A_n,\qquad \ell_n=\log n.
\]

The native class consists of finite positive pi,q, one population
D(pi||q)<=K, proposal-q independence Metropolis-Hastings G, and fixed
target-independent row-stochastic Q with reciprocal support and

\[
 \max_{x\ne y:Q_{xy}>0}|\log(Q_{yx}/Q_{xy})|\le A_n.
\]

On native proposal edges use exactly

\[
 S_{xy}=(q_y/q_x)^{\eta_n}(Q_{yx}/Q_{xy})^{\kappa_n},
 \quad r_\pi(x,y)=\pi_yQ_{yx}/(\pi_xQ_{xy}),
\]
\[
 L(x,y)=Q_{xy}\min(1,S_{xy})\min(1,r_\pi/S_{xy}),
 \quad L(x,x)=1-\sum_{y\ne x}L(x,y),
 \quad C=(I+\alpha G+\beta L)/2.                         \tag{1}
\]

**Native multilevel lower lemma.** Suppose that on an infinite subsequence
of horizons tending to infinity, for some fixed a>0,

\[
                 \frac{D_n}{\eta_n\log n}\ge a.           \tag{2}
\]

Choose any fixed integer J with Ja>1 and any fixed
0<b<1-exp(-K). There are admitted native instances at every sufficiently
large horizon in that subsequence, for either sign of delta_n, for which

\[
 \liminf\|qC^n-\pi\|_{TV}
       \ \ge\ b\left(\frac{\beta}{2\alpha+\beta}\right)^J>0. \tag{3}
\]

The same construction has the explicit finite lower bound (19) below.
Its support may grow and its exact-real precision cost may be arbitrarily
large. In particular, neither bounded support nor bounded precision is being
smuggled into the new information contract. The signs of delta_n may change
between horizons. All exponents are finite at each horizon but their sizes
need not be bounded across horizons.

If R_A(n) denotes the actual class supremum at these public parameters, one
may let fixed b increase to 1-exp(-K) after applying the lemma. Thus the
right side in (3) can be replaced by

\[
 (1-e^{-K})\left(\frac{\beta}{2\alpha+\beta}\right)^J
\]

as a lower bound for liminf R_A(n) along the stated subsequence. No optimality
of this positive floor is asserted.

For fixed eta in (0,1) and fixed kappa!=eta, a positive subsequential lower
bound on A_n/log n implies (2). Therefore a necessary condition for uniform
convergence in that fixed-power class is A_n=o(log n). This includes public
budgets below the one-crossing threshold |delta|A_n=eta log n: a sufficiently
large but fixed J accumulates the adverse effect. The lemma also supplies the
unbounded-distortion branch of the principal's moving-policy necessity proof.
The separate bounded eta_n log n branch is not proved here.

## 2. Exact public geometry, including both row budgets

Fix a horizon satisfying (2), omit its subscript, and put

\[
 R=e^A,\qquad M=\lceil R\rceil.
\]

Condition (2) implies A>0 and delta!=0. Thus M>=2 and

\[
                   1\le M/R<2.                           \tag{4}
\]

Take a complete M-ary tree of depth J, together with a separate core state
star. The tree is indexed by finite words over {1,...,M}, of lengths 0 to J.
Its orientation below determines the progress levels i=0,...,J. The native
state space is this actual labelled tree, not a quotient graph.

### Positive mismatch: kappa>eta, expansion

Use ordinary depth i as progress level i, so N_i=M^i native states occupy
level i. For every parent x and child y set

\[
                  Q_{xy}=\frac1{2M},\qquad
                  Q_{yx}=\frac R{2M}.                     \tag{5}
\]

At an internal vertex the total forward proposal probability is 1/2 and the
total backward proposal probability is R/(2M)<=1/2. The root has only forward
edges and a leaf only its backward edge.

### Negative mismatch: kappa<eta, coalescence

Use J minus ordinary depth as progress level i, so N_i=M^{J-i} native states
occupy level i. A progressing vertex x has its unique ordinary parent y as
the next-level neighbor. Set

\[
                  Q_{xy}=\frac R{2M},\qquad
                  Q_{yx}=\frac1{2M}.                       \tag{6}
\]

At an internal vertex the total forward proposal probability is R/(2M)<=1/2
and the total backward proposal probability, over M neighbors, is 1/2. The
level-0 union is the set of ordinary tree leaves; level J is its ordinary root.

In both cases give every vertex the remaining row mass as Q_xx, and set
Q_star,star=1. All row sums are exactly one. Internal diagonals equal
(M-R)/(2M)>=0. Endpoint diagonals use their actual single direction of
outflow and are also nonnegative. The support is reciprocal. Every native
off-diagonal log reverse/forward ratio is exactly +A in (5), or -A in (6),
so the advertised budget holds with equality. Q uses the public A and tree
labels only; it uses neither target probabilities nor target observations.

Write the aggregate forward proposal mass as

\[
 f=\begin{cases}1/2,&\delta>0,\\R/(2M),&\delta<0.
 \end{cases}
 \qquad \frac14<f\le\frac12.                             \tag{7}
\]

The weak bound f>=1/4 is sufficient below. Genuine probabilities R/(2M)
and 1/(2M), not a desired but unrealizable quotient matrix, enforce both
native row budgets.

## 3. Positive masses and the native first screen

Set

\[
 z=\begin{cases}
 M R^{-\kappa/\eta}=(M/R)e^{-D/\eta},&\delta>0,\\
 R^{\kappa/\eta}/M=(R/M)e^{-D/\eta},&\delta<0,
 \end{cases}
 \qquad V=-\log z.                                       \tag{8}
\]

By (2) and (4),

\[
             V\ge a\log n-\log2\longrightarrow\infty,
 \qquad 0<z\le2n^{-a}\longrightarrow0.                   \tag{9}
\]

For n sufficiently large define the terminal target mass and the level totals
by

\[
 p=\frac1{(\log n)^2(1+V)},\qquad
 q_i=bz^i,\qquad \pi_i=p\,n^{-2(J-i)},\quad 0\le i\le J.  \tag{10}
\]

Each native x in level i receives q_x=q_i/N_i and pi_x=pi_i/N_i. Give star
the remaining masses q_star=1-sum_i q_i and pi_star=1-sum_i pi_i.
All masses are strictly positive for sufficiently large n: sum_i q_i tends
to b<1, and sum_i pi_i<=p/(1-n^-2) tends to zero. In particular,

\[
           q_\star\to1-b,\qquad\pi_\star\to1.             \tag{11}
\]

The target probability is defined after Q. This order makes target independence
explicit. The same analytic prescription works regardless of the sign and
size of the exponent mismatch.

It is essential to compute native, individual-state ratios. On a forward
edge x in level i to y in level i+1 they are as follows:

| Quantity | Expansion, delta>0 | Coalescence, delta<0 |
|---|---:|---:|
| q_y/q_x | z/M=R^{-kappa/eta} | z M=R^{kappa/eta} |
| Q_yx/Q_xy | R | 1/R |
| pi_y/pi_x | n^2/M | n^2 M |
| r_pi(x,y) | n^2 R/M | n^2 M/R |
| S_xy | 1 | 1 |

Thus S=1 exactly at every forward edge, with no integer-rounding distortion
in the first screen. For n>=2 the target Hastings ratio is at least n^2/2>1,
so forward total acceptance is exactly one. The reverse first screen is also
one and the reverse total acceptance is exactly 1/r_pi. Consequently the
actual local kernel, after completing its true rejection diagonal, has

\[
 L(i,i+1)=f\quad(i<J),\qquad
 L(i,i-1)=f/n^2\quad(i>0)                                 \tag{12}
\]

as aggregate transitions between progress levels. For example, expansion has
backward proposal mass R/(2M) and backward acceptance M/(n^2R), giving
1/(2n^2)=f/n^2. Coalescence has M backward proposals of mass 1/(2M), each
accepted with probability R/(n^2M), giving R/(2Mn^2)=f/n^2. Both agree with
detailed balance of the level target masses.

At an internal level the true local diagonal is 1-f-f/n^2; at the two
endpoints it is respectively 1-f and 1-f/n^2. These are actual quotient
diagonals after all native self-proposals and rejected proposals are included.
Global moves within a nonsingleton level remain in that level and belong to
the quotient diagonal, even when the native state changes.

Tree automorphisms act transitively on every level and preserve q,pi,Q,G,L.
The partition into progress levels and star is therefore strongly lumpable.
The q start and every evolved distribution are uniform within each level.
The preceding calculations could also be used without lumping: every native
vertex in a given level has the same aggregate probabilities in (12).

## 4. One KL budget, uniformly even when V is arbitrarily large

Let W_i=pi_i/q_i denote the common importance ratio on level i. Then

\[
 W_i=(p/b)n^{-2(J-i)}e^{iV},\quad
 W_{i+1}/W_i=n^2e^V>1,\quad W_J=(p/b)e^{JV}.              \tag{13}
\]

No assumption that transient W_i<1 is made or needed. Some may be very
large when the public distortion is very large. For each level,

\[
 \log W_i=\log(p/b)-2(J-i)\log n+iV
               \le\log(1/b)+JV.
\]

The full native KL equals the KL of these level totals because q and pi have
the same uniform split inside each level. Bounding the core contribution by
log(1/q_star) gives the single-budget admission bound

\[
\begin{split}
 D(\pi\|q)
 &\le \log(1/q_\star)
   +\frac{p}{1-n^{-2}}\{\log(1/b)+JV\}\\
 &\le \log(1/q_\star)
   +\frac{\log(1/b)+J}{(\log n)^2(1-n^{-2})}
   \longrightarrow-\log(1-b)<K.                          \tag{14}
\end{split}
\]

This counts every native state and has strict eventual slack. The denominator
1+V in p is load-bearing when V can grow faster than every function of n.
Using a target mass fixed only as a power of n would not establish this
uniform admission statement for arbitrary moving exponents.

## 5. Terminal retention in the original chain

From (13), W_J is larger than every other tree ratio. It also eventually
exceeds W_star, since (9), Ja>1, and (10) imply W_J/n tends to infinity.
Here is a uniform verification that does not assume V=O(log n). The function
(1+v)e^{-Jv} decreases for v>=0 and every integer J>=1. Hence, writing
v_0=a log n-log2>0,

\[
 \frac n{W_J}=b n(\log n)^2(1+V)e^{-JV}
 \le b n(\log n)^2(1+v_0)e^{-Jv_0}
 =O\!\left(n^{1-Ja}(\log n)^3\right)\longrightarrow0.     \tag{15}
\]

Let T be the entire terminal union, not one terminal vertex. Since W_J is
maximal, its actual one-step escape probability under C is exactly

\[
 d_T=\frac{\alpha(1-p)}{2W_J}+\frac{\beta f}{2n^2}.        \tag{16}
\]

The first term sums all nonterminal target mass in the independence kernel.
Global moves between different terminal vertices stay inside T and are
retained. The second term is the actual accepted local backward flow (12).
Equation (15) proves n d_T->0. Starting anywhere in T, retaining the whole
terminal union for at most n further steps therefore has probability at
least (1-d_T)^n->1 in the unchanged chain.

## 6. Capture with deterministic finite waiting windows

This lower bound does not need any transient importance ratio comparison
with the core. It selects a subset of paths using the mixture's actual
random choice of I,G,L at each step. Until the first terminal arrival:

* a marked forward local transition is success for the current stage;
* every global G attempt is marked failure, including a rejection or a
  within-level global move;
* an accepted local backward transition is also marked failure;
* laziness and all other local holds keep the current stage running.

Marking an event as failure here only defines the subset used for the lower
bound. It does not change C, remove actual paths, or assert that a globally
rejected move truly left the level.

Put

\[
 c=\beta f/2,\qquad g=\alpha/2,\qquad
 E=c+g+c/n^2,\qquad h=\lfloor n/(2J)\rfloor.              \tag{17}
\]

At a transient progress level i, the exact per-step marked-event hazard is
e_i=c+g+1_{i>0}c/n^2. A forward marked event has probability c. The true local
diagonal gives all unmarked hold probability 1-e_i. Therefore the probability
that the next marked event is forward and occurs within h actual C steps is

\[
 \frac c{e_i}\{1-(1-e_i)^h\}
   \ge \frac cE\{1-e^{-(c+g)h}\}.                       \tag{18}
\]

The bound holds from every vertex at that level and after each conditional
arrival. Requiring J successes, each within its own h-step window, reaches T
by time Jh<=n/2. The Markov property multiplies these conditional lower
bounds; independence of the waiting times is not assumed. The root union has
initial q mass exactly b. Combining capture with original-chain retention
and then subtracting pi(T)=p proves the complete finite certificate

\[
 \boxed{\displaystyle
 \|qC^n-\pi\|_{TV}
 \ge b\left(\frac cE\right)^J
       \{1-e^{-(c+g)h}\}^J(1-d_T)^n-p.}                  \tag{19}
\]

All time counts in (19) are actual deterministic transition counts. There is
no replacement of a random attempt count by its expectation. The selected
event remains a subset of original full-chain paths. Once it arrives at T,
all global attempts and within-T movement are allowed; (16) accounts for
every route out. Paths that leave T and later return, or that reach T by an
unmarked route, are simply extra nonnegative contributions to qC^n(T).
Thus (19) is a lower bound for the original full risk, with its actual returns.

Since c>=beta/8, a safe explicit finite bound in (19) is

\[
 \frac cE\ge\frac{\beta}{4\alpha+\beta(1+n^{-2})}.
                                                               \tag{20}
\]

The timing factor tends to one because J is fixed and c+g>=beta/8+alpha/2>0.
The retention factor tends to one by (15)-(16), and p tends to zero. This
already yields the positive lower floor b[beta/(4alpha+beta)]^J.

For the stronger statement (3), f tends to 1/2 in both signs. It is exactly
1/2 in expansion. In coalescence, kappa>=0 implies |delta|=eta-kappa<=eta,
and (2) forces A>=a log n. Therefore R->infinity and R/ceil(R)->1. This
argument also applies when the signs alternate. Thus c->beta/4 and

\[
                c/E\longrightarrow\frac{\beta}{2\alpha+\beta}.
\]

Taking liminf in (19) proves (3). This is only a lower bound: when transient
weights exceed the core weight, the real chain can have additional successful
routes. No exact moving-policy TV limit is claimed.

## 7. Fixed-power consequence below the one-crossing threshold

Let eta in (0,1) and kappa!=eta be fixed, and put d=|kappa-eta|. If
c_0=limsup A_n/log n>0, choose any fixed a with 0<a<d c_0/eta. On an infinite
subsequence, D_n/(eta log n)>=a. Choose a fixed integer J>1/a and apply the
lemma. Hence limsup R_A(n)>0.

For example, if A_n/log n tends to c with 0<dc<eta, no individual edge has
enough mismatch distortion to offset the entire logarithmic drop required
for a horizon-n trap. Nevertheless any integer J>eta/(dc), with a small
strict margin when selecting the subsequence, admits the multilevel witness.
The native edge budget is never exceeded. Each level has q mass smaller by
a factor asymptotic to exp(-dA/eta), while its local forward acceptance is
exactly one. These losses of proposal mass accumulate across J levels, and
each level has a fixed positive chance of advancing before the next global
attempt. Fixed J preserves a positive capture probability.

This proves a necessary condition A_n=o(log n) for the fixed-power problem.
Sufficiency, and the complete moving-policy criterion, require the principal's
separate support-uniform upper argument. This file does not infer either
upper statement from the lower construction.

## 8. Ordinary independence sampling on the same native input

The witness does not make ordinary proposal-start IMH fail. Let
s_q=sum_{i=1}^J q_i<=bz/(1-z), and pi_tree=sum_i pi_i<=p/(1-n^-2).
Level 0 has the smallest W among tree levels, and its W_0 tends to zero,
so the core also has larger W eventually. From any root-union state, every
global proposal outside that union is consequently accepted. An IMH step
stays in the root union with probability b, moves to the core with probability
q_star, and moves to other tree levels with probability s_q.

The probability from the root union of entering the other tree levels before
the core is s_q/(1-b). The probability of remaining in the root union for j
steps is b^j. Once the core is first hit, the remaining original chain has TV
at most TV(delta_star,pi)=pi_tree by contraction, including every later return.
Initial mass already on other tree levels is at most s_q. Consequently

\[
 \|qG^j-\pi\|_{TV}
 \le\pi_{\rm tree}+\frac{s_q}{1-b}+b^{j+1}
 \le\frac p{1-n^{-2}}+\frac{bz}{(1-b)(1-z)}+b^{j+1}.       \tag{21}
\]

This tends to zero whenever j tends to infinity, in particular for
deterministic j/n tending to any positive constant. Analytic direct target
sampling remains allowed when the full displayed description is available.
No implementation advantage over those comparators follows from (19).

## 9. Actual support, indexing and precision costs

The exact number of native states, for either sign, is

\[
 N_{\rm native}=1+\sum_{i=0}^J M^i
              =1+\frac{M^{J+1}-1}{M-1},\qquad
 \log N_{\rm native}=J\log M+O(1).                        \tag{22}
\]

Here log M lies between A and A+log2. J is fixed on the chosen subsequence,
but A may be unbounded arbitrarily quickly. A vertex label requires up to
J ceil(log_2 M)+O(log J) bits; child selection requires log_2 M bits of index
information. A compact level-and-uniform-label sampler can avoid enumerating
all states, but its index generation and arithmetic are not constant cost.
In coalescence the initial root union itself contains M^J vertices; in
expansion the terminal union contains M^J vertices. Both multiplicities have
already been included in q,pi, their KL, and every native ratio.

On the tree the log magnitudes obey the explicit bounds

\[
 \log(1/q_x)\le\log(1/b)+J(V+\log M),
\]
\[
 \log(1/\pi_x)\le
 2J\log n+2\log\log n+\log(1+V)+J\log M.                 \tag{23}
\]

These are magnitude/precision scales, not a finite-bit implementation theorem.
For arbitrary real policies, exact evaluation of exp(A), its ceiling,
exp(-V), and native forward/reverse probabilities is part of the exact-real
description. A certified finite-precision implementation must charge whatever
precision is required, including near integer boundaries and in large
exponent products. No fixed word length, free normalizer, free target table,
free cache, or oracle-independent constant-time sampling claim is made.

The proof was derived algebraically. No exponentially large native tree was
materialized to establish the asymptotic statement. A small native finite
identity check, if supplied with this contribution, only checks the displayed
formulas and does not prove the asymptotic lemma or provide a speed benchmark.

## 10. What the predecessor contributes and what changes

MATCHED_POWERS_THEOREM.md supplied the native opposite-sign fan-in/fan-out
idea and demonstrated that a native ratio must retain block cardinality.
BRANCHING_SHARPNESS.md supplied the full finite-level capture/retention
method, including actual rejection holds, a terminal union, deterministic
waiting windows, and a source-bound comparison with ordinary IMH.
RECIPROCAL_PROPOSAL_THEOREM.md supplied the current enlarged reciprocal-Q
contract; its upper theorem is not reproved here.

The new steps are an exact per-edge public budget in both signs, simultaneous
native forward/backward row accounting, finite accumulation across levels,
the R versus ceil(R) construction valid even as A tends to zero with a huge
positive exponent mismatch, and the entropy allocation 1/(1+V) that admits
unbounded moving distortions. Marking all global attempts during capture
removes an unjustified transient-weight ordering that can fail in that regime.
The resulting lower bound closes a sharp convergence-criterion necessity
branch; it is more than an off-diagonal scalar extremum.
