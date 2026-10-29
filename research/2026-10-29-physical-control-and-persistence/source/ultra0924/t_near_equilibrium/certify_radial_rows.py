"""Outward full-domain row receiver for a proposed radial correction operator.

LAD chooses arbitrary dyadic controls; only subsequent interval bounds admit
them. No finite-preview value certifies a continuum sign. Gaussian tail is
analytic; there is no velocity cutoff on the target.
"""
from fractions import Fraction as F
from pathlib import Path
import json,math,time
import numpy as np
from scipy.special import roots_genlaguerre,erf
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,hstack,vstack,eye
from flint import arb,fmpq,ctx

ctx.prec=128
beta=F(3,4)

def ball(x):
    x=F(x);return arb(fmpq(x.numerator,x.denominator))

def dyadic(x):
    m,e=x.man_exp();m,e=int(m),int(e)
    return F(m*(1<<e)) if e>=0 else F(m,1<<-e)

def serialized(x):
    x=F(x);return [x.numerator,x.denominator]

class Receiver:
    def __init__(self):
        self.beta=ball(beta);self.sqrt2pi=(2/arb.pi()).sqrt()
        self.step=F(1,32);self.S=F(16);self.eta=F(99,100)
        self.grid=[self.step*j for j in range(int(self.S/self.step)+1)]
        self.A_cache={F(0):arb(4)}
        self.probabilities=[(self.cdf(b)-self.cdf(a)).upper() for a,b in zip(self.grid,self.grid[1:])]
        self.first_inverse=(self.sqrt2pi*self.beta.sqrt()*(1-(-self.beta*ball(self.step)**2/2).exp())).upper()
        self.first_probability=self.cdf(self.step).upper()
        ss=ball(self.S);ee=(-self.beta*ss**2/2).exp()
        self.tail0=(ss*(2*self.beta/arb.pi()).sqrt()*ee+(ss*(self.beta/2).sqrt()).erfc()).upper()
        self.tail_minus=(self.sqrt2pi*self.beta.sqrt()*ee).upper()
        self.tail1=(self.sqrt2pi*self.beta.sqrt()*ee*(ss**2+2/self.beta)).upper()
        self.tail2=(self.sqrt2pi*self.beta.sqrt()*ss**3*ee+3/self.beta*self.tail0).upper()
        xx,ww=roots_genlaguerre(192,.5)
        self.speed=np.sqrt(2*xx/float(beta));self.weights=ww/math.gamma(1.5)
        self.design=np.column_stack([np.ones(len(xx)),self.speed**2])
        mm=csr_matrix(self.design*self.weights[:,None]);ii=eye(len(xx),format='csr')
        self.constraints=vstack([hstack([-mm,-ii]),hstack([mm,-ii])],format='csr')
        self.evaluated=0

    def cdf(self,s):
        s=ball(s);return (s*(self.beta/2).sqrt()).erf()-s*(2*self.beta/arb.pi()).sqrt()*(-self.beta*s*s/2).exp()

    def A(self,s):
        s=F(s)
        if s not in self.A_cache:
            z=ball(s)
            self.A_cache[s]=4*(arb.pi()/2).sqrt()*((z*z/2).exp())*(z/arb(2).sqrt()).erf()/z-z*z/3
        return self.A_cache[s]

    def nu(self,v):
        if v==0:return 2*self.sqrt2pi
        v=ball(v)
        return self.sqrt2pi*(-v*v/2).exp()+(v+1/v)*(v/arb(2).sqrt()).erf()

    def controls(self,v):
        v=float(v)
        if v==0:kk=4/self.speed-self.speed
        else:
            mm=np.minimum(v,self.speed)
            kk=2*math.sqrt(2*math.pi)/(v*self.speed)*np.exp(mm**2/2)*erf(mm/math.sqrt(2))-((v+self.speed)**3-np.abs(v-self.speed)**3)/(6*v*self.speed)
        rhs=self.weights*kk
        fit=linprog(np.r_[np.zeros(2),np.ones(len(kk))],A_ub=self.constraints,
                    b_ub=np.r_[-rhs,rhs],bounds=[(None,None)]*2+[(0,None)]*len(kk),method='highs')
        if not fit.success:raise ArithmeticError(fit.message)
        return [F(round(float(x)*2**24),2**24) for x in fit.x[:2]]

    def bound(self,lo,hi,controls):
        self.evaluated+=1
        a,c=controls;delta=self.step
        total=self.A(delta).upper()*self.first_inverse
        total+=(ball(hi+4*delta/3+abs(a)+abs(c)*delta**2)*self.first_probability)
        for j in range(1,len(self.grid)-1):
            s0,s1=self.grid[j:j+2]
            low=self.A(min(lo,s0))/ball(max(hi,s1))-ball(max(hi,s1))
            high=self.A(min(hi,s1))/ball(max(lo,s0))-ball(max(lo,s0))
            p0=a+min(c*s0*s0,c*s1*s1);p1=a+max(c*s0*s0,c*s1*s1)
            upper=max(abs(low-ball(p1)).upper(),abs(high-ball(p0)).upper())
            total+=upper*max(arb(0),self.probabilities[j])
        total+=self.A(hi).upper()*self.tail_minus+self.tail1+ball(abs(a))*self.tail0+ball(abs(c))*self.tail2
        factor=self.beta**(-1)*self.beta.rsqrt()*(-(1-self.beta)*ball(lo)**2/2).exp()/self.nu(lo)
        return (factor*total).upper()


def main():
    started=time.perf_counter();receiver=Receiver()
    pending=[(F(0),F(8))];admitted=[];failed=[]
    while pending:
        lo,hi=pending.pop();controls=receiver.controls((lo+hi)/2)
        upper=receiver.bound(lo,hi,controls)
        if upper<ball(receiver.eta):
            admitted.append({'v_interval':[serialized(lo),serialized(hi)],
                             'controls':[serialized(x) for x in controls],
                             'row_bound_upper':serialized(dyadic(upper))})
        elif hi-lo<=F(1,4096) or receiver.evaluated>=8192:
            failed.append({'lo':str(lo),'hi':str(hi),'upper':str(upper)})
            break
        else:
            mid=(lo+hi)/2;pending.extend([(mid,hi),(lo,mid)])
        if receiver.evaluated%128==0:
            print('evaluated',receiver.evaluated,'admitted',len(admitted),'pending',len(pending),flush=True)
    # Full tail v>=8, no moment control: positive gain plus absolute loss.
    v=ball(8)
    tail=(4/(receiver.beta*(1-receiver.beta)*v*v)+receiver.beta**(-1)*receiver.beta.rsqrt()*(-(1-receiver.beta)*v*v/2).exp()*(1+2*(2/(arb.pi()*receiver.beta)).sqrt()/v)).upper()
    result={'status':'PASS_continuum_row_certificate' if not failed and not pending and tail<ball(receiver.eta) else 'NOT_ACQUIRED',
            'beta':'3/4','eta':'99/100','s_mesh_step':str(receiver.step),'analytic_tail_start':str(receiver.S),
            'head_admission':admitted,'failures':failed,'pending':[[str(a),str(b)] for a,b in pending],
            'v_tail_start':8,'v_tail_bound_upper':serialized(dyadic(tail)),
            'evaluated':receiver.evaluated,'elapsed_seconds':time.perf_counter()-started,
            'source_or_density_lower_bound_acquired':False,'normalized_iid_sampler_acquired':False}
    out=Path(__file__).parent/'RADIAL_ROW_CERTIFICATE.json';out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','eta','failures','evaluated','elapsed_seconds','v_tail_bound_upper']},indent=2))


if __name__=='__main__':
    main()
