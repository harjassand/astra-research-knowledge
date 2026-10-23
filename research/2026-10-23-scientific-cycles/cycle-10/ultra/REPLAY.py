#!/usr/bin/env python3
"""Verify immutable payloads; run only four new Cycle10 bounded admissions."""
from pathlib import Path
import argparse,hashlib,json,math,resource,shutil,subprocess,sys,tempfile,time
TIMINGS={'cpu_seconds','wall_seconds','runtime_seconds','process_cpu_seconds'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stable(v):
 if isinstance(v,dict):return {k:stable(x) for k,x in v.items() if k not in TIMINGS}
 if isinstance(v,list):return [stable(x) for x in v]
 return v
def equal(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,float):return math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-11)
 if isinstance(a,list):return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
 if isinstance(a,dict):return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
 return a==b
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 src=Path(__file__).resolve().parent;start=time.perf_counter();initial=resource.getrusage(resource.RUSAGE_CHILDREN)
 manifest=json.loads((src/'MANIFEST.json').read_text());before={}
 for e in manifest['payloads']:
  f=src/e['path'];assert f.stat().st_size==e['bytes'];assert sha(f)==e['sha256'];before[e['path']]=e['sha256']
 proof=manifest['principal_proof_sha256'];assert sha(src/'PROOF.txt')==proof
 for n in manifest['actual_principal_audits']:assert proof in (src/n).read_text()
 native=src/'sources/Astra_Amplification_Cycle9_ULTRA_20261022.zip'
 assert native.stat().st_size==10604540 and sha(native)=='0eb683200712cf4313d7e55da66df83ef02fece741e5c2633701a8be19e75925'
 jobs=[]
 with tempfile.TemporaryDirectory(prefix='astra_cycle10_relocated_') as td:
  dst=Path(td)/'source';shutil.copytree(src,dst)
  specs=[('calculations/principal/replay.py','calculations/principal/RESULT.json'),('studies/converse/replay.py','studies/converse/RESULT.json'),('studies/converse/resource_checks.py','studies/converse/RESOURCE_RESULT.json'),('studies/challenge/replay.py','studies/challenge/REPLAY_RESULT.json')]
  for script,result in specs:
   tick=time.perf_counter();done=subprocess.run([sys.executable,str(dst/script)],cwd=dst,capture_output=True,text=True,check=True,timeout=180)
   assert equal(stable(json.loads((src/result).read_text())),stable(json.loads((dst/result).read_text()))),script
   jobs.append({'script':script,'status':'PASS','result_reproduced':True,'wall_seconds':time.perf_counter()-tick,'comparison':'Exact rational/count/hash/type structure; floating entropy admissions rel/abs1e-11; timing excluded','stdout_summary':done.stdout[:1200].strip()})
 assert all(sha(src/n)==h for n,h in before.items());used=resource.getrusage(resource.RUSAGE_CHILDREN)
 out={'status':'PASS','manifest_payloads':len(before),'principal_proof_sha256':proof,'actual_principal_audits':manifest['actual_principal_audits'],'jobs':jobs,'source_unchanged':True,'wall_seconds':time.perf_counter()-start,'child_cpu_seconds':used.ru_utime+used.ru_stime-initial.ru_utime-initial.ru_stime,'scope':'ONLY four NEW bounded Cycle10 admissions; no quantum code, predecessor scientific replay, hardware or paid jobs.'}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','manifest_payloads','source_unchanged','wall_seconds','child_cpu_seconds']}))
if __name__=='__main__':main()
