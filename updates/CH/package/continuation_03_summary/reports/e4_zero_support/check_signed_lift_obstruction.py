"""Finite-energy, bounded-score SLD obstruction diagnostics, not the proof."""
import math,json
out=[]
for eta in [.75,.75000001,.7501,.751,.76,.7606,.761,.7841,.8]:
 a=v=1.5;b=eta*a+(1-eta)*v
 fe=(1-eta)/((1-eta)*a+eta/(4*v))
 gap=eta/fe-b
 row={'eta':eta,'input_N':1,'output_q_variance':b,'environment_SLD_FI':fe,
      'receiver_SLD_FI':eta/b,'unbiased_environment_variance_lower_bound':eta/fe,
      'unclipped_variance_gap':gap}
 if eta>.75:
  r=b*fe/eta
  L=math.sqrt(2*b*math.log(4/(1-r)))
  p=math.erf(L/math.sqrt(2*b))
  low=eta*p*p/fe
  assert low>b
  row.update({'bounded_clip_L':L,'bounded_score_CR_lower_bound':low,'bounded_score_receiver_variance_upper_bound':b})
 out.append(row)
with open('work/continuation_03/reports/e4_zero_support/signed_lift_obstruction_checks.json','w') as f:json.dump({'status':'diagnostics only; exact proof in e4_zero_capacity_gate.txt','rows':out},f,indent=2)
print(json.dumps(out,indent=2))
