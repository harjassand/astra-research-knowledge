"""Small diagnostics for the proved spectral-pinching EB lift.

Float fixtures verify transcription, not the theorem or general acquisition.
The first suite uses Fraction arithmetic and checks the one-step inequality.
"""
from fractions import Fraction
import json
import math
from pathlib import Path
import numpy as np


def exact_pair(d, h):
    spectrum = [Fraction(j, d) for j in range(d)]
    residues = sorted(set([Fraction(0), h] + [x % h for x in spectrum]))
    shifts = [(a + b) / 2 for a, b in zip(residues, residues[1:]) if a < b]
    candidates = []
    b2 = Fraction(d - 1, 2 * d)
    comm2 = Fraction(d - 1, 2 * d**3)
    for u in shifts:
        labels = [(x - u) // h for x in spectrum]
        off2 = sum(Fraction(1, 2 * d) for j in range(d - 1)
                   if labels[j] != labels[j + 1])
        rounded = [min(Fraction(1), max(Fraction(-1), u + (k + Fraction(1, 2))*h))
                   for k in labels]
        pivot2 = sum((x-y)**2 for x, y in zip(spectrum, rounded)) / d
        candidates.append((off2, pivot2, u))
    off2, pivot2, u = min(candidates)
    assert (h * off2)**2 <= comm2 * b2
    assert pivot2 <= h*h/4
    return {"dimension": d, "h": str(h), "chosen_shift": str(u),
            "offblock_squared_L2": str(off2), "pivot_squared_L2": str(pivot2),
            "commutator_squared_L2": str(comm2), "exact_pass": True,
            "candidate_count": len(shifts)}


def l2(a):
    return float(np.linalg.norm(a, 'fro') / math.sqrt(a.shape[0]))


def modulus(r, delta):
    if r <= 1 or delta == 0:
        return 0.0
    t = ((r-1)*delta)**(1/3)
    return min(1.0, math.hypot(t, modulus(r-1, min(2.0, delta+4*t))))


def block_diagonalize(pivot, blocks):
    d = len(pivot)
    w = np.zeros((d, d), dtype=complex)
    spectrum = np.zeros(d)
    for ids in blocks:
        vals, vecs = np.linalg.eigh(pivot[np.ix_(ids, ids)])
        w[np.ix_(ids, ids)] = vecs
        spectrum[ids] = vals
    return w, spectrum


def pinching_basis(matrices, delta):
    """Return a unitary basis; use the proof's predetermined recurrence."""
    d = matrices[0].shape[0]
    current = [x.copy() for x in matrices]
    u_total = np.eye(d, dtype=complex)
    blocks = [np.arange(d)]
    logs = []
    bound = delta
    for j in range(len(matrices)-1):
        w, spectrum = block_diagonalize(current[j], blocks)
        current = [w.conj().T @ x @ w for x in current]
        u_total = u_total @ w
        remaining = len(matrices)-j-1
        h = max(1e-12, (remaining*bound)**(1/3))
        cuts = np.unique(np.concatenate(([0.0, h], np.mod(spectrum, h))))
        shifts = [(a+b)/2 for a, b in zip(cuts, cuts[1:]) if b-a > 1e-13*h]
        if not shifts:
            shifts = [h/2]
        best = None
        for shift in shifts:
            labels = np.floor((spectrum-shift)/h).astype(np.int64)
            proposed = [old[labels[old] == label]
                        for old in blocks for label in np.unique(labels[old])]
            mask = np.zeros((d, d), dtype=bool)
            for ids in proposed:
                mask[np.ix_(ids, ids)] = True
            cost = sum(l2(x * (~mask))**2 for x in current[j+1:])
            if best is None or cost < best[0]:
                best = (cost, shift, proposed, mask)
        cost, shift, blocks, mask = best
        for k in range(j+1, len(current)):
            current[k] *= mask
        t = (remaining*bound)**(1/3)
        assert cost <= remaining*bound/h + 1e-10
        logs.append({"stage": j, "h": h, "sum_offblock_L2_squared": cost,
                     "proved_bound": remaining*bound/h, "block_count": len(blocks)})
        bound = min(2.0, bound+4*t)
    w, _ = block_diagonalize(current[-1], blocks)
    return u_total @ w, logs


def dephase(x, u):
    y = u.conj().T @ x @ u
    return u @ np.diag(np.diag(y)) @ u.conj().T


def float_suite():
    rng = np.random.default_rng(7075303)
    rows = []
    for d in [3, 5, 8, 12]:
        for r in [2, 3, 4]:
            for eps in [1e-2, 1e-5, 1e-9]:
                z = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
                q, _ = np.linalg.qr(z)
                matrices = []
                for j in range(r):
                    diag = np.diag(rng.uniform(-.65, .65, d))
                    noise = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
                    noise = (noise+noise.conj().T)/2
                    noise /= max(1, np.linalg.norm(noise,2))
                    matrices.append(q @ (diag+eps*noise) @ q.conj().T)
                delta = max(l2(a@b-b@a) for a in matrices for b in matrices)
                u, logs = pinching_basis(matrices, delta)
                errors = [l2(a-dephase(a,u)) for a in matrices]
                predicted = modulus(r,delta)
                assert max(errors) <= predicted + 2e-8
                assert np.linalg.norm(u.conj().T@u-np.eye(d)) < 1e-10
                rows.append({"d":d,"r":r,"epsilon":eps,"delta":delta,
                             "max_lift_L2_error":max(errors),"modulus":predicted,
                             "stages":logs})
    return rows


def eb_fixture():
    # T=(1-epsilon)*computational dephasing+epsilon*identity is bistochastic.
    d, eps = 4, .03
    rng = np.random.default_rng(7075304)
    z = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
    u, _ = np.linalg.qr(z)
    def t(x):
        return (1-eps)*np.diag(np.diag(x)) + eps*x
    projectors = [np.outer(u[:,j],u[:,j].conj()) for j in range(d)]
    effects = [t(p) for p in projectors]  # T*=T here.
    choi = sum(np.kron(m.T,p) for m,p in zip(effects,projectors))
    errors = []
    for i in range(d):
        for j in range(d):
            e = np.zeros((d,d),dtype=complex); e[i,j] = 1
            lhs = dephase(t(e),u)
            rhs = sum(np.trace(m@e)*p for m,p in zip(effects,projectors))
            errors.append(np.linalg.norm(lhs-rhs))
    assert min(np.linalg.eigvalsh(m).min() for m in effects) > -1e-12
    assert np.linalg.norm(sum(effects)-np.eye(d)) < 1e-12
    assert max(errors) < 1e-12
    assert np.linalg.eigvalsh(choi).min() > -1e-12
    return {"dimension":d,"epsilon":eps,"outcomes":len(effects),
            "minimum_effect_eigenvalue":float(min(np.linalg.eigvalsh(m).min() for m in effects)),
            "minimum_choi_eigenvalue":float(np.linalg.eigvalsh(choi).min()),
            "measure_prepare_identity_max_error":max(errors),
            "scope":"explicit separable Choi decomposition; float transcription check"}


if __name__ == '__main__':
    report = {"seed":7075303,"exact_pairs":[exact_pair(d,Fraction(1,k))
              for d,k in [(8,2),(27,3),(64,4)]],
              "float_approximate_commuting_fixtures":float_suite(),
              "eb_composition_fixture":eb_fixture(),
              "modulus_samples":[{"r":r,"delta":1e-12,"F":modulus(r,1e-12)}
                                  for r in range(2,9)],
              "scope":"bounded small exact/float diagnostics only; no uniform theorem inferred"}
    path = Path(__file__).with_name('pinching_lift_checks.json')
    path.write_text(json.dumps(report,indent=2))
    print(json.dumps({"exact_pairs":len(report['exact_pairs']),
                     "float_fixtures":len(report['float_approximate_commuting_fixtures']),
                     "eb_fixture":report['eb_composition_fixture'],
                     "modulus_samples":report['modulus_samples'],
                     "output":str(path)},indent=2))
