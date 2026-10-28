"""Finite PGF closure of an unbounded-time retained photon factory.

Probability, raw-source derivative and logarithmic wall-time derivative are
carried jointly. Exact Fraction and high-precision outputs stay separate.
"""
from fractions import Fraction as F
from math import factorial,comb
from functools import lru_cache
from pathlib import Path
import json,time,sys
import mpmath as mp
sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent;OUT=HERE/'outputs';OUT.mkdir(exist_ok=True)
SOURCE=(F(99,500),F(4,5),F(1,500));DET=F(19,20)

@lru_cache(None)
def bs_probability(i,j,k):
    if k<0 or k>i+j:return F(0)
    a=sum(comb(i,r)*comb(j,k-r)*(-1)**(j-k+r)
          for r in range(max(0,k-j),min(i,k)+1))
    return F(a*a*factorial(k)*factorial(i+j-k),factorial(i)*factorial(j)*2**(i+j))

def plus(x,y):return tuple(a+b for a,b in zip(x,y))
def scale(x,c):return tuple(c*a for a in x)
def times(x,y):return (x[0]*y[0],x[1]*y[0]+x[0]*y[1],x[2]*y[0]+x[0]*y[2])
ZERO=(0,0,0)

class Acquisition:
    def __init__(self,memory,exact=False,precision=90):
        self.memory=F(memory);self.exact=exact;self.precision=precision
        if not exact:mp.mp.dps=precision
        self.cast=(lambda x:F(x)) if exact else (lambda x:mp.mpf(x.numerator)/x.denominator if isinstance(x,F) else mp.mpf(x))
        self.lam=self.cast(self.memory);self.hcache={};self.kcache={}
        self.node_count=0;self.maximum_exponent=0
    def kernel(self,m):
        if m in self.kcache:return self.kcache[m]
        size=2*m+1;outsize=4*m+1;L=self.memory;D=DET;K=[]
        # One fusion clock has uniform loss on both modes, commuting with BS.
        # Herald survival combines with inefficiency; target loss is binomial.
        for i in range(size):
            ki=[]
            for j in range(size):
                p=[bs_probability(i,j,k) for k in range(i+j+1)];kr=[]
                for r in range(outsize):
                    ans=sum(p[k]*(1-D*L)**(i+j-k)*comb(k,r)*L**r*(1-L)**(k-r)
                            for k in range(r,i+j+1))
                    kr.append(self.cast(ans))
                if self.exact:assert sum(kr)<=1
                else:assert sum(kr)<=1+mp.mpf('1e-60')
                ki.append(kr)
            K.append(ki)
        self.kcache[m]=K;return K
    def H(self,n,e=0):
        if self.memory==1:e=0
        key=(n,e)
        if key in self.hcache:return self.hcache[key]
        self.node_count+=1;self.maximum_exponent=max(self.maximum_exponent,e)
        z=self.lam**e
        if n==1:
            ans=[(self.cast(p)*z,)*3 for p in SOURCE]
            self.hcache[key]=ans;return ans
        m=n//2;size=2*m+1;outsize=2*n+1
        left=self.H(m,e);K=self.kernel(m)
        shifted=[self.H(m,e+s) for s in range(size)] if self.memory!=1 else [left]*size
        A=[ZERO for _ in range(outsize)]
        for i in range(size):
            for l in (range(i+1) if self.memory!=1 else [i]):
                mixed=[ZERO for _ in range(size)]
                if self.memory==1:mixed=left
                else:
                    for s in range(i-l+1):
                        coeff=comb(i,l)*comb(i-l,s)*(-1)**s;row=shifted[l+s]
                        for j in range(size):mixed[j]=plus(mixed[j],scale(row[j],coeff))
                for j in range(size):
                    p=times(left[i],mixed[j])
                    if not any(p):continue
                    for r,kprob in enumerate(K[l][j]):
                        if kprob:A[r]=plus(A[r],scale(p,kprob))
        A=[(z*a,z*b,z*(c+a)) for a,b,c in A] # one fusion clock
        S=ZERO
        for row in left:S=plus(S,row)
        G=times(S,S);G=(z*G[0],z*G[1],z*(G[2]+G[0]))
        success=ZERO
        for row in A:success=plus(success,row)
        failure=tuple(x-y for x,y in zip(G,success));den=1-failure[0]
        assert den>0
        ans=[(a/den,b/den+a*failure[1]/den**2,c/den+a*failure[2]/den**2) for a,b,c in A]
        self.hcache[key]=ans;return ans
    def acquire(self,n):
        start=time.perf_counter();rows=self.H(n);total=sum(r[0] for r in rows)
        if self.exact:assert total==1 and min(r[0] for r in rows)>=0
        else:
            assert abs(total-1)<mp.mpf('1e-45'),str(total)
            assert min(r[0] for r in rows)>-mp.mpf('1e-45')
        mean=sum(k*r[0] for k,r in enumerate(rows))
        var=sum(k*k*r[0] for k,r in enumerate(rows))-mean**2
        source=sum(r[1] for r in rows);wall=sum(r[2] for r in rows)
        result={'n':n,'memory_survival_per_clock':str(self.memory),'mean':float(mean),'fano':float(var/mean),
                'expected_raw_source_attempts':float(source),'expected_wall_clocks':float(wall),
                'photon_wall_time_covariance':float(sum(k*r[2] for k,r in enumerate(rows))-mean*wall),
                'photon_source_cost_covariance':float(sum(k*r[1] for k,r in enumerate(rows))-mean*source),
                'PGF_nodes':self.node_count,'PGF_scalar_entries_including_derivatives':sum(3*len(v) for v in self.hcache.values()),
                'fusion_kernel_scalar_entries':sum(len(coeffrow) for matrix in self.kcache.values() for row in matrix for coeffrow in row),
                'cumulative_process_BS_probability_cache_entries':bs_probability.cache_info().currsize,
                'maximum_integer_exponent':self.maximum_exponent,'time_cutoff':None,
                'arithmetic':'exact Fraction' if self.exact else 'mpmath '+str(self.precision)+' digits, not interval certified',
                'elapsed_seconds':time.perf_counter()-start}
        if self.exact:
            result['exact_output_probabilities']=[str(r[0]) for r in rows]
            result['exact_source_attempts']=str(source);result['exact_wall_clocks']=str(wall)
            result['maximum_cached_numerator_bits']=max(v.numerator.bit_length() for row in self.hcache.values() for rr in row for v in rr)
            result['maximum_cached_denominator_bits']=max(v.denominator.bit_length() for row in self.hcache.values() for rr in row for v in rr)
        else:
            result['output_probabilities_decimal']=[mp.nstr(r[0],40) for r in rows]
            result['working_precision_decimal_digits']=self.precision
        return result

if __name__=='__main__':
    start=time.perf_counter();allresults=[]
    exact=Acquisition(F(999,1000),exact=True).acquire(4);allresults.append(exact)
    print('EXACT_N4',json.dumps({k:v for k,v in exact.items() if not k.startswith('exact_')}),flush=True)
    for memory in [F(999,1000),F(99999,100000)]:
        model=Acquisition(memory,precision=90)
        for n in [4,8,16]:
            row=model.acquire(n);allresults.append(row)
            print('PGF',json.dumps({k:v for k,v in row.items() if not k.startswith('output_')}),flush=True)
    import contextlib,io
    with contextlib.redirect_stdout(io.StringIO()):import bucket_factory as ideal
    for n in [4,8,16]:
        row=Acquisition(F(1),precision=90).acquire(n);target=ideal.law(n,SOURCE,DET)
        assert abs(row['mean']-float(target['mean']))<1e-11
        assert abs(row['expected_raw_source_attempts']-float(ideal.cost[n]))<1e-8
        assert abs(row['expected_wall_clocks']-float(ideal.elapsed_clock[n]))<1e-8
    result={'status':'FINITE_PGF_CLOSURE_ACQUIRED; exact small replay and high-precision larger examples; no independent audit',
            'source_probabilities':[str(p) for p in SOURCE],'bucket_efficiency':str(DET),'source_and_fusion_clocks':1,
            'models':allresults,'no_loss_controls':'mean, full source cost and wall time agree through n16 with separate positive integral formula',
            'physical_implementation':'NOT_ACQUIRED','historical_priority':'UNKNOWN','general_method_advantage':'UNKNOWN',
            'elapsed_seconds':time.perf_counter()-start}
    (OUT/'WAITING_LOSS_ACQUISITION.json').write_text(json.dumps(result,indent=2)+'\n')
    print('COMPLETED',json.dumps({'elapsed_seconds':result['elapsed_seconds']}),flush=True)
