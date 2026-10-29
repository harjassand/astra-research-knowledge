"""Exploratory floating controls; not a proof or acquired physical record."""
import json
from pathlib import Path
import numpy as np

def stationary(q):
    a=q.T.copy(); a[-1]=1
    b=np.zeros(len(q)); b[-1]=1
    return np.linalg.solve(a,b)

def rate(p,q,r):
    mask=~np.eye(len(q),dtype=bool)
    qd=q[mask]; rd=r[mask]
    term=np.zeros_like(q)
    term[mask]=qd*np.log(qd/rd)-qd+rd
    return float(p @ term.sum(axis=1))

def check(q,theta):
    p=stationary(q); pt=p[theta]; mu=(p+pt)/2
    f=p[:,None]*q; np.fill_diagonal(f,0)
    fr=f.T[np.ix_(theta,theta)]
    qb=(f+fr)/(2*mu[:,None]); np.fill_diagonal(qb,-qb.sum(axis=1))
    r=fr/pt[:,None]; np.fill_diagonal(r,-r.sum(axis=1))
    sig=rate(p,q,r); ip=rate(p,q,qb); ir=rate(pt,r,qb)
    assert np.max(np.abs(mu@qb))<1e-8
    assert abs(ip-ir)<1e-8
    return {'sigma':sig,'projection_rate':ip,'ratio':ip/sig,
            'js':float(np.sum(p*np.log(p/mu))),
            'hellinger_deficit':float(1-np.sqrt(p*pt).sum()),
            'rho':p.tolist(),'q':q.tolist(),'theta':theta.tolist()}

def main():
    rng=np.random.default_rng(131930)
    maximum=None; count=0
    for n in [2,3,4,6,10]:
        for scale in [.1,1,3,6]:
            for _ in range(1000):
                q=np.exp(rng.uniform(-scale,scale,(n,n)))
                np.fill_diagonal(q,0);np.fill_diagonal(q,-q.sum(axis=1))
                theta=np.arange(n)
                for a in range(0,n-1,2):theta[a],theta[a+1]=a+1,a
                item=check(q,theta); count+=1
                if maximum is None or item['ratio']>maximum['ratio']: maximum=item
    out={'scope':'exploratory floating search; proof required','tested':count,'max_ratio':maximum}
    path=Path(__file__).with_name('PARITY_PROJECTION_EXPLORATION.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
