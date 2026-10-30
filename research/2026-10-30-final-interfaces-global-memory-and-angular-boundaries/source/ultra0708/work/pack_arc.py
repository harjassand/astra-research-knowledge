from pathlib import Path
import sympy as S,json
p=Path(__file__).parent;out=Path(__file__).parents[1]/'outputs/angular_boundary'
j=json.loads((p/'generic_acoustic_jets.json').read_text());raw=json.loads((p/'angular_family.json').read_text())
tau=S.Symbol('tau',real=True);A=S.symbols('a b c d',real=True)
v=[S.Symbol(n,real=True) for n in raw['variables']];loc={str(x):x for x in (*A,*v,tau)}
funcs={k:S.Rational(x) for k,x in j['fixed_coefficients'].items()}
funcs.update({k:S.sympify(x,locals=loc) for k,x in zip(j['variables'],j['solution'])})
def pack_function(ex):
    nn,dd=S.fraction(S.cancel(ex));nn=S.Poly(nn,tau);dd=S.Poly(dd,tau)
    common=S.ilcm(*(x.q for x in nn.all_coeffs()+dd.all_coeffs()))
    return {'num':[int(nn.nth(i)*common) for i in range(nn.degree()+1)],'den':[int(dd.nth(i)*common) for i in range(dd.degree()+1)]}
basis=[]
for ex in raw['P']:
    rows=[]
    for powers,co in S.Poly(S.sympify(ex,locals=loc),*A).terms():
        weights=[]
        for i,x in enumerate(v):
            val=S.diff(co,x)
            if val:weights.append([i,int(val.p),int(val.q)])
        assert S.expand(co-sum(S.Rational(n,d)*v[i] for i,n,d in weights))==0
        rows.append({'powers':list(powers),'weights':weights})
    basis.append(rows)
data={'variables':list(map(str,v)),'functions':[pack_function(funcs[str(x)]) for x in v],
      'primitive_basis':basis,'checks_from_construction':j['checks'],
      'scope':'Explicit rational primitive family near tau=1/30. The positivity radius is qualitative, from the strict finite certificate at the center.'}
(out/'arc_data.json').write_text(json.dumps(data))
print('arc data bytes',(out/'arc_data.json').stat().st_size)
