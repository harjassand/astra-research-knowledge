import json,itertools,math,numpy as np,time
from pathlib import Path
root=Path('producer-workspace/four_program_extension');c=json.loads((root/'certificate.json').read_text())
from fractions import Fraction
B=np.array([[float(Fraction(x)) for x in row] for row in c['B']]);exps=[tuple(e) for e in c['exponents']];idx={e:i for i,e in enumerate(exps)}
T=np.array([B[idx[tuple(t.count(j) for j in range(4))],:] for t in itertools.product(range(4),repeat=4)])
K=np.zeros((256,256));cols=[16*a+b for a in range(9) for b in range(9)];K[:,cols]=4/math.sqrt(3)*T
A=K.T@K;I=np.eye(256);projectors={}
for lam in [0.,1/3,2/3,1.]:
 P=I.copy()
 for mu in [0.,1/3,2/3,1.]:
  if mu!=lam:P=P@(A-mu*I)/(lam-mu)
 projectors[lam]=P
D=projectors[0.]+math.sqrt(2/3)*projectors[1/3]+math.sqrt(1/3)*projectors[2/3]
E=I.copy()
for lam in [1/3,2/3,1.]:E+=(math.sqrt(1-lam)-1)/lam*(K@projectors[lam]@K.T)
U=np.block([[K,E],[D,-K.T]])
res=float(np.linalg.norm(U.T@U-np.eye(512),2));assert res<1e-11
# Actual known real-unitary QR decomposition into two-level row rotations.
Q=U.copy();rots=[];start=time.time()
for col in range(511):
 for row in range(511,col,-1):
  aa,bb=Q[row-1,col],Q[row,col]
  if abs(bb)<1e-16:continue
  norm=math.hypot(aa,bb);co,si=aa/norm,bb/norm
  old0=Q[row-1,:].copy();old1=Q[row,:].copy()
  Q[row-1,:]=co*old0+si*old1;Q[row,:]=-si*old0+co*old1
  rots.append((row-1,row,co,si))
qr_res=float(np.linalg.norm(Q-np.diag(np.diag(Q)),2));diag_res=float(max(abs(abs(np.diag(Q))-1)));assert qr_res<1e-10 and diag_res<1e-10
out=dict(dimension=512,encoded_qubits=9,valid_input_columns=len(cols),orthogonality_residual=res,two_level_rotations=len(rots),worst_dense_two_level_count=512*511//2,diagonal_sign_count=int(sum(np.diag(Q)<0)),qr_offdiagonal_residual=qr_res,diagonal_magnitude_residual=diag_res,qr_seconds=time.time()-start,scope='Executed double-precision known-unitary dilation and QR; no native gates or certified finite-precision synthesis')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
