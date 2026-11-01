"""Independent raw acquisition, exact certificate reconstruction, and bounded receiving.
No candidate modules imported. The mathematics was audited separately.
"""
from fractions import Fraction as Q
from functools import lru_cache
import hashlib,json,re

class DomainError(ValueError):pass
class UnknownComputation(RuntimeError):pass

def decimal(n):
 if type(n)is not int:raise DomainError('integer required')
 if n<0:return '-'+decimal(-n)
 if n.bit_length()<12000:return str(n)
 base=10**1000; chunks=[]
 while n: n,r=divmod(n,base);chunks.append(str(r))
 return chunks[-1]+''.join(c.zfill(1000) for c in reversed(chunks[:-1])) if chunks else '0'
def rational_text(x):
 x=Q(x);return decimal(x.numerator)+(('/'+decimal(x.denominator)) if x.denominator!=1 else '')
def encoded(x):
 if isinstance(x,Q):
  if max(abs(x.numerator).bit_length(),x.denominator.bit_length())>4096:return {'__fraction_hex__':[hex(x.numerator),hex(x.denominator)]}
  return rational_text(x)
 if type(x)is int and abs(x).bit_length()>4096:return {'__integer_hex__':hex(x)}
 if isinstance(x,dict):return {str(k):encoded(v) for k,v in x.items()}
 if isinstance(x,(tuple,list,set,frozenset)):return [encoded(v) for v in x]
 return x
def guard_tree(root,max_nodes=200000,max_depth=256,max_atom_bits=1000000):
 if any(type(x)is not int or x<0 for x in [max_nodes,max_depth,max_atom_bits]):raise DomainError('tree budgets')
 stack=[(root,0,False)];active=set();containers=set();nodes=0
 while stack:
  x,depth,leaving=stack.pop()
  if leaving:active.remove(id(x));continue
  nodes+=1
  if nodes>max_nodes or depth>max_depth:raise UnknownComputation('tree traversal budget')
  typ=type(x)
  if typ is bool or typ is float or x is None:raise DomainError('noncanonical scalar type')
  if typ is int:
   if abs(x).bit_length()>max_atom_bits:raise UnknownComputation('integer atom bit budget')
  elif typ is str:
   if len(x)*8>max_atom_bits:raise UnknownComputation('string atom budget')
  elif typ in (dict,list):
   if id(x)in containers:raise DomainError('cyclic or shared tree')
   containers.add(id(x))
   if nodes+len(x)>max_nodes:raise UnknownComputation('wide tree budget')
   active.add(id(x));stack.append((x,depth,True))
   if typ is dict:
    if any(type(k)is not str for k in x):raise DomainError('string dictionary keys')
    children=list(x.values())
   else:children=x
   if nodes+len(stack)+len(children)>max_nodes*2:raise UnknownComputation('pending tree budget')
   stack.extend((v,depth+1,False)for v in reversed(children))
  else:raise DomainError('canonical JSON tree required')
 return nodes

def strict_equal(a,b):
 stack=[(a,b)]
 while stack:
  a,b=stack.pop()
  if type(a)is not type(b):return False
  if isinstance(a,dict):
   if a.keys()!=b.keys():return False
   stack.extend((a[k],b[k])for k in a)
  elif isinstance(a,list):
   if len(a)!=len(b):return False
   stack.extend(zip(a,b))
  elif a!=b:return False
 return True

def parse_decimal(s):
 negative=s.startswith('-');s=s[1:]if negative else s
 if not s or any(c<'0'or c>'9'for c in s):raise DomainError('decimal integer')
 result=0
 for k in range(0,len(s),1000):
  chunk=s[k:k+1000];result=result*10**len(chunk)+int(chunk)
 return -result if negative else result

def ceil(x):x=Q(x);return -(-x.numerator//x.denominator)

def acquire(raw,canonical_internal=True):
 if not isinstance(raw,(list,tuple)) or not raw:raise DomainError('nonempty finite channel array')
 rows=[];dim=None
 for item in raw:
  if not isinstance(item,(list,tuple)) or len(item)!=3:raise DomainError('source,target,rate triple')
  u,v,k=item
  if not isinstance(u,(list,tuple)) or not isinstance(v,(list,tuple)):raise DomainError('count vectors')
  if dim is None:dim=len(u)
  if dim<3 or len(u)!=dim or len(v)!=dim:raise DomainError('uniform dimension >=3')
  if any(type(z)is not int or z<0 for z in list(u)+list(v)):raise DomainError('nonnegative integer counts')
  if type(k)not in (int,Q) or k<=0 or u==v:raise DomainError('positive rational rate and nontrivial channel')
  rows.append((tuple(u),tuple(v),Q(k)))
 channels={}
 for u,v,k in rows:channels[u,v]=channels.get((u,v),Q(0))+k
 if any((v,u)not in channels for u,v in channels):raise DomainError('reversibility')
 z=(0,)*dim;births=[v for u,v in channels if u==z]
 if len(births)!=1 or sum(births[0])!=1:raise DomainError('one immigration species')
 one=births[0];A=one.index(1);two=tuple(2*a for a in one);sat=tuple(i for i in range(dim) if i!=A)
 def shape(u):
  if u==two:return 'double'
  if sum(u)==2 and u[A]==1:return 'arm'
  if sum(u)==2 and u[A]==0 and all(a<=1 for a in u):return 'hub'
  return 'other'
 hubs=set();internal=[];ki={i:Q(0) for i in sat}
 for (u,v),k in channels.items():
  if (u,v)in ((z,one),(one,z)):continue
  a,b=shape(u),shape(v)
  if (a=='hub' and b in ('arm','double')):hubs.add(u)
  elif (b=='hub' and a in ('arm','double')):hubs.add(v)
  else:raise DomainError('binary hub-active channel shape')
  internal.append((u,v,k))
  if a=='arm':ki[next(i for i in sat if u[i])]+=k
 if not hubs or not all(ki.values()):raise DomainError('nonempty hubs, every satellite forward arm')
 if any((two,h)not in channels or (h,two)not in channels for h in hubs):raise DomainError('amplification at each hub')
 sorted_rows=tuple((u,v,k)for (u,v),k in sorted(channels.items()))
 raw_sha=hashlib.sha256(json.dumps(encoded(sorted_rows),sort_keys=True).encode()).hexdigest()
 hubs=tuple(sorted(hubs));edges=tuple(sorted(tuple(i for i in sat if h[i])for h in hubs))
 if canonical_internal:internal.sort()
 result=dict(m=dim,A=A,sat=sat,n=len(sat),hubs=hubs,edges=edges,channels=sorted_rows,internal=tuple(internal),lam=channels[z,one],mu=channels[one,z],a=sum((channels[two,h] for h in hubs),Q(0)),b=min(channels[h,two] for h in hubs),s=max(sum((k for (u,v),k in channels.items()if u==h),Q(0))for h in hubs),kmin=min(ki.values()),kmax=max(ki.values()),kX=ki,Srate=sum((k for u,v,k in internal),Q(0)),raw_sha256=raw_sha)
 if canonical_internal:result['normalized_reaction_sha256']=raw_sha
 return result

def construct(raw,max_masks=1000000,canonical_internal=True):
 if type(max_masks)is not int or max_masks<0:raise DomainError('nonnegative integer mask budget')
 r=acquire(raw,canonical_internal);n=r['n'];count=1<<n
 if count>max_masks:raise UnknownComputation('mask enumeration refused; qualitative architecture acquired')
 slots={s:i for i,s in enumerate(r['sat'])};edge_masks=[(1<<slots[a])|(1<<slots[b])for a,b in r['edges']]
 independent=[mask for mask in range(1,count)if all(mask&e!=e for e in edge_masks)]
 M=max(2,ceil(12*r['s']/r['b']));q=Q(M+1,M);aw=2*M;W=2*M+2;s0=M
 g=r['kmin']*M*(2*M+1)/Q((M+1)**2);h=r['b']*M/4
 Cstep=(4*M+4)*729;CA=Cstep*(r['a']+r['kmax'])+18*r['mu']*M;CH=Cstep*r['s'];d=Q(1,8*(3*M+3)**2)
 T=max(1,ceil(4*CA/g),ceil(4*CH*len(r['edges'])/h));B=1+n*T;R=Q((B+1)**2)/d;K=max(2,ceil(4*count*CH*R/h))
 faces=[]
 for mask in independent:
  I=frozenset(s for i,s in enumerate(r['sat'])if mask>>i&1)
  Near=frozenset(v for e in r['edges']if any(u in I for u in e)for v in e if v not in I)
  Far=frozenset(r['sat'])-I-Near
  resource_weights=tuple(aw if i==r['A']else 0 if i in I else W if i in Near else M+1 for i in range(r['m']))
  faces.append(dict(I=I,Near=Near,Far=Far,resource_weights=resource_weights,weight=K**(n-len(I))))
 P=sum(f['weight']for f in faces);RA=P*CA*(B+1);RQ=P*CH*(B+1)**2
 delta=Q(1,4);eta=Q(1,16*n);hh=eta**(n-1)/(2*n);epsC=min(Q(1,4),hh*hh/2,hh/8);gamma=hh/32
 sstar=min(g,h)*d*epsC/4;Cbirth=r['lam']*(P+1)+r['mu']**2/4;eps=min(Q(1),sstar/(16*Cbirth));t=1+eps;D=r['mu']*eps/t
 Fwd=2*r['a']+r['kmax'];e=min(Q(1,4),D/(4*(Fwd+1)));H=1+eps*(1+P);da_lower=Q(1,8*(3*M+1)**2)
 Nstar=max(2,ceil(4*RA/D),ceil(RQ/(e*r['b'])),ceil(1+4*r['mu']*H/(g*da_lower)),ceil(4*(Cbirth*eps+1)/(D*gamma)),ceil(2*(Cbirth*eps+1)/(e*r['b']*gamma**2)))
 nu=min(r['lam'],Q(1),sstar/8);Htot=P+1+H;zeta=nu/Htot
 result={k:v for k,v in locals().copy().items()if k in 'M q aw W s0 g h Cstep CA CH d T B R K P RA RQ delta eta hh epsC gamma sstar Cbirth eps t D Fwd e H da_lower Nstar nu Htot zeta'.split()}
 result.update(status='AUTHOR_COMPLETE_SMALL_T_CANDIDATE_NOT_INDEPENDENTLY_ACCEPTED',raw=r,faces=faces,mask_count=count)
 result['CF_expression']={'op':'mul','args':[zeta+r['lam']+r['mu']*Nstar+r['Srate']*Nstar*Nstar,Htot,{'op':'pow','base':t,'exponent':Nstar+1}]}
 result['moment_bound_expression']={'op':'mul','args':[Q(4,3)/zeta,result['CF_expression']]}
 return result

def receive(raw,claim,max_masks=1000000,canonical_internal=True):
 if isinstance(claim,(bytes,str)):
  if len(claim)>2000000:raise UnknownComputation('serialized certificate byte budget')
  try:claim=json.loads(claim,parse_int=parse_decimal)
  except Exception:return False
 try:
  guard_tree(claim)
  truth=encoded(construct(raw,max_masks,canonical_internal))
 except DomainError:return False
 return strict_equal(claim,truth)

def tag_integer(x):
 if type(x)is not dict or set(x)!={'__integer_hex__'}or type(x['__integer_hex__'])is not str:raise DomainError('integer hex tag')
 try:return int(x['__integer_hex__'],16)
 except Exception:raise DomainError('integer hex digits')

def eval_expression(expr,max_power_bits=1000000,max_nodes=10000,max_depth=256):
 if any(type(z)is not int or z<0 for z in [max_power_bits,max_nodes,max_depth])or max_nodes<1:raise DomainError('exact computation budgets')
 seen=0;active=set();tasks=[('enter',expr,0)];values=[]
 while tasks:
  action,x,depth=tasks.pop()
  if action=='exit':
   active.remove(id(x))
   if x['op']=='mul':
    size=len(x['args']);parts=values[-size:]if size else [];result=Q(1)
    if size:del values[-size:]
    for part in parts:result*=part
    values.append(result)
   else:
    base=values.pop();k=x['exponent'];k=tag_integer(k)if type(k)is dict else k;cost=k*max(abs(base.numerator).bit_length(),base.denominator.bit_length())
    if cost>max_power_bits:raise UnknownComputation('rational power intermediate bit bound refused')
    values.append(base**k)
   continue
  seen+=1
  if seen>max_nodes or depth>max_depth:raise UnknownComputation('expression traversal budget')
  if type(x)is int or isinstance(x,Q):values.append(Q(x));continue
  if type(x)is str:
   if not re.fullmatch(r'-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?',x):raise DomainError('canonical rational atom')
   bits=x.split('/');value=Q(parse_decimal(bits[0]),parse_decimal(bits[1])if len(bits)==2 else 1)
   if rational_text(value)!=x:raise DomainError('noncanonical rational atom')
   values.append(value);continue
  if type(x)is not dict:raise DomainError('expression node')
  if set(x)=={'__integer_hex__'}:values.append(Q(tag_integer(x)));continue
  if set(x)=={'__fraction_hex__'}:
   args=x['__fraction_hex__']
   if type(args)is not list or len(args)!=2 or any(type(v)is not str for v in args):raise DomainError('rational hex tag')
   try:value=Q(int(args[0],16),int(args[1],16))
   except Exception:raise DomainError('rational hex digits')
   values.append(value);continue
  if id(x)in active:raise DomainError('cyclic expression')
  if x.get('op')=='mul' and set(x)=={'op','args'} and type(x['args'])is list:
   children=x['args']
  elif x.get('op')=='pow' and set(x)=={'op','base','exponent'}:
   k=x['exponent'];k=tag_integer(k)if type(k)is dict else k
   if type(k)is not int or k<0:raise DomainError('nonnegative exact integer exponent')
   children=[x['base']]
  else:raise DomainError('expression grammar')
  if seen+len(tasks)+len(children)>max_nodes*2:raise UnknownComputation('pending expression traversal budget')
  active.add(id(x));tasks.append(('exit',x,depth));tasks.extend(('enter',v,depth+1)for v in reversed(children))
 assert len(values)==1
 return values[0]

def fixture(n=5,edges=((0,1),(0,2),(1,2),(3,4)),perturb=True,sparse=False):
 m=n+1
 def c(*ids):return tuple(ids.count(i)for i in range(m))
 raw=[(c(),c(0),Q(1)),(c(0),c(),Q(1))]
 for ei,(a,b)in enumerate(edges):
  hub=c(a+1,b+1);raw.extend([(c(0,0),hub,Q(1)),(hub,c(0,0),Q(1))])
  for i in range(n):
   if sparse and ei!=i%len(edges):continue
   raw.extend([(c(0,i+1),hub,Q(1)),(hub,c(0,i+1),Q(2 if perturb and ei==0 and i==0 else 1))])
 return raw

def transitions(p,x):
 r=p['raw']
 if type(x)not in (tuple,list)or len(x)!=r['m']or any(type(a)is not int or a<0 for a in x):raise DomainError('count state')
 for u,v,k in r['channels']:
  a=1
  for xi,ui in zip(x,u):
   if xi<ui:a=0;break
   for j in range(ui):a*=xi-j
  if a:yield k*a,tuple(xi-ui+vi for xi,ui,vi in zip(x,u,v)),sum(v)-sum(u)

class IntervalFoster:
 def __init__(self,p,precision=8192,exact_power_bits=20000):
  self.p=p;self.precision=precision;self.exact_power_bits=exact_power_bits;self.exact=0;self.enclosed=0;self.max_resource_bits=0;self.max_expanded_power_bits=0
 @lru_cache(None)
 def z(self,j):
  p=self.p;k=j+p['s0'];self.max_resource_bits=max(self.max_resource_bits,j.bit_length())
  bits=k*max(p['q'].numerator.bit_length(),p['q'].denominator.bit_length())
  if bits<=self.exact_power_bits:
   self.exact+=1;self.max_expanded_power_bits=max(self.max_expanded_power_bits,bits);qpower=p['q']**-k;z=(1-qpower)/k;return z,z
  self.enclosed+=1;error=Q(1,1<<min(self.precision,k//p['M']))
  return (1-error)/k,Q(1,k)
 @lru_cache(None)
 def d(self,j):
  p=self.p;k=j+p['s0'];bits=(k+1)*max(p['q'].numerator.bit_length(),p['q'].denominator.bit_length())
  if bits<=self.exact_power_bits:
   lo,hi=self.z(j);ln,hn=self.z(j+1);assert lo==hi and ln==hn;return lo-ln,lo-ln
  error=Q(1,1<<min(self.precision,k//p['M']));base=Q(1,k*(k+1));correction=Q(1,k)-1/(p['q']*(k+1))
  return base-error*correction,base
 @lru_cache(None)
 def psi(self,x):
  lo=hi=Q(0)
  for f in self.p['faces']:
   j=sum(a*b for a,b in zip(f['resource_weights'],x));a,b=self.z(j);lo+=f['weight']*a;hi+=f['weight']*b
  return lo,hi
 @lru_cache(None)
 def h(self,x):
  p=self.p;r=p['raw'];N=sum(x);A=x[r['A']];Qhub=sum(x[a]*x[b]for a,b in r['edges'])
  baseline=1-p['e']*A/(N+1)+(p['H']if A==0 and Qhub==0 else 0);lo,hi=self.psi(x)
  return baseline+lo,baseline+hi
 def generator(self,x,fn):
  initiallo,initialhi=fn(x);lo=hi=Q(0)
  for rate,y,delta in transitions(self.p,x):
   yl,yh=fn(y);factor=self.p['t']**delta;lo+=rate*(factor*yl-initialhi);hi+=rate*(factor*yh-initiallo)
  return lo,hi
 def global_rhs_lower(self,x):
  p=self.p;r=p['raw'];A=x[r['A']];N=sum(x);Qhub=sum(x[a]*x[b]for a,b in r['edges']);captureupper=Q(0)
  for f in p['faces']:
   bulk=sum(x[i]for i in f['I']);cross=sum(x[a]*x[b]for a,b in r['edges']if (a in f['I'])!=(b in f['I']));far=sum(x[a]*x[b]for a,b in r['edges']if a in f['Far']and b in f['Far']);j=sum(a*b for a,b in zip(f['resource_weights'],x));dl,du=self.d(j);assert dl>0
   captureupper+=f['weight']*(p['g']*A*bulk+p['h']*(cross+far))*du
  psilo,psihi=self.psi(x)
  return r['lam']*p['eps']*psilo-captureupper/2+p['RA']*A/(N+1)+p['RQ']*Qhub/Q((N+1)**2)
