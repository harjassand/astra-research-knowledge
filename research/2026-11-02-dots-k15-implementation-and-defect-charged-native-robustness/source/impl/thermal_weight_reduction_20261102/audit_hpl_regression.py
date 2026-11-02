from pathlib import Path
import numpy as np, json, itertools, math
rng=np.random.default_rng(551113)
def mm(a,b):return a@b%2
def rank(a):
 a=a.copy()%2;r=0
 for j in range(a.shape[1]):
  z=np.flatnonzero(a[r:,j]);
  if not len(z):continue
  k=r+z[0];a[[r,k]]=a[[k,r]]
  for l in range(a.shape[0]):
   if l!=r and a[l,j]:a[l]^=a[r]
  r+=1
  if r==a.shape[0]:break
 return r
def in_image(a,v):return rank(np.column_stack([a,v]))==rank(a)
# source 2 X checks, 3 qubits, 2 Z checks, including a repeated X check
levels=[2,2,1,1,1,0,0];nc=len(levels)
d=np.zeros((nc,nc),dtype=np.uint8)
d[2:5,0]=[1,1,0];d[2:5,1]=[1,1,0]
d[5,2:5]=[1,1,0];d[6,2:5]=[0,0,1]
assert not mm(d,d).any()
coords=[];hs=[];pairs=[]
for j,lev in enumerate(levels):
 hs.append(len(coords));coords.append((j,lev,lev))
 a=len(coords);coords.extend([(j,lev,0),(j,lev,1)]);pairs.append((a,a+1))
 a=len(coords);coords.extend([(j,lev,1),(j,lev,2)]);pairs.append((a,a+1))
N=len(coords);E=np.eye(N,dtype=np.uint8)
d0=np.zeros((N,N),dtype=np.uint8);h=d0.copy()
for low,high in pairs:d0[low,high]=1;h[high,low]=1
i=np.zeros((N,nc),dtype=np.uint8)
for j,a in enumerate(hs):i[a,j]=1
p=i.T;dc=d0^mm(mm(i,d),p)
assert np.array_equal(mm(d0,h)^mm(h,d0),E^mm(i,p))
idx0=[a for a,(_,_,deg) in enumerate(coords) if deg==0]
idx1=[a for a,(_,_,deg) in enumerate(coords) if deg==1]
old0=[a for a,lev in enumerate(levels) if lev==0]
old1=[a for a,lev in enumerate(levels) if lev==1]
checks=0;preimages=0
for trial in range(40):
 n=np.zeros((N,N),dtype=np.uint8)
 for a,(_,la,da) in enumerate(coords):
  for b,(_,lb,db) in enumerate(coords):
   if la<lb and da==db:n[a,b]=rng.integers(2)
 ti=E^n^mm(n,n);t=E^n
 assert np.array_equal(mm(t,ti),E)
 D=mm(mm(t,dc),ti);delta=D^d0
 hd=mm(h,delta);dh=mm(delta,h)
 I=mm(E^hd^mm(hd,hd),i)
 P=mm(p,E^dh^mm(dh,dh))
 H=mm(E^hd^mm(hd,hd),h)
 eff=mm(mm(p,delta),i)
 assert np.array_equal(eff,d)
 identities=[np.array_equal(mm(P,I),np.eye(nc,dtype=np.uint8)),np.array_equal(mm(P,D),mm(d,P)),np.array_equal(mm(D,I),mm(I,d)),np.array_equal(mm(D,H)^mm(H,D),E^mm(I,P)),not mm(P,H).any(),not mm(H,I).any(),not mm(H,H).any()]
 assert all(identities);checks+=len(identities)
 D1=D[np.ix_(idx0,idx1)];d1=d[np.ix_(old0,old1)];P0=P[np.ix_(old0,idx0)]
 if trial<3:
  for bits in itertools.product((0,1),repeat=len(idx0)):
   v=np.array(bits,dtype=np.uint8)
   assert in_image(D1,v)==in_image(d1,mm(P0,v));preimages+=1
# exact parity identity and log-cost inequality
parity_tests=0;maxerr=0.
for r in range(1,9):
 for B in (.01,.1,.7,2.,5.,10.):
  Bnew=B+math.log(r);q=math.exp(-Bnew)
  z0=sum(q**sum(x) for x in itertools.product((0,1),repeat=r) if sum(x)%2==0)
  z1=sum(q**sum(x) for x in itertools.product((0,1),repeat=r) if sum(x)%2==1)
  a=math.tanh(r*math.atanh(q))
  maxerr=max(maxerr,abs(z1/z0-a));assert abs(z1/z0-a)<1e-12
  assert z1/z0 <= math.exp(-B)*(1+1e-12)
  parity_tests+=1
result={'status':'PASS','random_hpl_cases':40,'hpl_identities_checked':checks,'endpoint_preimage_cases':preimages,'parity_parameter_cases':parity_tests,'parity_max_error':maxerr,'scope':'generic three-stratum contractions and parity fibers; not a compiled HLL cone or sheaf incidence certificate'}
print(json.dumps(result,indent=2))
open(str(Path(__file__).with_suffix('.json')),'w').write(json.dumps(result,indent=2)+'\n')
