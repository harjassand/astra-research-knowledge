# Eight-site Schlögl first-slab diagnostics

## Result

Three immutable candidates were tested on the original eight-site first-hit problem over **[0, 0.0001]**. All fail the intended full-forward error gate. No calculation progressed toward T = 1.

| Candidate | Rigorous integrated full-residual lower bound | Rigorous actual augmented-state error lower bound | Full floating residual triangle diagnostic |
|---|---:|---:|---:|
| Euclidean conservation enrichment | 0.0690132460 | 0.1380019503 | 4.842357348 × 10¹⁰ |
| Geometric weighting, larger per-vector ranks | 7.170972668 × 10⁻⁵ | 1.509585413 × 10⁻⁴ | 0.270841235943 |
| Constrained projection on the same localized basis | 1.491853365 × 10⁻⁵ | Not established | Not computed after decisive coordinate rejection |

The first two actual-state bounds use exact localization estimates and an outward total-mass enclosure. The third result rejects the full-forward-residual certificate route; it is **not** a lower bound on actual target-probability error. The table’s lower bounds are rounded downward. All exact authoritative fractions are retained in the JSON certificates.

The weighted trajectory materially improves the floating full-residual diagnostic relative to the prior Lie/linear path, whose one-coordinate residual already exceeded 2. The weighted diagnostic is not an outward upper enclosure. The structural follow-up removes the artificial off-support tail but still has a material dynamical residual.

This is the specified published stochastic reaction-network benchmark, not measured chemical hardware. “Actual state error” means error relative to its exact continuous-time Markov-chain law, not experimentally measured prediction error. “Physical ℓ₁” denotes the original probability coordinates rather than reduced or weighted solver norms.

These are independently written TT Arnoldi/Galerkin plus Chebyshev diagnostics. They are **not an execution or benchmark of full tAMEn/AMEn**, and they do not produce a certified rare-event probability.

## Unchanged physical contract

- Eight sites; all ten edges of the open 2 × 4 graph
- Counts 0 through 162; initial counts all 50
- First entry into all counts ≤ 15 is absorbing
- Physical outward transitions enter a separate overflow sink
- Target states remain frozen on the grid; their total mass is success, without a duplicate success sink
- Degree-32 anchored Chebyshev trajectories on the full slab h = 0.0001
- Exact initialization and no join defect for all three saved candidates

The candidates retain all physical dimensions. Compact support of individual trial vectors is a representation choice; full generator leakage at their support boundaries is included in every independent residual test.

## Error-budget interpretation

The rejection checks deliberately use a generous **10⁻⁹ interior budget**. If the goal is **10⁻⁹ total absolute error for the unbounded process**, the cap-162 overflow allowance 7.56906842744787 × 10⁻¹⁰ (rounded upward) leaves only 2.43093157255213 × 10⁻¹⁰ (rounded downward) for all interior and arithmetic errors. All three candidates fail even the more generous interior budget.

The hypothetical m = 320 uniformization tail allowance over 10,000 such slabs additionally uses less than 6.65 × 10⁻¹¹ of the remaining budget; it is not a state-solve certificate or a free error allowance.

## Reproduce the certificates

Requires Python 3 and NumPy. Verification does not require SciPy, MATLAB, network access, package installation, or rerunning an approximation solver.

    python verify_packet.py --output-dir verification_output

The entry point checks every packet file hash, runs 1,026 verifier self-tests, reproduces the exact rejection/localization/cap certificates, and checks the primary-incumbent scalar uniformization arithmetic. It executes only the independently written verification programs. Candidate solvers and acquired MATLAB source are never imported or executed. Temporary copies are used for checks that write beside their script. Expected certificates remain unchanged.

Most individual verifier processes impose 512 MiB and 120 CPU-second limits. The replay is sequential. Its JSON summary distinguishes verified certificates from diagnostic approximation data.

## Contents

- `reports/METHODS_AND_COSTS.md`: construction, complete residual decomposition, resources, and limits
- `verification/REPORT.md`: detailed mathematical verification, constrained-projection algebra, and exact certificates
- `experiments/candidate.npz`: first immutable candidate
- `experiments/weighted_repair/candidate.npz`: second immutable candidate
- `experiments/constrained_test/candidate.npz`: third immutable candidate
- `experiments/`: original independent solver code and numerical records, supplied for provenance, not run by the verification entry point
- `references/cap_source/`: unchanged acquired cap proof and source evidence
- `references/incumbent/`: primary-source audit of inexact tensor uniformization and its exact scalar rate/Poisson checker
- `references/tamen_source_text/`: acquired author MATLAB source, MIT license, and source manifest; text-only provenance
- `PACKET_MANIFEST.json`: SHA256 and byte count for every included file
- `EDITORIAL_AND_PATH_MAP.md`: editorial changes to report copies and mapping of historical paths

All three NPZ files are included byte for byte, with no basis deduplication. Although the second and third share localized basis arrays, their exact individual file identities are preserved.

## Closest incumbent and remaining gap

The primary audit identifies a genuine physical ℓ₁ internal-error bound in Vo–Sidje (2017): the stored space–power tensor's full recurrence residual controls inexact uniformization error when the transition operator is stochastic. That is stronger than a reduced/Frobenius stopping tolerance. The audit does not establish an executed, affordable, outward-rounded full-ℓ₁ implementation for this event and accuracy.

For the unchanged cap, the independently checked maximum exit rate is θ = 492588879/250, so θh = 197.0355516. The supplied exact Chernoff checker establishes sufficient uniformization cutoffs m = 315 and 320 for its stated scalar tail targets. It does not perform a state solve or establish a tensor-rank/runtime bound.

The missing result remains a sufficiently accurate continuous trajectory or endpoint construction with a rigorously enclosed full physical error. Conserved mass, a small reduced residual, and tiny reported success/overflow coordinates are not substitutes.
