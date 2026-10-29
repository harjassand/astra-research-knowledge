import numpy as np,json,itertools
from fractions import Fraction as F
from pathlib import Path
rng=np.random.default_rng(20261029);I=np.eye(2);ps=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])];res=[]
for trial in range(8):
 q=rng.normal(size=4);q/=np.linalg.norm(q);w,x,y,z=q;C=np.array([[w*w+x*x-y*y-z*z,2*(x*y-w*z),2*(x*z+w*y)],[2*(x*y+w*z),w*w-x*x+y*y-z*z,2*(y*z-w*x)],[2*(x*z-w*y),2*(y*z+w*x),w*w-x*x-y*y+z*z]])
 v=rng.normal(size=(24,8))+1j*rng.normal(size=(24,8));ks=np.linalg.qr(v)[0].reshape(3,8,8);a=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));sigma=a@a.conj().T;sigma/=np.trace(sigma)
 S=sum(C[i,j]*np.kron(ps[i],ps[j]) for i in range(3) for j in range(3));T=(np.eye(4)+S)/2;Ti=np.kron(T,I);inputweight=np.kron(np.eye(4),sigma)
 delta=sum(np.trace((k@Ti-Ti@k)@inputweight@(k@Ti-Ti@k).conj().T).real for k in ks)/8
 mean=0.
 for c,d,u,vv in itertools.product(range(3),range(3),[-1,1],[-1,1]):
  rho=np.kron((I+u*ps[c])/2,(I+vv*ps[d])/2);full=sum(k@np.kron(rho,sigma)@k.conj().T for k in ks);out=np.trace(full.reshape(4,2,4,2),axis1=1,axis2=3)
  for aa,b in itertools.product(range(3),repeat=2):
   corr=np.trace(np.kron(ps[aa],ps[b])@out).real
   mean+=(.75-2.25*corr*C[aa,b]-20.25*corr*u*vv*C[aa,b]*C[c,d])/324
 assert abs(mean-delta)<1e-12
 res.append({'trial':trial,'selected_loss':delta,'native_mean':mean,'difference':abs(mean-delta)})
# Candidate-dependent PUBLIC source choice is permitted pointwise; each case above has fresh channel/frame.
p=F(1,3);actual=p*F(1,2)+(1-p);wrong=p*F(1,2)/p
assert actual==F(5,6) and wrong==F(1,2) # invalid role-first selective abort can UNDERestimate.
out={'arbitrary_joint_CPTP_native_checks':res,'role_first_underestimate_actual':str(actual),'role_first_underestimate_estimator':str(wrong),'scope':'Independent floating native-bank versus full joint commutator identity; scalar exact invalid-order witness. No actual quantum yield.'}
Path(__file__).with_name('independent_checks.json').write_text(json.dumps(out,indent=2)+'\n');print('max residual',max(r['difference'] for r in res))
