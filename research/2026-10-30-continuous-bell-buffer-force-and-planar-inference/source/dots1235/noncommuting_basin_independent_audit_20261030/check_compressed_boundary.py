import numpy as np,json
from scipy.linalg import expm
from pathlib import Path
I2=np.eye(2,dtype=complex);X2=np.array([[0,1],[1,0]],complex);Y2=np.array([[0,-1j],[1j,0]],complex);n2=np.diag([0.,1.]);norm=lambda a:float(np.linalg.norm(a,2))
def at(n,pairs):
 a=np.ones((1,1),complex)
 for i in range(n):a=np.kron(a,pairs.get(i,I2))
 return a
rows=[]
for n in [3,4,5]:
 d=2**n;I=np.eye(d);E=sum(at(n,{i:n2}) for i in range(n));ener=np.diag(E).real
 cut=max(1,n//2);inds=np.where(ener<=cut)[0];P=np.diag((ener<=cut).astype(float));Q=I-P
 R=np.diag((ener>=max(0,cut-1)).astype(float))
 s=.7;t=.012;delta=.022;a=.08
 A=np.diag(np.exp((s-t)*ener));As=np.diag(np.sqrt(np.diag(A)));A0=A[np.ix_(inds,inds)]
 gates=[]
 for parity in [0,1]:
  for i in range(parity,n-1,2):gates.append((I+at(n,{i:X2,i+1:X2}))/2)
 gates += [(I+at(n,{i:Y2}))/2 for i in range(n)]
 Y=I.astype(complex);Ybd=I.astype(complex);Y0=np.eye(len(inds),dtype=complex);crossres=0.
 for X in gates:
  Xbd=P@X@P+Q@X@Q;cross=X-Xbd
  crossres=max(crossres,norm(cross-R@cross@R))
  Y=Y@expm(delta*X/2);Ybd=Ybd@expm(delta*Xbd/2)
  Y0=Y0@expm(delta*X[np.ix_(inds,inds)]/2)
 G0=Y0.conj().T@Y0;As0=np.diag(np.sqrt(np.diag(A0)));W0=As0@G0@As0
 vals,vecs=np.linalg.eigh(W0);p1=vecs[:,vals<=np.exp(a*n)];P1small=p1@p1.conj().T
 P1=np.zeros((d,d),complex);P1[np.ix_(inds,inds)]=P1small
 F=Q.astype(complex);F[np.ix_(inds,inds)]=W0
 W=As@Y.conj().T@Y@As;Wbd=As@Ybd.conj().T@Ybd@As
 invG=np.linalg.inv(G0);invW=np.linalg.inv(W0);powerres=[]
 for k in [1,2,3]:
  left=np.linalg.matrix_power(A0,k)@np.linalg.matrix_power(invW,k)
  right=np.eye(len(inds),dtype=complex)
  diag=np.diag(A0)
  for j in range(k,0,-1):
   right=right@np.diag(diag**(j-.5))@invG@np.diag(diag**(-j+.5))
  powerres.append(norm(left-right)/max(1,norm(left)))
 assert max(powerres)<1e-11 and crossres<1e-13
 rows.append({'N':n,'outer_dimension':len(inds),'inner_dimension':p1.shape[1],'crossing_strip_residual':crossres,'inverse_power_identity_relative_residuals':powerres,'P_block_Wdiag_equals_W0_residual':norm(P@(Wbd-F)@P),'inner_bilinear_FminusW_norm':norm(P1@(F-W)@P1),'inserted_local_bilinear_norm':norm(P1@at(n,{0:X2})@(F-W)@at(n,{0:X2})@P1)})
# Exact local counterexample to the unrepaired raw-P compression inequality.
delta=.05;M=3.;S=np.diag([1.,np.sqrt(M)]);Y=expm(delta*(I2+Y2)/2);W=S@Y.conj().T@Y@S;P=np.diag([1.,0.]);H=X2
full=P@(1j*(H@W-W@H))@P;killed=np.zeros((2,2),complex)
assert full[0,0].real<0
out={'scope':'Finite algebra only; no asymptotic boundary estimate inferred from these sizes.','compressed_checks':rows,'naive_killed_compression_counterexample':{'one_site_positive_gate':True,'compressed_full_drift':float(full[0,0].real),'killed_drift':0.,'false_order_violation':float((killed-full)[0,0].real)}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
