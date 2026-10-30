"""Independent noncommuting local witnesses/gates, with retained-bath noise."""
import numpy as np,json
from scipy.linalg import expm,eigvalsh
n=3;dim=2**(n+1);I=np.eye(dim)
paulis=[np.array([[0,1],[1,0]],complex),np.array([[1,0],[0,-1]],complex),np.array([[0,-1j],[1j,0]],complex)]
def embed(a,k):
 z=np.ones((1,1),complex)
 for j in range(n+1):z=np.kron(z,a if j==k else np.eye(2))
 return z
P=[embed(np.diag([0,1]),j) for j in range(n)]
X=[P[j]@(1.3*I+.3*embed(paulis[j],n)) for j in range(n)]
pairs=[(0,1),(1,2)];Yp=[P[b]@X[a] for a,b in pairs];PP=sum(P[a]@P[b] for a,b in pairs)
jumps=[embed(np.array([[0,1],[0,0]]),j) for j in range(n)]
H=sum(embed(paulis[0],j)@(I+.2*embed(paulis[(j+1)%3],n)) for j in range(n))
def L0(O):
 out=np.zeros_like(O)
 for j in jumps:
  a=j.conj().T@j;out+=j.conj().T@O@j-(a@O+O@a)/2
 return out
def product(gates):
 out=I.copy()
 for q in gates:out=out@q
 return out
def fast_eff(Y):
 yi=np.linalg.inv(Y);return yi.conj().T@L0(Y.conj().T@Y)@yi
A=512.;B=1.;delta=.003;C=32.;cases=[]
Qpair=I.copy()
for a,b in pairs:Qpair=Qpair@(I-P[a]@P[b])
for eps in [.001,.003,.01,.03]:
 F=A*eps**2*sum(X)+B*sum(Yp)
 LF=L0(F)+1j*eps*(H@F-F@H)
 additive=LF+.25*A*eps**2*sum(P)+.25*B*PP-C*A*eps**4*n*I
 singles=[expm(delta*A*eps**2*x) for x in X]
 gates=[expm(delta*B*y) for y in Yp]+singles
 Y=product(gates);G=Y.conj().T@Y;yi=np.linalg.inv(Y)
 LG=L0(G)+1j*eps*(H@G-G@H)
 rhs=(-.1*delta*A*eps**2*sum(P)-.1*delta*B*PP+C*delta*A*eps**4*n*I)@G
 relative=yi.conj().T@(LG-rhs)@yi
 full_fast=fast_eff(Y);single_fast=fast_eff(product(singles))
 pair_remainder=full_fast-single_fast-2*delta*B*sum(L0(y) for y in Yp)
 single_remainder=single_fast-2*delta*A*eps**2*sum(L0(x) for x in X)
 cases.append({'epsilon':eps,'additive_maxeig':float(eigvalsh(additive)[-1]),'multiplicative_relative_maxeig':float(eigvalsh((relative+relative.conj().T)/2)[-1]),'pair_remainder_outside_pair_corner':float(max(np.linalg.norm(Qpair@pair_remainder),np.linalg.norm(pair_remainder@Qpair))),'singleton_remainder_scaled':float(np.linalg.norm(single_remainder,2)/(delta**2*A**2*eps**4))})
 assert cases[-1]['additive_maxeig']<1e-10
 assert cases[-1]['multiplicative_relative_maxeig']<1e-10
 assert cases[-1]['pair_remainder_outside_pair_corner']<1e-10
# Nonunital similarity with a common bath and an f not commuting the gates.
f=I.copy()
for j in range(n):f=f@(I+.3*P[j])
f=f@(I+.2*embed(paulis[1],n))
YB=np.kron(Y,np.eye(2));YiB=np.linalg.inv(YB);fB=np.kron(f,np.eye(2))
HB=np.kron(embed(paulis[0],n),paulis[1])
N=lambda O:1j*(HB@O-O@HB)
NF=YiB.conj().T@N(YB.conj().T@fB@YB)@YiB
Ht=YB@HB@YiB
formula=1j*(Ht.conj().T@fB-fB@Ht)
NI=YiB.conj().T@N(YB.conj().T@YB)@YiB
result={'dimension':dim,'witness_noncommutator_norm':float(np.linalg.norm(X[0]@X[1]-X[1]@X[0])),'A':A,'B':B,'delta':delta,'source_C':C,'cases':cases,'common_bath_hamiltonian_formula_error':float(np.linalg.norm(NF-formula)),'transformed_noise_NONUNITAL_norm':float(np.linalg.norm(NI)),'f_gate_noncommutation':float(np.linalg.norm(f@Y-Y@f))}
assert result['witness_noncommutator_norm']>0
assert result['common_bath_hamiltonian_formula_error']<1e-10
assert result['transformed_noise_NONUNITAL_norm']>1e-5
assert result['f_gate_noncommutation']>1e-5
print(json.dumps(result,indent=2))
