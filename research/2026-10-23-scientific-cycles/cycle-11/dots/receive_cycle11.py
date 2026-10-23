"""Relocated replay of only the new endpoint calculations. No network or old science."""
import argparse,hashlib,json,os,resource,shutil,subprocess,sys,tempfile,time
from pathlib import Path
root=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output).resolve()
if out==root or root in out.parents: raise SystemExit('Receipt must be outside source tree')
t=time.perf_counter()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def payload():
 return {str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
before=payload()
if (root/'SHA256SUMS').exists():
 for line in (root/'SHA256SUMS').read_text().splitlines():
  h,n=line.split('  ',1)
  assert before[n]==h, n
commands=[]
with tempfile.TemporaryDirectory(prefix='dots_cycle11_') as td:
 w=Path(td)
 for folder in ['calculations','independent_endpoint']:
  shutil.copytree(root/folder,w/folder,ignore=shutil.ignore_patterns('__pycache__'))
 (w/'peroxide_evidence').mkdir()
 shutil.copy2(root/'peroxide_evidence/source_data.xlsx',w/'peroxide_evidence/source_data.xlsx')
 for script in ['calculations/endpoint_ledger.py','independent_endpoint/check.py']:
  a=time.perf_counter();p=subprocess.run([sys.executable,'-B',str(w/script)],cwd=w,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
  commands.append({'entrypoint':script,'returncode':p.returncode,'elapsed_seconds':time.perf_counter()-a,'stderr':p.stderr})
  if p.returncode: raise RuntimeError(p.stderr)
 for name in ['calculations/results.json','independent_endpoint/results.json']:
  assert json.loads((root/name).read_text())==json.loads((w/name).read_text()),name
 # Cross-implementation comparisons: independent Decimal strings versus parent floats.
 a=json.loads((w/'calculations/results.json').read_text())['arms']['H2O2']['sampling_scenarios'][1]
 b=json.loads((w/'independent_endpoint/results.json').read_text())['sequential_four_1mL']
 assert abs(a['net_nitrate_micromol']-float(b['net_nitrate_umol']))<1e-12
 assert abs(a['nitrate_per_nominal_peroxide_dosed']-float(b['net_per_nominal_dose']))<1e-14
assert before==payload(), 'source changed'
r={'status':'PASS','commands':commands,'payload_files_checked':len(before),'source_unchanged':True,'parent_independent_match':True,'elapsed_seconds':time.perf_counter()-t,'child_peak_RSS_KiB_Linux':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'scope':'New finite data arithmetic only. No original experiment, clinical/safety assertion, scientific acceptance, old trajectory, fit or network.','total_research_cost':'unknown'}
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
