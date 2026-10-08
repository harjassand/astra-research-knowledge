"""One structured exact target: the Hodge-cancelling input permutation cube."""
import sys,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent))
from exact_rank import rational_model
from diagnostics import choi,syms
from sep_sdp import whiten
import cvxpy as cp
import numpy as np

def gram_model():
    ks,s,_,_=rational_model()
    d=np.diag([2 if i==j else 1 for i,j in syms]).astype(object)
    m=s@np.kron(d,d)@s.T@s
    return choi(m,10,6)

def main():
    ji=gram_model();j=np.array(ji,dtype=float)/float(np.trace(ji))
    j,x,y=whiten(j,10,6);rng=np.random.default_rng(2724)
    vec=[np.eye(10)[i] for i in range(10)]
    for sign in (1,-1):
        vec += [np.eye(10)[i]+sign*np.eye(10)[k] for i in range(10) for k in range(i+1,10)]
    vec += list(rng.normal(size=(300,10)))
    vec=np.array(vec);vec/=np.linalg.norm(vec,axis=1,keepdims=True)
    pu=[(i,k) for i in range(10) for k in range(i,10)]
    qu=[(a,b) for a in range(6) for b in range(a,6)]
    p=np.array([[v[i]*v[k] for i,k in pu] for v in vec])
    target=np.array([[j[i*6+a,k*6+b] for a,b in qu] for i,k in pu])
    factors=[cp.Variable((6,6),symmetric=True) for _ in vec]
    v=cp.vstack([cp.hstack([b[a,c] for a,c in qu]) for b in factors])
    t=cp.Variable();prob=cp.Problem(cp.Maximize(t),[p.T@v==target]+[b-t*np.eye(6)>>0 for b in factors])
    before=time.monotonic();prob.solve(solver='SCS',eps=1e-6,max_iters=5000,verbose=False)
    out=dict(status=prob.status,margin=None if t.value is None else float(t.value),
             atoms=400,seconds=time.monotonic()-before,solver_iterations=prob.solver_stats.num_iters)
    if t.value is not None:
        bs=np.array([b.value for b in factors]);res=np.einsum('ni,nj,nab->iajb',vec,vec,bs)
        out.update(residual=float(np.max(abs(res-j.reshape(10,6,10,6)))),
                   min_factor_eig=float(min(np.linalg.eigvalsh(b)[0] for b in bs)))
        np.savez(Path(__file__).with_name('gram_candidate.npz'),vec=vec,bs=bs,x=x,y=y,j=j)
    Path(__file__).with_name('gram_sdp.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
