#!/usr/bin/env python3
"""Verify payloads and replay new jobs only in a disposable relocated copy."""
import argparse,hashlib,json,resource,shutil,subprocess,sys,tempfile,time
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stable(x):
 if isinstance(x,dict):return {k:stable(v) for k,v in x.items()
                             if k not in {'cpu_seconds','wall_seconds','process_cpu_seconds'}}
 if isinstance(x,list):return [stable(v) for v in x]
 return x

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
 args=p.parse_args();src=Path(__file__).resolve().parent
 wall=time.perf_counter();child=resource.getrusage(resource.RUSAGE_CHILDREN)
 manifest=json.loads((src/'MANIFEST.json').read_text());before={}
 for entry in manifest['payloads']:
  f=src/entry['path'];assert f.stat().st_size==entry['bytes']
  assert sha(f)==entry['sha256'];before[entry['path']]=entry['sha256']
 proof=manifest['principal_proof_sha256'];assert sha(src/'PROOF.txt')==proof
 for rel in ['audits/quantum/FINAL_INTEGRATED_AUDIT.txt',
             'audits/SEARCH_INTEGRATED_AUDIT.txt','audits/LOWER_INTEGRATED_AUDIT.txt']:
  assert proof in (src/rel).read_text()
 jobs=[]
 with tempfile.TemporaryDirectory(prefix='astra_cycle8_relocated_') as td:
  dst=Path(td)/'relocated';shutil.copytree(src,dst)
  specs=[('calculations/principal/replay.py',[],
          'calculations/principal/RESULT.json'),
         ('calculations/search/replay_fixture.py',
          ['--outdir',str(dst/'calculations/search')],
          'calculations/search/RESULT.json'),
         ('calculations/search/audit_integer_tree.py',[],None),
         ('calculations/lower/replay.py',[],
          'calculations/lower/RESULT.json'),
         ('calculations/public_coin/replay.py',[],
          'calculations/public_coin/RESULT.json')]
  for script,options,result in specs:
   start=time.perf_counter()
   done=subprocess.run([sys.executable,str(dst/script),*options],cwd=dst,
                       capture_output=True,text=True,check=True,timeout=180)
   equal=True
   if result:equal=stable(json.loads((src/result).read_text()))==stable(json.loads((dst/result).read_text()))
   else:
    expected=json.loads((src/'calculations/search/IMPLEMENTATION_AUDIT_CHECK.json').read_text())
    equal=stable(expected)==stable(json.loads(done.stdout))
   assert equal,script
   jobs.append({'script':script,'status':'PASS','result_reproduced':equal,
                'wall_seconds':time.perf_counter()-start,'stdout':done.stdout.strip()})
 assert all(sha(src/f)==h for f,h in before.items())
 used=resource.getrusage(resource.RUSAGE_CHILDREN)
 result={'status':'PASS','manifest_payloads':len(before),'jobs':jobs,
         'principal_proof_sha256':proof,'source_unchanged':True,
         'wall_seconds':time.perf_counter()-wall,
         'child_cpu_seconds':used.ru_utime+used.ru_stime-child.ru_utime-child.ru_stime,
         'scope':'Only five new bounded Cycle8 jobs; no predecessor science replay or hardware.'}
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result))

if __name__=='__main__':main()
