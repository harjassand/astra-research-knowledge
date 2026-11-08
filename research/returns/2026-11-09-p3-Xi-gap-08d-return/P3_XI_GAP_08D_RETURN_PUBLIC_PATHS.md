# P3 Xi completed return

Source: https://chatgpt.com/c/6af0a937-daa0-83ec-99c5-8df8b56023e0
Model: normal-web GPT-6 standard, Extra High. Turn: 08d48904-2e54-4f56-b284-5e03d8d4894b. Response: b24d0ab2-1463-4e77-b2a1-bc957e27cd6c. Completed: 2026-11-08T19:25:23.346Z.
ZIP: none supplied in the visible return.

## Actual prompt

Resolve a DIFFERENT FULL stochastic-kinetics question: is positivity of the physical-time Poincare spectral gap DECIDABLE for every finite complex-balanced mass-action network? Your general weak-reversibility recurrence allocation ends UNRESOLVED; the new task is not a claimed solution or a special-case answer to it. You own all representations, methods, sources and framing.

INPUT: arbitrary finite species/reaction lists y_r->y'_r with binary nonnegative integer stoichiometries, positive rational rates kappa_r, a supplied positive rational complex-balanced point c (all complex flux equations checked exactly), and initial population x0. Let Gamma be the ACTUAL reachable communicating class, including disabled boundary reactions, not automatically the whole stoichiometric lattice. Absorbing singleton and finite classes must be handled explicitly. Native rates are q_r(x)=kappa_r*(x)_(y_r), with falling factorials; physical time is not embedded jump count. On Gamma the accepted stationary probability is pi(x)=Z_Gamma^-1*c^x/x!, with nonexplosion/positive recurrence at this scope.

For the closed stationary Dirichlet form
    E(f,f)=1/2 sum_(x in Gamma,r) pi(x) q_r(x)
                         [f(x+y'_r-y_r)-f(x)]^2,
define lambda=inf E(f,f)/Var_pi(f) over its nonconstant form domain. This is the Poincare gap of the additive symmetrization, specifying the norm-one L2 exponential-contraction property; do not silently equate it with every possible nonreversible spectral or prefactor-allowed TV rate.

Construct ONE uniform deterministic terminating algorithm for ALL valid inputs that decides lambda>0 versus lambda=0. In the positive case output a rigorous rational lower bound ell>0 with a full-domain Poincare proof. In the zero case output a finite description of a computable certified witness family f_j with Var_pi(f_j)>0 and E(f_j,f_j)/Var_pi(f_j)<=1/j for every integer j>=1 (finite-support rational witnesses if justified, or another fully effective form-domain construction). All reachability, class membership, normalization/tails, boundary geometry, precision and infinite-state quantifiers must be paid. Give proved computable BIT bounds in the COMPLETE input length, and in j for witness evaluation; polynomial efficiency is not assumed. No supplied drift/path certificate, stationary-normalizer/spectral/reachability oracle, uncharged infinite search, fixed dimension/molecularity, openness or full-orthant promise.

Alternatively, prove that no such total decision algorithm exists by a valid reduction within this EXACT rational complex-balanced mass-action model. A failed path criterion, a slow example or generic CTMC undecidability outside this model is not that result.

Actually read powerful predecessors, credited as existing machinery:
* Anderson-Cappelletti-Fan-Kim2309.06970v2 https://arxiv.org/html/2309.06970v2 Section2.1/Assumption2.2/Theorem2.5/Corollary2.8/Theorem3.2/Example2.4: quantitative positive-gap path comparison, all-species inflow/outflow complex-balanced gap, and an explicit detailed-balanced ZERO-gap network. General path hypotheses are sufficient, not a complete decision procedure.
* Kim-Kim2402.05343v1 https://arxiv.org/html/2402.05343v1 Theorem2.1/Definition3.3/Theorem3.2/Section5: dominating active cycle paths force non-exponential return tails/zero gap under the stated class-accessibility and ergodicity assumptions. Absence of such a cycle is not proved sufficient for a positive gap.
* Wu-Kang-Jia2610.11443v1 https://arxiv.org/html/2610.11443v1 Sections2-3/Definition8/Theorems6-8: structural long-time classification for LINEAR networks, not arbitrary nonlinear mass action or an automatic nonreversible Poincare classification.

Your prior reference-network construction and max-envelope identities remain available capital. A bounded channelwise comparison to a recurrent reference does NOT transfer recurrence for changed invariant laws. At the new supplied complex-balanced scope the invariant law is known, so a different central geometric operation is accessible.

Optional ROOT interfaces, which you may discard: writing x=rho+y gives
    pi(rho+y)*kappa_(y->z)*(rho+y)_y
      =Z^-1*kappa_(y->z)*c^y*c^rho/rho!.
The stationary adjoint channel z->y has rate constant kappa_(y->z)*c^y/c^z. Thus the energy can be symmetrized by explicit finite reaction data without a free stationary solver. For two rate vectors preserving the SAME supplied c/support, min/max channel ratios compare their forms; this does not compare different c without controlling the changed weights.

The existing unit-rate 0<->A+B, B<->2B example has pi=e^-2/(a!b!), Gamma=N^2, and sets D_n={(n,0),(n+1,1)}. Direct flux gives E(1_Dn,1_Dn)/Var(1_Dn)=2/[(n+2)(1-pi(D_n))]->0. Fast factorial stationary tails therefore do not imply a gap; a finite population cutoff alone is not a zero/positive decision. These are source-compatibility checks, not a prescribed cycle/path solution or a newly earned classification.

Pursue FULL resolution persistently and independently. The desired new capability is exact identification/certification of fast versus arbitrarily slow relaxation from a finite nonlinear reaction model, or a genuine impossibility theorem for that task.

you may use all subagents avaible
All inherited source/access/transfer holds apply to every subagent, including unknown identities. The failed OpenAI Uniform-Permanence GitHub tree, NSF https://par.nsf.gov/servlets/purl/10314785 fulltext-timeout and EVERY older failed original/transfer remain HELD: no retry/raw/PDF/mirror/alternate/identifying recovery/held-source injection. No attachments, new model/worker/resource/account/spending, Sol or Dots action.

## Available user-visible activity

Worked for 27m 41s

I’ll inspect the three specified results, then separate the parts of the decision problem that can be handled effectively—reachability, finite classes, stationary weights and gap witnesses—from the infinite-state positivity test. I’ll test whether the complex-balanced structure closes that last step or supports an exact undecidability reduction.

Assessed decidability and clarified the proof

Analyzed spectral gaps, reversibility, computational limits, and decidability

Developed effective tests connecting operator theory

Studied operator degeneracy

Assessed parameter dependence and refined spectral analysis

Searched 29 websites

One part is fully effective: the actual reachable class is a congruence class of a finite commutative rewriting system, so it can be handled without replacing it by the entire stoichiometric lattice. The rational complex-balanced weights also allow exact evaluation of finite-support, mean-zero Rayleigh tests. I’m working through the form-domain approximation to determine whether these tests certify every zero-gap instance.

Assessed and refined spectral-gap criteria while comparing network rates

Assessed gap criteria and decidability

Assessed a partial route and its spectral gaps

Refined spectral-gap criteria

Searched 1 website

The form-domain argument is complete and gives an exact rational witness test for every zero-gap class. A further reduction removes even the weighted-mean constraint: positivity of the global Poincaré gap is equivalent to positivity of a Dirichlet eigenvalue obtained by pinning one reachable state. That simplifies certificate generation, but deciding whether the pinned eigenvalue stays positive over all finite truncations is still the missing step.

Refined the analysis

## Complete response

# Physical-time Poincaré-gap decidability for complex-balanced networks

## 1\. Determination

**I have not established a total decision algorithm or an undecidability reduction for the full input class.** The results below identify which parts can be decided exactly and where the unrestricted decision problem remains open in this investigation.

The three specified predecessors give different sufficient criteria\:

- Anderson–Cappelletti–Fan–Kim prove positive gaps under quantitative path hypotheses, including the all-species inflow/outflow case, and give a detailed-balanced zero-gap example. citeturn549027view0turn549027view3turn549027view4
- Kim–Kim prove non-exponential convergence under dominating-cycle conditions, subject to actual class accessibility. Their conditions do not characterize every zero-gap network. citeturn549027view5turn435964view1turn549027view7
- Wu–Kang–Jia classify several long-time regimes of linear reaction networks. Their results do not supply a nonlinear Poincaré-gap decision procedure. citeturn671949view2turn435964view5turn435964view6

A central simplification is nevertheless available: the additive-symmetrization form can be reduced exactly to a finite collection of translated factorial-weighted differences.

## 2\. Exact canonical Dirichlet form

Write \(z_r=y'_r\), \(\nu_r=z_r-y_r\), and

\[
w(x)=\frac{c^x}{x!},\qquad
Z_\Gamma=\sum_{x\in\Gamma}w(x).
\]

For every reaction, set

\[
\alpha_r=\kappa_r c^{y_r}\in\mathbb Q_{>0}.
\]

Substituting \(x=\rho+y_r\) into the given Dirichlet form yields

\[
\boxed{
\mathcal E(f,f)=
\frac1{2Z_\Gamma}
\sum_r\alpha_r
\sum_{\substack{\rho\in\mathbb N_0^d\\
\rho+y_r\in\Gamma}}
\frac{c^\rho}{\rho!}
\left[f(\rho+z_r)-f(\rho+y_r)\right]^2.
}
\tag{1}
\]

This identity is valid for unbounded classes, boundary-disabled reactions and arbitrary molecularity. The two endpoints lie in the same class whenever the translated reaction is enabled.

Define the canonical comparison form \(\mathcal E_0\) by replacing every \(\alpha_r\) in (1) by \(1\)\. Then

\[
\alpha_{\min}\mathcal E_0(f,f)
\leq\mathcal E(f,f)
\leq\alpha_{\max}\mathcal E_0(f,f).
\]

The stationary variance remains unchanged. Consequently,

\[
\boxed{
\alpha_{\min}\lambda_0
\leq\lambda
\leq\alpha_{\max}\lambda_0.
}
\tag{2}
\]

This proves that, **for fixed reaction support, reachable class and concentration vector \(c\), positivity of the gap is independent of the positive channel coefficients**\. The replacement form is realizable by a detailed-balanced network containing the corresponding forward and reverse channels.

Equation (2) is stronger than comparing arbitrary Markov chains by rate constants: it works because the stationary measure is exactly the same. It does not compare different concentration vectors or establish whether \(\lambda_0\) is positive.

## 3\. Exact reachability and finite-class decisions

Complex balance with strictly positive fluxes implies weak reversibility. Every enabled reaction \(y\to z\) can therefore be reversed at the population level by lifting a directed complex path \(z\leadsto y\)\.

The reachable class is precisely a congruence class of the commutative rewriting rules

\[
X^{y_r}\longleftrightarrow X^{z_r}.
\]

More explicitly, form the binomial ideal

\[
I=\langle X^{y_r}-X^{z_r}:r\rangle
\subseteq\mathbb Q[X_1,\ldots,X_d].
\]

For population vectors \(a,b\),

\[
\boxed{
a\in\Gamma(b)
\quad\Longleftrightarrow\quad
X^a-X^b\in I.
}
\tag{3}
\]

The forward direction follows by multiplying binomial generators by residual monomials. Conversely, regard monomials as basis vectors of a rational vector space. The ideal is the span of edge differences in the undirected population graph; a difference of two basis vectors belongs to that span exactly when the vertices are connected.

Thus Gröbner-basis membership gives a terminating exact class-membership procedure. It does not replace \(\Gamma\) by the stoichiometric lattice.

Moreover, this is a cyclic initialized Petri net. Its reachable set is effectively semilinear by established Petri-net results, so finiteness of \(\Gamma\) is decidable. citeturn846025search4turn846025search5

For a finite class, enumerate its \(N\) states, compute the rational stationary probabilities, and form the finite symmetrized conductances

\[
C_{uv}=\frac{\pi(u)q(u,v)+\pi(v)q(v,u)}2.
\]

Choose a spanning tree of its undirected transition graph and let \(C_{\min}>0\) be its minimum tree-edge conductance. The path Cauchy–Schwarz inequality gives

\[
\operatorname{Var}_\pi(f)
\leq\frac{N-1}{C_{\min}}\mathcal E(f,f),
\]

hence the rigorous rational certificate

\[
\boxed{\ell=\frac{C_{\min}}{N-1}>0\quad(N\geq2).}
\tag{4}
\]

For an absorbing singleton, the nonconstant test domain is empty; with the usual convention \(\inf\varnothing=+\infty\), its gap is infinite and contraction is vacuous.

These procedures handle every finite reachable class without an assumed reachability or spectral oracle. They do not decide the infinite-class case.

## 4\. Zero gap has exact finite rational test witnesses

This is the strongest general effective result I can establish.

**Theorem.** For every nonabsorbing complex-balanced class \(\Gamma\),

\[
\boxed{
\lambda=0
\iff
\forall j\geq1\ \exists f_j:
\begin{cases}
f_j\text{ is rational-valued and finitely supported on }\Gamma,\\
\sum_xw(x)f_j(x)=0,\\
\sum_xw(x)f_j(x)^2>0,\\
\mathcal E(f_j,f_j)/\operatorname{Var}_\pi(f_j)\leq1/j.
\end{cases}
}
\tag{5}
\]

Every individual witness is verifiable using **finite exact rational arithmetic**, without evaluating \(Z_\Gamma\)\.

### Proof that finite-support tests are sufficient

Let \(M(x)=\sum_i x_i\), \(C=\sum_i c_i\), \(H=\max_r|y_r|\), and \(K=\sum_r\kappa_r\)\.

The total jump rate satisfies

\[
\Lambda(x)\leq K(1+M(x))^H.
\]

Let \(\chi_N(x)=\mathbf1_{\{M(x)\leq N\}}\) and \(J=\max_r\|z_r-y_r\|_1\)\. Since every jump changes \(M\) by at most \(J\),

\[
\mathcal E(\chi_N,\chi_N)
\leq
\frac K{Z_\Gamma}
\sum_{m\geq N-J}(1+m)^H\frac{C^m}{m!}
\longrightarrow0.
\tag{6}
\]

The convergence is effective. For example, once \(m_0+1\geq\max(2H,4C)\), consecutive terms of the series on the right have ratio at most \(1/2\)\. Its tail from \(m_0\) is bounded by

\[
2(1+m_0)^H\frac{C^{m_0}}{m_0!},
\]

a rational number. Also \(Z_\Gamma\geq w(x_0)>0\)\.

For any finite-energy \(f\), first clip it to \([-L,L]\)\. These bounded truncations converge to \(f\) in the form norm by dominated convergence for the squared jump differences. Multiplying each bounded truncation by \(\chi_N\) then approximates it in the form norm: the energy outside the cutoff tends to zero, and the cutoff error is bounded using \(L^2\mathcal E(\chi_N,\chi_N)\)\.

Thus finitely supported functions are dense in the form domain.

If \(f\) has stationary mean zero, fix one reachable anchor \(a\) and correct a finite approximation \(g\) by

\[
g^\circ
=
g-
\frac{\sum_xw(x)g(x)}{w(a)}
\mathbf1_{\{a\}}.
\]

This preserves finite support, makes the weighted mean exactly zero, and leaves the approximation convergent in the form norm. Rational approximation of its finitely many coefficients is possible because all weights \(w(x)\) are rational.

The infimum defining \(\lambda\) can therefore be taken over exactly the functions in (5). This proves the theorem.

### Exact verifier

For a rational, finitely supported, weighted-mean-zero \(f\), calculate

\[
A(f)=\sum_xw(x)f(x)^2,
\]

and

\[
D(f)=\frac12\sum_{x,r}
w(x)\kappa_r(x)_{y_r}
[f(x+\nu_r)-f(x)]^2.
\]

Although displayed as sums over \(\Gamma\), both are finite because \(f\) has finite support and the reaction displacements are bounded.

Then

\[
\boxed{
\frac{\mathcal E(f,f)}
{\operatorname{Var}_\pi(f)}
=\frac{D(f)}{A(f)}\in\mathbb Q.
}
\tag{7}
\]

The normalizer cancels exactly. The verifier checks the finite support states using (3), verifies \(\sum wf=0\), checks \(A>0\), and tests

\[
jD(f)\leq A(f)
\]

by integer cross-multiplication.

No real-number or spectral oracle is involved.

## 5\. A universal zero-gap witness generator, conditional on zero gap

The theorem gives a uniform program \(W(\text{input},j)\)\:

```text

Enumerate reachable states by breadth-first search.

Dovetail over all finite subsets of the states already found
and all rational-valued functions on those subsets.

For each candidate f:
    enforce exact weighted mean zero;
    compute rational A(f), D(f);
    if A(f) > 0 and j*D(f) <= A(f):
        output the finite support and all rational values;
        halt.
```

For **every input with \(\lambda=0\)**, this program halts for every positive integer \(j\) and returns a certified witness.

For an input with \(\lambda>0\), it need not halt for sufficiently large \(j\)\. Consequently, this is a witness-generation procedure, **not a total gap-decision algorithm**\.

Each individual certificate can be checked with a computable bit bound. If its support has \(s\) states, population-coordinate bit length at most \(H_x\), and rational-value bit length at most \(F\), direct factorial arithmetic and schoolbook rational operations give a bound polynomial in

\[
B,\ s,\ F,\ \log(j+1),\ 2^{B+H_x}.
\]

This is deliberately loose but charges factorial construction, rational denominators, reaction evaluation and output. The missing requirement is an input-only computable bound on the *search* for witnesses as a function of \(B\) and \(j\), uniform over all zero-gap instances. I have not established such a bound.

The logical classification is exact\:

\[
\lambda=0
\iff
\forall j\in\mathbb N_{>0}\ \exists f\in\mathcal F_{\mathbb Q}:
jD(f)\leq A(f),
\]

where \(\mathcal F_{\mathbb Q}\) is the effectively enumerable set of nonzero, finite-support, weighted-mean-zero rational functions.

Thus zero gap has a \(\Pi^0_2\) description and positivity a \(\Sigma^0_2\) description in the arithmetic hierarchy. These are upper bounds on logical complexity, **not** undecidability or completeness results.

## 6\. A sharper reduction: pin one reachable state

There is a simpler equivalent formulation of the infinite-class question.

Fix any \(a\in\Gamma\), for example \(a=x_0\), and define the Dirichlet eigenvalue of the process killed at \(a\)\:

\[
\lambda_a^{\mathrm D}
=
\inf_{\substack{h\in\operatorname{Dom}(\mathcal E)\\
h(a)=0,\ \|h\|_{L^2(\pi)}>0}}
\frac{\mathcal E(h,h)}{\|h\|_{L^2(\pi)}^2}.
\]

**Theorem — Exact pinned-gap comparison**

\[
\boxed{
\pi(a)\lambda\leq\lambda_a^{\mathrm D}\leq\lambda.
}
\tag{8}
\]

For the first inequality, any \(h\) with \(h(a)=0\) satisfies, by Cauchy–Schwarz,

\[
\operatorname{Var}_\pi(h)
\geq\pi(a)\|h\|_{L^2(\pi)}^2.
\]

For the second, given any nonconstant \(f\), put \(h=f-f(a)\)\. Then \(h(a)=0\), the Dirichlet energy is unchanged, and

\[
\operatorname{Var}_\pi(f)=\operatorname{Var}_\pi(h)
\leq\|h\|_{L^2(\pi)}^2.
\]

Taking the corresponding infima proves (8).

Therefore,

\[
\boxed{\lambda>0\quad\Longleftrightarrow\quad
\lambda_a^{\mathrm D}>0.}
\tag{9}
\]

This equivalence is general for irreducible chains with a stationary probability; its usefulness here is that the pinned variational problem eliminates normalization and the global mean-zero constraint.

The cutoff argument from Section 4 shows that finite-support rational functions vanishing at \(a\) form a core for the pinned problem. Consequently,

\[
\lambda_a^{\mathrm D}
=
\inf_{\substack{f\in C_c(\Gamma;\mathbb Q)\\f(a)=0,\ A(f)>0}}
\frac{D(f)}{A(f)}.
\tag{10}
\]

Even the unknown stationary normalizer can be eliminated from the translation back to the original Poincaré quotient. Because

\[
Z_\Gamma\leq e^{\sum_i c_i}
\leq2^{\lceil2\sum_i c_i\rceil},
\]

the explicit rational number

\[
p_a=
\frac{w(a)}{2^{\lceil2\sum_i c_i\rceil}}>0
\]

satisfies \(p_a\leq\pi(a)\)\.

Thus every rational finite-support function with \(f(a)=0\) and

\[
jD(f)\leq p_a A(f)
\]

is a **certified physical-time \(1/j\) Poincaré witness**\.

In particular,

\[
\boxed{
\lambda=0
\iff
\forall j\geq1\ \exists f\in C_c(\Gamma;\mathbb Q):
\quad f(a)=0,\quad A(f)>0,\quad
jD(f)\leq p_aA(f).
}
\tag{11}
\]

This provides a simpler universal zero-gap witness generator than the mean-zero construction: enumerate rational finitely supported functions vanishing at \(a\) and stop at the first one passing the exact rational inequality.

The unresolved decision question has now been reduced to\:

> Given this explicitly defined, rational-coefficient, finite-range, factorial-weighted graph operator on an effectively semilinear reachable class, decide whether its pinned Dirichlet spectrum has a strictly positive bottom.

No normalization, stationary-law computation or reachability ambiguity remains in that formulation. **The infinite-state lower bound remains the obstacle.**

## 7\. An additional decidable zero-gap criterion

For the special situation in which the exact reachable class is \(\Gamma=\mathbb N_0^d\), one can extract a finite-dimensional algebraic test that certifies some zero-gap networks.

This does not replace the unrestricted decision procedure, but it produces a different kind of certificate from the path criteria in the literature.

For \(u=(u_1,\ldots,u_d)\in\mathbb Q_{>0}^d\), define

\[
f_u(x)=u^x=\prod_i u_i^{x_i},
\qquad
P_r(u)=u^{z_r}-u^{y_r}.
\]

The full product-Poisson law gives the exact Rayleigh quotient

\[
\boxed{
\frac{\mathcal E(f_u,f_u)}
{\operatorname{Var}_\pi(f_u)}
=
\frac{\frac12\sum_r\alpha_r P_r(u)^2}
{1-\exp\left(-\sum_i c_i(u_i-1)^2\right)}
}
\tag{12}
\]

whenever \(u\ne(1,\ldots,1)\)\.

The derivation uses

\[
\mathbb E_\pi f_u^2
=\exp\left(\sum_i c_i(u_i^2-1)\right),
\]

and the factorial translation identity (1). Every such function lies in the form domain because all Poisson exponential moments are finite.

Consequently, if there exist positive vectors \(u_n\) satisfying

\[
\max_i(u_n)_i\longrightarrow\infty,
\qquad
\sum_r\alpha_r P_r(u_n)^2\longrightarrow0,
\tag{13}
\]

then necessarily \(\lambda=0\)\.

**The existence of sequences satisfying (13) is decidable.** It is equivalent to the first-order statement over the real numbers

\[
\forall T>0\ \exists u\in\mathbb R_{>0}^d:
\quad
\left(\bigvee_i u_i>T\right)
\ \land\
T\sum_r\alpha_r P_r(u)^2<1.
\tag{14}
\]

All coefficients are rational, and the expressions are polynomials with finite integer exponents. Quantifier elimination over real closed fields therefore decides (14), although its worst-case complexity can be enormous.

When (14) is true, rational points can be found in its open feasible regions. Choosing \(T\) sufficiently large as a computable function of \(c\) and \(j\) produces a rational \(u_j\) for which (12) is at most \(1/j\)\. The finite description \(f_j(x)=u_j^x\) is then a certified, computable, physical-time zero-gap witness family.

This is a **decidable sufficient condition**, not a necessary condition established for all zero-gap networks. In particular, its proof assumes that \(\Gamma\) is the whole orthant.

### Check against the stipulated detailed-balanced example

Consider

\[
0\rightleftarrows A+B,\qquad B\rightleftarrows2B
\]

with unit rates, \(c=(1,1)\), and \(\Gamma=\mathbb N_0^2\)\.

For each integer \(j\geq1\), set

\[
T_j=2j+2,\qquad f_j(a,b)=T_j^{a-b}.
\]

The first reaction pair contributes exactly zero energy because \(u_Au_B=1\)\. The second gives

\[
\frac{\mathcal E(f_j,f_j)}
{\operatorname{Var}_\pi(f_j)}
=
\frac{(T_j^{-1}-T_j^{-2})^2}
{1-\exp\left(-[(T_j-1)^2+(T_j^{-1}-1)^2]\right)}.
\]

Since \(T_j\geq2\), the denominator exceeds \(1/2\), and hence

\[
\boxed{
0<
\frac{\mathcal E(f_j,f_j)}
{\operatorname{Var}_\pi(f_j)}
<
\frac2{T_j^2}
\leq\frac1j.
}
\]

This is an explicit rational-valued, infinite-support witness family for every requested \(j\)\. Its evaluation requires only integer exponentiation and rational arithmetic, with runtime polynomial in the output bit length. It establishes the zero gap directly in physical time, without using embedded-jump asymptotics.

The zero-gap phenomenon itself is established in Anderson–Cappelletti–Fan–Kim and analysed by Kim–Kim; the exponential-character calculation supplies a separate exact certificate. citeturn549027view4turn435964view0

## 8\. Final assessment against the full output contract

| Required capability | Result |
|--------|--------|
| Exact reachable-class membership | Decidable |
| Finite versus infinite reachable class | Decidable |
| Absorbing singleton | Handled |
| Finite-class gap and rational lower bound | Constructed |
| Rational stationary-normalizer tail bounds | Constructed |
| Full-domain finite-support core | Proved |
| Certified \(1/j\) witnesses for any known zero-gap input | Constructive witness generator |
| Decidable algebraic zero-gap criterion for some full-orthant inputs | Constructed |
| Positive rational lower bound for every infinite-class positive-gap instance | **Not established** |
| Terminating positive-versus-zero decision for every infinite class | **Not established** |
| Uniform input-and-\(j\) bit bounds for the complete requested algorithm | **Not established** |
| Exact-model undecidability reduction | **Not established** |

The central mathematical reduction is

\[
\boxed{
\lambda>0
\iff
\inf_{\substack{f\in C_c(\Gamma;\mathbb Q)\\
f(x_0)=0,\ f\ne0}}
\frac{
\frac12\sum_{x,r}w(x)q_r(x)[f(x+\nu_r)-f(x)]^2
}{
\sum_xw(x)f(x)^2
}>0.
}
\]

Every individual quantity in this infimum is exactly computable. The reachable set is effectively representable, the stationary weight is known, and its tails have effective bounds.

What remains is an algorithm that decides whether these finite rational Rayleigh quotients have a **uniform positive lower bound across the entire infinite class**\. Finite truncations and the supplied sufficient criteria do not settle that quantifier.

**Final determination\:** I cannot prove that the requested full decision problem is decidable or undecidable. The results above establish substantial effective reductions and certified witness constructions, but no total terminating algorithm or valid impossibility reduction. Claiming either conclusion would exceed the mathematics proved.
