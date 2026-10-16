from pathlib import Path
import numpy as np,json,hashlib
rng=np.random.default_rng(20261016)
def sup(A):return np.kron(A.conj(),A)
def diss(A):
 d=len(A);G=A.conj().T@A;return sup(A)-.5*(np.kron(np.eye(d),G)+np.kron(G.T,np.eye(d)))
def unitary(d):
 q,r=np.linalg.qr(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)));return q
mxp=mxk=mxg=0.;cases=0
for d in [2,3,4,8]:
 for case in range(8):
  A=(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)));A/=np.linalg.norm(A,2)
  if case==0:A[:,0]=0;A/=max(1,np.linalg.norm(A,2))
  l,s,r=np.linalg.svd(A);U=l@r;P=r.conj().T@np.diag(s)@r;V=r.conj().T@np.diag(s+1j*np.sqrt(np.maximum(0,1-s*s)))@r
  err=max(np.linalg.norm(U.conj().T@U-np.eye(d)),np.linalg.norm(V.conj().T@V-np.eye(d)),np.linalg.norm(A-(U@V+U@V.conj().T)/2));mxp=max(mxp,float(err));assert err<1e-12
 for phase,t in [(0,0),(.2,.1),(.9,1),(2.4,1)]:
  U=unitary(d);V=unitary(d);W=V.conj().T@U;M=.125;z=M*t*np.exp(1j*phase);theta=phase if t else 0;mag=abs(z)
  ks=[np.sqrt((M+mag)/2)*(U+np.exp(-1j*theta)*V),np.sqrt(max(0,(M-mag)/2))*(U-np.exp(-1j*theta)*V),np.sqrt(M/2)*W-z.conjugate()/np.sqrt(2*M)*np.eye(d),np.sqrt(M/2)*W.conj().T-z/np.sqrt(2*M)*np.eye(d),np.sqrt(max(0,M-mag*mag/M))*np.eye(d)]
  e=z*np.kron(V.conj(),U)+z.conjugate()*np.kron(U.conj(),V);S=z*W+z.conjugate()*W.conj().T;e-=.5*(np.kron(np.eye(d),S)+np.kron(S.T,np.eye(d)))
  F=M*(diss(U)+diss(V))+(M/2)*(diss(W)+diss(W.conj().T));got=sum(sup(K) for K in ks)-4*M*np.eye(d*d)
  ek=np.linalg.norm(sum(K.conj().T@K for K in ks)-4*M*np.eye(d));eg=np.linalg.norm(got-F-e);mxk=max(mxk,float(ek));mxg=max(mxg,float(eg));assert max(ek,eg)<1e-12;cases+=1
r={'status':'PASS_BOUNDED_ALGEBRA','dimensions':[2,3,4,8],'polar_cases':32,'edge_cases':cases,'max_polar_error':mxp,'max_kraus_intensity_error':mxk,'max_generator_error':mxg,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Finite numerical identities only; universal proof in KNOWN_OPERATOR_COMPILER.md; no physical or novelty validation.'}
Path(__file__).with_name('KNOWN_OPERATOR_CHECKS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
