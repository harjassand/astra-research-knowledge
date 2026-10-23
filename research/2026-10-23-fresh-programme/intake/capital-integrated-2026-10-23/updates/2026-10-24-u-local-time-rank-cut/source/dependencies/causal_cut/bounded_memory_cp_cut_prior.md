# Bounded-memory repetition: exact CP-cut comparator and prior boundary

## Scope of this source check

A targeted primary-source check did not identify a theorem directly giving parallel repetition for the following restricted model: Alice processes local inputs sequentially, carries only a $D$-dimensional quantum memory between rounds, may start with arbitrary cross-round/shared resources, and Bob may make an arbitrary joint measurement on his full input string. This is a bounded search result, not an absence or novelty claim. The exact channel-order calculation below is self-contained from Choi's finite-dimensional CP criterion and supplies a circuit-cut comparator; it does not itself prove the later event-filter or repetition argument.

## Exact positive channel-order bound

Let
\[
\mathcal D_D(X)=\operatorname{Tr}(X) I_D/D
\]
be the completely depolarizing channel on $M_D$. Use the unnormalized Choi convention $J(\Phi)=\sum_{ij}|i\rangle\langle j|\otimes\Phi(|i\rangle\langle j|)$. Then
\[
J(\mathrm{id}_D)=|\Omega\rangle\langle\Omega|,\qquad
J(\mathcal D_D)=I_{D^2}/D,
\quad |\Omega\rangle=\sum_i|ii\rangle.
\]
Since $\lVert\Omega\rVert^2=D$, $|\Omega\rangle\langle\Omega|\preceq D I_{D^2}$. Consequently
\[
J(D^2\mathcal D_D-\mathrm{id}_D)=D I_{D^2}-|\Omega\rangle\langle\Omega|\succeq0.
\]
By Choi's criterion, the difference map is completely positive, i.e. $\mathrm{id}_D\le_{\rm CP}D^2\mathcal D_D$. This order is stable under tensoring with any identity/reference system and under composition with completely positive maps. Tensoring $r$ cuts gives $\mathrm{id}^{\otimes r}\le_{\rm CP}D^{2r}\mathcal D_D^{\otimes r}$. Thus arbitrary correlations with other systems do not require a product-state assumption for this local CP-order step.

For the sequential-memory application, the factor $D^2$ is per cut $D$-dimensional incoming memory wire. A product of these bounds can dominate any positive downstream instrument/acceptance effect. The cut must include all persistent Alice-side information that can affect later outputs, including classical history if it is retained and consulted; otherwise its dimension/cardinality must also enter the accounting. An uncut auxiliary memory or side channel invalidates the bound. This comparison alone does not establish any derived coarse-steering estimate, binary-filter lift, or repetition exponent.

**Primary criterion:** M.-D. Choi, “Completely positive linear maps on complex matrices,” *Linear Algebra and its Applications* 10(3) (1975), 285–290, https://doi.org/10.1016/0024-3795(75)90075-0. Choi's finite-matrix criterion characterizes complete positivity through positivity of the Choi matrix; the $D^2$ inequality above is a direct application, not a claim that the paper states this particular depolarizing bound.

## Closest circuit-cutting result and distinction

Lowe et al., “Fast quantum circuit cutting with randomized measurements,” *Quantum* 7, 934 (2023), arXiv:2207.14734v2, https://arxiv.org/abs/2207.14734 (full source: https://arxiv.org/html/2207.14734v2), §2, Lemma 2.1 and Theorem 2.2, give the exact identity
\[
\mathrm{id}=(2d+1)\mathbb E_z[(-1)^z\Psi_z],\qquad
\Pr(z=1)=d/(2d+1),\quad \Psi_1=\mathcal D_d,
\]
where \(\Psi_0\) is a randomized measure-and-prepare channel. Their proof uses this signed quasiprobability identity for unbiased observable estimation; Theorem 2.2 gives $O(4^k(m+k^2)/\varepsilon^2)$ runtime for their circuit bipartitioning task when the overlap is at most $k$ wires. Their multiple-cut construction multiplies signed coefficients.

This is close in dimension scaling and wire-cut interpretation, but it is not the same positive domination: the minus sign is essential in their identity, while $\mathrm{id}\le_{\rm CP}d^2\mathcal D_d$ is a one-sided CP order statement. Their theorem concerns circuit simulation/estimation and does not supply a bounded-memory nonlocal-game repetition theorem or the later payoff/event selection step.
