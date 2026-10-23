#!/usr/bin/env python3
"""Bounded exact/interval receiver-value stress test; no owner scientific job."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import hashlib
import json
import time

ROOT=Path(__file__).resolve().parent
SCALE=10**18
NLOG=32

def rounded_interval(lo,hi):
    assert lo<=hi
    lower=(lo.numerator*SCALE)//lo.denominator
    upper=-((-hi.numerator*SCALE)//hi.denominator)
    return F(lower,SCALE),F(upper,SCALE)

def rational_log(x):
    """Rational enclosure via range reduction and atanhlike positive series."""
    assert x>0
    k=0
    y=x
    while y<1:
        y*=2;k-=1
    while y>=2:
        y/=2;k+=1
    def log12(v):
        assert 1<=v<=2
        z=(v-1)/(v+1)
        total=F(0)
        power=z
        for j in range(NLOG):
            total+=2*power/(2*j+1)
            power*=z*z
        remainder=2*power/((2*NLOG+1)*(1-z*z))
        return total,total+remainder
    lo,hi=log12(y)
    l2,h2=log12(F(2))
    if k>=0:lo+=k*l2;hi+=k*h2
    else:lo+=k*h2;hi+=k*l2
    return rounded_interval(lo,hi)

def sqrt3_interval():
    a=isqrt(3*SCALE*SCALE)
    assert a*a<3*SCALE*SCALE<(a+1)*(a+1)
    return F(a,SCALE),F(a+1,SCALE)

def entropy(intervals):
    lo=F(0);hi=F(0)
    for a,b in intervals:
        assert 0<a<=b<1
        loga=rational_log(a)[0]
        logb=rational_log(b)[1]
        # x and -log(x) are nonnegative on these intervals. Dependency is
        # discarded conservatively, so no monotonicity of -x log x is assumed.
        lo+=a*(-logb)
        hi+=b*(-loga)
    return rounded_interval(lo,hi)

def exact_list(xs):return [(x,x) for x in xs]

def show(iv):
    return {'lo':str(iv[0]),'hi':str(iv[1]),
            'decimal_lo':float(iv[0]),'decimal_hi':float(iv[1])}

def qop(a,b):
    """Product in Q(sqrt3), represented by rational coefficients."""
    return (a[0]*b[0]+3*a[1]*b[1],a[0]*b[1]+a[1]*b[0])

def main():
    start=time.perf_counter()
    D,L,r=4,2048,2
    lam=F(1,20)
    pA=[F(1,2),F(1,6),F(1,6),F(1,6)]
    qA=[F(1,10),F(3,10),F(3,10),F(3,10)]
    pB_alg=[(F(1,4),F(0)),(F(1,4),F(0)),
            (F(1,4),F(1,12)),(F(1,4),F(-1,12))]
    qB_alg=[(F(1,5),F(0)),(F(1,5),F(0)),
            (F(3,10),F(-1,10)),(F(3,10),F(1,10))]
    assert sum(pA)==sum(qA)==1
    assert all(p*q==lam for p,q in zip(pA,qA))
    for family in [pB_alg,qB_alg]:
        assert sum(x[0] for x in family)==1
        assert sum(x[1] for x in family)==0
    assert all(qop(p,q)==(lam,F(0)) for p,q in zip(pB_alg,qB_alg))
    s0,s1=sqrt3_interval()
    def enclose(a):
        return (a[0]+a[1]*s0,a[0]+a[1]*s1) if a[1]>=0 else (a[0]+a[1]*s1,a[0]+a[1]*s0)
    pB=[enclose(a) for a in pB_alg]
    qB=[enclose(a) for a in qB_alg]
    HP_A,HQ_A=entropy(exact_list(pA)),entropy(exact_list(qA))
    HP_B,HQ_B=entropy(pB),entropy(qB)
    # These exact interval comparisons identify the better orientation.
    assert HP_A[1]<HQ_A[0]
    assert HQ_B[1]<HP_B[0]
    hA,hB=HP_A,HQ_B
    assert hA[1]<hB[0]
    b=F(L-1,2)
    logL=rational_log(F(L))
    QA=(b*hA[0]*(r-1),(b*hA[1]+logL[1])*(r-1))
    QB=(b*hB[0]*(r-1),(b*hB[1]+logL[1])*(r-1))
    gap=QB[0]-QA[1]
    assert gap>10
    delta=(1-lam**L)/L
    delta_string=str(delta)
    m=rational_log(F(D))
    B=(F(L+1,2)*m[0],F(L+1,2)*m[1])
    # Common prefix probabilities use only lambda and uniform inventory.
    for i in [1,2,3,16,L,L+1]:
        p=(F(max(L-i+1,0))+sum(lam**(i-k) for k in range(1,min(L,i-1)+1)))/L
        assert 0<p<=1
        if i==1:assert p==1
    result={
      'status':'PASS','D':D,'L':L,'N':L,'r':r,'lambda':str(lam),
      'exact_algebra':'Both normalized positive product tails satisfy p_i q_i=1/20 in Q(sqrt3).',
      'entropy_nats':{'pA':show(HP_A),'qA':show(HQ_A),'pB':show(HP_B),'qB':show(HQ_B)},
      'best_orientation_entropy':{'A':show(hA),'B':show(hB)},
      'Qbar_optimized_over_all_collective_readouts_and_best_global_orientation':
          {'A':show(QA),'B':show(QB),'strict_B_minus_A_lower':str(gap),'strict_B_minus_A_lower_decimal':float(gap)},
      'shared_return_delta_formula':'(1-20^(-2048))/2048',
      'shared_return_delta_rational_sha256':hashlib.sha256(delta_string.encode()).hexdigest(),
      'shared_expected_exact_supply_per_copy_nats':show(B),
      'shared_entire_formation_resource_error_frontier':'Proved by explicit free local controlled tail replacement in each direction; see PROOF.txt. No numeric E_F optimization.',
      'same': ['D,L,N,r','fixed local shift/decrement circuit','uniform counted stock and cyclic clock','exact first Bell output','all complete-prefix Bell probabilities','complete one-use return delta','complete formation resource/error frontier'],
      'different':['faithful free input eta','tail-state distributions','general output-memory process','unknown thermodynamic preparation/control costs'],
      'not_claimed':['equal full external processes','new physical capability','a solution to the generic formation gap','superiority over ordinary optimal resource evaluation','general discovery or recursive amplification advantage'],
      'selection':'Explicitly selected after rough floating-point screening; exact interval verification is the executed result.',
      'algorithm':'Rational Q(sqrt3) identities; isqrt enclosure; 32-term atanh log series with proved positive remainder and rational outward rounding.',
    }
    (ROOT/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'COST.json').write_text(json.dumps({'wall_seconds':time.perf_counter()-start,'scope':'This bounded algebra/interval verification only; full design, reading, review and model inference cost UNKNOWN; no owner trajectory or model call.'},indent=2)+'\n')
    print(json.dumps({'status':'PASS','Q_A':show(QA),'Q_B':show(QB),'gap_lower':float(gap),'wall_seconds':time.perf_counter()-start}))

if __name__=='__main__':main()
