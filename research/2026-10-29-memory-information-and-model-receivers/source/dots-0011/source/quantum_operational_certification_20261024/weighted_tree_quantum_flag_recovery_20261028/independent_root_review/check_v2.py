import numpy as np,itertools,json
from pathlib import Path
rng=np.random.default_rng(2810262330)
def tn(a):return float(np.abs(np.linalg.eigvalsh((a+a.conj().T)/2)).sum())
def state():
 a=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));a=a@a.conj().T;return a/np.trace(a)
def plus(a):
 e,v=np.linalg.eigh((a+a.conj().T)/2);return (v*np.maximum(e,0))@v.conj().T
rows=[]
for test in range(120):
 n=4;par=[-1,0,0,2];root=rng.dirichlet(np.ones(4));tau=[state() for _ in range(4)]
 if test%3==0:root[2]=0;root/=root.sum()
 trans={i:rng.dirichlet(np.ones(4),size=4) for i in range(1,n)}
 if test%4==0:
  for i in trans:trans[i][:,3]=0;trans[i]/=trans[i].sum(1)[:,None]
 words=list(itertools.product(range(4),repeat=n));p=[];joint={i:np.zeros((4,4)) for i in range(1,n)}
 for x in words:
  v=root[x[0]]
  for i in range(1,n):v*=trans[i][x[par[i]],x[i]]
  p.append(v)
  for i in joint:joint[i][x[par[i]],x[i]]+=v
 sig=[root[a]*tau[a] for a in range(4)];A=[]
 for s in sig:
  h=.001*(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)));A.append(plus(s+h+h.conj().T))
 if test==0:A=[np.zeros((2,2),complex) for _ in range(4)]
 B={i:np.maximum(joint[i]+.001*rng.normal(size=(4,4)),0) for i in joint}
 if test%5==0:B[2][1]=0
 fitted={i:np.array([r/r.sum() if r.sum()>0 else np.ones(4)/4 for r in B[i]]) for i in B}
 z=sum(np.trace(a).real for a in A)
 rootcq=[a/z for a in A] if z>0 else [np.eye(2)/2]+[np.zeros((2,2)) for _ in range(3)]
 actual=0
 for x,v in zip(words,p):
  h=rootcq[x[0]].copy()
  for i in range(1,n):h*=fitted[i][x[par[i]],x[i]]
  actual+=tn(v*tau[x[0]]-h)/2
 eroot=sum(tn(a-s) for a,s in zip(A,sig));edge=sum(np.abs(B[i]-joint[i]).sum() for i in B);bound=eroot+edge
 assert actual<=bound+1e-12
 # Independently verify every weighted row inequality, including empty fitted rows.
 for i in B:
  for a in range(4):
   mass=joint[i][a].sum();true=joint[i][a]/mass if mass else np.ones(4)/4
   assert mass*np.abs(true-fitted[i][a]).sum()<=2*np.abs(joint[i][a]-B[i][a]).sum()+1e-12
 rows.append({'test':test,'half_trace_error':actual,'bound':bound,'empty_root':bool(z==0),'root_error':eroot,'edge_error':edge})
Path(__file__).with_suffix('.json').write_text(json.dumps({'status':'PASS_FLOATING_DIAGNOSTICS','seed':2810262330,'rows':rows},indent=2)+'\n')
print(json.dumps({'cases':len(rows),'max_violation':max(x['half_trace_error']-x['bound'] for x in rows)}))
