"""Independent deterministic replay of all serialized raw circuit certificates.
Does not import the producer or its Circuit class; expands with SymPy Poly.
The algorithm's general admission remains Monte Carlo; these runs gain replay.
"""
import json,hashlib,time
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
source=json.loads((ROOT/'quadratic_circuit_results.json').read_text())
reports=[]
for r in source['runs']:
 t=time.perf_counter();circ=r['raw_circuit'];n=circ['n'];x=s.symbols('x0:'+str(n));zero=s.Poly(0,*x);vals=[]
 for k,node in enumerate(circ['nodes']):
  op,*a=node
  if op=='var':v=s.Poly(x[a[0]],*x)
  elif op=='const':v=s.Poly(s.Rational(a[0]),*x)
  else:
   assert all(0<=j<k for j in a)
   if op=='add':v=vals[a[0]]+vals[a[1]]
   elif op=='mul':v=vals[a[0]]*vals[a[1]]
   else:raise AssertionError(op)
  vals.append(v)
 f=[vals[j] for j in circ['roots']];q=-sum((p.diff(x[i]) for i,p in enumerate(f)),zero)/(n+1)
 phi=[s.Poly(1,*x)]+[s.Poly(s.sympify(v),*x) for v in r['chart']]
 A=s.Matrix(r['matrix']).applyfunc(s.Rational)
 checks=[]
 for i,p in enumerate(phi):
  residual=q*p+sum((f[j]*p.diff(x[j]) for j in range(n)),zero)-sum((A[i,j]*v for j,v in enumerate(phi)),zero)
  checks.append(residual.is_zero);assert checks[-1]
 C=s.Matrix([p.as_expr() for p in phi[1:]]);origin=dict.fromkeys(x,0);offset=C.subs(origin);J=C.jacobian(x).subs(origin)
 assert J.det()!=0
 F=(J.inv()*(C-offset)).applyfunc(s.expand)
 expected=s.Matrix([x[i]+(x[i+1]**2 if i<n-1 else 0) for i in range(n)])
 # Test-family identity, not a generic acceptance prerequisite.
 assert all(s.expand(v)==0 for v in F-expected)
 R=s.eye(n+1);R[1:,0]=offset;R[1:,1:]=J
 M=R.inv()*A*R;assert M==s.Matrix(r['normalized_matrix']).applyfunc(s.Rational)
 target=s.zeros(n+1)
 for j in range(n//2):target[0,1+2*j]=1;target[1+2*j,2+2*j]=-(j+1);target[2+2*j,1+2*j]=j+1
 assert M==target
 report={'n':n,'raw_total_terms':sum(len(v.terms()) for v in f),'raw_degree':max(v.total_degree() for v in f),'global_closure_components':checks,'normalized_chart_is_chain':True,'normalized_matrix_exactly_rotation_form':True,'independent_replay_seconds':time.perf_counter()-t}
 reports.append(report);print(report,flush=True)
hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['quadratic_circuit_acquisition.py','quadratic_circuit_results.json','audit/quadratic_circuit_replay.py']}
assert source['source_sha256']==hashes['quadratic_circuit_acquisition.py']
out={'reports':reports,'source_hashes':hashes,'scope':'Deterministic coefficient replay for these serialized examples only; general circuit algorithm still Monte Carlo.'}
(ROOT/'audit'/'quadratic_circuit_replay.json').write_text(json.dumps(out,indent=2))
