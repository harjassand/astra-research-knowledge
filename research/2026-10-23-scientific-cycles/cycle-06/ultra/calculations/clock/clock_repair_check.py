#!/usr/bin/env python3
"""Finite matrix admission of the joint controller and correlated fallback.

This checks the specified receiving interface, not hidden-memory accessibility.
No measurement data, EF optimization, or performance experiment is used.
"""
import itertools, json, math, time
from pathlib import Path
import numpy as np


def tensor(xs):
    ans = np.ones((1,1))
    for x in xs:
        ans = np.kron(ans,x)
    return ans


def pair_states(D):
    v = np.eye(D).reshape(-1)/math.sqrt(D)
    phi = np.outer(v,v)
    nu = np.eye(D*D)/(D*D)
    z = np.zeros(D*D); z[0] = 1
    return phi,nu,np.outer(z,z)


def grouped(a,D,N):
    # Wire order A1 B1 A2 B2 ... -> A1 A2 ... B1 B2 ... .
    perm = [list(itertools.product(range(D),repeat=2*N)).index(
        tuple(itertools.chain.from_iterable(zip(x[:N],x[N:]))))
        for x in itertools.product(range(D),repeat=2*N)]
    return a[np.ix_(perm,perm)]


def comp_readout_Q(a,D,N):
    a=grouped(a,D,N); n=D**N
    q=0.0
    for x in range(n):
        b=a[x*n:(x+1)*n,x*n:(x+1)*n]
        p=float(np.trace(b))
        if p>1e-14:
            vals=np.linalg.eigvalsh(b/p)
            q-=p*sum(v*math.log(v) for v in vals if v>1e-14)
    return q


def matrix_case(D,L,N):
    phi,nu,z=pair_states(D)
    before=np.zeros((D**(2*N),D**(2*N)))
    after=before.copy(); prefixes=[]
    for k in range(1,L+1):
        j=1+((k-N-1)%L)
        recovered=1+((j+N-1)%L)
        assert recovered==k
        pre=tensor([phi if i<=k else nu for i in range(1,N+1)])
        post=tensor([phi if i<=k else z for i in range(1,N+1)])
        # Actual reset Kraus action on one exhausted pair:
        # K_ab=|00><ab|, with every outcome averaged.
        single=np.zeros_like(nu)
        for a in range(D*D):
            K=np.zeros_like(nu); K[0,a]=1
            single+=K@nu@K.T
        assert np.max(abs(single-z))<1e-14
        before+=pre/L; after+=post/L
        # The counted memory and its clock have same conditional state/weight;
        # compare their full block partial traces via output trace exactly here.
        assert abs(np.trace(pre)-np.trace(post))<1e-13
    for i in range(1,N+1):
        effect=tensor([phi]*i+[np.eye(D*D)]*(N-i))
        p=float(np.trace(effect@before)); pp=float(np.trace(effect@after))
        assert pp>=p-1e-13
        formula=(max(L-i+1,0)+sum(D**(-(i-k)) for k in range(1,min(L,i-1)+1)))/L
        assert abs(pp-formula)<1e-13
        prefixes.append([p,pp])
    Q=comp_readout_Q(after,D,N)
    assert abs(Q)<1e-12
    return dict(D=D,L=L,N=N,computational_Q=Q,prefixes=prefixes,
                clock_inverse="PASS",all_reset_Kraus_averaged="PASS")


def correlated_typical_case():
    D,L,N,r,t=2,2,2,2,3
    phi,nu,z=pair_states(D)
    # A global threshold creates genuine correlations BETWEEN the two tasks.
    # It is therefore not sufficient to check two independent marginals.
    total=np.zeros((D**(2*N*r),D**(2*N*r)))
    for ks in itertools.product(range(1,L+1),repeat=r):
        good=sum(ks)<=t
        blocks=[]
        for k in ks:
            # Before receiver: Phi/zero active and nu exhausted. After it,
            # exhausted positions are zero. All fallback branches are included.
            blocks.extend(phi if good and i<=k else z for i in range(1,N+1))
        total+=tensor(blocks)/L**r
    assert abs(np.trace(total)-1)<1e-12
    q=comp_readout_Q(total,D,N*r)
    assert abs(q)<1e-12
    # Directly check support in span{|x>_A |x>_B}, stronger than one entropy.
    g=grouped(total,D,N*r); n=D**(N*r)
    allowed=[x*n+x for x in range(n)]
    projected=np.zeros_like(g); projected[np.ix_(allowed,allowed)]=g[np.ix_(allowed,allowed)]
    assert np.max(abs(g-projected))<1e-14
    return dict(D=D,L=L,N=N,r=r,threshold=t,global_fallback_probability=0.25,
                complete_output_MC_support="PASS",whole_output_computational_Q=q)


def main():
    wall,cpu=time.perf_counter(),time.process_time()
    cases=[matrix_case(*x) for x in [(2,2,2),(2,2,3),(3,2,2)]]
    stable=dict(status="PASS",cases=cases,correlated_typical=correlated_typical_case(),
                scope="Specified controller finite matrix admission, not generic memory access or physical calibration.")
    Path(__file__).with_name("CLOCK_RESULT.json").write_text(json.dumps(stable,indent=2)+"\n")
    timing=dict(wall_seconds=time.perf_counter()-wall,process_cpu_seconds=time.process_time()-cpu,jobs=1,cases=4)
    Path(__file__).with_name("CLOCK_TIMING.json").write_text(json.dumps(timing,indent=2)+"\n")
    print(json.dumps(dict(status="PASS",**timing)))


if __name__=="__main__":
    main()
