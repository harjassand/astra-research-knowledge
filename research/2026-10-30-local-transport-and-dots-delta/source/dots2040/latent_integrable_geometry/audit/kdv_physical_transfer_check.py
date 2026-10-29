"""Exact receipt for odd-degree physical Abel differential determinant bounds.
This tests a lemma, not a KdV evolution algorithm.
"""
import sympy as s,json
from pathlib import Path
out=[]
for g in range(1,9):
  for mode in ['endpoints','midpoints','close_endpoints']:
    E=[s.Rational(j,2**(g if mode=='close_endpoints' else 0)) for j in range(2*g+1)]
    M=max(s.Integer(1),*map(abs,E));delta=min(s.Integer(1),*[E[j+1]-E[j] for j in range(2*g)])
    mu=[(E[2*j-1]+E[2*j])/2 if mode=='midpoints' else E[2*j-(j%2)] for j in range(1,g+1)]
    H=[s.prod(abs(mu[j-1]-E[k]) for k in range(2*g+1) if k not in [2*j-1,2*j]) for j in range(1,g+1)]
    V=s.Matrix(g,g,lambda k,j:mu[j]**k)
    detsq=s.cancel(V.det()**2/s.prod(H))
    lower=delta**(g*(g-1))/(2*M)**(g*(2*g-1))
    assert detsq>=lower>0
    assert V.det()==s.prod(mu[j]-mu[i] for i in range(g) for j in range(i+1,g))
    out.append({'genus':g,'case':mode,'determinant_squared':str(detsq),'lower_bound_squared':str(lower),'pass':True})
Path(__file__).with_suffix('.json').write_text(json.dumps({'scope':'exact determinant/endpoint continuation lemma only; no KdV evolution implementation','cases':out},indent=2))
print('Passed',len(out),'exact determinant/endpoint-bound cases')
