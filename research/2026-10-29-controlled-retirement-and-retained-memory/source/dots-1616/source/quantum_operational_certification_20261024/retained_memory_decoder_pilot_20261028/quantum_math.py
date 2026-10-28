"""Known qubit/decoder operations only. No plant or source parameters."""
import numpy as np
from scipy.linalg import null_space
I = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], complex)
Y = np.array([[0,-1j],[1j,0]], complex)
Z = np.diag([1.,-1.]).astype(complex)
PAULIS = (I,X,Y,Z)
BASIS = np.array([np.kron(a,b) for a in (X,Y,Z) for b in PAULIS])
D, K, DIM = 12, 4, 2
C0 = np.eye(K, dtype=complex)/K

def choi(theta):
    return C0 + np.einsum('a,aij->ij', theta, BASIS)

def coordinates(c):
    return np.einsum('aij,ji->a', BASIS, c).real/K

def barrier(c):
    inv = np.linalg.inv(c)
    a = np.einsum('ij,ajk->aik', inv, BASIS)
    grad = -np.trace(a, axis1=1, axis2=2).real
    hess = np.einsum('aij,bji->ab', a, a).real
    return grad, (hess+hess.T)/2

def tp_residual(c):
    return float(np.linalg.norm(np.einsum('aiaj->ij', c.reshape(2,2,2,2))-I/2))

def apply_decoder(c, r):
    return DIM*np.einsum('aibj,ij->ab',c.reshape(2,2,2,2),r)

def unitary_choi(u):
    v=u.reshape(-1)
    return np.outer(v,v.conj())/DIM

def compile_decoder(c):
    """FLOAT dense Kraus + Stinespring matrix, not rational or gate synthesis."""
    vals, vecs = np.linalg.eigh(c)
    if vals.min() < -1e-12:
        raise ValueError('Nonpositive played Choi')
    ks = [np.sqrt(DIM*max(v,0))*vecs[:,a].reshape(2,2)
          for a,v in enumerate(vals)]
    iso = np.concatenate(ks,axis=0)  # environment first, output second
    unitary = np.column_stack((iso, null_space(iso.conj().T)))
    reconstructed = sum(np.outer(a.reshape(-1),a.reshape(-1).conj())/DIM for a in ks)
    diagnostics = {
        'kraus_rank': int(sum(vals > 1e-13)),
        'kraus_tp_residual': float(np.linalg.norm(sum(a.conj().T@a for a in ks)-I)),
        'choi_reconstruction_residual': float(np.linalg.norm(reconstructed-c)),
        'stinespring_isometry_residual': float(np.linalg.norm(iso.conj().T@iso-I)),
        'unitary_residual': float(np.linalg.norm(unitary.conj().T@unitary-np.eye(8))),
        'unitary_dimension': 8,
        'dense_complex_entries': 64,
    }
    return ks, diagnostics

def apply_kraus(ks,r):
    return sum(k@r@k.conj().T for k in ks)

def rotation(axis, angle):
    axis=np.asarray(axis,dtype=float);axis=axis/np.linalg.norm(axis)
    p=sum(a*b for a,b in zip(axis,(X,Y,Z)))
    return np.cos(angle/2)*I-1j*np.sin(angle/2)*p

def trace_distance(a,b):
    return float(np.abs(np.linalg.eigvalsh((a-b+a.conj().T-b.conj().T)/2)).sum()/2)
