# Energy-moment-only gap SDP: prior-art screen

Date: 2026-11-05. This is a targeted literature screen, not an originality guarantee or independent validation of the proposed completeness proof.

## Finding

No primary source located states exactly the proposed energy-moment-only translation-invariance hierarchy and proves its convergence to the periodic thermodynamic gap. There is substantial close prior art: scalar quadratic-in-local-energy SDP certificates appear explicitly in Cruz et al. (2022), and the proposed hierarchy is a restricted ansatz inside Rai et al. (2026), with Knabe and apparently Gosset–Mozgunov certificates already included. The defensible possible contribution is a completeness theorem for a specific much smaller coefficient space, plus any experimentally demonstrated solver advantage. It is not the first quadratic-energy SDP or the first optimized finite-size gap certificate.

## 1. Closest older scalar SDP: Cruz et al.

Esther Cruz, Flavio Baccari, Jordi Tura, Norbert Schuch, J. Ignacio Cirac, *Preparation and verification of tensor network states*, Physical Review Research 4, 023161 (2022), arXiv:2105.06866v2.

Primary source: https://arxiv.org/html/2105.06866v2#S3.SS1 ; translation symmetrization: https://arxiv.org/html/2105.06866v2#A3 .

Section III.1 Eq. (12) maximizes x over real scalar coefficients a_ij and c_ij, subject to

    {h_i,h_j} + a_ij h_i^2 + a_ji h_j^2 - c_ij h_i - c_ji h_j >= 0,
    sum_(j != i) a_ij = 1,
    sum_(j != i) c_ij = x.

Summing yields H^2 >= xH. For disjoint supports they set coefficients to zero and discard automatically positive anticommutators. Appendix C symmetrizes a,c for translation-invariant periodic systems and obtains system-size-independent bounds.

Most important for novelty: the paragraph after Eq. (15) explicitly proposes relaxing pairwise positivity to positivity only after summing selected groups of terms, and gives blocking adjacent h_i into sums as a natural construction. Thus grouping quadratic energy terms and optimizing scalar redistributions is already a published strategy. Their stated SDP does not explicitly allow every arbitrary displacement-preserving redistribution of pair coefficients in the proposed reduced n-site q. Do not claim exact equivalence at all n without an additional argument. For nearest-neighbor n=3 the symmetrized pairwise constraint is exactly the reduced ansatz: one anticommutator, coefficients on h_1^2,h_2^2 summing to one, and coefficients on h_1,h_2 summing to minus delta.

No exact-gap hierarchy completeness statement was found here.

## 2. Rai hierarchy: exact containment and strongest direct benchmark

K. S. Rai et al., *A Hierarchy of Spectral Gap Certificates for Frustration-Free Spin Systems*, Quantum 10, 2065 (2026), arXiv:2411.03680v3.

Primary sources: https://arxiv.org/html/2411.03680v3 ; https://quantum-journal.org/papers/q-2026-04-13-2065/ .

The full primal searches q=g_n(delta)+I tensor Y-Y tensor I >=0 with arbitrary Hermitian Y. Restricting Y to span{h_i,h_i^2,{h_i,h_j}} is precisely dual to retaining only adjacent-translation equalities for those energy observables. It is a restriction of the published optimization, not a new global positivity principle.

Appendix B.1 explicitly constructs a Knabe q solely from h_i and anticommutators. Its coefficients have the requisite displacement sums, so it is feasible in the proposed reduced ansatz. Appendix B.2 Eqs. (90)-(93) proves the GM auxiliary inequality using positivity, ground-space projection, the local open gap, and equality only of the first energy moments Tr(rho h_i). Together with the quadratic expression Eq. (85), this strongly supports GM inclusion in the reduced hierarchy too. The latter is an inference from their proof, not an explicit reduced-hierarchy statement by the authors.

Appendix D replaces Y by P_(n-1)^perp Y P_(n-1)^perp so q annihilates the exact open-chain ground space and numerical certificates can be repaired. Every reduced-Y basis term already annihilates that ground space on both sides. Therefore reduced <= certifiable projected-Y <= unrestricted LTI at each level. Conditional completeness of the reduced hierarchy implies completeness of the projected-Y variant by squeezing when indexing conventions match. The separately checked extension is now documented in PROJECTED_VARIANT_EXTENSION.md, including the source's literal one-level shift; no same-level equality across different printed conventions is asserted. The second and third proof auditors did not separately review this extension.

Section 5 explicitly leaves both positive-gap detection completeness and convergence to the true gap unresolved. The authors use MOSEK, with quoted solver precision about 1e-8, and stress that naive approximate PSD can falsely certify a gap without their correction. The strongest directly relevant published benchmark located is AKLT delta >=0.34976 at n=6 (729-dimensional physical PSD block), compared to periodic n=12 gap approximately 0.35012. Other tests are deformed Z3 clock models and Glauber dynamics; n=5 beats Knabe/GM n=10 over the tested deformed-clock parameter region. These results are for their full/projected LTI computation, not the proposed small coefficient space.

No verified public repository or reproducible wall-time benchmark for the exact energy-moment-only variant was located. The Rai article contains no code-repository link in its HTML and the journal landing page gives none. This is a bounded search result, not proof that no code exists.

## 3. Distinguish from low-degree SOS

The proposal is a physical-matrix positivity SDP with a quadratic operator coefficient ansatz. It is not the ordinary degree-two noncommutative SOS obtained by demanding a PSD Gram matrix on {1,h_i}. A quadratic operator can be positive in the fixed physical representation without admitting that restricted Gram representation. Any comparison must keep this distinction: n grows the physical block size, not the formal polynomial degree.

Tura's February 2024 ICFO seminar already discussed both full positive local decompositions and a Pauli-monomial/NPA-like SOS alternative, with SU(2) block reduction for AKLT. This supports that generic reduced/SOS implementation ideas are old, but does not specify the energy-moment ansatz or a completeness theorem.

Primary source: https://www.icfo.eu/event/3593/seminar-certifying-spectral-gaps-of-1d-quantum-many-body-systems-via-semidefinite-programming/ .

## 4. Other relevant recent work

Rozman, Molnar, Schuch, arXiv:2607.19078v1, Secs. 4.4-4.5: scalar weights lambda_omega optimize blocked local gaps via an SDP; allowing positive operator splits A+B=H_p is a larger SDP. They prove the resulting periodic lower bound converges to limsup of open-chain gaps, not in general the periodic gap. AKLT periodic lower bound 0.2827 uses block size r=14. Their low virtual-dimension overlap calculation is a meaningful practical competitor, but not the proposed quadratic redistribution hierarchy.

Primary source: https://arxiv.org/html/2607.19078v1 .

Rao et al., arXiv:2510.08427v2: convergent finite-system qubit-gap certificates using an exterior-square representation and noncommutative polynomial algebra; polynomial size at fixed degree, convergence by degree n. This is a genuinely different hierarchy and does not already prove the reduced thermodynamic-limit assertion.

Primary source: https://arxiv.org/html/2510.08427v2 .

## 5. Precise size reduction and benchmarking implications

For nearest-neighbor n-site q, Y acts on n-1 sites and has L=n-2 local terms. The proposed scalar ansatz has at most

    2L + L(L-1)/2 = (n-2)(n+1)/2

real coefficients, before removing dependencies, plus delta. For projector h, h_i^2=h_i, leaving at most (n-2)(n-1)/2 coefficients plus delta. All translated moments are generated by this many adjacent-shift equalities; imposing every pair of translated locations redundantly can instead produce O(n^3) tests. Do not conflate those counts.

For AKLT n=6, this gives 10 scalar Y coefficients plus delta versus 3^10=59,049 real unrestricted Hermitian coordinates. Nevertheless the physical PSD matrix is still 729 by 729 (or 725 after exact four-dimensional ground-space removal), and matrix construction, eigenvalue work, symmetry reduction, and conditioning can dominate. Parameter reduction is exact. Runtime or memory advantage remains an empirical claim, and optimum quality must be compared at equal computational budgets.

A fair initial benchmark compares reduced, projected/full LTI, Knabe, GM, and the 2022 pairwise/grouped scalar SDP. Report certified bounds, primal/dual residuals, rigorous error repair, solver and tolerances, wall time, peak memory, and identical symmetry use. AKLT alone is not enough; include a generic non-projector proper parent and a deformation approaching a small gap.
