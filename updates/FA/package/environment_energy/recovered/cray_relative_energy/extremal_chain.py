"""Explicit environment and local channel approaching the sharp chain-motif bound."""
from __future__ import annotations
import numpy as np,json
from scipy.linalg import eigh
from pathlib import Path
from experiment import heisenberg

def run():
    h0=heisenberg(4,[(0,1,1),(0,2,1),(1,3,1)]).toarray()
    h1=h0+heisenberg(4,[(0,1,1)]).toarray()
    t=(1-np.sqrt(33))/8
    env=heisenberg(4,[(2,3,t)]).toarray()
    e0,v0=eigh(h0+env);e1,v1=eigh(h1+env)
    ps0=v0[:,0];G=v1[:,e1<e1[0]+1e-8]
    SS=heisenberg(4,[(i,j,2) for i in range(4) for j in range(i+1,4)]).toarray()+3*np.eye(16)
    es,us=eigh(G.T@SS@G);g=G@us
    gs=g[:,es<1];gt=g[:,abs(es-2)<1e-6]
    assert gs.shape[1]==1 and gt.shape[1]==3
    singlet=np.array([0,1,-1,0])/np.sqrt(2);P=np.outer(singlet,singlet)
    def weight(v):M=v.reshape(4,4);return np.trace(M.T@M@P)
    a0=weight(ps0);aS=weight(gs[:,0]);aT=sum(weight(v) for v in gt.T)/3
    p=(a0-aT)/(aS-aT)
    inv=np.linalg.inv(ps0.reshape(4,4))
    Ks=[np.sqrt(p)*gs[:,0].reshape(4,4)@inv]+[np.sqrt((1-p)/3)*v.reshape(4,4)@inv for v in gt.T]
    assert np.linalg.norm(sum(K.T@K for K in Ks)-np.eye(4))<1e-10
    image=sum(np.kron(K.T,np.eye(4))@h1@np.kron(K,np.eye(4)) for K in Ks)
    R=h0-image
    low=eigh(R,eigvals_only=True)
    # Choi convention C[i,a,j,b] = Phi(E_ij)[a,b].
    C=sum(np.outer(K.ravel(),K.ravel()) for K in Ks)
    # K.ravel uses the input/output orientation in this real Heisenberg convention.
    out={'environment_exchange':t,'weak_ground':float(e0[0]),'strong_ground':float(e1[0]),'difference':float(e1[0]-e0[0]),'channel_lower_reverse':float(low[0]),'singlet_weight':p,'residual_eigenvalues':low.tolist(),'unital_error':float(np.linalg.norm(sum(K.T@K for K in Ks)-np.eye(4)))}
    path=Path(__file__).parent
    np.savez(path/'extremal_chain.npz',h0=h0,h1=h1,environment=env,choi=C,kraus=np.array(Ks))
    (path/'extremal_chain.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
    return out
if __name__=='__main__':run()
