# New actual random-matching test comparison at n=4
2026-10-29. Author: review_actual_logical_comparator. This follow-on construction is separate from the independently received v9 comparison. The general matching theorem and this new implementation require their separate receiving review; the v9 receipt does not accept them implicitly.

Three perfect matchings of four qubits are sampled uniformly. Each prepares two singlets in the same counter-learned local frame Vhat. Pass means all originally paired Bell readouts return singlet. The physical state average equals EE*/2 exactly up to floating precision. A complete Bell measurement followed by discarding its detailed failed outcomes induces the same bath map as projecting onto the rank-one product-singlet pass projector versus its complement and then tracing out the full data register. This equality follows because off-diagonal terms between orthogonal data outcomes vanish under the partial trace. No source bath measurement is performed by the proposed protocol.

The program constructs these actual bath pass/fail maps for the same source U0 and final bath used in v8/v9. It does not obtain matching maps by scaling existing failure effects. It then propagates retained memory, service count and a saturated >6-fault counter. The matching source effect satisfies 2F-W positive in this fixture, with minimum eigenvalue0.00114282388776983. The universal coefficient C=2 at n=4 rests on the separately developed matching frame theorem, not this one-source inequality check.

With R=Cs/(1-s)=1, b=0, t=6,155 service calls and common cap1400:

- Matching C=2,s=1/3: acceptance0.7758593249101313, expected410.3483533063155 source calls.
- Full six-state C=1.5,s=0.4: acceptance0.9290182921559397, expected373.4894256949991 calls.
- Weighted exact C=3,s=0.25: acceptance0.8807827089050563, expected582.0203242292583 calls.

All have the same prior theorem's ideal accepted-subnormalized half-diamond bound1/128 if their respective universal witness premises hold. Their simulated accepted >6-fault weights are around1.5–1.8e-12; these small numerical tails are not used to assert a stronger uniform guarantee. Values are floating mathematical results, not hardware measurements or interval certification. Initial matched caps650/500/800 are preserved separately; common-cap results remove that simple cap-policy confound.

The stronger full logical test still wins both acceptance and expected calls in this particular source fixture. Matching reduces calls relative to weighted testing but loses acceptance. This is a useful rejected advantage claim: a better worst-case witness coefficient does not guarantee higher actual yield, because each test instrument has its own failure rate and bath backaction. It provides no general ordering of the three mechanisms.

All methods use the same one realized million-call learning history. Yield is conditional on that history, not averaged over training. Source model and final bath are evaluator-only. Trusted preparation/readout, hidden current settings/role, private service pads, buffers, inner and outer operations remain requirements. No full gate-duration or physical-error cost comparison has been performed. The matching test avoids full logical decoding on its test shots, but its routing and Bell-readout costs are not free.

## Reproduction
Run independent_review.py once to replay the supplied million-call source-generator learning fixture and export reviewed_fixture_arrays.npz. Run matching_comparison.py for original caps and matching_comparison_commoncap.py for common1400 cap. Both preserve complete bath maps in matching_memory_maps.npz. Imported older proof/program dependencies are retained in prior Capital packages. The supplied array cache is a reproducibility convenience, not physical access granted to the learner.
