"""Costed hard-BCS approximation admission with an exact frontier backend.

The Schur augmentation overlaps c03_l05 INITIAL (read before implementing).
This owned implementation adds forced-double auxiliary contraction, exact
greedy rational column acquisition, and a projected-norm error certificate.
No peer code is imported, executed or changed.
"""
import sys
from pathlib import Path
from math import comb
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from representation_compiler import C,Q,matrix,inverse,strip_diagonal
from banded_hard_bcs import pair_gate,add,local_masks,capped_rational_bit
from frontier_hard_bcs import recognize_frontier,insert_vacuum,compile_admission
from frontier_hard_bcs import prefix_count as full_frontier_count
from frontier_hard_bcs import sample_born as full_frontier_sample

def product(a,b):
    if not a:return []
    ncols=len(b[0]) if b else 0
    return [[sum((a[i][t]*b[t][j] for t in range(len(b))),C(0))
             for j in range(ncols)] for i in range(len(a))]

def adjoint(a):
    return [[a[i][j].conjugate() for i in range(len(a))] for j in range(len(a[0]) if a else 0)]

def frobenius2(a):return sum((x.abs2() for row in a for x in row),Q(0))

def subtract(a,b):return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]

def rational_rank_approximation(residual,rank_budget):
    """Greedily acquire independent columns and exact least-squares coefficients.

    This is certificate admission, not optimal numerical-rank recognition.
    If the exact residual rank is <= rank_budget, recovery is exact.
    """
    a=matrix(residual);n=len(a)
    if any(len(row)!=n for row in a) or not 0<=rank_budget<=n:
        raise ValueError('square residual and rank budget in [0,n] required')
    selected=[];error=a;u=[[] for _ in range(n)];v=[[] for _ in range(n)]
    approximation=[[C(0) for _ in range(n)] for _ in range(n)]
    for _ in range(rank_budget):
        norms=[sum((error[i][j].abs2() for i in range(n)),Q(0)) for j in range(n)]
        if not any(norms):break
        col=max(range(n),key=lambda j:(norms[j],-j));selected.append(col)
        u=[[a[i][j] for j in selected] for i in range(n)]
        ua=adjoint(u);gram=product(ua,u)
        coefficients=product(product(inverse(gram),ua),a)
        approximation=product(u,coefficients)
        error=subtract(a,approximation)
        v=[[coefficients[t][j] for t in range(len(selected))] for j in range(n)]
    return {'U':u,'V':v,'rank':len(selected),'selected_columns':selected,
            'approximation':approximation,'residual':error,
            'frobenius_residual_squared':frobenius2(error),
            'scope':'exact rational greedy acquisition; not best-rank approximation'}

def augmented_matrix(base,u,v):
    base=matrix(base);u=matrix(u);v=matrix(v);n=len(base)
    r=len(u[0]) if n else 0
    if len(u)!=n or len(v)!=n or any(len(row)!=r for row in u+v):
        raise ValueError('factor shape mismatch')
    return [base[i]+u[i] for i in range(n)]+[
        [-v[j][a] for j in range(n)]+[C(a==b) for b in range(r)]
        for a in range(r)]

def count_rank_update(base,u,v,mode_constraints=None,site_constraints=None,
                      physical_order=None,frontier_cap=None,collect_stats=False):
    """Exact all-sector/prefix contraction with every auxiliary site doubled."""
    base=matrix(base);n=len(base);r=len(u[0]) if n else 0
    base_cert=recognize_frontier(base,physical_order)
    order=base_cert['order']+list(range(n,n+r))
    ext=augmented_matrix(base,u,v)
    cert=recognize_frontier(ext,order,frontier_cap)
    if cert['status']!='ACCEPTED':raise ValueError(cert)
    assert cert['width']<=base_cert['width']+r
    pos={site:i for i,site in enumerate(order)}
    ff=[[ext[i][j] for j in order] for i in order]
    graph=[{pos[j] for j in cert['graph'][site]} for site in order]
    physical_allowed=local_masks(n,mode_constraints,site_constraints)
    allowed=[physical_allowed[site] if site<n else {3} for site in order]
    rho={(0,0,0):C(1)};live=[];peak=1;live_peak=0;gates=0
    for i,original_site in enumerate(order):
        needed={i}|{j for j in graph[i] if j>i}
        for j in sorted(needed-set(live)):
            at=sum(vv<j for vv in live)
            rho=insert_vacuum(rho,at);live.insert(at,j)
        assert live[0]==i
        live_peak=max(live_peak,len(live))
        for j in sorted(graph[i]):
            if j<=i:continue
            p=live.index(j)
            for coefficient,left,right in ((ff[i][j],0,2*p+1),(ff[j][i],2*p,1)):
                if coefficient:
                    rho=pair_gate(rho,coefficient,left,right);gates+=1
                    peak=max(peak,len(rho))
        # Physical diagonal creation is killed by the hard local filter.
        # Auxiliary diagonal creation MUST be retained for the identity pivot.
        if original_site>=n and ff[i][i]:
            rho=pair_gate(rho,ff[i][i],0,1);gates+=1
            peak=max(peak,len(rho))
        out={}
        for (a,b,q),weight in rho.items():
            occupation=a&3
            if occupation==(b&3) and occupation in allowed[i]:
                increment=occupation.bit_count() if original_site<n else 0
                add(out,(a>>2,b>>2,q+increment),weight)
        rho=out;live.pop(0);peak=max(peak,len(rho))
        assert set(order[j] for j in live)==set(cert['boundaries'][i])
    polynomial=[Q(0)]*(n+1)
    for (a,b,q),weight in rho.items():
        assert a==b==0 and weight.im==0 and weight.re>=0
        polynomial[q]+=weight.re
    assert all(not polynomial[q] for q in range(1,n+1,2))
    result={'coefficients':[polynomial[2*k] for k in range(n//2+1)],
            'base_width':base_cert['width'],'auxiliary_rank':r,
            'extended_width':cert['width'],'order':base_cert['order']}
    if collect_stats:result['stats']={'peak_density_coefficients':peak,
        'maximum_live_sites':live_peak,'pair_creation_gates':gates}
    return result

def acquire_certificate(f,base,rank_budget,k,epsilon=Q(1,100),
                        order=None,separator_budget=3,frontier_cap=None):
    """Return CERTIFIED or UNKNOWN_ADMISSION; failure says nothing about FPRAS.

    Base is an explicit charged matrix (or an explicitly costed finite guess).
    U,V and residual are acquired from F-base. No singular-value oracle is used.
    """
    f=matrix(f);base=matrix(base);n=len(f);epsilon=Q(epsilon)
    if len(base)!=n or any(len(row)!=n for row in f+base):raise ValueError('shape mismatch')
    if not 0<=k<=n//2 or not 0<epsilon<=1:raise ValueError('sector/error range')
    if order is None:
        admission=compile_admission(base,separator_budget)
        if admission['status']!='ACCEPTED':
            return {'status':'UNKNOWN_ADMISSION','reason':'base frontier search failed','admission':admission}
        order=admission['order']
    else:admission=recognize_frontier(base,order)
    factors=rational_rank_approximation(subtract(f,base),rank_budget)
    u,v=factors['U'],factors['V']
    h=[[base[i][j]+factors['approximation'][i][j] for j in range(n)] for i in range(n)]
    error=strip_diagonal(subtract(f,h))
    eta2=frobenius2(error)
    f0,h0=strip_diagonal(f),strip_diagonal(h)
    bound=max(sum((abs(x.re)+abs(x.im) for row in a for x in row),Q(0)) for a in (f0,h0))
    delta2=Q(0) if k==0 else comb(n,k)*k*k*eta2*bound**(2*k-2)
    if frontier_cap is not None:
        ext=augmented_matrix(base,u,v)
        ext_cert=recognize_frontier(ext,list(order)+list(range(n,n+factors['rank'])),frontier_cap)
        if ext_cert['status']!='ACCEPTED':
            return {'status':'UNKNOWN_ADMISSION','reason':'charged frontier cap exceeded',
                    'candidate_rank':factors['rank'],'extended_frontier':ext_cert['width']}
    counts=count_rank_update(base,u,v,physical_order=order,
        frontier_cap=frontier_cap,collect_stats=True)
    z=counts['coefficients'][k]
    accepted=bool(z) and delta2<=epsilon*epsilon*z/16
    return {'status':'CERTIFIED' if accepted else 'UNKNOWN_ADMISSION',
            'reason':'projected residual bound passed' if accepted else 'zero approximate sector or residual guard failed',
            'n':n,'k':k,'epsilon':epsilon,'F':f,'base':base,'U':u,'V':v,'H':h,
            'rank':factors['rank'],'selected_columns':factors['selected_columns'],
            'eta_squared':eta2,'operator_norm_upper_bound':bound,
            'amplitude_error_squared_bound':delta2,'norm_estimate':z,
            'guard_right_hand_side':epsilon*epsilon*z/16,'counts':counts,
            'base_admission':admission,'order':list(order),
            'guarantee':'relative norm error <= epsilon; pure-state trace distance <= epsilon/4'}

def acquire_banded_certificate(f,bandwidth,rank_budget,k,epsilon=Q(1,100),frontier_cap=None):
    """F-only deterministic admission: keep the specified band, then acquire rank."""
    f=matrix(f);n=len(f)
    if bandwidth<0:raise ValueError('negative bandwidth')
    base=[[f[i][j] if abs(i-j)<=bandwidth else C(0) for j in range(n)] for i in range(n)]
    return acquire_certificate(f,base,rank_budget,k,epsilon,order=list(range(n)),frontier_cap=frontier_cap)

def sample_certified(certificate,getrandbits):
    """Fair-bit capped sampler; whole-law TV <= 3 epsilon/4 on certification."""
    if certificate['status']!='CERTIFIED':return {'status':'UNKNOWN_ADMISSION'}
    n,k=certificate['n'],certificate['k'];eps=certificate['epsilon']
    attempts=0
    while Q(2*n,1<<attempts)>eps/2:attempts+=1
    prefix={};fallback=False;coin_bits=0;queries=0
    def count(p):
        nonlocal queries
        queries+=1
        return count_rank_update(certificate['base'],certificate['U'],certificate['V'],
             mode_constraints=p,physical_order=certificate['order'])['coefficients'][k]
    for site,spin in [(i,'U') for i in range(n)]+[(i,'D') for i in range(n)]:
        p0=dict(prefix);p0[site,spin]=0;p1=dict(prefix);p1[site,spin]=1
        z0,z1=count(p0),count(p1);assert z0+z1>0
        if fallback:bit=int(bool(z1))
        else:
            bit,used=capped_rational_bit(z1/(z0+z1),getrandbits,attempts);coin_bits+=used
            if bit is None:fallback=True;bit=int(bool(z1))
        prefix[site,spin]=bit
    up=[i for i in range(n) if prefix[i,'U']];down=[i for i in range(n) if prefix[i,'D']]
    assert len(up)==len(down)==k and not set(up)&set(down)
    return {'status':'SAMPLE','up':up,'down':down,'fallback':fallback,
        'coin_bits':coin_bits,'count_queries':queries,'norm_estimate':certificate['norm_estimate'],
        'TV_bound':3*eps/4,'randomness_contract':'independent fair random bits'}

def acquire_uniform_accuracy_certificate(f,base,rank_budget,k,order=None,
        separator_budget=3,frontier_cap=None):
    """Recognize a matrix class supporting EVERY requested accuracy.

    Exponentially small certified relative residual permits a fine-accuracy
    exact fallback: on that branch 16^n < epsilon^-8. Width/rank admission
    remains charged separately. This is no general approximation theorem.
    """
    certificate=acquire_certificate(f,base,rank_budget,k,Q(1),order,
                                  separator_budget,frontier_cap)
    if certificate['status']!='CERTIFIED':return certificate
    n=certificate['n'];rhs=certificate['norm_estimate']/Q(16*(1<<n))
    if certificate['amplitude_error_squared_bound']>rhs:
        certificate['status']='UNKNOWN_ADMISSION'
        certificate['reason']='uniform-accuracy precision-gap guard failed'
        certificate['uniform_accuracy_guard_rhs']=rhs
        return certificate
    certificate['status']='UNIFORM_CERTIFIED'
    certificate['uniform_accuracy_guard_rhs']=rhs
    certificate['guarantee']='all epsilon in (0,1]: polynomial in n,L,epsilon^-1 when base width+rank=O(log n)'
    return certificate

def acquire_banded_uniform_certificate(f,bandwidth,rank_budget,k,frontier_cap=None):
    f=matrix(f);n=len(f)
    if bandwidth<0:raise ValueError('negative bandwidth')
    base=[[f[i][j] if abs(i-j)<=bandwidth else C(0) for j in range(n)] for i in range(n)]
    return acquire_uniform_accuracy_certificate(f,base,rank_budget,k,
                    order=list(range(n)),frontier_cap=frontier_cap)

def uniform_branch(certificate,epsilon):
    epsilon=Q(epsilon)
    if not 0<epsilon<=1:raise ValueError('epsilon must lie in (0,1]')
    if certificate['status']!='UNIFORM_CERTIFIED':return 'UNKNOWN_ADMISSION'
    if certificate['amplitude_error_squared_bound']<=epsilon*epsilon*certificate['norm_estimate']/16:
        return 'APPROXIMATE_WIDTH_BACKEND'
    assert epsilon*epsilon < Q(1,1<<certificate['n'])
    # This exact rational assertion is the load-bearing fallback cost charge.
    assert Q(16**certificate['n']) < epsilon**(-8)
    return 'EXACT_FINE_ACCURACY'

def norm_uniform_accuracy(certificate,epsilon):
    branch=uniform_branch(certificate,epsilon)
    if branch=='UNKNOWN_ADMISSION':return {'status':branch}
    if branch=='APPROXIMATE_WIDTH_BACKEND':norm=certificate['norm_estimate']
    else:norm=full_frontier_count(certificate['F'],certificate['k'],order=certificate['order'])
    return {'status':'NORM','branch':branch,'norm':norm,'epsilon':Q(epsilon),
        'guarantee':'relative error <= epsilon; exact on fine-accuracy branch'}

def sample_uniform_accuracy(certificate,epsilon,getrandbits):
    branch=uniform_branch(certificate,epsilon)
    if branch=='UNKNOWN_ADMISSION':return {'status':branch}
    if branch=='APPROXIMATE_WIDTH_BACKEND':
        local=dict(certificate);local['status']='CERTIFIED';local['epsilon']=Q(epsilon)
        result=sample_certified(local,getrandbits)
    else:
        result=full_frontier_sample(certificate['F'],certificate['k'],getrandbits,
            epsilon=Q(epsilon),order=certificate['order'])
        result['TV_bound']=Q(epsilon)
    result['branch']=branch
    return result
