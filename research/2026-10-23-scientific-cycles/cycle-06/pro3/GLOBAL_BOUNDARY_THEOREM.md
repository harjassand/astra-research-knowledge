# Global-dominant critical sampling: weighted absorption and one crossing

Principal construction and complete synthesis: Astra PRO3. Scientific date:
22 October 2026, Australia/Brisbane. The principal owns the weighted absorbed
operator, its finite TV certificate and the complete upper. The independently
constructed one-crossing family is credited to `/root/heterogeneous_transport`;
the uniform information-allocation reduction and a distinct algebraic challenge
are credited to `/root/critical_budget`. Their original sources are preserved.
Source-bound review status is in STATUS.md. Historical originality and external
acceptance are separate from internal correctness.

## 1. Native class and exact result

Fix K>0 and alpha in (0,1); write beta=1-alpha. An instance consists of a
finite labelled space, strictly positive probability vectors pi,q with
D(pi||q)<=K, and a symmetric stochastic, target-independent Q. All objects
are fixed during a run. Supports may vary in the class supremum. Let W=pi/q,
G be independence Metropolis-Hastings with proposal q, and, for x!=y, set

\[
 L_\eta(x,y)=Q_{xy}\min\{1,(q_y/q_x)^\eta\}
       \min\{1,(\pi_y/\pi_x)(q_x/q_y)^\eta\},
 \qquad C_\eta=(I+\alpha G+\beta L_\eta)/2.       \tag{1}
\]

The diagonal of L is the actual rejection diagonal. The initial law is q.
TV is half l1; all logarithms are natural. Define

\[
 R_\eta(n)=\sup_{\rm native}\|qC_\eta^n-\pi\|_{\rm TV},
 \qquad r_0=\alpha e^{-K}/\beta.
\]

**Theorem 1 (global-dominant critical law, including equality).** Assume
r0>=1. For any deterministic across-run screen policy satisfying, for a fixed
real s,

\[
 u_n:=\eta_n\log n=\log\log n+s+o(1),
\]

one has

\[
 \boxed{\displaystyle
 \lim_{n\to\infty}(\log n)R_{\eta_n}(n)
 =\max\left\{K,{\beta\over\alpha}(e^K-1)e^{-s}\right\}.}       \tag{2}
\]

This closes the remaining native critical-amplitude regime. The previously
accepted interior law, for r0<1 and F(c*)=r0, remains unchanged:
eta_n log n=loglog n/c*+s+o(1) has amplitude
max{K,(1-exp(-K))exp(-c*s)}. The two laws agree at r0=1, where c*=1.
No uniform double limit in r0 and n is asserted here.

**Theorem 2 (small native adverse family).** For every fixed K>0 and
alpha in (0,1), the explicit three-state family in Section 7 obeys

\[
 (\log n)\|qC_{\eta_n}^n-\pi\|_{\rm TV}
 \longrightarrow {\beta\over\alpha}(e^K-1)e^{-s}.                 \tag{3}
\]

On exactly that same family, for m_n/n->t in (0,infinity),

\[
 \|qG^{m_n}-\pi\|_{\rm TV}\sim(\log n)^{-4}.                    \tag{4}
\]

In particular (4) holds at m_n=floor(alpha n/2), matching the expected number
of global attempts. This is an exact-law comparison, not a wall-time, cache
miss or target-call benchmark. A known three-state target can also be evaluated
in full at its actual cost and sampled directly. The construction does not
exclude that ordinary method or claim an oracle advantage.

The proofs use exact-real arithmetic. The sampler receives no free normalizer,
full target table, absorbed-chain simulator or empirical-to-population KL
certificate. Native query, proposal, uniform, cache and precision costs remain
in EXPERIMENT_CONTRACT.md. No finite-time TV ordering is inferred from a
Dirichlet or acceptance comparison.

## 2. Weighted finite absorption at theta=eta

Let 0<h<1, A={W<h}, B=A^c, b=q(A), E subset B and e=q(E).
On S=A union E define G^E,L^E to retain the original entries in rows A and
columns S, killing the other outgoing mass; rows E are identity rows. Put

\[
 P^E=(I+\alpha G^E+\beta L^E)/2.                  \tag{5}
\]

There is no row renormalization. For the original first hitting time
tau_B=inf{j>=0:X_j in B}, the exact absorption identity is

\[
 (q1_A)(P^E)^N(E)
 =\Pr_q(X_0\in A,\tau_B\le N,X_{\tau_B}\in E).                  \tag{6}
\]

This is a proof counter for first hits. Section 4 subsequently evolves the
full original chain, including all returns.

Fix 0<eta<=1/2, p=1/(1-eta), D=diag(q_x^eta) on S, and any w>=1.
For nonnegative row vectors v define the weighted p-energy

\[
 \mathcal E_w(v)=\sum_{x\in A}v_x^p+w\sum_{x\in E}v_x^p.
\]

If v=mu D^-1, then v_x^p=q_x(mu_x/q_x)^p. Define

\[
 \Delta_w=[\beta w-\alpha(1-b)]_+,\qquad
 \Gamma_w(e)={1\over2}+{2^{p-1}\over2}
                  (1+\Delta_w+\alpha we).                         \tag{7}
\]

**Lemma 3 (weighted absorption).** For every finite native instance,
every such E,w and nonnegative row v,

\[
 \mathcal E_w(vDP^ED^{-1})\le\Gamma_w(e)\mathcal E_w(v).           \tag{8}
\]

Consequently, for every integer N>=0,

\[
 \boxed{\displaystyle
 \Pr_q(X_0\in A,\tau_B\le N,X_{\tau_B}\in E)
 \le (b/w)^{1-\eta}e^\eta\Gamma_w(e)^{N(1-\eta)}.}              \tag{9}
\]

Empty A or E is handled directly. There is no support-size or minimum-q
constant. The lemma holds for arbitrary alpha,b, not only the asymptotic
global-dominant regime.

### Local estimate: a direct endpoint calculation

Let T=DL^ED^-1 and omega_x=1 on A, w on E. Every off-diagonal entry of T
is at most Q_xy. Indeed, for r=q_y/q_x,

\[
 r^{-\eta}\min(1,r^\eta)
       \min(1,(\pi_y/\pi_x)r^{-\eta})\le1.
\]

The actual diagonal is at most one; the absorbed E diagonal is exactly one.
Symmetry and stochasticity of Q imply every counting column sum of T is at
most two. For a row x in A, keeping its actual diagonal,

\[
 \sum_y\omega_yT_{xy}
 \le L_{xx}+w\sum_{y\ne x}Q_{xy}\le1+w.                          \tag{10}
\]

For x in E this weighted row sum is exactly w. Applying counting-column
Jensen at each output y and then multiplying by omega_y gives

\[
 \mathcal E_w(vT)\le2^{p-1}
 \left[(1+w)\sum_Av_x^p+w\sum_Ev_x^p\right].                    \tag{11}
\]

This directly establishes the theta=eta estimate. It does not substitute an
endpoint into the earlier strict-c scalar maximum or assert norm contraction.

### Global estimate: its own weighted density representation

Every independence proposal from A to B is accepted, since W_x<h<=W_y.
Thus G[A,A] has row mass exactly b and G_xx<=b for x in A.
The q-density column sum of G^E is at most 2b on A and exactly 1+b on E;
both are at most two. Explicitly, for y in A it is bounded by
G_yy+sum_(x in A,x!=y)q_x<=b+(b-q_y), while for y in E the absorbing
diagonal contributes one and the accepted A inflow contributes b.

The weighted actual row sums are

\[
 \sum_y\omega_yG^E_{xy}=b+we\ (x\in A),\qquad =w\ (x\in E).
\]

Apply Jensen with weights q_x G^E_xy/q_y to the density mu_x/q_x,
multiply the output by q_y omega_y, and sum. This proves

\[
 \mathcal E_w(vDG^ED^{-1})\le2^{p-1}
 \left[(b+we)\sum_Av_x^p+w\sum_Ev_x^p\right].                    \tag{12}
\]

This global argument is not a counting-column bound. Restricted q on S need
not have total mass one; Jensen uses the displayed column weights explicitly.

### Mixture and weighted Holder

Convexity under mixture weights 1/2,alpha/2,beta/2 combines (11)-(12).
The A coefficient is

\[
 {1\over2}+{2^{p-1}\over2}
  [\alpha(b+we)+\beta(1+w)]
 ={1\over2}+{2^{p-1}\over2}
  [1+\beta w-\alpha(1-b)+\alpha we].                              \tag{13}
\]

The E coefficient relative to its weighted input energy is
1/2+2^(p-1)/2. Both are at most Gamma_w(e), proving (8).

The initial transformed energy of q1_A is b. After N steps, weighted Holder
on E bounds its mass by e^(1-1/p)(b Gamma_w(e)^N/w)^(1/p), giving (9).
All first-hit times are accumulated in this one absorbed vector. No sum of
separate hit-time norms and no denominator r_b-1 occurs.

## 3. Canonical boundary weight and finite growth control

Write

\[
 r_b={\alpha(1-b)\over\beta},\qquad w=\max(1,r_b),\qquad
 \Delta=[\beta-\alpha(1-b)]_+.
\]

For this choice Delta_w=Delta. At r_b>=1, the additional boundary energy
is paid exactly by the actual global killing: beta w=alpha(1-b).
At r_b<1, w=1 and the deficit is explicitly charged. This avoids a singular
estimate when the finite h cutoff makes r_b slightly less than one.

Two useful uniform inequalities are

\[
 (b/w)^{1-\eta}\le b/w+\eta\le b/r_b+\eta,                        \tag{14}
\]

and

\[
 \Gamma_w(e)^{N/p}
 \le\exp\{N[\eta\log2+\Delta+\alpha we]\}.                       \tag{15}
\]

For (14), x^(1-eta)<= (1-eta)x+eta<=x+eta for x in [0,1]
by weighted AM-GM; take x=b/w and use w>=r_b>0. For (15), since
2^(p-1)(1+Delta+alpha we)>=1, Gamma is at most this latter quantity.
Then log(1+x)<=x and (p-1)/p=eta prove the assertion.
These are additive uniform controls, including when b tends to zero.

## 4. Finite TV certificate, preserving all full-chain returns

For n>=2, 0<=N<n, R>exp(1), 0<h<1/2, and 0<d_test<=1, put

\[
 M=e^{2K+1},\quad a=\pi(W>R),\quad
 J={2\over\alpha(2(n-N)+1)},\quad \rho=1-\alpha(1-b)/2,
\]

\[
 \bar e=\min\left(1-b,{a\over R}
       +{(N+1)(M/h+1)J\over d_{\rm test}^2}\right).                \tag{16}
\]

**Lemma 4 (complete finite certificate).** For any w>=1 and eta in (0,1/2],

\[
 \boxed{\begin{aligned}
 \|qC_\eta^n-\pi\|_{\rm TV}\le {}&a+\sqrt{(M+R)J}+d_{\rm test}
       +\bar e+b\rho^N\\
       &+(b/w)^{1-\eta}\bar e^\eta
                         \Gamma_w(\bar e)^{N(1-\eta)}.
 \end{aligned}}                                                   \tag{17}
\]

This uses actual a,b from the same instance. The right side may be capped
at one. It is a verifier bound, not an adaptive algorithm or new oracle.

For completeness, the interface is reproduced here. Both G and L are
pi-reversible, C is lazy, and the anchor A0={W<=M} has pi mass >=1/2.
For a bounded test 0<=f<=1, g=C^t f and z=pi(g1_A0)/pi(A0), the received
anchored smoothing estimate is

\[
 \sum_x{\pi_x(g_x-z)^2\over\max(W_x,M)}
       \le {2\over\alpha(2t+1)}.                                 \tag{18}
\]

Its short proof is in Appendix A. For j=0,...,N use g_j=C^(n-j)f and
its own anchor z_j, and form the ONE deterministic test-dependent set

\[
 E=\{W>R\}\cup\bigcup_{j=0}^N
          \{h\le W\le R:|g_j-z_j|>d_{\rm test}\}\subset B.
\]

Chebyshev applied to (18), and q(W>R)<=a/R, give q(E)<=bar e uniformly
over f. Let nu_j be the original unnormalized first-B-hit distribution.
The exact decomposition is

\[
 qC^n=\sum_{j=0}^N\nu_j C^{n-j}+\sigma_n,
 \qquad \sigma_n(\Omega)\le b\rho^N.                             \tag{19}
\]

Every original post-hit transition and return remains in C^(n-j).
Subtract nu_j(Omega)pi in each summand; its anchor scalar cancels.
Good first hits cost at most d_test in total. Bad time-zero hits cost q(E).
Bad hits from A are exactly (6), bounded by (9). Each stationary comparison
costs at most a+sqrt((M+R)J), multiplied by nu_j(Omega); their total mass is
at most one. The residual costs at most its mass. These observations give
(17), replacing e by bar e in its increasing bound. No optional count is
substituted into a deterministic-horizon risk formula.

## 5. One information budget and uniform critical tuning

The elementary entropy controls, proved in Appendix A, are

\[
 a\le {K\over\log R-1},\qquad
 k:=-\log(1-b)\le k_h:={K+H_2(h)\over1-h},                         \tag{20}
\]

and, when h+a<=1,

\[
 k+a\log R\le K+(h+a)(k+1)+h\log(1/h).                            \tag{21}
\]

The last inequality is the received single-budget lemma. It does not grant
K separately to the low-weight mass and the high-weight tail.

Set ell=log n and u=eta ell=log ell+s+o(1). For sufficiently large n take

\[
 h=u^{-4},\quad R=n/\ell^4,\quad d_{\rm test}=\ell^{-2},\quad
 N=\left\lceil{8\over\alpha e^{-K}}\log\ell\right\rceil.          \tag{22}
\]

All are proof parameters, fixed before a trajectory. In particular N=o(n).
Choose the canonical boundary weight w from Section 3. By (20),
q(B)>=exp(-k_h)=e^-K[1-O(h log(1/h))]. Under r0>=1 this implies

\[
 \Delta=O(h\log(1/h)),\qquad 1\le w\le\max(1,\alpha/\beta).
                                                                    \tag{23}
\]

The cap in (16) is uniformly inactive eventually. Its other argument is
between positive constants times n^-1 ell^4 and n^-1 ell^4 u^5.
Thus, uniformly over every finite native instance,

\[
 \log\bar e=-\ell+O(\log\ell),\qquad
 \bar e^\eta=e^{-u}(1+o(1)).                                      \tag{24}
\]

Also N eta=O(u^2/ell)->0, N Delta=O(u^-3 log u)->0, and N bar e->0.
Equation (15) gives Gamma_w(bar e)^(N/p)=1+o(1) uniformly. This proves
the accumulated estimate, rather than merely asserting Gamma_w->1.
The smoothing and test terms are O(ell^-2), bar e=o(ell^-1), and b rho^N
is O(ell^-2). By (14), the finite certificate therefore gives

\[
 \|qC^n-\pi\|_{\rm TV}
 \le a+\left[{b\over r_b}+o(1)\right]e^{-u}+o(\ell^{-1})
 =a+\left[{\beta\over\alpha}(e^k-1)+o(1)\right]e^{-u}
       +o(\ell^{-1}).                                             \tag{25}
\]

All error terms are uniform in support, probabilities and Q. In particular
no relative error is divided by b, and there is no margin assumption r_b>1.

## 6. Direct finite-budget maximization and the full-class upper

For clarity, the contributor's uniform reduction is given with explicit error.
Let a_max=K/(log R-1) and define the deterministic nonnegative allowance

\[
 \delta_n=(h+a_{\max})(k_h+1)+h\log(1/h)
                         +4a_{\max}\log\ell.                     \tag{26}
\]

It tends to zero. Equation (21) and ell-log R=4 log ell give
k+ell a<=K+delta_n, hence 0<=k<=K+delta_n. Multiplying (25) by ell, and
putting C_n=(beta/alpha)ell exp(-u), gives uniformly

\[
 \ell\|qC^n-\pi\|_{\rm TV}
 \le K+\delta_n-k+C_n(e^k-1)+o(1).                                \tag{27}
\]

The displayed function of k is convex. Its maximum on the ACTUAL finite
interval [0,K+delta_n] is one of the two endpoints, so

\[
 \ell\|qC^n-\pi\|_{\rm TV}
 \le\max\{K+\delta_n,C_n(e^{K+\delta_n}-1)\}+o(1).                \tag{28}
\]

Take the class supremum, then n->infinity. This proves the upper in (2),
with no assumption that a supremum is attained and no fixed support.
The optimization follows the proved transport estimate; it is not a premise
substituted for it. Mixed allocations cannot exceed this endpoint envelope.

## 7. A matching native one-crossing family and full-law sandwich

This section reproduces the independent contributor's construction so that
the main theorem has complete lower obligations in one source.
Write ell=log n, u=eta ell, delta=e^-K, b_K=1-delta and, eventually,

\[
 b=b_K-u^{-2},\quad p_n=\ell^{-4},\quad e={p_n\over n\ell^2},
 \qquad q=(b,e,1-b-e),
\]

\[
 \pi=(p_n/n^2,p_n,1-p_n-p_n/n^2),\qquad
 Q=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}.              \tag{29}
\]

The labels are root r, leaf l, core z. Q is literally the same symmetric
target-independent matrix for every n. Both probability vectors are positive
and normalized for sufficiently large n. Their weights obey
W_r=p_n/(b n^2)<1<W_z<W_l=n ell^2 eventually.
The root KL term is negative, while the core term is at most log(1/q_z).
Consequently

\[
 D(\pi\|q)\le p_n\log(n\ell^2)+\log(1/q_z)
 =K-e^K u^{-2}+o(u^{-2})<K.                                      \tag{30}
\]

Here p_n log(n ell^2)=O(ell^-3)=o(u^-2) and e=o(u^-2).
There is one budget and strict eventual admission.

Put sigma=(e/b)^eta. The forward local acceptance is exactly sigma and
the reverse exactly sigma/n^2, both from individual-state ratios. Hence

\[
 L_\eta=\begin{pmatrix}1-\sigma&\sigma&0\\
  \sigma/n^2&1-\sigma/n^2&0\\0&0&1\end{pmatrix},
\]

\[
 G=\begin{pmatrix}
 b&e&q_z\\
 \pi_r/W_l&1-(1-p_n)/W_l&\pi_z/W_l\\
 \pi_r/W_z&e&1-\pi_r/W_z-e
 \end{pmatrix}.                                                   \tag{31}
\]

These matrices retain their actual rejections and all reverse/global moves.
Define f=beta sigma/2, a_0=alpha q_z/2, c_0=f+alpha e/2,
v=a_0+c_0, and the actual leaf escape probability

\[
 d_l={\alpha(1-p_n)\over2n\ell^2}+{f\over n^2}.                  \tag{32}
\]

The exact probability, starting at the root, of first exiting to the leaf
by H=floor(n/2) is (c_0/v)[1-(1-v)^H]. Selecting paths which thereafter
remain at the leaf proves

\[
 \|qC^n-\pi\|_{\rm TV}
 \ge b{c_0\over v}[1-(1-v)^H](1-d_l)^n-p_n.                      \tag{33}
\]

This uses the full initial mass b and charges retention explicitly. Other
paths are retained in the actual chain; a lower event simply does not need them.

For the full-law upper, let tau_z be the first core hit, including time zero.
The probability not to hit the core by n is at most
e+b[c_0/v+(1-v)^n]. After a core hit at j, the ORIGINAL remaining law is
delta_z C^(n-j). Its TV error is at most 1-pi_z by contraction, including
all future excursions and returns. Thus

\[
 \|qC^n-\pi\|_{\rm TV}
 \le p_n(1+n^{-2})+e+b{c_0\over v}+b(1-v)^n.                    \tag{34}
\]

Now -log sigma=eta[ell+6 log ell+log b]=u+o(1), so
sigma=ell^-1 exp(-s)(1+o(1)). Also a_0->alpha e^-K/2>0, e/f->0, and

\[
 \ell b{c_0\over v}\longrightarrow
 {\beta\over\alpha}(e^K-1)e^{-s}.                               \tag{35}
\]

The waiting errors vanish exponentially, n d_l->0, and ell p_n,ell e->0.
Equations (33)-(35) prove (3) for the ACTUAL full law. This directly constructs
one strong crossing; no finite-spacing tree limit is invoked.

## 8. Ordinary lower and same-instance separation

The other minimax lower uses Q=I, making C=(1-alpha/2)I+(alpha/2)G.
For any fixed k<K let the rare target mass be p=k/log n and its proposal
mass e=p/[n(log n)^2], with two complementary positive masses. The KL tends
to k, so admission is eventual. G has nontrivial eigenvalue
1-1/[n(log n)^2]; thus the proposal-start C error is exactly

\[
 (p-e)\left(1-{\alpha\over2n(\log n)^2}\right)^n
 \sim{k\over\log n}.
\]

Increase k to K. This and (3) give the lower max in (2), completing the limit.
These are separate admitted families, not a combined construction spending K
twice. This elementary ordinary lower is an unchanged dependency, included
here for completeness rather than claimed as a new discovery.

For the one-crossing family (29), pure G satisfies for every integer m>=0

\[
 p_n-(m+1)e\le\|qG^m-\pi\|_{\rm TV}
 \le p_n(1+n^{-2})+{e\over1-b}+b^{m+1}.                          \tag{36}
\]

The lower is the leaf event: it can be occupied only if initially occupied
or proposed at least once. The upper is the same exact first-core argument:
at the root the leaf/core exit ratio is e/(1-b); later original-core
evolution costs at most 1-pi_z. If m/n->t in (0,infinity), both errors beyond
p_n in (36) are o(p_n), proving (4). Therefore the same-instance hybrid/IMH
TV ratio is asymptotic to

\[
 {\beta\over\alpha}(e^K-1)e^{-s}(\log n)^3.                      \tag{37}
\]

This supplies an explicit slowly growing deterioration on only three states.
It does not establish runtime or target-evaluation complexity: full caching
and an allowed three-point target enumeration must be charged and compared
honestly. The general pure-IMH minimax amplitude remains K, as proved in the
unchanged predecessor COMPARATOR.md and supplied again as source.

## 9. Consequence and scope

The endpoint amplitude has a mechanism change. In the interior r0<1, the
accepted many-level transport uses the full low-weight information budget.
In the present regime, actual global killing pays a boundary weight r_b;
its reciprocal is a smaller retained-capture amplitude. A three-state crossing
attains it. The single-budget exponential/linear allocation is convex, so
the worst case still lies at one of the two information endpoints.

The finite weighted lemma is reusable without the asymptotic r0 condition;
the exact all-class critical result uses it with r0>=1. At r0=1 the finite
cutoff defect is explicitly charged and accumulated. No divergent inverse
margin, c=1 substitution, disappearing error multiplied by an uncontrolled
horizon, or support-size constant is used.

For an allowed limiting amplitude A>K, the sharp fixed-offset transition in
this regime is s=log[(beta/alpha)(e^K-1)/A]. A strictly larger offset suffices
eventually, and a smaller offset has an admitted adverse family. Equality of
the limit alone is not a finite-n certification; use (17) or a strict margin.

This is robustness and finite-time law theory. The sampling primitive and
its target calls are unchanged. The result does not cover within-run adaptive
screens, nonreversible local kernels, deterministic compositions, empirical
KL training losses, an unbounded change of alpha with n, or finite-precision
acceptance error. Historical novelty, formal proof verification, external
acceptance and useful implementation remain separate claims.

## Appendix A. Reused anchor and entropy facts, with full obligations

The two reciprocal acceptance factors imply pi-reversibility of L; G is
pi-reversible by the usual MH identity. Hence C is reversible with spectrum
in [0,1]. The independence Dirichlet form is

\[
 \mathcal D_G(g,g)={1\over2}\sum_{x,y}
 {\pi_x\pi_y\over\max(W_x,W_y)}(g_x-g_y)^2.
\]

For H={W>R}, binary log-sum gives D(pi||q)>=a log R+(1-a)log(1-a)
>=a(log R-1), proving (20)'s high-tail bound. Taking M=e^(2K+1) gives
pi(A0)>=1/2. Restrict the y-sum in the Dirichlet form to A0 and apply Jensen
around z=pi(g1_A0)/pi(A0). This bounds the left side of (18) by
8 D_C(g,g)/alpha. For g=C^t f, 0<=f<=1, spectral calculus and
(1-lambda)lambda^(2t)<=1/(2t+1), Var_pi(f)<=1/4 prove (18).

For A={W<h}, d=pi(A)<=hb<=h. Binary log-sum and H2(d)<=H2(h) for h<1/2
give K>=-H2(h)-(1-h)log(1-b), proving k<=k_h.
For the joint bound, H={W>R} is disjoint from A. Three-cell log-sum gives

\[
 D(\pi\|q)\ge a\log R+d\log(d/b)
              +(1-d-a)\log{1-d-a\over1-b}.                       \tag{38}
\]

The actual middle q mass was replaced by the larger 1-b in the direction
lowering its contribution. The last two terms have derivative in d equal
to log[d(1-b)/(b(1-d-a))], nonpositive for d<=b(1-a).
Since d<=hb and h+a<=1, substitute d=hb to lower (38). Finally apply
(1-x)log(1-x)>=-x and b<=1 to obtain (21). When b=0 read the result directly
or by continuity. The selected cutoffs satisfy h+a<=1 eventually uniformly.

These arguments reproduce the precise received dependencies used here;
they do not reopen the already accepted interior proof.
