import numpy as np,json
from functools import reduce

def adj(O,H,js):
 out=1j*(H@O-O@H)
 for J in js:
  D=J.conj().T@J
  out+=J.conj().T@O@J-(D@O+O@D)/2
 return out
rows=[]
for om in [.2,1.,3.]:
 for kap in [.3,1.,2.]:
  for mu in [0.,.2,2.]:
   H=np.zeros((3,3),complex);H[0,1]=H[1,0]=om
   J=np.zeros_like(H);J[2,1]=np.sqrt(kap)
   js=[J]+[np.diag(np.eye(3)[i])*np.sqrt(mu) for i in range(3)]
   B=np.diag([1.,1.,0.]);R=np.zeros_like(H)
   R[:2,:2]=[[2/kap+(kap+2*mu)/(4*om**2),-.5j/om],[.5j/om,2/kap]]
   err=np.linalg.norm(adj(R,H,js)+B)
   eig=np.linalg.eigvalsh(R[:2,:2]);a=eig[0]/eig[-1];r=1/eig[-1];A=R/eig[-1]
   for u in [.1,1.,3.]:
    F=np.eye(3)+u*A; fe,U=np.linalg.eigh(F);logF=(U*np.log(fe))@U.conj().T
    # Exact two-site product generator
    V=np.kron(F,F);LV=np.kron(adj(F,H,js),F)+np.kron(F,adj(F,H,js))
    logV=np.kron(logF,np.eye(3))+np.kron(np.eye(3),logF)
    slack=-r/(1+u)*V@logV-LV
    mn=np.linalg.eigvalsh(slack)[0]
    rows.append(dict(omega=om,kappa=kap,mu=mu,u=u,poisson_error=float(err),min_drift_slack=float(mn),a=float(a),r=float(r)))
assert max(x['poisson_error'] for x in rows)<1e-10
assert min(x['min_drift_slack'] for x in rows)>-1e-10
print(json.dumps({'checks':len(rows),'max_poisson_error':max(x['poisson_error'] for x in rows),'min_drift_slack':min(x['min_drift_slack'] for x in rows),'rows':rows},indent=2))
