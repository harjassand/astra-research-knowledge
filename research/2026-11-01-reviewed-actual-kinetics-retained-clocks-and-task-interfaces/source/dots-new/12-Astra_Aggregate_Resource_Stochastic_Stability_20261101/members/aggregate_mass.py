"""Pending aggregate-resource construction; not independently reviewed.
Reuses accepted exact graph/profile primitives, not a favorable raw grouping.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'frozen_free_port'))
import free_port_glue as G
from fractions import Fraction as F

def recognize(raw):
 r=G.architecture(raw);incident={v for e in r['edges']for v in e}
 free=tuple(v for v in r['satellites']if v not in incident)
 if not free:raise G.Unsupported('requires a nonempty acquired set of isolated hub-graph vertices')
 rare=tuple(v for v in r['satellites']if v not in free)
 core=[(tuple(z for j,z in enumerate(u)if j not in free),tuple(z for j,z in enumerate(v)if j not in free),k)for u,v,k in r['channels']if not any(u[j]or v[j]for j in free)]
 cr=G.C.B.recognize(core);kx=dict(r['kX'])
 r.update(free=free,rare=rare,kfree=min(kx[v]for v in free),ell=max(sum((ell for x,k,ell in h['arms']if x in free),F(0))for h in r['hubs']),krminus=min(kx[v]for v in rare),krplus=max(kx[v]for v in rare),inventory=G.C.compile_inventory(dict(satellites=rare,edges=r['edges'])),core_raw_sha256=cr['raw_sha256'])
 return r

def tail_plan(r,t,max_core_steps=100000):
 t=G.rat(t)
 if t<=1:raise ValueError('t>1')
 if type(max_core_steps)is not int or max_core_steps<0:raise ValueError('nonnegative exact core-loop budget')
 lam,mu=r['lam'],r['mu'];d=len(r['rare']);E=len(r['edges']);D=mu*(1-1/t);L=lam*(t-1)
 p=G.profile(lam,t,r['bmin']/(16*E));Kf=r['a_sum']+d*r['krplus'];J0=max(p['K']+1,2,G.ceilq(4*p['c']*(mu+Kf+p['beta'])/D))
 if p['K']-1+J0-1>max_core_steps:return dict(status='UNKNOWN_CORE_PROFILE_BUDGET',required=p['K']-1+J0-1)
 p=G.materialize(p,lam,t);g=lambda j:G.gv(p,j);dg=lambda j:g(j)-g(j+1)
 rho0=min(F(1),r['bmin']*p['dlow']/(88*r['smax']),p['eps']/(44*(Kf+lam*t)))
 e=min(F(1,4),D/(4*(r['F0']+D)),p['eps']/(4*mu));CA=L+11*mu
 Qhead=max((j+1)**2*max(mu*(g(j-1)/t-g(j))+Kf*j*dg(j-1)+2*p['beta']*j*dg(j)+e*(r['F0']+D),0)for j in range(1,J0))
 C0=1+L*g(0)+(Kf+r['smax']*E)*p['D1']+mu*p['D1']/4+11*rho0*(Kf+r['smax']*E+lam*t)+rho0*CA/4+e*mu
 H0=g(0)+rho0/4;zeta0=min(p['eps'],lam)/4
 delta=min(F(1,2*(d+1)),F(1,2*E),r['bmin']/(8*E*r['smax']*p['Gratio']))
 U0=G.ceilq(max(F(1),4*CA/r['krminus'],4*Qhead/(rho0*r['krminus'])))
 c=F(1);rho=min(F(1),r['bmin']*c/(4*r['smax']));B=2*L*c+rho*L/2+rho*lam*t
 m=min(r['bmin']*c*delta**2/(288*E),rho*r['kfree']*delta/36);cfree=min(lam/2,m/2);eta=(C0+1)/cfree
 K=G.ceilq(max(F(2),2*t/(t-1),4*B/m,F(2*U0),8*eta*B/zeta0))
 return dict(status='ACQUIRED_TAIL_AND_HEAD_PLAN',t=t,core_profile=p,core=dict(D=D,L=L,Kf=Kf,J0=J0,rho0=rho0,e=e,CA=CA,Qhead=Qhead,C0=C0,H0=H0,zeta0=zeta0,delta=delta,U0=U0),mass=dict(c=c,rho=rho,B=B,m=m,cfree=cfree,eta=eta,K=K),core_profile_steps=p['K']-1+J0-1)

def fixture(free_count=1):
 n=4+free_count;z=lambda *ix:tuple(ix.count(i)for i in range(n));hubs=[z(1,2),z(1,3),z(2,3)]
 raw=[(z(),z(0),F(1)),(z(0),z(),F(1))]
 for h in hubs:raw.extend([(z(0,0),h,F(1)),(h,z(0,0),F(1))])
 for x in (1,2,3):
  h=hubs[x-1];raw.extend([(z(0,x),h,F(1)),(h,z(0,x),F(2 if x==3 else 1))])
 for f in range(4,n):
  for h in hubs:raw.extend([(z(0,f),h,F(1)),(h,z(0,f),F(1))])
 return raw
if __name__=='__main__':
 import json
 r=recognize(fixture());p=tail_plan(r,F(2));print(json.dumps(G.encode(dict(status=p['status'],core_profile_steps=p.get('core_profile_steps'),mass=p.get('mass'),core=p.get('core'),raw_sha256=r['raw_sha256'])),indent=2))

def geometric_head(plan,r):
 if plan['status']!='ACQUIRED_TAIL_AND_HEAD_PLAN':return plan
 m=plan['mass'];q=4*plan['t'];Q=G.ceilq(q);K=m['K'];rho=m['rho'];c=m['c'];d=q*(rho+c)/(q-1);C=1+c/K+d
 nu=min(F(1),plan['core']['zeta0']/2)
 db=min(F(1,4),rho*r['kfree']/(4*(9*C*(r['a_sum']+r['krplus']+r['mu']/plan['t'])+4*rho*r['mu']+1)))
 L0=G.ceil_log2(4/db)+K*G.ceil_log2(Q)
 Jcoef=max(1,G.ceilq(8*m['eta']*(r['ell']*len(r['edges'])+r['mu'])*(C+2*c+rho/2)/nu))
 co=plan['core'];p0=plan['core_profile'];du=co['delta'];E=len(r['edges'])
 ku=min(co['D']*du/4,co['e']*r['b0']*du**2/(32*E))
 outer=(max(F(1),F(p0['K'])/du,4*co['CA']/r['krminus'],4*co['Qhead']/(co['rho0']*r['krminus'])),(2*co['L']+2*r['mu']+co['rho0']*(11*r['lam']*plan['t']+co['CA'])+1)/ku,(2*p0['c']+11*co['rho0'])*r['S']/(du**2*ku))
 return dict(status='PENDING_FACTORED_MASS_GLUE',outer_head_coefficients=outer,H_coefficients=(co['H0']+m['eta']*rho/4,m['eta']*C),K=K,q=q,Q=Q,d=d,C=C,nu=nu,delta_base=db,L0=L0,Jcoef=Jcoef,
 expressions=dict(Bhead='Q^K',deltaF='delta_base/Bhead',Jcut='Jcoef*Bhead',CZ='C*Bhead+2c+rho/2',D2='9C*Bhead',Cdeath='9mu*C*Bhead/t+4rho*mu',cutoff_exponent='L0+Jcoef*Q^K+1'),
 cost_scope='Nested exact powers; no expanded new head, global numerical cutoff or stationary moment bound')

def mass_g(plan,head,j,max_power_output_bits=100000):
 if type(j)is not int or j<0:raise ValueError('nonnegative exact integer resource')
 if type(max_power_output_bits)is not int or max_power_output_bits<0:raise ValueError('nonnegative exact power-bit upper-budget')
 K=plan['mass']['K'];c=plan['mass']['c']
 if j>=K:return 1+c/j
 e=K-j;q=head['q'];upper=e*max(q.numerator.bit_length(),q.denominator.bit_length())+1
 if upper>max_power_output_bits:return dict(status='UNKNOWN_POWER_VALUE_BUDGET',required_upper_power_bits=upper,budget=max_power_output_bits)
 return q**e*head['C']-head['d']


FAMILY='aggregate-free-mass-dyadic-glue-v1'
def qualitative(raw):
 try:r=recognize(raw)
 except G.Unsupported as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')
 return dict(status='QUALITATIVE_ARGUMENT_ACQUIRED_PENDING_WHOLE_REVIEW',family=FAMILY,raw_sha256=r['raw_sha256'],core_raw_sha256=r['core_raw_sha256'],open_coordinate=r['a'],free_coordinates=r['free'],rare_coordinates=r['rare'],inventory=r['inventory'],conclusion='irreducible positive recurrence and every finite exponential stationary total-count moment for the stated raw class; pending independent review',stationary_fiber_laws=0,profile_steps=0)

def construct(raw,t,max_core_steps=100000):
 t=G.rat(t)
 if t<=1:raise ValueError('t>1')
 if type(max_core_steps)is not int or max_core_steps<0:raise ValueError('nonnegative exact core-loop budget')
 q=qualitative(raw)
 if q['status']=='UNKNOWN':return q
 r=recognize(raw);p=tail_plan(r,t,max_core_steps)
 if p['status']=='UNKNOWN_CORE_PROFILE_BUDGET':return dict(status=p['status'],family=FAMILY,qualitative=q,required_core_steps=p['required'],max_core_steps=max_core_steps)
 head=geometric_head(p,r)
 cert=dict(status='SYMBOLIC_FOSTER_ARGUMENT_ACQUIRED_PENDING_WHOLE_REVIEW',family=FAMILY,raw_sha256=r['raw_sha256'],t=t,qualitative=q,plan=p,mass_head=head,
  formulas=dict(Bhead='Q^K',H='H_coefficients[0]+H_coefficients[1]*Bhead',zeta='nu/(2H)',outer_U='2*(2^(L0+Jcoef*Bhead+1)+1)',Nstar='ceil(A1*outer_U+A2*outer_U^2+A4*outer_U^4+1)',Foster_constant='(zeta+lambda+mu*Nstar+S*Nstar^2)*H*t^(Nstar+1)',stationary_bound='pi(t^N)<=2*Foster_constant/zeta'),
  work=dict(core_backward_steps=p['core_profile']['K']-1,core_compensation_steps=p['core']['J0']-1,additional_core_profile_scan_points=4*p['core_profile']['K'],core_head_copies=p['core_profile']['K'],new_mass_head_unrolled_steps=0,expanded_mass_head_powers=0,expanded_outer_head=0,stationary_fiber_laws=0),
  cost_scope='Exact nested factored expression; no complete numerical-polynomial or practical stationary-tail claim. Core-loop budget excludes other scans, rational arithmetic, serialization and requested power expansions.')
 cert['work']['largest_retained_scalar_bits']=G.bits(cert)
 return cert
