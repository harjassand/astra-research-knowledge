"""Independent displaced coefficient checks; does not alter the implementation.

Run with ../gaussian_transfer/venv/bin/python from the workspace root.
Reference uses the positive O(n) coefficient recurrence, independently of the
saddle integral. Large-n checks use an exact leading-term enclosure.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib, json, sys, time
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'gaussian_transfer'))
from displaced_evaluator import log_H
from flint import arb, ctx

def aa(q):
    q=F(q)
    return arb(q.numerator)/arb(q.denominator)

def reference(n,a,c,prec=1000):
    with ctx.workprec(prec):
        a,c=aa(a),aa(c)
        if n==0: return arb(0)
        prev,cur=arb(1),c
        for k in range(2,n+1):
            prev,cur=cur,(c*cur+a*prev)/k
        return cur.log()

records=[]
for n,a,c,p,force in [
    (1,F(1,3),F(100),20,True),
    (2,F(1,3),F(100),40,True),
    (49,F(1,7),F(100),40,True),
    (50,F(1,7),F(100),40,True),
    (4000,F(1,3),F(1,7),20,False),
    (4001,F(1,3),F(1,7),40,False),
    (4000,F(1,3),F(1,7),80,False),
    (4001,F(1,3),F(1,2**1000),40,False),
    (4000,F(1,3),F(1,2**1000),40,False),
    (4001,F(1,2**1000),F(2**1000),40,False),
    (4001,F(2**1000),F(1,2**1000),40,False),
    (12001,F(1,3),F(1,7),200,False),
]:
    started=time.perf_counter()
    actual,meta=log_H(n,a,c,p,force_integral=force)
    exact=reference(n,a,c,prec=max(1500,5*p+4000))
    with ctx.workprec(300):
        radius=actual.rad()
        row=dict(n=str(n),a=str(a),c=str(c),p=p,
                 method=meta['method'],seconds=time.perf_counter()-started,
                 overlap=bool(actual.overlaps(exact)),
                 radius=str(radius),width_target_pass=bool(2*radius<arb(2)**(-p-1)))
    records.append(row)
    assert row['overlap'] and row['width_target_pass'],row

# If n=2r+1, the positive coefficient sum is between T and T*exp(U),
# T=(a/2)^r*c/r!, U=r*c*c/(3*a). This follows termwise because the
# successive ratios beyond T are at most U/(j+1).
for n,a,c,p in [
    (2**1000+1,F(1,3),F(1,2**1000),40),
    (10**100+1,F(1,3),F(1,10**200),80),
]:
    started=time.perf_counter()
    actual,meta=log_H(n,a,c,p)
    with ctx.workprec(5000):
        r=n//2
        lo=r*(aa(a)/2).log()+aa(c).log()-arb(r+1).lgamma()
        U=aa(F(r)*c*c/(3*a))
        expected=lo+arb(0,U.upper())
        radius=actual.rad()
        row=dict(n=str(n),a=str(a),c=str(c),p=p,
                 method='odd_leading_term_enclosure',
                 seconds=time.perf_counter()-started,
                 overlap=bool(actual.overlaps(expected)),
                 radius=str(radius),width_target_pass=bool(2*radius<arb(2)**(-p-1)))
    records.append(row)
    assert row['overlap'] and row['width_target_pass'],row

target=Path(__file__).resolve().parents[1]/'gaussian_transfer'/'displaced_evaluator.py'
result=dict(status='PASS',checks=len(records),
            implementation_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
            scope='Finite independent recurrence and leading-term checks; not formal verification.',
            records=records)
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'checks':len(records),
                  'max_seconds':max(r['seconds'] for r in records),
                  'implementation_sha256':result['implementation_sha256']},indent=2))
