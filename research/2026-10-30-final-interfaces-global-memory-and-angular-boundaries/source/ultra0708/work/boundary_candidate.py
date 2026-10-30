"""Rational candidate and diagnostics. All numeric checks are diagnostics only."""
from pathlib import Path
import sympy as S,numpy as np,json,time,os
p=Path(os.environ.get('ASTRA_ANGULAR_CASE',Path(__file__).parent))
cfg=json.loads((p/'case_config.json').read_text()) if (p/'case_config.json').exists() else {'beta':'11/13','r':'28/13'}
j=json.loads((p/'boundary_jets.json').read_text())
loc={v:S.Symbol(v,real=True) for v in j['variables']}
pr=json.loads((p/'boundary_jet_proposal.json').read_text())
sub={loc[v]:S.Rational(round(pr['parameters'][v]*10000),10000) for v in j['free']}
co={v:S.sympify(x,locals=loc).subs(sub) for v,x in zip(j['variables'],j['solution'])}
(p/'boundary_rational.json').write_text(json.dumps({k:str(v) for k,v in co.items()},indent=2)+'\n')
a,b,c,d,beta,r=S.symbols('a b c d beta r',real=True)
loc.update({str(x):x for x in (a,b,c,d,beta,r)})
data=json.loads((p/'angular_family.json').read_text())
C=S.Matrix([[S.sympify(x,locals=loc) for x in row] for row in data['C']])
C=C.subs({loc[k]:val for k,val in co.items()}).subs({a:1,c:0,beta:S.Rational(cfg['beta']),r:S.Rational(cfg['r'])}).applyfunc(S.expand)
(p/'boundary_matrix.json').write_text(json.dumps([[str(x) for x in row] for row in C.tolist()]))
ff=S.lambdify((b,d),C,'numpy',cse=True)
worst=(1e100,None)
for bb in np.linspace(0,1,171):
    for dd in np.linspace(-1,1,341):
        T=1+bb*bb+dd*dd; vals=np.linalg.eigvalsh(np.array(ff(bb,dd),float)/T**3)
        if vals[0]<worst[0]: worst=(float(vals[0]),[float(bb),float(dd)])
print('dense square min',worst,flush=True)
(p/'boundary_dense_diagnostic.json').write_text(json.dumps({'points':171*341,'minimum':worst,'scope':'floating finite grid only'},indent=2)+'\n')
