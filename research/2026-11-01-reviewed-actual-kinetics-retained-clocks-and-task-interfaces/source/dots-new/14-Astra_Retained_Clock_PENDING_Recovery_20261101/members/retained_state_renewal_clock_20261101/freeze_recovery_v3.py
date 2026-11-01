from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent
old=json.loads((P/'FROZEN_SHA256_RECOVERY_V2.json').read_text())
def rec(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
for n,d in old['dependencies'].items():assert rec(R/n)==d,n
# Keep all earlier payload bytes locally; the two changed historical payloads
# and old descriptor are also explicit current-package members.
for n,d in old['files'].items():assert rec(P/'pre_tree_guard_snapshot'/n)==d,n
hist=['pre_tree_guard_snapshot/FROZEN_SHA256_RECOVERY_V2.json','pre_tree_guard_snapshot/receive_clock.py','pre_tree_guard_snapshot/small_certificate.json']
newfiles=list(old['files'])+['RECEIVER_TREE_REPAIR.md','check_bounded_tree.py','bounded_tree_check_results.json','bounded_tree_stdout.txt','freeze_recovery_v3.py']+hist
out={'schema':'retained_state_renewal_clock_author_freeze.recovery_v3','status':'Post-incident exact-source recovery plus separately preserved bounded-tree receiver repair; 2503+18 author checks PASS; whole executable audit PENDING.','historical_v1_manifest_sha256':'847d4f65a454e209f4857615f8b3f79cff1354cfa794d0bd057cd1fb5afde8c1','historical_recovery_v2_manifest_sha256':'c292c4d2d258c2030b10ad28ac467f33bb5b094f2f245773e502936568b2b6ef','files':{n:rec(P/n)for n in newfiles},'dependencies':old['dependencies']}
(P/'FROZEN_SHA256_RECOVERY_V3.json').write_text(json.dumps(out,indent=2)+'\n')
for n,d in out['files'].items():assert rec(P/n)==d,n
print(json.dumps({'files':len(out['files']),'dependencies':len(out['dependencies']),'manifest':rec(P/'FROZEN_SHA256_RECOVERY_V3.json'),'source':rec(P/'receive_clock.py')},indent=2))
