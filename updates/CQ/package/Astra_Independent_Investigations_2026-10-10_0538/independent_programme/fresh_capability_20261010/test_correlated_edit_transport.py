"""Check the exact second-layer JVP and why score low rank does not suffice.
No complexity lower bound is inferred from numerical matrix rank.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np, json
from pathlib import Path

def soft(s):
    e=np.exp(s-s.max(axis=1)[:,None]); return e/e.sum(axis=1)[:,None]

def run(seed,n=40,d=12):
    rng=np.random.default_rng(seed)
    X=rng.normal(size=(n,d))
    Wq,Wk,Wv=[rng.normal(size=(d,d))/np.sqrt(d) for _ in range(3)]
    Q,K,V=X@Wq,X@Wk,X@Wv
    P1=soft(rng.normal(size=(n,d))@rng.normal(size=(d,n))/np.sqrt(d)); a=P1[:,n//3]
    # This is the rank-one hidden-state change produced by a value-only edit
    # to a single token in the preceding attention layer.
    u=rng.normal(size=d); u/=np.linalg.norm(u)
    dQ=np.outer(a,u@Wq); dK=np.outer(a,u@Wk); dV=np.outer(a,u@Wv)
    S=Q@K.T/np.sqrt(d); P=soft(S)
    dS=(dQ@K.T+Q@dK.T)/np.sqrt(d)
    dP=P*(dS-(P*dS).sum(axis=1)[:,None])
    dO=dP@V+P@dV
    h=1e-5
    plus=soft((Q+h*dQ)@(K+h*dK).T/np.sqrt(d))@(V+h*dV)
    minus=soft((Q-h*dQ)@(K-h*dK).T/np.sqrt(d))@(V-h*dV)
    fd=(plus-minus)/(2*h)
    svS=np.linalg.svd(dS,compute_uv=False); svP=np.linalg.svd(dP,compute_uv=False)
    rankS=int(np.sum(svS>svS[0]*1e-10)); rankP=int(np.sum(svP>svP[0]*1e-10))
    assert rankS<=2; assert rankP==n-1; assert np.max(np.abs(fd-dO))<1e-8
    # Mixed-moment decomposition; three P applications to NEW operands.
    t=K@(u@Wq); z=Q@(u@Wk)
    term_values=(P@a)[:,None]*(u@Wv)[None,:]
    term_queries=a[:,None]*((P@(t[:,None]*V))-(P@t)[:,None]*(P@V))/np.sqrt(d)
    term_keys=z[:,None]*((P@(a[:,None]*V))-(P@a)[:,None]*(P@V))/np.sqrt(d)
    reconstructed=term_values+term_queries+term_keys
    mixederr=float(np.max(np.abs(reconstructed-dO))); assert mixederr<1e-12
    return {'seed':seed,'n':n,'d':d,'hidden_edit_rank':1,'score_derivative_rank':rankS,'probability_derivative_rank':rankP,'smallest_nonzero_probability_singular_ratio':float(svP[-2]/svP[0]),'finite_difference_max_error':float(np.max(np.abs(fd-dO))),'mixed_moment_identity_max_error':mixederr,'new_required_operands':['P @ a','P @ (a[:,None]*V)','P @ (t[:,None]*V)'],'note':'Full rank is not a runtime lower bound. The first-layer exact update itself handles a full-rank probability change cheaply. The issue here is edit-dependent mixed products absent from the ordinary cache.'}

if __name__=='__main__':
    res={'cases':[run(s) for s in (7,19,41,83,137)],'claim':'Correlated rank-one state perturbations already generate generally full-rank probability derivatives. No subquadratic cached transport is obtained.'}
    Path(__file__).with_name('correlated_edit_transport_results.json').write_text(json.dumps(res,indent=2)+'\n')
    print(json.dumps(res,indent=2))
