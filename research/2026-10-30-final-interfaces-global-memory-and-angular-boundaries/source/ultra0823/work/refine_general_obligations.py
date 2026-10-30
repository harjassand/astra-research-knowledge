from pathlib import Path
import json,sympy as S,numpy as np
from scipy.optimize import minimize
case=Path(__file__).parent/'general_ray';j=json.loads((case/'candidate.json').read_text());b,d=S.symbols('b d')
exact=S.Matrix([[sum(S.Rational(n,dd)*b**ib*d**id_ for ib,id_,n,dd in ent) for ent in row] for row in j['C']])
fun=S.lambdify((b,d),exact.applyfunc(lambda x:S.Poly(x,b,d).as_expr().evalf(16)),'numpy',cse=True)
bc,dc=map(float,map(S.Rational,j['ray']['canonical_zero']))
def value(x):
    bb,dd=x;dist=(bb-bc)**2+(dd-dc)**2
    if dist<1e-8:return 1.
    return float(np.linalg.eigvalsh(fun(bb,dd))[0])/((1+bb*bb+dd*dd)**3*dist)
pts=[(value((bb,dd)),bb,dd) for bb in np.linspace(-1,1,97) for dd in np.linspace(-1,1,97)]
pts.sort();saved=[];path=case/'obligation_points.json';old=json.loads(path.read_text()) if path.exists() else []
starts=[(bb,dd) for _,bb,dd in pts[:8]]+[tuple(map(float,map(S.Rational,row))) for row in old]
for bb,dd in starts:
    fit=minimize(value,[bb,dd],method='L-BFGS-B',bounds=[(-1,1),(-1,1)],options={'ftol':1e-14,'gtol':1e-10,'maxiter':150})
    if fit.fun>=-1e-9:continue
    point=[S.Rational(round(float(x)*10**8),10**8) for x in fit.x]
    if any(np.linalg.norm(np.array(list(map(float,point)))-np.array(x))<1e-5 for x in saved):continue
    mat=exact.subs({b:point[0],d:point[1]});det=S.factor(mat.det(method='domain-ge'))
    print('weighted minimum',fit.fun,'point',list(map(str,point)),'exact determinant negative',bool(det<0),flush=True)
    saved.append(list(map(float,point)))
    if det<0 and list(map(str,point)) not in old:old.append(list(map(str,point)))
    if len(saved)>=3:break
path.write_text(json.dumps(old,indent=2)+'\n')
print('added',len(saved),'counterexample candidates',flush=True)
