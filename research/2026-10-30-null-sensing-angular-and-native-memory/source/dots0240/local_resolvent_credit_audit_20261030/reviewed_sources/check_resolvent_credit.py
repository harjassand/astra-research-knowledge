import json
from pathlib import Path
import numpy as np
from scipy.linalg import sqrtm

def sop(fun,d):
    cols=[]
    for j in range(d*d):
        e=np.zeros(d*d,complex); e[j]=1
        cols.append(fun(e.reshape(d,d)).reshape(-1))
    return np.stack(cols,axis=1)
def diss(k,o):
    p=k.conj().T@k
    return k.conj().T@o@k-(p@o+o@p)/2
out=[]
for g in [.1,.3,1.]:
    kap=.7; H=np.array([[0,g,0],[g,0,g],[0,g,0]],complex)
    a=np.zeros((3,3),complex); a[0,2]=np.sqrt(kap)
    A=a.conj().T@a
    kill=lambda o:1j*(H@o-o@H)-(A@o+o@A)/2
    R=np.linalg.solve(sop(kill,3),-np.eye(3).reshape(-1)).reshape(3,3)
    R=(R+R.conj().T)/2
    eig=np.linalg.eigvalsh(R); beta=.4/eig[-1]
    S=(1-beta*eig[-1])*np.eye(3)+beta*R
    v=np.diag([.2,1.]); phiv=.2*np.eye(2); d=v-phiv
    F=np.kron(phiv,np.eye(3))+np.kron(d,S)
    K=[np.array([[1,0],[0,0]],complex),np.array([[0,1],[0,0]],complex)]
    HH=np.kron(np.eye(2),H)
    Lf=1j*(HH@F-F@HH)+sum((diss(np.kron(k,a),F) for k in K),np.zeros_like(F))
    exact=np.kron(d,kill(S))
    target=-beta*np.kron(d,np.eye(3))-(1-beta*eig[-1])*np.kron(d,A)
    rs=np.asarray(sqrtm(S),dtype=complex); ris=np.asarray(sqrtm(np.eye(3)-S),dtype=complex)
    kraus=[np.kron(np.eye(2),rs)]+[np.kron(k,ris) for k in K]
    cv=np.kron(v,np.eye(3))
    TF=sum((k.conj().T@cv@k for k in kraus),np.zeros_like(cv))
    errs=[np.linalg.norm(Lf-exact),np.linalg.norm(Lf-target),np.linalg.norm(TF-F),np.linalg.norm(sum(k.conj().T@k for k in kraus)-np.eye(6))]
    assert min(eig)>0 and max(errs)<1e-10
    out.append(dict(g=g,R_min=float(eig[0]),R_max=float(eig[-1]),beta=float(beta),S_min=float(np.linalg.eigvalsh(S)[0]),residuals=[float(x) for x in errs]))
report={'scope':'Exact isolated finite quantum-controller regression, not many-hub service','results':out}
Path(__file__).with_name('resolvent_credit_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
