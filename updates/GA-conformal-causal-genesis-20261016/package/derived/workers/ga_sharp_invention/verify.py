"""Exact verification of the separated-first-potential nonlinear calibration.
This verifies one polynomial identity and rational positive matrices, not the
unresolved all-gradient conformal inequality or historical priority.
"""
from pathlib import Path
import json, hashlib, sympy as S
p=Path(__file__).parent
certificate=json.loads((p/'SEPARATED_STRESS_EXACT_CERTIFICATE.json').read_text())
a,b,c,d,s=S.symbols('a b c d s', real=True)
v=(a,b,c,d,s)
A=a+s; D=d+s
j=A*D-b*c
J=((A-D)**2+(b+c)**2)**2/S.Integer(8)+j*j+(A*A+c*c)*j
sigma1=-3*s*s*b+b**3/S.Integer(2)
sigma2=3*s**3+7*s*s*a+5*s*a*a+a**3/S.Integer(2)
G=S.expand(J-2*s**4-5*s**3*a-sigma1*c-sigma2*d)
mons=[S.prod(t**e for t,e in zip(v,k)) for k in certificate['mons']]
z=S.Matrix(mons)
Q=S.Matrix([[S.Rational(t) for t in row] for row in certificate['gram']])
checks={}
checks['exact_polynomial_identity']=S.expand((z.T*Q*z)[0]-G)==0
blocks=certificate['blocks']
checks['exact_block_diagonal']=all(Q[i,j]==0 for i in blocks[0] for j in blocks[1])
checks['covers_basis']=sorted(sum(blocks,[]))==list(range(13))
for label,epsilon in [('positive',S.Integer(0)),('quantitative_floor',S.Rational(1,128))]:
 pivots=[]
 for block in blocks:
  B=Q.extract(block,block)-epsilon*S.eye(len(block))
  dets=[S.factor(B[:k,:k].det(method='domain-ge')) for k in range(1,len(block)+1)]
  if not all(x>0 for x in dets):raise RuntimeError((label,'nonpositive exact minor',dets))
  pivots.append([str(dets[0])]+[str(S.factor(dets[k]/dets[k-1])) for k in range(1,len(dets))])
 checks[label+'_all_sylvester_minors_positive']=True
 certificate[label+'_ldl_pivots']=pivots
# Chain rule coefficient of f_xy in div sigma, because a_y=b_x=f_xy.
W=S.factor(S.diff(sigma1,b)+S.diff(sigma2,a))
checks['exact_divergence_coefficient']=S.expand(W-(4*s*s+10*s*a+S.Rational(3,2)*(a*a+b*b)))==0
M4=sum(m*m for m in mons if not m.has(s))
checks['complete_gradient_quadratic_monomials']=S.expand(M4-(a**4+b**4+c**4+d**4+a*a*b*b+a*a*c*c+a*a*d*d+b*b*c*c+b*b*d*d+c*c*d*d))==0
checks['quartic_control']=S.expand(M4-(a*a+b*b+c*c+d*d)**2/S.Integer(2)-(a**4+b**4+c**4+d**4)/S.Integer(2))==0
checks['source_identity_at_zero_background']=S.expand(G.subs(s,0)-(J.subs(s,0)-(a**3*d+b**3*c)/2))==0
if not all(checks.values()):raise RuntimeError(checks)
certificate['exact_divergence_coefficient']=str(W)
(p/'SEPARATED_STRESS_EXACT_CERTIFICATE.json').write_text(json.dumps(certificate,indent=2)+'\n')
receipt={'status':'PASS','scope':'Single polynomial nonlinear-stress identity and exact rational positive definiteness; no proof of universal Gamma_1 <= 1','checks':checks,'quantitative_floor':'1/128','certificate_sha256':hashlib.sha256((p/'SEPARATED_STRESS_EXACT_CERTIFICATE.json').read_bytes()).hexdigest()}
(p/'VERIFICATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
