"""Operator regression of the continuous-noise moment hierarchy.
Two healing system qubits, shared quantum bath, noncommuting coherent bath
couplings and a joint Lindblad perturbation. No sampled fault record.
"""
import numpy as np,json
from scipy.linalg import expm,eigvalsh
from pathlib import Path
I2=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);lower=np.array([[0,1],[0,0]],complex);Q=np.diag([0,1])
kron=lambda a,b,c:np.kron(np.kron(a,b),c)
I=np.eye(8);qs=[kron(Q,I2,I2),kron(I2,Q,I2)]
r=1.;eta=.025;beta=.7
H=.31*kron(I2,I2,Y)+eta*(kron(X,I2,X)+kron(I2,X,Z)+kron(X,X,I2))
jumps=[np.sqrt(r)*kron(lower,I2,I2),np.sqrt(r)*kron(I2,lower,I2),np.sqrt(eta)*kron(lower.conj().T,I2,X)]
L=1j*(np.kron(np.eye(8),H)-np.kron(H.T,np.eye(8)))
for J in jumps:
    A=J.conj().T@J
    L+=np.kron(J.T,J.conj().T)-.5*np.kron(np.eye(8),A)-.5*np.kron(A.T,np.eye(8))
def apply(O):return (L@O.reshape(-1,order='F')).reshape((8,8),order='F')
F={0:I,1:I+beta*qs[0],2:I+beta*qs[1],3:(I+beta*qs[0])@(I+beta*qs[1])}
# Each Hamiltonian source has adjoint norm <=2 eta. System0 also has
# a Lindblad perturbation with norm <=2 eta: max incident sum c_e is6.
Jincident=6.;b=2;C=Jincident*((1+beta)**b-1)
max_inst=-1e100;max_evol=-1e100
for mask in [1,2,3]:
    m=mask.bit_count();rhs=-r*m*F[mask]+(r+eta*C)*sum(F[mask^(1<<i)] for i in range(2) if mask>>i&1)
    defect=apply(F[mask])-rhs;defect=(defect+defect.conj().T)/2
    val=float(eigvalsh(defect)[-1]);max_inst=max(max_inst,val);assert val<1e-11
for t in np.linspace(0,8,33):
    E=expm(t*L);u=1+eta*C/r+(beta-eta*C/r)*np.exp(-r*t)
    for mask in [1,2,3]:
        out=(E@F[mask].reshape(-1,order='F')).reshape((8,8),order='F')
        defect=out-u**mask.bit_count()*I;defect=(defect+defect.conj().T)/2
        val=float(eigvalsh(defect)[-1]);max_evol=max(max_evol,val);assert val<1e-10,(t,mask,val)
out={'system_qubits':2,'shared_bath_qubits':1,'continuous_H_noise_terms':3,'continuous_Lindblad_noise_terms':1,'noncommuting_bath_operators':True,'beta':beta,'eta':eta,'r':r,'incident_norm_budget_J':Jincident,'max_touched_factors_b':b,'C_beta':C,'subset_checks_per_time':3,'time_points':33,'maximum_instantaneous_bound_violation':max_inst,'maximum_evolved_operator_bound_violation':max_evol,'all_joint_states_and_references_by_operator_check':True,'all_checks_pass':True,'scope':'generic moment-hierarchy algebra, not simulation of the full native LOCC apparatus'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
