from pathlib import Path
import os,sys,json,hashlib,subprocess,time
HERE=Path(__file__).resolve().parent;SOURCE=HERE/'optional_boundary_source'
OUT=Path(os.environ.get('AUDIT_OUTPUT_DIR',str(HERE)));OUT.mkdir(parents=True,exist_ok=True)
wanted={'FAST_ACTIVITY_GRAPH_BOUNDARY.md':'1f254ad2f5d60d288c7b45c5b0729753d08c244153117945d31a58aeaf8a1ad5','exact_graph_controls.py':'90ad4eaaa28594213f7b23f1b80bb6810701841b0e0ce40946e899994af0c9db','exact_graph_results.json':'9dbfe3ec80a0ac5f2bb587fbe351d3ac2301b488278bdc906f62cae05b4ae56e'}
bind={}
for name,expected in wanted.items():
 b=(SOURCE/name).read_bytes();actual=hashlib.sha256(b).hexdigest();assert actual==expected,name;bind[name]={'bytes':len(b),'sha256':actual}
start=time.perf_counter();p=subprocess.run([sys.executable,str(SOURCE/'exact_graph_controls.py')],cwd=OUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
result=dict(source_binding=bind,returncode=p.returncode,seconds=time.perf_counter()-start,stdout_bytes=len(p.stdout.encode()),stderr_bytes=len(p.stderr.encode()),output_sha256=hashlib.sha256(p.stdout.encode()).hexdigest(),exact_match=p.stdout.encode()==(SOURCE/'exact_graph_results.json').read_bytes())
(OUT/'optional_boundary.stdout.json').write_text(p.stdout);(OUT/'optional_boundary.stderr.txt').write_text(p.stderr)
assert p.returncode==0 and result['exact_match']
(OUT/'OPTIONAL_BOUNDARY_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
