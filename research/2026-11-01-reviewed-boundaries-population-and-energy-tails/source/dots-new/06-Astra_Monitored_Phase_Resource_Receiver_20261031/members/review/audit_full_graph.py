"""Direct simultaneous two-source/two-data laboratory Lindbladian audit."""
from pathlib import Path
import itertools,json
import numpy as np
from scipy.linalg import expm
from scipy import sparse as sp
from scipy.sparse.linalg import expm_multiply
from audit_independent import physical_bin,local_chans,kron,I,X,Z,sm
import monitored_phase as candidate
root=Path(__file__).resolve().parent
T=.7;bins=2
params=[(1,4,.3,.8,.35,T,.05),(.7,0,2,.2,.9,T,.03)]
q0=[0,1];angles=[.31,-.23,.49]
# Hilbert order S0,S1,D0,D1. Full H includes target and coupling simultaneously.
H=angles[0]/T*kron(I,I,Z,I)+angles[1]/T*kron(I,I,I,Z)+angles[2]/T*kron(I,I,Z,Z)
H=H+params[0][0]*kron(X,I,Z,I)+params[1][0]*kron(I,X,I,Z)
L=[kron(sm,I,I,I),kron(I,sm,I,I)]
Is=sp.eye(16,format='csc');Iv=sp.eye(256,format='csc')
kr=lambda a,b:sp.kron(a,b,format='csc')
H=sp.csc_matrix(H);A=-1j*(kr(Is,H)-kr(H.T,Is))
J=[]
for l,par in zip(L,params):
 c,loss,up,em,ep,T,d=par;l=sp.csc_matrix(l);q=l.conj().T@l;p=l@l.conj().T
 A-=loss/2*(kr(Is,q)+kr(q.T,Is))+up/2*(kr(Is,p)+kr(p.T,Is))
 J.append((loss*kr(l.conj(),l),up*kr(l.T.conj(),l.T)))
blocks=[[sp.csc_matrix((256,256),dtype=complex) for j in range(4)] for i in range(4)]
for flag in range(4):
 blocks[flag][flag]+=A
 for idx,par in enumerate(params):
  c,loss,up,em,ep,T,d=par;jm,jp=J[idx]
  if flag & (1<<idx):blocks[flag][flag]+=jm+jp
  else:
   blocks[flag][flag]+=(1-em)*jm+(1-ep)*jp-d*Iv
   blocks[flag|(1<<idx)][flag]+=em*jm+ep*jp+d*Iv
G=sp.bmat(blocks,format='csc')*(T/bins)
source=kron(np.diag([1,0]),np.diag([0,1]));init=np.zeros((256,16),complex)
for col in range(16):
 u=np.zeros(16);u[col]=1;u=u.reshape(4,4,order='F');init[:,col]=kron(source,u).reshape(256,order='F')
branches={():init}
for step in range(bins):
 records=list(branches);inp=np.zeros((1024,16*len(records)),complex)
 for j,r in enumerate(records):inp[:256,16*j:16*j+16]=branches[r]
 result=expm_multiply(G,inp)
 branches={r+(flag,):result[256*flag:256*(flag+1),16*j:16*j+16] for j,r in enumerate(records) for flag in range(4)}
locals_=[local_chans(par,q) for par,q in zip(params,q0)]
Ks=[a[0] for a in locals_];risks=[a[1] for a in locals_];decisions=[a[3] for a in locals_]
out=np.zeros((16,16),complex)
branch_weights=[]
for rec,m in branches.items():
 bits=[[int(bool(f&(1<<idx))) for f in rec] for idx in range(2)]
 correction=[decisions[i][(tuple(bits[i]),None)] for i in range(2)]
 U=kron(*[Z if b else I for b in correction]);reduced=np.zeros((16,16),complex)
 for col in range(16):
  rho=m[:,col].reshape(16,16,order='F');datarho=sum(rho[4*s:4*s+4,4*s:4*s+4] for s in range(4))
  reduced[:,col]=(U@datarho@U).reshape(16,order='F')
 out+=reduced
 # Every outcome law must be data independent: trace-row times branch = w trace-row.
 tr=np.eye(4).reshape(16,order='F');law=tr@reduced;weight=float(law[0].real)
 assert np.linalg.norm(law-weight*tr)<5e-12
 branch_weights.append(weight)
U=expm(-1j*(angles[0]*kron(Z,I)+angles[1]*kron(I,Z)+angles[2]*kron(Z,Z)))
expected=np.zeros((16,16),complex)
for bs in itertools.product([0,1],repeat=2):
 zz=kron(*[Z if b else I for b in bs]);w=np.prod([p if b else 1-p for b,p in zip(bs,risks)]);u=zz@U
 expected+=w*kron(u.conj(),u)
error=float(np.linalg.norm(out-expected));assert error<5e-11
# Recover joint error probabilities from the output on the weighted graph resource.
plus=np.ones(4)/2;target=U@plus;rho0=np.outer(plus,plus);final=(out@rho0.reshape(16,order='F')).reshape(4,4,order='F')
joint=[]
for bs in itertools.product([0,1],repeat=2):
 vec=kron(*[Z if b else I for b in bs])@target;p=float(np.vdot(vec,final@vec).real)
 pred=float(np.prod([r if b else 1-r for b,r in zip(bs,risks)]));assert abs(p-pred)<5e-12;joint.append(dict(errors=bs,actual=p,predicted=pred))

# Independent actual-lab echo channel: global sign flips must be received as a
# final known X frame for an arbitrary data channel, even when they cancel on |+>.
echo=[]
for c,l,a,T,bins,q in [(1,16,0,1,4,0),(.6,2,.3,.7,4,1),(1,1,0,1,64,0)]:
 M=sum(physical_bin(c,l,a,0,0,T/bins,0));S=kron(np.diag([1,0]) if q==0 else np.diag([0,1]),np.ones((2,2))/2)
 F=kron(I,X);Ad=kron(F.conj(),F);rho=S.reshape(16,order='F')
 for j in range(bins):
  rho=M@rho
  if j<bins-1:rho=Ad@rho
 if (bins-1)%2:rho=Ad@rho
 rho=rho.reshape(4,4,order='F');d=rho[:2,:2]+rho[2:,2:];p=float((1-2*d[0,1].real)/2)
 theory=candidate.raw_error(c,l,a,T,bins-1);assert abs(p-theory)<5e-12
 echo.append(dict(c=c,loss=l,up=a,T=T,pulses=bins-1,q0=q,actual=p,theory=theory))
result={'scope':'Full laboratory generator, no parity-frame or tensor-product assumption used in evolution; finite-bin independent detectors; photon-only optimal local correction; full data channel (therefore arbitrary reference)','superoperator_error':error,'local_risks':risks,'joint_error_distribution':joint,'record_probability_sum':sum(branch_weights),'echo_checks':echo,'echo_frame_caveat':'Odd pulse counts require a known final X frame for an arbitrary channel; ideal comparator includes this frame, not an extra physically free operation.'}
(root/'full_graph_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
