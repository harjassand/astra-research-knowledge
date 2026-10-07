"""Small diagnostic for SU(2) spin-one covariant broadcasters.
No solver, no universal theorem from these fixtures.
"""
import json, os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np
from pathlib import Path
I=np.eye(3,dtype=complex)
Jz=np.diag([1,0,-1]).astype(complex)
Jp=np.array([[0,2**.5,0],[0,0,2**.5],[0,0,0]],complex)
Js=[(Jp+Jp.conj().T)/2,(Jp-Jp.conj().T)/(2j),Jz]
dip=[x/2**.5 for x in Js]
quad=[]
for i in range(3):
 for j in range(i,3):
  A=(Js[i]@Js[j]+Js[j]@Js[i])/2
  A-=np.trace(A)*I/3
  for B in dip+quad: A-=np.trace(B.conj().T@A)*B
  n=np.linalg.norm(A)
  if n>1e-8: quad.append(A/n)
assert len(quad)==5

def star(fs):
 return sum(np.kron(H.T,np.kron(H,I)+np.kron(I,H)) for H in fs)
Kd,Kq=star(dip),star(quad)
records=[]
for a in [0,.01,.03,.1,.3,.5,.8,1,1.2,1.5,2,3,5,10,30,100]:
 b=1.
 K=a*Kd+b*Kq
 ev,u=np.linalg.eigh(K)
 v=u[:,ev>ev[-1]-1e-8]
 omega=v@v.conj().T/v.shape[1]
 lambdad=float(np.trace(omega@Kd).real/2)
 lambdaq=float(np.trace(omega@Kq).real/(2*5/3))
 V=a+5*b/3
 C=(a/2+b/6) if a>=b else 2*b/3
 F=ev[-1]/2
 ratio=(V-C)/(V-F)
 records.append(dict(a=a,b=b,lambda_dipole=lambdad,lambda_quad=lambdaq,positive=lambdad>=-1e-8 and lambdaq>=-1e-8,V=V,C=C,F=F,ratio=ratio,c2_slack=V+C-2*F,eig_multiplicity=v.shape[1]))
print(json.dumps(records,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(records,indent=2)+'\n')
