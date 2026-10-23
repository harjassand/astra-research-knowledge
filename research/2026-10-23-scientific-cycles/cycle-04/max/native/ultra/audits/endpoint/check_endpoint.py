"""Bounded finite-matrix/elementary checks; no optimality-search claim.
Run in a fresh copy: it writes RESULT.json beside this script.
"""
import itertools, json, math, os, platform, resource, sys, time
from pathlib import Path
import numpy as np

start=time.perf_counter(); cpu=time.process_time()
rng=np.random.default_rng(20261022)

def reduction(v, selected, sites, D):
    selected=tuple(sorted(selected)); rest=tuple(i for i in range(sites) if i not in selected)
    a=v.reshape((D,)*sites).transpose(selected+rest).reshape(D**len(selected),-1)
    return a@a.conj().T

def product_bell_overlap(a,b,selected,sites,D):
    ra=reduction(a,selected,sites,D); rb=reduction(b,selected,sites,D)
    return float(np.trace(ra.T@rb).real)/(D**len(selected))

matrix_checks=[]; worst_tail_excess=-1.; worst_moment_excess=-1.
for D,N,t,trials in [(2,2,2,20),(2,3,2,15),(3,2,2,10)]:
    sites=N*t; dim=D**sites; Z=1+(N-1)*(1-1/D)
    weights=[D]+[D**i-D**(i-1) for i in range(2,N+1)]
    for trial in range(trials):
        a=rng.normal(size=dim)+1j*rng.normal(size=dim); a/=np.linalg.norm(a)
        b=rng.normal(size=dim)+1j*rng.normal(size=dim); b/=np.linalg.norm(b)
        moment=0.
        for tail in itertools.product(range(1,N+1), repeat=t):
            selected=[block*N+j for block,i in enumerate(tail) for j in range(i)]
            prob=product_bell_overlap(a,b,selected,sites,D)
            bound=D**(-sum(tail)); excess=prob-bound
            worst_tail_excess=max(worst_tail_excess,excess)
            assert excess<1e-12
            moment+=math.prod(weights[i-1] for i in tail)*prob
        worst_moment_excess=max(worst_moment_excess,moment-Z**t)
        assert moment<=Z**t+1e-12
    matrix_checks.append({'D':D,'N':N,'copies':t,'random_global_A_B_product_states':trials})

# An A:B product comparator with local entanglement ACROSS copies.
# Neither ordinary factorization nor conditional marginal domination is valid.
D=2; a=np.eye(D).reshape(-1)/math.sqrt(D); b=a.copy()
pfirst=product_bell_overlap(a,b,[0],2,D)
psecond=product_bell_overlap(a,b,[1],2,D)
pboth=product_bell_overlap(a,b,[0,1],2,D)
assert abs(pfirst-D**-2)<1e-12 and abs(psecond-D**-2)<1e-12
assert abs(pboth-D**-2)<1e-12 and pboth>pfirst*psecond

# The exact finite supplied resource domination Phi_M <= M zeta_M.
resource_min_eigs=[]
for M in range(1,9):
    v=np.zeros(M*M); v[::M+1]=1/math.sqrt(M)
    z=np.zeros((M*M,M*M)); z[np.arange(M)*(M+1),np.arange(M)*(M+1)]=1/M
    mineig=float(np.linalg.eigvalsh(M*z-np.outer(v,v))[0]); assert mineig>-1e-12
    resource_min_eigs.append(mineig)

# An actual preparation protocol with M=1: output chi^N instead of the ideal
# erased uniform-stock tau_N. Both commute in the Bell-phase MC eigenbasis,
# so the exact trace distance is a scalar total variation, not an estimate.
actual=[]
for N,t in [(2,1),(2,2),(2,4),(2,6),(3,1),(3,2),(3,4)]:
    D=2; words=list(itertools.product(range(D), repeat=N))
    lam=np.array([sum((D**(-(N-h)) if all(z[j]==0 for j in range(h)) else 0.)
                     for h in range(1,N+1))/N for z in words])
    assert abs(lam.sum()-1)<1e-12
    p=np.array([sum(lam[j] for j,z in enumerate(words) if all(z[k]==0 for k in range(i)))
                for i in range(1,N+1)])
    mu=float(p.sum()); Z=1+(N-1)*(1-1/D); m=math.log(D); C=m*mu-math.log(Z)
    gamma=C; kappa=mu-gamma/(2*m)
    eigs=lam.copy()
    for _ in range(t-1): eigs=np.kron(eigs,lam)
    chi=np.full(eigs.size,1/eigs.size)
    error=float(np.abs(eigs-chi).sum()/2)
    beta=math.exp(-2*t*(mu-kappa)**2/(N-1)**2) if kappa>=1 else 0.
    if kappa<1: kappa=1.
    bound=1-beta-math.exp(-t*(m*kappa-math.log(Z)))
    assert error>=bound-1e-12
    actual.append({'D':D,'N':N,'copies':t,'mu':mu,'R':0.,'exact_global_half_trace_error':error,
                   'proved_lower_bound':max(0.,bound),'C_N':C})

# Exact erased-coin expected-resource counterconstruction, finite matrices.
gamble=[]
for D,t,q in [(2,1,.25),(2,3,.5),(3,2,.75)]:
    rank=D**t; phi=np.zeros((rank,rank)); phi[0,0]=1.
    chi=np.eye(rank)/rank; sigma=q*phi+(1-q)*chi
    err=float(np.abs(np.linalg.eigvalsh(sigma-phi)).sum()/2)
    expected=(1-q)*(1-1/rank)
    assert abs(err-expected)<1e-12
    gamble.append({'D':D,'copies':t,'good_probability':q,'exact_global_error':err,
                   'formula_error':expected,'expected_cost_nats':q*t*math.log(D),
                   'deterministic_threshold_nats':t*math.log(D)})

# Check the elementary expected-cost chord over wide finite ranges.
worst_chord=-math.inf
for b in [0.01,0.1,0.5,1.,2.,10.,100.]:
    for l in np.linspace(0,2*b,301):
        f=min(1.,math.exp(l-b)); chord=math.exp(-b)+(1-math.exp(-b))*l/b
        worst_chord=max(worst_chord,f-chord); assert f<=chord+1e-12

# Joint-scaling finite constants and initializer rounding, including J>1.
scaling=[]
for J in [1,2,5]:
    d=2; m=J*math.log(d); xi=.2
    for delta in [1e-2,1e-3,1e-5,1e-8]:
        N=math.ceil(1/delta); Z=1+(N-1)*(1-math.exp(-m))
        a=N-delta*N*(N-1)/2; kappa=(1-xi/2)/(2*delta)
        assert a-kappa>=xi/(4*delta)-1e-8
        assert N-1<=1/delta+1e-8
        if math.log(Z)>xi*m/(8*delta): continue
        t=1000; L=math.ceil(J/delta); mu=J+(L-1)/2
        B=math.ceil(t*mu+(L-1)*math.sqrt(t*math.log(t)/2))
        normalized=delta*math.log(d)*B/t
        upper=m/2+delta*m+m*math.sqrt(math.log(t)/(2*t))+delta*math.log(d)/t
        assert normalized<=upper+1e-12
        scaling.append({'J':J,'delta':delta,'N':N,'copies':t,
                        'normalized_initialization_cost':normalized,'proved_upper':upper})

raw_rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss_bytes=int(raw_rss if sys.platform=='darwin' else raw_rss*1024)
result={'status':'PASS','python':platform.python_version(),'numpy':np.__version__,
        'seed':20261022,'random_actual_global_separable_checks':matrix_checks,
        'worst_joint_tail_bound_excess':worst_tail_excess,'worst_moment_bound_excess':worst_moment_excess,
        'cross_copy_separable_counterexample':{'single_copy_Bell_probabilities':[pfirst,psecond],
                  'joint_Bell_probability':pboth,'false_product':pfirst*psecond},
        'Bell_resource_order_minimum_eigenvalues':resource_min_eigs,
        'actual_zero_resource_preparation_checks':actual,'exact_gamble_checks':gamble,'worst_chord_excess':worst_chord,
        'uniform_diagonal_initialization_checks':scaling,
        'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,
        'peak_RSS_bytes':rss_bytes,'total_research_cost':'UNKNOWN',
        'scope':'finite checks of the analytic proof; not a generic tensor witness or novelty assessment'}
Path(__file__).with_name('RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','wall_seconds','cpu_seconds','peak_RSS_bytes']}))
