"""Independent pointwise audit, no reuse of release verifier implementation."""
import itertools, json, math
from pathlib import Path
import numpy as np

OUT=Path(__file__).parent
PERMS=np.array(list(itertools.permutations(range(4))))
L=np.array([[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]],float)
RNG=np.random.default_rng(229003)

def vals(p):
    x=p @ L.T
    A=np.sum(x*x,axis=-1)
    B=np.prod(x,axis=-1)
    C=(x[...,0]*x[...,1])**2+(x[...,0]*x[...,2])**2+(x[...,1]*x[...,2])**2
    h4=-A*A/10-3*C/20
    h5=3*A*B/10
    h6=-A**3/50+7*A*C/100-51*B**2/100
    H=B+h4+h5+h6
    F=4*A-3*B+7*A*A/10-4*C-4*A*B/5
    G=1-161*A/100-31*B/10+773*A*A/1000+4*C-199*A*B/50
    return A,H,F,G,h4,h5,h6

def margins(p,q):
    p=np.asarray(p,dtype=float); q=np.asarray(q,dtype=float)
    Ap,Hp,Fp,Gp,*_=vals(p); Aq,Hq,Fq,Gq,*_=vals(q)
    U=4*p[:,None,:]*q[:,PERMS]
    z=U.sum(axis=-1)
    P=np.divide(U,z[...,None],out=np.zeros_like(U),where=z[...,None]>0)
    As,Hs,*_=vals(P)
    za=(z*As).mean(axis=-1); zh=(z*Hs).mean(axis=-1)
    cubic=Ap*Aq*(Ap+Aq)
    abase=Ap+Aq-Hp*Fq-Fp*Hq-za
    amargin=abase-cubic/1000
    bmargin=zh-Hp*Gq-Gp*Hq
    aratio=np.divide(abase,cubic,out=np.full_like(abase,np.inf),where=cubic>1e-18)
    return amargin,bmargin,aratio,Ap,Aq,Hp,Hq,za,zh

def sample(n,alpha):
    return np.sort(RNG.dirichlet(np.full(4,alpha),size=n),axis=-1)[:,::-1]

def lattice(N):
    return np.array([(a,b,c,N-a-b-c) for a in range(N+1) for b in range(N-a+1) for c in range(N-a-b+1)],float)/N

def record(best,key,vs,p,q=None,extra=None):
    idx=int(np.argmin(vs)); v=float(vs[idx])
    if key not in best or v<best[key]['value']:
        r={'value':v,'p':p[idx].tolist()}
        if q is not None:r['q']=q[idx].tolist()
        if extra is not None:r['extra']={k:float(x[idx]) for k,x in extra.items()}
        best[key]=r

def main():
    best={}; tested=0; scalar_count=0
    for alpha in [.025,.05,.1,.3,1.,5.,100.]:
        for _ in range(5):
            p=sample(4000,alpha); q=sample(4000,alpha)
            am,bm,ratio,Ap,Aq,Hp,Hq,za,zh=margins(p,q)
            record(best,'A_product',am,p,q)
            record(best,'H_product',bm,p,q)
            record(best,'A_cubic_coefficient',ratio,p,q)
            A,H,F,G,h4,h5,h6=vals(p)
            record(best,'F',F,p); record(best,'G',G,p); record(best,'H',H,p)
            record(best,'F_over_A',np.divide(F,A,out=np.full_like(A,np.inf),where=A>1e-18),p)
            t=RNG.random(len(p)); scaling=-h4-(1+t)*h5-(1+t+t*t)*h6
            record(best,'H_scaling_divided',scaling,p,extra={'t':t})
            tested+=len(p);scalar_count+=len(p)
    # Every lattice ordered representative at resolution 12, all ordered pair combinations.
    pts=np.unique(np.sort(lattice(12),axis=-1)[:,::-1],axis=0)
    for p0 in pts:
        p=np.repeat(p0[None,:],len(pts),axis=0);q=pts
        am,bm,ratio,*_=margins(p,q)
        record(best,'A_product',am,p,q);record(best,'H_product',bm,p,q)
        record(best,'A_cubic_coefficient',ratio,p,q);tested+=len(p)
    # Near-uniform corners with five independent scales; track cancellation sensitivity.
    near=[]
    for eta in [1e-1,1e-2,1e-3,1e-4,1e-5]:
        for sigma in [1e-1,1e-2,1e-3,1e-4,1e-5]:
            p=.25+eta*(sample(1000,.1)-.25);q=.25+sigma*(sample(1000,.1)-.25)
            am,bm,ratio,*_=margins(p,q)
            near.append({'eta':eta,'sigma':sigma,'amin':float(am.min()),'bmin':float(bm.min()),'ratio_min':float(ratio.min())})
            tested+=len(p)
    result={'seed':229003,'pair_tests':tested,'scalar_tests':scalar_count,'ordered_grid_size':len(pts),'best':best,'near_uniform':near}
    (OUT/'numerical_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
