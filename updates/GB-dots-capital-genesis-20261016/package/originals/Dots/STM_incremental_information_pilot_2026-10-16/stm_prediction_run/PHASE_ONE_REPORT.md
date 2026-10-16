# STM pilot phase one: frozen train/development findings

All numerical results concern recorded image-localization labels on the compatible serialized-new-image (recorded-scan proxy) subset. Interpretation as information immediately before physical scans remains conditional on documented logger timing/freshness semantics. No held-out predictions, scores, outcomes, or label-support summaries were accessed.

## Gates and acquisition
- Compatibility/eligibility gate: PASS.
- 220 planned files, 210,440,337 received bytes; exact size and Git blob SHA1 verified; SHA256 recorded per file. No retry or replacement.
- Protocol and manifest unchanged; independent reader, compatibility, and feature/firewall tests passed.
- development: 39 eligible episodes; 72 eligible boundaries.
- test: 60 eligible episodes; 100 eligible boundaries.
- train: 120 eligible episodes; 384 eligible boundaries.
- Development episode 1501 excluded because its image component touched burned diagnostic 1500. No schema exclusions. Two missing-trace dependent held-out boundaries were excluded/reanchored by fixed audit rules; their outcomes were not inspected.

## Development-only selection
Errors and empirical radii below are in nm. Candidates: 1 = ExtraTrees leaf 2; 2 = ExtraTrees leaf 8; 3 = two coordinate-specific HistGradientBoosting fits. All fitted on train only; no development refit.
- A: candidate 2; development macro-episode endpoint error 0.273011; empirical residual radius q=0.617667.
- A+C: candidate 2; development macro-episode endpoint error 0.276510; empirical residual radius q=0.575020.
- A+F: candidate 2; development macro-episode endpoint error 0.278816; empirical residual radius q=0.582898.
- command_request_endpoint: development macro-episode endpoint error 0.211710.
- persistence: development macro-episode endpoint error 0.848436.

### All prespecified candidates
| Arm | Candidate | Macro endpoint error |
|---|---:|---:|
| A+C | 1 | 0.326299 |
| A+C | 2 | 0.276510 |
| A+C | 3 | 0.414565 |
| A+F | 1 | 0.311872 |
| A+F | 2 | 0.278816 |
| A+F | 3 | 0.418396 |
| A | 1 | 0.291301 |
| A | 2 | 0.273011 |
| A | 3 | 0.367543 |

Selected A+F versus A: mean paired development improvement -0.005806 nm (-2.13%); median -0.005525; range [-0.113202, 0.048186]; strict episode win fraction 0.4103.
Development selection is optimistic and is not the held-out decision. Full prespecified endpoint/radius metrics, pooled quantiles, disagreement sensitivity, and all same-hyperparameter comparisons are retained in fits/fit_lock.json.

## Classification support (train/development only)
- development: {"counts": {"0": {"episodes": 19, "rows": 36}, "1": {"episodes": 36, "rows": 36}}, "meets_train_development_requirement": true}
- train: {"counts": {"0": {"episodes": 96, "rows": 329}, "1": {"episodes": 55, "rows": 55}}, "meets_train_development_requirement": true}
No classifier was fitted. Held-out label support remains unopened; classification will remain unavailable if the frozen support requirements fail.

## Interpretation and limits
- d is source-compatible radial tip displacement, not cumulative travel or atom displacement. Its pre-image timing shares the conditional interpretation.
- Stored start/end requests are pre-addition/pre-clipping; no run-specific physical calibration is certified. Numerical current is source-implied A converted to nA; hardware gain and servo mode unverified.
- Distinct objects plus changed bytes do not prove a physical scan; copied/ambiguous boundaries are conservatively omitted. Identical genuine scans may be omitted.
- Exact image connected components control exact duplicate leakage; near-duplicates and unknown tip/session regimes remain unresolved.
- No claim of physical safety, counterfactual control, saved scans, or novel current-to-site inversion follows.
- Empirical residual radii are descriptive development envelopes, not confidence or conformal guarantees.

## Freeze and next stage
- Fit lock SHA256: 3e2ae20e8141e99eb9fb4486771b6d45d362d6078316aae2d81ad20c0db6d9bb
- Feature schema SHA256: b84cca16b87a50f4650dd06fea6fcca23366ab0d1c518fbe19099d5dc359d44e
- All nine fitted candidates saved as numeric JSON snapshots; code, input, protocol, audit and model hashes are in fit_lock.json. Test labels remain sealed.
- Await root review and separate evaluation authorization. No GO/NO-GO scientific outcome has been declared from development data.
