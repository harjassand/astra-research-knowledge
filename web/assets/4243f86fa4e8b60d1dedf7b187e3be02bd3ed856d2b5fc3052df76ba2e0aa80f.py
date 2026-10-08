"""Finite diagnostics for the exact reference-weighted identity, not proof."""
import json
from pathlib import Path
import numpy as np
rng=np.random.default_rng(842713)
max_residual=0.; min_margin=1.; n=32; dim=6
sigma=np.diag([.1,.1,.2,.2,.2,.2]); sq=np.diag(np.sqrt(np.diag(sigma)))
for trial in range(n):
    H=np.zeros((dim,dim),complex)
    for start,k in [(0,2),(2,4)]:
        Z=rng.normal(size=(k,k))+1j*rng.normal(size=(k,k)); Z=(Z+Z.conj().T)/2
        Z-=np.trace(Z)*np.eye(k)/k; Z*=.8/np.linalg.norm(Z,2)
        H[start:start+k,start:start+k]=Z
    L=[np.eye(dim)+H,np.eye(dim)-H]; rho=[sq@v@sq for v in L]
    Z=rng.normal(size=(3*dim,dim))+1j*rng.normal(size=(3*dim,dim))
    V=np.linalg.qr(Z)[0]; kraus=[V[i*dim:(i+1)*dim] for i in range(3)]
    def phi(X): return sum(A@X@A.conj().T for A in kraus)
    def tr(X): return float(np.trace(X).real)
    C=sum(v@v for v in L)/2
    direct=sum(np.linalg.norm(v@(A@sq)-(A@sq)@v,'fro')**2/2 for A in kraus for v in L)
    score=sum(tr(v@(r-phi(r)))/2 for v,r in zip(L,rho))
    correction=tr(C@(phi(sigma)-sigma))/2
    max_residual=max(max_residual,abs(direct/2-score-correction))
    err=sum(np.linalg.norm(phi(r)-r,'nuc')/4 for r in rho)
    min_margin=min(min_margin,err-direct/(3*1.8-1))
assert max_residual<1e-12 and min_margin>=-1e-12
out={'scope':'32 random nonunital TP channels with unequal block reference weights and cross-sector Kraus operators; diagnostic only','fixtures':n,'max_identity_residual':max_residual,'min_risk_bound_margin':min_margin,'passed':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
