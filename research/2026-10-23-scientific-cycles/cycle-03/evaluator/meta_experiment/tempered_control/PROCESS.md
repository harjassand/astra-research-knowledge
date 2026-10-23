# Public process record

## Contract observed

- First clock: 2026-10-21 17:20:04 UTC. Hard deadline: 17:32:04 UTC.
- Read only BASE_INSTRUCTIONS.txt, CONTROL_METHOD.txt, and the three named tempered seed files; subsequently read only this participant's own output.
- No web, repository search, sibling-output access, collaboration, or subagents. Numerical calculations used installed NumPy and Python only.
- Final files are restricted to this participant's assigned directory. No novelty or scientific-program ownership is claimed.

## Representations attempted and disposition

1. **Repeated nonlinear set bounds.** The supplied one-step inequality alone suggests a progressively weaker exponent if naively reapplied to arbitrary input laws. This did not provide a useful uniform sharp-rate argument. No impossibility conclusion was drawn from that failure.
2. **Conjugated transition operator.** Conjugating by a diagonal power of q exposes a symmetric stochastic operator plus a normalized rank-one operator. Their counting-measure operator norms are dimension independent. This yields a fixed positive moment exponent for the proposal-start density at every time, with norm growth at most (3/2)^s.
3. **Direct square-integrability.** An initial L2-only reading suggests a threshold at eta = 1/2. Bounded test functions permit an interpolation estimate from any Lp density with p > 1, removing this artificial restriction. The final proof chooses theta = min(eta, 1/2).
4. **First-hit decomposition and spectral anchor.** A fixed positive weight threshold suffices to remove the initially overrepresented very-low-weight region. Unconditioned first-hit submeasures preserve the density moment under invariant-kernel propagation, including arbitrary returns. The remaining high-target tail has coefficient one in the TV bound.
5. **Sharpness and boundary.** The supplied two-state pure-IMH lower construction is admitted by taking Q = I. A separate three-state zero-screen construction gives a positive TV floor and checks the necessity of keeping the screen strength strictly positive.

## Concrete adversarial checks

- Tested the load-bearing entrywise conjugation bound and the stronger L^{1/(1-eta)}(q) moment estimate on 1,120 finite instances. Dimensions: 2, 3, 8, 25. Screen strengths: 0.02, 0.1, 0.25, 0.49, 0.5, 0.75, 0.95. Probability vectors ranged over 100 log units before normalization. These tests did not impose a KL restriction because the tested operator lemma does not require one.
- Checked 12 successive times per instance, totaling 13,440 density-norm comparisons. Largest comparison residual: 1.0547118733938987e-15. Largest norm / (3/2)^s: 0.9202547651566237. Largest stationarity residual: 2.220446049250313e-16. Largest detailed-balance residual: 6.938893903907228e-18.
- Checked the zero-screen endpoint with K = 1, alpha = 0.4, b = 0.3, at n = 100, 1,000, 10,000, and 1,000,000. KL was below one throughout; the exact matrix-power TV exceeded the proved path-event lower bound throughout. At n = 1,000,000, KL was 0.49434560985576226, TV was 0.19930618175383824, and the path-event lower bound was 0.08476074119017757.
- Audited the mathematical dependencies: Q must have column sums one; the moment conversion uses theta p = p - 1; first-hit laws remain subprobabilities; the interpolation uses bounded tests and 1/theta >= 2; the final split uses the same fixed kernel at every step. All are present in the proof.

The numerical checks are diagnostics, not evidence replacing the uniform proof. No trajectories of exponentially long chains were simulated. No unproved optimization output is used.

## Outcome and limits

PROOF.md gives the complete uniform theorem on the requested interval 0 < eta < 1, its natural extension to every fixed eta > 0 under the same kernel formula, the sharp deterministic-time asymptotic, and an optional eta = 0 counterexample. No mathematical gap remains within the stated finite-space contract. Constants are not uniform as eta decreases to zero, and the result asserts no practical speedup or finite-time domination over pure IMH.
