from fractions import Fraction as F
import projective_mass as p
import json

sp,raw=p.demo_network();base=p.recognize(sp,raw)
summary=[]
def check(label,rec,t=F(2),max_expanded_bits=100000):
    c=p.construct(rec,t=t,max_expanded_bits=max_expanded_bits);assert c['accepted'];n=len(sp);count=0
    for N in range(21):
      for x in p.comps(N,n):
        q=p.quotient(rec,c,x);assert q<=c['C0']-c['kappa']*N;count+=1
    huge=[]
    for N in [c['R']-1,c['R'],c['R']+1,10**6,10**50]:
      for x in [(0,N,0),(0,0,N),(1,N-1,0),(1,0,N-1),(4*(N//10),3*(N//10),N-7*(N//10))]:
        q=p.quotient(rec,c,x);bound=c['C0']-c['kappa']*N;assert q<=bound
        huge.append({'state':x,'quotient':q,'bound':bound})
    summary.append({'label':label,'certificate':c,'raw_recognition':rec,'ordinary_exact_checks':count,'targeted_checks':huge})
    return c

# Catalyzing each binary channel by each coordinate multiplies its count rate by N-2.
lift=raw[:2]
for u,v,k in raw[2:]:
 for j in range(3):
    lift.append((tuple(x+int(i==j) for i,x in enumerate(u)),tuple(x+int(i==j) for i,x in enumerate(v)),k))
cubic=p.recognize(sp,lift);c=check('cubic_lift_with_essential_radial_attenuation',cubic)
assert c['leading_order']==3 and c['denominator_degree']==c['degree']+1
for N in range(2,10):
 for x in p.comps(N,3):
    L2=sum(k*p.ff(x,u)*(p.evaluate(c['acquisition']['H'],tuple(z-a+b for z,a,b in zip(x,u,v)))-p.evaluate(c['acquisition']['H'],x)) for u,v,k in base['internal'] if p.ff(x,u))
    L3=sum(k*p.ff(x,u)*(p.evaluate(c['acquisition']['H'],tuple(z-a+b for z,a,b in zip(x,u,v)))-p.evaluate(c['acquisition']['H'],x)) for u,v,k in cubic['internal'] if p.ff(x,u))
    assert L3==(N-2)*L2
bad=dict(c);bad['denominator_degree']=bad['degree'];negative=[]
for q in [10**6,10**50]:
 x=(q,0,q);wrong=p.quotient(cubic,bad,x);correct=p.quotient(cubic,c,x)
 assert wrong>0 and correct<0
 negative.append({'state':x,'unattenuated_quotient':wrong,'corrected_quotient':correct})
check('base_near_one',base,F(65,64))
check('large_base_compact_constant',base,F(100),max_expanded_bits=0)
# A real top-order obstruction with a stronger ordinary lower-order comparator.
z=(0,0,0);A=(1,0,0);B=(0,1,0);C=(0,0,1);BB=(0,2,0);CC=(0,0,2)
stable_raw=[(z,A,1),(A,z,1),(A,B,1),(B,A,1),(A,C,1),(C,A,1),(BB,CC,1),(CC,BB,1)]
r=p.recognize(sp,stable_raw);decline=p.construct(r,max_degree=None,max_bases=None)
assert not decline['accepted'] and decline['support_certificate']['all_degree_strict_cone_impossible'] and decline['network_stability']=='UNKNOWN'
comparator_checks=0
for a in range(8):
 for b in range(8):
  for c0 in range(8):
   x=(a,b,c0);q=sum(k*p.ff(x,u)*(F(4)**(v[0]-u[0])*F(5)**(sum(v[1:])-sum(u[1:]))-1) for u,v,k in stable_raw)
   assert q==3-F(a,4)-F(b+c0,5);comparator_checks+=1
# The graph theorem applies here, but acquisition can still hit a finite work cap.
budget=p.construct(base,max_bases=330);assert not budget['accepted'] and budget['explicit_certificate_status']=='UNKNOWN'
degree=p.construct(base,max_degree=1);assert not degree['accepted'] and degree['explicit_certificate_status']=='UNKNOWN'
print(json.dumps(p.clean({'cases':summary,'essential_attenuation_negative_control':negative,
 'stable_quadratic_obstruction':decline,'ordinary_stability_comparator_checks':comparator_checks,
 'basis_budget_receipt':budget,'degree_budget_receipt':degree,'tests_supplement_the_proof':True}),indent=2,sort_keys=True))
