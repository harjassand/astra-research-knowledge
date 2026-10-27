## ASTRA Pro3 — Sparse nonlinear causal-memory acquisition

The strongest result of this continuation is a procedure that learns a finite-horizon nonlinear causal response, rather than assuming that overlapping interventions obey superposition.

I executed the acquisition through the preserved four-port Schur-reaction interface. The source contained a continuous linear relaxation spectrum plus five unknown pairwise intervention interactions.

Under a supplied quadratic-interaction contract, nonnegative interaction strengths and a minimum detectable strength, the compiler located all five interactions using grouped experiments instead of testing every possible pulse pair.

# 128

Intervention-history positions

# 5

Interactions identified

# 64

Later histories certified

| Acquisition method                                                                        | New scalar source readings   |
| ----------------------------------------------------------------------------------------- | ---------------------------- |
| Exhaustively measure every pair                                                           | At least 8,128 pair readings |
| Adaptive grouped-interaction compiler, including baseline and linear-response acquisition | 512                          |

The original eight moment-acquisition readings remain separately charged, giving 520 cumulative source readings for the new procedure.

This is a substantial saving against exhaustive pair testing, not against the strongest known sparse-recovery methods, which already achieve much better scaling than exhaustive reconstruction under suitable assumptions.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www2.eecs.berkeley.edu\&sz=32)

EECS at UC Berkeley

+1



With adversarial raw-reaction errors bounded by \\(10^{-8}\\), the compiler still identified the correct interaction support and produced valid response intervals for all 64 subsequently generated intervention histories. No additional source calls were used for those questions.

### Additional result: separating nonlinear memory from instrument drift

The grouped experiment uses three nonnegative intervention strengths: zero, one unit and two units. Its second-difference measurement cancels the unknown linear response.

It also cancels an unknown affine drift in the reciprocal instrument reading, provided the three readings occur at equally spaced session times.

I executed a revised 128-position acquisition that reuses the no-intervention readings already produced by the grouped experiments. Two of those readings calibrate the shared affine nuisance; the remaining readings test its consistency.

The revised procedure required 511 new scalar readings, recovered the five nonlinear interactions and all remaining linear coefficients, and certified 100 later intervention histories at subsequently specified session times.

The maximum later raw-reaction interval width was approximately \\(1.08\times10^{-7}\\). No separate calibration experiments or future learner source calls were needed.

A quadratic-drift alternative was rejected by 127 inconsistent historical baseline comparisons. This is a genuine model-falsification test, not a proof that every source passing it must continue drifting affinely.

### New mechanism: learning higher-order interactions without learning the whole source

I then weakened the model assumption substantially.

Rather than requiring the entire causal system to be quadratic or linear, I selected two intervention positions and measured their joint interaction, allowing the rest of the source to contain arbitrary nonlinear background responses and effects involving either anchor separately.

Only this selected interaction is assumed to depend affinely on other intervention amplitudes, with a sparse set of nonnegative modifiers.

The compiler discovered two unknown modifiers among 126 candidate positions:

| Procedure                                         | Native scalar reactions |
| ------------------------------------------------- | ----------------------- |
| Exhaustive four-corner testing of every candidate | 508                     |
| Adaptive grouped factorial procedure              | 112                     |

The 112 readings included the initial four-reading anchor calibration and 27 grouped tests. Every reading used nonnegative inputs within the original \\(1/5\\) total-dose limit, with raw sensor error at most \\(10^{-8}\\).

The resulting knowledge certified 100 later weighted-intervention questions with no additional source calls. It also tolerated an unknown affine between-run nuisance because the four readings were ordered to cancel that drift.

A fourth-order interaction was deliberately added to violate the assumed affine interaction rule. The compiler detected the resulting inconsistency after 16 native readings and rejected the model instead of producing an unsupported prediction.

This is a more useful form of partial scientific learning: the agent acquires a reusable causal relationship while leaving much of the underlying source unidentified.

### New experiments generated from acquired knowledge

The learner also synthesized two previously unspecified experimental procedures using only its retained uncertainty certificates.

| Future experimental objective                | Selected intervention                   | Certified response         |
| -------------------------------------------- | --------------------------------------- | -------------------------- |
| Maximize pairwise nonlinear response         | Equal dose of 0.1 at lags 4 and 69      | [0.001999854, 0.002000364] |
| Maximize the selected two-anchor interaction | Dose 0.05 at each anchor, 0.1 at lag 90 | [0.187352, 0.187671]       |

Independent source calculations confirmed the true optima of 0.002 and 0.1875, respectively. The two procedures were synthesized with zero additional source calls. Their certified worst-case regrets are below \\(5.10\times10^{-7}\\) and \\(3.19\times10^{-4}\\).

### Decisive information limits

The research preserved three distinct obstructions:

- Signed cancellation: Opposite interactions can cancel in a grouped measurement, causing the nonnegative sparse-recovery method to miss real effects.
- Insufficient excitation: A pair interaction of strength \\(10^{-6}\\) can remain indistinguishable from zero under the declared \\(10^{-8}\\) adversarial raw-sensor error, even with arbitrarily many adaptive experiments.
- Unobserved nonlinear activation: I constructed two smooth sources identical on all 112 acquired readings but differing by \\(1/5\\) in a future factorial interaction at an unvisited amplitude.

The last counterexample is particularly important. The newly acquired representation can support powerful future operations, but finite successful experiments cannot certify an unrestricted global causal law.

### Verification and preserved research

The independent verifier completed 6,871 exact checks, including native Schur reactions, measurement-error enclosures, later-source predictions and counterexamples. Five programmes passed isolated replay, reproducing nine result files byte-for-byte.

Complete research proofs and findings

Conditional theorems, physical observation contracts, experiment synthesis, noise guarantees, costs and information-theoretic failures.

Reproducible research archive

19 verified files containing the complete note, executable acquisition programmes, actual JSON results, independent verifier, clean replay and SHA-256 manifest.

Scientific assessment: The strongest advancement is learning an operation-specific nonlinear causal relationship without reconstructing the whole source. That acquired knowledge can then generate new intervention procedures and certify their consequences.

Sparse Möbius recovery, graph reconstruction and factorial experimental design remain important established comparators; equally informed methods can reproduce these mechanisms. No new physical law, historical priority or superior general research architecture has been established.

The next foundational obstacle is to obtain meaningful guarantees for signed, higher-order causal interactions without assuming their sparsity, positivity or maximum order, while retaining physically achievable signal-to-noise levels.

The work is preserved locally. The Astra GitHub repository was not modified.