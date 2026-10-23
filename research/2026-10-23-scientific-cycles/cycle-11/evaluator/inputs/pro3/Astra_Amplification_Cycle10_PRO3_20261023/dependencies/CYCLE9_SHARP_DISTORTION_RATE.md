# Sharp logarithmic risk under a public proposal-asymmetry budget

Principal construction and integration: Astra PRO3, 22 October 2026,
Australia/Brisbane. This is a continuation of the accepted Cycle8 theorem.
The complete native information contract and unchanged predecessor archive
accompany this proof. Independent source-bound review status is recorded in
STATUS.md; delivery alone is not mathematical acceptance.

## 1. Exact model and new result

Fix K>0 and alpha in (0,1), and put beta=1-alpha. At each integer horizon n
the public policy supplies finite A_n>=0, 0<eta_n<1 and kappa_n>=0. An
admitted instance has finite labelled strictly positive probability vectors
pi,q with D(pi||q)<=K, and a fixed target-independent row-stochastic Q
having reciprocal off-diagonal support and

    max_{x!=y:Q_xy>0} |log(Q_yx/Q_xy)| <= A_n.

The maximum over no edges is zero. All quantities are fixed within a run;
support, degrees and probabilities may vary across horizons. On a positive
edge, write r_Q=Q_yx/Q_xy and

    S_xy=(q_y/q_x)^eta r_Q^kappa,
    t_xy=(pi_y/pi_x)r_Q,
    L_xy=Q_xy min(1,S_xy) min(1,t_xy/S_xy).

The actual rejection diagonal completes L. G is proposal-q independence
Metropolis-Hastings, C=(I+alpha G+beta L)/2, and the initial law is q.
TV is half l1. Write R_n for the supremum of TV(q C^n,pi) over this exact
class, and set

\[
 \ell=\log n,\quad L=\log\ell,\quad
 D_n=|\kappa_n-\eta_n|A_n,\quad u_n=\eta_n\ell,
 \quad v_n=u_n/(1+D_n),\quad r=\alpha e^{-K}/\beta.       \tag{1}
\]

The letter D_n is a scalar discrepancy budget, not relative entropy or a
diagonal matrix. The accepted Cycle8 theorem proves R_n->0 exactly when
v_n->infinity. This proof does not reopen that criterion.

For d>=0 define the transport coefficient

\[
 c(d)=\inf_{a\ge0,\ d+a>0}
          \frac{\log(1+r e^a)}{d+a},\qquad
 g(d)=(1+d)c(d),\qquad \gamma=\log(1+r).                  \tag{2}
\]

Thus a=0 is excluded only when d=0. The infimum can be approached as
a->infinity; finite attainment is not assumed. We prove below that
0<c(d)<=1, that g extends continuously to d=infinity, and that
g(infinity)=gamma. In particular g is bounded above and away from zero
on the compactified nonnegative line.

**Theorem 1 (sharp logarithmic risk throughout the convergent class).**
For every public policy sequence with v_n->infinity,

\[
 \boxed{\displaystyle
 \frac{-\log R_n}
      {\min\{\log\log n,\ u_n c(D_n)\}}\longrightarrow1.} \tag{3}
\]

There is no assumed limit of eta_n, kappa_n, A_n or D_n. The supremum
includes every finite admitted support and proposal. This is a logarithmic
equivalent, not a multiplicative equivalent for R_n and not a critical
amplitude theorem.

In particular, if v_n/L->lambda in (0,infinity) and D_n->d in [0,infinity],

\[
 \frac{-\log R_n}{\log\log n}\longrightarrow
       \min\{1,\lambda g(d)\}.                            \tag{4}
\]

Here the extended value d=infinity is permitted, with g(infinity)=gamma.
If D_n->infinity and v_n->infinity, the entire logarithmic law reduces to

\[
 -\log R_n\sim\min\{\log\log n,\gamma v_n\}.             \tag{5}
\]

**Corollary 2 (same v is not a sharp-rate description).** At K=1 and
alpha=1/2 there are three policies with the SAME v_n=loglog n and the
SAME public asymmetry bound A_n, whose respective logarithmic risk
exponents are c(0), log 2, and log(1+e^-1). They are different. All three
risks converge to zero. Section 9 gives the actual policies.

The ordinary IMH comparator still has minimax amplitude K at scale 1/log n.
Nothing in (3)-(5) is a sampling speedup, a finite-time TV ordering, or a
fixed-word implementation guarantee. All sampler access and native costs
remain those in INFORMATION_AND_COST_CONTRACT.md.

## 2. Accepted finite operation and the new proof obligations

The exact Cycle8 source ASYMMETRY_BUDGET_THEOREM.md, Sections 3-5, is an
accepted dependency. Its SHA256 is
eba1595d9efec9c7dc8ac5c97257a9f0bf741f1f7931105114dc58faeae9e6c1.
It retains the actual accepted outflow, reverse-proposal Jensen coefficients,
killed global mass, all first-hit times and all full-chain post-hit returns.
Its finite interface is reproduced here to make the new asymptotics explicit.

Take 0<h<1/2, A={pi/q<h}, b=q(A), and let E be a proof-selected subset of
A^c with e=q(E). Absorb E and kill exits to A^c\\E only in a first-hit
counter, without row normalization. For proof parameters

\[
 0<\theta\le\eta,\quad\theta\le1/2,\quad p=(1-\theta)^{-1},
 \quad \tau=p(1-\theta/\eta),\quad U=e^{D\theta p/\eta},
\]

put

\[
 H=\sup_{0<z\le1}(Uz^\tau-z),\qquad
 \Gamma(e)=\frac12+\frac{2^{p-1}}2
       \{1+[\beta H-\alpha(1-b)]_++\alpha e\}.             \tag{6}
\]

Here w=1 is sufficient. If tau=0, H=U; if 0<tau<1, then

\[
 H=\begin{cases}
 U(1-\tau)(U\tau)^{\tau/(1-\tau)},&U\tau\le1,\\
 U-1,&U\tau\ge1.
 \end{cases}                                               \tag{7}
\]

The bound is a full weighted energy inequality, not just a pointwise
off-diagonal comparison. Iteration gives first-hit mass at most
b^(1-theta)e^theta Gamma(e)^(N/p). In the original full chain define

\[
 M_0=e^{2K+1},\quad a_R=\pi(W>R),\quad
 J_0=2/[\alpha(2(n-N)+1)],\quad \rho=1-\alpha(1-b)/2,
\]
\[
 \bar e=\min\{1-b,\ a_R/R+
              (N+1)(M_0/h+1)J_0/d_{\rm test}^2\}.
\]

The accepted full-return certificate is

\[
 \begin{split}
 TV(qC^n,\pi)\le{}&a_R+\sqrt{(M_0+R)J_0}+d_{\rm test}
       +\bar e+b\rho^N\\
       &+b^{1-\theta}\bar e^\theta\Gamma(\bar e)^{N/p}.
 \end{split}                                                \tag{8}
\]

It propagates each first hit by the ORIGINAL C for the remaining time.
The absorbed process is never a modified sampler. One population budget
simultaneously implies

\[
 a_R\le K/(\log R-1),\qquad
 -\log(1-b)\le [K+H_2(h)]/(1-h).                            \tag{9}
\]

We use throughout

\[
 h=\ell^{-2},\quad R=n/\ell^4,\quad d_{\rm test}=\ell^{-2},
 \quad N=\lceil 8L/(\alpha e^{-K})\rceil.                  \tag{10}
\]

Uniformly over instances, for large n,

\[
 \bar e\le E_n=C\ell^6(L+1)/n,\quad
 \sqrt{(M_0+R)J_0}+d_{\rm test}+\bar e+b\rho^N=O(\ell^{-2}),
\]
\[
 1-b\ge e^{-K}-O((L+1)/\ell^2).                            \tag{11}
\]

All constants in these displays depend only on K,alpha. The new tasks are
to find the correct exponent in (6), and to realize its transport loss by
native stochastic proposal rows with reachable retained mass. Scalar
optimization alone would not prove (3).

## 3. The scalar coefficient, with its exact regimes

For d>=0 and 0<c<1 write

\[
 H_d(c)=\sup_{0<z\le1}\{e^{dc}z^{1-c}-z\}.
\]

Putting z=e^-a shows the equivalence

\[
 H_d(c)\le r
 \ \Longleftrightarrow\
 e^{c(d+a)}\le1+r e^a\quad\hbox{for every }a\ge0
 \ \Longleftrightarrow\
 c\le c(d).                                                \tag{12}
\]

For d=0 the excluded a=0 constraint is simply 1<=1+r and imposes
no condition. Every c<c(d) gives H_d(c)<r: the scalar maximum is attained
on the compactified z-interval and the inequalities are strict, with the
z=0 limit also strictly below r when c<1. The infimum in (2) is at most
one because its ratio tends to one as a->infinity.

Define F(c)=c(1-c)^((1-c)/c), F(1)=1, and

\[
 d_*=\frac{1+r}{r}\log(1+r).
\]

Then the exact piecewise description is

\[
 c(d)=\begin{cases}
 1,& r\ge e^d,\\
 \text{the unique }c\in(0,1)\text{ with }F(c)=r e^{-d},
       &r<e^d\text{ and }d<d_*,\\
 \log(1+r)/d,&d\ge d_*.
 \end{cases}                                               \tag{13}
\]

At d=d_* the second and third descriptions coincide at c=r/(1+r).
The first case can occur only when r>=1. It includes the appropriate
endpoint d=log r. There is no division by zero in the third case, since
d_*>0.

Here is a direct check. The derivative numerator of
phi_d(a)=log(1+r e^a)/(d+a) is

    B(a)=(d+a) r e^a/(1+r e^a)-log(1+r e^a).

Its derivative is (d+a) r e^a/(1+r e^a)^2>0 for d+a>0,
and B(infinity)=d-log r. If r>=e^d, B remains nonpositive,
so the infimum is one at infinity. Otherwise an interior minimum exists
unless B(0)>=0. The latter condition is exactly d>=d_* and gives a=0,
c(d)=gamma/d. At an interior minimizer put c=r e^a/(1+r e^a).
The stationary equation (d+a)c=-log(1-c), together with
r e^a=c/(1-c), rearranges to F(c)=r e^-d. Since
d log F(c)/dc=-log(1-c)/c^2>0, the solution is unique.
These formulas prove continuity, including both finite joining points.
For d>=d_*, g(d)=gamma(1+1/d), hence g(infinity)=gamma>0.

Equation (13) is not yet a risk theorem. The remaining sections supply
the uniform upper and the actual attaining geometry.

## 4. Uniform upper when discrepancy has a finite limit

Consider a subsequence with D_n->d<infinity and v_n->infinity,
v_n=O(L). Then u_n=(1+D_n)v_n=O(L) and eta_n=u_n/ell->0.
Fix 0<c<c(d), put theta=c eta_n, and use (6)-(10). Then p->1,
tau->1-c, U->e^(dc), so (7), or compact scalar convergence, gives

    H -> H_d(c) < r.

Thus beta H-alpha(1-b) is uniformly negative for large n. The positive
part in (6) is zero. The explicit accumulated estimate is

    log Gamma(bar e)^(N/p) <= N theta log 2 + alpha N bar e = o(1),

because N theta=O(L^2/ell). The first-hit factor is bounded by

    bar e^theta <= exp[-c u_n + O(theta(L+1))]
                = exp[-c u_n+o(1)].

Empty bad sets are zero directly. Consequently

\[
 R_n\le\frac K{\ell-4L-1}+O(\ell^{-2})
                        +\exp[-c u_n+o(1)].                \tag{14}
\]

Every error is uniform over the native class; the threshold can depend
on the policy subsequence and fixed c,d. Letting c increase to c(d)
only AFTER taking asymptotic inequalities supplies the desired upper
logarithmic exponent for finite d. No unproved endpoint substitution
or finite-time TV ordering is used.

## 5. Uniform upper when discrepancy diverges

Suppose D_n->infinity. Put theta=gamma eta_n/D_n, which eventually
satisfies theta<=eta_n and theta<=1/2. Then

    p=(1-theta)^-1, tau=p(1-gamma/D_n), U=exp(gamma p).

Since tau->1 and U->e^gamma>1, U tau>1 eventually. The exact branch of
(7) is therefore H=e^(gamma p)-1. This is not substitution into an old
strict-contraction theorem. With Delta=[beta H-alpha(1-b)]_+, (11) gives

\[
 \Delta\le C\{\theta+(L+1)/\ell^2\}.                     \tag{15}
\]

The finite positive part need not vanish. From (6), for small theta,

    log Gamma(bar e) <= C(theta+Delta+bar e).

Combining all accumulated terms with theta log bar e and putting
w_n=eta_n ell/D_n=v_n(1+1/D_n) gives

\[
 R_n\le\frac K{\ell-4L-1}+O(\ell^{-2})+
 \exp\{-\gamma w_n[1-C(L+1)/\ell]+\varepsilon_n\},        \tag{16}
\]

where epsilon_n->0 uniformly over instances. Indeed the part not
proportional to theta is O(N(L+1)/ell^2+N E_n)=o(1); the theta part
is O(N theta+theta(L+1)), paid relative to theta ell. No bound on
v_n/L is needed for (16). If v_n=O(L), it simplifies to

\[
 R_n\le\frac K{\ell-4L-1}+O(\ell^{-2})+
                    \exp[-\gamma\eta_n\ell/D_n+o(1)].     \tag{17}
\]

This proves the required upper exponent for every diverging-D subsequence.
In particular, if liminf gamma v_n/L>1, the transport term is o(1/ell)
and the ordinary information-tail lower gives ell R_n->K. Nothing here
identifies a multiplicative prefactor at equality.

## 6. Native transport construction: both mismatch signs and growing depth

This section proves the lower for either D_n->d in (0,infinity), or
D_n->infinity, assuming v_n->infinity and v_n=O(L). In the finite-d
case choose any fixed attenuation a>=0; in the diverging-D case take a=0.
Fix b in (0,1-e^-K), before taking n to infinity. Write delta=kappa-eta,
R_A=exp(A_n), and h_n=2 log(v_n+1). Eventually D_n>0, hence A_n>0 and
delta!=0. The sign may change with n.

Use a complete M-ary labelled tree plus a core star. Its undirected edges
carry the directed probabilities

\[
 Q_{parent,child}=1/(M+R_A),\qquad
 Q_{child,parent}=R_A/(M+R_A).                              \tag{18}
\]

The internal row sum is exactly one. The root and leaves receive their
actual completing diagonals; Q_star,star=1. These proposal rows are fixed
from public quantities and labels before specifying the target. Their
maximum edge log asymmetry is exactly A_n.

If delta>0, progress is root to leaves, and M=ceil(R_A exp(h_n)).
If delta<0, progress is leaves to root, and M=ceil(R_A exp(-h_n)).
For the latter, kappa>=0 gives A_n>=D_n/eta_n. This tends to infinity
much faster than h_n: in the finite-d case eta_n=O(L/ell), and in the
diverging-D case D_n/eta_n~ell/v_n. Thus M>=2 eventually in both cases.

Define chi=M/R_A for expansion and chi=R_A/M for coalescence. Then

\[
 \chi=(v_n+1)^2(1+o(1)),\quad
 f=\frac\chi{1+\chi},\quad J(1-f)\to0\ \text{for the J below},
\]
\[
 z=\chi\exp[-(D_n+a)/\eta_n],\qquad V=-\log z.             \tag{19}
\]

Rounding is justified explicitly: in expansion
M/R_A=exp(h_n)+O(1/R_A); in coalescence
M/(R_A exp(-h_n))=1+O(exp(h_n-A_n))=1+o(1).
The errors are uniform over the two sign choices along the sequence.

In the finite-d case, V~(d+a)/eta_n and
ell/V~u_n/(d+a). In the diverging-D case, V~D_n/eta_n and
ell/V~v_n. In all cases V->infinity, V=o(ell), and V/L->infinity.

Put

\[
 p_T=\ell^{-4},\qquad T_n=\ell+6L+\log b,\qquad
 J=\lceil T_n/V\rceil,\qquad
 q_i=bz^i,\quad\pi_i=p_T n^{-2(J-i)},\quad0\le i\le J.    \tag{20}
\]

Split these level totals uniformly among M^i vertices in expansion or
M^(J-i) vertices in coalescence. Give the core the remaining q and pi
masses. Both are positive eventually, q_star->1-b and pi_star->1.
The integer depth obeys

\[
 J/u_n\to1/(d+a)\quad(D_n\to d>0),\qquad
 J/v_n\to1\quad(D_n\to\infty).                            \tag{21}
\]

In particular J->infinity and J=O(L). Integer rounding is an O(1)
error at this logarithmic scale, not a claimed vanishing prefactor error.

### 6.1 Per-vertex screen and native reverse acceptance

For a progress edge the exact per-vertex q ratio is z/M in expansion
and zM in coalescence. The reverse Q ratio is R_A or R_A^-1 respectively.
Substitution into the ACTUAL powers gives S_xy=e^-a in both cases.
The target Hastings ratio is n^2/chi in both cases, so t_xy/S_xy>1
eventually. Hence forward local acceptance is sigma=e^-a, and reverse
acceptance is chi sigma/n^2. Multiplying by all native proposals yields

\[
 L(i,i+1)=f\sigma,\qquad L(i,i-1)=f\sigma/n^2.             \tag{22}
\]

The actual diagonal is 1-f sigma-f sigma/n^2 at an internal level,
with only nonexistent directions omitted at endpoints. The reverse
aggregate in (22) counts all children in the coalescing orientation.
Using level probabilities as per-vertex ratios would be incorrect.

All automorphisms within each level preserve q,pi,Q. Transition mass
into any level is independent of the particular current vertex. Thus
the level-plus-core partition is strongly lumpable. The q start and all
evolved laws are uniform within each level, so quotient TV equals native
TV. A quotient is a proof/diagnostic representation, not a free sampler.

### 6.2 One KL budget, controlled transient weights and terminal retention

The level importance ratios are

\[
 W_i=(p_T/b)n^{-2(J-i)}e^{iV},\qquad W_{i+1}/W_i=n^2e^V.
\]

The exact depth choice gives

\[
 n\ell^2\le W_J<n\ell^2 e^V,\qquad
 W_{J-1}<\ell^2/n.                                       \tag{23}
\]

Consequently every transient W_i<1<W_star<W_J for large n.
Their entropy contributions are negative. Since log W_J<=ell+2L+V,

\[
 D(\pi\|q)\le\log(1/q_\star)+p_T(\ell+2L+V)
       \longrightarrow-\log(1-b)<K.                      \tag{24}
\]

This is one complete native admission calculation. No two lower families
share or add their information allocations. The fixed p_T=ell^-4 is
legitimate here because the NEW rate regime proves V=o(ell); it was not
legitimate for the arbitrary enormous V in the old nonconvergence proof.

For the entire terminal union T, including its internal global moves,
the exact one-step full-chain escape probability is

\[
 d_T=\frac{\alpha(1-p_T)}{2W_J}
                   +\frac{\beta f\sigma}{2n^2},\qquad
 n d_T\le\frac\alpha{2\ell^2}+\frac\beta{2n}\to0.         \tag{25}
\]

No return is erased from the actual chain. Selecting paths that stay
inside T after first capture is only a lower-bound event.

## 7. Actual competing exits and the logarithmic capture cost

Let c_f=beta f sigma/2. At a transient progress level i<J, every global
proposal to the core or a higher level is accepted by (23). A lower-level
proposal j<i is accepted with ratio W_j/W_i. Therefore the global
probability of LEAVING that level is exactly

\[
 g_i=q_\star+\sum_{j>i}q_j+\frac{\sum_{j<i}\pi_j}{W_i}.
\]

The first two terms total 1-sum_{j<=i}q_j<=1-b. Moreover

\[
 \frac{\sum_{j<i}\pi_j}{W_i}
       =q_i\sum_{k=1}^i n^{-2k}
       \le b/(n^2-1).
\]

Thus with

\[
 g_{\rm core}=\alpha q_\star/2,\qquad
 E=c_f+\alpha(1-b)/2+\alpha b/[2(n^2-1)]+c_f/n^2,
\]

the actual out-of-level hazard e_i satisfies

\[
 c_f+g_{\rm core}\le e_i=c_f+\alpha g_i/2
                          +1_{i>0}c_f/n^2\le E.          \tag{26}
\]

Mark a local forward exit as success; all other actual exits are failure.
All global rejections and within-level moves remain holds. A global
forward jump is conservatively failure, not an extra free success.

Let H=floor(n/(2J)). For each conditional arrival, the probability that
the next level exit is a successful local forward move within H steps is

\[
 \frac{c_f}{e_i}[1-(1-e_i)^H]
 \ge\frac{c_f}{E}[1-(1-c_f-g_{\rm core})^H].                \tag{27}
\]

Strong lumping, or the uniform native level hazards, makes this identity
valid after any conditional within-level history. Requiring J successive
such deterministic windows reaches T by time JH<=n/2. The Markov property
suffices; no optional number of steps is replaced by its expectation.
Retention under the original C then gives the actual finite certificate

\[
 \boxed{TV(qC^n,\pi)\ge P_n-p_T,\quad
 P_n=b(c_f/E)^J[1-(1-c_f-g_{\rm core})^H]^J(1-d_T)^n.}      \tag{28}
\]

Since J=O(L), c_f+g_core stays bounded away from zero, and H grows as n/J,
the timing factor tends to one. Equation (25) handles retention. Define
r_b=alpha(1-b)/beta. As J(1-f)->0 and J/n^2->0,

\[
 \log P_n=\log b-J\log(1+r_b e^a)+o(1).                 \tag{29}
\]

For finite d>0, this yields

\[
 -\log P_n/u_n\longrightarrow
             \log(1+r_b e^a)/(d+a).                       \tag{30}
\]

For D_n->infinity (a=0), it yields

\[
 -\log P_n/v_n\longrightarrow\log(1+r_b).                \tag{31}
\]

Choose finite a and b<1-e^-K before n, then let b increase to 1-e^-K
and optimize a. Continuity in r_b and strict approximation to the
infimum in (2) give the desired coefficients. For r>=e^d the infimum
at infinity is approached with large FIXED a, never an uncontrolled
within-run limit. The subtracted p_T is negligible whenever transport
has logarithmic exponent below one, and also when v_n=o(L); those are
exactly the cases where transport is needed to beat the ordinary tail
lower. At the transition the tail lower suffices.

## 8. Complete policy quantifiers, including d=0 and oscillations

First, the accepted two-state Q=I family is admitted under every public
A_n and every power policy. For any k in (0,K), take target rare mass
p=k/ell and proposal rare mass e=p/(n ell^2). It has KL<K eventually,
L=I, and

\[
 TV(qC^n,\pi)=(p-e)(1-\alpha/(2n\ell^2))^n\sim k/\ell.
                                                               \tag{32}
\]

Hence liminf ell R_n>=K for every policy. This gives the logarithmic
upper limit one and prevents a fictitious rate faster than ordinary IMH.

Second, the d=0 transport lower is inherited by exact subclass inclusion.
Every symmetric Q has A(Q)=0 and makes the actual screen independent
of kappa. The accepted Cycle4 BRANCHING_SHARPNESS.md, Sections 3-7,
supplies for u->infinity,u=O(L), fixed b<1-e^-K, integer branching B>=2
and fixed spacing t>0, an admitted native symmetric family with

\[
 R_n\ge b\exp[-\phi_{r_{b,B}}(t)u_n+O(1)](1-o(1))-\ell^{-m},
\]
\[
 \phi_s(t)=\log(1+s e^t)/t,\quad
 r_{b,B}=\alpha(1-b)(B+1)/(\beta B),\quad m>2.
                                                               \tag{33}
\]

Its infimum over finite b,B,t is c(0). That source's formula is stated
for u->infinity,u=O(L), so it also covers u/L->0; no new extrapolation
from a single critical limit is made. The original reverse branching
factor, true diagonals and return retention are unchanged. The exact
source hash is 119dfb8d0b8e77b3ce93fdef1f1450c01fc1d090a0f05c4dd7ae0ea7ada1d645.

We now prove (3). Its denominator is v_n times g(D_n), capped at L,
and tends to infinity because v_n->infinity and g is bounded away from
zero. On any subsequence extract further subsequences on which
D_n->d in [0,infinity] and v_n/L->x in [0,infinity]. This uses compactified
limits and does not assume the original sequence converges.

If x=infinity, the accepted Cycle8 upper exp(-c_0 v_n) and (32) give
ell R_n->K. The denominator in (3) is then L, so the ratio tends to one.

If x<infinity, v_n=O(L). For finite d the upper (14), followed by
c increasing to c(d), applies. For d=infinity use (16). These prove
the ratio's liminf is at least one, including x=0; additive constants
in logarithms vanish since the denominator diverges.

For the converse, if x g(d)>=1, including equality, (32) proves the
ratio's limsup is at most one. If x g(d)<1, use (30) for d in (0,infinity),
(31) for d=infinity, or (33) for d=0. Choose b,a (or the inherited finite
branching parameters) sufficiently close to their infimum that the
capture exponent is still below one. Then p_T/P_n->0 and (28) gives the
matching lower rate. When x=0, its logarithm is o(L), so subtraction of
ell^-4 is automatically negligible. Increase b and approximate the
finite scalar infimum only after taking the asymptotic inequality.

Every violating subsequence would contain one of these cases, a
contradiction. This proves (3) for arbitrary oscillating policies and
also proves (4)-(5). Separate lower constructions are compared by a
maximum of errors, not by summing independent KL allocations.

## 9. Explicit same-v separation, with a common public A

Take K=1, alpha=beta=1/2, so r=e^-1. For all sufficiently large n set

    A_n=ell/L-2,   v_n=L.

Arbitrary valid values may be assigned at the finitely many earlier n.
Consider the following three policies, all fixed within a run:

| Policy | eta_n | kappa_n | D_n | Limiting -log R_n/L |
|---|---|---|---|---|
| Matched | L/ell | eta_n | 0 | c(0), where F(c(0))=e^-1 |
| Finite discrepancy | (log 4)L/ell | eta_n+(log 4-1)/A_n | log 4-1 | log 2 |
| Growing discrepancy | 1/2 | 0 | ell/(2L)-1 | log(1+e^-1) |

All eta_n lie in (0,1) eventually and every kappa_n is nonnegative.
Direct substitution gives v_n=L EXACTLY for each policy. Their public
A_n is also identical; no support or proposal information has been hidden.

For the middle row F(1/2)=1/4=r exp[-(log4-1)], and its scalar maximum
is on the interior branch, so c(log4-1)=1/2 and g=log2. The first row
uses the unchanged matched result or (3); the third uses the new
diverging-D law. The values satisfy

    log(1+e^-1) < c(0) < log 2 < 1.

For the first inequality, F(c)<=c implies c(0)>=r>log(1+r).
For the second, F(2/3)=2/(3 sqrt(3))>e^-1: indeed
e>1+1+1/2+1/6=8/3>3 sqrt(3)/2, with the latter comparison equivalent
to 256>243. Monotonicity of F gives c(0)<2/3, while
log2=2 atanh(1/3)>2/3. Thus c(0)<2/3<log2 without a numerical
decision. Supplied rational brackets illustrate these exact constants;
the formulas and inequalities, not printed decimals, define the theorem.

In particular,

\[
 \frac{R_n^{growing}}{R_n^{matched}}
       =\ell^{\,c(0)-\log(1+e^{-1})+o(1)}\to\infty.        \tag{34}
\]

Thus v_n is sufficient to decide convergence but insufficient to decide
its sharp logarithmic rate. Within the stated unrestricted finite class,
(3) also says that once u_n and D_n are specified, A_n and mismatch do
not supply an additional leading logarithmic parameter. This latter
statement concerns the class supremum, not a fixed graph, fixed support,
or finite-time performance.

## 10. Ordinary comparator, actual resources, and the remaining question

The same adverse inputs do not make pure proposal-start G fail. Let
s_q=sum_{i>=1}q_i<=bz/(1-z) and pi_tree<=p_T/(1-n^-2). From level zero,
the first global departure hits the core with its actual probability;
the chance of another tree level before the core is s_q/(1-b). After
a core hit, total-variation contraction of the ORIGINAL G bounds all
remaining error by pi_tree, including returns. Thus for every j>=0,

\[
 TV(qG^j,\pi)\le p_T/(1-n^{-2})+
                  bz/[(1-b)(1-z)]+b^{j+1}.                \tag{35}
\]

In the newly constructed rate families V/L->infinity, so z is smaller
than every fixed power of 1/ell. At j/n->t>0, including j=floor(alpha n/2),
(35) is O(ell^-4). This is a same-input law comparison, not a target-call
or wall-time equality. Direct sampling is also legitimate when the
analytic target description is actually available to the recipient.

The native support is 1+sum_{i=0}^J M^i. Labels need up to
J ceil(log2 M)+O(log J) bits. Probability magnitudes can require

    log(1/q_x) <= log(1/b)+J(V+log M),
    log(1/pi_x) <= 4L+2J ell+J log M.

An implicit tree or small proved quotient does not remove these index,
proposal, target-evaluation, reverse-Q, precision, or cache costs. There
is no free target normalizer, complete target table, population-KL
estimator, or absorbed simulator. Exact arbitrary-real policies may
not be computable at bounded precision. The theorem is ideal-real
robustness/complexity knowledge, not a finite-arithmetic instability
claim or an efficient implementation theorem.

The finite tests check new native rows, screens, actual hazards and
full-law inequalities. They do not prove a universal asymptotic result.
The frozen coalescing fixture failed its K=1 admission gate and remains
an algebraic fixture only; it is not an admitted empirical point. See
NUMERICS.md for unchanged inputs, exact results and costs.

The selected continuation is a multiplicative critical-risk law at a
fixed nonzero discrepancy, especially d>d_* where the optimum uses
fully accepted local progress. At u_n c(d)=loglog n+O(1), integer depth,
partial final crossings, information allocation and reachable capture
can affect the amplitude. Determine whether the actual limit exists
and depends only on d, or whether a native geometry or policy exposes
additional information. No amplitude is asserted here. An O(1) depth
error is harmless for (3) and potentially decisive for that next question.

Internal correctness, historical priority, external mathematical acceptance,
finite-precision realization and practical performance remain separate.
The accepted finite energy and full-return operations were actually used
to prove a new rate law; archiving or replay alone is not the receiving
scientific use. No causal claim about a prompt tactic or agent count follows.
