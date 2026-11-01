"""80-digit independent mpmath signed-instrument and echo re-evaluation.
Numerical cross-check only; rational enclosure validity is audited analytically.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import mpmath as mp
mp.mp.dps=80
root=Path(__file__).resolve().parent
m=mp.mpf;j=mp.j

def frac(s):
 f=F(s);return m(f.numerator)/f.denominator

def check_interval(x,interval,name):
 lo,hi=map(frac,interval)
 assert lo<=x<=hi,(name,mp.nstr(x,60),mp.nstr(lo,60),mp.nstr(hi,60))
 return {'name':name,'value':mp.nstr(x,70),'interval_width':mp.nstr(hi-lo,8)}

rows=json.loads((root/'receiver_certificates.json').read_text())['rows'];out=[]
for row in rows:
 l=frac(row['parameters']['loss']);eta=m(99)/100;dt=m(1)/4;e=m(1)/1000
 # rho vector = [rho00,rho10,rho01,rho11]. Lowering recycles 11 into00.
 A=mp.matrix([[0,-j,j,0],[-j,-l/2,0,j],[j,0,-l/2,-j],[0,j,-j,-l]])
 J=mp.zeros(4);J[0,3]=l
 active=A-(1-eta)*J;blind=A-J;capture=eta*J
 M=mp.zeros(8)
 for i in range(4):
  for k in range(4):M[i,k]=active[i,k];M[4+i,4+k]=blind[i,k];M[4+i,k]=capture[i,k]
 E=mp.expm(M*dt);maps=[E[:4,:4],E[4:,:4]];branches=[mp.matrix([1,0,0,0])]
 for _ in range(4):branches=[U*v for v in branches for U in maps]
 noisy_score=sum(abs((1-e)*v[0]-e*v[3])+abs((1-e)*v[3]-e*v[0]) for v in branches)
 blind_score=(1-2*e)*sum(v[0]+v[3] for v in branches)
 phot_score=sum(abs(v[0]-v[3]) for v in branches);phot_blind=sum(v[0]-v[3] for v in branches)
 for name,score,interval in [('noisy_opt',noisy_score,row['bayes_risk_interval']),('noisy_blind',blind_score,row['blind_risk_interval']),('photon_opt',phot_score,row['photon_only_receiver']['bayes_risk_interval']),('photon_blind',phot_blind,row['photon_only_receiver']['blind_risk_interval'])]:
  assert abs(mp.im(score))<m('1e-75');out.append(check_interval((1-mp.re(score))/2,interval,str(l)+'_'+name))
 for b,key in [(1,'no_record_comparator'),(4,'three_pulse_echo_comparator')]:
  v=mp.matrix([1,0])
  for k in range(b):
   c=(-1)**k;Q=mp.matrix([[0,-2*j*c],[-2*j*c,-l/2]])
   v=mp.expm(Q/b)*v
  out.append(check_interval((1-mp.re(v[0]))/2,row[key]['raw_dephasing_interval'],str(l)+'_'+key))
(root/'high_precision_results.json').write_text(json.dumps({'scope':'Independent 80-digit numerical diagnostic, not an interval proof','checks':len(out),'results':out},indent=2)+'\n')
print('All',len(out),'independent high-precision values lie in claimed rational intervals.')
