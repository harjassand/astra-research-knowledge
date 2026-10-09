"""Exact fixed-lag negative Farkas functional via an exponential remainder bound."""
from fractions import Fraction as F
from pathlib import Path
import json
d=json.loads((Path(__file__).parent/'exact_certificate_v1.json').read_text())
Q=[[F(a) for a in row] for row in d['Q']]
v=[[F(a) for a in row] for row in d['points']]
z=[[F(a) for a in row] for row in d['farkas_z']]
Z=[[F(0),*z[i],*[sum(z[i][k]*v[i][k] for k in range(2))]*5] for i in range(5)]
def require(test,label):
    if not test:raise RuntimeError(label)
q_norm=max(sum(abs(a) for a in row) for row in Q)
field_norm=sum(sum(abs(a) for a in row) for row in Z)/10
require(q_norm<=2,'generator infinity norm bound')
require(field_norm<=2,'averaged field one norm bound')
require(all(abs(a)<=1 for row in d['H'] for a in map(F,row)),'observable feature infinity norm bound')
delta=-F(d['farkas_drift_pairing'])/2
t=F(1,1000)
error=4*t*t/(1-2*t)
margin=delta*t-error
require(margin>F(1968761,10**12),'fixed lag strict negative margin')
print(json.dumps(dict(status='PASS',lag=str(t),generator_norm_bound='2',field_norm_bound='2',taylor_error_bound=str(error),F_upper_bound=str(-margin),negative_margin_decimal=float(margin)),indent=2))
