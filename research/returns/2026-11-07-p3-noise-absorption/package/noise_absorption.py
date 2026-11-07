"""Local positive noise completion; mathematical data, not a hardware driver.

Schrodinger picture. Choi uses output tensor input, unnormalised maximally
entangled vector. Dense routines are exponential in LOCAL block size only.
The binary64 emitter is diagnostic; exact rational examples live separately.
"""
from __future__ import annotations
import itertools
import math
import numpy as np
from scipy.linalg import eigh, null_space

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
PAULI = {"I": I, "X": X, "Y": Y, "Z": Z}


def kron_all(items):
    out = np.array([[1.]], dtype=complex)
    for a in items:
        out = np.kron(out, a)
    return out


def product_state(probabilities):
    return kron_all([np.diag([1-p, p]) for p in probabilities])


def dissipator(f, rho):
    a = f.conj().T @ f
    return f @ rho @ f.conj().T - (a @ rho + rho @ a) / 2


def generator_action(h, jumps, rho):
    out = -1j * (h @ rho - rho @ h)
    for f in jumps:
        out = out + dissipator(f, rho)
    return out


def superoperator(action, d):
    """Column vectorisation of density matrices."""
    cols = []
    for j in range(d):
        for i in range(d):
            e = np.zeros((d, d), complex)
            e[i, j] = 1
            cols.append(action(e).reshape(-1, order="F"))
    return np.stack(cols, axis=1)


def choi_from_super(s, d):
    return s.reshape(d, d, d, d, order="F").transpose(0, 2, 1, 3).reshape(d*d, d*d)


def super_from_choi(c, d):
    return c.reshape(d, d, d, d).transpose(0, 2, 1, 3).reshape(d*d, d*d, order="F")


def reset_super(omega):
    d = len(omega)
    return np.outer(omega.reshape(-1, order="F"), np.eye(d).reshape(-1, order="F"))


def noise_super(h, jumps):
    return superoperator(lambda x: generator_action(h, jumps, x), len(h))


def complete_to_reset(omega, h, jumps, kappa=None, margin=0.05):
    """Positive CP-part domination, and the exact CCP optimal rate diagnostically.

    Returned controller has Hc=-h and positive jump operators. Its sum with
    supplied noise is kappa*(R_omega-id). Rates include jump amplitudes.
    kappa_cp is optimal for THIS CP-part subtraction construction;
    kappa_ccp is optimal over all Lindblad controllers for THIS reset embedding.
    Neither is an optimum over all target-stabilizing control strategies.
    """
    d = len(omega)
    w, v = eigh(omega)
    if w[0] <= 0:
        raise ValueError("A faithful target is required by this compiler")
    invsqrt = (v / np.sqrt(w)) @ v.conj().T
    cp_noise = sum((np.outer(f.reshape(-1), f.reshape(-1).conj()) for f in jumps),
                   np.zeros((d*d, d*d), complex))
    ar = np.kron(omega, np.eye(d))
    whitening = np.kron(invsqrt, np.eye(d))
    kcp = max(0., float(eigh(whitening @ cp_noise @ whitening, eigvals_only=True)[-1]))
    omvec = np.eye(d).reshape(-1) / math.sqrt(d)
    q = null_space(omvec.conj()[None, :])
    ac = q.conj().T @ ar @ q
    bc = q.conj().T @ cp_noise @ q
    kccp = max(0., float(eigh(bc, ac, eigvals_only=True)[-1]))
    if kappa is None:
        kappa = kcp * (1 + margin) + margin
    c = kappa * ar - cp_noise
    vals, vecs = eigh((c+c.conj().T)/2)
    scale = max(1., np.linalg.norm(c, 2))
    if vals[0] < -1e-11 * scale:
        raise ValueError("Chosen rate fails CP-part domination")
    ctrl_jumps = [np.sqrt(x) * vecs[:, j].reshape(d, d)
                  for j, x in enumerate(vals) if x > 1e-14 * scale]
    ns = noise_super(h, jumps)
    cs = noise_super(-h, ctrl_jumps)
    expected = kappa * (reset_super(omega)-np.eye(d*d))
    return dict(kappa=float(kappa), kappa_cp=kcp, kappa_ccp=kccp,
                h_controller=-h, jumps_controller=ctrl_jumps,
                conditional_choi_min=float(eigh(kappa*ac-bc, eigvals_only=True)[0]),
                cp_choi_min=float(vals[0]),
                reconstruction_residual=float(np.linalg.norm(ns+cs-expected, 2)),
                stationarity_residual=float(np.linalg.norm((ns+cs) @ omega.reshape(-1, order="F"))),
                controller_activity=float(np.linalg.norm(h, 2)+sum(np.linalg.norm(f, 2)**2 for f in ctrl_jumps)),
                controller_activity_upper=float(np.linalg.norm(h, 2)+np.trace(c).real),
                noise_activity=float(np.linalg.norm(h, 2)+sum(np.linalg.norm(f, 2)**2 for f in jumps)),
                noise_super=ns, controller_super=cs)


def kms_complete(omega, f):
    """Known KMS modular pairing, with its necessary coherent correction.

    Derived from the Fagnola-Umanita / Chen-Kastoryano-Gilyen /
    Ding-Li-Lin characterization. The returned Hamiltonian is NOT optional.
    """
    w, v = eigh(omega)
    if w[0] <= 0:
        raise ValueError("Faithful state required")
    root = (v*np.sqrt(w)) @ v.conj().T
    invroot = (v/np.sqrt(w)) @ v.conj().T
    j = root @ f.conj().T @ invroot
    k = f.conj().T @ f + j.conj().T @ j
    ke = v.conj().T @ k @ v
    sw = np.sqrt(w)
    ratio = (sw[:, None]-sw[None, :])/(sw[:, None]+sw[None, :])
    g = v @ (-0.5j*ratio*ke) @ v.conj().T
    before = dissipator(f, omega)+dissipator(j, omega)
    after = generator_action(g, [f, j], omega)
    return dict(jump=j, h_correction=g,
                without_h_residual=float(np.linalg.norm(before)),
                with_h_residual=float(np.linalg.norm(after)),
                hermiticity_residual=float(np.linalg.norm(g-g.conj().T)))


def embed(a, sites, n):
    sites = tuple(sites)
    rest = [i for i in range(n) if i not in sites]
    tmp = np.kron(a, np.eye(2**len(rest)))
    old = list(sites)+rest
    axes = [old.index(i) for i in range(n)]
    return tmp.reshape([2]*(2*n)).transpose(axes+[n+i for i in axes]).reshape(2**n, 2**n)


def clifford_conjugate_word(word, gate):
    """Return sign and word for g P g^dagger; H,S,CNOT,CZ supported."""
    name = gate[0]
    sites = gate[1:]
    if name == "H":
        local_u = np.array([[1, 1], [1, -1]], complex)/np.sqrt(2)
    elif name == "S":
        local_u = np.diag([1, 1j])
    elif name == "SDG":
        local_u = np.diag([1, -1j])
    elif name == "CZ":
        local_u = np.diag([1, 1, 1, -1])
    elif name == "CNOT":
        local_u = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], complex)
    else:
        raise ValueError(name)
    local_p = kron_all([PAULI[word[i]] for i in sites])
    got = local_u @ local_p @ local_u.conj().T
    for chars in itertools.product("IXYZ", repeat=len(sites)):
        p = kron_all([PAULI[c] for c in chars])
        coeff = np.trace(p @ got)/(2**len(sites))
        if abs(abs(coeff)-1)<1e-12:
            new = list(word)
            for i, c in zip(sites, chars): new[i] = c
            return (1 if coeff.real > 0 else -1), "".join(new)
    raise RuntimeError("Clifford image was not a Pauli")


def conjugate_pauli_sum(terms, gates, inverse=False):
    gs = list(reversed(gates)) if inverse else gates
    out = dict(terms)
    for g in gs:
        if inverse and g[0] in ("S", "SDG"):
            g = (("SDG" if g[0] == "S" else "S"), *g[1:])
        nxt = {}
        for word, coeff in out.items():
            sign, new = clifford_conjugate_word(word, g)
            nxt[new] = nxt.get(new, 0)+sign*coeff
        out = {k:v for k,v in nxt.items() if abs(v)>1e-15}
    return out


def terms_matrix(terms, sites=None):
    if not terms:
        if sites is None: raise ValueError("dimension missing")
        return np.zeros((2**len(sites), 2**len(sites)), complex)
    if sites is None: sites=range(len(next(iter(terms))))
    return sum((c*kron_all([PAULI[w[i]] for i in sites]) for w,c in terms.items()),
               np.zeros((2**len(sites), 2**len(sites)), complex))


def compile_physical_block(n, probabilities, gates, h_terms, jump_terms, margin=.05):
    hs = conjugate_pauli_sum(h_terms, gates, inverse=True)
    fs = [conjugate_pauli_sum(f, gates, inverse=True) for f in jump_terms]
    words = list(hs)
    for f in fs: words.extend(f)
    support = sorted({i for w in words for i,c in enumerate(w) if c!="I"})
    if not support: raise ValueError("Identity-only block has no state-control role")
    h = terms_matrix(hs, support)
    jumps = [terms_matrix(f, support) for f in fs]
    omega = product_state([probabilities[i] for i in support])
    comp = complete_to_reset(omega, h, jumps, margin=margin)
    comp.update(support=support, n=n, local_dimension=len(omega),
                target_min_eigenvalue=float(np.linalg.eigvalsh(omega)[0]),
                h_noise=h, jumps_noise=jumps, omega=omega)
    return comp


def mixing_time(n, minimum_coverage_rate, epsilon):
    if minimum_coverage_rate <= 0 or not 0 < epsilon < 1:
        raise ValueError("Positive coverage and 0<epsilon<1 required")
    return math.log(n/epsilon)/minimum_coverage_rate


def residual_floor(n, minimum_coverage_rate, half_diamond_rate_sum):
    return min(1., 2*half_diamond_rate_sum*(1+math.log(n))/minimum_coverage_rate)


def jsonable_matrix(a):
    return {"real": np.asarray(a).real.tolist(), "imag": np.asarray(a).imag.tolist()}


def public_record(comp, include_matrices=True):
    skip = {"noise_super", "controller_super", "h_noise", "jumps_noise", "omega"}
    out = {}
    for k,v in comp.items():
        if k in skip: continue
        if isinstance(v,np.ndarray):
            if include_matrices: out[k]=jsonable_matrix(v)
        elif k=="jumps_controller":
            if include_matrices: out[k]=[jsonable_matrix(x) for x in v]
            out["controller_jump_count"]=len(v)
        else: out[k]=v
    return out
