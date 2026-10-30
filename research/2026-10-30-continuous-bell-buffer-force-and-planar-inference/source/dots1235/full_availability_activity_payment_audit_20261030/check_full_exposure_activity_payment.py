"""Abstract source-corner diagnostic for the repaired exposure product.
This is not a simulation of the full native FSM. Its C-terminal reset structure,
source resolution and noncommuting ACTIVE-clock observable test the exact
algebra used in FULL_AVAILABILITY_DRIFT_AND_ACTIVITY_PAYMENT.md.
"""
import numpy as np,json
from pathlib import Path
# Controller order FREE,C0,C1; nontrivial ACTIVE coherence is deliberate.
R=np.array([[.9,0,0],[0,.5,.2],[0,.2,.7]],complex)
A=np.diag([0.,1.,1.]);I=np.eye(3)
energies=np.array([1.,2.,3.]);s=.4
v=np.diag(np.exp(s*energies));sv=np.diag(np.exp(s*energies/2))
a=np.diag([.4,.2,.6]);a_g=np.diag([0.,1-np.exp(-s),1-np.exp(-s)])
Rt=np.kron(R,I);At=np.kron(A,I);X=np.kron(R,a)
S=np.kron(I,sv);Si=np.linalg.inv(S)
jctrl=np.zeros((3,3),complex);jctrl[0,2]=1
js=[]
for j,f in enumerate([0,0,1]):
 jd=np.zeros((3,3),complex);jd[f,j]=1
 js.append(np.kron(jctrl,jd))
jp=[S@j@Si for j in js]
def lind(o,legs):
 gamma=sum(j.conj().T@j for j in legs)
 return sum(j.conj().T@o@j for j in legs)-(gamma@o+o@gamma)/2
physical_R=lind(Rt,js)
# Complete physical gain is type-only: recover its exact controller matrix.
Rdot=physical_R.reshape(3,3,3,3)[:,0,:,0]
assert np.linalg.norm(physical_R-np.kron(Rdot,I))<1e-12
D=lind(X,jp)-np.kron(Rdot,a)
free=np.eye(9)-At
corner=np.linalg.norm(D-At@D@At,2)
Gamma=sum(j.conj().T@j for j in js)
# On g's no-move data label0, the true full controller drift is nonzero,
# while the PRODUCT DISCREPANCY is zero; it must not have been dropped.
inds=[3*i for i in range(3)]
no_move_full=lind(X,js)[np.ix_(inds,inds)]
no_move_discrepancy=D[np.ix_(inds,inds)]
# Tiny classical contention chain: h acquisition rate1; g pending READ races
# h with rate2, then Alice-g holds the shared lock for mean1/mu. Bob LOAD absent.
lam=2.;mu=.5
Q=np.array([[-1,0,0],[0,-(1+lam),lam],[mu,0,-mu]],float)
mean=np.linalg.solve(-Q,np.ones(3))
res={'scope':'abstract exact product/source-corner and classical contention diagnostics, not full native proof','R_positive_min':float(np.linalg.eigvalsh(R).min()),'R_ACTIVE_commutator':float(np.linalg.norm(Rt@At-At@Rt)),'R_terminal_loss_commutator':float(np.linalg.norm(Rt@Gamma-Gamma@Rt)),'product_error_outside_ACTIVE':float(corner),'product_error_norm':float(np.linalg.norm(D,2)),'no_move_terminal_full_availability_product_drift':float(np.linalg.norm(no_move_full,2)),'no_move_product_discrepancy_after_retaining_physical_drift':float(np.linalg.norm(no_move_discrepancy,2)),'mean_ready_time_no_neighbor_request':float(mean[0]),'mean_ready_time_neighbor_READ_pending':float(mean[1]),'mean_ready_time_neighbor_Alice_lock_busy':float(mean[2])}
assert corner<1e-12 and res['R_terminal_loss_commutator']>.1
assert res['no_move_terminal_full_availability_product_drift']>.05
assert res['no_move_product_discrepancy_after_retaining_physical_drift']<1e-12
assert mean[1]>mean[0]
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
