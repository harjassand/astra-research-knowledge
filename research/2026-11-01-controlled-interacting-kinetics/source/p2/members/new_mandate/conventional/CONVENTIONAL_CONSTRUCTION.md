# Strong conventional construction for long-time kinetics

## Decision

The broad capability “compute rare kinetics without integrating one natural waiting time, without a perfect reaction coordinate or intermediate basin labels” is already supplied. Adaptive weighted ensemble (WE) supplies exact weighted path statistics; conventional backward-generator equations supply deterministic rates, first-passage means, and pathway currents when a representation of the generator is tractable. Current committor-learning systems extend the latter idea to larger molecular systems. There is no justified new-operation claim merely in combining short trajectories, adaptive bins, memory labels, or a learned committor.

The real unresolved bridge is acquiring a representation that preserves the kinetically important transverse structure, its conditional distributions, and rare competing channels at a finite total cost. WE's exactness does not supply that efficiency. A projected Markov model's good fit to observed data does not establish it. A new proposal must either earn this structure from accessible model information, or impose and justify a useful structural family.

The newly retrieved Astra ordinary-mobility construction is already a nontrivial instance of that second route. It computes actual full-state passage means and absolute CDFs uniformly over a high-dimensional homogeneous quartic family without identifying angular mixing. Its exact Gibbs preparation and global model premises remain unearned physically. This is substantially stronger prior machinery than a generic low-dimensional benchmark.

## Complete conventional service

An operational input must include the microscopic simulator and the physical observables defining the requested output. “No basin labels” does not make an outcome definition unnecessary: for example, an association distance, a reaction-product predicate, or a transport displacement. The algorithm need not receive a metastable partition, true reaction coordinate, hidden-state labels, or rate constants.

1. Run unmodified stochastic dynamics in a WE ensemble. Use REVO/wandering Voronoi regions, an adaptive metric, or learned progress coordinates to allocate replicas. Retain the complete microscopic state and the ancestry needed by requested path functionals.
2. Estimate finite-horizon outcome probabilities and path statistics directly by statistical weights. For multiple terminal outcomes, preserve their separate marked fluxes; do not reduce the desired output to one total transition count.
3. For a source-to-target MFPT, explicitly specify the reinjection law. Recycling at the target yields stationary flux equal to inverse MFPT for that source law. A finite transient flux is not the stationary answer. The reciprocal of a random flux estimate is not generally an unbiased MFPT estimator.
4. Use history-augmented microstate analysis and WE reinitialization to accelerate stationary convergence where the microstate conditional distributions are earned. Check current profiles and independent runs. A history label does not correct arbitrary transient initialization inside a coarse microstate.
5. If the energy/force model admits a tractable operator representation, solve the backward committor and Poisson equations directly. For reversible dynamics, use Dirichlet/Thomson variational constructions; for general dynamics preserve the backward generator and boundary conditions. Direct force/energy access is stronger than access to an unmodified trajectory propagator alone.

Existing exact milestoning/trajectory stratification can replace step 3/4, with the first-hitting distribution on interfaces supplied by its iterative construction. They do not grant free first-hitting sampling or loss of memory in arbitrary coarse bins.

## Why arbitrary adaptive WE remains exact

Let the current weighted path ensemble be `(w_i, X_i[0:t])`. For any bounded path functional `f`, its estimator is `sum_i w_i f(X_i)`. Splitting a weight `w` into daughter weights whose sum is `w` preserves this estimator before further propagation. Merging weights `w_i,w_j` by keeping path `i` with probability `w_i/(w_i+w_j)` and path `j` otherwise, assigning the survivor total weight `w_i+w_j`, preserves the estimator in conditional expectation. The decision about which walkers to split/merge can depend arbitrarily on the observed ensemble and history. Propagating each survivor with the correct conditional dynamics then preserves the true path law in expectation. Induction establishes finite-horizon unbiasedness.

This is an existing theorem, not a contribution here. It applies to arbitrary adaptive binning; for non-Markovian models, the retained state/history must permit the correct conditional propagation. Bad coordinates hurt variance and coverage, not the expectation identity. Merging individual trajectories can create a separate bias when forming longer-lag transition counts by following only survivor ancestry; merge-bias-corrected MSM methods now address that analysis issue.

## Executed positive construction

`kinetics_competitor.py` uses the published asymmetric double-path potential in Trizio–Kang–Parrinello, Eq. S5. It defines a reversible nearest-neighbor finite-grid CTMC approximating overdamped Langevin dynamics with beta=1 and diffusion coefficient 1. This is explicitly a different dynamics from the paper's underdamped simulation; its numerical results are not a reproduction of their physical kinetics.

For neighboring grid points, rates are

    Q_ij = exp[-(U_j-U_i)/2] / h_ij^2,

with reflecting outer grid boundary and Boltzmann stationary weights. The code receives only the energy function, domain/grid, and observable predicates `A={x<=-0.85}`, `B={x>=0.85}`. It does not receive a committor or any intermediate basin labels. It solves:

    Q q = 0 outside A and B, q|A=0, q|B=1;
    -Q t = 1 outside B, t|B=0.

It then computes the source-law MFPT from the exact grid Boltzmann law conditional on A, the separate capacity, and the net reactive current through x=0 split between upper/lower channels. These distinctions matter: capacity divided by source mass is not silently equated to the source-law inverse MFPT.

| Grid | Energy evaluations | Source-law MFPT | Capacity | Upper current fraction |
|---|---:|---:|---:|---:|
| 69 x 61 | 4,209 | 66,896.45 | 1.329286e-5 | 5.95077% |
| 103 x 91 | 9,373 | 66,799.68 | 1.331176e-5 | 5.93225% |
| 137 x 121 | 16,577 | 66,794.17 | 1.331317e-5 | 5.93082% |

The finest model has 65,792 directed edges. Sparse operator construction and two linear solves are also paid computation; the energy-evaluation number is not a complete CPU complexity estimate. Three grid resolutions support numerical stability but are not a rigorous continuum enclosure. Numerical capacity/source-flux and capacity/cut-flux balances agree to about 1e-14 relative.

A deliberately restricted, but optimally fitted, x-only Dirichlet ansatz overestimates capacity by **1.80422 times** and assigns **42.8677%** to the upper channel. It is the best x-only ansatz for this discrete Dirichlet form. The successful full generator construction therefore exposes a meaningful obstruction: low-dimensional progress alone can yield the wrong physical mechanism despite recovering the approximate total scale. It does not demonstrate a failure of WE's path-law exactness or of a sufficiently informed existing method.

## A useful scoped impossibility witness

If the only available operation is propagation of a precursor-free memoryless state with competing exit intensities lambda_1, lambda_2, splitting/merging cannot reduce the total physical-time exposure needed for the first discovery. Across aggregate propagated exposure T, the probability of no exit of type 2 is `exp(-lambda_2*T)`. Adaptation reallocates the same exposure; it cannot create a pre-exit distinction where none exists.

For lambda_2=3e-7, exposure 1e6 has 74.08% probability of no second-channel event. At least 9,985,774 exposure units are required for 95% discovery probability. A useful rate estimate costs more than first discovery.

This is **not** a lower bound for the assignment's full energy/force oracle: off-trajectory queries, analytic structure, a generator solve, or importance proposals with correct weights may supply additional information. That stronger input must be used by any new construction rather than hidden when claiming a simulation barrier.

## Current Astra machinery, pinned and read

Revision: `7ccbd09b6852ed12a3e54ca2bb131f5b2e5d218c`, 2026-11-01. Followed current `00_START_HERE.txt`, then packets N1602–N1605 and exact governing sources. `astra_sources.json` maps saved exact source files to immutable URLs and SHA-256 values. The hashes of the well-current and retained-renewal source files match their explicit source-bound acceptance records. The source files' historical “candidate” headers are preserved; later acceptance records are scoped to their named source hashes.

### N1602: actual means and absolute CDF, original mobility

For `F(y,z)=v(y)U(z)`, `v(y)=1+kappa(1-y^2)^2`, homogeneous positive quartic `U` in `m=4 alpha` variables with an acquired radial coercivity lower bound, and actual constant transverse mobility above a fixed positive floor, the construction uses exact full Gibbs conditioned on `y<=-1/2` and target `y>=1/2`.

The key operation is an explicit Poisson source current. It changes its conditional transverse Gibbs density inside the well to the density appropriate to the barrier top, then carries it through the rare slab with **zero transverse current**. Homogeneous dilation supplies the source redistribution; the unknown angular partition cancels analytically. The witness is mathematical and does not alter the physical drift or mobility. Separate source-A and source-slab currents earn the actual first-passage mean rather than assuming inverse capacity.

The scalar time scale is `T_alpha=beta M_alpha R_alpha`, with `M_alpha=int_(1/2)^infinity v^-alpha` and `R_alpha=int_(-1/2)^(1/2) v^alpha`. The proof obtains uniform mean and all-time absolute exponential-CDF limits over admitted angular potentials and constant mobilities above the floor. It needs no angular mixing time or global spectral gap. A global/killed gap actually vanishes because of longitudinal far-tail test functions. Exact Gibbs initialization, globally valid microscopic model/coercivity, physical parameter calibration, and empirical membership are not acquired by this theorem.

### N1605: continuing hidden-state clock

The later construction reflects the well current to form a global odd source, adds a separate slab residual, obtains a task-specific approximate eigen-observable, and applies an entropy chain rule to complete finite deterministic sampled histories. A completed-transition count identity and a cluster bound then give a time-jitter coupling to an alternating two-state clock on a finite scaled horizon. All hidden angular state remains present. Returns are charged; A-to-B output cycles include a B-to-A return.

This is not exact renewal at finite dimension, continuous timestamp TV, an indefinitely accurate record, free event detection, or a physically prepared autonomous clock. The finite consumer currently refuses a 0.10 error request for the stated ten-observation/continuous-jitter task (packet values 0.139873 and 0.412806). The reference time in that numerical instance is approximately 4.1945e36 model units, not acquired physical exposure. These failures should remain visible.

### N1604: a reusable two-sided energy estimate

The read proof assumes actual positive sub-Markov propagators and their adjoints, both sharing a full reference energy estimate for chronological forward densities and reversed backward observables. A reference bounded-density inequality plus a time-dependent norm envelope gives `integral H_actual(t)dt <= 4 Q_D`, where `Q_D=<1,A^-1 1>` is earned by separate whole-domain source currents. Thus the actual basin-conditioned mean is at most `4Q_D/M` even without a spectral gap. Uniform absolute CDF error alone would not imply this. The extra two-sided/full-source premise is essential and does not automatically admit feedback or free processing.

## Primary sources and executable systems

- Zhang, Jasnow, Zuckerman (2010), “The weighted ensemble path sampling method is statistically exact for a broad class of stochastic processes and binning procedures,” DOI https://doi.org/10.1063/1.3306345 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC2830257/ . Exact adaptive-resampling theorem.
- Donyapour, Roussey, Dickson (2019), REVO, DOI https://doi.org/10.1063/1.5100521 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC7043833/ ; https://github.com/ADicksonLab/wepy . The distance metric is still system-specific and should describe the events of interest.
- Russo et al. (2022), WESTPA 2.0, DOI https://doi.org/10.1021/acs.jctc.1c01154 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC8825686/ ; https://github.com/westpa/westpa ; https://github.com/westpa/westpa2_tutorials . Adaptive/binless sampling, first-passage analysis and haMSM restart.
- Copperman, Zuckerman (2020), non-Markovian microbin analysis, DOI https://doi.org/10.1021/acs.jctc.0c00273 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC8045600/ ; https://github.com/westpa/msm_we . Governing qualification: correct intra-microbin conditional distributions; short lag alone does not remove transient preparation bias.
- Bose et al. (2025), merging-bias-corrected MSMs, DOI https://doi.org/10.1021/acs.jctc.4c01141 ; https://github.com/SamikBose/MBC_MSM . Corrects a separate analysis bias from surviving WE ancestry.
- Lorpaiboon, Weare, Dinner (2026 issue), exact multiple-time-step committor/rate formulation, DOI https://doi.org/10.1021/acs.jpcb.5c06047 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC12768578/ ; https://github.com/dinner-group/evcn . Boundary stopping is essential; stationary full Markov dynamics are assumed, detailed balance for variational minimization.
- Trizio, Kang, Parrinello (2025), “Everything everywhere all at once,” DOI https://doi.org/10.1038/s43588-025-00799-5 ; https://arxiv.org/html/2410.17029v3 ; https://github.com/EnricoTrizio/committor_2.0 ; frozen data/code DOI https://doi.org/10.5281/zenodo.15089372 . Learns a committor with biased equilibrium sampling; initial/final states are supplied, overdamped variational theory is the rigorous base. The present code borrows only its explicitly defined two-path potential.
- Dinner et al., trajectory stratification, DOI https://doi.org/10.1137/16M1104329 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC8514164/ . Existing exact short-fragment framework, not free access to its conditional fragment distributions.

No primary source or software title is a guarantee of generic efficient convergence, historical priority, or an actual physical device. The executed comparison and the exact Astra mechanisms should displace weak novelty claims early while preserving the genuine remaining access/representation problem.
