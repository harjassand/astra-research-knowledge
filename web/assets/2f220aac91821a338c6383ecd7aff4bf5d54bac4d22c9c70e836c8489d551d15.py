"""Phased site-sign Pfaffian counter near an acquired real matching.

Derived from the c03_l10 paired-volume estimator after authorized cross-phase.
All production arithmetic is exact Q(i). Every sample costs polynomial bit
work. This module implements the counter/FPRAS, not an arbitrary prefix or
Born sampler. Finite exact tests do not certify the general theorem.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import grassmann_bcs as g
import lowrank_bcs as lr
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations,product
import random
import time
import json

def matmul(A,B):
    n=len(A)
    out=[[g.ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            x=g.ZERO
            for a in range(n): x=g.add(x,g.mul(A[i][a],B[a][j]))
            out[i][j]=x
    return out

def skew(F,signs,phased=True,alphas=None):
    n=len(F)
    phases=([g.qc(s) if not phased or i%2==0 else g.qc(0,s)
             for i,s in enumerate(signs)] if alphas is None else
            [g.mul(a,g.qc(s)) for a,s in zip(alphas,signs)])
    A=[[g.add(g.mul(phases[i],F[i][j]),g.neg(g.mul(F[j][i],phases[j])))
        for j in range(n)] for i in range(n)]
    assert all(A[i][j]==g.neg(A[j][i]) for i in range(n) for j in range(n))
    return A

def sqrt_coefficients(A,k):
    """[t^0..t^k] sqrt(det(I+t A* A)), via traces/Newton exactly."""
    n=len(A)
    Ah=[[g.conj(A[j][i]) for j in range(n)] for i in range(n)]
    B=matmul(Ah,A)
    power=[[g.ONE if i==j else g.ZERO for j in range(n)] for i in range(n)]
    traces=[Q(0)]
    d=[Q(1)]
    for m in range(1,k+1):
        power=matmul(power,B)
        tr=g.ZERO
        for i in range(n): tr=g.add(tr,power[i][i])
        assert tr[1]==0
        traces.append(tr[0])
        d.append(sum((1 if j%2 else -1)*d[m-j]*traces[j]
                     for j in range(1,m+1))/m)
    q=[Q(1)]
    for m in range(1,k+1):
        q.append((d[m]-sum(q[j]*q[m-j] for j in range(1,m)))/2)
    assert all(x>=0 for x in q)
    return q

def principal_pfaffian_coefficients(A):
    """Independent exponential verifier, used only on n<=6."""
    n=len(A)
    @lru_cache(None)
    def pf(R):
        if not R: return g.ONE
        x=g.ZERO
        for j in range(1,len(R)):
            c=g.mul(A[R[0]][R[j]],pf(R[1:j]+R[j+1:]))
            if j%2==0: c=g.neg(c)
            x=g.add(x,c)
        return x
    return [sum(g.abs2(pf(R)) for R in combinations(range(n),2*k))
            for k in range(n//2+1)]

def acquire(F,k):
    """Fixed pairs (0,1),(2,3),...; retain real matching entries and diagonal."""
    n=len(F)
    if n%2 or not 0<=k<=n//2: raise ValueError('even n and legal k required')
    G=[[F[i][i] if i==j else g.ZERO for j in range(n)] for i in range(n)]
    beta=[]
    for i in range(0,n,2):
        a=F[i][i+1][0]
        b=F[i+1][i][0]
        G[i][i+1]=g.qc(a)
        G[i+1][i]=g.qc(b)
        beta.append(a*a+b*b)
    cs=[Q(1)]+[Q(0)]*(n//2)
    for b in beta:
        for j in range(n//2,0,-1): cs[j]+=b*cs[j-1]
    delta2=sum(g.abs2(g.add(F[i][j],g.neg(G[i][j])))
               for i in range(n) for j in range(n))
    beta_min=min(beta,default=Q(0))
    accepted=(k==0) or (beta_min>0 and delta2<=beta_min/(256*k*k))
    return G,{'accepted':accepted,'n':n,'pair_count':k,'beta':beta,
              'beta_min':beta_min,'residual_Frobenius_squared':delta2,
              'threshold':None if k==0 else beta_min/(256*k*k),
              'baseline_counts':cs,'baseline_norm':cs[k]}

def acquire_complex(F,k):
    """Exact rational-unit-circle phases for arbitrary complex matching edges."""
    n=len(F)
    if n%2 or not 0<=k<=n//2: raise ValueError('even n and legal k required')
    G=[[F[i][i] if i==j else g.ZERO for j in range(n)] for i in range(n)]
    m=16*max(1,k)
    candidates=[]
    for j in range(-m,m+1):
        a=g.qc(Q(m*m-j*j,m*m+j*j),Q(2*m*j,m*m+j*j))
        candidates.extend((a,g.neg(a)))
    beta=[]
    alphas=[]
    phase_errors=[]
    for i in range(0,n,2):
        a=F[i][i+1]
        b=F[i+1][i]
        G[i][i+1],G[i+1][i]=a,b
        w=g.mul(a,g.conj(b))
        alpha=min(candidates,key=lambda z:abs(g.mul(w,g.conj(z))[0]))
        assert g.abs2(alpha)==1
        beta_i=g.abs2(a)+g.abs2(b)
        error=2*abs(g.mul(w,g.conj(alpha))[0])/beta_i if beta_i else Q(0)
        assert error<=Q(1,m)
        beta.append(beta_i)
        alphas.extend((g.ONE,alpha))
        phase_errors.append(error)
    cs=[Q(1)]+[Q(0)]*(n//2)
    for b in beta:
        for j in range(n//2,0,-1):cs[j]+=b*cs[j-1]
    delta2=sum(g.abs2(g.add(F[i][j],g.neg(G[i][j])))
               for i in range(n) for j in range(n))
    beta_min=min(beta,default=Q(0))
    accepted=(k==0) or (beta_min>0 and delta2<=beta_min/(1024*k*k))
    return G,{'accepted':accepted,'n':n,'pair_count':k,'beta':beta,
              'beta_min':beta_min,'residual_Frobenius_squared':delta2,
              'threshold':None if k==0 else beta_min/(1024*k*k),
              'baseline_counts':cs,'baseline_norm':cs[k],
              'phase_grid_m':m,'phase_errors':phase_errors,'phases':alphas}

def approximate_count(F,k,epsilon=Q(1,2),failure=Q(1,2),rng=None,complex_matching=False):
    """Capped median means. Certificate failure returns NOT_CERTIFIED."""
    if not 0<epsilon<=1 or not 0<failure<1: raise ValueError('invalid accuracy')
    G,c=(acquire_complex(F,k) if complex_matching else acquire(F,k))
    if not c['accepted']: return {'status':'NOT_CERTIFIED','certificate':c}
    if k==0: return {'status':'OK','estimate':Q(1),'samples':0,'random_bits':0,
                    'certificate':c}
    if rng is None: rng=random.SystemRandom()
    b=16/(epsilon*epsilon)
    batch=(b.numerator+b.denominator-1)//b.denominator
    bits=0
    D=1
    while D<1/failure: D*=2;bits+=1
    rounds=8*bits+1
    means=[]
    n=len(F)
    for _ in range(rounds):
        total=Q(0)
        for _ in range(batch):
            word=rng.getrandbits(n)
            signs=[1 if (word>>i)&1 else -1 for i in range(n)]
            x=sqrt_coefficients(skew(F,signs,alphas=c.get('phases')),k)[k]
            assert 3*c['baseline_norm']/4<=x<=4*c['baseline_norm']/3
            total+=x
        means.append(total/batch)
    means.sort()
    return {'status':'OK','estimate':means[rounds//2],'samples':batch*rounds,
            'random_bits':n*batch*rounds,'certificate':c}

def rational_rank(A):
    A=[list(row) for row in A]
    rows=len(A)
    cols=len(A[0]) if rows else 0
    p=0
    for j in range(cols):
        z=next((i for i in range(p,rows) if A[i][j]!=g.ZERO),None)
        if z is None: continue
        A[p],A[z]=A[z],A[p]
        a=A[p][j]
        A[p]=[g.div(x,a) for x in A[p]]
        for i in range(p+1,rows):
            a=A[i][j]
            A[i]=[g.add(x,g.neg(g.mul(a,y))) for x,y in zip(A[i],A[p])]
        p+=1
        if p==rows: break
    return p

def fixture(n,complex_tail=False):
    k=n//2
    t=Q(1,32*k*n) if not complex_tail else Q(1,128*k*n)
    F=[[g.qc(t/Q(i+j+1),t*Q((-1)**(i+j),7+i+2*j) if complex_tail else 0)
        for j in range(n)] for i in range(n)]
    for i in range(0,n,2):
        F[i][i+1]=g.add(F[i][i+1],g.ONE)
        F[i+1][i]=g.add(F[i+1][i],g.ONE)
    return F

def serialize(x):
    if isinstance(x,Q): return str(x)
    if isinstance(x,(list,tuple)): return [serialize(y) for y in x]
    if isinstance(x,dict): return {k:serialize(v) for k,v in x.items()}
    return x

def test():
    t0=time.monotonic()
    rows=[]
    words=coefficient_checks=mean_checks=0
    for n,complex_tail in ((4,False),(6,False),(4,True)):
        F=fixture(n,complex_tail)
        G,c=acquire(F,n//2)
        assert c['accepted']
        target=g.brute_counts(F)
        samples=[]
        for signs in product((-1,1),repeat=n):
            A=skew(F,signs)
            xs=sqrt_coefficients(A,n//2)
            assert xs==principal_pfaffian_coefficients(A)
            assert sqrt_coefficients(skew(G,signs),n//2)==c['baseline_counts']
            for k,x in enumerate(xs):
                assert 3*c['baseline_counts'][k]/4<=x<=4*c['baseline_counts'][k]/3
                coefficient_checks+=1
            samples.append(xs)
            words+=1
        means=[sum(x[k] for x in samples)/len(samples) for k in range(n//2+1)]
        assert means==target
        mean_checks+=len(target)
        ratios=[sum(x[k]*x[k] for x in samples)/len(samples)/(means[k]*means[k])
                for k in range(n//2+1)]
        assert all(r<=Q(256,81) for r in ratios)
        rows.append({'n':n,'complex_residual':complex_tail,'certificate':serialize(c),
                     'target_counts':[str(x) for x in target],
                     'relative_second_moments':[str(x) for x in ratios]})
    # Arbitrary complex strong matching entries, with rational-unit-grid phases.
    F=fixture(4,True)
    for j in range(2):
        F[2*j][2*j+1]=g.qc(1,Q(j+1,3))
        F[2*j+1][2*j]=g.qc(-2,Q(1,j+2))
    G,c=acquire_complex(F,2)
    assert c['accepted']
    target=g.brute_counts(F)
    samples=[]
    baseline_samples=[]
    for signs in product((-1,1),repeat=4):
        A=skew(F,signs,alphas=c['phases'])
        xs=sqrt_coefficients(A,2)
        assert xs==principal_pfaffian_coefficients(A)
        for k,x in enumerate(xs):
            assert 3*c['baseline_counts'][k]/4<=x<=4*c['baseline_counts'][k]/3
            coefficient_checks+=1
        samples.append(xs)
        baseline_samples.append(sqrt_coefficients(skew(G,signs,alphas=c['phases']),2))
        words+=1
    assert [sum(x[k] for x in samples)/16 for k in range(3)]==target
    assert [sum(x[k] for x in baseline_samples)/16 for k in range(3)]==c['baseline_counts']
    mean_checks+=3
    complex_case={'n':4,'certificate':serialize(c),'target_counts':[str(x) for x in target]}
    F_complex=[list(row) for row in F]
    target_complex=list(target)
    raw=[]
    for k in range(1,4):
        n=2*k
        F=[[g.ZERO for _ in range(n)] for _ in range(n)]
        for i in range(0,n,2):F[i][i+1]=F[i+1][i]=g.ONE
        xs=[sqrt_coefficients(skew(F,s,False),k)[k]
            for s in product((-1,1),repeat=n)]
        mu=sum(xs)/len(xs)
        ratio=sum(x*x for x in xs)/len(xs)/(mu*mu)
        assert mu==2**k and ratio==2**k
        raw.append({'k':k,'norm':str(mu),'relative_second_moment':str(ratio),
                    'phased_relative_second_moment':'1'})
    n=8
    F=fixture(n)
    G,c=acquire(F,4)
    assert c['accepted']
    cut=n//2
    cr=rational_rank([row[cut:] for row in F[:cut]])+rational_rank([row[:cut] for row in F[cut:]])
    assert cr==n and len(lr.factor(F)[1])==n and g.width(F,g.min_degree_order(F))==n-1
    smoke=approximate_count(fixture(4),2,Q(1),Q(1,2),random.Random(6190341))
    exact=g.brute_counts(fixture(4))[2]
    assert smoke['status']=='OK' and abs(smoke['estimate']-exact)<=exact
    complex_smoke=approximate_count(F_complex,2,Q(1),Q(1,2),random.Random(6190342),True)
    assert complex_smoke['status']=='OK' and abs(complex_smoke['estimate']-target_complex[2])<=target_complex[2]
    assert not acquire([[g.ONE for _ in range(4)] for _ in range(4)],2)[1]['accepted']
    out={'status':'PASS','exhausted_sign_words':words,
         'exact_coefficient_checks':coefficient_checks,'unbiased_sector_checks':mean_checks,
         'cases':rows,'complex_matching_case':complex_case,'raw_variance_fixtures':raw,
         'dense_structure':{'n':n,'rank_F':n,'support_width':n-1,'ordered_cut_rank_sum':cr,
                            'certificate':serialize(c)},
         'complete_FPRAS_smoke':{'status':smoke['status'],'samples':smoke['samples'],
                'random_bits':smoke['random_bits'],'estimate':str(smoke['estimate']),'target':str(exact)},
         'complex_FPRAS_smoke':{'status':complex_smoke['status'],'samples':complex_smoke['samples'],
                'random_bits':complex_smoke['random_bits'],'estimate':str(complex_smoke['estimate']),
                'target':str(target_complex[2])},
         'wall_seconds':time.monotonic()-t0,
         'scope':'Finite exact comparisons and two complete randomized count smoke calls; no generic confidence calibration or sampler.'}
    Path(__file__).with_name('phased_pfaffian_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('cases','dense_structure','complex_matching_case')},indent=2))

if __name__=='__main__':test()
