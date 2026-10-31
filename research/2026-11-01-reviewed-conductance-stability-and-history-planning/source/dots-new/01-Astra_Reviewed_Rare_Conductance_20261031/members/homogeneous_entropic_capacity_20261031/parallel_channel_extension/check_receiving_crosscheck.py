from fractions import Fraction as F
from pathlib import Path
import receive_parallel as r
import copy,json,subprocess,sys
count=0;groups={}
def ok(x,g):
 global count
 assert x,g
 count+=1;groups[g]=groups.get(g,0)+1
def no(fn,g):
 try:fn()
 except r.Unknown:ok(True,g);return
 raise AssertionError(g)
for k in [F(1,100),F(1,3),F(1),F(19),F(100)]:
 raw=r.base.fixture(3,kappa=k,axis=2,graph='none');c=r.certify(raw,quad_relative=F(1,5));sq=(16+23*k)/(14*(1+k));fac=F(c['factor_upper']);p=c['precision_bits']
 ok(c['factor_squared_exact']==str(sq),'factor');ok(fac**2>=sq and (fac-F(1,2**p))**2<sq,'factor');ok(sq<F(23,14) and sq>F(8,7),'factor')
 ok(F(c['full_rate']['lower'])*fac==F(c['free_rate']['lower']) and c['full_rate']['upper']==c['free_rate']['upper'],'endpoint')
 ok(r.verify(raw,c,quad_relative=F(1,5))['status']=='PASS','receiver')
raw=r.base.fixture(2);c=r.certify(raw,quad_relative=F(1,5))
def leaves(x,p=()):
 if type(x)is int:yield p,x
 elif type(x)is dict:
  for k,v in x.items():
   if k!='seconds':yield from leaves(v,p+(k,))
 elif type(x)is list:
  for k,v in enumerate(x):yield from leaves(v,p+(k,))
for path,val in leaves({k:c[k] for k in ['acquisition','task','N','precision_bits']}):
 for a in [float(val),bool(val)]:
  d=copy.deepcopy(c);o=d
  for k in path[:-1]:o=o[k]
  o[path[-1]]=a;no(lambda d=d:r.verify(raw,d,quad_relative=F(1,5)),'typed')
for field in ['schema','structural_method','scalar_source_sha256','factor_squared_exact','factor_upper','b','observable','basins','T','tail_upper']:
 d=copy.deepcopy(c);d[field]='invalid';no(lambda d=d:r.verify(raw,d,quad_relative=F(1,5)),'binding')
for field in ['mass','resistance','free_rate','full_rate']:
 for side in ['lower','upper']:
  d=copy.deepcopy(c);d[field][side]=str(F(d[field][side])+1);no(lambda d=d:r.verify(raw,d,quad_relative=F(1,5)),'endpoints')
for kw in [{'beta':F(2)},{'quad_relative':F(1,4)},{'max_grid':65536},{'ghost':0}]:no(lambda kw=kw:r.verify(raw,c,**kw),'external')
for x in [None,[],True]:no(lambda x=x:r.verify(raw,x,quad_relative=F(1,5)),'record')
for row in json.loads(Path(__file__).with_name('parallel_results.json').read_text()):ok(r.verify(r.base.fixture(row['m']),row['certificate'])['status']=='PASS','saved')
# Runtime dependency pin: mutate ONLY temporary copy, must reject before import.
p=r.SOURCE
if not p.resolve().is_relative_to(Path('/tmp')): raise RuntimeError('Run this hash-tamper test only in a /tmp copy with copied sibling engine')
old=p.read_bytes()
try:
 p.write_bytes(old+b'\n# independent tamper test\n')
 proc=subprocess.run([sys.executable,'-B','-c','import receive_parallel'],cwd=Path(__file__).parent,capture_output=True,text=True)
 ok(proc.returncode!=0 and 'source hash mismatch' in proc.stderr,'hash_pin')
finally:p.write_bytes(old)
print(json.dumps({'status':'PASS','independent_checks':count,'groups':groups},indent=2))
