from pathlib import Path
import numpy as np,json
from cone_bridge import heat
OUT=Path(__file__).parent

def feat(A):
    a,b,c,d=A.ravel();u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
    return np.array([u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w])

def normalize(p):
    roots=np.roots([p[1],p[5],p[2]+p[3],p[4],p[0]])
    roots=roots[roots.imag>0]
    assert len(roots)==2
    forms=[np.array([[abs(r)**2,-r.real],[-r.real,1.]]) for r in roots]
    ev,U=np.linalg.eigh(forms[0]);W=(U*(1/np.sqrt(ev)))@U.T
    lam,V=np.linalg.eigh(W@forms[1]@W)
    # P has column arguments; A -> A S has row arguments, hence transpose.
    S=(W@V@np.diag((p[1]*lam)**(-.25))).T
    rng=np.random.default_rng(4); AA=rng.normal(size=(50,2,2))
    B=np.array([feat(A) for A in AA]);target=np.array([feat(A@S)@p for A in AA])
    pn=np.linalg.lstsq(B,target,rcond=None)[0]
    assert np.linalg.norm(B@pn-target)<1e-7
    assert np.linalg.norm(pn[[0,1,4,5]]-[1,1,0,0])<1e-8
    return pn,S

if __name__=='__main__':
    d=np.load(OUT/'interfaces.npz'); results=[]
    for rec in json.loads((OUT/'cone_results.json').read_text()):
        p=np.array(rec['p']);pn,S=normalize(p)
        hr,xx,dual=heat(d,pn,steps=30000)
        hr.update(index=rec['index'],p=pn.tolist(),S=S.tolist(),r=float((pn[2]+pn[3])/2),status='NUMERICAL_ONLY')
        results.append(hr)
        np.savez(OUT/f'normalized_{rec["index"]}.npz',p=pn,S=S,heat=xx,dual=dual)
        (OUT/'normalized_results.json').write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps(hr),flush=True)
