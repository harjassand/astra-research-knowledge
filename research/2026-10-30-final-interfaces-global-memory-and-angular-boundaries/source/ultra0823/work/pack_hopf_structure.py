from pathlib import Path
import json,sympy as S
here=Path(__file__).parent;out=here.parent/'outputs/hopf_structure';out.mkdir(exist_ok=True)
raw=json.loads((here/'general_angular_basis.json').read_text());nf=json.loads((here/'exposed_normal_form.json').read_text())
data=json.loads((here/'general_ray/candidate.json').read_text());data['cover']=json.loads((here/'general_ray/cover.json').read_text())
A=S.symbols('a b c d',real=True);v=[S.Symbol(n,real=True) for n in raw['variables']];loc={str(x):x for x in (*A,*v)}
basis=[]
for expr in raw['P']:
    rows=[]
    for powers,co in S.Poly(S.sympify(expr,locals=loc),*A).terms():
        weights=[]
        for i,x in enumerate(v):
            val=S.diff(co,x)
            if val:weights.append([i,int(val.p),int(val.q)])
        assert S.expand(co-sum(S.Rational(n,dd)*v[i] for i,n,dd in weights))==0
        rows.append({'powers':list(powers),'weights':weights})
    basis.append(rows)
abc=A[:3]
normal=[[[*powers,int(co.p),int(co.q)] for powers,co in S.Poly(S.sympify(x,locals=loc),*abc).terms()] for x in nf['coefficient_polynomials']]
data['primitive_basis']=basis;data['profile_variables']=raw['variables'];data['dependent_indices']=[0,1,2]
data['normal_form']=normal
(out/'certificate.json').write_text(json.dumps(data))
prefix=(here.parent/'outputs/angular_boundary/receive_boundary.py').read_text().split('def main():')[0]
(out/'receive.py').write_text(prefix+(here/'receive_hopf_tail.py').read_text())
print('proof data bytes',(out/'certificate.json').stat().st_size)
