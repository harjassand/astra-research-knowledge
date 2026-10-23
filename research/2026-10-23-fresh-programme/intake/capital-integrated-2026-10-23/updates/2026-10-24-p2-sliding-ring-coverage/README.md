# P2 sliding-ring finite-contour coverage criterion — 24 October 2026

This update preserves one completed producer return on sliding polymer networks. The byte-preserved return and selected-source hashes are in [the source packet](source/producer_return.json) and [manifest](source_manifest.json). No source code was executed and no scientific validation was performed during intake.

## Reported model result

For a fixed network of three-dimensional Gaussian axles, with conserved total contour on each axle, point junctions, and conserved nonpassing spectator counts, the source derives a sufficient condition for positional free-energy convexity after integrating over contour allocations: every constrained interval must contain at least one spectator. The source extends the statement to arbitrary spans and heterogeneous spectator counts, and to fixed convex domains for unobserved junction positions. A finite contour footprint is covered only when the contour that remains Gaussian retains the assumed statistics.

The condition is local to each interval, not a bound on average ring density. The source gives a two-interval `(0, 2)` countercase with an empty interval that can favor contraction. The result does not establish a finite bulk modulus, fast sliding, uniform junction density, or stability when topology changes.

## Finite model diagnostics reported by the producer

The finite-chain calculation uses two 100-segment freely jointed chains crossing at 30 degrees, with anchors 10 segment lengths from the junction. The reported smallest conditional-stiffness shift moves from approximately `−0.01974` to `+0.01971 kBT/b²` after adding one point spectator to each interval. This is a source-reported finite calculation, not a replay in the capital intake.

The explicit-contact pilot uses a 64-bond axle, three rigid seven-bead rings, finite-extensibility bonds and repulsive ring–axle/ring–ring interactions. With one spectator on each side, two starting arrangements have mean distance from the nearer end `6.28 ± 0.66σ` and `6.44 ± 0.69σ`; with both spectators on one side and its reflected control, the values are `0.29 ± 0.10σ` and `0.22 ± 0.02σ`. The corresponding reported fractions within `2σ` are `9.4 ± 2.8%`, `8.0 ± 2.5%`, `98.1 ± 1.8%`, and `99.2 ± 0.5%`. The source reports sampler energy and reverse-proposal checks, but signed-position means were insufficiently mixed. It therefore makes no equilibrium-curvature or exact-flatness claim. This is a constrained contact-model diagnostic, not a physical experiment or a molecular sliding-rate measurement.

## Construction and priority boundary

Reversible polyrotaxane gels, placement-dependent mechanical response, and a mobile ring per subchain are acknowledged prior configurations. The candidate contribution is limited to the stated finite-contour coverage criterion and its network extension. No novelty or priority finding is made here.

The proposed alternating crosslinkable-A/spectator-B ring architecture still lacks demonstrated transit across its actual linker joins, ring-order retention without an imposed simulation restriction, and selective A coupling that leaves B unreactive while preserving aperture and contour transfer. The cited Suzuki step is phenylation rather than reversible inter-ring linking; generic hydroxyl linking would not provide the proposed selectivity.

## Evidence status

- Internal result: producer-reported derivation and finite calculations; not re-proved or replayed by this integration.
- Independent verification: `UNKNOWN` here.
- Physical experiment and practical advantage: `UNKNOWN`; the contact pilot is a model diagnostic.
- Novelty: not inferred; only the producer's bounded prior-art comparison is retained.
