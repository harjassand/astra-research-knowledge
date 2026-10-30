"""Exact symmetry reduction of the existing P5/T angular profile.

No SOS condition is imposed. The output is a small rational affine family
of CLOSED completions and its necessary acoustic-zero jets, not feasibility.
"""
from pathlib import Path
import hashlib,json,time
import sympy as S


def degrees(total,n):
    if n==1:yield(total,)
    else:
        for j in range(total+1):
            for p in degrees(total-j,n-1):yield(j,)+p


def main():
    start=time.perf_counter();A=S.symbols('a b c d',real=True);h=S.symbols('h0:6',real=True)
    powers=list(degrees(5,4));swap=(1,0,3,2);signs=(1,-1,-1,1)
    keys=[(i,p)for i in range(4)for p in powers if signs[i]*S.prod(signs[j]**p[j]for j in range(4))==-1]
    seen=set();basis=[]
    for key in keys:
        if key in seen:continue
        i,p=key;other=(swap[i],tuple(p[swap[j]]for j in range(4)))
        seen.add(key);seen.add(other)
        v=S.zeros(4,1)
        v[i]+=S.prod(A[j]**p[j]for j in range(4))
        k,q=other;v[k]-=S.prod(A[j]**q[j]for j in range(4));basis.append(v)
    z=S.symbols('z:'+str(len(basis)));P=sum((v*c for v,c in zip(basis,z)),S.zeros(4,1))
    J=S.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
    lie=P.jacobian(A)*J*S.Matrix(A)+J.T*P
    eq=[v for expr in lie for v in S.Poly(S.expand(expr),A).coeffs()]
    M,_=S.linear_eq_to_matrix(eq,z);N=S.Matrix.hstack(*M.nullspace())
    coeff=S.symbols('v:'+str(N.cols));rotation_sub=dict(zip(z,N*S.Matrix(coeff)))
    P=S.simplify(P.subs(rotation_sub));T=sum(v*v for v in A)
    Pjac=P.jacobian(A)
    # T² d(P/T); our skew matrix convention is Omega_ij=∂i alpha_j−∂j alpha_i.
    Omega=S.zeros(4)
    for i in range(4):
        for j in range(i+1,4):
            Omega[i,j]=S.expand(T*(Pjac[j,i]-Pjac[i,j])-2*(A[i]*P[j]-A[j]*P[i]));Omega[j,i]=-Omega[i,j]
    q=A[0]*A[3]-A[1]*A[2];x=A[0]**2+A[2]**2-A[1]**2-A[3]**2
    F=T*T+12*q*q+4*q*x;H=S.hessian(F,A)
    B1=S.Matrix([h[0],h[1],h[3],h[4]]);B2=S.Matrix([h[1],h[2],h[4],h[5]])
    C=S.hessian(T*T*(B1.T*H*B1+B2.T*H*B2)[0]+(B1.T*Omega*B2)[0],h)/2
    at=dict(zip(A,(1,0,0,1)));K=S.Matrix([[0,0],[0,1],[1,0],[0,0],[0,0],[0,-2]])
    equations=list(C.subs(at)*K)
    for a in A:
        block=K.T*C.diff(a).subs(at)*K
        equations.extend(block[i,j]for i in range(2)for j in range(i,2))
    D,rhs=S.linear_eq_to_matrix(equations,coeff)
    solution=next(iter(S.linsolve((D,rhs),coeff)));sub=dict(zip(coeff,solution))
    free=sorted(set().union(*(v.free_symbols for v in solution)),key=str)
    P=S.simplify(P.subs(sub));Omega=S.simplify(Omega.subs(sub));C=S.simplify(C.subs(sub))
    # Quotient exact primitive gauges: Omega depends only on image coordinates.
    rows=[]
    for i in range(4):
        for j in range(i+1,4):
            for val in S.Poly(Omega[i,j],A).coeffs():rows.append([S.diff(val,v)for v in free])
    Q=S.Matrix(rows);pivots=Q.rref()[1]
    # Set nonpivot gauge parameters to zero; pivot columns span exactly the image.
    gauge={free[j]:0 for j in range(len(free))if j not in pivots}
    P=S.simplify(P.subs(gauge));Omega=S.simplify(Omega.subs(gauge));C=S.simplify(C.subs(gauge))
    effective=[v for v in free if v not in gauge]
    out={'scope':'closed rational existing P5/T profile after actual Fstar symmetries and forced smooth jets; no SOS',
         'discrete_basis':len(basis),'rotation_kernel':N.cols,'jet_rank':D.rank(),
         'primitive_free':len(free),'exact_primitive_gauges':len(gauge),'effective_parameters':[str(v)for v in effective],
         'primitive_numerator':[str(v)for v in P],
         'cleared_omega':[[str(v)for v in row]for row in Omega.tolist()],
         'cleared_completion':[[str(v)for v in row]for row in C.tolist()],
         'seconds_after_imports':time.perf_counter()-start,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name('ANGULAR_REDUCTION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k]for k in ('discrete_basis','rotation_kernel','jet_rank','primitive_free','exact_primitive_gauges','effective_parameters','seconds_after_imports')},indent=2))
    print('P=',P)


if __name__=='__main__':main()
