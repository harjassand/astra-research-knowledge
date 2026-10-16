"""Exactly two preselected replays, then three fixed syndrome-only readouts."""
import json,subprocess,resource,time,pathlib,math,hashlib
root=pathlib.Path(__file__).resolve().parent
binary=root/'simulator_readouts'
expected='d8446b68cca4c6a9b9d44b743dff0ec5d3d9cebe4cb34f0fe83421ae9702b0c6'
assert hashlib.sha256(binary.read_bytes()).hexdigest()==expected
assert (root/'PHASE4_GATE_APPROVED.txt').exists()
resource.setrlimit(resource.RLIMIT_AS,(1<<30,1<<30))
start=time.monotonic();initial=resource.getrusage(resource.RUSAGE_SELF);base=initial.ru_utime+initial.ru_stime
manifest=dict(scope='Selected failed-endpoint readout-sensitivity diagnostic, NOT unbiased performance comparison',L=32,alpha=.001,T=5,seed=101,replays=[dict(method='sweep',beta=1),dict(method='toom',beta=4)],binary_sha256=expected,decoder_policies={'D0':'frozen all-or-nothing strict wrapped diameter<L/8','D1':'retain strict local fills; H of combined unresolved syndrome','D2':'consistent lift and each vertex coordinate max-min<L; local prism; H of combined unresolved'},decoder_input='S only; accumulated E used only after selecting recovery to score',cpu_cap_seconds=45,address_cap_bytes=1<<30,model='base instantaneous Pauli model only')
(root/'phase4_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
def used():
 a=resource.getrusage(resource.RUSAGE_SELF);b=resource.getrusage(resource.RUSAGE_CHILDREN);return a.ru_utime+a.ru_stime-base+b.ru_utime+b.ru_stime
def run(args,stdin=None):
 remain=45-used();assert remain>1,'aggregate CPU cap reached'
 def caps():
  resource.setrlimit(resource.RLIMIT_AS,(1<<30,1<<30));cap=max(1,math.floor(remain));resource.setrlimit(resource.RLIMIT_CPU,(cap,cap))
 p=subprocess.run([str(binary)]+args,input=stdin,capture_output=True,text=True,preexec_fn=caps,timeout=max(1,45-(time.monotonic()-start)))
 assert p.returncode==0,(p.returncode,p.stderr)
 return p.stdout
rows=[];endpoints={};checks=[]
for method,beta,filename in [('sweep',1,'phase2_raw.jsonl'),('toom',4,'phase3_raw.jsonl')]:
 ref=next(r for r in map(json.loads,(root/filename).read_text().splitlines()) if r['method']==method and r['alpha']==.001 and r['seed']==101)
 ep=root/f'phase4_endpoint_{method}.json'
 row=json.loads(run(['trial','32','.001','5','101',method,str(beta),str(ep)]))
 for k in ref:
  if not k.endswith('_seconds'):assert row[k]==ref[k],(method,k,row[k],ref[k])
 rows.append(row);checks.append(dict(method=method,status='PASS',matched_fields=[k for k in ref if not k.endswith('_seconds')]))
 data=json.loads(ep.read_text());assert data['format']=='4d-memory-endpoint-v1' and data['L']==32
 endpoints[method]=data
(root/'phase4_replays.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
(root/'phase4_legacy_regression.json').write_text(json.dumps(checks,indent=2)+'\n')
# No alternative is evaluated until BOTH legacy trajectories have matched.
L=32;N=L**4;strides=[L**3,L**2,L,1];pairs=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
def up(x,a):return x+(1 if (x//strides[a])%L<L-1 else -(L-1))*strides[a]
def toggle(s,x):
 if x in s:s.remove(x)
 else:s.add(x)
def boundary(F):
 out=set()
 for f in F:
  o,x=divmod(f,N);i,j=pairs[o]
  for e in (i*N+x,i*N+up(x,j),j*N+x,j*N+up(x,i)):toggle(out,e)
 return out
def hom(F):
 h=0
 for f in F:
  o,x=divmod(f,N);i,j=pairs[o]
  if (x//strides[i])%L==0 and (x//strides[j])%L==0:h^=1<<o
 return h
results=[]
for method,data in endpoints.items():
 S=set(data['S']);E=set(data['E']);assert boundary(E)==S
 inp=' '.join(map(str,sorted(S)))+'\n'
 for policy in range(3):
  text=run(['decode','32',str(policy)],inp);flag,line=text.split('\n',1);D=set(map(int,line.split()))
  assert boundary(D)==S
  C=E^D;assert not boundary(C);h=hom(C)
  rec=root/f'phase4_recovery_{method}_D{policy}.json';rec.write_text(json.dumps(dict(format='4d-memory-recovery-v1',L=L,policy=f'D{policy}',method=method,source_endpoint=f'phase4_endpoint_{method}.json',R=sorted(D)))+'\n')
  results.append(dict(method=method,policy=f'D{policy}',fallback=int(flag),failure=int(h!=0),logical_bits=h,recovery_faces=len(D),residual_faces=len(C),boundary_verified=True))
  if policy==0:assert h==next(r['logical_bits'] for r in rows if r['method']==method)
(root/'phase4_readout_results.json').write_text(json.dumps(results,indent=2)+'\n')
files=list(root.glob('phase4_endpoint_*.json'))+list(root.glob('phase4_recovery_*.json'))
(root/'PHASE4_ENDPOINT_SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in files))
a=resource.getrusage(resource.RUSAGE_SELF);b=resource.getrusage(resource.RUSAGE_CHILDREN)
report=dict(completed_replays=2,completed_readouts=6,stopping=None,cpu_seconds=used(),wall_seconds=time.monotonic()-start,max_child_rss_KiB=b.ru_maxrss,runner_maxrss_KiB=a.ru_maxrss)
(root/'phase4_resources.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(results=results,resources=report),indent=2))
