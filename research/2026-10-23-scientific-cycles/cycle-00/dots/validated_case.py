"""Mandatory acceptance boundary for future use of the historical shooting solver.
Stored bad roots are diagnostic evidence and cannot pass this wrapper.
"""
import argparse,json
from pathlib import Path

def require_valid(r):
 if 'profile' not in r:raise ValueError('no solved trajectory')
 if abs(r['cold_inlet_residual_K'])>=1e-3:raise ValueError('cold inlet boundary failed')
 if abs(r['heat_balance_residual_J_kg'])>=1e-6*r['gross_J_kg']:raise ValueError('energy balance failed')
 if r['mass_drift']>=1e-8 or r['min_Y']<=-1e-10:raise ValueError('mass or positivity failed')
 return r

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--test-stored',action='store_true');ap.add_argument('--Tq',type=float,default=2100);ap.add_argument('--length',type=float,default=.02);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 if a.test_stored:
  src=Path(__file__).resolve().parent/'results/counterflow.json';rows=json.loads(src.read_text())['rows'];out=[]
  for r in rows:
   try:require_valid(r);ok=True;reason='passed'
   except ValueError as e:ok=False;reason=str(e)
   out.append({'Tq_K':r['Tq_K'],'length_m':r['length_m'],'accepted':ok,'reason':reason})
  assert sum(x['accepted'] for x in out)==4
  a.output.write_text(json.dumps({'scope':'read-only stored trajectory gate; no solver run','cases':out},indent=2)+'\n')
 else:
  from counterflow import run
  r=require_valid(run(Tq=a.Tq,L=a.length));r['acceptance']='EXCHANGER_ONLY_NOT_COMPLETE_PROCESS';a.output.write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
