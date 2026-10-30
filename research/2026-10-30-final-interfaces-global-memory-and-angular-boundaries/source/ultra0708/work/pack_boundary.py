"""Produce local literal mathematical data; no external writes."""
from pathlib import Path
import json,sympy as S,os
p=Path(os.environ.get('ASTRA_ANGULAR_CASE',Path(__file__).parent))
cfg=json.loads((p/'case_config.json').read_text()) if (p/'case_config.json').exists() else {'beta':'11/13','r':'28/13'}
a,b,c,d=S.symbols('a b c d',real=True);A=(a,b,c,d)
raw=json.loads((p/'angular_family.json').read_text()); co=json.loads((p/'boundary_rational.json').read_text())
v={k:S.Symbol(k,real=True) for k in co};loc={**v,**{str(x):x for x in A}}
sub={v[k]:S.Rational(x) for k,x in co.items()}
P=[S.Poly(S.sympify(x,locals=loc).subs(sub),A) for x in raw['P']]
bl=json.loads((p/'acoustic_blowup.json').read_text()); pm=json.loads((p/'polynomial_matrices.json').read_text())
def pack2(s):
    return [[*pw,int(co.p),int(co.q)] for pw,co in S.Poly(S.sympify(s,locals=loc),b,d).terms()]
out={'beta':cfg['beta'],'r':cfg['r'],
     'P':[[[*pw,int(co.p),int(co.q)] for pw,co in pp.terms()] for pp in P],
     'kernel':[pack2(x) for x in bl['kernel']], 'w':pack2(bl['w']),'g':pack2(bl['g']),
     'matrices':pm,'cover':json.loads((p/'bernstein_certificate.json').read_text())}
if 'nonpc' in cfg:out['nonpc']=cfg['nonpc']
(p/'literal_boundary_certificate.json').write_text(json.dumps(out))
print('literal primitive terms',sum(len(x) for x in out['P']))
