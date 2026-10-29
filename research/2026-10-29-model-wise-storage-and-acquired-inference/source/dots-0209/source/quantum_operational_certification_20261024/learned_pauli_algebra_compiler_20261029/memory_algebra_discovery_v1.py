"""Exact conditional-memory branching aggregated by learned span; no iid substitution."""
import json,numpy as np
from scipy.linalg import expm
from algebra_compiler_v1 import compile_algebra,gate_rows,unitary,pauli,basis
from coherent_mixed_gauge_v2 import hermitian_paulis

def canon(A,n):
 if not len(A):return ()
 return tuple(tuple(map(int,r)) for r in basis(np.array(A,dtype=np.uint8).reshape(-1,2*n)))
def run():
 n=2;d=4;dm=2;g=1;k=1
 X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);Y=1j*X@Z;I=np.eye(2)
 scramble=[('H',0),('CX',0,1),('S',1),('H',1)]
 W=np.eye(d,dtype=complex)
 for gate in scramble:W=unitary(gate,n)@W
 H=.41*np.kron(np.kron(X,I),X)+.73*np.kron(np.kron(Z,I),Z)+.29*np.kron(np.kron(Y,I),I)+.17*np.kron(np.eye(d),Y)
 V=np.kron(W,I)@expm(-1j*H)@np.kron(W.conj().T,I)
 Ps=list(hermitian_paulis(n));ops=[]
 for v,P in Ps:
  A=np.einsum('ab,biaj->ij',P.conj().T,V.reshape(d,dm,d,dm))/d
  if np.linalg.norm(A)>1e-12:ops.append((tuple(map(int,v)),A))
 S=canon([v for v,A in ops],n)
 cache={}
 def compiled(key):
  if key in cache:return cache[key]
  if key:out=compile_algebra(np.array(key,dtype=np.uint8),n);gates=out['gates'];cost=out['a']+out['b']
  else:gates=[];cost=0
  assert cost<=g
  # Existing compiler places its cost gauge qubits first; pad to fixedg.
  U=np.eye(d,dtype=complex)
  for gate in gates:U=unitary(gate,n)@U
  good=[]
  for v,A in ops:
   p=np.array(v,dtype=np.uint8)[None,:]
   for gate in gates:gate_rows(p,gate,n)
   good.append(not np.any(p[0,g:n]) and not np.any(p[0,n+g:]))
  cache[key]=(U,good)
  return U,good
 rho=np.array([[.7,.12+.09j],[.12-.09j,.3]],complex)
 states={():rho};records=[];cum_loss=0.;cum_innov=0.;physical=[]
 for step in range(1,257):
  nxt={};loss=0.;innov=0.
  for key,R in states.items():
   U,good=compiled(key);mass=np.trace(R).real
   probs=[]
   for idx,(v,A) in enumerate(ops):
    Q=A@R@A.conj().T;p=np.trace(Q).real;probs.append(p)
    new=canon(list(key)+[v],n)
    if new!=key:innov+=p
    if not good[idx]:loss+=p
    nxt[new]=nxt.get(new,np.zeros((dm,dm),complex))+Q
   if step<=3 and mass>1e-14:
    # Full physical Choi experiment, axes R,B,M. C=U† encoder.
    C=U.conj().T;phi=np.eye(d).reshape(-1)/np.sqrt(d)
    rb=np.outer(phi,phi.conj());initial=np.kron(rb,R/mass)
    enc=np.kron(np.kron(np.eye(d),C),np.eye(dm))
    src=np.kron(np.eye(d),V)
    state=src@enc@initial@enc.conj().T@src.conj().T
    # Probe conjugate C on R; Bell projectors read physicalchannel labels.
    probe=np.kron(np.kron(C.conj(),np.eye(d)),np.eye(dm))
    qp=probe@state@probe.conj().T
    measured=[]
    for v,A in ops:
     P=dict((tuple(map(int,w)),P) for w,P in Ps)[v]
     bell=np.kron(np.eye(d),P)@phi
     effect=np.kron(np.outer(bell,bell.conj()),np.eye(dm))
     measured.append(np.trace(effect@qp).real)
    # Terminal inverseC=U, gauge pairsdiscard; Bell effect logical R_L,B_L.
    dec=np.kron(np.kron(np.eye(d),U),np.eye(dm));qt=dec@state@dec.conj().T
    effect=np.zeros((d*d*dm,d*d*dm),complex)
    for rg in range(2):
     for bg in range(2):
      for mem in range(dm):
       vec=np.zeros(d*d*dm,complex)
       for logical in range(2):vec[((2*rg+logical)*d+(2*bg+logical))*dm+mem]=1/np.sqrt(2)
       effect+=np.outer(vec,vec.conj())
    actual=np.trace(effect@qt).real;pred=sum(p for p,b in zip(probs,good) if b)/mass
    physical.append(dict(step=step,rank=len(key),probe_probability_error=float(np.max(np.abs(np.array(measured)-np.array(probs)/mass))),terminal_Fe_error=float(abs(actual-pred))))
  cum_loss+=loss;cum_innov+=innov;states=nxt
  assert loss<=innov+1e-10
  assert cum_innov<=len(S)+1e-10
  if step in [1,2,4,8,16,32,64,128,256]:records.append(dict(N=step,expected_private_terminal_Bell_loss=cum_loss/step,cumulative_innovations=cum_innov,rank_bound=len(S)/step,total_probability=float(sum(np.trace(R).real for R in states.values()))))
 print(json.dumps(dict(n=n,g=g,k=k,common_support_basis=S,common_rank=len(S),kraus_coefficient_count=len(ops),exact_branching=True,recorded_curves=records,physical_role_hiding_checks=physical),indent=2))
if __name__=='__main__':run()
