"""Qualify all-deadline law with unknown true stationary target mass."""
from fractions import Fraction as F
from pathlib import Path
import json
from run_gibbs import exp_bounds,out,ser

P=Path(__file__).resolve().parent
def frac(v):return F(int(v['numerator']),int(v['denominator']))
def main():
 data=json.loads((P/'gibbs_results.json').read_text())
 g=F(1,2);deadline=F(10**17);du=F(1,10**16);err=F(1,10**13)
 assert exp_bounds(F(80),200)[0]>1+1/(4*du*du)
 rows=[]
 for row in data['targets']:
  # Reuse directed outward decimal bounds to keep intermediate bit lengths
  # modest. This widens the certificate; it does not round toward its center.
  plo,phi=map(F,row['true_target_mass_interval'])
  lo=F(row['mean_lower_outward']);hi=F(row['mean_upper_outward'])
  mulo=(1-phi)*lo;muhi=(1-plo)*hi
  assert 1/(g*mulo)<du<F(1,4)
  assert (F(368,3)*du+phi)/(1-phi)<err
  elo,ehi=exp_bounds(deadline/muhi,60)
  low=max(F(0),1-1/elo-err)
  elo,ehi=exp_bounds(deadline/mulo,60)
  high=min(F(1),1-1/ehi+err)
  rows.append(dict(name=row['name'],probability_lower_outward=out(low),
   probability_upper_outward=out(high,True),exact_lower=ser(low),exact_upper=ser(high)))
 result=dict(deadline=int(deadline),uniform_law_error=ser(err),confidence_lower=data['confidence_lower'],
  qualification='True target mass varies within acquired interval; true initial law conditioned outside its target',targets=rows)
 (P/'gibbs_deadline_results.json').write_text(json.dumps(result,indent=2))
 print(json.dumps({k:v for k,v in result.items() if k!='targets'},indent=2))
 for row in rows:print(json.dumps({k:v for k,v in row.items() if not k.startswith('exact_')}))
if __name__=='__main__':main()
