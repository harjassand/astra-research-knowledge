# Frozen stage 2 stress specification

Written before executing the tests, 2026-10-26 approximately 08:59 UTC. Stage1 files are read-only inputs; no stage1 script is imported or rerun, avoiding even bytecode changes there. New files are written only in stage2.

The strongest competing explanation is transfer of established Ornstein--Uhlenbeck mean-estimation/optimal-design mathematics, rather than invention of a new optimization principle. Primary source found: Kiselak and Stehlik (2008), *Equidistant and D-optimal designs for parameters of Ornstein--Uhlenbeck process*, DOI 10.1016/j.spl.2007.12.012; publisher https://www.sciencedirect.com/science/article/abs/pii/S0167715207004208 and author institution https://research.jku.at/en/publications/equidistant-and-d-optimal-designs-for-parameters-of-ornstein-uhle-2/ . Its primary abstract explicitly establishes n-point equidistant optimality for the trend parameter. We will give the exact mathematical equivalence, rather than infer novelty from a missing thermal keyword.

Mathematical stress targets:

1. Independently implement rational Gaussian elimination and the general backwards moment equations. Enumerate every labelled tree with N=2,3,4,5 storage lumps and one bath using Prufer sequences. Source label 0 and bath label N remain fixed, so source-interior, source-leaf and multiple bath-branch configurations are all represented. For every topology, draw one positive rational capacity/conductance instance from a fixed new seed 17102602. These instances and topology enumeration were not used in stage1.
2. Compute branch-collapse second-moment difference exactly using rational arithmetic. Verify equality to the explicit nonnegative off-path term, equality of means, and the fixed-capacity ladder covariance inequality. Exact enumerated fixtures do not establish all real parameters; the governing algebra and concavity proof must supply that quantifier.
3. Check exact attainment at all N=2..12 for geometric cumulative ratios q=2 and q=3 using positive rational capacities/resistances and prescribed mean 1. Verify all constraints and equality of CV squared to the closed form expressed rationally through q.
4. Give ordinary generalized least-squares estimation access to the exact same exponential covariance kernel, then translate its weights into a thermal design. This is a pre-existing same-information mathematical incumbent, not an incumbent copying a newly disclosed thermal algorithm.

Physical/consequence stress targets:

5. Check the continuum tapered conductor's one-dimensional compatibility at fixed material, source capacity, and timescale. Derive any missing aspect-ratio constraint explicitly rather than assume transverse equilibration.
6. Attempt a stronger conventional switching representation for the original economical timed-release target. A mathematical gate calculation must be labelled an incumbent model, not an experimentally integrated new device; seek actual source-supported operations and retain the precise bridge not supplied.

No new success metric is to be substituted for the original sharp-heat-release question. RMS precision, delivered fraction, physical timing jitter, and a practical new operation remain distinct.

Additional frozen switching test (09:06 UTC, before execution): the source's own cooling controls an ordinary cold-closing conductance, with all leakage included. Compare the analytic contrast frontier from SWITCH_PROOF.md to ordinary scalar threshold minimization for K=3,7,25,111,1000,10000. Independently integrate its output density. Then let the ordinary designer retune a smooth logistic conductance threshold at K=100,1000 for widths 0.0001,0.001,0.01,0.05 times the initial source temperature rise. The width/contrast values are illustrative model parameters, not jointly measured switch data.

Additional conventional-method stress (09:12 UTC, before execution): solve a convex quadratic program for arbitrary piecewise-constant log-temperature resistance curves, including nonmonotone curves, using only a contrast constraint and normalized mean. Start on a fixed geometric knot grid, then refine its own transition cells three times. Compare K=7,111,1000 to the proven ideal frontier; no analytic switch threshold is supplied to the optimizer.
