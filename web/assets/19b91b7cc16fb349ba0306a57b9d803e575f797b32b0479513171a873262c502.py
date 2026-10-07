"""Bounded independent verification of optimal-prefix exact interval evidence.

Inputs use a DIFFERENT exponential enclosure: positive Taylor series for
exp(+y), an explicit geometric upper tail, reciprocal, and guarded squaring.
LDL is checked using independently implemented INTEGER outward arithmetic;
saved division bounds are checked by exact cross multiplication. No author's
Arithmetic import, libm, floating sign, or unrounded Fraction LDL is used.
"""
from pathlib import Path
from math import comb,gcd
import argparse,datetime,hashlib,json,time

OWN=Path(__file__).parent
DN,DD=138629437,100000000

def up(n,d):
    assert d>0
    return (n+d-1)//d

class Checker:
    def __init__(self,p,guard,deadline):
        self.p=p;self.D=1<<p;self.guard=guard;self.Q=1<<(p+guard)
        self.deadline=deadline;self.stage='initialization'
        self.counts={'independent_exp_inputs':0,'contained_q_enclosures':0,
                     'certified_blocks':0,'positive_pivots':0,'cross_multiplied_L_entries':0}
    def check_time(self,stage):
        self.stage=stage
        if time.perf_counter()>self.deadline:raise TimeoutError('Prospective verifier cap reached: '+stage)
    def add(self,a,b):return a[0]+b[0],a[1]+b[1]
    def sub(self,a,b):return a[0]-b[1],a[1]-b[0]
    def product(self,a,b):
        products=(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1])
        return min(products)//self.D,up(max(products),self.D)
    def sq(self,a):
        low=0 if a[0]<=0<=a[1] else min(a[0]*a[0],a[1]*a[1])
        high=max(a[0]*a[0],a[1]*a[1])
        return low//self.D,up(high,self.D)
    def independent_q(self,N,k):
        numerator=DN*(2*k-N)**2;denominator=DD*4*N
        if not numerator:
            lo=hi=self.Q
        else:
            g=gcd(numerator,denominator);numerator//=g;denominator//=g
            r=0
            while 16*numerator>denominator:denominator*=2;r+=1
            # y<=1/16. Sum positive exp(+y) terms with directed integer bounds.
            term_lo=term_hi=self.Q;sum_lo=sum_hi=self.Q;n=0
            threshold=1<<(self.guard//2)
            while True:
                n+=1
                term_lo=(term_lo*numerator)//(denominator*n)
                term_hi=up(term_hi*numerator,denominator*n)
                if term_hi<=threshold:
                    tail=up(term_hi*denominator*(n+1),denominator*(n+1)-numerator)
                    exp_plus_lo=sum_lo;exp_plus_hi=sum_hi+tail
                    break
                sum_lo+=term_lo;sum_hi+=term_hi
                if n>10000:raise ArithmeticError('Independent positive series failed to terminate')
            # Reciprocal at guard precision; each exact quantity stays enclosed.
            lo=(self.Q*self.Q)//exp_plus_hi;hi=up(self.Q*self.Q,exp_plus_lo)
            for _ in range(r):
                lo=(lo*lo)//self.Q;hi=up(hi*hi,self.Q)
        C=comb(N,k)
        self.counts['independent_exp_inputs']+=1
        return lo//C,up(hi,C)
    def inputs(self,case):
        N=case['N'];q=[tuple(map(int,a)) for a in case['q_intervals']]
        assert len(q)==N+1
        for k in range(N//2+1):
            self.check_time(f'N{N} independent exp input{k}')
            independent=self.independent_q(N,k)
            for j in {k,N-k}:
                assert q[j][0]<=q[j][1]
                assert q[j]==q[k],'Exact palindrome not represented consistently'
                # Cross multiplication compares the different guarded scales.
                assert q[j][0]*self.Q<=independent[0]*self.D
                assert independent[1]*self.D<=q[j][1]*self.Q
                self.counts['contained_q_enclosures']+=1
        return q
    def blocks(self,N,q):
        if N%2:
            m=N//2+1
            return [(0,'full_odd',m,[[q[i+j] for j in range(m)] for i in range(m)])]
        result=[]
        for shift in (0,1):
            m=(N-shift)//2+1;h=m//2
            H=[[q[i+j+shift] for j in range(m)] for i in range(m)]
            P=[];A=[]
            for i in range(h):
                pr=[];ar=[]
                for j in range(h):
                    p=self.add(H[i][j],H[i][m-1-j]);a=self.sub(H[i][j],H[i][m-1-j])
                    pr.append((2*p[0],2*p[1]));ar.append((2*a[0],2*a[1]))
                if m%2:pr.append((2*H[i][h][0],2*H[i][h][1]))
                P.append(pr);A.append(ar)
            if m%2:P.append([(2*H[h][i][0],2*H[h][i][1]) for i in range(h)]+[H[h][h]])
            result.extend([(shift,'plus',m,P),(shift,'minus',m,A)])
        return result
    def verify_block(self,N,expected,saved):
        shift,kind,original,H=expected;n=len(H)
        assert (saved['shift'],saved['block_kind'],saved['original_dimension'],saved['dimension'])==(shift,kind,original,n)
        ds=[tuple(map(int,a)) for a in saved['diagonal_intervals']]
        assert len(ds)==n and len(saved['L_strict_lower_intervals'])==n
        L=[[(0,0) for _ in range(n)] for _ in range(n)]
        for i,row in enumerate(saved['L_strict_lower_intervals']):
            assert len(row)==i
            for k,a in enumerate(row):L[i][k]=tuple(map(int,a));assert L[i][k][0]<=L[i][k][1]
            L[i][i]=(self.D,self.D)
        for i in range(n):
            self.check_time(f'N{N},shift{shift},{kind},pivot{i}')
            pivot=H[i][i]
            for k in range(i):pivot=self.sub(pivot,self.product(self.sq(L[i][k]),ds[k]))
            assert 0<ds[i][0]<=pivot[0]<=pivot[1]<=ds[i][1]
            self.counts['positive_pivots']+=1
            for j in range(i+1,n):
                self.check_time(f'N{N},shift{shift},{kind},L{j},{i}')
                numerator=H[j][i]
                for k in range(i):numerator=self.sub(numerator,self.product(self.product(L[j][k],L[i][k]),ds[k]))
                lo,hi=L[j][i]
                for u in numerator:
                    for d in ds[i]:
                        # All denominator endpoints are positive. No division
                        # rounding implementation is shared with the author.
                        assert lo*d<=u*self.D<=hi*d
                self.counts['cross_multiplied_L_entries']+=1
        self.counts['certified_blocks']+=1
    def case(self,case):
        N=case['N'];q=self.inputs(case);blocks=self.blocks(N,q)
        if N%2:assert case['omitted_matrix_identity']=='H1=J H0 J'
        else:assert case['omitted_matrix_identity'] is None
        assert len(blocks)==len(case['matrices'])
        for expected,saved in zip(blocks,case['matrices']):self.verify_block(N,expected,saved)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True);ap.add_argument('--wall-limit',type=float,required=True)
    ap.add_argument('--guard',type=int,default=64)
    args=ap.parse_args();assert 0<args.wall_limit<=60 and args.guard>=32
    source=Path(args.source)
    outpath=OWN/(source.stem+f'_independent_integer_G{args.guard}.json')
    if outpath.exists():raise SystemExit('Preserving earlier verification receipt; choose a new declared guard precision.')
    started=time.perf_counter();deadline=started+args.wall_limit
    receipt={'status':'RUNNING','source':str(source),'declared_total_wall_cap_seconds':args.wall_limit,
             'guard_bits':args.guard,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'input_algorithm':'positive directed Taylor exp(+y), y<=1/16, geometric tail, reciprocal, guarded squaring',
             'operation_algorithm':'independent outward INTEGER recurrence and exact cross-multiplication LDL division checks',
             'completed_cases':[]}
    checker=None
    try:
        data=json.loads(source.read_text())
        assert data['status']=='PASS all requested finite cases strictly positive'
        assert data['delta']==f'{DN}/{DD}'
        P=data['precision_bits'];assert int(data['denominator'])==1<<P
        lo,hi=data['requested_N_range'];assert 3<=lo<=hi<=199
        assert [c['N'] for c in data['cases']]==list(range(lo,hi+1))
        checker=Checker(P,args.guard,deadline)
        for case in data['cases']:
            checker.case(case);receipt['completed_cases'].append(case['N'])
        receipt['status']='PASS independent exact inputs/congruences/LDL for every requested case'
        receipt['requested_N_range']=[lo,hi];receipt['precision_bits']=P
    except Exception as e:
        receipt['status']='INCOMPLETE';receipt['failure']=repr(e)
        receipt['failure_stage']=checker.stage if checker else 'load/admission'
    receipt['wall_seconds']=time.perf_counter()-started
    receipt['verified_counts']=checker.counts if checker else None
    receipt['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    receipt['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    outpath.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='completed_cases'},indent=2))
    if receipt['status']=='INCOMPLETE':raise SystemExit(1)

if __name__=='__main__':main()
