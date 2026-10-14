"""Probe a signed Poisson-extension quartic storage. No certificate inferred from search."""
import os,json,math
os.environ['OMP_NUM_THREADS']='1'
import numpy as np
import torch
from numpy.polynomial.legendre import leggauss

torch.set_default_dtype(torch.float64);torch.set_num_threads(1)

def energy(z,w,kind='DM'):
    u=z.abs()**2;v=w.abs()**2;q=(z.conj()*w).imag
    if kind=='DM': return (u+v)**2-4/math.sqrt(3)*(u+v)*q
    if kind=='G': return 3*(u+v-2*q)**2+35/24*u**2+q**2-2.5*q*u
    raise ValueError(kind)
def odd(z,w,kind):
    u=z.abs()**2;v=w.abs()**2;q=(z.conj()*w).imag
    if kind=='DM': return -4/math.sqrt(3)*(u+v)*q
    return -14.5*q*u-12*q*v

class Basis:
    def __init__(self,N):
        self.N=N
        self.ns=torch.tensor([i for i in range(-N,N+1) if i])
        self.nv=torch.arange(-N,N+1)
        ny=4*N+1;y=torch.arange(ny)*2*math.pi/ny
        self.B=torch.exp(1j*self.ns[:,None]*y)
        self.Bv=torch.exp(1j*self.nv[:,None]*y)
        # t=e^x in (0,1), dx=dt/t. Quartic integrand degree at most 4N.
        t,wt=leggauss(2*N+1);t=(t+1)/2;wt=wt/2
        self.t=torch.tensor(t);self.wt=torch.tensor(wt/t)
        self.E=self.t[:,None]**self.ns.abs()[None,:]
    def storage(self,cr,kind):
        c=torch.view_as_complex(cr.contiguous())
        vx=((self.E*self.ns.abs()[None,:])*c[None,:])@self.B
        py=((self.E*(1j*self.ns)[None,:])*c[None,:])@self.B
        return .5*(odd(vx,py,kind).mean(-1)*self.wt).sum()
    def evaluate(self,cr,vr,kind,coef=1.):
        c=torch.view_as_complex(cr.contiguous());v=torch.view_as_complex(vr.contiguous())
        py=(1j*self.ns*c)@self.B
        vy=v@self.Bv
        P=self.storage(cr,kind)*coef
        g=torch.autograd.grad(P,cr,create_graph=True)[0]
        # profile velocity has zero mode invisible to storage
        vidxs=[i for i,n in enumerate(self.nv.tolist()) if n]
        dp=(g*vr[vidxs]).sum()
        norm=((vy.abs()**2+py.abs()**2)**2).mean()
        return (energy(vy,py,kind).mean()-dp)/norm, norm,P,dp

def run(N=3,kind='DM',seed=0,steps=400,coef=1.):
    torch.manual_seed(seed);bs=Basis(N)
    cr=torch.randn(2*N,2,requires_grad=True);vr=torch.randn(2*N+1,2,requires_grad=True)
    opt=torch.optim.Adam([cr,vr],lr=.025)
    best=None
    for k in range(steps):
        opt.zero_grad(); loss,norm,P,dp=bs.evaluate(cr,vr,kind,coef)
        if not torch.isfinite(loss):break
        loss.backward();opt.step()
        if best is None or loss.item()<best['ratio']:
            best=dict(N=N,kind=kind,seed=seed,coef=coef,step=k,ratio=loss.item(),norm=norm.item(),P=P.item(),dp=dp.item(),u=cr.detach().tolist(),v=vr.detach().tolist())
    # reevaluate saved next-iterate coefficients rather than mismatching reported values
    cr2=torch.tensor(best['u'],requires_grad=True);vr2=torch.tensor(best['v'],requires_grad=True)
    l,n,p,d=bs.evaluate(cr2,vr2,kind,coef)
    best.update(ratio=l.item(),norm=n.item(),P=p.item(),dp=d.item())
    return best
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--steps',type=int,default=400);ap.add_argument('--N',type=int,default=3);ap.add_argument('--kind',default='DM');ap.add_argument('--coef',type=float,default=1.);ap.add_argument('--seeds',type=int,default=3);a=ap.parse_args()
    out=[]
    for seed in range(a.seeds):
        r=run(a.N,a.kind,seed,a.steps,a.coef);out.append(r);print(seed,r['ratio'],flush=True)
    path=f'/mnt/data/ASTRA_Universal_Compensation/exploration/poisson_{a.kind}_N{a.N}_c{a.coef}.json'
    json.dump(out,open(path,'w'),indent=2)
