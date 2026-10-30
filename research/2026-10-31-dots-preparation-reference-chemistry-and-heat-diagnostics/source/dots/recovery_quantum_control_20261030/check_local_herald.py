import numpy as np,json,itertools
rng=np.random.default_rng(4321)
n=4;N=1<<n;C=[0,3,12,15];p=1/len(C);maxerr=0.;ratios=[];cases=0
for mask in range(1<<n):
 size=mask.bit_count(); loc=[g for g in C if g&~mask==0];h=len(loc).bit_length()-1
 for a in range(4):
  P=np.zeros((N,N))
  for j,g in enumerate(C):
   sign=(-1)**((j&a).bit_count())
   for x in range(N):P[x^g,x]+=p*sign
  for x in range(N):
   ids=[y for y in range(N) if (x^y)&~mask==0]
   norm=np.linalg.norm(P[np.ix_(ids,ids)],2)
   maxerr=max(maxerr,abs(norm-p*len(loc)));cases+=1
 # arbitrary operator on local DATA subcube and 2-dimensional bath
 d=(1<<size)*2;E=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));E/=np.linalg.norm(E,2)
 ids=[y for y in range(N) if y&~mask==0]
 P=np.zeros((N,N))
 for g in C:
  for x in range(N):P[x^g,x]+=p
 compress=np.kron(P[np.ix_(ids,ids)],np.eye(2))
 for localx in range(1<<size):
  V=E[:,2*localx:2*localx+2]
  val=np.linalg.norm(V.conj().T@compress@V,2)
  ratios.append(val/(p*len(loc)))
assert maxerr<1e-12 and max(ratios)<=1+1e-12
print(json.dumps(dict(result='PASS',compression_cases=cases,compression_residual=maxerr,max_random_bath_leg_bound_ratio=max(ratios),scope='finite algebra not physical native endpoint'),indent=2))
