"""Astra chemistry: bond-qualified fragment fusion, exact stochastic bounds.

SCOPED MODEL. No experimental implementation or novelty certification.
Run: python3 /mnt/data/astra_chemistry_certified_fusion.py

1. Independently-clocked intended reactions with permanently wrong crosslinks.
   Exact Laplace-transform identity and Jensen lower bounds.
2. Hierarchical covalent-junction selection: rejected joins irreversibly consume
   both submitted fragments, so every rejection triggers their reconstruction.
3. Optimal binary contiguous assembly tree by dynamic programming.
"""
from math import exp, log, log2, isclose, expm1
from functools import lru_cache
from random import Random


def exact_small(a, h, w):
    """Bellman recursion; w[i][j] is ordered-pair wrong hazard."""
    n=len(a)
    @lru_cache(None)
    def F(mask):
        if not mask: return 1.
        ids=[i for i in range(n) if mask >> i & 1]
        den=sum(a[i]+h[i] for i in ids) + sum(w[i][j] for i in ids for j in ids if i != j)
        return sum(a[i] * F(mask ^ (1 << i)) for i in ids) / den
    return F((1<<n)-1)


def jensen_lower(a, h, w):
    """Sharp first-cumulant lower bound for heterogeneous edge chemistry."""
    n=len(a)
    return exp(-sum(h[i]/a[i] for i in range(n))
               -sum(w[i][j]/(a[i]+a[j]) for i in range(n) for j in range(n) if i!=j))


def laplace_mc(a, h, w, draws=150000, seed=1387):
    rng=Random(seed)
    acc=0.
    n=len(a)
    for _ in range(draws):
        T=[rng.expovariate(rate) for rate in a]
        X=sum(h[i]*T[i] for i in range(n))
        X+=sum(w[i][j]*min(T[i],T[j]) for i in range(n) for j in range(n) if i!=j)
        acc+=exp(-X)
    return acc/draws



def jensen_deadline_lower(a, h, w, deadline):
    """Rigorous finite-deadline bound via conditional truncated exponential clocks.

    Probability all correct by deadline, no failures. Conditional on all
    target clocks <= deadline, apply Jensen to integrated killing hazards.
    """
    n=len(a); T=deadline
    assert T>0 and len(h)==n and len(w)==n
    p=[-expm1(-a[i]*T) for i in range(n)]
    mu=[1/a[i]-T/expm1(a[i]*T) for i in range(n)]
    def trunc_min(i,j):
        A,B=a[i],a[j]
        ea,eb=exp(-A*T),exp(-B*T)
        num=(-expm1(-(A+B)*T))/(A+B) - eb*p[i]/A - ea*p[j]/B + T*ea*eb
        return num/(p[i]*p[j])
    X=sum(h[i]*mu[i] for i in range(n))
    X+=sum(w[i][j]*trunc_min(i,j) for i in range(n) for j in range(n) if i!=j)
    return exp(sum(log(x) for x in p)-X)


def laplace_deadline_mc(a, h, w, deadline, draws=150000, seed=1248):
    rng=Random(seed)
    n=len(a);acc=0
    for _ in range(draws):
        Ti=[rng.expovariate(rate) for rate in a]
        if max(Ti)>deadline:continue
        X=sum(h[i]*Ti[i] for i in range(n))
        X+=sum(w[i][j]*min(Ti[i],Ti[j]) for i in range(n) for j in range(n) if i!=j)
        acc+=exp(-X)
    return acc/draws


def homogeneous_spatial_jensen(E, a, h, b, r):
    """w_ij=b*r**(|i-j|-1), i!=j."""
    s=sum((E-d)*r**(d-1) for d in range(1,E))
    return exp(-E*h/a-b*s/a)


def balanced_cost(L, success, leaf=1., join_cost=0.):
    assert L>=1 and (L&(L-1))==0 and 0<success<=1
    C=leaf
    for _ in range(L.bit_length()-1): C=(2*C+join_cost)/success
    return C


def serial_cost(L, success, leaf=1., join_cost=0.):
    """Failures destroy entire grown fragment; build one new leaf per step."""
    C=leaf
    for _ in range(L-1): C=(C+leaf+join_cost)/success
    return C


def fusion_fidelity(L, correct_accept, false_accept):
    """Conditional on a completely accepted binary product under IID joins."""
    s=correct_accept+false_accept
    assert correct_accept>0 and 0<s<=1
    return (correct_accept/s)**(L-1)


def max_false_accept(L, correct_accept, target_fidelity):
    """Largest false-acceptance probability per attempt for target fidelity."""
    return correct_accept*(target_fidelity**(-1/(L-1))-1)


def optimal_ordered_tree(success_by_boundary, leaf_cost=None, join_cost_by_boundary=None):
    """DP for minimum expected consumed resource, including all failed joins.

    Leaves are unique ordered fragments; each junction i|i+1 has independent
    acceptance probability success_by_boundary[i], uniform across fragment sizes.
    A rejection consumes both children irreversibly. Join costs are charged on
    each attempt. All fragment sizes permitted and left/right order preserved.
    """
    N=len(success_by_boundary)+1
    if leaf_cost is None: leaf_cost=[1.]*N
    if join_cost_by_boundary is None: join_cost_by_boundary=[0.]*(N-1)
    assert len(leaf_cost)==N and len(join_cost_by_boundary)==N-1
    assert all(0<s<=1 for s in success_by_boundary)
    dp=[[0.]*N for _ in range(N)]
    split=[[None]*N for _ in range(N)]
    for i in range(N): dp[i][i]=leaf_cost[i]
    for width in range(2,N+1):
        for i in range(N-width+1):
            j=i+width-1
            vals=[((dp[i][k]+dp[k+1][j]+join_cost_by_boundary[k]) / success_by_boundary[k], k)
                  for k in range(i,j)]
            dp[i][j],split[i][j]=min(vals)
    return dp[0][N-1],split


def cost_fixed_tree(success_by_boundary, pattern='balanced', leaf_cost=1., join_cost=0.):
    n=len(success_by_boundary)+1
    def rec(i,j):
        if i==j:return leaf_cost
        k = (i+j)//2 if pattern=='balanced' else j-1
        return (rec(i,k)+rec(k+1,j)+join_cost) / success_by_boundary[k]
    return rec(0,n-1)


def size_dependent_cost(L, baseline_success, steric_per_monomer, leaf=1.):
    """Balanced L=2^k; q(size)=q0*exp(-steric_per_monomer*size)."""
    assert (L&(L-1))==0 and 0<baseline_success<=1
    C=leaf
    n=2
    while n<=L:
        C=(2*C)/(baseline_success*exp(-steric_per_monomer*n))
        n*=2
    return C


def enumerate_all_trees(s, leaf_cost=None):
    """Independent explicit Catalan enumeration for small n."""
    n=len(s)+1
    if leaf_cost is None: leaf_cost=[1.]*n
    @lru_cache(None)
    def C(i,j):
        if i==j: return [leaf_cost[i]]
        out=[]
        for k in range(i,j):
            for A in C(i,k):
                for B in C(k+1,j):
                    out.append((A+B)/s[k])
        return out
    return C(0,n-1)


def tests():
    rng=Random(280)
    for n in (3,5,7):
        for k in range(4):
            a=[rng.uniform(.04,.15) for _ in range(n)]
            h=[rng.uniform(1e-4,2e-3) for _ in range(n)]
            w=[[rng.uniform(1e-5,1e-3) if i!=j else 0 for j in range(n)] for i in range(n)]
            val=exact_small(a,h,w)
            lb=jensen_lower(a,h,w)
            assert 0<lb<=val+1e-13 <=1+1e-13,(n,lb,val)
    for n in range(2,9):
        s=[rng.uniform(.35,.99) for _ in range(n-1)]
        dp,_=optimal_ordered_tree(s)
        brute=min(enumerate_all_trees(s))
        assert isclose(dp,brute,rel_tol=2e-14),(n,dp,brute)
    for L in (2,4,8,32,64):
        for q in (.5,.8,.95):
            dp,_=optimal_ordered_tree([q]*(L-1))
            bal=balanced_cost(L,q)
            assert isclose(dp,bal,rel_tol=1e-12), (L,q,dp,bal)
    for L in (2,4,8,1024):
        q=.9; k=.005
        exact=size_dependent_cost(L,q,k)
        closed=L*q**(-log2(L))*exp(2*k*(L-1))
        assert isclose(exact,closed,rel_tol=1e-12)
    return True


def demo():
    assert tests()
    print('INDEPENDENT_SMALL_GRAPH_JENSEN_DP_CATALAN_TESTS PASS')
    E=999; a=.05;h=5e-7;b=1e-7; r=.25
    print('SPATIAL_JENSEN_LOWER',homogeneous_spatial_jensen(E,a,h,b,r))
    from astra_chemistry_distributed_edge_assembly import p_local_lower, p_no_cross
    print('PREVIOUS_SPATIAL_LOWER',p_local_lower(E,a,h,b,r))
    print('SPATIAL_NO_CROSSLINK_UPPER',p_no_cross(E,a,h))
    a_vec=[.047,.053,.081,.067,.036]
    h_vec=[.00013,.00027,.0001,.0002,.0003]
    w=[[.00034 if i!=j else 0 for j in range(5)] for i in range(5)]
    print('HETEROGENEOUS_EXACT',exact_small(a_vec,h_vec,w))
    print('HETEROGENEOUS_JENSEN_LOWER',jensen_lower(a_vec,h_vec,w))
    print('HETEROGENEOUS_INDEPENDENT_MC',laplace_mc(a_vec,h_vec,w))
    print('FINITE_DEADLINE_50S_JENSEN_LOWER',jensen_deadline_lower(a_vec,h_vec,w,50.))
    print('FINITE_DEADLINE_50S_MC',laplace_deadline_mc(a_vec,h_vec,w,50.))
    L=1024;p=.9;f=1e-5; s=p+f
    print('HIERARCHICAL_1024_COST_LEAF_EQUIV',balanced_cost(L,s))
    print('HIERARCHICAL_1024_CONDITIONAL_PURITY',fusion_fidelity(L,p,f))
    print('MAX_FALSE_ACCEPT_95PCT',max_false_accept(L,p,.95))
    print('UNIFORM_SUCCESS_EXPONENT',log2(2/s))
    print('SERIAL_LOG10_COST',log(serial_cost(1024,s))/log(10))
    for k in (.0001,.001,.005,.01):
        penalty=size_dependent_cost(L,s,k)/balanced_cost(L,s)
        print('STERICS_EXP_PER_MONOMER',k,'COST_RATIO',penalty)
    n=32;s=[.95]*(n-1);s[15]=.35
    qopt,splits=optimal_ordered_tree(s,join_cost_by_boundary=[.25]*(n-1))
    print('HETEROGENEOUS_32_BALANCED_COST',cost_fixed_tree(s,'balanced',join_cost=.25))
    print('HETEROGENEOUS_32_OPT_COST',qopt)
    print('HETEROGENEOUS_32_OPT_ROOT_BOUNDARY',splits[0][n-1]+1)
    print('HETEROGENEOUS_32_BALANCED_ROOT_BOUNDARY',16)

if __name__=='__main__':demo()
