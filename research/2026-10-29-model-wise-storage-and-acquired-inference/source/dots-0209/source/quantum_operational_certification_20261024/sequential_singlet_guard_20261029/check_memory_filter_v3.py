import numpy as np,json
rng=np.random.default_rng(2026102909);I=np.eye(2);X=np.array([[0,1],[1,0]])
B0=np.diag(np.sqrt([.8,.4]));B1=X@np.diag(np.sqrt([.1,.3]));Babort=np.diag(np.sqrt([.1,.3]));Ebad=B1.conj().T@B1;Eacc=B0.conj().T@B0+Ebad;eps=np.linalg.eigvalsh(Ebad).max();maxdist=0
for _ in range(200):
 v=rng.normal(size=8)+1j*rng.normal(size=8);v/=np.linalg.norm(v);rho=np.outer(v,v.conj());A0=np.kron(np.kron(I,B0),I);A1=np.kron(np.kron(X,B1),I);Aid=np.kron(np.kron(I,B1),I)
 real=A0@rho@A0.conj().T+A1@rho@A1.conj().T;ideal=A0@rho@A0.conj().T+Aid@rho@Aid.conj().T;dist=.5*sum(abs(np.linalg.eigvalsh(real-ideal)));maxdist=max(maxdist,dist);assert dist<=eps+1e-12
phi=np.array([1,0,0,1])/np.sqrt(2);rho=np.outer(phi,phi);filtered=sum(np.kron(I,B)@rho@np.kron(I,B).conj().T for B in [B0,B1]);p=np.trace(filtered).real;marg=np.einsum('abcb->ac',filtered.reshape(2,2,2,2))/p
print(json.dumps({'scope':'Illustrative finite CP-instrument/flag-norm check of correlated-input ideal; not replacement for sequential source fixture','bad_effect_eigenvalues':np.linalg.eigvalsh(Ebad).tolist(),'accepted_effect_eigenvalues':np.linalg.eigvalsh(Eacc).tolist(),'uniform_halfdiamond_bound':float(eps),'max_trace_distance_over_200_entangled_reference_inputs':float(maxdist),'correlated_Bell_input_acceptance':float(p),'ideal_accepted_user_marginal_diagonal':np.diag(marg).real.tolist(),'initial_user_marginal_diagonal':[.5,.5]},indent=2))
