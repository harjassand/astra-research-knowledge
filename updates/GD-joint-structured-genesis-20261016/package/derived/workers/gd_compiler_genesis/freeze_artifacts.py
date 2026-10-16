#!/usr/bin/env python3
"""Write explicit provenance/resource receipts and a non-self-referential seal."""
import datetime
import hashlib
import json
import platform
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
W = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016')
R = Path('/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-16-joint-structured-genesis-v1')
PIN = '2688d7a383502df4fc1e64001d04bb76e6ec05e5'
observed = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=W, text=True).strip()
now = datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(path):
    data = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data), 'lines': len(data.splitlines())}


local_sources = [
    (W / 'AGENTS.md', 'Read full navigation instructions; original sources were treated as data.'),
    (W / '00_START_HERE.txt', 'Read full task-first retrieval/assumption requirements.'),
    (W / 'frontier/dossiers/N881.txt', 'Read current scope, notices, open gates, conditional receiving interfaces and exact proof routes; combined initial result truncated later route text.'),
    (W / 'frontier/dossiers/N894.txt', 'Read current scope, notices, comparator limits and exact proof routes.'),
    (W / 'cards/N881-autonomous-memory-structured-noise-and-bath-interfaces.txt', 'Read full card; source-derived-unreviewed status retained.'),
    (W / 'cards/N894-peak-constrained-control-and-fixed-refresh-minimax.txt', 'Read full card; comparator model limits retained.'),
    (R / 'originals/compiler/STRUCTURED_COMPILER.md', 'Read Sections 1-8 across the initial output and targeted Sections 5-8; starting criterion, sparse Pauli recipe, four-Kraus edge and coefficient-conversion limitation are supplied data.'),
    (R / 'originals/pair_clock/regularization_radius_audit/AUDIT.md', 'Read full audit; generic 2nu/d^2 radius is a separate error class and fixed-rate contract.'),
    (W / 'updates/FZ-positive-memory-genesis-20261016/package/derived/workers/fz_signed_gram_audit/SIGNED_GRAM_AUDIT.md', 'Read lines 1-210 explicitly; initial whole-file request had combined output truncation. Used exact normalization/range/gauge conventions, not a full independent audit claim.'),
    (W / 'updates/FZ-positive-memory-genesis-20261016/package/derived/workers/fz_memory_structured_noise_genesis/STRUCTURED_GRAM_REGULARIZATION.md', 'Whole-file request returned visible structured-criterion, jump-replacement, locality and conditional receiving excerpts in a truncated combined result. No assertion that all omitted content was read.'),
    (W / 'updates/FZ-positive-memory-genesis-20261016/package/derived/workers/fz_memory_bath_theorem_audit/RECEIVING_SUPPORT_CERTIFICATE_AUDIT.md', 'Read full 120-line support/quantifier audit. Conditional interface only; did not externally validate classical probability or topology.'),
    (W / 'updates/FZ-positive-memory-genesis-20261016/package/derived/workers/fz_memory_quantum_audit/PERSISTENT_BATH_THEOREM.md', 'Read lines 1-150: universal schedule, fixed decoder, finite bath, Kraus-span and input-independent location-law requirements.'),
]
source_entries = []
for path, scope in local_sources:
    entry = dict(digest(path), read_scope=scope)
    if path.is_relative_to(W):
        pinned_bytes = subprocess.check_output(['git', 'show', f'{PIN}:{path.relative_to(W)}'], cwd=W)
        entry['assigned_pin_sha256'] = hashlib.sha256(pinned_bytes).hexdigest()
        entry['matches_assigned_pin'] = entry['sha256'] == entry['assigned_pin_sha256']
        if not entry['matches_assigned_pin']:
            raise SystemExit(f'Input bytes differ from assigned pin: {path}')
    source_entries.append(entry)
source_receipt = {
    'recorded_utc': now,
    'worktree': str(W), 'assigned_pin': PIN, 'initial_observed_pin': PIN, 'final_observed_head': observed,
    'revision_drift_note': 'HEAD advanced during concurrent root work. Every read W input is separately checked byte-for-byte against the assigned pin; no worktree mutation by this worker.',
    'input_contract': 'Read-only supplied mathematical sources. No physical noise or architecture acquisition.',
    'integrity_scope': 'Byte hashes at freeze time and observed Git revision; hashes do not certify mathematics, priority, physical capability or preregistration.',
    'local_sources': source_entries,
    'primary_web_reads': [
        {'url': 'https://arxiv.org/pdf/1906.00693v1', 'served_url': 'https://arxiv.org/pdf/1906.00693', 'title': 'Quantum renewal processes', 'author': 'Bassano Vacchini', 'version_verified_in_pdf': 'arXiv:1906.00693v1, 3 June 2019', 'read_scope': 'Title/version, Eq. (11), Eqs. (12)-(16), continuous-between-event comparison; extracted PDF text viewed, original PDF bytes not saved or hashed.'},
        {'url': 'https://arxiv.org/abs/1906.00693', 'read_scope': 'Abstract/metadata inspected for version context.'},
        {'url': 'https://arxiv.org/html/2604.18533v2', 'title': 'Hamiltonian dynamics from pure dissipation', 'authors': 'Zhong-Xia Shang; Daniel Stilck França', 'version': 'v2, 4 October 2026', 'read_scope': 'Eqs. (4), (19)-(20) and local/gauge surrounding discussion; primary standard ingredient only; extracted HTML viewed, bytes not saved or hashed.'},
        {'url': 'https://arxiv.org/html/1906.00693v2', 'result': 'Tool internal error; no source claim relies on this unavailable HTML.'},
    ],
    'provenance': {
        'worker_derived': ['Direct nontraceless arbitrary-unitary pair compiler', 'Fixed unitary dictionary signed replacement rate with PSD quadratic improvement', 'Exact actual one-mode affine Pauli replacement minimax', 'Four-Kraus joint Pauli edge/product-drift compiler', 'Collision-free aggregate minimax lower bound against every fixed CPTP baseline'],
        'root_communication': 'Root investigator supplied the sharper two-unitary polar contraction lemma; independently reconstructed and tested here. No other worker files were read.',
        'peer_worker_reads': False,
        'producer_scientific_scripts_executed': False,
    },
}
(HERE / 'SOURCE_RECEIPT.json').write_text(json.dumps(source_receipt, indent=2) + '\n')
checks = json.loads((HERE / 'CHECKS.json').read_text())
resource_receipt = dict(checks['resource_receipt'])
resource_receipt.update({
    'recorded_utc': now, 'all_checks_pass': checks['all_checks_pass'],
    'test_command': f'python3 {HERE / "check_compiler_genesis.py"}',
    'freeze_command': f'python3 {HERE / "freeze_artifacts.py"}',
    'external_human_or_account_outreach': False,
    'subagents_spawned': False,
    'writes_confined_to': str(HERE),
    'source_or_worktree_mutations': False,
    'initial_scipy_probe': 'SciPy unavailable in system Python; no installation attempted and no checks require it.',
    'physical_resources': {
        'additional_floor_rate': 'For one replacement, <=3a epsilon+0.5 epsilon^2; actually installed unitary channels required.',
        'proposal_rate': 'For one replacement, <=4a epsilon+epsilon^2 with one full error-union PSD clock; pairwise alternative <=4a epsilon+2epsilon^2. All guard incidence and supports charged.',
        'dictionary_size': '<=2(m+1) unitary labels for m fixed error operators.',
        'matrix_construction': 'Dense local polar/spectral decompositions may require O(d_X^3) arithmetic and O(d_X^2) storage; unitary synthesis/control is not supplied.',
        'physical_acquisition': 'None. Dictionary, coefficient promises, exact floors and completed correction model are conditional inputs.',
        'useful_threshold_or_advantage': 'UNKNOWN; inherited classical constants and physical qualification remain open.',
    },
})
(HERE / 'RESOURCE_RECEIPT.json').write_text(json.dumps(resource_receipt, indent=2) + '\n')
names = ['PROOFS.md', 'REPORT.md', 'check_compiler_genesis.py', 'CHECKS.json', 'freeze_artifacts.py', 'SOURCE_RECEIPT.json', 'RESOURCE_RECEIPT.json']
frozen = {
    'schema': 'gd-compiler-genesis-freeze-v1', 'recorded_utc': now,
    'worker': 'gd_compiler_genesis', 'worktree_pin': PIN, 'final_observed_worktree_head': observed,
    'all_W_inputs_match_assigned_pin': all(x.get('matches_assigned_pin', True) for x in source_entries),
    'status': 'COMPLETE_CONDITIONAL_MATHEMATICS_AND_FINITE_CHECKS',
    'external_correctness': 'UNKNOWN', 'historical_priority': 'UNKNOWN', 'physical_capability': 'UNKNOWN',
    'claims': [
        {'id': 'GD-COMPILER-UNITARY-PAIR', 'status': 'internally_derived', 'scope': 'Fixed arbitrary unitary pairs, complex disk coefficient, five Kraus, rate4M, union support.'},
        {'id': 'GD-COMPILER-CORRECTION-DICTIONARY', 'status': 'internally_derived_conditional', 'scope': 'Specified affine error dictionary and supplied coefficient bounds; fixed floor, rate4a epsilon+epsilon^2 on full dictionary union; pairwise option4a epsilon+2epsilon^2. No Pauli conversion factor.'},
        {'id': 'GD-COMPILER-AFFINE-PAULI-MINIMAX', 'status': 'internally_derived', 'scope': 'Actual aP->aP+delta Q, complex coefficient disk |delta|<=epsilon, distinct Pauli P,Q; all fixed CPTP baselines; exact rate4a epsilon if epsilon<=a, else(a+epsilon)^2.'},
        {'id': 'GD-COMPILER-COLLISION-FREE-MINIMAX', 'status': 'internally_derived', 'scope': 'All fixed CPTP baselines; collision-free Pauli edge/product catalog; independent edge disks and product-H boxes; rate sum(2M+2sqrt(M^2+u^2)).'},
    ],
    'all_checks_pass': checks['all_checks_pass'],
    'artifacts': [digest(HERE / name) for name in names],
    'self_hash_omitted': True,
    'integrity_only_notice': 'Manifest hashes identify exact local artifacts, not scientific validity, external review, historical novelty or physical acquisition.',
}
(HERE / 'FROZEN.json').write_text(json.dumps(frozen, indent=2) + '\n')
print(json.dumps({'frozen': str(HERE / 'FROZEN.json'), 'sha256': digest(HERE / 'FROZEN.json')['sha256'], 'all_checks_pass': checks['all_checks_pass'], 'artifacts': len(names)}, indent=2))
