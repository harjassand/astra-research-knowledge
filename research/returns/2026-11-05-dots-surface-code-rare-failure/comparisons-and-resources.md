# Full stage costs, strong comparisons and adverse scaling

The [main result](README.md) demonstrates finite-confidence estimation on specified simulated instances. It is not a speed record, an all-distance algorithm or a hardware-reliability measurement.

## Separately timed work

| Main distance-13 circuit stage | Supplied timing |
|---|---:|
| Fresh circuit acquisition | 3.20 s |
| Floating proposal-table construction | 9.76 s |
| Integer certification | 3.04 s |
| Fresh setup including startup/output | 16.06 s |
| Load an already certified table in the production process | 0.25 s |
| 100,000 production trials | 48.69 s |
| Exact confidence computation | 5.10 s |
| Loaded production process total | 54.03 s |
| Sum of separately measured fresh setup and production | 70.09 s |

The [fresh setup receipt](package/qec_score_resolvent_20261105/fresh_setup_benchmark.json) and [production receipt](package/qec_score_resolvent_20261105/production_100k.json) describe shared-host measurements from separate stages. Their sum is not one uninterrupted benchmark or a matched time-to-accuracy experiment. Fresh graph, certified table and normalizer matched frozen production. Reported production peak process RAM is about 166.5 MiB; these are producer measurements, distinct from Capital's publication-job resources.

The phenomenological distance-21 calculation has different costs: original calculation 27.02 s before serialization, separate process replay 20.46 s and about 573 MiB. A supplied low-memory variant reproduced the result at about 181 MiB with a different runtime. These are implementation tradeoffs at the same model, rather than new sampling principles or controlled speed comparisons.

## Strong existing methods and what was actually compared

The [matched comparison report](package/mcmc4qec_matched_comparison_20261105/REPORT.md) covers ordinary single-flip Metropolis-Hastings, locally balanced Zanella proposals, exchange mixtures and warm-start splitting/Bennett ratios. Its executed comparisons use the same **unrotated distance-13 code-capacity graph and decoder**, not the later circuit model. They include charged anchors and a full ladder, so direct Monte Carlo at the tiny target is not used as a straw-man baseline.

The public mcmc4qec source was inspected read-only and pinned; the numerical comparators independently implement published equations. They are not executions or runtime benchmarks of upstream software. Their fixed budgets did not establish convergence or match candidate precision. No time-to-equal-accuracy speedup, optimal ladder/kernel tuning or impossibility for MCMC follows. A matched optimized **circuit-level** comparison remains unestablished.

Karp-Luby-Madras canonical covers, path-reliability importance sampling, exponential tilting, Doob/supersolution transforms and independent-sample confidence are established mechanisms. Existing QEC splitting already reports probabilities below `1e-20`; the tiny probability alone is not new. Other IID fault-weight/subset methods also need no MCMC mixing assumption. The demonstrated distinction is the completed finite-confidence specification on the stated target and its correction-derived, computable geometric cover. Exhaustive priority or superiority over all importance samplers has not been established.

## Exact adverse scaling is retained

The [independent scaling audit](package/canonical_qec_scaling_audit_20261105/REPORT.md) proves exponential acceptance loss on an exact planar IID serial-diamond family, even if all simple shortest paths could be enumerated perfectly. Thus non-simple walk waste is not the essential obstruction. With `m` diamonds,

\[
\alpha_{accept}\le(2m+1)R(p)^m,\qquad
R(p)\le(2+\sqrt2)/4<0.853554.
\]

This family has Z-distance `2m` and dual X-distance 2; it is not a balanced distance-`2m` surface-code family. Its target can itself be evaluated by an exact `O(m^2)` convolution, which supplies a strong ordinary baseline. Ordinary square-code screens also show acceptance decline, without proving its asymptotic rate.

The score-folded circuit proposal removes much of an initial exponential-tilt overhead on the demonstrated graph. It does not remove canonical-witness overlap, nonfailure proposals or the counterexample. A positive representation and exact normalization do not by themselves establish efficient estimation. There is no general FPRAS, all-distance guarantee or black-box arbitrary-code/decoder estimator.

## Publication and use boundaries

Ideal independent random bits, the exact minimum-weight decoder contract, fixed graph/tie convention and specified noise law are explicit inputs to confidence. The PRNG and frozen hashes support reproducibility, not a proof of physical entropy or measured device rates. Separate model examples retain separate confidence allocations. Earlier floating pilots remain feasibility evidence; the final exact production theorem and audit govern the certified circuit result.

The [release notes](package/RELEASE_NOTES.md) distinguish the portable release from the original machine-specific setup. The [release verification](package/RELEASE_VERIFICATION.json) reports a standalone 1,000-trial pilot and frozen production/hash checks. The completed full-production audit is separate and also included. Some source audit commands refer to historical interpreter paths; the release guide supplies the portable entry points. Those commands are archived reproduction data, not instructions to run them during Capital intake.

All proofs, source, licences, precommits, failures, logs, opaque arrays/tables and audits are preserved in the original ZIP and member tree. Existing source holds remain in force; no physical certification, practical incumbent advantage or civilisation-changing success is promoted by this publication.
