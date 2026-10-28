"""Separate exact-rational replay of direct CPTP primal/dual certificates."""
from pathlib import Path
import json
import sympy as sp
root=Path(__file__).parent
obj=json.loads((root/'finite_decoder_sdp_certificates.json').read_text())
def mat(a):return sp.Matrix([[sp.Rational(r)+sp.I*sp.Rational(i) for r,i in row] for row in a])
rows=[]
for c in obj['certificates']:
 k=c['k'];h=mat(c['H']);p=mat(c['C']);y=mat(c['Y'])
 tr=sp.Matrix(k,k,lambda i,j:p[2*i,2*j]+p[2*i+1,2*j+1])
 assert tr==sp.eye(k)
 for a in [h,p,h-sp.kronecker_product(y,sp.eye(2))]:
  assert a==a.conjugate().T
  assert all(sp.simplify(a[:i,:i].det(method='domain-ge')).is_positive for i in range(1,a.rows+1))
 primal=sp.simplify(sp.trace(h*p));dual=sp.trace(y);gap=sp.simplify(primal-dual)
 assert primal==sp.Rational(c['exact_primal']) and dual==sp.Rational(c['exact_dual']) and gap==sp.Rational(c['exact_gap'])
 assert gap.is_positive and gap<sp.Rational(1,1000000)
 rows.append({'name':c['name'],'k':k,'gap':str(gap),'gap_decimal':float(gap),'exact_TP_PSD_and_dual_feasible':True})
out={'status':'PASS','scope':'Exact rational feasibility and gaps below 1e-6 for three explicitly rounded coefficient SDPs; no assertion that a floating solver is exact or that the full quantum learner was executed.','checks':rows}
(root/'verify_decoder_sdp_certificates.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
