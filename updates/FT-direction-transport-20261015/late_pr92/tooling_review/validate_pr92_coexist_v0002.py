#!/usr/bin/env python3
"""Read-only additive adapter: PR92 validation scoped to its exact owned notices."""
from pathlib import Path
import argparse,contextlib,hashlib,io,json,sys
sys.dont_write_bytecode=True
ORIGINAL='updates/FT-foundational-capability-20261015/validate_intake.py'
EXPECTED='13a7be64800f409115dd101d904cdbf09a3620e2c332368a19b8a680f555d466'
BEFORE="new_notices=[x for x in notices.values() if x['notice_id'].startswith('SN-FT-')]"
AFTER="owned_notice_ids=[x['notice_id'] for x in load(UPDATE/'SCOPED_NOTICES.json')['notices']]\nif len(owned_notice_ids)!=len(set(owned_notice_ids)): fail('duplicate owned notice IDs')\nif not set(owned_notice_ids).issubset(notices): fail('owned notices missing')\nnew_notices=[notices[nid] for nid in owned_notice_ids]"
def adapt(raw):
 if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise ValueError('preserved PR92 validator hash changed; append a new reviewed adapter version')
 source=raw.decode();assert source.count(BEFORE)==1
 return source.replace(BEFORE,AFTER)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--report',type=Path);a=p.parse_args();root=a.repo.resolve()
 if a.report and a.report.resolve().is_relative_to(root):raise ValueError('receipt must remain outside checkout')
 original=root/ORIGINAL;raw=original.read_bytes();source=adapt(raw);capture=io.StringIO()
 with contextlib.redirect_stdout(capture):exec(compile(source,str(original),'exec'),{'__name__':'pr92_preserved_validator_scoped_v0002','__file__':str(original)})
 result=json.loads(capture.getvalue());assert result['status']=='PASS'
 receipt={'schema':'astra.ft-pr92-coexistence-validator.v0002','status':'PASS','original_path':ORIGINAL,'original_sha256':EXPECTED,'adapted_in_memory_sha256':hashlib.sha256(source.encode()).hexdigest(),'change':'Only global FT notice selection replaced by exact owned IDs from immutable PR92 SCOPED_NOTICES. Original validator bytes remain unchanged.','result':result,'scope':'Read-only structural/hash/scope checks only; no exporter, replay, publication or scientific certification.'}
 if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
