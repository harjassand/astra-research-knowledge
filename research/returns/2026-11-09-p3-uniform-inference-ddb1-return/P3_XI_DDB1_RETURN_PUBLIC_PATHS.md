# P3 completed return

Source: https://chatgpt.com/c/6af11227-f57c-83ec-80e4-caf25a4bae01
Model: GPT-6 standard, Extra High. No producer ZIP visible.

## Actual prompt

P3: pursue ONE FULL uniform inference question, retaining your current context and accepted E0C/072 constructions.

For EVERY fixed finite WEAKLY REVERSIBLE reaction structure R={(y_r,z_r)} in Z_+^d, with arbitrary arities/linkages and allowing the zero complex, construct a terminating deterministic compiler. No positive conservation law, finite population bound or finite communicating class is promised.

Variable input: positive rational activity vector lambda in Q_+^d, x0 in Z_+^d, and rational 0<epsilon<1, ALL in BINARY. Gamma is the ACTUAL communicating class of x0 under enabled rules x->x-y_r+z_r when x>=y_r. Weak reversibility makes every enabled transition returnable. Let q=Pr{Y in Gamma} for independent Y_i~Poisson(lambda_i), so q>0. The target law is pi(x)=q^-1*exp(-sum lambda_i)*prod_i lambda_i^x_i/x_i!, x in Gamma, including every finite/infinite class, disabled boundary, congruence, singleton and arbitrarily rare conditioning event.

FULL endpoint: the compiler emits ONE inference algorithm and COMPUTABLE rational C_R>=1/integer p_R>=1. On every valid variable input it deterministically computes rational a with |a-log q|<=epsilon and outputs one random binary population X whose UNCONDITIONAL law has TOTAL VARIATION distance <=epsilon from pi. EVERY possible run outputs X in Gamma and uses at most C_R*(1+L)^p_R BIT operations, random bits and memory, where L is the COMPLETE BINARY length of R,lambda,x0,epsilon. This is polynomial in accuracy BIT length, not epsilon^-1. Constants/degree depend computably only on the FIXED reaction structure, not on activities, populations, epsilon or hidden conditioning probabilities. Pay the compiler's finite computable BIT cost and all tables/preprocessing; no free advice, real/exact-counting/optimization/sampling oracle, postselection, expected-only uncapped loop or uncharged factorial/elementary-function evaluation. Pay output lengths, precision, normalization and capped-error budgets. You may challenge the framing; a negative must address this exact fixed-structure contract, with any complexity assumption explicit. Persist toward the FULL endpoint; a restricted family or conditional wrapper is not completion.

ACCEPTED CAPITAL: your FULL E0C e0c34814 volume-relaxation construction and FULL 072d6b36 conservative binary sampler are accepted at their stated scopes, not recurring reproof assignments. 072 supplies smooth factorial localization, finite-bit polynomial-weight approximation, exact fixed-dimensional moment normalization and unconditional sampling, with cost polynomial in L+epsilon^-1 for fixed conservative Theta. Its 1/n factorial remainder, conservation truncation and fixed activity constants do NOT already establish this new uniform, possibly infinite-class, precision-bit contract. ROOT's E0C compressed class locator is accepted for the recorded conservative setting; transfer must be justified rather than assumed.

Actually read source interfaces: Miller1009.2199v2 Sections2-3/Theorem3.3/Proposition3.7, https://arxiv.org/pdf/1009.2199v2 , gives affine-stratification existence for fibers of affine-semigroup maps to commutative monoids, not an already supplied uniform polynomial-bit class compiler. De Loera-Hemmecke-Koppe-Weismantel, Math.Oper.Res.31(2006)147-153 Lemma3.1/Section3, https://www.math.ucdavis.edu/~deloera/RECENT_WORK/fptasNLIP.pdf , gives exact polynomial-weight generating functions and residue evaluation polynomial in degree/input size in FIXED dimension. DLMF5.11.1/5.11(ii), https://dlmf.nist.gov/5.11 , gives positive-real log-Gamma truncation error bounded by the first omitted Bernoulli term. ACK0803.3042v4 Theorems4.1/4.3, https://arxiv.org/pdf/0803.3042v4 , supplies the familiar class-conditioned Poisson equilibrium law for complex-balanced kinetics; no kinetic-mixing or efficient-conditioning theorem is imported.

Optional intuition only: factorial coercivity may give a binary-sized truncation even without conservation, while higher-order factorial approximation may avoid inverse-epsilon degree. You own ALL ideas, representations, methods and source order, may discard this intuition or find a different route.

you may use all subagents avaible
Every helper inherits EVERY existing known/unknown source/access/transfer/resource hold. No retry, mirror/version/alternate or identifying recovery of held originals. ROOT math/0503537v1 and1410.4820v3 HTML404 remain UNREAD/HELD; Leroux-Sutre d-nb.info/990289982/34 governingSection5 timeout/Wang unknown publisher/NSF10314785-Cook-Gacs-Winfree uncertain overlap/Dots/Golding-Henderson/Serre/CarloAlberto/OpenAI-tree/2410.23225v3/TR26-272/2610.00548v2/AB/ZIP/unidentified holds remain. Kahle-Miller1107.4699v5 governing body remains unread; no theorem imported from its metadata. Accepted scopes remain usable without original recovery. No new principal seat/model/worker/resource/spending; Sol closed/Dots protected. Shared retrieval/Personal Context exposure means this is not a blind model comparison.

## Visible working explanation

Refined proof of reachability, approximation, and computational bounds

Planned an approximation

Refined the approximation algorithm and structured its proof

Refined an algorithmic approximation and construction structure

Validated approximation bounds

Refined and strengthened the approximation proof

Refined and structured the proof

Searched 16 websites

## Response, native source text

# P3 — Uniform binary-precision inference

The new requirement is substantially stronger than the accepted conservative sampler: the runtime must be polynomial in the **bit length of \(1/\epsilon\)**, the population and the activities, even when the actual class is infinite and its unconditioned Poisson probability is extraordinarily small.

The central route is to combine an effective description of the actual weakly reversible communicating class with high-precision factorial approximation and fixed-dimensional exact polynomial-weight counting.

## 1\. Infinite classes can be truncated without rare-event rejection

Let \(L\) denote the complete binary input length. Since the positive rational activities and \(\epsilon\) are given in binary,

\[
2^{-L}\le\lambda_i\le2^L,
\qquad
\epsilon\ge2^{-L}.
\]

Put

\[
\Lambda=\sum_i\lambda_i,\qquad n_0=\sum_i x_{0i}.
\]

The target class has probability

\[
q=\Pr(Y\in\Gamma)\ge\Pr(Y=x_0).
\]

Because \(x_{0i}\le2^L\),

\[
\log q
\ge-\Lambda-2Ln_0.
\]

Define the integer

\[
B_0=\lceil\Lambda\rceil+(2L+10)(n_0+1)
\]

and, for a fixed integer accuracy multiplier \(A\ge10\), define

\[
U=16\bigl(B_0+\lceil\Lambda\rceil+AL+d+20\bigr).
\]

Both have \(O_R(L)\) binary digits even if their numerical values are enormous.

For \(Y_i\sim\operatorname{Poisson}(\lambda_i)\), the Chernoff bound gives

\[
\Pr(Y_i>U)\le 2^{-U}
\]

because \(U\ge8\lambda_i\)\. A union bound therefore yields

\[
\Pr(\max_iY_i>U)
\le d\,2^{-U}
\le 2^{-AL-10}q.
\]

Consequently, replacing the possibly infinite class by

\[
\Gamma_U=\Gamma\cap[0,U]^d
\]

changes its conditional Poisson law by at most \(2^{-AL-10}\) in total variation and changes \(\log q\) by at most twice that amount.

**This reduction is unconditional and independent of the magnitude of \(q\)\.** It does not require sampling from an unconditioned Poisson law until the rare event occurs. It also ensures that every subsequent lattice polytope can be made bounded using inequalities whose binary descriptions have length \(O_R(L)\)\.

## 2\. Transfer the E0C class geometry without conservation

The class-location machinery can be extended to the present setting because its algebraic ingredients concern finite translation-invariant reaction templates, not stationary probabilities or finite state spaces.

### 2.1 Reversible graph templates

Weak reversibility means every reaction \(y\to z\) lies on a directed complex cycle. After applying that reaction at \(x\ge y\), the remaining cycle can return to \(x\)\: starting from \(x-y+z\), follow the complex path from \(z\) back to \(y\), carrying the nonnegative residual population \(x-y\)\.

Thus every enabled graph edge is returnable by a fixed reaction word, even with the zero complex and without conservation.

At a finite-control node, transitions can consequently be represented by finitely many symmetric templates

\[
(s,u+a)\longleftrightarrow(t,u+b),
\qquad u\in\mathbb Z_{\ge0}^k,
\]

where the control states \(s,t\) encode species whose populations have already been bounded.

### 2.2 Core-or-bounded-coordinate recursion

Let

\[
F=\mathbb Q[X_1,\ldots,X_k]^Q
\]

and let \(N\) be the submodule generated by the binomial vectors associated with the templates.

For a fixed sufficiently large core threshold \(T\), the accepted Noetherian construction computes \(K\) satisfying

\[
\bigcap_{i=1}^k(N+X_i^KF)
\subseteq N+(X_1\cdots X_k)^TF.
\tag{1}
\]

This gives the same dichotomy for arbitrary population graphs\:

- The actual class reaches a state with all unrestricted coordinates at least \(T\)\.
- Some unrestricted coordinate is less than \(K\) throughout the class.

The proof of (1) does not use a conservation law. Neither does the interpretation of binomial differences as graph connectivity.

The accepted backward-coverability procedure decides whether the first alternative occurs using a fixed finite table. If it fails, separate coverability tests for \(x_i\ge K\) identify a coordinate that is globally bounded, and that coordinate becomes part of the finite control.

The recursion has depth at most \(d\)\.

### 2.3 Exact core-class locator

At a core node, the accepted normalization words take every state reaching the core to a buffered representative with a fixed base control state.

Let \(b\) be the normalized representative obtained from \(x_0\), and let \(\Lambda_R\subseteq\mathbb Z^k\) be the precomputed integer cycle-displacement lattice.

For a candidate state \(x\), a feasible normalization word \(\omega\) maps it to \(x+\Delta_\omega\)\. The buffered Graver connectivity theorem gives the equivalence

\[
\boxed{
x\in\Gamma
\iff
\text{some eligible normalization word }\omega
\text{ has }x+\Delta_\omega-b\in\Lambda_R.
}
\tag{2}
\]

Control-component compatibility is included in eligibility.

Each word has fixed length and fixed population requirements. Its feasibility is expressible by finitely many coordinate inequalities \(x_i\ge h_i\)\. Partitioning at these fixed thresholds and assigning the first eligible word yields an exact *disjoint* representation

\[
\boxed{
\Gamma=\bigsqcup_{j=1}^{J}
\left\{
x=\alpha_j+B_jz:
z\in\mathbb Z^{k_j},\
H_jx\le h_j
\right\}.
}
\tag{3}
\]

Here\:

- \(J\le J_R\), with \(J_R\) a finite compiler-computed constant.
- The matrices \(B_j,H_j\) come from finitely many fixed-structure templates.
- The translated coset origins \(\alpha_j\) and right-hand sides \(h_j\) are computed from \(x_0\) in polynomially many bit operations.
- Every integer point in (3) is genuinely reachable from \(x_0\); no saturated-lattice fibre has replaced the actual class.

Intersecting (3) with \([0,U]^d\) produces finitely many bounded rational lattice polytopes, each with a binary description of length \(O_R(L)\)\.

This establishes the required transfer of the compressed class locator to weakly reversible, possibly infinite classes. The stationary product weights play no role in that transfer.

## 3\. The precision change required beyond 072

In 072, the first-order factorial remainder was controlled using a large-population threshold depending on \(\epsilon^{-1}\)\. That is insufficient here.

Instead, choose a rational working accuracy

\[
\eta=2^{-A_R(L+1)}
\]

with a sufficiently large fixed computable integer \(A_R\)\. Since \(\epsilon\ge2^{-L}\), we can arrange

\[
\eta\le\frac{\epsilon}{10^4}.
\]

The improvement is to use \(O_R(L)\) terms of Stirling's expansion, rather than a fixed number of terms. For positive integer \(n\),

\[
\log(n!)
=
\left(n+\frac12\right)\log n-n
+\frac12\log(2\pi)
+\sum_{r=1}^{s-1}
\frac{B_{2r}}{2r(2r-1)n^{2r-1}}
+\mathcal R_s(n).
\]

For positive real arguments, the remainder is bounded by the magnitude of the first omitted Bernoulli term. citeturn167472view0

Using the elementary bound

\[
|B_{2s}|\le4(2s)!
\]

gives the convenient conservative estimate

\[
|\mathcal R_s(n)|
\le\frac{4(2s)!}{n^{2s-1}}.
\]

If \(s=c_R(L+1)\) and

\[
n\ge Q_R(L+1)^2
\]

for a sufficiently large fixed \(Q_R\), this error is smaller than \(\eta\)\.

For integers below that threshold, the factorial can be computed directly with polynomially many bit operations.

**The resulting factorial evaluator has polynomial cost in \(L\) and \(\log(1/\eta)\), not in \(1/\eta\)\.** It works for populations as large as \(2^{O_R(L)}\), with all logarithms, Bernoulli coefficients and rational error intervals explicitly computed.

## 4\. Find a high-weight anchor in each lattice cell

Write

\[
W_\lambda(x)=\prod_i\frac{\lambda_i^{x_i}}{x_i!},
\qquad
F_\lambda(x)=-\log W_\lambda(x).
\]

To locate the important populations without computing factorials of enormous integers, use the smooth function

\[
h(t)=\left(t+\frac12\right)\log(t+1)-t
\]

and the separable convex surrogate

\[
\Phi_\lambda(t)=
\sum_i\left[h(t_i)-t_i\log\lambda_i\right].
\]

For every nonnegative integer \(n\),

\[
|\log(n!)-h(n)|\le10.
\]

Thus

\[
|F_\lambda(x)-\Phi_\lambda(x)|\le10d
\tag{4}
\]

at every population vector.

Its Hessian satisfies

\[
h''(t)=\frac1{t+1}+\frac1{2(t+1)^2}.
\]

On the global truncation box,

\[
\nabla^2\Phi_\lambda(t)\succeq\frac1{U+1}I,
\qquad
\|\nabla\Phi_\lambda(t)\|_\infty\le g_R(L+1)
\tag{5}
\]

for a compiler-computed integer \(g_R\)\.

Consider one nonempty cell \(S_j\) of (3), intersected with the global box. Let \(P_j\) be its continuous relaxation in the affine span of its lattice coset, and define

\[
a_j^*=\arg\min_{t\in P_j}\Phi_\lambda(t).
\]

### Computing the minimizer

Use an exact-rational ellipsoid implementation with rational approximations to \(\Phi_\lambda\) and its gradient.

The affine hull and its rational description are computed by fixed-dimensional linear algebra. The required positional precision can be chosen as

\[
\delta_{\rm opt}
=\frac1{100d(U+1)(g_R(L+1)+1)}.
\]

Because \(U\) has \(O_R(L)\) bits, the strong-convexity bound (5) implies that the corresponding objective-value precision requires only \(O_R(L)\) bits.

All oracle operations in the ellipsoid implementation are replaced by the explicit logarithm series and rational linear-inequality calculations. Standard rational cutting-plane complexity therefore gives a deterministic \(\operatorname{poly}_R(L)\)\-bit procedure for a feasible rational approximation \(\widetilde a_j\)\.

### Obtaining an integer anchor

The cell's integer constraints have a fixed coefficient matrix. Its fixed Graver basis gives a computable proximity constant \(G_R\)\: some integer optimum of the separable convex objective lies within \(G_R\) in \(\ell_\infty\) distance of the continuous optimum. The fixed-matrix proximity principle is established for separable convex integer programming. citeturn174812view2

Enumerate the integer vectors within distance \(G_R+2\) of \(\widetilde a_j\), testing the exact lattice congruence and cell inequalities. At least one succeeds.

Call the first successful vector \(m_j\)\. This search tests only \(O_R(1)\) candidates, independently of the numerical population sizes.

By (5),

\[
\boxed{
0\le\Phi_\lambda(m_j)-\Phi_\lambda(a_j^*)
\le b_R(L+1)
}
\tag{6}
\]

for a computable \(b_R\)\.

This supplies a certified high-weight anchor for every nonempty cell, including one consisting of a single boundary population.

## 5\. Localize the weight without introducing an exponential polynomial degree

A coordinate box alone is insufficient. If the constrained optimum lies on an active boundary, the log-weight can change by an exponentially large amount across a box of Poisson-scale width.

The required additional ingredient is a rational approximation to a supporting-gradient inequality.

Let \(N=L+1\), and choose

\[
T=K_RN
\]

for a sufficiently large compiler-computed integer \(K_R\)\.

Put \(a=a_j^*\) and \(g=\nabla\Phi_\lambda(a)\)\. Convex optimality gives

\[
g\cdot(x-a)\ge0,\qquad x\in P_j.
\]

The separable Bregman divergence satisfies

\[
\Phi_\lambda(x)-\Phi_\lambda(a)-g\cdot(x-a)
\ge
\sum_i
\frac{(x_i-a_i)^2}
{2(\max\{x_i,a_i\}+1)}.
\tag{7}
\]

In particular, every point with surrogate-energy excess at most \(T\) satisfies

\[
|x_i-a_i|\le2T+\sqrt{2T(a_i+1)}.
\tag{8}
\]

Compute integer radii

\[
D_i=
\left\lceil
10T+10\sqrt{T(\widetilde a_{ji}+2)}+10
\right\rceil.
\]

The square roots are rounded upwards by integer arithmetic; no irrational value is stored.

Calculate a rational gradient approximation \(\widetilde g_j\) sufficiently accurately that, throughout \([0,U]^d\),

\[
\left|
\widetilde g_j\cdot(x-\widetilde a_j)
-g\cdot(x-a)
\right|\le1.
\]

This requires \(O_R(L)\) precision bits.

Define the retained rational polytope

\[
\boxed{
\mathcal K_j=
P_j
\cap\bigcap_i\{|x_i-\widetilde a_{ji}|\le D_i\}
\cap
\{\widetilde g_j\cdot(x-\widetilde a_j)\le T+2\}.
}
\tag{9}
\]

Every integer point of \(S_j\) with energy excess at most \(T\) belongs to \(\mathcal K_j\)\. The anchor \(m_j\) also belongs to \(\mathcal K_j\) by choosing \(K_R\) sufficiently large relative to (6).

### Tail mass

Every excluded point has surrogate-energy excess greater than \(T\)\. Equations (4) and (6) give

\[
\frac{W_\lambda(x)}{W_\lambda(m_j)}
\le
\exp[-T+b_RN+20d].
\]

There are at most \((U+1)^d\) populations in the global box. Since

\[
\log(U+1)\le u_RN
\]

for a compiler-computed \(u_R\), choosing \(K_R\) large enough yields

\[
\boxed{
\sum_{x\in S_j\setminus\mathcal K_j}W_\lambda(x)
\le\eta\sum_{x\in S_j}W_\lambda(x).
}
\tag{10}
\]

This bound is relative to the cell's own weight and requires no minimum probability assumption.

### Uniform log-weight range

For any \(x\in\mathcal K_j\), the supporting-gradient term satisfies

\[
g\cdot(x-a)\le T+3.
\]

The coordinate box also gives an upper bound on the Bregman divergence.

When \(a_i\ge1000T\), the interval in (9) stays a fixed fraction away from zero and \(h''(t)=O(1/a_i)\)\. Its Bregman contribution is \(O(T)\)\.

When \(a_i<1000T\), the interval has width \(O(T)\), and \(h''(t)\le3/2\) gives a contribution \(O(T^2)\)\.

Consequently an explicit computable \(M_R\) satisfies

\[
\Phi_\lambda(x)-\Phi_\lambda(a)\le M_RN^2.
\]

Combining this with (4) and (6),

\[
\boxed{
|F_\lambda(x)-F_\lambda(m_j)|
\le M'_RN^2
\quad
\text{for every integer }x\in S_j\cap\mathcal K_j.
}
\tag{11}
\]

This is the crucial improvement over the previous sampling construction: even though the populations can be exponentially large, the *log-weight variation on the retained support* is polynomial in the binary input length.

## 6\. Construct a polynomial-precision rational weight polynomial

Using (11), construct

\[
P_j\in\mathbb Q[x_1,\ldots,x_d]
\]

such that

\[
\boxed{
(1-\eta)\frac{W_\lambda(x)}{W_\lambda(m_j)}
\le P_j(x)\le
(1+\eta)\frac{W_\lambda(x)}{W_\lambda(m_j)}
}
\tag{12}
\]

for every retained integer point.

The construction is entirely finite-bit.

Choose a threshold

\[
Q=2^{24}(T+s+A_RN+2)^2,
\qquad s=c_RN,
\]

where \(c_R\) is sufficiently large to meet the Stirling precision certificate. Thus \(Q=O_R(N^2)\)\.

For coordinates with \(a_{ji}^*<Q\), every integer value occurring in \(\mathcal K_j\) is at most \(2Q\)\. Compute rational approximations to \(\log(n!)\) for all \(0\le n\le2Q\), with prescribed error \(\eta/(100d)\), and interpolate those values by a rational polynomial. The number of values and the interpolation degree are polynomial in \(N\)\.

For coordinates with \(a_{ji}^*\ge Q\), all retained populations satisfy \(x_i\ge Q/2\)\. The high-order Stirling expansion of Section 3 applies. Expand its logarithmic and inverse-power terms about a nearby integer center \(t_i\)\. The localization bounds ensure

\[
\left|\frac{x_i-t_i}{t_i}\right|\le\frac1{20}.
\]

Truncating the ordinary logarithmic and negative-binomial Taylor series after \(O_R(N)\) terms yields error below \(\eta/(100d)\), including the multiplication by exponentially large \(x_i\)\.

The logarithms of \(\lambda_i\) are evaluated to sufficient rational precision before multiplication by \(x_i\)\.

Combining these coordinate polynomials and subtracting their value at \(m_j\) gives a rational polynomial \(H_j\) with

\[
|H_j(x)-[F_\lambda(x)-F_\lambda(m_j)]|
\le\eta/4
\]

at every retained integer point, and

\[
\deg H_j=O_R(N^2),\qquad
|H_j(x)|\le M''_RN^2.
\]

Now take the finite Taylor polynomial

\[
P_j(x)=
\sum_{k=0}^{r}
\frac{[-H_j(x)]^k}{k!},
\qquad
r=\left\lceil20(M''_RN^2+A_RN+10)\right\rceil.
\]

The explicit exponential remainder bound

\[
\left|e^{-H}-\sum_{k=0}^{r}\frac{(-H)^k}{k!}\right|
\le e^{|H|}\frac{|H|^{r+1}}{(r+1)!}
\]

proves (12), after allocating the stated precision margins.

In particular,

\[
\boxed{
\deg P_j=O_R(N^4),
}
\]

and all rational coefficients have polynomially bounded binary encoding lengths.

The polynomial need not be positive between integer populations. Equation (12) guarantees strict positivity at every integer point where it will be used.

## 7\. Exact normalization and sampling by polynomial-weight moments

For each retained cell compute

\[
M_j=
\sum_{x\in S_j\cap\mathcal K_j}P_j(x).
\tag{13}
\]

Parameterizing the affine lattice as \(x=\alpha_j+B_jz\) turns this into a rational-polynomial weighted lattice-point sum in fixed dimension.

The De Loera–Hemmecke–Köppe–Weismantel weighted generating-function construction computes such sums exactly with bit complexity polynomial in the input size and polynomial degree, provided dimension is fixed. Rational polynomial coefficients are handled by clearing a finite common denominator. citeturn683572view0

The same routine computes cumulative weights after adding constraints \(x_i\le t\)\.

### Relative cell normalizers

Calculate rational approximations \(\widetilde\ell_j\) to

\[
\ell_j=\log W_\lambda(m_j)
\]

with absolute error at most \(\eta\), using the high-precision factorial evaluator.

Choose an anchor \(j_*\) maximizing \(\widetilde\ell_j\)\. Discard cells for which

\[
\widetilde\ell_{j_*}-\widetilde\ell_j
>H_R^{\rm drop}N,
\]

where the fixed computable threshold is chosen larger than the logarithm of the maximum population count plus the anchor-energy surplus.

The discarded total weight is at most an \(\eta\) fraction of the full truncated weight.

For every retained cell compute a positive rational

\[
r_j=(1\pm\eta)
\frac{W_\lambda(m_j)}{W_\lambda(m_{j_*})}.
\]

The retained exponent differences are \(O_R(N)\), so rational exponential evaluation needs only polynomially many precision bits.

Now calculate the exact positive rational

\[
\widehat Z=\sum_{j\text{ retained}}r_jM_j.
\tag{14}
\]

Crucially, \(\widehat Z\) is a relative normalizer. It does not contain the potentially unrepresentably tiny factor \(e^{-\Lambda}\)\.

## 8\. Deterministically compute \(\log q\)

The desired class probability is

\[
q=e^{-\Lambda}\sum_{x\in\Gamma}W_\lambda(x).
\]

The construction gives

\[
q\approx e^{-\Lambda}W_\lambda(m_{j_*})\widehat Z
\]

with certified multiplicative error \(1\pm O(\eta)\), apart from the explicitly controlled global truncation, localization and cell-discard errors.

Compute

\[
\boxed{
a=-\Lambda+\widetilde\ell_{j_*}
+\widetilde{\log\widehat Z},
}
\tag{15}
\]

where both tilded quantities are rational approximations with predetermined absolute-error bounds.

The logarithm of the positive rational \(\widehat Z\) is evaluated by binary range reduction and the convergent series

\[
\log u=
2\sum_{k=0}^{s}
\frac{z^{2k+1}}{2k+1}+\mathcal R_s,
\qquad z=\frac{u-1}{u+1}.
\]

After range reduction \(|z|\le1/3\), and a polynomial number of terms gives the prescribed precision. All rational intermediate values have polynomially bounded bit lengths.

The potentially enormous terms \(-\Lambda\) and \(\widetilde\ell_{j_*}\) are stored as binary rationals. Their magnitudes may be exponential in \(L\), but their representations have polynomial length. No exponentially small probability is ever explicitly formed.

The relative-normalization error implies

\[
|\log q-\log q_{\rm approx}|
\le O(\eta),
\]

and the additive rational-evaluation error is independently bounded. Choosing the compiled precision constants to allocate less than \(\epsilon/10\) to each contribution gives

\[
\boxed{|a-\log q|\le\epsilon.}
\tag{16}
\]

## 9\. Generate one valid population with bounded randomness

Use the exact rational cell weights \(r_jM_j\) to choose a retained cell.

Inside that cell, sample population coordinates sequentially by binary splitting. A split at \(x_i\le t\) requires two exact weighted sums over rational lattice polytopes, obtained from (13) by appending the corresponding inequality.

At any decision with rational probability \(p\), generate exactly \(b\) fair bits and select the first branch when the resulting uniform integer in \(\{0,\ldots,2^b-1\}\) is less than

\[
\lfloor 2^bp\rfloor.
\]

This changes the branch probability by less than \(2^{-b}\)\. Take

\[
b=A_R(L+1).
\]

There are at most \(O_R(L)\) decisions because the number of cells is fixed and each population coordinate is bounded by \(U=2^{O_R(L)}\)\.

Consequently,

\[
\text{random bits}=O_R(L^2),
\]

and

## Response continuation, transcribed from the displayed response


the total variation error from all rounded decisions is at most

\[
O_R(L)\,2^{-A_R(L+1)}.
\]

Every nonzero branch weight is a sum of strictly positive rational weights over genuine points in \(S_j\cap K_j\). Thus every branch selected with positive probability has at least one valid continuation.

It follows that

\[
\Pr(X\in\Gamma)=1 \tag{17}
\]

for every execution, not merely with high probability.

No rejection sampling, failure restart, postselection or unbounded random-bit loop is used.

### Total variation

The total error is bounded by the sum of the global tail, local concentration tails, discarded-cell mass, rational polynomial-weight distortion, relative-scale distortion and finite-bit branching error.

The first three are bounded relative to the actual class mass, not relative to the unconditioned Poisson mass. The pointwise estimate (12) controls the normalized distribution on all retained integer populations.

With the compiler's fixed precision multipliers chosen sufficiently large,

\[
\|\mathcal L(X)-\pi\|_{\mathrm{TV}}\le\epsilon. \tag{18}
\]

This is the unconditional entire output law.

## 10. Compiler and per-invocation bit costs

The complete compiler performs finite exact computation of the Noetherian thresholds, backward-coverability tables, normalization words, control-graph lattices, Graver bases, fixed proximity bounds and all finite resource constants.

It also emits explicit implementations of rational convex minimization, logarithm and factorial approximation, polynomial interpolation, truncated exponential approximation, exact weighted generating-function summation and finite-bit branching.

Every operation is charged.

Let \(N=1+L\). The dominant per-invocation object sizes satisfy:

| Quantity | Effective bound |
| --- | --- |
| Global population cutoff | \(O_R(L)\) bits |
| Class decomposition | At most \(J_R\) cells |
| Convex optimizer precision | \(O_R(L)\) bits |
| Anchor search | \(O_R(1)\) candidates per cell |
| Concentration energy \(T\) | \(O_R(N)\) |
| Small-population threshold \(Q\) | \(O_R(N^2)\) |
| Retained log-weight range | \(O_R(N^2)\) |
| Stirling and local Taylor orders | \(O_R(N)\) |
| Rational weight polynomial degree | \(O_R(N^4)\) |
| Moment calculations | \(O_R(N)\) calls |
| Random bits | \(O_R(N^2)\) |
| Output encoding | \(O_R(N)\) bits |

Because the dimensions, numbers of cells and fixed constraint matrices are constants determined by \(R\), all exact weighted-moment calls and their intermediate rational arithmetic have polynomial bit costs.

### Computing the stated constants

Instrument the deterministic compiler to count every elementary bit operation, including the creation of its finite tables. Let its completed compilation cost be \(T_{\mathrm{comp}}(R)\).

The compiler constructs a nonnegative integer-coefficient resource polynomial

\[
P_R(N)=\sum_{k=0}^{t_R} a_k N^k
\]

by composing the explicit bit bounds of the emitted algorithms. Include \(T_{\mathrm{comp}}(R)\) as a constant term.

Return

\[
p_R=\max(1,t_R),\qquad C_R=1+\sum_{k=0}^{t_R}a_k. \tag{19}
\]

These are computable from the fixed reaction structure, with \(C_R\) a positive integer and hence an admissible rational constant.

For every valid input and every realization of the random bits,

\[
\begin{aligned}
\text{BIT operations}&\le C_R(1+L)^{p_R},\\
\text{Random bits}&\le C_R(1+L)^{p_R},\\
\text{Memory bits}&\le C_R(1+L)^{p_R}.
\end{aligned} \tag{20}
\]

The bound even absorbs the fixed one-time compilation cost. No table, coefficient, precision parameter or arithmetic operation is treated as uncharged advice.

## 11. Full endpoint

The construction yields a positive resolution of the stated fixed-structure inference question:

\[
a\in\mathbb Q,\quad |a-\log q|\le\epsilon,\qquad
X\in\Gamma\text{ on every run},\qquad
\|\mathcal L(X)-\pi\|_{\mathrm{TV}}\le\epsilon,\qquad
\text{every-run resources}\le C_R(1+L)^{p_R}.
\]

It applies to finite or infinite actual classes, arbitrary positive binary-rational activities, zero-complex reactions, disabled boundaries, lattice congruences, singleton classes and arbitrarily rare conditioning events.

The proof has two genuinely new requirements beyond the accepted E0C/072 scopes. First, the finite-control algebra must be used without conservation to produce the exact affine-lattice cell representation of an unbounded communicating class. Second, the retained cells need both coordinate localization and a supporting-gradient cut, followed by high-order Stirling approximation, so that polynomial-weight counting achieves precision polynomial in \(\log(1/\epsilon)\) rather than \(\epsilon^{-1}\).

The central computational consequence is that conditioning on an arbitrarily rare actual reaction class need not be implemented by rejection. Its log probability and conditional samples can instead be recovered from a fixed number of compressed weighted lattice computations.

This is a constructive mathematical argument, not an independently certified implementation or externally peer-verified theorem. Its full claim depends particularly on the exact unbounded-class cell construction and the fixed-matrix proximity/localization interface established above; those are the interfaces that warrant independent formal checking.

