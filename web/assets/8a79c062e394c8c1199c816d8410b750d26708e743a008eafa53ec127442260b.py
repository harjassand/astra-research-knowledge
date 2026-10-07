#!/usr/bin/env python3
"""Exact dyadic outward LDL certificates for a finite family; no float signs."""
from pathlib import Path
from fractions import Fraction as F
import argparse,datetime,hashlib,json,math,time
OWN=Path(__file__).parent
def cdiv(a,b):
    assert b>0
    return -((-a)//b)
class Arithmetic:
    def __init__(self,p):self.p=p;self.D=1<<p
    def add(self,a,b):return a[0]+b[0],a[1]+b[1]
    def sub(self,a,b):return a[0]-b[1],a[1]-b[0]
    def mul(self,a,b):
        v=[x*y for x in a for y in b]
        return min(v)//self.D,cdiv(max(v),self.D)
    def square(self,a):
        v=[a[0]*a[0],a[1]*a[1]]
        return (0 if a[0]<=0<=a[1] else min(v)//self.D),cdiv(max(v),self.D)
    def div(self,a,b):
        assert b[0]>0
        v=[(x*self.D,y) for x in a for y in b]
        return min(x//y for x,y in v),max(cdiv(x,y) for x,y in v)
    def exp_minus(self,x):
        assert x>=0
        y=x;r=0
        while y>F(1,8):y/=2;r+=1
        if not y:return (self.D,self.D),{'range_squares':r,'odd_terms':0}
        total=F(1);term=F(1);even=total;j=0
        while True:
            j+=1;term*=y/j;total+=(-1 if j%2 else 1)*term
            if not j%2:even=total
            if j%2 and term<=F(1,1<<(self.p+24)):
                assert total>0
                lo=total.numerator*self.D//total.denominator
                hi=cdiv(even.numerator*self.D,even.denominator)
                value=(lo,hi)
                for _ in range(r):value=self.square(value)
                return value,{'range_squares':r,'odd_terms':j}
    def populations(self,N):
        q=[];meta=[]
        for k in range(N+1):
            x=F((2*k-N)**2,4*N)
            ex,m=self.exp_minus(x);C=math.comb(N,k)
            q.append((ex[0]//C,cdiv(ex[1],C)));meta.append(m)
        return q,meta
    def ldl(self,N,shift,q):
        n=(N-shift)//2+1
        H=[[q[i+j+shift] for j in range(n)] for i in range(n)]
        L=[[(0,0) for _ in range(n)] for _ in range(n)];ds=[]
        for i in range(n):
            v=H[i][i]
            for k in range(i):v=self.sub(v,self.mul(self.square(L[i][k]),ds[k]))
            if v[0]<=0:raise ArithmeticError(f'uncertified positive pivot N={N},shift={shift},i={i},bounds={v}')
            ds.append(v);L[i][i]=(self.D,self.D)
            for j in range(i+1,n):
                v=H[j][i]
                for k in range(i):v=self.sub(v,self.mul(self.mul(L[j][k],L[i][k]),ds[k]))
                L[j][i]=self.div(v,ds[i])
        return {'shift':shift,'dimension':n,'diagonal_intervals':[[str(x),str(y)] for x,y in ds],
                'L_strict_lower_intervals':[[[str(x),str(y)] for x,y in row[:i]] for i,row in enumerate(L)],
                'minimum_lower_pivot_integer':str(min(d[0] for d in ds))}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--max-N',type=int,default=39);ap.add_argument('--precision',type=int,default=384)
    ap.add_argument('--wall-limit',type=float,default=30.);args=ap.parse_args()
    assert 2<=args.max_N<=64 and args.precision>=128 and 0<args.wall_limit<=60
    start=time.perf_counter();a=Arithmetic(args.precision);cases=[]
    out={'scope':'Finite exact interval PSD certificates at delta=1. Requires separate analytic N>=40 proof and compact Bernstein moment-cone lemma for all-N separability.',
         'delta':'1','precision_bits':args.precision,'denominator':str(a.D),'max_N_requested':args.max_N,'cases':cases,
         'algorithm':'outward dyadic interval arithmetic; alternating rational exp series with range squaring; interval LDL without square roots','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        for N in range(2,args.max_N+1):
            if time.perf_counter()-start>args.wall_limit:raise TimeoutError('declared bounded wall limit reached')
            q,meta=a.populations(N)
            case={'N':N,'q_intervals':[[str(x),str(y)] for x,y in q],'exp_enclosure_metadata':meta,'matrices':[a.ldl(N,s,q) for s in [0,1]]}
            cases.append(case)
        out['status']='PASS all requested finite cases strictly positive'
    except Exception as e:
        out['status']='INCOMPLETE';out['failure']=repr(e)
    out['wall_seconds']=time.perf_counter()-start;out['completed_max_N']=cases[-1]['N'] if cases else None
    out['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    path=OWN/'evidence'/f'axial_delta1_finite_N{args.max_N}_P{args.precision}.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'completed_max_N':out['completed_max_N'],'wall_seconds':out['wall_seconds'],'path':str(path)}))
    if out['status']=='INCOMPLETE':raise SystemExit(1)
if __name__=='__main__':main()
