# Independent sparse coherent CSS check using direct degree-filtered evaluation.
import numpy as np,itertools,json,collections
from pathlib import Path
rng=np.random.default_rng(202610290439);q=8;h=3;B=q;t=1;r=2*t
mod=0b1011
def mul(a,b):
 c=0
 while b:
  if b&1:c^=a
  b>>=1;a<<=1
  if a&q:a^=mod
 return c
def powr(a,k):
 v=1
 for _ in range(k):v=mul(v,a)
 return v
def inv(a):assert a;return powr(a,q-2)
def tr(a):
 z=a;w=a
 for _ in range(1,h):w=mul(w,w);z^=w
 assert z in(0,1);return z
def dot(a,b):
 s=0
 for x,y in zip(a,b):s^=mul(int(x),int(y))
 return s
def mv(A,x):return tuple(dot(a,x) for a in A)
def matinv(A):
 A=[list(a)+[int(i==j) for j in range(B)] for i,a in enumerate(A)]
 for j in range(B):
  k=next(i for i in range(j,B) if A[i][j]);A[j],A[k]=A[k],A[j];a=inv(A[j][j]);A[j]=[mul(x,a) for x in A[j]]
  for i in range(B):
   if i!=j:
    a=A[i][j];A[i]=[x^mul(a,y) for x,y in zip(A[i],A[j])]
 return [a[B:] for a in A]
def tj(j,x):
 z=1;den=1
 for w in range(1<<j):z=mul(z,x^w);den=mul(den,(1<<j)^w)
 return mul(z,inv(den))
def bi(i,x):
 z=1
 for j in range(h):
  if i>>j&1:z=mul(z,tj(j,x))
 return z
L=[[bi(i,x) for i in range(B)] for x in range(B)];Li=matinv(L);Lt=list(map(list,zip(*L)))
assert all(mv(Li,mv(L,[int(i==j) for i in range(B)]))==tuple(int(i==j) for i in range(B)) for j in range(B))
# Bind the independently constructed direct matrix to the actual binary compiler.
import sys
sys.path.insert(0,str(Path(__file__).parent/'replay'))
from additive_fft import Compiler
compiler=Compiler(h,mod)
for wire in range(B*h):
 u=[0]*B;u[wire//h]=1<<(wire%h)
 assert tuple(compiler.apply_bits(u))==mv(L,u)
H=Lt[:r];assert all(dot(H[i],Lrow)==0 for i in range(r) for Lrow in Lt[:B-r])
sx={};sz={}
errors=[(0,)*B]
for pos in range(B):
 for a in range(1,q):
  e=[0]*B;e[pos]=a;errors.append(tuple(e))
for e in errors:
 ex=mv(Li,e);ez=mv(Lt,e);assert ex[B-r:] not in sx;assert ez[:r] not in sz;sx[ex[B-r:]]=ex;sz[ez[:r]]=ez
# Choose an entangled logical/reference input, sparse rather than dense 8^8 storage.
messages=[(0,1,2,3),(7,4,6,5)];amps=[np.sqrt(.37),1j*np.sqrt(.63)]
# A coherent interaction between one physical symbol and an unmeasured bath qubit.
W=np.linalg.qr(rng.normal(size=(16,16))+1j*rng.normal(size=(16,16)))[0]
noise=[W.reshape(q,2,q,2)[:,b,:,0] for b in range(2)]
rows=[]
for pos in [0,3,7]:
 before=collections.defaultdict(complex)
 for ref,logical in enumerate(messages):
  for first in itertools.product(range(q),repeat=r):
   c=first+logical+(0,)*r;y=list(mv(L,c))
   for bath,A in enumerate(noise):
    for out in range(q):
     z=y.copy();z[pos]=out;coef=mv(Li,z)
     before[(ref,bath,coef)]+=amps[ref]/q*A[out,y[pos]]
 measured=collections.defaultdict(complex)
 for (ref,bath,c),amp in before.items():
  for phase in itertools.product(range(q),repeat=r):
   sy=(phase,c[B-r:]);ph=(-1)**tr(dot(phase,c[:r]))
   measured[(sy,bath,ref,c[r:B-r])]+=amp*ph/q
 after=collections.defaultdict(complex);invalid=0.
 for (sy,bath,ref,mid),amp in measured.items():
  if sy[0] not in sz or sy[1] not in sx:
   invalid+=abs(amp)**2;continue
  xe=sx[sy[1]];ze=sz[sy[0]]
  logical=tuple(x^e for x,e in zip(mid,xe[r:B-r]))
  ph=(-1)**tr(dot(ze[r:B-r],logical))
  after[(sy,bath,ref,logical)]+=amp*ph
 assert invalid<1e-24
 failure=sum(abs(a)**2 for (sy,b,ref,l),a in after.items() if l!=messages[ref])
 scalars={};mismatch=0.;norm=sum(abs(a)**2 for a in after.values())
 for sy in {k[0] for k in after}:
  for bath in range(2):
   z=[after.get((sy,bath,ref,messages[ref]),0)/amps[ref] for ref in range(2)]
   mismatch=max(mismatch,abs(z[0]-z[1]));scalars[(sy,bath)]=z[0]
 assert failure<1e-24 and mismatch<1e-12 and abs(norm-1)<1e-12
 rows.append({'physical_bad_position':pos,'wrong_logical_probability':float(failure),'reference_independence_max_residual':float(mismatch),'total_norm':float(norm),'syndrome_branches':len({k[0] for k in after})})
out={'field':'GF8 with modulus x^3+x+1','B':B,'t':t,'logical_qudits':B-4*t,'logical_qubits':h*(B-4*t),'scope':'Independent sparse coherent system-bath error and entangled reference check. Direct evaluation, not author FFT implementation; full quantum correction diagnostic, not a general proof.','all_binary_basis_compiler_checks':B*h,'cases':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
