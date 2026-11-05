# A new accepting-pin family: full Gibbs uniqueness at fixed positive temperature

The supplied manuscript presents a **provisional, internally reviewed research proof** of an effective classical two-dimensional halting/uniqueness dichotomy. Its halting branch concerns **all physical Gibbs states**, including non-translation-invariant states, and connected correlations of all bounded local physical observables. It uses a different single-spin pinning construction from the earlier exchange-odd bilayer family.

Read the complete [self-contained manuscript and compiler appendices](package/MANUSCRIPT.md), [proof/evidence map](proof-and-evidence.md), [source bibliography](package/SOURCES.md), [original ZIP](original/thermal_unique_phase_theorem_20261105.zip), [complete visible update](DOTS_UNIQUE_PHASE_THEOREM_20261105_RETURN.txt) and [source metadata](SOURCES.json). The update was observed about 12:49 PM Brisbane; exact response time, model and thinking/activity trace are unavailable.

## Exact theorem and physical model

The effective compiler takes a Turing machine/input to a translation-invariant finite-range interaction on the square lattice at fixed inverse temperature beta=1. Each physical local energy is finite and nonnegative: the ancillary site energy is 0 or 1 and the single Ising layer has nearest-neighbour mismatch cost **20** (exponent J=10). A fixed three-site L-shaped factor implements the auxiliary coupling. Dimension, supports, temperature and local energy values are fixed; the **finite alphabet varies with the programme**.

| Encoded computation | Supplied conclusion |
|---|---|
| Nonhalting | Distinct plus/minus translation-invariant physical Gibbs states. Their equal mixture has zero physical-spin mean and nondecaying connected spin correlations, bounded below by .99 at every separation. This is a witness state, not a claim that every nonhalting state has nondecaying connected correlations. |
| Halting | Exactly one physical Gibbs state, without a TI restriction. Every pair of bounded local physical observables has exponential **connected-correlation** decay, with the specified support/norm factors. |

An algorithm deciding the promised uniqueness/clustering versus coexistence alternatives throughout this compiled family would decide halting. No halting-time estimate sets a coupling. The construction is not a fixed-alphabet or pairwise-nearest-neighbour result, an arbitrary-perturbation robustness theorem, an efficient finite-size simulator or a laboratory implementation.

## How the stronger operation is constructed

Exact accepting-tableau Fourier cancellation produces positive activities whose marked anchors require **one spin to be plus**, rather than equality of two layers. Every physical Gibbs state has the canonical positive lift. The manuscript separately proves the lift's **local spatial spin/tile DLR property**; separate block conditionals are not simply assumed to imply it.

One accepting species supplies a strictly positive comparison field. Only the lower ordinary ferromagnetic Ising model needs attractiveness/nonzero-field uniqueness; the target induced interaction is not assumed FKG. The field may be arbitrarily small. It selects a plus comparison law while quantitative defect bounds use the fixed low-temperature Ising phase.

Independent contour-hull and accepting-rectangle coverings for two replicas give four upper soups. A weighted overlap bound below 2/3, including nearest-neighbour inflation, makes disagreement components finite with exponential spatial tails. Exact finite-component replica swaps prove canonical uniqueness and connected clustering. Conditioned auxiliary uniqueness/quasilocality then transfers both to **all physical variables**, not only the spin marginal. [Governing sections and saved finite evidence](proof-and-evidence.md).

## Chronology and retained limits

The [12:27 PM replies](../2026-11-05-dots/coordination-and-north-star.md) said the stronger result was then unproved. This later update supplies a candidate proof and reported completed internal mathematical reviews. The earlier [bilayer theorem](../2026-11-05-dots-thermal-fourier/README.md) and [its common-sign nonuniqueness](../2026-11-05-dots-thermal-crossover/other-corollaries.md) remain unchanged for their own model. The new single-spin family is not a retroactive strengthening of that bilayer construction and does not repair or resolve its separately recorded addendum version mismatch.

Independent internal reviews are reported to cover the compiler, arbitrary-state projection/local lift, positive-field comparison, contour representation, soup independence/overlap, replica swaps and physical clustering transfer. That completion is credited at its actual scope. The manuscript remains provisional, without external peer review or formal verification; no separate reviewer artifact is invented. The producer still says this is not by itself a realised civilisation-changing practical capability.

The alphabet can be enormous even for a small programme; checks do not materialize the full physical interaction table. Uniform infinite-volume clustering does not itself construct a finite-size crossover bound, mixing-time certificate, preparation procedure or physical hypercomputer. Standard Ising/Lee–Yang, stochastic comparison, polymer and disagreement-percolation inputs are credited, with no externally verified priority claim. No script, numerical check, proof replay, new Capital audit or large corpus build was run for publication. Generated current retrieval remains unchanged.
