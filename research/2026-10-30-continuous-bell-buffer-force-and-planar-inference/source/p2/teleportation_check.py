"""Verify finite-bank H, S, T gate teleportation on dirty resource registers.

For U in {H,S,T}, prepare its Choi state by measuring commuting
X x (U X U†) and Z x (U Z U†), then Bell-measure the input and the
first resource qubit.  Each of 16 records factors as U on the relocated
payload times a Kraus map on the two initially arbitrary resource qubits.
Corrections are mathematical reference frames.  For T their updates are
Clifford, so a usable interface must support the corresponding adaptive
measurement choices; no physical correction is silently supplied.
"""
import itertools
from functools import reduce
import numpy as np

I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1.,-1.]).astype(complex)
Y=1j*X@Z
def kron(*ops): return reduce(np.kron,ops)

def check():
    h=(X+Z)/np.sqrt(2)
    gates={'H':h,'S':np.diag([1,1j]),'T':np.diag([1,np.exp(1j*np.pi/4)])}
    phi=np.array([1,0,0,1],complex)/np.sqrt(2)
    # Input axes D,A,B; output axes B,D,A.
    perm=np.array([4*d+2*a+b for b in range(2) for d in range(2) for a in range(2)])
    results={}
    for name,u in gates.items():
        obs=[kron(I,X,u@X@u.conj().T),kron(I,Z,u@Z@u.conj().T),
             kron(X,X,I),kron(Z,Z,I)]
        worst=0.; completeness=np.zeros((8,8),complex)
        max_s_layers=0
        for a,b,c,d in itertools.product(range(2),repeat=4):
            k=np.eye(8,dtype=complex)
            for bit,q in zip((a,b,c,d),obs):
                k=(np.eye(8)+(-1)**bit*q)@k/2
            p=np.linalg.matrix_power(Z,a)@np.linalg.matrix_power(X,b)
            bellp=np.linalg.matrix_power(Z,c)@np.linalg.matrix_power(X,d)
            choi=kron(p,u)@phi
            bell=kron(I,bellp)@phi
            byproduct=p.T@bellp.conj()
            correction=u@byproduct.conj().T@u.conj().T
            # A T byproduct needs at most one S or S-dagger correction,
            # followed by an ordinary Pauli frame. No global Clifford frame
            # is required to establish a finite measurement bank.
            choices=[]
            for layers in (0,1,-1):
                sg=np.linalg.matrix_power(gates['S'],layers)
                for pauli in (I,X,Y,Z):
                    candidate=pauli@sg
                    ph=np.vdot(candidate,correction)/2
                    if abs(abs(ph)-1)<1e-12 and np.linalg.norm(correction-ph*candidate)<1e-12:
                        choices.append(abs(layers))
            assert choices
            max_s_layers=max(max_s_layers,min(choices))
            corrected=kron(I,I,correction)@k
            expected=.5*kron(u,np.outer(bell,choi.conj()))
            worst=max(worst,float(np.linalg.norm(corrected[perm,:]-expected,2)))
            completeness+=k.conj().T@k
        results[name]={'records':16,'factorization_residual':worst,
                       'completeness_residual':float(np.linalg.norm(completeness-np.eye(8),2)),
                       'max_additional_S_teleportations':max_s_layers}
    return results

if __name__=='__main__':
    import json
    print(json.dumps(check(),indent=2))
