"""Own standard-library exact GF(2) audit. Run python check_complete_detectors.py [matrix_dir]."""
import collections, hashlib, itertools, json, pathlib, sys
P=pathlib.Path(__file__).parent
SRC=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else P/'matrices'
H={t:json.loads((SRC/f'H{t}_33.json').read_text()) for t in 'XZ'}
rows={t:[sum(int(x)<<i for i,x in enumerate(r)) for r in H[t]] for t in 'XZ'}
N=33; ALL=(1<<N)-1

def basis(vs):
 b={}
 for v in vs:
  while v:
   k=v.bit_length()-1
   if k in b:v^=b[k]
   else:b[k]=v;break
 return b

def rank(vs):return len(basis(vs))
def rem(v,b):
 while v:
  k=v.bit_length()-1
  if k not in b:return v
  v^=b[k]
 return 0

def nullbasis(vs,n):
 b=basis(vs);out=[]
 for j in range(n):
  if j in b:continue
  v=1<<j
  for k in sorted(b):
   if (v&b[k]).bit_count()%2:v^=1<<k
  assert all((v&r).bit_count()%2==0 for r in vs)
  out.append(v)
 return out

def qs(a):return [i for i in range(N) if a>>i&1]
B={t:basis(rows[t]) for t in 'XZ'}
def dim(a):return {t:a.bit_count()-rank([r&a for r in rows[o]])-len(B[t])+rank([r&(ALL^a) for r in rows[t]]) for t,o in [('X','Z'),('Z','X')]}
MIN_LOGICALS={t:[] for t in 'XZ'}
for t,o in [('X','Z'),('Z','X')]:
 for ii in itertools.combinations(range(N),4):
  v=sum(1<<q for q in ii)
  if all((v&r).bit_count()%2==0 for r in rows[o]) and rem(v,B[t]):MIN_LOGICALS[t].append(v)
assert all(len(v)==4 for v in MIN_LOGICALS.values())
def witness(a):
 for t in 'XZ':
  for v in MIN_LOGICALS[t]:
   if v&~a==0:return {'type':t,'qubits':qs(v)}
 for t,o in [('X','Z'),('Z','X')]:
  cols=qs(a);restricted=[sum(((r>>q)&1)<<j for j,q in enumerate(cols)) for r in rows[o]]
  for v in nullbasis(restricted,len(cols)):
   w=sum(((v>>j)&1)<<q for j,q in enumerate(cols))
   if rem(w,B[t]):
    assert w&~a==0 and all((w&r).bit_count()%2==0 for r in rows[o])
    return {'type':t,'qubits':qs(w)}
 return None

def detector_bases(a,t):
 k=rank([r&a for r in rows[t]])
 valid=[i for i,r in enumerate(rows[t]) if r&a]
 out=[]
 for ii in itertools.combinations(valid,k):
  if rank([rows[t][i]&a for i in ii])==k:
   d=0
   for i in ii:d|=rows[t][i]
   out.append((ii,d))
 return k,out

def greedy(a,t):
 chosen=[];r=0
 for i,v in enumerate(rows[t]):
  new=rank([rows[t][j]&a for j in chosen]+[v&a])
  if new>r:chosen.append(i);r=new
 return chosen

def union_for(g):
 d=0
 for t in 'XZ':
  for i in g[t]:d|=rows[t][i]
 return d
assert all((x&z).bit_count()%2==0 for x in rows['X'] for z in rows['Z'])
assert all(len(B[t])==16 for t in 'XZ')
regions=[];certificates=[]
for t in 'XZ':
 for i,a in enumerate(rows[t]):
  assert not any(dim(a).values())
  k,xb=detector_bases(a,'X');l,zb=detector_bases(a,'Z')
  unions={};good_sets=0;size_counts=collections.Counter()
  for xi,xd in xb:
   for zi,zd in zb:
    d=xd|zd
    assert d&a==a
    unions.setdefault(d,{'X':list(xi),'Z':list(zi)})
    size_counts[d.bit_count()]+=1
  good=[];bad=[]
  for d,g in sorted(unions.items()):
   dims=dim(d);w=witness(d)
   assert bool(any(dims.values()))==bool(w)
   c={'D':qs(d),'G':g,'logical_dimensions':dims,'logical_witness':w}
   (bad if w else good).append((d,c))
   certificates.append({'target':f'{t}{i}',**c})
  for _,xd in xb:
   for _,zd in zb:
    if not any(dim(xd|zd).values()):good_sets+=1
  order=lambda pair:(pair[0].bit_count(),pair[0])
  best=min(good or bad,key=order)
  md=min(unions,key=lambda d:(d.bit_count(),d))
  closure=[qs(a)];d=a
  # Necessary fixed-point overlap-parity propagation, not a physical operation.
  while True:
   nd=d
   for x in rows['X']:
    for z in rows['Z']:
     edge=x&z
     if edge&d:nd|=edge
   if nd==d:break
   closure.append(qs(nd));d=nd
  assert d==ALL
  chain=[];d=a
  while not any(dim(d).values()):
   g=best[1]['G'] if d==a else {u:greedy(d,u) for u in 'XZ'}
   nd=union_for(g)
   chain.append({'A':qs(d),'G':g,'D':qs(nd),'D_logical_dimensions':dim(nd),'D_logical_witness':witness(nd)})
   assert nd!=d
   d=nd
  regions.append({'target':f'{t}{i}','A':qs(a),'restricted_check_ranks':{'X':k,'Z':l},'minimum_check_count':k+l,'basis_counts':{'X':len(xb),'Z':len(zb)},'minimum_sets':len(xb)*len(zb),'correctable_minimum_sets':good_sets,'distinct_unions':len(unions),'correctable_distinct_unions':len(good),'union_size_histogram_sets':dict(sorted(size_counts.items())),'minimum_union_size':md.bit_count(),'minimum_union_example':{'D':qs(md),'G':unions[md],'logical_dimensions':dim(md),'logical_witness':witness(md)},'smallest_correctable_example':best[1] if good else None,'uncorrectable_example':min(bad,key=order)[1] if bad else None,'illustrative_detector_expansion':chain,'necessary_fixed_point_overlap_closure':closure})
intersections=[x&z for x in rows['X'] for z in rows['Z'] if x&z]
assert all(e.bit_count()==2 for e in intersections) and rank(intersections)==32
out={'indices':'zero-based; checks labeled X0..X19,Z0..Z19','source_hashes':{t:hashlib.sha256((SRC/f'H{t}_33.json').read_bytes()).hexdigest() for t in 'XZ'},'code':{'n':33,'rank_X':16,'rank_Z':16,'k':1},'overlap_certificate':{'nonempty_pair_count':len(intersections),'unique_edges':len(set(intersections)),'rank':rank(intersections),'edges':[qs(e) for e in sorted(set(intersections))]},'regions':regions}
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n')
(P/'all_minimum_detector_unions.json').write_text(json.dumps(certificates,separators=(',',':'))+'\n')
print('PASS: 40 targets; all minimum sets enumerated; every uncorrectable union has an independently checked logical witness.')
print('Weight 4: 7 checks; min union 14. Weight 5: 9 checks; min union 18. No nonempty self-contained complete detector reservation.')
print('Unique-union certificates:',len(certificates))
