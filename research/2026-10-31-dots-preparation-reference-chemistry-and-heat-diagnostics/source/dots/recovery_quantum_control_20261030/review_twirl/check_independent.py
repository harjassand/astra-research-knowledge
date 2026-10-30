import numpy as np,json
n=7;N=2**n;rows=[0b1010101,0b0110011,0b0001111]
C={0}
for a in rows:C|={b^a for b in list(C)}
P=np.zeros((N,N),complex)
for x in range(N):
 for c in C:P[x^c,x]+=1/len(C)
allowed=np.array([min((x^c).bit_count() for c in C)<=1 for x in range(N)])
Q=np.diag(allowed.astype(float));Qbad=np.eye(N)-Q
assert np.linalg.norm(P@Q-Q@P)<1e-12
assert np.linalg.norm(np.diag(np.diag(Qbad@P@Qbad))-Qbad/len(C))<1e-12
rng=np.random.default_rng(710);v=rng.normal(size=2*N)+1j*rng.normal(size=2*N);v/=np.linalg.norm(v)
rho=np.outer(v,v.conj());twirl=np.zeros_like(rho)
for x in range(N):twirl[2*x:2*x+2,2*x:2*x+2]=rho[2*x:2*x+2,2*x:2*x+2]
PP=np.kron(P,np.eye(2));B=np.kron(Qbad,np.eye(2));out=PP@twirl@PP
partial=lambda a:np.einsum('iaib->ab',a.reshape(N,2,N,2))
p=1/len(C)
res=float(np.linalg.norm(partial(out)-p*partial(rho)))
badres=float(np.linalg.norm(partial(B@out@B)/p-partial(B@rho@B)))
prob=np.array([.2,.27,.31,.24,.36,.41,.3]);E=P.copy()
for x in range(N):
 for y in range(N):
  E[x,y]*=np.prod([1-2*prob[i] for i in range(n) if ((x^y)>>i)&1])
min_effect=float(np.linalg.eigvalsh(E)[0]);lb=(2*min(prob))**n*p
assert res<1e-12 and badres<1e-12 and min_effect>=lb-1e-12
print(json.dumps({'uniform_effect_reference_operator_residual':res,'bad_radius_reference_operator_no_amplification_residual':badres,'axis_module_dimension':int(allowed.sum()),'biased_effect_smallest_eigenvalue':min_effect,'biased_uniform_lower_bound':float(lb),'scope':'Ideal DATA twirl/projection algebra with retained reference; no noisy acceptance or native timing.'},indent=2))
