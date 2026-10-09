"""Finite diagnostics for exact local lemmas, not theorem verification."""
import json
import numpy as np
from pathlib import Path

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(20261009)


def hp(x, p):
    z, u = np.linalg.eigh((x + x.conj().T) / 2)
    assert z.min() >= -2e-10
    good = z > 1e-13
    v = np.zeros_like(z)
    v[good] = z[good] ** p
    return (u * v) @ u.conj().T


def pos(x):
    z, u = np.linalg.eigh((x + x.conj().T) / 2)
    return (u * np.maximum(z, 0)) @ u.conj().T


def tn(x):
    return np.linalg.svd(x, compute_uv=False).sum().real


def half(x, y):
    return tn(x - y) / 2


def state(d, rank=None):
    k = d if rank is None else rank
    v = rng.normal(size=(d, k)) + 1j * rng.normal(size=(d, k))
    x = v @ v.conj().T
    return x / np.trace(x)


def pur(nu):
    v = hp(nu, .5).T.reshape(-1)
    return np.outer(v, v.conj())


def local(x, a, d, f):
    y = np.zeros_like(x, dtype=complex).reshape(a, d, a, d)
    z = x.reshape(a, d, a, d)
    for i in range(a):
        for j in range(a):
            y[i, :, j, :] = f(z[i, :, j, :])
    return y.reshape(a * d, a * d)


def repair(nu, sig):
    m = nu + pos(sig - nu)
    k = hp(sig, .5) @ hp(m, -.5)
    q = float((1 - np.trace(k @ nu @ k.conj().T)).real)
    defect = np.eye(len(nu)) - k.conj().T @ k
    chi = (sig - k @ nu @ k.conj().T) / q if q > 1e-11 else sig
    return (lambda y: k @ y @ k.conj().T + np.trace(defect @ y) * chi), m, k, q


def basis(d):
    h = []
    for i in range(d):
        x = np.zeros((d, d), complex)
        x[i, i] = 1
        h.append(x)
    for i in range(d):
        for j in range(i + 1, d):
            x = np.zeros((d, d), complex)
            x[i, j] = x[j, i] = 1 / np.sqrt(2)
            h.append(x)
            y = np.zeros((d, d), complex)
            y[i, j] = -1j / np.sqrt(2)
            y[j, i] = 1j / np.sqrt(2)
            h.append(y)
    return h


def mat(f, h):
    return np.array([[np.trace(a @ f(b)).real for b in h] for a in h])


def eb(d, k=8):
    vs = [rng.normal(size=d) + 1j * rng.normal(size=d) for _ in range(k)]
    raw = [np.outer(v, v.conj()) for v in vs]
    z = hp(sum(raw), -.5)
    ms = [z @ a @ z for a in raw]
    ss = [state(d) for _ in range(k)]
    f = lambda x: sum(np.trace(m @ x) * s for m, s in zip(ms, ss))
    fs = lambda x: sum(np.trace(s @ x) * m for m, s in zip(ms, ss))
    return f, fs


repair_rows = []
for d in (2, 3, 5):
    for rank_n, rank_s in ((d, d), (1, d), (d, 1), (1, 1)):
        for _ in range(20):
            nu, sig = state(d, rank_n), state(d, rank_s)
            f, m, k, q = repair(nu, sig)
            delta = half(nu, sig)
            eps = tn((np.eye(d) - k) @ hp(nu, .5))  # HS recomputed below
            w = (np.eye(d) - k) @ hp(nu, .5)
            eps = float(np.trace(w.conj().T @ w).real)
            joint = pur(nu)
            got = local(joint, d, d, f)
            distance = half(joint, got)
            bound = np.sqrt(max(0, 2 * delta - delta**2))
            checks = {
                "min_m_minus_nu": float(np.linalg.eigvalsh(m - nu).min()),
                "min_m_minus_sigma": float(np.linalg.eigvalsh(m - sig).min()),
                "min_defect": float(np.linalg.eigvalsh(np.eye(d) - k.conj().T @ k).min()),
                "stationary_error": tn(f(nu) - sig),
                "q_minus_delta": q - delta,
                "eps_minus_delta": eps - delta,
                "extension_excess": distance - bound,
                "trace_error": abs(np.trace(got) - 1),
            }
            assert min(checks[name] for name in ("min_m_minus_nu", "min_m_minus_sigma", "min_defect")) >= -2e-9
            assert max(checks[name] for name in ("stationary_error", "q_minus_delta", "eps_minus_delta", "extension_excess", "trace_error")) <= 2e-9
            repair_rows.append(checks)

# Equal singular states test q=0 completion, including input outside support.
for d in (2, 5):
    nu = state(d, 1)
    f, m, k, q = repair(nu, nu)
    assert abs(q) < 2e-9
    assert tn(f(nu) - nu) < 2e-9
    for j in range(d):
        x = np.zeros((d, d), complex)
        x[j, j] = 1
        assert abs(np.trace(f(x)) - 1) < 2e-9

weighted_rows = []
for _ in range(24):
    d, a = 3, 2
    sig = state(d)
    t, ts = eb(d)
    nu = t(sig)
    sr, ni = hp(sig, .5), hp(nu, -.5)
    r = lambda y: sr @ ts(ni @ y @ ni) @ sr
    s = lambda y: r(t(y))
    ss = lambda y: ts(ni @ t(sr @ y @ sr) @ ni)
    h = basis(d)
    gm = mat(lambda x: hp(sig, .25) @ x @ hp(sig, .25), h)
    sm, hm = mat(s, h), mat(ss, h)
    l = np.linalg.solve(gm, sm @ gm)
    lh = gm @ hm @ np.linalg.inv(gm)
    tm = mat(t, h)
    gn = mat(lambda x: hp(nu, .25) @ x @ hp(nu, .25), h)
    v = np.linalg.solve(gn, tm @ gm)
    assert np.linalg.norm(l - l.T) < 2e-8
    assert np.linalg.norm(l - lh) < 2e-8
    assert np.linalg.norm(l - v.T @ v) < 2e-8
    assert np.linalg.eigvalsh(l).min() >= -2e-8
    assert np.linalg.eigvalsh(l).max() <= 1 + 2e-8
    assert tn(s(sig) - sig) < 2e-8
    ra = state(a)
    omega = np.kron(ra, sig)
    raw = rng.normal(size=(a*d, a*d)) + 1j * rng.normal(size=(a*d, a*d))
    hh = (raw + raw.conj().T) / 2
    hh -= np.trace(omega @ hh).real * np.eye(a*d)
    hh /= np.max(np.abs(np.linalg.eigvalsh(hh)))
    root_omega = hp(omega, .5)
    u = root_omega @ (np.eye(a*d) + .5 * hh) @ root_omega
    su = local(u, a, d, s)
    x = hp(omega, -.25) @ u @ hp(omega, -.25)
    coord_res = hp(omega, -.25) @ (u - su) @ hp(omega, -.25)
    energy = np.trace(x @ coord_res).real
    likelihood = hp(omega, -.5) @ u @ hp(omega, -.5)
    energy_direct = np.trace(likelihood @ (u - su)).real
    q_res = np.trace(coord_res @ coord_res).real
    full = tn(u - su)
    assert abs(energy - energy_direct) < 2e-8
    assert full**2 <= q_res + 2e-8
    assert q_res <= energy + 2e-8  # Psi=S in this EB diagnostic
    assert energy <= .5 * full + 2e-8
    weighted_rows.append({
        "conjugation_error": float(np.linalg.norm(l-lh)),
        "petz_factorization_error": float(np.linalg.norm(l-v.T@v)),
        "energy_identity_error": abs(energy-energy_direct),
        "HS_asymmetry": float(np.linalg.norm(sm-sm.T)),
        "unital_error": tn(s(np.eye(d))-np.eye(d)),
    })

# The entropy constant 2 for nonreversible channels approaches sharpness.
cycle_rows = []
for n, ratio in ((7, .4), (30, .7), (300, .97), (2000, .995)):
    p = ratio ** np.arange(n)
    p /= p.sum()
    shifted = np.roll(p, 1)
    entropy_production = float(np.dot(p-shifted, np.log(p)))
    energy = float(1-np.dot(np.sqrt(p), np.sqrt(shifted)))
    quotient = entropy_production / energy
    assert quotient >= 2-2e-10
    cycle_rows.append({"n": n, "ratio": ratio, "entropy_over_root_energy": quotient})

result = {
    "scope": "Finite diagnostics only; not proof, external validation, or a test of weighted C4 itself.",
    "seed": 20261009,
    "repair_cases": len(repair_rows),
    "repair_max_stationary_error": max(x["stationary_error"] for x in repair_rows),
    "repair_max_extension_excess": max(x["extension_excess"] for x in repair_rows),
    "repair_max_epsilon_excess": max(x["eps_minus_delta"] for x in repair_rows),
    "weighted_cases": len(weighted_rows),
    "weighted_max_conjugation_error": max(x["conjugation_error"] for x in weighted_rows),
    "weighted_max_petz_factorization_error": max(x["petz_factorization_error"] for x in weighted_rows),
    "weighted_max_energy_identity_error": max(x["energy_identity_error"] for x in weighted_rows),
    "nontracial_min_HS_asymmetry": min(x["HS_asymmetry"] for x in weighted_rows),
    "nontracial_min_unital_error": min(x["unital_error"] for x in weighted_rows),
    "directed_cycle_entropy_diagnostics": cycle_rows,
    "status": "PASS",
}
(OUT / "LOCAL_GATE_FINITE_CHECKS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
