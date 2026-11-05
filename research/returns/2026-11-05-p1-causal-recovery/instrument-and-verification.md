# A physical four-outcome candidate fails, with finite checks kept at scope

The operational constructor completed the rotated inverse tensor into a valid instrument rather than treating a non-trace-preserving tensor as a receiver. In the [exact obstruction](package/operational_constructor/pauli_completion_obstruction.md), `V=cI-2is Phi` and Pauli labels P_k give `K_k=V(P_k tensor I)/2`, with `sum_k K_k* K_k=I`.

After its first spent carrier is discarded, the complete source/receiver/classical-record state has already lost distinguishability of opposite source inputs. Later CPTP processing cannot recover that loss, even with the true source granted and unlimited later memory. Its half-diamond error floor begins `theta^2/2-11theta^4/12+O(theta^6)`. This excludes this specified instrument, not all physical completions or general causal receivers. Low MPO bond and a small algebraic statistic do not themselves provide a trace-preserving payload compression.

The source compares operational tensor-network compression premises with this ordered correlated mixed stream and preserves prior partial-SWAP recovery. A physical decoder still needs a reference-uniform guarantee and a joint angle/error/count/memory/processing bill. [Full report](package/output/pdf/causal_recovery_research_note.pdf).

## Supplied verification and audits

| Evidence | Actual scope |
|---|---|
| [Crossing/interpolation checks](package/operational_constructor/crossing_gap_checks.json) | 20 checks, n=1–4 and five signed parameter values; largest relative identity/interpolation residual about `3.4e-10`, dominated by interpolation cancellation |
| [Exact three-carrier calculation](package/channel_constructor/leading_gap.py) and [summary](package/verification_summary.json) | Symbolic effective matrix/generalized eigenvalue `(7-sqrt(33))/2`; programme retained, not rerun by Capital |
| [Erasure receipt](package/root_analysis/erasure_results.json) | 186 finite subsets/angles; maximum Gram error `4.44e-16` |
| [Independent instrument-floor check](package/operational_constructor/pauli_completion_floor_checks.json) | Seven angles; discrepancies about `2.5e-16` |
| [Full-space finite spectra](package/root_analysis/spectrum.json), [invariant-sector spectra](package/root_analysis/invariant_spectrum.json) | Exploratory small prefixes; an invariant-sector second singular value is not automatically the full-space value |

The independent [crossing audit](package/channel_constructor/crossing_gap_audit.txt), [sharp witness/erasure audit](package/channel_constructor/sharp_profile_and_gap_audit.txt) and [separate recovery audit](package/algebra_constructor/renes_profile_audit.txt) support their stated analytic scopes. The [exponential-gap attempt](package/algebra_constructor/exponential_gap_status.txt) explicitly retains the failed fixed-point-to-singular-loss implication and the unresolved logarithmic gap.

No scientific code, symbolic engine, eigensolver, PDF compiler, new audit or large quantum-state simulation was run for publication. Finite floating checks are not proofs, physical experiments or novelty certificates; the all-prefix asymptotic theorem rests on its analytic proof. [Original package/provenance](SOURCES.json).
