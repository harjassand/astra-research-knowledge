"""Recovered exact-rational arm-backbone prototype; new whole review required.
Reconstructed from warm transcript after workspace replacement; new byte version.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'frozen_aggregate'))
import aggregate_mass as A
G=A.G
from fractions import Fraction as F

def recognize(raw):
 full=G.architecture(raw);aux=tuple(h for h in full['hubs']if not h['arms']);ah={h['complex']for h in aux}
 base=[row for row in full['channels']if row[0]not in ah and row[1]not in ah]
 try:r=A.recognize(base)
 except G.Unsupported:
  r=G.architecture(base);incident={v for e in r['edges']for v in e}
  if set(r['satellites'])!=incident:raise
  cb=G.C.B.recognize(base);rare=r['satellites'];kx=dict(r['kX'])
  r.update(free=(),rare=rare,kfree=None,ell=F(0),krminus=min(kx.values()),krplus=max(kx.values()),inventory=G.C.compile_inventory(dict(satellites=rare,edges=r['edges'])),core_raw_sha256=cb['raw_sha256'])
 r.update(base_raw_sha256=r['raw_sha256'],raw_sha256=full['raw_sha256'],channels=full['channels'],internal=full['internal'],S=full['S'],F0=full['F0'],auxiliary=aux,aD=sum((h['to_hub']for h in aux),F(0)),BD=sum((h['to_two_a']for h in aux),F(0)),full_edges=full['edges'])
 return r

def plan(r,t,max_core_steps=100000):
 t=G.rat(t)
 if t<=1:raise ValueError('t>1')
 if type(max_core_steps)is not int or max_core_steps<0:raise ValueError('exact nonnegative loop budget')
 lam,mu=r['lam'],r['mu'];d=len(r['rare']);E=len(r['edges']);D=mu*(1-1/t);L=lam*(t-1);aD=r['aD'];BD=r['BD']
 p=G.profile(lam,t,r['bmin']/(16*E));Kf=r['a_sum']+d*r['krplus']
 J0=max(p['K']+2,4,G.ceilq(8*p['c']*(mu+Kf+2*aD+p['beta'])/D));steps=p['K']+J0-2
 if steps>max_core_steps:return dict(status='UNKNOWN_CORE_PROFILE_BUDGET',required=steps)
 p=G.materialize(p,lam,t);g=lambda j:G.gv(p,j);dg=lambda j:g(j)-g(j+1)
 rho0=min(F(1),r['bmin']*p['dlow']/(88*r['smax']),p['eps']/(4*(11*(Kf+lam*t)+20*aD+2*BD)))
 e=min(F(1,4),D/(4*(r['F0']+D)),p['eps']/(4*mu));CA=L+11*mu
 Qhead=max((j+1)**2*max(mu*(g(j-1)/t-g(j))+Kf*j*dg(j-1)+aD*j*(g(max(0,j-2))-g(j))+2*p['beta']*j*dg(j)+e*(r['F0']+D),0)for j in range(1,J0))
 C0=1+L*g(0)+(Kf+r['smax']*E)*p['D1']+mu*p['D1']/4+11*rho0*(Kf+r['smax']*E+lam*t)+rho0*CA/4+e*mu+aD*p['D2']+20*rho0*aD+2*rho0*BD
 H0=g(0)+rho0/4;zeta0=min(p['eps'],lam)/4
 delta=min(F(1,2*(d+1)),F(1,2*E),r['bmin']/(8*E*r['smax']*p['Gratio']))
 U0=G.ceilq(max(F(1),4*CA/r['krminus'],4*Qhead/(rho0*r['krminus'])))
 co=dict(D=D,L=L,Kf=Kf,J0=J0,rho0=rho0,e=e,CA=CA,Qhead=Qhead,C0=C0,H0=H0,zeta0=zeta0,delta=delta,U0=U0)
 out=dict(status='ACQUIRED_CORE_ENERGY_PLAN',t=t,core_profile=p,core=co,core_profile_steps=steps)
 if not r['free']:
  out['core_only_head']=core_head(r,out,F(1));return out
 c=F(1);rho=min(F(1),r['bmin']*c/(4*r['smax']));B=2*L*c+rho*L/2+rho*lam*t
 m=min(r['bmin']*c*delta**2/(288*E),rho*r['kfree']*delta/36);cfree=min(lam/2,m/2);eta=(C0+1)/cfree
 K=G.ceilq(max(F(2),2*t/(t-1),4*B/m,F(2*U0),8*eta*B/zeta0))
 out.update(status='ACQUIRED_TAIL_AND_HEAD_PLAN',mass=dict(c=c,rho=rho,B=B,m=m,cfree=cfree,eta=eta,K=K));return out

def core_head(r,p,gamma):
 co=p['core'];pf=p['core_profile'];delta=co['delta']*gamma
 cint=2*co['L']+2*r['mu']+(4*pf['c']+20*co['rho0'])*r['S']/delta**2+co['rho0']*(11*r['lam']*p['t']+co['CA'])
 kap=min(co['D']*delta/4,co['e']*r['b0']*delta**2/(32*len(r['edges'])))
 return G.ceilq(max(F(1),F(max(pf['K']+2,4))/delta,4*co['CA']/(r['krminus']*gamma),4*co['Qhead']/(co['rho0']*r['krminus']*gamma),(cint+1)/kap))

def geometric_head(p,r):
 m=p['mass'];q=4*p['t'];Q=G.ceilq(q);K=m['K'];rho=m['rho'];c=m['c'];d=q*(rho+c)/(q-1);C=1+c/K+d;nu=min(F(1),p['core']['zeta0']/2)
 db=min(F(1,4),rho*r['kfree']/(4*(C*(9*(r['a_sum']+r['krplus']+r['mu']/p['t'])+25*r['aD'])+40*rho*r['aD']+4*rho*r['mu']+1)))
 L0=G.ceil_log2(4/db)+K*G.ceil_log2(Q)
 Jcoef=max(1,G.ceilq(8*m['eta']*(r['ell']*len(r['edges'])+r['mu']+8*r['aD'])*(C+2*c+rho/2)/nu))
 co=p['core'];pf=p['core_profile'];du=co['delta'];E=len(r['edges']);ku=min(co['D']*du/4,co['e']*r['b0']*du**2/(32*E))
 outer=(max(F(1),F(max(pf['K']+2,4))/du,4*co['CA']/r['krminus'],4*co['Qhead']/(co['rho0']*r['krminus'])),(2*co['L']+2*r['mu']+co['rho0']*(11*r['lam']*p['t']+co['CA'])+1)/ku,(4*pf['c']+20*co['rho0'])*r['S']/(du**2*ku))
 return dict(status='PENDING_FACTORED_ARM_BACKBONE_GLUE',outer_head_coefficients=outer,H_coefficients=(co['H0']+m['eta']*rho/4,m['eta']*C),K=K,q=q,Q=Q,d=d,C=C,nu=nu,delta_base=db,L0=L0,Jcoef=Jcoef,expressions=dict(Bhead='Q^K',deltaF='delta_base/Bhead',Jcut='Jcoef*Bhead',D2='9C*Bhead',D4='25C*Bhead',CZ='C*Bhead+2c+rho/2',extra_cross='32CZ*aD/Jcut'),scope='Pending new full proof/code review; nested powers unexpanded')

def fixture():
 raw=A.fixture(2);n=6;z=lambda *ix:tuple(ix.count(i)for i in range(n));raw.extend([(z(0,0),z(4,5),F(1)),(z(4,5),z(0,0),F(1))]);return raw

def qualitative(raw):
 try:r=recognize(raw)
 except G.Unsupported as exc:return dict(status='UNKNOWN',reason=str(exc),stability='UNKNOWN')
 return dict(status='ARM_BACKBONE_ARGUMENT_PENDING_WHOLE_REVIEW',family='arm-backbone-amplification-detours-v1',raw_sha256=r['raw_sha256'],base_raw_sha256=r['base_raw_sha256'],open_coordinate=r['a'],free_coordinates=r['free'],rare_coordinates=r['rare'],arm_edges=r['edges'],auxiliary_edges=tuple(h['edge']for h in r['auxiliary']),inventory=r['inventory'],conclusion='nonexplosion, irreducible positive recurrence and every finite exponential stationary total-count moment for the stated raw class',stationary_fiber_laws=0)

def construct(raw,t,max_core_steps=100000):
 t=G.rat(t)
 if t<=1:raise ValueError('t>1')
 if type(max_core_steps)is not int or max_core_steps<0:raise ValueError('exact nonnegative loop budget')
 q=qualitative(raw)
 if q['status']=='UNKNOWN':return q
 r=recognize(raw);p=plan(r,t,max_core_steps)
 if p['status']=='UNKNOWN_CORE_PROFILE_BUDGET':return dict(status=p['status'],qualitative=q,required_core_steps=p['required'],max_core_steps=max_core_steps)
 common=dict(family=q['family'],raw_sha256=r['raw_sha256'],t=t,qualitative=q,plan=p,work=dict(core_backward_steps=p['core_profile']['K']-1,compensation_steps=p['core']['J0']-1,additional_core_scan_points=4*p['core_profile']['K'],core_head_copies=p['core_profile']['K'],mass_head_unrolled_steps=0,mass_head_powers_expanded=0,outer_head_powers_expanded=0),scope='Trusted exact constructor and nested expressions; independent whole review pending; no practical numeric moment bound')
 if not r['free']:common.update(status='PENDING_CORE_ONLY_FOSTER',head=p['core_only_head'],zeta=p['core']['zeta0'],H=p['core']['H0'])
 else:common.update(status='PENDING_NESTED_SYMBOLIC_FOSTER',mass_head=geometric_head(p,r))
 common['formulas']=dict(W='t^N * scaled_value',Foster_constant='(zeta+lambda+mu*Nstar+S*Nstar^2)*H*t^(Nstar+1)',stationary_bound='pi(t^N)<=2*Foster_constant/zeta',expression_interface='certificate_expressions(raw,received_certificate): explicit finite rational arithmetic DAG')
 common['work']['largest_retained_scalar_bits']=G.bits(common);return common

def receive_symbolic(raw,t,receipt,max_core_steps=100000):return G.canonical(construct(raw,t,max_core_steps))==G.canonical(receipt)

def power_at_most(q,k,limit):
 if any(type(x)is not int for x in(q,k,limit))or q<2 or k<0 or limit<0:raise ValueError('q>=2,k>=0,limit>=0 exact integers')
 if limit<1:return None
 acc=1;base=min(q,limit+1)
 while k:
  if k&1:
   acc*=base
   if acc>limit:return None
  k//=2
  if k:base=min(base*base,limit+1)
 return acc

def outside_head(cert,N):
 if type(N)is not int or N<0:raise ValueError('nonnegative exact integer count')
 if cert['status']=='PENDING_CORE_ONLY_FOSTER':return N>=cert['head']
 hd=cert['mass_head'];bits=N.bit_length();L0=hd['L0'];Jc=hd['Jcoef']
 if bits<=L0+2:return False
 limit=(bits-L0-3)//Jc;B=power_at_most(hd['Q'],hd['K'],limit)
 if B is None:return False
 exponent=L0+Jc*B+1;assert exponent+1<bits
 U=2*((1<<exponent)+1);a,b,c=hd['outer_head_coefficients'];cutoff=G.ceilq(a*U+b*U**2+c*U**4+1)
 return N>=cutoff

def _rational_power(q,k):return q**k

def scaled_value(r,cert,x):
 if type(x)not in(list,tuple)or len(x)!=r['n']or any(type(v)is not int or v<0 for v in x):raise ValueError('one exact nonnegative count per coordinate')
 p=cert['plan'];co=p['core'];N=sum(x);a=x[r['a']];R=a+G.C.cover_weight(r['inventory'],x)
 h0=G.gv(p['core_profile'],R)+co['rho0']*F(a,(R+1)**2)-co['e']*F(a,N+1)
 if cert['status']=='PENDING_CORE_ONLY_FOSTER':return h0
 hd=cert['mass_head'];f=sum(x[v]for v in r['free']);u=N-f;j=u+a
 numerator=G.dyadic(f+1)-G.dyadic(u+1)-hd['L0']
 if numerator<=0:return h0
 state_bits=(f+1).bit_length();assert hd['K']*G.ceil_log2(hd['Q'])+1<=state_bits
 power=_rational_power(hd['Q'],hd['K']);assert power.bit_length()<=state_bits
 phi=min(F(1),numerator/(hd['Jcoef']*power))
 if j>=hd['K']:g=1+p['mass']['c']/j
 else:g=_rational_power(hd['q'],hd['K']-j)*hd['C']-hd['d']
 return h0+p['mass']['eta']*phi*(g-1+p['mass']['rho']*F(a,(j+1)**2))

def scaled_drift(r,cert,x):
 value=scaled_value(r,cert,x);out=F(0)
 for src,dst,k in r['channels']:
  rate=k*G.C.B.falling(x,src)
  if rate:
   y=tuple(xx-uu+vv for xx,uu,vv in zip(x,src,dst));out+=rate*(cert['t']**(sum(dst)-sum(src))*scaled_value(r,cert,y)-value)
 return out

def certificate_expressions(raw,cert):
 r=recognize(raw)
 if r['raw_sha256']!=cert['raw_sha256']:raise ValueError('raw certificate binding')
 nodes=[]
 def q(x):
  x=G.rat(x);nodes.append(['q',x.numerator,x.denominator]);return len(nodes)-1
 def op(name,*children):nodes.append([name,*children]);return len(nodes)-1
 if cert['status']=='PENDING_CORE_ONLY_FOSTER':ns=q(cert['head']);H=q(cert['H']);zeta=q(cert['zeta']);out={}
 elif cert['status']=='PENDING_NESTED_SYMBOLIC_FOSTER':
  hd=cert['mass_head'];bh=op('pow',q(hd['Q']),q(hd['K']))
  exponent=op('add',q(hd['L0']+1),op('mul',q(hd['Jcoef']),bh));U=op('mul',q(2),op('add',q(1),op('pow',q(2),exponent)))
  a,b,c=hd['outer_head_coefficients'];ns=op('ceil',op('add',q(1),op('mul',q(a),U),op('mul',q(b),op('pow',U,q(2))),op('mul',q(c),op('pow',U,q(4)))))
  H=op('add',q(hd['H_coefficients'][0]),op('mul',q(hd['H_coefficients'][1]),bh));zeta=op('div',q(hd['nu']),op('mul',q(2),H));out=dict(Bhead=bh,cutoff_exponent=exponent,Ucut=U)
 else:raise ValueError('a complete symbolic certificate is required')
 cf=op('mul',op('add',zeta,q(r['lam']),op('mul',q(r['mu']),ns),op('mul',q(r['S']),op('pow',ns,q(2)))),H,op('pow',q(cert['t']),op('add',ns,q(1))))
 bound=op('div',op('mul',q(2),cf),zeta);out.update(Nstar=ns,H=H,zeta=zeta,Foster_constant=cf,stationary_bound=bound)
 return dict(format='exact-rational-dag-v1',raw_sha256=r['raw_sha256'],nodes=nodes,outputs=out)

def evaluate_expression(dag,name,max_power_bits=100000):
 if type(max_power_bits)is not int or max_power_bits<0:raise ValueError('nonnegative exact power budget')
 if type(dag)is not dict or dag.get('format')!='exact-rational-dag-v1':raise ValueError('DAG format')
 nodes=dag.get('nodes');outputs=dag.get('outputs')
 if type(nodes)is not list or type(outputs)is not dict or name not in outputs:raise ValueError('DAG output')
 arities=dict(add=None,mul=None,div=2,pow=2,ceil=1)
 for i,node in enumerate(nodes):
  if type(node)is not list or not node or type(node[0])is not str:raise ValueError('DAG node')
  if node[0]=='q':
   if len(node)!=3 or any(type(x)is not int for x in node[1:])or node[2]<=0:raise ValueError('rational leaf')
  else:
   if node[0]not in arities:raise ValueError('operation')
   arity=arities[node[0]]
   if(arity is None and len(node)<2)or(arity is not None and len(node)!=arity+1):raise ValueError('arity')
   if any(type(j)is not int or not 0<=j<i for j in node[1:]):raise ValueError('acyclic earlier node references')
 if any(type(j)is not int or not 0<=j<len(nodes)for j in outputs.values()):raise ValueError('output reference')
 class PowerBudget(Exception):pass
 cache={}
 def ev(i):
  if i in cache:return cache[i]
  node=nodes[i];op=node[0]
  if op=='q':result=F(node[1],node[2])
  else:
   args=[ev(j)for j in node[1:]]
   if op=='add':result=sum(args,F(0))
   elif op=='mul':
    result=F(1)
    for a in args:result*=a
   elif op=='div':result=args[0]/args[1]
   elif op=='ceil':result=F(G.ceilq(args[0]))
   else:
    b,e=args
    if e.denominator!=1 or e<0:raise ValueError('nonnegative integral exponent')
    e=int(e);upper=e*max(abs(b.numerator).bit_length(),b.denominator.bit_length())+1
    if upper>max_power_bits:raise PowerBudget((i,upper))
    result=b**e
  cache[i]=result;return result
 try:return ev(outputs[name])
 except PowerBudget as exc:return dict(status='UNKNOWN_POWER_INTERMEDIATE_BUDGET',node=exc.args[0][0],required_upper_power_bits=exc.args[0][1],budget=max_power_bits,expression_retained=True)

if __name__=='__main__':
 import json
 r=recognize(fixture());p=plan(r,F(2));h=geometric_head(p,r)
 print(json.dumps(G.encode(dict(status=p['status'],raw_sha256=r['raw_sha256'],free=r['free'],arm_edges=r['edges'],full_edges=r['full_edges'],auxiliary_rates=(r['aD'],r['BD']),core_steps=p['core_profile_steps'],core=p['core'],mass=p['mass'],head=h)),indent=2))
