"""All-order scalar response by an acquired signed observable dual.

Physical model: independent uniform equilibrium spins, local reversible flips
  w_i(s)=nu_i*(1 + 9/20 s_(i-2)s_(i+2) - 3/20 s_(i-1)s_(i+1)).
Even sites have clock 1/B, odd sites clock 1. Source is the normalized sum of
all even-site spins. The method sums EVERY perturbative order by a signed dual
walk; it never samples a physical time trajectory or enumerates global states.

The Fourier absolute-row contraction q=3/5 is acquired from the rate table.
All large-system walk decisions use integer probabilities, including 1/B clocks.
The normalized output is exactly 1+(9/10)*mean(score), score in {-1,0,1}.
N=64800 samples gives absolute normalized error <=0.01 with failure <=2exp(-4)
by Hoeffding; Jensen gives response/reference >=1, hence also relative error.
The RNG is a deterministic pseudorandom implementation of the mathematical IID
random-bit algorithm. Small sparse solves below are floating-point checks.
"""
import json, math, random, time
from pathlib import Path
from collections import Counter
from fractions import Fraction


def sample_order(rng):
    # P(J=j)=(2/5)(3/5)^(j-2), j>=2. Exactly integer choices.
    j=2
    while rng.randrange(5)<3:
        j+=1
    return j


def pivot(support, B, rng):
    # Integer-clock weights: odd sites B, even sites 1.
    sites=sorted(support)
    total=sum(B if x%2 else 1 for x in sites)
    u=rng.randrange(total)
    for x in sites:
        w=B if x%2 else 1
        if u<w:
            return x
        u-=w
    raise AssertionError('unreachable')


def one_score(n,B,rng):
    support={2*rng.randrange(n//2)}
    sign=1
    order=sample_order(rng)
    maximum=1
    for _ in range(order):
        i=pivot(support,B,rng)
        # The l1-normalized rates choose the first pair with probability 3/4.
        if rng.randrange(4)<3:
            a,b=(i-2)%n,(i+2)%n
            sign=-sign # - sign(9/20)
        else:
            a,b=(i-1)%n,(i+1)%n
            # - sign(-3/20) = +1
        support.symmetric_difference_update((a,b))
        maximum=max(maximum,len(support))
    if len(support)!=1 or next(iter(support))%2:
        return 0,order,maximum
    return sign,order,maximum


def run_walk(n,B,nsamples=64800,seed=20261101):
    assert n>=8 and n%2==0 and B>=1
    rng=random.Random(seed)
    begin=time.perf_counter()
    counts=Counter(); total_order=0; max_order=0; max_support=0
    for _ in range(nsamples):
        score,order,support=one_score(n,B,rng)
        counts[score]+=1; total_order+=order
        max_order=max(max_order,order);max_support=max(max_support,support)
    integer_sum=counts[1]-counts[-1]
    ratio_exact=1+Fraction(9*integer_sum,10*nsamples)
    ratio=float(ratio_exact)
    # log(40)<4. Compute a rational upward square-root bound with integers.
    scale=10**12
    square_num=648*scale**2; square_den=100*nsamples
    integer_root=math.isqrt(square_num//square_den)
    if integer_root**2*square_den<square_num:integer_root+=1
    radius_exact=Fraction(integer_root,scale)
    radius=float(radius_exact)
    return dict(n=n,clock_ratio=str(B),samples=nsamples,seed=seed,
        score_counts={str(k):counts[k] for k in (-1,0,1)},integer_score_sum=integer_sum,
        normalized_response=ratio,normalized_response_exact=str(ratio_exact),
        confidence_radius=radius,confidence_radius_exact=str(radius_exact),
        confidence_interval=[ratio-radius,ratio+radius],
        confidence_interval_exact=[str(ratio_exact-radius_exact),str(ratio_exact+radius_exact)],
        failure_bound='2*exp(-4) < 0.05',
        reference_response=f'{B}/2',
        response='normalized_response times reference_response',
        average_order=total_order/nsamples,total_steps=total_order,
        max_order=max_order,max_support=max_support,
        seconds=time.perf_counter()-begin)


def exact_sparse(n,B):
    """Independent full observable-space solve, small n only.

    Builds the entire physical generator in its orthonormal Walsh basis, then
    symmetrically preconditions it. This has exponential state cost and is used
    only to check the all-order signed-dual value. The residual gives a formal
    solve-error bound for the assembled floating matrix; it is not interval data.
    """
    import numpy as np
    from scipy.sparse import coo_matrix
    from scipy.sparse.linalg import cg
    assert 8<=n<=14
    dim=(1<<n)-1
    nu=np.array([1/B if i%2==0 else 1. for i in range(n)])
    d=np.array([2*sum(nu[i] for i in range(n) if s>>i&1) for s in range(1,1<<n)])
    rows=list(range(dim));cols=list(range(dim));vals=[1.]*dim
    for s in range(1,1<<n):
        for i in range(n):
            if not (s>>i&1):continue
            for jump,a in [(2,.45),(1,-.15)]:
                t=s^(1<<((i-jump)%n))^(1<<((i+jump)%n))
                assert t>0
                rows.append(s-1);cols.append(t-1)
                vals.append(2*nu[i]*a/math.sqrt(d[s-1]*d[t-1]))
    matrix=coo_matrix((vals,(rows,cols)),shape=(dim,dim)).tocsr()
    g=np.zeros(dim)
    for i in range(0,n,2):g[(1<<i)-1]=1/math.sqrt(n//2)
    x,info=cg(matrix,g,rtol=1e-13,atol=0.,maxiter=200)
    assert info==0
    residual=g-matrix@x
    lower=float(2*g@x-x@(matrix@x))
    width=float(residual@residual/.4)
    return dict(n=n,clock_ratio=str(B),walsh_states=dim,
        normalized_response=float(g@x),variational_lower=lower,
        residual_bound_width=width,max_symmetry_error=float(abs(matrix-matrix.T).max()),
        qualification='Floating sparse matrix; residual enclosure is for assembled matrix only.')


if __name__=='__main__':
    out={'model':'uniform Gibbs law; extensive two-spectator nonlinear rate factors',
         'contrast':[.4,1.6], 'absolute_row_contraction':.6,
         'source':'normalized sum of all even-site spins',
         'all_orders_included':True,
         'walks':[], 'small_checks':[]}
    for n in [8,12]:
        for B in [1,10**40]:
            exact=exact_sparse(n,B)
            walk=run_walk(n,B,seed=20261101+n+(B!=1))
            walk['small_exact']=exact['normalized_response']
            walk['exact_inside_reported_interval']=walk['confidence_interval'][0]<=exact['normalized_response']<=walk['confidence_interval'][1]
            out['small_checks'].append(exact);out['walks'].append(walk)
    for n in [64,256,4096]:
        out['walks'].append(run_walk(n,10**40,seed=20261101+n))
    path=Path(__file__).with_name('signed_dual_results.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
