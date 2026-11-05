"""Exact rational local certificate and independent full-input reset check."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
from fractions import Fraction as Q
from pathlib import Path
import json
import numpy as np
import scipy.linalg as la

OUT=Path(__file__).resolve().parent


def zeros(n):
    return [[Q(0) for _ in range(n)] for _ in range(n)]


def exact_model():
    h=zeros(9)
    for i,j,a,b in ((1,3,Q(4,5),Q(1,5)),(2,6,Q(1,5),Q(4,5))):
        h[i][i]=a;h[j][j]=b;h[i][j]=h[j][i]=Q(-2,5)
    for i in (4,5,7,8):h[i][i]=Q(1)
    V=[Q(0),Q(3,10),Q(-3,10)]
    hp=[row[:] for row in h]
    for i in range(9):hp[i][i]+=V[i//3]-V[i%3]
    # Exact positive-square decomposition of h'-(1/10)(n_L+n_R).
    R=zeros(9)
    for i,j in ((1,3),(2,6)):
        R[i][i]+=Q(2,5);R[j][j]+=Q(2,5)
        R[i][j]-=Q(2,5);R[j][i]-=Q(2,5)
    for i,c in ((4,Q(4,5)),(5,Q(7,5)),(7,Q(1,5)),(8,Q(4,5))):R[i][i]+=c
    margin=[row[:] for row in hp]
    for i in range(9):margin[i][i]-=Q(int(i//3!=0)+int(i%3!=0),10)
    assert R==margin
    assert all(sum(h[i][k]*h[k][j] for k in range(9))==h[i][j]
               for i in range(9) for j in range(9))
    return np.array(h,float),dict(
        arithmetic='Python Fraction, exact equality',
        h_projector_identity=True,
        shifted_particle_bound_positive_square_decomposition=True,
        exact_h_prime_eigenvalues=['0','1/10','1/10','2/5','9/10','9/10','1','1','8/5'],
        exact_periodic_gap='1/5',
        h_prime=[[str(x) for x in row] for row in hp])


def embed(h, axes, d, N):
    T=np.eye(d**N,dtype=complex).reshape(*([d]*N),d**N)
    order=list(axes)+[i for i in range(N+1) if i not in axes]
    A=T.transpose(order);shape=A.shape
    return (h@A.reshape(d*d,-1)).reshape(shape).transpose(np.argsort(order)).reshape(d**N,d**N)


def reset_test(h,d,N,label):
    M=float(la.norm(h,2))
    # T is the reset channel's output isometry after tracing both endpoints.
    T=np.zeros((d**N,d**(N-2)),complex)
    for j in range(d**(N-2)):T[j*d,j]=1
    Hb=embed(h,(0,1),d,N)+embed(h,(N-2,N-1),d,N)+embed(h,(N-1,0),d,N)
    F=(Hb@T).conj().T@(Hb@T)
    number=np.eye(d);number[0,0]=0
    Nc=np.kron(number,np.eye(d**(N-3)))+np.kron(np.eye(d**(N-3)),number)
    residual=2*M*M*Nc-F
    minimum=float(la.eigvalsh(residual).min())
    vacuum=np.zeros(d**(N-2));vacuum[0]=1
    assert minimum>-2e-12 and la.norm(F@vacuum)<1e-12
    assert la.norm(T.conj().T@T-np.eye(d**(N-2)))<1e-12
    return dict(model=label,N=N,site_dimension=d,M=M,
                reset_bound_minimum_eigenvalue=minimum,
                vacuum_annihilation_error=float(la.norm(F@vacuum)),
                boundary_square_norm=float(la.norm(F,2)))


def main():
    h,exact=exact_model();rows=[]
    rng=np.random.default_rng(807166)
    for d in (2,3):
        A=rng.normal(size=(d*d-1,d*d-1))+1j*rng.normal(size=(d*d-1,d*d-1))
        P=A.conj().T@A;P/=la.norm(P,2)
        R=np.zeros((d*d,d*d),complex);R[1:,1:]=P
        for N in (4,5):rows.append(reset_test(R,d,N,'arbitrary complex positive vacuum-annihilating h'))
    for N in (4,5):rows.append(reset_test(h,3,N,'exact closing-open-gap qutrit projector'))
    result=dict(exact_rational_certificate=exact,full_core_operator_checks=rows,
                note='Entire core operator tested, not selected states; arbitrary input endpoints are traced. Floating tests support the separate operator proof.')
    (OUT/'coboundary_reset_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(exact_rational_certificate_passed=True,full_core_checks=len(rows),
                         minimum_reset_bound_residual=min(x['reset_bound_minimum_eigenvalue'] for x in rows)),indent=2))


if __name__=='__main__':main()
