# Source scope and prior art

## The original Rai formulation

Kshiti Sneh Rai, Ilya Kull, Patrick Emonts, Jordi Tura, Norbert Schuch and Flavio Baccari, *A Hierarchy of Spectral Gap Certificates for Frustration-Free Spin Systems*, Quantum 10, 2065 (2026).

- Version inspected: arXiv:2411.03680v3, dated 1 April 2026.
- Primary text: https://arxiv.org/html/2411.03680v3
- Exact displayed dual: https://arxiv.org/html/2411.03680v3#S2.E17
- Published DOI: https://doi.org/10.22331/q-2026-04-13-2065

Section 2 defines a finite-dimensional, translation-invariant, geometrically local, frustration-free chain, with local terms shifted to be positive and the ground energy shifted to zero. It states: “Further, we consider periodic boundary condition in H, which means that the site indices are taken modulo N.” It then states: “The spectral gap is then the lowest non-zero eigenvalue of H and we denote it by Δ_N.” No uniqueness assumption is imposed in that setup.

The original displayed Eq. (17), specialized exactly as printed for nearest-neighbor terms, is

    delta_LTI(n) = min_(rho_n) Tr[rho_n (h_1^2
                           + sum_(j=2)^(n-1) {h_1,h_j})],
    rho_n >= 0,
    Tr_1(rho_n) = Tr_n(rho_n),
    Tr(rho_n h_1) = 1.

There is no trace-one constraint. The matching primal is Eqs. (11)-(12), with the arbitrary Hermitian (n-1)-site coboundary I tensor Y - Y tensor I. The Ising argument in this packet applies directly to that complete program, rather than a reduced set of marginals or a restricted ansatz for Y.

Section 2.3 explicitly cautions that replacing H-squared by its finite-distance truncation can change the minimizer, so its local-excitation intuition does not establish exact convergence. Section 3.2 distinguishes the periodic gap Delta from the open-chain gap epsilon. Section 5 states that the hierarchy's completeness was not resolved and separately asks whether it eventually detects a positive gap and whether its certified value converges to the true gap.

The counterexample answers only the second question negatively in the unrestricted class. The hierarchy's finite-level lower bounds remain valid, and its positive-gap detection question is not answered by these examples. The open Ising gap is 1, but substituting it for the paper's stated periodic gap would change the target.

The toric construction uses the rectangular analogue expressly defined in PROOF.md, not a claim that Eq. (17) itself was a two-dimensional formula. It establishes the same truncation obstruction in that natural full-LTI analogue.

## Primary source provenance

The checks above used the cached HTML and its text extraction from the inspected primary version. Their SHA-256 hashes were:

    HTML: 3857c63bbfe0a89d79d7bf224d1ce37c3027941953f499d3dd5a9af3f0246984
    Text: 502acb9b5bbc4384d372c62cee9640d095957db4e78d016989ea7e32ca00808e

These full source files are not needed by the scripts and are not bundled. The immutable version URL, exact equation anchor, section locators, and restated mathematical program above identify the source used. Formatting-only HTML changes may alter a future download's hash without altering the equation. The quote wording above is retained; math markup is rendered as ordinary symbols.

## Standard physical facts and normalization

1. A. Yu. Kitaev, *Fault-tolerant quantum computation by anyons*, https://arxiv.org/abs/quant-ph/9707021 . The toric-code stabilizers, paired excitations on a torus, and topological ground degeneracy are standard prior results, not discoveries claimed here.

2. P. Naaijkens, *Localized endomorphisms in Kitaev's toric code on the plane*, Rev. Math. Phys. 23 (2011), 347-373, https://arxiv.org/html/1012.3857v2 . Proposition 2.2 supplies the vacuum-GNS lower gap 4 in the -sum A-sum B convention. A single-edge Pauli creates two defects and attains that bound. For h=(I-A)/2+(I-B)/2, excitation energies are half as large, so the vacuum gap is 2. Section 3 treats charged sectors; these must not be confused with finite local excitations of the chosen vacuum.

3. B. Nachtergaele, R. Sims and A. Young, *Quasi-Locality Bounds for Quantum Lattice Systems. Part II. Perturbations of Frustration-Free Spin Models with Gapped Ground States*, Ann. Henri Poincare 23 (2022), 393-511, https://doi.org/10.1007/s00023-021-01086-5 . Later discussion of non-frustration-free toric-code algebraic ground states motivates avoiding a blanket assertion of uniqueness among all algebraic ground states. This packet only uses the specified frustration-free vacuum representation.

The Ising domain-wall parity calculation is elementary and standard. The toric model is topological/MPO-injective, not an injective-PEPS counterexample. The 1D Ising model has multiple product vacua, not a primitive proper-MPS parent. The restrictive positive results mentioned in the audit reports are therefore outside the counterexamples' scope.

## What the literature search does not establish

The audits performed targeted searches combining LTI or locally translationally invariant, spectral-gap hierarchy, H-squared truncation, Ising or toric code, and counterexample. They did not locate an explicit published statement of this exact all-level plateau. This limited negative search result is not evidence of priority, novelty, or publishability; the calculation may be known, implicit, or unpublished.

The first audit also distinguishes S. Rao, *A convergent hierarchy of spectral gap certificates for qubit Hamiltonians*, arXiv:2510.08427, https://arxiv.org/abs/2510.08427 . That is a different finite-system hierarchy and is not contradicted by a thermodynamic finite-cutoff LTI obstruction. No claim is made about all other gap-certification methods.

No external author contact, external peer review, or publication was undertaken. The included audits are independent internal algebraic and computational checks. The mathematical claim rests on explicit matching feasible witnesses, not on review status or an absence of search results.
