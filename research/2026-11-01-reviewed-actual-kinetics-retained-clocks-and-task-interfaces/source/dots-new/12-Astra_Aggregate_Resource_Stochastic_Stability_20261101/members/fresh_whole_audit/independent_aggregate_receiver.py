"""Independent aggregate raw acquisition, constants, receipt and nested arithmetic.
No author-module import. The retained older independent architecture/profile and
cover primitives are explicit capital, NOT one-hub acceptance for this theorem.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent/'retained_independent'))
import independent_glue_receiver as P
rat,ceil,canonical,digest,bits=P.rat,P.ceil,P.canonical,P.digest,P.bits
FAMILY='aggregate-free-mass-dyadic-glue-v1'

def parse(raw):
 r=P.architecture(raw);used=set().union(*(set(e)for e in r['edges']))
 fs=tuple(v for v in r['satellites']if v not in used)
 if not fs:raise P.Outside('requires a nonempty acquired set of isolated hub-graph vertices')
 rare=tuple(v for v in r['satellites']if v in used);keep=tuple(v for v in range(r['n'])if v not in fs)
 core=[]
 for u,v,k in r['channels']:
  if all(u[f]==v[f]==0 for f in fs):core.append((tuple(u[i]for i in keep),tuple(v[i]for i in keep),k))
 cr=P.B.parse(core);kx=dict(r['kX'])
 r.update(free=fs,rare=rare,kfree=min(kx[f]for f in fs),ell=max(sum((rate for x,_,rate in h['arms']if x in fs),F(0))for h in r['hubs']),krminus=min(kx[v]for v in rare),krplus=max(kx[v]for v in rare),inventory=P.C.compile_inventory(dict(satellites=rare,edges=r['edges'])),core_raw_sha256=cr['raw_sha256'])
 return r

def qualitative(raw):
 try:r=parse(raw)
 except P.Outside as e:return dict(status='UNKNOWN',family=FAMILY,reason=str(e),stability='UNKNOWN')
 return dict(status='QUALITATIVE_ARGUMENT_ACQUIRED_PENDING_WHOLE_REVIEW',family=FAMILY,raw_sha256=r['raw_sha256'],core_raw_sha256=r['core_raw_sha256'],open_coordinate=r['a'],free_coordinates=r['free'],rare_coordinates=r['rare'],inventory=r['inventory'],conclusion='irreducible positive recurrence and every finite exponential stationary total-count moment for the stated raw class; pending independent review',stationary_fiber_laws=0,profile_steps=0)

def plan(r,t,cap=100000):
 t=rat(t)
 if t<=1:raise ValueError('t>1')
 if type(cap)is not int or cap<0:raise ValueError('nonnegative exact loop cap')
 lam,mu=r['lam'],r['mu'];E=len(r['edges']);d=len(r['rare']);D=mu*(1-1/t);L=lam*(t-1)
 prof=P.shape(lam,t,r['bmin']/(16*E));Kf=r['a_sum']+d*r['krplus']
 J0=max(2,prof['K']+1,ceil(4*prof['c']*(mu+Kf+prof['beta'])/D));steps=prof['K']+J0-2
 if steps>cap:return dict(status='UNKNOWN_CORE_PROFILE_BUDGET',required=steps)
 prof=P.acquire_profile(prof,lam,t);g=lambda j:P.g(prof,j);slope=lambda j:g(j)-g(j+1)
 rho0=min(F(1),r['bmin']*prof['dlow']/(88*r['smax']),prof['eps']/(44*(Kf+lam*t)))
 e=min(F(1,4),D/(4*(r['F0']+D)),prof['eps']/(4*mu));CA=L+11*mu
 Qhead=F(0)
 for j in range(1,J0):
  cost=mu*(g(j-1)/t-g(j))+Kf*j*slope(j-1)+2*prof['beta']*j*slope(j)+e*(r['F0']+D)
  Qhead=max(Qhead,(j+1)**2*max(cost,0))
 C0=1+L*g(0)+(Kf+r['smax']*E)*prof['D1']+mu*prof['D1']/4+11*rho0*(Kf+r['smax']*E+lam*t)+rho0*CA/4+e*mu
 H0=g(0)+rho0/4;zeta0=min(prof['eps'],lam)/4
 delta=min(F(1,2*(d+1)),F(1,2*E),r['bmin']/(8*E*r['smax']*prof['Gratio']))
 U0=ceil(max(F(1),4*CA/r['krminus'],4*Qhead/(rho0*r['krminus'])))
 c=F(1);rho=min(c,r['bmin']/(4*r['smax']));B=2*L+rho*L/2+rho*lam*t
 m=min(r['bmin']*delta*delta/(288*E),rho*r['kfree']*delta/36);cfree=min(lam/2,m/2);eta=(C0+1)/cfree
 K=ceil(max(F(2),2*t/(t-1),4*B/m,F(2*U0),8*eta*B/zeta0))
 return dict(status='ACQUIRED_TAIL_AND_HEAD_PLAN',t=t,core_profile=prof,core=dict(D=D,L=L,Kf=Kf,J0=J0,rho0=rho0,e=e,CA=CA,Qhead=Qhead,C0=C0,H0=H0,zeta0=zeta0,delta=delta,U0=U0),mass=dict(c=c,rho=rho,B=B,m=m,cfree=cfree,eta=eta,K=K),core_profile_steps=steps)

def head(p,r):
 co=p['core'];m=p['mass'];K=m['K'];t=p['t'];q=4*t;Q=ceil(q);rho=m['rho'];c=m['c'];d=q*(rho+c)/(q-1);C=1+c/K+d;nu=min(F(1),co['zeta0']/2)
 db=min(F(1,4),rho*r['kfree']/(4*(9*C*(r['a_sum']+r['krplus']+r['mu']/t)+4*rho*r['mu']+1)))
 E=len(r['edges']);Jcoef=max(1,ceil(8*m['eta']*(r['ell']*E+r['mu'])*(C+2*c+rho/2)/nu));du=co['delta']
 ku=min(co['D']*du/4,co['e']*r['b0']*du**2/(32*E));pr=p['core_profile']
 coeff=(max(F(1),F(pr['K'])/du,4*co['CA']/r['krminus'],4*co['Qhead']/(co['rho0']*r['krminus'])),(2*co['L']+2*r['mu']+co['rho0']*(11*r['lam']*t+co['CA'])+1)/ku,(2*pr['c']+11*co['rho0'])*r['S']/(du**2*ku))
 return dict(status='PENDING_FACTORED_MASS_GLUE',outer_head_coefficients=coeff,H_coefficients=(co['H0']+m['eta']*rho/4,m['eta']*C),K=K,q=q,Q=Q,d=d,C=C,nu=nu,delta_base=db,L0=P.logceil(4/db)+K*P.logceil(Q),Jcoef=Jcoef,expressions=dict(Bhead='Q^K',deltaF='delta_base/Bhead',Jcut='Jcoef*Bhead',CZ='C*Bhead+2c+rho/2',D2='9C*Bhead',Cdeath='9mu*C*Bhead/t+4rho*mu',cutoff_exponent='L0+Jcoef*Q^K+1'),cost_scope='Nested exact powers; no expanded new head, global numerical cutoff or stationary moment bound')

def construct(raw,t,max_core_steps=100000):
 t=rat(t)
 if t<=1:raise ValueError('t>1')
 if type(max_core_steps)is not int or max_core_steps<0:raise ValueError('nonnegative exact loop cap')
 q=qualitative(raw)
 if q['status']=='UNKNOWN':return q
 r=parse(raw);p=plan(r,t,max_core_steps)
 if p['status']=='UNKNOWN_CORE_PROFILE_BUDGET':return dict(status=p['status'],family=FAMILY,qualitative=q,required_core_steps=p['required'],max_core_steps=max_core_steps)
 h=head(p,r)
 out=dict(status='SYMBOLIC_FOSTER_ARGUMENT_ACQUIRED_PENDING_WHOLE_REVIEW',family=FAMILY,raw_sha256=r['raw_sha256'],t=t,qualitative=q,plan=p,mass_head=h,formulas=dict(Bhead='Q^K',H='H_coefficients[0]+H_coefficients[1]*Bhead',zeta='nu/(2H)',outer_U='2*(2^(L0+Jcoef*Bhead+1)+1)',Nstar='ceil(A1*outer_U+A2*outer_U^2+A4*outer_U^4+1)',Foster_constant='(zeta+lambda+mu*Nstar+S*Nstar^2)*H*t^(Nstar+1)',stationary_bound='pi(t^N)<=2*Foster_constant/zeta'),work=dict(core_backward_steps=p['core_profile']['K']-1,core_compensation_steps=p['core']['J0']-1,additional_core_profile_scan_points=4*p['core_profile']['K'],core_head_copies=p['core_profile']['K'],new_mass_head_unrolled_steps=0,expanded_mass_head_powers=0,expanded_outer_head=0,stationary_fiber_laws=0),cost_scope='Exact nested factored expression; no complete numerical-polynomial or practical stationary-tail claim. Core-loop budget excludes other scans, rational arithmetic, serialization and requested power expansions.')
 out['work']['largest_retained_scalar_bits']=bits(out);return out

def receive(raw,t,receipt,**kw):return canonical(construct(raw,t,**kw))==canonical(receipt)

# Arithmetic DAG is JSON-serializable, exact and executable, not only display text.
# Rational leaves are Fraction; all non-leaf nodes are (operator, operands...).
def add(*xs):
 total=sum((x for x in xs if isinstance(x,(int,F))),F(0));rest=tuple(x for x in xs if not isinstance(x,(int,F)))
 if total:rest+=(total,)
 return F(0)if not rest else rest[0]if len(rest)==1 else ('add',*rest)
def mul(*xs):
 if any(x==0 for x in xs):return F(0)
 prod=F(1);rest=[]
 for x in xs:
  if isinstance(x,(int,F)):prod*=x
  else:rest.append(x)
 if prod!=1:rest.append(prod)
 return prod if not rest else rest[0]if len(rest)==1 else ('mul',*rest)
def power(b,e):
 if e==0:return F(1)
 if b==1:return F(1)
 return ('pow',F(b),e)
def quotient(a,b):return F(a)/b if isinstance(a,(int,F))and isinstance(b,(int,F))else ('div',a,b)
class Budget(Exception):pass
def evaluate(expr,max_power_bits=100000):
 if type(max_power_bits)is not int or max_power_bits<0:raise ValueError('nonnegative exact budget')
 def ev(x):
  if isinstance(x,(int,F)):return F(x)
  op,*args=x
  if op=='pow':
   b=ev(args[0]);e=ev(args[1]);assert e.denominator==1 and e>=0;e=int(e)
   bound=e*max(abs(b.numerator).bit_length(),b.denominator.bit_length())+1
   if bound>max_power_bits:raise Budget((bound,max_power_bits))
   return b**e
  z=[ev(v)for v in args]
  if op=='add':return sum(z,F(0))
  if op=='mul':
   out=F(1)
   for v in z:out*=v
   return out
  if op=='div':return z[0]/z[1]
  if op=='ceil':return F(ceil(z[0]))
  raise ValueError(op)
 try:return ev(expr)
 except Budget as e:return dict(status='UNKNOWN_POWER_INTERMEDIATE_BUDGET',required_upper_power_bits=e.args[0][0],budget=max_power_bits,symbolic_expression_retained=True)

def pow_leq(b,e,bound):
 """Decide integer b**e <= rational bound without exceeding bound-sized ints."""
 assert type(b)is int and b>=2 and type(e)is int and e>=0
 cap=bound.numerator//bound.denominator if isinstance(bound,F)else bound
 if cap<1:return False
 if e>=cap.bit_length():return False # b>=2
 acc=1
 while e:
  if e&1:
   if acc>cap//b:return False
   acc*=b
  e//=2
  if e:b=min(cap+1,b*b)
 return acc<=cap

def expressions(r,c):
 h=c['mass_head'];bh=power(h['Q'],h['K']);E=add(h['L0']+1,mul(h['Jcoef'],bh));U=mul(2,add(1,power(2,E)))
 a,b,d=h['outer_head_coefficients'];ns=('ceil',add(1,mul(a,U),mul(b,power_expr(U,2)),mul(d,power_expr(U,4))))
 H=add(h['H_coefficients'][0],mul(h['H_coefficients'][1],bh));z=quotient(h['nu'],mul(2,H))
 cf=mul(add(z,r['lam'],mul(r['mu'],ns),mul(r['S'],power_expr(ns,2))),H,power(c['t'],add(ns,1)))
 return dict(Bhead=bh,cutoff_exponent=E,Ucut=U,Nstar=ns,H=H,zeta=z,Foster_constant=cf,stationary_bound=quotient(mul(2,cf),z))
def power_expr(b,e):return ('pow',b,F(e))

def outside_head(c,N):
 if type(N)is not int or N<0:raise ValueError('nonnegative exact total')
 h=c['mass_head'];limit=N.bit_length()-h['L0']-2
 if limit<0 or not pow_leq(h['Q'],h['K'],F(limit,h['Jcoef'])):return False
 # Here Bhead and cutoff exponent are bounded by the supplied state's bit length.
 exponent=h['L0']+1+h['Jcoef']*h['Q']**h['K'];U=2*((1<<exponent)+1)
 a,b,d=h['outer_head_coefficients'];threshold=ceil(1+a*U+b*U**2+d*U**4)
 return N>=threshold

def coords(r,x):
 if type(x)not in (list,tuple)or len(x)!=r['n']or any(type(v)is not int or v<0 for v in x):raise ValueError('nonnegative exact state')
 N=sum(x);a=x[r['a']];f=sum(x[i]for i in r['free']);u=N-f;R=a+P.C.cover_weight(r['inventory'],x)
 return N,a,f,u,u+a,R

def mass_g(c,j):
 if type(j)is not int or j<0:raise ValueError('nonnegative exact resource')
 p,h=c['plan'],c['mass_head'];K=p['mass']['K']
 return 1+p['mass']['c']/j if j>=K else add(mul(h['C'],power(h['q'],K-j)),-h['d'])

def pieces(r,c,x):
 N,a,f,u,j,R=coords(r,x);p,h=c['plan'],c['mass_head'];co=p['core']
 hc=P.g(p['core_profile'],R)+co['rho0']*F(a,(R+1)**2)-co['e']*F(a,N+1)
 numerator=P.dyadic(f+1)-P.dyadic(u+1)-h['L0']
 if numerator<=0:return hc,F(0),F(0) # exact zero-product shortcut, no g_J evaluation
 bh=power(h['Q'],h['K']);phi=F(1)if pow_leq(h['Q'],h['K'],numerator/h['Jcoef'])else quotient(numerator,mul(h['Jcoef'],bh))
 z=add(mass_g(c,j),-1,p['mass']['rho']*F(a,(j+1)**2))
 return hc,z,phi

def hvalue(r,c,x):
 hc,z,phi=pieces(r,c,x);return add(hc,mul(c['plan']['mass']['eta'],phi,z))
def scaled_drift(r,c,x):
 old=hvalue(r,c,x);terms=[]
 for src,dst,rate,y in P.enabled(r,x):terms.append(mul(rate,add(mul(c['t']**(sum(dst)-sum(src)),hvalue(r,c,y)),mul(-1,old))))
 return add(*terms)

def decode_expression(node):
 """Decode only an arithmetic AST wire value; raw rates still reject strings."""
 if type(node)is int:return F(node)
 if type(node)is str:return F(node)
 if type(node)not in (list,tuple)or not node:raise ValueError('arithmetic expression')
 op=node[0];arity={'div':2,'pow':2,'ceil':1}
 if op not in ('add','mul','div','pow','ceil'):raise ValueError('arithmetic operator')
 if op in arity and len(node)!=arity[op]+1:raise ValueError('arithmetic arity')
 if op in ('add','mul')and len(node)<2:raise ValueError('nonempty arithmetic node')
 return (op,*(decode_expression(arg)for arg in node[1:]))

def receive_expression_bundle(raw,t,wire_bundle,**budget):
 """Reacquire the exact main nested semantics before accepting a JSON AST."""
 c=construct(raw,t,**budget)
 if c['status']!='SYMBOLIC_FOSTER_ARGUMENT_ACQUIRED_PENDING_WHOLE_REVIEW':return False
 return canonical(expressions(parse(raw),c))==canonical(wire_bundle)
