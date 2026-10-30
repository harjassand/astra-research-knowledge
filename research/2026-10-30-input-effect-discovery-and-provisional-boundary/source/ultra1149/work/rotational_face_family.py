"""A parameter-wide whole-face construction, rather than another seed."""
from pathlib import Path
import sympy as S,json,time,signal
from sympy.polys.matrices import DomainMatrix
signal.alarm(120);start=time.perf_counter();root=Path(__file__).resolve().parents[1]
A=S.symbols('a b c d');x,y,s,t,z=S.symbols('x y s t z');a,b,c,d=A
def deg(n,k):
    if k==1:yield(n,)
    else:
        for i in range(n+1):
            for pw in deg(n-i,k-1):yield(i,)+pw
U=S.Matrix([[x,-y],[y,x]]);V=S.Matrix([[s,-t],[t,s]]);R=S.Matrix([x*s,x*t,y*s,y*t]);K=S.Matrix(list(U*S.diag(z,1)*V.T))
def coeffs(p,n):
    P=S.Poly(S.expand(p),x,y,s,t)
    return [P.coeff_monomial(x**(n-i)*y**i*s**(n-j)*t**j) for i in range(n+1) for j in range(n+1)]
cp=list(deg(3,4));qp=list(deg(4,4));cub=[];quart=[]
for pw in cp:
    P=S.prod(v**e for v,e in zip(A,pw));grad=S.Matrix([S.diff(P,v) for v in A]);cub.append(coeffs((grad.subs(dict(zip(A,R)),simultaneous=True).T*K)[0],3))
for pw in qp:
    P=S.prod(v**e for v,e in zip(A,pw));H=S.hessian(P,A);vec=H.subs(dict(zip(A,R)),simultaneous=True)*K;quart.append(sum((coeffs(v,3) for v in vec),[]))
CM=S.Matrix.hstack(*map(S.Matrix,cub));QM=S.Matrix.hstack(*map(S.Matrix,quart))
def minor_identity(M):
    M0=M.subs(z,S.Rational(2,3));_,cols=DomainMatrix.from_Matrix(M0).rref();cols=list(cols)
    _,rows=DomainMatrix.from_Matrix(M0[:,cols].T).rref();rows=list(rows)
    sub=M[rows,cols];domain=S.QQ.poly_ring(z);dm=DomainMatrix.from_Matrix(sub).convert_to(domain)
    det=S.factor(domain.to_sympy(dm.det()))
    return {'rows':rows,'columns':cols,'determinant':str(det)},len(cols)
cm,cr=minor_identity(CM);print('cubic',cr,cm['determinant'],flush=True)
qm,qr=minor_identity(QM);print('quartic',qr,qm['determinant'],flush=True)
T=sum(v*v for v in A);D=a*d-b*c;F=S.expand(T*T-4*z*T*D+(6*z*z-2)*D*D)
def vector(P,powers):
    pp=S.Poly(S.expand(P),*A)
    return S.Matrix([pp.coeff_monomial(S.prod(v**e for v,e in zip(A,pw))) for pw in powers])
trans=S.Matrix.hstack(*(vector(S.diff(F,v),cp) for v in A));fv=vector(F,qp)
assert (CM*trans).applyfunc(S.expand)==S.zeros(16,4) and (QM*fv).applyfunc(S.expand)==S.zeros(64,1)
tr,rankt=minor_identity(trans);assert rankt==4
print('translation',tr['determinant'],flush=True)
out={'cubic_powers':cp,'quartic_powers':qp,
 'cubic_matrix':[[str(v) for v in row] for row in CM.tolist()],
 'quartic_matrix':[[str(v) for v in row] for row in QM.tolist()],
 'translation_cubics':[[str(v) for v in trans[:,j]] for j in range(4)],'F':[str(v) for v in fv],
 'cubic_minor':cm,'quartic_minor':qm,'translation_minor':tr,
 'exceptional_ranks':{str(v):{'cubic':DomainMatrix.from_Matrix(CM.subs(z,v)).rank(),'quartic':DomainMatrix.from_Matrix(QM.subs(z,v)).rank()} for v in (0,S.Rational(1,3),S.Rational(-1,3),1,-1)},
 'seconds':time.perf_counter()-start,'scope':'Symbolic full-space exposure and cubic rigidity certificates. Parameter exclusions must follow the literal determinant factors, not the sample rank.'}
(root/'work/rotational_face_family.json').write_text(json.dumps(out,indent=2)+'\n');print('seconds',out['seconds'],flush=True)
