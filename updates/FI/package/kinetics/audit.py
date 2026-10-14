import json,time
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import sympy as sp
from model import *
from solve import pcg_tensor
from certify import certify
from tt_ops import dense_for_audit_only
ROOT=Path(__file__).parent

def kron_all(ms):
    a=np.array([[F(1)]],dtype=object)
    for m in ms:a=np.kron(a,m)
    return a

def check_small(seed=11,B=3,m=2,context=False):
    checks=0;truth=fixture(B=B,m=m,rarity=1,seed=seed)
    if context:truth=add_context_clock(truth,F(1,10))
    learn,tr=acquire(truth);gs,pp=discover_partition(learn,max_local_bits=m);c=Compiler(learn,gs);dims=[len(p) for p in c.prob];N=int(np.prod(dims))
    A=sum((kron_all(ms) for ms in c.rawterms),np.full((N,N),F(0),dtype=object));C=np.full_like(A,F(0))
    for b,M in enumerate(c.refraw):C+=kron_all([M if b==j else eye(d) for j,d in enumerate(dims)])
    rho=[];ww=[];statephys=[]
    for aa in np.ndindex(*dims):
        p=F(1);x=0
        for b,a in enumerate(aa):
            p*=c.prob[b][a]
            for j,node in enumerate(gs[b]):x|=int(c.bits[b][a,j])<<node
        w=F(1)
        for b,s,d,t,g in c.cross:w*=(g if c.bits[b][aa[b],s]==c.bits[d][aa[d],t] else F(1))/min(F(1),g)
        rho.append(p);ww.append(w);statephys.append(x)
    inv={x:j for j,x in enumerate(statephys)}
    for j,x in enumerate(statephys):
        total=F(0)
        for i in range(learn['n']):
            xp=x^(1<<i);jp=inv[xp];mx=weight(truth,x);mp=weight(truth,xp);nu=truth['nu'][i]
            if context:
                z=sum(((x>>node)&1)<<k for k,node in enumerate(truth['clock_contexts'][i]));nu=truth['clock_tables'][i][z]
            q=nu*mp/(mx+mp)
            assert A[j,jp]==-ww[j]*q;checks+=1;total+=q
            ratio=A[j,jp]/C[j,jp];assert 1<=ratio<=c.R;checks+=1
            assert rho[j]*A[j,jp]==rho[jp]*A[jp,j];checks+=1
        kill=learn['kappa']*((x>>learn['target'])&1)
        assert A[j,j]==ww[j]*(total+kill);checks+=1
        assert sum(A[j,:])==ww[j]*kill;checks+=1
    assert sum(p*w for p,w in zip(rho,ww))==c.Z;checks+=1
    W=np.diag(np.array(rho,dtype=object));rng=np.random.default_rng(seed)
    for k in range(10):
        z=np.array([F(int(x),7) for x in rng.integers(-5,6,N)],dtype=object)
        ac=z@(W@A)@z;cc=z@(W@C)@z;assert cc<=ac<=c.R*cc;checks+=1
    results={'states':N,'checks':checks}
    if N<=16:
        AA=sp.Matrix(A);bb=sp.Matrix(ww);u=AA.inv()*bb
        mean=sum(p*w*F(u[j]) for j,(p,w) in enumerate(zip(rho,ww)))/c.Z
        v,log=pcg_tensor(c,rank=4,iterations=8);cert=certify(c,v);assert F(cert['lower'])<=mean<=F(cert['upper']);checks+=1
        # Exact preconditioned contraction, including noncommuting actual/reference forms.
        CC=sp.Matrix(C);invC=CC.inv();step=F(2)/(1+c.R);q=(c.R-1)/(c.R+1)
        for k in range(6):
            z=sp.Matrix([sp.Rational(int(x),9) for x in rng.integers(-4,5,N)]);ep=z-step*invC*AA*z
            en=(z.T*sp.Matrix(W)*CC*z)[0];ee=(ep.T*sp.Matrix(W)*CC*ep)[0];assert ee<=q*q*en;checks+=1
        results.update(exact_mean=str(mean),candidate_ratio=cert['ratio_float'],checks=checks)
    return results

def replay(name,transcript_name=None):
    tr=json.load(open(ROOT/((transcript_name or name)+'_transcript.json')))
    # Solve 1+n+n(n-1)/2 = query count exactly, avoiding float identification.
    n=next(k for k in range(1,200) if 1+k+k*(k-1)//2==tr['energy_queries'])
    learn=from_transcript(n,tr);gs,_=discover_partition(learn);c=Compiler(learn,gs)
    a=np.load(ROOT/(name+'.npz'));v=[a[str(i)] for i in range(c.B)];ans=certify(c,v)
    old=json.load(open(ROOT/(name+'.json')))
    assert F(ans['lower'])==F(old['lower']) and F(ans['upper'])==F(old['upper'])
    return {'name':name,'ratio':ans['ratio_float'],'seconds':ans['seconds'],'exact_endpoint_matches':2,'private_truth_used':False}

def main():
    start=time.perf_counter();small=[check_small(11,B=2,m=2),check_small(23,B=2,m=2,context=True),check_small(7,B=3,m=2),check_small(19,B=3,m=2,context=True)]
    replays=[replay('primary_r2'),replay('pcg_primary_r3','primary_r3'),replay('context_rare'),replay('strong_repair')]
    # Context tomography must detect a model that identical energy and all-zero probes cannot.
    a=json.load(open(ROOT/'primary_r2_transcript.json'));b=json.load(open(ROOT/'context_100_transcript.json'))
    assert a['weights']==b['weights']
    assert all(F(a['balanced_rates'][str(i)])==F(b['balanced_rates'][f'{i}:0']) for i in range(18))
    extra=1+18
    from response_ambiguity import main as ambiguity
    ambiguity();amb=json.load(open(ROOT/'response_ambiguity.json'))
    out={'small_models':small,'replays':replays,'exact_assertions':sum(x['checks'] for x in small)+sum(x['exact_endpoint_matches'] for x in replays)+extra+amb['exact_assertions'],'seconds':time.perf_counter()-start,'scope':'same-session algebra and deterministic replay; not external or formal review'}
    json.dump(out,open(ROOT/'audit_results.json','w'),indent=2);print(json.dumps(out,indent=2))
if __name__=='__main__':main()
