# Proof map and finite evidence for the accepting-pin theorem

This maps the supplied [complete manuscript](package/MANUSCRIPT.md) and saved checks at their actual scope. It is not an additional Capital mathematical audit. The theorem and model/chronology boundary are on the [main page](README.md).

## From the physical model to a local canonical representation

Appendix A gives the complete accepting-tableau compiler and finite-component soundness/completeness proof. Appendix B gives integer-energy realization, the free-boundary Fourier identity, conditioned auxiliary mixing, a low-activity polymer expansion and arbitrary-physical-state projection/converse lift. With t tile types, `C0=10000(t+1)`, `D=C0+t` and finite character group G, the single-spin physical alphabet has `2D|G|^2` symbols. Marked tile eligibility is `1[s=+]`; the multiplicity sum yields the positive factor `C(1+aF)` with `ta<1e-4`.

Conditioned auxiliary Dobrushin row sum is below `.0006`, uniformly in the complete spin configuration. Arbitrary-boundary local ratios are compared with the unique auxiliary law **before** applying a free Fourier identity. Section 3 proves full local spin/tile DLR by finite spatial removal, spin change and insertion moves, with every temporary external modification restored. Finite edits preserve the canonical finite-component subset; unrelated hard-tile sectors with infinite components are not silently classified.

## Comparison, coverings and replica swaps

Section 4 shows that any accepting species of weight w* gives a positive field `h*=(1/2)log[1+w* exp(-|gamma*|zeta)]`. It can be arbitrarily small; its strict positivity permits comparison with the ordinary Ising plus phase. Target FKG/attractiveness is not assumed.

Section 5 uses connected **even dual-edge components**, retaining degree-four vertices and nesting, to obtain an exact finite-box contour gas and an independent hull cover. Accepting rectangles have a separate iid upper cover whose law is independent of spins. The two replicas yield four independent soups. Section 6 inflates supports by a nearest-neighbour collar and bounds intersection chains; a nearest-neighbour path in the original bad set implies such a chain, rather than equating the two notions of component.

The recorded rational bound is about `.644115745024 < 2/3`, with exponential diameter weighting. Sections 7–8 then use finite disagreement-component swaps to establish canonical uniqueness and

```text
|Cov(f,g)| <= 4||f||||g|| |A||B| 2^-dist_infinity(A,B)
```

in the spin/tile representation. Uniform conditioned auxiliary mixing and quasilocal conditional expectations transfer exponential connected decay to all bounded local physical observables, with support-geometric constants and a positive universal rate. No lower accepting-activity or comparison-field bound is inserted into those rates. Nonhalting instead has the exact ordinary zero-field Ising spin specification and its physical plus/minus lifts.

## What the finite programs actually checked

| Original receipt | Stated evidence |
|---|---|
| [Tableau grammar](package/explicit_tableau_grammar_results.json) | 84 exact small-rectangle cases over seven example machines, geometric status checks and ancillary identity |
| [Physical realization](package/physical_realization_checks.json) | Selected character sums, single-spin eligibility and integer-energy/storage checks on an actual generated tileset; not the whole interaction table |
| [Even contours](package/even_contour_checks.json) | Exhaustive 2×2 and 3×3 plus-boundary encodings, degree-four/nested components, deletion, hull coverage and sizes |
| [Weighted branching](package/branching_checks.json) | Exact rational upper bounds conditional on the manuscript's counting/coupling lemmas; not a simulation proof of thermodynamics |

The physical check fixture has 3,712 tile types, group order 512 and about **1.95e13 physical on-site symbols**. That exposes the effective compiler's representation cost; no full physical table or device is claimed materialized. The scripts and all saved outputs are retained unchanged and unexecuted by Capital.

Section 11 reports completed independent internal mathematical reviews of the assembled ingredients. Standard positive-field Ising uniqueness/Lee–Yang, Holley-type comparison, Kotecky–Preiss and two-replica disagreement methods are credited in [SOURCES.md](package/SOURCES.md). Their use does not externally endorse this proposed reduction. The source comparison also retains the promise mismatch with all-equilibria-on-one-side observable-decision results; no contradiction, general pressure uncomputability or historical firstness is inferred. [Original ZIP/capture hashes and status](SOURCES.json).
