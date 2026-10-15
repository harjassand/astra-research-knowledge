"""Local mathematical checks, not external validation or a formal proof."""
import csv,json,sys
from fractions import Fraction as Q
import numpy as np
from mpmath import mp,iv
from compact_model import BASE,features,target,make_problem
from continuum_certificate import J,erel,I,weights_exact
mp.dps=70; iv.dps=35
# Exact minimum error forced by the high-frequency real-part monotonicity violation.
rows=list(csv.DictReader(open(BASE/'data/cell_001_eis.csv')))
assert len(rows)==70
r={Q(z['frequency_hz']):Q(z['Z_real_ohm']) for z in rows}
assert 1000*(r[Q(10000)]-r[Q(5484)])/2==Q(103,200)
# Gauge identity, endpoint values, and positivity on a wide deterministic mesh.
s=np.r_[0,np.geomspace(1e-12,1e12,20000)/(1+np.geomspace(1e-12,1e12,20000)),1.]
f=np.array([.01,1.,904.7]); F=features(s,f)
g=F[0].real-F[0].imag+.01*F[1].imag
assert np.max(abs(g-1))<1e-12
assert np.all(target(s,10)>0)
assert abs(target(np.array([0.]),10)[0]-1)<1e-15
assert abs(target(np.array([1.]),10)[0]-2*np.pi*.01*10/(1-1e-4))<1e-14
# Check E and its first two derivatives against independent high-precision integration.
for z in ['0','0.0001','0.1','0.7','1.1']:
 jet=J(iv.mpf(z),iv.mpf(1),iv.mpf(0)); e=erel(jet)
 for k,enc in enumerate([e.v,e.d,e.dd]):
  ref=(-1)**k*mp.quad(lambda u:u**k*mp.exp(-mp.mpf(z)*u),[0,1])
  # Compare at high precision using interval endpoint decimal values.
  lo=mp.mpf(enc.a._mpi_[0]); hi=mp.mpf(enc.b._mpi_[1])
  assert lo<=ref<=hi,(z,k,ref,enc)
# Exact inductance cancellation in every verified full-spectrum dual.
for rec in json.loads((BASE/'results/compact_lp.json').read_text()):
 for side in ['lower','upper']:
  f,v=weights_exact(rec,side); n=len(f)
  assert sum((v[n+j]*f[j] for j in range(n)),Q(0))==0
# Demonstrated ambiguity is genuine: two passive feasible models have distinct outcomes.
w=json.loads((BASE/'results/feasible_witnesses.json').read_text())
a,b=[x for x in w if x['time_s']==1000.]
assert a['max_component_error_mohm']<.1 and b['max_component_error_mohm']<.1
assert a['response_interval_mohm'][1]<101 and b['response_interval_mohm'][0]>528
assert all(x['inductance_H_approx']>0 for x in w)
print('UNIT_CHECKS_PASS')
