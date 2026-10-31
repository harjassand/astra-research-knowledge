"""Full eight-spin verification and explicit three-contact CZ compiler.

All spin matrices use S=sigma/2 and hbar=1.  Finite matrix verification is
separate from the analytic proof and does not establish device performance.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import eigh, expm

I2=np.eye(2)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.])
def tensor(xs):
    a=np.array([[1]],complex)
    for x in xs:a=np.kron(a,x)
    return a
def spins(n):
    return [[tensor([a/2 if k==i else I2 for k in range(n)])
             for a in [X,Y,Z]] for i in range(n)]
def dot(a,b):return sum(x@y for x,y in zip(a,b))
def sumsp(s,ids):return [sum(s[i][a] for i in ids) for a in range(3)]
def norm(a):return float(np.linalg.norm(a,2))

sg=np.array([0,1,-1,0])/np.sqrt(2)
tp=np.array([1,0,0,0]);tz=np.array([0,1,1,0])/np.sqrt(2);tm=np.array([0,0,0,1])
B4=np.column_stack([np.kron(sg,sg),
                   (np.kron(tp,tm)+np.kron(tm,tp)-np.kron(tz,tz))/np.sqrt(3)])
B=np.kron(B4,B4)
s=spins(8)
JA=sumsp(s,range(4));JB=sumsp(s,range(4,8));JT=sumsp(s,range(8))
JA2=dot(JA,JA);JB2=dot(JB,JB);JT2=dot(JT,JT)
V=dot(sumsp(s,[0,1]),sumsp(s,[4,5]))
H=(JA2+JB2)/2+V
e,W=eigh(H)
def evolution(t):return (W*np.exp(-1j*t*e))@W.conj().T
T=2*np.pi/np.sqrt(7)
phi=2*np.pi*(1-2/np.sqrt(7))
U=evolution(T)
CP=np.diag([1,1,1,np.exp(1j*phi)])
results=dict(T_Delta=float(T),controlled_phase=float(phi),phase_over_pi=float(phi/np.pi),
             complete_gate_error=norm(U@B-B@CP),
             global_spin_commutator=norm(H@JT2-JT2@H))
assert results['complete_gate_error']<2e-12

# Analytic minimal block and exact characteristic identity.
H3=np.array([[0,2/np.sqrt(3),0],
             [2/np.sqrt(3),1.5,np.sqrt(5/12)],
             [0,np.sqrt(5/12),4.5]])
A=H3-2*np.eye(3)
results['minimal_block_eigenvalues']=np.linalg.eigvalsh(H3).tolist()
results['minimal_characteristic_residual']=norm(A@A@A-7*A)
assert results['minimal_characteristic_residual']<1e-13

# Real local spin leakage during the fast gate is allowed and is retained.
P1A=JA2@(6*np.eye(256)-JA2)/8
P2A=JA2@(JA2-2*np.eye(256))/24
mid=[]
vector_residual=0.
num_faults=0
for t in np.linspace(0,T,17):
    Bt=evolution(t)@B
    assert norm(JT2@Bt)<3e-12
    mid.append(dict(time=float(t),J1_blockA=float(np.linalg.eigvalsh(Bt.conj().T@P1A@Bt)[-1]),
                    J2_blockA=float(np.linalg.eigvalsh(Bt.conj().T@P2A@Bt)[-1])))
    # Since U(T) returns the code, this expectation is the single-fault
    # accepted operator up to the known final logical CP.
    for i in range(8):
        for a in range(3):
            F=Bt.conj().T@(2*s[i][a])@Bt
            vector_residual=max(vector_residual,norm(F));num_faults+=1
results['midgate_local_leakage']=mid
results['single_vector_insertions']=num_faults
results['max_accepted_single_vector']=vector_residual
assert vector_residual<1e-12

# Known two-insertion and exchange-control counterexamples.
two=B.conj().T@(4*s[0][2]@s[1][2])@B
exchange=B.conj().T@dot(s[0],s[1])@B
results['accepted_two_vector_product']=np.real_if_close(two).tolist()
results['undetected_exchange_eigenvalues']=np.linalg.eigvalsh(exchange).tolist()
assert norm(exchange-np.trace(exchange)*np.eye(4)/4)>.49

# Explicit exact CZ from three native CP(phi) contacts and local rotations.
def rz(x):return expm(-.5j*x*Z)
def ry(x):return expm(-.5j*x*Y)
nz=1/(np.tan(phi)*np.tan(phi/2))
assert abs(nz)<1
beta=np.arccos(nz)
R=rz(2*phi)@ry(beta)@rz(phi)@ry(-beta)
assert abs(np.trace(R))<1e-12
M=1j*R # Hermitian involution, M=m dot sigma
assert norm(M-M.conj().T)<1e-12
evals,E=eigh(M)
Vloc=E[:,[1,0]]
# Vloc^dag M Vloc = Z.  Remove arbitrary determinant without changing conjugation.
Vloc*=np.exp(-.5j*np.angle(np.linalg.det(Vloc)))
Q=np.kron(I2,Vloc.conj().T)@CP@CP@np.kron(I2,ry(beta))@CP@np.kron(I2,ry(-beta))@np.kron(I2,Vloc)
correction=np.diag([1,np.exp(1j*(np.pi/2-3*phi/2))])
CZ=np.kron(correction,I2)@Q
target=np.diag([1,1,1,-1])
results['cz_compiler']={
    'native_contacts':3,'beta':float(beta),'axis_z':float(nz),
    'total_entangling_time_Delta':float(3*T),
    'matrix_error':norm(CZ-target),
    'target_rotation_real':Vloc.real.tolist(),
    'target_rotation_imag':Vloc.imag.tolist(),
    'control_phase_correction':float(np.pi/2-3*phi/2)}
assert results['cz_compiler']['matrix_error']<1e-12

# Local exchange axes on the same four-spin code used throughout.
sd=spins(4)
local={name:np.real_if_close(B4.conj().T@dot(sd[i],sd[j])@B4).tolist()
       for name,i,j in [('E12',0,1),('E23',1,2),('E34',2,3)]}
results['local_exchange_matrices']=local

# Hardware-calibrated coherent gate error need not be an erasure.  A wrong
# matched cross strength retains a nonscalar accepted phase at first order.
results['cross_strength_error']=[]
for eps in [1e-4,1e-3,1e-2]:
    UU=expm(-1j*T*(H+eps*V))
    K=B.conj().T@UU@B
    L=CP.conj().T@K
    scalar=np.trace(L)/4
    leak=1-np.linalg.eigvalsh(K.conj().T@K)[0]
    results['cross_strength_error'].append({
        'epsilon':eps,'accepted_nonscalar_norm':norm(L-scalar*np.eye(4)),
        'worst_gate_leakage':float(leak)})

out=Path(__file__).with_name('fast_exchange_gate_results.json')
out.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({k:v for k,v in results.items() if k!='midgate_local_leakage'},indent=2))
