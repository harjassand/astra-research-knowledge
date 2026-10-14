"""Independent exact finite checks and acquisition-class countermodels.

The original source files are imported only for a final exact cross-check of
its compact certificate and query inference. Full-state generators, stationary
weights, relaxation minorants, residuals, and rational solves are rebuilt here.
"""
from __future__ import annotations
import itertools, json, sys, time
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'source_snapshot'/'escape'
OUT=ROOT/'replay'
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0,str(SOURCE))
from collective_sector import CollectiveRing
from acquisition import acquire


def wallcount(x,n):
    return sum(((x>>i)&1) != ((x>>((i+1)%n))&1) for i in range(n))

def weights_for(n,t,exception=None):
    t=F(t)
    out=[t**(n-wallcount(x,n)) for x in range(1<<n)]
    if exception is not None:
        mask,factor=exception
        out[mask] *= F(factor)
    return out

def transition_matrix(n,t,nu=F(1),kappa=F(1),weights=None,slow_bit0=F(1)):
    t=F(t); nu=F(nu); kappa=F(kappa)
    if weights is None: weights=weights_for(n,t)
    N=1<<n
    K=[[F(0) for _ in range(N)] for _ in range(N)]
    for x in range(N):
        K[x][x] += kappa*int(bool(x&1))
        for i in range(n):
            y=x^(1<<i)
            prefactor=slow_bit0 if i==0 else F(1)
            q=nu*prefactor*weights[y]/(weights[x]+weights[y])
            K[x][x]+=q
            K[x][y]-=q
    Z=sum(weights)
    pi=[w/Z for w in weights]
    return K,pi

def mean_from_generator(K,pi):
    sol=solve_fraction(K,[F(1)]*len(K))
    return sum(p*v for p,v in zip(pi,sol))

def solve_fraction(A,b):
    """Exact Gauss-Jordan solve over Q; caller owns the matrix copy."""
    n=len(A)
    M=[list(map(F,row))+[F(rhs)] for row,rhs in zip(A,b)]
    for col in range(n):
        pivot=next((r for r in range(col,n) if M[r][col]),None)
        if pivot is None: raise ArithmeticError('singular exact system')
        if pivot!=col: M[col],M[pivot]=M[pivot],M[col]
        d=M[col][col]
        M[col]=[x/d for x in M[col]]
        for r in range(n):
            if r==col: continue
            a=M[r][col]
            if a: M[r]=[u-a*v for u,v in zip(M[r],M[col])]
    return [M[i][-1] for i in range(n)]

def exact_psd(A):
    """Exact symmetric Schur/LDL elimination, including zero pivots."""
    M=[list(map(F,row)) for row in A]
    n=len(M)
    for k in range(n):
        p=M[k][k]
        if p<0: return False,k,p
        if p==0:
            if any(M[k][j] for j in range(k,n)): return False,k,p
            continue
        for i in range(k+1,n):
            for j in range(i,n):
                M[i][j]-=M[i][k]*M[k][j]/p
                M[j][i]=M[i][j]
    return True,n,F(0)

def source_model_matrices(n,t,nu=F(1),kappa=F(1)):
    t=F(t);nu=F(nu);kappa=F(kappa)
    K,pi=transition_matrix(n,t,nu,kappa)
    N=1<<n
    eta=(t*t-1)/(t*t+1)
    lam=nu*(1-eta)
    gamma=nu*((1-eta)+F(4)*eta/F(n*n))
    mags=[F(2*x.bit_count()-n,n) for x in range(N)]
    s=sum(p*m*m for p,m in zip(pi,mags))
    C=[[F(0) for _ in range(N)] for _ in range(N)]
    for x in range(N):
        C[x][x]+=gamma+kappa*int(bool(x&1))
        for y in range(N):
            C[x][y]+=-gamma*pi[y]+(lam-gamma)*mags[x]*mags[y]*pi[y]/s
    weighted_gap=[[pi[x]*(K[x][y]-C[x][y]) for y in range(N)] for x in range(N)]
    assert all(weighted_gap[i][j]==weighted_gap[j][i] for i in range(N) for j in range(N))
    return K,C,pi,mags,lam,gamma,s,weighted_gap

def independent_residual_trial(n,t):
    K,C,pi,mags,lam,gamma,s,W=source_model_matrices(n,t)
    N=1<<n
    ok,piv,p=exact_psd(W)
    if not ok: raise AssertionError(f'complement minorant failed at pivot {piv}: {p}')
    S=[x for x in range(N) if wallcount(x,n)<=2]
    v=[F(int(x in S)) for x in range(N)]
    Kv=[sum(K[x][y]*v[y] for y in range(N)) for x in range(N)]
    r=[F(1)-Kv[x] for x in range(N)]
    source=sum(pi[x]*v[x] for x in range(N))
    energy=sum(pi[x]*v[x]*Kv[x] for x in range(N))
    lower=2*source-energy
    z=solve_fraction(C,r)
    error=sum(pi[x]*r[x]*z[x] for x in range(N))
    tau=mean_from_generator(K,pi)
    upper=lower+error
    if not (lower<=tau<=upper): raise AssertionError('independent full-source interval failed')
    neighborhood=set(S)
    for x in S:
        neighborhood.update(x^(1<<i) for i in range(n))
    if any(r[x]!=1 for x in range(N) if x not in neighborhood):
        raise AssertionError('omitted source residual is not one outside local neighborhood')
    compact=CollectiveRing(n,F(t)).certificate({x:F(1) for x in S})
    if compact[0]!=lower or compact[1]!=upper:
        raise AssertionError('compact certificate differs from full exact C inverse')
    return {
        'n':n,'t':str(t),'states':N,'minorant_psd_exact':ok,
        'slow_lambda':str(lam),'complement_gamma':str(gamma),
        'trial_states':len(S),'residual_neighborhood':len(neighborhood),
        'residual_exactly_one_outside_neighborhood':True,
        'tau_exact':str(tau),'lower_exact':str(lower),'upper_exact':str(upper),
        'residual_error_exact':str(error),'full_exact_interval_contains_tau':lower<=tau<=upper,
        'compact_formula_matches_full_exact_C_solve':True,
    }

def class_countermodels():
    n=6;t=F(2);trap=sum(1<<i for i in (1,2,3));factor=F(1000)
    base=weights_for(n,t)
    hidden=weights_for(n,t,(trap,factor))
    probes=[0]+[1<<i for i in range(n)]+[sum(1<<i for i in pair) for pair in itertools.combinations(range(n),2)]
    if any(base[x]!=hidden[x] for x in probes): raise AssertionError('countermodel changes a queried point')
    q_seen=[]
    def oracle(mask):
        q_seen.append(mask)
        return hidden[mask]
    inferred=acquire(n,oracle)
    if inferred['t']!=t or inferred['r']!=1 or len(q_seen)!=1+n+n*(n-1)//2:
        raise AssertionError('pairwise acquisition did not return the indistinguishable baseline')
    K0,pi0=transition_matrix(n,t,weights=base)
    Kh,pih=transition_matrix(n,t,weights=hidden)
    tau0=mean_from_generator(K0,pi0)
    tauh=mean_from_generator(Kh,pih)
    cert=CollectiveRing(n,t).run()
    # Independent detailed-balance check for the high-order hidden well.
    reversible=all(hidden[x]*Kh[x][x^(1<<i)]==hidden[x^(1<<i)]*Kh[x^(1<<i)][x]
                   for x in range(1<<n) for i in range(n))
    return {
        'n':n,'t':str(t),'trap_mask':trap,'hidden_weight_multiplier':str(factor),
        'queried_points':len(probes),'acquisition_queries':len(q_seen),
        'all_empty_single_pair_queries_identical':True,
        'inferred_t':str(inferred['t']),'inferred_field_r':str(inferred['r']),
        'inferred_cycle_edges':inferred['edges'],'hidden_model_reversible_exact':reversible,
        'baseline_tau_exact':str(tau0),'hidden_tau_exact':str(tauh),
        'hidden_over_baseline':float(tauh/tau0),
        'baseline_certificate_lo':cert['lower_exact'],'baseline_certificate_hi':cert['upper_exact'],
        'hidden_mean_exceeds_baseline_certificate':tauh>F(cert['upper_exact']),
        'hidden_mean_over_baseline_certificate_hi':float(tauh/F(cert['upper_exact'])),
    }

def tree_query_run(n, weights, order):
    """Exact transcript for the proposed shared balanced-tree degree-two learner."""
    V=(1<<n)-1
    edges={tuple(sorted((order[j],order[(j+1)%n]))) for j in range(n)}
    cache={};new_queries=[];contrasts=[];recovered=set()
    def W(mask):
        if mask not in cache:
            cache[mask]=weights[mask];new_queries.append(mask)
        return cache[mask]
    for mask in [0,V,*[1<<j for j in range(n)],V^1]: W(mask)
    root=W(V)*W(0)/(W(V^1)*W(1))
    a=root.numerator;b=root.denominator
    sqn=__import__('math').isqrt(a);sqd=__import__('math').isqrt(b)
    if sqn*sqn!=a or sqd*sqd!=b: raise AssertionError('root calibration not rational square')
    q=F(sqn,sqd)
    def build(lo,hi):
        if hi-lo==1:return (1<<lo,None,None)
        mid=(lo+hi)//2;L=build(lo,mid);R=build(mid,hi)
        return (L[0]|R[0],L,R)
    T=build(0,n)
    def rec(i,node,L,R,k):
        if L is None:
            if node.bit_count()!=1 or k!=1:raise AssertionError('invalid positive leaf')
            j=node.bit_length()-1;recovered.add(tuple(sorted((i,j))));return
        if node&(1<<i): A,B=(R,L) if L[0]&(1<<i) else (L,R)
        else:A,B=L,R
        a=A[0]
        ratio=W(a|(1<<i))*W(0)/(W(a)*W(1<<i))
        candidates=[m for m in (0,1,2) if ratio==q**m]
        if len(candidates)!=1:raise AssertionError('ratio not uniquely decodable')
        ka=candidates[0];kb=k-ka
        if kb<0 or kb>2:raise AssertionError('inconsistent inferred count')
        contrasts.append((i,a,str(ratio),ka,kb))
        if ka:rec(i,a,A[1],A[2],ka)
        if kb:rec(i,B[0],B[1],B[2],kb)
    for i in range(n):rec(i,V,T[1],T[2],2)
    if recovered!=edges:raise AssertionError('tree learner failed to recover graph')
    return {'q':str(q),'cache_masks':sorted(cache),'new_query_order':new_queries,
            'contrasts':contrasts,'edges':sorted(edges),'recovered':sorted(recovered)}

def tree_class_countermodel():
    n=6;t=F(2);order=list(range(n));base=weights_for(n,t)
    learned=tree_query_run(n,base,order)
    queried=set(learned['cache_masks'])
    candidates=[x for x in range(1<<n) if x.bit_count()>=3 and x not in queried]
    if 14 not in candidates:raise AssertionError('selected trap configuration is not an unqueried higher-order state')
    # This previously constructed trap state also defeats the pairwise probe
    # set; check it against the strictly richer adaptive tree transcript too.
    hidden_mask=14;factor=F(1000)
    hidden=weights_for(n,t,(hidden_mask,factor))
    hidden_run=tree_query_run(n,hidden,order)
    if learned['new_query_order']!=hidden_run['new_query_order'] or learned['contrasts']!=hidden_run['contrasts']:
        raise AssertionError('hidden unqueried term changed adaptive tree transcript')
    K0,pi0=transition_matrix(n,t,weights=base)
    Kh,pih=transition_matrix(n,t,weights=hidden)
    tau0=mean_from_generator(K0,pi0);tauh=mean_from_generator(Kh,pih)
    cert=CollectiveRing(n,t).run()
    reversible=all(hidden[x]*Kh[x][x^(1<<i)]==hidden[x^(1<<i)]*Kh[x^(1<<i)][x]
                   for x in range(1<<n) for i in range(n))
    return {'n':n,'t':str(t),'cycle_order':order,'tree_energy_queries_unique':len(queried),
      'pairwise_baseline_queries':1+n+n*(n-1)//2,'unqueried_higher_order_mask':hidden_mask,
      'hidden_weight_multiplier':str(factor),'same_adaptive_tree_query_sequence':True,
      'same_decoded_cycle_and_q':True,'hidden_model_reversible_exact':reversible,
      'baseline_tau_exact':str(tau0),'hidden_tau_exact':str(tauh),
      'hidden_over_baseline':float(tauh/tau0),
      'baseline_certificate_hi':cert['upper_exact'],
      'hidden_mean_exceeds_baseline_certificate':tauh>F(cert['upper_exact']),
      'hidden_mean_over_baseline_certificate_hi':float(tauh/F(cert['upper_exact']))}

def clock_countermodel():
    n=6;t=F(2);N=1<<n;speed=F(1,1000)
    base=weights_for(n,t)
    K,pi=transition_matrix(n,t,weights=base,slow_bit0=speed)
    # For every closed state the target-bit opening intensity is <= speed*nu.
    # Initial equilibrium gives exactly half the mass to x_0=0 by spin flip.
    lower=F(1,2)/speed
    return {'n':n,'t':str(t),'same_energy_law_and_queries':True,
            'heatbath_clock_assumed_by_certificate':'uniform nu=1',
            'countermodel_clock':'target-coordinate attempt prefactor nu_0=1/1000; all other nu_i=1',
            'equilibrium_mass_target_closed':str(sum(pi[x] for x in range(N) if not x&1)),
            'rigorous_mean_lower_from_closed_initial_sector':str(lower),
            'argument':'while x0=0, its opening intensity is at most 1/1000, so expected time to first opening is at least 1000; the equilibrium-closed half contributes at least 500 to the full mean.'}

def run_all():
    start=time.perf_counter()
    finite=[independent_residual_trial(4,F(2)),independent_residual_trial(5,F(10))]
    models=class_countermodels()
    tree_model=tree_class_countermodel()
    clock=clock_countermodel()
    return {'finite_exact_checks':finite,'higher_order_energy_countermodel':models,
            'shared_tree_higher_order_countermodel':tree_model,
            'clock_countermodel':clock,'seconds':time.perf_counter()-start,
            'scope':'Exact finite implementation checks and scoped countermodels; no external validation.'}

if __name__=='__main__':
    out=run_all()
    (OUT/'independent_checks.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
