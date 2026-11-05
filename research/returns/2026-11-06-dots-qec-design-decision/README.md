# Model-conditioned QEC sizing: d23 passes among three tested designs

For the supplied rotated memory-Z circuit, all four stochastic noise parameters exactly `1/1000`, `T=d`, frozen single-basis integer-cost MWPM decoder and terminal block-failure target `10^-12`, the record selects **d23 from {19,21,23}**. It is the smallest passing member of those three, with a narrow certified margin—not the minimum over other distances, architectures or real hardware.

The separate recorded-history completion allocation gives at least 99.9% joint coverage **conditional on its enumerated decision-eligible history being exhaustive**, along with the model and ideal independent-random-bit assumptions:

| Candidate | Recorded-family endpoint | Decision |
|---|---:|---|
| d19 | Lower `1.9968521813896402e-12` | Reject |
| d21 | Lower `1.5225336414803657e-12` | Reject |
| d23 | Upper `9.88298197899396e-13` | Pass |

The original preregistered three-candidate family, its exact endpoints and source outputs remain unchanged. This is a terminal single-basis event, not a full logical Pauli-channel guarantee, arbitrary-state quantum memory, failure at any time, per-cycle rate or hardware reliability certificate.

**6 November, separate code-family theorem:** [The minimum-19 proof package](../2026-11-06-dots-symmetric-code-minimum19/README.md) reports an exclusion of 18 physical qubits for arbitrary complex rank-two codes wholly in the fully symmetric subspace, with exact two-error correction and completed internal exact-certificate reviews. Here 19 is block length, not a surface-code distance. It does not alter this model-conditioned d23 decision, establish a physical memory or resolve autonomous-controller repair.

## Governing sources

| Read | Contents |
|---|---|
| [Original compact ZIP](original/qec_design_decision_compact_20261105.zip), [compact guide](package/README.md), [authoritative manifest](package/COMPACT_SHA256SUMS) | All 255 supplied members and 254 current release checksums |
| [Decision report](package/qec_design_direct_20261105/REPORT.md), [theorem](package/qec_design_direct_20261105/THEOREM.md), [decision](package/qec_design_direct_20261105/DECISION.json) | Frozen circuit/decoder, exact interval construction and stopping decision |
| [Recorded-family allocation](package/RECORDED_FAMILY_CONFIDENCE.json), [full-packet historical guide](package/FULL_PACKET_README.md) | Original versus completion coverage, multiplicity and history qualifications |
| [Completed challenger addendum](package/MATCHED_CHALLENGER_ADDENDUM.md) | Latest 31-rung conventional comparison, diagnostic-only uncertainty and cost caveats |
| [Confidence, full costs and reproduction](confidence-costs-and-reproduction.md), [actual human return](DOTS_QEC_DESIGN_20261106_RETURN.txt), [source map](SOURCES.json) | Scope, omitted arrays, provenance and complete visible response |

The compact packet deliberately omits large precomputed tables, binary intermediates and MCMC trajectory arrays. It is not the separate full archival release. Preserved expected digests and regeneration instructions do not mean those arrays are supplied or that a certified sampler runs immediately from this compact extraction. Capital preserves graph/parameter JSON and numerical arrays as bytes, without loading numerical structures or regenerating anything.

The source supplies completed independent checks at their actual scopes. No new Capital audit, sampling, model acquisition, confidence re-evaluation or scientific replay was performed. No speedup or new estimator principle over the best equally informed incumbent is established.

The [earlier rare-failure result](../2026-11-05-dots-surface-code-rare-failure/README.md) retains its model/accuracy/resource limits. The [separate coordination proposal](../2026-11-06-dots-coordination-proposal/README.md) is archived as a proposal, not an executed matched experiment or a demonstrated cause of this outcome. Dots' model and exact response time were unavailable; the exact prompt, visible time context and available interim messages are preserved rather than inferred.

**Later 6 November decoder/setup updates:** [The complete ordered visible updates](decoder-updates-and-compute-limit.md) retain a smaller-design decoder gain,larger-design non-gain,and defeat by a stronger published comparator. Full comparison replay was still underway. The harder coordination test was not ready after reported preparation overran a compute limit that failed to stop it;the source says the attempt was stopped. This is a separate candidate/setup record,not a revision of this sizing decision or evidence of policy/scalable-decoder advantage. No raw code/outcomes/ZIP were supplied with those updates.
