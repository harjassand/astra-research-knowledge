"""Ordinary small SU(2) variational spin-two MPS. No gap/tail inference.

An independent finite-ring integer contraction, rather than this optimization,
must establish any eventual strict variational input.
"""
from __future__ import annotations
import pathlib,sys,math,json,time,argparse
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'sol6_openings_20261027/positive_current_operation/vendor'))
import numpy as np
from scipy.optimize import minimize


def cg(j1,m1,j2,m2,J,M):
    if M!=m1+m2 or abs(M)>J or not(abs(j1-j2)<=J<=j1+j2):return 0.0
    f=math.factorial
    pref=math.sqrt((2*J+1)*f(J+j1-j2)*f(J-j1+j2)*f(j1+j2-J)/f(j1+j2+J+1))
    pref*=math.sqrt(f(J+M)*f(J-M)*f(j1-m1)*f(j1+m1)*f(j2-m2)*f(j2+m2))
    total=0.0
    for k in range(j1+j2+J+2):
        a=[k,j1+j2-J-k,j1-m1-k,j2+m2-k,J-j2+m1+k,J-j1-m2+k]
        if min(a)<0:continue
        total+=(-1)**k/math.prod(f(x) for x in a)
    return pref*total


class Ansatz:
    def __init__(self,jmax=3):
        self.js=list(range(jmax+1));self.labels=[(j,m)for j in self.js for m in range(-j,j+1)];self.dim=len(self.labels)
        self.pairs=[(j,k)for j in self.js for k in self.js if abs(j-k)<=2<=j+k]
        self.basis=[]
        for j,k in self.pairs:
            a=np.zeros((5,self.dim,self.dim))
            for i,(jj,m)in enumerate(self.labels):
                for l,(kk,n)in enumerate(self.labels):
                    if jj==j and kk==k:
                        for s in range(-2,3):a[s+2,i,l]=cg(j,m,2,s,k,n)
            self.basis.append(a)
        self.basis=np.array(self.basis)
        self.dims=np.array([2*j+1 for j in self.js],float)
        self.label_js=np.array([j for j,m in self.labels],int)

    def tensors(self,p):return np.einsum('p,psij->sij',np.asarray(p)/np.linalg.norm(p),self.basis)

    def energy(self,p,return_info=False):
        p=np.asarray(p)/np.linalg.norm(p);a=np.einsum('p,psij->sij',p,self.basis)
        reduced=np.zeros((len(self.js),len(self.js)))
        for v,(j,k)in zip(p,self.pairs):reduced[j,k]=v*v*self.dims[k]/self.dims[j]
        vals,right=np.linalg.eig(reduced);i=int(np.argmax(vals.real));lam=float(vals[i].real);r=right[:,i].real
        vl,left=np.linalg.eig(reduced.T);i2=int(np.argmin(np.abs(vl-lam)));ell=left[:,i2].real/self.dims
        if np.sum(r)<0:r=-r
        if np.sum(ell)<0:ell=-ell
        if min(r)<-1e-10 or min(ell)<-1e-10:raise ArithmeticError('nonpositive reduced fixed point')
        norm=np.sum(self.dims*ell*r);l=ell[self.label_js];rr=r[self.label_js];weight=l[:,None]*rr[None,:]
        b=np.einsum('sij,tjk->stik',a,a)
        energy=0.0
        for s in range(-2,3):
            for t in range(-2,3):
                energy+=s*t*np.sum(weight*b[s+2,t+2]**2)
                if s<2 and t>-2:
                    hop=.5*math.sqrt((6-s*(s+1))*(6-t*(t-1)))
                    energy+=2*hop*np.sum(weight*b[s+2,t+2]*b[s+3,t+1])
        energy/=lam*lam*norm
        if return_info:
            transfer=sum(np.kron(x,x)for x in a);ev=np.linalg.eigvals(transfer);mods=np.sort(np.abs(ev))[::-1];xi=-1/math.log(mods[1]/mods[0])
            return float(energy),{'norm_transfer_eigenvalue':lam,'correlation_length_from_mps_transfer':xi,'dimension':self.dim,'pairs':self.pairs,'parameters':p.tolist(),'tensors':a.tolist(),'auxiliary_labels':self.labels}
        return float(energy)


def optimize(jmax,output,restarts=3):
    ans=Ansatz(jmax);baseline=np.zeros(len(ans.pairs));baseline[ans.pairs.index((1,1))]=1
    aklt=ans.energy(baseline);assert abs(aklt+4.5)<1e-11
    rng=np.random.default_rng(271027);runs=[];best=None;start=time.monotonic()
    for trial in range(restarts):
        x0=baseline+.15*rng.standard_normal(len(baseline))
        opt=minimize(ans.energy,x0,method='BFGS',options={'maxiter':500,'gtol':2e-8})
        energy,info=ans.energy(opt.x,True);runs.append({'trial':trial,'energy':energy,'success':bool(opt.success),'message':str(opt.message),'iterations':int(opt.nit),'evaluations':int(opt.nfev)})
        print(runs[-1],flush=True)
        if best is None or energy<best['energy']:best={'energy':energy,**info}
        pathlib.Path(output).write_text(json.dumps({'status':'FLOATING_VARIATIONAL_SEARCH_NOT_FINITE_RING_CERTIFICATE','jmax':jmax,'aklt_energy':aklt,'best':best,'runs':runs,'seconds':time.monotonic()-start},indent=2))
    return best


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--jmax',type=int,default=3);ap.add_argument('--restarts',type=int,default=3);ap.add_argument('--output',required=True);a=ap.parse_args();optimize(a.jmax,a.output,a.restarts)
