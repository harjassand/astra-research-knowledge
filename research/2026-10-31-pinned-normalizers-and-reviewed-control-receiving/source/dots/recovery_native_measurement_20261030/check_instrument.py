import itertools,json,math
from pathlib import Path
# Steane [[7,1,3]], C_X=row(H), H columns the seven nonzero 3-bit vectors.
rows=[sum(((j>>b)&1)<<(j-1) for j in range(1,8)) for b in range(3)]
C=[0]
for r in rows:C += [x^r for x in C[:]]
def par(x):return x.bit_count()%2
def synd(x):return sum(par(x&r)<<b for b,r in enumerate(rows))
def label(y):
 s=synd(y)
 return par(y^(1<<(s-1) if s else 0))
# All Pauli products on DATA and RECORD at one common coordinate.
errors=[(0,0,0,0)]
for i in range(7):
 for xd,zd,xr,zr in itertools.product(range(2),repeat=4):
  if xd or zd or xr or zr:errors.append(tuple(v<<i for v in (xd,zd,xr,zr)))
def image(e,l):
 xd,zd,xr,zr=e
 return {(w^xd,w^xr): (-1)**(par(w&zd)+par(w&zr))/math.sqrt(8) for c in C for w in [c^(127 if l else 0)]}
def overlap(a,b,z=None):return sum(v*b.get(k,0) for k,v in a.items() if z is None or label(k[1])==z)
vec=[[image(e,l) for l in range(2)] for e in errors]
res=0.; checks=0; inter=0
for a in range(len(errors)):
 for b in range(len(errors)):
  scalar=overlap(vec[a][0],vec[b][0])
  for z,l,m in itertools.product(range(2),repeat=3):
   actual=overlap(vec[a][l],vec[b][m],z)
   expected=scalar if l==m==z else 0
   res=max(res,abs(actual-expected));checks+=1
for a in range(len(errors)):
 for l in range(2):
  inter+=sum(label(y)!=l for d,y in vec[a][l])
# Counterexample: preserving raw garbage makes auxiliary distinguish z perfectly.
raw0={c for c in C};raw1={c^127 for c in C}
# Bottom-up bound check using conservative xj=xstar*r^(2^j)
xstar=.01;x=.00001;r=x/xstar;B=12
p=math.expm1(B*sum(xstar*r**(2**j) for j in range(8)))
bound=math.expm1(B*x/(1-r))
out={'code':'Steane [[7,1,3]]; arbitrary Pauli on DATA+record at one coordinate','error_operators':len(errors),'cross_term_projector_checks':checks,'max_residual':res,'intertwining_violations':inter,'raw_garbage_logical_support_disjoint':raw0.isdisjoint(raw1),'tower_OR_strength':p,'tower_uniform_bound':bound,'scope':'Algebra check, not Tanner gadget/threshold certification.'}
assert res<1e-12 and inter==0 and p<=bound
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
