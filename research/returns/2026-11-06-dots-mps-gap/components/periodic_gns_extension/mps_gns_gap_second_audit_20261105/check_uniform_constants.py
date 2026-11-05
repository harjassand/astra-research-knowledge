"""Independent finite-rank checks for growing-support MPS comparisons.
No imports from either candidate proof or its numerical programs.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json
from pathlib import Path
import numpy as np

def hp(a,p):
    w,u=np.linalg.eigh((a+a.conj().T)/2)
    assert w.min()>-1e-12
    return (u*np.maximum(w,0)**p)@u.conj().T

def test(seed):
    d=3;D=2;rng=np.random.default_rng(seed)
    A=rng.normal(size=(d,D,D))+1j*rng.normal(size=(d,D,D))
    S=sum(a@a.conj().T for a in A)
    w,u=np.linalg.eigh(S);inv=(u*w**-.5)@u.conj().T
    A=np.einsum('ab,sbc->sac',inv,A)
    T=sum(np.kron(a,a.conj()) for a in A)
    sig=np.eye(D)/D
    for _ in range(10000):
        nxt=sum(a.conj().T@sig@a for a in A)
        if np.linalg.norm(nxt-sig)<1e-14:break
        sig=nxt
    sig=nxt/np.trace(nxt)
    Gi=np.kron(np.eye(D),sig); Wi=np.kron(sig.T,np.eye(D))
    F=np.eye(D*D).reshape(D,D,D,D).transpose(1,0,2,3).reshape(D*D,D*D)
    def gram(k):
        g=np.linalg.matrix_power(T,k).reshape(D,D,D,D).transpose(1,3,0,2).reshape(D*D,D*D)
        return (g+g.conj().T)/2
    out=[]
    for b in [2,4,8,12]:
        Gb=gram(b);Wb=F@Gb.T@F
        eps=np.linalg.norm(Gb-Gi,2)
        relative_delta=eps/np.linalg.eigvalsh(sig).min()
        assert np.linalg.eigvalsh(Wb-(1-relative_delta)*Wi).min()>-2e-11
        for k in [2,5,20,100,1000]:
            Gk=gram(k);R=hp(Gk,.5)
            Z=np.trace(Gk@Wb).real
            diff=R@(Wb/Z-Wi)@R
            distance=np.linalg.norm(diff,ord='nuc')
            bound=2*D*eps/Z
            singular=np.linalg.svd(R@F@hp(Gb,.5).T/np.sqrt(Z),compute_uv=False)
            lower=np.sqrt(np.linalg.eigvalsh(Gk).min()*np.linalg.eigvalsh(Gb).min()/Z)
            assert Z>.5
            assert distance<=bound+2e-11
            assert singular.min()+2e-12>=lower
            assert abs(np.trace(Gk@Wi)-1)<2e-11
            out.append(dict(buffer=b,core=k,normalization=float(Z),trace_distance=float(distance),bound=float(bound),schmidt_min=float(singular.min()),schmidt_lower_bound=float(lower),relative_delta=float(relative_delta),relative_positive_bound_nontrivial=bool(relative_delta<1)))
    return dict(seed=seed,sigma_eigenvalues=np.linalg.eigvalsh(sig).tolist(),cases=out)

if __name__=='__main__':
    out=[test(s) for s in [479,3031,17073]]
    Path(__file__).with_name('uniform_constants_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('Passed',sum(len(r['cases']) for r in out),'cases with core supports up to 1000 sites.')
    print('Max distance/bound',max(c['trace_distance']/c['bound'] for r in out for c in r['cases']))
