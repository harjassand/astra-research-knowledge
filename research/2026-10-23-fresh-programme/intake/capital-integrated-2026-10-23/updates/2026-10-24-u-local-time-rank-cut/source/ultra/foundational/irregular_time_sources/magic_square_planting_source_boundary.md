# Magic-square support planted into a Feige–Verbitsky graph: source boundary

## Primary finite quantum gadget

Coudron and Natarajan, “The Parallel-Repeated Magic Square Game is Rigid,” arXiv:1609.06306v1 (2016), §3, Figures 1–2, state the exact single-round game and an all-input perfect quantum strategy (https://arxiv.org/html/1609.06306). The referee gives Alice a row $r\in\{0,1,2\}$ and Bob a column $c\in\{0,1,2\}$. Alice returns two bits $a_0,a_1$ and sets $a_2=a_0\oplus a_1$; Bob returns two bits $b_0,b_1$ and sets $b_2=1\oplus b_0\oplus b_1$. They win iff $a_c=b_r$. Thus row parity is even (sign product $+1$), and column parity is odd (sign product $-1$).

Their shared state is $|\psi\rangle=\frac12\sum_{i,j\in\{0,1\}}|ij\rangle_A|ij\rangle_B$, two EPR pairs. The displayed observable square is
\[
\begin{matrix}
ZI & IZ & ZZ\\
IX & XI & XX\\
-ZX & -XZ & YY
\end{matrix}
\]
with each Alice row a commuting triple of product $+I$ and each Bob column a commuting triple of product $-I$. The parties measure their local commuting pair for the assigned row/column and infer the third entry from parity. The common cell is perfectly correlated, so all nine question pairs win.

For any fixed $(r,c)$, each player's parity-valid answer set has four strings. The winning-answer support graph on those $4+4$ outputs is $K_{2,2}\sqcup K_{2,2}$: the answer strings split by the shared cell's sign, and equality accepts precisely within each sign class. It has 8 of 16 possible edges and maximum complete-biclique area 4, while the quantum strategy wins with probability 1. This rules out a generic inference that small complete-biclique area of a finite answer-support graph, by itself, forces quantum value below 1. It does not settle a stronger tensor-kernel norm bound or show that this support graph embeds in the BG answer-string construction.

## Exact Feige–Verbitsky/Braverman–Garg hypothesis and scope

Braverman and Garg, “Small value parallel repetition for general games,” ECCC TR14-095 revision 1 (2015), §7, Theorem 7.1 and Lemmas 7.2–7.3 (primary text: https://eccc.weizmann.ac.il/report/2014/095/revision/1/download/), use $r=k^{1/3}$ and a bipartite graph with $kr$ vertices on each side. It has at least $k^{2r}/(2k^{1/5})$ edges, while every induced subgraph on $k$ selected vertices from each side has at most $k^2/k^{1/10}$ edges. Their game samples uniform $(x,y)\in[k]\times[k]$; the answers are $(s_A,l_A),(s_B,l_B)\in([k]^r\times[r])^2$, and acceptance requires
\[
l_A=l_B,\quad s_A(l_A)=x,\quad s_B(l_B)=y,\quad (s_A,s_B)\in E(G).
\]
The graph conditions support their **classical** value/repetition analysis: deterministic strategies induce a $k\times k$ win graph, and connected components are bounded using the induced-subgraph edge condition. The paper's theorem is not an entangled/commuting-value upper bound and does not preclude quantum-perfect correlations on a planted finite subkernel.

## Closest comparators found; remaining boundary

The Coudron–Natarajan paper also proves rigidity of parallel repetitions of this particular game: if an $n$-round strategy wins with probability $1-\varepsilon$, its state and measurements are close to the ideal $2n$-EPR strategy under a local isometry (abstract and §3–4). This is game-specific and starts from near-perfect repeated value; it supplies no generic bridge from BG-style rectangle sparsity to an entangled value bound or planting theorem.

A nearby classical-analysis precedent is Buhrman, Regev, Scarpa, and de Wolf, “Near-Optimal and Explicit Bell Inequality Violations,” *Theory of Computing* 8 (2012), 623–645, https://theoryofcomputing.org/articles/v008a027/ . They give a different Hidden-Matching nonlocal game with quantum value 1 and classical value $1/2+O((\log n)/\sqrt n)$; its classical upper bound is analyzed via the KKL inequality/Boolean Fourier analysis (see their §1.1 and Theorem 3.3). Its question law and predicate are specialized; it is not a support-graph biclique-area theorem and does not cover the BG graph family.

Within this bounded primary-source check, I found no result giving an entangled/commuting upper bound from the BG induced-$k\times k$ edge condition alone, nor a prior theorem for quantum-perfect planting of a magic-square kernel into the BG answer strings. This is a search-scope report, not a priority or novelty claim. The source-backed boundary is that finite answer-support biclique sparsity can coexist with perfect quantum value; whether the proposed random-background construction preserves the desired biclique and tensor-kernel estimates is a separate proof obligation.
