from pathlib import Path
import subprocess,sys,json,time,hashlib,os
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent if (HERE.parent/'compound_seed.py').exists() else HERE.parent/'stochastic_compound_seed_pending_20261031'
OUT=Path(os.environ.get('AUDIT_OUTPUT_DIR',str(HERE)));OUT.mkdir(parents=True,exist_ok=True)
manifest=SOURCE/'independent_audit/AUDIT_MANIFEST.json'
binding={'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'files':{}}
for name,want in json.loads(manifest.read_text())['files'].items():
 b=(SOURCE/name).read_bytes();found={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};assert found==want,name;binding['files'][name]=found
assert binding['manifest_sha256']=='aa35721e92f6c76a47f6769c9e940162162d6cea5942cf844e7f5872c303e60a'
rows=[]
for script,expected in [('exercise_independent.py','independent_results.json'),('extreme_and_wire_controls.py','extreme_and_wire_results.json'),('graph_inventory_checks.py','graph_inventory_results.json')]:
 start=time.perf_counter();p=subprocess.run([sys.executable,str(SOURCE/'independent_audit'/script)],cwd=OUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
 elapsed=time.perf_counter()-start
 name=Path(script).stem
 (OUT/(name+'.stdout.json')).write_text(p.stdout);(OUT/(name+'.stderr.txt')).write_text(p.stderr)
 row=dict(script='independent_audit/'+script,source_sha256=hashlib.sha256((SOURCE/'independent_audit'/script).read_bytes()).hexdigest(),returncode=p.returncode,seconds=elapsed,stdout_bytes=len(p.stdout.encode()),stderr_bytes=len(p.stderr.encode()))
 if p.returncode==0:
  row['exact_match_frozen_output']=p.stdout.encode()==(SOURCE/'independent_audit'/expected).read_bytes();row['output_sha256']=hashlib.sha256(p.stdout.encode()).hexdigest()
 rows.append(row);assert p.returncode==0 and row['exact_match_frozen_output'],row
(OUT/'INDEPENDENT_REPLAY.json').write_text(json.dumps(rows,indent=2)+'\n')
(OUT/'BOUND_INDEPENDENT_PACKAGE.json').write_text(json.dumps(binding,indent=2)+'\n')
print(json.dumps(rows,indent=2))
