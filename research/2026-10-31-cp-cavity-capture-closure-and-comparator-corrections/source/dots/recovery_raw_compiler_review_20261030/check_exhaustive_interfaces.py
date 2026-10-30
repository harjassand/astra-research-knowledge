"""Independent finite interface regression, not an infinite-state proof."""
import importlib.util,itertools,json,copy
from fractions import Fraction as F
from pathlib import Path
root=Path(__file__).parent
spec=importlib.util.spec_from_file_location('finder',root/'sources/acquire.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
raw=json.loads((root/'sources/raw_inputs.json').read_text())
# Generic accepted case not needing both original seeds: restore reaction-cycle
# access to 2D through A+D -> 2D instead.
v=copy.deepcopy(raw['original']);v['reactions']=[r for r in v['reactions'] if r['name']!='seed2']
v['reactions'].append(dict(name='A_to_D',source=dict(A=3,D=1,B=5),target=dict(A=2,D=2,B=5),rate='2/3'))
raw['one_seed_with_baseline_return']=v
# Read the predecessor's independently constructed generic accepted mutations.
old=json.loads((root.parent/'recovery_graph_profile_review_20261030/test_raw_compiler_challenge.json').read_text())
results={}
for name,net in raw.items():
 cert=m.acquire(net)
 if cert['status']!='CERTIFICATE_FOUND':results[name]={'status':cert['status']};continue
 ns=cert['residual_species'];A=ns.index(cert['connector']['A']);D=ns.index(cert['pivot']);a0=cert['connector']['a0'];B=cert['connector']['B'];q=cert['connector']['q'];pools=cert['pool_certificate']['pools'];dp=cert['pool_certificate']['protected_pool']
 rr=[]
 for r in net['reactions']:
  if r['source'].get(B,0)!=q or r['target'].get(B,0)!=q:continue
  y=[r['source'].get(s,0)-(a0 if i==A else 0) for i,s in enumerate(ns)]
  z=[r['target'].get(s,0)-(a0 if i==A else 0) for i,s in enumerate(ns)]
  assert min(y+z)>=0 and sum(y)==sum(z)==2
  rr.append((r['name'],y,z,F(r['rate'])))
 rest=[r for r in rr if r[1][D]==0 and r[1][A]!=2]
 def rate(y,k,x):
  for s,j in enumerate(y):
   for h in range(j):k*=x[s]-h
  return k
 def mix(x):return x[D]==0 and any(all(v>=w for v,w in zip(x,r[1])) for r in rest)
 states=0;checks=0
 for x in itertools.product(range(8),repeat=len(ns)):
  if not 2<=sum(x)<=7:continue
  states+=1
  for _,y,z,k in rr:
   if not all(v>=w for v,w in zip(x,y)):continue
   out=tuple(v+b-a for v,a,b in zip(x,y,z))
   # exact active indicator preserved by every residual move
   active=lambda t:t[D]>0 or mix(t) or t[A]>=2
   assert active(x)==active(out),(name,x,y,z,out)
   if x[D]>0 and out[D]==0 and not mix(out):assert out[A]>=2
   checks+=1
  if x[D]==0:continue
  Y=[sum(x[h] for h in b)-(j==dp) for j,b in enumerate(pools)]
  assert min(Y)>=0 and sum(Y)==sum(x)-1
  agg={}
  for _,y,z,k in rr:
   if y[A]==2:continue
   delta=tuple(sum(z[h]-y[h] for h in b) for b in pools)
   if not any(delta):continue
   i=delta.index(-1);j=delta.index(1)
   agg[i,j]=agg.get((i,j),F(0))+rate(y,k,x)/x[D]
  bas={(e['source'],e['target']):F(e['rate'])*Y[e['source']] for e in cert['pool_certificate']['baseline_edges']}
  for ij,b in bas.items():assert agg.get(ij,0)>=b
  for ij,v in agg.items():
   if ij[1]!=0:assert v==bas.get(ij,0),(name,x,ij,v,bas)
   assert Y[ij[0]]>0 or v==0 or ij[1]==0
 results[name]={'status':cert['status'],'states':states,'enabled_move_checks':checks,'L':cert['pool_certificate']['L']}
(root/'check_exhaustive_interfaces.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
