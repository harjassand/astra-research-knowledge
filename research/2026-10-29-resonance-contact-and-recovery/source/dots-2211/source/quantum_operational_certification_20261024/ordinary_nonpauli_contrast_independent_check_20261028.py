#!/usr/bin/env python3
"""Independent exact contrasts plus floating complete-circuit checks. No source samples."""
from pathlib import Path
import itertools,json,hashlib
import sympy as s
import numpy as np
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
def kron(*a):
 r=s.ones(1,1)
 for x in a:r=s.kronecker_product(r,x)
 return r
def op(P,i,n):return kron(*[P if k==i else I for k in range(n)])
def ratrot(t):return s.Matrix([[(1-t*t)/(1+t*t),-2*t/(1+t*t)],[2*t/(1+t*t),(1-t*t)/(1+t*t)]])
def partial(A,keep,n):
 keep=list(keep);other=[x for x in range(n) if x not in keep];out=s.zeros(2**len(keep))
 def idx(bits):return sum(v*2**(n-1-k) for k,v in enumerate(bits))
 for a,b in itertools.product(range(2**len(keep)),repeat=2):
  aa=[(a>>(len(keep)-1-k))&1 for k in range(len(keep))];bb=[(b>>(len(keep)-1-k))&1 for k in range(len(keep))]
  for c in itertools.product([0,1],repeat=len(other)):
   p=[0]*n;q=[0]*n
   for k,v,w in zip(keep,aa,bb):p[k]=v;q[k]=w
   for k,v in zip(other,c):p[k]=q[k]=v
   out[a,b]+=A[idx(p),idx(q)]
 return out
C=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
U=C*kron(ratrot(s.Rational(1,3)),ratrot(s.Rational(1,5)))
T=C*kron(ratrot(s.Rational(1,4)),ratrot(s.Rational(1,7)))
V=kron(U,T);n=4;assert V.H*V==s.eye(16)
g=[s.Rational(9,25),s.Rational(25,169),s.Rational(49,625),s.Rational(0)]
ks=[(s.diag(1,s.sqrt(1-a)),s.Matrix([[0,s.sqrt(a)],[0,0]])) for a in g]
def ad(A,k):return sum((q*A*q.H for q in ks[k]),s.zeros(2))
rhos=[ad(I/2,k) for k in range(n)]
B={(i,j):V*op(P,i,n)*V.H for i in range(n) for j,P in [('X',X),('Z',Z)]}
identity_count=0;gap_rows=[];other_commutator=False
for i in range(n):
 for j,P in [('X',X),('Z',Z)]:
  signed=[]
  for sign in [1,-1]:signed.append(V*kron(*[ad((I+sign*P)/2,k) if k==i else rhos[k] for k in range(n)])*V.H)
  Delta=(signed[0]-signed[1])/2;lam=s.sqrt(1-g[i]) if j=='X' else 1-g[i]
  R=V*kron(*[lam*I/2 if k==i else rhos[k] for k in range(n)])*V.H
  assert Delta==B[i,j]*R;identity_count+=256
  for jj in ['X','Z']:assert R*B[i,jj]==B[i,jj]*R;identity_count+=256
  for k in range(n):
   if k!=i and R*B[k,'X']!=B[k,'X']*R:other_commutator=True
  own=[0,1] if i<2 else [2,3];away=[2,3] if i<2 else [0,1]
  assert partial(Delta,away,n)==s.zeros(4);identity_count+=16
  RJ=partial(R,own,n);DJ=partial(Delta,own,n)
  BJ=partial(B[i,j],own,n)/4
  assert DJ==BJ*RJ;assert s.trace(RJ)==lam;identity_count+=17
  # Exact local eigenvalues are the corresponding pre-factor eigenvalues.
  partner=own[1] if own[0]==i else own[0]
  eigs=sorted([lam*(1-g[partner])/4,lam*(1+g[partner])/4])
  assert (RJ-eigs[0]*s.eye(4))*(RJ-eigs[1]*s.eye(4))==s.zeros(4);identity_count+=16
  a0=1-max(g);floor=a0**2/4;assert eigs[0]>=floor
  gap_rows.append({'i':i,'axis':j,'exact_local_gap':str(eigs[0]),'backward_cone_size':2,'certified_lower_gap':str(floor)})
assert other_commutator
assert any(ad(I/2,i)!=I/2 for i in range(n))
# Contrast translates cancel, whereas assuming unital output is false.
actualmixed=V*kron(*rhos)*V.H;assert actualmixed!=s.eye(16)/16
# Independent tensor shadow second moment on entangled nonunital state.
# One-site squared-shadow channel is L(A)=2 tr(A)I+A.
bell=s.Matrix([1,0,0,1])/s.sqrt(2);rho=bell*bell.H
rho=sum((kron(a,b)*rho*kron(a,b).H for a,b in itertools.product(ks[0],ks[1])),s.zeros(4))
second=s.zeros(4)
for axes in itertools.product([X,Y,Z],repeat=2):
 for signs in itertools.product([1,-1],repeat=2):
  Ps=[(I+e*A)/2 for e,A in zip(signs,axes)];E=kron(*Ps);shadow=kron(*[3*p-I for p in Ps]);prob=s.trace(E*rho)/9
  second+=prob*shadow**2
formula=4*s.eye(4)+2*kron(partial(rho,[0],2),I)+2*kron(I,partial(rho,[1],2))+rho
assert second==formula;assert max(np.linalg.eigvalsh(np.array(second,dtype=complex)))<=9+1e-12
# Two-qubit actual extraction with independently inconsistent fitted reflections.
In=np.eye(2);Xn=np.array(X,dtype=complex);Zn=np.array(Z,dtype=complex);Un=np.array(U,dtype=complex)
true={(i,j):Un@np.array(op(P,i,2),dtype=complex)@Un.conj().T for i in range(2) for j,P in [('X',X),('Z',Z)]}
def k2(a,b):return np.kron(a,b)
def anc(P,i):return k2(P,In) if i==0 else k2(In,P)
def block(SX,SZ,i):
 Q=k2((np.eye(4)+SZ)/2,np.eye(4))+k2((np.eye(4)-SZ)/2,anc(Xn,i))
 Cx=k2(np.eye(4),(np.eye(4)+anc(Zn,i))/2)+k2(SX,(np.eye(4)-anc(Zn,i))/2)
 return Q@Cx@Q
W0=np.eye(16,dtype=complex)
for i in range(2):W0=block(true[i,'X'],true[i,'Z'],i)@W0
rows=[]
for t in [0.02,0.007,0.001]:
 fits={};deltas={}
 for i,j in true:
  H=np.array(op(Y if j=='X' else X,1-i,2),dtype=complex)
  # Rotate with another nonlocal Pauli to ensure independent fit incompatibility.
  if j=='Z':H=H@np.array(op(Z,i,2),dtype=complex)
  rot=np.cos(t*(i+1))*np.eye(4)-1j*np.sin(t*(i+1))*H
  fits[i,j]=rot@true[i,j]@rot.conj().T
  deltas[i,j]=np.linalg.norm(fits[i,j]-true[i,j],2)
 W=np.eye(16,dtype=complex)
 for i in range(2):W=block(fits[i,'X'],fits[i,'Z'],i)@W
 debit=sum(2*deltas[i,'Z']+deltas[i,'X'] for i in range(2))
 err=np.linalg.norm(W-W0,2)
 assert np.linalg.norm(W.conj().T@W-np.eye(16),2)<1e-12 and err<=debit+1e-12
 # Actual mixed-ancilla retained output gives the exact inverse on all 16 matrix units.
 maximum=0
 for a,b in itertools.product(range(4),repeat=2):
  E=np.zeros((4,4),complex);E[a,b]=1
  out=W0@np.kron(E,np.eye(4)/4)@W0.conj().T
  red=sum(out[4*k:4*k+4,4*k:4*k+4] for k in range(4))
  maximum=max(maximum,np.linalg.norm(red-Un.conj().T@E@Un))
 assert maximum<1e-12
 rows.append({'tilt':t,'actual_circuit_operator_error':float(err),'three_gate_telescope':float(debit),'exact_inverse_matrix_unit_max_residual':float(maximum)})
result={'status':'PASS','scope':'Independent exact rational contrast/local-cone/variance identities and floating two-qubit actual circuit checks; no acquired source outcomes, no hardware or compiler run','source_outcomes':0,'rng_draws':0,'exact_matrix_entries_checked':identity_count,'nonunital_output':True,'factor_fails_other_qubit_commutation':other_commutator,'local_gap_cases':gap_rows,'two_qubit_circuit_cases':rows,'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_name('ordinary_local_contrast_factor_nonpauli_acquisition_20261028.md'),Path(__file__).with_name('ordinary_local_inverse_coherent_memory_fallback_20261028.md')]}}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
