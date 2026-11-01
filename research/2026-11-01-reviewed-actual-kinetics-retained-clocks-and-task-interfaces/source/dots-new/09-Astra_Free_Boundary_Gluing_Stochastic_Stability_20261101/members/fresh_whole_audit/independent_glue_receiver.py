"""Independent receiver of new glue semantics; no candidate imports.
Retained separately authored raw/circuit primitives are local, hash-bound capital.
Numerical construction and physical-generator evaluator below are new.
"""
from fractions import Fraction as Q
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'prior_independent'))
import independent_cover_receiver as B
import independent_circuit_receiver as C
FAMILY='single-free-port-dyadic-glue-v1'
rat,ceil,wire,canonical,digest,bits=B.rational,B.ceiling,B.wire,B.canonical,B.digest,B.maxbits
Outside=B.Outside

def architecture(raw):
 if type(raw) not in (tuple,list) or not raw:raise ValueError('nonempty raw list')
 table={};n=None;checks=0
 for row in raw:
  if type(row) not in (tuple,list) or len(row)!=3:raise ValueError('reaction triple')
  u,v,k=row
  if type(u) not in (tuple,list) or type(v) not in (tuple,list):raise TypeError('complex vectors')
  if n is None:n=len(u)
  if n<3 or len(u)!=n or len(v)!=n:raise ValueError('fixed dimension n>=3')
  for q in (*u,*v):
   checks+=1
   if type(q)is not int or q<0:raise ValueError('nonnegative exact integer counts')
  k=rat(k)
  if k<=0:raise ValueError('strictly positive rate')
  u,v=tuple(u),tuple(v)
  if u!=v:
   key=u,v;table[key]=table.get(key,Q(0))+k
 ch=tuple((u,v,k)for (u,v),k in sorted(table.items()));zero=(0,)*n
 noncon={(u,v)for u,v,k in ch if sum(u)!=sum(v)};ports=[]
 for i in range(n):
  one=tuple(int(j==i)for j in range(n))
  if noncon=={(zero,one),(one,zero)}:ports.append(i)
 if len(ports)!=1:raise Outside('requires one exact reversible port')
 a=ports[0];one=tuple(int(i==a)for i in range(n));aa=tuple(2*q for q in one)
 internal=tuple(z for z in ch if sum(z[0])==sum(z[1]));hubs={}
 for u,v,k in internal:
  for z in (u,v):
   if sum(z)!=2:raise Outside('only binary nonnull internals')
   occupied=tuple(i for i,q in enumerate(z)if q)
   if not z[a]:
    if len(occupied)!=2 or any(z[i]!=1 for i in occupied):raise Outside('hub must be square-free satellite pair')
    hubs[z]=occupied
   elif z!=aa:
    if z[a]!=1 or len(occupied)!=2:raise Outside('unrecognized active complex')
 if not hubs:raise Outside('at least one hub required')
 for u,v,k in internal:
  if (u in hubs)==(v in hubs):raise Outside('only hub/active edges')
  if (v,u)not in table:raise Outside('every included edge must be reversible')
 sats=tuple(i for i in range(n)if i!=a);kx={i:Q(0)for i in sats};rows=[]
 for h,edge in sorted(hubs.items()):
  if (aa,h)not in table or (h,aa)not in table:raise Outside('every hub needs 2A amplification pair')
  arms=[]
  for x in sats:
   ax=tuple(int(i==a)+int(i==x)for i in range(n))
   if (ax,h)in table:kx[x]+=table[ax,h];arms.append((x,table[ax,h],table[h,ax]))
  rows.append(dict(complex=h,edge=edge,to_hub=table[aa,h],to_two_a=table[h,aa],reverse_sum=table[h,aa]+sum((r for x,f,r in arms),Q(0)),arms=tuple(arms)))
 if min(kx.values())<=0:raise Outside('each satellite needs a forward/reverse arm')
 asum=sum((h['to_hub']for h in rows),Q(0))
 return dict(n=n,a=a,lam=table[zero,one],mu=table[one,zero],channels=ch,internal=internal,satellites=sats,edges=tuple(sorted(hubs.values())),hubs=tuple(rows),kX=tuple(kx.items()),kminus=min(kx.values()),kplus=max(kx.values()),a_sum=asum,bmin=min(h['to_two_a']for h in rows),smax=max(h['reverse_sum']for h in rows),b0=min(h['reverse_sum']+h['to_two_a']for h in rows),F0=2*asum+max(kx.values()),S=sum((k for u,v,k in internal),Q(0)),raw_sha256=digest(ch),work=dict(input_rows=len(raw),normalized_channels=len(ch),raw_coordinate_checks=checks,internal_complex_checks=2*len(internal),reverse_edge_tests=len(internal),amplification_edge_tests=2*len(rows),arm_incidence_tests=len(rows)*len(sats)))

def parse(raw):
 r=architecture(raw);incident={v for edge in r['edges']for v in edge};trials=[]
 for f in r['satellites']:
  if f in incident:continue
  arms=[(h,arm)for h in r['hubs']for arm in h['arms']if arm[0]==f]
  if len(arms)!=1:trials.append((f,'free species needs exactly one arm hub'));continue
  core=[(u[:f]+u[f+1:],v[:f]+v[f+1:],k)for u,v,k in r['channels']if not u[f] and not v[f]]
  try:core_r=B.parse(core)
  except Outside as exc:trials.append((f,str(exc)));continue
  h,(_,kf,ell)=arms[0];rare=tuple(v for v in r['satellites']if v!=f);kx=dict(r['kX'])
  r.update(f=f,rare=rare,h0=h['edge'],b_h0=h['to_two_a'],kF=kf,ellF=ell,krminus=min(kx[v]for v in rare),krplus=max(kx[v]for v in rare),inventory=C.compile_inventory(dict(satellites=rare,edges=r['edges'])),core_raw_sha256=core_r['raw_sha256'],free_role_trials=tuple(trials+[(f,'accepted')]))
  return r
 raise Outside('no isolated unique-arm satellite with a recognized dominating-cover raw core: '+str(trials))

def qual(r):
 return dict(status='CERTIFIED_QUALITATIVE',family=FAMILY,raw_sha256=r['raw_sha256'],conclusion='irreducible positive recurrence; every finite exponential stationary total-count moment',roles=dict(open_coordinate=r['a'],free_coordinate=r['f'],capture_hub=r['h0'],rare=r['rare']),core_inventory=r['inventory'],core_raw_sha256=r['core_raw_sha256'],free_role_trials=r['free_role_trials'],work=dict(raw=r['work'],profile_steps=0,expanded_head_bits=0,states_enumerated=0,stationary_fiber_laws=0),assurance='Ordinary proof supplied; independent whole-review status governed by the package manifest')
def qualitative(raw):
 try:return qual(parse(raw))
 except Outside as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')
def shape(lam,t,beta):
 L=lam*(t-1);eps=min(Q(1),(lam+beta)/2);c=4*(L+eps)/beta
 return dict(beta=beta,L=L,eps=eps,c=c,K=max(2,ceil(2*c)))
def g(p,r):return p['head'][r]if r<p['K']else 1+p['c']/r
def acquire_profile(p,lam,t):
 p=p.copy();K=p['K'];seq=[None]*(K+1);seq[K]=1+p['c']/K
 for j in reversed(range(1,K)):
  den=lam+p['beta']*j*j-p['eps'];assert den>0
  seq[j]=seq[j+1]*(lam*t+p['beta']*j*j)/den
 seq[0]=2*t*seq[1];p['head']=tuple(seq[:-1]);d=lambda j:g(p,j)-g(p,j+1)
 p['dlow']=min(p['c'],min((j+1)**2*d(j)for j in range(1,K)))
 p['Gratio']=max(Q(3),max(d(j-1)/d(j)for j in range(1,K+1)))
 p['D1']=max(4*p['c'],max((j+1)**2*d(j-1)for j in range(1,K+1)))
 p['D2']=max(8*p['c'],max((j+1)**2*(g(p,max(0,j-2))-g(p,j))for j in range(1,K+2)))
 return p

def logceil(q):
 q=rat(q)
 if q<=0:raise ValueError('positive rational logarithmic bound')
 n,d=q.numerator,q.denominator;k=n.bit_length()-d.bit_length()
 lower=Q(1<<k)if k>=0 else Q(1,1<<(-k))
 return k+int(q>lower)
def dyadic(z):
 if type(z)is not int or z<1:raise ValueError('positive exact integer dyadic input')
 k=z.bit_length()-1
 return Q(z,1<<k)+k-1

def construct(raw,t,max_profile_steps=100000):
 t=rat(t)
 if t<=1:raise ValueError('t>1')
 if type(max_profile_steps)is not int or max_profile_steps<0:raise ValueError('nonnegative exact loop budget')
 try:r=parse(raw)
 except Outside as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')
 lam,mu=r['lam'],r['mu'];d=len(r['rare']);E=len(r['edges']);L=lam*(t-1);D=mu*(1-1/t)
 p=shape(lam,t,r['bmin']/(16*E));f=shape(lam,t,r['b_h0']/2);Kf=r['a_sum']+d*r['krplus'];J0=max(2,p['K']+1,ceil(4*p['c']*(mu+Kf+p['beta'])/D));steps=p['K']+f['K']+J0-3
 if steps>max_profile_steps:return dict(status='UNKNOWN_PROFILE_BUDGET',family=FAMILY,qualitative=qual(r),required_profile_steps=steps,max_profile_steps=max_profile_steps)
 p=acquire_profile(p,lam,t);f=acquire_profile(f,lam,t);gp=lambda j:g(p,j);dp=lambda j:gp(j)-gp(j+1);gf=lambda j:g(f,j);df=lambda j:gf(j)-gf(j+1)
 rho0=min(Q(1),r['bmin']*p['dlow']/(88*r['smax']),p['eps']/(44*(Kf+lam*t)))
 e=min(Q(1,4),D/(4*(r['F0']+D)),p['eps']/(4*mu));CA=L+11*mu
 Qhead=Q(0)
 for j in range(1,J0):Qhead=max(Qhead,(j+1)**2*max(Q(0),mu*(gp(j-1)/t-gp(j))+Kf*j*dp(j-1)+2*p['beta']*j*dp(j)+e*(r['F0']+D)))
 C0=1+L*gp(0)+(Kf+r['smax']*E)*p['D1']+mu*p['D1']/4+11*rho0*(Kf+r['smax']*E+lam*t)+rho0*CA/4+e*mu
 H0=gp(0)+rho0/4;zeta0=min(p['eps'],lam)/4
 rhof=min(Q(1),r['bmin']*f['dlow']/(4*r['smax']),f['eps']/(44*lam*t));Cfor=(r['a_sum']+r['krplus'])*(f['D2']+20*rhof)
 Tr=f['c']*(mu+2*f['beta'])
 for j in range(1,f['K']+1):Tr=max(Tr,(j+1)*max(Q(0),mu*(gf(j-1)/t-gf(j))+2*f['beta']*j*df(j)+D))
 T=Tr+rhof*CA;deltaF=min(Q(1,4),rhof*r['kF']/(4*Cfor),rhof*r['kF']/(4*T));cfree=min(f['eps']/2,lam*gf(0)/4)
 CZ=max([2*f['c']+rhof]+[(j+1)*(gf(j)-1+rhof*Q(j,(j+1)**2))for j in range(f['K'])]);Ccross=4*CZ*(r['ellF']+mu);eta=(C0+1)/cfree;L0=max(0,logceil(4/deltaF));Jcut=max(1,ceil(4*eta*Ccross/zeta0));exponent=L0+Jcut+1
 du=min(Q(1,2*(d+1)),Q(1,2*E),r['bmin']/(8*E*r['smax']*p['Gratio']));ku=min(D*du/4,e*r['b0']*du**2/(32*E))
 A1=max(Q(1),Q(p['K'])/du,4*CA/r['krminus'],4*Qhead/(rho0*r['krminus']));A2=(2*L+2*mu+rho0*(11*lam*t+CA)+1)/ku;A4=(2*p['c']+11*rho0)*r['S']/(du**2*ku)
 H=H0+eta*(gf(0)-1+rhof/4);zeta=zeta0/(2*H)
 co=dict(D=D,L=L,Kf=Kf,J0=J0,rho0=rho0,e=e,CA=CA,Qhead=Qhead,C0=C0,H0=H0,zeta0=zeta0,rhof=rhof,Cfor=Cfor,Tr=Tr,T=T,deltaF=deltaF,cfree=cfree,CZ=CZ,Ccross=Ccross,eta=eta,L0=L0,Jcut=Jcut,delta_unit=du,kappa_unit=ku,H=H,zeta=zeta)
 out=dict(status='CERTIFIED_SYMBOLIC_FOSTER',family=FAMILY,raw_sha256=r['raw_sha256'],t=t,qualitative=qual(r),core_profile=p,free_profile=f,constants=co,symbolic_head=dict(exponent=exponent,coefficients=(A1,A2,A4),formula='U=2*(2^exponent+1); Nstar=ceil(A1*U+A2*U^2+A4*U^4+1)'),Foster=dict(formula='CF=(zeta+lambda+mu*Nstar+S*Nstar^2)*H*t^(Nstar+1); LW<=-zeta*W+CF*1_{N<Nstar}',stationary_moment='pi(t^N)<=2*CF/zeta'),work=dict(profile_steps=steps,additional_profile_formula_scan_points=4*p['K']+6*f['K'],head_value_copies=p['K']+f['K'],budget_scope='Only backward and compensation loops; additional formula scans, copies, arithmetic, raw scans and serialization charged separately',expanded_head_bits=0,expanded_Foster_powers=0,states_enumerated=0,stationary_fiber_laws=0),cost_scope='Exact W and factored algebraic head; numeric head expansion separate. No complete numerical polynomial claim; independent whole review pending.')
 out['work']['retained_scalar_bits']=bits(out);return out

def coordinates(r,x):
 N=sum(x);A=x[r['a']];f=x[r['f']];R=A+C.cover_weight(r['inventory'],x);P=A+min(x[v]for v in r['h0'])
 return N,A,f,N-f,R,P
def pieces(r,c,x):
 N,A,f,U,R,P=coordinates(r,x);co=c['constants']
 core=g(c['core_profile'],R)+co['rho0']*Q(A,(R+1)**2)-co['e']*Q(A,N+1)
 pair=g(c['free_profile'],P)-1+co['rhof']*Q(A,(P+1)**2)
 phi=min(Q(1),max(Q(0),(dyadic(f+1)-dyadic(U+1)-co['L0'])/co['Jcut']))
 return core,pair,phi

def enabled(r,x):
 for u,v,k in r['channels']:
  rate=k
  for z,need in zip(x,u):
   for j in range(need):rate*=max(0,z-j)
  if rate:yield u,v,rate,tuple(z-need+new for z,need,new in zip(x,u,v))
def drift(r,c,x):
 h,z,p=pieces(r,c,x);lh=lz=cross=direct=Q(0);eta=c['constants']['eta']
 for u,v,rate,y in enabled(r,x):
  nh,nz,np=pieces(r,c,y);tilt=c['t']**(sum(v)-sum(u))
  lh+=rate*(tilt*nh-h);lz+=rate*(tilt*nz-z);cross+=rate*tilt*nz*(np-p)
  direct+=rate*(tilt*(nh+eta*np*nz)-(h+eta*p*z))
 assert direct==lh+eta*(p*lz+cross)
 return lh,lz,cross,direct

def expand_head(c,max_power_bits):
 if type(max_power_bits)is not int or max_power_bits<0:raise ValueError('nonnegative exact power-bit expansion budget')
 sh=c['symbolic_head'];e=sh['exponent']
 if e+1>max_power_bits:return dict(status='UNKNOWN_POWER_EXPANSION_BUDGET',required_power_bits=e+1,max_power_bits=max_power_bits,symbolic_certificate_retained=True,scope='Only the power-of-two intermediate is capped, not total head output bits or arithmetic work')
 u=2*((1<<e)+1);a,b,d=sh['coefficients'];return ceil(1+u*(a+u*(b+u*u*d)))
def outside_head(c,N):
 if type(N)is not int or N<0:raise ValueError('nonnegative integer total')
 if N.bit_length()<=c['symbolic_head']['exponent']+1:return False
 return N>=expand_head(c,N.bit_length())
def receive_qualitative(raw,receipt):return canonical(qualitative(raw))==canonical(receipt)
def receive_symbolic(raw,t,receipt,**budget):return canonical(construct(raw,t,**budget))==canonical(receipt)
