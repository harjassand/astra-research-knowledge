# Exact accepting pins: theorem package

**Manuscript:** *Exact accepting pins and undecidable Gibbs uniqueness at fixed positive temperature*.

This package gives a self-contained provisional research proof for a two-dimensional classical finite-range model at inverse temperature one, with finite nonnegative integer physical energies and a computably varying finite alphabet. Nonhalting gives Ising coexistence; halting gives uniqueness among all physical Gibbs states and exponential connected-correlation decay for every bounded local physical observable.

The complete compiler, finite-energy realization, arbitrary-state projection, local positive lift, comparison and disagreement proof are included in `MANUSCRIPT.md`. `SOURCES.md` states the standard inputs and separates the proposed contribution from earlier work.

**Review status:** Independent internal proof reviews completed. This is not external peer review or machine-checked formal verification. No fixed-alphabet claim, arbitrary-perturbation robustness, efficient simulation, or laboratory feasibility is asserted.

## Reproduce the checks

Use Python 3.10 or later. No external packages or network access are needed. Run, from this directory:

    python check_explicit_tableau_grammar.py
    python check_physical_realization.py
    python check_even_contours.py
    python check_branching.py

The scripts write the accompanying JSON results:

- `explicit_tableau_grammar_results.json`: 84 exact small-rectangle checks for seven machines, exhaustive geometric status checks, and the exact ancillary polynomial identity.
- `physical_realization_checks.json`: selected exact finite-group character sums, one-spin accepting-pin masks, and finite integer-energy threshold/storage checks on an actual generated tileset.
- `even_contour_checks.json`: exhaustive 2×2 and 3×3 plus-boundary contour encodings, including degree-four vertices, nesting, whole-component deletion, hull coverage and size bounds.
- `branching_checks.json`: exact rational certification of the four-soup weighted branching bound below 2/3.

These finite tests and numerical bounds supplement the mathematical proof. They do not certify nonhalting or establish infinite-volume behavior by simulation. The checker does not materialize the enormous complete physical interaction table; the manuscript gives its effective finite specification.
