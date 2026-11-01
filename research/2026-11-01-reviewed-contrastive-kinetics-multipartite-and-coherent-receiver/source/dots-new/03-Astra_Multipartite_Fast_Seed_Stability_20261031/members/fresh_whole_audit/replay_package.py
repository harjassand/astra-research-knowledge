from pathlib import Path
import os,sys,json,hashlib,subprocess,time
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent if (HERE.parent/'multipartite_seed.py').exists() else HERE.parent/'stochastic_multipartite_seed_pending_20261031'
OUT=Path(os.environ.get('AUDIT_OUTPUT_DIR',str(HERE)));OUT.mkdir(parents=True,exist_ok=True)
bindings=[]
for name,expected in [('AUTHOR_MANIFEST.json','aa232d64c068a0de1ffb8a5e41af5f5728a241945b4edb5e4c74d02dd82e3e85'),('independent_audit/AUDIT_MANIFEST.json','0d69b6f2fc9d62335a933ef47b61878809c932b9642b407e768a17c3b0a8a385')]:
 b=(SOURCE/name).read_bytes();assert hashlib.sha256(b).hexdigest()==expected
 m=json.loads(b)
 for fn,want in m['files'].items():
  data=(SOURCE/fn).read_bytes();assert {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}==want,fn
 bindings.append(dict(manifest=name,sha256=expected,files=m['files']))
(OUT/'BOUND_SOURCE_PACKAGES.json').write_text(json.dumps(bindings,indent=2)+'\n')
rows=[]
for script,expected in [('multipartite_seed.py','triangle_demo.json'),('exercise_multipartite.py','exercise_results.json'),('independent_mechanism/multipartite_mechanism_checks.py','independent_mechanism/multipartite_mechanism_results.json'),('independent_audit/exercise_independent_multipartite.py','independent_audit/independent_multipartite_results.json'),('independent_audit/extreme_wire_multipartite.py','independent_audit/extreme_wire_multipartite_results.json')]:
 start=time.perf_counter();p=subprocess.run([sys.executable,str(SOURCE/script)],cwd=OUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
 seconds=time.perf_counter()-start;stem=Path(script).stem
 (OUT/(stem+'.stdout.json')).write_text(p.stdout);(OUT/(stem+'.stderr.txt')).write_text(p.stderr)
 row=dict(script=script,source_sha256=hashlib.sha256((SOURCE/script).read_bytes()).hexdigest(),returncode=p.returncode,seconds=seconds,stdout_bytes=len(p.stdout.encode()),stderr_bytes=len(p.stderr.encode()),output_sha256=hashlib.sha256(p.stdout.encode()).hexdigest(),exact_match=p.stdout.encode()==(SOURCE/expected).read_bytes())
 rows.append(row);assert p.returncode==0 and row['exact_match'],row
(OUT/'EXACT_REPLAYS.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
