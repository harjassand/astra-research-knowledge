"""Independent chart identities and adversarial non-chart controls."""
import json,sys,hashlib
from pathlib import Path
import sympy as S
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
import acquired_projective_chart as P
r=json.loads((root/'chart_results.json').read_text())
x,y,Y0,Y1=S.symbols('x y Y0 Y1');variables=(x,y);target=(Y0,Y1)
f=S.Matrix([S.sympify(z) for z in r['raw_vector_field']])
phi=S.Matrix([S.sympify(z) for z in r['basis']]);A=S.Matrix([[S.Rational(z) for z in row] for row in r['matrix']])
q=-sum(S.diff(f[i],variables[i]) for i in range(2))/3
identities=[S.expand(z)==0 for z in phi.jacobian(variables)*f+q*phi-A*phi]
chart=phi[1:,:];inverse=S.Matrix([S.sympify(z) for z in r['inverse']])
left=[S.expand(z)==0 for z in chart.subs(dict(zip(variables,inverse)),simultaneous=True)-S.Matrix(target)]
right=[S.expand(z)==0 for z in inverse.subs(dict(zip(target,chart)),simultaneous=True)-S.Matrix(variables)]
assert all(identities+left+right)
raw=[x-x*x,(2-4*x)*y];p=[P.ex.fromsym(z) for z in raw]
cyclic=P.acquire_cyclic_one(p,3);bad=P.acquire_chart(p,3,4)
assert cyclic['status']=='CLOSED' and len(cyclic['basis'])==3 and bad['status']=='SINGULAR_BASEPOINT'
localbad=P.acquire_polynomial_inverse(S.Matrix([x+x*x,y]),variables,4)
assert localbad['status']=='INVERSE_NOT_ACQUIRED'
out={'module_identities':identities,'chart_after_inverse':left,'inverse_after_chart':right,
     'chart_jacobian':str(S.factor(chart.jacobian(variables).det())),
     'nonchart_rank_n_plus_one_control':bad,'locally_invertible_nonpolynomial_inverse_control':localbad,
     'source_hashes':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ['acquired_projective_chart.py','chart_results.json']}}
(root/'audit'/'chart_replay.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
