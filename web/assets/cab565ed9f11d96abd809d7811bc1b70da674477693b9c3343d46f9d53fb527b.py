"""Duplicated d=3 control only; not a C8 advance beyond the prime-d line theorem.

Retained as a prior finite control after the branch pivoted to the unexplored
d=5 non-line-constant channel. No new d=3 claim is made here.

Original candidate-search note:

The star maximum is the exact support over compatible covariant extensions:
the dual is invariant under Weyl translations and parity, so averaging a top
star eigenstate over this irreducible representation and output swap repairs
the Choi marginals without changing the score. The pure-state scan below is
only a support lower bound and cannot certify a violation.
"""
import itertools
import numpy as np

d = 3
w = np.exp(2j * np.pi / d)
X = np.roll(np.eye(d, dtype=complex), 1, axis=1)
Z = np.diag([w**j for j in range(d)])
Id = np.eye(d, dtype=complex)
reps = [(0, 1), (1, 0), (1, 1), (1, 2)]
obs = []
for a, b in reps:
    W = np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, b)
    obs.append((W + W.conj().T) / np.sqrt(2))
    obs.append((W - W.conj().T) / (1j * np.sqrt(2)))
obs = np.asarray(obs)
obs_t = np.transpose(obs, (0, 2, 1))

def star(q):
    H = np.zeros((d**3, d**3), complex)
    for pair, weight in enumerate(q):
        for A in obs[2*pair:2*pair+2]:
            H += weight * (np.kron(np.kron(A.T, A), Id) + np.kron(np.kron(A.T, Id), A))
    return np.linalg.eigvalsh(H)[-1]

def random_states(rng, count):
    z = rng.normal(size=(count, d)) + 1j * rng.normal(size=(count, d))
    z /= np.linalg.norm(z, axis=1)[:, None]
    return z

def scores(states):
    rho = np.einsum("ni,nj->nij", states, states.conj())
    return np.stack([np.einsum("nij,ji->n", rho, A).real for A in obs], axis=1) ** 2

def f_and_tangent(psi, q):
    p = np.einsum("i,kij,j->k", psi.conj(), obs, psi).real
    weights = np.repeat(q, 2)
    f = float(np.dot(weights, p * p))
    grad = 2 * np.einsum("k,kij,j->i", weights * p, obs, psi)
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
        for __ in range(16):
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
    return f

def main():
    rng = np.random.default_rng(9322026)
    states = random_states(rng, 12000)
    vals = scores(states)
    best = None
    best_line_envelope = None
    for _ in range(700):
        q = rng.lognormal(0.0, 1.2, size=4)
        q /= q.sum()
        vals_q = vals @ np.repeat(q, 2)
        ix = np.argpartition(vals_q, -5)[-5:]
        support_lower = float(vals_q[ix].max())
        for i in ix:
            support_lower = max(support_lower, local_max(states[i], q))
        for __ in range(3):
            support_lower = max(support_lower, local_max(random_states(rng, 1)[0], q))
        trace_q = 2 * q.sum()
        gap = star(q) - trace_q - support_lower
        if best is None or gap > best[0]:
            best = (gap, q.copy(), star(q), trace_q, support_lower)
        line_gap = star(q) - trace_q - 2 * np.max(q)
        if best_line_envelope is None or line_gap > best_line_envelope[0]:
            best_line_envelope = (line_gap, q.copy(), star(q), trace_q)
    print("largest_candidate_gap_after_local_ascent", best[0])
    print("star", best[2], "traceQ", best[3], "support_lower", best[4])
    print("line_weights", [float(x) for x in best[1]])
    print("candidate_count", 700, "state_seeds", len(states))
    print("max_line_envelope_violation_sample", best_line_envelope[0])
    print("line_envelope_weights", [float(x) for x in best_line_envelope[1]])

if __name__ == "__main__":
    main()
