#!/usr/bin/env python3
"""Bounded actual-matrix admissions for the block-algebra proof.
No optimization, hardware experiment, or numerical proof of a universal claim.
"""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
    os.environ[k]='1'
import numpy as np
import itertools, json, math, time, resource, sys
from pathlib import Path

cpu,wall=time.process_time(),time.perf_counter(); rng=np.random.default_rng(202610224)
m=math.log(2);C=2-m
def entropy(rho):
    w=np.maximum(np.linalg.eigvalsh((rho+rho.conj().T)/2),0)
    return float(-sum(v*math.log(v) for v in w if v>1e-14))
def partial(a,S,n):
    t=a.reshape((2,)*(2*n));cur=n
    for s in sorted(S,reverse=True):
        t=np.trace(t,axis1=s,axis2=s+cur);cur-=1
    return t.reshape(2**cur,2**cur)
def erase(a,S,n):
    rest=[j for j in range(n) if j not in S]; order=list(S)+rest
    t=a.reshape((2,)*(2*n)).transpose(order+[j+n for j in order])
    L=2**len(S);R=2**len(rest)
    red=np.trace(t.reshape(L,R,L,R),axis1=0,axis2=2)
    z=np.einsum('ab,cd->acbd',np.eye(L)/L,red).reshape((2,)*(2*n))
    inv=np.argsort(order);return z.transpose(list(inv)+[int(j+n) for j in inv]).reshape(a.shape)
def cell_masks(N,mode):
    d=2**N;q=d*d
    if mode=='uniform': blocks=[list(range(2*j,2*j+2)) for j in range(d//2)]
    else:blocks=[list(range(2))]+[[j] for j in range(2,d)]
    masks=[];ranks=[]
    for a in range(2):
        fam=[]
        for b in blocks:
            # Complement B for task A, complement A for task B.
            mask=np.array([(v%d if a==0 else v//d) in b for v in range(q)])
            fam.append(mask)
        masks.append(fam);ranks.append([len(b) for b in blocks])
    return masks,ranks
def pinch(a,fam):
    z=np.zeros_like(a)
    for mask in fam:z[np.ix_(mask,mask)]=a[np.ix_(mask,mask)]
    return z
def joint_pinch(a,masks):
    for fam in masks:a=pinch(a,fam)
    return a
def stats(X,N,masks,ranks):
    n=2*N;q=2**n;rho=X.conj().T@X;S=entropy(rho);score=0.;steps=[];Hs=[];localS=[];cost=0.
    for a in range(2):
        ps=[float(np.linalg.norm(erase(X,list(range(a*N,a*N+i)),n))**2) for i in range(1,N+1)]
        score+=m*sum(ps)
        prob=[float(np.trace(rho[np.ix_(mask,mask)]).real) for mask in masks[a]]
        h=-sum(p*math.log(p) for p in prob if p>1e-14);Hs.append(h)
        localS.append(entropy(partial(rho,list(range(a*N,(a+1)*N)),n)))
        cost+=sum(p*math.log(k) for p,k in zip(prob,ranks[a]))
        steps.append(ps)
    return {'entropy':S,'score':score,'rank_cost':cost,'defect':score-S-cost,
            'prefix_probabilities':steps,'label_entropies':Hs,'complement_entropies':localS}

cases=[]; maxdef=-1e9; maxnon=0.;robust=[]
for N,mode,trials in [(2,'uniform',12),(2,'variable',12),(3,'uniform',8)]:
    q=2**(2*N);masks,ranks=cell_masks(N,mode)
    for t in range(trials):
        Z=rng.normal(size=(q,q))+1j*rng.normal(size=(q,q))
        X=joint_pinch(Z,masks);X/=np.linalg.norm(X)
        if t==0:X=np.eye(q)/math.sqrt(q)
        assert all(np.linalg.norm(X-pinch(X,fam))<1e-12 for fam in masks)
        s=stats(X,N,masks,ranks);maxdef=max(maxdef,s['defect'])
        assert s['defect']<=2*C+1e-10
        non=float(np.linalg.norm(X.conj().T@X-X@X.conj().T));maxnon=max(maxnon,non)
        for a in range(2):
            assert m*sum(s['prefix_probabilities'][a])<=s['entropy']-s['label_entropies'][a]+C+1e-10
            assert s['complement_entropies'][a]<=s['label_entropies'][a]+math.log(max(ranks[a]))+1e-10
        assert sum(s['complement_entropies'])>=s['entropy']-1e-10
        cases.append({'N':N,'mode':mode,'trial':t,'normality_commutator_HS':non,**s})
        if N==2 and t==1:
            Y=Z-joint_pinch(Z,masks);Y/=np.linalg.norm(Y)
            Lmax=sum(math.log(max(ks)) for ks in ranks)
            for eta in [0.,1e-6,.01,.25,1.]:
                V=math.sqrt(1-eta)*X+math.sqrt(eta)*Y
                assert abs(np.linalg.norm(V)-1)<1e-12
                ell=1-float(np.linalg.norm(joint_pinch(V,masks))**2)
                failures=[1-float(np.linalg.norm(pinch(V,fam))**2) for fam in masks]
                assert abs(ell-eta)<1e-12 and ell<=sum(failures)+1e-12
                v=stats(V,N,masks,ranks);u=min(math.sqrt(max(ell,0)),.5)
                hb=0 if u==0 else -u*math.log(u)-(1-u)*math.log(1-u)
                penalty=(2*math.log(q)+Lmax)*math.sqrt(max(ell,0))+hb
                bound=v['score']-2*C-v['rank_cost']-penalty
                assert v['entropy']>=bound-1e-10
                robust.append({'N':N,'mode':mode,'actual_leakage':ell,'summed_test_failures':sum(failures),
                               'true_pure_entanglement':v['entropy'],'robust_lower_bound':bound})

# Actual Weyl/Pauli expansion of the Bell-prefix observable, including nonnormal X.
P=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
N=2;n=4;q=16;masks,ranks=cell_masks(N,'variable');X=joint_pinch(rng.normal(size=(q,q))+1j*rng.normal(size=(q,q)),masks);X/=np.linalg.norm(X)
weyl=[]
for a in range(2):
    for i in range(1,N+1):
        avg=0.
        for word in itertools.product(range(4),repeat=i):
            ops=[np.eye(2) for _ in range(n)]
            for j,s in enumerate(word):ops[a*N+j]=P[s]
            U=ops[0]
            for v in ops[1:]:U=np.kron(U,v)
            avg+=float(np.trace(X.conj().T@U@X@U.conj().T).real)/4**i
        direct=float(np.linalg.norm(erase(X,list(range(a*N,a*N+i)),n))**2)
        assert abs(avg-direct)<1e-12
        weyl.append({'task':a,'prefix':i,'local_Pauli_estimator_exact_mean':avg,'actual_Bell_prefix_probability':direct})

raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
result={'status':'PASS','scope':'actual finite matrices; not optimizer, generic proof, laboratory measurement or optimal E_F calculation',
 'pure_block_algebra_cases':cases,'largest_normality_commutator_HS':maxnon,'maximum_score_minus_entropy_minus_rank_cost':maxdef,
 'robust_actual_pure_cases':robust,'Bell_prefix_local_estimator_identity':weyl,
 'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-wall,
 'peak_RSS_bytes':raw if sys.platform=='darwin' else raw*1024,'numpy':np.__version__,
 'total_discovery_reasoning_cost':'UNKNOWN'}
assert maxnon>.01
Path(__file__).with_name('RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','largest_normality_commutator_HS','cpu_seconds','wall_seconds','peak_RSS_bytes']}))
