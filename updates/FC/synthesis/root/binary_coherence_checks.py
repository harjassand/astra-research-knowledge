"""Independent finite matrix diagnostics for a written UCP entropy bound."""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import numpy as np


def entropy(matrix):
    eig=np.linalg.eigvalsh(matrix)
    assert eig.min()>-1e-10
    return float(-sum(v*math.log(v) for v in eig if v>0))


def h2(p):
    return -sum(v*math.log(v) for v in [p,1-p] if v>0)


def penalty(p,x):
    r=math.sqrt(max(0,(2*p-1)**2+x*x))
    assert r<=1+1e-9
    return h2(p)-h2((1+min(1,r))/2)


def gibbs(h,beta):
    e,v=np.linalg.eigh(h);weights=np.exp(-beta*(e-e.min()))
    rho=(v*(weights/weights.sum()))@v.conj().T
    return rho,float(-beta*e.min()+math.log(weights.sum()))


def main():
    rng=np.random.default_rng(131026)
    counts=dict(exact_qubit_feasibility=0,complex_choi_states=0,
                entropy_and_partition_bounds=0,confidence_bias_order=0)
    for p,x in [(F(1,10),F(2,5)),(F(1,4),F(1,2)),(F(1,2),F(3,4))]:
        assert p*(1-p)-x*x/4>=0
        counts['exact_qubit_feasibility']+=1
    largest_gain=0.0;smallest_choi=0.0;max_identity_error=0.0
    for n0,n1 in [(1,1),(1,3),(2,3),(4,3)]:
        n=n0+n1
        p0=np.diag([1.0]*n0+[0.0]*n1);p1=np.eye(n)-p0
        for fixture in range(30):
            raw=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
            h=(raw+raw.conj().T)/2
            h[:n0,:n0]+=rng.uniform(-3,3)*np.eye(n0)
            h[n0:,n0:]+=rng.uniform(-3,3)*np.eye(n1)
            d=p0@h@p0+p1@h@p1;t=h-d;b=p0@h@p1
            k=np.linalg.norm(b,2)*(1 if fixture%2 else 1.3)
            beta=[0.2,0.7,1.6][fixture%3]
            rho,logzh=gibbs(h,beta);rhod,logzd=gibbs(d,beta)
            sigma=p0@rho@p0+p1@rho@p1
            p=float(np.trace(p0@rho).real)
            a=-float(np.trace(rho@t).real);x=a/k
            assert a>=-1e-10 and x<=2*math.sqrt(p*(1-p))+1e-9
            choi=np.block([[p0,b/k],[b.conj().T/k,p1]])
            smallest_choi=min(smallest_choi,float(np.linalg.eigvalsh(choi).min()))
            assert np.linalg.eigvalsh(choi).min()>-1e-9
            z=np.trace(rho@b.conj().T)/k
            q=np.array([[p,z],[z.conjugate(),1-p]])
            assert np.linalg.eigvalsh(q).min()>-1e-9
            assert abs(2*k*z.real+a)<1e-9
            direct=entropy(sigma)-entropy(rho)
            lower=penalty(p,x);old=penalty(.5,x)
            assert direct>=h2(p)-entropy(q)-1e-9
            assert direct>=lower-1e-9 and lower>=old-1e-9
            logarithm=logzh-logzd
            new=beta*a-lower;previous=beta*a-old
            assert logarithm>=-1e-9 and logarithm<=new+1e-9
            assert new<=previous+1e-9
            es,vs=np.linalg.eigh(rhod)
            logs=(vs*np.log(es))@vs.conj().T
            relative=-entropy(sigma)-float(np.trace(sigma@logs).real)
            error=abs(logarithm-(beta*a-direct-relative))
            max_identity_error=max(max_identity_error,error)
            assert error<1e-9
            largest_gain=max(largest_gain,lower-old)
            counts['complex_choi_states']+=1
            counts['entropy_and_partition_bounds']+=1
    for lo,hi in [(.05,.2),(.2,.6),(.8,.95)]:
        closest=min(hi,max(lo,.5))
        for p in np.linspace(lo,hi,21):
            for x in np.linspace(0,2*math.sqrt(p*(1-p))*.99,11):
                assert penalty(p,x)>=penalty(closest,x)-1e-10
                counts['confidence_bias_order']+=1
    result=dict(status='PASS',seed=131026,counts=counts,
                maximum_activity_exponent_improvement=largest_gain,
                minimum_choi_eigenvalue_roundoff=smallest_choi,
                maximum_entropy_identity_residual=max_identity_error,
                exact_scope='Three rational qubit positivity determinants only.',
                floating_scope='Finite complex Hermitian eigensolver diagnostics, tolerance1e-9; not outward certificates.',
                boundary='Written proof carries universal statements; no physical data,external review or novelty clearance.')
    Path('binary_coherence_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
