"""Local optimization of norm-preserving legal perturbations near exact sinks."""
import json
import time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
import perturb_sink as ps

BASE=Path(__file__).resolve().parent
generators=[]
for i,j in [(1,3),(2,6),(4,8),(5,7),(0,4),(0,8)]:
    for phase in (1.,1j):
        g=np.zeros((9,9),complex)
        g[i,j]=phase
        g[j,i]=np.conj(phase)
        generators.append(g)
generators=np.asarray(generators)


def evaluate(v,detail=False):
    vv=v.reshape(9,12)
    aa=[]
    for k in range(3):
        pair=[]
        for i in range(2):
            h=np.einsum('a,aij->ij',vv[2*k+i],generators,optimize=False)
            u=ps.unitary(h)
            pair.append(ps.mm(ps.mm(u,ps.base[k][i]),u.conj().T))
        aa.append(pair)
    hh=[np.einsum('a,aij->ij',vv[6+k],generators,optimize=False) for k in range(3)]
    ratio,p,vec=ps.evaluate(aa,hh)
    return (ratio,p,vec,aa,hh) if detail else ratio


def main():
    rng=np.random.default_rng(2026101604)
    rows=[]
    start=time.time()
    for k,scale in enumerate((.03,.1,.3,.6)):
        v=rng.normal(0,scale,size=108)
        opt=minimize(lambda p:-evaluate(p),v,method='L-BFGS-B',bounds=[(-2,2)]*108,
                     options=dict(maxiter=140,ftol=1e-12,gtol=2e-7,maxls=20))
        ratio,p,vec,aa,hh=evaluate(opt.x,True)
        row=dict(start=k,scale=scale,ratio=ratio,probability=p,success=bool(opt.success),
                 message=str(opt.message),nfev=int(opt.nfev),nit=int(opt.nit))
        rows.append(row)
        np.savez(BASE/f'optimized_sink_{k}.npz',a=np.asarray(aa),h=np.asarray(hh),v=vec,parameters=opt.x)
        print(json.dumps(row),flush=True)
    (BASE/'optimized_sink_receipt.json').write_text(json.dumps(dict(
        family='d=9 seed-factorized sink; 108 sparse bath-rotation/baseline parameters',
        rng_seed=2026101604,results=rows,elapsed_seconds=time.time()-start,
        epistemic_status='bounded local floating-point optimization; not a theorem'),indent=2)+'\n')


if __name__=='__main__':
    main()
