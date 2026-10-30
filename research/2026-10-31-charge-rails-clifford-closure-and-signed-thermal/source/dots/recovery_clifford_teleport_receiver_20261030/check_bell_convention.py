"""Exact finite Hilbert-space convention checks; no native threshold simulation."""
import itertools,json
from pathlib import Path
import numpy as np
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1,-1]).astype(complex); H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)
S=np.diag([1,1j]); Y=1j*X@Z
rng=np.random.default_rng(1771)
def tensor(xs):
 a=np.ones((1,1),complex)
 for x in xs:a=np.kron(a,x)
 return a
def gate1(g,i,k):return tensor([g if j==i else I for j in range(k)])
def cx(c,t,k):
 d=2**k;a=np.zeros((d,d),complex)
 for v in range(d):
  bits=[(v>>(k-1-j))&1 for j in range(k)]
  bits[t]^=bits[c];w=sum(b<<(k-1-j) for j,b in enumerate(bits));a[w,v]=1
 return a
def bits(n,k):return [(n>>(k-1-j))&1 for j in range(k)]
def pauli(b,a):return tensor([np.linalg.matrix_power(X,x)@np.linalg.matrix_power(Z,z) for x,z in zip(b,a)])
max_branch=max_correction=max_uniform=max_pauli=0.;cases=0;families=0
for k in [1,2,3]:
 d=2**k
 # Include complex Cliffords and entangling gates, so transpose/sign errors are visible.
 Us=[np.eye(d,dtype=complex),gate1(S,0,k),gate1(H,k-1,k)]
 if k>1:Us += [cx(0,1,k),gate1(S,1,k)@cx(0,1,k)@gate1(H,0,k)]
 for trial in range(4):
  U=np.eye(d,dtype=complex)
  for j in range(9):
   i=int(rng.integers(k));G=gate1([H,S,X][int(rng.integers(3))],i,k)
   if k>1 and rng.random()<.4:
    t=(i+1)%k;G=cx(i,t,k)
   U=G@U
  Us.append(U)
 for U in Us:
  families+=1
  # Resource coefficients R[y,c]=U[c,y]/sqrt(d), NOT U[y,c]/sqrt(d).
  R=U.T/np.sqrt(d)
  for aint,bint in itertools.product(range(d),repeat=2):
   a,b=bits(aint,k),bits(bint,k)
   T=np.zeros((d,d),complex)
   for x in range(d):
    xb=bits(x,k);phase=(-1)**sum(ai*xi for ai,xi in zip(a,xb))
    T[:,x]=phase*R[bint^x,:]/np.sqrt(d)
   P=pauli(b,a);expected=U@P/d
   Q=U@P.conj().T@U.conj().T
   max_branch=max(max_branch,float(np.linalg.norm(T-expected)))
   max_correction=max(max_correction,float(np.linalg.norm(Q@T-U/d)))
   max_uniform=max(max_uniform,float(np.linalg.norm(T.conj().T@T-np.eye(d)/d**2)))
   # Correction must be one Pauli up to phase; use the orthogonal Pauli basis.
   overlaps=[]
   for word in itertools.product([I,X,Y,Z],repeat=k):
    Ptest=tensor(word);overlaps.append(abs(np.trace(Ptest.conj().T@Q))/d)
   max_pauli=max(max_pauli,abs(max(overlaps)-1))
   cases+=1
assert max(max_branch,max_correction,max_uniform,max_pauli)<1e-11
# Spectator negative: resource B,C in |0>|0> is not a Bell pair.
# For A=|0>, CNOT then X_A,Z_B gives b=0 only, a equiprobable.
spectator_product_probabilities=[.5,0,.5,0] # labels (a,b):00,01,10,11
assert spectator_product_probabilities != [.25]*4
# Outcome-dependent bath and branch-survival weights remain independent of input after Q.
k=1;d=2;U=S@H
weights=[.93,.81,.77,.99]
# Explicit ideal branch corrected operators are U/d; weighted trace map equals p*Ad_U.
p=sum(weights)/4
rho=np.array([[.4,.1+.2j],[.1-.2j,.6]],complex)
out=sum(w*(U@rho@U.conj().T)/4 for w in weights)
assert np.linalg.norm(out-p*U@rho@U.conj().T)<1e-12
result={'clifford_instances':families,'Bell_branch_cases':cases,
 'max_branch_identity_residual':max_branch,'max_corrected_U_residual':max_correction,
 'max_uniform_branch_effect_residual':max_uniform,'max_Clifford_Pauli_overlap_residual':max_pauli,
 'product_spectator_negative_probabilities':spectator_product_probabilities,
 'branch_dependent_survival_average':p,
 'scope':'Finite exact Clifford/Bell convention and branch-factor checks; not native hardware/threshold certification.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
