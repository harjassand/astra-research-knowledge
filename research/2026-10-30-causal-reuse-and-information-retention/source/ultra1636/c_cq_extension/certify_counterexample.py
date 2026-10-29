"""Finite scalar-reference CQ counterexample, rational intervals only.

No eigensolver, random Q/u screen, SDP or unsupported metric substitution.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time,resource
ROOT=Path(__file__).resolve().parent


class I:
    def __init__(self,a,b=None):self.a=F(a);self.b=F(a if b is None else b);assert self.a<=self.b
    def __add__(self,o):
        o=o if isinstance(o,I) else I(o);return I(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self):return I(-self.b,-self.a)
    def __sub__(self,o):return self+-asI(o)
    def __rsub__(self,o):return asI(o)+-self
    def __mul__(self,o):
        o=asI(o);v=[x*y for x in (self.a,self.b) for y in (o.a,o.b)];return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=asI(o);assert o.a>0;return self*I(1/o.b,1/o.a)
    def __rtruediv__(self,o):return asI(o)/self
    def record(self):
        # Compact OUTWARD exact dyadics, rather than huge exact series fractions.
        den=1<<160;lo=F((self.a*den).__floor__(),den);hi=F((self.b*den).__ceil__(),den)
        assert lo<=self.a<=self.b<=hi
        return {'lower':str(lo),'upper':str(hi),'diagnostic':[float(lo),float(hi)]}


def asI(o):return o if isinstance(o,I) else I(o)


def log_small(x,N=100):
    assert 1<=x<=2;z=(x-1)/(x+1);s=F(0);power=z
    for k in range(N):s+=2*power/(2*k+1);power*=z*z
    err=2*power/((2*N+1)*(1-z*z))
    return I(s,s+err)


LOG2=log_small(F(2))


def log_rational(x):
    assert x>0;k=0
    while x<1:x*=2;k-=1
    while x>2:x/=2;k+=1
    return log_small(x)+k*LOG2


def log_interval(x):
    x=asI(x);assert x.a>0
    a,b=log_rational(x.a),log_rational(x.b)
    return I(a.a,b.b)


def sqrt_rational(x):
    assert x>=0;lo=F(0);hi=max(F(1),x)
    for _ in range(220):
        mid=(lo+hi)/2
        if mid*mid<x:lo=mid
        else:hi=mid
    assert lo*lo<=x<=hi*hi
    return I(lo,hi)


def binary_D(p,q):
    return p*log_rational(p/q)+(1-p)*log_rational((1-p)/(1-q))


def qubit_D(r,p,q):
    """tau_p=(I+r[(1-p)X+pZ])/2; tau_q likewise."""
    rp2=r*r*(p*p+(1-p)*(1-p));sq2=r*r*(q*q+(1-q)*(1-q))
    rp,sq=sqrt_rational(rp2),sqrt_rational(sq2)
    lp=(1+rp)/2;lm=(1-rp)/2
    entropy_term=lp*log_interval(lp)+lm*log_interval(lm)
    dot=r*r*(p*q+(1-p)*(1-q))
    cross=log_rational((1-sq2)/4)/2+(dot/(2*sq))*log_interval((1+sq)/(1-sq))
    return entropy_term-cross


def main():
    start=time.perf_counter();p,q=F(3,4),F(1,2)
    pure_input=binary_D(p,q);pure_output=qubit_D(F(1),p,q)
    assert pure_output.a>0 and pure_input.a>pure_output.b
    r=F(4,5);signal=F(2,3);effective2=r*r/(2-r*r)
    assert effective2==F(8,17)
    free_coefficient=signal**2/effective2
    assert free_coefficient==F(17,18) and signal**2<effective2
    # For x=z^2 in[0,1], derivative of (1-e*x)/(1-a^2*x)
    # has numerator a^2-e<0. Positive denominator proves max x=0.
    assert signal**2-effective2<0 and 1-effective2>0
    prepared_det=(1-r*r)/4
    assert prepared_det==F(9,100)
    # [tau0,tau1]=i*r^2*Y/2 is nonzero.
    assert r*r/2==F(8,25)
    target_p=(1-signal)/2+signal*p
    target_q=(1-signal)/2+signal*q
    target=binary_D(target_p,target_q);reference=qubit_D(r,p,q)
    assert target.a>reference.b>0
    result={'scope':'finite faithful scalar-reference hypotheses; exact universal inverse comparison is analytic binary functional calculus',
        'hypotheses':{'p':['3/4','1/4'],'q':['1/2','1/2'],'reference_dimension':1},
        'pure_pair':{'tau0':[['1','0'],['0','0']],'tau1':[['1/2','1/2'],['1/2','1/2']],
            'one_family_comparison_coefficient':'1','classical_identity_D':pure_input.record(),
            'CQ_D':pure_output.record(),'true_finite_ratio':(pure_input/pure_output).record(),
            'false_budget_one_margin':(pure_input-pure_output).record()},
        'faithful_continuation':{'r':str(r),'prepared_min_eigenvalue':'1/10','prepared_determinant':str(prepared_det),
            'tau0':[['9/10','0'],['0','1/10']],'tau1':[['1/2','2/5'],['2/5','1/2']],
            'target_K':[['5/6','1/6'],['1/6','5/6']],
            'one_family_exact_all_reference_coefficient':str(free_coefficient),
            'strict_false_admission_budget':'1','target_D':target.record(),'CQ_reference_D':reference.record(),
            'true_finite_ratio':(target/reference).record(),'false_budget_one_margin':(target-reference).record()},
        'arithmetic':{'sqrt_bisections':220,'log_atanh_terms':100,'all_comparisons_exact_rational':True,
            'numerical_eigenvalues_or_logs':False,'SDP_calls':0,'random_reference_queries':0},
        'seconds':time.perf_counter()-start,'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (ROOT/'COUNTEREXAMPLE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'ONE_FAMILY_REPRESENTATION_REFUTED',
        'pure_finite_ratio':result['pure_pair']['true_finite_ratio']['diagnostic'],
        'faithful_finite_ratio':result['faithful_continuation']['true_finite_ratio']['diagnostic'],
        'faithful_inverse_coefficient':str(free_coefficient),'seconds':result['seconds']},indent=2))


if __name__=='__main__':main()
