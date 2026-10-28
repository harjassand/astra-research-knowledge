"""Independent exact coefficient/jet constants, no producer imports or floats."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json
import sympy as s

a,b,c,d=s.symbols('a b c d'); vs=(a,b,c,d)
u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
x=u-v;y=2*w;z=2*q
F=s.Rational(55220381,10**10)*(u*u+v*v)+s.Rational(114430029,625000000)*u*v-s.Rational(801761987,5000000000)*w*w+s.Rational(118849817,4000000000)*q*(u-v)
coef=[s.Rational(6222019,200000000),s.Rational(1686519911,10**10),s.Rational(81172813,2000000000),s.Rational(1726116771,10**10),s.Rational(128626163,5000000000),s.Rational(373321239,2000000000)]
p=sum(t*m for t,m in zip(coef,[x**3,x*x*z,x*z*z,z**3,x*y*y,y*y*z]))
C=sum(abs(t) for t in s.Poly(F,*vs).coeffs())
P=sum(abs(t) for t in s.Poly(p,*vs).coeffs())
U=12*C+11*P;V=10*P;M=(U*U+V*V)*2400000
assert s.Poly(F,*vs).total_degree()==4 and s.Poly(p,*vs).total_degree()==6
base=Path(__file__).resolve().parents[3]/'sol8_opportunity_selection_20261027'
bindings={}
for name in ['rational_selector/PROOF.md','rational_selector/EXACT_RATIONAL_SUPPORT.json']:
    bindings[name]=hashlib.sha256((base/name).read_bytes()).hexdigest()
assert bindings['rational_selector/PROOF.md']=='f1533738a7244823a6005741010bb2b0edf9c9617de3f973235374efaa11af32'
assert bindings['rational_selector/EXACT_RATIONAL_SUPPORT.json']=='ecbd2bd7d333abe79810625c7be6e1d218d4411095cc28c049fa731958059191'
out={'status':'EXACT_CONSTANTS_AND_INPUT_BINDINGS_PASS','C':str(C),'P':str(P),'U':str(U),'V':str(V),'delta':'1/2400000','M_R1':str(M),'F_terms':len(s.Poly(F,*vs).terms()),'p_terms':len(s.Poly(p,*vs).terms()),'bindings':bindings}
Path(__file__).with_name('EXACT_CONSTANTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
