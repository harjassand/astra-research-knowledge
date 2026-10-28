"""Exact scalar/finite-cap checks. No source or Bernoulli sampling, no RNG."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

tau=F(1,80);p0=F(1,40)
parameters=[];branch_checks=0;low=0;high=0
for gamma,eps,M in product([F(1),F(1,2),F(1,8),F(1,64)],[F(1),F(1,4),F(1,64),F(1,1024)],[1,2,7,31]):
 e=eps/(8*M);alpha=gamma/2;a=tau*(gamma+e)/64
 assert a<=9*tau/512<tau/4
 eps0=4*a;delta=a/256;root_m=delta*delta/8
 assert 0<eps0<=1 and root_m<=F(1,16)
 assert 168*delta+eps0/32==25*a/32<a
 assert 1/(gamma+e)**2<=1/(4*gamma*e)==2*M/(gamma*eps)
 assert F(2)>=F(9,8)  # stated holdout cap exceeds Hoeffding requirement
 # Coherent learner's two root-risk contributions and optimization debit.
 m_bound=alpha*e/512+alpha*e/512
 assert m_bound==alpha*e/256
 assert 128*m_bound/alpha+4*(alpha*e/8)/alpha==e
 debit=2*M*e+eps/4+2*(eps/64+eps/64)+eps/4
 assert debit==13*eps/16<=eps
 risks=[F(0),tau/4,tau/2,tau-2*a,tau,tau+2*a,F(1,4),F(3,4),1-a]
 for ell,u,v in product(risks,[F(0),F(1,2),F(1)],[F(-1),F(0),F(1)]):
  p=ell+u*a;phat=p+v*a
  if not (0<=ell<=p<=1 and 0<=phat<=F(3,2)):continue
  assert p<=ell+a and abs(phat-p)<=a
  branch_checks+=1
  if phat<=tau:
   low+=1;assert p<=tau+a<p0
  else:
   high+=1;assert ell>tau-2*a>=tau/2
   assert p-ell<=a<=gamma*ell/32+e/64<=alpha*ell+e
 parameters.append({'gamma':str(gamma),'epsilon':str(eps),'M':M,'pilot_a':str(a),'good_event_pilot_excess':'25*a/32 < a','complete_additive_debit':str(debit)})

power_checks=0;mixture_checks=0
for M in [1,2,3,7,16]:
 for a in [F(j,8) for j in range(9)]:
  for f in [a*F(j,8) for j in range(9)]:
   assert a**M-f**M<=M*a**(M-1)*(a-f)
   assert M*a**(M-1)*(1-a)<=1-a**M
   power_checks+=1
  for f1,f2,weight,alpha,e in product([0,a/2,a],[0,a/2,a],[F(1,4),F(1,2),F(3,4)],[F(1,4),F(1,2)],[F(1,128),F(1,16)]):
   mean=weight*f1+(1-weight)*f2
   if a-mean<=alpha*(1-a)+e:
    true_delta=2*(1-weight*f1**M-(1-weight)*f2**M)
    assert true_delta<=(1+alpha)*2*(1-a**M)+2*M*e
    mixture_checks+=1

coding=[]
for Q,eps in product([3,30,3000,3*10**12],[F(1),F(1,64),F(1,1024)]):
 delta_ref=eps/4;L=0
 while F(Q,5*4**(2**L))>delta_ref:L+=1
 pL=F(1,10*4**(2**L))
 assert 2*Q*pL<=delta_ref
 if L:assert F(Q,5*4**(2**(L-1)))>delta_ref
 recurrent=p0
 for _ in range(L):recurrent=10*recurrent**2
 assert recurrent==pL
 coding.append({'Q':Q,'epsilon':str(eps),'L':L,'carrier_calls':Q*5**L,'exact_complete_transfer_bound':str(2*Q*pL)})

result={'status':'PASS','source_calls':0,'Bernoulli_samples':0,'RNG_draws':0,'kind':'Exact branch/comparator/code-count arithmetic on prescribed values; not simulated source qualification.','parameter_cases':len(parameters),'branch_checks':branch_checks,'LOW_checks':low,'HIGH_checks':high,'power_inequality_checks':power_checks,'shared_history_mixture_checks':mixture_checks,'code_cap_cases':coding,'parameter_summaries':parameters,'retained_warnings':{'shared_history_not_tensor_average':{'source':'Identity source; one shared random decoder is I or Z with equal probabilities.','M':2,'E_f_power_M':'1/2','power_of_E_f':'1/4','true_complete_error':'1','wrong_tensor_average_error':'3/2'},'no_postselection_of_bad_mass':{'bad_probability':'1/1000','accept_rule':'accept exactly the bad histories','conditional_bad_probability':'1','conclusion':'A global bad-mass budget cannot be reused after acceptance normalization.'}}}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print('PASS:',len(parameters),'parameter cases;',branch_checks,'branch checks;',mixture_checks,'shared-history mixtures;',len(coding),'code caps; zero sampling.')
