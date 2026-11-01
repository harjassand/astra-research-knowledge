import pathlib,hashlib,json,os,subprocess,sys,time
HERE=pathlib.Path(__file__).resolve().parent
SOURCE=pathlib.Path(os.environ.get('GLUE_SOURCE_DIR',(HERE.parent if (HERE.parent/'free_port_glue.py').is_file() else HERE.parent/'stochastic_free_port_glue_pending_20261031'))).resolve()
OUT=pathlib.Path(os.environ.get('AUDIT_OUTPUT_DIR',HERE)).resolve();OUT.mkdir(parents=True,exist_ok=True)
manifest=SOURCE/'AUTHOR_MANIFEST.json';expected='bb5719119c114e9aa1f5ae359af17a0dc85652be9d9cb3c825d7f8572d1c6960'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
bindings=json.loads(manifest.read_text())['files']
for name,item in bindings.items():
 data=(SOURCE/name).read_bytes();assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
(OUT/'SOURCE_BINDINGS.json').write_text(json.dumps({'manifest_sha256':expected,'files':bindings},indent=2)+'\n')
rows=[]
for script,published in [('free_port_glue.py','glue_demo.json'),('exercise_glue.py','glue_results.json'),('receiving_controls.py','receiving_results.json')]:
 start=time.monotonic();p=subprocess.run([sys.executable,str(SOURCE/script)],capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 (OUT/(script+'.stdout.txt')).write_bytes(p.stdout);(OUT/(script+'.stderr.txt')).write_bytes(p.stderr)
 assert p.returncode==0 and not p.stderr and p.stdout==(SOURCE/published).read_bytes(),(script,p.returncode,p.stderr)
 rows.append(dict(script=script,published=published,sha256=hashlib.sha256(p.stdout).hexdigest(),seconds=time.monotonic()-start,byte_identical=True))
 print(script,'PASS',flush=True)
(OUT/'AUTHOR_REPLAY.json').write_text(json.dumps({'status':'PASS','rows':rows},indent=2)+'\n')
