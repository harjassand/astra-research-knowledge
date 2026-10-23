# Finite-distortion interpolation: an attainable native lower

Contributor: `/root/cycle9_lower`, Astra PRO3 Cycle9. Date: 22 October 2026.
This is a bounded extension requested after completing
`GROWING_DEPTH_LOWER.md`; that earlier file remains unchanged. The principal
supplied the finite-distortion question and the attenuated-screen idea. This
contribution checks its actual native realization, all path factors and the
variational identity. No numerical experiment was run.

## 1. Exact statement

Retain the exact finite reciprocal-Q model, rejection diagonal, q start,
one population D(pi||q)<=K, and fixed-within-run policies of the Cycle8
principal proof and `GROWING_DEPTH_LOWER.md`. Let

\[
 \ell=\log n,\quad L_0=\log\ell,\quad
 D_n=|\kappa_n-\eta_n|A_n\to d\in(0,\infty),\quad
 v_n=\frac{\eta_n\ell}{1+D_n},\quad
 \frac{v_n}{L_0}\to\lambda\in(0,\infty).
                                                               \tag{1}
\]

Thus eta_n->0, v_n->infinity and eta_n ell/L_0 ->lambda(1+d).
Fix an arbitrary screen attenuation a>=0, which is constant as n grows,
and a fixed 0<b<1-exp(-K). Write

\[
 \sigma=e^{-a},\quad r_b=\alpha(1-b)/\beta,
 \quad\gamma_b(a)=\log(1+r_b e^a).
\]

There are admitted native instances with terminal target mass p=ell^-4
and an explicit retained capture lower bound P_n for which

\[
 \|qC^n-\pi\|_{TV}\ge P_n-p,\qquad
 -\frac{\log P_n}{L_0}\longrightarrow
       \lambda(1+d)\frac{\gamma_b(a)}{d+a}.              \tag{2}
\]

When the last constant is below four, p/P_n->0. The construction is valid
for both signs of kappa_n-eta_n, including signs alternating across n,
and for a=0. All public budgets are met exactly. The target normalizer,
full table, indices, arithmetic precision and implicit tree representation
are not free operations.

Define

\[
 r_0=\alpha e^{-K}/\beta,\qquad
 c_d=\inf_{a\ge0}\frac{\log(1+r_0e^a)}{d+a}.             \tag{3}
\]

The consequence for the class supremum is

\[
 \boxed{\displaystyle
 \limsup\frac{-\log\mathscr R_n}{\log\log n}
       \le\min\{1,\lambda(1+d)c_d\}.}                  \tag{4}
\]

The one in (4) comes from the preserved Q=I information-tail lower; the
second term comes from this attainable transport construction. Equation
(4) is the lower side of a sharp-rate theorem. Its matching upper is a
distinct principal obligation. No critical amplitude is established here.

## 2. Saturated reciprocal proposals fixed before the target

Suppress horizon subscripts. Put R=exp(A), h=2log(v+1). On an ordinary
complete M-ary tree of depth J, set on each parent-child edge x,y

\[
 Q_{xy}=1/(M+R),\qquad Q_{yx}=R/(M+R).                  \tag{5}
\]

Fill the genuine remaining diagonal and give a separate core star the
proposal Q_star,star=1. Internal outgoing rows have exactly M child terms
and one parent term, summing to one. Endpoints omit only their absent
direction. Every nonzero off-diagonal reverse/forward ratio has absolute
logarithm A. The proposal is target-independent and has reciprocal support.

For delta=kappa-eta>0 use M=ceil(R exp(h)) and ordinary depth as progress.
For delta<0 use M=ceil(R exp(-h)) and reverse ordinary depth as progress.
Let

\[
 \chi=\begin{cases}M/R,&\delta>0,\\R/M,&\delta<0,
 \end{cases}\qquad f=\chi/(1+\chi).
\]

Because D->d>0, delta and A are nonzero eventually. In coalescence,
kappa>=0 implies A>=D/eta, and (1) gives

\[
 A\ge\left(\frac d{(1+d)\lambda}+o(1)\right)\ell/L_0.
\]

Consequently R exp(-h)->infinity and its ceiling has vanishing relative
error. In expansion the relative ceiling error is at most exp(-h)/R.
Both sign constructions therefore satisfy

\[
 M\ge2,\quad\chi=(v+1)^2(1+o(1)),\quad
 \log\chi=h+o(1),\quad1-f=O((v+1)^{-2}).                \tag{6}
\]

The target has not entered the specification of Q.

## 3. An exact attenuated screen in either orientation

Define

\[
 z=\chi\exp[-(D+a)/\eta],\qquad
 V=-\log z=(D+a)/\eta-\log\chi.                          \tag{7}
\]

Equivalently,

\[
 z=\begin{cases}
 M R^{-\kappa/\eta}e^{-a/\eta},&\delta>0,\\
 R^{\kappa/\eta}e^{-a/\eta}/M,&\delta<0.
 \end{cases}
\]

Here

\[
 V\sim(D+a)/\eta\asymp\ell/L_0,
 \qquad V\to\infty,\qquad V=o(\ell),\qquad z\to0.
\]

Set, exactly as a finite construction,

\[
 p=\ell^{-4},\quad T_*=\ell+6L_0+\log b,\quad
 J=\lceil T_*/V\rceil,\quad
 q_i=bz^i,\quad\pi_i=p n^{-2(J-i)},\quad0\le i\le J.     \tag{8}
\]

Split level masses uniformly over M^i vertices for expansion and M^(J-i)
vertices for coalescence; give star the remaining masses. The resulting
positive distributions satisfy q_star->1-b and pi_star->1. Moreover,

\[
 \frac J{L_0}\longrightarrow\frac{\lambda(1+d)}{d+a},
 \qquad J=O(L_0),\qquad J\to\infty.                     \tag{9}
\]

For each forward native edge the ratios, with all native multiplicities
included, are

| Quantity | Expansion | Coalescence |
|---|---:|---:|
| q_y/q_x | R^(-kappa/eta) exp(-a/eta) | R^(kappa/eta) exp(-a/eta) |
| Q_yx/Q_xy | R | 1/R |
| pi_y/pi_x | n²/M | n² M |
| S_xy | exp(-a) | exp(-a) |
| target Hastings ratio t_xy | n²/chi | n²/chi |

Thus the first screen is exactly sigma in both signs, not a relaxed bound.
The reverse first screen is sigma^-1. Since t_xy/sigma=n²/(chi sigma)>1
eventually, forward acceptance is exactly sigma. Reverse acceptance is
exactly sigma/t_xy. Therefore the actual local aggregate probabilities are

\[
             L(i,i+1)=f\sigma,
             \qquad L(i,i-1)=f\sigma/n^2.                \tag{10}
\]

The internal rejection diagonal is 1-f sigma-f sigma/n²; endpoints omit
the absent direction. Nonnegativity follows from the native calculation.
Strong lumpability holds by the ordinary tree automorphisms and uniform
within-level masses. The analysis does not give a free quotient sampler.

## 4. Transient/core ordering and a single KL budget

As before,

\[
 W_i=(p/b)n^{-2(J-i)}e^{iV},\qquad W_{i+1}/W_i=n²e^V>1.
\]

The actual integer choice of J in (8) ensures

\[
 W_J\ge n\ell²,\qquad W_{J-1}<\ell²/n\to0.             \tag{11}
\]

Since W_star->1/(1-b), every transient ratio is below the core ratio
eventually. The single full KL calculation is

\[
 D(\pi\|q)\le\log(1/q_\star)+
       \frac p{1-n^{-2}}\{\log(1/b)+JV\}
       \longrightarrow-\log(1-b)<K.                     \tag{12}
\]

Indeed JV<T_*+V=ell+o(ell), making the second term O(ell^-3).
Multiplicity cancels only because both q and pi were split uniformly
within each actual native level. One information budget covers the whole
instance; no independent KL allocation is used for capture and retention.

## 5. Accepted global hazards and all original-chain returns

For transient level i<J, the true probability under G of leaving that
progress level is

\[
 g_i=q_\star+\sum_{j>i}q_j+
                         \frac{\sum_{j<i}\pi_j}{W_i}.
\]

The core proposal is accepted by (11); higher tree levels are also accepted.
For lower levels the acceptance produces pi_j/W_i. Consequently

\[
 q_\star\le g_i\le1-b+\frac b{n²(1-n^{-2})}.             \tag{13}
\]

Global moves within a level and global rejections remain genuine holds.
Set

\[
 c=\beta f\sigma/2,\quad
 E=c+\frac\alpha2\left(1-b+
                \frac b{n²(1-n^{-2})}\right)+c/n²,
 \quad H=\lfloor n/(2J)\rfloor.
\]

Before capture, mark a local forward move as success, a local accepted
backward move or any global out-of-level move as failure, and otherwise
hold the stage. From each native state at level i the exact event hazard
is c+alpha g_i/2+1_{i>0}c/n². Thus forward success within H actual steps
before failure has probability at least

\[
          (c/E)\{1-e^{-(c+\alpha q_\star/2)H}\}.          \tag{14}
\]

Condition successively on the J stage arrivals. These deterministic windows
reach the terminal union by JH<=n/2 without substituting a random count by
its expectation. No independence of waiting times is assumed.

The entire terminal union has maximal W. Its actual escape probability
under C is

\[
 d_T=\alpha(1-p)/(2W_J)+\beta f\sigma/(2n²),
 \qquad nd_T\le\alpha/(2\ell²)+\beta\sigma/(2n)\to0.    \tag{15}
\]

All native global moves between terminal vertices remain inside the union.
After capture the selected event retains the original chain in that union;
paths that exit and return only add to the final mass. Therefore

\[
 \boxed{\displaystyle
 \|qC^n-\pi\|_{TV}\ge
 b(c/E)^J\{1-e^{-(c+\alpha q_\star/2)H}\}^{J}
                              (1-d_T)^n-p.}             \tag{16}
\]

This is a lower bound on the original full risk with all returns. Denote
the product before subtraction by P_n.

## 6. Limit and minimax optimization

For each fixed a, sigma>0 is a fixed constant. Equations (6), (9), and
(13)-(16) give

\[
 \log(c/E)=-\log(1+r_b e^a)+O(1-f)+O(n^{-2}),
 \qquad J(1-f)\to0.
\]

The timing factor tends to one because c tends to beta sigma/2>0,
J=O(L_0), and H is asymptotic to n/(2J). Retention tends to one by (15).
Hence

\[
              P_n=b\exp[-\gamma_b(a)J+o(1)],             \tag{17}
\]

which proves (2). The fixed attenuation a can be arbitrarily large, but
it is chosen before taking n to infinity; no uniform-in-a statement is
being inferred from c bounded away from zero for a fixed a.

If lambda(1+d)c_d<1, choose a fixed finite a for which
lambda(1+d)log(1+r_0 e^a)/(d+a)<1, with value as close to the infimum as
desired. Choose fixed b sufficiently close to 1-exp(-K) to preserve this
strict inequality with r_b. Then the constant in (2) is below one, so
p/P_n->0. Let b increase to its endpoint and let the chosen ratio approach
the infimum only after the n limit. This proves the second bound in (4).

If lambda(1+d)c_d>=1, the inherited Q=I two-state lower already gives
liminf ell R_n>=K and therefore the exponent upper bound one. This also
handles equality without a new joint-budget construction. The two lower
families are alternatives inside the supremum, not simultaneous spenders
of K. An infimum attained only as a->infinity is legitimate in this
order of limits; every construction actually used has finite fixed a.

## 7. Exact scalar identity and the three regimes

For d>0, r>0 and 0<=c<=1, define

\[
 H_d(c)=\sup_{0<z\le1}\{e^{dc}z^{1-c}-z\}.
\]

Substituting z=exp(-a), a>=0, gives the exact equivalence

\[
 H_d(c)\le r
 \ \Longleftrightarrow\
 e^{c(d+a)}\le1+r e^a\ \text{for every }a\ge0
 \ \Longleftrightarrow\
 c\le\inf_{a\ge0}\frac{\log(1+r e^a)}{d+a}.             \tag{18}
\]

The infimum is at most one by a->infinity. Thus it is exactly the largest
c in [0,1] admitted by H_d(c)<=r. This is the variational bridge between
the finite-energy envelope and the independently attainable native path
attenuation. It is not a claim that a scalar extremizer alone gives a
mixing lower; Sections 2-6 supply that missing realization.

For 0<c<1 let

\[
 F(c)=c(1-c)^{(1-c)/c},\qquad
 v_*(c)=-\log(1-c)/c.
\]

Direct differentiation in z gives

\[
 H_d(c)=\begin{cases}
 e^d F(c),&d\le v_*(c),\\
 e^{dc}-1,&d\ge v_*(c).
 \end{cases}                                             \tag{19}
\]

At c=0 the value is zero; at c=1 it is e^d, approached as z tends to zero.
The latter is not e^d-1: the endpoint maximum changes location.
H_d(c) is continuous and strictly increasing in c on [0,1].

Let gamma=log(1+r) and

\[
       d_c=\frac{1+r}{r}\log(1+r).
\]

The value c_d(r)=inf_a log(1+r e^a)/(d+a) has the explicit cases

\[
 c_d(r)=\begin{cases}
 1,&r\ge e^d,\\
 \text{the unique }c\in(0,1)\text{ with }F(c)=r e^{-d},
       &r<e^d\text{ and }d\le d_c,\\
 \gamma/d,&d\ge d_c.
 \end{cases}                                             \tag{20}
\]

At d=d_c the last two cases coincide. To check the transition, simultaneous
equality in the branches of (19) gives r=c/(1-c), so c=r/(1+r), and
d=v_*(c)=d_c. Also d_c>log r, so the capped first case and the final case
do not conflict. For d>d_c the optimum is the unscreened edge a=0. In
the strict middle case it is a finite positive a (a=0 at the transition);
in the capped case its infimum
may require a->infinity. Formula (20) follows from (18)-(19), not from
an unproved convex or transport premise.

Taking r=r_0 gives precisely the c_d in (3). As d tends to infinity,
(1+d)c_d tends to log(1+r_0), agreeing with the separately proved
strong-distortion construction. As d decreases to zero, the coefficient
connects to the preserved matched-screen c_* (or one when r_0>=1).
These scalar limits do not by themselves prove a uniform moving-d theorem;
the principal must check its upper and lower quantifiers.

## 8. Comparator, resources and limitations

The same native input has the inherited full-return ordinary IMH estimate

\[
 \|qG^j-\pi\|_{TV}\le
 p/(1-n^{-2})+bz/[(1-b)(1-z)]+b^{j+1}.                    \tag{21}
\]

For j/n->t>0 this is O(ell^-4), since V asymptotic to a positive constant
times ell/L_0 makes z smaller than every inverse power of ell. Direct
sampling remains a legitimate comparator when the analytic target is
fully available. No step-count law is a target-call or wall-time speedup.

The actual support is 1+sum_{i=0}^J M^i. A native index can need
J ceil(log_2 M)+O(log J) bits. The q and pi magnitude bounds from the
growing-depth construction remain valid, with V now (D+a)/eta-log chi.
All exp(A), integer ceilings, q/target evaluations, forward/reverse proposal
evaluations, cache operations and required precision retain their costs.
No large graph or exact-real sampler was materialized. No finite-precision
stability or practical implementation advantage is asserted.

The direct native argument here requires d>0. In particular its coalescence
rounding proof uses A>=D/eta->infinity. It is not silently extended to
D->0 when A may vanish. The accepted matched-screen construction is the
proper separate lower dependency at that endpoint. The finite envelope
identity (18) remains a scalar identity, and its use at a moving endpoint
still needs a valid full-law proof.

The construction changes the candidate sharp rate from a function of v
alone to one involving the finite distortion d through (1+d)c_d. Internal
checking, principal acceptance, historical originality, external acceptance
and useful implementation are distinct. Total inference, token and
discovery costs remain unknown.
