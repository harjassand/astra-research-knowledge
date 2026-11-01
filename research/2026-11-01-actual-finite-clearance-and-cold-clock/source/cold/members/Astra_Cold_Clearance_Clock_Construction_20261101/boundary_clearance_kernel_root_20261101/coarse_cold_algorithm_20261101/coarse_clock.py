#!/usr/bin/env python3
"""Exact-integer validated enclosure of e'=2(s+3e^2/4)^2 blow-up time.
No floating-point value participates in a mathematical decision or certificate.
See PROOF.md for startup, inverse Taylor and nonexpansive error propagation.
"""
from fractions import Fraction as F
from dataclasses import dataclass
from pathlib import Path
import argparse, hashlib, json, time

BITS = 80
Q = 1 << BITS
OPS = {'add': 0, 'mul': 0, 'div': 0}

def ceildiv(a, b):
    assert b > 0
    return -((-a)//b)

def floorq(x): return x.numerator*Q//x.denominator
def ceilq(x): return ceildiv(x.numerator*Q, x.denominator)

@dataclass(frozen=True)
class IV:
    lo: int
    hi: int
    def __post_init__(self):
        assert self.lo <= self.hi
        if max(abs(self.lo).bit_length(),abs(self.hi).bit_length())>2048:
            raise RuntimeError('2048-bit interval stored-word guard')
    @staticmethod
    def exact(x):
        x = F(x)
        return IV(floorq(x), ceilq(x))
    @staticmethod
    def bounds(a,b): return IV(floorq(F(a)),ceilq(F(b)))
    def __add__(self, other):
        if not isinstance(other, IV): other=IV.exact(other)
        OPS['add'] += 1
        return IV(self.lo+other.lo,self.hi+other.hi)
    __radd__=__add__
    def __neg__(self): return IV(-self.hi,-self.lo)
    def __sub__(self,other): return self+-other if isinstance(other,IV) else self+(-F(other))
    def __mul__(self,other):
        if not isinstance(other,IV): other=IV.exact(other)
        OPS['mul'] += 1
        p=[self.lo*other.lo,self.lo*other.hi,self.hi*other.lo,self.hi*other.hi]
        return IV(min(p)//Q,ceildiv(max(p),Q))
    __rmul__=__mul__
    def reciprocal(self):
        assert self.lo>0 or self.hi<0, 'interval division through zero'
        OPS['div'] += 1
        # Reciprocal is decreasing on each connected component away from zero.
        if self.lo>0:
            return IV(Q*Q//self.hi,ceildiv(Q*Q,self.lo))
        return -((-self).reciprocal())
    def __truediv__(self,other):
        if not isinstance(other,IV): other=IV.exact(other)
        return self*other.reciprocal()
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        result=IV.exact(1)
        for _ in range(n): result=result*self
        return result

MAX_RATIONAL_BITS=0
STARTUP_PAIR_VISITS=0
def guard_rational(x):
    global MAX_RATIONAL_BITS
    x=F(x)
    bits=max(abs(x.numerator).bit_length(),x.denominator.bit_length())
    MAX_RATIONAL_BITS=max(MAX_RATIONAL_BITS,bits)
    if bits>2048: raise RuntimeError('2048-bit rational stored-word guard')
    return x

def conv(a,b):
    global STARTUP_PAIR_VISITS
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                STARTUP_PAIR_VISITS+=1
                if y: out[i+j]=guard_rational(out[i+j]+guard_rational(x*y))
    return out

def peval(a,x):
    out=F(0)
    for c in reversed(a): out=guard_rational(guard_rational(out*x)+c)
    return out

def startup(degree=28):
    """Nonnegative forward polynomial plus a certified linear supersolution."""
    p=[F(0)]*(degree+1)
    # e'=2s^2+3s e^2+(9/8)e^4.
    for n in range(degree):
        p2=conv(p[:n+1],p[:n+1])
        p4=conv(p2,p2)
        coeff=(F(2) if n==2 else 0)
        if n>=1 and n-1<len(p2): coeff+=3*p2[n-1]
        if n<len(p4): coeff+=F(9,8)*p4[n]
        p[n+1]=guard_rational(coeff/(n+1))
    p2=conv(p,p); p4=conv(p2,p2)
    residual=[F(0)]*max(len(p4),len(p2)+1,degree,3)
    residual[2]+=2
    for j,c in enumerate(p2): residual[j+1]+=3*c
    for j,c in enumerate(p4): residual[j]+=F(9,8)*c
    for j in range(degree): residual[j]-=(j+1)*p[j+1]
    assert all(c>=0 for c in residual)
    assert all(c==0 for c in residual[:degree])
    s0=F(1,2); bound=F(1,4)
    # f_e=6se+(9/2)e^3 <= 105/128 on this rectangle.
    lipschitz=6*s0*bound+F(9,2)*bound**3
    assert lipschitz==F(105,128) and s0*lipschitz<1
    residual_max=peval(residual,s0)
    delta=guard_rational(residual_max/(1-s0*lipschitz))
    e_lo=peval(p,s0); e_hi=guard_rational(e_lo+delta*s0)
    assert e_hi<bound
    # Fixed inverse start a >= e(s0); e'(s)>=2s0^2 for s>=s0.
    a=F(ceilq(e_hi),Q)
    s_hi=s0+(a-e_lo)/(2*s0*s0)
    init=IV.bounds(s0,s_hi)
    return a,init,{
        'polynomial_degree':degree,'s0':str(s0),'forward_e_lower':str(e_lo),
        'forward_e_upper':str(e_hi),'residual_max':str(residual_max),
        'linear_barrier_delta':str(delta),'lipschitz':str(lipschitz),
        'inverse_e_start':str(a),'inverse_s_lower':str(F(init.lo,Q)),
        'inverse_s_upper':str(F(init.hi,Q)),
        'startup_time_width':str(F(init.hi-init.lo,Q)),
        'residual_coefficients_nonnegative':True,
        'matched_coefficients_zero':True,
    }

def inverse_jets(e,s,order):
    """Taylor coefficients for s(e+h), interval initial (e,s) allowed."""
    cs=[s]; ws=[]; qs=[]
    e2=[e*e,2*e,IV.exact(1)]
    for j in range(order):
        wj=cs[j]+(F(3,4)*e2[j] if j<3 else 0)
        ws.append(wj)
        if j==0: qs.append(wj.reciprocal())
        else:
            total=IV.exact(0)
            for k in range(1,j+1): total=total+ws[k]*qs[j-k]
            qs.append(-qs[0]*total)
        total=IV.exact(0)
        for k in range(j+1): total=total+qs[k]*qs[j-k]
        cs.append(total/F(2*(j+1)))
    return cs

def step(a,h,prior,order):
    mid=(prior.lo+prior.hi)//2
    radius=max(mid-prior.lo,prior.hi-mid)
    center=IV(mid,mid)
    aa=IV.exact(a); hh=IV.exact(h)
    coeff=inverse_jets(aa,center,order)
    poly=coeff[-1]
    for c in reversed(coeff[:-1]): poly=poly*hh+c
    f0=coeff[1]
    # Center trajectory increases, while f decreases in e and s.
    tube=IV(mid,(center+hh*f0).hi)
    remainder_coeff=inverse_jets(IV.bounds(a,a+h),tube,order+1)[order+1]
    local=poly+remainder_coeff*(hh**(order+1))
    out=IV(local.lo-radius,local.hi+radius)
    assert out.lo>0
    return out,local.hi-local.lo

def dec_down(q,digits=18):
    q=F(q); scale=10**digits
    n=q.numerator*scale//q.denominator
    return f'{n//scale}.{n%scale:0{digits}d}'
def dec_up(q,digits=18):
    q=F(q); scale=10**digits
    n=ceildiv(q.numerator*scale,q.denominator)
    return f'{n//scale}.{n%scale:0{digits}d}'

def solve(order=6,grid_power=6,E=16,degree=28):
    start=time.monotonic_ns()
    for key in OPS: OPS[key]=0
    a,enc,init=startup(degree)
    initial_width=F(enc.hi-enc.lo,Q)
    steps=0; quadrature_ticks=0; checkpoints=[]
    # 2^-grid_power until e>=1; then fixed number per dyadic annulus.
    while a<E:
        if steps>=512: raise RuntimeError('fixed step ceiling exceeded')
        scale=1
        while 2*scale<=a: scale*=2
        h=min(F(scale,1<<grid_power),F(E)-a)
        enc,w=step(a,h,enc,order)
        quadrature_ticks+=w
        a+=h; steps+=1
        if steps%64==0 or a==E:
            checkpoints.append({'step':steps,'e':str(a),'s_lower':str(F(enc.lo,Q)),
                's_upper':str(F(enc.hi,Q)),'width':str(F(enc.hi-enc.lo,Q))})
    lo,hi=F(enc.lo,Q),F(enc.hi,Q)
    assert 0<lo<=hi<2
    E=F(E)
    tail0=F(8,27)/E**3
    # Baseline tail lower from s<=2; valid even if lower expression negative.
    baseline_lower=max(F(0),tail0-F(128,135)/E**5)
    # Refined: lo <= s(e) <= hi+tail0 throughout e>=E.
    U=hi+tail0
    refined_lower=tail0-F(64,135)*U/E**5
    refined_upper=tail0-F(64,135)*lo/E**5+F(128,189)*lo**2/E**7
    assert 0<refined_lower<=refined_upper<=tail0
    lower=lo+refined_lower; upper=hi+refined_upper
    certificate={
        'status':'RIGOROUS_RATIONAL_ENCLOSURE_AUTHOR_PENDING_INDEPENDENT_REVIEW',
        'equation':"e'=2(s+3e^2/4)^2, e(0)=0",
        'bits':BITS,'taylor_order':order,'grid_power':grid_power,'terminal_e':str(E),
        'steps':steps,'startup':init,'s_at_E_lower':str(lo),'s_at_E_upper':str(hi),
        'startup_width':str(initial_width),
        'inverse_taylor_and_rounding_width':str(hi-lo-initial_width),
        'sum_local_interval_widths':str(F(quadrature_ticks,Q)),
        'tail_basic_upper':str(tail0),'tail_baseline_lower_using_s_le_2':str(baseline_lower),
        'tail_refined_lower':str(refined_lower),'tail_refined_upper':str(refined_upper),
        'tail_width':str(refined_upper-refined_lower),
        's_star_lower':str(lower),'s_star_upper':str(upper),
        's_star_decimal_outward':[dec_down(lower),dec_up(upper)],
        'total_width':str(upper-lower),'total_width_decimal_upper':dec_up(upper-lower,24),
        'checkpoints':checkpoints,'integer_interval_operations':OPS.copy(),
        'wall_nanoseconds_nonproof':time.monotonic_ns()-start,
    }
    return certificate

def selftest():
    samples=[F(-7,3),F(-1,7),F(0),F(1,11),F(3,2),F(123456789,100)]
    def contains(iv,x): assert F(iv.lo,Q)<=x<=F(iv.hi,Q)
    for a in samples:
        for b in samples:
            aa,bb=IV.exact(a),IV.exact(b)
            contains(aa+bb,a+b); contains(aa*bb,a*b)
            if b: contains(aa/bb,a/b)
    # Known local Taylor derivatives: s'=1/(2w^2), s''=-v/w^3.
    a=F(2,3); s=F(5,4); w=s+F(3,4)*a*a; v=1/(2*w*w)+F(3,2)*a
    jets=inverse_jets(IV.exact(a),IV.exact(s),3)
    contains(jets[1],1/(2*w*w)); contains(jets[2],-v/(2*w**3))
    contains(jets[3],(3*v*v/w**4+v/w**6-F(3,2)/w**3)/6)
    return True


FIXED_PARAMETERS={'bits':80,'degree':28,'order':6,'grid_power':6,'terminal_e':16}
def rational_fields(result):
    # Exclude only environmental observation; all mathematical fields must match.
    return {k:v for k,v in result.items() if k!='wall_nanoseconds_nonproof'}

def main():
    assert selftest()
    first=solve()
    # A complete second exact pass is part of the proposed cold algorithm,
    # not an uncharged retained lookup or a fourth old fine acquisition.
    second=solve()
    assert rational_fields(first)==rational_fields(second)
    lo,hi=F(first['s_star_lower']),F(first['s_star_upper'])
    assert hi-lo<F(1,100000)
    assert 0<lo<hi<2
    for v in (lo,hi,hi-lo): guard_rational(v)
    first['status']='COARSE_COLD_SCALAR_AUTHOR_PENDING_INDEPENDENT_REVIEW'
    first['second_exact_pass_matched']=True
    first['fixed_parameters']=FIXED_PARAMETERS
    first['maximum_guarded_rational_bits']=MAX_RATIONAL_BITS
    first['startup_pair_visits_both_passes']=STARTUP_PAIR_VISITS
    first['algorithm_source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    here=Path(__file__).resolve().parent
    (here/'COARSE_CERTIFICATE.json').write_text(json.dumps(first,indent=2)+'\n')
    print(json.dumps({k:first[k] for k in ['status','fixed_parameters','s_star_decimal_outward','total_width_decimal_upper','steps','integer_interval_operations','second_exact_pass_matched','maximum_guarded_rational_bits','startup_pair_visits_both_passes']},indent=2))

if __name__=='__main__':
    main()
