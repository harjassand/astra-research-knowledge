"""Finite diagnostic of the new classical-channel lift; not its proof."""
import numpy as np, json, time, resource
from pathlib import Path
start=time.perf_counter(); rng=np.random.default_rng(942713)
def herm(n):
 a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)); return (a+a.conj().T)/2
def met(s,h,kind):
 a,u=np.linalg.eigh(s); z=u.conj().T@h@u
 if kind=='sld': w=2/(a[:,None]+a[None,:])
 else:
  w=np.empty((len(a),len(a)))
  for i,x in enumerate(a):
   for j,y in enumerate(a):
    w[i,j]=1/x if abs(x-y)<1e-13*max(x,y) else (np.log(x)-np.log(y))/(x-y)
 return float(np.sum(abs(z)**2*w).real)
def lift(s,h,e,q):
 r=len(s); g=(np.kron(np.eye(r),s)+np.kron(s.T,np.eye(r)))/(2*r)
 b=np.zeros((r*r+1,r*r+1),complex); b[:-1,:-1]=(1-e)*g;b[-1,-1]=e*q
 t=np.zeros_like(b);v=h.reshape(-1,order='F');t[:-1,-1]=v;t[-1,:-1]=v.conj()
 return b,t
cases=[]
for case in range(8):
 m,n,r=3,2,2
 ss=[]
 for i in range(m):
  x=herm(r);ss.append(x@x+0.2*np.eye(r))
 ss=np.array(ss);ss/=sum(np.trace(x).real for x in ss)
 hs=np.array([herm(r) for _ in range(m)]);hs-=np.mean(hs,axis=0)
 k=rng.uniform(.05,1,(n,m));k/=np.sum(k,axis=0)
 so=np.einsum('yi,ijk->yjk',k,ss);ho=np.einsum('yi,ijk->yjk',k,hs)
 q=rng.uniform(.1,1,m);q/=sum(q);qo=k@q
 si=sum(met(s,h,'sld') for s,h in zip(ss,hs));su=sum(met(s,h,'sld') for s,h in zip(so,ho))
 runs=[]
 for e in [1e-3,1e-7,1e-15,1e-40,1e-100]:
  bi=sum(met(*lift(s,h,e,z),'bkm') for s,h,z in zip(ss,hs,q))
  bo=sum(met(*lift(s,h,e,z),'bkm') for s,h,z in zip(so,ho,qo))
  runs.append({'epsilon':e,'bkm_ratio':bo/bi,'input_scaled':bi/(2*r*np.log(1/e)),'output_scaled':bo/(2*r*np.log(1/e))})
 assert np.linalg.norm(sum(hs))<1e-12
 assert abs(runs[-1]['input_scaled']/si-1)<.04
 assert abs(runs[-1]['output_scaled']/su-1)<.04
 cases.append({'channel':k.tolist(),'sld_ratio':su/si,'sld_input':si,'sld_output':su,'reference_tangent_residual':float(np.linalg.norm(sum(hs))),'lifts':runs})
out={'purpose':'Finite independent arithmetic diagnostic of classical Liouville lift, not universal proof','seed':942713,'cases':cases,'elapsed_seconds':time.perf_counter()-start,'peak_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'cases':len(cases),'elapsed_seconds':out['elapsed_seconds'],'peak_rss_kib_linux':out['peak_rss_kib_linux'],'max_last_ratio_error':max(abs(c['lifts'][-1]['bkm_ratio']-c['sld_ratio']) for c in cases)}))
