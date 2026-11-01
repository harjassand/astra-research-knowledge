from pathlib import Path
import os,sys,json,hashlib,time,subprocess
HERE=Path(__file__).resolve().parent
SOURCE=Path(os.environ.get('CIRCUIT_SOURCE_DIR',str(HERE.parent if (HERE.parent/'cover_circuit.py').exists() else HERE.parent/'stochastic_cover_circuit_pending_20261031')))
OUT=Path(os.environ.get('AUDIT_OUTPUT_DIR',str(HERE)));OUT.mkdir(parents=True,exist_ok=True)
m=SOURCE/'AUTHOR_MANIFEST.json';b=m.read_bytes();sha=hashlib.sha256(b).hexdigest();assert sha=='64be3db4d97541eef968548572887f3f518c3e3343377a05c07e693ab26cb60d';files=json.loads(b)['files']
for name,wanted in files.items():
 b=(SOURCE/name).read_bytes();assert {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}==wanted
(OUT/'CIRCUIT_SOURCE_BINDING.json').write_text(json.dumps(dict(manifest_sha256=sha,files=files),indent=2)+'\n')
rows=[]
for script,expected in [('cover_circuit.py','p4_circuit_demo.json'),('exercise_circuit.py','circuit_results.json')]:
 start=time.perf_counter();p=subprocess.run([sys.executable,str(SOURCE/script)],cwd=OUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
 stem=Path(script).stem;(OUT/(stem+'.stdout.json')).write_text(p.stdout);(OUT/(stem+'.stderr.txt')).write_text(p.stderr)
 row=dict(script=script,seconds=time.perf_counter()-start,returncode=p.returncode,stdout_bytes=len(p.stdout.encode()),stderr_bytes=len(p.stderr.encode()),output_sha256=hashlib.sha256(p.stdout.encode()).hexdigest(),exact_match=p.stdout.encode()==(SOURCE/expected).read_bytes());rows.append(row)
 assert row['returncode']==0 and row['exact_match'],row
(OUT/'CIRCUIT_EXACT_REPLAYS.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
