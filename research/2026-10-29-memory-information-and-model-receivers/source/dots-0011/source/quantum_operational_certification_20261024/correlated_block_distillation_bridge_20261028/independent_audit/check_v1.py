import itertools,math,json,hashlib,time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
D=Path(__file__).resolve().parent;root=D.parent
start=time.time()
# Independent syndrome convention: base-4 I,X,Z,Y labels, 25-bit masks.
def pword(w):
 return (sum((c in 'XY')<<i for i,c in enumerate(w)),sum((c in 'ZY')<<i for i,c in enumerate(w)))
def inner(a,b):return ((a[0]&b[1])^(a[1]&b[0])).bit_count()%2
base=[pword(w) for w in ('XZZXI','IXZZX','XIXZZ','ZXIXZ')]
xl=pword('XXXXX');zl=pword('ZZZZZ')
nontrivial=[]
for labels in itertools.product(range(4),repeat=5):
 e=(sum((v&1)<<i for i,v in enumerate(labels)),sum(((v>>1)&1)<<i for i,v in enumerate(labels)))
 if all(inner(e,g)==0 for g in base) and (inner(e,xl) or inner(e,zl)):
  nontrivial.append(((e[0]|e[1]).bit_count(),e))
assert min(w for w,e in nontrivial)==3
G=[(x<<(5*b),z<<(5*b)) for b in range(5) for x,z in base]
G += [(sum(31<<(5*b) for b in range(5) if x>>b&1),sum(31<<(5*b) for b in range(5) if z>>b&1)) for x,z in base]
assert all(inner(g,h)==0 for g in G for h in G)
# Construct actual first-match decoder, retaining syndrome->logical error class.
# All matching errors have identical class iff their product is stabilizer.
one={}
for i in range(25):
 for v in (1,2,3):
  e=((v&1)<<i,((v>>1)&1)<<i)
  sy=sum(inner(e,g)<<j for j,g in enumerate(G))
  cl=inner(e,((1<<25)-1,0)) | (inner(e,(0,(1<<25)-1))<<1)
  one[i,v]=(sy,cl,e[0]|(e[1]<<25))
lookup={0:0};counts=[1];collisions=0
for w in range(1,5):
 count=0
 for positions in itertools.combinations(range(25),w):
  for vals in itertools.product((1,2,3),repeat=w):
   sy=cl=rep=0
   for i,v in zip(positions,vals):
    s,l,r=one[i,v];sy^=s;cl^=l;rep^=r
   if sy in lookup:
    old=lookup[sy];oldclass=((old>>25).bit_count()%2)|(((old&((1<<25)-1)).bit_count()%2)<<1)
    assert oldclass==cl,(positions,vals,sy)
    collisions+=1
   else:lookup[sy]=rep
   count+=1
 counts.append(count)
assert sum(counts)==1089526
# Independently condition on retained weight k, summing sample support h=w-k.
def tail(n,m,t,c):
 result=[]
 for w in range(n+m+1):
  p=F(0)
  for k in range(t+1,n+1):
   h=w-k
   if not 0<=h<=m:continue
   failtail=sum(F(math.comb(h,j)*2**j,3**h) for j in range(min(c,h)+1))
   p+=F(math.comb(n,k)*math.comb(m,h),math.comb(n+m,w))*failtail
  result.append(p)
 mx=max(result);return mx,[w for w,p in enumerate(result) if p==mx]
p,ws=tail(25,100,4,0);assert p==F(97106,217474455) and ws==[7]
# Small exact classical exhaustive check against independent retained-first formula.
small=[]
for n,m,t,c in [(2,3,0,0),(3,3,1,1),(3,4,1,0)]:
 mx=F(0)
 for bits in itertools.product((0,1),repeat=n+m):
  pex=F(0)
  for subset in itertools.combinations(range(n+m),m):
   h=sum(bits[i] for i in subset)
   if sum(bits)-h<=t:continue
   pex+=sum(F(math.comb(h,j)*2**j,3**h) for j in range(min(c,h)+1))/math.comb(n+m,m)
  mx=max(mx,pex)
 assert mx==tail(n,m,t,c)[0];small.append(str(mx))
# One-pair quantum Bell dephasing, correlated with an explicit environment qubit.
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.]);P=[I,X,Y,Z]
phi=np.array([1,0,0,1],complex)/np.sqrt(2);bells=[np.kron(I,q)@phi for q in P]
rng=np.random.default_rng(5102859);v=rng.normal(size=8)+1j*rng.normal(size=8);v/=np.linalg.norm(v);rho=np.outer(v,v.conj())
twirled=sum(np.kron(np.kron(q.conj(),q),I)@rho@np.kron(np.kron(q.conj(),q),I).conj().T for q in P)/4
diag=np.zeros((8,8),complex)
for b in bells:
 proj=np.kron(np.outer(b,b.conj()),I);diag+=proj@rho@proj
err=float(np.max(abs(twirled-diag)));assert err<1e-14
parities=[]
for b in bells:
 vals=[float(np.vdot(b,np.kron(q,q)@b).real) for q in (X,Y,Z)]
 bad=sum(abs(a-s)>1e-8 for a,s in zip(vals,(1,-1,1)));parities.append(bad)
assert parities==[0,2,2,2]
# Independently reproduce every saved tail row and iid-only yield diagnostic.
author=json.loads((root/'exact_block_test_v1.json').read_text());tailrows=[]
for row in author['rows']:
 q,ww=tail(25,row['m'],4,0)
 assert q==F(row['max_bad_accept_num'],row['max_bad_accept_den'])
 assert row['maximizing_total_weight'] in ww
 tailrows.append({'m':row['m'],'beta':str(q),'argmax':ww})
rate=F(1,100);accept=(1-F(2,3)*rate)**100
bad=sum(F(math.comb(25,k))*rate**k*(1-rate)**(25-k) for k in range(5,26))
assert float(accept)==author['honest_iid_diagnostic']['accept_probability']
assert float(bad)==author['honest_iid_diagnostic']['remaining_weight_gt4']
# Binding and audit data, source is never imported.
out={'status':'independent exact combinatorics and exhaustive syndrome-decoder checks','all_weight_counts':counts,'syndrome_table_distinct_entries':len(lookup),'actual_representatives_constructed':True,'table_sha256':hashlib.sha256(b''.join(s.to_bytes(3,'little')+r.to_bytes(7,'little') for s,r in sorted(lookup.items()))).hexdigest(),'syndrome_collisions_checked':collisions,'all_collisions_same_logical_class':True,'base_distance':3,'beta':str(p),'argmax':ws,'all_tail_rows':tailrows,'small_exhaustive_tails':small,'quantum_twirl_max_error':err,'Bell_parity_mismatch_axis_counts':parities,'elapsed_seconds':time.time()-start,'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'GOVERNING_BRIDGE_v1.md',root/'exact_block_test_v1.py',root/'exact_block_test_v1.json']}}
(D/'results_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
