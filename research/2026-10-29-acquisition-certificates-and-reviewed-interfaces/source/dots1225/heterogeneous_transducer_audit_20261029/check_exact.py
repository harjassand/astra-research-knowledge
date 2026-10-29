import sympy as s,json
from pathlib import Path
r=Path(__file__).parent;z=json.loads(Path('producer-workspace/certificate.json').read_text());B=s.Matrix([[s.Rational(v) for v in row] for row in z['B']]);assert all(B[:,9*i+j]==B[:,9*j+i] for i in range(9) for j in range(9))
u,v=s.symbols('u v',real=True);C0=s.Rational(9,2)*s.eye(4);C1=s.diag(s.Rational(41,18),*[s.Rational(31,54)]*3);C2=s.diag(s.Rational(16,27),0,0,0);a,b=u/8,1-9*u/8;c,d=v/8,1-9*v/8
O=a*c*C0+(a*d+b*c)*C1/2+b*d*C2;p=s.factor(s.trace(O));w=s.factor(3*O[1,1]/p);D=405*u*v-360*(u+v)+512
assert s.simplify(p-D/864)==0 and s.simplify(w-3*(31*(u+v)-9*u*v)/D)==0
N=s.factor(s.diff(w,u)*D**2/3);assert N==15872-4608*v-9315*v*v and N.subs(v,s.Rational(8,9))==4416
assert s.diff(p,u)==(405*v-360)/864
out={'input_swap_symmetry_exact':True,'success':str(p),'infidelity':str(w),'derivative_scaled_numerator':str(N),'derivative_lower_numerator':4416,'success_minimum':'2/9','domain':'0<=u,v<=8/9'};(r/'check_exact.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
