# Unfloored exact-dyadic count guide

This is a proposal-design interface, not a committor construction or claimed speedup. It retains the area-envelope interpolation and explicitly heuristic free-energy extrapolation of `coarse_count_guide.py`, but removes its global positive floor. That floor compressed the dynamic range to about 36 nats and could make deep-core guidance ineffective.

`dyadic_count_guide.py` quantizes each designed exponential weight to a positive 24-bit mantissa times an integer power of two. The chosen dyadic values define the guide exactly; floating arithmetic used to choose those values is not asserted to certify the underlying exponential. All increments remain strictly positive across the full approximately 21,397-nat designed range.

Build with `g, metadata = build()`. `g.gap(l,u)` returns `(m,e)` representing the exact sum of increments from l through u−1, as m·2^e. Equal endpoints return zero. Blocks of 256 use exact local integer prefixes; a small tree sums full blocks without subtracting nearly equal global cumulative values. Range queries use logarithmically many tree nodes.

For native single-site coupled moves, use `g.update(h,l,u,dl,du)`, where each endpoint displacement is −1, 0 or +1 and final endpoints are ordered. This adds/subtracts at most two boundary increments. Consequently all possible next guide gaps can be computed with a constant number of integer operations per event. Integer bit complexity is not constant: it depends on the exponent span of the current interval, at most about 31,000 bits at these parameters. Ratios of positive dyadic gaps are exact rational numbers; combining them with native transcendental heatbath rates still requires separate exact/interval sampling or explicitly numerical treatment.

Executed checks: all intervals and legal endpoint moves for four small random arrays compared exactly with Python Fractions; 10,000 range/update consistency checks on the R200 table. Build 0.585 seconds, approximate Python storage 69.2 MB, 10,000 range/update checks 0.076 seconds on this run. The table is regenerated, not bundled as a large binary.

No full first-passage path was run here. No variance bound, mean runtime bound, or approximation to the actual committor has been proved. In particular, avoiding the floor repairs numerical support/dynamic range, not the mismatch between area-basin envelope data and actual level-to-level flux.
