from __future__ import annotations
from fractions import Fraction as F
import json,time
import numpy as np
import sympy as sp
from slow_sector import SlowRing,polymul,polyadd
from probe_moments import sf,ff

class RefinedRing(SlowRing):
    def setup(self):
        g=self.gamma;kap=self.kappa
        self.da=(1/g+1/(g+kap))/2; self.db=(1/(g+kap)-1/g)/2
        self.Dinv={0:self.da,1:self.db}
        H=sf(self.da)*self.G+sf(self.db)*self.R
        J=(self.T-sf(g)*sp.eye(self.n+1))*self.G.inv(method='DM')
        self.W=(sp.eye(self.n+1)+J*H).inv(method='DM')*J
        self.Wfloat=np.array(self.W,dtype=float)
    def favg(self,p): return sum(float(v)*float(self.corr(k)) for k,v in p.items())
    def inner(self,p,q):
        return sum(float(a)*float(b)*self.corrfloat(k^l) for k,a in p.items() for l,b in q.items())
    def Kfloat(self,p):
        out={};nu=float(self.nu);eta=float(self.eta);kap=float(self.kappa)
        for m,v in p.items():
            out[m]=out.get(m,0.)+(nu*m.bit_count()+kap/2)*v
            out[m^1]=out.get(m^1,0.)+kap*v/2
            for i in range(self.n):
                if (m>>i)&1:
                    for j in ((i-1)%self.n,(i+1)%self.n):
                        key=m^(1<<i)^(1<<j)
                        out[key]=out.get(key,0.)-nu*eta*v/2
        return {k:v for k,v in out.items() if v}
    def Cinvfloat(self,p):
        pD=polymul(p,{0:float(self.da),1:float(self.db)})
        z=np.array([sum(float(v)*float(self.corr(k^key)) for k,v in pD.items()) for key in self.ids])
        y=self.Wfloat@z
        correction=polymul({self.ids[i]:y[i] for i in range(self.n+1)}, {0:float(self.da),1:float(self.db)})
        return polyadd(pD,correction,-1.)
    def certificate(self,p,bits=32):
        a={k:F(round(float(v)*2**bits),2**bits) for k,v in p.items() if v}
        Ka=self.applyK(a);r=polyadd({0:F(1)},Ka,-1)
        lower=2*self.avg(a)-self.exinner(a,Ka)
        rD=polymul(r,self.Dinv)
        R0=self.exinner(r,rD)
        z=sp.Matrix([sf(sum(val*self.corr(mask^key) for mask,val in rD.items())) for key in self.ids])
        error=R0-ff((z.T*self.W*z)[0])
        if error<0: raise AssertionError('negative error')
        return {'tau_lo':float(lower),'tau_hi':float(lower+error),'ratio':float((lower+error)/lower),
                'terms':len(a),'residual_terms':len(r),'lower_exact':str(lower),'upper_exact':str(lower+error),
                'witness':{str(k):str(v) for k,v in a.items()}}
    def run(self,iterations=4,certify=True):
        start=time.perf_counter();self.setup();setup=time.perf_counter()
        # Full coefficient residual used every step to avoid drift.
        rhs=np.eye(self.n+1)[:,0]
        aa=np.linalg.solve(np.array(self.M,dtype=float),rhs)
        x={key:aa[i] for i,key in enumerate(self.ids)}
        r=polyadd({0:1.},self.Kfloat(x),-1.)
        z=self.Cinvfloat(r);d=z;rz=self.inner(r,z)
        rows=[]
        for it in range(iterations+1):
            if certify:
                c0=time.perf_counter();row=self.certificate(x);row['certificate_s']=time.perf_counter()-c0
            else:
                L=2*self.favg(x)-self.inner(x,self.Kfloat(x));er=self.inner(r,self.Cinvfloat(r))
                row={'tau_lo':L,'tau_hi':L+er,'ratio':(L+er)/L,'terms':len(x),'residual_terms':len(r)}
            row.update(iteration=it,elapsed_s=time.perf_counter()-start)
            rows.append(row)
            print(json.dumps({k:v for k,v in row.items() if k not in ['lower_exact','upper_exact','witness']}),flush=True)
            if it==iterations:break
            Kd=self.Kfloat(d);alpha=rz/self.inner(d,Kd)
            x=polyadd(x,d,alpha)
            rnew=polyadd({0:1.},self.Kfloat(x),-1.)
            znew=self.Cinvfloat(rnew);rznew=self.inner(rnew,znew)
            beta=rznew/rz
            d=polyadd(znew,d,beta);r=rnew;z=znew;rz=rznew
        return {'n':self.n,'t':str(self.t),'nu':str(self.nu),'kappa':str(self.kappa),
                'setup_s':setup-start,'total_s':time.perf_counter()-start,'rows':rows}
if __name__=='__main__':
    import sys
    n=int(sys.argv[1]);t=F(sys.argv[2]);its=int(sys.argv[3]);dest=sys.argv[4]
    R=RefinedRing(n,t);out=R.run(its)
    json.dump(out,open(dest,'w'))
