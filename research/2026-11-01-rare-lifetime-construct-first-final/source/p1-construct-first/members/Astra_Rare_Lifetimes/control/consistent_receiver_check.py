"""Executed rare-sector receiver and a nonlinear-mask failure.

The fixed source is accessed only through counted vector actions. Dense truth is
used only in the N=128 auditor. Results are floating diagnostics, not interval
certification. Scientific guarantees are proved in consistent_receiver.md.
"""
import json, math, time
from pathlib import Path
import numpy as np
from scipy.fft import dct
from scipy.special import betainc


class FixedSource:
    def __init__(self, u, diag, delta=1.0):
        self.u, self.diag, self.delta = u, diag, delta
        self.calls = 0
    def action(self, v):
        self.calls += v.shape[1] if v.ndim == 2 else 1
        return ((2*self.delta+self.diag)[:,None]*v
                -self.delta*self.u@(self.u.T@v))


class MaskedSource:
    def __init__(self, e, u, eta, delta=1.0):
        self.e, self.u, self.eta, self.delta = e, u, eta, delta
        self.calls, self.escapes = 0, 0
    def action(self, v):
        self.calls += v.shape[1]
        z=self.u@v
        excess=np.maximum(self.delta*np.abs(z)-self.eta*np.linalg.norm(v,axis=0),0)
        self.escapes += int(np.count_nonzero(excess))
        return (2*self.delta*v-self.delta*self.e[:,None]*(self.e@v)[None,:]
                -self.u[:,None]*(np.sign(z)*excess)[None,:])


def parameters(n, eta=0.1, delta=1.0, failure=0.05, eps=0.01, s=32):
    t=math.sqrt(2*math.log(4/failure))
    a0=math.sqrt(s)-math.sqrt(2)-t
    assert a0>0
    k=math.sqrt(n)+math.sqrt(s)+t
    tau=min(0.25,eps*a0/(4*k))
    a=2*eta/(delta+2*eta)
    h=0.5-a
    m=math.ceil(math.log(1/tau)/(2*h*h))
    if not m%2: m+=1
    return dict(s=s,a0=a0,tau=tau,m=m,threshold=3*a0/8,
                epsilon=eps,failure=failure)


def coeffs(m):
    theta=np.pi*(np.arange(m+1)+0.5)/(m+1)
    vals=betainc((m+1)/2,(m+1)/2,(np.cos(theta)+1)/2)
    c=dct(vals,type=2)/(m+1)
    c[0]/=2
    return c


def acquire(source,n,rng,eta=0.1,delta=1.0):
    p=parameters(n,eta,delta)
    g=rng.standard_normal((n,p['s']))
    c=coeffs(p['m'])
    def xact(v):
        return (3*delta*v-2*source.action(v))/(delta+2*eta)
    bnext=c[-1]*g
    bafter=np.zeros_like(g)
    for j in range(len(c)-2,0,-1):
        b=2*xact(bnext)-bafter+c[j]*g
        bafter,bnext=bnext,b
    y=xact(bnext)-bafter+c[0]*g
    left,sv,_=np.linalg.svd(y,full_matrices=False)
    r=int(np.count_nonzero(sv>p['threshold']))
    return left[:,:r],sv,p,y,g,c


def state_error(true_u, learned_u, x, n):
    r=true_u.shape[1]
    if learned_u.shape[1]!=r:
        return None,None
    cosines=np.linalg.svd(true_u.T@learned_u,compute_uv=False)
    sines=np.sqrt(np.maximum(0,1-np.minimum(1,cosines)**2))
    return float((x-1)*sines.sum()/(n+r*(x-1))),float(sines.max())


def main():
    rng=np.random.default_rng(314159)
    rows=[]
    eta=0.1
    for n in [128,4096,16384]:
        for r in [1,2]:
            u=np.linalg.qr(rng.standard_normal((n,r)),mode='reduced')[0]
            diag=rng.uniform(-eta,eta,n)
            diag[0]=eta
            src=FixedSource(u,diag)
            start=time.perf_counter()
            learned,sv,p,y,g,c=acquire(src,n,rng,eta)
            elapsed=time.perf_counter()-start
            terr,perr=state_error(u,learned,n,n)
            assert learned.shape[1]==r
            bound=r*(n-1)/(n+r*(n-1))*(eta/(1-eta)+p['epsilon'])
            assert terr<=bound+1e-10
            audit=None
            if n==128:
                b=np.diag(2+diag)-u@u.T
                ev,w=np.linalg.eigh(b)
                tv=((2+eta)-ev)/(1+2*eta)
                exact=w@(betainc((p['m']+1)/2,(p['m']+1)/2,tv)[:,None]*(w.T@g))
                audit=float(np.linalg.norm(y-exact)/np.linalg.norm(exact))
                assert audit<1e-10
            rows.append(dict(kind='fixed_symmetric_bias',N=n,rank=r,
                learned_rank=learned.shape[1],source_vector_calls=src.calls,
                filter_degree=p['m'],Gaussian_columns=p['s'],
                filter_tolerance=p['tau'],threshold=p['threshold'],
                leading_singular_values=sv[:4].tolist(),
                subspace_operator_error=perr,
                Gibbs_half_trace_error_at_x_N=terr,
                Gibbs_error_bound=bound,
                dense_audit_relative_output_error=audit,
                seconds=elapsed,
                dense_auditor_calls_included=False))
    n=16384
    u=np.linalg.qr(rng.standard_normal((n,2)),mode='reduced')[0]
    masked=MaskedSource(u[:,0],u[:,1],eta)
    learned,sv,p,*_=acquire(masked,n,rng,eta)
    assert masked.escapes==0
    assert learned.shape[1]==1
    rows.append(dict(kind='nonlinear_mask_contract_failure',N=n,
        true_rank=2,learned_rank=learned.shape[1],
        source_vector_calls=masked.calls,escaped_queries=masked.escapes,
        lower_bound_log_q_at_delta_005=math.log(0.45)+(n-1)*eta**2/2,
        relative_partition_gap_at_x_N=(n-1)/(2*n-1),
        mean_energy_gap_at_x_N=n*n/((2*n-1)*(3*n-2)),
        note='No conflict with positive theorem: this globally bounded-error oracle is nonlinear.'))
    result=dict(scope='Floating executable diagnostic; exact proofs and qualification are in the companion notes.',
                seed=314159,rows=rows)
    path=Path(__file__).with_name('consistent_receiver_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
