"""Verify the frozen package, optionally replay its two independent test programs."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
p=argparse.ArgumentParser();p.add_argument('--run-tests',action='store_true');a=p.parse_args()
rows=[]
for line in (HERE/'SHA256SUMS').read_text().splitlines():
 sha,name=line.split('  ',1);file=(ROOT/name).resolve()
 if not file.is_relative_to(ROOT):raise ValueError('Unsafe path '+name)
 if not file.is_file():raise FileNotFoundError(file)
 actual=hashlib.sha256(file.read_bytes()).hexdigest()
 if actual!=sha:raise ValueError('Hash mismatch '+name)
 rows.append(name)
update=json.loads((HERE/'CITATION_UPDATE.json').read_text())
proof=(HERE/'PROOF.md').read_bytes();marker=update['body_boundary_marker'].encode()
body,sep,rest=proof.partition(marker)
assert sep and hashlib.sha256(body).hexdigest()==update['previous_reviewed_full_proof_sha256']
assert hashlib.sha256(proof).hexdigest()==update['updated_full_proof_sha256']
reviewed=(ROOT/update['independent_review_record']).read_text().split()[0]
assert reviewed==update['previous_reviewed_full_proof_sha256']
out={'hashes_verified':len(rows),'status':'PASS','reviewed_mathematical_body_unchanged':True,'tests':[]}
if a.run_tests:
 for folder,script in [('mps_gns_gap_extension_20261105','check_embedding.py'),('mps_gns_gap_second_audit_20261105','check_uniform_constants.py')]:
  t=time.perf_counter();r=subprocess.run([sys.executable,script],cwd=ROOT/folder,capture_output=True,text=True)
  item={'script':folder+'/'+script,'returncode':r.returncode,'seconds':time.perf_counter()-t}
  if r.returncode:print(r.stdout+r.stderr);raise RuntimeError(item)
  out['tests'].append(item)
 x=json.loads((HERE/'embedding_results.json').read_text())
 assert len(x['records'])==12 and all(all(r['checks'].values()) for r in x['records'])
 y=json.loads((ROOT/'mps_gns_gap_second_audit_20261105/uniform_constants_results.json').read_text())
 assert sum(len(s['cases']) for s in y)==60
 out['full_operation_cases_passed']=12;out['independent_uniform_cases_passed']=60
print(json.dumps(out,indent=2))
