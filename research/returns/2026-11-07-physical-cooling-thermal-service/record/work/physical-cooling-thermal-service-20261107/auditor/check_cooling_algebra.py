"""Finite algebra checks, not an asymptotic/hardware validation."""
from pathlib import Path
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parent
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
PAULIS = dict(I=I, X=X, Y=Y, Z=Z)


def kron_all(seq):
    result = np.ones((1, 1), dtype=complex)
    for item in seq:
        result = np.kron(result, item)
    return result


def pauli(word):
    return kron_all([PAULIS[c] for c in word])


def trace_norm(a):
    return float(np.abs(np.linalg.eigvalsh((a + a.conj().T) / 2)).sum())


def unitary(h, t):
    vals, vecs = np.linalg.eigh(h)
    return (vecs * np.exp(-1j * t * vals)) @ vecs.conj().T


def choi(channel, dim):
    result = np.zeros((dim * dim, dim * dim), dtype=complex)
    for j in range(dim):
        for k in range(dim):
            e = np.zeros((dim, dim), dtype=complex)
            e[j, k] = 1
            result[j * dim:(j + 1) * dim,
                   k * dim:(k + 1) * dim] = channel(e) / dim
    return result


def collision_check():
    q = 0.073
    tau = np.diag([1 - q, q])
    lower = np.array([[0, 1], [0, 0]], dtype=complex)
    v = np.kron(lower, lower.conj().T) + np.kron(lower.conj().T, lower)
    n = np.diag([0, 1])
    h0 = np.kron(n, I) + np.kron(I, n)
    errors = []
    for angle in [0.13, 0.78, math.pi / 2]:
        u = unitary(v, angle)
        def channel(rho):
            joint = u @ np.kron(rho, tau) @ u.conj().T
            return np.trace(joint.reshape(2, 2, 2, 2), axis1=1, axis2=3)
        for s in [0.1, 0.7, 1.3]:
            weighted = np.diag([1, np.exp(s)])
            # Reconstruct dual using matrix units.
            dual = np.zeros((2, 2), dtype=complex)
            for j in range(2):
                for k in range(2):
                    e = np.zeros((2, 2), dtype=complex)
                    e[j, k] = 1
                    dual[k, j] = np.trace(weighted @ channel(e))
            t = math.sin(angle) ** 2
            expected = np.diag([
                1 + q * t * (np.exp(s) - 1),
                np.exp(s) * (1 + (1 - q) * t * (np.exp(-s) - 1))])
            errors.append(float(np.max(np.abs(dual - expected))))
        errors.append(float(np.max(np.abs(channel(tau) - tau))))
    return dict(max_residual=max(errors), energy_commutator=float(np.max(np.abs(h0 @ v - v @ h0))))


def correlated_thermal_counterexample():
    stabs = [pauli(s) for s in ['XZZXI', 'IXZZX', 'XIXZZ', 'ZXIXZ']]
    ident = np.eye(32, dtype=complex)
    projector = ident.copy()
    for s in stabs:
        projector = projector @ ((ident + s) / 2)
    logical_z = pauli('ZZZZZ')
    logical_x = pauli('XXXXX')
    initial = np.zeros(32, dtype=complex)
    initial[0] = 1
    zero_l = projector @ ((ident + logical_z) / 2) @ initial
    zero_l /= np.linalg.norm(zero_l)
    one_l = logical_x @ zero_l
    bell = (np.kron(zero_l, [1, 0]) + np.kron(one_l, [0, 1])) / math.sqrt(2)
    rho = np.outer(bell, bell.conj())
    lx = np.kron(logical_x, I)
    p = 0.017
    actual = (1 - p) * rho + p * lx @ rho @ lx
    h = sum((ident - s) / 2 for s in stabs)
    return dict(p=p, half_trace_error=trace_norm(actual - rho) / 2,
                code_energy=float(np.trace(np.kron(h, I) @ actual).real),
                max_ancilla_marginal_error=0.0,
                all_subset_fault_probability=p,
                falsely_inferred_independent_probability=p ** 5)


def wh_counterexample():
    results = []
    for dim in [2, 4, 8]:
        def plus(a):
            return (np.trace(a) * np.eye(dim) + a.T) / (dim + 1)
        def minus(a):
            return (np.trace(a) * np.eye(dim) - a.T) / (dim - 1)
        e00 = np.zeros((dim, dim), dtype=complex)
        e00[0, 0] = 1
        results.append(dict(dim=dim,
                            pure_output_norm=trace_norm(plus(e00) - minus(e00)),
                            pure_formula=4 / (dim + 1),
                            reference_norm=trace_norm(choi(plus, dim) - choi(minus, dim))))
    return results


def minorization_check():
    tau = np.diag([0.89, 0.11])
    u = unitary(X, 0.0002)
    tau_actual = u @ tau @ u.conj().T
    epsilon = trace_norm(tau_actual - tau)
    p = 2 * epsilon / 0.11
    residual = np.kron(I / 2, tau_actual - (1 - p) * tau)
    return dict(epsilon=epsilon, p_bound=p,
                residual_choi_min=float(np.linalg.eigvalsh(residual).min()),
                residual_trace=float(np.trace(residual).real))


def thermal_pair_check():
    n = np.diag([0, 1]).astype(complex)
    lower = np.array([[0, 1], [0, 0]], dtype=complex)
    v = np.kron(lower, lower.conj().T) + np.kron(lower.conj().T, lower)
    beta, gap, h = 3.1, 1.7, 0.4
    h_pair = gap * (np.kron(n, I) + np.kron(I, n)) + h * v
    vals, vecs = np.linalg.eigh(h_pair)
    omega = (vecs * np.exp(-beta * vals)) @ vecs.conj().T
    omega /= np.trace(omega)
    z = 1 + 2 * np.exp(-beta * gap) * np.cosh(beta * h) + np.exp(-2 * beta * gap)
    p_bad = 1 - 1 / z
    p_bound = 3 * np.exp(-beta * (gap - abs(h)))
    token = np.trace(omega.reshape(2, 2, 2, 2), axis1=1, axis2=3)
    token_formula = (np.exp(-2 * beta * gap) + np.exp(-beta * gap) * np.cosh(beta * h)) / z
    work = -h * np.trace(v @ omega).real
    work_formula = 2 * h * np.exp(-beta * gap) * np.sinh(beta * h) / z
    waiting = unitary(h_pair, 12345.0)
    tau = np.diag([1, np.exp(-beta * gap)]) / (1 + np.exp(-beta * gap))
    product = np.kron(tau, tau)
    return dict(p_bad=p_bad, p_bound=p_bound,
                stationary_residual=float(np.max(np.abs(waiting @ omega @ waiting.conj().T - omega))),
                token_formula_residual=float(abs(token[1, 1] - token_formula)),
                work_formula_residual=float(abs(work - work_formula)),
                work=work,
                product_stationarity=float(np.max(np.abs(h_pair @ product - product @ h_pair))),
                product_vs_interacting_gibbs=trace_norm(product - omega))


def sweep_check():
    stab_words = ['XZZXI', 'IXZZX', 'XIXZZ', 'ZXIXZ']
    def anticommutes(a, b):
        return sum(x != y and x != 'I' and y != 'I' for x, y in zip(a, b)) % 2
    moves = []
    for j in range(5):
        for p in ['X', 'Y', 'Z']:
            word = 'I' * j + p + 'I' * (4 - j)
            moves.append(sum(anticommutes(word, s) << k for k, s in enumerate(stab_words)))
    labels = [(move, d) for move in moves for d in range(1, 5)]
    def energy(sigma):
        return sigma.bit_count()
    def active(sigma, label):
        move, d = label
        return energy(sigma ^ move) - energy(sigma) == -d
    kappa = min(sum(active(sigma, label) for label in labels) / energy(sigma)
                for sigma in range(1, 16))
    r0 = max(sum(active(sigma, label) != active(sigma ^ move, label)
                 for label in labels) for sigma in range(16) for move in moves)
    a = min(0.5, kappa / (r0 + 1))
    cases = []
    for sigma in range(16):
        current = sigma
        successes = 0
        active_start = sum(active(sigma, label) for label in labels)
        for label in labels:
            if active(current, label):
                current ^= label[0]
                successes += 1
        assert active_start <= (r0 + 1) * successes
        assert energy(current) <= (1 - a) * energy(sigma) + 1e-12
        cases.append(dict(start=sigma, u_start=energy(sigma), u_end=energy(current), successes=successes))
    return dict(kappa=kappa, predicate_overlap=r0, a=a, cases=cases)


out = dict(collision=collision_check(), correlated_ancilla=correlated_thermal_counterexample(),
           state_channel=wh_counterexample(), refresh_minorization=minorization_check(),
           finite_sweep=sweep_check(), thermal_pair=thermal_pair_check(),
           scope='finite algebra only; no actual-code asymptotic, bath-renewal, hardware or advantage certification')
assert out['collision']['max_residual'] < 1e-12
assert out['collision']['energy_commutator'] < 1e-12
assert abs(out['correlated_ancilla']['half_trace_error'] - out['correlated_ancilla']['p']) < 1e-12
assert abs(out['correlated_ancilla']['code_energy']) < 1e-12
assert out['refresh_minorization']['residual_choi_min'] >= -1e-12
assert out['thermal_pair']['p_bad'] <= out['thermal_pair']['p_bound']
for key in ['stationary_residual', 'token_formula_residual', 'work_formula_residual', 'product_stationarity']:
    assert out['thermal_pair'][key] < 1e-12
for item in out['state_channel']:
    assert abs(item['pure_output_norm'] - item['pure_formula']) < 1e-12
    assert abs(item['reference_norm'] - 2) < 1e-12
(ROOT / 'cooling_algebra_checks.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({key: value for key, value in out.items() if key != 'finite_sweep'}, indent=2))
print('Finite sweep cases:', len(out['finite_sweep']['cases']), 'all passed')
