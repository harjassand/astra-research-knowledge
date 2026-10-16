#!/usr/bin/env python3
"""Hash only the sources actually consulted and freeze this worker directory."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import subprocess

HERE=Path(__file__).resolve().parent
R=HERE.parent.parent
ROOT=R.parent.parent
W=ROOT/'work/astra-positive-memory-20261016'
PIN='2688d7a383502df4fc1e64001d04bb76e6ec05e5'
FILES=[
    (W/'AGENTS.md','complete'),
    (W/'00_START_HERE.txt','complete'),
    (W/'frontier/dossiers/N881.txt','current scope and gates read; navigation routes inspected'),
    (R/'originals/pair_clock/sources_and_handoff/PRINCIPAL_PAIR_THEOREM.md','complete'),
    (R/'originals/pair_clock/sources_and_handoff/UNIVERSAL_PAIR_CLOCK_ENVELOPE.md','complete'),
    (R/'originals/pair_clock/sources_and_handoff/STOPPED_TORUS_REPLAY.md','complete'),
    (R/'originals/pair_clock/sources_and_handoff/REGULARIZED_ROBUST_MEMORY.md','complete'),
    (R/'originals/pair_clock/sources_and_handoff/COARSE_LSS_EXCERPTS.txt','complete extract; not whole original members'),
    (R/'originals/pair_clock/sources_and_handoff/CLUSTER_IMPORT_EXCERPT.txt','complete extract; not whole original member'),
    (R/'originals/pair_clock/sources_and_handoff/DECODER_EXCERPTS.txt','complete extracts; not whole original members'),
    (R/'originals/pair_clock/sources_and_handoff/AUDIT_HANDOFF.md','complete'),
    (R/'originals/pair_clock/pair_clock_adversary/REVIEW.md','complete'),
    (R/'originals/pair_clock/regularization_radius_audit/AUDIT.md','radius proof and scope; not an independent source audit here'),
    (R/'originals/compiler/STRUCTURED_COMPILER.md','complete'),
]
EXPECTED={
    'PRINCIPAL_PAIR_THEOREM.md':'d14cbf73c598237c5f8913bdb9775317d3831771b4916bc0c0b494ee52bc2edd',
    'UNIVERSAL_PAIR_CLOCK_ENVELOPE.md':'d837200b12c7c2f4b725e0a850dbb7aa5033c14cfa6e55a9d188c94bd241fb09',
    'STOPPED_TORUS_REPLAY.md':'35e38d583ef446266177b7cc6907700b091f2e5359b8ba738fc83b8be9f61b8d',
    'REGULARIZED_ROBUST_MEMORY.md':'cff378f1af5e958b300d5f868191c1a85c5bace6d43ab192c71e3872f7f84225',
}

def receipt(path):
    data=path.read_bytes()
    return dict(path=str(path),byte_count=len(data),sha256=sha256(data).hexdigest())

if __name__=='__main__':
    actual_pin=subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD'],text=True).strip()
    assert actual_pin==PIN
    sources=[]
    for path,read_scope in FILES:
        item=receipt(path)
        item['read_scope']=read_scope
        if path.name in EXPECTED:
            assert item['sha256']==EXPECTED[path.name], path
            item['matches_preserved_audit_hash']=True
        sources.append(item)
    for name in ['ht_v2.pdf','ht_v2.html','RETRIEVAL_RECEIPTS.json']:
        sources.append({**receipt(HERE/'primary'/name),'read_scope':'primary acquisition; exact theorem text checked through web source interface'})
    manifest=dict(schema='gd_memory_receiving_source_manifest_v1',generated_at_utc=datetime.now(timezone.utc).isoformat(),
                  checkout=str(W),required_pin=PIN,actual_pin=actual_pin,sources=sources,
                  memory_use=dict(path='/Users/harjas/.codex/memories/MEMORY.md',scope='retrieval discipline and model distinction only; not a mathematical premise',
                                  relevant_lines='29-31,44-46',rollout_id='01a14073-fc31-7c03-b84d-c4536b82e6b9'))
    (HERE/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    checks=json.loads((HERE/'checks.json').read_text())
    assert checks['all_checks_passed']
    artifacts=[]
    for path in sorted(HERE.rglob('*')):
        if path.is_file() and path.name!='FROZEN.json' and '__pycache__' not in path.parts:
            item=receipt(path)
            item['path']=str(path.relative_to(HERE))
            artifacts.append(item)
    frozen=dict(schema='gd_memory_receiving_frozen_v1',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
                worker='gd_memory_receiving',status='NEW_LOCAL_CLOSURE_CONDITIONAL_GLOBAL_TRANSFER',
                report='REPORT.md',source_manifest='SOURCE_MANIFEST.json',obligations='OBLIGATIONS.json',resources='RESOURCES.json',
                checkout_pin=PIN,originals_read_only=True,no_installs=True,no_spawn=True,no_outreach=True,
                independent_external_validation=False,practical_memory_claim=False,
                finite_checks_passed=True,LSS_original_pages='NOT_ACQUIRED',HT_version='2212.08437v2',
                artifacts=artifacts)
    (HERE/'FROZEN.json').write_text(json.dumps(frozen,indent=2)+'\n')
    print(json.dumps(dict(status=frozen['status'],source_count=len(sources),artifact_count=len(artifacts),
                          report=str(HERE/'REPORT.md')),indent=2))
