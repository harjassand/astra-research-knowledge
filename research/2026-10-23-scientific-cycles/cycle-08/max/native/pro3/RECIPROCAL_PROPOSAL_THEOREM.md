# Reciprocal proposal budgets preserve the sharp critical sampling law

Principal construction and synthesis: Astra PRO3. Scientific date: 22 October
2026, Australia/Brisbane. This is a declared extension of the finite proposal
class, not a new completion of the already accepted symmetric theorem.
The new operation is reverse-proposal weighted Jensen, with the actual local
rejection diagonal. The complete finite absorption and full-return argument
are below. The unchanged symmetric lower constructions are dependencies.
Independent checks and exact source identities are recorded in STATUS.md.

## 1. The enlarged class and result

Fix K>0, alpha in (0,1), and beta=1-alpha. An instance has a finite labelled
space, strictly positive probability vectors pi,q with population D(pi||q)<=K,
and a fixed target-independent row-stochastic Q with reciprocal off-diagonal
support: Q_xy>0 if and only if Q_yx>0. Q need not be symmetric, reversible,
q-invariant, doubly stochastic, or bounded in its counting column sums.
Support and proposal degrees may grow across instances. All parameters and
kernels stay fixed within each run; the initial law is q.

Let G be independence Metropolis-Hastings with proposal q. On a positive
off-diagonal proposal edge define

\[
 r_{xy}=\frac{q_yQ_{yx}}{q_xQ_{xy}},\qquad
 t_{xy}=\frac{\pi_yQ_{yx}}{\pi_xQ_{xy}},\qquad
 a_{xy}=\min(1,r_{xy}^{\eta})\min(1,t_{xy}/r_{xy}^{\eta}),
\]
\[
 \bar L_\eta(x,y)=Q_{xy}a_{xy},\qquad
 \bar L_\eta(x,x)=1-\sum_{y\ne x}Q_{xy}a_{xy},\qquad
 \bar C_\eta=(I+\alpha G+\beta\bar L_\eta)/2.                 \tag{1}
\]

Absent edges have zero transition and no undefined ratio is evaluated.
The actual diagonal includes self-proposals and both rejection stages.
The sampler has no free normalizer, complete target table or KL estimator.
Both Q_xy and Q_yx must actually be evaluable at their charged cost.
Define TV as half l1, all logs natural, and

\[
 \bar R_\eta(n)=\sup_{\rm enlarged\ class}\|q\bar C_\eta^n-\pi\|_{TV},
 \quad r_0=\alpha e^{-K}/\beta,\quad b_K=1-e^{-K},
 \quad F(c)=c(1-c)^{(1-c)/c}\ (0<c<1),\ F(1)=1.
\]

**Theorem 1 (sharp critical law without proposal symmetry).**
For fixed real s:

* If r0<1, let c_* in (0,1) be the unique solution F(c_*)=r0.
  For eta_n log n=loglog n/c_*+s+o(1),
  \[
  \lim_{n\to\infty}(\log n)\bar R_{\eta_n}(n)
       =\max\{K,b_K e^{-c_*s}\}.                              \tag{2}
  \]
* If r0>=1, including equality, for
  eta_n log n=loglog n+s+o(1),
  \[
  \lim_{n\to\infty}(\log n)\bar R_{\eta_n}(n)
       =\max\{K,(\beta/\alpha)(e^K-1)e^{-s}\}.                 \tag{3}
  \]

Thus arbitrary reciprocal proposal asymmetry cannot increase the previously
proved critical minimax risk. These are fixed-K, fixed-alpha statements;
no moving-alpha crossover, within-run adaptation, deterministic composition,
nonreversible target kernel or finite-precision guarantee is asserted.
The finite lemma below is stated for 0<eta<1, sufficient for both policies.

The bounds are transition-count robustness laws. Pure proposal-start IMH has
the better or equal general amplitude K under the same population-KL budget.
No implementation speedup follows from (2)-(3). The three-state adverse
comparison in the unchanged predecessor still belongs to this larger class.

## 2. Full weighted local energy from reverse proposal probabilities

This is the new load-bearing finite operation. Let A,E be disjoint subsets,
S=A union E. Form L^E by retaining the ACTUAL Lbar entries in rows A and
columns S, killing the remaining mass, and making rows E absorbing. Do not
renormalize killed rows. Choose

\[
 0<\eta<1,\quad 0<\theta\le\eta,\quad\theta\le1/2,
 \quad p=(1-\theta)^{-1},\quad D=\operatorname{diag}(q_x^\theta)_{x\in S}.
\]

For any w>=1 put omega_x=1 on A and w on E, and

\[
 \mathcal E_w(v)=\sum_{x\in S}\omega_x|v_x|^p,
 \quad \tau=p(1-\theta/\eta)\in[0,1),\quad
 H_w=\sup_{0<z\le1}(w z^\tau-z).                              \tag{4}
\]

When tau=0 this supremum is w; no value 0^0 or finite attainment is assumed.
For 0<tau<1 it is explicitly

\[
 H_w=\begin{cases}
 w(1-\tau)(w\tau)^{\tau/(1-\tau)},&w\tau\le1,\\
 w-1,&w\tau\ge1.
 \end{cases}                                                  \tag{5}
\]

The formulas agree at equality. In particular H_w>=w-1>=0.

**Lemma 2 (reverse-proposal local energy).** With T=D L^E D^-1,

\[
 \mathcal E_w(vT)\le2^{p-1}
       \left[(1+H_w)\sum_A|v_x|^p+w\sum_E|v_x|^p\right]        \tag{6}
\]

for every row vector v. The constant is independent of support size, proposal
degree, minimum atom, proposal asymmetry and any invariant measure of Q.

**Proof.** At each output y define auxiliary Jensen coefficients B_xy:
off diagonal use Q_yx when x is in A; on the diagonal use the actual Lbar_xx
for x in A and one for x in E; all other entries are zero. Reciprocal support
ensures B_xy=0 implies T_xy=0. Zero diagonal terms are simply omitted.
Because these coefficients use the OUTGOING row of Q at y,

\[
 \sum_{x\in S}B_{xy}\le1+\sum_{x\ne y}Q_{yx}\le2.             \tag{7}
\]

This does not assume a bounded counting column of Q or T. Weighted Jensen
and the triangle inequality give

\[
 |(vT)_y|^p\le2^{p-1}
       \sum_{x:B_{xy}>0}|v_x|^p\frac{T_{xy}^p}{B_{xy}^{p-1}}.
                                                                    \tag{8}
\]

For an off-diagonal retained edge from A, using p-1=theta p,

\[
 \frac{T_{xy}^p}{B_{xy}^{p-1}}
 =\frac{Q_{xy}^p a_{xy}^p(q_x/q_y)^{\theta p}}{Q_{yx}^{p-1}}
 =Q_{xy}a_{xy}^p r_{xy}^{-\theta p}.                            \tag{9}
\]

The diagonal powered coefficient remains exactly Lbar_xx or the absorbed
one. Multiply (8) by omega_y and sum over outputs. For input x in A, its
coefficient is bounded, using the true rejection diagonal, by

\[
 \bar L_{xx}+\sum_{y\in S,y\ne x}\omega_yQ_{xy}a_{xy}^p r_{xy}^{-\theta p}
 \le1+\sum_{y\in S,y\ne x}Q_{xy}
                      (w a_{xy}^p r_{xy}^{-\theta p}-a_{xy}).   \tag{10}
\]

The accepted outflow into the killed complement is nonpositive in this
expression and was dropped only after subtraction. For r>=1 and 0<=a<=1,
the bracket is at most (w-1)a<=w-1<=H_w. For 0<r<1, the permitted
interval is 0<=a<=r^eta. The bracket is convex in a, so its maximum is at
zero or r^eta. At the latter endpoint, with z=r^eta, it is

\[
 w r^{p(\eta-\theta)}-r^\eta=w z^\tau-z\le H_w.
\]

Since sum_{y!=x}Q_xy<=1, (10) is at most 1+H_w. For x in E the only
entry is its absorbing diagonal and its weighted coefficient is w. This
proves (6). Maximizing the scalar function gives (5). All calculations use
finite nonnegative sums; absent edges and empty sets are harmless. QED.

### The two interfaces needed for the critical law

For w=1 and theta=c eta, 0<c<1, set

\[
 c_{\rm eff}=1-\tau=\frac{c(1-\eta)}{1-c\eta}\le c.
\]

Equation (4) gives H_1=F(c_eff)<=F(c), since
F(c)=sup_{0<z<=1}(z^(1-c)-z) is increasing. Thus the complete prior
interior LOCAL energy inequality, not just its pointwise bound, remains
valid with its original coefficient 1+F(c).

For theta=eta, tau=0 and H_w=w for EVERY w>=1. Thus the complete previous
weighted endpoint energy coefficient 1+w also remains valid. No substitution
of c=1 into an unproved strict-c statement is used. The finite c_eff and c
are not asserted equal, and a scalar norm extremum is not called a mixing lower.

## 3. Actual killed-global mass and accumulated first-hit capture

Now let W=pi/q, 0<h<1, A={W<h}, B=A^c, b=q(A), E subset B, e=q(E).
On S=A union E form G^E analogously and put

\[
 P^E=(I+\alpha G^E+\beta L^E)/2.
\]

Start this proof counter at the restricted subprobability q1_A. If tau_B
is the first original-chain hit of B, its exact absorbed mass at time N is

\[
 (q1_A)(P^E)^N(E)=\Pr_q(X_0\in A,\tau_B\le N,X_{\tau_B}\in E). \tag{11}
\]

Every IMH proposal from A to B is accepted. Therefore G[A,A] has actual
row mass b and G_xx<=b on A. The q-density column sums of G^E are at most
2b on A and exactly 1+b on E, both at most two. The weighted ACTUAL row
sums are b+we on A and w on E. With v=mu D^-1 one has
|v_x|^p=q_x|mu_x/q_x|^p. Jensen in the density representation, using
coefficients q_x G^E_xy/q_y, consequently gives

\[
 \mathcal E_w(vDG^ED^{-1})\le2^{p-1}
          [(b+we)\sum_A|v_x|^p+w\sum_E|v_x|^p].                \tag{12}
\]

This global step remains distinct from the local reverse-proposal Jensen.
It is independent of Q and retains global killing, self-proposals and
rejections. Applying convexity to the actual lazy mixture yields

\[
 \mathcal E_w(vDP^ED^{-1})\le\Gamma_{\theta,w}(e)\mathcal E_w(v),
\]
\[
 \Gamma_{\theta,w}(e)=\frac12+\frac{2^{p-1}}2
   \left(1+[\beta H_w-\alpha(1-b)]_++\alpha we\right).          \tag{13}
\]

Indeed the A coefficient in the bracket is
alpha(b+we)+beta(1+H_w)=1+beta H_w-alpha(1-b)+alpha we;
the E coefficient relative to its weighted input is one. The positive
part in (13) bounds both. The initial transformed energy is exactly b.
Iterate (13) and apply weighted Holder on E to obtain, for every N>=0,

\[
 \boxed{\Pr_q(X_0\in A,\tau_B\le N,X_{\tau_B}\in E)
 \le(b/w)^{1-\theta}e^\theta
                    \Gamma_{\theta,w}(e)^{N(1-\theta)}.}       \tag{14}
\]

Empty A or E gives zero directly. All first-hit times accumulate in one
absorbed vector. This matrix is a proof counter, never a free modified
sampler. In particular (14) has not discarded any full-chain return.

## 4. Finite full-chain certificate and one population information budget

For n>=2, 0<=N<n, R>exp(1), 0<h<1/2 and 0<d_test<=1, define

\[
 M=e^{2K+1},\quad a=\pi(W>R),\quad
 J=\frac{2}{\alpha(2(n-N)+1)},\quad\rho=1-\alpha(1-b)/2,
\]
\[
 \bar e=\min\left\{1-b,\frac aR+
          \frac{(N+1)(M/h+1)J}{d_{\rm test}^2}\right\}.        \tag{15}
\]

**Lemma 3 (full-return certificate).** For all parameters admitted in
Lemma 2 and w>=1,

\[
 \begin{split}
 \|q\bar C_\eta^n-\pi\|_{TV}\le{}&a+\sqrt{(M+R)J}+d_{\rm test}
          +\bar e+b\rho^N\\
 &+(b/w)^{1-\theta}\bar e^\theta
                      \Gamma_{\theta,w}(\bar e)^{N(1-\theta)}.
 \end{split}                                                    \tag{16}
\]

The right side can be capped at one. This uses the same instance's a,b.
Proof sets and normalized tables are verifier objects, not sampler access.

**Proof with all returns.** Reciprocal acceptance factors give
a_xy/a_yx=t_xy, hence pi-reversibility of Lbar. G is reversible, so Cbar
is reversible with spectrum in [0,1]. The binary log-sum bound gives
a<=K/(log R-1); therefore A0={W<=M} has pi mass at least 1/2.
For 0<=f<=1, g=Cbar^t f and z=pi(g1_A0)/pi(A0), the IMH Dirichlet form

\[
 \mathcal D_G(g,g)=\frac12\sum_{x,y}
       \frac{\pi_x\pi_y}{\max(W_x,W_y)}(g_x-g_y)^2
\]

and D_Cbar>=alpha D_G/2 give

\[
 \sum_x\frac{\pi_x(g_x-z)^2}{\max(W_x,M)}
        \le\frac{2}{\alpha(2t+1)}.                             \tag{17}
\]

To check constants, restrict the y-sum to A0 and apply Jensen around z;
the left side is at most 8 D_Cbar(g,g)/alpha. Spectral calculus with
(1-lambda)lambda^(2t)<=1/(2t+1) and Var_pi(f)<=1/4 proves (17).
No initial L2 density or assumption on Q's stationary law is needed.

For j=0,...,N use g_j=Cbar^(n-j)f and its own anchor z_j. Form one set

\[
 E=\{W>R\}\cup\bigcup_{j=0}^N
       \{h\le W\le R:|g_j-z_j|>d_{\rm test}\}\subset B.
\]

Chebyshev and (17) give q(E)<=bar e. If nu_j is the original unnormalized
first-B-hit measure, the exact identity is

\[
 q\bar C^n=\sum_{j=0}^N\nu_j\bar C^{n-j}+\sigma_n,
 \qquad\sigma_n(\Omega)\le b\rho^N.                            \tag{18}
\]

Each hit is followed by the ORIGINAL Cbar, with all later excursions,
global attempts and returns. On the test side, subtract nu_j(Omega)pi,
cancel its anchor scalar, and sum. Good hits cost at most d_test in total;
bad initial hits cost q(E); later bad first hits cost (14). The stationary
comparison is at most a+sqrt((M+R)J), times first-hit mass whose total is
at most one. The residual costs its mass. These give (16), uniformly in f.

The information controls needed below are also independent of Q. Put
k=-log(1-b), k_h=(K+H_2(h))/(1-h). Binary log-sum gives

\[
 a\le a_{\max}:=K/(\log R-1),\qquad k\le k_h.                  \tag{19}
\]

For h+a<=1, three-cell log-sum on A,{W>R},their complement gives

\[
 k+a\log R\le K+(h+a)(k+1)+h\log(1/h).                       \tag{20}
\]

For completeness, d=pi(A)<=hb. The log-sum lower is
a log R+d log(d/b)+(1-d-a)log((1-d-a)/(1-b)). The derivative of the last
two terms in d is log[d(1-b)/(b(1-d-a))], nonpositive for
d<=b(1-a). Substitute d=hb, then use (1-x)log(1-x)>=-x and b<=1.
This proves (20), with b=0 direct or by continuity. The binary estimate
for k uses -H_2(d)>=-H_2(h) and 1-d>=1-h. There is only ONE KL budget.
QED.

## 5. Uniform asymptotic upper: interior

Suppose r0<1 and u=eta log n=loglog n/c_*+s+o(1). Write ell=log n.
Use the same deterministic proof cutoffs

\[
 h=u^{-4},\quad R=n/\ell^4,\quad d_{\rm test}=\ell^{-2},\quad
 N=\left\lceil\frac{8}{\alpha e^{-K}}\log\ell\right\rceil.    \tag{21}
\]

Take w=1, theta=c_* eta, eventually <=1/2 and eta<1. Lemma 2 gives
H_1<=F(c_*), so (13) is at most the predecessor multiplier with
Delta=[beta F(c_*)-alpha(1-b)]_+=O(h log(1/h)), uniformly, by (19).
The cap in (15) is inactive eventually. Its other argument lies between
positive constants times n^-1 ell^4 and n^-1 ell^4 u^5. Hence

\[
 \log\bar e=-\ell+O(\log\ell),\quad
 \bar e^\theta=e^{-c_*u}(1+o(1)),\quad
 N\theta+N\Delta+N\bar e=o(1).                                \tag{22}
\]

Since log Gamma=O(theta+Delta+bar e), the accumulated Gamma^(N/p) is
1+o(1), not merely Gamma->1. The other terms in (16) are o(1/ell):
the square-root and d_test are O(ell^-2), bar e is exponentially small,
and b rho^N<=ell^-2 eventually. The additive power bound
x^(1-theta)<=x+theta on [0,1] handles small b uniformly. Thus

\[
 TV(q\bar C^n,\pi)\le a+(b+o(1))e^{-c_*u}+o(1/\ell).          \tag{23}
\]

Equations (19)-(20) imply k<=K+o(1) and k+a log R<=K+o(u^-2),
uniformly. Along ANY sequence of instances choose a subsequence where
k->k_infty in [0,K]. If k_infty<K, continuity of F permits fixed
c in (c_*,1) with beta F(c)<alpha exp(-k_infty). Apply the SAME finite
certificate with theta=c eta,w=1. Its Delta is eventually zero, its
accumulated multiplier again tends to one, and its transport term is
O(exp(-cu))=O(ell^(-c/c_*))=o(1/ell). The remaining amplitude is at
most K-k_infty<=K. If k_infty=K, (20) forces ell a->0 and b->b_K;
(23) has limsup amplitude at most b_K exp(-c_*s).

If the class-supremum upper failed, select near-supremum finite instances
within o(1/ell) on the violating horizons and then such a subsequence;
either case is a contradiction. This proves the upper in (2) over ALL
reciprocal proposals. No fixed degree, finite support cap or minimum reverse
probability appears in an error term.

## 6. Uniform asymptotic upper: global dominance and equality

Suppose r0>=1 and u=eta ell=log ell+s+o(1). Use (21), now theta=eta
and w=max(1,r_b), r_b=alpha(1-b)/beta. The new local lemma gives
H_w=w exactly; therefore

\[
 \Delta_w=[\beta w-\alpha(1-b)]_+
       =[\beta-\alpha(1-b)]_+=O(h\log(1/h)).                    \tag{24}
\]

This includes r0=1, where the finite h cutoff need not give r_b>=1.
No division by r_b-1 or uniform strict margin is used. Also
1<=w<=max(1,alpha/beta). The additive power and accumulated controls are

\[
 (b/w)^{1-\eta}\le b/w+\eta\le b/r_b+\eta,
 \quad\Gamma^{N/p}\le
       \exp\{N[\eta\log2+\Delta_w+\alpha w\bar e]\}=1+o(1).
                                                                    \tag{25}
\]

Here N eta=O(u^2/ell), N Delta_w=O(u^-3 log u), N bar e=o(1), all
uniform. The same estimate on log bar e as (22) gives

\[
 TV(q\bar C^n,\pi)\le a+
       [(\beta/\alpha)(e^k-1)+o(1)]e^{-u}+o(1/\ell).            \tag{26}
\]

The single-budget inequality gives k+ell a<=K+delta_n for

\[
 \delta_n=(h+a_{\max})(k_h+1)+h\log(1/h)
                          +4a_{\max}\log\ell\longrightarrow0.
\]

Thus k lies in [0,K+delta_n]. Let C_n=(beta/alpha)ell exp(-u).
Multiplying (26) by ell gives a uniform upper
K+delta_n-k+C_n(e^k-1)+o(1). This function is convex in k, so its
maximum on the ACTUAL finite interval is an endpoint:

\[
 \ell\,TV(q\bar C^n,\pi)
 \le\max\{K+\delta_n,C_n(e^{K+\delta_n}-1)\}+o(1).             \tag{27}
\]

Taking the class supremum then the limit proves the upper in (3).
The convex reduction follows the proved transport premise; it does not
replace it or allocate K twice.

## 7. Matching admitted lowers: exact inclusion, no new lower assumption

Every symmetric stochastic Q has reciprocal support. For such Q, r=q_y/q_x
and t=pi_y/pi_x, so (1) is IDENTICALLY the native accepted kernel including
its diagonal. Therefore every previous positive finite lower instance,
with the same target-independent Q and the same cost contract, belongs to
the present class and has the same law at every finite time.

The ordinary Q=I two-state lower gives amplitude K in both regimes. For
r0<1 the unchanged accepted Cycle4 critical tree lower gives
b_K exp(-c_*s). Its full source and necessary branching theorem are inside
the original source chain; readable copies are supplied. They use actual
per-vertex masses, corrected reverse D factor, integer-depth control, exact
level quotient, one KL budget and an event retaining the entire leaf union.
They do not use a one-step norm extremizer as a mixing lower.

For r0>=1 the unchanged Cycle6 three-state proof gives
(beta/alpha)(e^K-1)exp(-s). In detail let ell=log n,u=eta ell,
b=b_K-u^-2,p_n=ell^-4,e=p_n/(n ell^2), and

\[
 q=(b,e,1-b-e),\quad
 \pi=(p_n/n^2,p_n,1-p_n-p_n/n^2),\quad
 Q=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}.
\]

All probabilities are positive eventually and
D(pi||q)<=p_n log(n ell^2)+log(1/(1-b-e))<K. The exact local forward
screen is sigma=(e/b)^eta, reverse sigma/n^2. With
f=beta sigma/2,a0=alpha(1-b-e)/2,c0=f+alpha e/2,v=a0+c0,
d_l=alpha(1-p_n)/(2n ell^2)+f/n^2, the full law satisfies

\[
 b(c0/v)[1-(1-v)^{\lfloor n/2\rfloor}](1-d_l)^n-p_n
 \le TV\le p_n(1+n^{-2})+e+b(c0/v)+b(1-v)^n.
\]

The lower selects retained leaf paths; the upper propagates the ORIGINAL
chain after its first core hit and charges error at most 1-pi_core.
Their common amplitude is as stated. On the same family pure IMH has
TV~ell^-4 for m/n->t>0, including m=floor(alpha n/2).
These already-proved sources are preserved unchanged and not rerun.

Combine exact subclass inclusion with the new upper. This proves both
limits and closes the declared reciprocal-proposal critical question.
Separate admitted lower families yield a maximum, never a sum of budgets.

## 8. What the theorem establishes and what it does not

The controlling local quantity is a reciprocal proposal FLOW ratio,
q_y Q_yx/(q_x Q_xy). Reverse-proposal Jensen turns a possibly huge incoming
column into a bounded outgoing proposal row, while the actual rejection
diagonal pays accepted outflow. This is why the support-uniform critical
law survives nonreversible and highly asymmetric proposal matrices Q,
even though the corrected target kernel itself remains reversible.

The distinction is substantive. The separately constructed source
`contributors/PROPOSAL_RATIO_NECESSITY.md` considers a different, still
pi-reversible factorization whose first screen omits Q_yx/Q_xy. It gives
a positive worst-case error floor for every fixed eta>0. That counterexample
does not refute (2)-(3); it isolates an actual information/operation premise.

The easy factorized detailed-balance identity is established delayed-acceptance
theory. Jensen/Holder and the IMH Dirichlet anchor are standard tools.
The present contribution is the full finite weighted absorption estimate
under arbitrary reciprocal proposals, its uniform integration with the one-KL
and full-return proof, and the exact enlarged-class law. Historical priority,
external mathematical acceptance and formal verification are unestablished.

The theorem is not an algorithmic acceleration. Computing both proposal
probabilities, sampling Q, evaluating q, obtaining target ratios after the
first screen, uniforms, caching and numerical precision have their real costs.
Some proposal mechanisms cannot supply a cheap reverse probability. They
do not acquire that access through this theorem. Ordinary IMH, and complete
target enumeration when naturally available, remain admitted comparators.
No empirical training loss is converted to population KL. Absorption and
test-dependent boundary sets are only proof operations.

## 9. Source dependencies and receiving use

Exact predecessor: Astra_Amplification_Cycle6_PRO3_20261022.zip,
2,234,694 bytes, SHA256
`89328a974f6d0ed862a9e990fc4614fbb15d78ad48565461f25b4448c097601c`.
The attached common packet's original is byte-identical to the latest local
owner source. That whole ZIP is preserved under sources/; no old source is
edited. It contains Cycle5, Cycle4 and their original accepted proof chain.

Actually reused mathematics: anchored bounded-test smoothing, accumulated
absorbed first hits, the test-set union and original post-hit propagation,
the one-KL information inequality, interior allocation argument, global
boundary weight, and matching symmetric native lower constructions.
The new reverse-proposal representation makes these dependencies usable in
a strictly broader class. This is scientific receiving use, not evidence
that a prompting tactic, numerical instrument or agent quota caused discovery.

Read this file with the exact counterconstruction, information/cost contract,
finite-check record and independent review scopes. The continuation seed
states the next selected question separately; no unproved extension is part
of Theorem 1. Max owns programme integration; delivery is not acceptance.
