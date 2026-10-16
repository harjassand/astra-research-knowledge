"""Original integer-only certifier composing standard exterior-square heat kernels
with two-sided pair Duhamel bounds. No acquired executable code.
Input graph is an ordered nearest-neighbor path, with nonnegative integer rates.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
from fractions import Fraction as F
import math,heapq,time,json,resource,sys
from pathlib import Path
BASE=Path(os.environ.get('PAIR_CERTIFICATE_BASE',str(Path(__file__).resolve().parent/'original_dependencies')))
sys.path.insert(0,str(BASE))
from fair_bit_sampler import sampler_error

class PathSurvival:
    def __init__(self,rates,accuracy_bits=80):
        assert rates and all(F(x).denominator==1 and x>=0 for x in rates)
        self.rates=list(map(int,rates));self.n=len(rates)+1;n=self.n
        L=np.zeros((n,n),dtype=object)
        for i,r in enumerate(self.rates):
            L[i,i]+=r;L[i+1,i+1]+=r;L[i,i+1]-=r;L[i+1,i]-=r
        self.Lambda=max(map(int,np.diag(L)))
        self.m=max(1,(self.Lambda*self.Lambda).bit_length()+accuracy_bits+3)
        self.N=1<<self.m
        self.p=self.m+accuracy_bits+n.bit_length()+5
        self.Q=1<<self.p;self.D=self.Q*self.Q
        P=np.eye(n,dtype=object)*self.Q-L*(self.Q//self.N)
        self.powers=[P]
        self.matmul_count=0
        t=time.perf_counter()
        for j in range(self.m):
            P=(P@P)//self.Q;self.matmul_count+=1
            assert np.all(P>=0)
            assert all(sum(P[i,:])<=self.Q for i in range(n))
            self.powers.append(P)
        self.preprocess_seconds=time.perf_counter()-t
        # Row l1 error <= 2 Lambda^2/N + n N/Q.
        # The antisymmetric bilinear form has error <= twice row l1 error.
        self.survival_error_num=4*self.Lambda*self.Lambda*(self.Q//self.N)+2*n*self.N
        self.survival_error=F(self.survival_error_num,self.Q)
        self.cache={F(0):([self.D]*(n-1),[self.D]*(n-1))}
        self.query_seconds=0
    def at(self,t):
        t=F(t)
        if t in self.cache:return self.cache[t]
        assert 0<=t<=1 and self.N%t.denominator==0
        before=time.perf_counter(); k=t.numerator*(self.N//t.denominator)
        M=np.eye(self.n,dtype=object)*self.Q;j=0
        while k:
            if k&1:
                M=(M@self.powers[j])//self.Q;self.matmul_count+=1
            j+=1;k>>=1
        lo=[];hi=[];err=self.survival_error_num*self.Q
        for x in range(self.n-1):
            row=M[x+1,:];total=sum(row);prefix=0;s=0
            for a in range(self.n):
                s+=int(M[x,a])*(total-row[a]-2*prefix);prefix+=row[a]
            lo.append(max(0,min(self.D,int(s)-err)))
            hi.append(max(0,min(self.D,int(s)+err)))
            assert lo[-1]<=hi[-1]
        self.cache[t]=(lo,hi);self.query_seconds+=time.perf_counter()-before
        return lo,hi
    def receipt(self):
        return dict(n=self.n,Lambda=self.Lambda,clock_m=self.m,fixed_bits_p=self.p,
            survival_error_exact=str(self.survival_error),powers=len(self.powers),
            stored_power_entries=len(self.powers)*self.n*self.n,queries=len(self.cache),
            matrix_multiplications=self.matmul_count,preprocess_seconds=self.preprocess_seconds,
            query_seconds=self.query_seconds)

def classical_tail(n,start,rates,boost):
    s=n-start;W=boost[start];Gamma=rates[start-1]
    assert all(x==W for x in boost[start:]) and W>0
    fac=math.factorial(s)-1;q=math.isqrt(fac);A=F(q+(q*q<fac),2)
    k=0
    while F(1<<k)<A:k+=1
    assert W>=A*s**4/8
    return F(1,W)+F(Gamma*(Gamma+2)*(k+1)*s*s,4*W)

def integrate(SA,SB,delta,tail,epsilon=F(1,20),max_intervals=10000):
    D=SA.D*SB.D
    def segment(a,b):
        alo,ahi=SA.at(a);blo,bhi=SA.at(b)
        clo,chi=SB.at(1-b);dlo,dhi=SB.at(1-a)
        upper=F(sum(d*x*y for d,x,y in zip(delta,ahi,chi)),D)*(b-a)
        lower=F(sum(d*x*y for d,x,y in zip(delta,blo,dlo)),D)*(b-a)
        assert upper>=lower>=0
        return lower,upper
    low,up=segment(F(0),F(1));heap=[(-(up-low),0,F(0),F(1),low,up)];count=1
    while up+tail>epsilon and len(heap)<max_intervals:
        _,_,a,b,l,u=heapq.heappop(heap);mid=(a+b)/2
        l1,u1=segment(a,mid);l2,u2=segment(mid,b)
        low+=l1+l2-l;up+=u1+u2-u
        heapq.heappush(heap,(-(u1-l1),count,a,mid,l1,u1));count+=1
        heapq.heappush(heap,(-(u2-l2),count,mid,b,l2,u2));count+=1
    return low,up,len(heap),max(b.denominator.bit_length()-1 for _,_,a,b,l,u in heap)

def certify(n=20,epsilon=F(1,20)):
    assert n>=4, 'This averaging wrapper needs at least four sites'
    rates=[10**i for i in range(n-1)];W=10**n;boost=[1,10]+[W]*(n-3)
    delta=[abs(a-b) for a,b in zip(rates,boost)]
    bits=sum(delta).bit_length()+40
    begin=time.perf_counter();SA=PathSurvival(boost,bits);SB=PathSurvival(rates,bits)
    tail=classical_tail(n,2,rates,boost)
    low,up,intervals,depth=integrate(SA,SB,delta,tail,epsilon)
    sample_error=sampler_error(n);total=up+tail+sample_error
    return dict(method='path exterior square with integer Euler powers',n=n,
        rates=rates,boost=boost,fast_vertices=list(range(2,n)),pair_states=n*(n-1)//2,
        one_walker_states=n,accuracy_bits=bits,epsilon_exact=str(epsilon),
        Duhamel_lower_exact=str(low),Duhamel_upper_exact=str(up),Duhamel_upper_float=float(up),
        classical_tail_exact=str(tail),sampler_error_exact=str(sample_error),
        sampler_error_float=float(sample_error),total_upper_exact=str(total),total_upper_float=float(total),
        certified=total<=epsilon,quadrature_intervals=intervals,maximum_dyadic_depth=depth,
        heat_receipts=[SA.receipt(),SB.receipt()],wall_seconds=time.perf_counter()-begin,
        peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        original_expected_attempts=sum(rates),averaged_expected_attempts=11,
        worst_case_sampler_random_bits=64+64*32*(4+(n-3).bit_length())+
            32*sum((m-1).bit_length() for m in range(2,n-1)),
        randomness='independent fair bits; existing sampler unchanged')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=20);p.add_argument('--output',default='exterior_receipt.json');a=p.parse_args()
    r=certify(a.n);Path(a.output).write_text(json.dumps(r,indent=2));print(json.dumps(r),flush=True)
