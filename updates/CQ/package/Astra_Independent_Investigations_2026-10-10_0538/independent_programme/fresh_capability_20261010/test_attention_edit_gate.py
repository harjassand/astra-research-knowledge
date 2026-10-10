"""Native-CPU falsification gate for group-summary attention edit certificates.

No external model/data; these are synthetic residual attention stacks, not LLM
benchmarks. Full changed forwards are used ONLY as ground truth, never by the
online certificate. Output and bounds use float64; tests are numerical checks,
not formally rounded floating-point certificates. O(NB) certificate cost per
layer excludes the initial full forward and its summary construction.
"""
import json, math, os, time
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
from pathlib import Path

OUT=Path(__file__).resolve().parent

def sphere(x):
    return x*np.sqrt(x.shape[1])/np.linalg.norm(x,axis=1)[:,None]

def normalize_radius(x,r):
    """Exact worst Euclidean change of R*x/||x|| inside an r-ball.
    If ball reaches origin use its full diameter. No small-gain assumption.
    """
    R=np.sqrt(x.shape[1]); n=np.linalg.norm(x,axis=1)
    t=np.minimum(r/n,1.)
    # Rationalized form avoids catastrophic cancellation for tiny t.
    val=R*t*np.sqrt(2/(1+np.sqrt(np.maximum(0,1-t*t))))
    return np.where(r<n,val,2*R)

def layer(x,weights,alpha):
    Q,K,V,O=weights; xn=sphere(x)
    q=xn@Q; k=xn@K; v=xn@V
    s=q@k.T/np.sqrt(x.shape[1]); s-=s.max(axis=1)[:,None]
    p=np.exp(s); p/=p.sum(axis=1)[:,None]
    a=p@v
    return x+alpha*(a@O),(q,k,v,p,a)

def summaries(cache,B):
    q,k,v,p,a=cache; n=len(q)
    groups=np.array_split(np.arange(n),B)
    P=np.stack([p[:,g].sum(axis=1) for g in groups],axis=1)
    C=np.stack([(p[:,g]*np.linalg.norm(v[g][None,:,:]-a[:,None,:],axis=2)).sum(axis=1) for g in groups],axis=1)
    kn=np.array([np.linalg.norm(k[g],axis=1).max() for g in groups])
    return groups,P,C,kn

def propagate(x,r,weights,cache,summ,alpha):
    Q,K,V,O=weights; q,k,v,p,a=cache
    groups,P,C,kn=summ
    nq,nk,nv,no=[np.linalg.norm(W,2) for W in weights]
    dr=normalize_radius(x,r)
    dmax=np.array([dr[g].max() for g in groups])
    dq=nq*dr; dk=nk*dmax; dv=nv*dmax
    b=(np.linalg.norm(q,axis=1)[:,None]*dk[None,:]+dq[:,None]*kn[None,:]+dq[:,None]*dk[None,:])/np.sqrt(x.shape[1])
    # Algebraically rescaled expression keeps exponentials finite.
    m=b.max(axis=1)
    ep=np.exp(b-m[:,None]); en=np.exp(-b-m[:,None]); one=np.exp(-m)
    numerator=((ep-one[:,None])*C+ep*P*dv[None,:]).sum(axis=1)
    denominator=(en*P).sum(axis=1)
    raw=np.divide(numerator,denominator,out=np.full_like(numerator,np.inf),where=denominator>0)
    # Both exact old/new values lie inside radius sqrt(d)||V||.
    da=np.minimum(raw,2*np.sqrt(x.shape[1])*nv)
    return r+alpha*no*da

def run_case(seed,n=192,d=24,L=12,alpha=.5,edit_norm=.5,Bs=(1,8,32,192)):
    rng=np.random.default_rng(seed)
    x=rng.normal(size=(n,d)); xp=x.copy()
    e=rng.normal(size=d); e*=edit_norm/np.linalg.norm(e); xp[n//3]+=e
    rinit=np.linalg.norm(xp-x,axis=1)
    weights=[[rng.normal(size=(d,d))/np.sqrt(d) for _ in range(4)] for _ in range(L)]
    radii={B:rinit.copy() for B in Bs}; hist=[]
    for l,W in enumerate(weights):
        xn,c=layer(x,W,alpha); xpn,_=layer(xp,W,alpha)
        actual=np.linalg.norm(xpn-xn,axis=1)
        record={'layer':l+1,'actual_last':float(actual[-1]),'actual_max_unchanged_input':float(np.delete(actual,n//3).max()),'bounds':{}}
        for B in Bs:
            radii[B]=propagate(x,radii[B],W,c,summaries(c,B),alpha)
            assert np.all(actual <= radii[B]+1e-10),(seed,l,B,float((actual-radii[B]).max()))
            record['bounds'][str(B)]={'last':float(radii[B][-1]),'max':float(radii[B].max()),'last_bound_over_error':float(radii[B][-1]/max(actual[-1],1e-300)),'certifies_unit_readout_margin_0_25':bool(radii[B][-1]<.125)}
        hist.append(record); x,xp=xn,xpn
    return {'seed':seed,'n':n,'d':d,'layers':L,'alpha':alpha,'edit_norm':edit_norm,'initial_edit_token':n//3,'history':hist}

def update_identity_test(seed=20261010,n=80,d=9,k=3):
    rng=np.random.default_rng(seed)
    q,kold,vold=[rng.normal(size=(n,d)) for _ in range(3)]
    idx=np.array([3,17,35]); knew=kold.copy(); vnew=vold.copy()
    knew[idx]+=rng.normal(size=(len(idx),d)); vnew[idx]+=rng.normal(size=(len(idx),d))
    s=q@kold.T/np.sqrt(d); shift=s.max(axis=1); ex=np.exp(s-shift[:,None]); Z=ex.sum(axis=1); old=ex@vold
    esold=np.exp(q@kold[idx].T/np.sqrt(d)-shift[:,None]); esnew=np.exp(q@knew[idx].T/np.sqrt(d)-shift[:,None])
    updated=(old-esold@vold[idx]+esnew@vnew[idx])/(Z-esold.sum(axis=1)+esnew.sum(axis=1))[:,None]
    snew=q@knew.T/np.sqrt(d); ss=np.exp(snew-snew.max(axis=1)[:,None]); exact=ss@vnew/ss.sum(axis=1)[:,None]
    err=float(np.abs(updated-exact).max()); assert err<1e-12
    return {'max_absolute_error':err,'changed_KV_rows':len(idx),'queries_fixed':True,'warning':'Queries become changed and generally dense in the next layer; this identity is not a whole-transformer update.'}

def moment_collision(m=5,t=4.):
    # Two caches agree on moments sum p_j k_j^r v_j for r=0,...,m.
    # Same positive weights/keys. Opposite value signs differ under new query.
    n=m+1; k=np.arange(n+1,dtype=float)
    p=np.array([math.comb(n,j)/2**n for j in range(n+1)])
    v=(-1.)**k
    moments=[float(np.dot(p*v,k**r)) for r in range(m+1)]
    z=t*k; z-=z.max(); prob=p*np.exp(z); prob/=prob.sum()
    y=float(prob@v); formula=float((-np.tanh(t/2))**n)
    assert max(abs(a) for a in moments)<1e-11
    assert abs(y-formula)<1e-12
    # A fixed +0.25 bias gives strictly positive old margin and opposite new decisions.
    assert .25+y>0 and .25-y<0
    return {'moment_degree':m,'keys':k.tolist(),'weights':p.tolist(),'cached_value_moments':moments,'query_old':0,'query_new':t,'new_plus_value':y,'new_minus_value':-y,'old_classification_score_both':.25,'new_classification_scores':[.25+y,.25-y],'score_range_change':float(t*n),'note':'Not an arbitrary-sketch lower bound; closes fixed low-order moment summaries without a score-range or margin condition.'}

def main():
    begin=time.time(); cases=[]
    for alpha in (.1,.5,1.):
        for seed in (7,19,41):
            cases.append(run_case(seed=seed,alpha=alpha))
    result={'purpose':'Mechanism rejection/qualification gate, not a benchmark or invention claim','update_identity':update_identity_test(),'moment_collision':moment_collision(),'cases':cases,'elapsed_seconds':time.time()-begin,'numpy':np.__version__}
    (OUT/'attention_edit_gate_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'elapsed_seconds':result['elapsed_seconds'],'identity_max_error':result['update_identity']['max_absolute_error'],'runs':len(cases),'endpoints':[{'alpha':c['alpha'],'seed':c['seed'],'actual':c['history'][-1]['actual_last'],'bounds':{B:round(v['last'],6) for B,v in c['history'][-1]['bounds'].items()},'last_certifiable_layer':{B:max([0]+[r['layer'] for r in c['history'] if r['bounds'][B]['certifies_unit_readout_margin_0_25']]) for B in c['history'][0]['bounds']}} for c in cases]},indent=2))

if __name__=='__main__': main()
