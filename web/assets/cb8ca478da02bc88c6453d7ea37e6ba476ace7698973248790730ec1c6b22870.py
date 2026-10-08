"""Exact finite algebra replay plus separately labelled numeric controls.
The general proof is in CLIFFORD_FACTOR_TWO.txt, not inferred from tests.
"""
import json
from pathlib import Path
import sympy as s
import numpy as np


def generators(n):
    X=s.SparseMatrix([[0,1],[1,0]])
    Y=s.SparseMatrix([[0,-s.I],[s.I,0]])
    Z=s.diag(1,-1)
    I=s.eye(2)
    gs=[]
    for k in range(n):
        for a in [X,Y]:
            gs.append(s.SparseMatrix(s.kronecker_product(*([Z]*k+[a]+[I]*(n-k-1)))))
    gs.append(s.SparseMatrix(s.kronecker_product(*([Z]*n))))
    return gs


def is_zero(M):
    return all(v==0 for v in M.values())


rows=[]
for q in range(2,6):
    n=q//2
    gs=generators(n)[:q]
    d=2**n
    eye=s.eye(d)
    ss=[s.SparseMatrix(s.kronecker_product(a.T,a,eye)) for a in gs]
    zs=[s.SparseMatrix(s.kronecker_product(eye,a,a)) for a in gs]
    W=sum((s.SparseMatrix(s.kronecker_product(a.T,a,eye)+s.kronecker_product(a.T,eye,a)) for a in gs),s.zeros(d**3))
    eye3=s.eye(d**3)
    identities=[]
    identities.append(is_zero(s.SparseMatrix(W-sum((ss[i]*(eye3+zs[i]) for i in range(q)),s.zeros(d**3)))))
    for i in range(q):
        for j in range(q):
            identities.append(is_zero(ss[i]*ss[j]-ss[j]*ss[i]))
            identities.append(is_zero(zs[i]*zs[j]-zs[j]*zs[i]))
            identities.append(is_zero(ss[i]*zs[j]-((-1)**(i!=j))*zs[j]*ss[i]))
    if q%2==0:
        fs=[]
        for i in range(q):
            f=s.SparseMatrix(eye3)
            for j in range(q):
                if j!=i:f=f*ss[j]
            fs.append(f)
        P=s.SparseMatrix(eye3)
        for f in fs:P=P*f
        L=sum((fs[i]*(eye3+zs[i])/2 for i in range(q)),s.zeros(d**3))
        identities.append(is_zero(s.SparseMatrix(W-2*P*L)))
        identities.append(is_zero(s.SparseMatrix(W*W-4*L.conjugate().T*L)))
        for i in range(q):
            for j in range(q):
                identities.append(is_zero(fs[i]*zs[j]-((-1)**(i==j))*zs[j]*fs[i]))
    else:
        ps=s.SparseMatrix(eye3);pz=s.SparseMatrix(eye3)
        for i in range(q):ps=ps*ss[i];pz=pz*zs[i]
        identities.append(is_zero(ps-eye3))
        identities.append(is_zero(pz-((-1)**(q*(q-1)//2))*eye3))
    wn=np.array(W.tolist(),complex)
    top=float(np.linalg.eigvalsh(wn)[-1])
    row={'q':q,'d':d,'exact_identities_checked':len(identities),
         'all_exact_identities_pass':all(identities),
         'numeric_top_eigenvalue':top,
         'proved_formula':str(s.sqrt(q*(q+2)) if q%2==0 else q+1),
         'status':'EXACT_FINITE_ALGEBRA_PLUS_FLOATING_POINT_SPECTRUM'}
    rows.append(row)
    print(json.dumps(row),flush=True)
    assert all(identities)
Path(__file__).with_name('clifford_replay.json').write_text(json.dumps(rows,indent=2)+'\n')
