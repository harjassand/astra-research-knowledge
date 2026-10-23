"""Deterministic checks of the exact family in RESULT.txt, not an optimizer."""
import json, math
import numpy as np
from pathlib import Path

def conditional_expectation_prefix(x, d, D, i):
    k=D**i
    h=d//k
    # Matrix order: S_prefix, S_suffix, R on both rows and columns.
    a=x.reshape(k,h,d,k,h,d)
    z=np.einsum('abcade->bcde',a)/k
    return np.einsum('af,bcde->abcfde',np.eye(k),z).reshape(d*d,d*d)

def ent_tau(z):
    vals=np.linalg.eigvalsh(z)
    vals=vals[vals>1e-12]
    return float(np.sum(vals*np.log(vals))/z.shape[0])

rows=[]
for D,N in [(2,1),(2,2),(2,3),(3,1),(3,2)]:
    d=D**N
    v=np.eye(d).reshape(-1)/np.sqrt(d)
    X=d*np.outer(v,v)
    Y=X@X
    reduced=np.trace(Y.reshape(d,d,d,d),axis1=0,axis2=2)/d
    entropy=ent_tau(Y)-ent_tau(reduced)
    p=[]
    for i in range(1,N+1):
        e=conditional_expectation_prefix(X,d,D,i)
        p.append(float(np.trace(e.T@e)/(d*d)))
    expected=[D**(-2*i) for i in range(1,N+1)]
    assert np.allclose(p,expected,atol=1e-12)
    assert np.isclose(entropy,2*N*math.log(D))
    energy=math.log(D)*sum(1-q for q in p)
    rows.append({'D':D,'N':N,'dimension_matrix':d*d,'norm2_tau':float(np.trace(Y)/(d*d)), 'prefix_norms_squared':p,'conditional_entropy':entropy,'energy':energy,'required_additive_defect':entropy-energy,'predicted_defect':math.log(D)*(N+(1-D**(-2*N))/(D*D-1)),'target_two_block_defect':2*math.log(D)*sum(p)})
p=Path(__file__).with_name('COMPUTE_RECEIPT.json')
p.write_text(json.dumps({'kind':'deterministic exact-family floating-point crosscheck','assertions':'PASS','cases':rows},indent=2)+'\n')
print(p.read_text())
