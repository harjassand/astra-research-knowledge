import json
from pathlib import Path
import numpy as np

def diss(k,o):
 p=k.conj().T@k; return k.conj().T@o@k-(p@o+o@p)/2

gamma=.8; mu=.3; nu=.6; kap=.9; delta=.2; d=(gamma+mu)/2+delta
C0=max(1/(2*d),1/nu)+.5; b=.1
out=[]
for eps in [.3,.1,.03,.01]:
 H=np.zeros((4,4),complex); H[0,1]=H[1,0]=eps
 jumps=[]
 for src,dst,rate in [(1,2,gamma),(1,3,mu),(3,0,nu)]:
  k=np.zeros((4,4),complex); k[dst,src]=np.sqrt(rate); jumps.append(k)
 # Four projector dephasings at rate delta give offdiagonal damping delta.
 for i in range(4):
  k=np.zeros((4,4),complex); k[i,i]=np.sqrt(delta); jumps.append(k)
 A=np.zeros((4,4),complex); A[2,2]=kap
 kill=lambda o:1j*(H@o-o@H)+sum((diss(k,o) for k in jumps),np.zeros_like(o))-(A@o+o@A)/2
 r=(gamma+mu)*d/(2*gamma*eps**2)+2/gamma+1/kap+mu/(gamma*nu)
 R=np.diag([r,r-d/(2*eps**2),1/kap,r+1/nu]).astype(complex); R[0,1]=-1j/(2*eps); R[1,0]=1j/(2*eps)
 residual=np.linalg.norm(kill(R)+np.eye(4))
 eig=np.linalg.eigvalsh(R); beta=b*eps**2; S=(1-beta*(r+C0))*np.eye(4)+beta*R
 service=np.linalg.norm(kill(S)+beta*np.eye(4)+(1-beta*(r+C0))*A)
 assert residual<1e-9 and service<1e-11 and eig[0]>0
 assert eig[-1]-r<=max(1/(2*d),1/nu)+1e-9
 out.append(dict(epsilon=eps,resolvent_residual=float(residual),service_residual=float(service),max_above_idle=float(eig[-1]-r),idle_deficit_over_epsilon_squared=float((1-S[0,0].real)/eps**2),offdiag_over_epsilon=float(abs(S[0,1])/eps),min_S=float(np.linalg.eigvalsh(S)[0])))
report={'scope':'isolated exact four-phase controller with identity aborts; not native overlap theorem','gamma':gamma,'mu':mu,'nu':nu,'kappa':kap,'delta':delta,'C0':C0,'b':b,'results':out}
Path(__file__).with_name('weak_initiation_fixture_checks.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
