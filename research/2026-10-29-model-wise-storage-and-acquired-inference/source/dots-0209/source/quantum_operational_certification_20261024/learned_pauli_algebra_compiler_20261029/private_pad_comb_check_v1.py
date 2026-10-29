"""Actual adaptive two-payload circuit versus latent input-independent Pauli comb.
Physical path explicitly performs all private pads and gauge partial traces.
The parallel latent path retains only source memory + Pauli labels.
"""
import json,numpy as np
from scipy.linalg import expm
from algebra_compiler_v1 import compile_algebra,unitary,gate_rows
from coherent_mixed_gauge_v2 import hermitian_paulis
from memory_algebra_discovery_v1 import canon

def run():
 n=2;d=4;dm=2;J=2;q=.25;cap=24
 X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);Y=1j*X@Z;I=np.eye(2)
 W=np.eye(d,dtype=complex)
 for gate in [('H',0),('CX',0,1),('S',1),('H',1)]:W=unitary(gate,n)@W
 H=.41*np.kron(np.kron(X,I),X)+.73*np.kron(np.kron(Z,I),Z)+.29*np.kron(np.kron(Y,I),I)+.17*np.kron(np.eye(d),Y)
 V=np.kron(W,I)@expm(-1j*H)@np.kron(W.conj().T,I)
 ops=[]
 for v,P in hermitian_paulis(n):
  A=np.einsum('ab,biaj->ij',P.conj().T,V.reshape(d,dm,d,dm))/d
  if np.linalg.norm(A)>1e-12:ops.append((tuple(map(int,v)),P,A))
 cache={}
 def compiled(key):
  if key in cache:return cache[key]
  gates=compile_algebra(np.array(key,dtype=np.uint8),n)['gates'] if key else[]
  U=np.eye(d,dtype=complex)
  for gate in gates:U=unitary(gate,n)@U
  labels=[]
  for v,P,A in ops:
   row=np.array(v,dtype=np.uint8)[None,:]
   for gate in gates:gate_rows(row,gate,n)
   labels.append((int(row[0,1]),int(row[0,3])))
  Vc=np.kron(U,I)@V@np.kron(U.conj().T,I)
  cache[key]=(Vc,labels);return Vc,labels
 # Physical state axes: L0,L1,R(dimension4),M.
 dims=[2,2,4,2];D=32
 def permute(R,order):return R.reshape(dims+dims).transpose(order+[i+4 for i in order]).reshape(D,D)
 def unpermute(R,order):
  dd=[dims[i] for i in order];inv=list(np.argsort(order))
  return R.reshape(dd+dd).transpose(inv+[i+4 for i in inv]).reshape(D,D)
 def service_actual(R,j,Vc):
  order=[j,3,1-j,2];S=permute(R,order);rest=8
  out=np.zeros_like(S)
  VV=np.kron(Vc,np.eye(rest))
  for kv,K in hermitian_paulis(1):
   KK=np.kron(K,np.eye(16));inp=np.kron(I/2,KK@S@KK.conj().T)
   state=VV@inp@VV.conj().T
   unkey=np.kron(I,KK);state=unkey@state@unkey.conj().T
   out+=np.trace(state.reshape(2,D,2,D),axis1=0,axis2=2)/4
  return unpermute(out,order)
 phi=np.eye(4).reshape(-1)/2;payload=np.outer(phi,phi.conj())
 memory=np.array([[.7,.12+.09j],[.12-.09j,.3]],complex)
 physical={((),0):np.kron(payload,memory)};done=np.zeros((D,D),complex)
 latent={((),0,(0,0,0,0)):memory};done_lat={};cumfaults=0.;cuminnov=0.;records=[]
 for step in range(1,cap+1):
  pn={};ln={}
  for (key,j),R in physical.items():
   Vc,labels=compiled(key)
   for v,P,A in ops:
    B=np.kron(np.eye(16),A);Q=(1-q)*B@R@B.conj().T
    new=canon(list(key)+[v],n);idx=(new,j);pn[idx]=pn.get(idx,np.zeros_like(Q))+Q
   S=q*service_actual(R,j,Vc)
   if j+1==J:done+=S
   else:
    idx=(key,j+1);pn[idx]=pn.get(idx,np.zeros_like(S))+S
  for (key,j,pattern),R in latent.items():
   Vc,labels=compiled(key)
   for idxop,(v,P,A) in enumerate(ops):
    T=A@R@A.conj().T;new=canon(list(key)+[v],n)
    if new!=key:cuminnov+=(1-q)*np.trace(T).real
    idx=(new,j,pattern);ln[idx]=ln.get(idx,np.zeros_like(T))+(1-q)*T
    label=labels[idxop];newpat=list(pattern);newpat[2*j:2*j+2]=label;newpat=tuple(newpat)
    if any(label):cumfaults+=q*np.trace(T).real
    if j+1==J:done_lat[newpat]=done_lat.get(newpat,np.zeros_like(T))+q*T
    else:
     idx=(key,j+1,newpat);ln[idx]=ln.get(idx,np.zeros_like(T))+q*T
  physical=pn;latent=ln
  if step in [4,8,16,24]:
   actual=np.trace(done.reshape(16,2,16,2),axis1=1,axis2=3)
   predicted=np.zeros_like(actual)
   for pattern,R in done_lat.items():
    PP=np.eye(1,dtype=complex)
    for j in range(J):PP=np.kron(PP,np.linalg.matrix_power(X,pattern[2*j])@np.linalg.matrix_power(Z,pattern[2*j+1]))
    PP=np.kron(PP,np.eye(4));predicted+=np.trace(R).real*(PP@payload@PP.conj().T)
   records.append(dict(cap=step,completed_mass=float(np.trace(done).real),physical_vs_latent_Choi_error=float(np.linalg.norm(actual-predicted)),expected_service_faults=cumfaults,probe_innovations=cuminnov,charged_fault_bound=q/(1-q)*cuminnov,common_rank_fault_bound=q/(1-q)*2))
   assert np.linalg.norm(actual-predicted)<1e-10
   assert cumfaults<=q/(1-q)*cuminnov+1e-10
 print(json.dumps(dict(J=J,q=q,source_memory_dimension=2,physical_path='explicit keys,gauge input,source jointunitary,gauge trace',latent_path='independent memorybank + input-independent Pauli histories',input='maximally entangled whole2qubitpayload with4D externalreference',records=records),indent=2))
if __name__=='__main__':run()
