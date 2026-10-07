"""Exact rational sample primitives for weighted paired-volume estimation.

Extends the attributed c03_l10/c03_l06 Pfaffian norm estimator using complex
four-root phases, rational activation and an acquired complement contraction.
No algebraic activity square roots or coefficient enumeration in production.
"""
from low_rank_parity import G, Q, cast, inverse, uniform_below, determinant, rref
from math import isqrt, comb
import secrets


def matmul(A, B):
    if not A:
        return []
    cols = len(B[0]) if B else 0
    return [[sum((A[i][a]*B[a][j] for a in range(len(B))), G())
             for j in range(cols)] for i in range(len(A))]


def adjoint(A):
    return [[cast(A[i][j]).conj() for i in range(len(A))]
            for j in range(len(A[0]) if A else 0)]


def det_elimination(A):
    A = [[cast(v) for v in row] for row in A]
    n = len(A); out = G(1)
    for j in range(n):
        p = next((i for i in range(j,n) if A[i][j]), None)
        if p is None:
            return G()
        if p != j:
            A[j], A[p] = A[p], A[j]; out = -out
        v = A[j][j]; out *= v
        for i in range(j+1,n):
            if A[i][j]:
                f = A[i][j]/v
                for a in range(j+1,n):
                    A[i][a] -= f*A[j][a]
                A[i][j] = G()
    return out


def norm_coefficient(B, k):
    """[t^k] sqrt(det(I+t B^*B)); O(k d^3+k^2) exact field operations."""
    d = len(B)
    if k < 0 or 2*k > d:
        return Q(0)
    M = matmul(adjoint(B), B)
    P = [[G(int(i==j)) for j in range(d)] for i in range(d)]
    traces = [Q(0)]
    for _ in range(k):
        P = matmul(P, M)
        v = sum((P[i][i] for i in range(d)), G())
        assert not v.im
        traces.append(v.re)
    coeff = [Q(1)]; root = [Q(1)]
    for r in range(1,k+1):
        coeff.append(sum(((-1)**(j-1)*coeff[r-j]*traces[j]
                          for j in range(1,r+1)), Q(0))/r)
        root.append((coeff[r]-sum((root[j]*root[r-j]
                                  for j in range(1,r)), Q(0)))/2)
        assert root[-1] >= 0
    return root[k]


def validate(U,V,activities):
    m = len(U); d = len(U[0]) if m else 0
    if len(V)!=m or any(len(v)!=d for v in U+V):
        raise ValueError('bad vector dimensions')
    U = [[cast(v) for v in u] for u in U]
    V = [[cast(v) for v in u] for u in V]
    lam = [Q(1)]*m if activities is None else [Q(v) for v in activities]
    if len(lam)!=m or any(v<0 for v in lam):
        raise ValueError('bad activities')
    keep = [i for i in range(m) if lam[i]]
    return [U[i] for i in keep], [V[i] for i in keep], [lam[i] for i in keep], d


def activated_phase(variance, randbits=secrets.randbits):
    """Mean zero, E|eta|^2=variance, E|eta|^4<=2variance^2, rational eta.
    Exact square activities use unit-magnitude phases without activation.
    """
    variance = Q(variance)
    if variance <= 0:
        raise ValueError('positive variance required')
    a,b = variance.numerator,variance.denominator
    sa,sb = isqrt(a),isqrt(b)
    if sa*sa==a and sb*sb==b:
        radius = Q(sa,sb)
    else:
        t = isqrt(16*a*b)
        if t*t<16*a*b:
            t += 1
        radius = Q(t,4*b)
    probability = variance/(radius*radius)
    assert Q(16,25) <= probability <= 1
    if probability != 1 and uniform_below(probability.denominator,randbits) >= probability.numerator:
        return G()
    phase = [G(1),G(-1),G(0,1),G(0,-1)][randbits(2)]
    return phase*radius


def skew_sum(U,V,z,d):
    B = [[G() for _ in range(d)] for _ in range(d)]
    for u,v,a in zip(U,V,z):
        if a:
            for i in range(d):
                for j in range(i+1,d):
                    term = a*(u[i]*v[j]-v[i]*u[j])
                    B[i][j] += term; B[j][i] -= term
    return B


def forced_projection(U,V,indices,d):
    """Known Gram mass and rational projected remaining vector pairs."""
    columns = [vec for i in indices for vec in (U[i],V[i])]
    if not columns:
        return Q(1),U,V
    C = [[vec[a] for vec in columns] for a in range(d)]
    Cstar = adjoint(C); Gram = matmul(Cstar,C)
    mass = det_elimination(Gram)
    assert not mass.im and mass.re >= 0
    if not mass:
        return Q(0),U,V
    H = matmul(matmul(C,inverse(Gram)),Cstar)
    P = [[G(int(i==j))-H[i][j] for j in range(d)] for i in range(d)]
    def project(v):
        return [sum((P[i][j]*v[j] for j in range(d)),G()) for i in range(d)]
    return mass.re,[project(u) for u in U],[project(v) for v in V]


def evaluate_direct(U,V,k,z,d):
    return norm_coefficient(skew_sum(U,V,z,d),k)


def evaluate_complement(U,V,k,z,activities,d):
    """Nonnegative reciprocal contraction, including exactly zero phases."""
    forced = [i for i,a in enumerate(z) if not a]
    if len(forced)>k:
        return Q(0)
    mass,PU,PV = forced_projection(U,V,forced,d)
    if not mass:
        return Q(0)
    scalar = Q(1)
    for weight in activities:
        scalar *= weight
    reciprocals = []
    for a in z:
        if a:
            scalar *= a.norm(); reciprocals.append(G(1)/a)
        else:
            reciprocals.append(G())
    return scalar*mass*norm_coefficient(skew_sum(PU,PV,reciprocals,d),k-len(forced))


def sample_value(U,V,k,activities=None,randbits=secrets.randbits,mode='auto'):
    """One exact rational unbiased sample of weighted Z_k.

    Variance <=binom(2r,r)Z^2 with r=min(k,m-k) in auto mode. The sharper
    24/5 second-moment constant holds for r=2. This returns one value,
    not a normalizer estimate or a Born sample.
    """
    U,V,lam,d = validate(U,V,activities);m = len(U)
    if not isinstance(k,int) or k<0:
        raise ValueError('invalid pair number')
    if k>m or 2*k>d:
        return Q(0),{'mode':'zero','effective_degree':0,'positive_labels':m}
    _,pivots = rref(U+V)
    if 2*k>len(pivots):
        return Q(0),{'mode':'zero-rank','effective_degree':0,'positive_labels':m,'pair_span_rank':len(pivots)}
    chosen = ('direct' if k<=m-k else 'complement') if mode=='auto' else mode
    if chosen=='direct':
        z = [activated_phase(w,randbits) for w in lam]
        return evaluate_direct(U,V,k,z,d),{'mode':chosen,'effective_degree':k,'positive_labels':m}
    if chosen=='complement':
        z = [activated_phase(1/w,randbits) for w in lam]
        return evaluate_complement(U,V,k,z,lam,d),{'mode':chosen,'effective_degree':m-k,'positive_labels':m,'forced_zero_labels':sum(not a for a in z)}
    raise ValueError('invalid estimator mode')


def ceil_fraction(q):
    q=Q(q)
    return (q.numerator+q.denominator-1)//q.denominator


def ceil_log2(q):
    q=Q(q);t=max(0,q.numerator.bit_length()-q.denominator.bit_length())
    while Q(1<<t)<q:t+=1
    return t


def approximate(U,V,k,activities=None,epsilon=Q(1,4),delta=Q(1,4),randbits=secrets.randbits):
    """Capped median-of-means FPRAS for weighted Z_k at low min(k,m-k).

    All returned estimates are rational. Abort from the random-bit cap returns
    zero, charged to confidence failure. Zero output on a positive instance
    is not an exact zero certificate. No Born sampler is implemented here.
    """
    U,V,lam,d=validate(U,V,activities);m=len(U)
    epsilon,delta=Q(epsilon),Q(delta)
    if not Q(0)<epsilon<=Q(1,2) or not Q(0)<delta<Q(1):
        raise ValueError('bad approximation parameters')
    if not isinstance(k,int) or k<0:raise ValueError('invalid pair number')
    if k==0:return Q(1),{'samples':0,'status':'EXACT_VACUUM'}
    _,pivots=rref(U+V)
    if k>m or 2*k>len(pivots):return Q(0),{'samples':0,'status':'EXACT_ZERO_RANK'}
    if k==m:
        columns=[v for i in range(m) for v in (U[i],V[i])]
        matrix=[[v[a] for v in columns] for a in range(d)]
        value=det_elimination(matmul(adjoint(matrix),matrix))
        assert not value.im and value.re>=0
        scalar=Q(1)
        for a in lam:scalar*=a
        return scalar*value.re,{'samples':0,'status':'EXACT_COMPLETE_VOLUME'}
    r=min(k,m-k);C=Q(24,5) if r==2 else Q(comb(2*r,r))
    batch=ceil_fraction(4*C/(epsilon*epsilon))
    repeats=8*(ceil_log2(4/delta)+1)+1
    total=batch*repeats
    attempt_cap=ceil_log2(4*max(1,m*total)/delta)+1
    call_cap=max(1,m*total)*(attempt_cap+1)
    calls=0;max_width=0
    class Abort(Exception):pass
    def capped(bits):
        nonlocal calls,max_width
        calls+=1;max_width=max(max_width,bits)
        if calls>call_cap:raise Abort()
        return randbits(bits)
    means=[]
    try:
        for _ in range(repeats):
            values=[sample_value(U,V,k,lam,capped)[0] for _ in range(batch)]
            means.append(sum(values,Q(0))/batch)
    except Abort:
        return Q(0),{'status':'RANDOM_BIT_CAP_ABORT','calls':calls,'call_cap':call_cap,'max_width':max_width}
    return sorted(means)[repeats//2],{'status':'CAPPED_MEDIAN_MEANS','samples':total,'batch':batch,
                                    'repeats':repeats,'effective_degree':r,'second_moment_bound':str(C),
                                    'calls':calls,'call_cap':call_cap,'max_width':max_width}
