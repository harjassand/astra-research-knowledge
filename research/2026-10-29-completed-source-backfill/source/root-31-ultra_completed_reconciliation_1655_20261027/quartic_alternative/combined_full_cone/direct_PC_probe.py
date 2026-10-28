"""A materially different true-PC support test; numerical witnesses only here."""
import json,time
import numpy as np
from scipy.optimize import differential_evolution
from maps import ROOT


def FGHT(z,p):
    z=np.atleast_2d(z);a,b,c,d=z.T
    u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
    energy=p[0]*u*u+p[1]*v*v+p[2]*u*v+p[3]*w*w+p[4]*u*w+p[5]*v*w+p[6]*q*u+p[7]*q*v+p[8]*q*w
    du=2*p[0]*u+p[2]*v+p[4]*w+p[6]*q
    dv=2*p[1]*v+p[2]*u+p[5]*w+p[7]*q
    dw=2*p[3]*w+p[4]*u+p[5]*v+p[8]*q;dq=p[6]*u+p[7]*v+p[8]*w
    B=np.stack([np.stack([2*a,0*a,2*c,0*a],axis=1),np.stack([0*a,2*b,0*a,2*d],axis=1),
                np.stack([b,a,d,c],axis=1),np.stack([d,-c,-b,a],axis=1)],axis=2)
    J=np.array([[2*p[0],p[2],p[4],p[6]],[p[2],2*p[1],p[5],p[7]],
                [p[4],p[5],2*p[3],p[8]],[p[6],p[7],p[8],0]])
    Hu=np.diag([2,0,2,0]);Hv=np.diag([0,2,0,2])
    Hw=np.array([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]])
    Hq=np.array([[0,0,0,1],[0,0,-1,0],[0,-1,0,0],[1,0,0,0]])
    H=B@J@np.swapaxes(B,1,2)+np.einsum('ni,ijk->njk',np.stack([du,dv,dw,dq],axis=1),np.stack([Hu,Hv,Hw,Hq]))
    g=np.einsum('nij,nj->ni',B,np.stack([du,dv,dw,dq],axis=1))
    T=H/2-g[:,:,None]*g[:,None,:]/(4*energy[:,None,None])
    return energy,g,H,T/q[:,None,None]


def pair(z):
    tm,dm,tp,dp,alpha=np.asarray(z)
    minus=np.stack([np.cos(tm),np.sin(tm)*np.cos(dm),np.zeros_like(tm),np.sin(tm)*np.sin(dm)],axis=-1)
    plus=np.stack([np.cos(tp)*np.cos(alpha),np.sin(tp)*np.cos(alpha+dp),
                   np.cos(tp)*np.sin(alpha),np.sin(tp)*np.sin(alpha+dp)],axis=-1)
    return np.atleast_2d(minus),np.atleast_2d(plus)


def params(rm,rp):
    alpha=np.arctan2(rm[2],rm[0]);c,s=np.cos(alpha),np.sin(alpha)
    def rot(r):return np.array([c*r[0]+s*r[2],c*r[1]+s*r[3],-s*r[0]+c*r[2],-s*r[1]+c*r[3]])
    rm,rp=rot(rm),rot(rp)
    def t(r):return np.arctan2(np.linalg.norm(r[[1,3]]),np.linalg.norm(r[[0,2]]))
    def delta(r):return np.arctan2(r[0]*r[3]-r[1]*r[2],r[0]*r[1]+r[2]*r[3])
    return np.array([t(rm),delta(rm),t(rp),delta(rp),np.arctan2(rp[2],rp[0])])


def main():
    from fractions import Fraction as F
    start=time.monotonic();record=json.loads((ROOT/'heat_normal_extreme_ROC.json').read_text())
    p=np.array([float(F(c)) for c in record['coefficients']]);rng=np.random.default_rng(20261028);n=100000
    rm=rng.normal(size=(n,4));rp=rng.normal(size=(n,4));rm/=np.linalg.norm(rm,axis=1)[:,None];rp/=np.linalg.norm(rp,axis=1)[:,None]
    for z,positive in [(rm,False),(rp,True)]:
        det=z[:,0]*z[:,3]-z[:,1]*z[:,2];flip=det<0 if positive else det>0;z[flip,1]*=-1;z[flip,3]*=-1
    difference=FGHT(rp,p)[3]-FGHT(rm,p)[3];eigen,vec=np.linalg.eigh(difference);i=int(np.argmin(eigen[:,0]))
    best={'value':float(eigen[i,0]),'Rminus':rm[i].tolist(),'Rplus':rp[i].tolist(),'A':vec[i,:,0].tolist(),'source':'100000 random signed pairs'}
    bounds=[(1e-5,np.pi/2-1e-5),(-np.pi+1e-5,-1e-5),(1e-5,np.pi/2-1e-5),(1e-5,np.pi-1e-5),(-np.pi,np.pi)]
    def objective(z):
        minus,plus=pair(z);value=np.linalg.eigvalsh(FGHT(plus,p)[3]-FGHT(minus,p)[3])[:,0]
        return value[0] if np.asarray(z).ndim==1 else value
    for seed in [20261028,20261029]:
        population=np.array([rng.uniform(a,b,80) for a,b in bounds]).T;population[0]=params(np.array(best['Rminus']),np.array(best['Rplus']))
        result=differential_evolution(objective,bounds,seed=seed,init=population,maxiter=180,tol=1e-10,atol=1e-12,
                                      vectorized=True,updating='deferred',workers=1,polish=True)
        minus,plus=pair(result.x);values,vectors=np.linalg.eigh(FGHT(plus,p)[3]-FGHT(minus,p)[3])
        if values[0,0]<best['value']:
            best={'value':float(values[0,0]),'Rminus':minus[0].tolist(),'Rplus':plus[0].tolist(),'A':vectors[0,:,0].tolist(),'source':f'bounded DE seed{seed}'}
    out={'status':'NUMERICAL_TRUE_PC_WITNESS_SEARCH_ONLY','best':best,'seconds':time.monotonic()-start,
         'scope':'Only exact finite support reconstruction can prove non-PC; a positive search is inconclusive.'}
    (ROOT/'DIRECT_PC_PROBE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
