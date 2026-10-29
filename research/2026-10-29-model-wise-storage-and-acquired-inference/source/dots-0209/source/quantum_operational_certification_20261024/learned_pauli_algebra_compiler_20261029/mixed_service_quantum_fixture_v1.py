"""Actual unmeasured service resources, retained quantum memory, exact branch aggregation."""
import json,numpy as np
from scipy.linalg import expm
from algebra_compiler_v1 import compile_algebra,unitary
from coherent_mixed_gauge_v2 import hermitian_paulis
from memory_algebra_discovery_v1 import canon

def run():
 n=2;d=4;dm=2;dg=2;dl=2;J=2;q=.1;Lmax=128
 X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);Y=1j*X@Z;I=np.eye(2)
 W=np.eye(d,dtype=complex)
 for gate in [('H',0),('CX',0,1),('S',1),('H',1)]:W=unitary(gate,n)@W
 H=.41*np.kron(np.kron(X,I),X)+.73*np.kron(np.kron(Z,I),Z)+.29*np.kron(np.kron(Y,I),I)+.17*np.kron(np.eye(d),Y)
 V=np.kron(W,I)@expm(-1j*H)@np.kron(W.conj().T,I)
 ops=[]
 for v,P in hermitian_paulis(n):
  A=np.einsum('ab,biaj->ij',P.conj().T,V.reshape(d,dm,d,dm))/d
  if np.linalg.norm(A)>1e-12:ops.append((tuple(map(int,v)),P,A))
 cache={};tp_errors=[]
 def service_maps(key):
  if key in cache:return cache[key]
  gates=compile_algebra(np.array(key,dtype=np.uint8),n)['gates'] if key else[]
  U=np.eye(d,dtype=complex)
  for gate in gates:U=unitary(gate,n)@U
  maps=[]
  for go in range(dg):
   for gi in range(dg):
    K=np.zeros((dl*dl*dm,dm),complex)
    for v,P,A in ops:
     block=(U@P@U.conj().T).reshape(dg,dl,dg,dl)[go,:,gi,:]
     K+=np.kron(block.T.reshape(-1,1),A)/np.sqrt(dg*dl)
    maps.append(K)
  tp_errors.append(float(np.linalg.norm(sum(K.conj().T@K for K in maps)-np.eye(dm))))
  cache[key]=maps;return maps
 rho=np.array([[.7,.12+.09j],[.12-.09j,.3]],complex)
 active={((),0):rho};done=np.zeros((4**J*dm,4**J*dm),complex)
 cuminnov=0.;birth_loss=0.;records=[]
 bell=np.array([1,0,0,1])/np.sqrt(2);Pbell=np.outer(bell,bell)
 Eall=np.kron(np.kron(Pbell,Pbell),I)
 for step in range(1,Lmax+1):
  nxt={}
  for (key,j),R in active.items():
   dimold=4**j
   for v,P,A in ops:
    M=np.kron(np.eye(dimold),A);Q=(1-q)*(M@R@M.conj().T)
    new=canon(list(key)+[v],n)
    if new!=key:cuminnov+=np.trace(Q).real
    idx=(new,j);nxt[idx]=nxt.get(idx,np.zeros_like(Q))+Q
   S=np.zeros((dimold*4*dm,dimold*4*dm),complex)
   for K in service_maps(key):
    M=np.kron(np.eye(dimold),K);S+=q*(M@R@M.conj().T)
   neweffect=np.kron(np.eye(dimold),np.kron(Pbell,I))
   birth_loss+=np.trace(S).real-np.trace(neweffect@S).real
   if j+1==J:done+=S
   else:
    idx=(key,j+1);nxt[idx]=nxt.get(idx,np.zeros_like(S))+S
  active=nxt
  if step in [8,16,32,64,128]:
   successmass=np.trace(done).real;capmass=sum(np.trace(R).real for R in active.values())
   unconditional_completed_bad=successmass-np.trace(Eall@done).real
   bound=q/(1-q)*2
   records.append(dict(cap=step,completed_probability=successmass,cap_probability=capmass,completed_joint_Bell_shortfall=unconditional_completed_bad,all_arrived_service_birth_shortfall=birth_loss,actual_probe_innovations=cuminnov,innovation_service_bound=q/(1-q)*cuminnov,rank_service_bound=bound,worst_fallback_joint_loss_upper=unconditional_completed_bad+capmass))
   assert unconditional_completed_bad<=birth_loss+1e-10
   assert birth_loss<=q/(1-q)*cuminnov+1e-10
   assert cuminnov<=2+1e-10
   assert abs(successmass+capmass-1)<1e-10
 # Demonstrate actual retained correlations; completed normalized state notproduct.
 norm=done/np.trace(done).real
 resh=norm.reshape(4,4,dm,4,4,dm)
 R12=np.einsum('abmc dm->abcd',resh) if False else np.trace(resh,axis1=2,axis2=5).reshape(16,16)
 R1=np.trace(R12.reshape(4,4,4,4),axis1=1,axis2=3)
 R2=np.trace(R12.reshape(4,4,4,4),axis1=0,axis2=2)
 print(json.dumps(dict(J=J,q=q,max_cap=Lmax,stored_resources_never_Bell_measured=True,source_memory_dimension=dm,service_map_max_TP_error=max(tp_errors),resource_product_deviation_frobenius=float(np.linalg.norm(R12-np.kron(R1,R2))),records=records),indent=2))
if __name__=='__main__':run()
