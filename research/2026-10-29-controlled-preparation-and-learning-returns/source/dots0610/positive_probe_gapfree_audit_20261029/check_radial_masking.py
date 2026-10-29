import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(295452)
# Generic finite positive linear-loss actions, independent of SO3 geometry.
A=np.array([[1.,0,1],[0,1,1],[-1.,0,1],[0,-1,1]])
ell=np.array([.1,.2,.4]);q=A@ell;sc=np.repeat([.5,1.],len(A));rad=np.vstack([A/2,A]);w=rng.dirichlet(np.ones(8),size=50);xs=w@rad;alpha=w@sc;mix=rng.dirichlet(np.ones(50));S=np.einsum('i,ij,ik->jk',mix,xs,xs)
physical=[];weighted=[];second=[]
for j in range(50):
 p=(w[j,:4]*.5+w[j,4:])/alpha[j]
 assert abs(p.sum()-1)<1e-12 and np.linalg.norm(alpha[j]*(p@A)-xs[j])<1e-12
 phys=p@q;z=alpha[j]*phys;z2=alpha[j]**2*phys
 assert z2<=z+1e-12 and phys<=2*z+1e-12
 physical.append(phys);weighted.append(z);second.append(z2)
rho=.017
estimate=sum(mix[j]*np.linalg.solve(S,xs[j])*rho*weighted[j] for j in range(50))
assert np.linalg.norm(estimate-rho*ell)<1e-12
out={'radial_examples':50,'unbiased_masked_estimator_residual':float(np.linalg.norm(estimate-rho*ell)),'maximum_physical_to_weighted_ratio':float(max(p/z for p,z in zip(physical,weighted))),'scope':'Finite conditional-expectation identity only; no continuous-density learner simulation.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(out)
