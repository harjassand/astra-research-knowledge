"""Independent coefficient replay of the serialized circuit-acquired decoder."""
import json,hashlib,time
from pathlib import Path
import sympy as S
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'results.json').read_text())
c=json.loads((root/'circuit_results.json').read_text())[-1]
x,y=S.symbols('x y')
f=[S.Poly(S.sympify(z),x,y) for z in data['raw_vector_field']]
q=-(f[0].diff(x)+f[1].diff(y))/3;m=c['weight']
def T(p):return f[0]*p.diff(x)+f[1]*p.diff(y)+m*q*p
cache={(0,0):S.Poly(1,x,y),(1,0):S.Poly(x,x,y),(2,0):S.Poly(y,x,y)}
def jet(i,k):
    if (i,k) not in cache:cache[i,k]=T(jet(i,k-1))
    return cache[i,k]
start=time.perf_counter();zero=S.Poly(0,x,y)
basis=[sum((S.Rational(z)*jet(i,k) for i,k,z in b),zero) for b in c['basis_jet_combinations']]
checks=[]
for i,row in enumerate(c['matrix']):
    checks.append((T(basis[i])-sum((S.Rational(z)*p for z,p in zip(row,basis)),zero)).is_zero)
for i,row in enumerate(c['seed_reconstruction']):
    checks.append((cache[i,0]-sum((S.Rational(z)*p for z,p in zip(row,basis)),zero)).is_zero)
assert all(checks)
out={'exact_identity_checks':checks,'count':len(checks),'seconds':time.perf_counter()-start,
     'circuit_code_sha256':hashlib.sha256((root/'circuit_jets.py').read_bytes()).hexdigest(),
     'circuit_output_sha256':hashlib.sha256((root/'circuit_results.json').read_bytes()).hexdigest()}
(root/'audit'/'circuit_output_replay.json').write_text(json.dumps(out,indent=2))
print(out)
