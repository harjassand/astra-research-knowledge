# Fixed-positive-temperature undecidability of a specified order parameter

The supplied manuscript gives an effective two-dimensional classical model whose **exchange-odd translation-invariant Gibbs behaviour** distinguishes halting from nonhalting. It reports completed independent internal assembly and adversarial end-to-end reviews with no unresolved construction-specific hypothesis. It remains a provisional research proof, without external peer review or formal machine verification. The finite checks support their stated compiler/algebra/constants scope; they do not establish the infinite-volume theorem by simulation.

Read the complete [manuscript with Appendices A–F](package/MANUSCRIPT.md), [construction/evidence map](construction-and-evidence.md), [original ZIP](original/thermal_fourier_reduction_20261105.zip), [visible return](DOTS_FINITE_TEMPERATURE_PROOF_20261105_RETURN.txt) and [source metadata](SOURCES.json). The subsequent [crossover addendum](../2026-11-05-dots-thermal-crossover/README.md) adds conditional finite-size and pressure consequences. Its recorded base-version hash differs from this supplied manuscript; both hashes are retained and exact version identity is not asserted.

A later [single-spin accepting-pin construction](../2026-11-05-dots-unique-phase/README.md) supplies a provisional internally-reviewed proof of full all-Gibbs uniqueness in its halting branch. It changes the physical family and is self-contained. The bilayer exchange-odd theorem here,its both-branch full nonuniqueness and the separately recorded addendum version mismatch remain at their original scopes.

## Exact family and dichotomy

From a deterministic Turing machine and finite input, the compiler produces a finite alphabet, translation-invariant finite-range interaction on the square lattice, an on-site layer-exchange involution and `O=(s-r)/2` taking values -1,0,+1. All physical local energies are **finite nonnegative integers**, with fixed inverse temperature beta=1. The lattice dimension, support shapes and Ising mismatch energy 6 (exponent coefficient J=3) are fixed. The alphabet and explicit energy table depend on the program.

| Machine behaviour | Supplied theorem at beta=1 |
|---|---|
| Never halts | Two translation-invariant Gibbs states exchanged by layer swap have opposite O means with magnitude above 1/2. Their equal mixture has zero mean and O two-point correlations uniformly bounded below by a positive constant. |
| Halts | Every translation-invariant Gibbs state has zero O mean and `|E[O_0 O_x]|<=10(0.03)^||x||_infinity`. More generally bounded local exchange-odd means vanish and separated exchange-odd correlations decay exponentially. |

The effective map therefore gives no algorithm deciding which of these mutually exclusive **observable-specific** behaviours occurs throughout the compiled family. No halting-time estimate is used to set a coupling or cutoff.

This is not a fixed-local-dimension or pairwise-nearest-neighbour theorem. Group variables can be stored in the on-site alphabet, but a site factor then reads a three-site L-shaped support. The auxiliary finite alphabet can grow with the program. Hard constraints in the dual/polymer or Edwards–Sokal proof are not infinite-energy constraints in the physical model.

## Proof operation and limits

Finite-group Fourier orthogonality makes finite selected components **exact accepting computation rectangles**, with invalid tableaux canceling exactly after auxiliary summation. Conditional Dobrushin mixing identifies the induced spin specification for every physical Gibbs state, rather than only a chosen free-boundary limit. A canonical positive polymer lift, pressure comparison and entropy-preserving recoloring supply the all-translation-invariant conditional bond domination. An accepting species then merges the two Ising backbones; finite disagreement-component swaps cancel exchange-odd observables. The [detailed proof map](construction-and-evidence.md) identifies the governing appendices and supplied finite receipts.

The proof does not assume reliable noisy computation, independent sparse defects, spin FKG for the induced interaction, or pointwise absence of infinite dual supports. Its analytic treatment of those issues must not be replaced by finite checks or an ordinary finite-volume FK formula.

The claim excludes full Gibbs uniqueness, exactly two pure phases, classification of non-translation-invariant states and arbitrary perturbation robustness. The [addendum proves common-sign nonuniqueness in both branches](../2026-11-05-dots-thermal-crossover/other-corollaries.md), so full uniqueness and all-observable decay are not hidden extensions of this family. No laboratory device, physically efficient compiler, thermodynamic preparation algorithm or hypercomputation is delivered.

Standard Dobrushin comparison, Kotecky–Preiss polymer expansion, Gibbs/entropy variational principles, the stated equilibrium-to-Gibbs SFT theorem, Edwards–Sokal and Peierls inputs are credited in the [source bibliography](package/SOURCES.md). Their use does not externally endorse this reduction, and an exhaustive priority claim is not established by publication. No scientific code, check runner, new audit or corpus build was run by Capital. Generated current retrieval remains unchanged; the complete proof and these scoped pages are directly public on GitHub.
