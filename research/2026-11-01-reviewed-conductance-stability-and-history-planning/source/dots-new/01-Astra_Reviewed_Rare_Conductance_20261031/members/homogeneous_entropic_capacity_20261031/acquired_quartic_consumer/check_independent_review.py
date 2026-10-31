import importlib.util, json, copy, random, hashlib
from fractions import Fraction as F
from pathlib import Path
spec=importlib.util.spec_from_file_location('quartic',Path(__file__).with_name('compile.py')); c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
n=0; groups={}
def ok(x,g):
 global n
 assert x,g
 n+=1;groups[g]=groups.get(g,0)+1
def reject(f,g):
 try:f()
 except c.Unknown:ok(True,g);return
 raise AssertionError('accepted '+g)
rng=random.Random(87621)
# Exhaustive small perfect and inexact roots, independently using powered endpoints.
for deg in [2,4]:
 for num in range(17):
  for den in range(1,10):
   p=(num+den)%7; a=F(num,den);l,u=c.root_bounds(a,p,deg)
   ok(F(l,2**p)**deg<=a<=F(u,2**p)**deg and (u-l in (0,1)),'root_enclosure')
# General raw coefficients, non-first axis, unrelated diagonals and sparse graph.
def raw_model(m,axis,k,d,edges):
 n=m+1; fib=[i for i in range(n) if i!=axis]; terms=[]
 for coords,a in [([fib[i]]*4,d[i]) for i in range(m)]+[([fib[i]]*2+[fib[j]]*2,a) for i,j,a in edges]:
  p=[0]*n
  for j in coords:p[j]+=1
  for e,f in [(0,1+k),(2,-2*k),(4,k)]:
   pp=p.copy();pp[axis]=e;terms.append({'powers':pp,'coefficient':str(a*f)})
 return {'n':n,'terms':terms}
models=[]
for axis in range(4):
 raw=raw_model(3,axis,F(3,5),[F(2,7),F(9),F(1,3)],[(0,2,F(123,7))]);ac=c.acquire(raw)
 ok(ac['axis']==axis and ac['d_min']=='2/7' and ac['coercivity_a']=='2/21' and ac['kappa']=='3/5','acquisition')
 cert=c.certify(raw,beta=F(7,3),quad_relative=F(1,10));ok(c.verify(raw,cert,beta=F(7,3),quad_relative=F(1,10))['status']=='PASS','receiver')
 fac=F(cert['factor_upper']);v=1+F(9,16)*F(3,5)
 ok((fac-1)**2>=F(3,5)**2/(4*F(7,3)*F(2,7)*v**3),'factor_outward')
 models.append((raw,cert))
# Full identity corruption: positive/minus/omitted terms, including missing-coordinate ambiguity.
raw=c.fixture(2);cert=c.certify(raw,quad_relative=F(1,5))
for i in range(len(raw['terms'])):
 for mutation in ['drop','negative','add']:
  b=copy.deepcopy(raw)
  if mutation=='drop':b['terms'].pop(i)
  elif mutation=='negative':b['terms'][i]['coefficient']=str(-F(b['terms'][i]['coefficient']))
  else:b['terms'][i]['coefficient']=str(F(b['terms'][i]['coefficient'])+F(1,101))
  reject(lambda b=b:c.acquire(b),'raw_mutation')
for bad in [None,[],True,{'n':3,'terms':[]},{'n':True,'terms':raw['terms']},{**raw,'extra':0}]:reject(lambda bad=bad:c.acquire(bad),'schema')
for val in ['+1','1.0',' 1','1/1','-0','1e2','0/1',True,1.0,float('nan')]:
 b=copy.deepcopy(raw);b['terms'][0]['coefficient']=val;reject(lambda b=b:c.acquire(b),'rational_schema')
# Recursive certificate aliases in every numeric proof field, plus nested graph/diagonals.
def integer_paths(obj,path=()):
 if type(obj)is int:yield path,obj
 elif type(obj)is dict:
  for k,v in obj.items():
   if k!='seconds':yield from integer_paths(v,path+(k,))
 elif type(obj)is list:
  for k,v in enumerate(obj):yield from integer_paths(v,path+(k,))
proof={'acquisition':cert['acquisition'],'task':cert['task'],'N':cert['N'],'precision_bits':cert['precision_bits']}
for path,value in integer_paths(proof):
 for alias in [float(value),bool(value)]:
  b=copy.deepcopy(cert);o=b
  for k in path[:-1]:o=o[k]
  o[path[-1]]=alias
  reject(lambda b=b:c.verify(raw,b,quad_relative=F(1,5)),'typed_receiver')
for key in ['mass','resistance','free_rate','full_rate']:
 for side in ['lower','upper']:
  b=copy.deepcopy(cert);b[key][side]=str(F(b[key][side])+1)
  reject(lambda b=b:c.verify(raw,b,quad_relative=F(1,5)),'interval_tamper')
for key,value in [('T','1'),('tail_upper','0'),('factor_upper','1'),('observable','MFPT'),('b','1'),('schema',None)]:
 b=copy.deepcopy(cert);b[key]=value;reject(lambda b=b:c.verify(raw,b,quad_relative=F(1,5)),'task_tamper')
for kw in [{'beta':F(2)},{'max_grid':65536},{'quad_relative':F(1,4)}]:reject(lambda kw=kw:c.verify(raw,cert,**kw),'external_task')
# Tail is an actual power envelope; m=2 is included and T-pieces are geometrically paid.
for m in [2,3,7]:
 ii=c.Integrator(m,F(3,7),128,10000,100000)
 for T in [F(2),F(4),F(16)]:
  tail=ii.tail(T); exact_power= (1/(F(3,7)*(1-1/T**2)**2))**m
  ok((tail*(m-1)/T**(1-m))**4>=exact_power,'tail_outward')
  for y in [T,2*T,3*T]:
   v=1+F(3,7)*(1-y*y)**2
   ok(v>=F(3,7)*y**4*(1-1/T**2)**2,'tail_point')
# Guard rejects before expensive exponentiation; operation count remains zero.
ii=c.Integrator(5,F(1),192,1000,100)
reject(lambda:ii.power(F(3,2),5),'power_budget');ok(ii.power_calls==0,'power_budget')
for kw in [{'max_points':32},{'max_grid':63},{'max_precision':191},{'max_cutoff':1},{'max_power_bits':700}]:reject(lambda kw=kw:c.certify(raw,**kw),'budget')
# Exact graph insensitivity is only of this common certified enclosure.
for graph,coupling in [('none',F(1)),('complete',F(10**40))]:
 cc=c.certify(c.fixture(2,graph=graph,coupling=coupling),quad_relative=F(1,5))
 ok(cc['full_rate']==cert['full_rate'],'graph_bound')
# Verify every saved certificate from actual raw coefficients (not displays).
saved=json.loads(Path(__file__).with_name('results.json').read_text())
for row in saved:
 f=row['fixture'];rr=c.fixture(f['m'],graph=f['graph'],coupling=F(f['coupling']))
 ok(c.verify(rr,row['certificate'])['status']=='PASS','saved')
rr=json.loads(Path(__file__).with_name('dense_graph_raw.json').read_text());cc=json.loads(Path(__file__).with_name('dense_graph_certificate.json').read_text());ok(c.verify(rr,cc)['status']=='PASS','saved')
print(json.dumps({'status':'PASS','independent_checks':n,'groups':groups},indent=2))
