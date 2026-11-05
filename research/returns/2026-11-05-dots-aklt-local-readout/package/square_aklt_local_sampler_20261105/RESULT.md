# Exact local AKLT readout, with an executed infinite-lattice result

## Result

The completed operation computes local equal-time spin correlations in a specified two-dimensional AKLT ground-state limit without burn-in, finite-box extrapolation, a loop-length cutoff, or estimating a partition-function denominator.

For nearest-neighbor spin-2 sites, the executed run returned

    Estimated <S_0 dot S_(1,0)> = -3.559889190566645
    Outward-rounded 95% interval: [-3.569890, -3.549889]

The mathematical interval has coverage at least 95% under the algorithm's independent ideal-fair-bit specification. The implementation uses Python's seeded pseudorandom generator; the seed makes the experiment reproducible but is not a certificate of physical independent randomness. Exact rational arithmetic prevents an additional inward-rounding error. The result is a Monte Carlo confidence statement, not a deterministic enclosure of the true expectation.

The precise physical target is the thermodynamic pair-correlation limit of expanding open square-lattice spin-2 AKLT regions with virtual-identity boundary mixtures:

    sigma_R = V_R I_boundary V_R† / Tr(V_R I_boundary V_R†).

The Hamiltonian is the square-lattice AKLT projector Hamiltonian, with unit spin-4 bond-projector coefficients. This is not an arbitrary-boundary uniqueness theorem, a spectral-gap result, quantum-state preparation, or a dynamical susceptibility calculation.

## What was actually executed

The budget was fixed in advance from a deterministic range bound:

- 542,236 complete independent attempts, seed 2026110501.
- 463,946 non-null source paths requiring local loop queries.
- 722.901 seconds of computation plus 0.106 seconds of setup, about 12 minutes 3 seconds on the shared execution host.
- Exact rational half-width 0.009999995258; both unrounded interval endpoints are preserved in the result JSON.
- The largest observed ancestor clan had 35 cylinders; the largest observed loop had 104 edges. These are observations, not cutoffs.
- No sample means were used to choose the stopping time.

Each local query included, on average, 1.4823 seed proposals, 2.6368 parent proposals, 2.5016 exact-time comparisons and 1.0564 retained ancestor cylinders. Null proposals, rejected parents, geometry, exact-time ordering, cleaning and rational readout are included in the measured elapsed time. Timing is a measurement, not a guaranteed latency or a comparison with optimized production QMC.

The full machine-readable result is `physical_local_infinite_precision001.json`. The precommitment and frozen source hashes are in `production_manifest.json`.

## The missing operation that was constructed

The physical source-path identity was known machinery. The missing executable step was to acquire the exact stationary loop information needed by one local question, including every possible long loop, without constructing or equilibrating the whole surrounding system.

The implementation supplies:

1. An exact all-length rational oracle for every routed loop intersecting an arbitrary finite query set. An auxiliary finite torus supplies a positive proposal bound; actual lattice closure and contact corrections remove its aliases exactly.
2. A consistent residual marked-Poisson ancestor exploration. Shared ancestors and exposed pair marks are reused. New candidates are thinned against earlier revealed regions, so overlapping queries do not independently redraw the same process.
3. Exact lazy event-time comparisons. Symbolic exponential sums are ordered using refining rational logarithm bounds rather than floating tolerances.
4. A normalized local spin estimator. A proposed open path queries only the loops touching its vertices, then evaluates their exact contact-suppression product. Perfect sampling handles the partition-function denominator directly.
5. An infinite-volume coupling. Every queried ancestor clan is finite almost surely. Sufficiently large open boxes therefore eventually agree with the infinite query under one common Poisson construction. This identifies the selected physical limit without estimating a boundary error.

Concretely, the open-path proposal returns each routed path p with probability a_p/C, where a_p=3^(-L_p)(3/5)^(r_p), and returns null for the remaining mass. A non-null path gives the estimator

    X = 9 (-1)^parity(i,j) C product_{gamma touching p} delta(p,gamma).

A null path gives X=0. The loop collection is an independent exact joint local marginal. Each delta is zero for an edge overlap and otherwise (3/5) raised to the number of shared vertices. Thus X has deterministic range width9C, and its expectation is exactly the selected spin-pair limit. Self-contacts and endpoint revisits are included in the audited source-path activity, not discarded.

The loop gas itself has activity w_gamma=3^(1-L_gamma)(3/5)^r_gamma and the usual hard edge exclusion/soft vertex-contact factors. The all-length certificate gives a type-weighted ancestor contraction below 0.907806 at the actual AKLT parameter point, rather than only on a truncated loop catalog.

## Cost and confidence

For a finite query K, independently checked bounds include

- Expected retained clan length below 34.481635|K|.
- Expected birth-oracle calls below 14.120548|K|, including null proposals.
- Expected attempted loop-walk steps below 171.505|K|.
- An explicit exponential moment for total retained weight and total proposals, paying history and known-pair scans.
- Qualitatively finite expected exact arithmetic for each fixed finite query, including adaptive lazy-time comparisons and the Poisson primitive. The random, unbounded source-path query is also covered, so a full physical attempt has finite expected arithmetic.

No enclosing physical volume appears in these bounds. Query size and coordinate bit length still cost work. There is no finite deterministic worst-case running time, no useful small universal bit-operation constant, and no demonstrated linear bit complexity in query size.

The nearest-neighbor estimator has deterministic range width 9C, where

    C = 301805115576299 / 500964985405440.

Hoeffding's inequality with outward rational logarithm/square-root bounds gives the stated fixed-sample confidence interval. It does not cover model mismatch or arbitrary quantum boundary conditions. Additive accuracy does not make distant, exponentially small correlations easy to estimate to relative accuracy.

## Independent checks, including the retained anomaly

The technical assembly includes separate checks of the contraction, local birth probabilities, residual-Poisson invariant, implementation, physical source identity, exact-time arithmetic and complete cost accounting.

- Complete 4x4 enumeration checked 793 routed loop types and 21,288 rooted oriented encodings for four query sets using exact fractions.
- Direct small-system quantum/VBS calculations independently checked the physical factor 9, signs, source contacts and finite-box observable identity.
- A separately coded geometric-exposure sampler checked the full 15-category marginal of a 3x3 query.
- An early selected rare category was low across two main-code pilot batches, about 3.7 standard deviations in combination. Those results were retained. A fresh pre-registered 2,000,000-draw main-code check found 770 events versus 781.861 expected, exact two-sided binomial p=.693942; the selected deficit was not reproduced.
- Independent high-activity finite-support stress tests exercised shared ancestors and repeated earlier-region exclusions much more frequently than the physical parameter does.

Nonrejection in a test is not a proof of correctness. The signoff rests on the mathematical invariant and code/primitive audits, with the statistical tests used as implementation diagnostics. These are reproducible technical audits, not a claim of external journal peer review or proof-assistant verification.

## Strongest existing approaches

[Silva, Schakel and Vasconcelos 2013](https://arxiv.org/abs/1306.4996) already give the matching crossing O(N) loop gas, a finite-lattice Metropolis worm and open-endpoint correlation observables. [Wierschem and Beach 2016](https://arxiv.org/abs/1603.03444) directly compute AKLT observables by valence-bond loop Monte Carlo. These are strong same-access practical comparators.

Generic exact finite-window infinite-volume ancestor simulation is established prior work, including [Fernandez, Ferrari and Garcia 2002](https://arxiv.org/abs/math/9911162). The construction therefore does not invent the loop representation, physical loop observables, ancestor sampling or infinite-volume local perfect sampling as a general framework.

The scoped distinction is an executable exact all-length intersecting-loop oracle, a verified parameter-specific subcriticality certificate, and bounded independent physical readouts at this particular point. The targeted literature check did not locate the same finite-sample infinite-volume guarantee, but that is not a proof of priority.

On the recorded 32x32 pilot, the local readout was about 67 times faster per attempt than this project's earlier **global exact** implementation. That is not a speedup claim over the 2013 worm or 2016 AKLT Monte Carlo; neither published implementation was run head-to-head here. The established advantage is the exact local guarantee and removal of enclosing-volume work, not a QMC speed record.

## Reproduce

From the release root, with Python and NumPy installed:

    python square_aklt_local_sampler_20261105/estimate_local_spin.py --infinite --attempts 542236 --seed 2026110501 --output reproduced_result.json

The release includes the exact proposal data, all runtime dependencies within this project, proof notes, confidence checker, independent audits, retained pilot/focused tests, machine-readable final output and SHA-256 manifest. The code was smoke-tested from a clean extracted directory. NumPy is required for execution; mpmath and SciPy are used by additional audit/certificate scripts.
