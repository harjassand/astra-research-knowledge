# Dots: finite-confidence estimation of rare surface-code failures

This completed result estimates rare logical failures for specified simulated surface-code noise and decoder models with a finite-sample confidence interval, without assuming that a failure-conditioned MCMC chain has mixed. The main circuit run estimates a 13-round failure probability of `2.64809e-8`, with a separately allocated 99.9% interval `[2.40981e-8, 2.90208e-8]`. Its original implementation, exact certificates, completed independent internal audits and limitations are preserved here.

This is a useful model-specific research capability. It does not certify a physical quantum computer, establish a matched speedup over the strongest existing methods or achieve the stated civilisation-changing objective.

## Start with the final result

| Entry | Contents |
|---|---|
| [Complete visible return](DOTS_SURFACE_CODE_RARE_FAILURE_20261105_RETURN.txt) | Dots update, visible time, available prompt context and absence of a visible thinking trace |
| [Original release guide](package/README.md) | Final model/result, exact reproduction expectations, stage costs and limits |
| [Construction and certificates](construction-and-certificates.md) | Canonical witnesses, exact circuit projection, finite score quotient, terminal correction and audit scope |
| [Comparison, scaling and resources](comparisons-and-resources.md) | Strong existing methods, exact adverse scaling, full costs and distinct noise/benchmark contracts |
| [Final theorem](package/qec_score_resolvent_20261105/THEOREM.md), [production result](package/qec_score_resolvent_20261105/production_100k.json) | Fixed circuit law, exact normalizer, counts and outward interval |
| [Completed final independent audit](package/qec_score_resolvent_audit_20261105/AUDIT.md) | All-row certificate checks, finite exact cases and instrumented production replay |
| [Original ZIP](original/surface_code_rare_failure_release_20261105.zip), [release checksums](package/SHA256SUMS_RELEASE), [publication metadata](SOURCES.json) | Complete supplied archive, all original members and provenance |

The [existing Dots conversation](https://chatgpt.com/dots/e80f65ea-ba9f-4235-9233-fb2e264a73aa~6ad0272c4008819ebb67fc4b4e411b17) visibly posted this update at 7:48 PM Brisbane on 5 November 2026, after intervening replies to an earlier human question. No new human prompt immediately preceded it. The underlying model and any user-visible reasoning/activity trace are unavailable in the viewer. The archive and response are supplied evidence; no archived request to continue research is executed by this intake.

## Three demonstrated models remain separate

| Model and endpoint | Supplied evidence |
|---|---|
| Rotated distance-13 Z-basis circuit memory, 13 rounds; 169 data and 337 used data-plus-ancilla qubits; exact rational `p=1/1000` on all four declared noise knobs; fixed integer 4/5-cost decoder | 100,000 proposal trials, 1,249 accepted canonical witnesses; estimate `2.6480902568e-8`; 99.9% interval `[2.4098106601e-8, 2.9020797021e-8]`, including conversion/rounding TV budget below `8.791e-17`; no length cutoff |
| Unrotated distance-21 phenomenological memory, 21 data-error rounds and 20 noisy syndrome observations, perfect initial/final closure; 841 physical qubits and 26,061 independent fault locations at `p=.001` | 10,000 proposals, 898 accepted; 21-round **block** estimate `3.9033e-23`; 99.9% interval `[3.5058e-23, 4.3280e-23]`, including omitted-long-path bound below `3.8e-74` |
| Unrotated distance-13 code-capacity model, 313 qubits and ideal checks | Separately allocated 99.9% interval `[3.6126e-16, 4.0213e-16]` |

Each example has its own 99.9% allocation. All three jointly have at least 99.7% coverage by a union bound, not a simultaneous 99.9% guarantee. The phenomenological block result is not a per-cycle certificate or the circuit-depolarizing model. Model noise rates are specified inputs, not measured device rates.

The main circuit projection preserves one detector basis plus the final logical observable, including the complete correlated marginal through exact factorization. It does not preserve the discarded detector basis or emulate a joint correlation-aware decoder. Integer-cost matching with its fixed tie convention is the chosen decoder, not optimal decoding or exact log-likelihood weighting.

## Version and audit order

The final score-folded theorem, frozen `production_100k.json`, release guide and completed final audit govern the circuit estimate. Earlier floating tilted pilots and the circuit-projection audit's statements that no efficient estimator was yet demonstrated describe earlier stages. They are retained unchanged and must not be substituted for the later certified production result or treated as independent final estimates.

The completed internal audits are preserved at their actual mathematical and finite-instance scopes. The confidence theorem assumes ideal independent random bits and the specified exact minimum-weight decoder contract; the frozen seeded PRNG supplies reproducibility. Exhaustive smaller decoder checks are not a formal proof of every library execution.

Capital publishes all 143 original members, including binary tables and numerical traces as opaque bytes. No sampler, audit script, solver, compiler, numerical array load, simulation or heavy corpus build ran during publication. Existing source holds and generated current retrieval remain unchanged.
