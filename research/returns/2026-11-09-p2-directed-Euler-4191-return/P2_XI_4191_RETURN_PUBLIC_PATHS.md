# P2 completed return

Source: https://chatgpt.com/c/6af0d94a-c2ac-83ec-bb1c-2245049b09e6
Model: GPT-6 standard, Extra High. The original and continuation had shown delivery timeouts; the continuation has now returned an answer. No producer ZIP visible.

## Original prompt

Resolve the SAME FULL near-linear ENTIRE-TV sampling question for arbitrary directed Eulerian multigraphs. Your1F5 bidirected construction and exact matching-cut reformulation stand; the asymmetric full-class algorithm is still missing. You own every method, representation, source order and framing.

INPUT: an explicit finite strongly connected directed Eulerian multigraph G with n>=1 vertices and m labelled distinguishable arcs, all degrees/loops/parallel arcs allowed. B is COMPLETE binary input length including labels and rational 0<epsilon<=1/2. ET(G) is cyclic Eulerian arc orderings modulo rotation, represented with the smallest-labelled arc first. Handle n=1,m=0 by the empty tour.

Construct ONE uniform randomized finite-word algorithm whose EVERY run outputs a VALID tour, whose unconditional ENTIRE law is within TVepsilon of Unif(ET(G)), and whose EVERY-run TOTAL BIT work/random-bit count/memory are
 C*(n+m+B)*L^c, L=1+ceil(log2((n+m+B+2)/epsilon)),
for fixed computable C,c independent of graph/epsilon. Words O(L) bits; actual word-operation bit costs, graph validation, starting tour, preprocessing, degree reduction, indices, rebuilding, numerical precision, randomness and output ALL paid. No expected-only/unbounded rejection, hidden scans, free counting/determinant/flow/dynamic-query oracle, large uncharged preprocessing or tiny-event conditioning. No symmetry/degree/expansion/planarity promise. Alternatively prove a genuine full-contract impossibility under a precisely justified assumption, not failure of one walk/data structure.

Accepted scoped capital, credited once:
* Anari2605.29566v1 https://arxiv.org/html/2605.29566v1 Thms1-4/Sections2-6/Lemmas19-20/Thm21/Thm26 already give the full-class m^(3/2)*polylog sampler. Degree-two flat skew-determinantal support has near-linear flip-repair MIXING STEPS; actual crossing-chord backend costs (s+M/s)logM per step. Pointwise degree gadgets, not local-TV conditioning, preserve near-uniform projection. Neither square-root backend nor general no-go is a premise.
* Your1F5 near-linear bidirected sampler: pair reverse arcs, sample an undirected spanning tree, orient toward root, then BEST last-exit completion with fixed-bit local shuffles. Full arbitrary directed graphs are not bidirected. Anari-Liu-OveisGharan-Vinzant-Vuong2004.07220v2 https://arxiv.org/pdf/2004.07220v2 Thms1-2 supplies O(k log(k/delta)) down-up mixing from every start and the established near-linear undirected-tree operation; ROOT read those contracts.
* BEST equivalence has equal factorial lift counts, no rejection. In the degree-two core the crossing set is the boundary of a fixed matching across a dynamically reordered interval, equivalently the support of a parity sum. Your exact reformulation does NOT supply adaptively valid uniform support sampling/counts/polylog updates. Local-order Hierholzer can be biased (3,3,2 on the bidirected triangle); independent local-transition acceptance can be n/2^n on a bidirected cycle. These are route diagnostics, not full negatives.

NEW actually ROOT-read alternative operation: Fleischmann-Li-Saranurak-Wang2610.10898v1 https://arxiv.org/html/2610.10898v1 , Lemma2.1/Lemma3.0/Sections3-4/Thm4.4. For an OUT-arborescence T rooted at r and rational q dominating SOME point of its arborescence polytope (that feasible point is not supplied/computed), a global random-tree update satisfies
 E[1_(T')|T]<=(1_T+q)/2.
It routes one demand flow on O(m log^2 n) auxiliary edges, rounds preserving EXPECTED edge flows, partitions a 2-edge-connected 2(n-1)-arc union into two arborescences, and chooses one. Cost is ONE max-flow computation plus near-linear extra work, NOT a free/polylog update. The paper's overall mincut result assumes polynomially bounded integral weights and yields m^(1+o(1)), not your required bit-near-linear bound. Reverse arcs to compare in-arborescences. Its marginal contraction gives NEITHER uniform joint law, reversibility, TV mixing nor a free feasible q oracle.

Optional ROOT intuition only: this global directed-tree operation is a different candidate from maintaining every crossing query; it might permit a different full sampler, but marginal information is insufficient. On bidirected K4 rooted at r, the uniform law on four oriented stars and the uniform law on twelve oriented Hamilton paths have IDENTICAL directed-edge marginals and disjoint supports (TV1). You may discard this operation and intuition.

Pursue FULL resolution persistently. Do not replace it with another bidirected sampler, a conditional data-structure theorem, an edge-marginal result or m^(1+o(1)) work.

you may use all subagents avaible
All inherited source/access/transfer/resource holds apply to every subagent, including unknown identities. EVERY failed original/transfer, including NSF10314785, OpenAI Uniform-Permanence tree, Dots/Golding-Henderson/Serre/CarloAlberto/root2410.23225v3/TR26-272/2610.00548v2 and all others, remains HELD: no retry/raw/PDF/mirror/alternate/identifying recovery/held-source injection. No attachments, extra principal/model/worker/resource/account/spending, Sol or Dots action.

## Continuation

please continue.

## Visible working explanation

I’ll continue from the asymmetric case, focusing on whether the BEST correspondence can be paired with a genuinely near-linear directed-arborescence sampler. I’ll also test a different route through exact tree distributions, rather than assuming the new global update gives total-variation mixing.

Explored dynamic arborescence sampling and assessed exact methods

Searched 8 websites

The alternative arborescence update does not appear to close the gap: its proved inequality controls edge marginals, not the joint tree law, and each update pays for a max-flow computation. I’m now testing whether the matching-cut problem admits a smaller exact algebraic representation that would avoid maintaining crossing counts explicitly.

Searched 10 websites

## Full response

# Continued investigation: arbitrary directed Eulerian-tour sampling

**The full \(O((n+m+B)L^c)\) worst-case bit-work theorem remains unresolved.** I examined the two main routes against the actual guarantees of Anari (2026) and Fleischmann–Li–Saranurak–Wang (2026). Neither currently establishes the requested sampler. citeturn840538view0citeturn840538view1

I can establish an additional obstruction to one proposed algebraic implementation, but it is deliberately narrower than an impossibility theorem for the full problem.

## 1\. A lower bound for deterministic fixed linear summaries

In the degree-two core, fix a queried chord \(x\) and let the remaining \(N-1\) chords have two labelled endpoints each. For a cyclic ordering \(\Gamma\), define

\[
z(\Gamma,x)\in\mathbb F_2^{N-1},
\]

where \(z_y=1\) exactly when chord \(y\) crosses \(x\)\.

**Lemma.** Every vector \(z\in\mathbb F_2^{N-1}\) is realizable as \(z(\Gamma,x)\) by some cyclic ordering of these endpoints.

**Proof.** Place the first endpoint of \(x\), then exactly one endpoint of each chord \(y\) with \(z_y=1\), then the second endpoint of \(x\)\. Place all remaining endpoints outside that interval. Each selected chord crosses \(x\) exactly once, and no unselected chord does. Thus the crossing vector equals \(z\)\. \(\square\)

Now suppose a data structure retains only

\[
Az\in\mathbb F_2^k,
\]

for a fixed matrix \(A\), and uses this summary to answer every possible crossing query exactly.

If \(k<N-1\), then \(A\) has a nonzero kernel vector \(h\)\. Consequently,

\[
A0=Ah.
\]

But for the zero crossing vector, the flip-repair step must return \(x\) with probability one. For the nonzero vector \(h\), it must return \(x\) with probability

\[
\frac1{1+|\operatorname{supp}(h)|}<1.
\]

The same summary cannot specify both exact distributions.

Therefore,

\[
\boxed{k\ge N-1}
\]

is necessary for this particular deterministic, fixed-linear-summary representation.

This does not rule out randomized sketches, nonlinear structures, query-specific randomness, or data structures using additional state. It also does not imply that every crossing pattern can occur within the tour orbit of one fixed directed graph. Hence it is **not** a full-class lower bound.

It does establish why simply replacing the chunk vectors by one short, deterministic XOR aggregate cannot solve the exact problem.

## 2\. Why the new directed-tree operation does not imply TV mixing

The Fleischmann–Li–Saranurak–Wang update guarantees

\[
\mathbb E[\mathbf1_{T'}\mid T]
\leq \frac{\mathbf1_T+q}{2}.
\]

This is an inequality about individual edge-inclusion probabilities, not the probability of an entire tree. The algorithm uses a global flow computation, integral rounding and a decomposition into two arborescences. citeturn385419view2

To turn this into the requested sampler, one would need at least two additional results\:

1. A transition kernel with the uniform arborescence distribution as an invariant measure, and a proved sufficiently rapid convergence bound in total variation.
2. An implementation of that kernel with sufficiently small *total* worst-case bit work, including all flow computations.

Neither follows from marginal contraction. Even convergence of every edge marginal to its uniform value would not imply convergence of the joint distribution.

In particular, the uniform directed-tree law cannot be reconstructed from the vector of edge marginals alone. Thus the new update is useful for its min-cut objective but does not yet replace Anari's flip-repair walk as a uniform sampler.

## 3\. The strongest remaining routes

There are two distinct ways a full positive result could emerge.

**Route A: Improve the flip-repair implementation.** Retain the accepted near-linear mixing-step count, but replace the square-root chunk backend with a polylogarithmic dynamic crossing sampler. Such a sampler must correctly handle both the crossing count and the conditional selection law under adaptive changes to the cyclic order. The existing source proves the mixing and square-root implementation, but not this stronger operation. citeturn385419view0

**Route B: Sample directed arborescences directly.** Use BEST to transform an entire-TV-accurate directed-arborescence sample into an entire-TV-accurate tour. This avoids degree reduction and dynamic chord queries. However, I have not obtained a near-linear, worst-case-bounded directed-arborescence sampler for arbitrary asymmetric Eulerian digraphs.

There is also a useful distinction between these routes: Route A requires only an approximate crossing distribution per step, with errors controlled conditionally along the chain. Route B requires an approximate distribution on whole directed trees. Neither can be replaced by accurate edge marginals.

## 4\. Resource-contract audit

The remaining requirements cannot be considered discharged merely by obtaining polylogarithmic mathematical operation counts.

A complete proof must supply explicit algorithms and bounds for fixed-bit random choices, word-size arithmetic, dynamically reordered sequence storage, amortized rebuilding across every execution, gadget construction failure, and the TV error of the final projection.

In particular, an implementation that has \(O(m\operatorname{polylog}m)\) *expected* work but an unbounded random stopping time would still fail the specification. A random sketch with high success probability would need an explicitly charged fallback that always outputs a valid tour.

## Final determination

The work in this continuation establishes one additional scoped lemma—the linear-summary lower bound—and confirms that the global directed-arborescence update does not supply the missing joint-distribution guarantee.

It does **not** construct the required full-class near-linear sampler, and it does **not** establish an impossibility theorem under a justified complexity assumption.

The strongest applicable full-class result I can substantiate remains Anari's \(\widetilde O(m^{3/2})\) sampler. No justified conclusion presently closes the gap to \(O((n+m+B)L^c)\)\.

