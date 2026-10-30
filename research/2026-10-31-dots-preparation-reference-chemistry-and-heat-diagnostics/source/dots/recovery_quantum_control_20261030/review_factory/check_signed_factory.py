import numpy as np,itertools,json
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex)
def kron(xs):
 o=np.ones((1,1),complex)
 for x in xs:o=np.kron(o,x)
 return o
def pauli(bits,p):return kron([p if x else I for x in bits])
xs=[(1,1,1,1)];zs=[(1,1,0,0),(0,0,1,1)]
XX=pauli(xs[0],X);ZZ=[pauli(z,Z) for z in zs];zlog=pauli((1,0,1,0),Z)
zero=np.eye(16)[:,0];maxres=0.;maxlogical=0.;cases=0
for sx in (0,1):
 for sz in itertools.product((0,1),repeat=2):
  P=(np.eye(16)+(-1)**sx*XX)/2
  for sign,S in zip(sz,ZZ):P=P@(np.eye(16)+(-1)**sign*S)/2
  target=(np.eye(16)+(-1)**sx*XX)@zero/2
  for a in itertools.product((0,1),repeat=4):
   ai=sum(v*2**(3-i) for i,v in enumerate(a));state=P[:,ai]
   if np.linalg.norm(state)<1e-12:continue
   transformed=pauli(a,X)@state
   maxres=max(maxres,float(np.linalg.norm(transformed-target)))
   maxlogical=max(maxlogical,float(np.linalg.norm(zlog@transformed-transformed)))
   for z in itertools.product((0,1),repeat=4):
    if sum(z)%2==sx:
     fixed=pauli(z,Z)@transformed
     ideal=(np.eye(16)+XX)@zero/2
     assert np.linalg.norm(fixed-ideal)<1e-12
   cases+=1
assert maxres<1e-12 and maxlogical<1e-12
path=[]
for n in (4,6,8,10,12):
 m=n//2;D=tuple(int(i==m-1) for i in range(n-1));pre=[]
 for z in itertools.product((0,1),repeat=n):
  if tuple(z[i]^z[i+1] for i in range(n-1))==D:pre.append(z)
 assert len(pre)==2 and min(sum(z) for z in pre)==min(m,n-m)
 path.append({'n':n,'preimages':2,'minimum_weight_mod_known_logical_Z':min(sum(z) for z in pre)})
print(json.dumps({'signed_Bell_nonzero_outcomes_checked':cases,'X_mask_identity_residual':maxres,'known_logical_Z_residual':maxlogical,'path_syndrome_tests':path,'scope':'Exact finite algebra diagnostics; no native factory or particular Tanner-family acquisition test.'},indent=2))
