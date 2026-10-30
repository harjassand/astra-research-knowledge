"""Noncommuting full-Hilbert singleton witnesses and common-bath noise scaling.
Finite algebra diagnostic only; not a native many-body or logical-memory simulation.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm
I2=np.eye(2);X=np.array([[0,1],[1,0]],complex);Yp=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=np.diag([0,1]);sm=np.array([[0,1],[0,0]],complex)
def kron(*xs):
 o=np.array([[1]],complex)
 for x in xs:o=np.kron(o,x)
 return o
# Two controller flags, one degenerate payload/auxiliary factor, one common bath.
I=np.eye(16);P0=kron(P,I2,I2,I2);P1=kron(I2,P,I2,I2);M=P0+P1
X0=P0@(I+.2*kron(I2,I2,X,I2));X1=P1@(I+.2*kron(I2,I2,Z,I2))
H0=.1*M@kron(I2,I2,Yp,I2)
Js=[2*kron(sm,I2,I2,I2),2*kron(I2,sm,I2,I2)]
Hs=[kron(X,I2,I2,I2),kron(I2,X,I2,I2)]
def dissip(J,O):
 JJ=J.conj().T@J;return J.conj().T@O@J-(JJ@O+O@JJ)/2
def L0(O):return 1j*(H0@O-O@H0)+sum((dissip(j,O) for j in Js),np.zeros_like(O))
for p,x in [(P0,X0),(P1,X1)]:
 assert np.linalg.eigvalsh(L0(x)+p).max()<1e-12
 for q in [P0,P1]:assert np.linalg.norm(x@q-q@x)<1e-12
noncomm=float(np.linalg.norm(X0@X1-X1@X0));assert noncomm>0
Hn=kron(X,I2,I2,X)+.37*kron(I2,I2,Z,Z)
Jn=.5*kron(I2,sm.conj().T,I2,X)
def Noise(O):return 1j*(Hn@O-O@Hn)+dissip(Jn,O)
assert np.linalg.norm(Noise(I))==0
records=[];noise=[]
for delta in [.001,.005,.02,.08,.16]:
 yy=expm(delta*X0)@expm(delta*X1);G=yy.conj().T@yy
 ev,V=np.linalg.eigh(G);Gi=(V/np.sqrt(ev))@V.conj().T
 lo=np.linalg.eigvalsh(G-expm(1.6*delta*M)).min();up=np.linalg.eigvalsh(expm(2.4*delta*M)-G).min()
 assert lo>-1e-12 and up>-1e-12
 Qready=(I-P0)@(I-P1);assert np.linalg.norm((G-I)@Qready)<1e-12
 for eps in [.002,.01,.04,.1]:
  H=Hs[0]+Hs[1];LG=L0(G)+eps*1j*(H@G-G@H)
  # Reserve a=2 and an intentionally loose C0=16.
  residual=Gi@(LG+(2*delta*M-16*delta*eps**2*2*I)@G)@Gi
  e=float(np.linalg.eigvalsh(residual).max());assert e<1e-11
  records.append({'delta':delta,'epsilon':eps,'max_relative_drift_residual':e})
 nrel=Gi@Noise(G)@Gi;ratio=float(np.linalg.norm(nrel,2)/delta)
 noise.append({'delta':delta,'relative_noise_norm':float(np.linalg.norm(nrel,2)),'relative_noise_norm_over_delta':ratio})
assert max(x['relative_noise_norm_over_delta'] for x in noise)<10
out={'dimension':16,'noncommuting_witness_commutator_norm':noncomm,'drift_checks':records,'centered_common_bath_noise_scaling':noise,'all_ready_initial_G_equals_I':True,'scope':'Noncommuting-witness/weak-block/noise-derivative algebra in a fixed16D fixture. Native locality, code protection and long-time concentration rely on the analytic proof and reviewed actual witness.'}
Path(__file__).with_name('singleton_busy_congruence_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
