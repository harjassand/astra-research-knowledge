#!/usr/bin/env python3
"""Full EPR-then-teleport service versus a directly Pauli-twirled channel.

Carried systems: unknown D, arbitrary bath M, untouched reference E.
No factorization of D from M or E; two Kraus physical channels.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
I=np.eye(2, dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.]).astype(complex)
P=[I,X,Y,Z]
K0=np.array([1,0],complex); K1=np.array([0,1],complex)
phi=(np.kron(K0,K0)+np.kron(K1,K1))/np.sqrt(2)
U0=expm(-1j*(.61*np.kron(Z,(I+Z)/2)+.31*np.kron(X,X)+.17*np.kron(I,Y)))
U1=expm(-1j*(.38*np.kron(X,(I+Y)/2)+.37*np.kron(Y,Z)+.11*np.kron(I,X)))
Kraus=[np.sqrt(.65)*U0,np.sqrt(.35)*U1]
B=[[] for _ in range(4)]
for A in Kraus:
    for s,p in enumerate(P):
        B[s].append(.5*np.einsum('ab,biaj->ij',p,A.reshape(2,2,2,2)))

def ind5(d,t,c,m,e):return ((((d*2+t)*2+c)*2+m)*2+e)
def ind3(d,m,e):return ((d*2+m)*2+e)
V=np.zeros((32,8),complex)
for d in range(2):
 for m in range(2):
  for e in range(2):
   for t in range(2): V[ind5(d,t,t,m,e),ind3(d,m,e)]=1/np.sqrt(2)
Kfive=[]
for K in Kraus:
 F=np.zeros((32,32),complex)
 for d in range(2):
  for t in range(2):
   for e in range(2):
    for c in range(2):
     for m in range(2):
      for cp in range(2):
       for mp in range(2):
        F[ind5(d,t,cp,mp,e),ind5(d,t,c,m,e)]=K[cp*2+mp,c*2+m]
 Kfive.append(F)

Tm=[]
for p in P:
 beta=np.kron(I,p)@phi
 T=np.zeros((8,32),complex)
 for d in range(2):
  for t in range(2):
   for c in range(2):
    for m in range(2):
     for e in range(2):
      for cp in range(2):
       T[ind3(cp,m,e),ind5(d,t,c,m,e)]=np.conj(beta[d*2+t])*p[cp,c]
 Tm.append(T)

net=[T@F@V for F in Kfive for T in Tm]
diag=[np.kron(np.kron(P[s],bs),I) for s in range(4) for bs in B[s]]
# Sum of net CP maps equals the twirled channel, not merely a Bell-fidelity number.
rng=np.random.default_rng(101926)
maxdist=0
maxfro=0
for i in range(40):
 A=rng.standard_normal((8,8))+1j*rng.standard_normal((8,8))
 rho=A@A.conj().T;rho/=np.trace(rho)
 a=sum(k@rho@k.conj().T for k in net)
 b=sum(k@rho@k.conj().T for k in diag)
 D=(a-b+(a-b).conj().T)/2
 maxdist=max(maxdist,float(.5*np.sum(abs(np.linalg.eigvalsh(D)))))
 maxfro=max(maxfro,float(np.linalg.norm(a-b)))
assert maxdist<2e-13
# Because equality of CP maps was tested only on 40 states, also test EVERY
# matrix unit (basis elements need not be states) to establish linear-map check.
max_matrix_unit=0
for i in range(8):
 for j in range(8):
  R=np.zeros((8,8),complex);R[i,j]=1
  a=sum(k@R@k.conj().T for k in net)
  b=sum(k@R@k.conj().T for k in diag)
  max_matrix_unit=max(max_matrix_unit,float(np.linalg.norm(a-b)))
assert max_matrix_unit<2e-13
res={'full_five_qubit_wire_order':'D,T,C,M,E before Bell; C,M,E after Bell',
     'incoming_payload_bath_reference':'arbitrarily entangled three-qubit state',
     'physical_noise':'two-Kraus channel jointly on transmitted qubit C and bath M',
     'trusted_terminal_teleportation':'four complete Bell outcomes, corrected and retired',
     'max_complete_channel_random_state_half_trace_error':maxdist,
     'max_complete_channel_random_state_frobenius_error':maxfro,
     'max_complete_map_matrix_unit_frobenius_error':max_matrix_unit,
     'operator_scope':'Equality of full CPTP maps on input D,M,E; not just fidelity or bath effects.'}
Path(__file__).with_name('ebit_complete_teleport_reference_results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
