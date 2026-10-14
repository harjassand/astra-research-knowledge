"""Exact test of source/mass-changing energy envelope on reversible networks.
Only small proof diagnostics; large-domain envelope uses algebra, not these states.
"""
import sympy as s, random,json
from pathlib import Path
rng=random.Random(7339);checks=0
for n in range(2,7):
 for rep in range(4):
    m=s.Matrix([s.Rational(rng.randint(1,7),7) for _ in range(n)])
    ratio=s.Rational(101,100) if rep%2 else s.Rational(2)
    weights=[s.Rational(1) if rng.randrange(2) else 1/ratio for _ in range(n)]
    mt=s.Matrix([m[i]*weights[i] for i in range(n)])
    A=s.zeros(n);At=s.zeros(n)
    for i in range(n):
     c=s.Rational(rng.randint(1,5),11);A[i,i]+=c;At[i,i]+=c*weights[i]
     for j in range(i):
      c=s.Rational(rng.randint(1,5),13);ct=c*min(weights[i],weights[j])
      for X,z in [(A,c),(At,ct)]:X[i,i]+=z;X[j,j]+=z;X[i,j]-=z;X[j,i]-=z
    t0=(m.T*A.inv()*m)[0]/sum(m);t1=(mt.T*At.inv()*mt)[0]/sum(mt)
    assert t0/ratio**2<=t1<=t0*ratio**2;checks+=1
out={'exact_networks_checked':checks,'passed':True,'bound':'tau0/R^2 <= tau <= R^2*tau0 when invariant masses and conductances are within [1/R,1] of reference; source mass is recomputed, not fixed'}
Path(__file__).with_name('energy_envelope_audit_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
