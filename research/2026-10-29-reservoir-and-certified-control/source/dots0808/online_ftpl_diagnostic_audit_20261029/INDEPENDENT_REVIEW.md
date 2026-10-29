# Independent review: 120-call finite FTPL diagnostic
2026-10-29. This is separate from both the same-bank frozen-candidate guard experiment and the mathematical finite-FTPL theorem.

## Scope and outcome
The executed diagnostic is a faithful finite-source model exercise of the new controller: 120 calls, 38 product-probe updates, 59 matching validations, and 23 averaged service calls; all 360 requested optimization certificates meet the declared gap. It exhibits 25 validation failures and mean service bad weight about0.3362. This is NOT evidence of useful quantum protection, readiness, a superior learning rate, or performance against a matched baseline. It runs no outer code or unknown payload. Validation failures do not stop the diagnostic. Its starting bath is the declared initial bath, not the final bath of the earlier 60k training run.

## Independent certificate and trajectory checks
`check_all_certificates.py` imports no optimizer/LDL verifier. It independently reconstructs the 35 monomial Gram equations for every stored query, verifies exact rational-unit-quaternion feasible upper values, checks positive definiteness by rational Schur-complement pivots, and confirms the actual interval width meets the declared tolerance77/1920. All360 passed; maximum observed exact gap is about0.000204933.

`physical_replay.py` replays the entire source/probe/validation/service evolution using those independently certified stored oracle outputs rather than rerunning the numerical optimizer. It asserts equality of every fresh perturbed query and tolerance, every role, and every stored per-call diagnostic. The retained bath is updated throughout the trajectory. All values reproduce exactly under the same deterministic numerical simulation environment. The replay's shorter runtime is NOT an optimizer runtime result: it deliberately substitutes certified stored outputs. Original finder runtime of about72 seconds is a one-run observation, not a guaranteed latency.

## Algorithm correspondence
The 35 feature coefficients are accumulated exactly as Fractions with probe importance factor1/p, p=1/3. Current midpoint perturbations use fresh 21-bit coordinate draws, radius2310, with the correct query `(G+Z)/2` for x=(phi+1)/2. The role distribution is p=1/3, validation4/9, service2/9. Source index is fixed before each current candidate and role draw, based only on declared time/history. On a probe, actual prepared/readout axes and outcomes are candidate-independent conditional the actual past. The model source can retain quantum memory and change its current unitary with prior probe history.

Service uses the accepted averaged physical-orbit interface, not a sampled full unknown logical payload implementation. Its total bath update is the actual source on the current frame's P/d input, and its scalar good branch gives the reported bad mass. The D/d=8 star-loss transfer is checked. Matching validations use actual prepared pair singlets and update the bath conditioned on the sampled pass/fail result. No iid bath reset is inserted within a trajectory.

## Required limits
The configured oracle point cap would stop the diagnostic upon failure; such a stop is explicitly NOT a neutral abort or automatic successful theorem instance. In this finite trajectory every call certified, so the cap was not reached. This does not establish all-input success or cheap fallback.

The simulation has a discrete source clock. Its unmodeled optimizer walltime, physical source drift/clock leakage, learned gate synthesis and calibration, readout/reset/control errors, buffering and source isolation remain real implementation obligations. Seeded PRNGs provide repeatability, not a physical private-bit source. The roughly72-second observed solver time cannot be removed from a deployment by calling it offline: this diagnostic chooses new candidates online. The abstract FTPL theorem requires its stated padding/isolation contract.

No same-bank frozen-candidate acceptance ratios, SOS-versus-Hedge yield ratios, or completed outer-decoder evidence should be attributed to this separate 120-call diagnostic. No historical novelty claim is reviewed.
