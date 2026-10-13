"""Build and verify a rational Choi/residual certificate using exact LDL^T.
A successful verification is independent of the floating-point optimizer.
"""
from __future__ import annotations
from pathlib import Path
import json,time
import numpy as np
import sympy as s

def exact_pd(M:s.Matrix):
    """Exact LDL^T without pivoting: positive pivots prove positive definiteness."""
    n=M.rows;L=s.eye(n);p=[]
    for j in range(n):
        dj=s.cancel(M[j,j]-sum(L[j,k]**2*p[k] for k in range(j)))
        if dj<=0:raise ArithmeticError(f'Nonpositive pivot {j}: {dj}')
        p.append(dj)
        for i in range(j+1,n):L[i,j]=s.cancel((M[i,j]-sum(L[i,k]*L[j,k]*p[k] for k in range(j)))/dj)
    return p

def partial_input(C,d):return s.Matrix(d,d,lambda a,b:sum(C[i*d+a,i*d+b] for i in range(d)))
def channel_image(C,H,d):
    r=H.rows//d
    return s.Matrix(d*r,d*r,lambda x,y:sum(C[i*d+x//r,j*d+y//r]*H[i*r+x%r,j*r+y%r] for i in range(d) for j in range(d)))
def ratmatrix(M,den=10**10):return s.Matrix([[s.Rational(round(float(x)*den),den) for x in row] for row in M])

def build():
    start=time.perf_counter();root=Path(__file__).parent;z=np.load(root/'extremal_chain.npz');d=4
    C=ratmatrix(z['choi']);I=s.eye(d)
    C-=s.kronecker_product(I/d,partial_input(C,d)-I)
    # A small exact depolarizing component puts Choi into the PSD interior.
    eps=s.Rational(1,10**6);C=(1-eps)*C+eps*s.eye(d*d)/d
    assert partial_input(C,d)==I
    Hstrong=ratmatrix(z['h1']);Hweak=ratmatrix(z['h0']);bound=s.Rational(22421,100000)
    R=Hweak-channel_image(C,Hstrong,d)-bound*s.eye(16)
    cp=exact_pd(C);rp=exact_pd(R)
    data={'dimension_active':d,'dimension_collar':4,'lower_reverse':str(bound),'meaning':'E(strong)-E(weak) <= -22421/100000 for every compatible environment',
          'choi':[[str(x) for x in row] for row in C.tolist()],
          'hstrong':[[str(x) for x in row] for row in Hstrong.tolist()],
          'hweak':[[str(x) for x in row] for row in Hweak.tolist()]}
    (root/'rational_chain_certificate.json').write_text(json.dumps(data,indent=2))
    summary={'verification':'exact rational LDL^T','unital_exact':True,'choi_positive_pivots':len(cp),'residual_positive_pivots':len(rp),'certified_difference_interval':['-3/4','-22421/100000'],'seconds':time.perf_counter()-start,
          'smallest_choi_pivot_numeric':float(min(cp)),'smallest_residual_pivot_numeric':float(min(rp))}
    (root/'rational_chain_verification.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))

def verify():
    root=Path(__file__).parent;x=json.loads((root/'rational_chain_certificate.json').read_text());d=x['dimension_active'];C=s.Matrix(x['choi']);Hstrong=s.Matrix(x['hstrong']);Hweak=s.Matrix(x['hweak']);c=s.Rational(x['lower_reverse'])
    assert C==C.T and partial_input(C,d)==s.eye(d)
    exact_pd(C);exact_pd(Hweak-channel_image(C,Hstrong,d)-c*s.eye(Hweak.rows))
    print('VERIFIED: E(strong)-E(weak) in [-3/4, -22421/100000], uniformly over arbitrary common environments.')
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--verify-only',action='store_true');a=p.parse_args()
    verify() if a.verify_only else build()
