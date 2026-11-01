from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent
old=json.loads((P/'FROZEN_SHA256_RECOVERY_V3.json').read_text())
def rec(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
assert rec(P/'FROZEN_SHA256_RECOVERY_V3.json')['sha256']=='d4a87d9995113c14b78646aeca51b8b83121e1ce3f5b81dfe4c64af6772308c7'
for n,d in old['dependencies'].items():assert rec(R/n)==d,n
hist=['tree_guard_v3_history/FROZEN_SHA256_RECOVERY_V3.json','tree_guard_v3_history/receive_clock.py','tree_guard_v3_history/check_bounded_tree.py']
for n in hist:
 original=n.split('/',1)[1]
 if original!='FROZEN_SHA256_RECOVERY_V3.json':assert rec(P/n)==old['files'][original],n
newfiles=list(old['files'])+['RECEIVER_ALLOCATION_REPAIR.md','freeze_recovery_v4.py']+hist
out={'schema':'retained_state_renewal_clock_author_freeze.recovery_v4','status':'Fresh 2503+22 author checks PASS; whole executable audit PENDING. Original scientific formulas unchanged; separately preserved iterative proof-tree recursion and pending-allocation guards.','historical_v1_manifest_sha256':'847d4f65a454e209f4857615f8b3f79cff1354cfa794d0bd057cd1fb5afde8c1','historical_recovery_v2_manifest_sha256':'c292c4d2d258c2030b10ad28ac467f33bb5b094f2f245773e502936568b2b6ef','historical_recovery_v3_manifest_sha256':'d4a87d9995113c14b78646aeca51b8b83121e1ce3f5b81dfe4c64af6772308c7','files':{n:rec(P/n)for n in newfiles},'dependencies':old['dependencies']}
(P/'FROZEN_SHA256_RECOVERY_V4.json').write_text(json.dumps(out,indent=2)+'\n')
for n,d in out['files'].items():assert rec(P/n)==d,n
print(json.dumps({'files':len(out['files']),'dependencies':len(out['dependencies']),'manifest':rec(P/'FROZEN_SHA256_RECOVERY_V4.json'),'source':rec(P/'receive_clock.py')},indent=2))
