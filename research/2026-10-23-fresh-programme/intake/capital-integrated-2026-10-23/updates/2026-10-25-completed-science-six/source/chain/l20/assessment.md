# L20 — A Chern-number route beyond the alpha headline

## Selection

I selected the condensed-matter/topology thread (Part XIV, especially Theorem 225.1 and instrument I.51), rather than another route to the fine-structure constant. This has the highest upside among the non-alpha chapters because an actual identification of the chain construction with a band Chern number would connect it to a quantized transport observable. The live obstruction is decisive at this draft: the compendium itself labels the Chern-number derivation “awaited,” calls the Hall integer a name beside the construction, and says the finite winding carries those names by correspondence (printed pp. 739–740). The band result is also explicitly flat and has “no value and no material constant” (pp. 558–560).

The draft's own closest predecessor is the TKNN result it cites as reference [254]: the Hall conductance quantization is tied to a two-dimensional periodic system with a Fermi gap. The [original APS paper](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.49.405) is the exact physical target. The [Qi–Wu–Zhang two-dimensional model](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.74.085308) supplies a compact primary benchmark for a nonzero band invariant.

## Exact obstruction: one loop does not determine a Chern number

Here is an explicit pair of two-band Bloch Hamiltonians on the Brillouin torus. Let \(\sigma_x,\sigma_y,\sigma_z\) be Pauli matrices and \((k_x,k_y)\in T^2\):

\[
H_1(k_x,k_y)=\sin k_x\,\sigma_x+\sin k_y\,\sigma_y+(-1+\cos k_x+\cos k_y)\,\sigma_z,
\]
\[
H_0(k_x,k_y)=\sin k_x\,\sigma_x+\cos k_x\,\sigma_z.
\]

Both have an exact gap of at least 2. For \(H_0\), \(|d|^2=\sin^2 k_x+\cos^2 k_x=1\). For \(H_1\), writing \(x=\cos k_x\), \(y=\cos k_y\),

\[
|d|^2=\sin^2 k_x+\sin^2 k_y+(-1+x+y)^2=1+2(1-x)(1-y)\ge 1.
\]

At the entire slice \(k_y=0\), the two Hamiltonians agree pointwise:

\[
H_1(k_x,0)=H_0(k_x).
\]

Thus their lower-band eigenstates and Berry/Wilson holonomies around this \(k_x\)-cycle agree exactly. The common loop is \(H=\sin k_x\,\sigma_x+\cos k_x\,\sigma_z\): its eigenvector changes sign after one turn, so the holonomy is \(-1\), or Berry phase \(\pi\) modulo \(2\pi\).

The two-dimensional invariants differ. For \(H_0\), the projector is independent of \(k_y\), so its Berry curvature has \(F_{xy}=0\) everywhere and \(C=0\). For \(H_1=d\cdot\sigma\), the normalized vector \(n=d/|d|:T^2\to S^2\) has degree of magnitude one: the north pole has exactly one preimage, \((0,0)\), and the local Jacobian there is nonzero with positive orientation. The occupied-band Chern number is therefore \(|C|=1\) (the sign depends on band and Berry-curvature conventions). The exact shared one-cycle holonomy is compatible with either \(C=0\) or \(|C|=1\).

This is the live obstruction for Theorem I.51.2–I.51.3: a finite product of register-letter transport around one graph cycle can be a well-defined holonomy/winding, but it cannot determine the first Chern number without a two-parameter family of occupied subspaces and its curvature. The finite counts and the parity of stable configurations do not supply that missing \(T^2\)-family. This is an underdetermination result, not a claim that no extension can be built.

## Relative no-go theorem for any finite graph data

The same obstruction holds for an arbitrary finite embedded graph, not just for the one-loop example. Let \(\Gamma\subset T^2\) be a finite embedded 1-skeleton and let a disk \(D_R\) have closure disjoint from \(\Gamma\). Suppose any smooth, gapped two-band model realizing the proposed graph data exists. After spectral flattening it is \(H_0(k)=n_0(k)\cdot\sigma\), with \(|n_0|=1\), and its lower-band projector is \(P_0=(I-n_0\cdot\sigma)/2\).

First flatten \(n_0\) on a smaller disk without touching \(\Gamma\): in polar coordinates on \(D_R\), choose a smooth radial map \(\rho:[0,R]\to[0,R]\) which is 0 for \(r\le R/3\) and equals \(r\) in a collar of \(R\). The map \(\Phi(re^{i\phi})=\rho(r)e^{i\phi}\), extended as the identity outside \(D_R\), is smooth and homotopic to the identity relative to the outer collar. Thus \(\tilde n_0=n_0\circ\Phi\) has the same degree and exactly the same values near \(\Gamma\), while it is constant, say \(q\in S^2\), on \(r\le R/3\).

Here is a smooth bubble of degree magnitude one when \(|\ell|=1\), with its sign made explicit. For an integer \(\ell\ne0\), set \(m=|\ell|\), choose a smooth radial cutoff \(\chi\) equal to 1 for \(r\le R/9\) and 0 for \(r\ge 2R/9\), and put \(a(r)=\chi(r)r^{-m}\). On \(r>0\), define

\[
s_\ell(r,\phi)=\left(\frac{2a(r)\cos(\ell\phi)}{1+a(r)^2},\frac{2a(r)\sin(\ell\phi)}{1+a(r)^2},\frac{1-a(r)^2}{1+a(r)^2}\right).
\]

It is the north pole \((0,0,1)\) for \(r\ge2R/9\). Near the center it has the nonsingular form

\[
(s_x+i s_y)=\frac{2r^m e^{i\ell\phi}}{1+r^{2m}},\qquad s_z=\frac{r^{2m}-1}{r^{2m}+1}.
\]

Since \(r^m e^{i\ell\phi}=(x+i\operatorname{sgn}(\ell)y)^m\), these components are smooth Cartesian functions at \(r=0\); the cutoff is flat where it reaches zero, so they are smooth across the constant collar too. The vector has unit norm everywhere. Equivalently \(s_\ell=(\sin f\cos(\ell\phi),\sin f\sin(\ell\phi),\cos f)\) with \(f(r)=2\arctan a(r)\), extended by \(f(0)=\pi\); hence \(f(0)=\pi\), \(f(R)=0\).

With the standard orientation \(dx\wedge dy\), its degree is

\[
\deg(s_\ell)=\frac{1}{4\pi}\int_0^R\!\int_0^{2\pi}
s_\ell\cdot(\partial_r s_\ell\times\partial_\phi s_\ell)\,d\phi\,dr
=\frac{\ell}{2}\int_0^R f'(r)\sin f(r)\,dr
=\frac{\ell}{2}[-\cos f]_0^R=-\ell.
\]

For the lower band and Berry convention \(A=i\langle u_-|du_-\rangle\), \(F=i\operatorname{tr}(P_-\,dP_-\wedge dP_-)=\tfrac12 n\cdot(\partial_x n\times\partial_y n)\,dx\wedge dy\), so \(C_-=(2\pi)^{-1}\int F=\deg(n)\). To shift the Chern number by any prescribed \(j\in\mathbb Z\), use \(\ell=-j\) (for \(j=0\), insert the constant map). Choose a constant rotation \(R_q\in SO(3)\) taking the north pole to \(q\), replace \(\tilde n_0\) on the disk \(r\le R/3\) by \(R_qs_{-j}\), and leave it unchanged outside. The bubble is identically \(q\) for \(r\ge2R/9\), so the glued map is smooth. It changes the degree by exactly \(j\) and leaves \(n_0\) unchanged on an open neighborhood of \(\Gamma\).

In particular, from the constant base map take \(n_k=s_{-k}\) on \(D_R\) and \(n_k=(0,0,1)\) outside it. Then \(H_k=n_k\cdot\sigma\) equals \(\sigma_z\) on an open neighborhood of \(\Gamma\) and everywhere outside \(D_R\), has eigenvalues exactly \(\pm1\), and has lower-band Chern number \(k\). All graph-cycle Hamiltonians, projectors, and Berry holonomies are identical for every \(k\in\mathbb Z\), including the constant \(k=0\) case.

Therefore \(H_j=\tilde n_j\cdot\sigma\) has eigenvalues exactly \(\pm1\) and the same gap, projectors, and all Berry holonomies evaluated on graph cycles as the original model, but \(C_-(H_j)=C_-(H_0)+j\). If no smooth gapped extension of the graph data exists, there is no Chern prediction to begin with; if one exists, there are extensions with every integer Chern number and identical graph-restricted data. This proves that finite graph-loop data alone cannot determine the Hall/Chern integer. A rule fixing how the model is extended over the two-dimensional faces would be additional structure and a separate theorem obligation.

## What would make this a real theorem

The useful next target is to construct from a chain unit cell a gapped Bloch Hamiltonian or occupied projector \(P(k_x,k_y)\), explain what the two independent periodic variables mean in the chain, and prove that its Chern integer equals a specified chain invariant. A valid chain-to-TKNN theorem must state the gap condition, the Berry connection/curvature (or an equivalent gauge-invariant lattice formula), and the observable to which the integer couples. It must also survive the allowed chain moves and re-matchings. Those definitions are absent here; adding them would be new model structure and must be identified as such.

The present result is therefore not an original Chern insulator, a derivation of the TKNN formula, a quantized Hall-conductance prediction, or evidence of a material phase. Its value is a precise repair target and a no-go witness for the current one-cycle identification. If the chain network can supply the missing gapped two-parameter family without importing a conventional tight-binding model by hand, that would be the novel result worth pursuing.

## Reproducibility artifact

The exact proof above is analytic. [The companion script](chern_loop_underdetermination.py) computes the minimum direct gap, the fixed-slice Berry phase, and a Fukui–Hatsugai–Suzuki lattice Chern estimate for both models. On an 81×81 periodic grid it reports the same \(+\pi\) slice phase, direct gaps 2, and Chern estimates \(-1\) and 0 under the script's orientation convention. The numerical sign is convention-dependent; the nonzero-versus-zero distinction is not.

## Scope and source notes

- Local source: `work/sources/ChainTheoryCompendium.pdf`, printed pp. 554–560 and 738–740. The relevant instrument says “The Chern number” is awaited, while its winding results cite the Hall integer by name.
- Exact primary predecessor: Thouless, Kohmoto, Nightingale & den Nijs, “Quantized Hall Conductance in a Two-Dimensional Periodic Potential,” *PRL* 49, 405 (1982), [APS DOI page](https://doi.org/10.1103/PhysRevLett.49.405). It is also compendium reference [254].
- Benchmark model: Qi, Wu & Zhang, “Topological quantization of the spin Hall effect in two-dimensional paramagnetic semiconductors,” *PRB* 74, 085308 (2006), [APS DOI page](https://doi.org/10.1103/PhysRevB.74.085308).
- Provenance: the requested [publications landing page](https://alexwg.org/publications/) was opened during this audit; its visible publications list did not expose the supplied Chain Theory working draft. The assessment therefore treats the task-supplied local PDF as the draft under review.
