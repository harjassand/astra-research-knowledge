"""Independent numerical check of local-cycle capacity robustness."""
from pathlib import Path
import json
import numpy as np

rng=np.random.default_rng(437120)

def cap(L,B):
    n=len(L); A=np.array([i for i in range(n) if i not in B])
    u=np.zeros(n)
    u[A]=np.linalg.solve(L[np.ix_(A,A)],np.ones(len(A)))
    C=1/u.mean()
    return C,1-C*u,u

def cycle_P(n,cycle):
    P=np.eye(n)
    for x,y in zip(cycle,cycle[1:]+cycle[:1]):
        P[x]=0;P[x,y]=1
    return P

def run():
    rows=[]
    for n in [7,13,31,63]:
      for ell in [3,4,6]:
       for trial in range(6):
        Ps=[]
        # Overlapping triangles form an irreducible cycle graph.
        for i in range(1,n-1): Ps.append(cycle_P(n,[0,i,i+1]))
        for _ in range(n):
            m=int(rng.integers(2,ell+1)); cyc=rng.choice(n,m,replace=False).tolist()
            Ps.append(cycle_P(n,cyc))
        lam=np.exp(rng.uniform(-4,2,len(Ps)))
        eps=.24
        dh=rng.uniform(-eps,eps,len(Ps))
        lh=lam*(1+dh)
        L=sum((w*(np.eye(n)-P) for w,P in zip(lam,Ps)),np.zeros((n,n)))
        H=sum((w*(np.eye(n)-P) for w,P in zip(lh,Ps)),np.zeros((n,n)))
        B={n-1}
        C,h,u=cap(L,B);Cs,hs,us=cap(L.T,B);Ch,hh,uh=cap(H,B)
        E=lambda f,generator: float(f@generator@f/n)
        identity=float(hs@(H-L)@hh/n)
        K=1/np.sin(np.pi/max(ell,3))
        a=eps*K/np.sqrt(1-eps)
        bound=2*np.arcsinh(a/2)
        actual=abs(np.log(Ch/C))
        assert abs(Cs/C-1)<1e-10
        assert abs(identity-(Ch-C))<1e-10
        assert abs(E(h,L)/C-1)<1e-10
        assert abs(E(hs,L)/C-1)<1e-10
        assert actual<=bound+1e-10
        rows.append(dict(n=n,ell=max(ell,3),trial=trial,C=C,Chat=Ch,
                         log_ratio=actual,log_bound=bound,
                         identity_error=abs(identity-(Ch-C))))
    out=dict(trials=len(rows),max_identity_error=max(r['identity_error'] for r in rows),
             max_log_ratio_over_bound=max(r['log_ratio']/r['log_bound'] for r in rows),
             records=rows)
    Path(__file__).with_name('cycle_capacity_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))

if __name__=='__main__': run()
