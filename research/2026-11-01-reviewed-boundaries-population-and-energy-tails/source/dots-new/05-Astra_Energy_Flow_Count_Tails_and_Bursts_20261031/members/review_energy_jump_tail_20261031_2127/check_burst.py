import numpy as np, json
from scipy.linalg import expm
from pathlib import Path
p=Path(__file__).parent
I=np.eye(3); H=np.diag([0.,1.,2.]); L1=np.zeros((3,3)); L1[0,1]=np.sqrt(2); L2=np.zeros((3,3));L2[1,2]=2
Ls=[L1,L2];D=sum(L.T@L for L in Ls);J=sum(np.kron(L,L) for L in Ls)
kappa=2
GstarH=sum(L.T@H@L-.5*(L.T@L@H+H@L.T@L) for L in Ls)
c=(1-np.exp(-1))**2*(1-np.exp(-2))/8
rows=[]
for g in [.001,.003,.01,.1,.5,1.]:
 V=np.zeros((3,3));V[0,2]=V[2,0]=g
 B=-1j*(np.kron(I,V)-np.kron(V.T,I))-.5*(np.kron(I,D)+np.kron(D.T,I))
 S=B+J;Z=np.zeros_like(B)
 # Density blocks for zero, exactly one, and at least two physical counts.
 A=np.block([[B,Z,Z],[J,B,Z],[Z,J,S]])
 rho=np.diag([1.,0.,0.]);x=np.concatenate([rho.reshape(-1,order='F'),np.zeros(18)])
 y=expm(2*A)@x
 probs=[np.trace(y[i*9:(i+1)*9].reshape(3,3,order='F')).real for i in range(3)]
 rows.append({'g':g,'P_N2_ge_2':probs[2],'lower_bound':c*g*g,'P_over_g_squared':probs[2]/g**2,'total_probability':sum(probs)})
assert all(z['P_N2_ge_2']>=z['lower_bound']-1e-12 and abs(z['total_probability']-1)<1e-10 for z in rows)
out={'GstarH_plus_kappaH_norm':float(np.linalg.norm(GstarH+kappa*H)),'intensity_minus_2H_norm':float(np.linalg.norm(D-2*H)),'lower_bound_coefficient':c,'rows':rows,'limitations':'Floating-point matrix-exponential corroboration only, not an exact arithmetic certificate or physical device.'}
(p/'check_burst.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
