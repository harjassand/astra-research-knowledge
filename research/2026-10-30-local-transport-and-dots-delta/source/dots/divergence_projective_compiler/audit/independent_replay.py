"""Independent SymPy coefficient replay; does not import producer algebra code."""
import json, hashlib, time
from pathlib import Path
import sympy as S

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'results.json').read_text())
x,y,u,v=S.symbols('x y u v')
raw=[S.sympify(f) for f in data['raw_vector_field']]
q=S.expand(-(S.diff(raw[0],x)+S.diff(raw[1],y))/3)
record=next(z for z in data['runs'] if z['status']=='EXACT_CLOSURE')
m=record['weight']
def decode(poly):
    return S.Add(*[S.Rational(c)*x**a[0]*y**a[1] for a,c in poly])
phi=list(map(decode,record['basis']))
A=S.Matrix([[S.Rational(c) for c in row] for row in record['matrix']])
start=time.perf_counter();valid=[]
for i,p in enumerate(phi):
    residual=raw[0]*S.diff(p,x)+raw[1]*S.diff(p,y)+m*q*p
    residual-=sum(A[i,j]*phi[j] for j in range(len(phi)))
    valid.append(S.Poly(S.expand(residual),x,y).is_zero)
assert all(valid)
monomials=sorted({a for p in phi for a,c in S.Poly(p,x,y).terms()})
coeff=S.Matrix([[S.Poly(p,x,y).coeff_monomial(a) for a in monomials] for p in phi])
rank=coeff.rank();assert rank==len(phi)==13
h=S.Matrix([u+v**2,v+(u+v**2)**2]);g=S.Matrix([u-u*u,7*v-u*v])
pull=[S.expand(f.subs({x:h[0],y:h[1]},simultaneous=True)) for f in raw]
push=h.jacobian([u,v])*g
mapping=[S.expand(pull[i]-push[i])==0 for i in range(2)]
covariance=S.expand(q.subs({x:h[0],y:h[1]},simultaneous=True)-(u-S.Rational(8,3)))==0
assert all(mapping) and covariance
out={'closure_identity_results':valid,'number_identities':len(valid),'exact_coefficient_rank':rank,
     'q_from_raw':str(q),'hidden_pushforward_verified':mapping,'divergence_covariance_verified':covariance,
     'seconds':time.perf_counter()-start,'source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
       for name in ['results.json','experiment.py','PROOF.md']}}
(ROOT/'audit'/'independent_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
