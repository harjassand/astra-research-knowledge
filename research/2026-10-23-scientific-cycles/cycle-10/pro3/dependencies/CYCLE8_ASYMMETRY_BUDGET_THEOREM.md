# A sharp convergence criterion under a public proposal-asymmetry budget

Principal: Astra PRO3. Scientific date: 22 October 2026, Australia/Brisbane.
This is the Cycle8 principal construction and integrated proof. It continues
the accepted reciprocal-proposal programme without reopening its critical
laws. Source-bound challenge and acceptance status are recorded separately
in STATUS.md. All logarithms are natural.

## 1. Exact class, quantifiers, and result

Fix K>0 and 0<alpha<1, and write beta=1-alpha. At each integer horizon n,
the public deterministic policy consists of finite real numbers

\[
 0<\eta_n<1,\qquad 0\le\kappa_n<\infty,\qquad 0\le A_n<\infty.
\]

No uniform bound on kappa_n or A_n, or positive lower bound on eta_n, is
assumed. These parameters are fixed throughout that run.

An admitted instance has a finite labelled space, strictly positive
probability vectors pi,q, one population information budget D(pi||q)<=K,
and a fixed target-independent row-stochastic proposal Q with reciprocal
off-diagonal support. The public promise is

\[
 A(Q):=\max_{\substack{x\ne y\\Q_{xy}>0}}
             |\log(Q_{yx}/Q_{xy})|\le A_n.                    \tag{1}
\]

The maximum over no off-diagonal edges is defined to be zero. Support size,
degree, atom sizes, and forward/reverse proposal probabilities have no
additional restrictions. They can change between instances and horizons.
Target independence means Q is fixed without observing the target; our lower
construction first specifies Q from public quantities and labels, and then
specifies pi. It is not an assumption that pi cannot be an adverse member
of the class for that Q.

Let G be independence Metropolis-Hastings with proposal q and target pi.
For a positive off-diagonal proposal edge, define

\[
 R_{xy}=Q_{yx}/Q_{xy},\quad r_{xy}=(q_y/q_x)R_{xy},\quad
 t_{xy}=(\pi_y/\pi_x)R_{xy},
\]
\[
 S_{xy}=(q_y/q_x)^{\eta_n}R_{xy}^{\kappa_n},\quad
 a_{xy}=\min(1,S_{xy})\min(1,t_{xy}/S_{xy}),
\]
\[
 L_{xy}=Q_{xy}a_{xy},\quad
 L_{xx}=1-\sum_{y\ne x}L_{xy},\quad
 C=(I+\alpha G+\beta L)/2.                                  \tag{2}
\]

Absent edges require no ratio evaluation. These are the true rejection
diagonals. The chain starts from q. The full risk is

\[
 \mathscr R_n=\sup_{\substack{\text{finite admitted instances}\\A(Q)\le A_n}}
                       \|qC^n-\pi\|_{\rm TV},               \tag{3}
\]

where TV is half l1. Define the two public scales

\[
 D_n=|\kappa_n-\eta_n|A_n,\qquad
 u_n=\eta_n\log n,\qquad v_n=\frac{u_n}{1+D_n}.               \tag{4}
\]

**Theorem 1 (exact criterion for uniform convergence).**
For every such deterministic policy sequence,

\[
 \boxed{\mathscr R_n\longrightarrow0
   \quad\Longleftrightarrow\quad
   \frac{\eta_n\log n}{1+|\kappa_n-\eta_n|A_n}
                         \longrightarrow\infty.}           \tag{5}
\]

Equivalently, both u_n->infinity and D_n=o(u_n) are necessary and sufficient.
This is a sharp condition on convergence, not an exact rate formula for
every policy and not an exact positive error floor.

**Theorem 2 (finite upper and a sufficient ordinary-optimal regime).**
Let

\[
 r_0=\alpha e^{-K}/\beta,\qquad
 \varepsilon_0=\min\{1/4,r_0/8\},\qquad c_0=\varepsilon_0/4.
\]

There are C_0<infinity and n_0, depending only on K and alpha, such that for
every admitted policy triple at every n>=n_0, with ell=log n,

\[
 \boxed{\mathscr R_n\le
  \frac K{\ell-4\log\ell-1}+\frac{C_0}{\ell^2}
                         +2e^{-c_0 v_n}.}                 \tag{6}
\]

The right side may be capped at one. In particular,

\[
 \frac{v_n}{\log\log n}\longrightarrow\infty
       \quad\Longrightarrow\quad
       (\log n)\mathscr R_n\longrightarrow K.              \tag{7}
\]

Condition (7) is sufficient, not claimed necessary for amplitude K.
It does not identify the sharp transport exponent or critical amplitude
when v_n is comparable to loglog n.

**Corollary 3 (fixed powers).** For fixed 0<eta<1 and fixed finite
kappa>=0 with kappa!=eta,

\[
 \mathscr R_n\to0\quad\Longleftrightarrow\quad A_n=o(\log n).
                                                                    \tag{8}
\]

In particular, any fixed finite public asymmetry bound permits arbitrary
fixed mismatch and still gives (log n) R_n -> K. This conclusion uses a
genuine restriction on the admitted Q. It does not contradict the Cycle7
positive floor for mismatched powers over unrestricted reciprocal Q.
If kappa_n=eta_n, (5) reduces to the previously established
eta_n log n -> infinity condition. No new completion of that case is claimed.

The mathematical model is exact real arithmetic. Population K is supplied;
it is not inferred from target evaluations or training loss. Native q
sampling, local proposals, target and proposal probability evaluations,
indices, caching, and precision retain their actual costs. A public bound
on proposal asymmetry is not a finite-precision error model.

## 2. Accepted dependency and what changes

The accepted Cycle7 file RECIPROCAL_PROPOSAL_THEOREM.md is an explicit
dependency, preserved inside sources/Astra_Amplification_Cycle7_PRO3_20261022.zip.
Its SHA256 is

584c2fcbedcead37578b91596ace85eeb75426537d564cdd646d44831f4dbc6a.

Its finite full-return smoothing argument (Lemma 3) uses only reversibility,
laziness, the IMH component, the one KL budget, and a valid absorbed local
energy bound. Its proof is reproduced at the interface below so the changed
hypothesis is visible. The accepted earlier critical amplitudes are not used
to infer the new asymptotic criterion.

The two new obligations are different. First, discrepancy must be carried
through the actual local rejection energy and the accumulated first-hit
multiplier. Second, an adverse scalar screen must be realized by a native
proposal with BOTH row budgets, the public edge bound, and one KL budget.
Sections 3-5 meet the first obligation. Sections 6-8 meet the second. The
bounded-u branch of necessity uses an already valid symmetric three-state
family, solely to exhaust the new moving-policy quantifiers.

## 3. Distorted finite energy with the actual diagonal

Suppress n in a single finite instance. Put delta=kappa-eta. Then

\[
 S_{xy}=r_{xy}^{\eta}e^{\xi_{xy}},\qquad
 \xi_{xy}=\delta\log R_{xy},\qquad |\xi_{xy}|\le D=|\delta|A. \tag{9}
\]

Reciprocity gives S_yx=1/S_xy and t_yx=1/t_xy. The identity
min(1,z)/min(1,z^-1)=z implies a_xy/a_yx=t_xy. Therefore L is
pi-reversible, C is pi-reversible, and C has spectrum in [0,1].
This uses the actual target Hastings ratio, not a q-stationarity property
of Q.

Choose proof parameters

\[
 0<\theta\le\eta,\quad\theta\le1/2,\quad p=(1-\theta)^{-1},
 \quad w\ge1,\quad
 \tau=p(1-\theta/\eta)\in[0,1),\quad
 U=w e^{D\theta p/\eta}.
\]

Define the relaxed scalar envelope

\[
 H_w(D)=\sup_{0<z\le1}(Uz^\tau-z).                           \tag{10}
\]

For every 0<=a<=min(1,e^D r^eta),

\[
 wa^p r^{-\theta p}-a\le H_w(D).                            \tag{11}
\]

Indeed for a>0 the screen bound gives
r^{-\theta p}<=e^{D\theta p/\eta}a^{-\theta p/\eta};
hence the left side is at most Ua^tau-a. At a=0 the original expression
is zero and H_w(D)>=U-1>=0. This avoids assigning a meaning to 0^0.
Equivalently one may maximize the convex expression at the actual screen
endpoints, as the independent contribution does.

If tau=0, H_w(D)=U, approached as z tends to zero. For 0<tau<1,

\[
 H_w(D)=
 \begin{cases}
 U(1-\tau)(U\tau)^{\tau/(1-\tau)},&U\tau\le1,\\
 U-1,&U\tau\ge1.
 \end{cases}                                               \tag{12}
\]

Both formulas agree at equality. These are exact maxima of (10), not a
whole-matrix norm claim or a reachable mixing lower.

Let A_0,E be disjoint proof sets. Retain actual L entries from A_0 into
A_0 union E, kill the other exits, and make E absorbing. Call this L^E.
No killed row is renormalized. Put

\[
 {\mathsf D}=\operatorname{diag}(q_x^\theta),\quad
 T={\mathsf D}L^E{\mathsf D}^{-1},\quad
 \mathcal E_w(v)=\sum_{A_0}|v_x|^p+w\sum_E|v_x|^p.
\]

At output y, use Jensen coefficients B_xy=Q_yx on retained off-diagonal
edges from A_0, B_xx=L_xx on A_0, and B_xx=1 on E. All others are zero.
Reciprocal support makes zero coefficients harmless, and

\[
 \sum_x B_{xy}\le2,\qquad
 \frac{T_{xy}^p}{B_{xy}^{p-1}}
       =Q_{xy}a_{xy}^p r_{xy}^{-\theta p}\quad(x\ne y).       \tag{13}
\]

The column bound uses the outgoing row of Q at y. It does not impose a
counting-column bound on Q. The powered diagonal coefficient is exactly
the original L_xx, or the absorbed one.

For an input x in A_0, let omega_y=1 on A_0 and w on E. Actual accepted
outflow subtraction gives

\[
\begin{split}
 L_{xx}+\sum_{\substack{y\in A_0\cup E\\y\ne x}}
          \omega_y Q_{xy}a_{xy}^p r_{xy}^{-\theta p}
 &\le1+\sum_{\substack{y\in A_0\cup E\\y\ne x}}
       Q_{xy}(w a_{xy}^p r_{xy}^{-\theta p}-a_{xy})\\
 &\le1+H_w(D).                                             \tag{14}
\end{split}
\]

The accepted exits into the killed complement are dropped only after their
nonpositive contribution is accounted for. On an input in E the coefficient
is w. Jensen therefore proves, for every row vector v,

\[
 \mathcal E_w(vT)\le2^{p-1}
       [(1+H_w(D))\sum_{A_0}|v_x|^p+w\sum_E|v_x|^p].        \tag{15}
\]

All constants are independent of support size, degree, minimum atom, and
any invariant law of Q. This is a full energy statement.

## 4. Actual first hits, smoothing, and all post-hit returns

Take W=pi/q, 0<h<1/2, A_0={W<h}, B_0=A_0^c, b=q(A_0).
For E subset B_0 write e=q(E). Form G^E in the same way, and
P^E=(I+alpha G^E+beta L^E)/2. Its absorbed mass from q1_A0 is exactly
the measure of first B_0 hits landing in E. The actual sampler is C.

Every independence proposal from A_0 into B_0 is accepted. Thus G[A_0,A_0]
has actual row sum b. The separate global q-density Jensen step has
coefficient b+we on A_0 and w on E, with the same factor 2^(p-1).
Combining it with (15) and the lazy identity gives

\[
 \mathcal E_w(v{\mathsf D}P^E{\mathsf D}^{-1})
       \le\Gamma(e)\mathcal E_w(v),
\]
\[
 \Gamma(e)=\frac12+\frac{2^{p-1}}2
       \{1+[\beta H_w(D)-\alpha(1-b)]_++\alpha we\}.         \tag{16}
\]

The transformed initial energy of q1_A0 is b. Iteration and weighted
Holder on E yield, for every integer N>=0,

\[
 \Pr_q(X_0\in A_0,\tau_{B_0}\le N,X_{\tau_{B_0}}\in E)
  \le(b/w)^{1-\theta}e^\theta\Gamma(e)^{N(1-\theta)}.        \tag{17}
\]

Empty A_0 or E is handled directly as zero. All first-hit times accumulate
in one absorbed vector.

Here is the inherited full-chain interface with this new Gamma. For
n>=2, 0<=N<n, R>exp(1), 0<d_test<=1, define

\[
 M_0=e^{2K+1},\quad a=\pi(W>R),\quad
 J_0=\frac{2}{\alpha(2(n-N)+1)},\quad
 \rho=1-\alpha(1-b)/2,
\]
\[
 \bar e=\min\left\{1-b,\frac aR+
             \frac{(N+1)(M_0/h+1)J_0}{d_{\rm test}^2}\right\}.
\]

Then

\[
\begin{split}
 \|qC^n-\pi\|_{\rm TV}\le&
 a+\sqrt{(M_0+R)J_0}+d_{\rm test}+\bar e+b\rho^N\\
 &+(b/w)^{1-\theta}\bar e^\theta
                            \Gamma(\bar e)^{N(1-\theta)}.  \tag{18}
\end{split}
\]

For clarity, the reason this remains a full-return certificate is as follows.
The anchor A_*={W<=M_0} has pi mass at least one half by the KL tail bound.
For 0<=f<=1, g=C^t f, and m=pi(g1_A*)/pi(A_*), the inherited IMH
Dirichlet form and laziness give

\[
 \sum_x\frac{\pi_x(g_x-m)^2}{\max(W_x,M_0)}
                         \le\frac{2}{\alpha(2t+1)}.        \tag{19}
\]

This follows from D_C>=alpha D_G/2 and the positive-spectrum bound
(1-lambda)lambda^(2t)<=1/(2t+1); it needs no initial L2 density assumption.

For each j=0,...,N use g_j=C^(n-j)f and its own anchor m_j. Let E be
{W>R} union all {h<=W<=R:|g_j-m_j|>d_test}. Equation (19) and Chebyshev
give q(E)<=bar e. If nu_j is the original unnormalized first-B_0-hit
measure, including the j=0 portion of q, the exact decomposition is

\[
 qC^n=\sum_{j=0}^N\nu_j C^{\,n-j}+\sigma_n,\qquad
 \sigma_n(\Omega)\le b\rho^N.                               \tag{20}
\]

Subtract nu_j(Omega)pi in each summand and cancel its anchor. Good hits
cost d_test in total; initial bad hits cost q(E); later bad first hits
cost (17). The stationary comparison from (19) costs
a+sqrt((M_0+R)J_0). The residual costs its mass. This proves (18).
Every hit is followed by the ORIGINAL C for the remaining steps. All later
global attempts, exits, and returns are included.

The same population information budget gives the binary log-sum bounds

\[
 a\le\frac K{\log R-1},\qquad
 k:=-\log(1-b)\le
            \frac{K+H_2(h)}{1-h}.                          \tag{21}
\]

Only this one admitted budget is used. The bounds in (21) are simultaneous
inequalities for that instance. We do not add separate extremal KL
allocations to assert a sharp amplitude; the coarse convergence upper does
not need the tighter three-cell allocation used for earlier critical laws.

## 5. Uniform upper, including all moving-parameter errors

Let ell=log n and choose proof parameters

\[
 \theta=\frac{\eta_n\varepsilon_0}{2(1+D_n)},\quad w=1,\quad
 h=\ell^{-2},\quad R=n/\ell^4,\quad d_{\rm test}=\ell^{-2},
\]
\[
 N=\left\lceil\frac{8}{\alpha e^{-K}}\log\ell\right\rceil.    \tag{22}
\]

They never alter the actual run. Eventually all conditions for (18) hold,
uniformly in the public policy. In particular theta<=eta_n/8<1/2.

Put lambda=D_n theta p/eta_n and c_eff=1-tau.
Using p<=2 gives lambda<=epsilon_0 and

\[
 0<c_{\rm eff}=\frac{\theta p(1-\eta_n)}{\eta_n}
                       \le\varepsilon_0.
\]

For F(c)=sup_{0<z<=1}(z^(1-c)-z)<=c, (10) implies

\[
 H_1(D_n)\le e^\lambda-1+F(c_{\rm eff})
       \le e^{\varepsilon_0}-1+\varepsilon_0
       \le3\varepsilon_0\le3r_0/8.                         \tag{23}
\]

By (21), q(B_0)>=e^-K/2 eventually uniformly. Hence the positive part
in (16) is exactly zero for all sufficiently large n, not just small:

\[
 [\beta H_1(D_n)-\alpha(1-b)]_+=0.                         \tag{24}
\]

Moreover J_0=O_alpha(1/n), N=O_{K,alpha}(log ell), and

\[
 \bar e\le E_n:=C_1\ell^6\log\ell/n,\qquad
 \sqrt{(M_0+R)J_0}+d_{\rm test}+\bar e=O_{K,\alpha}(\ell^{-2}),
\]
\[
 b\rho^N\le\exp[-\alpha e^{-K}N/4]\le\ell^{-2}.            \tag{25}
\]

C_1 and all thresholds depend only on K,alpha, not on the policy or support.
When needed, E_n can be replaced by the explicit upper
K ell^4/[n(ell-4logell-1)]
+(N+1)(M_0 ell^2+1)2ell^4/(alpha n), valid for N<=n/2.

It is essential not to discard the accumulated multiplier. From (16),(24),

\[
 \Gamma(\bar e)^{N/p}
       \le \exp\{N\theta\log2+\alpha N\bar e\}.             \tag{26}
\]

The last term of (18) is thus at most

\[
 \exp\{-\theta\ell+
   \theta(\log C_1+6\log\ell+\log\log\ell+N\log2)
                 +\alpha N E_n\}
       \le 2e^{-\theta\ell/2}=2e^{-c_0v_n}                \tag{27}
\]

for all sufficiently large n, uniformly in every policy. The expression
multiplying theta after -theta ell is O_{K,alpha}(log ell)=o(ell), and
N E_n->0; no lower bound on theta is needed. If eta is fixed and D_n is
bounded, Gamma^(N/p) need not tend to one. Equation (27), not that false
claim, is the argument.

Combining (21),(25),(27) proves (6), hence sufficiency in (5). Under the
stronger hypothesis in (7), ell e^(-c_0v_n)->0. Thus limsup ell R_n<=K.

For the matching K lower, take Q=I, so A(Q)=0 and L=I for every policy.
Fix 0<k<K, put p=k/ell, e=p/(n ell^2), and on two states use
pi=(p,1-p), q=(e,1-e). Eventually D(pi||q)<=K, since
p log(p/e)=k+o(1) and the complementary term is nonpositive.
The exact nontrivial eigenvalue of C=(1-alpha/2)I+(alpha/2)G is
1-alpha/(2n ell^2). Therefore

\[
 \|qC^n-\pi\|_{\rm TV}
        =(p-e)(1-\alpha/(2n\ell^2))^n\sim k/\ell.           \tag{28}
\]

Letting k increase to K proves liminf ell R_n>=K for ALL policies,
and completes (7). This is an ordinary global-weight trap already in the
admitted class, not a new mismatch mechanism.

## 6. Necessity branch I: bounded u_n

Suppose u_n=eta_n ell is bounded by a finite U along an infinite subsequence.
Fix any 0<b<1-e^-K. Use the symmetric three-state proposal

\[
 Q=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}.
\]

Its asymmetry is zero and it is admitted under every A_n. Put

\[
 p=\ell^{-4},\quad e=p/(n\ell^2),\quad
 q=(b,e,1-b-e),\quad
 \pi=(p/n^2,p,1-p-p/n^2).                                  \tag{29}
\]

All masses are positive eventually. A single KL calculation gives

\[
 D(\pi\|q)\le \log(1/(1-b-e))+p\log(n\ell^2)
                         \longrightarrow-\log(1-b)<K.
\]

The first coordinate's entropy term is negative eventually and has only
been discarded for this upper admission bound.

The actual local forward probability from state 0 to state 1 is

\[
 \sigma=(e/b)^{\eta_n}
      =\exp[-u_n-\eta_n(6\log\ell+\log b)],
\]

because its target ratio is n^2 and the second stage accepts. Thus
liminf sigma>=e^-U. The reverse local probability is sigma/n^2.
The terminal importance ratio is W_1=n ell^2 and is maximal eventually;
its exact full-chain escape probability is

\[
 d_T=\alpha(1-p)/(2n\ell^2)+\beta\sigma/(2n^2),
 \qquad nd_T\to0.
\]

The actual event of starting at 0, taking the local crossing on the first
step, and then staying in the entire terminal state gives

\[
 \|qC^n-\pi\|_{\rm TV}
    \ge b\beta\sigma(1-d_T)^n/2-p,
 \quad\liminf\mathscr R_n\ge b\beta e^{-U}/2>0.             \tag{30}
\]

This conservative event needs neither a fictitious conditional sampler nor
a limit substitution in a previous endpoint theorem. Returns not selected
by the event can only increase qC^n({1}).

## 7. Necessity branch II: discrepancy accumulated across native levels

Suppose instead that, on an infinite subsequence, for a fixed a_0>0,

\[
 \frac{D_n}{\eta_n\log n}\ge a_0.                           \tag{31}
\]

Choose a fixed integer J with J a_0>1 and fixed 0<b<1-e^-K.
The depth is fixed on this subsequence, even if very large. Necessarily
A_n>0 and delta_n!=0 there. Write

\[
 R_A=e^{A_n},\quad M=\lceil R_A\rceil\ge2,\quad 1\le M/R_A<2.
\]

Use a complete M-ary labelled tree of depth J plus a core star.
For positive mismatch, progress is from its root to its leaves; for
negative mismatch, progress is from the leaf union to the root.
The table gives all native forward-edge quantities:

| Native quantity | delta>0: expansion | delta<0: coalescence |
|---|---|---|
| Number of states in progress level i | M^i | M^(J-i) |
| Forward Q_xy | 1/(2M) to each child | R_A/(2M) to its parent |
| Reverse Q_yx | R_A/(2M) to parent | 1/(2M) to each child |
| Forward aggregate proposal f | 1/2 | R_A/(2M) |
| Ratio Q_yx/Q_xy | R_A | 1/R_A |
| q-level ratio z | M R_A^(-kappa/eta) | R_A^(kappa/eta)/M |

At every internal vertex the sum of outgoing proposal probabilities is
1/2+R_A/(2M)<=1. Supply the exact remaining Q_xx; endpoint rows have
their actual one-direction sums. Let Q_star,star=1. Thus Q is a genuine
row-stochastic reciprocal proposal whose largest edge log ratio is exactly
A_n. It is defined before target probabilities. Both sign constructions
have 1/4<f<=1/2.

The level q ratio can also be written

\[
 z=
 \begin{cases}
 (M/R_A)e^{-D_n/\eta_n},&\delta_n>0,\\
 (R_A/M)e^{-D_n/\eta_n},&\delta_n<0,
 \end{cases}
 \quad V=-\log z\ge a_0\ell-\log2\longrightarrow\infty.       \tag{32}
\]

Put

\[
 p=\frac1{\ell^2(1+V)},\quad
 q_i=bz^i,\quad \pi_i=p\,n^{-2(J-i)},\qquad0\le i\le J.     \tag{33}
\]

Split each level total uniformly over its native states and give the core
the remaining q and pi masses. All are strictly positive for sufficiently
large n; q_star->1-b and pi_star->1.

### 7.1 Native screens and real reverse acceptance

In expansion the per-vertex ratio q_y/q_x=z/M=R_A^(-kappa/eta);
in coalescence it is zM=R_A^(kappa/eta). Hence the actual first screen
is exactly S_xy=1 in BOTH cases. It is not a statement about level-total
ratios alone. The forward target Hastings ratios are respectively

\[
 t_{xy}=n^2R_A/M\quad\hbox{and}\quad t_{xy}=n^2M/R_A,
\]

both exceeding one for n>=2. Forward acceptance is one and reverse
acceptance is 1/t_xy. Multiplying by all native backward proposals gives

\[
 L(i,i+1)=f,\qquad L(i,i-1)=f/n^2.                          \tag{34}
\]

Internal aggregate diagonals are 1-f-f/n^2. Endpoints omit only the absent
direction. Global moves between vertices in one level remain in its
aggregate diagonal. Tree automorphisms preserve q,pi,Q and make the
level-plus-core partition strongly lumpable. The q start and every evolved
law are uniform within each level, so quotient TV equals native TV.
The proof itself uses actual native aggregate probabilities, not a free
quotient transition oracle.

### 7.2 One information budget for arbitrary distortion size

The importance ratio on level i is

\[
 W_i=(p/b)n^{-2(J-i)}e^{iV},\qquad W_{i+1}/W_i=n^2e^V>1.
\]

Native multiplicities cancel within the KL sum because q and pi have
the same within-level uniform split. Without assuming V=O(log n),

\[
\begin{split}
 D(\pi\|q)
 &\le\log(1/q_\star)+
   \frac{p}{1-n^{-2}}[\log(1/b)+JV]\\
 &\le\log(1/q_\star)+
  \frac{\log(1/b)+J}{\ell^2(1-n^{-2})}
       \longrightarrow-\log(1-b)<K.                       \tag{35}
\end{split}
\]

This is a single whole-instance admission calculation. The factor 1/(1+V)
in p is necessary to make it valid even when kappa or A grows arbitrarily
quickly. Intermediate W_i need not be below one or below W_star.

### 7.3 Retention of the whole terminal union

The terminal ratio is W_J=(p/b)e^{JV}. Since (1+v)e^{-Jv} decreases on
v>=0,

\[
 \frac n{W_J}
   =b n\ell^2(1+V)e^{-JV}
   \le O_{a_0,J,b}(n^{1-Ja_0}\ell^3)\longrightarrow0.       \tag{36}
\]

Thus W_J is eventually the maximal ratio, including the core. The true
escape probability from the whole terminal union T is

\[
 d_T=\alpha(1-p)/(2W_J)+\beta f/(2n^2),\qquad nd_T\to0.     \tag{37}
\]

All global moves within T are retained, including moves between different
leaves in expansion.

### 7.4 Capture uses actual transition counts

Before first terminal arrival, select paths on which every G attempt is
marked failure, even if that attempt would reject or stay in the level.
Also mark any accepted local backward move as failure. A forward local
move succeeds at that stage; laziness and local holds remain in it.
This defines a subset of actual trajectories and does not change C.

Let

\[
 c=\beta f/2,\quad g=\alpha/2,\quad E_0=c+g+c/n^2,\quad
 H=\lfloor n/(2J)\rfloor.
\]

At transient level i the exact marked hazard is
e_i=c+g+1_{i>0}c/n^2. The probability of a forward marked event within
H actual steps, before failure, is
c[1-(1-e_i)^H]/e_i. It is bounded below by

\[
 (c/E_0)[1-e^{-(c+g)H}].                                  \tag{38}
\]

Condition successively on each arrival and require J such deterministic
waiting windows. This reaches T by JH<=n/2. The Markov property suffices;
independent holding times and random-horizon substitutions are unnecessary.
Original-chain retention after the hit then proves

\[
 \boxed{\|qC^n-\pi\|_{\rm TV}\ge
 b(c/E_0)^J[1-e^{-(c+g)H}]^J(1-d_T)^n-p.}                 \tag{39}
\]

The selected event allows all original transitions inside T after capture.
Paths outside that event, including exits followed by returns, have only
been excluded from a lower bound, never removed from the chain.

The timing and retention factors tend to one. In expansion f=1/2.
In coalescence kappa>=0 implies |delta|<=eta, so (31) forces
A_n>=a_0 log n; hence R_A/ceil(R_A)->1 and again f->1/2.
This remains true if signs alternate. Therefore

\[
 \liminf\mathscr R_n
       \ge b\left(\frac{\beta}{2\alpha+\beta}\right)^J>0
       \quad\hbox{on the subsequence}.                    \tag{40}
\]

For a class supremum b can subsequently increase to 1-e^-K. The
constant is a positive lower bound, not asserted to be optimal.

## 8. Exhausting moving policies and completing Theorem 1

If v_n does not tend to infinity, there is an infinite subsequence on which
v_n<=B for some finite B>0. If u_n has a bounded subsequence there, (30)
rules out convergence. Otherwise u_n tends to infinity along that
subsequence (or pass to such a further subsequence). For all sufficiently
large selected n,

\[
 D_n\ge u_n/B-1\ge u_n/(2B).
\]

Condition (31) holds with a_0=1/(2B), so (40) rules out convergence.
This proves necessity without imposing an artificial upper bound on
kappa_n, restricting the sign of delta_n, or requiring a positive lower
bound on A_n. In particular A_n may tend to zero while an unbounded
positive mismatch makes (31) hold. The construction then uses M=2;
the exact per-vertex q ratio still gives S=1.

Together with Section 5 this proves (5). The equivalence with
u_n->infinity and D_n=o(u_n) follows directly from v_n=u_n/(1+D_n).
The fixed-power corollary follows because u_n is then proportional to
log n and |delta| is a fixed positive constant.

## 9. Strong ordinary comparator on the same lower instances

The multilevel lower does not make proposal-start pure IMH fail.
Write s_q=sum_{i=1}^J q_i<=bz/(1-z) and
pi_tree=sum_i pi_i<=p/(1-n^-2). The level-0 importance ratio is the
smallest and tends to zero, whereas W_star tends to 1/(1-b).
From any level-0 vertex every global proposal outside that union is
accepted. Thus an IMH step stays in the root union with probability b,
hits the core with probability q_star, or hits another tree level with
probability s_q.

The probability of another tree level before the core is s_q/(1-b).
If the core has been reached, contraction of the ORIGINAL G bounds all
remaining TV by TV(delta_star,pi)=pi_tree, including returns. Initial
mass on other tree levels is s_q. Consequently for every j>=0,

\[
 \|qG^j-\pi\|_{\rm TV}
   \le\pi_{\rm tree}+\frac{s_q}{1-b}+b^{j+1}
   \le\frac p{1-n^{-2}}+
        \frac{bz}{(1-b)(1-z)}+b^{j+1}.                     \tag{41}
\]

This tends to zero for any j->infinity, including j/n tending to any
positive constant. No wall-time or target-call equivalence follows from
a deterministic transition-count comparison alone; those resources must
be measured in an implementation. The overall minimax ordinary-IMH
amplitude remains K under the same supplied KL budget. If the displayed
analytic target description is known, direct sampling of its core and
level masses is also an admissible comparator.

## 10. Resource boundary, significance, and remaining frontier

The exact native support in (32)-(33) has

\[
 1+\sum_{i=0}^J M^i
    =1+(M^{J+1}-1)/(M-1)
\]

states. A vertex label needs up to J ceil(log_2 M)+O(log J) bits.
The probabilities satisfy magnitude bounds

\[
 \log(1/q_x)\le\log(1/b)+J(V+\log M),
\]
\[
 \log(1/\pi_x)\le2J\log n+2\log\log n+\log(1+V)+J\log M.
\]

Implicit tree sampling can avoid enumerating the support; it does not remove
index bits, native proposal/target evaluations, reverse-proposal
probabilities, or arithmetic precision. For arbitrary real public policies
computing exp(A), its ceiling, and very small probabilities may require
unbounded precision. These lower instances establish an exact-real minimax
obstruction, not an efficient finite-word sampler or floating-point
instability theorem.

The scientific distinction established here is sharp: fixed power mismatch
is harmless for uniform convergence under sublogarithmic public asymmetry,
whereas any positive logarithmic asymmetry along a subsequence can be
accumulated across finitely many native crossings into retained mass.
For moving policies, the screen strength eta log n must dominate both
one and the total edge discrepancy scale |kappa-eta|A. A single-crossing
test would miss the latter obstruction for small positive ratios.

The next selected question is the sharp transport rate within the convergent
region, especially when v_n is of order loglog n. Does a rate depend only on
v_n or also separately on the public asymmetry and multiplicity available
at each crossing? The present finite envelope and the admitted two-sign
geometry are tools for that question; neither settles its critical
amplitude. We will not infer it by optimizing (10) without a matching
reachable native construction and a joint information allocation.

Internal proof checking, historical originality, external mathematical
acceptance, finite-precision realization, and practical performance are
separate claims. This theorem supplies robustness knowledge and an admitted
failure mechanism. It supplies no advantage over ordinary IMH.

