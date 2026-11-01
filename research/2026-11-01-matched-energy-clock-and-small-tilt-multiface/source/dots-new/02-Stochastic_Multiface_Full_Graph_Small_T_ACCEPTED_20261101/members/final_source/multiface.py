"""Author exact-rational constructor; pending independent mathematical/code review.
No claim of all finite exponential moments; no general weak-reversibility claim.
"""
from fractions import Fraction as F
from itertools import combinations
from math import prod
from functools import lru_cache
import hashlib,json

class Unsupported(ValueError): pass
class BudgetRefusal(RuntimeError): pass

def ceilq(x):
 x=F(x); return -((-x.numerator)//x.denominator)

def integer_text(x):
 # Decimal conversion has a runtime digit guard; hexadecimal is linear-size and
 # does not mutate the process-wide guard. This is explicit exact serialization.
 return str(x) if abs(x).bit_length()<=4096 else hex(x)

def encode(x):
 if isinstance(x,F):
  if max(abs(x.numerator).bit_length(),x.denominator.bit_length())>4096:
   return {'__fraction_hex__':[hex(x.numerator),hex(x.denominator)]}
  return str(x)
 if type(x)is int and abs(x).bit_length()>4096:return {'__integer_hex__':hex(x)}
 if isinstance(x,dict): return {str(k):encode(v) for k,v in x.items()}
 if isinstance(x,(tuple,list,set,frozenset)): return [encode(v) for v in x]
 return x

def input_list_sha256(raw):
 # Ordered parsed input identity, NOT an original-file byte hash. Channel order
 # and splitting duplicates matter here, unlike the normalized reaction digest.
 rows=tuple((tuple(u),tuple(v),F(k)) for u,v,k in raw)
 return hashlib.sha256(json.dumps(encode(rows),sort_keys=True).encode()).hexdigest()

def recognize(raw):
 if not raw: raise Unsupported('nonempty raw reaction list required')
 m=len(raw[0][0]); ch={}
 if m<3: raise Unsupported('at least A and two satellites')
 for u,v,k in raw:
  if len(u)!=m or len(v)!=m or any(type(z)is not int or z<0 for z in tuple(u)+tuple(v)): raise Unsupported('count complexes')
  if type(k) not in (int,F) or k<=0 or tuple(u)==tuple(v): raise Unsupported('positive rational nontrivial rates')
  uv=(tuple(u),tuple(v));ch[uv]=ch.get(uv,F(0))+F(k)
 for u,v in ch:
  if (v,u) not in ch: raise Unsupported('every directed channel must have a positive reverse')
 zero=(0,)*m; ups=[v for (u,v) in ch if u==zero]
 if len(ups)!=1 or sum(ups[0])!=1: raise Unsupported('sole 0<->A pair')
 one=ups[0];A=one.index(1);two=tuple(2*z for z in one);sat=tuple(i for i in range(m) if i!=A)
 lam=ch[(zero,one)];mu=ch[(one,zero)];internal=[];hubs={};kX={i:F(0) for i in sat}
 def hub(u):
  return u[A]==0 and sum(u)==2 and max(u)<=1
 def arm(u):
  return u[A]==1 and sum(u)==2 and sum(u[i] for i in sat)==1
 for (u,v),k in ch.items():
  if (u,v) in ((zero,one),(one,zero)):continue
  if sum(u)!=2 or sum(v)!=2 or not ((hub(u) and (v==two or arm(v))) or (hub(v) and (u==two or arm(u)))):raise Unsupported('binary hub-active architecture')
  internal.append((u,v,k))
  hh=u if hub(u) else v; hubs[hh]=tuple(i for i,z in enumerate(hh) if z)
  if arm(u):kX[next(i for i in sat if u[i])]+=k
 if not hubs or any(v<=0 for v in kX.values()):raise Unsupported('nonempty hub graph and every satellite covered by an arm')
 for hh in hubs:
  if (two,hh) not in ch or (hh,two) not in ch:raise Unsupported('each hub has amplification pair')
 rows=tuple((u,v,k) for (u,v),k in sorted(ch.items()))
 digest=hashlib.sha256(json.dumps(encode(rows),sort_keys=True).encode()).hexdigest()
 return dict(m=m,A=A,sat=sat,n=len(sat),hubs=tuple(sorted(hubs)),edges=tuple(sorted(hubs.values())),channels=rows,internal=tuple(sorted(internal)),lam=lam,mu=mu,a=sum((ch[(two,h)] for h in hubs),F(0)),b=min(ch[(h,two)] for h in hubs),s=max(sum((k for (u,v),k in ch.items() if u==h),F(0)) for h in hubs),kmin=min(kX.values()),kmax=max(kX.values()),kX=kX,Srate=sum((k for u,v,k in internal),F(0)),raw_sha256=digest,normalized_reaction_sha256=digest)

def construct(raw,max_masks=1000000):
 if type(max_masks)is not int or max_masks<0:raise ValueError('exact nonnegative integer mask budget')
 r=recognize(raw);n=r['n']; masks=2**n
 if masks>max_masks:raise BudgetRefusal('independent-set mask budget: required 2^'+str(n)+' masks ('+str(n+1)+' bits)')
 Isets=[]
 for mask in range(1,masks):
  I=frozenset(r['sat'][i] for i in range(n) if mask>>i&1)
  if not any(u in I and v in I for u,v in r['edges']):Isets.append(I)
 M=max(2,ceilq(12*r['s']/r['b']));q=F(M+1,M);aw=2*M;W=2*M+2;s0=M
 g=r['kmin']*(1-q**-2)/(q-1);h=r['b']/(4*(q-1));Cstep=(4*M+4)*3**6
 CA=Cstep*(r['a']+r['kmax'])+18*r['mu']*M;CH=Cstep*r['s'];d=F(1,8*(W+s0+1)**2)
 T=max(1,ceilq(4*CA/g),ceilq(4*CH*len(r['edges'])/h));B=1+n*T;R=(B+1)**2/d
 K=max(2,ceilq(4*masks*CH*R/h));faces=[]
 for I in Isets:
  near=frozenset(v for edge in r['edges'] for v in edge if v not in I and any(u in I for u in edge));far=frozenset(r['sat'])-I-near
  ww=tuple(aw if i==r['A'] else 0 if i in I else W if i in near else M+1 for i in range(r['m']))
  faces.append(dict(I=I,Near=near,Far=far,resource_weights=ww,weight=K**(n-len(I))))
 P=sum(f['weight'] for f in faces);RA=P*CA*(B+1);RQ=P*CH*(B+1)**2
 delta=F(1,4);eta=delta/(4*n);hh=eta**(n-1)/(2*n);epsC=min(F(1,4),hh**2/2,hh/8);gamma=delta*hh/8
 sstar=min(g,h)*d*epsC/4;Cbirth=r['lam']*(1+P)+r['mu']**2/4;eps=min(F(1),sstar/(16*Cbirth));t=1+eps
 D=r['mu']*(1-1/t);Fwd=2*r['a']+r['kmax'];e=min(F(1,4),D/(4*(Fwd+1)));H=1+eps*(1+P)
 da_lower=F(1,8*(aw+s0+1)**2)
 Nstar=ceilq(max(F(2),4*RA/D,RQ/(e*r['b']),1+4*r['mu']*H/(g*da_lower),4*(Cbirth*eps+1)/(D*gamma),2*(Cbirth*eps+1)/(e*r['b']*gamma**2)))
 nu=min(r['lam'],F(1),sstar/8);Htot=1+P+H;zeta=nu/Htot
 out=dict(status='AUTHOR_COMPLETE_SMALL_T_CANDIDATE_NOT_INDEPENDENTLY_ACCEPTED',raw=r,faces=faces,M=M,q=q,aw=aw,W=W,s0=s0,g=g,h=h,Cstep=Cstep,CA=CA,CH=CH,d=d,T=T,B=B,R=R,K=K,P=P,RA=RA,RQ=RQ,delta=delta,eta=eta,hh=hh,epsC=epsC,gamma=gamma,sstar=sstar,Cbirth=Cbirth,eps=eps,t=t,D=D,Fwd=Fwd,e=e,H=H,da_lower=da_lower,Nstar=Nstar,nu=nu,Htot=Htot,zeta=zeta,mask_count=masks)
 out['CF_expression']={'op':'mul','args':[zeta+r['lam']+r['mu']*Nstar+r['Srate']*Nstar**2,Htot,{'op':'pow','base':t,'exponent':Nstar+1}]}
 out['moment_bound_expression']={'op':'mul','args':[F(4,3)/zeta,out['CF_expression']]}
 return out

@lru_cache(maxsize=100000)
def profile_exact(q,s0,j):return (1-q**(-(j+s0)))/F(j+s0)

def profile(p,j,max_power=100000):
 if type(max_power)is not int or max_power<0:raise ValueError('exact nonnegative integer exponent budget')
 if type(j)is not int or j<0:raise ValueError('nonnegative integer resource')
 if j+p['s0']>max_power:raise BudgetRefusal('pointwise power exponent budget')
 return profile_exact(p['q'],p['s0'],j)

def diff(p,j,max_power=100000):return profile(p,j,max_power)-profile(p,j+1,max_power)

def face_stats(p,f,x,max_power=100000):
 r=p['raw'];A=x[r['A']];FI=sum(x[i] for i in f['I']);U=sum(x)-FI;j=sum(w*z for w,z in zip(f['resource_weights'],x))
 cross=sum(x[u]*x[v] for u,v in r['edges'] if (u in f['I'])!=(v in f['I']))
 far=sum(x[u]*x[v] for u,v in r['edges'] if u in f['Far'] and v in f['Far'])
 bad=sum(x[u]*x[v] for u,v in r['edges'] if u not in f['I'] and v not in f['I'] and (u in f['Near'] or v in f['Near']))
 DD=diff(p,j,max_power);z=profile(p,j,max_power);rr=(p['g']*A*FI+p['h']*(cross+far))*DD
 return dict(U=U,F=FI,J=j,Qcross=cross,Qfar=far,Qbad=bad,D=DD,Z=z,r=rr)

def psi(p,x,max_power=100000):return sum((f['weight']*profile(p,sum(w*z for w,z in zip(f['resource_weights'],x)),max_power) for f in p['faces']),F(0))

def value(p,x,max_power=100000):
 r=p['raw'];N=sum(x);A=x[r['A']];Q=sum(x[u]*x[v] for u,v in r['edges'])
 return 1-p['e']*A/(N+1)+psi(p,x,max_power)+(p['H'] if A==0 and Q==0 else 0)

def propensity(u,x):
 out=1
 for a,b in zip(u,x):
  if b<a:return 0
  for j in range(a):out*=b-j
 return out

def generator(p,x,fn,t=None):
 if t is None:t=p['t']
 fx=fn(x);out=F(0)
 for u,v,k in p['raw']['channels']:
  rate=k*propensity(u,x)
  if rate:
   y=tuple(xx+vv-uu for xx,uu,vv in zip(x,u,v));out+=rate*(t**(sum(v)-sum(u))*fn(y)-fx)
 return out

def fixture(nsat=5,edges=None,perturb=True):
 if edges is None:edges=((0,1),(0,2),(1,2),(3,4))
 m=nsat+1;z=lambda *ix:tuple(ix.count(i) for i in range(m));raw=[(z(),z(0),F(1)),(z(0),z(),F(1))]
 for j,(u,v) in enumerate(edges):
  hh=z(u+1,v+1);raw.extend([(z(0,0),hh,F(1)),(hh,z(0,0),F(1))])
  for i in range(nsat):
   raw.extend([(z(0,i+1),hh,F(1)),(hh,z(0,i+1),F(2 if perturb and j==0 and i==0 else 1))])
 return raw
