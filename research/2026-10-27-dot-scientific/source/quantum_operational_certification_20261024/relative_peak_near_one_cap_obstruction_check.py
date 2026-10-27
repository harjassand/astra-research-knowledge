import sympy as s
from pathlib import Path
import json
c,d,p,t=s.symbols('c d p t',real=True)
h=2*p*p/((1-c)*(d-1));K=c*h+2*p*p/(1-c)
U=s.diag(1,h*t*t);V=s.Matrix([[1-t*t,p*t],[p*t,K*t*t]])
assert s.simplify((V-c*U).det()-p*p*t*t*(1-2*t*t/(1-c)))==0
assert s.simplify((d*U-V).det()-p*p*t*t*(1+2*t*t/(d-1)))==0
assert s.simplify((s.eye(2)-V).det()-t*t*(1-p*p-K*t*t))==0
B=(U+8*V)/9;a=1-B[0,0];b=a*a+B[0,1]**2
assert s.simplify(b/a-s.Rational(8,9)*(p*p+t*t))==0
floor=s.Rational(8,9)*s.Rational(99,100)**2
assert floor==s.Rational(1089,1250)>s.Rational(5,6)
# Fully rational near-unit sample; checks BOTH sectors directly.
k=s.Rational(1001,1000);cv=(9/k-1)/8;dv=k/(9-8*k)
vals={c:cv,d:dv,p:s.Rational(99,100),t:s.Rational(1,10**6)}
Uv=U.subs(vals);Vv=V.subs(vals);Bv=(Uv+8*Vv)/9
for M in [Uv,Vv,s.eye(2)-Vv,k*Bv-Uv,k*Bv-Vv]:
 assert M[0,0]>0 and M.det()>0
assert Uv[1,1]<1
report={'status':'PASS','all_three_symbolic_determinants':True,'b_over_a_formula':'8(p^2+t^2)/9','limiting_ratio_p_99_over_100':str(floor),'exact_sample_relative_peak':str(k),'sample_t':'1/1000000','both_peak_sectors_checked':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
