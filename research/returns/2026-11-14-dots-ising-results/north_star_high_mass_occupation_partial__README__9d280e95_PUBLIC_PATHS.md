# Reusable partial result: actual occupation of a high-mass thermal rough-boundary family

## What is genuinely new relative to the earlier delivered package

The earlier work reduced selected entrance-current exceptions. This package establishes an actual-voltage occupation bound for a specified family near the zero-energy droplet size: a4R-square with four independently rough Ferrers corners, arbitrary positive-magnetization thermal interior, and small exterior thermal companions.

This family does NOT have small Gibbs mass. For the same non-target states, its mass is at least n/3 times the core normalizer in the first three examples. Nevertheless, testing a bit-preserving native flow against the original global voltage proves exponentially small occupation. Thus the result cannot be obtained from the elementary inequality v<=1 or from relabeling a rare-equilibrium-state estimate.

At theta4,phi4/R,L8R,epsilon.01, with the ORIGINAL core and source clock:

| R | r | Non-target family mass / Z_A | Actual occupation N_G / Z_A |
|---|---|---|---|
|80|5|at least n/3|at most exp(-612)|
|200|5|at least n/3|at most exp(-1703)|
|1000|6|at least n/3|at most exp(-9047)|
|10000|7|at least n/6|at most exp(-91930)|

These are finite analytic certificates. No trajectory of exponential duration, full committor computation, or large-volume state enumeration was run.

## Exact scope

The family includes exponentially many monotone staircase corner shapes and full thermal interior bits. It does not include arbitrary contours/overhangs, arbitrary large or winding sectors, or multiple exterior macroscopic droplets. This result does not establish coverage of the actual entrance current, complete growth, the full mean hitting-time enclosure, or the North Star. The original research problem remains open.

The construction pools interior bits before aggregating geometric shapes, retains first-target stopping, uses no Gibbs approximation to actual current, and pays contour collisions through a weighted energy triangle inequality and an explicit partition-function bound.

## Read in this order

1.05_four_corner_family/RESULT.md: complete construction, actual-voltage inequality and fair non-target mass baseline.
2.DEPENDENCIES_AND_REVIEW.md: source conventions, exact dependencies, review and limitations.
3.04_optimized_capacity/RESULT.md: finite trial capacity upper with the actual source.
4.03_interior_hole_reduction/: ordinary-interior FKG normalizer reduction; no FKG in a component-capped gas.
5.02_thermal_prefix_flow/RESULT.md: inherited bit-preserving physical-edge moment theorem.
6.06_independent_four_corner_checks/: integer geometry and independent scalar reviews.

01_inherited_source_and_prior contains the previous reusable package as an explicit dependency record. Its older scoped statements are not new headlines.08_authorized_source_snapshot contains the visible repository return used for the inherited model/core interface; its complete underlying acquisition archive was not reconstructed here.

## Reproduction

Requires Python3 standard library only. Run:

    python run_checks.py

The checks recompute scalar certificates and finite integer/rational diagnostics. They are not an external mathematical audit or independent reconstruction of the entire original Astra source theorem. See CHECK_OUTPUT.txt for the recorded run and SHA256SUMS.txt for the manifest.

## Additional, genuinely winding family

09_core_image_winding_annulus proves the same kind of voltage suppression for a specified thermal annulus winding around the torus. It is the spin-flipped image of actual core states with prescribed boundary/collar columns and a positive annular magnetization condition, NOT every positive-interior annulus.

AtR1000, its actual NON-TARGET Gibbs mass is at least0.96399925 Z_A, but its actual occupation is at most exp(-10733) Z_A. The analogous R80,200,10000 bounds are documented in that folder. A separate review supplies a rejection sampler from the inherited core sampler with explicit acceptance, TV/arithmetic and truncation accounting. This is acquisition of the specified Gibbs source family, not sampling the unknown actual entrance current.

The annulus proof avoids assuming an unproved Peierls theorem for winding minus holes. It does not cover general winding states, multiple annuli, arbitrary rough annular boundaries, or all paths exiting the earlier area cutoff. Its finite capacity exponents are cross-checked against the freshly generated capacity certificates by the package runner.
