#!/usr/bin/env python3
"""Separate stable-source precision/proposal proxy; not gates or a source backend."""
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
 R=ceil_up(mp.iv.log(100*(K+1)/eta)/mp.iv.log(I(5)/4))+1
 ht=minlo(I(1),eta/(10**5*(1+(R+1)*nu+2*c)*(K+1)**2),beta/(10**5*(1+1+mu*(aH+1))*(K+1)**2))
 hp=minlo(ht/100,eta/(10**5*(1+nu)*(K+1)*(R+1)))
 ustep=eta*hp/(10**6*(K+1)*(R+1))
 J_old=old['bits_inner_time']-6 # exact since tau=2^-8 and J=ceil(log2(tau/ht))+2
 row={k:old[k] for k in ['n','epsilon','lambda_value','call_cap','Aamp','OAA_degree','virtual_cap','padded_source_kernel_slot_proxy','outer_uniform_bits','bits_outer_time']}
 row.update(rejection_cap=R,inner_time_bits=bits(ht),proposal_time_bits=bits(hp),inner_uniform_bits=bits(ustep),
  previous_inner_uniform_bits=old['inner_uniform_bits'],previous_inner_bisection_depth=J_old,
  capped_conditional_proposals_per_word=K*R,previous_capped_bisection_iterations_per_word=K*J_old,
  whole_capped_conditional_proposal_proxy=str(S*dA*K*R),
  whole_previous_bisection_iteration_proxy=str(S*dA*K*J_old),
  scope='Different elementary operations, NOT gates. New cap includes ALL coherent rejection attempts, not expectation. Poisson scans/sorts, LCHS and encoding gates remain separately paid.')
 rows.append(row)
json.dump({'status':'UNREVIEWED stable hierarchical source candidate; sharp stage count and all physical/count/window fixtures unchanged.', 'rows':rows},open('native_first_event_optimization_20261031/stable_source_ledger.json','w'),indent=2)
for r in rows:
 if r['lambda_value']=='1000000000000000000000000' or r==next(x for x in rows if x['n']==r['n'] and x['epsilon']==r['epsilon']):
  print(*(r[k] for k in ['n','epsilon','lambda_value','rejection_cap','inner_uniform_bits','previous_inner_uniform_bits','capped_conditional_proposals_per_word','previous_capped_bisection_iterations_per_word']))
