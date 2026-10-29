"""Independent bank/orientation check through physical SU(2), exact SymPy arithmetic."""
import sympy as s,json,itertools,random
from pathlib import Path
root=Path('producer-workspace/quaternion_oracle_controller_20261029');rng=random.Random(290629)
pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
rows=[]
for file in sorted(root.glob('oracle_*edge*.json')):
 obj=json.loads(file.read_text());bank=json.loads((root/Path(obj['source']).name).read_text());edge=obj['edge']
 for rep in range(5):
  k=[rng.randrange(-6,7) for _ in range(3)];m=7;ss=sum(x*x for x in k);q=[s.Rational(m*m-ss,m*m+ss)]+[s.Rational(2*m*x,m*m+ss) for x in k]
  V=q[0]*s.eye(2)-s.I*sum((q[i+1]*pa[i] for i in range(3)),s.zeros(2))
  C=s.Matrix(3,3,lambda a,b:s.simplify(s.trace(pa[a]*V*pa[b]*V.conjugate().T)/2))
  assert C.T*C==s.eye(3) and C.det()==1
  direct=3*bank['probe_calls']
  for a,b in itertools.product(range(3),repeat=2):
   direct-=9*bank['B'][edge][a][b]*C[a,b]
   for c,d in itertools.product(range(3),repeat=2):direct-=81*bank['C'][edge][a][b][c][d]*C[a,b]*C[c,d]
  poly=sum(t['coefficient']*s.prod(q[i]**t['exponents'][i] for i in range(4)) for t in obj['quartic_coefficients'])
  assert s.simplify(poly-direct)==0
  rows.append({'certificate':file.name,'quaternion':[str(x) for x in q],'physical_SU2_orientation_and_exact_bank_equality':True})
out={'scope':'30 exact physical SU2/quartic orientation identities, independent of finder implementation','cases':rows};Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(len(rows))
