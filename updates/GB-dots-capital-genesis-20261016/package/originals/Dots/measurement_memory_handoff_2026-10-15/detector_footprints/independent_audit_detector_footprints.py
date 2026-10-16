"""Independent audit, does not import or execute the submitted implementation."""
import json,itertools,collections,hashlib,pathlib
P=pathlib.Path(__file__).parent;S=P/'matrices'
H={t:json.loads((S/f'H{t}_33.json').read_text()) for t in 'XZ'}
R={t:[sum(int(v)*2**j for j,v in enumerate(r)) for r in H[t]] for t in 'XZ'}
n=33;full=2**n-1
# Lowest-pivot elimination, independent of audited highest-pivot implementation.
def echelon(vectors):
 b={}
 for x in vectors:
  while x:
   bit=x&-x
   if bit in b:x^=b[bit]
   else:b[bit]=x;break
 return b
def rank(vectors):return len(echelon(vectors))
def is_member(x,b):
 while x:
  bit=x&-x
  if bit not in b:return False
  x^=b[bit]
 return True
def mask(qs):return sum(2**q for q in qs)
B={t:echelon(R[t]) for t in 'XZ'}
assert [len(B[t]) for t in 'XZ']==[16,16]
assert all((x&z).bit_count()%2==0 for x in R['X'] for z in R['Z'])
# Stabilizers supported on D: kernel of puncturing-to-complement.
# Centralizer supported on D: kernel of the opposite check restriction.
def logical_dims(d):
 return {t:d.bit_count()-rank(v&d for v in R[o])-16+rank(v&(full^d) for v in R[t]) for t,o in [('X','Z'),('Z','X')]}
def check_witness(d,w):
 if w is None:return
 t=w['type'];v=mask(w['qubits']);o='Z' if t=='X' else 'X'
 assert v and v&d==v
 assert all((v&r).bit_count()%2==0 for r in R[o])
 assert not is_member(v,B[t])
res=json.loads((P/'results.json').read_text());certs=json.loads((P/'all_minimum_detector_unions.json').read_text())
for t in 'XZ':assert res['source_hashes'][t]==hashlib.sha256((S/f'H{t}_33.json').read_bytes()).hexdigest()
bytarget=collections.defaultdict(dict)
for c in certs:
 d=mask(c['D']); assert d not in bytarget[c['target']]
 bytarget[c['target']][d]=c
 assert c['logical_dimensions']==logical_dims(d)
 assert bool(c['logical_witness'])==any(logical_dims(d).values())
 check_witness(d,c['logical_witness'])
summary=[]
for rec in res['regions']:
 t=rec['target'][0];i=int(rec['target'][1:]);a=R[t][i];assert mask(rec['A'])==a
 assert not any(logical_dims(a).values())
 assert (rec['minimum_check_count'],rec['minimum_union_size'])==({4:(7,14),5:(9,18)}[a.bit_count()])
 choices={};ranks={}
 for u in 'XZ':
  k=rank(v&a for v in R[u]);ranks[u]=k;choices[u]=[]
  for inds in itertools.combinations(range(len(R[u])),k):
   if rank(R[u][j]&a for j in inds)==k:
    d=0
    for j in inds:d|=R[u][j]
    choices[u].append((inds,d))
 assert ranks==rec['restricted_check_ranks']
 assert {u:len(choices[u]) for u in 'XZ'}==rec['basis_counts']
 unions=collections.Counter();hist=collections.Counter()
 for (xi,xd),(zi,zd) in itertools.product(choices['X'],choices['Z']):
  d=xd|zd;assert d&a==a;unions[d]+=1;hist[d.bit_count()]+=1
 assert set(unions)==set(bytarget[rec['target']])
 for d,c in bytarget[rec['target']].items():
  actual=0
  for u in 'XZ':
   inds=c['G'][u];assert len(inds)==ranks[u]
   assert rank(R[u][j]&a for j in inds)==ranks[u]
   for j in inds:actual|=R[u][j]
  assert actual==d
 good=[d for d in unions if not any(logical_dims(d).values())]
 assert rec['minimum_check_count']==sum(ranks.values())
 assert rec['minimum_sets']==sum(unions.values())
 assert rec['distinct_unions']==len(unions)
 assert rec['correctable_minimum_sets']==sum(unions[d] for d in good)
 assert rec['correctable_distinct_unions']==len(good)
 assert {int(k):v for k,v in rec['union_size_histogram_sets'].items()}==dict(hist)
 assert rec['minimum_union_size']==min(d.bit_count() for d in unions)
 for e in ('minimum_union_example','smallest_correctable_example','uncorrectable_example'):
  if rec[e] is not None:
   c=rec[e];d=mask(c['D']);assert d in unions
   assert c['logical_dimensions']==logical_dims(d);check_witness(d,c['logical_witness'])
 for c in rec['illustrative_detector_expansion']:
  d=mask(c['D']);actual=0;a0=mask(c['A'])
  for u in 'XZ':
   assert rank(R[u][j]&a0 for j in c['G'][u])==rank(v&a0 for v in R[u])
   for j in c['G'][u]:actual|=R[u][j]
  assert d==actual and d&a0==a0
  assert c['D_logical_dimensions']==logical_dims(d);check_witness(d,c['D_logical_witness'])
 summary.append({k:rec[k] for k in ('target','minimum_check_count','minimum_sets','minimum_union_size','correctable_minimum_sets','distinct_unions','correctable_distinct_unions')})
# Independent graph connectivity certificate.
edges={x&z for x in R['X'] for z in R['Z'] if x&z}
assert len(edges)==112 and all(e.bit_count()==2 for e in edges)
assert rank(edges)==32
adj=[set() for _ in range(n)]
for e in edges:
 i,j=[q for q in range(n) if e>>q&1];adj[i].add(j);adj[j].add(i)
seen={0};front=[0]
while front:
 for j in adj[front.pop()]:
  if j not in seen:seen.add(j);front.append(j)
assert len(seen)==33
for rec in res['regions']:
 d=mask(rec['A']);chain=[d]
 while True:
  nxt=d
  for e in edges:
   if e&d:nxt|=e
  if nxt==d:break
  d=nxt;chain.append(d)
 assert d==full and chain==[mask(qs) for qs in rec['necessary_fixed_point_overlap_closure']]
# Check claimed distance independently across every pure X and pure Z weight <=4.
counts={}
for t,o in [('X','Z'),('Z','X')]:
 counts[t]={}
 for w in range(1,5):
  count=0
  for qs in itertools.combinations(range(n),w):
   v=mask(qs)
   if all((v&r).bit_count()%2==0 for r in R[o]) and not is_member(v,B[t]):count+=1
  counts[t][w]=count
 assert counts[t]=={1:0,2:0,3:0,4:4}
output={'status':'PASS','target_count':len(summary),'minimum_sets':sum(x['minimum_sets'] for x in summary),'union_certificates_verified':len(certs),'overlap_edges':len(edges),'overlap_rank':rank(edges),'connected_vertices':len(seen),'pure_logical_weight_counts':counts,'targets':summary}
(P/'independent_audit_detector_footprints.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({k:v for k,v in output.items() if k!='targets'},indent=2))
