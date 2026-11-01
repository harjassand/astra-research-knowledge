from fractions import Fraction as F
from pathlib import Path
import receive_dilation as c
import copy,json,random
n=0;groups={}
def ok(x,g):
 global n
 assert x,g
 n+=1;groups[g]=groups.get(g,0)+1
def no(fn,g):
 try:fn()
 except c.Unknown:ok(True,g);return
 raise AssertionError('accepted '+g)
# Reduced-exponent exact-root enclosures, including negative powers and rational branches.
for d in [2,4]:
 for m in range(1,9):
  ii=c.Integrator(m,F(2,7),d,48,1000,100000)
  for x in [F(1,17),F(1),F(29,3)]:
   for nn in [-m,m]:
    l,u=ii.bounds(x,nn,d);ok(F(l,2**48)**d<=x**nn<=F(u,2**48)**d,'root')
# Independent exact rational reference when m/p is integer: all three Darboux sums.
for m,d in [(1,2),(2,2),(4,4),(8,4)]:
 ii=c.Integrator(m,F(3,5),d,60,10000,100000);s=lambda y:1+F(3,5)*(1-y*y)**2;a=s(F(0))
 for kind,left,right in [('q',F(1,2),F(1)),('r0',F(0),F(1,2)),('rplus',F(0),F(1,2))]:
  if kind=='rplus' and m%d:continue
  fun=(lambda y:s(y)**(-m)) if kind=='q' else ((lambda y:s(y)**m) if kind=='r0' else (lambda y:(a**(2*d)/(2*a**d-s(y)**d))**(m//d)))
  N=13;h=(right-left)/N;ys=[left+h*i for i in range(N+1)];lo=h*sum(min(fun(ys[i]),fun(ys[i+1])) for i in range(N));hi=h*sum(max(fun(ys[i]),fun(ys[i+1])) for i in range(N))
  l,u=ii.integrate(left,right,N,kind);ok(l<=lo<=hi<=u,'exact_sum');ok(lo-l<=(right-left)/2**60 and u-hi<=(right-left)/2**60,'sum_rounding')
# Physical m tail identity, not degree-cap-dependent.
for m in [1,2,7]:
 for T in [F(2),F(8)]:
  x=[]
  for d in [2,4]:
   ii=c.Integrator(m,F(3,5),d,80,1000,100000);tail=ii.tail(T);x.append(tail)
   ok(tail==F(3,5)**(-m)*(1-T**-2)**(-2*m)*T**(1-4*m)/(4*m-1),'tail')
  ok(x[0]==x[1],'tail_degree')
# Radial well raw model: reject both constant-shifted representations.
for R in [F(1),F(4)]:
 records=[]
 for deg,coef in [(2,-2*R**2),(4,F(1))]:
  for j,b in enumerate(c.profile_coefficients(F(1),deg)):
   if b:records.append({'powers':[2*j,deg],'coefficient':str(coef*b)})
 raw={'n':2,'terms':records};no(lambda raw=raw:c.acquire(raw),'well_reject')
 rr=copy.deepcopy(raw);rr['terms'].append({'powers':[0,0],'coefficient':str(R**4)});no(lambda rr=rr:c.acquire(rr),'well_reject')
# Exact constants and energy barrier dichotomy independent of normalizer.
c1=F(8065,4096);c2=F(7121,4096);A=(c1*c1-c2*c2)/(c1*c1+c2*c2);t=2/(c1*c1+c2*c2)
for R in [F(1),F(2),F(10)]:
 for z in [F(i,8) for i in range(-160,161)]:
  center=z*z>=t*R*R;ys=[F(-1,8),F(0),F(1,8)] if center else [F(3,8),F(7,16),F(1,2)]
  ok(all(((1+(1-y*y)**2)**2*z*z-R*R)**2>=A*A*R**4 for y in ys),'well_barrier')
# All possible aligned axes and non-unit parameter, standalone raw-identity test.
for axis in range(4):
 raw=c.fixture(3,kappa=F(2,7),quadratic=F(3,11),quartic=F(0),coupling=F(9,2),axis=axis);a=c.acquire(raw)
 ok(a['axis']==axis and a['kappa']=='2/7' and a['q_min']=='3/11' and a['degree_cap']==4,'acquisition')
raw=c.fixture(1);kw={'quad_relative':F(1,5)};cert=c.certify(raw,**kw)
# Actual combined count ceiling and exact external total ratio.
total=cert['scalar_evaluations'];no(lambda:c.certify(raw,max_evaluations=total-1,**kw),'evaluation_budget');cc=c.certify(raw,max_evaluations=total,**kw);ok(cc['scalar_evaluations']==total,'evaluation_budget')
ratio=F(cert['full_ratio_exact']);cc=c.certify(raw,full_ratio=ratio,**kw);ok(c.verify(raw,cc,full_ratio=ratio,**kw)['status']=='PASS','total_ratio');no(lambda:c.certify(raw,full_ratio=(ratio+1)/2,**kw),'total_ratio');no(lambda:c.verify(raw,cc,**kw),'total_ratio')
def leaves(x,p=()):
 if type(x)is dict:
  for k,v in x.items():
   if k!='seconds':yield from leaves(v,p+(k,))
 elif type(x)is list:
  for k,v in enumerate(x):yield from leaves(v,p+(k,))
 else:yield p,x
for group in ['acquisition','mobility_family','task']:
 for path,val in leaves(cert[group]):
  bad=copy.deepcopy(cert);o=bad[group]
  for k in path[:-1]:o=o[k]
  o[path[-1]]=0 if type(val)is bool else (float(val) if type(val)is int else 'altered');no(lambda bad=bad:c.verify(raw,bad,**kw),'typed_scope')
for field in ['mass','resistance','jensen_resistance','free_rate','uniform_rate_enclosure','structural_ratio']:
 for side in ['lower','upper']:
  bad=copy.deepcopy(cert);bad[field][side]=str(F(bad[field][side])+1);no(lambda bad=bad:c.verify(raw,bad,**kw),'endpoints')
for key in ['schema','method','marginal','observable','basins','b','tail_upper','full_ratio_exact']:
 bad=copy.deepcopy(cert);bad.pop(key);no(lambda bad=bad:c.verify(raw,bad,**kw),'missing_scope')
for key in ['max_exponent_entries','max_total_coefficient_bits']:
 for val in [True,1.0,0,-1]:no(lambda key=key,val=val:c.certify(raw,**{key:val}),'input_budget_types')
# Full input-cost bounds can be exactly saturated and are checked against actual input.
a=c.acquire(raw);ok(c.acquire(raw,max_exponent_entries=a['raw_exponent_entries'])['raw_polynomial_sha256']==a['raw_polynomial_sha256'],'input_budget');no(lambda:c.acquire(raw,max_exponent_entries=a['raw_exponent_entries']-1),'input_budget');ok(c.acquire(raw,max_total_coefficient_bits=a['total_input_coefficient_bits'])['raw_polynomial_sha256']==a['raw_polynomial_sha256'],'input_budget');no(lambda:c.acquire(raw,max_total_coefficient_bits=a['total_input_coefficient_bits']-1),'input_budget')
print(json.dumps({'status':'PASS','independent_checks':n,'groups':groups},indent=2))
