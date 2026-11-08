# P1 Xi return

Chat: https://chatgpt.com/c/6af0a89e-1ea0-83ec-a929-c30a009d952b
Prompt source: P1_FULL_PARALLEL_MATCHING_SAMPLER_FINAL_20261109.txt
Prompt turn: 8d9aff85-cb19-48b1-8b17-d3708fe7c4b2
Response: be4ccff8-cb0e-4024-92e2-96dabcd47bee
Model selected at dispatch: GPT-6 standard, Extra High. Collected 9 November 2026 Brisbane.
No ZIP visible.

## Complete response

# Parallel monomer–dimer sampling on arbitrary graphs

**Status: The requested theorem is not established by the cited results.** The central obstacle is achieving polylogarithmic parallel depth while retaining near-linear total bit work for arbitrary maximum degree.

Miao–Yin (18 September 2026) explicitly identifies sampling matchings in RNC as an open problem in Section 7. That question permits polynomial work; your requirement of near-linear work is stronger. citeturn419364view4turn994516view0

For fixed \(\lambda>0\), the strongest directly applicable guarantee in that paper is\:

| Requirement | Miao–Yin result | Requested |
|--------|--------|--------|
| Sampling law | Full monomer–dimer law | Same |
| Graphs | Arbitrary simple graphs | Same |
| Total work | \(\widetilde O_\lambda(n+m)\) arithmetic operations | \((n+m+B)L^{O_\lambda(1)}\) bit operations |
| Depth | \(\widetilde O_\lambda(\min\{\Delta,m^{1/3},\sqrt n\})\) with high probability | \(L^{O_\lambda(1)}\) on every execution |
| Randomness | Exact random choices assumed | Every fair bit charged |

The Ising localization algorithms of Chen–Liu–Yin–Zhang do achieve polylogarithmic depth, but for their specified Ising and random-cluster regimes. Their implementation does not establish a monomer–dimer posterior sampler. citeturn419364view5turn568058view4

The remaining question is whether a different sampling representation or a stronger analysis can eliminate the polynomial-depth dependence. That requires an additional theorem, not merely a finite-precision implementation of existing results.

## 1\. A finite-bit result that can be established

There is a useful strengthening of the existing result: its random-choice assumptions can be eliminated while preserving near-linear total bit work and obtaining a deterministic execution cap.

Proposition — finite-word implementation of the Miao–Yin sampler

For every fixed positive rational \(\lambda\), there are computable constants \(C_\lambda,c_\lambda\) and a uniform finite-word CREW algorithm satisfying\:

\[
\begin{aligned}
d_{\rm TV}(\mathcal L(M),\mu_{G,\lambda})&\le\varepsilon,\\
W_{\rm bit}&\le C_\lambda(n+m+B)L^{c_\lambda},\\
D_{\rm PRAM}&\le C_\lambda(1+D_G)L^{c_\lambda},
\end{aligned}
\]

on every execution, where

\[
D_G=\min\{\Delta,\lceil m^{1/3}\rceil,\lceil\sqrt n\rceil\}
\]

for \(m\ge1\)\. Word length is \(O_\lambda(L)\)\. The algorithm uses no unbounded rejection loop.

This is **not the requested theorem**\: the factor \(D_G\) remains.

### Construction and error accounting

Write \(\lambda=a/b\), with fixed positive integers \(a,b\), and set

\[
p=\frac{a}{a+b}.
\]

Use the Miao–Yin mixing theorem to choose

\[
N=\left\lceil C_\lambda m
\left(\log^2(n+2)+\log(4/\varepsilon)\right)\right\rceil
=O_\lambda(mL^2)
\]

random-scan updates. The exact chain, started at the empty matching, has TV error at most \(\varepsilon/4\)\.

Each update needs a uniform edge index and an independent Bernoulli(\(p\)\) bit. Both can be implemented with fixed-length fair-bit blocks, without rejection.

Choose

\[
k=\left\lceil\log_2\frac{8N(m+1)}{\varepsilon}\right\rceil
=O_\lambda(L).
\]

For independent uniform \(k\)\-bit integers \(U,V\), use

\[
e=1+\left\lfloor\frac{mU}{2^k}\right\rfloor,
\qquad
C=\mathbf1\left\{V<\left\lfloor p2^k\right\rfloor\right\}.
\]

The edge-index law is within \(m/2^k\) in TV of uniform, and the coin law is within \(2^{-k}\) of Bernoulli(\(p\)\). By coupling all \(N\) update instructions, their joint-law discrepancy is bounded by

\[
\delta_{\rm bits}
\le\frac{N(m+1)}{2^k}
\le\frac{\varepsilon}{8}.
\]

All \(2Nk=O_\lambda(mL^3)\) fair bits are generated and charged. The threshold for \(p\) is determined by finite integer arithmetic. Neither irrational probabilities nor exact-real operations are used.

Next, simulate the update instructions with Miao–Yin's interval records. Lemma 5.7 charges work to records, rather than repeated scanning over every peeling round. Apply Theorem 5.1 with failure budget \(\eta=\varepsilon/4\), impose its corresponding deterministic round cap, and return the empty matching if the cap is exceeded. citeturn419364view0turn419364view2

Using the exact chain as a coupling reference gives

\[
\begin{aligned}
d_{\rm TV}(\mathcal L(M_{\rm output}),\mu)
&\le
\delta_{\rm mixing}
+\delta_{\rm bits}
+\delta_{\rm overflow}\\
&\le \frac{\varepsilon}{4}
+\frac{\varepsilon}{8}
+\frac{\varepsilon}{4}
<\varepsilon.
\end{aligned}
\]

The record work bound, fixed-length randomness, finite-word graph processing, and fixed round cap give the claimed worst-case bit-work and depth bounds. Input handling and pointer indexing can be charged within the \(B\operatorname{poly}(L)\) allowance.

The empty graph requires no random bits and returns \(\varnothing\)\. Isolated vertices never generate records. At \(\lambda=1\), the stationary distribution used here is exactly uniform over every matching.

The proposition closes the finite-word accounting gap for this **sublinear-depth** approach, but does not supply polylogarithmic depth on arbitrary graphs.

## 2\. Testing alternative approaches

I examined whether negative-dependence methods, localization, and parallel counting-to-sampling reductions could bypass interval simulation. Two mathematical obstructions are particularly relevant.

### A. Matching edge indicators need not be negatively correlated

Consider the four-vertex path with edges \(e_1,e_2,e_3\)\.

Its partition function is

\[
Z=1+3\lambda+\lambda^2.
\]

For the two nonadjacent end edges,

\[
\Pr(e_1,e_3\in M)=\frac{\lambda^2}{Z},
\qquad
\Pr(e_1\in M)=\frac{\lambda+\lambda^2}{Z}.
\]

Consequently,

\[
\boxed{\operatorname{Cov}(X_{e_1},X_{e_3})
=\frac{\lambda^3}{(1+3\lambda+\lambda^2)^2}>0.}
\]

This rules out directly identifying arbitrary matching edge laws with negatively associated or strongly Rayleigh distributions. In particular, a standard determinantal-point-process sampler cannot simply be applied to the edge-indicator law.

It does not rule out a more sophisticated auxiliary-variable construction.

### B. Uniform covariance control fails under arbitrary exponential tilts

This matters because parallel continuous-walk sampling reductions require covariance or transport control under exponential tilts, together with efficient weighted counting. Miao–Yin explicitly distinguishes these requirements from its decreasing-field estimates. citeturn106628view0turn438024view0

Here is a concrete obstruction for the natural edge-indicator representation.

Take an even cycle \(C_{2q}\), \(q\ge2\), and give every edge weight

\[
w=2^{4q}.
\]

There are exactly two perfect matchings, each of weight \(w^q\)\. Every other matching contains at most \(q-1\) edges. Therefore,

\[
\Pr(|M|<q)
\le\frac{2^{2q}w^{q-1}}{2w^q}
=2^{-2q-1}.
\]

Number the edges cyclically and define

\[
F(M)=\sum_{i=1}^{2q}(-1)^iX_{e_i}.
\]

Rotational symmetry gives \(\mathbb EF=0\)\. On the two perfect matchings, \(F=\pm q\)\. Hence

\[
\operatorname{Var}(F)\ge(1-2^{-2q-1})q^2.
\]

Because the coefficient vector has squared Euclidean norm \(2q\),

\[
\boxed{
\lambda_{\max}(\operatorname{Cov}(X))
\ge (1-2^{-2q-1})\frac q2.
}
\]

Thus the covariance operator norm is unbounded under arbitrary positive edge-activity tilts, even for cycles.

This is a genuine obstruction to applying a dimension-independent arbitrary-tilt covariance theorem to the edge variables. It is **not a lower bound against parallel monomer–dimer sampling at fixed \(\lambda\)**\.

### C. Sampling monomers does not complete the problem

Let \(U(M)\) be the set of unmatched vertices, and let \(\operatorname{pm}(H)\) denote the number of perfect matchings of a graph \(H\)\. Exactly,

\[
\Pr(U(M)=U)
=
\frac{
\lambda^{(n-|U|)/2}\operatorname{pm}(G[V\setminus U])
}{
Z_G(\lambda)
}
\]

when \(n-|U|\) is even.

Conditioned on \(U\), the remaining matching is uniform over the perfect matchings of \(G[V\setminus U]\)\.

Therefore, an algorithm that generates only the correct monomer set has not generated the matching. It must also implement this conditional distribution, with its work and depth fully charged.

Neither the monomer covariance bounds nor approximate partition-function estimates alone establish that implementation.

## 3\. What remains to prove

A positive resolution requires replacing the remaining \(D_G\) factor in Section 1 with polylogarithmic depth while keeping all of the following simultaneously\:

- Near-linear total bit work on every execution.
- Fixed-length, charged randomness and finite-word arithmetic.
- A valid matching on every execution, including capped failures.
- A TV guarantee for the unconditional joint output law.
- Uniformity over all graphs, degrees and fixed positive rational activities.

One possible sufficient result would be a new degree-independent, record-charged parallel evaluator for the Glauber trajectory. Another would be a genuinely different generative process with an efficiently implementable global transition and provably polylogarithmic mixing.

Neither has been proved here.

There is also no established reduction or independently justified complexity assumption from this investigation yielding the required negative result. The large-depth behavior of a particular chain simulation is not a lower bound for sampling the distribution itself.

## Final determination

The full question remains unresolved.

The concrete result established above is a finite-bit, worst-case-work implementation of the existing sublinear-depth sampler. The covariance calculations rule out two straightforward ways of importing generic parallel-sampling machinery, but do not establish impossibility.

In particular, I cannot justify either

\[
\boxed{
\exists\ \text{a uniform near-linear-work, polylog-depth sampler}
}
\]

or its negation under your stated model.

Claiming either would require an additional mathematical argument that I have not obtained.

## Visible activity — Worked for 25m 31s

I’ll examine the two specified papers and the strongest related parallel-sampling results, then test whether a different representation can remove the degree-dependent depth. I’ll also check any proposed construction against the finite-word, random-bit, total-work, and unconditional-TV requirements. I’ll distinguish a complete proof from a restricted result or an unresolved gap.
Assessed sampling methods and analyzed parallel block updates
Assessed exact simulation methods, representations, difficulty, and sampling frontiers
Developed auxiliary representations and assessed sparsification limits
Synthesized obstacles and checked known status
Evaluated sampling barriers, complexity, and parallelization possibilities
Evaluated parallel sampling strategies
Assessed sampling barriers
Assessed sampling routes
Searched 36 websites
