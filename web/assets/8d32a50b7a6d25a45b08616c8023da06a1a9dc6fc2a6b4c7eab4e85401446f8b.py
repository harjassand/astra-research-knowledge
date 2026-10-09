"""Nonunital random-channel check of the inverse-Choi/Gram identity.
Floating point diagnostic only. Uses SciPy SLSQP, not an SDP certification.
"""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import fractional_matrix_power

PAULI=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]

def rho(z): return (np.eye(2)+sum(z[i]*PAULI[i] for i in range(3)))/2

def run(seed):
    rng=np.random.default_rng(seed)
    ks=[rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)) for _ in range(4)]
    ksum=sum(k.conj().T@k for k in ks)
    inv=fractional_matrix_power(ksum,-.5)
    ks=[k@inv for k in ks]
    def ph(f): return sum(k.conj().T@f@k for k in ks)
    j=sum(np.outer(k.T.ravel(),k.T.ravel().conj()) for k in ks)
    ji=np.linalg.inv(j)
    def q(z):
        mat=np.kron(np.eye(2),rho(z)); v=mat@ji@mat
        return np.trace(v.reshape(2,2,2,2),axis1=1,axis2=3)
    def cons(z):return np.r_[np.linalg.eigvalsh(rho(z[:3])),np.linalg.eigvalsh(z[3]*np.eye(2)-q(z[:3]))]
    x0=np.r_[np.zeros(3),np.max(np.linalg.eigvalsh(q(np.zeros(3))))+1]
    opt=minimize(lambda z:z[3],x0,method='SLSQP',constraints=[{'type':'ineq','fun':cons}],options={'ftol':1e-12,'maxiter':2000})
    sig=rho(opt.x[:3]); M=np.max(np.linalg.eigvalsh(q(opt.x[:3]))); eta=1-1/M
    fs=[]
    for i in range(2):
        for l in range(2):
            f=np.zeros((2,2));f[i,l]=1;fs.append(f)
    a=np.vstack([ph(f) for f in fs])
    alpha=(1-eta)*np.array([np.trace(sig@f) for f in fs])
    ac=a-np.kron(alpha[:,None],np.eye(2))
    g=np.block([[ph(f@h.conj().T) for h in fs] for f in fs])
    defect=eta*g-ac@ac.conj().T
    ev=np.linalg.eigvalsh(defect)
    return {'seed':seed,'solver_success':bool(opt.success),'min_constraint':float(min(cons(opt.x))),
      'M':float(M),'eta':float(eta),'min_Gram_defect':float(ev[0]),
      'Gram_defect_spectrum':ev.tolist(),'center_eigenvalues':np.linalg.eigvalsh(sig).tolist(),
      'nonunital_norm':float(np.linalg.norm(sum(k@k.conj().T for k in ks)-np.eye(2)))}

if __name__=='__main__':
    out=[run(seed) for seed in range(5)]
    Path(__file__).with_suffix('.json').write_text(json.dumps({'status':'NUMERICAL ONLY','trials':out},indent=2)+'\n')
    print(json.dumps(out,indent=2))
