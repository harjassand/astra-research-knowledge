"""Own bounded pilot runner. Invoke only after independent gate passes."""
import json,subprocess,resource,time,pathlib,math,sys
root=pathlib.Path(__file__).resolve().parent
m=json.loads((root/'manifest.json').read_text())
if not (root/'PILOT_GATE_APPROVED.txt').exists(): raise SystemExit('Independent validation gate not yet approved')
start=time.monotonic(); initial=resource.getrusage(resource.RUSAGE_CHILDREN); baseline=initial.ru_utime+initial.ru_stime
rows=[]; stopping=None
with (root/'pilot_raw.jsonl').open('w') as f:
 for alpha in m['noise_ratios']:
  for seed in m['seeds_zero'] if alpha==0 else m['seeds_nonzero']:
   for method in m['methods']:
    r=resource.getrusage(resource.RUSAGE_CHILDREN);used=r.ru_utime+r.ru_stime-baseline
    remain=180-used
    if remain<=1:stopping='Aggregate CPU cap reached';break
    def caps():
     resource.setrlimit(resource.RLIMIT_AS,(1<<30,1<<30))
     cap=max(1,math.floor(remain));resource.setrlimit(resource.RLIMIT_CPU,(cap,cap))
    cmd=[str(root/'simulator'),'trial','16',str(alpha),'5',str(seed),method]
    try:p=subprocess.run(cmd,capture_output=True,text=True,preexec_fn=caps,timeout=max(1,180-(time.monotonic()-start)))
    except subprocess.TimeoutExpired:stopping='180-second wall safety cap reached';break
    if p.returncode:stopping=f'Exit {p.returncode}: {p.stderr}';break
    row=json.loads(p.stdout);rows.append(row);f.write(json.dumps(row)+'\n');f.flush()
   if stopping:break
  if stopping:break
r=resource.getrusage(resource.RUSAGE_CHILDREN)
report=dict(completed_trials=len(rows),planned_trials=20,stopping=stopping,wall_seconds=time.monotonic()-start,cpu_seconds=r.ru_utime+r.ru_stime-baseline,maxrss_KiB=r.ru_maxrss)
(root/'pilot_resources.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
