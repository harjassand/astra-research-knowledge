"""Checks the exact joint instrument on correlated logical-memory-reference inputs."""
import json,numpy as np
from scipy.linalg import expm
from algebra_compiler_v1 import unitary
from coherent_mixed_gauge_v2 import hermitian_paulis

def run():
 rng=np.random.default_rng(202610290032);d=4;dg=2;dl=2;dm=2;dr=2
 C=np.eye(d,dtype=complex)
 for g in [('H',0),('CX',0,1),('S',1),('H',1)]:C=unitary(g,2)@C
 H=rng.normal(size=(d*dm,d*dm))+1j*rng.normal(size=(d*dm,d*dm));H=(H+H.conj().T)/6
 V=expm(-1j*H);Vc=np.kron(C.conj().T,np.eye(dm))@V@np.kron(C,np.eye(dm))
 coeff=[]
 for v,P in hermitian_paulis(2):
  A=np.einsum('ab,biaj->ij',P.conj().T,V.reshape(d,dm,d,dm))/d
  Pc=C.conj().T@P@C
  # Locate its single tensorPauli in compiledcoordinates, includingphase.
  found=None
  for gv,G in hermitian_paulis(1):
   for lv,L in hermitian_paulis(1):
    z=np.trace(np.kron(G,L).conj().T@Pc)/d
    if abs(z)>.5:found=(L,z*A)
  assert found is not None;coeff.append(found)
 records=[]
 for trial in range(8):
  z=rng.normal(size=(dl*dm*dr,dl*dm*dr))+1j*rng.normal(size=(dl*dm*dr,dl*dm*dr));rho=z@z.conj().T;rho/=np.trace(rho)
  direct=np.zeros_like(rho);masked=np.zeros((d*dm*dr,d*dm*dr),complex)
  for kv,K in hermitian_paulis(1):
   key=np.kron(K,np.eye(dm*dr));input=np.kron(np.eye(dg)/dg,key@rho@key.conj().T)
   masked+=input/4
   W=np.kron(Vc,np.eye(dr));after=W@input@W.conj().T
   unkey=np.kron(np.eye(dg),key);after=unkey@after@unkey.conj().T
   direct+=np.trace(after.reshape(dg,dl*dm*dr,dg,dl*dm*dr),axis1=0,axis2=2)/4
  predicted=np.zeros_like(rho)
  for L,A in coeff:
   B=np.kron(np.kron(L,A),np.eye(dr));predicted+=B@rho@B.conj().T
  rhoMR=np.trace(rho.reshape(dl,dm*dr,dl,dm*dr),axis1=0,axis2=2)
  records.append(dict(trial=trial,joint_instrument_error=float(np.linalg.norm(direct-predicted)),precall_decoupling_error=float(np.linalg.norm(masked-np.kron(np.eye(d)/d,rhoMR))),output_trace=float(np.trace(direct).real)))
 print(json.dumps(dict(seed=202610290032,source='generic coherent joint unitary, notPauli diagonal',logical_memory_reference_input='generic correlated density matrices',records=records),indent=2))
if __name__=='__main__':run()
