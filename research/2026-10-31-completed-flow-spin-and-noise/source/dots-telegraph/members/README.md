# Retained telegraph-noise simulation

Research checkpoint, 31 October 2026 UTC. New work completed after the stability and kinetics recovery volumes.

## Result
An internally independently reviewed theoretical construction simulates a quantum system driven by a fixed operator and rapidly switching symmetric telegraph noise, retaining its correlations across prescribed intervention times. At fixed physical resources, its cost is polynomial in the logarithm of the switching rate and logarithm of inverse approximation error. It does not generate every noise switch, assume a free trajectory oracle, or reset the noise at intervention boundaries.

The result is a finite-circuit existence theorem. No complete quantum compiler was implemented, no practical speedup was measured, and historical novelty is unresolved. Standard sampling, Dirichlet trees, limited independence and interaction-picture simulation are explicitly credited. The physical resource cost remains polynomial in the drift strength, accumulated diffusion strength and number of control slots; this checkpoint does not optimize that polynomial.

## Reading order
1. RETAINED_TELEGRAPH_COMPILER_THEOREM_CANDIDATE.md: complete assembled statement and scope. The filename preserves its working history; the later independent receipt governs mathematical acceptance.
2. INTEGRATED_TELEGRAPH_SOURCE_COMPILER.md: full source construction, finite-bit arithmetic and capped samplers. Its original candidate header is unchanged; read with the later receipt.
3. ROOT_PATH_AND_PROCESS_STABILITY.md and FINITE_QUERY_SOURCE_PRINCIPLE.md: receiving bounds and precise private-seed interface. The natural-scale clipping completion supersedes the earlier unit-grid bound for resource accounting.
4. INDEPENDENT_MATHEMATICAL_REVIEW.md: source-hash-bound review and mandatory completions. Its source-location label was editorially normalized to the included filename; the mathematical text and source checksum are unchanged.
5. FINITE_RATE_DIFFUSION_SCALE_LOWER_BOUND.md: separate finite-rate query lower-bound derivation; consult its review status.

## Checks
The two Python scripts are small numerical sanity tests, not implementations of the claimed quantum compiler or certified arbitrary-precision samplers. The time-warp fixture passed 105 cases through 4096 intervals. Rejection-envelope fixtures passed 102 Gamma and 10 Poisson cases. Floating calculations support diagnostics only; the mathematical proofs carry the guarantees.

## Boundaries
One fixed noise operator; stationary symmetric telegraph law; known finite-description parameters; exact or precision-capable controlled block encodings whose costs are paid; prescribed finite-description intervention times; private seed and bounded query budget. Adaptive operations and retained records at those slots are included. Arbitrary adaptive times, noncommuting noise families, unlimited reuse, seed exposure and normalized rare postselection are not included. Source acquisition from experiments and observable-estimation sampling remain separate costs.

The earlier recovery ZIPs are unchanged. This checkpoint does not amend their scopes or claim publication/integration elsewhere.
