"""One existing P5/T profile, with acoustic value/first-jet Gram face removed.

This is the SAME profile already acquired for the strict neighboring Hopf
energy in ROOT25, not an open-ended degree search. A numerical failure is
not an all-angular obstruction. One proposal is made and fully charged.
"""
from pathlib import Path
import hashlib,json,time
import numpy as np
import sympy as S
from scipy import sparse
import cvxpy as cp


def degree(total,n):
    if n==1:yield(total,)
    else:
        for j in range(total+1):
            for tail in degree(total-j,n-1):yield(j,)+tail


def main():
    start=time.perf_counter();A=S.symbols('a:4');h=S.symbols('h0:6')
    B1=S.Matrix([h[0],h[1],h[3],h[4]]);B2=S.Matrix([h[1],h[2],h[4],h[5]])
    T=sum(v*v for v in A);q=A[0]*A[3]-A[1]*A[2];x=A[0]**2+A[2]**2-A[1]**2-A[3]**2
    F=T*T+12*q*q+4*q*x;H=S.hessian(F,A)
    target=S.expand(T*T*(B1.T*H*B1+B2.T*H*B2)[0])
    mons=[a+b for a in degree(6,4) for b in degree(2,6)];index={m:i for i,m in enumerate(mons)}
    rhs=np.zeros(len(mons))
    for mon,value in S.Poly(target,(*A,*h)).terms():rhs[index[mon]]=int(value)
    cols=[];primitives=[]
    for coord in range(4):
        for nu in degree(5,4):
            mon=S.prod(v**e for v,e in zip(A,nu));expr=0
            for i in range(4):
                expr+=(T*S.diff(mon,A[i])-2*A[i]*mon)*(B1[i]*B2[coord]-B2[i]*B1[coord])
            col=np.zeros(len(mons))
            for key,value in S.Poly(S.expand(expr),(*A,*h)).terms():col[index[key]]=int(value)
            cols.append(col);primitives.append([coord,list(nu)])
    J=sparse.csc_matrix(np.array(cols).T)
    z=[]
    for nu in degree(3,4):
        for j in range(6):
            hh=[0]*6;hh[j]=1;z.append(nu+tuple(hh))
    C,D=S.symbols('C D');kernel=[]
    for av,hv,hprime in [([-D,C,C,D],[C,0,0,D,0,0],[2*D,C,0,-2*C,D,0]),
                         ([C,-D,D,C],[0,0,C,0,0,D],[0,C,2*D,0,D,-2*C])]:
        for hs in (hv,hprime):
            zs=[S.prod(v**e for v,e in zip(av,key[:4]))*hs[key[4:].index(1)] for key in z]
            for k in range(5):
                kernel.append(S.Matrix([S.Poly(v,C,D).coeff_monomial(C**(4-k)*D**k) for v in zs]))
    N=S.Matrix.hstack(*kernel);basis=S.Matrix.hstack(*N.T.nullspace())
    assert N.T*basis==S.zeros(N.cols,basis.cols)
    B=sparse.csc_matrix(np.array(basis,dtype=float));active=B.shape[1]
    rows=[];cc=[]
    for i,zi in enumerate(z):
        for j,zj in enumerate(z):rows.append(index[tuple(a+b for a,b in zip(zi,zj))]);cc.append(len(z)*i+j)
    gram=sparse.coo_matrix((np.ones(len(z)**2),(rows,cc)),shape=(len(mons),len(z)**2)).tocsc()
    reduced=(gram@sparse.kron(B,B,format='csc')).tocsc()
    G=cp.Variable((active,active),symmetric=True);alpha=cp.Variable(len(primitives));margin=cp.Variable()
    eq=reduced@cp.vec(G,order='C')==rhs+J@alpha
    problem=cp.Problem(cp.Maximize(margin),[eq,G-margin*np.eye(active)>>0])
    acquisition=time.perf_counter()-start;tick=time.perf_counter()
    problem.solve(solver='CLARABEL',max_iter=150,tol_gap_abs=1e-8,tol_feas=1e-8,tol_gap_rel=1e-8)
    out={'scope':'one fixed endpoint and existingP5/T profile; no all-degree inference',
         'status':problem.status,'margin':None if margin.value is None else float(margin.value),
         'kernel_rank':N.rank(),'active_gram_dimension':active,'equations':len(mons),
         'alpha':None if alpha.value is None else alpha.value.tolist(),
         'gram':None if G.value is None else G.value.tolist(),
         'feature_reduction_sparse':[[i,j,str(basis[i,j])] for i in range(basis.rows) for j in range(basis.cols) if basis[i,j]],
         'primitives':primitives,'z':[list(x) for x in z],
         'acquisition_seconds':acquisition,'solve_seconds':time.perf_counter()-tick,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'cvxpy_version':cp.__version__}
    if G.value is not None:
        out['equality_residual']=float(np.max(abs(reduced@G.value.reshape(-1)-rhs-J@alpha.value)))
        out['min_gram_eigenvalue_display_only']=float(np.linalg.eigvalsh(G.value).min())
    Path(__file__).with_name('ENDPOINT_RATIONAL_PROPOSAL.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','margin','kernel_rank','active_gram_dimension','acquisition_seconds','solve_seconds')},indent=2))


if __name__=='__main__':main()
