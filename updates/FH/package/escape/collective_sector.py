"""Two-dimensional acquired slow-mode closure plus energy-discovered defects.
Uses no tensor-rank hypothesis or full-state array. All final contractions are rational.
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import lru_cache
import time,json
import numpy as np
import scipy.sparse as ss
import scipy.sparse.linalg as sla

class CollectiveRing:
    def __init__(self,n:int,t:F,nu:F=F(1),kappa:F=F(1)):
        if n<4 or t<1 or nu<=0 or kappa<=0:raise ValueError('invalid model')
        self.n=n;self.t=F(t);self.nu=F(nu);self.kappa=F(kappa)
        self.eta=(self.t**2-1)/(self.t**2+1)
        self.lam=self.nu*(1-self.eta)
        self.gamma=self.nu*((1-self.eta)+4*self.eta/F(n*n))
        u=(self.t-1)/(self.t+1)
        self.s=self.t/F(n)*(1-u**n)/(1+u**n)
        self.Z=(self.t+1)**n+(self.t-1)**n
        self.da=(1/self.gamma+1/(self.gamma+self.kappa))/2
        self.db=(1/(self.gamma+self.kappa)-1/self.gamma)/2
        # J is diagonal, so W=(J^{-1}+H)^{-1}. J may have a zero entry
        # at t=1; use (I+JH)^{-1}J to cover that case as well.
        j0=-self.gamma;j1=(self.lam-self.gamma)/self.s
        h00=self.da;h01=self.db*self.s;h11=self.da*self.s
        a=1+j0*h00;b=j0*h01;c=j1*h01;d=1+j1*h11
        det=a*d-b*c
        self.W00=d*j0/det;self.W01=-b*j1/det;self.W11=a*j1/det
        assert self.W01==-c*j0/det
    def states(self):
        n=self.n;states={0,(1<<n)-1}
        for start in range(n):
            mask=0
            for length in range(1,n):
                mask|=1<<((start+length-1)%n);states.add(mask)
        return sorted(states)
    @lru_cache(None)
    def wallcount(self,x):
        rot=((x<<1)&((1<<self.n)-1)) | (x>>(self.n-1))
        return (x^rot).bit_count()
    @lru_cache(None)
    def prob(self,x):return self.t**(self.n-self.wallcount(x))/self.Z
    def rate(self,x,i):
        n=self.n;s=1 if (x>>i)&1 else -1
        a=1 if (x>>((i-1)%n))&1 else -1
        b=1 if (x>>((i+1)%n))&1 else -1
        return self.nu*(1-self.eta*s*F(a+b,2))/2
    def certificate(self,v):
        Kv={}
        for x,vx in v.items():
            diag=self.kappa*int(bool(x&1))
            for i in range(self.n):
                rt=self.rate(x,i);diag+=rt;y=x^(1<<i)
                Kv[y]=Kv.get(y,F(0))-self.rate(y,i)*vx
            Kv[x]=Kv.get(x,F(0))+diag*vx
        dr={x:-val for x,val in Kv.items() if val}
        src=sum(self.prob(x)*vx for x,vx in v.items())
        energy=sum(self.prob(x)*vx*Kv[x] for x,vx in v.items())
        lower=2*src-energy
        R0=self.da;z0=self.da;z1=self.db*self.s
        for x,dx in dr.items():
            wt=self.prob(x)/(self.gamma+self.kappa*int(bool(x&1)))
            R0+=wt*(2*dx+dx*dx)
            z0+=wt*dx;z1+=wt*dx*F(2*x.bit_count()-self.n,self.n)
        error=R0-(self.W00*z0*z0+2*self.W01*z0*z1+self.W11*z1*z1)
        if error<0:raise AssertionError('negative error')
        return lower,lower+error,len(dr)
    def run(self,bits=32):
        started=time.perf_counter();states=self.states();indices={s:i for i,s in enumerate(states)}
        rows=[];cols=[];vals=[];N=len(states)
        for row,x in enumerate(states):
            diag=float(self.kappa*int(bool(x&1)))
            for i in range(self.n):
                rate=float(self.rate(x,i));diag+=rate;y=x^(1<<i)
                if y in indices:rows.append(row);cols.append(indices[y]);vals.append(-rate)
            rows.append(row);cols.append(row);vals.append(diag)
        K=ss.csr_matrix((vals,(rows,cols)),shape=(N,N))
        v0=sla.spsolve(K,np.ones(N))
        v={s:F(round(float(v0[i])*2**bits),2**bits) for i,s in enumerate(states)}
        proposed=time.perf_counter();lo,hi,RN=self.certificate(v);ended=time.perf_counter()
        return {'n':self.n,'t':str(self.t),'nu':str(self.nu),'kappa':str(self.kappa),
                'tau_lo':float(lo),'tau_hi':float(hi),'ratio':float(hi/lo),
                'closed_lo':float(2*lo-2/self.kappa),'closed_hi':float(2*hi-2/self.kappa),
                'low_states':len(states),'residual_neighborhood':RN,'full_states':str(1<<self.n),
                'lambda_slow':str(self.lam),'gamma_complement':str(self.gamma),
                'proposal_s':proposed-started,'certification_s':ended-proposed,'run_s':ended-started,
                'lower_exact':str(lo),'upper_exact':str(hi),'witness':{str(k):str(v) for k,v in v.items()},
                'bits':bits,'omitted_mass':str(1-sum(self.prob(x) for x in states))}

if __name__=='__main__':
    import sys
    n=int(sys.argv[1]);t=F(sys.argv[2]);dest=sys.argv[3]
    start=time.perf_counter();R=CollectiveRing(n,t);out=R.run();out['total_s']=time.perf_counter()-start
    json.dump(out,open(dest,'w'))
    print(json.dumps({k:v for k,v in out.items() if k not in ['witness','lower_exact','upper_exact']}))
