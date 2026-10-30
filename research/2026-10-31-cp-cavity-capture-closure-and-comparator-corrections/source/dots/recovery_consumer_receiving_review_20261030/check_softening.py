import numpy as np,json
rng=np.random.default_rng(20261030)
worst=1.; worst_foster=1.; worst_drop=1.; comm=0.
for trial in range(1000):
 d=4; N=7; s=.6; lam=.9; k=.7; g=.08
 E=rng.integers(0,9,d); logs=rng.uniform(0,g*N,d); v=np.exp(s*E+logs)
 Us=[]
 for z in range(3):
  x=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); q,r=np.linalg.qr(x); Us.append(q)
 def T(x):return sum(u.conj().T@np.diag(x)@u for u in Us)/len(Us)
 fv=T(v); logv=T(v*np.log(v)); ev=T(E*v)
 margin=lam*ev-k*logv+k*g*N*fv
 worst=min(worst,float(np.linalg.eigvalsh(margin)[0]))
 comm=max(comm,float(np.linalg.norm(fv@logv-logv@fv)))
 c=.8; foster=logv-c*N*fv+np.exp(c*N-1)*np.eye(d)
 worst_foster=min(worst_foster,float(np.linalg.eigvalsh(foster)[0]))
 roots=1+rng.exponential(size=3); a=1.
 ffull=np.kron(np.diag(roots),fv); fdrop=np.kron(np.eye(3),fv)
 drop=np.exp(-a*N)*(ffull-fdrop)
 worst_drop=min(worst_drop,float(np.linalg.eigvalsh(drop)[0]))
assert min(worst,worst_foster,worst_drop)>-1e-8
print(json.dumps(dict(trials=1000,min_log_conversion_eigenvalue=worst,min_scalar_foster_eigenvalue=worst_foster,min_factor_drop_eigenvalue=worst_drop,max_noncommutation=comm,scope='finite algebra regressions only; proof in review'),indent=2))
