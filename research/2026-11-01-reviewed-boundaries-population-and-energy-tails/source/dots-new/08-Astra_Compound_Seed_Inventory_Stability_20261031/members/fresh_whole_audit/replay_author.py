from pathlib import Path
import subprocess,sys,json,time,hashlib,os
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent if (HERE.parent/'compound_seed.py').exists() else HERE.parent/'stochastic_compound_seed_pending_20261031'
OUT=Path(os.environ.get('AUDIT_OUTPUT_DIR',str(HERE)));OUT.mkdir(parents=True,exist_ok=True)
author_manifest=SOURCE/'AUTHOR_MANIFEST.json'
binding={'manifest_sha256':hashlib.sha256(author_manifest.read_bytes()).hexdigest(),'files':{}}
assert binding['manifest_sha256']=='3f5605a4850e0d7e638c418254b7dbd509cbfcd4a8e926677fd3f1c61198d13a'
for name,want in json.loads(author_manifest.read_text())['files'].items():
 b=(SOURCE/name).read_bytes();found={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};assert found==want,name;binding['files'][name]=found
(OUT/'BOUND_AUTHOR_PACKAGE.json').write_text(json.dumps(binding,indent=2)+'\n')
jobs=[('compound_seed.py','main_demo.json'),('exercise_compound.py','exercise_results.json'),('comparators/exact_comparator_checks.py','comparators/exact_comparator_results.json'),('comparators/compound_geometry_checks_pending.py','comparators/compound_geometry_results_pending.json'),('comparators/matching_boundary_checks_pending.py','comparators/matching_boundary_results_pending.json')]
rows=[]
for script,expected in jobs:
 start=time.perf_counter()
 p=subprocess.run([sys.executable,str(SOURCE/script)],cwd=OUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
 elapsed=time.perf_counter()-start
 name=Path(script).stem
 (OUT/(name+'.stdout.json')).write_text(p.stdout)
 (OUT/(name+'.stderr.txt')).write_text(p.stderr)
 row=dict(script=script,source_sha256=hashlib.sha256((SOURCE/script).read_bytes()).hexdigest(),returncode=p.returncode,seconds=elapsed,stdout_bytes=len(p.stdout.encode()),stderr_bytes=len(p.stderr.encode()))
 if p.returncode==0:
  actual=json.loads(p.stdout); row['semantic_match_frozen_output']=actual==json.loads((SOURCE/expected).read_text()); row['exact_match_frozen_output']=p.stdout.encode()==(SOURCE/expected).read_bytes(); row['output_sha256']=hashlib.sha256(p.stdout.encode()).hexdigest()
 rows.append(row)
 assert p.returncode==0 and row['semantic_match_frozen_output'] and row['exact_match_frozen_output'],row
(OUT/'AUTHOR_REPLAY.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
