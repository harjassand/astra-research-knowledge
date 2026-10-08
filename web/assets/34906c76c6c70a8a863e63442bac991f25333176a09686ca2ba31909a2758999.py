"""Numerical candidate search only; no finite grid is used as a certificate.

Enumerates two-qubit Pauli-invariant positive duals and compares the exact
finite-matrix star eigenvalue (legal after Pauli twirl) against a random-state
lower estimate of canonical EB support. A positive gap here is only a
candidate: support needs a global moment-dual envelope before it is a
counterexample.
"""
import itertools
import numpy as np

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
paulis1 = [I, X, Y, Z]
labels = list(itertools.product(range(4), repeat=2))[1:]
obs = [np.kron(paulis1[a], paulis1[b]) for a, b in labels]
obs_t = [p.T for p in obs]
Id = np.eye(4, dtype=complex)

def star(q):
    H = np.zeros((64, 64), complex)
    for w, p, pt in zip(q, obs, obs_t):
        H += w * (np.kron(np.kron(pt, p), Id) + np.kron(np.kron(pt, Id), p))
    return np.linalg.eigvalsh(H)[-1]

def random_states(rng, count):
    z = rng.normal(size=(count, 4)) + 1j * rng.normal(size=(count, 4))
    z /= np.linalg.norm(z, axis=1)[:, None]
    return z

def scores(states):
    rho = np.einsum("ni,nj->nij", states, states.conj())
    return np.stack([np.einsum("nij,ji->n", rho, p).real for p in obs], axis=1) ** 2

def f_and_tangent(psi, q):
    p = np.einsum("i,kij,j->k", psi.conj(), np.asarray(obs), psi).real
    f = float(np.dot(q, p * p))
    grad = 2 * np.einsum("k,kij,j->i", q * p, np.asarray(obs), psi)
    grad -= psi * np.vdot(psi, grad).real
    return f, grad

def local_max(seed, q, steps=160):
    psi = seed / np.linalg.norm(seed)
    f, grad = f_and_tangent(psi, q)
    for _ in range(steps):
        norm = np.linalg.norm(grad)
        if norm < 1e-11:
            break
        eta = 0.4 / max(norm, 1e-12)
        improved = False
        for __ in range(18):
            trial = psi + eta * grad
            trial /= np.linalg.norm(trial)
            f2, grad2 = f_and_tangent(trial, q)
            if f2 > f + 1e-14:
                psi, f, grad = trial, f2, grad2
                improved = True
                break
            eta *= 0.5
        if not improved:
            break
    return f, psi

def support_lower(q, states, vals):
    # Random states seed a lower bound; Riemannian ascent improves it. This
    # remains only a lower bound on S(Q), so it cannot certify a violation.
    scores_q = vals @ q
    ix = np.argpartition(scores_q, -5)[-5:]
    best = float(scores_q[ix].max())
    for i in ix:
        value, _ = local_max(states[i], q)
        best = max(best, value)
    for _ in range(3):
        value, _ = local_max(random_states(rng, 1)[0], q)
        best = max(best, value)
    return best

def main():
    global rng
    rng = np.random.default_rng(812733)
    states = random_states(rng, 5000)
    vals = scores(states)
    candidates = []
    # Include sparse/equal supports and random positive weights.
    for mask_size in range(1, 16):
        for _ in range(12):
            idx = rng.choice(15, mask_size, replace=False)
            q = np.zeros(15)
            q[idx] = rng.lognormal(mean=0.0, sigma=1.4, size=mask_size)
            q /= q.sum()
            candidates.append(q)
    best = None
    for count, q in enumerate(candidates, 1):
        s_lower = support_lower(q, states, vals)
        candidate_gap = star(q) - q.sum() - s_lower
        if best is None or candidate_gap > best[0]:
            best = (candidate_gap, q.copy(), star(q), s_lower)
    print("largest_candidate_gap_after_local_ascent", best[0])
    print("star", best[2], "traceQ", best[1].sum(), "support_lower", best[3])
    print("weights_by_label", [(labels[i], float(w)) for i, w in enumerate(best[1]) if w > 1e-10])
    print("candidate_count", len(candidates), "state_seeds", len(states))

if __name__ == "__main__":
    main()
