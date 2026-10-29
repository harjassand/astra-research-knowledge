"""Independent exact five-qubit KL and randomized faithful interval-layout checks.
Integer-complex entries stay below 32, so these integer sums are exactly represented.
No source samples or large quantum-state simulation.
"""
import numpy as np,json,random
from pathlib import Path
# Pauli action on computational basis, rightmost symbol is low bit.
def apply(word,v):
 out=np.zeros_like(v)
 for z in range(32):
  zz=z;phase=1
  for bit,p in enumerate(reversed(word)):
   b=(z>>bit)&1
   if p in 'XY':zz^=1<<bit
   if p=='Z':phase*=1-2*b
   if p=='Y':phase*=1j*(1-2*b)
  out[zz]+=phase*v[z]
 return out
v=np.zeros(32,dtype=complex);v[0]=1
for g in ['XZZXI','IXZZX','XIXZZ','ZXIXZ']:v=v+apply(g,v)
assert np.vdot(v,v)==16
v1=apply('XXXXX',v);V=np.stack([v,v1],axis=1);assert np.array_equal(V.conj().T@V,16*np.eye(2))
words=['IIIII']+['I'*i+p+'I'*(4-i) for i in range(5) for p in 'XYZ']
images=[np.stack([apply(w,V[:,j]) for j in range(2)],axis=1) for w in words]
U=np.concatenate(images,axis=1)
assert np.array_equal(U.conj().T@U,16*np.eye(32)) and np.array_equal(U@U.conj().T,16*np.eye(32))
# Every recovery/error block equals delta_ab I, including offdiagonal syndrome cancellation.
for a in range(16):
 for b in range(16):assert np.array_equal(images[a].conj().T@images[b],16*np.eye(2) if a==b else np.zeros((2,2)))
# A shared bad coin is NOT a product/local-map composition: XXXXX is logical X.
logicalX=np.stack([apply('XXXXX',V[:,j]) for j in range(2)],axis=1)
assert np.array_equal(V.conj().T@logicalX,16*np.array([[0,1],[1,0]]))
from fractions import Fraction as F
h=F(1,100);false_bound=((1+2*h)**5-1-10*h)/2
assert false_bound<h
rng=random.Random(202610282117);layouts=[]
for W in range(1,6):
 L=(2*W-1)**2;n=5*L
 for trial in range(2):
  S=[];J=[];x=0
  while x<n:
   width=rng.randint(1,min(W,n-x));block=set(range(x,x+width))
   for _ in range(width):
    left=rng.randint(max(0,x-(W-width)),x);right=rng.randint(x+width-1,min(n-1,left+W-1));S.append(block);J.append(set(range(left,right+1)))
   x+=width
  # Independent factors on each disjoint block are faithful (any block-local mixer).
  order=sorted(range(n),key=lambda i:(min(J[i]),i));rank={i:a for a,i in enumerate(order)};layers=[]
  for i in order:
   for layer in layers:
    if all(J[i].isdisjoint(J[k]) for k in layer):layer.append(i);break
   else:layers.append([i])
  assert len(layers)<=2*W-1
  modes=[J[i]|{n+i} for i in range(n)];color={i:a for a,layer in enumerate(layers) for i in layer};maxspan=0
  for i in range(n):
   cone=set(modes[i])
   for layer in layers[color[i]+1:]:
    add=[k for k in layer if not modes[k].isdisjoint(cone)]
    for k in add:cone|=modes[k]
   ranks=sorted(rank[k-n] for k in cone if k>=n);span=ranks[-1]-ranks[0]+1;maxspan=max(maxspan,span);assert span<=L
   assert len(set(a%L for a in ranks))==len(ranks)
  maxmacro=maxnative=0
  for b in range(L):
   cone={n+order[b+t*L] for t in range(5)};owners=set()
   for layer in reversed(layers):
    add=[k for k in layer if not modes[k].isdisjoint(cone)]
    owners.update(add)
    for k in add:cone|=modes[k]
   physical={k for k in cone if k<n};native={i for i in range(n) if not S[i].isdisjoint(physical)}
   assert len(owners)<=5*L and len(native)<=5*L;maxmacro=max(maxmacro,len(owners));maxnative=max(maxnative,len(native))
  layouts.append({'W':W,'trial':trial,'n':n,'L':L,'depth':len(layers),'max_single_fault_rank_span':maxspan,'max_logical_macro_locations':maxmacro,'max_logical_native_locations':maxnative})
out={'status':'PASS_EXACT_CODE_ALGEBRA_AND_FAITHFUL_LAYOUTS','KL_error_pairs_checked':256,'complete_recovery_syndrome_basis':True,'shared_bad_coin_boundary':{'marginal_error':str(h),'actual_logical_error':str(h),'false_product_bound':str(false_bound)},'layouts':layouts,'scope':'Exact integer five-qubit correction algebra plus finite faithful support fixtures; not proof by set counting alone, not hardware or large-state simulation.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
