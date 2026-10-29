"""Independent actual pair Bell preparation/readout check with arbitrary global channels."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh,expm
rng=np.random.default_rng(997310)
bells=np.array([[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]],complex).T/np.sqrt(2)
signs=[1,1,1,-1]
rows=[]
for n in [2,3,4]:
    D=2**n; spectator=np.eye(D//4)
    for _ in range(3):
        Vs=[]
        for j in range(2):
            h=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)); Vs.append(expm(1j*(h+h.conj().T)))
        U=np.kron(*Vs); b=U@bells
        S=np.kron(spectator,b@np.diag(signs)@b.conj().T)
        A=rng.normal(size=(4,D,D))+1j*rng.normal(size=(4,D,D))
        w,v=eigh(sum(a.conj().T@a for a in A)); R=(v/np.sqrt(w))@v.conj().T; A=[a@R for a in A]
        joint=np.zeros((4,4))
        for j in range(4):
            rho=np.kron(spectator/(D//4),np.outer(b[:,j],b[:,j].conj()))
            out=sum(a@rho@a.conj().T for a in A)
            for k in range(4): joint[j,k]=np.trace(np.kron(spectator,np.outer(b[:,k],b[:,k].conj()))@out).real/4
        q=sum(joint[j,k] for j in range(4) for k in range(4) if signs[j]!=signs[k])
        target=(1-sum(np.trace(S@a.conj().T@S@a).real for a in A)/D)/2
        assert abs(joint.sum()-1)<1e-12 and abs(q-target)<1e-12
        rows.append({'n':n,'positive_transition_probability':float(q),'autocorrelation_target':float(target)})
Path(__file__).with_suffix('.json').write_text(json.dumps({'all_assertions_passed':True,'checks':rows},indent=2)+'\n')
print('9 nonunital global-channel local-Bell checks passed')
