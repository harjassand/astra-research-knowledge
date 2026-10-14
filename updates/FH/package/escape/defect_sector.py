"""Energy-discovered defect states plus exact all-state source certification.
Only zero/two-wall states and their one-flip neighborhood are listed.
"""
from fractions import Fraction as F
from functools import lru_cache
import json,time
import numpy as np
import scipy.sparse as ss
import scipy.sparse.linalg as sla
import sympy as sp
from refine_sector import RefinedRing
from probe_moments import sf,ff

class DefectRing(RefinedRing):
    def states(self):
        n=self.n;S={0,(1<<n)-1}
        for start in range(n):
            mask=0
            for length in range(1,n):
                mask|=1<<((start+length-1)%n);S.add(mask)
        return sorted(S)
    @lru_cache(None)
    def wallcount(self,x):
        n=self.n
        rot=((x<<1)&((1<<n)-1)) | (x>>(n-1))
        return (x^rot).bit_count()
    def prob(self,x):
        n=self.n;t=self.t
        return t**(n-self.wallcount(x))/((t+1)**n+(t-1)**n)
    def rate(self,x,i):
        n=self.n;s=1 if (x>>i)&1 else -1
        a=1 if (x>>((i-1)%n))&1 else -1
        b=1 if (x>>((i+1)%n))&1 else -1
        return self.nu*(1-self.eta*s*F(a+b,2))/2
    def run(self,bits=32):
        start=time.perf_counter();self.setup();setup=time.perf_counter()
        states=self.states();indices={s:i for i,s in enumerate(states)}
        rows=[];cols=[];vals=[];N=len(states)
        for row,x in enumerate(states):
            diag=float(self.kappa*((x&1)!=0))
            for i in range(self.n):
                rate=float(self.rate(x,i));diag+=rate;y=x^(1<<i)
                if y in indices:rows.append(row);cols.append(indices[y]);vals.append(-rate)
            rows.append(row);cols.append(row);vals.append(diag)
        K=ss.csr_matrix((vals,(rows,cols)),shape=(N,N))
        v0=sla.spsolve(K,np.ones(N))
        v={s:F(round(float(v0[i])*2**bits),2**bits) for i,s in enumerate(states)}
        proposed=time.perf_counter()
        # Exact K v with v=0 on the unrepresented states. Detailed balance
        # permits collecting incoming changes from the known local moves.
        Kv={}
        for x,vx in v.items():
            diag=self.kappa*int(bool(x&1))
            for i in range(self.n):
                rate=self.rate(x,i);diag+=rate;y=x^(1<<i)
                Kv[y]=Kv.get(y,F(0))-self.rate(y,i)*vx
            Kv[x]=Kv.get(x,F(0))+diag*vx
        # r=1+delta_r where delta_r=-Kv, supported on a polynomial neighborhood.
        dr={x:-v for x,v in Kv.items() if v}
        # Exact variational lower.
        src=sum(self.prob(x)*vx for x,vx in v.items())
        energy=sum(self.prob(x)*vx*Kv[x] for x,vx in v.items())
        lower=2*src-energy
        # Whole-space r^2/D and <B,r/D>, including the entire unlisted source 1.
        R0=self.da
        z=[self.da]+[self.db*self.corr(1^(1<<i)) for i in range(self.n)]
        for x,dx in dr.items():
            invD=1/(self.gamma+self.kappa*int(bool(x&1)))
            wt=self.prob(x)*invD
            R0+=wt*(2*dx+dx*dx)
            z[0]+=wt*dx
            for i in range(self.n):z[i+1]+=wt*dx*(1 if (x>>i)&1 else -1)
        zs=sp.Matrix([sf(a) for a in z])
        error=R0-ff((zs.T*self.W*zs)[0])
        if error<0:raise AssertionError('negative error')
        upper=lower+error
        ended=time.perf_counter()
        return {'n':self.n,'t':str(self.t),'nu':str(self.nu),'kappa':str(self.kappa),
                'tau_lo':float(lower),'tau_hi':float(upper),'ratio':float(upper/lower),
                'closed_lo':float(2*lower-2/self.kappa),'closed_hi':float(2*upper-2/self.kappa),
                'low_states':len(states),'residual_neighborhood':len(dr),'full_states':str(1<<self.n),
                'setup_s':setup-start,'proposal_s':proposed-setup,'certification_s':ended-proposed,'total_s':ended-start,
                'lower_exact':str(lower),'upper_exact':str(upper),'witness':{str(k):str(v) for k,v in v.items()},
                'bits':bits,'omitted_mass':str(1-sum(self.prob(x) for x in states))}
if __name__=='__main__':
    import sys
    R=DefectRing(int(sys.argv[1]),F(sys.argv[2]));out=R.run();json.dump(out,open(sys.argv[3],'w'))
    print(json.dumps({k:v for k,v in out.items() if k not in ['witness','lower_exact','upper_exact']}))
