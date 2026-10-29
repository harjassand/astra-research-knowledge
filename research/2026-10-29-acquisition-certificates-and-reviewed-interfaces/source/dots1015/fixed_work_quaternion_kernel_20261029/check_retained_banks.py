import sys,json,time
from pathlib import Path
from fractions import Fraction as F
from fixed_work_oracle import solve,verify
sys.path.insert(0,'producer-workspace/quaternion_oracle_controller_20261029');from quartic_sos_oracle import bank_polynomial
r=Path(__file__).parent;src=Path('producer-workspace/quaternion_oracle_controller_20261029');rows=[]
for bankname in ['one_axis','drift']:
 bank=json.load(open(src/f'bank_{bankname}.json'))
 for edge in range(3):
  raw=bank_polynomial(bank,edge);st=time.time();c=solve(raw);assert verify(raw,c);elapsed=time.time()-st;reference=json.load(open(src/f'oracle_{bankname}_edge{edge}.json'));scale=F(reference['scale']);optlo=F(reference['rational_lower'])*scale;optup=F(reference['rational_upper'])*scale
  row=dict(bank=bankname,edge=edge,seconds=elapsed,certificate=c,mean_probe_gap=float(F(c['gap'])/(4*bank['probe_calls'])),candidate_excess_vs_old_upper=float((F(c['upper'])-optup)/(4*bank['probe_calls'])),lower_shortfall_vs_old_lower=float((optlo-F(c['lower']))/(4*bank['probe_calls'])));rows.append(row);print({k:v for k,v in row.items() if k!='certificate'},flush=True)
zero=solve({});assert verify({},zero) and F(zero['gap'])==0
cholam={(2,2,0,0):1,(0,2,2,0):1,(2,0,2,0):1,(0,0,0,4):1,(1,1,1,1):-4};c=solve(cholam);assert verify(cholam,c);rows.append(dict(bank='Choi-Lam',certificate=c,known_exact_minimum=0))
(r/'retained_bank_results.json').write_text(json.dumps(dict(rows=rows,zero_polynomial_certificate=zero,scope='Executedfixedwork rational arithmetic/certificates. No adaptive quantum or physical-clock experiment, no optimization-quality promise.'),indent=2)+'\n')
