from pathlib import Path
from fractions import Fraction as F
import sympy as s
import json,hashlib,math
x,z,a=s.symbols('x z a',positive=True)
eta=a*z*x*(1-x)/(1-z*x)
t=s.symbols('t',positive=True)
assert s.simplify(s.diff(eta,x).subs({z:1-t*t,x:1/(1+t)}))==0
assert s.simplify(eta.subs({z:1-t*t,x:1/(1+t)})-a*(1-t)/(1+t))==0
m=s.Matrix([[1,s.Rational(1,2)],[s.Rational(1,2),1]])
fixtures=[(m,s.eye(2),s.Rational(1)),(s.Matrix([[1,s.Rational(1,2)],[s.Rational(1,20),s.Rational(1,10)]]),s.diag(1,10),s.Rational(1,10)),(s.Matrix([[s.Rational(1,10),s.Rational(1,20)],[s.Rational(1,2),1]]),s.diag(10,1),s.Rational(10))]
records=[]
for L,D,ratio in fixtures:
 assert D*L==m
 H=(L+L.T)/2
 assert H[0,0]>0 and H.det()>0
 zz=s.factor(L[0,1]*L[1,0]/(L[0,0]*L[1,1]));assert zz==s.Rational(1,4)
 assert L[1,0]/L[0,1]==ratio
 records.append(dict(matrix=str(L),gain=str(D),symmetric_determinant=str(H.det()),z=str(zz),efficiency_multiplier=str(ratio)))
for z0 in [F(i,100) for i in range(1,100)]:
 e=(1-math.sqrt(1-float(z0)))/(1+math.sqrt(1-float(z0)))
 for u in [0,.1,.5,.9,1]:
  aa=e+(1/e-e)*u
  assert float(z0)*(aa+1)**2<=4*aa+1e-10
  assert e*e-1e-12<=aa*e<=1+1e-12
# Exact3port gain cycles and normalized-square invariants.
L=s.Matrix([[3,1,s.Rational(1,2)],[1,4,1],[s.Rational(1,2),1,2]])
A=s.diag(2,7,3);B=s.diag(5,11,13);M=A*L*B
assert M[0,1]*M[1,2]*M[2,0]==M[1,0]*M[2,1]*M[0,2]
for i in range(3):
 for j in range(i):assert s.factor(M[i,j]*M[j,i]/(M[i,i]*M[j,j]))==L[i,j]**2/(L[i,i]*L[j,j])
out=dict(status='PASS',scope='Exact algebra and supplied passive matrix countermodels; no physical acquisition or historical novelty.',fixtures=records,scalar_cases=495,three_port_gain_cycle=True,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
Path(__file__).with_name('TERMINAL_CALIBRATION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
