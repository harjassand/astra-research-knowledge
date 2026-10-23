# Finite-cross-Choi rank-ratio source gate

**Verdict: close exact rank-index theorems exist for local MPO/MPU tensor flattenings; the exact finite-collar Choi-marginal identity in `RANK_MATCHING_OPENING.txt` is not explicitly stated by the sources below.** Treat it as a plausible tensor-reshaping bridge, not a source-verified theorem, until the two cross-collar marginals are identified with the source's flattenings, including collar orientation and any blocking/normalization. Also align conventions: these papers define an *additive logarithmic* index; if the opening's \(\mathrm{ind}(\alpha)\) means the usual multiplicative GNVW rational \(\kappa\), then \(\kappa=2^{\mathrm{ind}_{\log}}\) and the theorem's ratio is \(\kappa^{\pm2}\). If the opening uses the logarithmic convention instead, it must use \(2^{\pm2\,\mathrm{ind}_{\log}}\), not \(\mathrm{ind}_{\log}^{\pm2}\).

## Decisive primary sources

1. Elisabeth Wagner, Ramil Nigmatullin, Alexei Gilchrist, and Gavin Brennen, “Information Flow in Non-Unitary Quantum Cellular Automata,” *SciPost Physics* **16**, 014 (2024), [arXiv:2204.09922](https://arxiv.org/abs/2204.09922), especially §2.2, Eqs. (1)–(4), Fig. 3. The paper defines left/right matrices `M_L,M_R` as the two left/right partitionings of the local MPO tensor `M`; for a **unitary 1D QCA** it states
   \[
   \mathrm{ind}=\tfrac12\log_2\frac{\operatorname{rank}M_R}{\operatorname{rank}M_L}
   =\tfrac12\bigl(S_0(\sigma_R)-S_0(\sigma_L)\bigr),\quad
   \sigma_\beta=\frac{M_\beta^\dagger M_\beta}{\operatorname{Tr}(M_\beta^\dagger M_\beta)},\quad S_0(\rho)=\log_2\operatorname{rank}\rho.
   \]
   Thus the flattening-rank ratio is exactly \(2^{2\,\mathrm{ind}}\) in their stated orientation (or its reciprocal if the two cuts are swapped). Fig. 3 identifies the virtual indices \(\alpha,\beta\) and grouped physical input/output indices. The paper notes that its equations at the furthest-right site require locality. This is an exact unitary-QCA rank theorem, not a theorem specifically about the opening's finite cross-Choi marginals.

2. J. Ignacio Cirac, David Pérez-García, Norbert Schuch, and Frank Verstraete, “Matrix Product Unitaries: Structure, Symmetries, and Topological Invariants,” arXiv:1703.09188v2 (2017), [primary full text](https://arxiv.org/html/1703.09188), §III.2 and §IV, Definition III.6, Theorem III.8, Definition IV.1. They define \(r,\ell\) as the ranks of two SVD flattenings of the local MPU tensor formed by the two different groupings of auxiliary/physical indices (§III.2); for a simple (blocked) MPU, Theorem III.8 gives \(r\ell=d^2\). Their index definition is
   \[
   \mathrm{ind}=\tfrac12(\log_2r-\log_2\ell),
   \]
   hence \(r/\ell=2^{2\,\mathrm{ind}}\). The index is independent of the chosen sufficiently large blocking (Proposition IV.2). The paper also states any finite-bond-dimension MPU is a 1D QCA and vice versa (Corollary III.11). Again, these are local tensor flattenings, not explicitly the particular reduced Choi operators \(J_A,J_B\) on the opening's finite collars.

## Exact compatibility still needed for the proposed use

The opening needs \(\operatorname{rank}(J_A)/\operatorname{rank}(J_B)=\mathrm{ind}(\alpha)^{-2}\) (up to orientation) for its specific finite range-\(r\) collars \(A=L_1'R_1\), \(B=L_1R_1'\). The primary results establish the same kind of rank ratio for the two flattenings of a local MPO/MPU tensor. They do not, in the cited statements, assert that the ranks of those flattenings equal the ranks of these two finite-collar Choi marginals. The remaining gate is a concrete vectorization/partial-trace identification showing that (i) the Choi Schmidt ranks across the stated A|B cuts equal the corresponding tensor-flattening ranks, (ii) the chosen finite collar captures all support because the QCA has strict finite range (including inverse/locality boundary conditions), and (iii) no extra rank factors arise from identity/tracial legs or a blocked-cell convention. Until that map is written and checked, the rank-ratio step in the opening is **supported by a close exact invariant but not source-verified in its exact stated Choi form**.

No claim is made here that the Rényi-2 identity from the non-unitary-QCA literature itself implies this Rényi-0 Choi statement; the rank theorem used above is specifically for unitary QCA/MPUs.
