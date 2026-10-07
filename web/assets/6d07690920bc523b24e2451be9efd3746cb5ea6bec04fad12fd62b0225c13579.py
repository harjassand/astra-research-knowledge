"""Exact rational interval certificates for the finite N=4..7 prefix.

No floating-point operation or SDP is used to decide any sign. Taylor's
integral remainder puts exp(-x) between the odd and even truncations for x>=0.
Positive interval LDL pivots then prove positive definite Hankel matrices.
"""
from fractions import Fraction as F
from math import factorial,comb
from pathlib import Path
import json

class Interval:
    def __init__(self,lo,hi=None):
        self.lo=F(lo); self.hi=F(lo if hi is None else hi)
        assert self.lo<=self.hi
    def __add__(self,o):
        return Interval(self.lo+o.lo,self.hi+o.hi)
    def __sub__(self,o):
        return Interval(self.lo-o.hi,self.hi-o.lo)
    def __mul__(self,o):
        p=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi]
        return Interval(min(p),max(p))
    def __truediv__(self,o):
        assert not o.lo<=0<=o.hi
        p=[self.lo/o.lo,self.lo/o.hi,self.hi/o.lo,self.hi/o.hi]
        return Interval(min(p),max(p))
    def square(self):
        upper=max(self.lo**2,self.hi**2)
        lower=0 if self.lo<=0<=self.hi else min(self.lo**2,self.hi**2)
        return Interval(lower,upper)

def exp_negative(x,even_degree=12):
    # Taylor integral remainder has sign (-1)^(degree+1).
    upper=sum((-x)**j/F(factorial(j)) for j in range(even_degree+1))
    lower=upper+(-x)**(even_degree+1)/F(factorial(even_degree+1))
    assert lower>0
    return Interval(lower,upper)

def certify_ldl(H):
    n=len(H); L=[[Interval(0) for _ in range(n)] for _ in range(n)];D=[]
    for i in range(n):
        p=H[i][i]
        for k in range(i):p=p-L[i][k].square()*D[k]
        assert p.lo>0,(i,p.lo,p.hi)
        D.append(p);L[i][i]=Interval(1)
        for j in range(i+1,n):
            u=H[j][i]
            for k in range(i):u=u-L[j][k]*L[i][k]*D[k]
            L[j][i]=u/p
    return D

def fraction_string(z):return f'{z.numerator}/{z.denominator}'

rows=[]
for N in range(4,8):
    q=[]
    for k in range(N+1):
        x=F(3*(2*k-N)**2,16*N)
        q.append(exp_negative(x)/Interval(comb(N,k)))
    for offset in (0,1):
        dimension=(N-offset)//2+1
        H=[[q[i+j+offset] for j in range(dimension)] for i in range(dimension)]
        pivots=certify_ldl(H)
        rows.append({'N':N,'offset':offset,'dimension':dimension,
                     'positive_pivot_intervals':[{'lower_exact':fraction_string(p.lo),
                                                  'upper_exact':fraction_string(p.hi),
                                                  'lower_diagnostic_decimal':float(p.lo)} for p in pivots]})

checks={}
def test(name,val):
    assert val,name
    checks[name]=True
test('phase_sqrt_bound',F(3,5)**2<F(3,8))
phase=F(1024,9375)*F(27,64)*F(25,128)/(F(3,8)**3*F(3,5))
test('phase_bound',phase==F(64,225)<F(2,7))
test('vertical_exponent',F(4,3)-F(75,256)-F(5,6)==F(53,256))
test('sqrt2_lt10_over7',2<F(10,7)**2)
test('vertical_exp_bound',sum(F(53,32)**j/factorial(j) for j in range(5))>F(100,21))
test('vertical_ratio',F(25,14)/F(100,21)==F(3,8))
test('density_margin',1-F(2,7)-F(1,1000)-F(3,8)==F(296,875)>F(1,3))
test('correction_exponent',-F(32,3)+F(75,32)==-F(799,96)<-8)
test('exp4_lower48',sum(F(4**j,factorial(j)) for j in range(7))>48)
test('correction_ratio_coarse',F(768,48**2)<F(1,2))
test('correction_real_N_derivative',1-F(55,48)<0)
out={'status':'EXACT_RATIONAL_INTERVAL_PREFIX_AND_ANALYTIC_CONSTANTS_PASS',
     'delta_exact':'3/4','Taylor_upper_degree_even':12,'Taylor_lower_degree_odd':13,
     'Hankel_convention':'q_k=exp[-(3/4)(k-N/2)^2/N]/binom(N,k)',
     'prefix_N':[4,5,6,7],'rows':rows,'analytic_tail_constants':checks,
     'scope':'Positive exact interval LDL pivots certify the entire finite prefix. General analytic inequalities in proof10 certify every N>=8.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'prefix_N':out['prefix_N'],
                  'minimum_pivot_lower_diagnostic':min(p['lower_diagnostic_decimal'] for r in rows for p in r['positive_pivot_intervals']),
                  'analytic_tail_constants':checks},indent=2))
