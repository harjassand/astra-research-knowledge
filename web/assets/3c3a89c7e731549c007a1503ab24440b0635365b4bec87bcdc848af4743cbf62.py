"""Rationalize and EXACTLY VERIFY a separable decomposition of original ABA.

The external solver supplies candidates only. Integer residual correction,
exact reconstruction, and positive leading principal minors prove the claim.
No floating tolerance enters verification.
"""
import json,hashlib
from pathlib import Path
import numpy as np
from exact_rank import rational_model

BASE=Path(__file__).parent

def det(a):
    """Bareiss exact determinant with row swaps."""
    a=[[int(z) for z in row] for row in a]
    n=len(a);previous=1;sign=1
    if n==0:return 1
    for k in range(n-1):
        if not a[k][k]:
            pivot=next((i for i in range(k+1,n) if a[i][k]),None)
            if pivot is None:return 0
            a[k],a[pivot]=a[pivot],a[k];sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=a[i][j]*pivot-a[i][k]*a[k][j]
                assert numerator%previous==0
                a[i][j]=numerator//previous
            a[i][k]=0
        previous=pivot
    return sign*a[-1][-1]

def rounded(a,den):
    return np.array([[int(round(float(z)*den)) for z in row] for row in a],dtype=object)

def build():
    z=np.load(BASE/'sep_candidate.npz');x=z['x'];y=z['y'];vec=z['vec'];bs=z['bs']
    # balance factors to avoid huge individual entries, without changing x kron y
    scale=np.linalg.norm(x)/np.sqrt(10);x=x/scale;y=y*scale
    qx=10**8;qv=10**6;qb=10**10
    xi=rounded(x,qx);yi=rounded(y,qx)
    vi=rounded(vec,qv);bi=[]
    for n,b in enumerate(bs):
        if 10<=n<100:b=b/2
        bi.append(rounded((b+b.T)/2,qb))
    bi=np.array(bi,dtype=object)
    # Standard first 100 atoms are kept exactly, with pair normalization in B.
    for n in range(100):
        vi[n,:]=0
    for i in range(10):vi[i,i]=qv
    at=10
    for sign in (1,-1):
        for i in range(10):
            for j in range(i+1,10):vi[at,i]=qv;vi[at,j]=sign*qv;at+=1
    _,_,_,j=rational_model();trace=int(np.trace(j))
    local=np.kron(xi,yi);target=local@j@local.T
    targetden=trace*qx**4
    approx=sum(np.kron(np.outer(v,v),b) for v,b in zip(vi,bi))
    approxden=qv*qv*qb
    denominator=targetden*approxden
    residual=target*approxden-approx*targetden
    # Correct the first 55 standard spanning atoms to remove residual exactly.
    r=residual.reshape(10,6,10,6)
    correction=[r[i,:,i,:].copy() for i in range(10)]
    for i in range(10):
        for j0 in range(i+1,10):
            c=r[i,:,j0,:].copy()
            assert np.array_equal(c,c.T)
            correction.append(c)
            correction[i]-=c;correction[j0]-=c
    final=bi*(denominator//qb)
    for n,c in enumerate(correction):final[n]+=c
    payload={'schema':'family272_original_cube_separable_v1',
      'boundary_dim':[10,6],
      'x_numerator':xi.tolist(),'y_numerator':yi.tolist(),'filter_denominator':qx,
      'input_numerators':vi.tolist(),'input_denominator':qv,
      'output_numerators':final.tolist(),'output_denominator':denominator,
      'rational_target_trace':trace}
    path=BASE/'cube_separable_certificate.json'
    path.write_text(json.dumps(payload,separators=(',',':'))+'\n')
    return path

def verify(path):
    raw=path.read_bytes();z=json.loads(raw)
    xi=np.array(z['x_numerator'],dtype=object);yi=np.array(z['y_numerator'],dtype=object)
    vi=np.array(z['input_numerators'],dtype=object)
    bi=np.array(z['output_numerators'],dtype=object)
    qx=z['filter_denominator'];qv=z['input_denominator'];den=z['output_denominator']
    assert qx>0 and qv>0 and den>0
    assert det(xi)!=0 and det(yi)!=0
    all_minors=[]
    for b in bi:
        assert np.array_equal(b,b.T)
        minors=[det(b[:i,:i]) for i in range(1,7)]
        assert all(v>0 for v in minors)
        all_minors.append(minors)
    _,_,_,j=rational_model();trace=int(np.trace(j));assert trace==z['rational_target_trace']
    local=np.kron(xi,yi);target=local@j@local.T
    reconstructed=sum(np.kron(np.outer(v,v),b) for v,b in zip(vi,bi))
    assert np.array_equal(reconstructed*(trace*qx**4),target*(qv*qv*den))
    out={'status':'EXACTLY_VERIFIED','claim':'original family272 channel cube is EB',
         'verified_matrix':'invertibly real-locally filtered Choi(ABA)',
         'input_factors':len(vi),'output_factor_dimension':6,
         'every_output_factor':'positive definite by exact Sylvester principal minors',
         'reconstruction':'exact integer equality',
         'local_filters':'invertible by exact nonzero determinant',
         'certificate_bytes':len(raw),'certificate_sha256':hashlib.sha256(raw).hexdigest(),
         'smallest_minor_numerator':str(min(v for m in all_minors for v in m)),
         'verification_uses_solver':False}
    (BASE/'exact_separability.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--verify-only',action='store_true')
    args=ap.parse_args()
    path=BASE/'cube_separable_certificate.json' if args.verify_only else build()
    verify(path)
