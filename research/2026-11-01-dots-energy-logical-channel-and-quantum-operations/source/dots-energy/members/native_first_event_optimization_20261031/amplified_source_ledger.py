#!/usr/bin/env python3
"""Constant-degree conditional-source preparation ledger, not gates."""
import json,sys
sys.path.insert(0,'native_resource_audit_20261031')
import resource_ledger as core
mp,I=core.mp,core.I
lo,hi,ceil_up,minlo,bits,fmt=core.lo,core.hi,core.ceil_up,core.minlo,core.bits,core.fmt
rows=[]
for old in json.load(open('native_first_event_optimization_20261031/sharp_ledger.json'))['rows']:
 n=old['n'];eps=I(1)/int(old['epsilon'].split('/')[1]);lam=int(old['lambda_value'])
 mu=I(19)*lam/20;B=I(20)/19;c=mp.iv.sqrt(mu*B);delta=mu/2-2*c;nu=mp.iv.sqrt(delta**2+8*c*c)
 aH=I(20*n)/19;A=old['Aamp'];K=old['virtual_cap'];S=old['call_cap'];dA=old['OAA_degree']
 e=eps/(1000*S);beta=e/(128*A);eta=beta/10000
 ds=eta/(10**6*(K+1)**2)
 ht=minlo(I(1),eta/(10**6*(1+64*nu+2*c)*(K+1)**2),beta/(10**6*(1+1+mu*(aH+1))*(K+1)**2))
 hp=minlo(ht/100,ds/(100*(1+nu)))
 sigma=ds/100;ustep=sigma*hp/100
 row={k:old[k] for k in ['n','epsilon','lambda_value','call_cap','Aamp','OAA_degree','virtual_cap','padded_source_kernel_slot_proxy','outer_uniform_bits','bits_outer_time']}
 row.update(inner_time_bits=bits(ht),proposal_time_bits=bits(hp),inner_uniform_bits=bits(ustep),
  acceptance_error_bits=bits(ds),component_probability_error_bits_lower_bound=bits((ds/100)**2),
  previous_inner_uniform_bits=old['inner_uniform_bits'],
  conditional_proposal_unitary_calls_per_path_PREP=3*K,
  conditional_proposal_unitary_calls_including_path_unprepare=6*K,
  whole_conditional_proposal_unitary_call_proxy=str(6*S*dA*K),
  scope='NOT gates. Each proposal unitary contains exp/log/sqrt, scalar P arithmetic, rotations and fresh uniforms. Source scalar arithmetic, kernel gates, Poisson scans and controls remain paid separately; no rejection expectation used.')
 rows.append(row)
json.dump({'status':'UNREVIEWED constant-amplification source candidate; unchanged exact physical fixtures/count/window/word caps.', 'rows':rows},open('native_first_event_optimization_20261031/amplified_source_ledger.json','w'),indent=2)
for r in rows:
 if r['lambda_value']=='1000000000000000000000000' or r==next(x for x in rows if x['n']==r['n'] and x['epsilon']==r['epsilon']):
  print(*(r[k] for k in ['n','epsilon','lambda_value','inner_uniform_bits','acceptance_error_bits','whole_conditional_proposal_unitary_call_proxy']))
