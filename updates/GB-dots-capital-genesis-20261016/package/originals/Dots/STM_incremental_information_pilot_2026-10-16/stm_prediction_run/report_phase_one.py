"""Assemble phase-one report from gate and train/development lock only."""
import json,pathlib,hashlib
R=pathlib.Path(__file__).resolve().parent
x=json.loads((R/'fits/fit_lock.json').read_text());a=json.loads((R/'audit_report.json').read_text());q=json.loads((R/'acquisition_ledger.json').read_text())
lines=['# STM pilot phase one: frozen train/development findings','',
'All numerical results concern recorded image-localization labels on the compatible serialized-new-image (recorded-scan proxy) subset. Interpretation as information immediately before physical scans remains conditional on documented logger timing/freshness semantics. No held-out predictions, scores, outcomes, or label-support summaries were accessed.','',
'## Gates and acquisition',f"- Compatibility/eligibility gate: {a['status']}.",f"- {len(q['verified'])} planned files, {q['received_payload_bytes']:,} received bytes; exact size and Git blob SHA1 verified; SHA256 recorded per file. No retry or replacement.",'- Protocol and manifest unchanged; independent reader, compatibility, and feature/firewall tests passed.']
for split,c in a['counts'].items():lines.append(f"- {split}: {c['eligible_episodes']} eligible episodes; {c['eligible_boundaries']} eligible boundaries.")
lines+=['- Development episode 1501 excluded because its image component touched burned diagnostic 1500. No schema exclusions. Two missing-trace dependent held-out boundaries were excluded/reanchored by fixed audit rules; their outcomes were not inspected.','',
'## Development-only selection','Errors and empirical radii below are in nm. Candidates: 1 = ExtraTrees leaf 2; 2 = ExtraTrees leaf 8; 3 = two coordinate-specific HistGradientBoosting fits. All fitted on train only; no development refit.']
for arm,s in x['selected'].items():lines.append(f"- {arm}: candidate {s['candidate']}; development macro-episode endpoint error {s['development_macro_endpoint_error']:.6f}; empirical residual radius q={s['q']:.6f}.")
for name,m in x['development_baselines'].items():lines.append(f"- {name}: development macro-episode endpoint error {m['macro_endpoint_error']:.6f}.")
lines+=['','### All prespecified candidates','| Arm | Candidate | Macro endpoint error |','|---|---:|---:|']
for name,m in x['development_candidates'].items():
 arm,c=name.split(':');lines.append(f"| {arm} | {c} | {m['macro_endpoint_error']:.6f} |")
p=x['development_selected_paired']['A+F_versus_A'];den=x['selected']['A']['development_macro_endpoint_error']
lines+=['',f"Selected A+F versus A: mean paired development improvement {p['mean']:.6f} nm ({100*p['mean']/den:.2f}%); median {p['median']:.6f}; range [{p['min']:.6f}, {p['max']:.6f}]; strict episode win fraction {p['strict_win_fraction']:.4f}.",
'Development selection is optimistic and is not the held-out decision. Full prespecified endpoint/radius metrics, pooled quantiles, disagreement sensitivity, and all same-hyperparameter comparisons are retained in fits/fit_lock.json.','',
'## Classification support (train/development only)']
for split,s in x['classification_support'].items():lines.append(f"- {split}: {json.dumps(s,sort_keys=True)}")
lines+=['No classifier was fitted. Held-out label support remains unopened; classification will remain unavailable if the frozen support requirements fail.','',
'## Interpretation and limits','- d is source-compatible radial tip displacement, not cumulative travel or atom displacement. Its pre-image timing shares the conditional interpretation.','- Stored start/end requests are pre-addition/pre-clipping; no run-specific physical calibration is certified. Numerical current is source-implied A converted to nA; hardware gain and servo mode unverified.','- Distinct objects plus changed bytes do not prove a physical scan; copied/ambiguous boundaries are conservatively omitted. Identical genuine scans may be omitted.','- Exact image connected components control exact duplicate leakage; near-duplicates and unknown tip/session regimes remain unresolved.','- No claim of physical safety, counterfactual control, saved scans, or novel current-to-site inversion follows.','- Empirical residual radii are descriptive development envelopes, not confidence or conformal guarantees.','',
'## Freeze and next stage',f"- Fit lock SHA256: {hashlib.sha256((R/'fits/fit_lock.json').read_bytes()).hexdigest()}",f"- Feature schema SHA256: {x['schema_hash']}",'- All nine fitted candidates saved as numeric JSON snapshots; code, input, protocol, audit and model hashes are in fit_lock.json. Test labels remain sealed.','- Await root review and separate evaluation authorization. No GO/NO-GO scientific outcome has been declared from development data.']
(R/'PHASE_ONE_REPORT.md').write_text('\n'.join(lines)+'\n')
print('PHASE_ONE_REPORT.md created from gates and train/development freeze only')
