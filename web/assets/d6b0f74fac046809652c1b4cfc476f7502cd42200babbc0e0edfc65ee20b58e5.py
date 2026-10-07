"""Rational interval/random-bit quartic sampler and product-qubit description.

Standard library only. The certified primitive uses exact Fraction arithmetic.
It emits a classical positive rational Bloch vector, not a hardware state.
Distributional guarantees assume the bits() interface supplies iid fair bits.
The test replay uses a seeded bit source and is labelled as such.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations
import argparse
import datetime
import json
import math
from pathlib import Path
import random
import secrets
import time

def ceilq(x):
    return -((-x.numerator)//x.denominator)

def ceilbits(target):
    assert target > 0
    q = max(0, target.denominator.bit_length()-target.numerator.bit_length())
    while F(1,1<<q)>target:
        q+=1
    return q

def exp_interval(x, bits):
    """Enclose exp(rational x), width <=2^-bits; no real comparison."""
    x=F(x)
    if x==0:
        return F(1),F(1)
    if x<=-(bits+1):
        return F(0),F(1,1<<(bits+1))
    j=0
    t=x
    while abs(t)>F(1,2):
        t/=2
        j+=1
    guard=j+ceilq(2*max(x,F(0)))+(j+1).bit_length()+12
    threshold=F(1,1<<(bits+guard))
    term=F(1)
    total=term
    n=0
    while True:
        rem=2*abs(term*t/F(n+1))
        if 2*rem<=threshold:
            break
        n+=1
        term=term*t/F(n)
        total+=term
    lo=max(F(0),total-rem)
    hi=total+rem
    if x<0:
        hi=min(F(1),hi)
    # Outward dyadic rounding keeps every interval register polynomial-sized.
    # The guard covers base rounding and each squaring, including amplification.
    scale=1<<(bits+guard)
    def outward(low,high):
        return F((low*scale).numerator//(low*scale).denominator,scale),F(ceilq(high*scale),scale)
    lo,hi=outward(lo,hi)
    for _ in range(j):
        lo,hi=outward(lo*lo,hi*hi)
    assert 0<=lo<=hi and hi-lo<=F(1,1<<bits)
    return lo,hi

def root_interval(x,power,bits,upper):
    x=F(x)
    if x==0:
        return F(0),F(0)
    lo=F(0)
    hi=F(upper)
    assert hi**power>=x
    tol=F(1,1<<bits)
    while hi-lo>tol:
        mid=(hi+lo)/2
        if mid**power<=x:
            lo=mid
        else:
            hi=mid
    return lo,hi

def det(M):
    if len(M)==1:
        return M[0][0]
    return sum(((-1)**j)*M[0][j]*det([row[:j]+row[j+1:] for row in M[1:]]) for j in range(len(M)))

def verify_input(A,b,M,B):
    assert M>=0 and B>=0 and len(A)==3 and len(b)==3
    assert all(len(row)==3 for row in A)
    assert all(A[i][j]==A[j][i] for i in range(3) for j in range(3))
    for sign in [-1,1]:
        D=[[F(int(i==j))*M+sign*A[i][j] for j in range(3)] for i in range(3)]
        for k in [1,2,3]:
            for I in combinations(range(3),k):
                assert det([[D[i][j] for j in I] for i in I])>=0
    assert sum(z*z for z in b)<=B*B

def rational_bloch(x,N,eps):
    """Positive rational Bloch vector enclosing tau_N(x), with charged bias."""
    r2=sum(z*z for z in x)
    if r2==0:
        return [F(0)]*3, {'near_zero':True,'bloch_error_upper':'0'}
    local_tol=eps/(2048*N)
    p=ceilbits(local_tol)+32
    rupper=1+ceilq(max(F(1),r2))
    refinements=0
    while True:
        alo,ahi=root_interval(F(16,N),4,p,2)
        rlo,rhi=root_interval(r2,2,p,rupper)
        if rlo==0:
            p+=16
            continue
        zlo,zhi=alo*rlo,ahi*rhi
        elo,_=exp_interval(2*zlo,p)
        _,ehi=exp_interval(2*zhi,p)
        tlo=(elo-1)/(elo+1)
        thi=(ehi-1)/(ehi+1)
        scalar_lo=max(F(0),tlo)/rhi
        scalar_hi=thi/rlo
        boxes=[]
        for xi in x:
            vals=[xi*scalar_lo,xi*scalar_hi]
            boxes.append((min(vals),max(vals)))
        width=max(hi-lo for lo,hi in boxes)
        if width<=local_tol:
            break
        p+=16
        refinements+=1
    midpoint=[(lo+hi)/2 for lo,hi in boxes]
    # Euclidean midpoint error <=sqrt(3)*width/2 <=width.
    # Scaling by (1+2width) ensures exact positivity and adds <=2width.
    e=2*width
    answer=[z/(1+e) for z in midpoint]
    assert sum(z*z for z in answer)<=1
    # Euclidean error <=3width, trace distance <=3width/2.
    return answer, {'working_bits':p,'refinements':refinements,
                    'component_enclosures':[[str(lo),str(hi)] for lo,hi in boxes],
                    'bloch_error_upper':str(3*width),
                    'one_qubit_trace_error_upper':str(3*width/2),
                    'N_product_trace_error_upper':str(N*3*width/2)}

class BitSource:
    def __init__(self,seed=None):
        self.seed=seed
        self.rng=None if seed is None else random.Random(seed)
        self.used=0
    def bits(self,n):
        self.used+=n
        return secrets.randbits(n) if self.rng is None else self.rng.getrandbits(n)

def sample(A,b,M,B,N,eps,seed=None):
    A=[[F(z) for z in row] for row in A]
    b=[F(z) for z in b]
    M,B,eps=F(M),F(B),F(eps)
    assert isinstance(N,int) and N>=1 and 0<eps<F(1,4)
    verify_input(A,b,M,B)
    e=ceilbits(eps)
    eps0=F(1,1<<e)
    kg=ceilq(2*(3*(M+2)**2/16+B*B/4)+1)
    k0=ceilq(2*(3*(M+1)**2/16+B*B/4)+1)
    zbound=ceilq(2*(F(4,3)+M+B))
    need=kg+zbound+e+8
    L=math.isqrt(need)
    if L*L<need:
        L+=1
    L=max(1,L)
    Henv=1<<k0
    volume=(2*L)**3
    p0=F(1,(1<<zbound)*2*volume*Henv)
    K=ceilq(F(e+4)/p0)
    radius=2*L
    La=F(16,3)*radius**3+2*M*radius+B
    q=max(ceilbits(eps0/(1024*K*(2*L*La+4))),
          ceilbits(eps0/(1024*N*L)))
    dyadic=1<<q
    bits=BitSource(seed)
    attempts=0
    accepted=None
    exp_calls=0
    start=time.monotonic()
    for attempts in range(1,K+1):
        x=[F((2*bits.bits(q)+1)-dyadic,dyadic)*L for _ in range(3)]
        r2=sum(z*z for z in x)
        ell=-F(4,3)*r2*r2+sum(x[i]*A[i][j]*x[j] for i in range(3) for j in range(3))+sum(b[i]*x[i] for i in range(3))
        lo,hi=exp_interval(ell,q+4)
        exp_calls+=1
        lo/=Henv
        hi=min(F(1),hi/Henv)
        alpha=(lo+hi)/2
        threshold=(alpha*dyadic).numerator//(alpha*dyadic).denominator
        u=bits.bits(q)
        if u<threshold:
            accepted={'x':x,'ell':ell,'alpha_interval':[lo,hi],
                      'uniform_integer':u,'dyadic_threshold':threshold}
            break
    if accepted is None:
        bloch=[F(0)]*3
        quantum={'fallback':True,'one_qubit_trace_error_upper':'UNKNOWN'}
    else:
        bloch,quantum=rational_bloch(accepted['x'],N,eps0)
    def sdata(v):
        if isinstance(v,F):
            return str(v)
        if isinstance(v,list):
            return [sdata(z) for z in v]
        if isinstance(v,dict):
            return {k:sdata(z) for k,z in v.items()}
        return v
    return sdata({'scope':'Certified rational scalar enclosures and positive product-qubit description; no hardware emissions.',
        'random_bit_model':'OS random bits treated as iid fair interface' if seed is None else 'Seeded replay; not an iid sampling claim',
        'seed':seed,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'input':{'A':A,'b':b,'M':M,'B':B,'N':N,'epsilon':eps},
        'budget':{'epsilon_dyadic':eps0,'cube_halfwidth':L,'normal_envelope_log2':kg,
                  'cube_envelope':Henv,'Z_lower':F(1,1<<zbound),'acceptance_lower':p0,
                  'proposal_cap':K,'draw_precision_bits':q,'tail_upper':F(12*(1<<kg)*(1<<zbound),1<<(L*L)),
                  'acceptance_coupling_upper':K*(2*L*La+4)*F(1,dyadic),
                  'coordinate_product_error_upper':2*L*N*F(1,dyadic),
                  'native_emission_error_allocation':eps0/16},
        'run':{'attempts':attempts,'exhausted':accepted is None,'random_bits_used':bits.used,
               'exp_interval_calls':exp_calls,'wall_seconds':time.monotonic()-start},
        'accepted_proposal':accepted,'bloch_vector':bloch,'bloch_norm_squared':sum(z*z for z in bloch),
        'quantum_description_certificate':quantum,
        'theorem_boundary':'Output description approximates S_N p_(A,b); adding whole-state density-transport bound is an unaudited mathematical candidate.'})

def primitive_checks():
    import mpmath as mp
    mp.mp.dps=120
    cases=[]
    for x in [F(-120),F(-37,3),F(-1,7),F(0),F(1,7),F(4,3),F(10)]:
        lo,hi=exp_interval(x,70)
        v=mp.exp(mp.mpf(x.numerator)/x.denominator)
        assert mp.mpf(lo.numerator)/lo.denominator<=v<=mp.mpf(hi.numerator)/hi.denominator
        cases.append({'x':str(x),'interval_width':str(hi-lo)})
    return {'scope':'High-precision floating cross-check of exact rational interval primitive; containment proof is analytic.',
            'exp_cases':cases}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--seed',type=int)
    parser.add_argument('--N',type=int,default=256)
    parser.add_argument('--epsilon',default='1/16')
    parser.add_argument('--output',default='certified_quartic_sample.json')
    parser.add_argument('--cross-check',action='store_true',help='Optional mpmath floating cross-check; not required by sampler.')
    args=parser.parse_args()
    A=[['1/8','1/32','0'],['1/32','-1/8','1/64'],['0','1/64','1/16']]
    b=['1/8','1/16','-1/32']
    result=sample(A,b,'1/4','1/4',args.N,F(args.epsilon),args.seed)
    if args.cross_check:
        result['primitive_cross_checks']=primitive_checks()
    target=Path(__file__).with_name(args.output)
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'path':str(target),'run':result['run'],'budget':result['budget'],
                      'physical_quantum_emissions':0,'bloch_positive':F(result['bloch_norm_squared'])<=1},indent=2))
