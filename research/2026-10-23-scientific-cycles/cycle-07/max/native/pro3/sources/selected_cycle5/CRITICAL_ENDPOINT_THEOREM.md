# The critical-window law: absorbed first hits and a single information budget

Principal construction and proof: Astra PRO3. Scientific date: 22 October 2026,
Australia/Brisbane. This is a continuation of the unchanged Cycle4 source.
The new operation is a finite absorbed-boundary energy inequality. The joint
information lemma was independently supplied by `/root/critical_budget` and is
proved in full below. Independent source-bound review status is in `STATUS.md`.
Historical originality and external acceptance are separate and unestablished.

## 1. Exact family, definitions and main theorem

Fix K>0 and alpha in (0,1), and put beta=1-alpha. An instance is a finite
labelled space with strictly positive probability vectors pi,q, a symmetric
stochastic target-independent Q, and population D(pi||q)<=K. Put W=pi/q.
G is independence Metropolis-Hastings with proposal q and target pi. For x!=y,

\[
 L_\eta(x,y)=Q_{xy}\min\{1,(q_y/q_x)^\eta\}
       \min\{1,(\pi_y/\pi_x)(q_x/q_y)^\eta\},\qquad
 C_\eta=(I+\alpha G+\beta L_\eta)/2.                 \tag{1}
\]

The actual rejection diagonal completes L. Every run starts from q and keeps
Q,eta,alpha,pi,q fixed. Supports may grow in the class supremum. The sampler
does not receive the target normalizer or a full target table. These are
exact-real statements; the native information/implementation contract remains
in `EXPERIMENT_CONTRACT.md`. TV is half l1, or the supremum over events. Define

\[
 R_\eta(n)=\sup_{\rm admitted}\|qC_\eta^n-\pi\|_{\rm TV},\quad
 F(c)=c(1-c)^{(1-c)/c},\quad r_0=\alpha e^{-K}/\beta.
\]

Assume throughout the main critical theorem that r_0<1, and let c_* in (0,1)
be the unique solution F(c_*)=r_0. Write b_K=1-exp(-K). All logs are natural.

**Theorem (exact critical amplitude).** For any deterministic across-run
policy satisfying, for fixed real s,

\[
 u_n:=\eta_n\log n={\log\log n\over c_*}+s+o(1),
\]

the native minimax risk has the limit

\[
 \boxed{\displaystyle
 \lim_{n\to\infty}(\log n)R_{\eta_n}(n)
       =\max\{K,b_K e^{-c_*s}\}.}                  \tag{2}
\]

The matching lower is the accepted, unchanged Cycle4
`CRITICAL_WINDOW_LOWER.md`, together with its ordinary Q=I family. The new
work proves the upper for the entire native finite class. It does not assume
tree geometry, a single target core, monotone target weights, few atoms,
bounded support growth, or the absence of return paths.

The ordinary pure-IMH comparator has leading risk K/log n under the same
forward-KL premise. Thus (2) identifies a robustness penalty, not a sampler
speedup. At s>=log(b_K/K)/c_* the leading hybrid amplitude equals K; for
smaller s it is larger. Finite-time ordering is not asserted.

## 2. Received anchor and elementary entropy facts, with proofs

Both G and the two-factor L in (1) are pi-reversible: the two factors for a
directed edge have the usual reciprocal product, and Q is symmetric. C is
lazy and reversible, so its spectrum lies in [0,1]. No initial L2 density is
required for the following bounded-test estimate.

The binary log-sum inequality, applied to H={W>R} with a=pi(H), gives, for R>e,

\[
 a\le {K\over\log R-1}.                              \tag{3}
\]

Indeed the H term is at least a log R, and the complementary term is at least
(1-a)log(1-a)>=-a. Take M=exp(2K+1), A0={W<=M}, and s0=pi(A0)>=1/2.
For 0<=f<=1 and g=C^t f define z=pi(g 1_A0)/s0. Then

\[
 \sum_x {\pi_x(g_x-z)^2\over\max(W_x,M)}
       \le J_t:={2\over\alpha(2t+1)}.               \tag{4}
\]

For completeness, the independence Dirichlet form is

\[
 \mathcal E_G(g,g)={1\over2}\sum_{x,y}
 {\pi_x\pi_y\over\max(W_x,W_y)}(g_x-g_y)^2.
\]

Restrict its y-sum to A0 and apply Jensen. This lower-bounds it by s0/2 times
the left side of (4). Since E_C>=alpha E_G/2 and s0>=1/2, that left side is
at most 8 E_C(g,g)/alpha. Spectral calculus and
(1-lambda)lambda^(2t)<=1/(2t+1), Var_pi(f)<=1/4 give (4). This is the same
anchor as the received first-hit proofs; its constants are included here so
that the new certificate is directly reusable.

For A={W<h}, 0<h<1/2, B=A^c, b=q(A), binary log-sum also gives

\[
 q(B)\ge\delta_h:=\exp[-(K+H_2(h))/(1-h)],\qquad
 H_2(h)=-h\log h-(1-h)\log(1-h).                     \tag{5}
\]

To see this, d=pi(A)<=h, and binary entropy bounds imply
K>=-H_2(h)-(1-h)log q(B). In particular q(B) is uniformly bounded away from
zero as h decreases to zero. For every x in A every G proposal to B is accepted.
Thus the actual G[A,A] row mass is exactly b, and the actual C escapes A with
probability at least alpha q(B)/2 at each step.

## 3. A finite absorbed-boundary energy lemma

Choose an arbitrary subset E of B and put e=q(E). On the finite set A union E
define G^E and L^E as follows: rows in A retain the entries of the original
G and L into A union E, with the other mass killed; rows in E are absorbing
identity rows. Put

\[
 P^E=(I+\alpha G^E+\beta L^E)/2.                     \tag{6}
\]

This is a proof process. There is **no renormalization of a killed row** and
no alteration of the sampler. Starting with the restricted subprobability
q 1_A (not q conditioned on A), its mass in E after N steps is exactly

\[
 \Pr_q(X_0\in A,\ \tau_B\le N,\ X_{\tau_B}\in E),
 \quad \tau_B=\inf\{j\ge0:X_j\in B\}.              \tag{7}
\]

Choose 0<c<1, theta=c eta<=1/2, p=1/(1-theta), D=diag(q_x^theta) on A union E.
For a row measure mu put v=mu D^{-1}; then

\[
 \|v\|_p^p=\sum_x q_x|\mu_x/q_x|^p.                \tag{8}
\]

Define the nonnegative endpoint deficit and energy multiplier

\[
 \Delta=[\beta F(c)-\alpha(1-b)]_+,\qquad
 \Gamma(e)={1\over2}+{2^{p-1}\over2}(1+\Delta+\alpha e).
                                                                    \tag{9}
\]

**Lemma 1.** For all nonnegative row vectors v,

\[
 \|vDP^ED^{-1}\|_p^p\le\Gamma(e)\|v\|_p^p.
                                                                    \tag{10}
\]

Consequently, for every integer N>=0,

\[
 \Pr_q(X_0\in A,\tau_B\le N,X_{\tau_B}\in E)
 \le b^{1-\theta}e^\theta\Gamma(e)^{N/p}.            \tag{11}
\]

Empty A or E gives zero on the relevant side and is handled directly.

### 3.1 Local energy: keep the real rejection diagonal

Write L_theta=DL^ED^{-1}. On A its row sum is at most 1+F(c); on E its
row sum is exactly 1. Indeed, for r=q_y/q_x<1 the positive change relative
to the original killed row is at most

\[
 Q_{xy}r^\eta(r^{-\theta}-1)
   =Q_{xy}(v_0^{1-c}-v_0)\le Q_{xy}F(c),\quad v_0=r^\eta.
\]

For r>=1 the change is nonpositive. The exact scalar maximum is
max_(0<=v0<=1)(v0^(1-c)-v0)=F(c); the accepted outflow remains subtracted
in the actual rejection diagonal. Sum Q_xy<=1.

Every counting column sum of L_theta is at most 2, including a column in E:
off-diagonal entries are at most Q_xy because
min(1,r^eta)r^(-theta)<=1, Q is symmetric stochastic, and the one diagonal
entry is at most 1 (exactly 1 for an absorbed E row). Counting-measure Jensen
therefore proves

\[
 \|vL_\theta\|_p^p\le 2^{p-1}
  \left[(1+F(c))\sum_{x\in A}|v_x|^p+
                         \sum_{x\in E}|v_x|^p\right].               \tag{12}
\]

In detail, at each y apply
(sum_x v_x L_theta,xy)^p <= (sum_x L_theta,xy)^(p-1)
sum_x |v_x|^p L_theta,xy, then sum over y. This avoids replacing the
different A and E row coefficients by a global operator-norm maximum.

### 3.2 Independence energy: retain actual killing

Rows of G^E have masses b+e on A and 1 on E. For y in A its q-density
column is at most 2b:

\[
 {1\over q_y}\sum_{x\in A}q_xG_{xy}
 =G_{yy}+\sum_{x\in A,x\ne y}q_x\min(1,W_y/W_x)
 \le b+(b-q_y)\le2b.
\]

Here G_yy<=b follows from the exact killed row mass. For y in E the q-density
column of G^E is **exactly 1+b**, because all A-to-E proposals are accepted
and E has its absorbing diagonal. Both column bounds are at most 2.

Apply weighted Jensen to f_x=mu_x/q_x and the weights q_x G^E_xy/q_y, then
sum in q_y. Using (8) and the actual row masses gives

\[
 \|vDG^ED^{-1}\|_p^p\le 2^{p-1}
 \left[(b+e)\sum_{x\in A}|v_x|^p+
                      \sum_{x\in E}|v_x|^p\right].                 \tag{13}
\]

This is not a counting-column estimate for G. No minimum-q or dimension
constant occurs in (12) or (13).

### 3.3 The mixture and accumulated absorption

Convexity of the p-th power, using the mixture weights 1/2,alpha/2,beta/2,
combines (12)-(13). The A energy coefficient is

\[
 {1\over2}+{2^{p-1}\over2}
       [\alpha(b+e)+\beta(1+F(c))],
\]

and the E coefficient is 1/2+2^(p-1)/2. Since the bracket on A is
1+beta F(c)-alpha(1-b)+alpha e, both are at most Gamma(e). This proves (10).

The initial transformed p-energy of q 1_A is exactly b. Iterate (10), then
apply Holder on E with q mass e. This gives (11). Absorbed mass from EVERY
first-hit time has accumulated in the same vector; there is no sum of separate
Lp norms and no factor 1/(1-rho) requiring strict contraction.

Gamma may exceed 1. The lemma is useful when theta and Delta are small and
only a short first-hit horizon is required. It is not a claim of endpoint
strict induced-norm contraction, which the previous obstruction excludes.

## 4. Full finite TV certificate, with all post-hit returns

Take n>=2, 0<=N<n, R>e, 0<h<1/2 and 0<d_test<=1. Keep the notation above,
and let a=pi(W>R),

\[
 J={2\over\alpha(2(n-N)+1)},\qquad
 \bar e=\min\left\{1-b,\ {a\over R}
       +{(N+1)(M/h+1)J\over d_{\rm test}^2}\right\},\quad
 \rho=1-\alpha(1-b)/2.                              \tag{14}
\]

**Lemma 2 (finite certificate).** With theta=c eta<=1/2,

\[
 \boxed{\begin{aligned}
 \|qC^n-\pi\|_{\rm TV}\le {}&a+\sqrt{(M+R)J}+d_{\rm test}+\bar e
       +b^{1-\theta}\bar e^\theta\Gamma(\bar e)^{N/p}
       +b\rho^N.
 \end{aligned}}                                                    \tag{15}
\]

The right side can be capped at one. This finite statement holds for any
admitted instance; it uses the actual a and b, not two independent KL budgets.

**Proof.** Fix an arbitrary test 0<=f<=1. For each j=0,...,N put
g_j=C^(n-j)f and use its own anchor z_j from (4). Define ONE bad boundary set

\[
 E=\{W>R\}\ \cup\ \bigcup_{j=0}^N
       \{h\le W\le R:\ |g_j-z_j|>d_{\rm test}\}\subset B.           \tag{16}
\]

On h<=W<=R, (4) gives
sum q_x(g_j-z_j)^2 <=(M/h+1)J. Chebyshev and q(W>R)<=a/R prove q(E)<=bar e.
The dependence of E on f is harmless: the mass bound is uniform over tests.

Let nu_j be the original, unnormalized first-hit distribution
Pr_q(X_j in .,tau_B=j). The exact decomposition is

\[
 qC^n=\sum_{j=0}^N\nu_j C^{n-j}+\sigma_n,\qquad
 \sigma_n(\Omega)=\Pr_q(\tau_B>N)\le b\rho^N.        \tag{17}
\]

After each first hit, the full original C propagates nu_j. Thus ALL later
exits, returns, revisits and local/global transitions are retained. Absorption
in Lemma 1 only counts the location of the first hit; it does not replace
this propagation.

Compare nu_j C^(n-j) with nu_j(Omega)pi. Its anchor scalar cancels. The sum
of nu_j integrals of |g_j-z_j| is at most

\[
 d_{\rm test}+q(E)+
 \Pr_q(X_0\in A,\tau_B\le N,X_{\tau_B}\in E).
\]

The term q(E) is the bad part of nu_0=q 1_B. Lemma 1 bounds the remaining
bad mass; its bound is increasing in e, so replace e by bar e.
On the stationary side, for each j, weighted Cauchy-Schwarz in (4) gives

\[
 \pi|g_j-z_j|\le a+\sqrt{(M+R)J}.
\]

Multiply by nu_j(Omega) and sum, using total mass at most one. The residual
sigma_n differs from its equal-mass stationary comparison by TV at most its
mass. These estimates prove (15), uniformly in f, hence in TV.

## 5. The joint information inequality

This lemma is the independent contribution of `/root/critical_budget`; the
complete derivation is included so that (2) has no hidden budget assumption.
Use A={W<h}, H={W>R}, b=q(A), a=pi(H), k=-log(1-b), and d=pi(A)<=hb.
For h+a<=1, three-cell log-sum gives

\[
 D(\pi\|q)\ge a\log R+d\log(d/b)
                   +(1-d-a)\log{1-d-a\over1-b}.                    \tag{18}
\]

The H contribution is at least a log R; replacing the complementary q mass
1-b-q(H) by the larger 1-b only lowers its term. As a function of d, the last
two terms have derivative
log[d(1-b)/(b(1-d-a))], which is nonpositive for d<=b(1-a). Since d<=hb and
h+a<=1, replacing d by hb lowers this bound. Consequently

\[
 D(\pi\|q)\ge a\log R+hb\log h+
                     (1-hb-a)\log{1-hb-a\over1-b}.                  \tag{19}
\]

At b=0 the same statement is read directly by continuity. Using
(1-x)log(1-x)>=-x yields the useful allocation inequality

\[
 \boxed{\displaystyle
 k+a\log R\le K+(h+a)(k+1)+h\log(1/h).}             \tag{20}
\]

Here k<=(K+H2(h))/(1-h) by (5), and a<=K/(log R-1) by (3). Thus the
remainder in (20) is uniformly controlled. This is one information budget:
the low-weight proposal mass costs k, and a retained high-weight tail costs
a log R. They cannot independently spend K.

## 6. Endpoint tuning of the finite certificate

Put L=log n and use the policy in Theorem (2), so u=eta L is asymptotic to
log L/c_*. For all sufficiently large n choose

\[
 h=u^{-4},\quad R=n/L^4,\quad d_{\rm test}=L^{-2},\qquad
 N=\left\lceil{8\over\alpha e^{-K}}\log L\right\rceil.              \tag{21}
\]

These are proof parameters, not adaptive sampler decisions. In particular
N=O(u)=o(n). Let b_n=q(W<h), k_n=-log(1-b_n), a_n=pi(W>R). Uniformly over
the native class,

\[
 k_n\le K+o(1),\quad a_n=O(L^{-1}),\quad
 k_n+a_n\log R\le K+o(u^{-2}).                      \tag{22}
\]

The last assertion follows from (20): its remainder is
O(u^-4 log u+L^-1)=o(u^-2). Positivity causes no minimum-atom restriction.

At c=c_* choose theta=c_*eta. For large n theta<=1/2, and since
beta F(c_*)=alpha exp(-K), (5) gives

\[
 0\le\Delta\le\alpha[e^{-K}-\delta_h]_+
       =O(h\log(1/h)).                              \tag{23}
\]

The cap 1-b in (14) is eventually inactive: its other entry is
O(n^-1 L^4 u^5), whereas 1-b>=delta_h tends to at least exp(-K).
That entry is also bounded below by a positive constant times n^-1 L^4,
so, uniformly over instances,

\[
 \log\bar e=-L+O(\log L),\qquad
 \bar e^\theta=\exp[-c_*u+o(1)].                   \tag{24}
\]

All accumulation errors vanish:

\[
 N\theta=O(u^2/L)=o(1),\quad
 N\Delta=O(u^{-3}\log u)=o(1),\quad N\bar e=o(1).
\]

Since p-1=O(theta), log Gamma(bar e)=O(theta+Delta+bar e), and therefore

\[
 \Gamma(\bar e)^{N/p}=1+o(1).                      \tag{25}
\]

This is the endpoint step that strict contraction could not supply. It does
not assert Gamma<1. It controls its small growth over the short first-hit
horizon, while storing every absorbed first hit in the same vector.

Moreover sqrt((M+R)J)=O(L^-2), d_test=L^-2, bar e=o(L^-1). For large n,
q(B)>=exp(-K)/2, so (21) gives b rho^N<=L^-2. Finally
sup_(0<=b<=1)|b^(1-theta)-b|=o(1). Inserting these facts in (15) proves the
uniform endpoint estimate

\[
 \|qC^n-\pi\|_{\rm TV}
     \le a_n+(b_n+o(1))e^{-c_*u}+o(L^{-1}).          \tag{26}
\]

The o terms here are uniform over all finite native instances. By itself
(26) is a SUM upper; the next step is necessary to obtain the correct maximum.

## 7. Separate entropy slack from critical capture

Consider ANY sequence of admitted instances at the prescribed policy and
horizons. The bounded k_n has a convergent subsequence, k_n->k in [0,K].

If k<K, choose a fixed c in (c_*,1) sufficiently close to c_* that
beta F(c)<alpha exp(-k). Such a choice exists by continuity and the strict
gap. Since q(B)=exp(-k_n), Delta in (9) is eventually zero for this c.
Use the SAME finite certificate and proof parameters (21), now with
theta=c eta. Equations (24)-(25) hold with c, and its transport term is

\[
 O(e^{-cu})=O(L^{-c/c_*})=o(L^{-1}).
\]

This uses a fixed strict margin supplied by the actual information slack,
not an endpoint substitution. Equations (15) and (22) yield

\[
 \limsup L\|qC^n-\pi\|_{\rm TV}\le K-k\le K.       \tag{27}
\]

If k=K, (22) forces L a_n->0, and b_n->b_K. Equation (26) then gives

\[
 \limsup L\|qC^n-\pi\|_{\rm TV}\le b_K e^{-c_*s}.  \tag{28}
\]

These cases exhaust all subsequential limits. To pass to the class supremum,
if the desired uniform limsup failed, select for each offending n a finite
instance within o(1/L) of its supremum and then a convergent subsequence of
k_n. Either (27) or (28) contradicts the violation. Therefore

\[
 \limsup L R_{\eta_n}(n)\le\max\{K,b_K e^{-c_*s}\}.  \tag{29}
\]

The unchanged Cycle4 lower gives the matching liminf, proving (2), including
existence. No deterministic-horizon risk was evaluated at an optional count,
and no diagonal monotonicity in n or eta was assumed.

## 8. Consequence, dependencies and remaining scope

The critical limit is the envelope proposed by the previous lower construction.
There is no admitted heterogeneous geometry above it under these hypotheses.
The reason it is a maximum is structural: a sequence that sustains endpoint
transport saturates the low-weight information cost and leaves no leading
high-weight tail entropy. If it reserves a positive entropy amount for that
tail, actual global killing is stronger and transport is asymptotically smaller.

The new finite argument combines three ingredients: (i) absorbed first-hit
energy retaining the actual global killing and local rejection diagonal,
(ii) one boundary set covering the bounded-test deviations at all relevant
first-hit times, and (iii) the single-budget allocation (20). Absorption is
used only for measuring a first-hit event; (17) keeps the subsequent full
chain. The one-step strict norm ceiling remains valid and is not contradicted.

For a target error A/log n with fixed A>K, (2) places the sharp transition
at s=log(b_K/A)/c_*: larger fixed offsets give eventual uniform accuracy,
and smaller offsets give an admitted adverse sequence. Equality alone does
not give a finite-n guarantee; the finite certificate (15) or a strict
asymptotic margin is needed. This is a complexity/robustness statement with
the original oracle and precision boundary, not a target-call speed comparison.

Dependencies: the native model, reversibility and anchor are established
capital, reproved where used above; the incoming operator theorem and its
ceiling stay accepted; the Cycle4 native branching and Q=I lower are used
unchanged. No new numerical evidence is needed to infer the limit. Exact
finite checks, if supplied, diagnose the new absorbed construction only.

The present theorem assumes r_0<1. At r_0=1 or r_0>1 the old finite-v lower
refinement does not apply, so (2) is not silently extended there. The fixed
positive-screen and first-order accuracy-policy laws remain closed for all
their original parameters. Nonreversible or adaptive kernels, deterministic
LG/GL schedules, empirical training losses and finite-precision errors remain
outside the theorem. Historical priority, formal verification and external
mathematical acceptance are not established by this source or its delivery.
