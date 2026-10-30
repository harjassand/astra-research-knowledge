from pathlib import Path
import sympy as S,json
p=Path(__file__).parent
t=S.Symbol('t'); j=json.loads((p/'boundary_jets.json').read_text()); mod=S.sympify(j['modulus'])
def red(x): return S.rem(S.expand(x),mod,t)
K=S.Matrix([S.sympify(x) for x in j['kernel']]); scale=S.Rational(1183,2112)
K=K*scale
a,b,c,d=K; T=red(a*a+b*b+c*c+d*d)
num=[red(a*a+c*c-b*b-d*d),red(2*(a*b+c*d)),red(2*(a*d-b*c))]
ni=[red(x*S.invert(T,mod,t)) for x in num]
out={'kernel_scaled':list(map(str,K)),'hopf':list(map(str,ni)),
     'squared_hopf':list(map(str,[red(x*x) for x in ni]))}
print(json.dumps(out,indent=2))
(p/'boundary_geometry.json').write_text(json.dumps(out,indent=2)+'\n')
