#!/usr/bin/env python3
"""Integrity only. Does not run any scientific computation or certify proofs."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'MANIFEST.json').read_text())
count=0
for item in manifest['files']:
    rel=Path(item['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    p=ROOT/rel
    assert p.is_file(),str(rel)
    data=p.read_bytes()
    assert len(data)==item['bytes'],str(rel)
    assert hashlib.sha256(data).hexdigest()==item['sha256'],str(rel)
    count+=1
required=[
 'inputs/max/Astra_Amplification_Cycle9_MAX_20261022/evaluator/meta_representation/source/src/active_ports.py',
 'inputs/pro3/Astra_Amplification_Cycle9_PRO3_20261022/code/exact_checks.py',
 'inputs/pro3/Astra_Amplification_Cycle9_PRO3_20261022/evidence/exact/EXACT_INPUTS.json',
 'inputs/pro3/Astra_Amplification_Cycle9_PRO3_20261022/evidence/exact/expansion_native32.json',
 'original_dependencies/Astra_Amplification_Cycle5_PRO2_20261022.zip',
]
assert all((ROOT/p).is_file() for p in required)
print(json.dumps({'status':'PASS','checked_payload_files':count,
 'required_native_inputs_present':True,
 'scope':'Source integrity and portable paths only; no scientific replay, proof certification or novelty claim.'}))

