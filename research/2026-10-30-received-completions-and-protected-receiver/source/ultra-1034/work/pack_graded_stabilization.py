"""Exact literal data for cubic stabilization of the acquired generic ray."""
from pathlib import Path
import json,sympy as S
root=Path(__file__).resolve().parents[1];out=root/'outputs/graded_stabilization';out.mkdir(exist_ok=True)
old=json.loads((root/'outputs/hopf_structure/certificate.json').read_text())
raw=json.loads((root/'work/full_face_and_cubics.json').read_text())
A=S.symbols('a b c d');x,y=S.symbols('x y');a,b,c,d=A
u,l,p,n,q,r=map(S.Rational,old['ray']['K_coefficients'])
X=a*a+c*c-b*b-d*d;Y=2*(a*b+c*d);Z=2*(a*d-b*c)
F=S.expand(u*X*X+2*l*X*Y+2*p*X*Z+n*Y*Y+2*q*Y*Z+r*Z*Z)
cp=raw['cubic_powers'];qp=raw['quartic_powers'];CM=S.Matrix(raw['cubic_matrix']);QM=S.Matrix(raw['quartic_matrix'])
def vec(poly,powers):
    pp=S.Poly(S.expand(poly),*A)
    return S.Matrix([pp.coeff_monomial(S.prod(z**e for z,e in zip(A,pw))) for pw in powers])
trans=S.Matrix.hstack(*(vec(S.diff(F,z),cp) for z in A));basis=CM.nullspace()
N1=31217529334374656693061585;N2=11227847587653454406233358;N3=11325834422047516078245
example=S.expand(c*c*(N1*b-N2*c-N3*d)/(N1+N2+N3));ev=vec(example,cp)
assert CM*ev==S.zeros(8,1) and trans.rank()==4 and trans.row_join(ev).rank()==5
bc,dc=map(S.Rational,old['ray']['canonical_zero']);kb=S.Rational(old['ray']['A0'][1])
Ac=S.Matrix([1,bc,0,dc]);Rc=S.Matrix([0,kb,0,1])
def rot(v):return S.Matrix([x*v[0]-y*v[2],x*v[1]-y*v[3],y*v[0]+x*v[2],y*v[1]+x*v[3]])
def gam(v):return S.Matrix([v[3],-v[2],v[1],-v[0]])
columns=[]
for pw in cp:
    G=S.prod(z**e for z,e in zip(A,pw));grad=[S.diff(G,z) for z in A];col=[]
    for transform in (lambda v:v,gam):
        K=transform(rot(Ac));R=transform(rot(Rc))
        value=S.expand(2*sum(gg.subs(dict(zip(A,R)),simultaneous=True)*vv for gg,vv in zip(grad,K)))
        col.extend(S.Poly(value,x,y).coeff_monomial(x**(3-i)*y**i) for i in range(4))
    columns.append(col)
FM=S.Matrix.hstack(*map(S.Matrix,columns));assert CM.col_join(FM).rank()==8
cert={
  'base_completion':'../hopf_structure/certificate.json',
  'base_parameters':old['ray']['A0'],
  'quartic_powers':qp,'cubic_powers':cp,
  'quartic_constraint_matrix':raw['quartic_matrix'],'cubic_constraint_matrix':raw['cubic_matrix'],
  'cubic_kernel_basis':[[str(z) for z in v] for v in basis],
  'translation_cubics':[[str(z) for z in trans[:,j]] for j in range(4)],
  'example_cubic_coefficients':[str(z) for z in ev],
  'example_formula':str(example),
  'cubic_dimension':12,'translation_dimension':4,'quartic_face_dimension':1,
  'full_polynomial_face_dimension':28,'modulo_null_lagrangians_dimension':22,
  'uniform_margin_power':64,'stabilization_power':112,
  'example_quadratic_coefficient':str(2**112),
  'scope':'Exact finite data for the graded proof. Global QC uses the acquired angular completion and the form-bound argument in PROOF.txt. No classification of all lower quadratic terms.'}
(out/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
print(json.dumps({'quartic_rank':QM.rank(),'cubic_rank':CM.rank(),'translation_rank':trans.rank(),
 'translation_plus_example_rank':trans.row_join(ev).rank(),'canonical_null_constraint_rank':CM.col_join(FM).rank(),
 'example_l1':str(sum(abs(z) for z in ev)), 'example_nu':str(2**112)},indent=2))
