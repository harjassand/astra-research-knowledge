"""Execute the proved variational ascent on three specified finite starting points.
Not a certificate of global optimality or the unrestricted inequality.
"""
import numpy as np,json,time,resource
from scipy.linalg import expm
rng=np.random.default_rng(1651);start=time.perf_counter()
def ptr(X,r):return np.trace(X.reshape(3,r,3,r),axis1=0,axis2=2)
def wh(X,r):return (np.kron(np.eye(3),ptr(X,r))-X.reshape(3,r,3,r).transpose(2,1,0,3).reshape(3*r,3*r))/2
def logm(X):
 w,V=np.linalg.eigh((X+X.conj().T)/2)
 if min(w)<=0:raise ValueError('nonpositive state')
 return (V*np.log(w))@V.conj().T,float(w.min())
def ent(X):
 w=np.linalg.eigvalsh(X);w=w[w>0];return float(-sum(w*np.log(w)))
def info(X,r):
 L,m=logm(X);LR,_=logm(ptr(X,r));G=2*wh(L,r)-np.kron(np.eye(3),LR)
 w,V=np.linalg.eigh(G);shift=max(w);z=np.exp(w-shift);Y=(V*(z/sum(z)))@V.conj().T
 return float(shift+np.log(sum(z))),Y,m
runs=[]
for name,r in [('mixed_interior',3),('rotated_antisymmetric',3),('larger_reference',4)]:
 z=rng.normal(size=(3*r,3*r))+1j*rng.normal(size=(3*r,3*r));X=z@z.conj().T;X/=np.trace(X)
 if name=='mixed_interior':X=.5*X+.5*np.eye(3*r)/(3*r)
 if name=='rotated_antisymmetric':
  S=np.eye(9).reshape(3,3,3,3).transpose(1,0,2,3).reshape(9,9);H=(z+z.conj().T);H/=np.linalg.norm(H);U=expm(.5j*H)
  X=U@(.99*(np.eye(9)-S)/6+.01*np.eye(9)/9)@U.conj().T
 history=[];reason='iteration_budget'
 for k in range(500):
  val,Y,m=info(X,r);Q=wh(Y,r);nextval,_,mn=info(Q,r)
  L,_=logm(X);LQ,_=logm(Q);D=float(np.trace(Q@(LQ-L)).real)
  F=ent(Y)-2*ent(Q)+ent(ptr(Y,r));res=np.linalg.norm(Q-X)
  history.append(dict(iteration=k,log_phi=val,next_log_phi=nextval,entropy_objective=F,kl_step=D,ascent_slack=nextval-val-D,residual=float(res),min_eigenvalue=m))
  X=Q
  if nextval-val-D < -1e-9:reason='numerical_monotonicity_failure';break
  if mn<1e-13:reason='conditioning_boundary_not_global_solution';break
  if res<1e-10:reason='stationary_tolerance_not_global_solution';break
 np.savez(__file__.replace('.py','_'+name+'.npz'),X=X,Y=Y)
 runs.append(dict(name=name,reference_dimension=r,stop_reason=reason,steps=len(history),final=history[-1],history=history))
out={'runs':runs,'elapsed_seconds':time.perf_counter()-start,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Floating monotone-ascent implementation, three declared starts only. No unrestricted proof or global optimization claim.'}
open(__file__.replace('.py','.json'),'w').write(json.dumps(out,indent=2)+'\n');print(json.dumps({**{k:v for k,v in out.items() if k!='runs'},'runs':[{k:v for k,v in r.items() if k!='history'} for r in runs]},indent=2))
