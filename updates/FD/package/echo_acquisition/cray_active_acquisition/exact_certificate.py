"""Exact rational/symbolic checks for declared CRAY fixtures.

This does not certify physical calibration or turn simulated data into an
experiment. It proves the algebra and a conditional confidence/sign calculation.
"""
from __future__ import annotations
from fractions import Fraction as F
import json, math
from pathlib import Path
import sympy as s
OUT=Path(__file__).resolve().parent
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
PS=[I,X,Y,Z]
def p(n,entries):
    out=s.ones(1,1)
    for j in range(n):out=s.kronecker_product(out,PS[entries.get(j,0)])
    return out

def exact_pair():
    terms=[(70,{0:3}),(43,{1:1}),(31,{1:3}),
           (83,{0:1,1:1}),(61,{0:2,1:2}),(97,{0:3,1:3}),
           (79,{1:1,2:1}),(57,{1:2,2:2}),(88,{1:3,2:3})]
    h0=s.zeros(8)
    for c,a in terms:h0+=s.Rational(c,100)*p(3,a)
    P=p(3,{0:3,1:1});u=(s.eye(8)+s.I*P)/s.sqrt(2)
    w=s.Rational(1,5);delta=s.Rational(3,100)
    h1=u*h0*u.conjugate().T+w*s.eye(8)+delta*p(3,{0:3,2:3})
    r=s.simplify(u.conjugate().T*h1*u-h0-w*s.eye(8))
    assert s.simplify(u.conjugate().T*u)==s.eye(8)
    assert r==delta*p(3,{0:3,2:3})
    assert r*r==delta**2*s.eye(8)
    return dict(w=str(w),residual_norm=str(delta),interval=['17/100','23/100'],
                arbitrary_host_condition='Additional common terms commute with U; no state or equilibrium assumption.')

def exp_lower(x:F,n:int=100)->F:
    assert x>=0
    term=F(1);res=term
    for k in range(1,n+1):term*=x/k;res+=term
    return res

def exact_data():
    observed=json.loads((OUT/'echo_results.json').read_text())['null_simulation']
    N=observed['N'];k=observed['failures']
    assert N==100_000_000 and k==3
    q=F(101,10**9);x=N*q
    # Binomial(n,q) lower tail <= exp(-nq) sum_{j=0}^k
    # [nq/(1-q)]^j/j!. Verify a strict 1% upper bound rationally.
    a=x/(1-q)
    poly=sum(a**j/F(math.factorial(j)) for j in range(k+1))
    exp_lo=exp_lower(x)
    tail_upper=poly/exp_lo
    assert tail_upper<F(1,100)
    gamma=F(1,10**8);Lambda=F(879,50);d=8;t=F(1,50)
    invsqrt_lower=F(35355,100000)
    assert invsqrt_lower**2*d<=1
    coefficient=t*t*(invsqrt_lower-Lambda*t/2)**2/4
    assert invsqrt_lower>Lambda*t/2
    radius_square=(q+gamma)/coefficient
    radius_upper=F(188,1000)
    assert radius_square<radius_upper**2
    w=F(1,5)
    return dict(provenance='Seeded synthetic acquisition counts; not laboratory data.',
                N=N,failures=k,alpha='1/100',q_upper=str(q),
                rational_binomial_tail_upper=str(tail_upper),
                rational_binomial_tail_upper_float=float(tail_upper),
                apparatus_probability_error_bound=str(gamma),Lambda=str(Lambda),
                local_dimension=d,t=str(t),norm_radius_upper=str(radius_upper),
                deltaF_interval=[str(w-radius_upper),str(w+radius_upper)],
                valid_for='Every beta>0 and ground energies, conditional on the local-support, control, time, norm and calibration contract.',
                no_IID_claim='Coverage follows from a conditional failure-probability lower bound and binomial domination, not iid specimens.')

def exact_hidden_signs():
    # For beta=2, partition differences are Laurent polynomials in x=exp(1).
    # enclosures x in [2718/1000,2719/1000] suffice for both signs.
    x=s.symbols('x', positive=True)
    out=[]
    # Return exact polynomial and an elementary interval-arithmetic sign proof.
    lo=F(2718,1000);hi=F(2719,1000)
    exp_lo=exp_lower(F(1),20)
    term=F(1,math.factorial(21));tail=term/(1-F(1,22))
    assert exp_lo>lo and exp_lo+tail<hi
    for b in [-4,4]:
        coeff={}
        for n in [0,1]:
            for z in [0,1]:
                h=n*(1-2*z)+b*z
                for power,c in [(-2*h-1+2*n,1),(-2*h,-1)]:coeff[power]=coeff.get(power,0)+c
        minpower=min(coeff);shift=-min(0,minpower)
        low=F(0);high=F(0)
        for power,c in coeff.items():
            pp=power+shift
            if c>=0:low+=c*lo**pp;high+=c*hi**pp
            else:low+=c*hi**pp;high+=c*lo**pp
        if b<0:assert low>0;sign='DeltaF<0'
        else:assert high<0;sign='DeltaF>0'
        out.append(dict(b=b,sign=sign,shifted_partition_difference_coefficients={str(k+shift):v for k,v in coeff.items()},
                        polynomial_lower=str(low),polynomial_upper=str(high)))
    return out
if __name__=='__main__':
    result=dict(pairing=exact_pair(),conditional_acquisition=exact_data(),hidden_sector=exact_hidden_signs())
    (OUT/'exact_certificate.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='conditional_acquisition'},indent=2))
    print('Conditional interval:',result['conditional_acquisition']['deltaF_interval'])
    print('Tail bound:',result['conditional_acquisition']['rational_binomial_tail_upper_float'])
