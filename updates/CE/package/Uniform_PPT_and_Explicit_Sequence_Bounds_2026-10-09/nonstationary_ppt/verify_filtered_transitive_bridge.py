"""Bounded numerical check of the rectangular filtered transitivity bridge.
Not a proof. Uses the published DMR Example 2.2 transitive 4x4 space,
whose square is not the full matrix space, and independently varying
unitarily transformed seeds. All seeds/filters are Choi-trace normalized.
"""
import json
from pathlib import Path
import numpy as np
rng=np.random.default_rng(20261009)
d=4

def make_seed():
    out=[]
    for k in range(8):
        a,b,c,e0,e,f,g,h=np.eye(8)[k]
        # e0 denotes the source variable d, avoiding dimension-name overlap.
        out.append(np.array([[a,b,h,2*g],[c,e0,f,e],[e,f,a,b],[g,h,c,e0]],complex))
    q=lambda: np.linalg.qr(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))[0]
    U,V=q(),q()
    out=[U@K@V for K in out]
    scale=np.sqrt(sum(np.vdot(K,K).real for K in out))
    return [K/scale for K in out]

def superop(ks): return sum(np.kron(K.conj(),K) for K in ks)
def choi(S):
    J=np.zeros((d*d,d*d),complex)
    for a in range(d):
        for b in range(d):
            E=np.zeros((d,d));E[a,b]=1
            Y=(S@E.reshape(-1,order='F')).reshape((d,d),order='F')
            J += np.kron(Y,E)
    return (J+J.conj().T)/2

def filt(rank,ill=False):
    U=np.linalg.qr(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))[0]
    V=np.linalg.qr(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))[0]
    vals=np.zeros(d);vals[:rank]=np.geomspace(1,1e-9,rank) if ill else rng.uniform(.5,1,rank)
    A=U@np.diag(vals)@V
    return A/np.linalg.norm(A)

patterns=[[1,1,1],[1,2,3],[2,2,2],[2,3,4],[3,3,3],[4,4,4]]
records=[]
for varying in [False,True]:
    for ill in [False,True]:
        for ranks in patterns:
            seeds=[make_seed() for _ in range(d)]
            if not varying:seeds=[seeds[0]]*d
            Ss=[superop(K) for K in seeds]
            filters=[filt(r,ill) for r in ranks]
            S=Ss[0]
            for j,A in enumerate(filters):S=Ss[j+1]@superop([A])@S
            ev=np.linalg.eigvalsh(choi(S))
            records.append(dict(varying_seeds=varying,ill_conditioned=ill,filter_ranks=ranks,min_choi_eigenvalue=float(ev[0]),max_choi_eigenvalue=float(ev[-1]),relative_min=float(ev[0]/ev[-1]),full_rank=bool(ev[0]>1e-11*ev[-1])))
assert all(x['full_rank'] for x in records)
result=dict(seed=20261009,dimension=d,cases=len(records),all_full_choi_rank=True,min_relative_eigenvalue=min(x['relative_min'] for x in records),scope='Numerical support for d strictly-positive seeds separated by singular or ill-conditioned filters. No PPT assumption is made on these test seeds.',records=records)
out=Path(__file__).with_name('filtered_transitive_bridge_verification.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
