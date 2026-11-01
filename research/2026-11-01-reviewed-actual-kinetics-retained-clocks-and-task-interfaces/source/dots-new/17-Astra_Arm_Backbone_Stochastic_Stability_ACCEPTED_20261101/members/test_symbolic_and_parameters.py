"""NEW recovery wire/AST/count arithmetic and fractional-rate preflight."""
from fractions import Fraction as F
from itertools import product
from copy import deepcopy
import json,hashlib
import arm_backbone as B
A,G=B.A,B.G
counts={}
def hit(k):counts[k]=counts.get(k,0)+1
raw=B.fixture();r=B.recognize(raw);c=B.construct(raw,2);wire=json.loads(G.canonical(c))
assert B.receive_symbolic(raw,2,wire);hit('full_wire_receipt')
for key in('K','Q','L0','Jcoef','nu','delta_base'):
 bad=deepcopy(wire);bad['mass_head'][key]=0;assert not B.receive_symbolic(raw,2,bad);hit('semantic_mutations')
saved=B._rational_power
B._rational_power=lambda *a:(_ for _ in ()).throw(AssertionError('unpaid power'))
for k in(0,1,10,1000,10000):
 for aa in(0,1,2):
  x=[0]*r['n'];x[r['free'][0]]=10**k;x[r['a']]=aa
  assert B.scaled_value(r,c,x)>=F(3,4);B.scaled_drift(r,c,x);assert not B.outside_head(c,sum(x));hit('actual_zero_cutoff_power_free')
B._rational_power=saved
for K in(2,3,8):
 p=deepcopy(c['plan']);p['mass']['K']=K;hd=B.geometric_head(p,r);hd['Jcoef']=1;syn=deepcopy(c);syn['plan']=p;syn['mass_head']=hd;power=hd['Q']**K
 for aa in(0,1,2):
  for rc in(0,1,2):
   for offset in(1,2,min(power,300)):
    x=[0]*r['n'];x[r['a']]=aa
    for v in r['rare']:x[v]=rc
    U=sum(x);x[r['free'][0]]=((U+1)<<(hd['L0']+offset))-1;N=sum(x);J=U+aa;R=aa+G.C.cover_weight(r['inventory'],x);co=p['core']
    h0=G.gv(p['core_profile'],R)+co['rho0']*F(aa,(R+1)**2)-co['e']*F(aa,N+1)
    phi=max(F(0),min(F(1),(G.dyadic(x[r['free'][0]]+1)-G.dyadic(U+1)-hd['L0'])/power))
    assert phi>0 and B.scaled_value(r,syn,x)==h0+p['mass']['eta']*phi*(A.mass_g(p,hd,J)-1+p['mass']['rho']*F(aa,(J+1)**2));hit('synthetic_positive_cutoff')
for q in range(2,7):
 for k in range(10):
  for lim in(0,1,q**k-1,q**k,q**k+1,7,100):
   assert B.power_at_most(q,k,lim)==(q**k if q**k<=lim else None);hit('capped_power_comparisons')
for Q in(2,3,4):
 for K in(1,2,3):
  for jc in(1,2):
   for l0 in(0,3):
    syn=deepcopy(c);h=syn['mass_head'];h.update(Q=Q,K=K,Jcoef=jc,L0=l0,outer_head_coefficients=(F(1),F(3,2),F(1,3)))
    U=2*((1<<(l0+jc*Q**K+1))+1);ns=G.ceilq(1+U+F(3,2)*U**2+F(1,3)*U**4)
    for N in(0,1,ns-1,ns,ns+1):assert B.outside_head(syn,N)==(N>=ns);hit('nested_head_comparisons')
for bad in(True,1.0,'1',-1,None):
 try:B.outside_head(c,bad)
 except(ValueError,TypeError):hit('count_domain_refusals')
 else:raise AssertionError('invalid count')
dag=B.certificate_expressions(raw,c);assert G.digest(dag)=='fd2eec4926b4016c47edcd027a7e62c2bb10a9d787c47438d3c0e1bb8b21b7d2'
for name in dag['outputs']:
 assert B.evaluate_expression(dag,name,100000)['status']=='UNKNOWN_POWER_INTERMEDIATE_BUDGET';hit('actual_DAG_refusals')
for K in(2,3,4):
 syn=deepcopy(c);h=syn['mass_head'];h.update(K=K,Q=2,L0=1,Jcoef=1,outer_head_coefficients=(F(1),F(1,2),F(1,4)),H_coefficients=(F(2),F(3)),nu=F(1,7))
 d=B.certificate_expressions(raw,syn);bh=2**K;ex=2+bh;U=2*(2**ex+1);N=G.ceilq(1+U+F(1,2)*U**2+F(1,4)*U**4);H=2+3*bh;zeta=F(1,7)/(2*H)
 for key,val in dict(Bhead=bh,cutoff_exponent=ex,Ucut=U,Nstar=N,H=H,zeta=zeta).items():assert B.evaluate_expression(d,key,10000)==val;hit('synthetic_DAG_exact_outputs')
 for key in('Foster_constant','stationary_bound'):assert B.evaluate_expression(d,key,10000)['status']=='UNKNOWN_POWER_INTERMEDIATE_BUDGET';hit('synthetic_DAG_power_refusals')
syn=deepcopy(c);syn.update(status='PENDING_CORE_ONLY_FOSTER',head=3,H=F(5),zeta=F(1,11));d=B.certificate_expressions(raw,syn);cf=(F(1,11)+r['lam']+3*r['mu']+9*r['S'])*5*2**4
for key,val in dict(Nstar=3,H=5,zeta=F(1,11),Foster_constant=cf,stationary_bound=22*cf).items():assert B.evaluate_expression(d,key)==val;hit('synthetic_DAG_exact_outputs')
for bad in({},dict(format='bad',nodes=[],outputs={}),dict(format='exact-rational-dag-v1',nodes=[['q',True,1]],outputs={'x':0}),dict(format='exact-rational-dag-v1',nodes=[['add',0]],outputs={'x':0}),dict(format='exact-rational-dag-v1',nodes=[['q',1,0]],outputs={'x':0}),dict(format='exact-rational-dag-v1',nodes=[['q',1,1]],outputs={'x':-1})):
 try:B.evaluate_expression(bad,'x')
 except ValueError:hit('malformed_DAG_refusals')
 else:raise AssertionError('malformed DAG')
parameters=[]
for t,af,ar in[(F(7,5),F(1,1000),F(1000)),(F(17,5),F(100),F(1,100))]:
 rr=[]
 for i,(u,v,k)in enumerate(raw):
  if sum(u)==0:k=F(2,7)
  elif sum(v)==0:k=F(11,3)
  elif u[4]+u[5]==2:k=ar
  elif v[4]+v[5]==2:k=af
  else:k*=F(i%3+2,i%2+1)
  rr.append((u,v,k))
 rec=B.recognize(rr);cert=B.construct(rr,t,250000);assert cert['status']=='PENDING_NESTED_SYMBOLIC_FOSTER';hit('joint_fractional_certificates')
 co=cert['plan']['core'];K=cert['mass_head']['K']
 for x in product(range(2),repeat=rec['n']):assert B.scaled_drift(rec,cert,x)<=co['C0'];hit('joint_fractional_core_states')
 for j in range(K-5,K+5):
  gj=A.mass_g(cert['plan'],cert['mass_head'],j);g1=A.mass_g(cert['plan'],cert['mass_head'],j+1);g2=A.mass_g(cert['plan'],cert['mass_head'],j+2)
  assert gj-g1>=F(1,(j+1)**2)
  if j<K:assert gj>=2*t*(g2+cert['plan']['mass']['rho'])
  hit('joint_actual_head_joins')
 NN=B.core_head(rec,cert['plan'],F(1,2))+10
 for aa in(0,1,NN//3):
  x=[0]*rec['n'];x[rec['a']]=aa
  for j,v in enumerate(rec['rare']):x[v]=(NN-aa)//len(rec['rare'])+(j<(NN-aa)%len(rec['rare']))
  x[rec['free'][0]]=NN
  assert B.scaled_drift(rec,cert,x)<=-co['zeta0']*B.scaled_value(rec,cert,x);hit('joint_partial_core_tail')
 parameters.append(dict(t=str(t),q=str(cert['mass_head']['q']),Q=cert['mass_head']['Q'],core_steps=cert['plan']['core_profile_steps'],mass_K=K))
print(json.dumps(dict(status='PASS_NEW_RECOVERY_SYMBOLIC_AND_PARAMETERS',counts=counts,parameters=parameters,main_canonical_bytes=len(G.canonical(c).encode()),main_sha256=G.digest(c),expression_nodes=len(dag['nodes']),expression_sha256=G.digest(dag),scope='New test bytes, author receiving only. Synthetic arithmetic is not global Foster validation; all actual enormous heads and moment bounds unexpanded.'),indent=2))
