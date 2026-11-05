"""Independent dense-circuit and classical-operator checks for theorem.md.

NumPy only. Dense replay uses arbitrary explicit Clifford schedules, not an
assertion that shallow random gate strings sample Cliffords uniformly.
An independent finite group closure verifies exact two-qubit transitivity.
"""
import itertools
import json
import math
from collections import deque
from pathlib import Path

import numpy as np

PAULI = [np.eye(2, dtype=complex),
         np.array([[0, 1], [1, 0]], complex),
         np.array([[0, -1j], [1j, 0]], complex),
         np.diag([1, -1]).astype(complex)]
H = np.array([[1, 1], [1, -1]], complex) / math.sqrt(2)
S = np.diag([1, 1j])


def kron_all(xs):
    z = np.array([[1]], complex)
    for x in xs:
        z = np.kron(z, x)
    return z


def pauli(p):
    return kron_all([PAULI[a] for a in p])


def one(g, i, n):
    return kron_all([g if j == i else PAULI[0] for j in range(n)])


def permutation_gate(n, transform):
    out = np.zeros((2**n, 2**n), complex)
    for j in range(2**n):
        bits = [(j >> (n - 1 - k)) & 1 for k in range(n)]
        bb = transform(bits)
        ii = sum(x << (n - 1 - k) for k, x in enumerate(bb))
        out[ii, j] = 1
    return out


def cnot(c, t, n):
    def f(bits):
        bits[t] ^= bits[c]
        return bits
    return permutation_gate(n, f)


def swap(i, j, n):
    def f(bits):
        bits[i], bits[j] = bits[j], bits[i]
        return bits
    return permutation_gate(n, f)


def trace_first(x, dfirst, dsecond):
    return np.einsum('abad->bd', x.reshape(dfirst, dsecond, dfirst, dsecond))


def trace_second(x, dfirst, dsecond):
    return np.einsum('abcb->ac', x.reshape(dfirst, dsecond, dfirst, dsecond))


def labels(n):
    return list(itertools.product(range(4), repeat=n))


def pauli_action(C, ps):
    mats = [pauli(p) for p in ps]
    out = []
    for P in mats:
        q = C @ P @ C.conj().T
        vals = [abs(np.trace(Q @ q) / len(C)) for Q in mats]
        k = int(np.argmax(vals))
        assert abs(vals[k] - 1) < 1e-12
        out.append(k)
    return np.array(out, dtype=int)


def local_kernel(theta):
    s, c = math.sin(theta), math.cos(theta)
    K = np.zeros((4, 4))
    K[0, 0] = 1
    for a in range(1, 4):
        K[a, 0] = s**4
        for b in range(1, 4):
            K[a, b] = c**4 if a == b else c*c*s*s
    return K


def dense_case(n, cycles, theta, rng):
    m = n * cycles
    total = n + m
    ps = labels(n)
    source_dim, bath_dim = 2**n, 2**m
    W = np.eye(2**total, dtype=complex)
    cumulative_C = np.eye(source_dim, dtype=complex)
    actions = []
    for t in range(cycles):
        C = np.eye(source_dim, dtype=complex)
        for _ in range(4*n+3):
            k = int(rng.integers(n))
            typ = int(rng.integers(3 if n > 1 else 2))
            if typ == 0:
                G = one(H, k, n)
            elif typ == 1:
                G = one(S, k, n)
            else:
                kk = (k + int(rng.integers(1, n))) % n
                G = cnot(k, kk, n)
            C = G @ C
        actions.append(pauli_action(C, ps))
        cumulative_C = C @ cumulative_C
        W = np.kron(C, np.eye(bath_dim)) @ W
        for k in range(n):
            U = math.cos(theta)*np.eye(2**total) + 1j*math.sin(theta)*swap(k, n+n*t+k, total)
            W = U @ W

    K = kron_all([local_kernel(theta) for _ in range(n)]).real
    dense_B, source_B, q_classical, predicted_t = [], [], [], []
    max_decoder_resid = 0.0
    for mu in (1, 2, 3):
        p0 = (mu,) + (0,)*(n-1)
        P0 = pauli(p0)
        evolved = W @ np.kron(P0, np.eye(bath_dim)) @ W.conj().T
        B = trace_first(evolved, source_dim, bath_dim) / source_dim
        dense_B.append(B)
        source_B.append(trace_second(evolved, source_dim, bath_dim)/bath_dim)
        prob = np.zeros(4**n)
        prob[ps.index(p0)] = 1
        label = ps.index(p0)
        amplitude = 1.0
        for action in actions:
            pp = np.zeros_like(prob)
            pp[action] = prob
            prob = pp @ K
            label = int(action[label])
            amplitude *= math.cos(theta)**(2*sum(a != 0 for a in ps[label]))
        q_classical.append(1-prob[0])
        predicted_t.append(amplitude)
        gamma_sigma = 2 * B/bath_dim
        recovered_all = W.conj().T @ np.kron(np.eye(source_dim)/source_dim, gamma_sigma) @ W
        recovered_source = trace_second(recovered_all, source_dim, bath_dim)
        recovered_qubit = trace_second(recovered_source, 2, 2**(n-1))
        expected = prob[0] * PAULI[mu]
        max_decoder_resid = max(max_decoder_resid, float(np.linalg.norm(recovered_qubit-expected)))

    gram = np.array([[np.trace(B @ C).real/bath_dim for C in dense_B] for B in dense_B])
    expect_gram = np.diag(1-np.array(q_classical))
    delta_choi = sum(np.kron(PAULI[mu].T, source_B[mu-1]) for mu in (1,2,3))/(2*source_dim)
    source_trace_distance = float(np.linalg.eigvalsh(delta_choi).astype(float).__abs__().sum()/2)
    expected_source = max(sum(predicted_t)/4, max(predicted_t)/2)
    return dict(n=n, cycles=cycles, theta=theta,
                gram_residual=float(np.max(np.abs(gram-expect_gram))),
                decoder_residual=max_decoder_resid,
                source_choi_residual=abs(source_trace_distance-expected_source),
                carrier_gram_diagonal=np.diag(gram).tolist(),
                source_distance=source_trace_distance)


def two_qubit_group():
    ps = labels(2)
    gens = [one(H,0,2),one(H,1,2),one(S,0,2),one(S,1,2),cnot(0,1,2),cnot(1,0,2)]
    perms = [pauli_action(g, ps) for g in gens]
    initial = tuple(range(16))
    seen, queue = {initial}, deque([initial])
    while queue:
        p = np.array(queue.popleft())
        for g in perms:
            nxt = tuple(g[p].tolist())
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    assert len(seen) == 720
    hist = np.zeros((16, 16), dtype=int)
    for p in seen:
        hist[np.arange(16),p] += 1
    assert hist[0,0] == 720
    assert np.all(hist[1:,1:] == 48)
    return len(seen), hist


def ensemble_check():
    order, hist = two_qubit_group()
    out=[]
    for theta in (.13,.4,math.pi/4,1.2):
        K = np.kron(local_kernel(theta),local_kernel(theta))
        transfer = (hist/order) @ K
        for cycles in (1,2,7,19):
            pp=np.zeros(16);pp[4]=1
            pp=pp @ np.linalg.matrix_power(transfer,cycles)
            kap=((1+3*math.sin(theta)**4)**2-1)/15
            out.append(abs((1-pp[0])-(1-kap)**cycles))
    return dict(projective_two_qubit_symplectic_order=order,
                maximum_transitivity_recurrence_residual=max(out))


def acquisition_table():
    rows=[]
    epsilon=.01
    alpha=4*epsilon/3
    for n in (1,5,10,20,50):
        kap=((7/4)**n-1)/(4**n-1)
        eta=((5/2)**n-1)/(4**n-1)
        denom=-math.log1p(-kap)
        lower=math.ceil(math.log(1/(2*alpha-alpha*alpha))/denom)
        upper=math.ceil(math.log(1/alpha)/denom)
        rows.append(dict(n=n,theta="pi/4",target_error=epsilon,kappa=kap,
                         source_one_cycle_upper=1.5*eta,
                         necessary_cycles=lower,sufficient_cycles=upper,
                         stored_carriers=n*upper))
    return rows


def main():
    rng=np.random.default_rng(20261105)
    cases=[]
    for n,cycles in ((1,1),(1,3),(2,1),(2,2),(3,1)):
        for theta in (.19,.61,1.1):
            cases.append(dense_case(n,cycles,theta,rng))
    maxres=max(max(c[k] for c in cases) for k in ('gram_residual','decoder_residual','source_choi_residual'))
    assert maxres < 2e-11
    result=dict(dense_cases=cases,max_dense_residual=maxres,ensemble=ensemble_check(),table=acquisition_table())
    Path(__file__).with_name('verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
