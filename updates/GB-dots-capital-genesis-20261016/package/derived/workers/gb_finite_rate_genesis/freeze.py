#!/usr/bin/env python3
"""Integrity-only source receipts and authored artifact freeze; no theorem claim."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parent
DOTS=Path('/Users/harjas/Downloads/Dots')
WORK=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016')
EXPECTED='61389569d6c53b439764f0d148b35b7fa6083eec'
SOURCE_FILES={
    'finite_rate_joint_syndrome_2026-10-15':[
        'HANDOFF.md','single/DERIVATION.md','joint/REPORT.md','joint/DYSON_CONSTRUCTION.md',
        'tracked_control/FOURIER_INTERFACE_ADDENDUM.md','joint/BRIDGE_PRIOR_ART.md'],
    'measurement_memory_handoff_2026-10-15':[
        'START_HERE.md','foundations/deletion_null_detector_bridge/DETECTOR_SUBSET_CANDIDATE.md',
        'foundations/deletion_null_detector_bridge/DETECTOR_SUBSET_AUDIT.md',
        'measurement/DETERMINISTIC_MEASUREMENT_CELL_COROLLARY.md',
        'measurement/UNREAD_MEASUREMENT_REFINEMENT.md',
        'measurement/PARTIAL_DEPHASING_BOUNDARY_THEOREM.md',
        'measurement/MEASUREMENT_COST_CRITERION.md',
        'measurement/FULL_DETECTOR_FOOTPRINT_CLOSURE_OBSTRUCTION.md'],
    'randomizer_control_cost_2026-10-15':[
        'control_cost/REPORT.md','control_cost/OBSTRUCTIONS.md',
        'control_cost/COHERENT_RESIDUAL_AUDIT.md','control_cost/NEXT_GATE.md'],
    'finite_duration_syndrome_addendum_2026-10-15':[
        'README.md','syndrome/SYNDROME_SANDWICH_ALTERNATIVE.md',
        'syndrome/SYNDROME_SANDWICH_AUDIT.md'],
    'qualified_correction_core_addendum_2026-10-15':[
        'HANDOFF.md','core/GATE_INTERFACE_AND_OBSTRUCTION.md'],
    'overlapping_weak_pulses_2026-10-15':[
        'README.md','quantum/SUBSET_CHARACTER_CANDIDATE.md',
        'quantum/SUBSET_MOMENT_AND_LOCALITY_PROOF.md'],
    'coherent_memory_packet_2026-10-15':[
        'originals/PERSISTENT_BATH_THEOREM.md','bridge/BATH_QUANTUM_AUDIT.md'],
}


def receipt(path):
    data=path.read_bytes()
    return {'path':str(path),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}


def main():
    observed_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=WORK,text=True).strip()
    pin=EXPECTED
    checks=json.loads((ROOT/'CHECK_RESULTS.json').read_text())
    assert checks['status']=='PASS'
    sources=[receipt(DOTS/packet/name) for packet,names in SOURCE_FILES.items() for name in names]
    for name in ('AGENTS.md','00_START_HERE.txt',
                 'cards/N881-autonomous-memory-structured-noise-and-bath-interfaces.txt',
                 'updates/FZ-positive-memory-genesis-20261016/package/derived/workers/'
                 'fz_memory_bath_theorem_audit/COUNTERMODELS_AND_SCOPE.md',
                 'updates/FZ-positive-memory-genesis-20261016/package/derived/workers/'
                 'fz_memory_bath_theorem_audit/RECEIVING_SUPPORT_CERTIFICATE_AUDIT.md'):
        item=receipt(WORK/name)
        pinned_bytes=subprocess.check_output(['git','show',f'{EXPECTED}:{name}'],cwd=WORK)
        pinned_sha=hashlib.sha256(pinned_bytes).hexdigest()
        assert item['sha256']==pinned_sha, (name,'requested-pin input differs')
        item['requested_git_pin']=EXPECTED
        item['requested_pin_sha256']=pinned_sha
        item['matches_requested_pin']=True
        sources.append(item)
    inputs={'status':'PINNED','record_kind':'integrity_only','repo_pin':pin,
            'observed_checkout_head_at_freeze':observed_head,
            'head_drift_note':'Requested decisive source bytes verified by git show; worker did not modify checkout.',
            'supplied_files_unchanged_by_worker':True,'files':sources}
    (ROOT/'INPUT_RECEIPTS.json').write_text(json.dumps(inputs,indent=2)+'\n')
    files=[receipt(p) for p in sorted(ROOT.iterdir())
           if p.is_file() and p.name!='FROZEN_MANIFEST.json']
    manifest={'status':'FROZEN','created_utc':datetime.now(timezone.utc).isoformat(),
              'repo_pin':pin,'observed_checkout_head_at_freeze':observed_head,
              'check_status':checks['status'],
              'proof_status':'internal_derivation_external_correctness_unknown',
              'historical_priority':'UNKNOWN','hardware_capability':'NOT_ESTABLISHED',
              'receipt_scope':'hashes establish bytes only; no scientific certification',
              'files':files}
    (ROOT/'FROZEN_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'status':'FROZEN','authored_files':len(files),
                      'pinned_input_files':len(sources),'repo_pin':pin},indent=2))


if __name__=='__main__':
    main()
