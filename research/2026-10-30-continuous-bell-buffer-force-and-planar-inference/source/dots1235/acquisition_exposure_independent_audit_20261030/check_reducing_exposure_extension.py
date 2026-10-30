"""Independent quantum FREE/LOAD-guard exposure fixture with ACTIVE inflow.
Shows why zero extension is invalid and verifies local reducing compression.
This is a syntactic model of the guard algebra, not the native FIFO word.
"""
import numpy as np,json
from pathlib import Path
from scipy.linalg import solve,eigvalsh,expm
n=5;I=np.eye(n);F=np.diag([1.,1.,1.,1.,0.]);P=np.diag([0.,0.,0.,1.,0.]);A=I-F
H=np.zeros((n,n),complex);H[0,1]=H[1,0]=.8
spec=[(2,1,.9),(0,2,.4),(0,3,.4),(3,2,.7),(0,4,1.2),(0,0,.3),(0,1,.3)]
js=[]
for target,source,rate in spec:
 j=np.zeros((n,n),complex);j[target,source]=np.sqrt(rate);js.append(j)
def gen(jumps,O):return 1j*(H@O-O@H)+sum(j.conj().T@O@j-(j.conj().T@j@O+O@j.conj().T@j)/2 for j in jumps)
jred=[F@j@F+A@j@A for j in js];C=P+A
L=lambda O:gen(js,O);Lred=lambda O:gen(jred,O)
K=lambda O:Lred(O)-(C@O+O@C)/2
cols=[]
for i in range(n*n):
 e=np.zeros((n,n),complex);e.flat[i]=1;cols.append(K(e).ravel())
KM=np.column_stack(cols);R=solve(KM,-I.ravel()).reshape(n,n);R=(R+R.conj().T)/2
norm=lambda O:float(np.linalg.norm(O,2));top=lambda O:float(eigvalsh((O+O.conj().T)/2)[-1])
Rzero=F@R@F
bound=F@L(R)@F+F-norm(R)*P
out={'dimension':n,'FREE_dimension':4,'LOAD_guard_dimension':1,'active_inflow_rate':1.2,'resolvent_min_eigenvalue':float(eigvalsh(R)[0]),'resolvent_max_eigenvalue':float(eigvalsh(R)[-1]),'commutator_FREE':norm(R@F-F@R),'commutator_LOAD_guard':norm(R@P-P@R),'resolvent_equation_error':norm(K(R)+I),'compressed_actual_equals_reducing_error':norm(F@(L(R)-Lred(R))@F),'maximum_exposure_bound_violation':top(bound),'invalid_zero_extension_active_derivative':float((A@L(Rzero)@A)[4,4].real),'coherent_Q0_Q1_resolvent_entry':float(abs(R[0,1])),'scope':'exact reducing-extension and guard-commutant algebra, not actual native FIFO arrival service'}
assert out['commutator_FREE']<1e-11 and out['commutator_LOAD_guard']<1e-11
assert out['resolvent_min_eigenvalue']>0
assert out['resolvent_equation_error']<1e-11
assert out['compressed_actual_equals_reducing_error']<1e-11
assert out['maximum_exposure_bound_violation']<1e-11
assert out['invalid_zero_extension_active_derivative']>1
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
