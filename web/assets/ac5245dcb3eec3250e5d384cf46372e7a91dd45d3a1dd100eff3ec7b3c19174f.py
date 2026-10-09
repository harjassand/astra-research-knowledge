import sympy as s
from mpmath import iv
import json
iv.dps=70
r0,r1,r2,a,b=s.symbols('r0 r1 r2 a b',real=True)
v=[r0,r1,r2,a,b]
F=(r0*r0+r1*r1-2*r0*r1*s.cos(a))**s.Rational(-1,2)+(r0*r0+r2*r2-2*r0*r2*s.cos(b))**s.Rational(-1,2)+(r1*r1+r2*r2-2*r1*r2*s.cos(a-b))**s.Rational(-1,2)
H=s.hessian(F,v)
fun=s.lambdify(v,H.tolist(),modules=[{'cos':iv.cos,'sin':iv.sin,'sqrt':iv.sqrt}])
def box(c): return iv.mpf(c)+iv.mpf(['-1e-24','1e-24'])
profiles={'P':['1','3.7632172480656902','0.4252867292159305',box('-2.31519449795229144495537793024521332991267343417911360489657'),box('2.93625533340134823331274447381288438335285498495327179821596')], 'Q':['1','1.7669840027711121',box('0.651229694383177673341856698546369810578028841843670943555922'),box('1.99517837342569275658441495398085752254415210737441872519361'),box('-2.38590226052078909118582472062049710156516203011416797569951')]}
res={}
for name,values in profiles.items():
 values=[iv.mpf(x) if isinstance(x,str) else x for x in values]
 h=fun(*values)
 aa,ab,bb=h[3][3],h[3][4],h[4][4]
 det=aa*bb-ab*ab
 assert aa.a>0 and det.a>0
 inv=[[bb/det,-ab/det],[-ab/det,aa/det]]
 reduced=[[h[i][j]-sum(h[i][3+k]*inv[k][l]*h[3+l][j] for k in range(2) for l in range(2)) for j in range(3)] for i in range(3)]
 signs={str((i,j)):bool(reduced[i][j].a>0 or reduced[i][j].b<0) for i,j in [(0,1),(0,2),(1,2)]}
 assert all(signs.values())
 res[name]={'Hangulardet':str(det),'reduced_radial_hessian':[[str(x) for x in row] for row in reduced],'all_cross_nonzero':all(signs.values())}
print(json.dumps(res,indent=2))
