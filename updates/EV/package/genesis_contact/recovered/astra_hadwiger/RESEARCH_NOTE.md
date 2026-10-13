# Astra Genesis: contact completion and chromatic-critical compression

Date: 13 October 2026

## Status and scope

The selected universal objective is

\[
\chi(G)\le 2h(G),
\]

where \(h(G)\) is the largest order of a complete-graph minor in a finite simple graph \(G\). This note does **not** prove that inequality. It establishes a local contact-completion certificate, an exact matching pin-release operation, and an application separating ordinary from dominating clique-minor models in a modified Suzuki–Tits construction. It also proves that a published family obstructing perfect connected partitions is chromatically redundant: each member has a clique of its full chromatic number.

The contact certificate is an application of established lopsided-local-lemma machinery, not a new local lemma. The pin-release operation belongs to the established resampling-oracle framework. The additional application and structural observations were derived in this investigation, but their priority has not been certified. None of the proofs here has been checked in a formal proof assistant or independently refereed.

### Current-status inputs

Wood's 7 October 2026 preprint [W] states a universal bound \(\chi(G)\le19{,}885{,}160h(G)\), refining a linear theorem of Norin and Steiner. Separately, the supplied OpenAI archive [O] claims counterexamples to the exact inequality \(\chi\le h\). The archive claim has not been independently audited here; [W] still describes the exact conjecture as open. These sources should not be represented as an independently reconciled consensus. Neither statement supplies the factor-two theorem targeted here.

## 1. Exact pair-contact completion

Two disjoint edges of a graph **touch** when an edge joins their endpoint sets. A pairwise-touching matching of size \(r\) is a \(K_r\)-minor model with two-vertex branch sets. This is stronger than saying that all matching edges lie in a connected component.

Let \(H\) be a graph on an even number \(N\ge4\) of vertices, and let \(G=\overline H\). Write

\[
D=\Delta(H),\qquad
C=\max_v c_H(v),
\]

where \(c_H(v)\) counts induced four-cycles containing \(v\), each four-cycle counted once.

### Theorem 1. Finite contact certificate

For \(x,y\in(0,1)\), put

\[
L=(1-x)^D(1-y)^C.
\]

If

\[
\frac1{N-1}\le xL^2,
\qquad
\frac1{(N-1)(N-3)}\le yL^4,
\tag{1}
\]

then \(G\) has a pairwise-touching perfect matching. In particular,

\[
h(G)\ge N/2.
\]

#### Proof

Choose a perfect matching \(M\) uniformly from all perfect matchings of the complete graph \(K_N\). Introduce two kinds of bad events.

* For every edge \(e\) of \(H\), the event \(e\in M\), of probability \(p_1=1/(N-1)\).
* For every induced four-cycle of \(H\), the event that both of its diagonals belong to \(M\), of probability \(p_2=1/((N-1)(N-3))\).

Avoidance of the first kind makes every matching edge an edge of \(G\). If two such matching edges do not touch in \(G\), all four cross pairs are edges of \(H\), while their two diagonals are not edges of \(H\). Thus the four vertices induce exactly a four-cycle of \(H\), giving a bad event of the second kind. Conversely, that event certifies failure of contact. This reduction is exact.

Every bad event is the occurrence of a specified partial matching in a uniform complete-graph perfect matching. By the Lu–Székely negative-dependency theorem [LS], incompatibility of the specified partial matchings gives a negative dependency graph. Enlarge it by joining all events whose vertex supports intersect; adding dependency edges preserves the required property.

Every vertex belongs to at most \(D\) events of the first kind and \(C\) events of the second kind. Assign local-lemma activity \(x\) to the first kind and \(y\) to the second. For an event supported on \(r\) vertices, the product of \(1-\text{activity}\) over its neighbours is at least \(L^r\). Counting a neighbour more than once, or including the event itself in this lower bound, only decreases the product. Here \(r=2\) or \(4\), respectively. Conditions (1) are therefore sufficient for the lopsided local lemma. With positive probability no bad event occurs. Contracting the matching edges produces \(K_{N/2}\). QED.

### Corollary 1. A dimensionless local-conflict threshold

Consider an even-order sequence \(H_N\) such that

\[
\Delta(H_N)=o(N),\qquad
\limsup_{N\to\infty}\frac{\max_v c_{H_N}(v)}{N^2}<\frac1{4e}.
\tag{2}
\]

Then \(\overline{H_N}\) has a pairwise-touching perfect matching for every sufficiently large \(N\) in the sequence.

#### Proof

Choose \(c\in(0,1/(4e))\) exceeding the limsup in (2). Set \(x=A/N\) and \(y=B/N^2\), for fixed positive constants. For large \(N\),

\[
\log L\ge -cB-o(1).
\]

The required strict limiting inequalities are

\[
Ae^{-2cB}>1,\qquad Be^{-4cB}>1.
\]

Taking \(B=1/(4c)\) makes the second left-hand side \(1/(4ce)>1\). Then choose \(A>e^{2cB}\). The strict margins absorb the finite-\(N\) corrections. QED.

The number \(1/(4e)\) is a threshold of this scalar activity calculation. It is **not** claimed to be the optimal graph-theoretic threshold.

### Vertex-dependent version

Assign an activity \(z_E\in(0,1)\) to each canonical bad event \(E\), and define

\[
L_v=\prod_{E:\,v\in\operatorname{supp}(E)}(1-z_E).
\]

It suffices to check

\[
\Pr(E)\le z_E\prod_{v\in\operatorname{supp}(E)}L_v
\]

for every event. The same support-counting proof applies. This can retain nonuniform local information that the maxima \(D,C\) discard.

### Rooted extension of an existing model

Suppose \(B_1,\ldots,B_r\) are disjoint connected, pairwise-touching branch sets in a larger graph \(G\), and \(U\) is a disjoint even set of unused vertices, \(|U|=N\). Put \(H=\overline{G[U]}\), and

\[
S_i=\{u\in U: N_G(u)\cap B_i=\varnothing\}.
\]

Define a forbidden-edge graph on \(U\) by

\[
F=H\cup\bigcup_{i=1}^r K_{S_i}.
\]

Apply Theorem 1 with the first-kind events indexed by \(E(F)\), and the second-kind events still indexed by induced four-cycles of \(H\). Thus use \(D=\Delta(F)\), while \(C\) is computed from \(H\).

Avoidance gives a perfect matching of \(G[U]\) whose edges touch one another and every old branch set. Consequently it extends the old model to a \(K_{r+N/2}\)-model without moving or overlapping old branch sets. The added restrictions are ordinary forbidden matching edges, not an assumed minor-extension theorem.

This operation is only useful when its explicit local budget is satisfied. The present note contains no universal theorem producing such a budget from high chromatic number.

## 2. An exact local operation: release matching pins

Let a perfect matching \(M\) be uniformly distributed conditional on containing specified disjoint edges \(F\). One can remove this conditioning exactly, while creating new edges only incident to the original support of \(F\).

For one pinned edge \(ab\), on a free vertex set \(W\), choose \(x\) uniformly from \(W\setminus\{a\}\). If \(x=b\), do nothing. Otherwise let \(xy\) be the matching edge at \(x\), and replace

\[
\{ab,xy\}\quad\text{by}\quad\{ax,by\}.
\tag{3}
\]

The result is a uniform perfect matching on \(W\). Indeed, given an output matching \(M'\), its unique inverse choice is \(x=M'(a)\). If \(x\ne b\), let \(y=M'(b)\) and undo the switch. Thus conditioned matchings together with the random choice are in bijection with all unconditioned matchings.

For several pins, release them one at a time, temporarily excluding the endpoints of the still-pinned edges from \(W\). At each stage the remaining conditioning is exactly the set of pins not yet released. Iteration gives the uniform unconditioned law.

Every newly created edge in (3) meets \(\{a,b\}\). Consequently no canonical bad event supported outside the original pin support can be newly created. This is an explicit matching resampling oracle in the established framework [HV, H]. It does not, by itself, prove termination of an arbitrary repeated-repair rule. No new general algorithmic-local-lemma claim is made here.

`pin_release.py` implements this operation, validates its inputs, and exhaustively checks its bijection and support locality on complete graphs of orders 4, 6, 8 and 10 with up to three pins. For order 10, all 945 output perfect matchings have exactly one preimage in each tested release experiment.

## 3. Application to a hard dominating-model obstruction

This section uses the following published geometric input, rather than claiming its invention. The Suzuki–Tits graph \(S_q\), for \(q=2^{2h+1}\), has \(N=q^4\) vertices and \(q^5+q^3\) special affine lines of length \(q\). Every vertex is on \(q^2+1\) lines; all triangles lie on a line. Adjacent pairs have \(q-2\) common neighbours, and nonadjacent pairs have \(q(q-1)\). The deterministic part of [IS] rules out a dominating model of order \(\lceil(1/2-\delta)N\rceil\) in the complement of a line-bipartite subgraph whenever all line sides have size at least \(q/3\), noncollinear pairs have codegree at least \(q^2/5\), and independence number is below \(2q^3\), for an absolute \(\delta>0\).

### Theorem 2. Ordinary chromatic-size models coexist with the dominating obstruction

For every sufficiently large \(q=2^{2h+1}\), there exists a graph \(G_q\) with \(N=q^4\) vertices such that

\[
\alpha(G_q)=2,\qquad \chi(G_q)=N/2,
\]

\(G_q\) has a \(K_{N/2}\)-model all of whose branch sets have size two, but \(G_q\) has no dominating \(K_{\lceil(1/2-\delta)N\rceil}\)-model for a fixed absolute \(\delta>0\).

In particular, the conclusion is \(h(G_q)\ge\chi(G_q)\); equality of these two parameters is **not** asserted.

#### Construction

Choose one special direction. Its \(q^3\) parallel lines partition all vertices. On each such line, fix a balanced bipartition into two sets of size \(q/2\). On every other special line, independently assign a fair binary label to each of its vertices. Keep only the edges joining differently labelled vertices on a line, and call the resulting subgraph \(H_q\). Let \(G_q=\overline{H_q}\).

#### Proof of exact chromatic number

The graph \(H_q\) is triangle-free because every original triangle lies on one line, whose retained graph is bipartite. The fixed parallel class consists of disjoint copies of \(K_{q/2,q/2}\), so \(H_q\) contains a perfect matching. Its edges form independent pairs in \(G_q\), giving \(\chi(G_q)\le N/2\). Triangle-freeness gives \(\alpha(G_q)\le2\), hence the reverse chromatic inequality. The perfect matching also ensures \(\alpha(G_q)\ge2\).

#### Proof of the local conflict estimate

Fix noncollinear vertices \(u,w\), meaning a nonedge of \(S_q\). Their \(q(q-1)\) common neighbours each use two special lines, one through \(u\) and one through \(w\). All these lines are distinct. For example, two common neighbours lying on the same line through \(u\) would, with \(w\), form a triangle and hence force \(u,w\) onto the same special line, a contradiction.

At most two of these common-neighbour witnesses involve fixed parallel-class lines: at most one line through each endpoint can be fixed, and no line is reused. Apart from these at most two exceptions, witness survival events are mutually independent Bernoulli variables of parameter \(1/4\). Therefore, uniformly over noncollinear pairs, with probability \(1-o(1)\),

\[
d_{H_q}(u,w)=\bigl(1/4+o(1)\bigr)q^2.
\tag{4}
\]

For a concrete uniform error, a Chernoff bound with deviation \(Kq\sqrt{\log q}\), for a sufficiently large fixed \(K\), permits a union bound over fewer than \(q^8\) pairs. The two exceptional witnesses contribute only a bounded error. For collinear pairs, codegree is at most \(q\), deterministically.

In a triangle-free graph,

\[
c_H(v)=\sum_{w\ne v}\binom{d_H(v,w)}2.
\tag{5}
\]

Each four-cycle through \(v\) has a unique opposite vertex \(w\), explaining the absence of an additional factor. There are \(O(q^3)\) collinear choices of \(w\). Equations (4)–(5) give, uniformly in \(v\),

\[
\begin{aligned}
c_{H_q}(v)
&\le O(q^3)\binom q2
 +N\binom{(1/4+o(1))q^2}2\\
&\le (1/32+o(1))N^2.
\end{aligned}
\]

Also \(\Delta(H_q)\le(q^2+1)(q-1)=o(N)\). Since \(1/32<1/(4e)\), Corollary 1 produces a pairwise-touching perfect matching in \(G_q\).

#### Preservation of the published dominating obstruction

The fixed line sides have size exactly \(q/2\); the other lines have both sides at least \(q/3\) with high probability. Equation (4) gives the required codegree lower bound. For a fixed set \(I\) of size \(2q^3\), use only the \(q^5\) nonfixed lines. Each vertex belongs to exactly \(q^2\) of these lines, so independence in their retained bipartite graphs has probability at most

\[
2^{q^5-q^2|I|}=2^{-q^5}.
\]

A union bound over at most \(2^N\) sets gives \(\alpha(H_q)<2q^3\) with high probability. The fixed lines can only make independence harder. Thus all inputs to the deterministic obstruction in [IS] survive the modification, and its proof excludes the indicated dominating model. All the high-probability properties hold simultaneously, completing the existence proof. QED.

Theorem 2 is a separation result for a concrete construction, not a proof that arbitrary high-chromatic graphs admit such pair models.

## 4. Why pair-only universality is false

Let \(G\) consist of two disjoint copies of \(K_4\), together with one bridge joining them. Then

\[
\alpha(G)=2,\qquad\chi(G)=h(G)=4.
\]

A perfect matching cannot use the bridge, because that would leave three unmatched vertices on each side and no available cross edge. Hence every perfect matching has two edges on each side. On either side, one of these matching edges avoids the bridge endpoint and cannot touch any matching edge on the other side. There is no pairwise-touching perfect matching.

Nevertheless four singleton vertices in one \(K_4\) already give a chromatic-size minor. Thus the failure concerns the imposed pair-only, vertex-covering representation.

Exhaustive enumeration gives 105 perfect matchings of the ambient \(K_8\), nine legal perfect matchings of \(G\), and zero pairwise-touching ones. This calculation checks the example; the argument above proves it.

## 5. A distinct route: discard chromatic redundancy before compression

A graph is vertex-chromatic-critical if deleting any vertex reduces its chromatic number. Every finite nonempty graph contains such an induced subgraph with the same chromatic number, by repeated deletion.

Suppose a graph \(J\) has a partition \(\mathcal P\) into connected induced bipartite subgraphs and the quotient \(Q=J/\mathcal P\) is perfect. Then

\[
\chi(J)\le2\chi(Q)=2\omega(Q)\le2h(J).
\tag{6}
\]

The first inequality uses two colours for each quotient colour. The last holds because connected disjoint bags make \(Q\) a minor of \(J\).

Requiring such a partition for **every entire graph** is false: Scott–Seymour–Wood [SSW] construct graphs where every perfect connected partition contains an arbitrarily large clique inside a part. The following observation explains why their explicit family does not settle the chromatic-critical variant.

### Proposition 3. The recursive perfect-partition obstruction is globally weakly perfect

For the explicit graphs \(A(k,r)\) constructed in Section 3, Lemma 6 of the 16 June 2017 version of [SSW],

\[
\chi(A(k,r))=\omega(A(k,r))
=\frac{2k(k^2-1)}3+1+k(r-1).
\tag{7}
\]

The notation \(A\) here merely distinguishes that source's recursive graphs from the unrelated \(G_q\) above. Formula (7) is derived from its construction, not quoted as a theorem of the source.

#### Proof

Let \(a_k=\chi(A(k,1))=\omega(A(k,1))\). The base construction is \(A(1,1)=K_1\), and its \(r\)-recursion gives \(A(1,r)=K_r\).

The \(r+1\) step attaches, to every \(k\)-clique \(C\) in \(A(k,1)\), a copy of \(A(k,r)\) complete to \(C\), with no other new edges to the core. If the chromatic and clique numbers of the copy are \(b\), the attachment has chromatic and clique number \(b+k\). Different copies can reuse colours. Thus the whole graph has both numbers \(a_k+k(r-1)\) at stage \(r\).

For the \((k,1)\) step with \(k\ge2\), the old core is \(A(k-1,2k+1)\). Each attached gadget consists of two \(K_{k+1}\)'s sharing one vertex. Every gadget vertex is joined to its own prescribed \((k-1)\)-clique of the core. Put

\[
a_k=a_{k-1}+2k(k-1).
\]

The old core has chromatic and clique number \(a_k\), by the \(r\)-formula. In an \(a_k\)-colouring of the core, each gadget vertex forbids at most \(k-1\) colours. The gadget is \(k\)-degenerate, while

\[
a_k-(k-1)\ge k+1.
\]

It therefore has a proper list-colouring from its available colours, obtained by greedy colouring in a reverse degeneracy order. Different gadgets have no edges between them, so all extend the same core colouring. A clique of order \(a_k\) remains in the old core. Hence chromatic and clique numbers are both \(a_k\).

Solving the recurrence gives

\[
a_k=1+2\sum_{j=2}^k j(j-1)
=1+\frac{2k(k^2-1)}3,
\]

and proves (7). QED.

Consequently every member of this particular obstruction family has a full-chromatic induced clique. Keeping that clique and deleting everything else removes the perfect-partition obstruction completely. This is not a claim that the source's counterexample theorem is wrong: it concerns partitions of the entire graph, for which deletion is forbidden.

### Exact remaining structural question

> Does every finite vertex-chromatic-critical graph admit a partition into connected induced bipartite subgraphs whose quotient is perfect?

An affirmative proof would establish (6) for a full-chromatic induced core of every graph, and therefore prove the universal factor-two target. This statement is an **unproved, falsifiable proposal**, not an achieved reduction of the difficult part. No argument here excludes a critical counterexample.

A critical graph has no nontrivial clique cutset. Indeed, when two pieces meet in a clique, their colourings can be aligned by permuting colours, so the chromatic number is the maximum of the two piece chromatic numbers. A proper piece would then preserve the full chromatic number, contradicting criticality. This removes a basic attachment mechanism used by [SSW], but does not classify all possible obstructions.

### Closure under the Mycielski construction

For a graph \(F\) without isolated vertices, form its Mycielski graph: retain the original vertices, add an independent shadow \(u_v\) for each \(v\), join \(u_v\) to the original neighbours of \(v\), and add a root adjacent to all shadows. Suppose \(F\) has the required bipartite/perfect partition. Retain its old bags and make the root together with all shadows one new bag. This bag is an induced star and touches every old bag. The new quotient is the cone over the old perfect quotient, hence is perfect. Thus the partition property is preserved by this construction.

This closure permits unbounded chromatic number and is not limited to fixed-order tests. It still does not generate or classify all critical graphs.

### Finite falsification tests

The code checks all 1,253 graphs in the NetworkX graph atlas, of order at most seven, with two independently implemented exact chromatic-number routines. Exactly 18 nonempty graphs in that atlas are vertex-chromatic-critical; the code finds and verifies a bipartite/perfect partition for all 18.

A stronger test asks for at most \(\lceil\chi/2\rceil\) connected bipartite bags. Such a quotient would necessarily be complete, since its chromatic number is at least \(\lceil\chi/2\rceil\). This stronger property also passed for the 18 critical atlas graphs and for 99 reproducibly generated edge-minimal critical examples, with maximum order 14 and chromatic numbers 3 through 6. The random sample includes repeated isomorphism types and is not a completeness claim. All outputs are witnesses, not evidence sufficient to establish a universal theorem.

## 6. A rejected shortcut that would merely restate exact Hadwiger

Another tempting statement is

\[
\chi(G)\le\max_{J\preceq G}\chi_f(J)
\quad\text{for every }G.
\tag{8}
\]

It might appear that (8), combined with the known fractional inequality \(\chi_f\le2h\), is an independent route to the factor-two target. In fact, (8) is equivalent to exact Hadwiger.

Hadwiger immediately implies (8), by taking a clique minor. Conversely, suppose (8). Take a minor-minimal \(k\)-chromatic graph \(J\). Every proper minor is at most \((k-1)\)-colourable. If \(J\ne K_k\), its order \(n\) exceeds \(k\), and deleting any vertex leaves a \((k-1)\)-colourable graph. Give weight \(1/(n-1)\) to each colour class in one such colouring for each deleted vertex. Every vertex is covered exactly \(n-1\) times before weighting, giving

\[
\chi_f(J)\le\frac{n(k-1)}{n-1}<k.
\]

Every proper minor also has fractional chromatic number below \(k\). Thus (8) fails for \(J\), a contradiction. Hence every minor-minimal \(k\)-chromatic graph is \(K_k\), which implies Hadwiger for all graphs.

This shortcut is therefore rejected, independently of whether the archive's announced disproof is accepted: it is not a genuinely easier missing theorem.

## 7. Remaining mathematical obligation

The proven contact certificate operates where forbidden-edge and four-cycle incidence budgets are controlled. High chromatic number does not automatically provide those budgets; the bridge example already rules out a universal pair-only completion theorem. Neither the exact release operation nor its finite tests fills this gap.

The distinct structural route is to eliminate chromatically redundant vertices, then build connected bipartite bags with a perfect quotient. Proposition 3 shows that one published obstruction family does not obstruct this normalized task. What remains is a global existence proof, or a critical counterexample, not an optimization of the scalar local-lemma constant.

Accordingly, this note preserves a rigorously specified mechanism and a concrete research obligation. It does not establish a foundational resolution or an exceptional new mathematical primitive.

## References and provenance

[LS] Linyuan Lu and László Székely, *A new asymptotic enumeration technique: the Lovász Local Lemma*, arXiv:0905.3983v4. Used for canonical-event negative dependency and the lopsided local lemma.

[HV] Nicholas Harvey and Jan Vondrák, *An Algorithmic Proof of the Lovász Local Lemma via Resampling Oracles*, arXiv:1504.02044. Prior art for the resampling-oracle framework.

[H] David G. Harris, *Oblivious resampling oracles and parallel algorithms for the Lopsided Lovász Local Lemma*, arXiv:1702.02547. Additional matching-oracle prior art.

[IS] Freddie Illingworth and Raphael Steiner, *Disproof of the dominating Hadwiger conjecture*, arXiv:2609.35361v1, 28 September 2026. Inputs: Lemma 2.1, the three conditions of Lemma 3.1, and the deterministic proof in Section 3.2. The fixed parallel class and resulting ordinary-minor completion are the modification analysed here.

[SSW] Alex Scott, Paul Seymour and David R. Wood, *Bad News for Chordal Partitions*, 16 June 2017 preprint hosted on Paul Seymour's Princeton webpage; later Journal of Graph Theory 90 (2019), 5–12. Proposition 3 here refers specifically to the Section 3, Lemma 6 recursion in that preprint.

[W] David R. Wood, *Tweaking the constant in the Linear Hadwiger Theorem*, arXiv:2610.10831v1, 7 October 2026.

[O] OpenAI mathematical manuscript archive, *A counterexample to Hadwiger's conjecture*, directory dated 23 September 2026. Read introduction at `preprints/A-counterexample-to-Hadwigers-conjecture-September-23-2026/build/sections/01-introduction.tex`, main branch fetched 13 October 2026. Claim not independently audited here.

### Reproduction

With Python and NetworkX installed, run:

```sh
python finite_checks.py
python pin_release.py
python critical_palette_checks.py
```

These generate JSON test records. The mathematical asymptotic construction is proved symbolically; the supplied programs do not construct the large Suzuki–Tits examples or check the cited external manuscripts.
