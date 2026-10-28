"""Rational universal noise compiler plus an actual48-state mixed receiver.

This compiler reuses its owned exact field arithmetic/design constructor;
it is not described as an independent producer review.
"""
from fractions import Fraction as Q
from pathlib import Path
from time import perf_counter
import json,sys
import exact_entropy as e
import certify_design_obstruction as field
sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent
def admission(d,t):
 assert d>=2 and 0<=t<=1
 slack=1-Q(1,d*d)-t*t;assert slack>=0
 aa=Q(d-2,2*d);var=Q(d-1,d*d*(d+1))
 upper=e.sub(e.sqrtq(aa*aa+t*t*var),e.iv(aa))
 # The exact squared test proves the cap even when a fixed-bit square
 # root interval is too coarse to resolve its tiny slack in large d.
 upper=upper[0],min(upper[1],Q(1,d*d))
 assert upper[1]<=Q(1,d*d)
 return{'d':d,'retained_fraction':e.serial(t),'white_fraction':e.serial(1-t),
 'threshold_squared_slack':e.serial(slack),'uniform_hemisphere_upper':e.record(upper),
 'all_weights_entropy_coefficient':'1/2','generic_best_depolarizing_factor_is_at_least':e.serial(t*t)}
def main():
 start=perf_counter();dimension_controls=[]
 for d in[2,3,4,8,64,1000000]:
  t=Q(2*(d*d-1),2*d*d-1)
  assert 1-Q(1,d*d)-t*t==Q(d*d-1,d*d*(2*d*d-1)**2)
  dimension_controls.append(admission(d,t))
 t=Q(16,17);d=3;pure,weights,radii=field.build_design()
 mixed=[[[field.add(field.scale(s[i][j],t),field.f((1-t)/d if i==j else 0))for j in range(d)]for i in range(d)]for s in pure]
 assert field.weighted(weights,mixed)==[[field.f(Q(1,3)if i==j else 0)for j in range(d)]for i in range(d)]
 checks=0
 for i in range(d):
  for j in range(d):
   for k in range(d):
    for l in range(d):
     delta=int(i==j and k==l);swap=int(i==l and k==j)
     p=field.total(field.scale(field.mul(s[i][j],s[k][l]),w)for w,s in zip(weights,pure))
     assert p==field.f(Q(delta+swap,12))
     actual=field.total(field.scale(field.mul(s[i][j],s[k][l]),w)for w,s in zip(weights,mixed))
     expected=t*t*Q(delta+swap,12)+(1-t*t)*Q(delta,9)
     assert actual==field.f(expected);checks+=1
 # Actual source p uniform on the high-radius24 labels.
 yy=t*Q(5,6)+(1-t)/d;small=(1-yy)/2
 source=field.weighted([Q(1,24)if y==Q(5,6)else Q(0)for y in radii],mixed)
 assert source==[[field.f(yy if i==0 else small)if i==j else field.f()for j in range(d)]for i in range(d)]
 gap=e.add(e.sub(e.logq(Q(11,2)),e.scale(e.logq(3),2)),e.scale(e.entropy([e.iv(yy),e.iv(small),e.iv(small)]),2))
 assert gap[0]>0
 too_high=Q(19,20)
 hinge=sum(w*max(2*(too_high*y+(1-too_high)/d)-1,0)for w,y in zip(weights,radii))
 assert hinge==Q(37,330)and hinge-Q(1,9)==Q(1,990)
 out={'status':'PASS','universal_rational_controls':dimension_controls,
 'actual_mixed_receiver':{'d':3,'design_atoms':48,'t':'16/17','pure_and_mixed_second_moment_components':checks,
 'all_preparation_weights_admitted':True,'one_source_output_spectrum':list(map(e.serial,[yy,small,small])),
 'one_source_Din_minus_2Dout':e.record(gap)},
 'above_gate_control':{'t':'19/20','hemisphere_value':'37/330','strict_convex_order_violation':'1/990','entropy_failure_claim':False},
 'source_qualification_paid_here':True,'seconds':perf_counter()-start,
 'general_scope':'UNIVERSAL_NOISE.md analytic proof; finite dimension controls illustrate the rational compiler, not the all-d proof.',
 'historical_priority':'UNKNOWN','quantum_memory_claim':False}
 (HERE/'NOISE_RECEIVER.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':'PASS','seconds':out['seconds'],'actual_mixed_gap':gap and list(map(float,gap)),
 'above_gate_mechanism_failure':'1/990','all_weights_on_actual_design':True},indent=2))
if __name__=='__main__':main()
