#!/usr/bin/env python3
"""Read-only verification of the source-bound factorial-entropy audit."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def meta(path):
    data=path.read_bytes()
    return {'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
manifest=json.loads((ROOT/'AUDIT_SHA256.json').read_text())
for section,base in [('audit_payloads',ROOT),('original_source_files',ROOT.parent),
                     ('harmonic_dependency_files',ROOT.parent.parent/'rate2_explicit_macro_removal')]:
    for rel,expected in manifest[section].items():
        assert meta(base/rel)==expected,(section,rel)
assert meta(ROOT.parent/'FACTORIAL_ENTROPY_OUTPUT_SERVICE.md')['sha256']=='bc5e25aacdeddf99d5e01a4429bd83dfad5b547a86b653cad0a1fcf161522bd9'
assert (ROOT/'author_replay/CHECK_RESULTS.json').read_bytes()==(ROOT/'inputs/CHECK_RESULTS.json').read_bytes()
assert (ROOT/'author_replay.stdout').read_bytes()==(ROOT/'inputs/check.stdout').read_bytes()
assert (ROOT/'independent_check.stdout').read_bytes()==(ROOT/'INDEPENDENT_CHECK_RESULTS.json').read_bytes()
independent=json.loads((ROOT/'INDEPENDENT_CHECK_RESULTS.json').read_text())
assert independent['assertions']==59739
assert independent['additional_certified_T5_N1e19_total_failure_upper']=='1.1e-10'
receipt=json.loads((ROOT/'REVIEW_RECEIPT.json').read_text())
assert receipt['verdict']=='PASS_NO_SOURCE_REPAIR_REQUIRED'
print(json.dumps({'status':'PASS_READ_ONLY_SOURCE_BOUND_AUDIT',
                  'source_sha256':receipt['source_sha256'],
                  'manifest_sha256':meta(ROOT/'AUDIT_SHA256.json')['sha256'],
                  'audit_payloads':len(manifest['audit_payloads']),
                  'original_source_files':len(manifest['original_source_files']),
                  'harmonic_dependency_files':len(manifest['harmonic_dependency_files'])},indent=2))
