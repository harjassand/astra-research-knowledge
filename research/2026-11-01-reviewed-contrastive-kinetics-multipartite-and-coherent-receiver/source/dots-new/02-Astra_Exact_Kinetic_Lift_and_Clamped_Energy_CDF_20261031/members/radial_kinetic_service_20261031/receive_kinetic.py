"""Exact raw homogeneous kinetic lift + finite clamped-protocol energy CDF.
No physical actuation, unknown-model inference, or autonomous hitting-time solver.
All proof endpoints are rational dyadic enclosures; float fields are diagnostics.
"""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import hashlib,json,re,time
class Unknown(ValueError):pass

def strict_int(x,name,lo=1):
 if type(x)is not int or x<lo:raise Unknown(name+' must be a strict integer >= '+str(lo))
 return x

def frac(x,name,positive=False):
 if type(x)is not F or (positive and x<=0):raise Unknown(name+' must be an exact Fraction'+(' >0' if positive else ''))
 return x

def fs(x):
 try:return str(x.numerator) if x.denominator==1 else str(x.numerator)+'/'+str(x.denominator)
 except ValueError:raise Unknown('exact rational serialization exceeds Python finite digit budget')
def raw_frac(x,max_bits):
 if type(x)is not str or len(x)>2*(max_bits+3) or not re.fullmatch(r'-?[0-9]+(?:/[0-9]+)?',x):raise Unknown('canonical raw rational string')
 try:q=F(x)
 except (ValueError,ZeroDivisionError):raise Unknown('invalid raw rational')
 if fs(q)!=x or max(q.numerator.bit_length(),q.denominator.bit_length())>max_bits:raise Unknown('raw rational canonical/bit budget')
 return q

def same(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
 if type(a)is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b

def show(x):
 try:return float(x)
 except OverflowError:return None

def enclosure(lo,hi):return {'lower':fs(lo),'upper':fs(hi),'display':[show(lo),show(hi)]}
def canonical_hash(raw):return hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()

class RationalBudget:
 def __init__(self,bits):self.bits=bits;self.max_stored_bits=0;self.operations=0
 def keep(self,x):
  b=max(x.numerator.bit_length(),x.denominator.bit_length());self.max_stored_bits=max(self.max_stored_bits,b)
  if b>self.bits:raise Unknown('stored rational bit budget')
  return x
 def add(self,a,b):
  if max(a.numerator.bit_length()+b.denominator.bit_length(),b.numerator.bit_length()+a.denominator.bit_length(),a.denominator.bit_length()+b.denominator.bit_length())+1>self.bits:raise Unknown('rational addition precheck budget')
  self.operations+=1;return self.keep(a+b)
 def mul(self,a,b):
  if max(a.numerator.bit_length()+b.numerator.bit_length(),a.denominator.bit_length()+b.denominator.bit_length())>self.bits:raise Unknown('rational product precheck budget')
  self.operations+=1;return self.keep(a*b)

def acquire(raw,initial_state,*,max_dimension=1024,max_terms=100000,max_coefficient_bits=4096,max_exponent_entries=64000000,max_total_coefficient_bits=32000000,max_rational_bits=1000000):
 budgets=locals().copy()
 for key in ['max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits']:strict_int(budgets[key],key)
 if type(raw)is not dict or set(raw)!={'dimension','energy_terms','tangent_program'}:raise Unknown('complete kinetic model program schema')
 m=strict_int(raw['dimension'],'dimension')
 if m>max_dimension:raise Unknown('dimension budget')
 if type(initial_state)is not list or len(initial_state)!=m:raise Unknown('initial state length')
 for x in initial_state:
  frac(x,'initial coordinate')
  if max(x.numerator.bit_length(),x.denominator.bit_length())>max_coefficient_bits:raise Unknown('initial coordinate bit budget')
 ts=raw['energy_terms']
 if type(ts)is not list or not 1<=len(ts)<=max_terms or len(ts)*m>max_exponent_entries:raise Unknown('term/exponent-entry budget')
 tangent=raw['tangent_program']
 if type(tangent)is not dict or set(tangent)!={'kind','weight'} or tangent['kind']!='complete_pair_gradient':raise Unknown('actual tangent program schema')
 weight=raw_frac(tangent['weight'],max_coefficient_bits)
 if weight<0:raise Unknown('negative tangent weight')
 p=None;seen=set();pure={};terms=[];total_bits=0;r=RationalBudget(max_rational_bits);u0=F(0)
 for rec in ts:
  if type(rec)is not dict or set(rec)!={'powers','coefficient'}:raise Unknown('complete energy term schema')
  powers=rec['powers']
  if type(powers)is not list or len(powers)!=m:raise Unknown('powers length')
  for n in powers:
   if type(n)is not int or n not in (0,2,4):raise Unknown('nonnegative even exponent grammar')
  degree=sum(powers)
  if degree not in (2,4) or (p is not None and p!=degree):raise Unknown('homogeneous degree 2 or 4 required')
  p=degree;key=tuple(powers)
  if key in seen:raise Unknown('duplicate monomial')
  seen.add(key);c=raw_frac(rec['coefficient'],max_coefficient_bits)
  if c<=0:raise Unknown('strictly positive listed monomial coefficients')
  total_bits+=c.numerator.bit_length()+c.denominator.bit_length()
  if total_bits>max_total_coefficient_bits:raise Unknown('total coefficient bit budget')
  support=[(i,n) for i,n in enumerate(powers) if n]
  if len(support)==1:pure[support[0][0]]=c
  val=c
  for i,n in support:
   for _ in range(n):val=r.mul(val,initial_state[i])
  u0=r.add(u0,val);terms.append((support,c))
 if len(pure)!=m:raise Unknown('missing pure positive coercive monomial')
 if m<p:raise Unknown('alpha<1 origin interface not admitted')
 if u0<=0:raise Unknown('positive-energy initial state required')
 dmin=min(pure.values());a=dmin/F(m**(p//2-1));alpha=F(m,p)
 info={'raw_sha256':canonical_hash(raw),'m':m,'p':p,'alpha':fs(alpha),'coercivity_lower':fs(a),'pure_coefficient_min':fs(dmin),'initial_energy':fs(u0),
 'tangent_weight':fs(weight),'transverse_SPD_away_origin':weight>0,'raw_terms':len(ts),'exponent_entries_read':len(ts)*m,'coefficient_bits_read':total_bits,
 'initial_energy_rational_operations':r.operations,'initial_energy_max_stored_bits':r.max_stored_bits,
 'model':'divergence-form radial lift plus complete-pair tangent diffusion; not the constant-mobility model'}
 return info,u0,alpha

class Fixed:
 def __init__(self,P,max_operations,max_integer_bits,max_exp_terms,max_series_terms):
  self.P=P;self.S=1<<P;self.max_operations=max_operations;self.limit=max_integer_bits;self.max_exp_terms=max_exp_terms;self.max_series_terms=max_series_terms
  self.operations=0;self.max_guarded_bits=0;self.exp_calls=0;self.exp_terms=0;self.cdf_terms=0
 def tick(self):
  self.operations+=1
  if self.operations>self.max_operations:raise Unknown('fixed arithmetic operation budget')
 def product(self,a,b):
  self.tick();size=abs(a).bit_length()+abs(b).bit_length();self.max_guarded_bits=max(self.max_guarded_bits,size)
  if size>self.limit:raise Unknown('fixed product bit budget')
  return a*b
 def rat(self,q):
  if q<0:raise Unknown('internal positive interval')
  num=self.product(q.numerator,self.S);a,rem=divmod(num,q.denominator)
  return a,a+(rem!=0)
 def mul(self,a,b):
  lo=self.product(a[0],b[0])>>self.P;v=self.product(a[1],b[1]);hi=(v+self.S-1)>>self.P
  return lo,hi
 def times(self,a,q):
  if q<0:raise Unknown('internal negative scalar')
  lo=self.product(a[0],q.numerator)//q.denominator;v=self.product(a[1],q.numerator);hi=(v+q.denominator-1)//q.denominator
  return lo,hi
 def expminus(self,x):
  if x<0:raise Unknown('nonnegative exponential argument')
  self.exp_calls+=1
  if not x:return self.S,self.S
  s=max(0,x.numerator.bit_length()-x.denominator.bit_length()+2)
  if s>self.max_exp_terms:raise Unknown('exponential scaling budget')
  r=x/F(1<<s)
  while r>F(1,2):s+=1;r/=2
  term=(self.S,self.S);total=term
  for j in range(1,self.max_exp_terms+1):
   term=self.times(term,r/j);total=(total[0]+term[0],total[1]+term[1]);self.exp_terms+=1
   nxt=self.times(term,r/(j+1))
   if nxt[1]<=1:
    total=(total[0],total[1]+2);break
  else:raise Unknown('exponential Taylor budget')
  sq=self.product(self.S,self.S)
  ans=(sq//total[1],(sq+total[0]-1)//total[0])
  for _ in range(s):ans=self.mul(ans,ans)
  return max(0,ans[0]),min(self.S,ans[1])
 def cdf_point(self,alpha,lam,x,tail_tolerance):
  # Monotone point inputs; Gamma CDF is a Poisson tail for integer alpha.
  w=self.expminus(lam);t=self.expminus(x)
  if w[0]<=0:raise Unknown('positive Poisson seed unresolved at fixed precision')
  prefix=t
  for k in range(1,alpha):
   t=self.times(t,x/k);prefix=(prefix[0]+t[0],prefix[1]+t[1])
  total=(0,0);mass_lo=0
  for n in range(self.max_series_terms):
   g=(max(0,self.S-prefix[1]),min(self.S,max(0,self.S-prefix[0])))
   term=self.mul(w,g);total=(total[0]+term[0],total[1]+term[1]);mass_lo+=w[0];self.cdf_terms+=1
   tail=max(0,self.S-mass_lo)
   if F(tail,self.S)<=tail_tolerance:return max(0,total[0]),min(self.S,total[1]+tail)
   w=self.times(w,lam/F(n+1));t=self.times(t,x/F(alpha+n));prefix=(prefix[0]+t[0],prefix[1]+t[1])
  raise Unknown('noncentral-Gamma series budget')

def certify(raw,*,initial_state,protocol,beta=F(1),kappa=F(1),threshold,cdf_absolute_error=F(1,10**8),precision_bits=256,
 max_segments=1024,max_dimension=1024,max_terms=100000,max_coefficient_bits=4096,max_exponent_entries=64000000,max_total_coefficient_bits=32000000,max_rational_bits=1000000,
 max_operations=10000000,max_integer_bits=1000000,max_exp_terms=16384,max_series_terms=100000):
 start=time.perf_counter();args=locals().copy();args.pop('start');args.pop('raw')
 for key in ['precision_bits','max_segments','max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits','max_operations','max_integer_bits','max_exp_terms','max_series_terms']:strict_int(args[key],key)
 if precision_bits<16 or precision_bits>max_integer_bits//2:raise Unknown('precision allocation budget')
 for key in ['beta','kappa','threshold','cdf_absolute_error']:
  q=frac(args[key],key,True)
  if max(q.numerator.bit_length(),q.denominator.bit_length())>max_coefficient_bits:raise Unknown('task rational bit budget')
 if cdf_absolute_error>=1:raise Unknown('CDF error must be less than one')
 if type(protocol)is not list or not 1<=len(protocol)<=max_segments:raise Unknown('protocol segment budget')
 for seg in protocol:
  if type(seg)is not dict or set(seg)!={'y','duration'}:raise Unknown('complete externally declared clamp protocol')
  frac(seg['y'],'clamp position');frac(seg['duration'],'duration',True)
  for q in seg.values():
   if max(q.numerator.bit_length(),q.denominator.bit_length())>max_coefficient_bits:raise Unknown('protocol rational bit budget')
 aq={k:args[k] for k in ['max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits']}
 info,u0,alpha=acquire(raw,initial_state,**aq)
 if alpha.denominator!=1:raise Unknown('finite CDF engine currently requires integer alpha; path-law theorem does not')
 ii=Fixed(precision_bits,max_operations,max_integer_bits,max_exp_terms,max_series_terms);S=ii.S
 E=(S,S);B=(0,0);duration=F(0);parameters=[]
 for seg in protocol:
  y=seg['y'];v=1+kappa*(1-y*y)**2;e=ii.expminus(v*seg['duration']);E=ii.mul(e,E)
  first=ii.mul(e,B);second=ii.times((S-e[1],S-e[0]),1/(beta*v));B=(first[0]+second[0],first[1]+second[1]);duration+=seg['duration']
  parameters.append({'v':fs(v),'duration':fs(seg['duration']),'E':enclosure(F(E[0],S),F(E[1],S)),'B':enclosure(F(B[0],S),F(B[1],S))})
 if B[0]<=0:raise Unknown('positive protocol diffusion scale unresolved')
 Elo,Ehi=F(E[0],S),F(E[1],S);Blo,Bhi=F(B[0],S),F(B[1],S)
 lamlo=Elo*u0/Bhi;lamhi=Ehi*u0/Blo;xlo=threshold/Bhi;xhi=threshold/Blo
 lower=ii.cdf_point(alpha.numerator,lamhi,xlo,cdf_absolute_error/8)[0]
 upper=ii.cdf_point(alpha.numerator,lamlo,xhi,cdf_absolute_error/8)[1]
 lo,hi=F(lower,S),F(upper,S)
 if not 0<=lo<=hi<=1 or hi-lo>cdf_absolute_error:raise Unknown('total requested CDF absolute width not certified')
 task={}
 for key,val in args.items():
  if type(val)is F:task[key]=fs(val)
  elif key=='initial_state':task[key]=[fs(x) for x in val]
  elif key=='protocol':task[key]=[{k:fs(v) for k,v in seg.items()} for seg in val]
  else:task[key]=val
 mean=(Elo*u0+alpha*Blo,Ehi*u0+alpha*Bhi);variance=(2*Elo*Blo*u0+alpha*Blo*Blo,2*Ehi*Bhi*u0+alpha*Bhi*Bhi)
 return {'schema':'exact_homogeneous_kinetic_clamped_cdf.v1','task':task,'acquisition':info,
 'operation':'terminal energy CDF for the actual externally clamped radial-plus-tangent divergence-form model',
 'not_claimed':['autonomous Y hitting time','original constant-mobility dynamics','physical membership or actuation','angular equilibrium sampling'],
 'law':'u_T/B | N ~ Gamma(alpha+N,rate=1), N~Poisson(E*u0/B)',
 'parameters':parameters,'total_protocol_duration':fs(duration),'terminal_CDF':enclosure(lo,hi),'terminal_mean':enclosure(*mean),'terminal_variance':enclosure(*variance),
 'work':{'fixed_operations':ii.operations,'largest_guarded_product_bits':ii.max_guarded_bits,'exponential_calls':ii.exp_calls,'Taylor_terms':ii.exp_terms,'Poisson_series_terms':ii.cdf_terms},'seconds':time.perf_counter()-start}

def verify(raw,certificate,**external_task):
 exp=certify(raw,**external_task)
 if type(certificate)is not dict:raise Unknown('certificate object')
 for key in ['schema','task','acquisition','operation','not_claimed','law','total_protocol_duration']:
  if not same(certificate.get(key),exp[key]):raise Unknown('external model/task binding: '+key)
 for key in ['terminal_CDF','terminal_mean','terminal_variance']:
  if type(certificate.get(key))is not dict:raise Unknown('interval schema')
  for side in ['lower','upper']:
   if not same(certificate[key].get(side),exp[key][side]):raise Unknown('exact endpoint binding: '+key)
 ps=certificate.get('parameters')
 if type(ps)is not list or len(ps)!=len(exp['parameters']):raise Unknown('protocol parameter sequence')
 for a,b in zip(ps,exp['parameters']):
  if type(a)is not dict or set(a)!=set(b):raise Unknown('protocol parameter schema')
  for key in ['v','duration']:
   if not same(a[key],b[key]):raise Unknown('protocol parameter binding')
  for key in ['E','B']:
   if type(a[key])is not dict:raise Unknown('protocol parameter interval')
   for side in ['lower','upper']:
    if not same(a[key].get(side),b[key][side]):raise Unknown('protocol exact interval binding')
 return {'status':'PASS','scope':exp['operation'],'m':exp['acquisition']['m'],'cdf_width_exact':fs(F(exp['terminal_CDF']['upper'])-F(exp['terminal_CDF']['lower'])),'physical_membership':'not authenticated'}

def fixture(m=8,p=4,coupling=F(20),tangent=F(1)):
 terms=[]
 for i in range(m):
  powers=[0]*m;powers[i]=p;terms.append({'powers':powers,'coefficient':'1'})
 if p==4 and coupling>0:
  for i in range(m-1):
   powers=[0]*m;powers[i]=powers[i+1]=2;terms.append({'powers':powers,'coefficient':fs(coupling)})
 return {'dimension':m,'energy_terms':terms,'tangent_program':{'kind':'complete_pair_gradient','weight':fs(tangent)}}

def external_from_record(record):
 t=dict(record['task'])
 for k in ['beta','kappa','threshold','cdf_absolute_error']:t[k]=F(t[k])
 t['initial_state']=[F(x) for x in t['initial_state']]
 t['protocol']=[{k:F(v) for k,v in seg.items()} for seg in t['protocol']]
 return t

if __name__=='__main__':
 out=[]
 for m,coupling,tangent in [(4,F(0),F(0)),(8,F(20),F(1)),(512,F(20),F(1)),(512,F(10**100),F(10**80))]:
  raw=fixture(m,coupling=coupling,tangent=tangent);z0=[F(1)]+[F(0)]*(m-1)
  protocol=[{'y':F(-1),'duration':F(1,3)},{'y':F(0),'duration':F(1,2)},{'y':F(1,2),'duration':F(2,3)}]
  cert=certify(raw,initial_state=z0,protocol=protocol,threshold=F(m,8),cdf_absolute_error=F(1,10**10))
  out.append({'fixture':{'m':m,'p':4,'coupling':fs(coupling),'tangent':fs(tangent)},'certificate':cert})
  Path('results.json').write_text(json.dumps(out,indent=2)+'\n')
  print(m,fs(coupling),cert['terminal_CDF']['display'],cert['seconds'],flush=True)
