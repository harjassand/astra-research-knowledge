#!/usr/bin/env python3
"""Trusted exact free-port glue constructor; independent whole review pending.
Graph and pointwise dyadic circuit acquired; enormous head retained symbolically.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent/'frozen_core'))
import cover_circuit as C
rat,ceilq,encode,canonical,digest,bits=C.rat,C.ceilq,C.encode,C.canonical,C.digest,C.bits
Unsupported=C.B.Unsupported
FAMILY='single-free-port-dyadic-glue-v1'
def architecture(raw):
    if type(raw) not in (list,tuple) or not raw:raise ValueError('nonempty raw list')
    n=None;rates={};coordinate_checks=0
    for row in raw:
        if type(row) not in (list,tuple) or len(row)!=3:raise ValueError('reaction triple')
        u,v,k=row
        if type(u) not in (list,tuple) or type(v) not in (list,tuple):raise TypeError('complex vectors')
        if n is None:n=len(u)
        if n<3 or len(u)!=n or len(v)!=n:raise ValueError('fixed dimension n>=3')
        for z in tuple(u)+tuple(v):
            coordinate_checks+=1
            if type(z) is not int or z<0:raise ValueError('nonnegative exact integer counts')
        k=rat(k)
        if k<=0:raise ValueError('strictly positive rate')
        u,v=tuple(u),tuple(v)
        if u!=v:rates[u,v]=rates.get((u,v),F(0))+k
    channels=tuple((u,v,k) for (u,v),k in sorted(rates.items()))
    zero=(0,)*n;noncon=[(u,v,k) for u,v,k in channels if sum(u)!=sum(v)];roles=[]
    for a in range(n):
        e=tuple(int(i==a) for i in range(n))
        if len(noncon)==2 and {(u,v) for u,v,k in noncon}=={(zero,e),(e,zero)}:roles.append(a)
    if len(roles)!=1:raise Unsupported('requires one exact reversible port')
    a=roles[0];e=tuple(int(i==a) for i in range(n));aa=tuple(2*int(i==a) for i in range(n))
    internal=tuple(row for row in channels if sum(row[0])==sum(row[1]));hubs={};active={};complex_checks=0
    for u,v,k in internal:
        for z in (u,v):
            complex_checks+=1
            if sum(z)!=2:raise Unsupported('only binary nonnull internals')
            if z[a]==0:
                inds=[i for i,q in enumerate(z) if q]
                if len(inds)!=2 or any(z[i]!=1 for i in inds):raise Unsupported('hub must be square-free satellite pair')
                hubs[z]=tuple(inds)
            elif z==aa:active[z]=None
            elif z[a]==1:
                inds=[i for i,q in enumerate(z) if q and i!=a]
                if len(inds)!=1 or z[inds[0]]!=1:raise Unsupported('active complex must be A+X')
                active[z]=inds[0]
            else:raise Unsupported('unrecognized active complex')
    if not hubs:raise Unsupported('at least one hub required')
    reverse_tests=0
    for u,v,k in internal:
        if (u in hubs)==(v in hubs):raise Unsupported('only hub/active edges')
        reverse_tests+=1
        if (v,u) not in rates:raise Unsupported('every included edge must be reversible')
    satellites=tuple(i for i in range(n) if i!=a)
    graph={i:set() for i in satellites}
    for i,j in hubs.values():graph[i].add(j);graph[j].add(i)
    kX={i:F(0) for i in range(n) if i!=a};hubrows=[];amp_tests=0;incidence_tests=0
    for h,ij in sorted(hubs.items()):
        amp_tests+=2
        if (aa,h) not in rates or (h,aa) not in rates:raise Unsupported('every hub needs 2A amplification pair')
        arms=[]
        for x in sorted(kX):
            ax=tuple(int(i==a)+int(i==x) for i in range(n));incidence_tests+=1
            if (ax,h) in rates:
                kX[x]+=rates[ax,h];arms.append((x,rates[ax,h],rates[h,ax]))
        hubrows.append(dict(complex=h,edge=ij,to_hub=rates[aa,h],to_two_a=rates[h,aa],
                            reverse_sum=rates[h,aa]+sum((v for x,u,v in arms),F(0)),arms=tuple(arms)))
    if min(kX.values())<=0:raise Unsupported('each satellite needs a forward/reverse arm')
    as_=sum((h['to_hub'] for h in hubrows),F(0));bmin=min(h['to_two_a'] for h in hubrows)
    rec=dict(n=n,a=a,lam=rates[zero,e],mu=rates[e,zero],channels=channels,internal=internal,
        satellites=satellites,edges=tuple(sorted(hubs.values())),hubs=tuple(hubrows),
        kX=tuple(sorted(kX.items())),kminus=min(kX.values()),kplus=max(kX.values()),a_sum=as_,
        bmin=bmin,smax=max(h['reverse_sum'] for h in hubrows),
        b0=min(h['reverse_sum']+h['to_two_a'] for h in hubrows),
        F0=2*as_+max(kX.values()),S=sum((k for u,v,k in internal),F(0)),
        raw_sha256=digest(channels),work=dict(input_rows=len(raw),normalized_channels=len(channels),
        raw_coordinate_checks=coordinate_checks,internal_complex_checks=complex_checks,
        reverse_edge_tests=reverse_tests,
        amplification_edge_tests=amp_tests,arm_incidence_tests=incidence_tests))
    return rec


def recognize(raw):
 rec=architecture(raw);possible=[];trials=[]
 incident={v for e in rec['edges']for v in e}
 for f in rec['satellites']:
  if f in incident:continue
  arms=[h for h in rec['hubs']if any(x==f for x,u,v in h['arms'])]
  if len(arms)!=1:trials.append((f,'free species needs exactly one arm hub'));continue
  # Build the raw core by deleting this actual reversible arm pair and coordinate.
  core=[]
  for u,v,k in rec['channels']:
   if u[f] or v[f]:continue
   core.append((tuple(z for j,z in enumerate(u)if j!=f),tuple(z for j,z in enumerate(v)if j!=f),k))
  try:cr=C.B.recognize(core)
  except Unsupported as exc:trials.append((f,str(exc)));continue
  h0=arms[0];af=next((x,u,v)for x,u,v in h0['arms']if x==f)
  rare=tuple(x for x in rec['satellites']if x!=f);kx=dict(rec['kX'])
  rec.update(f=f,rare=rare,h0=h0['edge'],b_h0=h0['to_two_a'],kF=af[1],ellF=af[2],
    krminus=min(kx[x]for x in rare),krplus=max(kx[x]for x in rare),
    inventory=C.compile_inventory(dict(satellites=rare,edges=rec['edges'])),core_raw_sha256=cr['raw_sha256'],
    free_role_trials=tuple(trials+[(f,'accepted')]))
  return rec
 raise Unsupported('no isolated unique-arm satellite with a recognized dominating-cover raw core: '+str(trials))

def profile(lam,t,beta):
 L=lam*(t-1);eps=min(F(1),(lam+beta)/2);c=4*(L+eps)/beta;K=max(2,ceilq(2*c))
 return dict(beta=beta,L=L,eps=eps,c=c,K=K)
def materialize(p,lam,t):
 K,c,beta,eps=p['K'],p['c'],p['beta'],p['eps'];head={K:1+c/K}
 for r in range(K-1,0,-1):head[r]=(lam*t+beta*r*r)/(lam+beta*r*r-eps)*head[r+1]
 head[0]=2*t*head[1];p=dict(p,head=tuple(head[r]for r in range(K)))
 g=lambda r:gv(p,r);d=lambda r:g(r)-g(r+1)
 p.update(dlow=min([c]+[(r+1)**2*d(r)for r in range(1,K)]),
  Gratio=max([F(3)]+[d(r-1)/d(r)for r in range(1,K+1)]),
  D1=max([4*c]+[(r+1)**2*d(r-1)for r in range(1,K+1)]),
  D2=max([8*c]+[(r+1)**2*(g(max(0,r-2))-g(r))for r in range(1,K+2)]))
 return p
def gv(p,r):return p['head'][r]if r<p['K']else 1+p['c']/r
def dyadic(z):
 if type(z)is not int or z<1:raise ValueError('positive exact integer dyadic input')
 k=z.bit_length()-1;power=1<<k
 return F(k)+F(z-power,power)
def ceil_log2(q):
 q=rat(q)
 if q<=0:raise ValueError('positive rational logarithmic bound')
 k=q.numerator.bit_length()-q.denominator.bit_length()
 if k>=0:
  if q>1<<k:k+=1
 else:
  if q>F(1,1<<(-k)):k+=1
 return k

def _qual(rec):
 return dict(status='CERTIFIED_QUALITATIVE',family=FAMILY,raw_sha256=rec['raw_sha256'],
  conclusion='irreducible positive recurrence; every finite exponential stationary total-count moment',
  roles=dict(open_coordinate=rec['a'],free_coordinate=rec['f'],capture_hub=rec['h0'],rare=rec['rare']),
  core_inventory=rec['inventory'],core_raw_sha256=rec['core_raw_sha256'],free_role_trials=rec['free_role_trials'],
  work=dict(raw=rec['work'],profile_steps=0,expanded_head_bits=0,states_enumerated=0,stationary_fiber_laws=0),
  assurance='Ordinary proof supplied; independent whole-review status governed by the package manifest')
def qualitative(raw):
 try:return _qual(recognize(raw))
 except Unsupported as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')

def construct(raw,t,max_profile_steps=100000):
 t=rat(t)
 if t<=1:raise ValueError('t>1')
 if type(max_profile_steps)is not int or max_profile_steps<0:raise ValueError('nonnegative exact loop budget')
 try:rec=recognize(raw)
 except Unsupported as exc:return dict(status='UNKNOWN',family=FAMILY,reason=str(exc),stability='UNKNOWN')
 lam,mu=rec['lam'],rec['mu'];d=len(rec['rare']);E=len(rec['edges']);D=mu*(1-1/t);L=lam*(t-1)
 p0=profile(lam,t,rec['bmin']/(16*E));pf=profile(lam,t,rec['b_h0']/2)
 Kf=rec['a_sum']+d*rec['krplus'];J0=max(p0['K']+1,2,ceilq(4*p0['c']*(mu+Kf+p0['beta'])/D))
 steps=p0['K']-1+pf['K']-1+J0-1
 if steps>max_profile_steps:return dict(status='UNKNOWN_PROFILE_BUDGET',family=FAMILY,qualitative=_qual(rec),required_profile_steps=steps,max_profile_steps=max_profile_steps)
 p0=materialize(p0,lam,t);pf=materialize(pf,lam,t);g=lambda r:gv(p0,r);df=lambda r:g(r)-g(r+1)
 rho0=min(F(1),rec['bmin']*p0['dlow']/(88*rec['smax']),p0['eps']/(44*(Kf+lam*t)))
 e=min(F(1,4),D/(4*(rec['F0']+D)),p0['eps']/(4*mu));CA=L+11*mu
 Qhead=max((r+1)**2*max(mu*(g(r-1)/t-g(r))+Kf*r*df(r-1)+2*p0['beta']*r*df(r)+e*(rec['F0']+D),0)for r in range(1,J0))
 C0=1+L*g(0)+(Kf+rec['smax']*E)*p0['D1']+mu*p0['D1']/4+11*rho0*(Kf+rec['smax']*E+lam*t)+rho0*CA/4+e*mu
 H0=g(0)+rho0/4;zeta0=min(p0['eps'],lam)/4
 gf=lambda r:gv(pf,r);dd=lambda r:gf(r)-gf(r+1)
 rhof=min(F(1),rec['bmin']*pf['dlow']/(4*rec['smax']),pf['eps']/(44*lam*t))
 Cfor=(rec['a_sum']+rec['krplus'])*(pf['D2']+20*rhof)
 Tr=max([pf['c']*mu+2*pf['beta']*pf['c']]+[(r+1)*max(mu*(gf(r-1)/t-gf(r))+2*pf['beta']*r*dd(r)+D,0)for r in range(1,pf['K']+1)])
 T=Tr+rhof*CA;deltaF=min(F(1,4),rhof*rec['kF']/(4*Cfor),rhof*rec['kF']/(4*T))
 cfree=min(pf['eps']/2,lam*gf(0)/4)
 CZ=max([2*pf['c']+rhof]+[(r+1)*(gf(r)-1+rhof*F(r,(r+1)**2))for r in range(pf['K'])])
 Ccross=4*CZ*(rec['ellF']+mu);eta=(C0+1)/cfree
 L0=max(0,ceil_log2(4/deltaF));Jcut=max(1,ceilq(4*eta*Ccross/zeta0));exponent=L0+Jcut+1
 # A factored explicit integer head dominates B2 for gamma=1/U, U=2(2^exponent+1).
 du=min(F(1,2*(d+1)),F(1,2*E),rec['bmin']/(8*E*rec['smax']*p0['Gratio']))
 ku=min(D*du/4,e*rec['b0']*du**2/(32*E))
 A1=max(F(1),F(p0['K'])/du,4*CA/rec['krminus'],4*Qhead/(rho0*rec['krminus']))
 A2=(2*L+2*mu+rho0*(11*lam*t+CA)+1)/ku
 A4=(2*p0['c']+11*rho0)*rec['S']/(du**2*ku)
 HF=gf(0)-1+rhof/4;H=H0+eta*HF;zeta=zeta0/(2*H)
 co=dict(D=D,L=L,Kf=Kf,J0=J0,rho0=rho0,e=e,CA=CA,Qhead=Qhead,C0=C0,H0=H0,zeta0=zeta0,
  rhof=rhof,Cfor=Cfor,Tr=Tr,T=T,deltaF=deltaF,cfree=cfree,CZ=CZ,Ccross=Ccross,eta=eta,L0=L0,Jcut=Jcut,
  delta_unit=du,kappa_unit=ku,H=H,zeta=zeta)
 out=dict(status='CERTIFIED_SYMBOLIC_FOSTER',family=FAMILY,raw_sha256=rec['raw_sha256'],t=t,qualitative=_qual(rec),
  core_profile=p0,free_profile=pf,constants=co,
  symbolic_head=dict(exponent=exponent,coefficients=(A1,A2,A4),formula='U=2*(2^exponent+1); Nstar=ceil(A1*U+A2*U^2+A4*U^4+1)'),
  Foster=dict(formula='CF=(zeta+lambda+mu*Nstar+S*Nstar^2)*H*t^(Nstar+1); LW<=-zeta*W+CF*1_{N<Nstar}',
   stationary_moment='pi(t^N)<=2*CF/zeta'),
  work=dict(profile_steps=steps,additional_profile_formula_scan_points=4*p0['K']+6*pf['K'],head_value_copies=p0['K']+pf['K'],budget_scope='Only backward and compensation loops; additional formula scans, copies, arithmetic, raw scans and serialization charged separately',expanded_head_bits=0,expanded_Foster_powers=0,states_enumerated=0,stationary_fiber_laws=0),
  cost_scope='Exact W and factored algebraic head; numeric head expansion separate. No complete numerical polynomial claim; independent whole review pending.')
 out['work']['retained_scalar_bits']=bits(out);return out

def coordinates(rec,cert,x):
 N=sum(x);A=x[rec['a']];Fcount=x[rec['f']];U=N-Fcount;R=A+C.cover_weight(rec['inventory'],x);B,Ccount=(x[v]for v in rec['h0']);P=A+min(B,Ccount)
 return N,A,Fcount,U,R,P

def pieces(rec,cert,x):
 N,A,Fcount,U,R,P=coordinates(rec,cert,x);co=cert['constants']
 h0=gv(cert['core_profile'],R)+co['rho0']*F(A,(R+1)**2)-co['e']*F(A,N+1)
 Z=gv(cert['free_profile'],P)-1+co['rhof']*F(A,(P+1)**2)
 phi=max(F(0),min(F(1),(dyadic(Fcount+1)-dyadic(U+1)-co['L0'])/co['Jcut']))
 return h0,Z,phi

def hvalue(rec,cert,x):
 h0,Z,phi=pieces(rec,cert,x);return h0+cert['constants']['eta']*phi*Z

def scaled_pieces(rec,cert,x):
 N=sum(x);t=cert['t'];co=cert['constants'];h0,Z,phi=pieces(rec,cert,x);L0=LZ=cross=F(0)
 for u,v,k in rec['channels']:
  rate=k*C.B.falling(x,u)
  if not rate:continue
  xp=tuple(xx-uu+vv for xx,uu,vv in zip(x,u,v));p0,pZ,pphi=pieces(rec,cert,xp);factor=t**(sum(v)-sum(u))
  L0+=rate*(factor*p0-h0);LZ+=rate*(factor*pZ-Z);cross+=rate*factor*pZ*(pphi-phi)
 return L0,LZ,cross,L0+co['eta']*(phi*LZ+cross)
def expand_head(cert,max_power_bits):
 if type(max_power_bits)is not int or max_power_bits<0:raise ValueError('nonnegative exact power-bit expansion budget')
 sh=cert['symbolic_head'];e=sh['exponent']
 if e+1>max_power_bits:return dict(status='UNKNOWN_POWER_EXPANSION_BUDGET',required_power_bits=e+1,max_power_bits=max_power_bits,symbolic_certificate_retained=True,scope='Only the power-of-two intermediate is capped, not total head output bits or arithmetic work')
 U=2*((1<<e)+1);a,b,c=sh['coefficients'];return ceilq(a*U+b*U*U+c*U**4+1)
def outside_head(cert,N):
 if type(N)is not int or N<0:raise ValueError('nonnegative integer total')
 e=cert['symbolic_head']['exponent']
 if N.bit_length()<=e+1:return False
 return N>=expand_head(cert,N.bit_length())

def fixture():
 n=5;z=lambda *ix:tuple(ix.count(i)for i in range(n));hubs=[z(1,2),z(1,3),z(2,3)]
 raw=[(z(),z(0),F(1)),(z(0),z(),F(1))]
 for h in hubs:raw.extend([(z(0,0),h,F(1)),(h,z(0,0),F(1))])
 for x in (1,2,3):
  h=hubs[x-1];raw.extend([(z(0,x),h,F(1)),(h,z(0,x),F(2 if x==3 else 1))])
 raw.extend([(z(0,4),hubs[0],F(1)),(hubs[0],z(0,4),F(1))]);return raw
if __name__=='__main__':
 cert=construct(fixture(),F(2));co=cert['constants']
 print(json.dumps(encode(dict(status=cert['status'],raw_sha256=cert['raw_sha256'],constants=co,symbolic_head=cert['symbolic_head'],work=cert['work'],head_expansion=expand_head(cert,100000),certificate_sha256=digest(cert))),indent=2))

# Research self-checks; independent semantic receiving remains a separate task.
def receive_qualitative(raw,receipt):return canonical(qualitative(raw))==canonical(receipt)
def receive_symbolic(raw,t,receipt,**budget):return canonical(construct(raw,t,**budget))==canonical(receipt)
