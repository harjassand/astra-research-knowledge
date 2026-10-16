"""Exact finite-state tests for symmetric interchange/exclusion rate saturation.
All code is original for this check; inputs are synthetic supplied-rate graphs.
No Monte Carlo, material measurements, trajectory claims, or acquired code.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import itertools, json, math, csv, time
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from scipy.integrate import quad
from scipy.optimize import brentq

OUT=Path(__file__).resolve().parent

def space(n,mode,k=None):
    if mode=='interchange': return list(itertools.permutations(range(n)))
    return [tuple(int(i in S) for i in range(n)) for S in itertools.combinations(range(n),k)]

def swap_maps(states,edges):
    index={x:i for i,x in enumerate(states)}
    maps=[]
    for a,b in edges:
        out=[]
        for x in states:
            y=list(x); y[a],y[b]=y[b],y[a]
            out.append(index[tuple(y)])
        maps.append(np.array(out))
    return maps,index

def laplacian(maps,rates):
    N=len(maps[0]); L=np.zeros((N,N)); idx=np.arange(N)
    for p,r in zip(maps,rates):
        L[idx,idx]+=r; L[idx,p]-=r
    return L

def endpoint(L,initial,T=1.):
    eig,V=eigh(L,check_finite=False,driver='evr')
    scale=max(1.,float(np.max(eig)))
    if eig[0]<-1e-11*scale: raise AssertionError(('negative eigenvalue',eig[0],scale))
    eig=np.maximum(eig,0.)
    coeff=V[initial,:] if isinstance(initial,(int,np.integer)) else V.T@initial
    p=V@(np.exp(-T*eig)*coeff)
    return p, {'mass_error':abs(float(p.sum())-1), 'minimum_probability':float(p.min()), 'minimum_eigenvalue':float(eig.min())}

def clean(p):
    assert p.min()>-1e-7
    p=np.maximum(p,0); return p/p.sum()

def tv(p,q): return .5*np.abs(p-q).sum()

def limit_endpoint(states,clusters,Lslow,initial):
    buckets={}
    for j,state in enumerate(states):
        key=tuple(tuple(sorted(state[i] for i in C)) for C in clusters)
        buckets.setdefault(key,[]).append(j)
    U=np.zeros((len(states),len(buckets)))
    for col,ids in enumerate(buckets.values()): U[ids,col]=1/math.sqrt(len(ids))
    red=U.T@Lslow@U
    init=U[initial]
    eig,V=eigh(red,check_finite=False)
    p=U@(V@(np.exp(-np.maximum(eig,0))*(V.T@init)))
    return clean(p),len(buckets)

def c_local(s): return s*(s-1)/4

def bound_local(K,cs,bs):
    if any(K<2*c for c in cs): return float('nan')
    return sum(c*c/K*(b*b+2*(1+b)*(2+math.log(K/c))) for c,b in zip(cs,bs))

def bound_pair(K,bs):
    return sum(b*b/(2*(2*K+b))+b/(2*K+b)-b*b/(2*(2*K+b)**2)+.5*math.exp(-2*K-b) for b in bs)

def bound_global(K,n,m):
    c=n*n/2
    if K<2*c: return float('nan')
    return m*c*c/K*(6+2*math.log(K/c))

def a_local(t,w,c,b): return 1. if t==0 else min(1.,c/w*(1/t+b))

def cap_for_eps(fun,low,eps=.01):
    high=low
    while fun(high)>eps: high*=2
    return brentq(lambda k:fun(k)-eps,low,high)

specs=[]
n=10; clusters=[(2*i,2*i+1) for i in range(5)]
fast=[tuple(C) for C in clusters]; slow=[(2*i+1,(2*i+2)%n) for i in range(5)]
specs.append(dict(name='ten_vertex_fast_matching_exclusion',n=n,mode='exclusion',k=5,clusters=clusters,fast=fast,slow=slow,beta=.2,initial=tuple(i%2==0 for i in range(n)),Ks=[1,2,5,10,30,100,120,300,1000],W=1e5))
clusters=[tuple(range(4)),tuple(range(4,8))]
specs.append(dict(name='eight_vertex_two_cliques_exclusion',n=8,mode='exclusion',k=4,clusters=clusters,fast=[e for C in clusters for e in itertools.combinations(C,2)],slow=[(3,4)],beta=.2,initial=tuple(int(i in {0,1,4,5}) for i in range(8)),Ks=[2,5,10,30,100,300,1000,3000,10000],W=1e5))
clusters=[(0,1,2),(3,4,5)]
specs.append(dict(name='six_vertex_two_triangles_interchange',n=6,mode='interchange',k=None,clusters=clusters,fast=[e for C in clusters for e in itertools.combinations(C,2)],slow=[(2,3)],beta=.2,initial=tuple(range(6)),Ks=[1,2,5,10,30,100,300,1000],W=1e5))

results=[]; diagnostics=[]; crossovers=[]
for sp in specs:
    start=time.time(); n=sp['n']; edges=sp['fast']+sp['slow']; nf=len(sp['fast']); beta=sp['beta']
    states=space(n,sp['mode'],sp['k']); maps,index=swap_maps(states,edges); initial=index[sp['initial']]
    rates=[sp['W']]*nf+[beta]*len(sp['slow'])
    po,diag=endpoint(laplacian(maps,rates),initial); po=clean(po)
    pinf,norbit=limit_endpoint(states,sp['clusters'],laplacian(maps,[0]*nf+[beta]*len(sp['slow'])),initial)
    cs=[]; bs=[]
    for e in sp['fast']:
        C=next(C for C in sp['clusters'] if e[0] in C and e[1] in C)
        degree={x:sum(r for (a,b),r in zip(edges,rates) if (a==x and b not in C) or (b==x and a not in C)) for x in C}
        bs.append(sum(sorted(degree.values(),reverse=True)[:2])); cs.append(c_local(len(C)))
    gl=lambda K:bound_global(K,n,nf)
    lo=lambda K:bound_local(K,cs,bs)
    co=dict(graph=sp['name'],state_count=len(states),infinite_orbits=norbit,fast_edges=nf,slow_edges=len(sp['slow']),beta=beta,original_W=sp['W'],local_c=cs[0],local_b=bs[0],original_to_infinite_TV=float(tv(po,pinf)),original_event_intensity=sum(rates),certificate_eps=.05,global_K=cap_for_eps(gl,n*n,eps=.05),local_K=cap_for_eps(lo,2*max(cs),eps=.05))
    if all(c==.5 for c in cs):
        co['pair_K']=cap_for_eps(lambda K:bound_pair(K,bs),1e-6,eps=.05)
        co['pair_capped_event_intensity']=nf*co['pair_K']+beta*len(sp['slow'])
    co['tightened_global_K']=cap_for_eps(lambda K:bound_local(K,[c_local(n)]*nf,[0]*nf),2*c_local(n),eps=.05)
    co['local_capped_event_intensity']=nf*co['local_K']+beta*len(sp['slow'])
    co['homogeneous_clique_K']=cap_for_eps(lambda K:bound_pair(K,bs),1e-6,eps=.05)
    co['homogeneous_clique_capped_event_intensity']=nf*co['homogeneous_clique_K']+beta*len(sp['slow'])
    for cert in ('local','homogeneous_clique'):
        pp,dd=endpoint(laplacian(maps,[co[cert+'_K']]*nf+[beta]*len(sp['slow'])),initial)
        co[cert+'_actual_TV']=float(tv(po,clean(pp)))
    def endpoint_error(K):
        pp,_=endpoint(laplacian(maps,[K]*nf+[beta]*len(sp['slow'])),initial)
        return tv(po,clean(pp))
    co['observed_TV_05_crossing_K']=brentq(lambda K:endpoint_error(K)-.05,.01,100)
    co['observed_TV_01_crossing_K']=brentq(lambda K:endpoint_error(K)-.01,.01,100)
    for K in sp['Ks']:
        pk,d=endpoint(laplacian(maps,[K]*nf+[beta]*len(sp['slow'])),initial); pk=clean(pk)
        result=dict(graph=sp['name'],K=K,TV_original_vs_cap=float(tv(po,pk)),TV_infinite_vs_cap=float(tv(pinf,pk)),global_bound=gl(K),local_bound=lo(K),pair_bound=bound_pair(K,bs) if all(c==.5 for c in cs) else None,homogeneous_clique_bound=bound_pair(K,bs),capped_event_intensity=nf*K+beta*len(sp['slow']))
        assert not math.isfinite(result['local_bound']) or result['TV_original_vs_cap'] <= result['local_bound']+1e-8
        assert result['TV_original_vs_cap']<=result['homogeneous_clique_bound']+1e-8
        if result['pair_bound'] is not None: assert result['TV_original_vs_cap']<=result['pair_bound']+1e-8
        results.append(result); diagnostics.append(dict(graph=sp['name'],K=K,**d))
    diagnostics.append(dict(graph=sp['name'],K=sp['W'],**diag));crossovers.append(co)
    print(json.dumps(co),flush=True);print('elapsed',time.time()-start,flush=True)

# Direct smoothing and derivative checks with other internal rates spread over 10 orders.
rng=np.random.default_rng(727)
checks=[]
n=6; states=space(n,'exclusion',3)
edges=[(0,1),(0,2),(1,2),(2,3),(3,4),(4,5),(3,5)]
maps,index=swap_maps(states,edges); C=(0,1,2); c=c_local(3); b=.2
for sample in range(60):
    w=10**rng.uniform(0,5)
    rates=[w,10**rng.uniform(-5,5),10**rng.uniform(-5,5),.2,10**rng.uniform(-5,5),10**rng.uniform(-5,5),10**rng.uniform(-5,5)]
    L=laplacian(maps,rates); eig,V=eigh(L); eig=np.maximum(eig,0)
    t=10**rng.uniform(-4,1)
    P=(V*np.exp(-eig*t))@V.T
    actual=.5*np.abs(P-P[maps[0]]).sum(axis=1).max()
    envelope=a_local(t,w,c,b)
    assert actual<=envelope+1e-7,(actual,envelope)
    # Spectral Fréchet derivative of exp(-L), exact finite-state linear algebra.
    E=V.T@(np.eye(len(states))-np.eye(len(states))[maps[0]])@V
    lam1=eig[:,None];lam2=eig[None,:];d=lam1-lam2
    # stable divided difference of exp(-lambda)
    F=np.empty_like(d); close=np.abs(d)<1e-8
    F[close]=-np.exp(-((lam1+lam2)/2+np.zeros_like(d))[close])
    num=np.exp(-lam1)-np.exp(-lam2)
    F[~close]=num[~close]/d[~close]
    DP=V@(F*E)@V.T
    actual_derivative=.5*np.abs(DP).sum(axis=1).max()
    env_integral=quad(lambda s:a_local(s,w,c,b)*a_local(1-s,w,c,b),0,1,epsabs=1e-12,points=[.5],limit=200)[0]
    assert actual_derivative<=env_integral+1e-8,(actual_derivative,env_integral)
    checks.append(dict(sample=sample,w=w,other_rates=rates[1:],t=t,smoothing=actual,envelope=envelope,sensitivity=actual_derivative,sensitivity_envelope=env_integral))
print('random smoothing/sensitivity checks:',len(checks),flush=True)

# Exact restricted-pair meeting check, including comparison with tightened constant.
meetings=[]
for s in range(2,9):
    pairs=list(itertools.combinations(range(s),2)); lookup={p:i for i,p in enumerate(pairs)}
    for repeat in range(30):
        rates=np.zeros((s,s)); rates[0,1]=rates[1,0]=10**rng.uniform(-3,3)
        for x,y in itertools.combinations(range(s),2):
            if (x,y)!=(0,1): rates[x,y]=rates[y,x]=10**rng.uniform(-5,5)
        H=np.zeros((len(pairs),len(pairs)))
        for j,(x,y) in enumerate(pairs):
            H[j,j]=2*rates[x,y]
            for a,z in ((x,y),(y,x)):
                for v in range(s):
                    if v in (a,z): continue
                    u=lookup[tuple(sorted((v,z)))]; H[j,j]+=rates[a,v];H[j,u]-=rates[a,v]
        assert np.allclose(H,H.T)
        h=np.linalg.solve(H,np.ones(len(pairs)))
        assert abs(float((H@np.ones(len(pairs)))@h)-len(pairs))<1e-5
        val=float(h[lookup[(0,1)]])*rates[0,1]
        assert val<=c_local(s)*(1+1e-6),(s,val,c_local(s))
        meetings.append(dict(s=s,w_times_mean_meeting=val,c_bound=c_local(s)))
print('restricted meeting checks:',len(meetings),flush=True)

payload=dict(results=results,crossovers=crossovers,diagnostics=diagnostics,random_checks=checks,meeting_checks=meetings,versions=dict(numpy=np.__version__))
(OUT/'results.json').write_text(json.dumps(payload,indent=2,allow_nan=True))
with (OUT/'endpoint_results.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=results[0].keys());w.writeheader();w.writerows(results)
print('Wrote',OUT/'results.json')
