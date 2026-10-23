#!/usr/bin/env python3
"""Verify exact payloads; replay ONLY new Cycle9 admissions in a fresh copy."""
from pathlib import Path
import argparse,hashlib,json,math,resource,shutil,subprocess,sys,tempfile,time

TIMINGS={'cpu_seconds','wall_seconds','runtime_seconds','process_cpu_seconds'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stable(x):
 if isinstance(x,dict):return {k:stable(v) for k,v in x.items() if k not in TIMINGS}
 if isinstance(x,list):return [stable(v) for v in x]
 return x
def equivalent(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,float):return math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-11)
 if isinstance(a,dict):return a.keys()==b.keys() and all(equivalent(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(equivalent(x,y) for x,y in zip(a,b))
 return a==b

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
 args=parser.parse_args();src=Path(__file__).resolve().parent
 wall=time.perf_counter();initial=resource.getrusage(resource.RUSAGE_CHILDREN)
 manifest=json.loads((src/'MANIFEST.json').read_text());before={}
 for entry in manifest['payloads']:
  f=src/entry['path'];assert f.stat().st_size==entry['bytes']
  assert sha(f)==entry['sha256'];before[entry['path']]=entry['sha256']
 proof=manifest['principal_proof_sha256'];assert sha(src/'PROOF.txt')==proof
 for audit in manifest['actual_principal_audits']:
  assert proof in (src/audit).read_text()
 jobs=[]
 with tempfile.TemporaryDirectory(prefix='astra_cycle9_relocated_') as td:
  dst=Path(td)/'source';shutil.copytree(src,dst)
  specs=[('calculations/principal/replay.py','calculations/principal/RESULT.json',False),
         ('studies/loss_converse/replay_loss_lemmas.py','studies/loss_converse/EXACT_REPLAY_RESULTS.json',False),
         ('studies/collective/replay.py','studies/collective/REPLAY_RESULT.json',False),
         ('studies/collective/challenge/analytic_checks.py','studies/collective/challenge/analytic_checks.json',False),
         ('studies/receiver_challenge/replay.py','studies/receiver_challenge/RESULT.json',True),
         ('studies/receiver_challenge/aided_primitive_admission.py','studies/receiver_challenge/AIDED_PRIMITIVE_RESULT.json',True)]
  for script,result,stdout_result in specs:
   t=time.perf_counter()
   done=subprocess.run([sys.executable,str(dst/script)],cwd=dst,
                       capture_output=True,text=True,check=True,timeout=180)
   observed=json.loads(done.stdout) if stdout_result else json.loads((dst/result).read_text())
   assert equivalent(stable(json.loads((src/result).read_text())),stable(observed)),script
   jobs.append({'script':script,'status':'PASS','result_reproduced':True,
                'wall_seconds':time.perf_counter()-t,
                'comparison':'exact counts/rational/decimal strings; floating admissions atol/rtol1e-11; timing excluded',
                'stdout':done.stdout.strip()})
 assert all(sha(src/f)==h for f,h in before.items())
 used=resource.getrusage(resource.RUSAGE_CHILDREN)
 out={'status':'PASS','manifest_payloads':len(before),'principal_proof_sha256':proof,
      'actual_principal_audits':manifest['actual_principal_audits'],'jobs':jobs,
      'source_unchanged':True,'wall_seconds':time.perf_counter()-wall,
      'child_cpu_seconds':used.ru_utime+used.ru_stime-initial.ru_utime-initial.ru_stime,
      'scope':'Only six new Cycle9 bounded admissions; predecessor source hashed/preserved but its science not rerun.'}
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:out[k] for k in ['status','manifest_payloads','wall_seconds','child_cpu_seconds','source_unchanged']}))

if __name__=='__main__':main()
