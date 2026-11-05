# Priority audit: finite-block coboundaries, PVBS, LTI, and GNS

2026-11-05. Targeted primary-literature audit of `COBOUNDARY_REPAIR.md`, `NATIVE_PVBS_EXTENSION.md`, `PVBS_EXTENSION.md`, and the existing review. This is not external proof verification or certification of novelty. Added after the frozen checksum manifest; not part of that manifest.

## Conclusions

1. No existing theorem was located that states the candidate's fixed-block coercive-coboundary condition implies convergence of the **original interaction's unrestricted Rai LTI hierarchy**, with the endpoint-reset proof or its O(n^(-1/2)) rate.
2. Much of the infrastructure is established prior art: PVBS ground spaces and edge localization; noncritical one-dimensional PVBS gap positivity; coboundary freedom of local generators; and finite-volume lower bounds passing to the GNS gap.
3. Native multispecies exact full-gap formulas are not proved by the original PVBS reference. That paper explicitly conjectures the familiar minimum one-particle mass formula for the full system. The candidate correctly avoids needing it.
4. There is an exact reduction of the **GNS-equality question** for the entire fixed-block class to strict product parents. This is an elementary deduction recorded below, not a located published equality theorem. It can use the separate provisional proper-parent GNS proof if that proof is accepted.
5. No general weak-parent completeness, invariance of finite-level LTI values under changing h, or automatic existence of the coercive coboundary follows from the references checked. Novelty remains unresolved.

## A. The closest hierarchy prior art

K. S. Rai et al., *A Hierarchy of Spectral Gap Certificates for Frustration-Free Spin Systems*, Quantum (2026), arXiv:2411.03680v3.

Primary text: https://arxiv.org/html/2411.03680v3

- Equations (17)–(18) give the unrestricted formulation under discussion.
- **Appendix A, equations (49)–(51)** proves that two n-site local generators with equal periodic translation sums differ by A tensor I minus I tensor A, for sufficiently large rings (m>=2n-1 in its precise statement). Thus telescoping freedom itself is prior art.
- **Section 3.2** includes established finite-size bounds; it does not remove boundary effects to recover every exact periodic gap.
- **Section 5** explicitly leaves both eventual detection and exact convergence of the hierarchy open in general, including the one-dimensional frustration-free question.

The proposed occupation bound and reset estimate for an unnormalized LTI witness are additional arguments, not assertions extracted from Appendix A. In particular, the hierarchy first truncates the expansion of H^2 using positivity of distant products of the chosen h terms. Equal periodic sums of h and a different interaction do not automatically give equal finite-level truncated SDPs.

Sujit Rao, *A convergent hierarchy of spectral gap certificates for qubit Hamiltonians*, arXiv:2510.08427v2.

Primary text: https://arxiv.org/html/2510.08427v2

**Sections 1.2.1 and 6.2** establish convergence for a different hierarchy on a fixed finite n-qubit system. It uses a representation encoding the sum of the first two eigenvalues and a ground-energy upper bound. It is not a completeness theorem for Rai's thermodynamic, geometrically local, translation-invariant relaxation. Its title must not be used as evidence for that stronger identification.

## B. Established PVBS results and their limits

Sven Bachmann and Bruno Nachtergaele, *Product vacua with boundary states and the classification of gapped phases*, arXiv:1212.3718v3.

Primary text: https://arxiv.org/html/1212.3718

The exact native pair conventions are equations (2.1)–(2.2). **Proposition 2.1** proves a uniform positive open-chain gap when every occupied lambda_i differs from 1. The following paragraph carries a lower bound to the GNS spectrum. **Proposition 2.8**, equation (2.20), and **Lemma 2.9** establish product bulk limits, edge localization, and interval splitting.

Near the end of the proof of Proposition 2.1, the authors identify 1-2/(lambda_i+lambda_i^(-1)) as the thermodynamic gap of the **one-particle restriction**. The immediately following paragraph explicitly **conjectures** that the minimum over species is the full-system gap. Consequently the source does not establish that many-body formula, exact periodic/GNS equality for arbitrary multispecies parameters, or the LTI theorem. The candidate's restriction to finitely many positive noncritical lambda values, including repetitions and arbitrary allowed phases, matches its own independent algebra rather than an exact-gap formula quoted from this source.

Sven Bachmann, Eman Hamza, Bruno Nachtergaele, Amanda Young, *Product Vacua and Boundary State Models in d-Dimensions*, J. Stat. Phys. 160 (2015), 636–658.

Primary text: https://arxiv.org/html/1410.0398

**Theorem 2.3** gives lower gap bounds on rectangular volumes and infinite limits, and a GNS upper bound on the full lattice. **Theorem 4.1** gives GNS gap >= liminf finite-volume gap. These are inequalities, not equality of exact periodic and GNS gaps. Equation (2.18) explicitly writes the one-species model as an XY interaction plus magnetic-field terms, with an XXZ-type extension. **Proposition 2.4** exhibits gapless edge excitations on a two-dimensional slanted half-plane; it does not supply a one-dimensional closing-open-gap example.

Michael Bishop, *Spectral gaps for the Two-Species Product Vacua and Boundary States models on the d-dimensional lattice*, arXiv:1705.04755v2.

Primary text: https://arxiv.org/html/1705.04755v2

**Theorem 3** proves that the two-species full-lattice GNS Hamiltonian is gapped exactly when neither species' logarithmic anisotropy vector is zero. This classifies positivity, not its numerical value or convergence of periodic gaps. The discussion after the theorem explicitly warns that a simple embedding into independent one-species layers is not available. Thus the candidate appropriately treats native species and tensor-product layers as distinct arguments.

Marius Lemm and Bruno Nachtergaele, *Gapped PVBS models for all species numbers and dimensions*, arXiv:1902.09678v2.

Primary text: https://arxiv.org/html/1902.09678v2

**Theorem 1.1** proves a uniform periodic gap for d>=2 and any finite species number in a specified small-anisotropy regime, equation (1.2). It is not an all-parameter or exact-gap result. The text explicitly credits the arbitrary-species one-dimensional positive-gap result to Bachmann–Nachtergaele. Its finite-size comparison does not provide the candidate's LTI convergence or finite-block diagonal potential.

## C. GNS equality: exact reduction supplied by the block hypothesis

This section is my deduction from the candidate's stated inequality, not a quotation or novelty claim.

Suppose, as in the fixed-block criterion,

    B_k = sum_(i=1)^(k-1) h_i + X_1-X_k
        >= c (I-|0^k><0^k|),

with h>=0 and h|00>=0. Define the range-k interaction

    b = B_k/(k-1).

The vacuum expectation of B_k is zero. Positivity then gives B_k|0^k>=0, and the coercive inequality gives exactly ker b=span{|0^k>}. Thus b is a strict product parent. Its sufficiently long open intervals have only the vacuum kernel and a uniform positive gap: each local b dominates c/(k-1) times its block vacuum-complement, and the sum of those commuting block projections dominates the full interval vacuum-complement.

For sufficiently large periodic rings,

    sum_j tau_j(b) = sum_j tau_j(h),

because each original bond occurs k-1 times and the X terms telescope. The infinite derivations also coincide on every local observable: summing the b terms over larger intervals reproduces each interior h term k-1 times, while all discrepancies eventually lie outside the observable's support. The infinite product state is the same, so its implementing GNS Hamiltonian, normalized to annihilate the cyclic vector, is the same.

Therefore:

- The original h and the strict product representative b have exactly the same periodic gaps and product-state GNS gap.
- The separate proper-parent periodic/GNS candidate, if accepted for finite interaction range, applies with D=1 to b and hence to h.
- This reduction includes the full fixed-block condition even if the individual onsite-shifted two-site interaction is not positive. For native PVBS the positive h' with eventual unique vacuum kernel is another convenient representative.
- This does **not** prove equality of finite-level Rai hierarchy values for h and b. The original-h reset argument remains a distinct ingredient.

The standard published easy direction remains **Nachtergaele–Sims–Young, Theorem 7.4, equation (7.29)**:

https://arxiv.org/html/2010.15337

For rank-one convergent periodic vacuum states it gives limsup Delta_N <= Delta_GNS. No matching general reverse-direction equality theorem was located in this audit or the preceding proper-parent audit.

## D. What remains unresolved or must remain explicit

- Existence of an onsite X and fixed k,c with the block inequality is a substantive extra hypothesis. Unique product bulk data, even a positive periodic gap, do not establish it by the references checked.
- Noncritical parameters are essential to the displayed native construction. At lambda_i=1 its vacuum/species block loses strict positivity; the proof cannot simply retain the same constants.
- The local native determinant argument and repeated-species finite-block kernel argument were not located as a named prior result. They may still be elementary folklore or appear elsewhere; absence from targeted searches is not a priority claim.
- Product-phase equivalence by a quasi-local spectral flow is weaker than equality of Hamiltonians modulo an exact finite-support coboundary. It preserves phase/gap positivity under its hypotheses, not exact spectral values or finite-level SDP optima.
- The asymmetric buffer channel must be controlled on the entire relevant ground code, including arbitrary external references. Ordinary local expectation convergence in Proposition 2.8 is not by itself that channel estimate.
- Original open-chain spectra can differ drastically from the strict-product representative. Accordingly the candidate correctly uses full LTI occupation control rather than importing an unproved original open gap.
- All gap equalities must distinguish a bulk GNS gap, a periodic finite-volume limit, and a limit of open gaps. The PVBS literature provides explicit examples and warnings showing why these distinctions matter.

Recommended positioning: the candidate supplies a sufficient **original-interaction LTI completeness criterion** and an explicit algebraic verification for noncritical native PVBS. Describe the physical PVBS gap and boundary structure as established, and retain “priority unresolved” for the reset criterion, the all-species diagonal potential, and the reverse GNS comparison.
