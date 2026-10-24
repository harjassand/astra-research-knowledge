"""Independent dense-matrix check of the regular-simplex equal-reference construction."""
import numpy as np, scipy.linalg as la,json
from pathlib import Path
exec(Path(__file__).with_name('search_quantum_bkm.py').read_text().split('start=time.perf_counter()')[0])
def make(N,e):
 v0=np.ones(N)/np.sqrt(N);vs=[(np.eye(N)[i]-np.ones(N)/N)/np.sqrt(1-1/N) for i in range(N)]
 ss=[(1-e)*np.outer(v,v)+e*np.eye(N)/N for v in vs];hs=[np.outer(v,v0)+np.outer(v0,v) for v in vs];return ss,hs
records=[]
for N in [2,3,4,5]:
 for e in [1e-2,1e-5,1e-8]:
  l=.5;s,h=make(N,e);tau=sum(s)/N;j=sum(h)/N;c=l+(1-l)/(N-1)
  g=lambda a,b:metric(a,np.array([b]))[0,0]
  gi=sum(g(a,b) for a,b in zip(s,h))/N;go=sum(g(l*a+(1-l)*tau,l*b) for a,b in zip(s,h))/N
  expected=l*l/c*np.log1p(N*(1-e)*c/e)/np.log1p(N*(1-e)/e)
  records.append({'N':N,'epsilon':e,'metric_ratio':go/gi,'formula_ratio':expected,'zero_reference_error':float(la.norm(j)),'min_input_eigenvalue':float(min(la.eigvalsh(a)[0] for a in s))})
# Independent Bell reverse-map metric verification at N4.
s,h=make(4,1e-5);phi=np.array([1,0,0,1])/np.sqrt(2);U=[np.eye(2),np.array([[0,1],[1,0]]),np.diag([1,-1]),np.array([[0,-1],[1,0]])]
bells=[np.kron(u,np.eye(2))@phi for u in U]
sig=sum(np.kron(np.outer(v,v),a) for v,a in zip(bells,s))/4
H=sum(np.kron(np.outer(v,v),b) for v,b in zip(bells,h))/4
out=channel(sig,8,.5);Ho=channel(H,8,.5)
bell={'reference_dimension':8,'zero_reference_error':float(la.norm(ptr(H,8))),'qubit_BKM_ratio':float(metric(out,np.array([Ho]))[0,0]/metric(sig,np.array([H]))[0,0]),'input_min_eigenvalue':float(la.eigvalsh(sig)[0])}
result={'kind':'dense floating audit, not interval certificate','simplex_records':records,'Bell_transfer':bell};print(json.dumps(result,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2))
