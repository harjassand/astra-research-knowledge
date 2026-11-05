# Fixed-temperature Fourier reduction

This package contains a self-contained mathematical research manuscript and reproducible finite checks for an effective two-dimensional finite-temperature undecidability construction.

## Status

The result is provisional. Independent internal mathematical reviews of the assembled argument and an adversarial end-to-end review found no unresolved construction-specific hypothesis. It has not undergone external peer review or formal machine verification. The finite checks support the local compiler, algebra and numerical margins; they do not certify the full infinite-volume theorem.

## Exact scope

The construction maps a deterministic Turing machine and finite input to a finite-alphabet, translation-invariant, finite-range classical interaction on the square lattice. All physical local energies are finite nonnegative integers, and inverse temperature is fixed at one.

- Nonhalting: two translation-invariant Gibbs states have opposite exchange-odd means of magnitude above one half, and their equal mixture has zero mean with nondecaying correlations.
- Halting: every translation-invariant Gibbs state has zero exchange-odd mean and exponentially decaying exchange-odd correlations. For the specified on-site observable the manuscript gives the uniform bound 10 times 0.03 to the lattice distance.

The physical mismatch energy is 6, equivalent to Ising exponent coefficient 3. The auxiliary interaction includes a three-site L-shaped factor; it is finite range, not asserted to be pairwise nearest-neighbor.

## Limitations

The theorem does not claim uniqueness of the full Gibbs state, exactly two pure phases, a classification of non-translation-invariant Gibbs states, or a computable bound on the finite-size crossover for a late-halting machine. Standard Dobrushin, polymer expansion, entropy and variational results are explicitly stated and cited. Infinite-volume claims are proved mathematically, not inferred from simulations. No independent-defect assumption or reliable noisy computation is used.

## Files

- `MANUSCRIPT.md`: theorem, constants, effective compiler and complete detailed proof appendices.
- `SOURCES.md`: verified bibliographic citations, links and the role of each standard input.
- `run_checks.py`: portable runner for all four finite checks.
- `checks/check_explicit_tableau_grammar.py`: actual Wang-table generation, small-box assembly, component geometry and exact ancillary identity.
- `checks/check_folded_machine.py`: independent ordinary signed-tape oracle compared with the folded local update.
- `checks/check_final_constants.py`: exact rational certificates for every numerical margin, including the all-distance correlation bound.
- `checks/check_fk_merger_algebra.py`: exact finite-graph partition, conditional-probability, insertion and component-swap checks.
- `checks/*_results.json`: compact results from the verified run.
- `SHA256SUMS.txt`: integrity hashes for the package files.

## Run the checks

Requirements: Python 3.10 or newer. Only the standard library is used. No network access, package installation, credentials or external data are required.

After extracting the ZIP, run from the package directory:

    python3 run_checks.py

Or run any individual script, for example:

    python3 checks/check_final_constants.py

The scripts print their results and rewrite the corresponding JSON files beside them. The independent-machine test uses the fixed seed 20261105. The rational constant check is an analytic verification for all integer distances, not merely a finite sweep.

The compiler checks cover 84 width/height combinations over seven example machines and all status patterns in boxes through 5 by 4. The independent signed-tape check covers 160 random machines, 923 finite-width trajectories and 21,532 exact state/tape comparisons. These are finite tests; the manuscript supplies the general proof.
