"""Exact rational setup for a globally correlated canonical boson receiver.

Reuses the FROZEN zero-hopping M64 canonical interval; no new diagonal DP.
All displayed decimals are diagnostic conversions of saved Fraction bounds.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math,time,sys
sys.set_int_max_str_digits(0)

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'canonical_overlap/CONDITIONAL_EXECUTION.json'

def rec(x):return {'numerator':str(x.numerator),'denominator':str(x.denominator)}
def read(x):return F(int(x['numerator']),int(x['denominator']))
def ceil(x):return -(-x.numerator//x.denominator)
def down(x,b=128):
    y=x*(1<<b);return F(y.numerator//y.denominator,1<<b)
def up(x,b=128):return F(ceil(x*(1<<b)),1<<b)

def exp_bounds(x,n=90):
    assert x>=0
    term=F(1);s=term
    for k in range(1,n+1):term*=x/k;s+=term
    nxt=term*x/(n+1)
    assert x<F(n+2)
    return s,s+nxt/(1-x/F(n+2))

def onsite(r,qlo,qhi,D=6):
    al=1+2*sum((r**d*qlo**(d*d) for d in range(1,D+1)),F(0))
    au=1+2*sum((r**d*qhi**(d*d) for d in range(1,D+1)),F(0))
    bl=2*sum((d*r**d*qlo**(d*d) for d in range(1,D+1)),F(0))
    bu=2*sum((d*r**d*qhi**(d*d) for d in range(1,D+1)),F(0))
    x=r**(D+1)*qhi**((D+1)**2);a=r*qhi**(2*D+3)
    au+=2*x/(1-a)
    bu+=2*x*((D+1)/(1-a)+a/(1-a)**2)
    m0=r*r/(1-r*r)
    return al,au,m0+bl/(2*au),m0+bu/(2*al)

def radius(qlo,qhi,bits=48):
    den=1<<bits;lo=7*den//10;hi=71*den//100+1
    assert onsite(F(lo,den),qlo,qhi)[3]<1
    assert onsite(F(hi,den),qlo,qhi)[2]>1
    while hi-lo>1:
        mid=(lo+hi)//2;r=F(mid,den);a,b,ml,mh=onsite(r,qlo,qhi)
        if mh<1:lo=mid
        elif ml>1:hi=mid
        else:raise ArithmeticError('Increase onsite precision; no exact-root oracle.')
    return F(lo,den),F(hi,den),(F(lo,den)+F(hi,den))/2

def conv(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def grand_zero(M,r,qlo,qhi,D=4,bits=120):
    den=1<<bits
    lower=[];upper=[]
    for d in range(-D,D+1):
        x=r**abs(d)*qlo**(d*d)*den
        y=r**abs(d)*qhi**(d*d)*den
        lower.append(x.numerator//x.denominator);upper.append(ceil(y))
    lp=up=[1]
    for _ in range(M):lp=conv(lp,lower);up=conv(up,upper)
    scale=F(1,den**M);cl=lp[D*M]*scale;cu=up[D*M]*scale
    _,afull,_,_=onsite(r,qlo,qhi,D)
    apoly=sum((r**abs(d)*qhi**(d*d) for d in range(-D,D+1)),F(0))
    tail=afull-apoly
    cu+=M*tail*afull**(M-1)
    factor=(1-r*r)**(-M)
    return cl*factor,cu*factor,{'fourier_cut':D,'coefficient_bits':bits,
        'max_integer_bits':max(max(x.bit_length() for x in lp),max(x.bit_length() for x in up)),
        'scope':'Positive integer Laurent convolution plus exact omitted-Fourier l1 bound, not a source occupation cutoff.'}

def main():
    start=time.perf_counter();M=K=64;L=16;J=F(1,4)
    el,eh=exp_bounds(F(4));qlo,qhi=down(1/eh,160),up(1/el,160)
    rl,rh,r=radius(qlo,qhi)
    assert F(7,10)<r<F(71,100)
    al,ah,ml,mh=onsite(r,qlo,qhi)
    c0l,c0h,meta=grand_zero(M,r,qlo,qhi)
    c0l,c0h=down(c0l),up(c0h)
    old=json.loads(OLD.read_text());assert old['M']==M and old['K_each_flavor']==K and old['beta_U']==4
    z0l,z0h=read(old['partition_lower']),read(old['partition_upper'])
    p0l,p0h=down(r**(2*K)*z0l/c0h),up(r**(2*K)*z0h/c0l)
    _,env=exp_bounds(2*r*J/(1-r));env=up(env)
    le,ue=exp_bounds(2*F(K,M)*J);lower_shift=down(1/ue)
    acceptance=down(lower_shift*p0l/env)
    Q=ceil(F(20,3)*(F(17*M,4)+42))
    assert F(3*Q,20)>=F(17*M,4)+42
    w=list(range(M+1,2*M+1));s=sum(x*x for x in w)
    out={'M':M,'K_each_flavor':K,'beta':1,'U':4,'slices':L,
      'J':rec(J),'rank':1,'T_definition':'T=J*w*w^T/sum(w^2); positive rank-one, all positive triangle products, nonuniform distinct w.',
      'w':w,'w_squared_norm':s,'r':rec(r),'r_root_lower':rec(rl),'r_root_upper':rec(rh),
      'mean_density_lower':rec(down(ml)),'mean_density_upper':rec(up(mh)),
      'saddle_density_total_error_upper':rec(up(M*max(abs(ml-1),abs(mh-1)))),
      'q_lower':rec(qlo),'q_upper':rec(qhi),'A0_lower':rec(down(al)),'A0_upper':rec(up(ah)),
      'grand_balanced_zero_lower':rec(c0l),'grand_balanced_zero_upper':rec(c0h),
      'grand_relative_width':rec((c0h-c0l)/c0l),'grand_acquisition':meta,
      'pK_zero_lower':rec(p0l),'pK_zero_upper':rec(p0h),
      'determinant_envelope_upper':rec(env),'canonical_partition_ratio_lower':rec(lower_shift),
      'final_acceptance_lower':rec(acceptance),'expected_final_proposals_upper':rec(1/acceptance),
      'G0_trapezoid_points':Q,'G0_ideal_absolute_error_upper':rec(F(1,2**40)),
      'frozen_diagonal_input':{'path':str(OLD.resolve()),'sha256':hashlib.sha256(OLD.read_bytes()).hexdigest(),
           'scope':'Reused existing canonical interval, no DP rerun.'},
      'seconds':time.perf_counter()-start,
      'scope':'Exact rational setup/bounds; no Gaussian RNG or hopping trajectory in this compiler.'}
    (HERE/'INPUT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'seconds':out['seconds'],'r':float(r),'density_error':float(read(out['saddle_density_total_error_upper'])),
      'grand_relative_width':float((c0h-c0l)/c0l),'pK0':[float(p0l),float(p0h)],'envelope':float(env),
      'acceptance_lower':float(acceptance),'expected_proposals_upper':float(1/acceptance),'G0_points':Q},indent=2))

if __name__=='__main__':main()
