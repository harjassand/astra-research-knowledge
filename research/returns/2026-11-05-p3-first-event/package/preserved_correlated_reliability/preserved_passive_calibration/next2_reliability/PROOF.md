# A finite relative certificate for the entire first-failure distribution

## Status and precise outcome

This document completes the finite-confidence and finite-arithmetic construction left unfinished in the preceding run. It is a mathematical algorithm, with published static counting used as an explicitly priced subroutine. Generic Karger counting is not newly implemented here. Numerical checks and the implementation scope are recorded separately. Historical priority and practical superiority are not asserted.

**Theorem.** Consider the finite reversible continuous-time model specified below, initially distributed according to its invariant law conditional on safety. For rational \(0<\epsilon,\delta\le1\), an algorithm constructs one finite certificate. With probability at least \(1-\delta\), that certificate supplies an interval containing the first-failure probability at **every positive rational deadline**, each with endpoint ratio at most \(1+\epsilon\). Preprocessing work is polynomial in the succinct input length, the value \(g^{-1}\), \(\epsilon^{-1}\), and \(\log(1/\delta)\), including the stated static-oracle work. It has no inverse stationary failure probability or mean-lifetime factor. A query at a binary-encoded rational deadline requires polynomial bit work in the certificate size and deadline bit length, without another stochastic trajectory or counting call.

The same construction has a discrete-time version for positive-semidefinite reversible endpoint kernels. The continuous result uses genuine uniformization and preserves the actual deadline distribution; it does not replace a fixed-tick process by a mean-matching continuous surrogate.

## 1. Succinct input and the access actually used

The state is a binary vector on the \(m\) edges of a known connected undirected graph. The failure event \(B\) is disconnection; \(A=B^c\). The specified invariant law is
\[
\pi(x)=\prod_{i=1}^m q_i^{x_i}(1-q_i)^{1-x_i},
\qquad q_i\in(0,1)\cap\mathbb Q.
\]
Write \(p=\pi(B)\), \(a=1-p\), and assume \(0<p\le1/2\). The initial law is \(\nu=\pi(\cdot\mid A)\). It can be sampled computationally by product draws and rejection, with acceptance \(a\ge1/2\). Physically preparing this law is a distinct, paid operation.

The fitted generator \(Q\) has a polynomial-sized description as a mixture or sum of bounded-block reversible local tables and an operating independent refresh backbone. All supplied numbers are rational. Alternatively, the theorem accepts any succinct reversible generator for which the following three operations and bounds are supplied with their actual costs:

1. ordinary kernel updates and evaluation of the failure predicate;
2. a proved upper bound on all exit rates;
3. a proved positive lower bound on the full spectral gap.

Choose a rational \(R\ge2\max_x[-Q(x,x)]\), computable from the local table bounds, and put
\[
P=I+Q/R,\qquad g=\gamma/R,\qquad u=Rt.
\]
Here \(\gamma>0\) is the certified gap lower bound. We may decrease \(g\) so \(g\le1\). Then \(P\) is reversible and positive semidefinite. The original continuous process is exactly the process obtained by applying \(P\) at the points of an independent rate-\(R\) Poisson clock. This is an identity of path laws, including null events.

The static subroutine Count estimates undirected all-terminal disconnection probability to relative error \(\alpha\) with failure probability \(\beta\), at bit cost
\[
T_{\rm stat}(m,b,\alpha,\beta),
\]
polynomial in \(m,b,\alpha^{-1},\log(1/\beta)\). This is existing all-terminal unreliability FPRAS machinery, imported through the accepted P2 construction. It is not a free arbitrary-predicate oracle. Its application to every contracted/deleted prefix graph is included in the work below. Cases of static probability zero or one are recognized directly.

The entire algorithm can also be stated for a different failure predicate if that predicate has these same explicitly costed static estimation and conditional-sampling operations. No general FPRAS for arbitrary predicates follows.

## 2. Spectral facts, including a stronger tail bound

Let \(P_A\) be the killed restriction and \(K=I-P_A\), considered on \(\ell^2(A,\pi)\). Let \(v=1_A\). The eigenvalues satisfy \(0<\lambda_i\le1\), and
\[
F(u)=\Pr_\nu(\tau_B\le u/R)
=\frac{\langle v,(I-e^{-uK})v\rangle_\pi}{a}
=\sum_i\alpha_i(1-e^{-\lambda_i u}),
\]
where \(\alpha_i\ge0\) and \(\sum_i\alpha_i=1\).

Let
\[
j=\sum_{x\in A,y\in B}\pi(x)P(x,y).
\]
Poincare applied to \(1_A\), zero extension of safe functions, and the Rayleigh quotient give
\[
gpa\le j\le p,\qquad
gp\le\lambda:=\lambda_1(K)\le j/a\le p/a.                 \tag{1}
\]
Principal-submatrix interlacing gives \(\lambda_2(K)\ge g\), when there is a second eigenvalue.

Let \(r=1-\alpha_1\). The spectral first moment gives
\[
r\le \frac{j}{ag}\le\frac{p}{ag}.                       \tag{2}
\]
There is also a stronger bound relevant to the tail. Extend a normalized killed ground eigenvector \(e_1\) by zero on \(B\). Its full-chain variance is
\[
1-|\langle 1,e_1\rangle_\pi|^2
=1-a\alpha_1=p+ar.
\]
Poincare therefore implies
\[
\lambda\ge g(p+ar),\qquad \frac r\lambda\le\frac1{ag}.  \tag{3}
\]
This argument does not assume the eigenvector commutes with another operator.

For \(f(u,\lambda)=1-e^{-\lambda u}\),
\[
f(u,\lambda)\le F(u),\qquad
\frac{F(u)-f(u,\lambda)}{f(u,\lambda)}
\le \frac r{e^{\lambda u}-1}
\le\frac r{\lambda u}
\le\frac2{gu}.                                         \tag{4}
\]
The claim concerns relative failure probability. It does not certify relative accuracy of the tiny surviving tail.

The spectral representation also implies monotonicity and concavity:
\[
0<s\le t \quad\Longrightarrow\quad
1\le F(t)/F(s)\le t/s.                                 \tag{5}
\]

## 3. Three bounded-observable experiments

### 3.1 Boundary sampling and a Palm identity

Draw \(y\sim\pi(\cdot\mid B)\), apply one \(P\) update \(y\to x\), and accept if \(x\in A\). The acceptance probability is
\[
c=j/p\ge ag\ge g/2.                                    \tag{6}
\]
By detailed balance, the accepted ordered pair \(x\to y\) has probability \(\pi(x)P(x,y)/j\): it is a stationary boundary crossing.

To generate a forced-crossing path over uniformized time \(u\), draw \(M\sim{\rm Poisson}(u)\), choose a position uniformly among \(M+1\) positions, place the accepted boundary crossing there, and simulate the other \(M\) ordinary \(P\) updates backwards and forwards. Reversibility justifies the backwards kernel. Let \(N\ge1\) be the number of \(A\to B\) crossings in the resulting path and return
\[
W=\frac{1_{\{X_0\in A\}}}{N}\in[0,1].
\]

No continuous event times are needed. To verify the identity on skeletons, an unforced stationary skeleton with \(l\) potential events has its usual Markov path probability multiplied by \(e^{-u}u^l/l!\). The forced law gives the same skeleton weight multiplied by
\[
\frac{e^{-u}u^{l-1}}{(l-1)!}\frac{N}{lj}
=\frac{N}{ju}\frac{e^{-u}u^l}{l!}.
\]
Consequently
\[
aF(u)=ju\,\mu(u)=pcu\,\mu(u),\qquad \mu(u)=EW.          \tag{7}
\]
This is an explicit adaptation of established inverse-multiplicity/Palm sampling.

Since \(F(u)\ge1-e^{-gpu}\ge gpu/(1+gpu)\),
\[
\mu(u)\ge\frac{ag}{1+gpu}.                             \tag{8}
\]

### 3.2 Ordinary safe-start simulation when failure is not rare

Sample \(\nu\) by product draws and safe rejection, simulate \({\rm Poisson}(u)\) ordinary \(P\) steps, and return the indicator that any state was failed. Its expectation is exactly \(F(u)\).

Suppose a simultaneous static interval \([p_L,p_U]\) has width at most
\[
r_\xi=(1+\xi)/(1-\xi)\le2.
\]
At a grid point, use the Palm experiment if \(ugp_U\le1\). Then (8) gives \(\mu(u)\ge g/4\). Otherwise
\[
ugp\ge ugp_L>1/r_\xi\ge1/2,
\]
so direct simulation has mean \(F(u)>1-e^{-1/2}>1/3\). Thus every estimated grid observable has a known inverse-polynomial mean. This hybrid avoids the earlier unnecessarily small mean floor of order \(1/H\).

### 3.3 A short reverse no-return statistic for the slow eigenvalue

Draw \(Y\sim\pi(\cdot\mid B)\), apply one \(P\) update, and return \(Z=1\) if it enters \(A\) and then stays safe through a further independent Poisson number of updates of mean \(\ell\). Reversibility gives
\[
D_\ell:=pEZ=\langle v,Ke^{-\ell K}v\rangle_\pi
=a\sum_i\alpha_i\lambda_i e^{-\ell\lambda_i}.           \tag{9}
\]

Define integer ceilings without transcendental computation:
\[
L_g=\lceil\log_2(4/(g\xi))\rceil,\quad
\ell=\lceil L_g/g\rceil,\quad
p_{\rm gate}=\xi/(2\ell).
\]
The logarithmic ceiling is obtained by comparisons with integer powers of two.

If \(p\le p_{\rm gate}\), then \(\lambda\ell\le\xi\), \(r\le\xi\), and the slow term in \(D_\ell/a\) is at least \((1-\xi)^2\lambda\). Its fast contribution, relative to \(\lambda\), is at most
\[
e^{-g\ell}\frac{j/a}{\lambda}
\le \frac{e^{-g\ell}}{ag}\le\xi/2.
\]
Therefore
\[
(1-2\xi)\lambda\le D_\ell/a\le(1+\xi)\lambda,\qquad
EZ\ge g/4.                                             \tag{10}
\]
The rare branch has a unique slow eigenvalue because
\(\lambda\le2p\le\xi/\ell<g\).

## 4. Finite approximate samplers, with every bias allocated

All following tolerances are independent of the confidence parameter \(\delta\). Approximate draws are treated as small biases of bounded observables, not as an assertion that every counting call succeeds.

Set
\[
\xi=\epsilon/40,\quad q_0=g/4,\quad
\tau_B=\xi gq_0/128,\quad \tau_P=\xi q_0/64.
\]
Choose a dyadic mesh \(h_W=2^{-b_W}\le\xi q_0/64\); round \(W\) down to that mesh. The resulting loss of expectation is at most \(h_W\).

### 4.1 A finite conditional-failure sampler

Sequentially reveal the \(m\) edges. At a prefix, the two conditional failure masses are static unreliabilities on the two contracted/deleted graphs. Multiply by the corresponding product-bit probability and normalize to obtain the next-bit probability. Use fresh Count calls for each draw and prefix.

Request relative error at most \(\tau_B/(32m)\) and failure probability at most \(\tau_B/(16m)\) in each of the two calls. Round each positive mass with absolute error at most \(\tau_Bp_{\rm floor}/(32m)\), so its total relative budget is at most \(\tau_B/(16m)\). On their joint success event, normalization changes the conditional next-bit law by at most twice that relative budget. Their failure probability contributes at most twice the confidence budget. Thus the conditional next-bit distribution differs from the exact one by at most \(\tau_B/(4m)\). Sequential coupling gives total-variation error at most \(\tau_B\), with slack.

If an impossible prefix or invalid zero denominator is produced by a failed Count call, or the final state is not in \(B\), return a fixed known failed state. This postprocessing is the identity on every exact target draw and cannot increase its TV distance. Every returned state is in \(B\). The sampler uses at most \(2m\) counting calls per draw and always has finite prescribed work. Repeated calls are independent.

A positive static mass has a known bit-length floor
\[
p_{\rm floor}=\prod_i\min(q_i,1-q_i)>0.
\]
The same floor works for positive prefix failure probabilities. It permits relative output rounding using only polynomially many bits; no inverse-\(p\) arithmetic loop is used.

### 4.2 A finite rational Poisson sampler

For any rational \(u\le H\), let
\[
K_u=\lceil2u\rceil+\lceil\log_2(1/\tau_P)\rceil.
\]
The exponential Markov bound with \(E2^M=e^u\le2^{2u}\) gives
\[
\Pr(M>K_u)\le\tau_P.
\]
Use exactly the conditional Poisson law on \(0,\ldots,K_u\). Its weights are proportional to \(u^k/k!\), so they are rational and the factor \(e^{-u}\) cancels.

For \(u=A/B\), integer weights can be taken as
\[
w_k=A^kB^{K_u-k}\frac{K_u!}{k!}.
\]
These are computed and sampled by finite integer arithmetic. Normalizing them produces the exact truncated conditional distribution, whose TV distance from the desired Poisson law is its omitted tail probability, at most \(\tau_P\). The number of simulated updates is now deterministically bounded by \(K_u\).

### 4.3 Boundary conditioning and the combined mean biases

The joint law of a conditional-failure draw and its one-step update has TV error at most \(\tau_B\). Its acceptance probability is at least \(g/2-\tau_B\ge g/4\). Conditioning on acceptance changes its pair law by at most \(2\tau_B/c\le4\tau_B/g\).

Thus the difference between the mean of the actual finite Palm observable and its ideal mean is at most
\[
4\tau_B/g+\tau_P+h_W
\le \xi q_0/16<\xi q_0/8.                              \tag{11}
\]
The direct simulation bias is at most \(\tau_P\); the \(Z\) bias is at most \(\tau_B+\tau_P\); the \(c\) bias is at most \(\tau_B\). Each is at most \(\xi q_0/8\).

Boundary rejection and safe-initialization rejection are initially analyzed without caps. Their cap failures will be charged as abort events; no conditioning on a cap is used to justify an estimator.

## 5. A finite biased-mean confidence routine

The following lemma is used for \(c,Z\), every Palm grid observable, and every direct grid observable.

Suppose \(0\le Y\le1\), its ideal mean \(\mu\ge q_0\), and the implemented iid mean \(\widetilde\mu\) obeys
\[
|\widetilde\mu-\mu|\le \xi q_0/8.
\]
Take
\[
N=\left\lceil\frac{384}{q_0\xi^2}\log(2/\beta)\right\rceil
\]
independent samples; replacing the logarithm by its base-two ceiling only increases \(N\). Multiplicative bounded-variable concentration, with relative deviation \(\xi/8\), gives failure probability at most \(\beta\), since \(\widetilde\mu\ge q_0/2\). On that event,
\[
|\overline Y-\mu|
\le \xi\mu/8+(\xi/8)(1+\xi/8)\mu
\le17\xi\mu/64<\xi\mu/2.
\]
Therefore
\[
\left[\frac{\overline Y}{1+\xi/2},
      \min\{1,\frac{\overline Y}{1-\xi/2}\}\right]         \tag{12}
\]
contains \(\mu\) and has width at most \(r_\xi\). Zero or inconsistent empirical intervals may trigger abort; on the good event this never happens.

The rounded Palm observations share a dyadic denominator. Their sums need only \(O(b_W+\log N)\) bits. There is no unpriced growth from summing arbitrary reciprocal integers.

## 6. The complete finite certificate

### 6.1 Static interval and choice of finite horizon

Obtain a static estimate with relative error at most \(\xi/8\) and failure probability \(\delta/8\). Round to a dyadic absolute mesh at most \(\xi p_{\rm floor}/32\). A static interval formed with relative radius \(\xi/4\) then contains \(p\) on that event and has width at most \(r_\xi\). Intersect its upper endpoint with \(1/2\); abort if the resulting interval is empty or its lower endpoint is not positive. This cannot happen on the good static event. Let
\[
a_L=1-p_U,\qquad a_U=1-p_L.
\]
Then \(a_U/a_L\le p_U/p_L\le r_\xi\).

If \(p_U\le p_{\rm gate}\), choose the rare branch and
\[
H=\max\{\lceil2/(g\xi)\rceil,\ell+1\}.
\]
Otherwise \(p_L>p_{\rm gate}/2\). Choose the nonrare branch and
\[
H=\max\{\lceil L_\xi/(gp_L)\rceil,\ell+1\},
\qquad L_\xi=\lceil\log_2(1/\xi)\rceil.
\]
Even if the static estimate fails, its constructed width ensures the nonrare branch cannot select an arbitrarily small \(p_L\); the work remains bounded by the stated polynomial.

Build a rational grid from \(u_0=\xi\). To keep denominators small, put \(h=\xi^2/4\) and set the next point to \(h\lceil(1+\xi)u/h\rceil\), unless this exceeds \(H\), in which case include \(H\) and stop. Growth is at least \(1+\xi\), and every adjacent ratio is at most \(1+5\xi/4\le r_\xi\). All points after the first share the denominator of \(h\), up to reduction. Let the number of points be \(G\). Then
\[
G=O(\xi^{-1}\log(H/\xi)).
\]
At each point select Palm or direct simulation as in Section 3.2. Estimate \(c\) once and \(Z\) in the rare branch. All use the routine (12), with individual confidence \(\delta/[8(G+2)]\).

### 6.2 Head interval: every arbitrarily small positive deadline

Because \(0<\lambda_i\le1\), for \(0<u\le\xi\),
\[
(1-u/2)\frac ja\,u\le F(u)\le\frac ja\,u.
\]
Thus the certificate returns
\[
\left[(1-\xi/2)\frac{p_Lc_L}{a_U}u,\;
      \min\{1,\frac{p_Uc_U}{a_L}u\}\right].              \tag{13}
\]
Its width is at most \(r_\xi^4\). This covers arbitrarily tiny positive probabilities with relative accuracy; no time grid accumulating at zero is needed.

### 6.3 Middle interval: one finite grid covers a continuum

At a Palm node use
\[
L(u)=p_Lc_Lu\mu_L/a_U,\qquad
U(u)=\min\{1,p_Uc_Uu\mu_U/a_L\}.
\]
At a direct node use (12). Every node interval has width at most \(r_\xi^4\). Between adjacent nodes \(s<t\), return \([L(s),U(t)]\). By (5), its width is at most
\[
r_\xi^4\frac{F(t)}{F(s)}r_\xi^4\le r_\xi^9.            \tag{14}
\]
The confidence event is finite; it does not allocate a failure probability separately to each queried deadline.

### 6.4 Tail interval

In the nonrare branch, for \(u\ge H\), \(F(u)\ge1-e^{-gpu}\ge1-\xi\); return \([1-\xi,1]\).

In the rare branch define
\[
\lambda_L=\frac{p_Lz_L}{a_U(1+\xi)},\qquad
\lambda_U=\frac{p_Uz_U}{a_L(1-2\xi)}.
\]
These contain \(\lambda\) and have ratio at most \(r_\xi^5\), since
\((1+\xi)/(1-2\xi)\le r_\xi^2\) for \(\xi\le1/3\).
Their construction also ensures \(0<\lambda_L\le\lambda_U<1/2\) whenever the routine has not aborted.

For \(u\ge H\), return
\[
[f(u,\lambda_L),\;\min\{1,(1+\xi)f(u,\lambda_U)\}],
                                                               \tag{15}
\]
with the outward finite-arithmetic evaluation specified next. The exact mathematical interval has width at most \(r_\xi^6\), because \(f(u,\lambda)\) is increasing and concave in \(\lambda\), and vanishes at \(\lambda=0\).

## 7. Finite arithmetic for arbitrary binary deadlines

All head and middle endpoints are rational. Grid construction, interval products, comparisons, and locating a query use exact rational/integer arithmetic of polynomial bit length.

For (15), the required function is \(1-e^{-x}\) at a positive rational \(x=\lambda Rt\), possibly astronomically small or large. The following elementary evaluator provides a finite outward interval without cancellation.

Let \(L=\lceil\log_2(64/\xi)\rceil\). If \(x\ge L\), return \([1-\xi/64,1]\), since \(e^{-x}\le2^{-L}\le\xi/64\).

Otherwise choose a power of two \(M\) so \(y=x/M\le1/2\), using \(M=1\) when already true. Then \(M\le4L\). Choose an even \(d\) with
\[
2^{-d}\le \xi/(128L).
\]
The alternating Taylor sums
\[
T_d(y)=\sum_{k=0}^{d}(-y)^k/k!,\qquad T_{d+1}(y)
\]
are exact rational upper and lower bounds on \(e^{-y}\). Their error is at most \(y2^{-d}\). Raising these two bounds to the integer power \(M\) preserves their order. Since numbers involved lie in \([0,1]\), their error relative to \(e^{-x}\) is at most \(My2^{-d}=x2^{-d}\), which is at most
\[
(\xi/128)\min\{x,1\}.
\]
As \(1-e^{-x}\ge\frac12\min\{x,1\}\), subtracting the power bounds from one gives relative errors at most \(\xi/64\).

The degree and power are \(O(\log(1/\xi))\). Exact numerator and denominator lengths are polynomial in the bit length of \(x\) and \(\log(1/\xi)\). Thus this routine works in polynomial bit time even when \(t\) is enormous or tiny. Its error enlarges the rare tail ratio by at most one additional factor \(r_\xi\).

The worst certificate ratio is therefore \(r_\xi^9\). For \(\xi=\epsilon/40\le1/40\),
\[
9\log r_\xi\le \frac{18\xi}{1-\xi}\le(6/13)\epsilon.
\]
Convexity of the exponential on \([0,1]\), and \(e^{6/13}<2\), imply
\(r_\xi^9\le1+\epsilon\).

## 8. Abort probabilities, overall confidence, and worst-case work

Let \(N_{\rm all}\) be the predetermined number of bounded-observable trials after the static interval and grid have been fixed. In a boundary draw, acceptance probability is at least \(g/4\). Cap its independent attempts at
\[
C_B=\left\lceil(4/g)\lceil\log_2(8N_{\rm all}/\delta)\rceil\right\rceil.
\]
The probability that any cap is exceeded is at most \(\delta/8\). For exact safe-equilibrium rejection use a cap
\[
C_A=\lceil\log_2(8N_{\rm all}/\delta)\rceil,
\]
since acceptance is at least \(1/2\). Any exceeded cap aborts the whole construction; it does not silently replace a sample.

A rational categorical draw is made by a uniform integer below its finite common denominator. Rejection from a binary interval of the next power-of-two size has acceptance at least \(1/2\). The total number of outer categorical requests has a deterministic bound \(U\). Cap each binary rejection at \(\lceil\log_2(8U/\delta)\rceil\), charging another \(\delta/8\) abort probability. The prescribed finite-time static subroutine includes its own computation and randomness.

Static-estimate failure costs \(\delta/8\); all bounded-mean failures together cost at most \(\delta/8\); these three abort categories cost at most \(3\delta/8\). Thus total failure or abort probability is at most \(5\delta/8<\delta\). Approximate conditional sampling and Poisson truncation are already deterministic mean-bias budgets, not additional confidence losses. Conditioning on the initial static result is legitimate: subsequent calls use fresh randomness, and every stated sample count is then fixed.

For transparent work accounting define
\[
K_{\max}=\lceil2H\rceil+\lceil\log_2(1/\tau_P)\rceil,\qquad
N=O(g^{-1}\xi^{-2}\log(G/\delta)).
\]
There are \(O(NG)\) bounded trials, at most \(O(NG(K_{\max}+C_B+C_A+1))\) ordinary updates and failure tests including boundary attempts and preparation rejection, at most \(O(N(2+GC_B))\) conditional-failure draws, and at most \(O(NGC_A)\) product-state preparation attempts. Each conditional-failure draw costs at most \(2m\) static calls at relative tolerance \(\tau_B/(32m)\) and confidence parameter \(\tau_B/(16m)\), plus polynomial prefix and arithmetic work.

The rough horizons satisfy
\[
H_{\rm rare}=O(g^{-1}[\xi^{-1}+\log(1/(g\xi))]),
\]
\[
H_{\rm nonrare}
=O(g^{-2}\xi^{-1}\log(1/(g\xi))\log(1/\xi)).
\]
Dependence on \(g^{-1}\) is on its value. Exponentially small gaps remain expensive.

Poisson integer tables have \(K_{\max}+1\) entries per grid value. An entry has at most
\[
O(K_{\max}[b_u+\log K_{\max}])
\]
bits, where \(b_u\) is the grid-value bit length, itself polynomial in the input and \(G\). Their construction, storage and exact categorical draws have polynomial bit cost; these tables are not assumed free. The bounds above are deliberately conservative and can be very large.

## 9. Discrete endpoint version

For an actual positive-semidefinite reversible endpoint kernel, replace \(e^{-uK}\) by \(P_A^n\). The forced boundary path has exactly \(n-1\) other updates and a uniformly selected crossing position. Its density is \(N/(jn)\), so \(aF_n=j n EW\). The reverse statistic uses exactly \(\ell\) further updates. Every spectral estimate above holds with \(e^{-\lambda u}\) replaced by \((1-\lambda)^n\), using \((1-\lambda)^{-n}-1\ge n\lambda\). There is no small-time head; the grid includes all integers through \(\lceil1/\xi\rceil\), then rounded geometric points whose adjacent ratio is at most \(r_\xi\).

For a binary integer query, evaluate \(1-(1-\lambda)^n\) by outward dyadic repeated squaring. A precision \(b\) with \(2^{-b}\le\xi\lambda_L/(16n)\) suffices: unfolding the multiplication tree bounds each endpoint error by \(2n2^{-b}\), while the CDF is at least \(\lambda_L\). Thus \(b=O(\log n+\log(1/\lambda_L)+\log(1/\xi))\). This is polynomial bit work, not a loop of length \(n\).

## 10. What the theorem adds, and what it does not

The completed operation is a finite, nonasymptotic, simultaneous relative risk curve from succinct reversible dynamics and explicitly supplied static access. Mean-only computation, additive exponential approximation and a fresh estimator for each requested horizon do not by themselves provide that object.

Karger and subsequent work already supply static all-terminal rare-probability approximation. Aldous-Brown supply strong reversible exponential approximation. Nakayama-Shahabuddin already combine small-horizon simulation and large-horizon regenerative bounds, including dynamics and all-working starts outside the present model. Their work is a substantial alternative, not an omitted baseline. No historical first or unconditional advantage is established here.

This theorem supplies neither a complete unknown dynamics model nor a physical initialization. Their acquisition and uncertainty are treated in the companion calibration note, using the accepted bounded-port P2 interface. Unknown baths, undeclared larger transitions, hidden memory, ageing and unverified error floors remain outside that model. A physical finite-TV initialization can fail to give relative correctness as \(t\downarrow0\); that boundary is retained explicitly.

### Primary sources used for machinery and comparison

- D. R. Karger, *A Fully Polynomial Randomized Approximation Scheme for the All Terminal Network Reliability Problem*, SIAM Journal on Computing 29 (1999), 492–514: https://arxiv.org/abs/cs/9809012 .
- R. Cen, W. He, J. Li and D. Panigrahi, *Beyond the Quadratic Time Barrier for Network Unreliability*, SODA 2024: https://arxiv.org/abs/2304.06552 . Faster static methods may replace the counted static subroutine when their hypotheses apply; no running-time claim here discards their accuracy or probability-model restrictions.
- M. K. Nakayama and P. Shahabuddin, *Quick Simulation Methods for Estimating the Unreliability of Regenerative Models of Large, Highly Reliable Systems*, PEIS 18 (2004), 339–368: https://doi.org/10.1017/S0269964804183058 ; author PDF https://web.njit.edu/~marvin/papers/PEIS_published.pdf .
- D. Aldous and M. Brown, *Inequalities for rare events in time-reversible Markov chains II*, SPA 44 (1993), 15–25: https://www.sciencedirect.com/science/article/pii/0304414993900353 .
- R. M. Karp and M. Luby, *A New Monte-Carlo Method for Estimating the Failure Probability of an n-Component System*, UCB/CSD-83-117: https://www2.eecs.berkeley.edu/Pubs/TechRpts/1983/6351.html .
- Accepted P2 unknown-local-ports source, fixed revision 324acb589443002bf8d529cc15e160129c5e36d2: https://github.com/harjassand/astra-research-knowledge/tree/324acb589443002bf8d529cc15e160129c5e36d2/research/returns/2026-11-05-p2-unknown-local-ports .
