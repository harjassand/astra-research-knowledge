"""Original finite-bit enclosure of a two-sided physical-pair Duhamel bound.
Only integer arithmetic is used for the enclosure. Final decimals are display.
No acquired code, material parameters, or simulations.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np,itertools,math,heapq,json,time
from fractions import Fraction
from pathlib import Path
OUT=Path(__file__).resolve().parent

def pair_H(n,edges,rates):
    assert len(edges)==len(rates) and len({tuple(sorted(e)) for e in edges})==len(edges)
    assert all(0<=x<n and 0<=y<n and x!=y for x,y in edges)
    assert all(Fraction(r).denominator==1 and r>=0 for r in rates), "Integer nonnegative rates are required; do not truncate"
    pairs=list(itertools.combinations(range(n),2)); idx={p:i for i,p in enumerate(pairs)}
    W=np.zeros((n,n),dtype=object)
    for (x,y),r in zip(edges,rates):W[x,y]=W[y,x]=int(r)
    H=np.zeros((len(pairs),len(pairs)),dtype=object)
    for i,(x,y) in enumerate(pairs):
        H[i,i]=2*W[x,y]
        for a,z in ((x,y),(y,x)):
            for v in range(n):
                if v in (a,z):continue
                j=idx[tuple(sorted((v,z)))];H[i,i]+=W[a,v];H[i,j]-=W[a,v]
    return H,[idx[tuple(sorted(e))] for e in edges]

class EnclosedSurvival:
    def __init__(self,H):
        self.d=len(H); self.Lam=int(max(H[i,i] for i in range(self.d)))
        self.m=(self.Lam*self.Lam).bit_length()+60
        self.N=1<<self.m;self.p=self.m+100;self.Q=1<<self.p
        self.ec=self.Lam*self.Lam*(1<<(self.p-self.m))
        self.er=2*self.N*self.d+self.m+2
        P=np.eye(self.d,dtype=object)*self.Q-H*(1<<(self.p-self.m))
        assert np.all(P>=0) and all(sum(P[i,:])<=self.Q for i in range(self.d))
        self.powers=[P]
        for j in range(self.m):
            P=(P@P)//self.Q
            assert np.all(P>=0) and all(sum(P[i,:])<=self.Q for i in range(self.d))
            self.powers.append(P)
        self.cache={Fraction(0):([self.Q]*self.d,[self.Q]*self.d)}
    def at(self,t):
        t=Fraction(t)
        if t in self.cache:return self.cache[t]
        assert t>=0 and t<=1 and self.N%t.denominator==0
        k=t.numerator*(self.N//t.denominator)
        v=np.full(self.d,self.Q,dtype=object);j=0
        while k:
            if k&1:v=(self.powers[j]@v)//self.Q
            j+=1;k>>=1
        lo=[max(0,int(x)-self.ec) for x in v]
        hi=[min(self.Q,int(x)+self.ec+self.er) for x in v]
        self.cache[t]=(lo,hi);return lo,hi

def certify(n,edges,rates,boost,start,epsilon=Fraction(1,20)):
    A,ei=pair_H(n,edges,boost);B,_=pair_H(n,edges,rates)
    t=time.time();SA=EnclosedSurvival(A);SB=EnclosedSurvival(B)
    delta=[abs(a-b) for a,b in zip(rates,boost)]
    denom=SA.Q*SB.Q
    def segment(a,b):
        alo,ahi=SA.at(a);blo,bhi=SA.at(b)
        clo,chi=SB.at(1-b);dlo,dhi=SB.at(1-a)
        upper=Fraction(sum(d*ahi[e]*chi[e] for d,e in zip(delta,ei)),denom)*(b-a)
        lower=Fraction(sum(d*blo[e]*dlo[e] for d,e in zip(delta,ei)),denom)*(b-a)
        assert upper>=lower>=0
        return lower,upper
    # A rigorous rational coarse tail bound avoids using floating-point logs.
    # General local tail: mf*c²/W [b²+2(1+b)(2+log(W/c))].
    # log(W/c) <= ceil(log2(W/c)) since log(2)<1, computed with integer powers.
    s=n-start;c=Fraction(s*(s-1),4);boundary=rates[start-1];mf=n-1-start;W=boost[-1]
    klog=0
    while Fraction(1<<klog)<Fraction(W,1)/c:klog+=1
    tail=Fraction(mf,1)*c*c/W*(boundary*boundary+2*(1+boundary)*(2+klog))
    assert W>=2*c
    low,up=segment(Fraction(0),Fraction(1)); heap=[(-(up-low),0,Fraction(0),Fraction(1),low,up)];counter=1
    while up+tail>epsilon and len(heap)<50000:
        _,_,a,b,l,u=heapq.heappop(heap);mid=(a+b)/2
        l1,u1=segment(a,mid);l2,u2=segment(mid,b)
        low+=l1+l2-l;up+=u1+u2-u
        heapq.heappush(heap,(-(u1-l1),counter,a,mid,l1,u1));counter+=1
        heapq.heappush(heap,(-(u2-l2),counter,mid,b,l2,u2));counter+=1
    result=dict(n=n,edges=edges,original_rates=rates,intermediate_rates=boost,fast_vertices=list(range(start,n)),pair_states=len(A),epsilon=str(epsilon),certificate_lower_float=float(low),certificate_upper_float=float(up),tail_upper_float=float(tail),total_upper_float=float(up+tail),total_upper_exact=str(up+tail),certified=up+tail<=epsilon,quadrature_intervals=len(heap),survival_queries=[len(SA.cache),len(SB.cache)],precision=[dict(Lambda=ob.Lam,clock_power_m=ob.m,fixed_bits_p=ob.p,clock_error_bound=str(Fraction(ob.ec,ob.Q)),round_error_bound=str(Fraction(ob.er,ob.Q))) for ob in (SA,SB)],seconds=time.time()-t)
    if edges==[(i,i+1) for i in range(n-1)] and all(x==W for x in boost[start:]):
        factorial=math.factorial(s)-1;root=math.isqrt(factorial)
        amp_upper=Fraction(root+(root*root<factorial),2)
        log_upper=0
        while Fraction(1<<log_upper)<amp_upper:log_upper+=1
        if W>=amp_upper*s**4/8:
            generic_tail=Fraction(1,W)+Fraction(boundary*(boundary+2)*(log_upper+1)*s*s,4*W)
            result['path_Aldous_tail_upper']=str(generic_tail)
            result['path_Aldous_total_upper_float']=float(up+generic_tail)
            result['path_Aldous_total_upper_exact']=str(up+generic_tail)
    if n==6 and start==2 and rates==[1,10,100,1000,10000] and W>=24:
        classical_tail=Fraction(1+4*boundary*(boundary+2),W)
        result['classical_averaging_tail_upper']=str(classical_tail)
        result['classical_total_upper_float']=float(up+classical_tail)
        result['classical_total_upper_exact']=str(up+classical_tail)
    print(json.dumps(result),flush=True)
    return result

if __name__=='__main__':
    n=6;edges=[(i,i+1) for i in range(n-1)];rates=[1,10,100,1000,10000];boost=[1,10,1000000,1000000,1000000]
    r=certify(n,edges,rates,boost,2)
    (OUT/'rigorous_pair_certificate.json').write_text(json.dumps(r,indent=2))
