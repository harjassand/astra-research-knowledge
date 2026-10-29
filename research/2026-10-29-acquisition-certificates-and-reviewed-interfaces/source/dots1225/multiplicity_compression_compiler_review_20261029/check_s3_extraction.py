import numpy as np,itertools,math,json
from pathlib import Path
perms=list(itertools.permutations(range(3)))
B=np.array([[1/math.sqrt(2),1/math.sqrt(6)],[-1/math.sqrt(2),1/math.sqrt(6)],[0,-2/math.sqrt(6)]])
Ds=[]
for p in perms:
 P=np.zeros((3,3))
 for j in range(3):P[p[j],j]=1
 sg=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
 Ds.append([np.array([[1.]]),np.array([[float(sg)]]),B.T@P@B])
labels=[(l,a,b) for l,f in enumerate([1,1,2]) for a in range(f) for b in range(f)]
Q=np.array([[math.sqrt([1,1,2][l]/6)*Ds[g][l][a,b] for g in range(6)] for l,a,b in labels]);assert np.linalg.norm(Q@Q.T-np.eye(6))<1e-13

def permutation(D,p):
 out=np.zeros((D**3,D**3))
 for old in itertools.product(range(D),repeat=3):
  new=[0]*3
  for i in range(3):new[p[i]]=old[i]
  out[sum(new[i]*D**(2-i) for i in range(3)),sum(old[i]*D**(2-i) for i in range(3))]=1
 return out

def kraus(D):
 U=[permutation(D,p) for p in perms]
 return {(l,a,b):sum((math.sqrt([1,1,2][l])/6*Ds[g][l][a,b]*U[g] for g in range(6)),np.zeros_like(U[0])) for l,a,b in labels}
ks={D:kraus(D) for D in [2,4]}
def extract(psi,D,keep='column'):
 out=np.zeros((8,8),complex);offset=0
 for l,f in enumerate([1,1,2]):
  for b in range(f):
   for bp in range(f):
    block=np.zeros((2,2),complex)
    for a in range(f):
     A=ks[D][l,a,b] if keep=='column' else ks[D][l,b,a];C=ks[D][l,a,bp] if keep=='column' else ks[D][l,bp,a]
     v=A@psi;w=C@psi;block+=v.T@w.conj()
    out[2*(offset+b):2*(offset+b+1),2*(offset+bp):2*(offset+bp+1)]=block
  offset+=f
 return out
rng=np.random.default_rng(713209);worst=0;wrong=0
for _ in range(10):
 Z=rng.normal(size=(4,2))+1j*rng.normal(size=(4,2));V=np.linalg.qr(Z)[0];psi=rng.normal(size=(8,2))+1j*rng.normal(size=(8,2));psi/=np.linalg.norm(psi);encoded=np.kron(np.kron(V,V),V)@psi
 small=extract(psi,2);large=extract(encoded,4);err=np.linalg.norm(small-large);worst=max(worst,err);assert err<1e-12 and abs(np.trace(large)-1)<1e-12
 wrong=max(wrong,float(np.linalg.norm(large-extract(encoded,4,'row'))))
assert wrong>1e-3
out={'n':3,'small_dimension':2,'large_dimension':4,'reference_dimension':2,'random_complex_isometry_cases':10,'QFT_unitarity_residual':float(np.linalg.norm(Q@Q.T-np.eye(6))),'isometry_independence_residual':float(worst),'wrong_index_difference':wrong,'kept_index':'column b for D(pi)*_ab convention','scope':'Dense floating diagnostic of exact group-orthogonality proof; no full large-D circuit or native compiler'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
