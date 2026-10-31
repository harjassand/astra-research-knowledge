from fractions import Fraction as F
from pathlib import Path
import copy,json,random,subprocess,sys
import receive_family as f
count=0;groups={}
def ok(x,g):
 global count
 assert x,g
 count+=1;groups[g]=groups.get(g,0)+1
def no(fn,g):
 try:fn()
 except f.Unknown:ok(True,g);return
 raise AssertionError('accepted '+g)
kw={'quad_relative':F(1,5),'full_ratio':F(2)};raw=f.base.fixture(3);c=f.certify(raw,**kw)
def leaves(x,p=()):
 if type(x)is dict:
  for k,v in x.items():yield from leaves(v,p+(k,))
 elif type(x)is list:
  for k,v in enumerate(x):yield from leaves(v,p+(k,))
 else:yield p,x
for group in ['kinetic_family','exact_attainable_set','task','acquisition']:
 for path,val in leaves(c[group]):
  if path[-1]=='seconds':continue
  d=copy.deepcopy(c);o=d[group]
  for k in path[:-1]:o=o[k]
  alias=0 if type(val)is bool else (float(val) if type(val)is int else 'not the accepted value')
  o[path[-1]]=alias;no(lambda d=d:f.verify(raw,d,**kw),'leaf_binding')
for key in ['schema','structural_method','finite_source_sha256','range_proof_sha256','family_task','numerical_scope','observable','b','basins']:
 d=copy.deepcopy(c);d.pop(key);no(lambda d=d:f.verify(raw,d,**kw),'missing_scope')
for key in ['mass','resistance','free_rate','jensen_resistance','structural_ratio','uniform_rate_enclosure']:
 for side in ['lower','upper']:
  d=copy.deepcopy(c);d[key][side]=str(F(d[key][side])+1);no(lambda d=d:f.verify(raw,d,**kw),'endpoint')
for x in ['all_SPD','arbitrary_physical_model','fixed_M','all_fixed_transverse_SPD ',None,True,1]:no(lambda x=x:f.certify(raw,family=x,**kw),'external_family')
for x in [None,[],True]:no(lambda x=x:f.verify(raw,x,**kw),'record')
for key in ['M','transverse_matrix','cross_mobility','longitudinal_mobility','physical_membership','control']:
 no(lambda key=key:f.certify(raw,**{key:1},**kw),'unimplemented_input')
for old in [f.engine.certify(raw,**kw),f.base.certify(raw,quad_relative=F(1,5))]:no(lambda old=old:f.verify(raw,old,**kw),'stale')
for key in ['full_rate','factor_upper']:
 d=copy.deepcopy(c);d[key]='stale';no(lambda d=d:f.verify(raw,d,**kw),'stale')
no(lambda:f.verify(raw,c,quad_relative=F(1,4),full_ratio=F(2)),'external_task')
no(lambda:f.verify(raw,c,quad_relative=F(1,5),full_ratio=F(3)),'external_task')
no(lambda:f.verify(f.base.fixture(3,coupling=F(21)),c,**kw),'raw_model')
# Same numerical values, distinct physical model records; no identification.
other=f.certify(f.base.fixture(3,graph='none',dmin=F(100),axis=2),**kw)
ok(other['uniform_rate_enclosure']==c['uniform_rate_enclosure'],'range_scope')
ok(other['acquisition']!=c['acquisition'],'range_scope')
ok(c['exact_attainable_set']['alpha']=='3/4' and c['exact_attainable_set']['endpoints_attained']is False,'range_scope')
a=f.family_descriptor();a['excluded'].clear();ok(len(f.family_descriptor()['excluded'])==6,'fresh')
a=f.range_descriptor(3);a['endpoints_attained']=True;ok(f.range_descriptor(3)['endpoints_attained']is False,'fresh')
# Exact 3D SPD inverse cancellations using explicit lower-triangular factor.
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def tr(A):return list(map(list,zip(*A)))
def inv(A):
 n=len(A);D=[row[:]+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
 for i in range(n):
  d=D[i][i];assert d;D[i]=[x/d for x in D[i]]
  for j in range(n):
   if i!=j:
    d=D[j][i];D[j]=[x-d*y for x,y in zip(D[j],D[i])]
 return [row[n:] for row in D]
rng=random.Random(1954)
for case in range(15):
 L=[[F(rng.randrange(-20,21),7) if j<i else F(0) for j in range(3)] for i in range(3)]
 for i in range(3):L[i][i]=F(i+1,10**(case%5))
 M=mm(L,tr(L));Mi=inv(M);I=mm(M,Mi);ok(I==[[F(i==j) for j in range(3)] for i in range(3)],'SPD_Lyapunov')
 z=[F(rng.randrange(-10,11),3) for _ in range(3)];U=sum(x**4 for x in z)+20*sum(z[i]**2*z[j]**2 for i in range(3) for j in range(i+1,3))
 grad=[4*z[i]**3+40*z[i]*sum(z[j]**2 for j in range(3) if j!=i) for i in range(3)]
 iz=[sum(Mi[i][j]*z[j] for j in range(3)) for i in range(3)];mg=[sum(M[i][j]*grad[j] for j in range(3)) for i in range(3)]
 ok(sum(iz[i]*mg[i] for i in range(3))==4*U,'SPD_Lyapunov')
# Actual import-hash failure: only copied proof in /tmp can be changed.
p=f.PROOF;assert p.resolve().is_relative_to(Path('/tmp'));old=p.read_bytes()
try:
 p.write_bytes(old+b'\n# audit tamper\n');run=subprocess.run([sys.executable,'-B','-c','import receive_family'],cwd=Path(__file__).parent,capture_output=True,text=True)
 ok(run.returncode!=0 and 'source hash mismatch' in run.stderr,'proof_hash')
finally:p.write_bytes(old)
print(json.dumps({'status':'PASS','independent_checks':count,'groups':groups},indent=2))
