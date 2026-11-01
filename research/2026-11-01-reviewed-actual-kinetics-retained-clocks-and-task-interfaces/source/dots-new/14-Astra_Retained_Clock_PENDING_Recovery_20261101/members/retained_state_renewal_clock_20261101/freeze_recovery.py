from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent
old=json.loads((P/'FROZEN_SHA256_PRE_INCIDENT.json').read_text())
def rec(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
assert rec(P/'FROZEN_SHA256_PRE_INCIDENT.json')['sha256']=='847d4f65a454e209f4857615f8b3f79cff1354cfa794d0bd057cd1fb5afde8c1'
for n,d in old['dependencies'].items():assert rec(R/n)==d,n
newfiles=list(old['files'])+['FROZEN_SHA256_PRE_INCIDENT.json','RECOVERY_COMPARISON.json','WORKSPACE_INCIDENT_RECOVERY.md','recovery_check_before_source_install.txt','freeze_recovery.py','audit_global_odd_renewal_recovery_20261101_0118/SOURCE_BOUND_ACCEPTANCE.md']
out={'schema':'retained_state_renewal_clock_author_freeze.recovery_v2','status':'Fresh post-incident author replay PASS; whole executable audit PENDING. Exact original scientific/code sources, three honestly regenerated timing-bearing files.','historical_manifest_sha256':rec(P/'FROZEN_SHA256_PRE_INCIDENT.json')['sha256'],'files':{n:rec(P/n)for n in newfiles},'dependencies':old['dependencies']}
(P/'FROZEN_SHA256_RECOVERY_V2.json').write_text(json.dumps(out,indent=2)+'\n')
for n,d in out['files'].items():assert rec(P/n)==d,n
print(json.dumps({'files':len(out['files']),'dependencies':len(out['dependencies']),'manifest':rec(P/'FROZEN_SHA256_RECOVERY_V2.json')},indent=2))
