# Astra: a compact, certified first-passage law

Research handoff, 15 October 2026.

## Capability

For the specified stationary product model, replace a hitting-time distribution over 2^128 joint states with 304 rational positive exponential components and an exactly preserved initial-target atom. The representation can be reused for distribution evaluation and sampling.

## Evidence

The original rational model has independent binary components with target probabilities 1/2 and distinct relaxation rates 5^(-i)(1+i/1280), i=0,...,127. Exact integer convolution, rational secular-root brackets, and exact probability enclosures certify a coupling with relative time error at most 0.031991361899 except on probability at most 4.851373100e-7. No physical parameters or data are claimed.

Measured preparation: 0.118 seconds exact spectral convolution, 0.421 seconds numerical candidate proposals, and 4.906 seconds exact certification. A separate clean-directory replay produced the identical compact law with approximately 5.21 seconds certification. Timings depend on the execution environment.

The numerical proposals are not trusted for acceptance. Exact checks bound all omitted probability, including roots missed by the proposal code. The million-draw floating benchmark is not a certified finite-bit sampler.

## Mechanism and nearest prior results

Round the positive summed spectral rate with a pathwise multiplicative bound; preserve its probability weights exactly. Feed this compact rate law into the established stationary renewal identity, then acquire its interlacing positive exponential mixture. This avoids repeatedly simulating or estimating the enormous geometric sum.

Brown's renewal representation and Fill–Lyzinski's interlacing theory are established prior art. Approximation of positive random-variable sums has substantial prior art, including Li–Shi's sum-distribution FPTAS. The potential contribution is the contract-specific composition, its native acquisition, and this exact computational certificate. Historical novelty has not been established.

Primary references:
- https://www.ams.jhu.edu/~fill/papers/intertwinings.pdf
- https://arxiv.org/html/1303.6071
- https://qed.usc.edu/paolieri/papers/2025_epew_first_passage_replicated_components.pdf

## What the comparison establishes

An exact interval calculation proves that the mean-matched atom-preserving exponential misses a Laplace-transform value by at least 0.142437. The prior mark-compression algorithm, even with a sharpened stratum bound, analytically expects about 25.1 million marks per draw at the comparison tolerance. These are specified comparisons, not a lower bound against all algorithms.

Ignoring fast gates can look accurate at selected transform values but changes the initial atom. At least 20 half-probability gates must be retained merely to pass the necessary atom test at failure tolerance 1e-6. A clever hybrid that separately preserves the fast atom remains a serious competitor; no universal superiority claim is made.

## Missing operation and consequence

The delivered object is a certified law representation. A fully certified finite-random-bit exponential drawing implementation is a separate step. A physically justified independent, reversible, stationary generator model is also absent. The extreme rate span in this synthetic family should not be interpreted as measured molecular kinetics.

The plausible computational consequence is reusable, compact access to a highly non-exponential first-passage distribution without enumerating the joint generator. The scientific consequence remains conditional on finding a justified model where this output changes an important decision.

## Decisive next tests

1. Independently reproduce all certificate checks and the compact law.
2. Compare against equally accurate slow-gate/hybrid reductions, including acquisition and repeated-query costs.
3. Test a genuinely justified scientific generator, with independence, reversibility, stationarity and parameter uncertainty explicitly checked.

See heterogeneous/README.md for reproduction. THEOREM.md gives the direct positive-rounding argument. Native multistate acquisition is provided as related background; it is not needed for the exact binary fixture.
