# Exact local square-AKLT loop sampling and spin readout

This research implementation samples the joint routed-loop marginal touching any finite lattice query, directly on Z² or in a finite open box. It has no burn-in or space/time/loop-length cutoff. The loop sampler and source-path identity also give a bounded estimator of a specified thermodynamic spin-pair correlation, without estimating and dividing by a partition-function denominator.

The precise mathematical target, proof, costs and limitations are in `LOCAL_SAMPLING_THEOREM.md`. Independent audits and exact certificates accompany the code. An initial rare-category deficit in a finite-law implementation screen is retained. The fresh pre-registered2,000,000-draw main-engine check found770 events versus781.861 expected (exact p=.693942), so the selected deficit was not reproduced. The implementation signoff combines the analytic invariant, code audit, exact primitive checks and independent diagnostics; nonrejection alone is not a proof. Read the final audit status and fixed-budget physical result.

## Run a local marginal

From the parent directory:

    python square_aklt_local_sampler_20261105/local_perfect_sampler.py --infinite --samples 1000

For programmatic use, add this directory to the Python import path, then:

    from local_perfect_sampler import LocalPerfectLoopSampler
    sampler = LocalPerfectLoopSampler([(0,0),(1,0)], box=None, seed=123)
    loops, work = sampler.sample()
    other_loops, other_work = sampler.sample(query_vertices=[(0,0),(1000000,0)])

`loops` is the entire joint accepted-loop collection touching the requested vertices. The loop routes can extend arbitrarily far away. Each call is a fresh independent marginal draw; it is not an adaptive extension of a previously returned infinite configuration. Query all sites needed for a joint observable in the same call.

Use `box=(width,height)` for an open box with coordinates0..width-1 and0..height-1. The query must lie inside the box. The auxiliary16x16 torus inside the proposal code is not a periodic physical boundary condition.

## Run the physical pair estimator

    python square_aklt_local_sampler_20261105/estimate_local_spin.py --infinite --attempts 10000 --seed 123 --output spin_pilot.json

The default pair is nearest neighbors. For the precommitted95% additive0.01 experiment, use542236 attempts. The theorem assumes ideal independent fair bits; the seeded implementation is a reproducible pseudorandom diagnostic. The output preserves the exact rational sample mean, outward rational Hoeffding interval, seed, sample count and work counters. Floating means and wall times are display values, not sample-law decisions.

The infinite-volume observable is the spin-2 pair-correlation limit selected by expanding open AKLT virtual-identity-boundary mixtures. It is not a statement about arbitrary boundary states, a periodic pure state, a Kubo susceptibility, state preparation or a quantum spectral gap.

## Verification

    python square_aklt_local_sampler_20261105/verify_local_primitives.py
    python square_aklt_local_sampler_20261105/certify_oracle_work.py
    python square_aklt_local_sampler_20261105/certify_oracle_work_sharp.py

The first checks all793 routed loops and21,288 rooted oriented encodings of the complete4x4 graph for four query sets, and exact lazy-time ordering against high-precision diagnostics. The two work checkers use exact integer/rational inequalities. The full all-loop contraction is checked separately by the operator-bridge certificate scripts; the physical source identity has independent small-system exact/VBS checks in the observable-join directory.

Core execution requires Python and NumPy. Exact primitive audits also use mpmath; regenerating the Fourier contraction witness uses SciPy. The tested environment was Python3.12.14, NumPy2.3.5, SciPy1.17.0 and mpmath1.3.0.

## Comparison

The O(3) loop representation and worm/open-path observables already appear in Silva, Schakel and Vasconcelos, PRE88,021301(R)(2013), arXiv:1306.4996. Ancestor perfect simulation is established prior work, notably Ferrari, Fernandez and Garcia, SPA102(2002)63-88. The acquired ingredients here are a checked physical-parameter contraction, an executable exact all-length intersecting-loop oracle, and the local physical readout. No speedup over the published worm or first-invention claim for generic perfect sampling is established.
