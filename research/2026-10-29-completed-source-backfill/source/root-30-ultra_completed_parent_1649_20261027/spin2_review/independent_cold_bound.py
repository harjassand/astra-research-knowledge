"""Independent literal physical-basis replay of the cold count obstruction.
NumPy object multiplication is integer-only. No producer module is imported.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
from math import isqrt
import numpy as np,json,time,hashlib
ROOT=Path(__file__).resolve().parent
def run():
    started=time.monotonic();path=ROOT/'inputs/open5_rational_cholesky.npz'
    data=np.load(path);scale=int(data['denominator']);assert scale==2**40
    lint=data['L_numerator'];xint=data['X_numerator']
    words=[w for w in product(range(-2,3),repeat=5) if sum(w)==0]
    index={w:i for i,w in enumerate(words)};n=len(words);assert n==381
    h0=np.zeros((n,n),dtype=np.int64);h1=np.zeros((n,n),dtype=np.int64)
    for j,w in enumerate(words):
        h0[j,j]=sum(w[k]*w[k+1] for k in range(4))
        for k in range(4):
            for step in [-1,1]:
                mi,mj=w[k],w[k+1]
                if not(-2<=mi+step<=2 and -2<=mj-step<=2):continue
                v=list(w);v[k]+=step;v[k+1]-=step;i=index[tuple(v)]
                square=(6-mi*(mi+step))*(6-mj*(mj-step))
                root=isqrt(square)
                if root*root==square:assert root%2==0;h0[i,j]+=root//2
                else:assert square==24;h1[i,j]+=1
    assert np.array_equal(h0,h0.T) and np.array_equal(h1,h1.T)
    assert lint.shape==xint.shape==(n,n) and not np.triu(lint,1).any()
    L=lint.astype(object);X=xint.astype(object)
    LL=L@L.T;LX=L@X
    residual=[[abs((scale**2 if i==j else 0)-int(LX[i,j])) for j in range(n)] for i in range(n)]
    rho=F(max(max(map(sum,residual)),max(sum(row[j] for row in residual) for j in range(n))),scale**2)
    assert rho<1
    xn=max(max(sum(abs(int(v)) for v in row) for row in xint),
           max(sum(abs(int(xint[i,j])) for i in range(n)) for j in range(n)))
    B=F(xn,scale)/(1-rho)
    lo=F(2449489742783178098,10**18);hi=F(2449489742783178099,10**18)
    assert lo*lo<6<hi*hi
    shift=F(4901,250);errors=[]
    for i in range(n):
        row=F(0)
        for j in range(n):
            value=F(int(h0[i,j]))+(shift if i==j else 0)-F(int(LL[i,j]),scale**2)
            coefficient=int(h1[i,j])
            row+=max(abs(value+coefficient*lo),abs(value+coefficient*hi))
        errors.append(row)
    error=max(errors);margin=1/(B*B)-error;assert margin>0
    out={'status':'INDEPENDENT_INTEGER_DYADIC_OPEN5_LOWER_BOUND_PASS',
      'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
      'literal_physical_M0_dimension':n,'open5_energy_lower':'-4901/250',
      'rational_inverse_residual_upper':str(rho),'rational_inverse_norm_upper':str(B),
      'rational_matrix_residual_upper':str(error),'strict_positive_shifted_energy_margin':str(margin),
      'all_ring_energy_per_bond_lower':'-4901/1000',
      'cold_moment_method_obstruction':'Tr K^4/||K||^4 >=exp(99 beta/250)/625; A4 projected ratio >=exp(99 beta/250)/7500',
      'seconds':time.monotonic()-started,
      'scope':'Exact all-entry certificate plus reviewed integer-spin SU2 completeness and translated open-cluster comparison. Bounds the stated fourth-moment residual strategy, not arbitrary compression or the physical gap.'}
    (ROOT/'INDEPENDENT_COLD_BOUND.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
