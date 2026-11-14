"""Independent classical comparator, not execution/recovery of producer files.

Positive rational rates are introduced inputs. Exact transfer matrices give the
same birth-death clock by ordinary methods. Arithmetic counts are NOT bit-cost
or novelty claims. A competing-killing diagnostic is not a physical bulk model.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
import hashlib
import json


def multiply(a,b):
    return [[sum((x*y for x,y in zip(row,col)),F(0))
             for col in zip(*b)] for row in a]


def power(a,n):
    ans=[[F(int(i==j)) for j in range(len(a))] for i in range(len(a))]
    products=0
    while n:
        if n&1:ans=multiply(ans,a);products+=1
        n>>=1
        if n:a=multiply(a,a);products+=1
    return ans,products


A=F(1,80); B=F(79,80); LAMBDA=F(2,5); MU=F(3,5)


def recurrence_mean(m):
    d=1/A;t=d
    for n in range(1,m):
        d=(1+(B if n==1 else MU)*d)/LAMBDA
        t+=d
    return t


def matrix_mean(m):
    if m==1:return 1/A,0
    d1=(1+B/A)/LAMBDA
    rho=MU/LAMBDA;c=1/LAMBDA
    mat=[[rho,F(0),c],[rho,F(1),c],[F(0),F(0),F(1)]]
    p,count=power(mat,m-2)
    v=multiply(p,[[d1],[1/A+d1],[F(1)]])
    return v[1][0],count+1


def mean_closed_form(m):
    if m==1:return 1/A
    n=m-1;rho=MU/LAMBDA;d1=(1+B/A)/LAMBDA
    if rho==1:return 1/A+n*d1+F(n*(n-1),2)/LAMBDA
    series=(rho**n-1)/(rho-1)
    return 1/A+d1*series+(series-n)/(LAMBDA*(rho-1))


def transform_continued_fraction(m,s):
    g=A/(s+A);result=g
    for n in range(1,m):
        death=B if n==1 else MU
        g=LAMBDA/(s+LAMBDA+death-death*g)
        result*=g
    return result


def transform_determinant(m,s):
    d1=s+A
    if m==1:return A/d1,0
    d2=(s+LAMBDA+B)*d1-A*B
    mat=[[s+LAMBDA+MU,-LAMBDA*MU],[F(1),F(0)]]
    p,count=power(mat,m-2)
    det=multiply(p,[[d2],[d1]])[0][0]
    return A*LAMBDA**(m-1)/det,count+1


def log10(x):
    with localcontext() as c:
        c.prec=40
        return float(Decimal(x.numerator).log10()-Decimal(x.denominator).log10())


def main():
    means=[]
    for m in (1,2,20,100,5000):
        t=recurrence_mean(m);tm,products=matrix_mean(m)
        assert t==tm==mean_closed_form(m)
        means.append({'target':m,'positive_matrix_products':products,
                      'mean_log10':log10(t),'numerator_bits':t.numerator.bit_length(),
                      'denominator_bits':t.denominator.bit_length(),
                      'exact_comparison_of_three_classical_formulas':True})
    transforms=[]
    for m in (1,2,20,100):
        for s in (F(0),F(1,10000),F(1,10)):
            x=transform_continued_fraction(m,s)
            y,products=transform_determinant(m,s)
            assert x==y
            transforms.append({'target':m,'s':str(s),'transform':float(x),
                               'matrix_products':products,'exact_equality':True})
    killing=[]
    for m in (20,50,100):
        # Independent killing of a baseline process at constant introduced rate.
        # No-killing-before-first-passage probability is exactly F(rate).
        for rate in (F(1,10**6),F(1,10**9)):
            survival=transform_determinant(m,rate)[0]
            killing.append({'target':m,'killing_rate':str(rate),
                            'kill_before_target':float(1-survival),
                            'no_kill_probability_log10':log10(survival)})
    result={'scope':'INTRODUCED rational birth-death comparator and classical transfer construction; no producer execution, scientific novelty or physical-data claim',
            'introduced_rates':{'a':str(A),'b':str(B),'lambda':str(LAMBDA),'mu':str(MU)},
            'mean_results':means,'laplace_results':transforms,'competing_killing_results':killing,
            'self_returning_excursions':{
                'premise':'Attach only excursions returning to the SAME entry state, no other macro exit; rates u and v introduced and identical at all transient states.',
                'exact_mean_identity':'T_with_excursions=(1+u/v)*T_baseline',
                'clock_memory':'M(s)=1+u/(s+v)',
                'limitation':'Nonfatal excursions are not equivalent to killing. General bulk droplets need not return to the same macrostate, and no such decomposition is acquired here.'},
            'cost_limits':['O(log m) counts constant-size matrix products only; rational bit lengths grow with m and input precision.',
                           'The determinant recurrence has signed entries; no floating stability or interval bound is claimed.',
                           'Mean/log-mean and finite-precision probability are different output contracts.',
                           'A fatal-leakage union bound is not a bound for all physical off-front fluctuations.',
                           'No growing-width many-body reduction or actual material lifetime is supplied.']}
    p=Path(__file__);result['script_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    q=p.with_suffix('.json');q.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'means':means,'killing':killing,'exact_laplace_comparisons':len(transforms),
                      'script_bytes':p.stat().st_size,'script_sha256':result['script_sha256'],
                      'json_bytes':q.stat().st_size,'json_sha256':hashlib.sha256(q.read_bytes()).hexdigest()}))


if __name__=='__main__':main()
