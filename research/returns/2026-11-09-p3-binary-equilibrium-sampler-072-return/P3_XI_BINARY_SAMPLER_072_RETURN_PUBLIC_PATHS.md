# P3 Xi binary-size equilibrium sampler return

Source: https://chatgpt.com/c/6af11227-f57c-83ec-80e4-caf25a4bae01
Model: GPT-6 standard, Extra High. Turn 072d6b36-cb03-40bf-9d8e-196cb7de0f8b; response a1b67654-ba14-42ce-a7b5-70503cb3ba4e. UI showed a complete response and idle composer.
Capture: native reader returned 20,000 characters with truncation. The response through section 8 is preserved from that native text; section 9 onward is transcribed from the rendered view with TeX mathematical annotations, not raw source. The expanded visible activity and one available code/output trace are included. No producer ZIP visible.

## Actual prompt

P3: pursue this ONE DIFFERENT FULL computational question, keeping your current context and the accepted complete volume-relaxation construction.

For EVERY fixed finite conservative complex-balanced mass-action network Theta=(y_r->z_r,kappa,c,w,R) with arbitrary arities/linkages, positive binary-rational kappa,c,w,R, w.(z_r-y_r)=0 and the exact complex-balance identities, construct a uniform finite algorithm for sampling its equilibrium law efficiently in the COMPLETE BINARY input length, including enormous populations.

Variable input is integer V>=1 in BINARY, x0 in Z_+^d in BINARY with w.x0<=R*V, and rational 0<epsilon<1. Gamma is the ACTUAL closed communicating class of x0 under the original enabled reaction rules. Output ONE binary population vector whose UNCONDITIONAL law is within TOTAL VARIATION epsilon of pi_(V,Gamma)(x)=Z_Gamma^-1*prod_i(V*c_i)^x_i/x_i!, x in Gamma. All disabled boundaries, singleton classes, rare conservation conditions, lattice congruences and small species populations are included. No promised interior, typical class, supplied support decomposition, known partition function or minimum conditioning probability.

FULL positive endpoint: ONE terminating deterministic compiler taking Theta to a randomized sampler and COMPUTABLE rational C_Theta>=1/integer p_Theta>=1, such that EVERY RUN on every valid variable input uses at most C_Theta*(1+L+epsilon^-1)^p_Theta BIT operations, random bits and memory, where L is the complete binary length of Theta,V,x0,epsilon. Pay the compiler's own finite computable BIT cost and any preprocessing per invocation; it cannot be an uncharged advice table. Constants and degree may depend computably on fixed Theta, not on V,x0,epsilon. Give the full uniform argument. This is genuinely polynomial in log V and population bit lengths: a numeric-V chain simulation or population/state enumeration is not the endpoint. Output encoding length, rational heights, elementary-function evaluation, normalization, class access, all randomness, capped failures and unconditional fallback errors are paid. No real/exact-counting/optimization/sampling oracle, infinite precision, expected-time-only loop, postselection or free rare conditioning.

A genuine negative may use a precisely stated complexity assumption, but must address this exact FIXED-Theta finite-bit sampling contract. Changing Theta/dimension with V or showing that the original physical chain mixes slowly is not a negative to it. You may challenge or improve the framing. Persist toward full resolution; a conditional wrapper or easier family is not completion.

ACCEPTED CAPITAL: your COMPLETE E0C return e0c34814-8d24-4d6d-be62-c51cac331891 constructs the uniform numeric-V Poincare theorem for all these actual classes. Its finite-control module dichotomy, terminating backward coverability, fixed-word Graver realizations, convex weight paths and original-clock comparison are accepted at their actual scope; no recurring reproof assignment. Its physical/optional per-V costs are not already a binary-size sampler. Root independently checked the key module, lifting, convexity and clock interfaces. Standard stationary-product/Graver/Noetherian machinery is credited once.

One useful consequence ROOT checked: from your finite coverability bases, core membership is decidable by comparisons with fixed minimal vectors. If core is unreachable, precompute coverability of each target x_i>=K; a failed test identifies a coordinate globally bounded on this class and selects a child. At a core node, the stored bounded words normalize to base control and an explicit lattice coset. Comparing normalized buffered representatives by integer-lattice membership decides whether they are in the same class. All these tables are fixed-Theta finite preprocessing; this supplies a plausible compressed class locator, not a weighted normalizer or sampler.

Read source contracts freely in your own order. Relevant actually read interfaces: Eisenbrand etal arXiv:1904.01361v3 Definition2/Proposition3 and Theorem32/Corollary35 give sign-compatible/proximity-scaling operations for separable-convex OPTIMIZATION, not weighted sampling: https://arxiv.org/html/1904.01361v3 . Pak, On sampling integer points in polyhedra (2002), Theorem1/Section1 reduces UNIFORM integer-point sampling to paid counting: https://math.ucla.edu/~pak/papers/barv2.pdf ; it does not count factorial weights. Barvinok, Computing the theta function, author PDF dated4June2023, Sections2.4/7.2-7.5, gives discrete-Gaussian TV sampling under explicit theta/Gram conditions with polynomial dependence on inverse lambda_min: https://sites.lsa.umich.edu/barvinok/wp-content/uploads/sites/1434/2025/05/thetalog.pdf . No free well-conditioned Gaussian or counting premise is supplied.

Optional intuition only: your finite class geometry may permit accelerated or scaled weighted sampling, but all boundary mass, parameter-dependent anisotropy and normalization must be handled. You own every idea, representation, method and source order, may discard this intuition and may find an unexpected route.

you may use all subagents avaible
Every helper inherits EVERY existing known/unknown source/access/transfer/resource hold. No retry, mirror/version/alternate or identifying recovery of held originals. NEW ROOT https://arxiv.org/html/math/0503537v1 returned404 and remains UNREAD/HELD; no alternate recovery or theorem import. Existing1410.4820v3 unread404/Leroux-Sutre d-nb.info/990289982/34 Section5 timeout/Wang publisher unknown-original/NSF10314785-Cook-Gacs-Winfree uncertain overlap/Dots/Golding-Henderson/Serre/CarloAlberto/OpenAI-tree/2410.23225v3/TR26-272/2610.00548v2/AB/ZIP/unidentified holds remain. Accepted scopes remain usable without recovering originals. No new principal seat/model/worker/resource/spending; Sol closed/Dots protected. Shared retrieval/Personal Context exposure means this is not a blind model comparison.

## Available user-visible activity

Worked for 32m 57s.

Developed a theoretical counting approach with refined local approximations I’ll use the accepted class-locator as the starting point, then look for a sampler that works directly with the factorial-product weights in binary-size time. The key subproblem is sampling a fixed-dimensional lattice-coset region without enumerating its potentially enormous population range or conditioning on a rare event. Structured class regions and built an efficient sampler Refined sampler using algorithmic foundations and polynomial weighting Developed and refined weighted lattice sampling for relevant high-weight regions Refined the approximation algorithm and weighted counting approach

Searched 16 websites

The class geometry appears strong enough for a binary-size approach: at a selected core node, the accepted bounded-word construction can describe the class as finitely many disjoint lattice-coset cells with fixed coordinate thresholds. That avoids rare-event rejection. I’m checking whether factorial weights on those cells can be approximated and summed using only polynomially many bits. Refined the sampler approximation and proof structure

Searched 12 websites

Refined the sampler

Developed a fully polynomial sampler for fixed-dimensional Petri nets

Refined the sampler and finalized its construction Refined sampler construction Refined and structured the sampler and sampling proof

Searched 14 websites

A useful analytic simplification is to replace log(n!) temporarily by a smooth convex surrogate whose error is bounded by a constant for every integer n, even when n is enormous. That gives a polynomial-bit concentration box around each cell’s continuous optimum. Inside the box, rational polynomials can approximate the true weights, allowing exact fixed-dimensional polynomial-weight counting. Refined construction and finalized complexity bounds

Analyzed — Python:
```python
import math
def diff(n):
    return math.lgamma(n+1)-((n+.5)*math.log(n+1)-n)
for n in [0,1,2,3,4,5,10,100,1000,10000]:
    print(n,diff(n))
```

STDOUT/STDERR:
```
0 0.0
1 -0.039720770839917874
2 -0.05338354111032961
3 -0.06027079469156149
4 -0.06441677560550607
5 -0.0671853379722549
10 -0.07348779130737881
100 -0.08023638698313107
1000 -0.08097821671526617
10000 -0.08105313431588002
```

## Complete available response

# P3 — Binary-size equilibrium sampling

The accepted E0C construction supplies more than a polynomial physical-time relaxation bound. Its bounded-word and buffered-lattice structure can be used to eliminate the most difficult obstacle to direct sampling: identifying the **actual communicating class without enumerating its populations**\.

The proposed route is to replace simulation of the reaction chain by finite-dimensional weighted lattice-point sampling.

## 1\. Exact compressed representation of the class

For each fixed network \(\Theta\), the E0C finite-control construction can be compiled into finitely many class templates.

Given binary \(V,x_0\), its coverability tests select a node in the finite-control tree. At a core node, every state in the class has a bounded-length physical reaction word that reaches a buffered base-control state.

For each such word \(\omega\), feasibility from population \(x\) is equivalent to finitely many inequalities

\[
x_i\ge h_{\omega i},
\]

where \(h_{\omega i}\) are fixed integers. Its endpoint differs from \(x\) by a fixed vector \(\Delta_\omega\)\.

The buffered-lattice theorem then gives the exact membership condition

\[
x+\Delta_\omega-b\in\Lambda,
\]

where \(b\) is one computed buffered representative and \(\Lambda\) is the node's fixed integer cycle lattice.

For a fixed control state, the different word displacements belong to the same lattice coset. Partitioning the finitely many threshold inequalities into disjoint regions yields

\[
\boxed{
\Gamma=\bigsqcup_{j=1}^{J_\Theta}
\left\{
a_j+B_jz:
z\in\mathbb Z^{k_j},\
\ell_j\le a_j+B_jz\le u_j
\right\}.
}
\tag{1}
\]

Empty regions are omitted. Each \(B_j\), its dimension and the number of templates are fixed by \(\Theta\)\. The translated origins \(a_j\) and any population-dependent bounds have binary lengths \(O_\Theta(L)\)\. Coordinates bounded by the E0C recursion can be split into finitely many exact control values.

The same representation applies to classes selected through the noncore branches, by recursively incorporating their globally bounded coordinates into the finite controls.

**Consequences.** Equation (1) is an exact, disjoint support decomposition, not a stoichiometric-fibre approximation. Its construction costs polynomially many bit operations in \(L\) after finite fixed-network compilation. It preserves disabled boundaries, congruences, singleton classes and the original conserved population.

It reduces P3 to the following computational task\:

> Sample factorial-product weights on finitely many fixed-dimensional affine lattice polytopes with binary-sized right-hand sides, without enumerating their integer points.

## 2\. A smooth convex surrogate for factorial weights

The main analytic device is a surrogate with a uniformly bounded approximation error, independent of the population size.

For integer populations define

\[
F_V(x)=\sum_{i=1}^d
\left[\log(x_i!)-x_i\log(Vc_i)\right].
\]

The equilibrium weights are proportional to \(e^{-F_V(x)}\)\.

For real \(t\ge0\), put

\[
h(t)=\left(t+\frac12\right)\log(t+1)-t
\]

and define

\[
\Phi_V(t)=\sum_{i=1}^d
\left[h(t_i)-t_i\log(Vc_i)\right].
\]

Two properties are decisive.

### 2.1 Uniform factorial approximation

Stirling's inequalities give, for every integer \(n\ge0\),

\[
\left|\log(n!)-h(n)\right|\le10.
\]

More precisely, writing

\[
\delta_\infty=\frac12\log(2\pi)-1,
\]

one has the conservative bound

\[
\left|\log(n!)-h(n)-\delta_\infty\right|
\le\frac{10}{n+1}.
\tag{2}
\]

Consequently,

\[
\boxed{|F_V(x)-\Phi_V(x)|\le10d}
\tag{3}
\]

at every integer population, regardless of \(V\)\.

Notice that this is an *additive log-weight error*, not a relative factorial error growing with \(V\)\.

### 2.2 Strong convexity

Direct differentiation gives

\[
h'(t)=\log(t+1)-\frac1{2(t+1)},
\]

\[
\boxed{
h''(t)=\frac1{t+1}+\frac1{2(t+1)^2}>0.
}
\]

Let

\[
A_\Theta=\max\left\{1,\left\lceil\frac{R}{\min_iw_i}\right\rceil\right\}.
\]

All feasible populations satisfy \(x_i\le A_\Theta V\)\. On the corresponding continuous domain,

\[
\nabla^2\Phi_V(t)\succeq
\frac1{A_\Theta V+1}I.
\tag{4}
\]

Also,

\[
\|\nabla\Phi_V(t)\|_\infty
\le a_\Theta(1+L)
\tag{5}
\]

for an effectively computable integer \(a_\Theta\)\.

These estimates use only rational arithmetic and logarithms of positive rationals. The latter can be evaluated by finite, explicitly bounded power series.

## 3\. Every cell has a computable concentration box

Consider one nonempty cell \(S_j\) from (1), and let \(P_j\) be its continuous affine-lattice relaxation, retaining its fixed coordinate equalities and lower bounds.

Let

\[
a_j^*=\arg\min_{t\in P_j}\Phi_V(t).
\]

Strict convexity gives a unique minimizer in the population coordinates.

### 3.1 Find a nearby feasible integer population

The fixed-lattice proximity theorem applies after writing the cell as

\[
x-B_jz=a_j,\qquad x,z\text{ integral},
\]

and treating \(\Phi_V(x)\) as a separable convex objective with zero cost on the auxiliary \(z\)\-coordinates.

The resulting constraint matrix is fixed by \(\Theta\)\. Its Graver proximity bound is therefore a fixed computable integer \(H_\Theta\)\.

There exists an integer population \(m_j\in S_j\) satisfying

\[
\|m_j-a_j^*\|_\infty\le H_\Theta.
\tag{6}
\]

This is the applicable form of the basic proximity theorem of Eisenbrand and collaborators. citeturn668709view0

We do not need to solve the discrete factorial-weight optimization problem.

Instead, calculate a rational feasible approximation \(\widetilde a_j\) to \(a_j^*\) with

\[
\|\widetilde a_j-a_j^*\|_\infty\le\frac14.
\]

This can be done in polynomial bit time by rational convex cutting planes. Indeed, (4) converts an objective-value accuracy of order \(1/(A_\Theta V+1)\) into the required positional accuracy. The logarithmic evaluation and separation precision require \(O_\Theta(L)\) bits.

Then enumerate the fixed-radius integer cube

\[
\|x-\widetilde a_j\|_\infty\le H_\Theta+2
\]

and select its first point in \(S_j\)\.

The cube has at most

\[
(2H_\Theta+5)^d
\]

candidates, a number independent of \(V\)\. Exact lattice-coset membership determines feasibility.

From (5) and (6),

\[
\Phi_V(m_j)-\Phi_V(a_j^*)
\le b_\Theta(1+L)
\tag{7}
\]

for a computable constant \(b_\Theta\)\.

### 3.2 A concentration estimate without a Gaussian assumption

For each coordinate the Bregman divergence of \(h\) satisfies

\[
h(x)-h(a)-h'(a)(x-a)
\ge
\frac{(x-a)^2}{2(\max\{x,a\}+1)}.
\]

The first-order optimality condition at \(a_j^*\) therefore gives, for all \(x\in P_j\),

\[
\boxed{
\Phi_V(x)-\Phi_V(a_j^*)
\ge
\sum_{i=1}^d
\frac{(x_i-a_{ji}^*)^2}
{2(\max\{x_i,a_{ji}^*\}+1)}.
}
\tag{8}
\]

In particular, points whose surrogate energy is within \(T\) of the optimum satisfy

\[
|x_i-a_{ji}^*|
\le 2T+\sqrt{2T(a_{ji}^*+1)}.
\tag{9}
\]

Choose a computable integer \(K_\Theta\) sufficiently large and set

\[
T=K_\Theta(1+L).
\]

Using \(\widetilde a_j\), construct integer radii

\[
D_{ji}=
\left\lceil
4T+4\sqrt{T(\widetilde a_{ji}+2)}
+H_\Theta+8
\right\rceil.
\]

Integer square-root arithmetic, rounded upwards, suffices.

Define

\[
\mathcal B_j=
\{x:|x_i-\widetilde a_{ji}|\le D_{ji}
\text{ for every }i\}.
\tag{10}
\]

The box contains \(m_j\) and every point with surrogate-energy excess at most \(T\)\.

### 3.3 Explicit tail bound

Equations (3) and (7) imply

\[
F_V(x)-F_V(m_j)
\ge
\Phi_V(x)-\Phi_V(a_j^*)
-b_\Theta(1+L)-20d.
\]

Thus for \(x\in S_j\setminus\mathcal B_j\),

\[
\frac{W_V(x)}{W_V(m_j)}
\le
\exp\!\left[-T+b_\Theta(1+L)+20d\right].
\]

Since

\[
|S_j|\le(A_\Theta V+1)^d,
\]

and both \(\log V\) and \(\log(\epsilon^{-1})\) are bounded by the binary input length, \(K_\Theta\) can be computed large enough that

\[
\boxed{
\sum_{x\in S_j\setminus\mathcal B_j}W_V(x)
\le\frac{\epsilon}{100J_\Theta}
\sum_{x\in S_j}W_V(x).
}
\tag{11}
\]

This estimate applies even if the cell lies entirely on a boundary face or has extremely small probability under an unconditioned product-Poisson law.

## 4\. Replace the retained factorial weights by a rational polynomial

The concentration box may still contain exponentially many integer populations. We will not enumerate them.

Let

\[
N=1+L+\epsilon^{-1},
\qquad
\eta=\frac{\epsilon}{1000}.
\]

Choose a rational-integer threshold

\[
Q=
\left\lceil
\frac{10^6(d+1)(T+H_\Theta+2)^2}{\eta}
\right\rceil.
\tag{12}
\]

In particular,

\[
Q\le q_\Theta N^3
\]

for a computable constant \(q_\Theta\)\.

Split coordinates according to whether their continuous center \(a_{ji}^*\) is below or above \(Q\)\. The rational approximation \(\widetilde a_j\), with an additional unit of padding at the threshold, implements the split deterministically.

### 4.1 Small coordinates

If \(a_{ji}^*\) is below \(Q\), every integer value of \(x_i\) in \(\mathcal B_j\) is at most \(2Q+O_\Theta(1)\)\.

For each such integer \(k\), compute a rational approximation to

\[
\log(k!)-k\log(Vc_i)
\]

with error at most \(\eta/(100d)\)\.

Interpolate these finitely many values by a rational polynomial \(H_{ji}(t)\)\.

This polynomial has degree \(O_\Theta(Q)\)\. Its values at the relevant integer arguments approximate the *true factorial log-weights*, regardless of its behavior between those integers.

The interpolation table has polynomial size in \(N\)\. It does not enumerate populations of size \(V\) unless \(V\) itself is bounded by this permitted polynomial in \(N\)\.

### 4.2 Large coordinates

If \(a_{ji}^*\ge Q\), (10)–(12) guarantee that throughout the retained box,

\[
x_i\ge Q/2
\]

and

\[
\left|\frac{x_i-t_i}{t_i+1}\right|\le\frac13,
\]

where \(t_i\) is a nearby integer center.

Expand

\[
\log(x_i+1)
=
\log(t_i+1)+
\sum_{k=1}^{s}
\frac{(-1)^{k+1}}{k}
\left(\frac{x_i-t_i}{t_i+1}\right)^k
+\mathcal R_s.
\]

The remainder decreases geometrically. Taking

\[
s=O_\Theta(L+\log\eta^{-1})
\]

controls the error even after multiplication by \(x_i+\tfrac12\), which may be as large as \(O(V)\)\.

This produces a rational polynomial approximation \(H_{ji}\) to the surrogate coordinate energy.

The approximation is also sufficient for **differences of true factorial energies**\. By (2), for two integers \(n,m\ge Q/2\),

\[
\left|
[\log(n!)-h(n)]-
[\log(m!)-h(m)]
\right|
\le\frac{40}{Q}.
\]

The constant \(\delta_\infty\) cancels. Choosing \(Q\) as in (12) makes the total correction smaller than the required error budget.

### 4.3 Polynomial log-ratio approximation

Combine the coordinate polynomials\:

\[
H_j(x)=
\sum_{i=1}^d
\left[H_{ji}(x_i)-H_{ji}(m_{ji})\right].
\]

For every integer population \(x\in S_j\cap\mathcal B_j\),

\[
\boxed{
|H_j(x)-[F_V(x)-F_V(m_j)]|
\le \eta/10.
}
\tag{13}
\]

This is a rational polynomial with computably bounded degree and coefficient bit lengths.

We also need a bound on its range.

For coordinates with large centers, the Bregman contribution on the box is \(O_\Theta(T)\)\. For small-center coordinates, the global bound \(h''\le3/2\) makes that contribution \(O_\Theta(Q^2)\)\.

The remaining first-order term is controlled by the normal cone at the constrained optimum. All active lower bounds are fixed cell thresholds. Their multipliers can be chosen with magnitude \(O_\Theta(L+1)\), because the affine constraint matrices are fixed and (5) bounds the gradient.

Consequently,

\[
0\le\Phi_V(x)-\Phi_V(a_j^*)
\le
O_\Theta\bigl((Q+T)^2+T(L+1)\bigr)
\]

throughout the retained feasible box.

Together with (3), (7) and (13), this supplies an explicitly computed integer \(M\) satisfying

\[
|H_j(x)|\le M,\qquad
M\le m_\Theta N^6.
\tag{14}
\]

### 4.4 Polynomial approximation to the exponential

Define

\[
P_j(x)=
\sum_{k=0}^{s_j}\frac{(-H_j(x))^k}{k!},
\]

where

\[
s_j=
\left\lceil100(M+\log_2\eta^{-1}+1)\right\rceil.
\]

Taylor's remainder bound, using \(|H_j|\le M\), gives

\[
\left|
P_j(x)-e^{-H_j(x)}
\right|
\le \eta e^{-M}/10
\]

after enlarging the harmless numerical constant if needed.

Combining this with (13) gives

\[
\boxed{
(1-\eta)\frac{W_V(x)}{W_V(m_j)}
\le P_j(x)\le
(1+\eta)\frac{W_V(x)}{W_V(m_j)}
}
\tag{15}
\]

for every retained integer population.

In particular, \(P_j(x)>0\) on its sampling support.

The degree satisfies the deliberately loose effective bound

\[
\boxed{\deg P_j=O_\Theta(N^9).}
\tag{16}
\]

Its rational coefficient bit lengths are polynomial in \(N\)\. Although expanding the polynomial may be expensive, there are at most \(\binom{\deg P_j+d}{d}\) monomials, which is polynomial in \(N\) because \(d\) is fixed.

## 5\. Exact polynomial-weight lattice counting

This is the computational step that replaces a weighted-normalization oracle.

For a rational polynomial \(P\) and a bounded fixed-dimensional rational lattice polytope \(\mathcal K\), define

\[
\mathsf M(\mathcal K,P)=
\sum_{z\in\mathcal K\cap\mathbb Z^k}P(z).
\]

There is a deterministic exact rational algorithm for this operation with bit complexity polynomial in the polytope's binary description, the polynomial's degree and its coefficient bit lengths, for fixed \(k\)\.

To see the construction, compute the short rational generating function

\[
G_{\mathcal K}(t)=
\sum_{z\in\mathcal K\cap\mathbb Z^k}t^z
\]

using fixed-dimensional Barvinok decomposition. This is the established polynomial-time lattice-point generating-function machinery. citeturn717156search0

For a monomial weight \(z^\alpha\), apply

\[
\prod_{i=1}^k
\left(t_i\frac{\partial}{\partial t_i}\right)^{\alpha_i}
\]

to the generating function. Linearity handles arbitrary rational polynomial weights.

Evaluate the resulting rational expression at \(t=(1,\ldots,1)\) through a finite Laurent-series calculation. Expansion order at most \(\deg P+k\) suffices. All poles cancel in the complete finite weighted sum.

Every operation is exact rational arithmetic, with polynomially bounded intermediate bit lengths in fixed dimension.

Thus

\[
\boxed{
\mathsf M(\mathcal K,P)
\text{ is computable in }
\operatorname{poly}_\Theta(N)\text{ bit operations}.
}
\tag{17}
\]

The same routine works after adding coordinate inequalities \(x_i\le h\), so it supplies every conditional cumulative weight needed for binary-search sampling.

## 6\. Combine the cells without computing gigantic factorial normalizers

It remains to place the different cells on a common scale.

For each nonempty cell, calculate \(F_V(m_j)\) to additive error at most \(\eta/100\)\.

This does not require forming \(m_j!\) when \(m_j\) is enormous. For small arguments, compute factorials exactly. For large arguments, use (2) with its explicit \(O(1/n)\) remainder and rational approximations to logarithms and \(\pi\)\.

All requested precision is polynomially bounded in \(N\)\.

Let \(j_0\) minimize these computed log-energies, with deterministic tie-breaking.

### 6.1 Discard negligible cells

Choose a computable threshold

\[
H_\Theta^{\mathrm{drop}}=h_\Theta(1+L)
\]

large enough to dominate the logarithm of the maximum number of populations and the bounded anchor-to-optimum energy gap.

If the computed difference

\[
F_V(m_j)-F_V(m_{j_0})
\]

exceeds this threshold, with appropriate precision slack, discard the cell.

The total true stationary mass of all discarded cells is at most \(\epsilon/100\) of the full mass. This follows from the bound

\[
Z_j\le |S_j|\exp\!\bigl(b_\Theta(1+L)+20d\bigr)W_V(m_j)
\]

and the fact that the full partition function is at least \(W_V(m_{j_0})\)\.

No discarded cell is conditioned on or sampled by rejection.

### 6.2 Compute the retained relative scales

For each retained cell, calculate a positive rational number \(r_j\) satisfying

\[
r_j=(1\pm\eta)\frac{W_V(m_j)}{W_V(m_{j_0})}.
\tag{18}
\]

The retained logarithmic ratios are only \(O_\Theta(L)\)\. Rational exponential approximation by range reduction and finite Taylor expansion therefore uses polynomially many bits.

Define the rational weights

\[
\widehat W_j(x)=r_jP_j(x),
\qquad x\in S_j\cap\mathcal B_j.
\]

By (15) and (18), these are uniformly within \(1\pm O(\eta)\) of the true weights divided by the common positive factor \(W_V(m_{j_0})\)\.

Their exact rational normalizers are

\[
\widehat Z_j=
r_j\,\mathsf M(S_j\cap\mathcal B_j,P_j).
\tag{19}
\]

No original factorial partition function is computed or assumed.

## 7\. The complete sampler

The following is the deterministic compiler's emitted per-invocation procedure. All tie-breaking, precision rules and iteration counts are fixed in its code.

1. Validate the binary input \(V,x_0,\epsilon\)\. For a singleton class, return \(x_0\) immediately.
2. Use the precompiled E0C coverability, bounded-coordinate and lattice tables to construct the exact disjoint cells (1). Test and omit empty cells using fixed-dimensional exact lattice counting.
3. For each nonempty cell, calculate the rational approximation to its continuous surrogate minimizer, choose a nearby feasible integer anchor \(m_j\), and construct its concentration box \(\mathcal B_j\)\.
4. Calculate anchor log-weights and discard cells certified to have negligible total mass.
5. For every retained cell, construct the rational polynomial \(P_j\), relative scale \(r_j\), and exact approximate normalizer \(\widehat Z_j\)\.
6. Choose a cell using its rational probability \(\widehat Z_j/\sum_k\widehat Z_k\)\.
7. Within the selected cell, recover each population coordinate by binary splitting. At each branch, use exact polynomial-weight moment sums with the accumulated coordinate constraints.
8. Return the resulting integer population vector in binary.

### Finite-bit randomness

Every branch probability is a rational number computed exactly.

Choose

\[
b=
\left\lceil
\log_2\frac{1000(J_\Theta+d(L+1)+1)}{\epsilon}
\right\rceil.
\]

For a rational branch probability \(p\), generate precisely \(b\) fair random bits and select the branch with probability

\[
2^{-b}\lfloor 2^bp\rfloor.
\]

The error at one decision is at most \(2^{-b}\)\.

There are at most

\[
O_\Theta(1+L)
\]

decisions: a fixed number for the cell and at most \(O(L)\) for each of the fixed \(d\) population coordinates.

Therefore total variation error from finite-bit random choices is below \(\epsilon/100\)\.

Every selected branch has positive approximate weight, and (15) guarantees that positive weight occurs only on valid retained class populations. **Every possible run outputs an element of \(\Gamma\)\.**

There is no rejection loop, conditional resampling, postselection, timeout or fallback.

## 8\. Complete total-variation estimate

Let \(\pi\) denote the target equilibrium distribution and \(\widehat\pi\) the rational distribution defined by (18)–(19), before finite-bit choice errors.

We have four explicitly controlled contributions.

| Error source | Certified upper bound |
|--------|--------|
| Removed cells | \(\epsilon/100\) |
| Removed tails inside retained cells | \(\epsilon/100\) |
| Polynomial and relative-scale approximation, after normalization | \(O(\eta)\), below \(\epsilon/50\) |
| Finite-bit branching | \(\epsilon/100\) |

Taking \(\eta=\epsilon/1000\), with the displayed conservative precision margins, gives

\[
\boxed{
\|\mathcal L(X_{\rm output})-\pi_{V,\Gamma}\|_{\rm TV}
<\epsilon.
}
\tag{20}
\]

This is a statement about the **unconditional entire output law**\. No probability of a successful preprocessing event is being conditioned upon.

### Rendered continuation (section 9 onward)

## 9. Bit-cost certificate

Let

$N=1+L+\epsilon^{-1}.$

The preceding construction provides the following effective size bounds, where the constants depend only on the compiled network.

| Object or operation | Bound |
| --- | --- |
| Class-location comparisons | $O_\Theta(\operatorname{poly}(L))$ |
| Number of disjoint cells | $J_\Theta$, fixed |
| Continuous minimizer computation | $\operatorname{poly}_\Theta(L)$ bits |
| Nearby integer anchor search | Fixed number of $O(L)$-bit checks |
| Concentration threshold $T$ | $O_\Theta(N)$ |
| Small-coordinate threshold $Q$ | $O_\Theta(N^3)$ |
| Log-energy range bound $M$ | $O_\Theta(N^6)$ |
| Degree of rational weight polynomial | $O_\Theta(N^9)$ |
| Total coefficient encoding length | $N^{O_\Theta(d)}$ |
| Exact weighted-moment computation | $N^{O_\Theta(1)}$ bit operations |
| Number of moment queries | $O_\Theta(L)$ |
| Random bits | $O_\Theta(L^2)$ |
| Output length | $O_\Theta(L)$ bits |

The exact logarithms used in the mathematical analysis are not invoked as oracles. Rational logarithms use range reduction and the convergent series

$\log u=2\sum_{k=0}^{s}
\frac{z^{2k+1}}{2k+1}+\mathcal R_s,
\qquad z=\frac{u-1}{u+1},$

with $|z|\le1/3$ after range reduction. The remainder is geometrically bounded. The fixed $\log(2\pi)$ constant can likewise be computed through certified rational arctangent and logarithm series.

The algebraic decomposition, interpolation, polynomial expansion, rational generating-function arithmetic and truncated probability choices all have predetermined finite stopping bounds.

### Computing $C_\Theta$ and $p_\Theta$

The compiler fixes concrete implementations of the rational convex cutting-plane algorithm and the fixed-dimensional Barvinok weighted-moment algorithm.

Let $q_\Theta$ be a computable integer exponent dominating their certified polynomial bit bounds on the fixed collection of dimensions and constraint matrices generated from $\Theta$.

One deliberately excessive choice is

$\boxed{
p_\Theta=1000(d+1)(q_\Theta+1).
}
\tag{21}$

Polynomial propagation of the bounds above gives a computable positive integer $C_\Theta$ that dominates every coefficient in those bounds, the number and size of all compiled tables, and the input-validation and output costs.

Enlarge it to at least $1$.

Then on every execution

$\boxed{
\operatorname{BITWORK},
\operatorname{RANDOMBITS},
\operatorname{MEMORY}
\le C_\Theta(1+L+\epsilon^{-1})^{p_\Theta}.
}
\tag{22}$

These are bit-operation, rather than unit-cost exact-real or unbounded-word, estimates.

### Compiler cost

The fixed-network compilation itself runs the accepted E0C terminating constructions, computes the lattice templates and Graver-proximity constants, constructs the fixed geometric and analytic bounds, and emits the sampler and its complexity certificate.

Its finite bit cost includes all Gröbner, Hilbert-basis, lattice-normal-form, backward-coverability and finite-control calculations.

For a fully effective, though potentially extremely large, worst-case bound in network encoding length $B$, one may define

$\mathfrak B(B)=
\max_{\substack{\Theta\text{ valid}\\|\Theta|\le B}}
\operatorname{BITWORK}(\operatorname{Compile}(\Theta)).$

This is a computable integer-valued function: enumerate the finitely many binary presentations of length at most $B$, verify the rational input conditions exactly, execute the proved-terminating compiler on each valid presentation, and take the maximum observed cost.

Thus compiler work and the stored fixed-network tables are explicitly paid. Neither is an uncharged advice oracle.

## 10. Conclusion

The proposed construction establishes the positive binary-size sampling endpoint, using the accepted E0C class geometry and fixed-dimensional rational generating-function machinery.

For every fixed valid $\Theta$, it specifies a terminating deterministic compiler producing a randomized sampler and computable $C_\Theta,p_\Theta$ such that

$\boxed{
X\in\Gamma\ \text{on every run},\qquad
\|\mathcal L(X)-\pi_{V,\Gamma}\|_{\rm TV}<\epsilon,
}$

with the requested every-run polynomial bound (22).

The essential distinction from E0C is that the sampler never pays for the number of populations along a physical mixing trajectory. Instead, it uses the accepted exact class locator, concentrates the factorial weights in polynomially describable regions, approximates those weights by rational polynomials, and performs exact polynomial-weight lattice summation in fixed dimension.

The genuinely additional argument is the combination of the constant-error smooth factorial surrogate, proximity localization, bounded-degree rational weight approximation and exact moment-based inverse sampling. No polynomial-in-$\log V$ mixing theorem is needed.

This is a new proof construction presented here, rather than an independently published or externally verified theorem. Its central interfaces have been made explicit, particularly the exact disjoint-cell derivation from E0C and the uniform log-weight range bound needed for polynomial approximation; those are the points on which formal independent verification should concentrate.

