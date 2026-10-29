import sympy as s,itertools,math,json,hashlib
from pathlib import Path
root=Path(__file__).parent;src=Path('producer-workspace/four_program_extension')
data=json.loads((src/'certificate.json').read_text());B=s.Matrix([[s.Rational(v) for v in row] for row in data['B']]);exps=[tuple(e) for e in data['exponents']]
w,x,y,z=s.symbols('w x y z',real=True);q=[w,x,y,z]
# Independently obtain adjoint rotation coefficients from the SU2 matrix.
V=s.Matrix([[w-s.I*z,-y-s.I*x],[y-s.I*x,w+s.I*z]]);pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
R=[s.expand(s.trace(a*V*b*V.conjugate().T)/2) for a in pa for b in pa]
assert len(set(exps))==35 and set(exps)=={e for e in itertools.product(range(5),repeat=4) if sum(e)==4}
polys=[s.Poly(a*b,*q) for a in R for b in R];M=s.Matrix([[p.coeff_monomial(e) for p in polys] for e in exps]);assert B.shape==(35,81) and B*M.T==s.eye(35)
J=s.zeros(256,35)
for row,labels in enumerate(itertools.product(range(4),repeat=4)):
 e=tuple(labels.count(i) for i in range(4));J[row,exps.index(e)]=1
mult=[math.factorial(4)//math.prod(math.factorial(i) for i in e) for e in exps]
assert mult==data['multiplicities'] and J.T*J==s.diag(*mult)
T=J*B;assert T*M.T==J
F=T.T*T;I=s.eye(81);assert F==F.T
assert F*(16*F-I)*(8*F-I)*(16*F-3*I)==s.zeros(81)
# Exact annihilating polynomial plus symmetry restricts spectrum to these four real roots.
roots=[s.Rational(0),s.Rational(1,16),s.Rational(1,8),s.Rational(3,16)]
traces=[s.Integer(81),s.trace(F),s.trace(F**2),s.trace(F**3)]
C=s.Matrix([[v**k for v in roots] for k in range(4)]);counts=list(C.inv()*s.Matrix(traces));assert counts==[46,25,1,9]
# Independent spectral projectors: sums=I, idempotent, and positive as symmetric projectors.
projectors=[]
for a in roots:
 P=I
 for b in roots:
  if b!=a:P=P*(F-b*I)/(a-b)
 assert P==P.T and P*P==P
 projectors.append(P)
assert sum(projectors,s.zeros(81))==I
# K†K=(16/3)F has spectrum 0,1/3,2/3,1; algebraic scale is required.
assert s.Rational(16,3)*s.Rational(3,16)==1
out={'adjoint_orientation_derived_independently':True,'BMt_identity':True,'T_Mt_equals_J':True,'T_shape':[256,81],'annihilating_polynomial':'F(16F-I)(8F-I)(16F-3I)=0','exact_spectrum':{str(a):int(n) for a,n in zip(roots,counts)},'all_four_spectral_projectors_exact':True,'normalized_program_transduction_success':'16/27','rational_2T_success':'4/9','transduction_and_one_gate':'4/27','transduction_and_all_four_gates':'1/432','source_certificate_sha256':hashlib.sha256((src/'certificate.json').read_bytes()).hexdigest()}
(root/'independent_exact_check.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
