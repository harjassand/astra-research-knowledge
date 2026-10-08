"""New JOINT_CAPTURE root/energy/frame-moment conventions, not proof.

Reuses the exact small polar matrices; never reruns their old test suite.
One BLAS thread is sufficient. No iid, novelty or external validation.
"""
import json
import math
from pathlib import Path

import numpy as np

from check_transverse_gram import matrices


def hs2(x):
    return float(np.vdot(x, x).real)


def comm(a, b):
    return a @ b-b @ a


def spin_generators(k):
    sp=np.zeros((k+1,k+1))
    for ell in range(1,k+1):
        sp[ell-1,ell]=math.sqrt(ell*(k-ell+1))
    return [(sp+sp.T)/2,(sp-sp.T)/(2j),
            np.diag([k/2-ell for ell in range(k+1)])]


def root_and_energy(k,m,cutoff,rng):
    a,num,spin,ps,gram,dyson,bd,phys=matrices(k,m,cutoff+1)
    nf=num.shape[0]//(k+1)
    pns=[np.diag((np.diag(num)==n).astype(float)) for n in range(cutoff+2)]
    e12=spin[0][1]-a[1].T@a[0]
    jz=(spin[0][0]-spin[1][1]-a[0].T@a[0]+a[1].T@a[1])/2
    total=jz@jz+(e12@e12.T+e12.T@e12)/2
    alpha=np.zeros(num.shape)
    beta=np.zeros(num.shape)
    g=np.zeros(num.shape)
    for (s,n),proj in ps.items():
        g+=(s*(k+n+1-s)-n*(n-1)/2)*proj
        aa=math.sqrt(m-n+s)
        bb=math.sqrt(m+k+1-s)
        alpha+=(m+aa*bb)/(aa+bb)*proj
        beta+=proj/(aa+bb)
    ds=[comm(g,x.T) for x in a]
    x=[[spin[i][j]-(m*np.eye(num.shape[0]) if i==j else 0)
        for j in (0,1)] for i in (0,1)]
    formula_error=first_error=0.
    for i in (0,1):
        for n in range(cutoff+1):
            formula_error=max(formula_error,
                float(np.linalg.norm((a[i].T@alpha+ds[i]@beta-bd[i])@pns[n])))
            explicit=sum(a[j].T@(x[j][i]-(num if j==i else 0)) for j in (0,1))
            first_error=max(first_error,float(np.linalg.norm((ds[i]-explicit)@pns[n])))
    assert formula_error<1e-9
    assert first_error<1e-9

    fixtures=[]
    rmat=[(q,np.diag([max(0.,1-ell/q) for ell in range(k+1)]))
          for q in range(1,k+1)]
    rmat.append((k+1,np.eye(k+1)))
    random=rng.normal(size=(k+1,k+1))+1j*rng.normal(size=(k+1,k+1))
    rmat.append(('random-Hermitian',(random+random.conj().T)/2))
    js=spin_generators(k)
    moment_error=0.
    for label,rsmall in rmat:
        r=np.kron(rsmall,np.eye(nf))
        e2=sum(hs2(comm(j,rsmall)) for j in js)
        sr=hs2(rsmall)
        for n in range(cutoff+1):
            actual=hs2(comm(total,r)@pns[n])
            expected=(n+1)*n*(n+2)*e2/3
            moment_error=max(moment_error,abs(actual-expected))
            coupling=sum(hs2(comm(b,r)@pns[n]) for b in bd)
            bound=3*(n+1)*(n+2)*e2/m
            assert coupling<=bound+1e-8
            fixtures.append({'R':label,'N':n,'coupling':coupling,'bound':bound})
        if label=='random-Hermitian':
            continue
        f=np.diag([max(0.,(cutoff+1-n)/(cutoff+1))
                   for n in np.diag(num)])
        seed=r@f
        s=hs2(seed)
        ext=sum(hs2(comm(b,seed)) for b in bd)
        internal=sum(hs2(comm(jphys,seed)) for jphys in
                     ((e12+e12.T)/2,(e12-e12.T)/(2j),jz))
        sk=(cutoff+2)**2*(cutoff+3)/(12*(cutoff+1))
        assert abs(s-sr*sk)<1e-8
        assert abs(internal-sk*e2)<1e-8
        bound=8*(m+k)/(cutoff+2)+6*(cutoff+2)*e2/(m*sr)
        assert ext/s<=bound+1e-8
    assert moment_error<1e-7
    return {'k':k,'m':m,'K':cutoff,'root_error':formula_error,
            'first_commutator_error':first_error,'casimir_moment_error':moment_error,
            'coupling_cases':fixtures}


def weighted_frame(k,m):
    a,num,spin,ps,gram,dyson,bd,phys=matrices(k,m,k+m+1)
    nf=num.shape[0]//(k+1)
    d=(k+1)*(m+1)*(m+k+2)/2
    ratio=(k+1)/d
    cases=[]
    max_scalar_error=0.
    for n in range(min(3,m)+1):
        unweighted={s:0. for s in range(min(k,n)+1)}
        weighted={s:0. for s in range(min(k,n)+1)}
        for q in range(k+1):
            chi=np.zeros(num.shape[0])
            chi[q*nf]=1.
            for step in range(n):
                chi=bd[0]@chi
                chi/=np.linalg.norm(chi)
            trials=m+k-q
            w0=2*(n+1)/((trials+1)*(trials+2))
            w1=w0*(n+2)/(trials+3)
            for s in unweighted:
                proj=ps[s,n]
                dim=k+n-2*s+1
                mass=float(np.vdot(chi,proj@chi).real)
                unweighted[s]+=w0*mass/dim
                weighted[s]+=w1*mass/dim
        for s in unweighted:
            max_scalar_error=max(max_scalar_error,abs(unweighted[s]-ratio))
            assert abs(unweighted[s]-ratio)<1e-10
            bound=(n+2)/(m+3)*ratio
            assert weighted[s]<=bound+1e-10
            cases.append({'N':n,'s':s,'unweighted':unweighted[s],
                          'weighted':weighted[s],'bound':bound})
    return {'k':k,'m':m,'max_unweighted_scalar_error':max_scalar_error,'cases':cases}


def main():
    rng=np.random.default_rng(481516)
    roots=[root_and_energy(k,m,cutoff,rng)
           for k in (0,1,3) for m in (16,32) for cutoff in (0,2,3)]
    frames=[weighted_frame(k,m) for k,m in ((0,2),(1,3),(2,4),(3,4))]
    record={'status':'FINITE-EVIDENCE',
            'scope':'Exact joint root formula, first commutator, spin-Casimir moment, coupling/energy upper and weighted-frame operator convention only',
            'root_carrier_cutoffs':len(roots),'weighted_frame_carriers':len(frames),
            'max_root_error':max(x['root_error'] for x in roots),
            'max_first_commutator_error':max(x['first_commutator_error'] for x in roots),
            'max_casimir_moment_error':max(x['casimir_moment_error'] for x in roots),
            'max_unweighted_frame_error':max(x['max_unweighted_scalar_error'] for x in frames),
            'root_cases':roots,'weighted_frame_cases':frames,
            'asymptotic_or_external_validation':False,'old_tests_rerun':False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ('root_cases','weighted_frame_cases')},indent=2))


if __name__=='__main__':
    main()
