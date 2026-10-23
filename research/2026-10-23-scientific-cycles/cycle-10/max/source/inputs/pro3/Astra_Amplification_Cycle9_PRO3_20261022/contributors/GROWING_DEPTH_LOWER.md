# Saturated native transport through a growing number of levels

Contributor: `/root/cycle9_lower`, Astra PRO3 Cycle9. Date: 22 October 2026.
This is a bounded independent derivation of the new lower construction. The
principal owns the theorem and integration. The proof establishes a lower law
for the actual native chain; no reduced process is supplied to the sampler.

## 1. Statement and source boundary

Fix K>0, alpha in (0,1), beta=1-alpha. At each horizon n use the exact
Cycle8 class: finite positive pi,q, one population D(pi||q)<=K, proposal-q
independence MH G, fixed target-independent row-stochastic reciprocal Q,
public A>=max |log(Q_yx/Q_xy)|, and fixed-within-run powers 0<eta<1,
kappa>=0. The screen and local kernel are

\[
 S_{xy}=(q_y/q_x)^\eta(Q_{yx}/Q_{xy})^\kappa,
 \quad L_{xy}=Q_{xy}\min(1,S_{xy})
                 \min\{1,\pi_yQ_{yx}/(\pi_xQ_{xy}S_{xy})\},
 \quad C=(I+\alpha G+\beta L)/2.                         \tag{1}
\]

Every rejection completes the actual diagonal. The initialization is q and
TV is half l1. Put

\[
 \ell=\log n,\quad L_0=\log\ell,\quad
 D=|\kappa-\eta|A,\quad v=\frac{\eta\ell}{1+D}.
\]

Suppose

\[
       D_n\to\infty,\qquad v_n\to\infty,
       \qquad v_n=O(\log\log n).                         \tag{2}
\]

For each fixed 0<b<1-exp(-K), define

\[
 r_b=\frac{\alpha(1-b)}\beta,\qquad
 \gamma_b=\log(1+r_b).
\]

There are admitted native instances, valid for either sign of kappa-eta and
also when that sign changes with n, with a terminal union T_n, pi(T_n)=ell^-4,
and an explicit lower bound P_n on the probability of a selected event in the
original chain such that

\[
 qC^n(T_n)\ge P_n,
 \qquad -\frac{\log P_n}{v_n}\longrightarrow\gamma_b,
 \qquad \|qC^n-\pi\|_{TV}\ge P_n-\ell^{-4}.             \tag{3}
\]

The finite positive lower certificate is (19) below. In particular, if
v_n/L_0 ->lambda in [0,infinity) and lambda gamma_b<4, then
ell^-4/P_n ->0 and

\[
 \limsup\frac{-\log \mathscr R_n}{v_n}\le\gamma_b.       \tag{4}
\]

Here R_n is the native class supremum. For lambda=0 this gives a genuine
subcritical rate. For finite positive lambda, combining (4) with the
preserved Q=I information-tail lower and then taking b up to 1-exp(-K)
gives

\[
 \limsup\frac{-\log\mathscr R_n}{\log\log n}
 \le\min\{1,\lambda\log(1+\alpha e^{-K}/\beta)\}.       \tag{5}
\]

Equation (5) is a lower-obstruction statement, not the upper theorem. The
principal's distinct energy proof is needed for equality. No critical
amplitude is claimed here.

The source read was the unchanged Cycle8
`ASYMMETRY_BUDGET_THEOREM.md`, Sections 7-9 (including its exact native edge
and full-retention calculations), and the complete
`contributors/ASYMMETRY_LOWER.md`. The earlier construction used fixed
depth, a forward local proposal mass asymptotic to one half, and marked
every global attempt as failure. None of those three choices is retained
without checking its changed role below.

## 2. Public native geometry and saturated row budgets

All quantities in this section are public deterministic horizon quantities.
For sufficiently large n, D>0, A>0, and delta=kappa-eta is nonzero. Write

\[
 R=e^A,\qquad h=2\log(v+1).
\]

Use an ordinary complete M-ary tree, with depth J chosen in Section 3,
and one disconnected local core state star. On every ordinary parent-child
edge x,y, set

\[
 Q_{xy}=\frac1{M+R},\qquad Q_{yx}=\frac R{M+R},          \tag{6}
\]

where x is the ordinary parent. Fill every remaining row with its genuine
diagonal, and set Q_star,star=1. At an internal vertex the M child proposals
sum to M/(M+R), while the parent proposal is R/(M+R); their sum is exactly
one. Endpoint rows contain their actual one-direction outflow. Thus Q is
row-stochastic, reciprocal and target-independent. Its edge asymmetry is
exactly A. No target evaluations have occurred in its specification.

If delta>0, choose M=ceil(R exp(h)), and let progress run from ordinary
root to leaves. If delta<0, choose M=ceil(R exp(-h)), and let progress run
from ordinary leaves to root. In the latter case kappa>=0 gives

\[
 A\ge D/\eta
   =\frac\ell v\frac D{1+D}\asymp\ell/v.
\]

Under (2), R exp(-h) tends to infinity. Therefore M>=2 eventually in both
orientations. Define

\[
 \chi=\begin{cases}M/R,&\delta>0,\\R/M,&\delta<0,\end{cases}
 \qquad f=\frac\chi{1+\chi}.
\]

Integer rounding is controlled rather than ignored:

\[
 \chi=e^h(1+o(1))=(v+1)^2(1+o(1)),\quad
 \log\chi=h+o(1),\quad 1-f=O((v+1)^{-2}).                \tag{7}
\]

For expansion, M/R=exp(h)+O(1/R), so the relative error is O(exp(-h)).
For coalescence, M=R exp(-h)(1+O(exp(h)/R)); its relative error tends to
zero faster than any inverse power of log n. These estimates are valid
on alternating sign subsequences. The actual forward aggregate proposal
mass is f in either orientation, and it tends to one. This improves the
old half-budget construction without violating the reverse native rows.

## 3. Masses, depth, and all transient importance ratios

Define

\[
 z=\begin{cases}
 M R^{-\kappa/\eta},&\delta>0,\\
 R^{\kappa/\eta}/M,&\delta<0,
 \end{cases}
 \quad z=\chi e^{-D/\eta},\quad
 V=-\log z=D/\eta-\log\chi.                              \tag{8}
\]

Since v=O(L_0), (2) and (7) give

\[
 V\sim\ell/v\longrightarrow\infty,
 \qquad V=o(\ell),\qquad z\to0.
\]

The fact V=o(ell) uses v->infinity. Choose

\[
 p=\ell^{-4},\quad T_*=\ell+6\log\ell+\log b,
 \quad J=\left\lceil T_*/V\right\rceil,\quad
 q_i=bz^i,\quad\pi_i=p n^{-2(J-i)},\quad 0\le i\le J.     \tag{9}
\]

Progress level i has N_i=M^i native states in expansion and
N_i=M^(J-i) in coalescence. Split both level masses uniformly over these
states; give star the remaining masses. All probabilities are strictly
positive eventually, q_star->1-b and pi_star->1. Also

\[
     J/v\to1,\qquad J\to\infty,\qquad J=O(L_0).          \tag{10}
\]

For example, ell/V=v(1+o(1)), the O(L_0)/V term from T_* is o(1), and
integer rounding contributes at most one, negligible relative to v.

The level importance ratio is

\[
 W_i=(p/b)n^{-2(J-i)}e^{iV},\qquad
 W_{i+1}/W_i=n^2e^V>1.
\]

Depth was chosen for two simultaneous purposes:

\[
 W_J\ge n\ell^2,\qquad
 W_{J-1}<\frac p b n^{-2}e^{T_*}=\ell^2/n\to0.          \tag{11}
\]

The second inequality is strict because (J-1)V<T_*. Since W_star->1/(1-b),
every transient tree ratio lies below W_star eventually. This is an actual
proved premise of the new global capture calculation. It was not true in
the older arbitrary-distortion, fixed-depth proof.

## 4. Native acceptance and the exact rejection diagonal

On a forward edge the native quantities are

| Quantity | Expansion | Coalescence |
|---|---:|---:|
| q_y/q_x | z/M=R^(-kappa/eta) | zM=R^(kappa/eta) |
| Q_yx/Q_xy | R | 1/R |
| pi_y/pi_x | n²/M | n² M |
| S_xy | 1 | 1 |
| target Hastings ratio | n² R/M=n²/chi | n² M/R=n²/chi |

By (7), n²/chi>1 eventually. Forward acceptance is therefore exactly one;
reverse acceptance is chi/n². Multiplying by all actual backward proposals
gives

\[
             L(i,i+1)=f,\qquad L(i,i-1)=f/n^2.           \tag{12}
\]

The true internal local diagonal is 1-f-f/n²; endpoint diagonals omit only
the nonexistent direction. Its nonnegativity also follows from the native
acceptance calculation; explicitly chi<n² ensures f+f/n²<=1.
The native multiplicity has not been replaced by level totals in any
Hastings ratio.

Tree automorphisms preserve q,pi,Q and the resulting kernels and act
transitively within a level. Hence the level-plus-core partition is
strongly lumpable, with q start and later laws uniform inside each level.
The proof can alternatively be read directly from the native aggregate
probabilities, which are the same at every vertex of a fixed level.

## 5. A single full information allocation

Within-level uniform factors cancel in D(pi||q). As in the native model,
this is one KL budget for the entire instance. Since log W_i is at most
log(1/b)+JV, and the core contribution is at most log(1/q_star),

\[
 D(\pi\|q)\le\log(1/q_\star)+
       \frac p{1-n^{-2}}\{\log(1/b)+JV\}.                \tag{13}
\]

The ceiling in (9) gives JV<T_*+V=ell+o(ell). Thus the second term is
O(ell^-3), and the first tends to -log(1-b)<K. This proves strict eventual
admission. A fixed p=ell^-4 is valid here because (2) proved V=o(ell) and
JV=ell+o(ell). It would not be valid without that new scale restriction.
No separate information budget is allocated to the core and the trap.

## 6. Improved competing hazards: global moves inside a level are holds

For a transient progress level i<J, independence MH has actual probability
of leaving that level

\[
 g_i=q_\star+\sum_{j>i}q_j+
                    \frac{\sum_{j<i}\pi_j}{W_i}.         \tag{14}
\]

The core term is q_star because (11) ensures its proposal is accepted.
Higher tree levels have larger W and their proposals are also accepted.
Lower tree levels contribute pi_j/W_i. Native global moves within the
same level, including changes of vertex, remain in its aggregate hold.
Using pi_{i-r}=pi_i n^(-2r) gives

\[
 q_\star\le g_i\le 1-b+
                   \frac{b}{n^2(1-n^{-2})}.              \tag{15}
\]

For the upper bound, q_star+sum_{j>i}q_j=1-sum_{j<=i}q_j<=1-b, while
sum_{j<i}pi_j/W_i<=q_i/[n²(1-n^-2)]<=b/[n²(1-n^-2)]. In particular,
g_0=1-b exactly. This calculation retains global rejections and global
within-level movement. Marking every global attempt as failure would
instead pay alpha/2 and lose the desired constant.

Before first arrival in the terminal level select the following subset of
original paths: a local forward move succeeds at the current stage; any
accepted local backward move or any global move out of that progress level
is a failure; all other steps hold the stage. Define

\[
 c=\beta f/2,\qquad
 E=c+\frac\alpha2\left(1-b+
              \frac b{n^2(1-n^{-2})}\right)+c/n^2,
 \qquad H=\left\lfloor\frac n{2J}\right\rfloor.           \tag{16}
\]

At level i its exact marked hazard is
e_i=c+alpha g_i/2+1_{i>0}c/n². Thus
c+alpha q_star/2<=e_i<=E. The probability that the next marked event is
forward and occurs within H actual C steps equals

\[
 \frac c{e_i}\{1-(1-e_i)^H\}
 \ge\frac cE\{1-\exp[-(c+\alpha q_\star/2)H]\}.         \tag{17}
\]

This holds from every native state in that level, despite within-level
global movement, because its aggregate probabilities are constant.
Successive conditioning and the Markov property give J such successes
within JH<=n/2. No independent waiting-time assumption is needed, and no
optional number of attempts is replaced by its mean.

## 7. All terminal return paths and a complete finite certificate

Let T be the entire progress level J. By (11), its W is maximal in the
whole instance eventually. Its actual full-chain escape probability is

\[
 d_T=\frac{\alpha(1-p)}{2W_J}+\frac{\beta f}{2n^2},
 \qquad n d_T\le\frac\alpha{2\ell^2}+\frac\beta{2n}\to0.\tag{18}
\]

The first term sums every global destination outside T; global movement
between different members of T is retained. The second is the actual
accepted local reverse flow. Conditional on capture by n/2, remaining in
the terminal union to time n has probability at least (1-d_T)^n. This
uses the original chain throughout. Paths not selected by this event,
including exits followed by returns, only add to qC^n(T).

Starting in progress level zero has q probability b. Combining (17)-(18)
therefore proves the finite certificate

\[
 \boxed{\displaystyle
 \|qC^n-\pi\|_{TV}\ge
 b\left(\frac cE\right)^J
 \{1-e^{-(c+\alpha q_\star/2)H}\}^{J}(1-d_T)^n-p.}       \tag{19}
\]

Define P_n as the product before subtracting p. It is a lower bound on
the probability of an explicitly selected event of the original full
chain. Equation (19) is not a first-hit mass being misidentified with
the final distribution.

## 8. Growing-depth error accumulation and the sharp lower exponent

From (7), (10), and (16),

\[
 \log(c/E)=-\log(1+r_b)+O(1-f)+O(n^{-2})
          =-\gamma_b+O((v+1)^{-2})+O(n^{-2}).             \tag{20}
\]

Multiplication by J=O(v) makes the error o(1). The timing factor in (19)
also tends to one: c is bounded below by beta/4 eventually,
H asymptotic to n/(2J), J=O(loglog n), and therefore
J exp[-(c+alpha q_star/2)H]->0. By (18) the retention factor tends to one.
Consequently

\[
       P_n=b\exp[-\gamma_b J+o(1)],
       \qquad -\log P_n/v\to\gamma_b.                   \tag{21}
\]

If v/L_0->lambda and lambda gamma_b<4, then
log(p/P_n)=(-4+lambda gamma_b+o(1))L_0->-infinity. Thus (3)-(4) follow.
This includes every transport-dominated regime needed for (5), where
lambda gamma_*<1 and gamma_*=log(1+alpha exp(-K)/beta): choose fixed b
close enough to 1-exp(-K) that lambda gamma_b<1, apply (4), then increase
b to the endpoint only after taking the asymptotic bound.

If lambda gamma_*>=1, the preserved Q=I two-state family already gives
liminf ell R_n>=K, so its log exponent is at most one. This proves (5)
also at equality; it does not add two independent lower budgets.
If lambda=0, (4) and b increasing to 1-exp(-K) give the lower rate
limsup[-log R_n]/v_n<=gamma_* directly. An upper proof is still a separate
obligation in all these cases.

## 9. Strong ordinary comparison on the identical input

Let s_q=sum_{i=1}^J q_i<=bz/(1-z) and
pi_tree=sum_{i=0}^J pi_i<=p/(1-n^-2). From every level-zero vertex, every
proposal outside that level is accepted by G, because its importance ratio
is the smallest. The next non-level-zero proposal hits the core with
probability q_star/(1-b) or another level with probability s_q/(1-b).
Once the core is reached, ordinary total-variation contraction gives error
at most pi_tree for all later times, retaining all later returns. Accounting
also for initial mass on the other levels yields, for every integer j>=0,

\[
 \|qG^j-\pi\|_{TV}\le
 \frac p{1-n^{-2}}+\frac{bz}{(1-b)(1-z)}+b^{j+1}.         \tag{22}
\]

For deterministic j/n->t>0, the right side is O(ell^-4): under (2),
z=exp[-(1+o(1))ell/v] is smaller than every inverse power of ell.
The hybrid transport lower can instead be ell^(-lambda gamma_b+o(1)),
or exp[-(gamma_b+o(1))v] in the slower subcritical regime. This is an
adverse law comparison. It is not a wall-time, evaluation-count or
implementation advantage for the hybrid. Direct target sampling remains
legitimate when the explicit analytic masses and indexing are disclosed.

## 10. Resource boundary and changed premises

The actual native support is

\[
       1+\sum_{i=0}^J M^i
       =1+(M^{J+1}-1)/(M-1),
\]

and a native index may require J ceil(log_2 M)+O(log J) bits. The depth
now grows like v, whereas log M can be arbitrarily large under a finite
but unrestricted public A. Native log probability magnitudes satisfy

\[
 \log(1/q_x)\le\log(1/b)+J(V+\log M),\qquad
 \log(1/\pi_x)\le4\log\ell+2J\ell+J\log M.
\]

These are exact-real finite instances. Computing exp(A), its nearby
integer ceiling, target/proposal ratios and tiny probabilities has whatever
index and precision cost it actually needs. No fixed-word or uniformly
efficient construction is asserted. The absorbed proof operator is not
used here as an executable sampler. No large native graph was materialized
in deriving this contribution, and no numeric curve establishes the limit.

Three predecessor choices must change to obtain the new exponent:

1. A forward aggregate probability of one half wastes half the native row
   budget. Choosing M/R or R/M near (v+1)^2 makes the forward aggregate
   tend to one while both native row budgets remain exact.
2. Marking all G attempts as failure loses the factor 1-b. The new depth
   selection proves W_i<W_star for every transient i, making the exact
   accepted global out-of-level hazard available. Global rejections and
   same-level moves remain holds.
3. A growing number of stages requires accumulating the f, timing and
   retention errors. Equations (20)-(21) do that explicitly. A fixed-depth
   convergence statement alone would not justify the new exponent.

The older p=1/[ell²(1+V)] was needed for arbitrary V in the convergence
necessity theorem. Here V~ell/v and JV~ell are proved first, so p=ell^-4
is admissible. This is a narrowed rate regime with an explicitly justified
mass choice, not a repair or weakening of the accepted Cycle8 theorem.

The scientific consequence of this lower is a sharp candidate transport
constant gamma_*=log(1+alpha exp(-K)/beta) in the strong-distortion regime,
realized by a native construction. Acceptance of the matching upper and the
integrated same-v separation remains with the principal. Historical novelty,
external mathematical acceptance and efficient useful implementation remain
unestablished. Inference, token and total discovery costs are unknown.
