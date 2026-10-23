"""Finite checks for the quantum-mask mass construction, not a proof.

Uses complex ancillary effects so an omitted physical-Bob transpose fails.
Two tested positions, two predicate types, correlated original coarse
answer strings, noncommuting original fine effects, one fixed pool.
Only NumPy is required. Outputs stay in this agent's own work directory.
"""
from itertools import product
from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parent
rng = np.random.default_rng(2601024)


def sqrt_psd(a, inverse=False):
    vals, vecs = np.linalg.eigh(a)
    if inverse:
        vals = np.where(vals > 1e-13, 1.0 / np.sqrt(np.maximum(vals, 1e-300)), 0.0)
    else:
        vals = np.sqrt(np.maximum(vals, 0.0))
    return (vecs * vals) @ vecs.conj().T


def povm(n, d=2):
    raw = []
    for _ in range(n):
        z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
        raw.append(z @ z.conj().T + 0.1 * np.eye(d))
    inv = sqrt_psd(sum(raw), inverse=True)
    return [inv @ a @ inv for a in raw]


def proj(angle):
    v = np.array([np.cos(angle), np.sin(angle)])
    return np.outer(v, v)


def chi(s, f, h):
    value = np.trace(s @ f @ s @ h)
    assert abs(value.imag) < 1e-11
    return float(value.real)


def tensor_all(items):
    out = np.ones((1, 1), dtype=complex)
    for a in items:
        out = np.kron(out, a)
    return out


def dictionary(kind, angle):
    # U tensor conjugate(U) fixes Phi+, retaining the chosen Schmidt basis.
    u = np.array([[np.cos(angle), 1j*np.sin(angle)],
                  [1j*np.sin(angle), np.cos(angle)]])
    if kind == 0:  # L
        mask = np.array([[1, 1], [0, 1]], dtype=int)
        ea = [proj(np.pi/6), proj(np.pi/2)]
        bb = [proj(0), proj(np.pi/3)]
        lam, cap = 8/3, 4/3
    else:  # equality
        mask = np.eye(2, dtype=int)
        ea = [proj(0), proj(np.pi/2)]
        bb = [proj(0), proj(np.pi/2)]
        lam, cap = 2, 1
    e = [u @ a @ u.conj().T for a in ea]
    b_phys = [u.conj() @ a @ u.T for a in bb]
    h = [a.T for a in b_phys]
    sigma = np.eye(2) / np.sqrt(2)
    q = np.array([[chi(sigma, a, b) for b in h] for a in e])
    q_wrong = np.array([[chi(sigma, a, b) for b in b_phys] for a in e])
    assert np.max(abs(lam*q-mask)) < 1e-12
    return dict(mask=mask, e=e, h=h, b_phys=b_phys, lam=lam, cap=cap,
                wrong_error=float(np.max(abs(lam*q_wrong-mask))))


dicts = {(ell, kind): dictionary(kind, 0.19+0.17*ell+0.11*kind)
         for ell in range(2) for kind in range(2)}
pool_slots = list(dicts)
sigma_pool = np.eye(16) / 4
sigma = np.array([[0.65, 0.15+0.13j], [0.15-0.13j, 0.35]])
sigma /= np.sqrt(np.trace(sigma@sigma).real)
sigma_total = np.kron(sigma, sigma_pool)
assert abs(np.trace(sigma_total@sigma_total)-1) < 1e-12

# Each complete eight-outcome POVM is indexed (tested answer string, live
# answer); its four tested coarse effects are not assumed product effects.
G = np.array([povm(8) for _ in range(2)]).reshape(2, 4, 2, 2, 2)
K = np.array([povm(8) for _ in range(2)]).reshape(2, 4, 2, 2, 2)
F, H = G.sum(axis=2), K.sum(axis=2)
answers = list(product(range(2), repeat=2))
question_probability = np.array([1/5, 4/5])
live_mu = np.array([[0.4, 0.1], [0.2, 0.3]])

all_c = list(product(range(2), repeat=2))
Lambda = sum(np.prod([question_probability[q] for q in c]) *
             np.prod([dicts[(ell,q)]["lam"] for ell,q in enumerate(c)])
             for c in all_c)
original_p, tilted_p = 0.0, 0.0
GA, GB = 0.0, 0.0
original_live = np.zeros((2, 2, 2, 2))
tilted_live = np.zeros_like(original_live)
max_fine_error, max_cap_error, checks = 0.0, 0.0, 0

for c in all_c:
    prior_c = np.prod([question_probability[q] for q in c])
    lam = np.prod([dicts[(ell,q)]["lam"] for ell,q in enumerate(c)])
    cap = np.prod([dicts[(ell,q)]["cap"] for ell,q in enumerate(c)])
    prior_tilt = prior_c*lam/Lambda

    def ancillary(answer, key):
        factors = []
        for ell, kind in pool_slots:
            factors.append(dicts[(ell,kind)][key][answer[ell]]
                           if c[ell] == kind else np.eye(2))
        return tensor_all(factors)

    es = [ancillary(a,"e") for a in answers]
    hs = [ancillary(b,"h") for b in answers]
    gh = [[sum(np.kron(G[x,alpha,a],es[alpha]) for alpha in range(4))
           for a in range(2)] for x in range(2)]
    kh = [[sum(np.kron(K[y,gamma,b],hs[gamma]) for gamma in range(4))
           for b in range(2)] for y in range(2)]
    fh, hh = [sum(row) for row in gh], [sum(row) for row in kh]
    eye = np.eye(32)
    for effect in fh+hh:
        assert np.linalg.eigvalsh(effect).min() > -1e-12
        assert np.linalg.eigvalsh(eye-effect).min() > -1e-12

    local_A = sum(live_mu[x].sum()*lam*chi(sigma_total,fh[x],eye)
                  for x in range(2))
    local_B = sum(live_mu[:,y].sum()*lam*chi(sigma_total,eye,hh[y])
                  for y in range(2))
    GA += prior_c*local_A
    GB += prior_c*local_B
    max_cap_error = max(max_cap_error,abs(local_A-cap),abs(local_B-cap))

    for x,y,a,b in product(range(2),repeat=4):
        target = 0.0
        for alpha,gamma in product(range(4),repeat=2):
            mask = np.prod([dicts[(ell,c[ell])]["mask"][answers[alpha][ell],
                                                               answers[gamma][ell]]
                            for ell in range(2)])
            target += mask*chi(sigma,G[x,alpha,a],K[y,gamma,b])
        actual = chi(sigma_total,gh[x][a],kh[y][b])
        max_fine_error = max(max_fine_error,abs(lam*actual-target))
        original_live[x,y,a,b] += prior_c*live_mu[x,y]*target
        tilted_live[x,y,a,b] += prior_tilt*live_mu[x,y]*actual
        checks += 1

original_p = original_live.sum()
tilted_p = tilted_live.sum()
kappa = sum(question_probability[q]*dicts[(0,q)]["cap"] for q in range(2))
assert max_fine_error < 1e-11
assert max_cap_error < 1e-11
assert abs(GA-kappa**2) < 1e-11
assert abs(GB-kappa**2) < 1e-11
assert abs(tilted_p-original_p/Lambda) < 1e-11
conditional_table_error = np.max(abs(original_live/original_p - tilted_live/tilted_p))
assert conditional_table_error < 1e-11
wrong_orientation_error = max(d["wrong_error"] for d in dicts.values())
assert wrong_orientation_error > 0.1

# Normalized matrix trace needs sqrt(d) times the ordinary-Tr vector.
d = sigma_total.shape[0]
sigma_normalized_trace = np.sqrt(d)*sigma_total
trace_scaling_error = abs(np.trace(sigma_normalized_trace@sigma_normalized_trace)/d-1)
assert trace_scaling_error < 1e-12

result = dict(status="PASS finite algebra only; not a proof or resource benchmark",
              matched_fine_entries=checks,
              max_fine_identity_error=max_fine_error,
              max_pointwise_mass_cap_error=max_cap_error,
              kappa=kappa, measured_G_A=GA, measured_G_B=GB,
              predicted_G=kappa**2, Lambda_C=float(Lambda),
              original_event_p=float(original_p), tilted_event_p=float(tilted_p),
              conditional_table_error=float(conditional_table_error),
              wrong_Bob_transpose_mask_error=wrong_orientation_error,
              normalized_trace_scaling_error=float(trace_scaling_error))
(ROOT/"quantum_mass_replay_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
