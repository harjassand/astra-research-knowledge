"""Explicitly authorized L32 diagnostic with first-pair fallback stopping rule."""
import json,subprocess,resource,time,pathlib,math,hashlib
root=pathlib.Path(__file__).resolve().parent
expected='7915b8f4fd4d2a5aa19df3352f0d7d679227bada888a67793e7292f32639b454'
assert hashlib.sha256((root/'simulator').read_bytes()).hexdigest()==expected
manifest=dict(L=32,kappa=1,T=5,noise_ratios=[.001,.01],seeds=[101,102,103],methods=['sweep','toom'],binary_sha256=expected,maximum_endpoints=12,cpu_cap_seconds=180,address_cap_bytes=1<<30,first_pair_stopping_rule='Pause remaining10 if both alpha.001 seed101 methods invoke fallback',decoder='Unchanged frozen phase1 common syndrome-only decoder',component_diameters='Not instrumented in frozen binary; existing eligible/component totals retained')
(root/'phase2_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
start=time.monotonic();rows=[];stopping=None
with (root/'phase2_raw.jsonl').open('w') as f:
 for alpha in manifest['noise_ratios']:
  for seed in manifest['seeds']:
   for method in manifest['methods']:
    r=resource.getrusage(resource.RUSAGE_CHILDREN);remain=180-r.ru_utime-r.ru_stime
    if remain<=1:stopping='Aggregate CPU cap reached';break
    def caps():
     resource.setrlimit(resource.RLIMIT_AS,(1<<30,1<<30));cap=max(1,math.floor(remain));resource.setrlimit(resource.RLIMIT_CPU,(cap,cap))
    try:p=subprocess.run([str(root/'simulator'),'trial','32',str(alpha),'5',str(seed),method],capture_output=True,text=True,preexec_fn=caps,timeout=max(1,180-(time.monotonic()-start)))
    except subprocess.TimeoutExpired:stopping='180-second wall safety cap reached';break
    if p.returncode:stopping=f'Exit{p.returncode}: {p.stderr}';break
    row=json.loads(p.stdout);assert row['L']==32 and row['alpha']==alpha and row['seed']==seed and row['method']==method and row['unresolved']==0
    rows.append(row);f.write(json.dumps(row)+'\n');f.flush()
   if stopping:break
   if len(rows)==2 and all(r['fallback'] for r in rows):stopping='Predeclared first-pair rule: both alpha.001 seed101 methods fallback; remaining10 paused for parent decision';break
  if stopping:break
r=resource.getrusage(resource.RUSAGE_CHILDREN)
report=dict(completed_endpoints=len(rows),maximum_planned_endpoints=12,stopping=stopping,wall_seconds=time.monotonic()-start,cpu_seconds=r.ru_utime+r.ru_stime,maxrss_KiB=r.ru_maxrss)
(root/'phase2_resources.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
