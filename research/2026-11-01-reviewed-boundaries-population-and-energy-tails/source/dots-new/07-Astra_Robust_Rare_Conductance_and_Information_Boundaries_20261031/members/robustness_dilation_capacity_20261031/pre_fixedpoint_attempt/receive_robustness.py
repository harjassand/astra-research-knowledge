"""Exact raw radial-envelope capacity receiver. No partition or angular solver."""
from pathlib import Path
import hashlib,importlib.util,json
from math import comb,isqrt
from time import perf_counter
BASE_PATH=Path(__file__).resolve().parents[1]/'dilation_partition_free_20261031'/'receive_dilation.py'
BASE_SHA='d760c77b7efaa81bdb3ee424fd818359840d1da767fba4398c177a63f93bf4e8'
if hashlib.sha256(BASE_PATH.read_bytes()).hexdigest()!=BASE_SHA:raise RuntimeError('accepted dependency hash mismatch')
_spec=importlib.util.spec_from_file_location('accepted_dilation_backend',BASE_PATH);base=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(base)
F=base.F;Unknown=base.Unknown;fs=base.fs;bits=base.bits;interval=base.interval;same_typed=base.same_typed

def trim(a):
 a=list(a)
 while len(a)>1 and not a[-1]:a.pop()
 return a or [F(0)]
def add(a,b):
 c=[F(0)]*max(len(a),len(b))
 for i,x in enumerate(a):c[i]+=x
 for i,x in enumerate(b):c[i]+=x
 return trim(c)
def scale(a,c):return trim([x*c for x in a])
def mul(a,b):
 c=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return trim(c)
def ppow(a,n):
 c=[F(1)]
 for _ in range(n):c=mul(c,a)
 return c

def error_numerator(shape):
 if shape=='well_sensitive':return [F(0),F(1),F(2),F(1)]
 if shape=='critical_flat':return [F(0),F(1),F(-2),F(1)]
 raise Unknown('unsupported scalar envelope shape')
def error_max(shape):return F(1,4) if shape=='well_sensitive' else F(1,16)
def scalar_poly(kappa,delta,shape,d):
 s=[1+kappa,-2*kappa,kappa];B=add(ppow([F(1),F(1)],4),scale(error_numerator(shape),delta))
 return mul(ppow(mul(s,B),d),ppow([F(1),F(1)],16-4*d))

class Bernstein:
 """Sufficient budgeted nonnegativity certificate on t>=0."""
 def __init__(self,max_nodes,max_depth,max_bits):
  self.max_nodes=max_nodes;self.max_depth=max_depth;self.max_bits=max_bits
  self.nodes=0;self.leaves=0;self.peak_bits=0;self.depth=0
 def guard(self,b):
  peak=max(bits(x) for x in b);self.peak_bits=max(self.peak_bits,peak)
  if peak>self.max_bits:raise Unknown('Bernstein stored-coefficient bit budget')
 def positive(self,p):
  p=trim(p);D=len(p)-1;stack=[([a/F(comb(D,i)) for i,a in enumerate(p)],0)]
  while stack:
   b,dep=stack.pop();self.nodes+=1;self.depth=max(self.depth,dep)
   if self.nodes>self.max_nodes:raise Unknown('total Bernstein-node budget')
   self.guard(b)
   if min(b)>=0:self.leaves+=1;continue
   if b[0]<0 or b[-1]<0 or max(b)<=0:raise Unknown('radial-envelope polynomial negative somewhere')
   if dep>=self.max_depth:raise Unknown('polynomial not certified within Bernstein depth')
   rows=[b]
   while len(rows[-1])>1:
    row=[(x+y)/2 for x,y in zip(rows[-1][:-1],rows[-1][1:])];self.guard(row);rows.append(row)
   if rows[-1][0]<0:raise Unknown('radial-envelope polynomial negative at dyadic point')
   stack.append(([r[-1] for r in reversed(rows)],dep+1));stack.append(([r[0] for r in rows],dep+1))

def acquire(raw,delta,shape,max_dimension=1024,max_terms=100000,max_coefficient_bits=65536,
 max_exponent_entries=64000000,max_total_coefficient_bits=32000000,max_bernstein_nodes=100000,
 max_bernstein_depth=16,max_bernstein_bits=1000000):
 start=perf_counter()
 if type(delta)is not F or delta<0:raise Unknown('strict nonnegative Fraction delta')
 error_numerator(shape)
 for k,v in list(locals().items()):
  if k.startswith('max_'):base.positive_int(v,k)
 if bits(delta)>max_coefficient_bits:raise Unknown('delta bit budget')
 if type(raw)is not dict or set(raw)!={'n','denominator','terms'}:raise Unknown('raw rational-potential schema')
 n=raw['n'];records=raw['terms'];den=raw['denominator']
 if type(n)is not int or not 2<=n<=max_dimension:raise Unknown('physical dimension budget')
 if type(den)is not dict or set(den)!={'axis','power'} or type(den['axis'])is not int or type(den['power'])is not int or not 0<=den['axis']<n or den['power']!=16:raise Unknown('exact positive denominator syntax')
 if type(records)is not list or not 0<len(records)<=max_terms or n*len(records)>max_exponent_entries:raise Unknown('raw term/exponent-entry budget')
 terms={};total_bits=0
 for rec in records:
  if type(rec)is not dict or set(rec)!={'powers','coefficient'}:raise Unknown('raw monomial schema')
  v=rec['powers']
  if type(v)is not list or len(v)!=n or any(type(x)is not int or not 0<=x<=52 for x in v):raise Unknown('strict numerator exponents')
  v=tuple(v)
  if v in terms or not 2<=sum(v)<=52:raise Unknown('duplicate/unsupported numerator degree')
  q=base.decode_rational(rec['coefficient'],max_coefficient_bits)
  if not q:raise Unknown('zero numerator term')
  total_bits+=bits(q)
  if total_bits>max_total_coefficient_bits:raise Unknown('total input coefficient-bit budget')
  terms[v]=q
 diag={}
 for v,q in terms.items():
  if sum(v)!=2:continue
  support=[i for i,a in enumerate(v) if a]
  if len(support)!=1 or v[support[0]]!=2 or q<=0:raise Unknown('positive aligned quadratic anchor')
  diag[support[0]]=q
 absent=set(range(n))-set(diag)
 if len(absent)!=1:raise Unknown('no unique quadratic null axis')
 axis=next(iter(absent))
 if axis!=den['axis']:raise Unknown('acquired axis differs from denominator')
 profiles={};degrees={}
 for v,q in terms.items():
  if v[axis]%2:raise Unknown('even macro profile needed for basin symmetry')
  j=v[axis]//2;w=list(v);w[axis]=0;w=tuple(w);d=sum(w);supp=[i for i,a in enumerate(w) if a]
  valid=(d==2 and len(supp)==1 and w[supp[0]]==2) or (d==4 and ((len(supp)==1 and w[supp[0]]==4) or(len(supp)==2 and all(w[i]==2 for i in supp))))
  if not valid or j>16+2*d:raise Unknown('transverse atom/macro-degree grammar')
  if w not in profiles:profiles[w]=[F(0)]*(17+2*d);degrees[w]=d
  profiles[w][j]=q
 first=next(w for w in profiles if degrees[w]==2);a=profiles[first]
 if a[0]<=0 or a[-1]<=0:raise Unknown('positive anchor/tail needed')
 ratio=a[-1]/a[0];r=F(isqrt(ratio.numerator),isqrt(ratio.denominator))
 if r*r!=ratio or not 0<r<1:raise Unknown('exact rational nominal-parameter root not acquired')
 kappa=r/(1-r);s0=1+kappa
 if delta>kappa/(2*s0):raise Unknown('envelope monotonicity delta budget')
 h=min(F(1,8),kappa/2)*(1-delta*error_max(shape));K=F(1);qmin=None
 proof=Bernstein(max_bernstein_nodes,max_bernstein_depth,max_bernstein_bits);cache={};nominal={};count2=count4=0
 for w,N in profiles.items():
  d=degrees[w]
  if N[0]<=0:raise Unknown('every atom needs positive anchor')
  cj=N[0]/s0**d;P=trim([x/cj for x in N]);key=(d,tuple(P))
  if d==2:count2+=1;qmin=cj if qmin is None else min(qmin,cj)
  else:count4+=1
  if key not in cache:
   if d not in nominal:nominal[d]=(scalar_poly(kappa,-delta,shape,d),scalar_poly(kappa,delta,shape,d))
   lo,hi=nominal[d];proof.positive(add(P,scale(lo,-1)));proof.positive(add(hi,scale(P,-1)));cache[key]=True
  K=max(K,1+(2*(len(P)-1)*sum(abs(x) for x in P)/h**d+32)/d)
 if count2!=n-1:raise Unknown('missing quadratic coercivity')
 digest=hashlib.sha256(('robust_rational_potential.v1;n='+str(n)+';axis='+str(axis)+';denpower=16\n').encode())
 for v in sorted(terms):digest.update((json.dumps([list(v),fs(terms[v])],separators=(',',':'))+'\n').encode())
 return {'route':'quadratic_axis_tail_anchor_nominal_and_complete_univariate_radial_envelopes','n':n,'m':n-1,'axis':axis,
  'kappa':fs(kappa),'degree_cap':max(degrees.values()),'shape':shape,'delta':fs(delta),'anchor_q_min':fs(qmin),
  'lyapunov_K':fs(K),'raw_terms':len(terms),'raw_exponent_entries':n*len(terms),'total_input_coefficient_bits':total_bits,
  'quadratic_atoms':count2,'quartic_atoms':count4,'distinct_normalized_profiles':len(cache),
  'bernstein_nodes':proof.nodes,'bernstein_leaves':proof.leaves,'bernstein_depth':proof.depth,'bernstein_peak_stored_bits':proof.peak_bits,
  'raw_potential_sha256':digest.hexdigest(),'anchor_energy':'nonnegative mixed components; no partition or angular solve',
  'actual_potential':'received by global inequalities, not asserted exact dilation','seconds':perf_counter()-start}

class Integrator(base.Integrator):
 def __init__(self,m,kappa,d,delta,shape,P,max_evaluations,max_power_bits):
  super().__init__(m,kappa,d,P,max_evaluations,max_power_bits);self.delta=delta;self.shape=shape
 def profiles_at(self,y):
  if y not in self.profiles:
   t=y*y;s=1+self.kappa*(1-t)**2;e=t/(1+t)**2 if self.shape=='well_sensitive' else t*(t-1)**2/(1+t)**4
   self.profiles[y]=(s*(1-self.delta*e),s*(1+self.delta*e))
  return self.profiles[y]
 def point(self,kind,y):
  key=(kind,y)
  if key in self.cache:return self.cache[key]
  if len(self.cache)>=self.max_evaluations:raise Unknown('total scalar-evaluation budget')
  l,u=self.profiles_at(y)
  if kind=='ql':ans=self.bounds(l,-self.m)
  elif kind=='qu':ans=self.bounds(u,-self.m)
  elif kind=='r0':
   if not 0<=y<=F(1,2):raise Unknown('resistance outside half slab')
   ans=self.bounds(l,self.m)
  elif kind=='rp':
   if not 0<=y<=F(1,2):raise Unknown('Jensen resistance outside half slab')
   ans=self.bounds(self.s02p/(2*self.s0p-self.power(u,self.d)),self.m,self.d)
  else:raise Unknown('unknown scalar integrand')
  self.cache[key]=ans;return ans
 def tail(self,T,kind='ql'):
  self.tail_calls+=1;b=1/(self.kappa*(1-1/(T*T))**2)
  if kind=='ql':b/=1-self.delta*error_max(self.shape)
  elif kind!='qu':raise Unknown('tail type')
  return self.power(b,self.m)*self.power(T,1-4*self.m)/(4*self.m-1)

def certify(raw,delta,shape='critical_flat',beta=F(1),quad_relative=F(1,100),full_ratio=None,
 max_dimension=1024,max_terms=100000,max_coefficient_bits=65536,max_exponent_entries=64000000,
 max_total_coefficient_bits=32000000,max_bernstein_nodes=100000,max_bernstein_depth=16,max_bernstein_bits=1000000,
 max_grid=131072,max_evaluations=2000000,max_cutoff=65536,max_precision=16384,max_power_bits=4000000):
 start=perf_counter();task=locals().copy();del task['raw'];del task['start']
 for k in ['beta','quad_relative']:
  if type(task[k])is not F or task[k]<=0:raise Unknown('strict positive Fraction '+k)
 if type(delta)is not F or delta<0:raise Unknown('strict nonnegative Fraction delta')
 error_numerator(shape)
 if full_ratio is not None and(type(full_ratio)is not F or full_ratio<=1):raise Unknown('strict total ratio Fraction>1')
 for k,v in task.items():
  if k.startswith('max_'):base.positive_int(v,k)
 if max_grid<64 or max_cutoff<2:raise Unknown('initial grid/cutoff budget')
 if max(bits(beta),bits(delta),bits(quad_relative),bits(full_ratio) if full_ratio else 0)>max_coefficient_bits:raise Unknown('task rational bit budget')
 keys=['delta','shape','max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_bernstein_nodes','max_bernstein_depth','max_bernstein_bits']
 acq=acquire(raw,**{k:task[k] for k in keys});m=acq['m'];k=F(acq['kappa']);d=acq['degree_cap'];P=max(192,m*(bits(k)+4)+128)
 if P>max_precision:raise Unknown('fixed precision budget')
 ii=Integrator(m,k,d,delta,shape,P,max_evaluations,max_power_bits);seed=ii.integrate(F(1),F(5,4),32,'qu')[0]
 if seed<=0:raise Unknown('unresolved positive seed')
 T=F(2)
 while ii.tail(T,'ql')>quad_relative*seed/16:
  T*=2
  if T>max_cutoff:raise Unknown('tail cutoff budget')
 N=64
 while True:
  if N>max_grid:raise Unknown('quadrature grid budget')
  if N*(2*T.numerator.bit_length()+2)+4>max_evaluations:raise Unknown('necessary final point budget')
  masses={}
  for kind in ['ql','qu']:
   ml,mu=ii.integrate(F(1,2),F(1),N,kind);a=F(1)
   while a<T:
    lo,hi=ii.integrate(a,2*a,N,kind);ml+=lo;mu+=hi;a*=2
   masses[kind]=(ml,mu+ii.tail(T,kind))
  a,b=ii.integrate(F(0),F(1,2),N,'r0');r0=2*a,2*b
  a,b=ii.integrate(F(0),F(1,2),N,'rp');rp=2*a,2*b
  pl=pu=F(1)
  for lo,hi in [masses['ql'],masses['qu'],r0,rp]:pl*=lo;pu*=hi
  if pl>0 and pu<=(1+quad_relative)*pl:break
  N*=2
 low=1/(beta*masses['ql'][1]*rp[1]);high=1/(beta*masses['qu'][0]*r0[0]);ratio=high/low
 if full_ratio is not None and ratio>full_ratio:raise Unknown('robust OUTER interval misses requested TOTAL ratio')
 return {'schema':'acquired_radial_envelope_conductance.v1','dependency_sha256':BASE_SHA,
  'method':'unnormalized_capacity_and_basin_comparison_common_unknown_anchor_partition',
  'task':{k:fs(v) if type(v)is F else v for k,v in task.items()},'acquisition':acq,
  'mobility_family':base.family_descriptor(),'observable':'for every declared M: cap_mu,M(A,B)/mu(A)',
  'basins':'acquired full fibers x[axis]<=-1/2 and x[axis]>=1/2',
  'mass_lower_profile':interval(masses['ql']),'mass_upper_profile':interval(masses['qu']),
  'resistance_lower_profile':interval(r0),'jensen_upper_profile':interval(rp),
  'uniform_rate_enclosure':interval((low,high)),'full_ratio_exact':fs(ratio),'N':N,'T':fs(T),'precision_bits':P,
  'tail_lower_profile':fs(ii.tail(T,'ql')),'tail_upper_profile':fs(ii.tail(T,'qu')),
  'scalar_evaluations':len(ii.cache),'profile_evaluations':len(ii.profiles),'power_calls':ii.power_calls,
  'max_power_integer_bits':ii.max_power_integer_bits,'numerical_product_ratio_display':base.show(pu/pl),'seconds':perf_counter()-start}

def verify(raw,certificate,**external_task):
 exp=certify(raw,**external_task)
 if type(certificate)is not dict:raise Unknown('certificate schema')
 for k in ['schema','dependency_sha256','method','task','mobility_family','observable','basins','full_ratio_exact','N','T','precision_bits','tail_lower_profile','tail_upper_profile']:
  if not same_typed(certificate.get(k),exp[k]):raise Unknown('original task/model binding: '+k)
 ac=certificate.get('acquisition')
 if type(ac)is not dict or not same_typed({k:v for k,v in ac.items() if k!='seconds'},{k:v for k,v in exp['acquisition'].items() if k!='seconds'}):raise Unknown('complete raw/envelope binding')
 for k in ['mass_lower_profile','mass_upper_profile','resistance_lower_profile','jensen_upper_profile','uniform_rate_enclosure']:
  if type(certificate.get(k))is not dict:raise Unknown('interval schema')
  for side in ['lower','upper']:
   if not same_typed(certificate[k].get(side),exp[k][side]):raise Unknown('exact endpoint binding')
 return {'status':'PASS','scope':'acquired non-geometric rational potential; universal fixed-SPD conductance OUTER interval',
  'physical_m':exp['acquisition']['m'],'full_ratio_exact':exp['full_ratio_exact'],'actual_physical_membership':'not authenticated'}

def fixture(m,delta=F(1,500),shape='critical_flat',kappa=F(1),axis=0,angular_scale=F(1),mixed=True,heterogeneous=True):
 n=m+1;fiber=[i for i in range(n) if i!=axis];atoms=[]
 for i in fiber:
  v=[0]*n;v[i]=2;atoms.append((v,2,angular_scale))
  if mixed:v=[0]*n;v[i]=4;atoms.append((v,4,angular_scale))
 if mixed:
  for i,j in zip(fiber[:-1],fiber[1:]):
   v=[0]*n;v[i]=v[j]=2;atoms.append((v,4,20*angular_scale))
 records=[]
 for idx,(v,d,cj) in enumerate(atoms):
  e=delta*F([-1,0,1][idx%3],2) if heterogeneous else delta
  for j,q in enumerate(scalar_poly(kappa,e,shape,d)):
   if q:
    w=v.copy();w[axis]=2*j;records.append({'powers':w,'coefficient':fs(cj*q)})
 return {'n':n,'denominator':{'axis':axis,'power':16},'terms':records}

if __name__=='__main__':
 out=[]
 for m,delta,shape,num,target in [(2,F(1,100),'critical_flat',F(1,100),None),(16,F(1,100),'critical_flat',F(1,100),None),
  (128,F(1,500),'critical_flat',F(1,200),None),(512,F(1,500),'critical_flat',F(1,2000),F(101,100)),
  (512,F(1,100000),'well_sensitive',F(1,2000),F(101,100))]:
  t=perf_counter();raw=fixture(m,delta,shape);generation=perf_counter()-t
  cert=certify(raw,delta=delta,shape=shape,quad_relative=num,full_ratio=target);out.append({'m':m,'fixture_seconds':generation,'certificate':cert})
  print(json.dumps({'m':m,'shape':shape,'delta':fs(delta),'raw_terms':cert['acquisition']['raw_terms'],'profiles':cert['acquisition']['distinct_normalized_profiles'],
   'bernstein_nodes':cert['acquisition']['bernstein_nodes'],'low':cert['uniform_rate_enclosure']['lower_display'],'high':cert['uniform_rate_enclosure']['upper_display'],
   'ratio':base.show(F(cert['full_ratio_exact'])),'evaluations':cert['scalar_evaluations'],'seconds':cert['seconds']}),flush=True)
  Path('results.json').write_text(json.dumps(out,indent=2))
 raw=fixture(2,axis=2);cert=certify(raw,delta=F(1,500))
 Path('small_raw_fixture.json').write_text(json.dumps(raw,indent=2));Path('small_certificate.json').write_text(json.dumps(cert,indent=2))
