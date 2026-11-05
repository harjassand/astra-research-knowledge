# Matched independent implementation screen

Committed before running this comparator. This does NOT execute or benchmark the upstream mcmc4qec software. It independently implements the published MH and BAR equations after read-only source inspection.

- Same current canonical_qec_witness Model: unrotated planar distance 13, n=313, independent Z noise p=0.001, ideal syndrome, the same PyMatching object construction, integer unit weights and edge insertion/tie convention.
- Established kernels: uniform one-bit flip; square-root locally balanced one-bit flip; 70% locally balanced plus 30% exchange of two occupied and two empty positions. The latter matches the paper's bit-flip default. No extra 5% laziness from the newer package default.
- Frozen ladder from p0=0.15, recursive p_next=p*exp[-0.8/sqrt(max(np,7))], ending exactly at0.001. Same ladder for all kernels. It is chosen from code size/noise, not candidate failure data.
- Eight independent chains per rung; 8,000 retained steps after1,000 burn-in steps. Initial states alternate a known straight logical string (13errors) and its minimal failing 7-edge prefix, on varying rows. No candidate-generated conditional sample is given to the comparator.
- Fixed50,000-trial independently drawn anchor at p0, reused across kernels. Charge its full cost to each kernel. BAR point estimate uses pooled weight histograms; whole-chain ladder estimates give cross-chain uncertainty diagnostics and initial-state contrast. Nominal99.9% Student-t/delta intervals are diagnostic only and do not claim finite-sample coverage or mixing certification.
- Record all moves/decoder calls, sampling/analysis time, traces and per-rung diagnostics. Independently check the kernel detailed-balance formulas on exhaustively enumerated distance-3 failures before the distance-13 run.
- No reserved or held-out decoder data is used. Installed libraries and the public specified model only.

Before any chain run, source inspection confirmed the upstream caches decoder results. To avoid a weak comparator, this independent implementation likewise caches the correction's logical parity by exact syndrome bytes, shared across chains within a rung and reset at the next rung. It stores only the sufficient correction parity, not the full correction vector. Record both failure-gate queries and actual decoder calls. The anchor has completed but has not been used to tune any chain parameter.
