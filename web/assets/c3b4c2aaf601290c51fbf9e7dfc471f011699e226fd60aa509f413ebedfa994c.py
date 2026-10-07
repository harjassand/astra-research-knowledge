"""Finite checks for arbitrary bistochastic instrument/Petz correction.

Only the symbolic instrument class is under test, never universal EB rounding.
NumPy only; no optimization solver or inferred separability certificate.
"""

import json
import platform
import sys

import numpy as np

SEED = 7072963
rng = np.random.default_rng(SEED)


def h_basis(d):
    result = []
    for i in range(d):
        z = np.zeros((d, d), complex)
        z[i, i] = np.sqrt(d)
        result.append(z)
    for i in range(d):
        for j in range(i + 1, d):
            z = np.zeros((d, d), complex)
            z[i, j] = z[j, i] = np.sqrt(d / 2)
            result.append(z)
            z = np.zeros((d, d), complex)
            z[i, j] = -1j * np.sqrt(d / 2)
            z[j, i] = 1j * np.sqrt(d / 2)
            result.append(z)
    return result


def psd_power(z, exponent):
    ev, u = np.linalg.eigh((z + z.conj().T) / 2)
    return (u * np.maximum(ev, 1e-15) ** exponent) @ u.conj().T


def norm1(z):
    return float(np.abs(np.linalg.eigvalsh((z + z.conj().T) / 2)).sum())


def superop(f, basis, d):
    return np.array([[np.trace(a @ f(b)).real / d for b in basis] for a in basis])


def min_eig(z):
    return float(np.linalg.eigvalsh((z + z.conj().T) / 2)[0])


def swap(z, d):
    return z.reshape(d, d, d, d).transpose(1, 0, 3, 2).reshape(d*d, d*d)


def partial_trace(z, d, receiver):
    t = z.reshape(d, d, d, d)
    return np.einsum('abcb->ac', t) if receiver == 0 else np.einsum('abad->bd', t)


def apply_local(z, f, d, receiver):
    t = z.reshape(d, d, d, d)
    ans = np.zeros_like(t)
    for i in range(d):
        for j in range(d):
            if receiver == 0:
                ans[:, i, :, j] = f(t[:, i, :, j])
            else:
                ans[i, :, j, :] = f(t[i, :, j, :])
    return ans.reshape(d*d, d*d)


def random_kraus(d, outcomes):
    raw = []
    for _ in range(outcomes):
        z = rng.normal(size=(d, d)) + 1j*rng.normal(size=(d, d))
        raw.append(z.conj().T @ z)
    scale = psd_power(sum(raw), -.5)
    effects = [scale @ z @ scale for z in raw]
    z = rng.normal(size=(d, d)) + 1j*rng.normal(size=(d, d))
    u, _ = np.linalg.qr(z)
    return [u @ psd_power(m, .5) for m in effects]


records = {
    'seed': SEED,
    'python_version': sys.version,
    'numpy_version': np.__version__,
    'platform': platform.platform(),
    'solver': None,
    'instrument_fixtures': [],
    'tensor_fixtures': [],
}
saved = []

fixtures = [(d, trial, random_kraus(d, 2+trial))
            for d in range(2, 8) for trial in range(3)]
z = np.diag([1., -1.]).astype(complex)
fixtures.append((2, 'negative_half_eigenvalue', [np.sqrt(.4)*z, np.sqrt(.6)*z]))

for d, trial, ks in fixtures:
    ms = [k.conj().T @ k for k in ks]
    ns = [k @ k.conj().T for k in ks]
    assert np.max(np.abs(sum(ms)-np.eye(d))) < 1e-12
    assert np.max(np.abs(sum(ns)-np.eye(d))) < 1e-12
    assert max(abs(np.trace(m)-np.trace(n)) for m, n in zip(ms, ns)) < 1e-12

    def t_map(a):
        return sum(k @ a @ k.conj().T for k in ks)

    def t_adjoint(a):
        return sum(k.conj().T @ a @ k for k in ks)

    def psi(a, effects):
        return sum(np.trace(m @ a)*m/np.trace(m) for m in effects)

    basis = h_basis(d)
    tm = superop(t_map, basis, d)
    pm = superop(lambda a: psi(a, ms), basis, d)

    def c_map(a):
        return (t_map(a)+psi(a, ms))/2

    def c_adjoint(a):
        return (t_adjoint(a)+psi(a, ms))/2

    def q_map(a):
        return c_adjoint(c_map(a))

    cm = (tm+pm)/2
    qm = cm.T @ cm
    ident = np.eye(d*d)
    lower = min(min_eig(pm), min_eig(ident-pm),
                min_eig(ident-tm.T @ tm), min_eig(ident+pm-2*qm),
                min_eig(qm), min_eig(ident-qm))
    sos = ident-tm.T @ tm+pm-pm @ pm+(tm-pm).T @ (tm-pm)/2
    assert np.max(np.abs(sos-(ident+pm-2*qm))) < 2e-12
    assert lower > -1e-11
    assert np.max(np.abs(superop(c_adjoint, basis, d)-cm.T)) < 1e-12
    assert np.max(np.abs(superop(q_map, basis, d)-qm)) < 2e-12
    assert np.max(np.abs(c_map(np.eye(d))-np.eye(d))) < 2e-12
    assert np.max(np.abs(c_adjoint(np.eye(d))-np.eye(d))) < 2e-12
    assert np.max(np.abs(q_map(np.eye(d))-np.eye(d))) < 2e-12

    h = rng.normal(size=(d, d)) + 1j*rng.normal(size=(d, d))
    h = (h+h.conj().T)/2
    h -= np.trace(h)*np.eye(d)/d
    h /= 2*np.max(np.abs(np.linalg.eigvalsh(h)))
    rho = (np.eye(d)+h)/d
    forward = sum(np.kron(k @ rho @ k.conj().T, m/np.trace(m))
                  for k, m in zip(ks, ms))
    joint_c = (forward+swap(forward, d))/2
    assert max(np.max(np.abs(partial_trace(joint_c, d, receiver)-c_map(rho)))
               for receiver in (0, 1)) < 2e-12
    joint_q = apply_local(apply_local(joint_c, c_adjoint, d, 0), c_adjoint, d, 1)
    marginal_error = max(np.max(np.abs(partial_trace(joint_q, d, receiver)-q_map(rho)))
                         for receiver in (0, 1))
    assert marginal_error < 2e-12
    assert min_eig(joint_q) > -2e-12
    assert abs(np.trace(joint_q)-1) < 2e-12
    residual = norm1(q_map(rho)-rho)
    eb_error = norm1(psi(rho, ms)-rho)/2
    bound = np.sqrt(residual)/2  # theta=.5, c=2
    assert eb_error <= bound+2e-12
    records['instrument_fixtures'].append({
        'd': d, 'trial': trial, 'outcomes': len(ks),
        'smallest_C_Hermitian_part_eigenvalue': min_eig((cm+cm.T)/2),
        'C_selfadjoint_defect': float(np.max(np.abs(cm-cm.T))),
        'loewner_min_eigenvalue': lower,
        'Q_minus_Psi_min_eigenvalue': min_eig(qm-pm),
        'local_Phi_Psi_commutator_2': float(np.linalg.norm(qm @ pm-pm @ qm)),
        'joint_marginal_max_abs_error': float(marginal_error),
        'full_trace_residual': residual, 'EB_half_trace_error': eb_error,
        'analytical_bound': float(bound),
    })
    if d <= 3:
        saved.append((d, qm, pm))

for i in range(0, len(saved)-1, 2):
    da, qa, pa = saved[i]
    db, qb, pb = saved[i+1]
    ident = np.eye((da*db)**2)
    lower = min_eig(2*(ident-np.kron(qa, qb))-(ident-np.kron(pa, pb)))
    assert lower > -2e-11
    records['tensor_fixtures'].append({'dimensions': [da, db], 'loewner_min_eigenvalue': lower})

records['status'] = 'PASS: finite arbitrary bistochastic-instrument/Petz correction fixtures only; unrestricted theorem unproved.'
with open('work/cycle4/bistochastic_instrument_checks.json', 'w') as f:
    json.dump(records, f, indent=2)
print(json.dumps({
    'status': records['status'], 'python_version': platform.python_version(),
    'numpy_version': np.__version__, 'instrument_fixtures': len(records['instrument_fixtures']),
    'tensor_fixtures': len(records['tensor_fixtures']),
    'smallest_C_Hermitian_part_eigenvalue': min(x['smallest_C_Hermitian_part_eigenvalue'] for x in records['instrument_fixtures']),
    'maximum_C_selfadjoint_defect': max(x['C_selfadjoint_defect'] for x in records['instrument_fixtures']),
    'smallest_Q_minus_Psi_eigenvalue': min(x['Q_minus_Psi_min_eigenvalue'] for x in records['instrument_fixtures']),
    'worst_marginal_error': max(x['joint_marginal_max_abs_error'] for x in records['instrument_fixtures']),
    'smallest_Loewner_eigenvalue': min(x['loewner_min_eigenvalue'] for x in records['instrument_fixtures']+records['tensor_fixtures']),
}, indent=2))
