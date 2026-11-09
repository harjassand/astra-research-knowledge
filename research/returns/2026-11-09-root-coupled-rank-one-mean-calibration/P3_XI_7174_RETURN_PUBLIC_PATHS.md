# Completed Xi return — 71748613-c569-4b02-b9d3-c624fc81e50c

Source: https://chatgpt.com/c/6af11227-f57c-83ec-80e4-caf25a4bae01
Model: GPT-6 standard, Extra High. Exact prompt reference: P3_RANK_ONE_EXACT_SUPPLIED_PROOF_BODY.txt.

No producer ZIP visible.

## Visible activity

Developed research strategy and bounded geometric dual parameters

Developed and strengthened a hierarchical optimization proof with local witnesses

Assessed structural guarantees, counterexamples, and geometric height bounds

Refined geometric convexity arguments and inverse calibration bounds

Assessed local geometry

Assessed geometric bounds

Generalized multipartite fibers and assessed geometric and algorithmic bounds

Searched 29 websites

The accepted backward-coverability machinery yields another rank-independent fact: every active reaction can be enabled within a network-dependent bounded number of steps from any state of the same class. Combined with factorial weight ratios, this gives an explicit lower bound on covariance eigenvalues whenever the log-activities are bounded. It strengthens the inverse optimizer, but does not yet bound how far the required activities may lie.

Extended multipartite networks

## Complete response

## New result: the parameter-selection problem reduces to an inverse-height bound

The accepted constructions already give polynomial-bit forward evaluation and moment evaluation at any specified positive rational activity vector. A new reduction removes a second apparent obstacle: **once a polynomial bound on the magnitude of the required log-activities is available, an efficient global selector can be constructed without an interior-margin or covariance lower-bound promise.**

Let

\[
A(\theta)=\log\sum_{x\in\Gamma}\frac{e^{\theta\cdot x}}{x!},
\qquad
F_m(\theta)=A(\theta)-m\cdot\theta.
\]

Then

\[
\nabla F_m(\theta)=\mathbb E_\theta[X]-m,
\quad
\nabla^2F_m(\theta)=\operatorname{Cov}_\theta(X)\succeq0.
\]

### Conditional-radius theorem

Suppose a rational radius \(B\ge1\) is supplied and there exists some real \(\theta^*\) satisfying

\[
\|\theta^*\|_2\le B,
\qquad
\|\nabla F_m(\theta^*)\|_2\le\frac{\epsilon}{32}.
\tag{1}
\]

Then a deterministic algorithm can calculate ordinary positive rational activities \(\lambda_i\) satisfying

\[
\|\mathbb E_{\pi_\lambda}[X]-m\|_\infty\le\epsilon
\]

using

\[
\operatorname{poly}_R(L+B)
\]

bit operations and memory, including conversion from log-activities to rational activities.

Here \(B\) enters as a **numerical bound on log-activity magnitude**\. Thus, if \(B\) is polynomial in \(L\), the complete requested polynomial-bit contract follows.

### Proof: regularized convex inversion

Define

\[
G_\tau(\theta)=F_m(\theta)+\frac{\tau}{2}\|\theta\|_2^2,
\qquad
\tau=\frac{\epsilon}{32B}.
\]

This function is strongly convex and has a unique minimizer \(\theta_\tau\)\.

Convex-gradient monotonicity, compared with \(\theta^*\), gives

\[
\tau\bigl(\|\theta_\tau\|^2-
\theta_\tau\cdot\theta^*\bigr)
\le
\|\nabla F_m(\theta^*)\|\,
\|\theta_\tau-\theta^*\|.
\]

Writing \(r=\|\theta_\tau\|\), condition (1) yields

\[
r(r-B)\le B(r+B).
\]

Therefore

\[
\boxed{\|\theta_\tau\|\le(1+\sqrt2)B<3B.}
\tag{2}
\]

At the regularized optimum,

\[
\nabla F_m(\theta_\tau)=-\tau\theta_\tau.
\]

Consequently,

\[
\boxed{
\|\nabla F_m(\theta_\tau)\|_\infty
<3\epsilon/32.
}
\tag{3}
\]

This works equally well for boundary targets. No covariance eigenvalue lower bound was used.

### Effective finite-bit optimization

Optimize \(G_\tau\) over the box \([-4B,4B]^d\)\. The minimizer lies strictly inside this box by (2).

The Poisson-anchor argument from the accepted DDB1 construction provides an explicit bound

\[
\|\nabla^2F_m(\theta)\|_{\rm op}\le H
\]

throughout the box, where

\[
\log_2(H+1)=\operatorname{poly}_R(L+B).
\]

The accepted moment and log-partition evaluators can be called with rational approximations to \(e^\theta\)\. On this bounded box, certified exponential evaluation, rational rounding and Poisson moment bounds ensure that each value and gradient query costs \(\operatorname{poly}_R(L+B+\log(1/\delta))\) bits for requested error \(\delta\)\.

Standard rational convex cutting planes can therefore find a rational \(\widehat\theta\) with

\[
G_\tau(\widehat\theta)-G_\tau(\theta_\tau)
\le
\frac{\tau\epsilon^2}{10^5(H+1)^2}
\]

in polynomial bit time.

Strong convexity then implies that \(\widehat\theta\) is close enough to \(\theta_\tau\) for

\[
\|\nabla F_m(\widehat\theta)\|_\infty<\epsilon/4.
\]

Finally, approximate each \(e^{\widehat\theta_i}\) by a positive rational with relative error small enough that the Hessian bound controls the change in mean by less than \(\epsilon/4\)\.

Every returned numerator and denominator has \(O(\operatorname{poly}_R(L+B))\) bits. Thus the output is an ordinary rational vector, not a symbolic representation of logarithms.

### Consequence

The previous status had two separate unresolved requirements: bounding inverse activities and efficiently selecting them. This argument eliminates the independent selection requirement.

**It is sufficient to prove a polynomial-in-\(L\) bound on the log-activity radius of an approximate inverse.** Once such a bound is explicit and computable, convex optimization and DDB1 complete the remaining algorithm.

This is a genuine reduction, not a full resolution: the required radius bound is not yet proved for arbitrary coupled structures of rank at least two.

## New higher-rank positive theorem: a genuinely coupled reaction family

The rank-one restriction can be exceeded without assuming independence. In particular, the full calibration contract holds for the following family, of arbitrarily high stoichiometric rank.

Consider species \(A,B_1,\ldots,B_k\), with \(k\ge2\), and reactions

\[
0\ \rightleftarrows\ A+B_i,
\qquad i=1,\ldots,k.
\tag{4}
\]

All reactions share species \(A\)\. Their stoichiometric rank is \(k\), and the equilibrium law does not factor into independent one-species distributions.

### Theorem

For every fixed \(k\), the reaction structure (4) has a deterministic compiler satisfying the full requested polynomial-binary calibration guarantee for every feasible binary \(x_0,m,\epsilon\)\.

This includes arbitrarily large conserved populations, zero target components and infinite classes.

### Exact class and partition reduction

Write a population as \((a,b_1,\ldots,b_k)\)\. The invariant is

\[
a-\sum_{i=1}^k b_i=h,
\qquad
h=a_0-\sum_i b_{0i}.
\]

The actual class is exactly

\[
\boxed{
\Gamma_h=
\{(a,b)\in\mathbb Z_{\ge0}^{k+1}:
a-\sum_i b_i=h\}.
}
\tag{5}
\]

For \(h\ge0\), repeated deaths reach \((h,0,\ldots,0)\), and births reconstruct any other fibre population. For \(h<0\), deaths reach \(a=0\), after which a birth followed by a death exchanges one unit between any two \(B\)\-species. This connects every boundary composition before births reconstruct the target. Thus (5) is an exact actual-class statement.

Set

\[
S=\sum_i\lambda_{B_i},\quad
q=\lambda_A S,\quad
p_i=\lambda_{B_i}/S.
\]

Summing the multinomial factorial weights gives

\[
Z_{\Gamma_h}(\lambda)
=
S^{-h}
\sum_{n\ge\max(0,h)}
\frac{q^n}{n!(n-h)!}.
\tag{6}
\]

Consequently, with \(N=X_A\),

\[
\Pr_q(N=n)=
\frac{q^n/[n!(n-h)!]}
{\displaystyle\sum_{\ell\ge\max(0,h)}
q^\ell/[\ell!(\ell-h)!]},
\tag{7}
\]

and, conditionally on \(N=n\),

\[
(X_{B_1},\ldots,X_{B_k})
\sim\operatorname{Multinomial}(n-h;p_1,\ldots,p_k).
\tag{8}
\]

Thus

\[
\mathbb E[X_A]=f_h(q),\qquad
\mathbb E[X_{B_i}]=p_i(f_h(q)-h).
\tag{9}
\]

This is a coupled rank-\(k\) family whose entire inverse mean problem reduces to one scalar activity and explicit rational proportions.

### Polynomial-height calibration

Let the feasible target be

\[
m=(\alpha,\beta_1,\ldots,\beta_k),
\qquad
\alpha-\sum_i\beta_i=h.
\]

Set \(M=\sum_i\beta_i\) and choose

\[
\zeta=\frac{\epsilon}{64k},
\qquad
p_i=\frac{\beta_i+\zeta}{M+k\zeta}.
\]

Every \(p_i\) is strictly positive, rational and has \(O_k(L)\) binary digits. Moreover,

\[
|Mp_i-\beta_i|\le k\zeta\le\epsilon/64.
\tag{10}
\]

For the scalar parameter \(q\), the consecutive-weight ratio in (7) is

\[
\frac{w_q(n+1)}{w_q(n)}
=\frac{q}{(n+1)(n+1-h)}.
\]

Let \(n_{\min}=\max(0,h)\), and set

\[
q_{\rm lo}=\frac{\epsilon}{1024(k+1)},
\]

\[
N_1=\lceil\alpha\rceil+3,\qquad
q_{\rm hi}=4(N_1+|h|+1)^2.
\]

For the lower bracket, every successive weight ratio is at most \(q_{\rm lo}\), giving

\[
n_{\min}\le f_h(q_{\rm lo})
\le n_{\min}+\frac{q_{\rm lo}}{(1-q_{\rm lo})^2}.
\]

For the upper bracket, the ratios below \(N_1\) are at least \(4\)\. Therefore

\[
f_h(q_{\rm hi})
\ge N_1-\sum_{j\ge1}j4^{-j}
=N_1-\frac49>\alpha.
\]

The interval endpoints have \(O_k(L)\) ordinary binary digits.

The function \(f_h\) is strictly increasing\:

\[
f_h'(q)=\frac{\operatorname{Var}_q(N)}q>0.
\]

The accepted DDB1 moment evaluator computes \(f_h(q)\) to additive precision \(\delta\) in polynomial complete-binary cost, using activities

\[
\lambda_A=1,\qquad \lambda_{B_i}=qp_i.
\]

A Poisson-anchor second-moment bound supplies a uniform Lipschitz constant on the rational bracket whose logarithm has \(O_k(L)\) bits. Consequently, certified rational bisection requires only \(O_k(L)\) steps to find \(q\) satisfying

\[
|f_h(q)-\alpha|\le\frac{\epsilon}{8}.
\]

Return

\[
\boxed{
\lambda_A=1,\qquad
\lambda_{B_i}=qp_i.
}
\tag{11}
\]

Equations (9)–(10) show

\[
\left|\mathbb E[X_{B_i}]-\beta_i\right|
\le |p_i(f_h(q)-\alpha)|+|p_iM-\beta_i|
<\epsilon.
\]

The \(A\)\-coordinate satisfies the same requirement.

All preprocessing, arithmetic, oracle calls, precision and returned rational encodings have polynomial cost in \(L\), with constants computable from the fixed structure.

**Significance\:** The full endpoint is therefore established for a non-product, arbitrarily high-rank family. Independent stoichiometric directions are not necessary for efficient calibration.

This does not by itself establish the theorem for every coupled weakly reversible structure.

## Further extension: complete multipartite creation networks

The preceding hub construction extends to an arbitrarily large number of coupled species groups and arbitrary fixed reaction molecularity.

Partition the species into \(s\ge2\) nonempty groups

\[
G_1,\ldots,G_s.
\]

For every tuple of species \(i_g\in G_g\), include the reversible reaction

\[
\boxed{
0\rightleftarrows
X_{1,i_1}+X_{2,i_2}+\cdots+X_{s,i_s}.
}
\tag{12}
\]

This is a fixed weakly reversible network of stoichiometric rank

\[
r=d-s+1.
\]

Its rank can be arbitrarily large, and the species are genuinely coupled.

### Exact class reduction

Let \(N_g\) denote the total population in group \(g\)\. The conserved differences are

\[
N_g-N_1=h_g,\qquad h_1=0.
\]

The entire nonnegative integer fibre satisfying these equations is one communicating class.

Indeed, whenever all group totals are positive, one molecule from each group can be removed by a death reaction. A birth followed by a death also exchanges the identities of molecules within any chosen group while preserving every group total. These operations connect all compositions at the minimal admissible group totals, after which births reconstruct every other population in the fibre.

Define

\[
S_g=\sum_{i\in G_g}\lambda_{g,i},
\quad
p_{g,i}=\frac{\lambda_{g,i}}{S_g},
\quad
q=\prod_{g=1}^s S_g.
\]

With \(n=N_1\) and

\[
n_{\min}=\max_g(-h_g,0),
\]

multinomial summation gives

\[
Z_\Gamma(\lambda)
=
\left(\prod_g S_g^{h_g}\right)
\sum_{n\ge n_{\min}}
\frac{q^n}{\prod_g(n+h_g)!}.
\tag{13}
\]

Conditionally on \(n\), populations within different groups are independent multinomials with totals \(n+h_g\) and probabilities \(p_{g,i}\)\.

Thus the full multidimensional inverse problem again reduces to one scalar function

\[
f(q)=
\frac{\displaystyle\sum_{n\ge n_{\min}}
nq^n/\prod_g(n+h_g)!}
{\displaystyle\sum_{n\ge n_{\min}}
q^n/\prod_g(n+h_g)!}.
\tag{14}
\]

Its derivative is

\[
f'(q)=\frac{\operatorname{Var}_q(n)}q>0.
\]

For a feasible target, let

\[
M_g=\sum_{i\in G_g}m_{g,i},
\quad \alpha=M_1.
\]

The target necessarily satisfies \(M_g=\alpha+h_g\)\. Choose positive rational multinomial proportions

\[
p_{g,i}=\frac{m_{g,i}+\zeta}{M_g+|G_g|\zeta},
\qquad
\zeta=\frac{\epsilon}{100d}.
\]

The coordinate errors introduced by this smoothing are less than \(\epsilon/100\)\.

The scalar consecutive-weight ratio is

\[
\frac{w_q(n+1)}{w_q(n)}
=
\frac{q}{\prod_g(n+1+h_g)}.
\]

Set \(H=\max_g|h_g|\), \(N_1=\lceil\alpha\rceil+3\), and take

\[
q_{\rm lo}=\frac{\epsilon}{1024(d+1)},\qquad
q_{\rm hi}=4(N_1+H+1)^s.
\]

As in the hub theorem,

\[
f(q_{\rm lo})\le n_{\min}+O(\epsilon),
\qquad
f(q_{\rm hi})> \alpha.
\]

A particularly useful direct resource bound follows from the scalar weights. For \(q\le Q=\lceil q_{\rm hi}\rceil+1\), choose

\[
T=\max\{n_{\min},2Q+H+2\}.
\]

For \(n\ge T\), successive weights decrease by a factor at least two. Therefore

\[
\mathbb E_q[n^2]
\le T^2+\sum_{j\ge0}(T+j)^2\,2^{-j}
\le(2T+4)^2.
\]

Hence

\[
\boxed{
0<f'(q)\le\frac{(2T+4)^2}{q_{\rm lo}}
}
\tag{15}
\]

throughout the bracket.

The right-hand side has \(O_R(L)\) binary digits, even though its numerical value can be enormous. Certified bisection therefore requires \(O_R(L)\) iterations, each using the accepted DDB1 moment evaluator at polynomial-bit rational activities.

Finally choose

\[
S_1=q,\qquad S_2=\cdots=S_s=1,
\qquad
\lambda_{g,i}=S_gp_{g,i}.
\]

This gives positive ordinary rational activities with polynomial binary height and the requested mean accuracy.

Thus **complete multipartite creation networks of arbitrary fixed molecularity and rank satisfy the full calibration contract**\.

## New rank-independent result: uniform local reaction witnesses

There is also a structural theorem applying to *every* fixed weakly reversible structure, not just the preceding examples.

For a reaction \(r\), let

\[
U_r=\{x\in\mathbb Z_{\ge0}^d:x\ge y_r\}.
\]

Call \(r\) active in \(\Gamma\) when \(U_r\cap\Gamma\ne\varnothing\)\.

### Uniform witness lemma

There is a computable integer \(D_R\), depending only on the fixed reaction structure, such that\:

For every actual class \(\Gamma\), every state \(x\in\Gamma\), and every active reaction \(r\), there are states \(z,z+\nu_r\in\Gamma\), with \(\nu_r=z_r-y_r\), satisfying

\[
\boxed{
\|z-x\|_\infty,\,
\|z+\nu_r-x\|_\infty\le D_R.
}
\tag{16}
\]

To prove this, use the accepted backward-coverability construction for the fixed upward-closed target \(U_r\)\.

Its predecessor set is upward-closed and has finitely many minimal elements. Each minimal predecessor has a fixed witness word reaching \(U_r\)\. Taking the maximum word length over these finitely many witnesses gives a bound independent of \(x_0\) and of the size of the populations.

Because every state of a weakly reversible communicating class can reach every other state, the witness can be lifted from one of the minimal predecessors to any \(x\in\Gamma\)\.

After the witness, fire reaction \(r\)\. The total coordinate displacement is bounded by a network-dependent constant.

This proves (16).

### Quantitative covariance consequence

Let

\[
S_\Gamma=\operatorname{span}_{\mathbb R}
\{\nu_r:r\text{ is active in }\Gamma\}.
\]

This is precisely the direction space of the affine hull of \(\Gamma\)\.

For the equilibrium law at \(\theta=\log\lambda\), there exists a computable integer \(c_R\ge1\) such that, whenever \(\|\theta\|_\infty\le B\), \(B\ge1\),

\[
\boxed{
v^\top\operatorname{Cov}_\theta(X)v
\ge
2^{-c_R(1+L+B)}\|v\|_2^2,
\qquad v\in S_\Gamma.
}
\tag{17}
\]

Here \(L\) includes the binary encoding of \(x_0\)\. The inequality is vacuous for rank-zero singleton classes.

The proof uses a conditional-Poisson tail estimate to find a state carrying probability at least \(2^{-O_R(L+B)}\)\. The witnesses in (16) put both endpoints of every active reaction direction within bounded distance of that state.

For populations bounded by \(2^{O_R(L+B)}\), fixed-distance factorial-weight ratios are at worst \(2^{-O_R(L+B)}\)\. Thus every active direction has a pair of nearby class states, both carrying probability at least \(2^{-O_R(L+B)}\)\.

Applying

\[
\operatorname{Var}(v\cdot X)
=
\frac12\sum_{x,y}\pi(x)\pi(y)
[v\cdot(x-y)]^2
\]

to a linearly independent set of active reaction increments proves (17). The least singular value needed for the independent increments has a positive computable lower bound, because the reaction vectors come from a fixed finite integer set.

**Consequence\:** The inverse moment map has an explicit, polynomial-bit local conditioning bound on every bounded log-activity region, after removing the exact conservation-law directions.

Combined with the conditional-radius selector, this controls both local sensitivity and numerical optimization. It still does not provide the missing global radius bound.

## Why a genuine reaction-class theorem is necessary

One can construct elementary connected bounded-step supports for which polynomial-bit inverse calibration actually fails.

For even \(N\), consider the artificial support

\[
S_N=
\{(k,0):0\le k\le N\}\cup\{(N,1)\}
\]

with factorial-product weights, and target

\[
m_N=(N/2,1/2),\qquad \epsilon=1/100.
\]

If \(p\) is the probability of \((N,1)\), mean accuracy requires

\[
0.49\le p\le0.51.
\]

Conditioned on the lower row, the first coordinate is a Poisson variable with activity \(\lambda_1\), truncated at \(N\)\. The first-coordinate mean constraint then forces its conditional mean below \(0.022N\) for sufficiently large \(N\)\.

Monotonicity of the truncated-Poisson mean implies

\[
\lambda_1<N/4.
\]

But balancing the upper point against the lower row requires

\[
\lambda_2
=
\frac p{1-p}
\frac{N!}{\lambda_1^N}
\sum_{k=0}^N\frac{\lambda_1^k}{k!}.
\]

Consequently,

\[
\boxed{
\lambda_2\ge
\frac{0.49}{0.51}
\left(\frac4e\right)^N.
}
\tag{18}
\]

Any ordinary positive rational encoding of \(\lambda_2\) therefore needs \(\Omega(N)\) binary digits, although \(N\) itself requires only \(O(\log N)\) digits.

This is **not a negative answer to the requested question**, because no fixed weakly reversible reaction structure realizing these supports has been established.

In fact, the uniform witness lemma rules out the most obvious attempted realization: if the second species is positive anywhere in an actual class, it can become positive within a fixed number of reactions from every state of that class. The artificial support violates this for large \(N\)\.

The example explains why arbitrary finite-support entropy bounds and ordinary graph connectivity are insufficient. The extra translation-invariant reachability structure of weakly reversible reaction systems is essential.

## Final status

| Result | Scope |
|--------|--------|
| Efficient global selector given polynomial log-activity radius | All fixed weakly reversible \(R\) |
| Uniform local active-reaction witnesses | All fixed weakly reversible \(R\) |
| Quantitative covariance lower bound on bounded parameter regions | All fixed weakly reversible \(R\) |
| Full inverse calibration in rank at most one | Accepted ROOT construction |
| Full inverse calibration for complete multipartite creation networks | Established above, arbitrary fixed rank |
| Full inverse calibration for arbitrary coupled weakly reversible structures | **Unresolved** |

The new machinery narrows the general problem. The selector and local conditioning no longer need to be treated as independent gaps. What remains is proving—or disproving—a **uniform polynomial-binary inverse-height theorem** for the complete range of actual weakly reversible classes.

The most relevant comparison remains Straszak and Vishnoi's urlMaximum Entropy Distributions: Bit Complexity and Stabilityhttps://proceedings.mlr.press/v99/straszak19a.html\. Their general finite-support bounds do not immediately control the factorial-weight and large-population regime here. citeturn142607search0 Work on urlA-hypergeometric distributions and Newton polytopeshttps://www.sciencedirect.com/science/article/pii/S0196885818300563 addresses moment-map inversion for related conditioned distributions, but does not establish this fixed-structure, every-run polynomial-bit contract. citeturn593668search0

**Verdict\:** No full positive or negative resolution for arbitrary rank is justified yet. The completed advances are a general radius-to-selector reduction, a uniform covariance theorem, and a full inverse algorithm for a substantial new arbitrarily high-rank family.
