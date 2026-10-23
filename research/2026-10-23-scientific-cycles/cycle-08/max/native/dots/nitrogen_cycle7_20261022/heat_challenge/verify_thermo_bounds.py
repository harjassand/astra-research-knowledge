"""Exact rational interval proof and antiderivatives, not grid sampling."""
import csv, hashlib, json
from fractions import Fraction as R
from pathlib import Path
p=Path(__file__).parent
manifest=json.loads((p/'INPUT_MANIFEST.json').read_text())
for name,item in manifest['files'].items():
    assert hashlib.sha256((p/'inputs'/name).read_bytes()).hexdigest()==item['sha256']
lo,mid,hi=R('0.29815'),R('0.4'),R('0.5')
# On positive t, t^k is monotonic for k=1,2,3 and reciprocal t^-2.
# Upper sum of independently bounded terms is rigorous even if extrema
# of separate terms do not coincide. Two covering intervals suffice.
def cp_upper(c,a,b):
    return c[0]+sum(max(v*a**k,v*b**k) for v,k in zip(c[1:],[1,2,3,-2]))
def primitive(c,t):
    A,B,C,D,E=c
    return A*t+B*t*t/2+C*t**3/3+D*t**4/4-E/t
results=[]
for row in csv.DictReader((p/'inputs/nist_shomate.csv').open()):
    c=[R(row[k]) for k in 'ABCDE']
    bounds=[cp_upper(c,a,b) for a,b in [(lo,mid),(mid,hi)]]
    assert max(bounds)<50
    # Integral cp(T)dT =1000*(primitive(t2)-primitive(t1)) J/mol.
    sensible=1000*(primitive(c,hi)-primitive(c,lo))
    assert 0<sensible<50*(R(500)-R('298.15'))
    results.append({'species':row['species'],'interval_cp_upper_J_molK':[float(v) for v in bounds],
      'exact_interval_cp_upper_rationals':[str(v) for v in bounds],
      'integrated_h_298p15_to_500_J_mol':float(sensible)})
F=R(20)/(60*R('22.414')); A=R(90290); B=R(33100)
# H(z)=F*(A*x+(B-A)*z)/(1+z/2).
# H'(z)=F*((B-A)-A*x/2)/(1+z/2)^2.
# Since B<A and x>=0, derivative is negative throughout 0<=z<=x.
for row in csv.DictReader((p/'inputs/digitized_experiments.csv').open()):
    x=R(row['NOx_pct'])/100
    assert 0<x<1 and (B-A)-A*x/2<0
    h=lambda z:F*(A*x+(B-A)*R(z))/(1+R(z)/2)
    assert h(0)==F*A*x
    assert h(x)==F*B*x/(1+x/2)
    assert h(x)<h(x/2)<h(0)
print(json.dumps({'analytic_cp_certificates':results,'chemical_enthalpy_monotonicity':'strictly decreasing in z at fixed x; exact derivative sign and endpoint identities checked on all eight inputs','input_hashes':'verified'},indent=2))
