import subprocess,json,resource,time,pathlib
root=pathlib.Path(__file__).resolve().parent
start=time.monotonic();rows=[json.loads(x) for x in (root/'pilot_raw.jsonl').read_text().splitlines()];out=[]
def caps():
 resource.setrlimit(resource.RLIMIT_AS,(1<<30,1<<30));resource.setrlimit(resource.RLIMIT_CPU,(20,20))
for method in ['sweep','toom']:
 ref=next(r for r in rows if r['alpha']==.01 and r['method']==method)
 for beta_arg in [[],['1']]:
  result=json.loads(subprocess.check_output([str(root/'simulator_equalreads'),'trial','16','.01','5',str(ref['seed']),method]+beta_arg,text=True,preexec_fn=caps,timeout=30))
  for k in ref:
   if not k.endswith('_seconds'):assert result[k]==ref[k],(method,k)
  out.append(dict(method=method,explicit_beta=bool(beta_arg),status='PASS',seed=ref['seed'],alpha=.01,legacy_nontiming_fields_matched=len(ref)-2))
selftest=json.loads(subprocess.check_output([str(root/'simulator_equalreads'),'test'],text=True,preexec_fn=caps,timeout=30))
invalid=[]
for method,beta in [('sweep','4'),('toom','0'),('toom','2'),('toom','-1'),('unknown','1')]:
 p=subprocess.run([str(root/'simulator_equalreads'),'trial','16','.001','0','101',method,beta],capture_output=True,text=True,preexec_fn=caps,timeout=30);assert p.returncode!=0;invalid.append(dict(method=method,beta=beta,status='rejected',error=p.stderr.strip()))
r=resource.getrusage(resource.RUSAGE_CHILDREN);report=dict(regressions=out,selftest=selftest,invalid_cases=invalid,wall_seconds=time.monotonic()-start,cpu_seconds=r.ru_utime+r.ru_stime,maxrss_KiB=r.ru_maxrss)
(root/'equalreads_regression.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
