"""Near-saturation and exact forced-inverse response in sector source class.
All finite witness checks use rational arithmetic; existence of full maps
follows from a separately proved Lipschitz extension theorem.
"""
from fractions import Fraction as Q
from math import isqrt
import json
from pathlib import Path
from astra_pro3_sector_joint import vec,add,sub,mul,sq,B,C,M,A,rend,sqrt_upper
ROOT=Path(__file__).resolve().parent

def sqrt_lower(v, scale=1<<48):
 assert v>=0
 scaled=v*scale*scale
 floor=scaled.numerator//scaled.denominator
 return Q(isqrt(floor),scale)

def consistent_native(points):
 for i in range(len(points)):
  for j in range(i):
   xi,pi=points[i];xj,pj=points[j]
   if sq(sub(sub(pi,pj),mul(M,sub(xi,xj))))>A*A*sq(sub(xi,xj)):
    return False
 return True

def instance(eps):
 s=Q(2)+eps
 old=[(vec(-1,0),vec(-s,0)),(vec(1,0),vec(s,0))]
 assert consistent_native(old)
 p=vec(0,0)
 c1=add(old[0][0],mul(C,sub(p,old[0][1])))
 c2=add(old[1][0],mul(C,sub(p,old[1][1])))
 r2=B*B*sq(sub(p,old[0][1])); assert r2==B*B*sq(sub(p,old[1][1]))
 avg=mul(Q(1,2),add(c1,c2)); assert avg==vec(0,0)
 # Equal-weighted sum of two ball constraints proves ||x*||² <= t².
 t2=r2-sq(mul(Q(1,2),sub(c1,c2)))
 expected=eps*(Q(2)-eps)/8
 assert t2==expected and t2>=0
 tlo=sqrt_lower(t2);thi=sqrt_upper(t2)
 # Reconstruct two mutually incompatible global sources via finite inverse
 # point constraints. Kirszbraun extension supplies real global sources.
 xplus=vec(0,tlo);xminus=vec(0,-tlo)
 assert consistent_native(old+[(xplus,p)]) and consistent_native(old+[(xminus,p)])
 if eps==0:assert tlo==thi==0
 return dict(epsilon=eps,retained_first_responses=old,force_request=p,
   disk_centers=(c1,c2),single_disk_radius_squared=r2,
   joint_equilibrium_squared_radius=t2,
   joint_y_radius_lower=tlo,joint_y_radius_upper=thi,
   separation_between_compatible_inverse_y_values=2*tlo,
   independent_y_interval_width_at_least=2*sqrt_lower(r2),
   independent_to_joint_ratio_lower=(sqrt_lower(r2)/thi if thi>0 else 'infinite'),
   rational_feasible_ambiguous_inverse_positions=(xplus,xminus),
   exact_joint_formula='x_y in [-sqrt(eps*(2-eps)/8), +sqrt(eps*(2-eps)/8)]',
   proof='Intersect two endpoint-residual disks; average squared inequalities; prove attainability by one-point Euclidean Lipschitz extension.')

def contract_cannot_be_learned_from_finite_readings():
    # A compactly supported perturbation matches the sector law at every old
    # input in [-1,1] but breaks even monotonicity elsewhere.
    def bump(x):return max(Q(0),Q(1,4)-(x-10)**2)**4
    def alternative(x):return 3*x-1000*bump(x)
    old=[Q(-1),Q(0),Q(1)]
    assert all(alternative(x)==3*x for x in old)
    bad1=Q(39,4);bad2=bad1+Q(1,100)
    bad_gap=alternative(bad2)-alternative(bad1)
    assert bad_gap<0
    return dict(old_sites=old,old_responses=[3*x for x in old],
       new_falsifying_sites=[bad1,bad2],
       decrease_of_alternative=bad_gap,
       smoothness='Alternative is C^3; hidden compact support is disjoint from observed sites.',
       interpretation='Finite consistency never certifies global Lipschitz/monotonicity. A separate native two-point test would reject this alternative.')

def execute():
 instances=[instance(Q(0))]+[instance(Q(1,10**k)) for k in (2,4,6,8)]
 out=dict(controls=instances,global_contract_indistinguishability=contract_cannot_be_learned_from_finite_readings(),
  near_saturation_scaling='For eps down to zero, exact inverse uncertainty is sqrt(eps*(2-eps)/8), so hidden transverse inverse uncertainty is square-root in the observed saturation defect.',
  threshold='At eps=0 the inverse of zero force is determined exactly by two old forward queries, despite no query at the inverse point.',
  warning='Nearly saturated data do not justify rounding the ambiguity to zero. Smoothness of the recovered Lipschitz map is not claimed.')
 (ROOT/'astra_pro3_sector_saturation_results.json').write_text(json.dumps(rend(out),indent=2)+'\n')
 for r in instances:print('eps',float(r['epsilon']),'joint max y',float(r['joint_y_radius_upper']), 'versus single',float(sqrt_upper(r['single_disk_radius_squared'])))
 return out
if __name__=='__main__':execute()
