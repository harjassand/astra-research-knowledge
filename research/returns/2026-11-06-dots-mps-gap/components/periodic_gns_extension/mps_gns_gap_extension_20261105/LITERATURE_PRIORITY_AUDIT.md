# Literature-priority audit: periodic versus GNS gap

Audit date: 2026-11-05. Target: `PROOF.md` in this directory. This is a targeted primary-literature audit, not proof verification or a certification of novelty. It was added after the initial package and is now included in the rebuilt checksum manifest and archive. Packaging edits update this status, correct the first author of the Rozman paper to Milán Ádám Rozmán as confirmed by that primary source, and add the established embedding/block-variational prior from the earlier independent audit. The priority conclusion and FNW access limitation are unchanged.

## Finding

I did not locate an existing theorem giving the full equality

    lim_N gap(H_N^PBC) = gap(H_omega)

under precisely the proper primitive injective-MPS-parent assumptions in `PROOF.md`, nor the proposed one-sided estimate

    gap(H_omega) <= gap(H_N^PBC) + O(log N / N).

The strongest exact general reference located supplies the opposite inequality, including the limsup and the GNS-core justification. Consequently, the proof's reverse inequality is not a direct consequence of the standard finite-volume-to-GNS theorem cited below. This does not establish that it is new: original sources, equivalent formulations, and expert knowledge can contain a result a targeted search misses.

The defensible present status is: **no matching full theorem located; novelty unresolved; standard easy direction explicitly identified.**

## 1. Exact reference for the standard direction

Bruno Nachtergaele, Robert Sims, Amanda Young, *Quasi-Locality Bounds for Quantum Lattice Systems. Part II. Perturbations of Frustration-Free Spin Models with Gapped Ground States*, Annales Henri Poincare 23 (2022), 393–511.

- Primary full text: https://arxiv.org/html/2010.15337
- Version inspected: arXiv:2010.15337v3.
- Published article: https://doi.org/10.1007/s00023-021-01086-5
- Exact result: **Theorem 7.4, especially equations (7.26)–(7.29)**.

Its hypotheses are convergence of finite-volume commutator derivations on local observables; shrinking low-energy windows; a positive limsup lower gap outside the windows; and local indistinguishability expressed by nonzero projections Q_n <= P_n with norm(P_n A Q_n - omega(A) Q_n) tending to zero. Equation (7.29) gives the GNS variational gap inequality with coefficient limsup gamma_n. Section 7.2 supplies the local-vector core for the GNS Hamiltonian. Corollary 7.5 applies this to stability models.

**Application to this candidate (my deduction):** take H_n to be large centered periodic rings, epsilon_n=0, gamma_n=Delta_n, and P_n=Q_n the rank-one periodic MPS ground projection. Fixed local expectations converge to omega, and the periodic seams eventually lie outside any fixed observable. Thus the theorem gives

    limsup_N Delta_N <= Delta_GNS.

No estimate of Delta_GNS from above by Delta_N, no convergence of the Delta_N sequence, and no O(log N/N) reverse error is asserted in this theorem. Its Appendix B, including Theorem B.2, also provides standard MPS local-indistinguishability input, not equality of the two gaps. Equations (B.14)-(B.15) specifically give the Gram-conditioning estimate used by the present proof, attributing it to FNW Lemma 5.2.

## 2. Earlier general spectral-exclusion statement is also one-way

Sven Bachmann, Wojciech Dybalski, Pieter Naaijkens, *Lieb-Robinson bounds, Arveson spectrum and Haag-Ruelle scattering theory for gapped quantum spin systems*.

- Primary full text: https://arxiv.org/html/1412.2970
- Version inspected: arXiv:1412.2970v2 (2015).
- Exact result: **Proposition 5.4**.

If an interval around E is uniformly absent from all sufficiently large finite-volume spectra after subtracting their ground energies, then E is absent from the GNS spectrum of a weak-* limiting ground state. This is spectral exclusion, not recovery of every limiting finite-volume excitation in the selected GNS sector. It does not prove the reverse inequality needed here. Equality of finite-volume and infinite-volume dynamics on fixed observables does not change that distinction.

## 3. Later standard parent-gap theorems located give positivity, not exact equality

Bruno Nachtergaele, *The spectral gap for some spin chains with discrete symmetry breaking*, Communications in Mathematical Physics 175 (1996), 565–606.

- Primary full text: https://arxiv.org/html/cond-mat/9410110
- Exact result: **Proposition 12 (proof of Theorem 2), equation (6.10)** and its concluding proof.

For the stated GVBS-parent class it establishes a common positive lower bound for open-interval gaps and carries that lower bound to the GNS Hamiltonian in every relevant pure infinite-volume state. Section 2 and equation (3.16) explicitly describe this same one-way passage. It does not identify the exact periodic finite-volume limit with the exact GNS gap.

Oleg Szehr and Michael M. Wolf, *Perturbation Theory for Parent Hamiltonians of Matrix Product States*.

- Primary full text: https://arxiv.org/html/1402.4175
- Version inspected: arXiv:1402.4175v2 (2015).
- Exact results: **Theorem 2**, **Corollary 3**, importing the conclusions of **Theorem 1**.

The theorem concerns periodic canonical parents of tensors obeying the eventual full-matrix-span condition (G1), with interaction length larger than the injectivity threshold; the corollary allows locally comparable interactions such as AKLT. It proves stability of a uniform finite-volume gap, ground-state thermodynamic convergence, and clustering. These conclusions do not state equality of exact GNS and periodic gaps.

Mark Fannes, Bruno Nachtergaele, Reinhard F. Werner, *Finitely correlated states on quantum spin chains*, Communications in Mathematical Physics 144 (1992), 443–490.

- Primary bibliographic source: https://doi.org/10.1007/BF02099178
- Archival source: https://projecteuclid.org/journals/communications-in-mathematical-physics/volume-144/issue-3/Finitely-correlated-states-on-quantum-spin-chains/cmp/1104249404.full

The abstract establishes the original generalized-VBS gap result. **Access limitation:** the original full article was not successfully inspected in this pass: Springer supplied a preview and Project Euclid presented a security-check page. I therefore do not certify that this original article contains no equivalent statement. The later full-text results above explicitly formulate the standard implication as a lower bound, not the desired equality.

## 4. A nearby excitation-localization theorem needs extra hypotheses

Jutho Haegeman, Spyridon Michalakis, Bruno Nachtergaele, Tobias J. Osborne, Norbert Schuch, Frank Verstraete, *Elementary excitations in gapped quantum spin systems*, Physical Review Letters 111, 080401 (2013).

- Primary full text: https://arxiv.org/html/1305.2176
- Published article: https://doi.org/10.1103/PhysRevLett.111.080401
- Version inspected: arXiv:1305.2176v2.
- Exact result: **Theorem 1**, equations (2)–(4).

It approximates a periodic momentum eigenstate by the momentum superposition of a local operator acting on the ground state. Crucially it assumes an eigenvalue isolated from the rest of its momentum sector by a volume-independent separation and a local operator with nonvanishing volume-independent spectral weight. These assumptions are not included in the present proper-parent hypothesis. A first-gap sequence need not have an isolated nondegenerate band or the required local spectral weight. Thus this theorem does not by itself supply the candidate's unrestricted reverse inequality.

### Established embedding and stronger block-variational prior

Packaging cross-reference to the earlier independent source audit: page 4 of Haegeman et al., arXiv:1305.2176, explicitly uses injectivity to turn local-operator minimization into an interval Hamiltonian with two added boundary sites and terms. Thus bounded local preparation/finite-boundary embedding is established prior, not by itself a new capability of the candidate.

Haegeman, Osborne and Verstraete, *Post-Matrix Product State Methods: To tangent space and beyond*, Physical Review B 88, 075133 (2013), Section VII A, equation (96), and Table I, p. 075133-28, optimize a K-site replacement tensor with a momentum superposition. Their AKLT p=pi estimates are 10/27 for K=1, 0.350634581086138 for K=2, and 0.350124157337687 for K=12. These printed decimal values are not interval-certified rounding bounds. They are substantially stronger practical estimates than the candidate's approximately 0.432 small-construction test.

- Primary: https://arxiv.org/abs/1305.1894
- Published: https://doi.org/10.1103/PhysRevB.88.075133

The possible distinction is the complete comparison of the first periodic gap with the GNS gap without assuming an isolated momentum band or uniform local spectral weight. No priority is claimed for the individual embedding or variational ingredients.

## 5. Current tensor-network gap-bound literature does not close this gap

Milán Ádám Rozmán, András Molnár, Norbert Schuch, *Lower Bounds on Spectral Gaps of Parent Hamiltonians via Tensor Networks* (2026).

- Primary full text: https://arxiv.org/html/2607.19078v1
- Exact locations: **Section 3.2**, **Theorem 6**, and **Section 4.4, “Convergence to infinite system value.”**

The proper-parent condition is eventual equality of open kernels with the MPS boundary spaces. The paper proves uniform gap existence for open and periodic chains. Its explicit convergence statement for the lower bounds is to limsup of the **open-chain** gaps, not to the GNS gap or the periodic-gap limit. The article has no GNS theorem located. Wording such as “infinite system value” should not be used to substitute a stronger boundary-independent statement for the formula actually proved.

## 6. Boundary-condition pitfall and exact remaining claim

It is false that the open and periodic exact gaps must agree even for proper primitive injective parents. For the product MPS with local h=I-|00><00|, the open gap is 1 and the periodic gap is 2 for N>=3. The infinite product-state GNS gap is also 2: every nonempty finite spin-flip configuration costs at least two violated bonds. This direct example explains why open-gap convergence does not settle the candidate. It does not contradict periodic/GNS equality.

The potential added result in `PROOF.md` is specifically the construction transferring *arbitrary low-energy periodic eigenvectors* into the infinite MPS GNS sector with vanishing energy loss. The support-uniform marginal estimate, bounded preparation after projecting a quiet buffer, and positive seam estimate are what the standard fixed-support limiting theorem does not provide. A rigorous independent proof audit is separate from priority; the literature search alone validates neither these steps nor the claimed rate.

Recommended manuscript language: “We give a direct proof of periodic-gap convergence to the GNS gap under the stated proper primitive MPS-parent assumptions. The standard inequality limsup Delta_N <= Delta_GNS follows from Nachtergaele–Sims–Young, Theorem 7.4. We have not established priority for the reverse inequality or the quantitative bound.”
