"""Seal checkpoint metadata without modifying frozen mathematical reports."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / 'work/state'
PACKET = ROOT / 'outputs/bounded-capacity-classicality'

def read(path):
    return json.loads(path.read_text())

def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

copies = {
    'FULL_ENDPOINT_EXPOSED_AUDIT.txt': 'work/agents/covariant_review_sol/cycle03_capacity_exposed/POST_EXPOSURE_AUDIT.txt',
    'ENDPOINT_BLIND_BASELINE.txt': 'work/agents/covariant_review_sol/cycle03_capacity_blind/BLIND_BASELINE.txt',
    'ROOT_CAPACITY_CHAIN_REVIEW.txt': 'work/agents/root_cycle03/ROOT_CAPACITY_CHAIN_REVIEW.txt',
    'ENDPOINT_AUDIT_FREEZE.json': 'work/agents/covariant_review_sol/cycle03_capacity_exposed/FINAL_FREEZE.json',
    'ENDPOINT_EXACT_CONSTANT_CHECKS.json': 'work/agents/covariant_review_sol/cycle03_capacity_exposed/EXACT_CONSTANT_CHECKS.json',
    'PRIOR_ART_REPORT.txt': 'work/agents/broadcast_literature_luna/cycle03_consequences/REPORT.txt',
}
manifest = read(PACKET / 'MANIFEST.json')
rows = {row['path']: row for row in manifest['files']}
for name, source in copies.items():
    shutil.copyfile(ROOT / source, PACKET / name)
    rows[name] = {'path': name, 'source': source, 'sha256': hashlib.sha256((PACKET / name).read_bytes()).hexdigest()}
manifest['files'] = list(rows.values())
manifest['status'] = 'complete internal proof; fresh full endpoint exposed adversarial audit PASS; blind endpoint baseline UNKNOWN; external/formal/priority unverified'
save(PACKET / 'MANIFEST.json', manifest)

p = PACKET / 'README.txt'
s = p.read_text().replace('Cycle03 local candidate proof packet — fresh endpoint review pending.', 'Cycle03 local candidate proof packet — full endpoint internal audit PASS.')
s = s.replace('Proof status: complete internal model-assisted proof with independently reconstructed main mechanism and separate stage audits; fresh full-endpoint adversarial review pending at this draft.', 'Proof status: complete internal model-assisted proof with independently reconstructed main mechanism, separate stage audits, root reconstruction, and a fresh full-endpoint exposed adversarial audit PASS. The endpoint reviewer\'s theorem-first phase remained UNKNOWN; ENDPOINT_BLIND_BASELINE.txt preserves that result. FULL_ENDPOINT_EXPOSED_AUDIT.txt records the later twelve-step audit after proof exposure. The independent theorem-first proof applies to the universal comparison mechanism, not to the entire capacity endpoint.')
s += '\nBoundary clarification: when the centralization parameter Xi=0 and the raw half-error u=1, use the trivial e<=1 branch; alternatively take the limit through the general continuous Petz bound. The final exposed audit spells out this harmless boundary branch without altering the frozen originating proof.\n'
s = s.replace('checks20', 'checks 20').replace('and3 ', 'and 3 ')
p.write_text(s)

p = STATE / 'STATUS_DRAFT.txt'
s = p.read_text().replace('A fresh complete-endpoint adversarial audit is PENDING at this draft.', 'A fresh complete-endpoint exposed adversarial audit passed all twelve reductions, the explicit constant, and the zero-error limit. Its earlier theorem-first baseline remained UNKNOWN and is preserved separately.')
s = s.replace('General endpoint: complete assembled proof and root/independent constant checks; fresh full-chain review PENDING.', 'General endpoint: complete assembled proof, root/independent constant checks, and fresh full-chain exposed adversarial review PASS. The endpoint itself was not independently derived during its theorem-first phase.')
for old, new in [('foundational10/10', 'foundational 10/10'), ('the29-claim', 'the 29-claim'), ('prior719-manuscript/372-family', 'prior 719-manuscript/372-family'), ('factor8', 'factor 8'), ('factor2', 'factor 2'), ('necessary;4', 'necessary; 4'), ('ASTRA pin:39', 'ASTRA pin: 39'), ('math pin:fd', 'math pin: fd')]:
    s = s.replace(old, new)
p.write_text(s)

p = STATE / 'CLAIM_LEDGER.json'
d = read(p)
d['checkpoint'] = 'cycle03 complete local checkpoint; ultimate foundational objective OPEN'
row = next(c for c in d['claims'] if c['id'] == 'BCAST-CAPACITY-027')
row['status'] = 'complete assembled internal proof; component reconstructions, root review, and fresh twelve-step full endpoint exposed adversarial audit PASS'
row['limitations'][0] = 'Internal model-assisted proof; endpoint theorem-first baseline UNKNOWN, subsequent exposed audit PASS; independent theorem-first derivation applies to the universal core'
for source in [copies['FULL_ENDPOINT_EXPOSED_AUDIT.txt'], copies['ENDPOINT_BLIND_BASELINE.txt']]:
    if source not in row['evidence']:
        row['evidence'].append(source)
save(p, d)

(STATE / 'CYCLE_03_PENDING.txt').write_text('CYCLE 03 — CLOSED CHECKPOINT\nAll 25 worker assignments have final reports; zero pending reports. The complete capacity endpoint, all reductions, explicit constant 400 and zero-error limit passed the fresh exposed internal audit. The separate theorem-first endpoint baseline remains UNKNOWN. Core independent derivation, graph audit, permanence audit and bounded primary-source comparisons are complete.\nNo formal kernel replay, external certification, historical priority or 10/10 designation is established. Ultimate objective OPEN. No publication, canonical merge or external message occurred.\nOnly the coordinator is active for packaging. Conservative reservation 10/30; historical all-worker simultaneous upper bound 26/30.\n')
with (STATE / 'CYCLE_03.txt').open('a') as f:
    f.write('\nCLOSURE: all admitted work and the bounded-capacity escalation are complete at this checkpoint. The main core has an independent theorem-first proof; the full endpoint has a preserved UNKNOWN theorem-first baseline followed by a fresh exposed PASS audit. All 25 workers completed. The current ledger and checkpoint03 status supersede earlier pending labels without modifying frozen proofs. The ultimate foundational objective remains OPEN.\n')

p = STATE / 'dispatch.json'
d = read(p)
d['active_task_names'] = []
d['active_session_ids'] = ['01a11bf8-98a4-7342-b565-17a798a3759f']
d['active_as_of_utc'] = datetime.now(timezone.utc).isoformat()
d['active_status_source'] = 'Live collaboration.list_agents confirms all 25 workers completed; only coordinator remains active for packaging. No descendants.'
save(p, d)

p = STATE / 'cycle03_frozen_hashes.json'
d = read(p)
d['files'].update({
    copies['FULL_ENDPOINT_EXPOSED_AUDIT.txt']: '6a2faec427a947324d746cb64a152ff8994c1509c67d379deaa6df3d2789d23b',
    copies['ENDPOINT_AUDIT_FREEZE.json']: '7a4dd65ac1b70226caaeaa6657585b8e024ecf776eac23be06ba66a85b351fba',
    'work/agents/quadratic_dilation_sol/cycle03_capacity/PROOF_STAGE_AUDIT.txt': '8bc86d8e68b9213d7573dde2808b49adeb6bb11badf9d926beb676851fab66a5',
})
for name, expected in d['files'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
save(p, d)
print('Metadata finalized; 16 frozen identities verified. Resource snapshot and inventory remain next.')
