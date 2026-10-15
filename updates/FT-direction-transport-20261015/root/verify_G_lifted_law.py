from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import sympy as s
OUT=Path(__file__).resolve().parent
I=s.eye(2);J=s.diag(1,-1);pts=[36*I,-36*I,J,-J];weights=[s.Rational(1,2594)]*2+[s.Rational(648,1297)]*2
assert sum(weights)==1;mean=sum((p*w for p,w in zip(pts,weights)),s.zeros(2));assert mean==s.zeros(2);assert sum(w*p.det() for p,w in zip(pts,weights))==0
def G(A):
 u=A[0,0]**2+A[1,0]**2;v=A[0,1]**2+A[1,1]**2;j=A.det();return 3*(u+v-2*j)**2+s.Rational(35,24)*u*u+j*j-s.Rational(5,2)*j*u
value=sum(w*G(p) for p,w in zip(pts,weights));moment=sum(w*sum(x*x for x in p)**2 for p,w in zip(pts,weights));assert value==-s.Rational(1350,1297);assert moment==5184
bound=s.Rational(1350,1297)/(60*19**3);assert 0<bound<1;assert 48+s.Rational(35,6)+1+5==s.Rational(359,6)<60
r=dict(status='EXACT_PASS',scope='Six exact finite arithmetic identities supporting the separately proved universal heat/compatibility consequence; no sampled field or physical validation.',mean_matrix=[[str(x) for x in row] for row in mean.tolist()],det_mean='0',G_mean=str(value),fourth_norm_moment=str(moment),rational_W4_separation=str(bound),approximate_separation=float(bound),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(OUT/'G_LIFTED_LAW_CHECK.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
