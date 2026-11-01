"""Bind the explicit accepted audit allowlist, never arbitrary working-directory files."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((P/'FINAL_INPUT_BINDING.json').read_text())
for row in source['files']:
 p=P/'final_source'/row['path'];assert p.stat().st_size==row['bytes']and sha(p)==row['sha256']
math=P/'mathematical_audit';assert sha(math/'FINAL_AUDIT_MANIFEST.json')=='8be681223cb20050a8a420a9bf035b1d34a4af2e12e6a01622787349d5dee365'
for row in json.loads((math/'FINAL_AUDIT_MANIFEST.json').read_text())['files']:
 p=math/row['path'];assert p.stat().st_size==row['bytes']and sha(p)==row['sha256']
core=['WHOLE_AUDIT.md','README_AUDIT.md','AUDIT_RECEIPT.json','FINAL_INPUT_BINDING.json','INPUT_BINDING.json','REPAIR_V1_INPUT_BINDING.json','ORIGINAL_DEFECTS.json','REPAIR_V1_DEFECTS.json','INDEPENDENT_FIXTURE_CERTIFICATE.json','INDEPENDENT_REPLAY_RECEIPT.json','FINAL_AUTHOR_REPLAY_RECEIPT.json','WHOLE_RECEIVING_RESULTS.json','RESOURCE_INTERFACE_RESULTS.json','HUGE_FOSTER_RESULTS.json','WHOLE_RECEIVING_STDOUT.json','RESOURCE_INTERFACE_STDOUT.json','HUGE_FOSTER_STDOUT.json','independent_receiver.py','check_whole_receiving.py','check_resource_interfaces.py','check_huge_foster.py','finalize_audit.py']
files=core+['final_source/'+r['path']for r in source['files']]+['mathematical_audit/'+n for n in json.loads((math/'ARTIFACT_ALLOWLIST.json').read_text())['members']]
assert len(files)==len(set(files))
members=sorted(files+['ARTIFACT_ALLOWLIST.json','FINAL_AUDIT_MANIFEST.json'])
allow={'scope':'Final v3 mathematical/constructor/independent-receiving whole PASS only. Historical bindings/defects are not acceptance of old executables.','member_count':len(members),'members':members,'source_members':27,'mathematical_receipt_members':11}
(P/'ARTIFACT_ALLOWLIST.json').write_text(json.dumps(allow,indent=2,sort_keys=True)+'\n')
bound=sorted(files+['ARTIFACT_ALLOWLIST.json'])
manifest={'status':'SCOPED_WHOLE_PASS_V3','author_manifest_sha256':source['manifest_sha256'],'bound_file_count':len(bound),'files':[{'path':n,'bytes':(P/n).stat().st_size,'sha256':sha(P/n)}for n in bound]}
(P/'FINAL_AUDIT_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
for n in ['WHOLE_AUDIT.md','AUDIT_RECEIPT.json','ARTIFACT_ALLOWLIST.json','FINAL_AUDIT_MANIFEST.json']:print(n,sha(P/n))
print('strict_members',len(members),'manifest_bound',len(bound))
