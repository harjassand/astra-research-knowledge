"""Exact first-jet necessary conditions for a smooth closed heat completion.

The extra null vector is forced by fourth-order acoustic degeneracy at I,
not assumed as a polynomial/SOS restriction.
"""
from pathlib import Path
import hashlib,json,time
import sympy as S


def main():
    start=time.perf_counter()
    A=S.symbols('a b c d',real=True);h=S.symbols('h0:6',real=True)
    pairs=[(i,j) for i in range(4) for j in range(i+1,4)]
    o=S.symbols('o0:6');w=S.symbols('w0:24');unknown=(*o,*w)
    base=S.Matrix([1,0,0,1]);delta=S.Matrix(A)-base
    Omega=S.zeros(4);Omega0=S.zeros(4)
    for n,(i,j) in enumerate(pairs):
        Omega[i,j]=o[n]+sum(w[4*n+k]*delta[k] for k in range(4));Omega[j,i]=-Omega[i,j]
        Omega0[i,j]=o[n];Omega0[j,i]=-o[n]
    T=sum(x*x for x in A);q=A[0]*A[3]-A[1]*A[2];x=A[0]**2+A[2]**2-A[1]**2-A[3]**2
    F=T*T+12*q*q+4*q*x;H=S.hessian(F,A)
    B1=S.Matrix([h[0],h[1],h[3],h[4]]);B2=S.Matrix([h[1],h[2],h[4],h[5]])
    density=(B1.T*H*B1+B2.T*H*B2+B1.T*Omega*B2)[0]
    C=S.hessian(density,h)/2
    sub=dict(zip(A,base));C0=C.subs(sub)
    # ξ=(t,1), eta=(1,-2t/(1+t²)); h'=e_(u1xy)-2e_(u2yy).
    K=S.Matrix([[0,0],[0,1],[1,0],[0,0],[0,0],[0,-2]])
    equations=list(C0*K)
    for coordinate in A:
        block=K.T*C.diff(coordinate).subs(sub)*K
        equations.extend(block[i,j] for i in range(2) for j in range(i,2))
    # Coefficient homogeneity degree2.
    for i,j in pairs:
        equations.append(sum(base[k]*S.diff(Omega[i,j],A[k]) for k in range(4))-2*Omega0[i,j])
    # Closedness, coefficient degree1 in this first jet.
    for i in range(4):
        for j in range(i+1,4):
            for k in range(j+1,4):
                equations.append(S.diff(Omega[j,k],A[i])-S.diff(Omega[i,k],A[j])+S.diff(Omega[i,j],A[k]))
    # Lie invariance under output rotations.
    J=S.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
    V=J*base
    lie=sum((V[k]*Omega.diff(A[k]) for k in range(4)),S.zeros(4))+J.T*Omega0+Omega0*J
    equations.extend(lie[i,j] for i,j in pairs)
    # F invariant under A->C A C, with spatial orientation sign -1.
    signs=[1,-1,-1,1]
    for n,(i,j) in enumerate(pairs):
        equations.append((1+signs[i]*signs[j])*o[n])
        for k in range(4):equations.append((1+signs[i]*signs[j]*signs[k])*w[4*n+k])
    mat,rhs=S.linear_eq_to_matrix([S.expand(v) for v in equations],unknown)
    rank=mat.rank();aug=mat.row_join(rhs).rank()
    solution=S.linsolve((mat,rhs),unknown)
    out={'scope':'necessary equivariant closed FIRST JET; no finite-degree primitive assumption',
         'equations':mat.rows,'unknowns':mat.cols,'rank':rank,'augmented_rank':aug,
         'consistent':rank==aug,'solution':str(solution),'unknown_order':[str(v) for v in unknown],
         'matrix':[[str(v) for v in row] for row in mat.tolist()],'rhs':[str(v) for v in rhs],
         'seconds_after_imports':time.perf_counter()-start,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name('LOCAL_CLOSED_JET.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('equations','unknowns','rank','augmented_rank','consistent','solution','seconds_after_imports')},indent=2))


if __name__=='__main__':main()
