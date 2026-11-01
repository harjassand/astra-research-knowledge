"""New recovered-source whole receiver, no candidate imports.
Only separately authored raw/profile/cover/arithmetic primitives are retained.
"""
from pathlib import Path
from fractions import Fraction as F
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'retained'))
import independent_aggregate_receiver as I
P=I.P
rat,ceil,canonical,digest,bits=I.rat,I.ceil,I.canonical,I.digest,I.bits

def parse(raw):
 full=P.architecture(raw);aux=tuple(h for h in full['hubs']if not h['arms']);omit={h['complex']for h in aux}
 base=[(u,v,k)for u,v,k in full['channels']if u not in omit and v not in omit];r=P.architecture(base)
 used={v for e in r['edges']for v in e};free=tuple(v for v in r['satellites']if v not in used);rare=tuple(v for v in r['satellites']if v in used);kx=dict(r['kX']);keep=[i for i in range(r['n'])if i not in free]
 core=[(tuple(u[i]for i in keep),tuple(v[i]for i in keep),k)for u,v,k in r['channels']if not any(u[f]or v[f]for f in free)];cr=P.B.parse(core)
 r.update(free=free,rare=rare,kfree=min(kx[v]for v in free)if free else None,ell=max(sum((back for x,_,back in h['arms']if x in free),F(0))for h in r['hubs']),krminus=min(kx[v]for v in rare),krplus=max(kx[v]for v in rare),inventory=P.C.compile_inventory(dict(satellites=rare,edges=r['edges'])),core_raw_sha256=cr['raw_sha256'])
 r.update(base_raw_sha256=r['raw_sha256'],raw_sha256=full['raw_sha256'],channels=full['channels'],internal=full['internal'],S=full['S'],F0=full['F0'],auxiliary=aux,aD=sum((h['to_hub']for h in aux),F(0)),BD=sum((h['to_two_a']for h in aux),F(0)),full_edges=full['edges']);return r

def qualitative(raw):
 try:r=parse(raw)
 except P.Outside as e:return dict(status='UNKNOWN',reason=str(e),stability='UNKNOWN')
 return dict(status='ARM_BACKBONE_ARGUMENT_PENDING_WHOLE_REVIEW',family='arm-backbone-amplification-detours-v1',raw_sha256=r['raw_sha256'],base_raw_sha256=r['base_raw_sha256'],open_coordinate=r['a'],free_coordinates=r['free'],rare_coordinates=r['rare'],arm_edges=r['edges'],auxiliary_edges=tuple(h['edge']for h in r['auxiliary']),inventory=r['inventory'],conclusion='nonexplosion, irreducible positive recurrence and every finite exponential stationary total-count moment for the stated raw class',stationary_fiber_laws=0)

def core_head(r,p,gamma):
 co=p['core'];pf=p['core_profile'];delta=co['delta']*gamma;kap=min(co['D']*delta/4,co['e']*r['b0']*delta**2/(32*len(r['edges'])))
 cint=2*co['L']+2*r['mu']+(4*pf['c']+20*co['rho0'])*r['S']/delta**2+co['rho0']*(11*r['lam']*p['t']+co['CA'])
 return ceil(max(F(1),F(max(pf['K']+2,4))/delta,4*co['CA']/(r['krminus']*gamma),4*co['Qhead']/(co['rho0']*r['krminus']*gamma),(cint+1)/kap))

def plan(r,t,cap=100000):
 lam,mu=r['lam'],r['mu'];d=len(r['rare']);E=len(r['edges']);L=lam*(t-1);D=mu*(1-1/t);ad,bd=r['aD'],r['BD'];pf=P.shape(lam,t,r['bmin']/(16*E));kf=r['a_sum']+d*r['krplus'];jm=max(pf['K']+2,4,ceil(8*pf['c']*(mu+kf+2*ad+pf['beta'])/D));steps=pf['K']+jm-2
 if steps>cap:return dict(status='UNKNOWN_CORE_PROFILE_BUDGET',required=steps)
 pf=P.acquire_profile(pf,lam,t);g=lambda j:P.g(pf,j);dg=lambda j:g(j)-g(j+1)
 rho0=min(F(1),r['bmin']*pf['dlow']/(88*r['smax']),pf['eps']/(4*(11*(kf+lam*t)+20*ad+2*bd)))
 e=min(F(1,4),D/(4*(r['F0']+D)),pf['eps']/(4*mu));CA=L+11*mu;qh=F(0)
 for j in range(1,jm):
  Er=mu*(g(j-1)/t-g(j))+kf*j*dg(j-1)+ad*j*(g(max(0,j-2))-g(j))+2*pf['beta']*j*dg(j)
  qh=max(qh,(j+1)**2*max(Er+e*(r['F0']+D),0))
 C0=1+L*g(0)+(kf+r['smax']*E)*pf['D1']+mu*pf['D1']/4+11*rho0*(kf+r['smax']*E+lam*t)+rho0*CA/4+e*mu+ad*pf['D2']+20*rho0*ad+2*rho0*bd
 H0=g(0)+rho0/4;zeta0=min(pf['eps'],lam)/4;delta=min(F(1,2*(d+1)),F(1,2*E),r['bmin']/(8*E*r['smax']*pf['Gratio']));U0=ceil(max(F(1),4*CA/r['krminus'],4*qh/(rho0*r['krminus'])))
 co=dict(D=D,L=L,Kf=kf,J0=jm,rho0=rho0,e=e,CA=CA,Qhead=qh,C0=C0,H0=H0,zeta0=zeta0,delta=delta,U0=U0)
 out=dict(status='ACQUIRED_CORE_ENERGY_PLAN',t=t,core_profile=pf,core=co,core_profile_steps=steps)
 if not r['free']:out['core_only_head']=core_head(r,out,F(1));return out
 rho=min(F(1),r['bmin']/(4*r['smax']));birth=2*L+rho*L/2+rho*lam*t;mm=min(r['bmin']*delta**2/(288*E),rho*r['kfree']*delta/36);cfree=min(lam/2,mm/2);eta=(C0+1)/cfree
 K=ceil(max(F(2),2*t/(t-1),4*birth/mm,F(2*U0),8*eta*birth/zeta0));out.update(status='ACQUIRED_TAIL_AND_HEAD_PLAN',mass=dict(c=F(1),rho=rho,B=birth,m=mm,cfree=cfree,eta=eta,K=K));return out

def head(p,r):
 m=p['mass'];rho=m['rho'];c=m['c'];t=p['t'];K=m['K'];q=4*t;Q=ceil(q);d=q*(rho+c)/(q-1);C=1+c/K+d;co=p['core'];pf=p['core_profile'];nu=min(F(1),co['zeta0']/2)
 db=min(F(1,4),rho*r['kfree']/(4*(C*(9*(r['a_sum']+r['krplus']+r['mu']/t)+25*r['aD'])+40*rho*r['aD']+4*rho*r['mu']+1)))
 L0=P.logceil(4/db)+K*P.logceil(Q);jc=max(1,ceil(8*m['eta']*(r['ell']*len(r['edges'])+r['mu']+8*r['aD'])*(C+2*c+rho/2)/nu));du=co['delta'];ku=min(co['D']*du/4,co['e']*r['b0']*du**2/(32*len(r['edges'])))
 outer=(max(F(1),F(max(pf['K']+2,4))/du,4*co['CA']/r['krminus'],4*co['Qhead']/(co['rho0']*r['krminus'])),(2*co['L']+2*r['mu']+co['rho0']*(11*r['lam']*t+co['CA'])+1)/ku,(4*pf['c']+20*co['rho0'])*r['S']/(du**2*ku))
 return dict(status='PENDING_FACTORED_ARM_BACKBONE_GLUE',outer_head_coefficients=outer,H_coefficients=(co['H0']+m['eta']*rho/4,m['eta']*C),K=K,q=q,Q=Q,d=d,C=C,nu=nu,delta_base=db,L0=L0,Jcoef=jc,expressions=dict(Bhead='Q^K',deltaF='delta_base/Bhead',Jcut='Jcoef*Bhead',D2='9C*Bhead',D4='25C*Bhead',CZ='C*Bhead+2c+rho/2',extra_cross='32CZ*aD/Jcut'),scope='Pending new full proof/code review; nested powers unexpanded')

def construct(raw,t,max_core_steps=100000):
 t=rat(t)
 if t<=1:raise ValueError('t>1')
 if type(max_core_steps)is not int or max_core_steps<0:raise ValueError('exact nonnegative loop budget')
 q=qualitative(raw)
 if q['status']=='UNKNOWN':return q
 r=parse(raw);p=plan(r,t,max_core_steps)
 if p['status']=='UNKNOWN_CORE_PROFILE_BUDGET':return dict(status=p['status'],qualitative=q,required_core_steps=p['required'],max_core_steps=max_core_steps)
 out=dict(family=q['family'],raw_sha256=r['raw_sha256'],t=t,qualitative=q,plan=p,work=dict(core_backward_steps=p['core_profile']['K']-1,compensation_steps=p['core']['J0']-1,additional_core_scan_points=4*p['core_profile']['K'],core_head_copies=p['core_profile']['K'],mass_head_unrolled_steps=0,mass_head_powers_expanded=0,outer_head_powers_expanded=0),scope='Trusted exact constructor and nested expressions; independent whole review pending; no practical numeric moment bound')
 if r['free']:out.update(status='PENDING_NESTED_SYMBOLIC_FOSTER',mass_head=head(p,r))
 else:out.update(status='PENDING_CORE_ONLY_FOSTER',head=p['core_only_head'],zeta=p['core']['zeta0'],H=p['core']['H0'])
 out['formulas']=dict(W='t^N * scaled_value',Foster_constant='(zeta+lambda+mu*Nstar+S*Nstar^2)*H*t^(Nstar+1)',stationary_bound='pi(t^N)<=2*Foster_constant/zeta',expression_interface='certificate_expressions(raw,received_certificate): explicit finite rational arithmetic DAG');out['work']['largest_retained_scalar_bits']=bits(out);return out

def receive(raw,t,receipt,**kw):return canonical(construct(raw,t,**kw))==canonical(receipt)
def coords(r,x):return I.coords(r,x)
def core(r,c,x):
 N,a,f,u,j,R=coords(r,x);p=c['plan'];co=p['core'];return P.g(p['core_profile'],R)+co['rho0']*F(a,(R+1)**2)-co['e']*F(a,N+1)
def mass(r,c,x):
 _,a,_,_,j,_=coords(r,x);g=I.evaluate(I.mass_g(c,j));assert isinstance(g,F),'mass-power budget refused';return g-1+c['plan']['mass']['rho']*F(a,(j+1)**2)
def scaled(r,c,x):
 hc=core(r,c,x)
 if c['status']=='PENDING_CORE_ONLY_FOSTER':return hc
 _,a,f,u,j,R=coords(r,x);h=c['mass_head'];num=P.dyadic(f+1)-P.dyadic(u+1)-h['L0']
 if num<=0:return hc
 assert h['K']*P.logceil(h['Q'])+1<=(f+1).bit_length()
 bh=h['Q']**h['K'];phi=min(F(1),num/(h['Jcoef']*bh));g=1+c['plan']['mass']['c']/j if j>=h['K']else h['C']*h['q']**(h['K']-j)-h['d']
 return hc+c['plan']['mass']['eta']*phi*(g-1+c['plan']['mass']['rho']*F(a,(j+1)**2))
def drift(r,c,x,fn=None,selection=lambda u,v:True):
 if fn is None:fn=lambda y:scaled(r,c,y)
 old=fn(x);return sum((rate*(c['t']**(sum(v)-sum(u))*fn(y)-old)for u,v,rate,y in P.enabled(r,x)if selection(u,v)),F(0))
def outside(c,N):
 if type(N)is not int or N<0:raise ValueError('nonnegative exact count')
 return N>=c['head']if c['status']=='PENDING_CORE_ONLY_FOSTER'else I.outside_head(c,N)

def dag(raw,c):
 r=parse(raw)
 if r['raw_sha256']!=c['raw_sha256']:raise ValueError('raw binding')
 nodes=[]
 def q(x):
  x=rat(x);nodes.append(['q',x.numerator,x.denominator]);return len(nodes)-1
 def op(name,*refs):nodes.append([name,*refs]);return len(nodes)-1
 out={}
 if c['status']=='PENDING_CORE_ONLY_FOSTER':ns=q(c['head']);H=q(c['H']);zeta=q(c['zeta'])
 else:
  h=c['mass_head'];bh=op('pow',q(h['Q']),q(h['K']));ex=op('add',q(h['L0']+1),op('mul',q(h['Jcoef']),bh));U=op('mul',q(2),op('add',q(1),op('pow',q(2),ex)));a,b,d=h['outer_head_coefficients']
  ns=op('ceil',op('add',q(1),op('mul',q(a),U),op('mul',q(b),op('pow',U,q(2))),op('mul',q(d),op('pow',U,q(4)))))
  H=op('add',q(h['H_coefficients'][0]),op('mul',q(h['H_coefficients'][1]),bh));zeta=op('div',q(h['nu']),op('mul',q(2),H));out.update(Bhead=bh,cutoff_exponent=ex,Ucut=U)
 cf=op('mul',op('add',zeta,q(r['lam']),op('mul',q(r['mu']),ns),op('mul',q(r['S']),op('pow',ns,q(2)))),H,op('pow',q(c['t']),op('add',ns,q(1))))
 bound=op('div',op('mul',q(2),cf),zeta);out.update(Nstar=ns,H=H,zeta=zeta,Foster_constant=cf,stationary_bound=bound)
 return dict(format='exact-rational-dag-v1',raw_sha256=r['raw_sha256'],nodes=nodes,outputs=out)
def evaluate(d,name,budget=100000):
 if type(d)is not dict or d.get('format')!='exact-rational-dag-v1':raise ValueError('DAG format')
 ns=d.get('nodes');outs=d.get('outputs');tree=[];arities={'add':None,'mul':None,'pow':2,'div':2,'ceil':1}
 if type(ns)is not list or type(outs)is not dict or name not in outs:raise ValueError('DAG output')
 for i,n in enumerate(ns):
  if type(n)is not list or not n or type(n[0])is not str:raise ValueError('node')
  op,*refs=n
  if op=='q':
   if len(refs)!=2 or any(type(x)is not int for x in refs)or refs[1]<=0:raise ValueError('rational leaf')
   tree.append(F(*refs));continue
  if op not in arities or (arities[op]is not None and len(refs)!=arities[op])or not refs:raise ValueError('arity')
  if any(type(j)is not int or not 0<=j<i for j in refs):raise ValueError('acyclic refs')
  tree.append((op,*(tree[j]for j in refs)))
 if any(type(i)is not int or not 0<=i<len(ns)for i in outs.values()):raise ValueError('output reference')
 return I.evaluate(tree[outs[name]],budget)
