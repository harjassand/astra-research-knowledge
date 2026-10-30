"""Full equivariant degree-two closed-form completion, before any SOS test.

This class is exhaustive for homogeneous cubic polynomial primitives after
the literal symmetries of Fstar are averaged. No Gram/SOS assumption is made.
"""
from pathlib import Path
import hashlib,json,time
import sympy as S


def main():
    start=time.perf_counter();A=S.symbols('a b c d',real=True)
    h=S.symbols('h0:6',real=True);pairs=[(i,j) for i in range(4) for j in range(i+1,4)]
    powers=[A[i]*A[j] for i in range(4) for j in range(i,4)]
    z=S.symbols('z0:60');Om=S.zeros(4)
    for r,(i,j) in enumerate(pairs):
        Om[i,j]=sum(z[10*r+k]*v for k,v in enumerate(powers));Om[j,i]=-Om[i,j]
    equations=[]
    for i in range(4):
        for j in range(i+1,4):
            for k in range(j+1,4):
                p=S.Poly(S.diff(Om[j,k],A[i])-S.diff(Om[i,k],A[j])+S.diff(Om[i,j],A[k]),A)
                equations.extend(p.coeffs())
    J=S.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
    V=J*S.Matrix(A)
    lie=sum((V[k]*Om.diff(A[k]) for k in range(4)),S.zeros(4))+J.T*Om+Om*J
    equations.extend(v for i,j in pairs for v in S.Poly(lie[i,j],A).coeffs())
    # A -> C A C and A -> A S both reverse spatial orientation.
    transforms=[S.diag(1,-1,-1,1),S.Matrix([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]])]
    for R in transforms:
        at=dict(zip(A,R*S.Matrix(A)))
        diff=R.T*Om.subs(at,simultaneous=True)*R+Om
        equations.extend(v for i,j in pairs for v in S.Poly(diff[i,j],A).coeffs())
    T=sum(v*v for v in A);q=A[0]*A[3]-A[1]*A[2];x=A[0]**2+A[2]**2-A[1]**2-A[3]**2
    F=T*T+12*q*q+4*q*x;H=S.hessian(F,A)
    B1=S.Matrix([h[0],h[1],h[3],h[4]]);B2=S.Matrix([h[1],h[2],h[4],h[5]])
    C=S.hessian((B1.T*H*B1+B2.T*H*B2+B1.T*Om*B2)[0],h)/2
    # The fourth-order acoustic null forces both these vectors into ker C(I).
    K=S.Matrix([[0,0],[0,1],[1,0],[0,0],[0,0],[0,-2]])
    equations.extend(C.subs(dict(zip(A,[1,0,0,1])))*K)
    M,rhs=S.linear_eq_to_matrix(equations,z)
    solution=next(iter(S.linsolve((M,rhs),z)));sub=dict(zip(z,solution))
    free=sorted(set().union(*(v.free_symbols for v in solution)),key=str)
    Om=S.simplify(Om.subs(sub));C=S.simplify(C.subs(sub))
    out={'scope':'all symmetry-averaged closed quadratic-coefficient 2forms; NO SOS restriction',
         'linear_equations':M.rows,'unknowns':60,'rank':M.rank(),
         'parameters':[str(v) for v in free],
         'omega':[[str(v) for v in row] for row in Om.tolist()],
         'completion':[[str(v) for v in row] for row in C.tolist()],
         'seconds_after_imports':time.perf_counter()-start,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name('QUADRATIC_COMPLETION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('scope','linear_equations','unknowns','rank','parameters','seconds_after_imports')},indent=2))
    print('OMEGA',Om)


if __name__=='__main__':main()
