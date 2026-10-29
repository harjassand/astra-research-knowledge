import numpy as np,itertools,math,json
from pathlib import Path
rng=np.random.default_rng(202610291026);rows=[]
def kron(xs):
 a=np.array([[1]],complex)
 for x in xs:a=np.kron(a,x)
 return a
for d in [3,4,5]:
 r=d-1;A=np.zeros((d,d**r),complex)
 for a in range(d):
  rest=[i for i in range(d) if i!=a]
  for p in itertools.permutations(rest):
   inv=sum(p[i]>p[j] for i in range(r) for j in range(i+1,r));idx=sum(p[i]*d**(r-1-i) for i in range(r));A[a,idx]=(-1)**(a+inv)/math.sqrt(math.factorial(r))
 assert np.linalg.norm(A@A.conj().T-np.eye(d))<1e-12
 v=rng.normal(size=d)+1j*rng.normal(size=d);v/=np.linalg.norm(v);tmp=np.column_stack([v,rng.normal(size=(d,d-1))+1j*rng.normal(size=(d,d-1))]);U,_=np.linalg.qr(tmp);v=U[:,0];B=U[:,1:]
 z=rng.normal(size=(r**r,3))+1j*rng.normal(size=(r**r,3));z/=np.linalg.norm(z);psi=kron([B]*r)@z;out=A@psi;P=np.outer(v.conj(),v);res=np.linalg.norm((np.eye(d)-P)@out);assert res<1e-12
 rho=kron([B@B.conj().T/r]*r);record=A@rho@A.conj().T;iiderr=np.linalg.norm(record-P/r**r);assert iiderr<1e-12
 # Too-small occupied span makes all full-wedge events impossible.
 small=B[:,:r-1];z2=rng.normal(size=((r-1)**r,2))+1j*rng.normal(size=((r-1)**r,2));zero=np.linalg.norm(A@kron([small]*r)@z2);assert zero<1e-12
 rows.append(dict(d=d,correlated_bath_dimension=3,decoupling_residual=float(res),iid_identity_residual=float(iiderr),rank_deficient_success_amplitude=float(zero),correlated_success_probability=float(np.linalg.norm(out)**2),iid_best_probability=1/r**r))
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(scope='Small-dimension dense diagnostics of general exterior-power proof; exactd9 theorem not inferred solely from numerics',rows=rows),indent=2)+'\n');print(rows)
