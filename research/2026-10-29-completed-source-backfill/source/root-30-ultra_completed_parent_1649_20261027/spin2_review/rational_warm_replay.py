"""Independent all-rational warm transfer enclosure; stdlib only.
The candidate polynomial and exact open moments are source data, not imported
producer logic. Exp and spectral roots have proved rational outward bounds.
"""
from fractions import Fraction as F
from pathlib import Path
from math import factorial,isqrt,prod
import json,time,hashlib
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'inputs/degree96'
def add(a,b):return a[0]+b[0],a[1]+b[1]
def scale(a,c):return (a[0]*c,a[1]*c) if c>=0 else (a[1]*c,a[0]*c)
def mul(a,b):
    v=[x*y for x in a for y in b];return min(v),max(v)
def divide(a,b):
    assert b[0]>0
    return mul(a,(1/b[1],1/b[0]))
def total(items):
    answer=(F(0),F(0))
    for value in items:answer=add(answer,value)
    return answer
def exact(q):return F(q),F(q)
def exp_box(x):
    x=F(x)
    if x<0:
        a,b=exp_box(-x);return 1/b,1/a
    n=128;assert x<n+2
    term=F(1);value=term
    for k in range(1,n+1):term=term*x/k;value+=term
    remainder=term*x/(n+1)/(1-x/F(n+2))
    return value,value+remainder
def root_upper(q,p,bits=64):
    assert q>=0 and p in [2,4]
    n=(q.numerator*2**(bits*p)+q.denominator-1)//q.denominator
    r=isqrt(n) if p==2 else isqrt(isqrt(n))
    if r**p<n:r+=1
    answer=F(r,2**bits);assert answer**p>=q
    return answer
def upward(q,digits=20):
    q=F(q);scale=10**digits
    return F(-((-q.numerator*scale)//q.denominator),scale)
def downward(q,digits=20):
    q=F(q);scale=10**digits
    return F(q.numerator*scale//q.denominator,scale)
def open_box(row,beta):
    n=row['n'];m=list(map(int,row['trace_2H_powers']));degree=len(m)-1
    value=sum((F(v)*(-beta/F(2))**k/factorial(k) for k,v in enumerate(m)),F(0))
    x=6*(n-1)*beta
    tail=5**n*exp_box(x)[1]*x**(degree+1)/factorial(degree+1)
    return (value-tail)/5**n,(value+tail)/5**n
def quadratic(c,m,offset):
    return total(scale(m[i+j+offset],c[i]*c[j]) for i in range(len(c)) for j in range(len(c)))
def full_moments(beta):
    pair=total(scale(exp_box(-2*beta*e),d) for d,e in [(1,-6),(3,-5),(5,-3),(7,0),(9,4)])
    periodic=total(scale(exp_box(-beta*F(j*(j+1)-a*(a+1)-b*(b+1),2)),2*j+1)
       for a in range(5) for b in range(5) for j in range(abs(a-b),a+b+1))
    return {2:scale(pair,F(1,25)),4:scale(periodic,F(1,625))}
def run():
    started=time.monotonic();raw=(SOURCE/'open_moments_exact_degree96.json').read_bytes();data=json.loads(raw)
    candidates_raw=(SOURCE/'vacuum_krylov_transfer_degree96.json').read_bytes();candidates=json.loads(candidates_raw)
    records={row['n']:row for row in data['chains']};assert set(records)==set(range(1,7))
    # Full exact independent spectral checks for the two shortest open chains.
    pair_e=[(d,2*e) for d,e in [(1,-6),(3,-5),(5,-3),(7,0),(9,4)]]
    triple_e=[(2*j+1,j*(j+1)-a*(a+1)-6) for a in range(5) for j in range(abs(a-2),a+3)]
    for n,spectrum in [(2,pair_e),(3,triple_e)]:
        assert [sum(d*e**k for d,e in spectrum) for k in range(97)]==list(map(int,records[n]['trace_2H_powers']))
    for n,row in records.items():
        moments=list(map(int,row['trace_2H_powers']));assert len(moments)==97
        assert moments[:4]==([5,0,0,0] if n==1 else [5**n,0,48*(n-1)*5**n,-48*(n-1)*5**n])
        assert all(abs(v)<=5**n*(12*(n-1))**k for k,v in enumerate(moments))
        if n>1:
            modulus=prod(row['CRT_primes']);bound=max(5**n*(12*(n-1))**k for k in range(97))
            assert modulus==int(row['CRT_modulus']) and modulus>2*bound
    rows=[]
    for beta in [F(1,8),F(1,4),F(1,2)]:
        source=next(row for row in candidates['rows'] if F(row['beta_exact'])==beta)
        c=list(map(F,source['candidate_rational_decimal_coefficients']))
        m=[exact(1)]+[open_box(records[n],beta) for n in range(1,7)]
        norm=quadratic(c,m,0);assert norm[0]>0
        theta=divide(quadratic(c,m,1),norm)
        variance=add(divide(quadratic(c,m,2),norm),scale(mul(theta,theta),-1));assert variance[1]>=0
        options=[]
        for p,value in full_moments(beta).items():
            remainder=value[1]-theta[0]**p
            assert remainder>=0
            rho=root_upper(remainder,p)
            options.append((rho,p,remainder))
        rho,p,remainder=min(options);assert theta[0]>rho
        upper=theta[1]+variance[1]/(theta[0]-rho)
        delta=(upper-theta[0])/theta[0]
        ratio=upward(rho/theta[0],12);assert ratio<1
        rings=[]
        for n in [128,256]:
            assert n*delta<1
            tail=(remainder/theta[0]**p)*ratio**(n-p)
            width=n*delta/(1-n*delta)+tail
            rings.append({'n':n,'log_normalized_Z_width_upper_rational':str(upward(width)),
              'log_width_diagnostic_float':float(width),'spatial_defect_upper_rational':str(upward(2*tail))})
        rows.append({'beta':str(beta),'selected_complete_even_moment':p,
          'all_other_moduli_upper_rational':str(rho),
          'strict_separation_lower_rational':str(downward(theta[0]-rho)),
          'rings':rings})
    result={'status':'INDEPENDENT_PURE_RATIONAL_WARM_INPUT_REPLAY_PASS',
       'moment_source_sha256':hashlib.sha256(raw).hexdigest(),
       'candidate_source_sha256':hashlib.sha256(candidates_raw).hexdigest(),
       'independent_full_moment_spectral_controls_sites':[2,3],
       'exact_moment_CRT_source_scope':'Whole producer algorithm reviewed; n4..6 moment powers not independently regenerated here. All reconstruction bounds/all-state leading identities checked.',
       'rows':rows,'seconds':time.monotonic()-started,
       'scope':'Actual continuous-kernel warm enclosure under the reviewed exact moment inputs and source transfer identities. No imported interval engine, finite rank, cold seed or uniform gap premise.'}
    (ROOT/'RATIONAL_WARM_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()
