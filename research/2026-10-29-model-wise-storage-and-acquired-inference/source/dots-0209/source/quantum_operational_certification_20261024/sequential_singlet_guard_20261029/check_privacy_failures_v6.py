import numpy as np,json
from scipy.linalg import eigh,expm
from functools import reduce
P=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])];kron=lambda xs:reduce(np.kron,xs);n=4;d=16
J=[sum(kron([P[a] if i==j else P[0] for i in range(n)]) for j in range(n))/2 for a in [1,2,3]];v,Z=eigh(sum(A@A for A in J));E=Z[:,v<1e-8];Ps=E@E.conj().T;rows=[]
for i in range(n):
 for j in range(i+1,n):
  idx=[]
  for x in range(d):
   a=(x>>(3-i))&1;b=(x>>(3-j))&1;idx.append(x^((a^b)<<(3-i))^((a^b)<<(3-j)))
  S=np.eye(d)[idx];q=(1-np.trace(Ps@S@S.conj().T@S@S).real/2)/2;Fe=abs(np.trace(E.conj().T@S@E))**2/4
  assert abs(q)<1e-12 and Fe<1e-20
  rows.append({'edge':[i,j],'leaked_edge_test_failure':float(q),'service_Bell_loss':float(1-Fe)})
phi=np.eye(2).reshape(-1)/np.sqrt(2);rho=np.outer(phi,phi);theta=.1;out=[]
for sign in [1,-1]:
 U=np.kron(expm(1j*sign*theta*P[3]),P[0]);out.append(U@rho@U.conj().T)
retired=sum(out)/2;flagdistance=sum(.25*np.abs(np.linalg.eigvalsh(A-rho)).sum() for A in out);retireddistance=.5*np.abs(np.linalg.eigvalsh(retired-rho)).sum()
assert abs(flagdistance-abs(np.sin(theta)))<1e-12 and abs(retireddistance-np.sin(theta)**2)<1e-12
print(json.dumps({'edge_examples':rows,'late_key_release':{'theta':theta,'retired_key_halfdiamond':float(retireddistance),'accessible_sign_record_halfdiamond':float(flagdistance),'sin_squared':float(np.sin(theta)**2),'sin_absolute':float(abs(np.sin(theta)))}},indent=2))
