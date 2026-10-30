"""Construct the full polynomial face at the DM endpoint, over Q(sqrt(3))."""
from pathlib import Path
import sympy as S,json,time,signal
from sympy.polys.matrices import DomainMatrix
signal.alarm(120);start=time.perf_counter();root=Path(__file__).resolve().parents[1]
A=S.symbols('a b c d');x,y,s,t=S.symbols('x y s t');a,b,c,d=A;rt=S.sqrt(3);field=S.QQ.algebraic_field(rt)
def deg(n,k):
    if k==1:yield(n,)
    else:
        for i in range(n+1):
            for pw in deg(n-i,k-1):yield(i,)+pw
def rank(M):return DomainMatrix.from_Matrix(M).convert_to(field).rank()
U=S.Matrix([[x,-y],[y,x]]);V=S.Matrix([[s,-t],[t,s]]);R=S.Matrix([x*s,x*t,y*s,y*t]);K=U*S.diag(1,rt)*V.T;K=S.Matrix(list(K))
cp=list(deg(3,4));qp=list(deg(4,4));cub=[];quart=[]
def coeffs(p,n):
    P=S.Poly(S.expand(p),x,y,s,t)
    return [P.coeff_monomial(x**(n-i)*y**i*s**(n-j)*t**j) for i in range(n+1) for j in range(n+1)]
for pw in cp:
    P=S.prod(z**e for z,e in zip(A,pw));gradient=S.Matrix([S.diff(P,z) for z in A])
    cub.append(coeffs((gradient.subs(dict(zip(A,R)),simultaneous=True).T*K)[0],3))
for pw in qp:
    P=S.prod(z**e for z,e in zip(A,pw));H=S.hessian(P,A);v=H.subs(dict(zip(A,R)),simultaneous=True)*K
    quart.append(sum((coeffs(z,3) for z in v),[]))
CM=S.Matrix.hstack(*map(S.Matrix,cub));QM=S.Matrix.hstack(*map(S.Matrix,quart));cr=rank(CM);qr=rank(QM)
T=sum(z*z for z in A);det=a*d-b*c;F=S.expand(T*T-4*rt*T*det/3)
def vector(P,powers):
    p=S.Poly(S.expand(P),*A)
    return S.Matrix([p.coeff_monomial(S.prod(z**e for z,e in zip(A,pw))) for pw in powers])
trans=S.Matrix.hstack(*(vector(S.diff(F,z),cp) for z in A));fv=vector(F,qp)
assert all(S.simplify(z)==0 for z in CM*trans) and all(S.simplify(z)==0 for z in QM*fv)
assert cr==16 and qr==34 and rank(trans)==4
def alg(z):
    p=S.Poly(S.expand(z),rt,extension=True)
    # Coefficients here are in the literal basis 1,sqrt(3).
    zz=S.expand(z);q=S.simplify((zz-zz.xreplace({rt:-rt}))/(2*rt));p=S.simplify(zz-q*rt)
    assert p.is_Rational and q.is_Rational
    return [int(p.p),int(p.q),int(q.p),int(q.q)]
out={'cubic_powers':cp,'quartic_powers':qp,'cubic_matrix':[[alg(z) for z in row] for row in CM.tolist()],
 'quartic_matrix':[[alg(z) for z in row] for row in QM.tolist()],
 'translation_cubics':[[alg(z) for z in trans[:,j]] for j in range(4)],
 'F':[alg(z) for z in fv],'cubic_rank':cr,'quartic_rank':qr,'seconds':time.perf_counter()-start,
 'scope':'Exact full-space exposure and cubic translation rigidity. QC of the leading DM endpoint is the published primary theorem; lower-degree classification is derived here.'}
(root/'work/dm_full_face.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k in ('cubic_rank','quartic_rank','seconds','scope')},indent=2))
