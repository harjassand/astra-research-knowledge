"""Deterministic finite checks of the analytic polar reduction; no optimization."""
from pathlib import Path
import numpy as np, json

def norm2(x): return float(np.vdot(x,x).real/x.shape[0])
def absolute(x):
    u,s,vh=np.linalg.svd(x)
    return (vh.conj().T*s)@vh, (u*s)@u.conj().T, s

def expectation(x,D,N,r,a,i):
    sites=N*r
    chosen=list(range(a*N,a*N+i))
    rest=[j for j in range(sites) if j not in chosen]
    perm=chosen+rest+[sites+j for j in chosen+rest]
    k=D**i; h=D**(sites-i)
    z=x.reshape([D]*(2*sites)).transpose(perm).reshape(k,h,k,h)
    red=np.einsum('abad->bd',z)/k
    e=np.einsum('ac,bd->abcd',np.eye(k),red).reshape([D]*(2*sites))
    return e.transpose(np.argsort(perm)).reshape(x.shape)

def ent(s,d):
    p=s*s/d; p=p[p>1e-13]
    return float(-sum(p*np.log(p)))

rows=[]
for D,N,r in [(2,2,2),(2,3,2),(3,2,2)]:
    d=D**(N*r)
    j,k=np.indices((d,d))
    x=np.cos((j+1)*(k+2)*0.37)+1j*np.sin((j+3)*(k+1)*0.19)
    x=x/np.sqrt(norm2(x))
    p,q,s=absolute(x)
    totals=np.zeros(3)
    min_margin=float('inf')
    for a in range(r):
        for i in range(1,N+1):
            vals=[norm2(expectation(z,D,N,r,a,i)) for z in [x,p,q]]
            totals+=vals
            margin=np.sqrt(vals[1]*vals[2])-vals[0]
            min_margin=min(min_margin,margin)
            assert margin>=-1e-10
    assert totals[0]<=np.sqrt(totals[1]*totals[2])+1e-10
    assert np.isclose(norm2(p),1) and np.isclose(norm2(q),1)
    assert np.allclose(np.linalg.svd(p,compute_uv=False),s)
    assert np.allclose(np.linalg.svd(q,compute_uv=False),s)
    rows.append({'D':D,'N':N,'r':r,'matrix_dimension':d,'sum_prefixes_X':float(totals[0]),'sum_prefixes_absX':float(totals[1]),'sum_prefixes_absXstar':float(totals[2]),'smallest_pointwise_geometric_margin':min_margin,'same_entropy':ent(s,d)})
result={'scope':'checks of proved polar reduction only; not tests settling tensor conjecture','assertions':'PASS','cases':rows}
out=Path(__file__).with_name('COMPUTE_RECEIPT.json'); out.write_text(json.dumps(result,indent=2)+'\n'); print(out.read_text())
