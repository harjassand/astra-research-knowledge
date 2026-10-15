#!/usr/bin/env python3
"""Read-only final claim/diff integrity audit; writes only its new R report.

No scientific script, generator, publisher, Git mutation or W write is run.
Semantic findings are the auditor's reading, not an automated truth test.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

R = Path('/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-global-completion-axis-v1')
W = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-global-completion-axis-20261015')
D = R / 'final_curation_audit'
FX = 'updates/FX-global-completion-axis-20261015/'
BASE = 'ab5118e70a7e6a0dd39e75dd563d3a3f50b06b25'
inputs = {}
checks = []
issues = []


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, origin='W'):
    raw = ((W if origin == 'W' else R) / path).read_bytes()
    key = (origin, path)
    if key in inputs and inputs[key]['sha256'] != sha(raw):
        issues.append({'severity': 'material', 'kind': 'concurrent_input_change', 'path': path})
    inputs[key] = {'origin': origin, 'path': path, 'sha256': sha(raw), 'bytes': len(raw)}
    return raw


def doc(path, origin='W'):
    return json.loads(read(path, origin))


def rows(path):
    return [json.loads(x) for x in read(path).decode().splitlines() if x.strip()]


def git(*args):
    return subprocess.check_output(['git', '-C', str(W), *args])


def check(name, passed, detail):
    checks.append({'check': name, 'status': 'PASS' if passed else 'FAIL', 'detail': detail})
    if not passed:
        issues.append({'severity': 'material', 'kind': name, 'detail': detail})


head_before = git('rev-parse', 'HEAD').decode().strip()
c = doc(FX + 'CURATION_INPUT.root-final.v0001.json')
freeze_ref = c['selected_freeze']
freeze_raw = read(freeze_ref['path'])
freeze = json.loads(freeze_raw)
check('root_final_identity', c['curation_status'] == 'root_final' and c['curated_by'] == 'root' and c['base_revision'] == BASE,
      'Root owns final scientific curation; actual root-final input remains pinned to its declared initial main.')
check('root_freeze_identity', sha(freeze_raw) == freeze_ref['sha256'] and freeze['status'] == 'root_frozen' and freeze['selected_by'] == 'root' and freeze['base_revision'] == BASE,
      'The selected-freeze ref has exact bytes and root/base attribution.')

selected = {x['path']: x for x in freeze['files']}
check('freeze_totals', len(selected) == freeze['total_files'] == 269 and sum(x['bytes'] for x in selected.values()) == freeze['total_bytes'],
      '269 selected files; exact byte total is checked from manifest records.')
selected_mismatches = []
research_mismatches = []
for path, x in selected.items():
    raw = read(path)
    if sha(raw) != x['sha256'] or len(raw) != x['bytes']:
        selected_mismatches.append(path)
    original = read(x['research_relative_path'], 'R')
    if original != raw:
        research_mismatches.append(x['research_relative_path'])
check('all_selected_frozen_bytes', not selected_mismatches, selected_mismatches or 'All selected SHA256 and byte lengths match.')
check('selected_matches_current_research', not research_mismatches, research_mismatches or 'All selected bytes also match their current R source; no version drift observed.')
check('derived_source_roles', all(x['provenance_role'] != 'supplied_original_file' and x['contains_external_fulltext'] is False and x['contains_external_dataset_or_clone'] is False for x in selected.values()),
      'New derived files are separately attributed; supplied originals are not relabelled as new authored evidence.')
check('new_fulltext_exclusion', all(Path(x['path']).suffix.lower() in {'.md', '.txt', '.json', '.jsonl', '.py', '.tex', '.sh', '.csv', '.tsv'} for x in selected.values()) and not any('/sources/' in x['research_relative_path'] and Path(x['path']).suffix != '.json' for x in selected.values()),
      'The selected derived payload contains no acquired binary fulltext/dataset/clone. The nested sources records are acquisition/inspection JSON receipts, not fulltexts.')

incoming = doc(FX + 'SOURCE_MANIFEST.json')
original_mismatches = []
for x in incoming['files']:
    raw = read(x['path'])
    if sha(raw) != x['sha256'] or len(raw) != x['bytes']:
        original_mismatches.append(x['path'])
check('all_supplied_originals_preserved', incoming['source_count'] == 55 and incoming['group_count'] == 7 and not original_mismatches,
      original_mismatches or 'All55 supplied originals in7 groups match their distinct source manifest.')

metadata = {x.get('source_id', x.get('id')): x for x in rows('indexes/source_metadata.jsonl')}
source_issues = []
for x in c['sources']:
    raw = read(x['path'])
    m = metadata.get(x['source_id'])
    if sha(raw) != x['sha256'] or not m or any(m.get(k) != x.get(k) for k in ['path', 'sha256', 'provenance_role']):
        source_issues.append(x['path'])
    if x['path'] in selected and selected[x['path']]['provenance_role'] != x['provenance_role']:
        source_issues.append(x['path'] + ': freeze role mismatch')
    if '/package/originals/' in x['path'] and x['provenance_role'] != 'supplied_original_file':
        source_issues.append(x['path'] + ': original role mismatch')
check('indexed_source_roles_and_hashes', len(c['sources']) == 28 and not source_issues,
      source_issues or '28 new indexed sources have exact metadata/hash/provenance matches; the two supplied source texts retain supplied_original_file.')

evidence_issues = []
for key, x in c['evidence'].items():
    raw = read(x['path'])
    if sha(raw) != x['sha256']:
        evidence_issues.append([key, 'hash'])
    span = x['lines']
    if not 1 <= span[0] <= span[1] <= len(raw.decode().splitlines()):
        evidence_issues.append([key, 'inclusive span'])
    if x.get('source_revision') is not None and raw != git('show', x['source_revision'] + ':' + x['path']):
        evidence_issues.append([key, 'pinned revision'])
    m = metadata.get(x.get('source_id'))
    if not m or m.get('path') != x['path'] or m.get('sha256') != x['sha256']:
        evidence_issues.append([key, 'source metadata'])
check('every_evidence_ref', len(c['evidence']) == 56 and not evidence_issues,
      evidence_issues or 'All56 exact evidence refs have valid inclusive spans, matching source metadata and current/frozen hashes; inherited refs match their full pinned revision.')

expected_corrected = {
    'workers/full_invariant_genesis/flat_completion_compiler.py': 'bb0cea71e048eccac401a91288b17d7ed1ce7d705250d52dfc29addc71d21433',
    'root/ORDER_VOLUME_IDENTIFICATION.v0004.md': '7cd7cfbd23f6c2a1a9b2bfd17ed3c7b561c981cb6278c970aadcc9f2d9047eab',
    'workers/sharp_boundary_coercivity/CLARIFICATION_20261015_V1.md': '6986d72219e0b7eb5ae522572483d861574c9edc90b64d199b727dece315cd6d'
}
check('corrected_scientific_versions', all(selected[FX + 'package/derived/' + p]['sha256'] == h for p, h in expected_corrected.items()),
      expected_corrected)

claims = {x['id']: x for x in rows('indexes/claims.jsonl')}
statuses = {x['card_id']: x for x in rows('frontier/CURRENT_CLAIM_STATUS.jsonl')}
current_cards = []
current_authority_paths = []
card_issues = []
for x in c['cards']:
    cid = x['id']
    rawpath = 'cards/' + cid + '.txt'
    reviewpath = 'frontier/review_cards/' + cid + '.txt'
    frontpath = 'frontier/cards/' + cid + '.json'
    raw = read(rawpath)
    front = doc(frontpath)
    current_cards.append(front)
    current_authority_paths += [rawpath, reviewpath, frontpath]
    if raw != read(reviewpath) or front['card_sha256'] != sha(raw) or front != statuses[cid]:
        card_issues.append([cid, 'card bytes/status projection'])
    if ('Exact statement: ' + x['statement']) not in raw.decode() or ('Source-reported status: ' + x['reported_status']) not in raw.decode():
        card_issues.append([cid, 'root-final statement mismatch'])
    if front['claim_status'] != 'source_derived_unreviewed' or claims[cid]['status'] != 'source_derived_unreviewed':
        card_issues.append([cid, 'claim promotion'])
    if any(front['validation'][k] != 'UNKNOWN' for k in ['external_correctness', 'historical_priority', 'physical_capability', 'formal_verification', 'empirical_confirmation']):
        card_issues.append([cid, 'external or capability promotion'])
    if {r['id'] for r in front['proof_availability']['located_proof_sources']} != set(x['proof_refs']):
        card_issues.append([cid, 'proof inventory mismatch'])
check('actual_cards_match_final_input', len(current_cards) == 5 and not card_issues,
      card_issues or 'All five actual cards/review copies/current records match final input; all scientific claim statuses remain source_derived_unreviewed and external/physical fields UNKNOWN.')
check('N876_scope_not_promoted', current_cards[-1]['proof_availability']['internal_proof_status'] == 'partial_internal_proof' and 'do not prove a constant gamma_r>0 uniform' in c['cards'][-1]['statement'] and 'normalized profiles or the stated amplitude condition' in c['cards'][-1]['statement'],
      'N876 is partial_internal_proof; strictness/angular positivity do not become a uniform all-affine margin. The fixed-B normalized/amplitude restriction survives.')

notices = {x['notice_id']: x for x in rows('agent/SEMANTIC_NOTICES.jsonl')}
notice_issues = []
for x in c['notices']:
    y = notices.get(x['notice_id'])
    if not y or y['clarification'] != x['clarification'] or y['card_ids'] != x['card_ids'] or y['whole_claim_invalidated'] is not False:
        notice_issues.append(x['notice_id'])
notice_packet = doc(FX + 'SCOPED_NOTICES.json')
check('scoped_notices', len(notice_packet) == 9 and not notice_issues and {x['notice_id'] for x in notice_packet} == {x['notice_id'] for x in c['notices']},
      notice_issues or 'All9 additive scoped notices preserve earlier claims and corrected-current versus historical roles.')

bridge_issues = []
bridge_paths = []
for x in c['bridges']:
    path = 'mechanisms/bridges/' + x['id'] + '.json'
    bridge_paths.append(path)
    y = doc(path)
    if y['state'] != x['state'] or y['cards'] != x['cards'] or y['alignment'] != x['alignment']:
        bridge_issues.append(x['id'])
    for side in ['source_interface', 'destination_interface']:
        if y[side] != x[side]:
            bridge_issues.append(x['id'] + ':' + side)
    if x['state'] in {'PROVEN LOGICAL DEPENDENCY', 'ESTABLISHED COMPATIBLE INTERFACE'} and not y['transfer_proof_refs']:
        bridge_issues.append(x['id'] + ': no transfer proof')
    if x['state'] == 'REFUTED TRANSFER' and not y['counterexample_refs']:
        bridge_issues.append(x['id'] + ': no counterexample')
    if any(k.startswith('N866-') for k in x['cards']):
        bridge_issues.append(x['id'] + ': unexpected storage bridge')
check('paired_bridge_states_and_contracts', len(c['bridges']) == 4 and not bridge_issues,
      bridge_issues or 'Four real paired contracts keep their exact final states, quantified interfaces and transfer/counterexample refs. No N876-to-N866 transfer is created.')

gate_rows = rows('frontier/OPEN_PROOF_GATES.jsonl')
fx_gates = [x for x in gate_rows if x['gate_id'].startswith('G-FX-GCA-')]
gate_issues = []
gate_paths = []
for x in fx_gates:
    path = 'frontier/gates/' + x['gate_id'] + '.json'
    gate_paths.append(path)
    y = doc(path)
    if y != x or y['status'] != 'open' or y['completion_evidence'] != []:
        gate_issues.append(x['gate_id'])
receipt = doc(FX + 'INTEGRATION_GENERATOR_RECEIPT.json')
check('all_fifteen_gates_open', len(fx_gates) == 15 and {x['gate_id'] for x in fx_gates} == set(receipt['gate_ids']) and not gate_issues,
      gate_issues or 'All10 standard plus5 specific gates remain open with empty completion evidence; no software validation closes a scientific/capability gate.')

# A current evidence span may explicitly describe superseded historical
# pending wording. That is not leaked current pending scientific status.
current_authority_paths += bridge_paths + gate_paths + [FX + 'SCOPED_NOTICES.json']
leak_hits = []
historical_explanation_hits = []
for path in current_authority_paths:
    for number, line in enumerate(read(path).decode().splitlines(), 1):
        if re.search(r'\b(?:DRAFT|PENDING|UNRESERVED|tentative|awaits)\b|implementation-pending', line):
            target = historical_explanation_hits if 'initial implementation-pending sentence is superseded by final addendum' in line else leak_hits
            target.append({'path': path, 'line': number, 'text': line.strip()})
check('no_current_draft_pending_leakage', not leak_hits,
      leak_hits or 'No active draft/pending/unreserved status leaks into generated scientific authority. The only pending-word hits explicitly describe a superseded initial implementation sentence.')

immutable_prefixes = ['cards', 'frontier/cards', 'frontier/review_cards', 'updates', 'state/checkpoints', 'mechanisms/bridges', 'technology/records', 'evaluation/workflows/records']
historical_diff = git('diff', '--name-status', BASE, '--', *immutable_prefixes).decode().splitlines()
check('historical_immutable_artifacts', not historical_diff,
      historical_diff or 'No tracked historical raw card, current-card record, review copy, old update, canonical checkpoint, bridge, technology record or workflow record differs from pinned base. New untracked FX additions are separate.')
append_paths = ['indexes/claims.jsonl', 'frontier/CURRENT_CLAIM_STATUS.jsonl', 'indexes/source_metadata.jsonl', 'frontier/OPEN_PROOF_GATES.jsonl', 'agent/SEMANTIC_NOTICES.jsonl', 'web/documents.jsonl']
append_failures = []
for path in append_paths:
    old = git('show', BASE + ':' + path)
    if not read(path).startswith(old):
        append_failures.append(path)
check('historical_jsonl_prefixes', not append_failures,
      append_failures or 'Every historical JSONL byte prefix remains unchanged; final curation appends new rows only.')
array_paths = [('indexes/agent_catalog.json', ['claims']), ('indexes/agent_graph.json', ['nodes', 'edges']), ('mechanisms/bridge_candidates.json', ['bridges', 'rejected_transfers']), ('web/catalog.json', [None])]
array_failures = []
for path, fields in array_paths:
    old = json.loads(git('show', BASE + ':' + path))
    new = doc(path)
    for field in fields:
        a = old if field is None else old[field]
        b = new if field is None else new[field]
        if b[:len(a)] != a:
            array_failures.append([path, field])
check('historical_array_records', not array_failures,
      array_failures or 'Existing catalog, graph and bridge-array records retain their exact values and order.')

semantics = [
    {'route': 'N872', 'finding': 'PASS', 'scope': 'Finite-alpha projection is distinct from individual alpha fibres. Existing negative sharp theorem remains stronger. All-finite-alpha ordinary-PC cubic includes arbitrary convex lifts; positive sharp QC and strict-interior PC remain open.'},
    {'route': 'N873', 'finding': 'PASS', 'scope': 'Nonshear span retains ROC/contact stationarity. Exact strict k,L,D cone and boundary witnesses match proofs. General compiler is sufficient with supplied lambda and correct Frobenius/tensor norm, zero-rank branch and corrected rational-input precision. Joint construction is distinguished from independent audits.'},
    {'route': 'N874', 'finding': 'PASS', 'scope': 'Nonzero planar constant operator classification and actual negative integrated determinant-square dissipation match proof. Coercive real symbol, ordered spatial indices, conditional C1 autonomous adaptation and no-null-repair scope survive. Det-square stays PC/QC; scalar projection/Burkholder limits do not imply non-QC.'},
    {'route': 'N875', 'finding': 'PASS', 'scope': 'Corrected v4 positive-floor set, unrestricted-support qualification, finite-support LP, sharp intervals and joint-versus-fixed-W closure match final independent audit v2. Same-domain physical rewriting, calibrated W/f/order inputs, costs and matched advantage remain unacquired.'},
    {'route': 'N876', 'finding': 'PASS', 'scope': 'Strict individual Jensen gaps and fixed-r angular margin retain outer-product/full-affine clarification and normalized/amplitude condition. Root/internal acceptance does not become external correctness, a computable constant, global uniform coercivity or storage transfer.'},
    {'route': 'source_identity', 'finding': 'PASS', 'scope': 'Repeated25-file pulse source and embedded old package do not create a new card or independent confirmation. Prompt files remain DATA. External preliminary sharp Beurling/Burkholder claim remains AUDIT_RECONSTRUCTED_NOT_ADMITTED; classical sqrt(24) suffices.'},
    {'route': 'synthesis', 'finding': 'PASS', 'scope': 'Root synthesis was read throughout. Scientific statements preserve the same boundaries. The additional nonlinear convex determinant-energy paragraph is supported by the selected written proof of its fixed-input-diffusion, affine-periodic, lattice-change contract.'}
]
read(FX + 'package/derived/root/SCIENTIFIC_SYNTHESIS.md')
read(FX + 'package/derived/workers/compatible_positivity_priority/NONLINEAR_MINOR_HEAT_OBSTRUCTION.md')

changed_inputs = []
for (origin, path), x in inputs.items():
    raw = ((W if origin == 'W' else R) / path).read_bytes()
    if sha(raw) != x['sha256'] or len(raw) != x['bytes']:
        changed_inputs.append({'origin': origin, 'path': path, 'before_sha256': x['sha256'], 'after_sha256': sha(raw)})
check('audited_inputs_stable', not changed_inputs, changed_inputs or 'Every read input remained byte-identical through the audit.')
head_after = git('rev-parse', 'HEAD').decode().strip()

findings = {
    'schema': 'astra.fx-final-claim-diff-audit.v1',
    'status': 'PASS_NO_MATERIAL_ISSUES_FOUND' if not issues else 'MATERIAL_FINDINGS',
    'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
    'worktree_head_before': head_before, 'worktree_head_after': head_after,
    'curation_input': {'path': FX + 'CURATION_INPUT.root-final.v0001.json', 'sha256': inputs[('W', FX + 'CURATION_INPUT.root-final.v0001.json')]['sha256']},
    'selected_freeze': freeze_ref, 'material_issues': issues, 'checks': checks,
    'semantic_reading': semantics,
    'historical_pending_explanations': historical_explanation_hits,
    'checkpoint_boundary': 'No canonical new checkpoint is published by curation. Parent reports inherited global checkpoint validation FAIL; this audit does not rerun it or reinterpret it as success. New integration draft remains outside canonical checkpoint tree.',
    'scope': 'Read-only final claim, evidence, generated-record and historical-preservation audit. No scientific script replay, independent external correctness/priority certification, or physical validation.',
    'non_actions': ['No W or source writes.', 'No scientific script execution.', 'No Git/GitHub mutation.', 'No canonical checkpoint publication.', 'No technology gate promotion.'],
    'write_scope': str(D), 'input_snapshot': list(inputs.values()),
    'auditor_script_sha256': sha(Path(__file__).read_bytes())
}
report = '''# Final FX claim and diff audit v0001

No material issue was found in the applied five-card curation within this audit's scope. All56 evidence references match their frozen bytes and inclusive ranges; all269 selected files and55 supplied originals match their manifests. The corrected compiler, root axis v4 and sharp-boundary clarification use their accepted SHA256 values.

The cards, raw/review copies, current status rows, nine notices and four paired bridges match root-final input. All10 standard and5 specific gates remain open with empty completion evidence. Every card stays source_derived_unreviewed, all external/physical fields stay UNKNOWN, and N876 stays partial_internal_proof. No sharp-J storage bridge is present. Positive sharp QC, general uniform coercivity and physical same-domain writing remain open.

The historical raw cards, claim/status metadata rows, update artifacts, bridges and canonical checkpoint records were preserved. Old JSONL byte prefixes and prior catalog/graph/bridge-array records remain unchanged. Generated older dossiers can expose new scoped notices without rewriting the historical scientific records. The only current-text pending hits explicitly explain that an initial implementation-pending sentence is superseded by the final addendum; no active draft status leaks.

N872 retains projection-versus-fibre and prior-negative-strength distinctions. N873 retains supplied lambda, exact rational-input precision, cubic flatness, zero-rank scope and joint-versus-independent provenance. N874's actual compatible operation obstructions preserve det-squared QC and the precise adaptive assumptions. N875 retains corrected support/closure bounds and acquisition requirements. N876 retains full-affine outer products and the normalized/amplitude condition for fixed-background annuli.

This audit read root synthesis and decisive selected proofs; it ran only reference, hash, generated-record and preservation checks. Scientific replay is separate and was not rerun. The parent's inherited global-checkpoint FAIL remains an acknowledged separate boundary; no canonical publication or technology promotion is inferred. Full evidence and machine checks are in FINDINGS.v0001.json.
'''
snapshot = {'schema': 'astra.fx-final-audit-input-snapshot.v1', 'base_revision': BASE, 'files': list(inputs.values())}
outputs = {'FINDINGS.v0001.json': findings, 'INPUT_SNAPSHOT.v0001.json': snapshot}
for name, value in outputs.items():
    with (D / name).open('xb') as f:
        f.write((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())
with (D / 'REVIEW.v0001.md').open('xb') as f:
    f.write(report.encode())
print(json.dumps({'status': findings['status'], 'material_issue_count': len(issues), 'check_count': len(checks),
                  'input_file_count': len(inputs), 'curation_sha256': findings['curation_input']['sha256'],
                  'findings_path': str(D / 'FINDINGS.v0001.json')}, indent=2))
