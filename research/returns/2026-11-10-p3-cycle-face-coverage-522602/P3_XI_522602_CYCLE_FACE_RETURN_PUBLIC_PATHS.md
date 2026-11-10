# P3 Xi completed return — robust realization continuation

Source: https://chatgpt.com/c/6af1fcc7-7bcc-83ec-bc2e-2e1c39dd3ddb; response 5226027d-ad79-4878-9b91-9c22b401ae3c; user turn 7d6d0f76-20cb-4c11-84dd-42ba534beb88.
Exact question: work/astra-renewed-pro-programmes-20261103/P3_FULL_ROBUST_KINETICS_AFTER_AF33EF_XI_20261110.txt; source SHA256 64f8b623d2773e7895b62f55cf9d93228a45e0f9a0ae4cc1c5a74cf2c188e668; posted text SHA256 a17231153d360cf472048b385e7f723b0b0415d31b0a9e38adb33f249caf99c1. Model at generation GPT-6 Standard Extra High. No ZIP identified.

## Available visible activity

Worked for 24m 35s. Analyzed recurrence and addressed boundary difficulties.

ChatGPT said: I’ll test two approaches in parallel: a perturbation bound based on local stationary flux, and a boundary-adapted drift construction based on the reaction graph. The key distinction is whether a small coefficient error can accumulate over arbitrarily many fast firings, or whether the factorial tail of the target law prevents that accumulation from destabilizing the process.

Developed robust supersolutions and tested certificate strategies. Developed robust stabilization criteria with Poisson correctors and catalytic funnels. Searched the web.

ChatGPT said: The cycle-level calculation gives a strict extension of the earlier pure-source theorem. A pure-source drain need only be maximal within a selected directed cycle, not within its entire linkage class. I’m also checking how far this can be weakened when conservation laws prevent some species from becoming large independently.

Developed generalized cycle, stability, and drift criteria. Developed a drift theorem.

ChatGPT said: The face-cover argument now closes the full stochastic resource contract for a new class of mixed-reactant networks, including an infinite rank-two communicating class with a non-factorizing conditional-Poisson target. I’m separating that completed positive result from the remaining all-network issue: some graphs force every immediate move at a boundary state to increase population, so any universal proof must control multi-step excursions rather than rely on one-step radial drift.

Developed a drift criterion. Finalizing the theorem.

## Complete native response

## P3 continuation — a new higher-rank robust realization theorem

**Universal status: still open.** The unrestricted problem has not been resolved, but the previous pure-source theorem can be strengthened substantially.

The new construction allows population-decreasing reactions with mixed-species reactants, provided those reactions collectively control every possible unbounded direction of the stoichiometric system.

It also replaces maximum molecularity across an entire linkage class with maximum molecularity inside a selected directed cycle.

### 1\. Cycle-face coverage theorem

Let

\[
S_R=\operatorname{span}_{\mathbb R}\{z_r-y_r:r\in R\},
\]

and define the normalized nonnegative recession cone

\[
\mathcal K_R=
\left\{v\in S_R\cap\mathbb R_{\ge0}^d:
\sum_i v_i=1\right\}.
\]

This cone captures possible directions in which population can become arbitrarily large while remaining in an affine stoichiometric class.

For each directed cycle \(C\) in the original finite complex graph, put

\[
d_C=\max_{y\in C}|y|_1.
\]

Call a reaction \(y\to z\) on \(C\) a *maximal drain* when

\[
|y|_1=d_C,\qquad |z|_1<d_C.
\]

Its source may contain several species.

**Cycle-face coverage condition.** For every extreme ray \(v\) of the cone \(S_R\cap\mathbb R_{\ge0}^d\), there exists a directed cycle \(C_v\) with a maximal drain \(y_v\to z_v\) such that

\[
\boxed{
\operatorname{supp}(y_v)
\subseteq\operatorname{supp}(v).
}
\tag{1}
\]

Equivalently, every possible unbounded stoichiometric direction enables at least one selected maximal drain when its positive coordinates become sufficiently large.

**Theorem.** Every fixed finite weakly reversible network satisfying (1) admits the complete graph-preserving robust conditional-Poisson kinetic compiler, for every binary initial population, positive rational activity vector and rational accuracy input.

The conclusion includes exact nominal stationarity, independent-coefficient-error nonexplosion and recurrence, unique perturbed stationarity, both whole-law TV bounds, both absolute first-moment bounds, polynomial complete-binary compiler cost and polynomial numerical reaction-firing cost.

If \(\mathcal K_R\) is empty, every affine nonnegative stoichiometric fibre is bounded. The accepted finite-class compiler covers that case.

#### Construction

Retain the accepted nominal catalytic baseline with degree \(K_0\)\.

Choose one cycle and maximal drain witnessing (1) for each extreme ray. There are finitely many because \(R\) is fixed.

Set

\[
D=\max_r|y_r|_1,
\qquad H\ge K_0+D+3.
\]

For each selected cycle \(C\), add its complete translated circulation using every catalyst

\[
\boxed{
w\in\mathbb N^d,\qquad |w|_1\le H-d_C.
}
\tag{2}
\]

Assign coefficients proportional to

\[
\frac{1}{w!\lambda^{y_r}},
\]

with a common positive rational scale \(c\) having polynomially bounded inverse in

\[
V_\lambda=1+\sum_i(\lambda_i+\lambda_i^{-1}).
\]

Superimpose these circulations on the nominal baseline. Combine overlapping contributions into their labelled channels.

Each translated directed cycle has constant nominal product-Poisson flow. Consequently the augmentation preserves exact nominal complex balance.

Every added transition uses an original reaction vector and requires at least the original reactant. The \(w=0\) baseline remains present. Thus the entire directed population-transition graph is exactly unchanged.

All coefficients can be made at most one, with inverse bounded by \(C_RV_\lambda^{p_R}\)\.

### 2\. The central drift calculation

Let \(N=|x|_1\)\. For a selected maximal drain \(y\to z\) on cycle \(C\), put \(d_C=|y|_1\)\.

Summing its catalytic intensities gives

\[
q_C^-(x)=
c\lambda^{-y}(x)_{\underline y}
F_{H-d_C}(N-d_C),
\]

when enabled, where

\[
F_k(n)=\sum_{j=0}^k\binom nj.
\]

Because all degrees are fixed, its leading homogeneous term at \(x=Nu\), \(\sum_i u_i=1\), is

\[
\frac{c\lambda^{-y}}{(H-d_C)!}
N^H u^y.
\]

The lower-degree error is bounded by

\[
C_RV_\lambda^{p_R}(1+N)^{H-1}.
\]

Now consider any reaction that **increases** total population within the same selected cycle. Its product has molecularity at most \(d_C\), so its source has molecularity at most \(d_C-1\)\. After catalysis its reactant degree is at most \(H-1\)\.

The original baseline's population-increasing intensities likewise have degree at most \(D+K_0\), strictly below \(H\)\.

Define

\[
P(u)=\sum_{\text{selected drains }j}
(|y_j|_1-|z_j|_1)u^{y_j}.
\]

Condition (1) implies

\[
\boxed{
\min_{u\in\mathcal K_R}P(u)=\rho_R>0.
}
\tag{3}
\]

Indeed, \(\mathcal K_R\) is the convex hull of finitely many normalized extreme rays. Every \(u\) assigns positive convex weight to at least one ray witnessing a drain whose reactant support lies inside that ray. The corresponding monomial is strictly positive. Compactness supplies a uniform margin.

Because the extreme rays are rational and fixed, a positive rational lower bound for \(\rho_R\) is computable during fixed-\(R\) preprocessing.

Every actual population \(x\in\Gamma_R(x_0)\) satisfies

\[
x-x_0\in S_R.
\]

Therefore, when \(N\) is sufficiently large relative to \(1+|x_0|_1\), the normalized vector \(x/N\) lies close to \(\mathcal K_R\)\. A computable rational polyhedral error bound makes this quantitative\:

\[
N\ge C_R(1+|x_0|_1)
\quad\Longrightarrow\quad
P(x/N)\ge\rho_R/2.
\]

Combining the selected negative leading terms with every possible positive lower-degree contribution gives, uniformly for independent relative errors \(\delta\le1/4\),

\[
\boxed{
\widetilde LN(x)
\le
-c_RV_\lambda^{-a_R}N^H+
C_RV_\lambda^{b_R}(1+N)^{H-1}
}
\tag{4}
\]

outside a radius proportional to \(1+|x_0|_1\)\.

Hence, for a computable fixed exponent \(p_R\),

\[
\boxed{
\widetilde LN(x)\le
-c_R'V_\lambda^{-p_R}N^H
\quad\text{whenever}\quad
N\ge C_R'(1+|x_0|_1)V_\lambda^{p_R}.
}
\tag{5}
\]

This is a robust, uniform, one-step population drift. It does not assume that the perturbed rates preserve complex balance.

### 3\. Completion of the stochastic resource contract

For every fixed integer \(s\ge1\), apply the generator to

\[
H_s(x)=(1+|x|_1)^s.
\]

A population-decreasing reaction changes \(H_s\) by a negative quantity of order \(N^{s-1}\); an increasing reaction contributes a positive quantity of the same order. Zero-population-change channels contribute zero drift but remain included in firing costs.

The degree separation in (4) therefore yields

\[
\boxed{
\widetilde LH_s(x)
\le A_{R,s}(V_\lambda,|x_0|_1)
-b_{R,s}(V_\lambda)H_s(x),
}
\tag{6}
\]

where \(A_{R,s}\) and \(b_{R,s}^{-1}\) have computable fixed-polynomial bounds in \(W\)\.

These bounds establish nonexplosion and positive recurrence on every nonsingleton actual class. Since all original enabled transitions remain present with positive rates, the perturbed chain is irreducible and has a unique stationary law.

They also give, for each fixed \(s\),

\[
\sup_{t\ge0}
\mathbb E_{x_0}^{\tilde\kappa}(1+|X_t|_1)^s
\le C_{R,s}W^{p_{R,s}},
\]

and

\[
\mathbb E_{\mu_{\tilde\kappa}}(1+|X|_1)^s
\le C_{R,s}W^{p_{R,s}}.
\]

The complete augmented reactant degree is at most \(H\), so sufficiently high fixed moments pay the intensity of every labelled reaction channel.

Finally, the accepted robustness-transfer theorem converts these estimates and the retained nominal Poincaré gap into all four \(\epsilon\)\-accuracy conditions with

\[
T,\quad \delta^{-1},\quad
\max_{r,w}\kappa_{r,w}^{-1},\quad
\mathbb E[\text{actual firings up to }T]
\le C_RW^{p_R'}.
\]

The finite catalyst lists, rational rates and quantitative Foster majorants use only fixed-degree rational arithmetic. Complete-binary work, memory and output are bounded by \(C_R(1+L)^{p_R'}\)\.

Thus the cycle-face condition is a complete, effectively checkable **structural sufficient condition for the original full compiler**\.

### 4\. A coupled rank-two example with no pure-source drains

Consider three species \(A,B,C\), with the original network

\[
\boxed{
A+C\rightleftarrows2A+2C,
\qquad
B+C\rightleftarrows2B+2C,
\qquad
A+C\rightleftarrows B+C.
}
\tag{7}
\]

This is one weakly reversible linkage class. Its stoichiometric subspace has dimension two\:

\[
S_R=\operatorname{span}\{(1,0,1),(0,1,1)\}.
\]

It has no zero complex, no immigration–degradation backbone, and **no reaction with a pure-species reactant**\.

The nonnegative recession directions have the form

\[
v=(a,b,a+b),\qquad a,b\ge0,
\]

so their extreme rays are

\[
v_A=(1,0,1),\qquad v_B=(0,1,1).
\]

Select the reversible cycles

\[
A+C\rightleftarrows2A+2C
\]

and

\[
B+C\rightleftarrows2B+2C.
\]

Their maximal drains are

\[
2A+2C\longrightarrow A+C,
\]

and

\[
2B+2C\longrightarrow B+C.
\]

The first reactant is supported on \(\{A,C\}\), matching \(v_A\); the second is supported on \(\{B,C\}\), matching \(v_B\)\.

Thus the cycle-face coverage condition holds.

For example, starting from \(x_0=(1,1,2)\), the actual communicating class is

\[
\Gamma=
\{(a,b,a+b):a,b\in\mathbb N,\ a+b\ge1\}.
\]

Its required target is the genuinely coupled conditional-Poisson law

\[
\pi_\lambda(a,b,a+b)
=
\frac1{Z_\Gamma}
\frac{
\lambda_A^a\lambda_B^b\lambda_C^{a+b}
}{
a!\,b!\,(a+b)!
}.
\]

The class is infinite, its two variable coordinates are not independent under this law, and its transitions couple the three populations.

Nevertheless, the new theorem constructs a **fixed finite catalytic realization** that is exactly stationary at this law and meets the entire independent-perturbation, recurrence, absolute-moment, mixing-time and firing-resource contract.

This example is outside the earlier pure-source maximum-drain theorem. The strengthening to mixed-reactant drains is therefore substantive rather than just a different proof of an already completed case.

### 5\. Every weakly reversible network has a bounded-length inward word outside its initial-population scale

The accepted marked-pair geometry yields another quantitative statement that applies **without** the cycle-face condition.

Fix an arbitrary weakly reversible \(R\), initial population \(x_0\), and actual class \(\Gamma=\Gamma_R(x_0)\)\.

Define

\[
\Phi_{x_0}(x)=\|x-x_0\|_2^2.
\]

**Lemma — universal bounded-word contraction.** There are computable constants \(L_R,E_R,B_R\), depending only on \(R\), such that whenever

\[
|x|_1\ge 2|x_0|_1+B_R,
\qquad x\in\Gamma,
\]

there exists an enabled original directed reaction word of length at most \(L_R\),

\[
x=x^{(0)}\to x^{(1)}\to\cdots\to x^{(m)}=x',
\]

with

\[
\boxed{
\Phi_{x_0}(x')-\Phi_{x_0}(x)
\le-\frac{|x|_1}{2d}
}
\tag{8}
\]

and

\[
\boxed{
\max_{0\le j\le m}
\|x^{(j)}-x\|_1\le E_R.
}
\tag{9}
\]

#### Proof

Put \(v=x-x_0\), and let \(M=\|v\|_\infty\)\.

The accepted marked balancing table supplies a bounded vector \(g\), sign-conformal to \(v\), with a nonzero component in a largest-difference coordinate. It also supplies a fixed original reaction word implementing

\[
x\longrightarrow x-g.
\]

Because \(g\) is sign-conformal,

\[
v\cdot g\ge M.
\]

The marked table has a fixed bound \(\|g\|_2^2\le H_R\)\. Therefore

\[
\begin{aligned}
\Phi_{x_0}(x-g)-\Phi_{x_0}(x)
&=-2v\cdot g+\|g\|_2^2\\
&\le-2M+H_R.
\end{aligned}
\]

For sufficiently large \(M\), this is at most \(-M\)\.

Moreover,

\[
M\ge\frac{|x|_1-|x_0|_1}{d}.
\]

Increasing the fixed threshold \(B_R\) proves (8).

The original word is obtained by translating one of finitely many precompiled reaction words. Its length and intermediate coordinate excursions are bounded independently of \(x,x_0,\lambda,\epsilon\), proving (9).

#### Exact stochastic limitation

For any fixed allowed positive-rate catalytic design with maximum reactant degree \(D_R\) and smallest nominal coefficient \(\kappa_{\min}\), the probability of executing this particular original word during the next \(m\) firings, under independent relative errors at most \(1/2\), is bounded below by

\[
\boxed{
\left[
\frac{\kappa_{\min}}
{4Q_R(1+|x|_1+E_R)^{D_R}}
\right]^{L_R}.
}
\tag{10}
\]

Thus every state sufficiently far from its initial anchor has an **inward original reaction route of uniformly bounded length**, with a reciprocal-polynomial success probability at each attempt.

The critical distinction is that failed attempts do not restart at the same population. They can change both the large and small coordinates and thereby change which word is appropriate.

Consequently, (8)–(10) do not yet give a negative expected drift over a stopping time. In particular, an inward path of bounded length is not equivalent to a uniformly effective inward stochastic policy.

This identifies a concrete all-network resource interface: the combinatorial availability and polynomial probability of an inward word are established; controlling the actual dynamics between successive attempts is not.

### 6\. A finite exact test for the new sufficient condition

The cycle-face coverage condition does not require searching over unbounded populations.

A deterministic fixed-\(R\) precompiler can\:

1. Enumerate the finite directed simple cycles of the original complex graph and identify their maximal-molecularity decreasing edges.
2. Calculate a rational basis for \(S_R\) and enumerate the rational extreme rays of \(S_R\cap\mathbb R_{\ge0}^d\)\.
3. For each extreme ray, find a maximal drain whose reactant support is contained in that ray's support.
4. If all rays are covered, construct the finite catalytic menu and its rational coefficient and drift bounds. Otherwise, report that this particular sufficient condition does not apply.

There is no variable-input population enumeration in this operation.

For completeness, the rate formula can be written explicitly. Let \(a_r\) be the accepted positive integer circulation and \(C_j\) the selected directed cycles. Define

\[
\boxed{
\kappa_{r,w}
=
\frac{c}{w!\lambda^{y_r}}
\left[
a_r\mathbf1_{\{|w|_1\le K_0\}}
+
\sum_{j:r\in C_j}
\mathbf1_{\{|w|_1\le H-d_{C_j}\}}
\right],
}
\tag{11}
\]

outputting exactly the channels whose bracket is positive.

Choose

\[
c=\frac{1}{4A_R(1+V_\lambda)^D},
\]

where \(A_R\) is a fixed integer larger than the sum of all circulation multiplicities appearing in (11).

Then every nominal channel coefficient is at most one, and

\[
\max_{r,w}\kappa_{r,w}^{-1}
\le C_R(1+V_\lambda)^{2D}.
\]

The constants in the drift certificate can be made equally explicit. If \(v^{(1)},\ldots,v^{(M)}\) are the normalized rational extreme rays, and the chosen drain for ray \(j\) has source \(y_j\) and product \(z_j\), a valid positive lower bound for (3) is

\[
\boxed{
\rho_R\ge
\min_{1\le j\le M}
\left[
(|y_j|_1-|z_j|_1)
M^{-|y_j|_1}(v^{(j)})^{y_j}
\right].
}
\tag{12}
\]

This is an ordinary positive rational fixed-\(R\) constant. Rational polyhedral error bounds and the finite polynomial expansions of the mass-action intensities then yield explicit computable constants for (5)–(6).

For the example in Section 4, the exact leading drain polynomial is

\[
P(u)=2u_C^2(u_A^2+u_B^2).
\]

On its normalized recession cone, \(u_C=1/2\) and \(u_A+u_B=1/2\), so

\[
\boxed{\min_{\mathcal K_R}P=\frac1{16}.}
\]

Thus even the key strict inward-drift margin is explicit.

### 7\. Why the theorem cannot simply be declared universal

Consider again the accepted trapping network

\[
\varnothing\rightleftarrows A+B,
\qquad B\rightleftarrows2B.
\]

For every population \((n,0)\), the only enabled population-changing original reaction is

\[
\varnothing\longrightarrow A+B.
\]

Every permitted catalytic copy enabled there has the same positive population change.

Therefore, for **any allowed finite catalytic design and any positive coefficient choices**,

\[
\boxed{
\widetilde L h(|x|_1)(n,0)>0
}
\]

for every strictly increasing function \(h\) of total population.

These states occur at arbitrarily large populations in an infinite communicating class.

Hence no universal theorem asserting an eventually negative one-step drift of an increasing radial population function can hold for all weakly reversible networks, regardless of catalyst choices.

This is not an obstruction to robust realization: the same network has the previously accepted complete positive compiler. Its stability arises through nonradial or multi-step effects.

The new bounded-word lemma establishes that an inward route always exists outside a scale determined by \(x_0\)\. What is missing is a way to ensure that competing reaction firings do not overwhelm the inward effect, uniformly under independent coefficient errors.

For perspective, recent stochastic-reaction-network research continues to distinguish bulk stabilization from boundary control; the broader arbitrary-dimensional weak-reversibility recurrence question is still described as open. citeturn579804search0turn579804academia33

## Research status after this continuation

| Result family | Scope | Status |
|--------|--------|--------|
| Complete robust compiler for finite classes | All weakly reversible \(R\) | Previously completed |
| Complete robust compiler for rank-one systems | All eligible classes | Previously completed |
| Complete robust compiler for the trapping network | Its actual classes, all activities | Previously completed |
| Complete robust compiler with original immigration–degradation backbone | Interacting higher-rank systems | Previously completed |
| Pure-source maximal-drain compiler | Earlier structural class | Previously completed |
| **Mixed-reactant cycle-face coverage compiler** | Higher-rank infinite classes satisfying (1) | **New complete positive theorem** |
| Explicit three-species, single-linkage conditional-Poisson example | Rank two, no pure-source drains | **New complete positive example** |
| Fixed-\(R\) finite recognition and construction for cycle-face coverage | Every given reaction structure | **New effective sufficient-condition test** |
| Quantitative bounded-length inward original word | All weakly reversible \(R\) | **New quantitative consequence of accepted geometry** |
| Robust control of stochastic failures around inward words | Arbitrary interacting boundary regimes | Open |
| Universal full robust kinetic compiler | Every weakly reversible \(R\) | **Open** |

The principal mathematical advance is that **pure-species decreasing reactions are not necessary for a complete robust compiler**\. A finite set of mixed-reactant decreasing cycles suffices whenever their supports cover the extreme unbounded directions of the stoichiometric cone.

The remaining universal problem is more sharply localized: it concerns boundary directions in which every immediately enabled original reaction fails to provide inward population drift, but short sequences of permitted reactions can still produce inward motion.

A full solution must control those sequences and their competing firings with a uniform polynomial-resource certificate—or establish an obstruction applying to every permitted catalytic design. Neither endpoint follows from the present results.
