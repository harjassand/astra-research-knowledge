import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np,json,itertools
from pathlib import Path
from scipy.linalg import expm
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);J=.2;g=1.;dt=.4;S=np.kron(Z,I)
H=np.kron(I,3*X)+J*np.kron(X,Z);n=4
L=-1j*(np.kron(np.eye(n),H)-np.kron(H.T,np.eye(n)))+g*(np.kron(S.T,S)-np.eye(n*n));E=expm(dt*L)
P=[np.diag([1,1,0,0]),np.diag([0,0,1,1])]
bath=np.array([[.5,.3j],[-.3j,.5]]);rho0=np.kron(np.diag([1,0]),bath)
eps=J*J/g*(dt+np.expm1(-2*g*dt)/(2*g));paths=[]
for outcomes in itertools.product(range(2),repeat=5):
 rho=rho0.copy();prev=0;flips=[]
 for s in outcomes:
  rho=(E@rho.reshape(-1,order='F')).reshape((n,n),order='F');rho=P[s]@rho@P[s];flips.append(s!=prev);prev=s
 paths.append((flips,float(np.trace(rho).real)))
assert abs(sum(p for _,p in paths)-1)<1e-12
maxratio=0
for mask in range(1,32):
 slots=[j for j in range(5) if (mask>>j)&1]
 prob=sum(p for flips,p in paths if all(flips[j] for j in slots));b=eps**len(slots)
 assert prob<=b+1e-13;maxratio=max(maxratio,prob/b)
# Simultaneous spatial counterexample: one XX term flips BOTH checks.
H=J*np.kron(X,X);S1=np.kron(Z,I);S2=np.kron(I,Z);t=.01
L=-1j*(np.kron(np.eye(n),H)-np.kron(H.T,np.eye(n)))+sum(g*(np.kron(A.T,A)-np.eye(n*n)) for A in [S1,S2])
rho=np.diag([1,0,0,0]);out=(expm(t*L)@rho.reshape(-1,order='F')).reshape((n,n),order='F')
pboth=float(out[3,3].real);single_bound=J*J/g*(t+np.expm1(-2*g*t)/(2*g))
r={'serial_intervals':5,'all_specified_flip_subsets_checked':31,'epsilon':eps,'maximum_probability_to_product_bound_ratio':maxratio,'spatial_joint_flip_probability':pboth,'invalid_product_of_single_check_bounds':single_bound**2,'ratio_joint_to_invalid_product':pboth/single_bound**2}
Path(__file__).with_name('serial_checks.json').write_text(json.dumps(r,indent=2));print(r)
