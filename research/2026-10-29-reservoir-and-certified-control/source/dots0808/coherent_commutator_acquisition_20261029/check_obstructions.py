"""Check the Schur-not-spectral interface and lost-flag-coherence counterexample."""
import numpy as np,json
from pathlib import Path
P=Path(__file__).parent
z=np.load(P/'twisted_collective_nonunital.npz');H=z['gram'];C=z['kernel'];c=C/np.linalg.norm(C);Ks=z['Kraus'];psi=z['memory_reference_input'];sig=psi@psi.conj().T
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);ops=[np.kron(a,b) for a in [X,Y,Z] for b in [X,Y,Z]];D=4
out=np.zeros((9,9),complex)
for K in Ks:
 ds=[K@np.kron(p,np.eye(2))-np.kron(p,np.eye(2))@K for p in ops]
 for j in range(9):
  for k in range(9):out[j,k]+=c[j]*c[k].conjugate()*np.trace(ds[j]@np.kron(np.eye(D),sig)@ds[k].conj().T)/(4*D)
rho=np.outer(c,c.conj());schur=.5*rho*H.T
assert np.linalg.norm(out-schur)<1e-12
pminus=np.trace(out).real;u=np.ones(9)/3;ppost=np.vdot(u,out@u).real
assert pminus>1e-3 and abs(ppost)<1e-12
# Identity source and flag dephasing: classical path mixture produces nonzero minus data.
# Plus/minus each probability1/2; product Pauli HS orthogonality makes retained control I9/18.
wrong=np.array([[np.trace(p@q)/(18*D) for q in ops] for p in ops]);assert np.linalg.norm(wrong-np.eye(9)/18)<1e-12
r={'kernel_coefficient_input_minus_probability':float(pminus),'kernel_coefficient_input_THEN_uniform_control_postselection_probability':float(ppost),'schur_formula_residual':float(np.linalg.norm(out-schur)),'false_spectral_map_residual':float(np.linalg.norm(out-H@rho@H)),'label_dephasing_destroys_kernel_residual':float(np.linalg.norm(np.diag(np.diag(H))@C)),'identity_channel_true_gram_zero':True,'identity_channel_with_flag_dephasing_minus_probability':float(np.trace(wrong).real),'scope':'These are exact-interface counterexamples evaluated numerically, not a lower bound against every possible downstream coherent algorithm.'}
(P/'obstructions.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
