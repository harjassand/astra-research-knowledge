"""Binary64 finite-matrix emitter for the report's thermal controller.

Not a rigorous finite-bit or hardware certificate. The report supplies the
analytic construction and locality bounds. This emitter includes the full
Gaussian CKG cross-frequency Gram matrix, not a Davies/secular replacement.
"""
import numpy as np
from scipy.linalg import eigh, expm

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
DOWN = np.array([[0, 1], [0, 0]], dtype=complex)


def kron_all(mats):
    out = np.ones((1, 1), dtype=complex)
    for a in mats:
        out = np.kron(out, a)
    return out


def onsite(a, i, n):
    return kron_all([a if k == i else I2 for k in range(n)])


def two_site(a, i, b, j, n):
    return kron_all([a if k == i else b if k == j else I2 for k in range(n)])


def gibbs(h, beta):
    ee, u = eigh(h)
    p = np.exp(-beta*(ee-ee.min()))
    p /= p.sum()
    return (u*p) @ u.conj().T


def coherent(h, k, beta):
    ee, u = eigh(h)
    kk = u.conj().T @ k @ u
    out = 0.5j*np.tanh(beta*(ee[:, None]-ee[None, :])/4)*kk
    out = u @ out @ u.conj().T
    return (out+out.conj().T)/2


def complete_noise(h, f, beta, drift=None):
    ee, u = eigh(h)
    ff = u.conj().T @ f.conj().T @ u
    jj = np.exp(-beta*(ee[:, None]-ee[None, :])/2)*ff
    j = u @ jj @ u.conj().T
    k = f.conj().T @ f + j.conj().T @ j
    g = coherent(h, k, beta)
    if drift is not None:
        g = g-drift
    return j, g


def dissipator(f):
    d = len(f)
    k = f.conj().T @ f
    eye = np.eye(d)
    return np.kron(f.conj(), f)-0.5*np.kron(eye, k)-0.5*np.kron(k.T, eye)


def commutator(h):
    d = len(h)
    return -1j*(np.kron(np.eye(d), h)-np.kron(h.T, np.eye(d)))


def ckg_site(h, proposals, beta):
    """Exact analytic Gaussian integral evaluated in binary64.

    Proposals are normalized as A = Pauli/d for qubits d=2. The nonzero
    eigenvalues of the CP Gram matrix give a finite jump list. Near-zero
    roundoff negatives are recorded, not treated as rigorous PSD proofs.
    """
    ee, u = eigh(h)
    d = len(h)
    gaps = beta*(ee[:, None]-ee[None, :]).reshape(-1, order="F")
    aa, bb = gaps[:, None], gaps[None, :]
    kernel = np.exp(-0.5-(aa*aa+bb*bb)/4+(aa+bb-2)**2/16)/np.sqrt(2)
    choi = np.zeros((d*d, d*d), dtype=complex)
    for a in proposals:
        av = (u.conj().T @ a @ u).reshape(-1, order="F")
        choi += av[:, None]*av[None, :].conj()*kernel
    vals, vecs = eigh((choi+choi.conj().T)/2)
    raw_min = float(vals.min())
    cutoff = 1e-13*max(1.0, float(vals.max()))
    jumps = []
    discarded_mass = 0.0
    for val, vec in zip(vals, vecs.T):
        if val > cutoff:
            z = np.sqrt(val)*vec.reshape((d, d), order="F")
            jumps.append(u @ z @ u.conj().T)
        else:
            discarded_mass += abs(float(val))
    k = sum((f.conj().T @ f for f in jumps), start=np.zeros_like(h))
    g = coherent(h, k, beta)
    generator = commutator(g)
    for f in jumps:
        generator += dissipator(f)
    return generator, jumps, g, {"raw_gram_min_eigenvalue": raw_min,
                               "discarded_eigenvalue_mass": discarded_mass,
                               "jump_count": len(jumps)}


def apply_channel_super(s, rho):
    return (s @ rho.reshape(-1, order="F")).reshape(rho.shape, order="F")


def apply_with_reference(s, rho, d, r):
    """Work tensor reference; untouched reference may be entangled."""
    out = np.zeros_like(rho)
    z = rho.reshape(d, r, d, r)
    for a in range(r):
        for b in range(r):
            out.reshape(d, r, d, r)[:, a, :, b] = apply_channel_super(s, z[:, a, :, b])
    return out


def entropy_relative(rho, tau):
    p = np.linalg.eigvalsh((rho+rho.conj().T)/2)
    p = np.maximum(p, 0)
    val, vec = eigh(tau)
    logtau = (vec*np.log(val)) @ vec.conj().T
    nz = p > 1e-15
    return float(np.sum(p[nz]*np.log(p[nz]))-np.trace(rho @ logtau).real)


def trace_distance(a, b):
    return float(np.linalg.svd(a-b, compute_uv=False).sum()/2)
