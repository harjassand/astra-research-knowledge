"""Finite search near an exact asynchronous product-saturating sink.

All randomness is fixed numerical search input, never a selected private seed.
Conjugating each physical A separately preserves seed factorization and norms.
"""
import json
import time
from pathlib import Path
import numpy as np

BASE=Path(__file__).resolve().parent
X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1,-1])
I=np.eye(2)
d=9
z1=np.repeat([1,1,-1,-1],d)
z2=np.repeat([1,-1,1,-1],d)
out=np.zeros(4*d)
out[3*d:]=1


def unitary(h):
    e,v=np.linalg.eigh(h)
    return np.einsum('ij,j,kj->ik',v,np.exp(-1j*e),v.conj(),optimize=False)


def mm(a,b):
    # Explicit einsum avoids stale Apple BLAS floating-point status warnings.
    return np.einsum('ij,jk->ik',a,b,optimize=False)


def turn(k):
    a=np.zeros((3,3),complex)
    a[0,k]=a[k,0]=1
    return a


base=[]
for k in range(3):
    a1=np.kron(turn(1 if k==0 else 2),np.eye(3))
    a2=np.kron(np.eye(3),turn(1 if k<2 else 2))
    base.append((a1,a2))


def evaluate(aa,hh=None,action=.35):
    effect=np.diag(out).astype(complex)
    for k in (2,1,0):
        h=action*(np.kron(np.kron(X,I),aa[k][0])+
                  np.kron(np.kron(I,X),aa[k][1]))
        if hh is not None:
            h+=np.kron(np.eye(4),hh[k])
        u=unitary(h)
        effect=mm(mm(u.conj().T,effect),u)
        if k==2:
            effect=(effect+z2[:,None]*effect*z2[None,:])/2
        elif k==1:
            effect=(effect+z1[:,None]*effect*z1[None,:])/2
    e,v=np.linalg.eigh(effect[:d,:d])
    q=1-np.cos(action)**2*np.cos(2*action)**2
    return float(e[-1]/q**2),float(e[-1]),v[:,-1]


def random_herm(rng):
    q=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    q=(q+q.conj().T)/2
    return q/np.linalg.norm(q,2)


def main():
    rng=np.random.default_rng(2026101602)
    initial=evaluate(base)
    start=time.time()
    rows=[]
    best=initial[0]
    for scale in (.002,.01,.05,.15,.5,1.5):
        bestrow=None
        for k in range(160):
            aa=[]
            for pair in base:
                ap=[]
                for a in pair:
                    u=unitary(scale*random_herm(rng))
                    ap.append(mm(mm(u,a),u.conj().T))
                aa.append(ap)
            hh=[scale*random_herm(rng) for _ in range(3)]
            ratio,prob,vec=evaluate(aa,hh)
            row=dict(scale=scale,case=k,ratio=ratio,probability=prob)
            if bestrow is None or ratio>bestrow['ratio']:
                bestrow=row
            if ratio>best:
                best=ratio
                np.savez(BASE/'perturb_sink_best.npz',a=np.asarray(aa),h=np.asarray(hh),v=vec)
        rows.append(bestrow)
        print(json.dumps(bestrow),flush=True)
    data=dict(family='seed-factorized; d=9 product sink with legal bath rotations and baseline',
              action_each_segment=.35,pinch_order=[1,2],rng_seed=2026101602,
              exact_baseline_ratio=initial[0],cases=960,rows=rows,
              elapsed_seconds=time.time()-start,
              epistemic_status='floating-point diagnostics; no proof')
    (BASE/'perturb_sink_receipt.json').write_text(json.dumps(data,indent=2)+'\n')


if __name__=='__main__':
    main()
