import numpy as np,json
from scipy.linalg import expm
from pathlib import Path
N=40;n_keep=6;omega=1.;gA=gB=.25;T=2*np.pi
Z=np.diag([1,-1]);O=gA*np.kron(Z,np.eye(2))+gB*np.kron(np.eye(2),Z)
a=np.diag(np.sqrt(np.arange(1,N)),1);num=a.T@a
H=np.kron(np.eye(4),num)+np.kron(O,a+a.T)
U=expm(-1j*T*H);target=np.kron(expm(1j*2*np.pi*O@O),np.eye(N))
idx=[s*N+n for s in range(4) for n in range(n_keep)]
err=float(np.linalg.norm((U-target)[:,idx],2))
res={'oscillator_truncation':N,'audited_input_fock_states':n_keep,'gate_time':T,'ZZ_angle':4*np.pi*gA*gB,'finite_truncation_return_residual':err,'status':'Numerical diagnostic only; exact infinite oscillator proof in note'}
assert err<1e-11
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
