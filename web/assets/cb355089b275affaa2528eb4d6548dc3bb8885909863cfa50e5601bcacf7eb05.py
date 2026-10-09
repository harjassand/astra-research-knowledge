"""Exploratory rank-two searches. A nonnegative minimum found numerically is not a proof."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from npt_core import endpoint, endpoint_action

def search(n: int, starts: int, maxiter: int, seed: int) -> list[dict]:
    rng=np.random.default_rng(seed);D=3**n;dims=(3,)*n;records=[]
    def unpack(z):
        z=np.ascontiguousarray(z).view(np.complex128)
        return z[:2*D].reshape(D,2),z[2*D:].reshape(D,2)
    def objective(z):
        U,V=unpack(z);C=U@V.conj().T;norm=float(np.vdot(C,C).real)
        if norm<1e-100: raise FloatingPointError('Degenerate parameterization')
        W=endpoint_action(C,dims);f=float(np.vdot(C,W).real/norm);G=(W-f*C)/norm
        grad=np.concatenate([(2*G@V).ravel(),(2*G.conj().T@U).ravel()])
        return f,np.ascontiguousarray(grad).view(np.float64)
    for trial in range(starts):
        U=np.linalg.qr(rng.normal(size=(D,2))+1j*rng.normal(size=(D,2)))[0]
        V=np.linalg.qr(rng.normal(size=(D,2))+1j*rng.normal(size=(D,2)))[0]
        mode='random'
        if trial%3==1:
            mode='near_kernel';m=D//3
            u=rng.normal(size=m)+1j*rng.normal(size=m);u/=np.linalg.norm(u)
            v=rng.normal(size=m)+1j*rng.normal(size=m);v/=np.linalg.norm(v)
            U0=np.zeros((D,2),complex);V0=U0.copy()
            U0[:m,0]=u;U0[m:2*m,1]=u;V0[:m,0]=v;V0[m:2*m,1]=v
            U=U0+.1*U;V=V0+.1*V
        elif trial%3==2:
            mode='normal_start';V=U.copy();V[:,1]*=np.exp(1j*rng.uniform(0,2*np.pi))
        z0=np.ascontiguousarray(np.concatenate([U.ravel(),V.ravel()])).view(np.float64)
        if trial==0:
            direction=rng.normal(size=z0.size);direction/=np.linalg.norm(direction)
            f,g=objective(z0);h=1e-6
            fd=(objective(z0+h*direction)[0]-objective(z0-h*direction)[0])/(2*h)
            assert abs(fd-g@direction)<1e-7,(fd,g@direction)
        result=minimize(objective,z0,jac=True,method='L-BFGS-B',
                        options={'maxiter':maxiter,'ftol':1e-15,'gtol':1e-9,'maxls':40})
        U,V=unpack(result.x);C=U@V.conj().T;C/=np.linalg.norm(C);value=endpoint(C,dims)
        sv=np.linalg.svd(C,compute_uv=False)
        rec={'sites':n,'trial':trial,'seed':seed,'mode':mode,'q':float(value),
             'iterations':int(result.nit),'gradient_norm':float(np.linalg.norm(result.jac)),
             'success':bool(result.success),'message':str(result.message),
             'third_singular_value':float(sv[2]) if len(sv)>2 else 0.}
        records.append(rec);print(json.dumps(rec),flush=True)
        if value < -1e-9:
            np.savez(Path(__file__).with_name(f'negative_candidate_n{n}_trial{trial}.npz'),U=U,V=V,C=C)
    return records
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,required=True)
    p.add_argument('--starts',type=int,default=6);p.add_argument('--maxiter',type=int,default=300)
    p.add_argument('--seed',type=int,default=20261009);a=p.parse_args()
    records=search(a.n,a.starts,a.maxiter,a.seed+a.n)
    out={'status':'exploratory floating point; not a positivity proof','records':records,
         'minimum_q':min(x['q'] for x in records)}
    Path(__file__).with_name(f'SEARCH_n{a.n}.json').write_text(json.dumps(out,indent=2)+'\n')
