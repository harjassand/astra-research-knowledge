"""Source-aware slow-sector certificate for a zero-field ferromagnetic Ising ring.
All static contractions are exact. A float linear ansatz is converted to a dyadic
rational witness. No microscopic conformation enumeration occurs in this file.
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import lru_cache
import json,time,math
import numpy as np
import sympy as sp
from probe_moments import sf,ff

def polyadd(a,b,c=F(1)):
    out=a.copy()
    for key,val in b.items():
        out[key]=out.get(key,F(0))+c*val
        if not out[key]: del out[key]
    return out

def polymul(a,b):
    out={}
    for key,x in a.items():
        for key2,y in b.items(): out[key^key2]=out.get(key^key2,F(0))+x*y
    return {key:v for key,v in out.items() if v}

class SlowRing:
    def __init__(self,n:int,t:F,nu:F=F(1),kappa:F=F(1)):
        if n<4 or t<1 or nu<=0 or kappa<=0: raise ValueError('invalid model')
        self.n=n; self.t=F(t); self.nu=F(nu); self.kappa=F(kappa)
        self.u=(self.t-1)/(self.t+1)
        self.ca=self.u.numerator; self.cb=self.u.denominator
        self.Zcorr=self.ca**n+self.cb**n
        self.eta=(self.t**2-1)/(self.t**2+1)
        self.gamma=2*self.nu*((1-self.eta)+2*self.eta/F(n*n))
        self.lambdaslow=self.nu*(1-self.eta)
        self.ids=[0]+[1<<i for i in range(n)]
        self.G=sp.Matrix(n+1,n+1,lambda i,j: sf(self.corr(self.ids[i]^self.ids[j])))
        self.T=sp.zeros(n+1)
        for j in range(n):
            self.T[j+1,j+1]=sf(self.nu)
            self.T[(j-1)%n+1,j+1]=-sf(self.nu*self.eta/2)
            self.T[(j+1)%n+1,j+1]=-sf(self.nu*self.eta/2)
        self.R=sp.Matrix(n+1,n+1,lambda i,j:sf(self.corr(self.ids[i]^self.ids[j]^1)))
        self.M=self.G*self.T+sf(self.kappa/2)*(self.G+self.R)
        self.kpoly={0:self.kappa/2,1:self.kappa/2}
    @lru_cache(None)
    def corrnum(self,mask:int):
        if not mask:return self.Zcorr
        if mask.bit_count()%2:return 0
        inds=[i for i in range(self.n) if (mask>>i)&1]
        ell=sum(inds[i+1]-inds[i] for i in range(0,len(inds),2))
        return self.ca**ell*self.cb**(self.n-ell)+self.ca**(self.n-ell)*self.cb**ell
    @lru_cache(None)
    def corr(self,mask:int):
        return F(self.corrnum(mask),self.Zcorr)
    @lru_cache(None)
    def corrfloat(self,mask:int):
        return self.corrnum(mask)/self.Zcorr
    def exinner(self,p,q,mask=0):
        import math
        dp=1;dq=1
        for v in p.values():dp=math.lcm(dp,v.denominator)
        for v in q.values():dq=math.lcm(dq,v.denominator)
        pp=[(k,v.numerator*(dp//v.denominator)) for k,v in p.items()]
        qq=[(k,v.numerator*(dq//v.denominator)) for k,v in q.items()]
        total=sum(a*b*self.corrnum(k^l^mask) for k,a in pp for l,b in qq)
        return F(total,dp*dq*self.Zcorr)
    def avg(self,poly):return sum(val*self.corr(key) for key,val in poly.items())
    def applyL(self,poly):
        out={}
        for mask,val in poly.items():
            out[mask]=out.get(mask,F(0))+self.nu*mask.bit_count()*val
            for i in range(self.n):
                if (mask>>i)&1:
                    for j in ((i-1)%self.n,(i+1)%self.n):
                        key=mask^(1<<i)^(1<<j)
                        out[key]=out.get(key,F(0))-self.nu*self.eta*val/2
        return {key:v for key,v in out.items() if v}
    def applyK(self,poly):return polyadd(self.applyL(poly),polymul(self.kpoly,poly))
    def solve(self,bits=40,exact_proposal=False):
        start=time.perf_counter();n=self.n
        b=sp.zeros(n+1,1); b[0]=1
        if exact_proposal:
            a=self.M.inv(method='DM')*b
            a=[ff(x) for x in a]
        else:
            arr=np.array(self.M,dtype=float)
            ar=np.linalg.solve(arr,np.eye(n+1)[:,0])
            a=[F(round(float(x)*2**bits),2**bits) for x in ar]
        proposed=time.perf_counter()
        v={self.ids[i]:a[i] for i in range(n+1)}
        Kv=self.applyK(v); residual=polyadd({0:F(1)},Kv,-1)
        lower=2*self.avg(v)-self.avg(polymul(v,Kv))
        g=self.gamma; kap=self.kappa
        da=(1/g+1/(g+kap))/2; db=(1/(g+kap)-1/g)/2
        Dinv={0:da,1:db}
        # Exact Woodbury formula: C=D+B J B*, J=(T-gamma I)G^{-1}.
        # Invert only (n+1)x(n+1); never assemble the full generator.
        H=sf(da)*self.G+sf(db)*self.R
        J=(self.T-sf(g)*sp.eye(n+1))*self.G.inv(method='DM')
        z=sp.Matrix([sf(self.avg(polymul({key:F(1)},polymul(Dinv,residual)))) for key in self.ids])
        R0=self.avg(polymul(polymul(residual,residual),Dinv))
        acquired=time.perf_counter()
        y=(sp.eye(n+1)+J*H).inv(method='DM')*(J*z)
        correction=ff((z.T*y)[0])
        error=R0-correction
        if error<0: raise AssertionError('negative certified error')
        upper=lower+error
        final=time.perf_counter()
        return {'n':n,'t':str(self.t),'nu':str(self.nu),'kappa':str(kap),
                'lambda_slow':float(self.lambdaslow),'gamma_complement':float(g),
                'tau_lo':float(lower),'tau_hi':float(upper),'ratio':float(upper/lower),
                'closed_lo':float(2*lower-2/kap),'closed_hi':float(2*upper-2/kap),
                'proposal_s':proposed-start,'static_certificate_s':acquired-proposed,
                'small_inverse_s':final-acquired,'solve_total_s':final-start,
                'residual_terms':len(residual),'coefficients':[str(x) for x in a],
                'lower_exact':str(lower),'upper_exact':str(upper),'rounding_bits':bits,
                'error_exact':str(error)}

if __name__=='__main__':
    import sys
    n=int(sys.argv[1]) if len(sys.argv)>1 else 16
    t=F(sys.argv[2]) if len(sys.argv)>2 else F(10)
    start=time.perf_counter();R=SlowRing(n,t);out=R.solve();out['assembly_and_total_s']=time.perf_counter()-start
    print(json.dumps(out),flush=True)
