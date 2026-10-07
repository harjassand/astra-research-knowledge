"""Independent exact-Fraction verification of saved delta=5/4 interval evidence.

This does not import the author's arithmetic implementation. It verifies the
Taylor input enclosures and that every saved LDL interval contains the direct
unrounded rational-interval recurrence using previously certified intervals.
"""
from fractions import Fraction as F
from math import comb,factorial
from pathlib import Path
import hashlib,json,time

class I:
    def __init__(self,lo,hi=None):
        self.lo=F(lo);self.hi=F(lo if hi is None else hi)
        assert self.lo<=self.hi
    def __add__(self,b):return I(self.lo+b.lo,self.hi+b.hi)
    def __sub__(self,b):return I(self.lo-b.hi,self.hi-b.lo)
    def __mul__(self,b):
        v=[self.lo*b.lo,self.lo*b.hi,self.hi*b.lo,self.hi*b.hi]
        return I(min(v),max(v))
    def square(self):
        v=[self.lo**2,self.hi**2]
        return I(0 if self.lo<=0<=self.hi else min(v),max(v))
    def __truediv__(self,b):
        assert b.lo>0
        v=[self.lo/b.lo,self.lo/b.hi,self.hi/b.lo,self.hi/b.hi]
        return I(min(v),max(v))
    def contains(self,b):return self.lo<=b.lo<=b.hi<=self.hi

started=time.perf_counter()
author_path=Path('work/cycle6/c07_s02/phase2/evidence/axial_delta5over4_finite_N63_P384.json')
replay_path=Path('work/cycle6/c05_s03/revisions/evidence/axial_delta5over4_finite_N63_P384.json')
author=json.loads(author_path.read_text());replay=json.loads(replay_path.read_text())
assert author['cases']==replay['cases']
P=author['precision_bits'];D=int(author['denominator'])
assert P==384 and D==2**P
delta=F(author['delta']);assert delta==F(5,4)
assert [c['N'] for c in author['cases']]==list(range(2,64))

def decode(a):return I(F(int(a[0]),D),F(int(a[1]),D))
counts={'exponential_input_enclosures':0,'matrices':0,'positive_pivots':0,'lower_L_entries':0}
for case in author['cases']:
    assert time.perf_counter()-started<30,'Declared30second independent-check cap reached'
    N=case['N'];qraw=case['q_intervals']
    assert len(qraw)==len(case['exp_enclosure_metadata'])==N+1
    for k,(qenc,meta) in enumerate(zip(qraw,case['exp_enclosure_metadata'])):
        x=delta*F((2*k-N)**2,4*N);r=meta['range_squares'];j=meta['odd_terms']
        assert isinstance(r,int) and r>=0
        y=x/F(2**r);assert 0<=y<=F(1,8)
        if not x:
            assert j==0 and r==0
            lo=hi=D
        else:
            assert j>0 and j%2==1
            total=F(1);term=F(1)
            for n in range(1,j+1):
                term*=y/n
                total+=(-term if n%2 else term)
            assert 0<term<=F(1,2**(P+24)) and total>0
            even=total+term
            lo=(total.numerator*D)//total.denominator
            hi=(even.numerator*D+even.denominator-1)//even.denominator
            for _ in range(r):
                lo=(lo*lo)//D
                hi=(hi*hi+D-1)//D
        C=comb(N,k)
        assert list(map(int,qenc))==[lo//C,(hi+C-1)//C]
        counts['exponential_input_enclosures']+=1

    q=list(map(decode,qraw))
    assert [m['shift'] for m in case['matrices']]==[0,1]
    for m in case['matrices']:
        shift=m['shift'];n=(N-shift)//2+1
        assert m['dimension']==n
        ds=list(map(decode,m['diagonal_intervals']))
        assert len(ds)==n
        L=[[I(0) for _ in range(n)] for _ in range(n)]
        for i,row in enumerate(m['L_strict_lower_intervals']):
            assert len(row)==i
            for k,a in enumerate(row):L[i][k]=decode(a)
            L[i][i]=I(1)
        for i in range(n):
            p=q[2*i+shift]
            for k in range(i):p=p-L[i][k].square()*ds[k]
            assert ds[i].contains(p) and ds[i].lo>0
            counts['positive_pivots']+=1
            for j in range(i+1,n):
                numer=q[i+j+shift]
                for k in range(i):numer=numer-L[j][k]*L[i][k]*ds[k]
                candidate=numer/ds[i]
                assert L[j][i].contains(candidate)
                counts['lower_L_entries']+=1
        counts['matrices']+=1

wrapper=Path('work/cycle6/c07_s02/phase2/axial_finite_rational_delta_certificate.py')
code=Path('work/cycle6/c07_s02/phase2/axial_finite_psd_certificate.py')
analytic=Path('work/cycle6/c05_s03/revisions/12_axial_five_fourths_analytic_tail.txt')
out={'status':'INDEPENDENT_EXACT_FIVE_FOURTHS_PREFIX_PASS',
     'delta_exact':'5/4','prefix_range':'every N2..63','precision_bits':P,
     'author_wrapper_sha256':hashlib.sha256(wrapper.read_bytes()).hexdigest(),
     'author_arithmetic_sha256':hashlib.sha256(code.read_bytes()).hexdigest(),
     'author_evidence_sha256':hashlib.sha256(author_path.read_bytes()).hexdigest(),
     'own_analytic_tail_sha256':hashlib.sha256(analytic.read_bytes()).hexdigest(),
     'own_replay_evidence_path':str(replay_path),'own_replay_wall_seconds':replay['wall_seconds'],
     'deterministic_cases_equal':True,'verified_counts':counts,
     'independent_verifier_wall_seconds':time.perf_counter()-started,
     'scope':'Exact finite prefix; joining with proof12 supplies allN symmetric separability and the allalpha subset consequence.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
