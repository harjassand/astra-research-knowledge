import json,subprocess,resource,time,pathlib,math,hashlib
root=pathlib.Path(__file__).resolve().parent
m=json.loads((root/'phase3_manifest.json').read_text());assert (root/'PHASE3_GATE_APPROVED.txt').exists()
assert hashlib.sha256((root/'simulator_equalreads').read_bytes()).hexdigest()==m['binary_sha256']
start=time.monotonic();rows=[];stopping=None
with (root/'phase3_raw.jsonl').open('w') as f:
 for seed in m['seeds']:
  r=resource.getrusage(resource.RUSAGE_CHILDREN);remain=90-r.ru_utime-r.ru_stime
  if remain<=1:stopping='Aggregate90CPU-second cap reached';break
  def caps():
   resource.setrlimit(resource.RLIMIT_AS,(1<<30,1<<30));cap=max(1,math.floor(remain));resource.setrlimit(resource.RLIMIT_CPU,(cap,cap))
  try:p=subprocess.run([str(root/'simulator_equalreads'),'trial','32','.001','5',str(seed),'toom','4'],capture_output=True,text=True,preexec_fn=caps,timeout=max(1,90-(time.monotonic()-start)))
  except subprocess.TimeoutExpired:stopping='90-second wall safety cap reached';break
  if p.returncode:stopping=f'Exit{p.returncode}: {p.stderr}';break
  row=json.loads(p.stdout);assert row['L']==32 and row['alpha']==.001 and row['seed']==seed and row['method']=='toom' and row['correction_multiplier']==4 and row['unresolved']==0
  rows.append(row);f.write(json.dumps(row)+'\n');f.flush()
r=resource.getrusage(resource.RUSAGE_CHILDREN)
report=dict(completed_endpoints=len(rows),planned_endpoints=3,stopping=stopping,wall_seconds=time.monotonic()-start,cpu_seconds=r.ru_utime+r.ru_stime,maxrss_KiB=r.ru_maxrss)
(root/'phase3_resources.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
