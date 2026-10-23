#!/usr/bin/env python3
"""Relocated replay of the TWO NEW finite calculations only; no network/old suite."""
from pathlib import Path
import hashlib,json,tempfile,shutil,subprocess,sys,time,math,resource,argparse
root=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args()
start=time.perf_counter();before={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
if (root/'SHA256SUMS').exists():
 for line in (root/'SHA256SUMS').read_text().splitlines():
  sha,rel=line.split('  ',1);q=Path(rel);assert not q.is_absolute() and '..' not in q.parts
  assert hashlib.sha256((root/q).read_bytes()).hexdigest()==sha,rel

def equal(a,b):
 if isinstance(a,dict):
  assert set(a)-{'cost'}==set(b)-{'cost'}
  for k in a:
   if k!='cost':equal(a[k],b[k])
 elif isinstance(a,list):
  assert len(a)==len(b)
  for x,y in zip(a,b):equal(x,y)
 elif isinstance(a,(int,float)) and not isinstance(a,bool):assert math.isclose(a,b,rel_tol=2e-12,abs_tol=1e-15),(a,b)
 else:assert a==b,(a,b)
logs=[]
with tempfile.TemporaryDirectory(prefix='dots_cycle10_') as td:
 dst=Path(td)/'calculations';shutil.copytree(root/'calculations',dst)
 for script,out in [('photon_ledger.py','results.json'),('electron_competition.py','electron_competition.json')]:
  expected=json.loads((root/'calculations'/out).read_text());t=time.perf_counter()
  r=subprocess.run([sys.executable,str(dst/script)],cwd=td,capture_output=True,text=True,timeout=30)
  assert r.returncode==0,r.stderr
  equal(expected,json.loads((dst/out).read_text()))
  logs.append({'script':script,'exit_code':r.returncode,'wall_seconds':time.perf_counter()-t})
after={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
assert before==after
receipt={'status':'PASS','source_unchanged':True,'relocated_calculations':logs,'wall_seconds':time.perf_counter()-start,'children_peak_RSS_KiB_Linux':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'scope':'Two new finite ledgers only. No experimental replication, closure certification, full kinetic solve or plant admission.'}
s=json.dumps(receipt,indent=2)+'\n'
if args.output:Path(args.output).write_text(s)
print(s)
