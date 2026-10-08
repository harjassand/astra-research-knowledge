"""Fresh independent reduced-Schur diagnostic. No dense Hilbert-space arrays.
Exact rational sector identities at small N; floating entropy at larger N.
Scientific scope: arithmetic fixtures only, not asymptotic/novelty certification.
"""
import math, json
from fractions import Fraction
from scipy.special import gammaln

def mult(n, a2):
    k=(n-a2)//2
    return math.comb(n,k)-(math.comb(n,k-1) if k else 0)

def exact(n):
    f=[Fraction(1)]
    for j in range(1,n+1): f.append(f[-1]/(2*j+1))
    Z=sum((2*j+1)*mult(2*n,2*j)*f[j] for j in range(n+1))
    ps=[Fraction(0) for _ in range(n+1)]
    qab=Fraction(0)
    for a in range(n%2,n+1,2):
        for b in range(n%2,n+1,2):
            for j in range(abs(a-b)//2,(a+b)//2+1):
                v=mult(n,a)*mult(n,b)*(2*j+1)*f[j]/Z
                ps[j]+=v; qab+=v
    assert qab==1
    assert all(ps[j]==(2*j+1)*mult(2*n,2*j)*f[j]/Z for j in range(n+1))
    return {'N':2*n,'normalization_exact':True,'global_J_law_exact':True}

def numeric(n, cut=40):
    cut=min(cut,n)
    lf=[0.]
    for j in range(1,cut+1): lf.append(lf[-1]-math.log(2*j+1))
    def lm(N,a):
        k=(N-a)//2
        return gammaln(N+1)-gammaln(k+1)-gammaln(N-k+1)+math.log(a+1)-math.log(N-k+1)
    ref=lm(2*n,0)
    Z=sum(math.exp(lm(2*n,2*j)-ref+lf[j])*(2*j+1) for j in range(cut+1))
    normalization=elog=avgs=0.
    for a in range(n%2,n+1,2):
        for b in range(max(n%2,a-2*cut),min(n,a+2*cut)+1,2):
            lo=abs(a-b)//2; hi=min((a+b)//2,cut)
            zs=sum((2*j+1)*math.exp(lf[j]) for j in range(lo,hi+1))
            if not zs: continue
            ss=math.log(zs)-sum((2*j+1)*math.exp(lf[j])*lf[j] for j in range(lo,hi+1))/zs
            q=math.exp(lm(n,a)+lm(n,b)-ref)*zs/Z
            normalization+=q; elog+=q*math.log(b+1); avgs+=q*ss
    return {'N':2*n,'J_cutoff':cut,'normalization':normalization,
            'expected_log_spin_dimension':elog,'mean_conditional_entropy':avgs,
            'flagged_coherent_information':elog-avgs,
            'CI_minus_half_log_N':elog-avgs-0.5*math.log(2*n)}

if __name__=='__main__':
    out={'units':'nats','exact':[exact(n) for n in range(1,9)],
         'numeric':[numeric(n) for n in [4,8,16,32,64,128,256,512,1024]]}
    print(json.dumps(out,indent=2))
