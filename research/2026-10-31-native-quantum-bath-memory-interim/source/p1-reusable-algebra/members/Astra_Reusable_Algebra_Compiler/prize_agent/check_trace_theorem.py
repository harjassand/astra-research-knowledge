"""Independent numerical checks of the saturation/concentration proof.

This script does not establish historical novelty or finite-precision correctness
of arbitrary algebra decomposition. It checks the Gaussian degrees, module rank,
all-positive-cone error, and confidence inversion on small generated examples.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def cg(rng, shape):
    return (rng.normal(size=shape) + 1j * rng.normal(size=shape)) / np.sqrt(2)


def herm(rng, n):
    a = cg(rng, (n, n))
    return (a + a.conj().T) / 2


def block_diag(blocks):
    n = sum(a.shape[0] for a in blocks)
    out = np.zeros((n, n), complex)
    offset = 0
    for a in blocks:
        k = a.shape[0]
        out[offset:offset+k, offset:offset+k] = a
        offset += k
    return out


def spinup(generators, seeds, tol=1e-10):
    vectors = []

    def add(v):
        v = np.array(v, copy=True)
        for _ in range(2):
            for u in vectors:
                v -= u * np.vdot(u, v)
        norm = np.linalg.norm(v)
        if norm > tol:
            vectors.append(v / norm)
            return True
        return False

    for g in seeds.T:
        add(g)
    cursor = 0
    calls = 0
    while cursor < len(vectors):
        u = vectors[cursor]
        for a in generators:
            calls += 1
            add(a @ u)
        cursor += 1
    q = np.column_stack(vectors)
    return q, calls


def acquire_algebra_basis(generators, tol=1e-9):
    k = generators[0].shape[0]
    basis = []

    def add(b):
        b = b.copy()
        for _ in range(2):
            for c in basis:
                b -= c * np.vdot(c, b)
        norm = np.linalg.norm(b)
        if norm > tol:
            basis.append(b / norm)

    add(np.eye(k, dtype=complex))
    cursor = 0
    while cursor < len(basis):
        b = basis[cursor]
        for a in generators:
            add(a @ b)
        cursor += 1
    return basis


def nullspace(a, tol=1e-8):
    _, s, vh = np.linalg.svd(a, full_matrices=True)
    rank = np.sum(s > tol)
    return vh.conj().T[:, rank:]


def cluster_eigenvalues(vals, tol=1e-6):
    groups = []
    for j, value in enumerate(vals):
        if not groups or abs(value - vals[groups[-1][0]]) > tol:
            groups.append([j])
        else:
            groups[-1].append(j)
    return groups


def decompose_center(generators, rng):
    """Discover simple-block sizes from the reduced matrices, no hidden labels."""
    basis = acquire_algebra_basis(generators)
    commutators = np.column_stack([
        np.concatenate([(a @ b - b @ a).ravel() for a in generators])
        for b in basis
    ])
    center_coeffs = nullspace(commutators)
    centers = []
    for c in center_coeffs.T:
        z = sum(ci * b for ci, b in zip(c, basis))
        centers.extend([(z + z.conj().T) / 2,
                        (z - z.conj().T) / (2j)])
    z = sum(w * c for w, c in zip(rng.normal(size=len(centers)), centers))
    vals, vecs = np.linalg.eigh(z)
    result = []
    for indices in cluster_eigenvalues(vals):
        u = vecs[:, indices]
        # Dimension of the restricted algebra is r_alpha squared.
        restricted = np.column_stack([(u.conj().T @ b @ u).ravel() for b in basis])
        da = np.linalg.matrix_rank(restricted, tol=1e-8)
        r = int(round(np.sqrt(da)))
        assert r*r == da
        assert len(indices) % r == 0
        s = len(indices)//r
        result.append((r, s, u))
    return result


def shape_interval(w, t):
    lo = max(0.0, np.sqrt(max(w-t/2, 0.0))-np.sqrt(t/2))**2
    hi = (np.sqrt(w+t/2)+np.sqrt(t/2))**2
    return lo, hi


def run():
    rng = np.random.default_rng(20261031)
    cases = [
        (1, [(2, 1), (2, 2), (3, 6)]),
        (2, [(2, 3), (2, 4), (2, 7)]),
        (3, [(1, 2), (1, 3), (1, 10)]),
    ]
    rows = []
    for q, structure in cases:
        n = sum(r*m for r,m in structure)
        generators = []
        # Distinct generic simple blocks; not supplied to acquisition.
        for _ in range(2):
            generators.append(block_diag([
                np.kron(herm(rng, r), np.eye(m)) for r,m in structure
            ]))
        u, _ = np.linalg.qr(cg(rng, (n,n)))
        generators = [u @ a @ u.conj().T for a in generators]
        seeds = cg(rng, (n,q))
        Q, calls = spinup(generators, seeds)
        reduced = [Q.conj().T @ a @ Q for a in generators]
        learned = decompose_center(reduced, rng)
        expected = sorted((r, min(m,q*r)) for r,m in structure)
        observed = sorted((r,s) for r,s,_ in learned)
        assert expected == observed, (expected, observed)
        expected_k = sum(r*min(m,q*r) for r,m in structure)
        assert Q.shape[1] == expected_k
        assert calls == len(generators)*expected_k
        invariance = max(np.linalg.norm(a@Q-Q@(Q.conj().T@a@Q)) for a in generators)
        # Match central blocks only for test ground truth and compare weights.
        true_projectors = []
        offset = 0
        for r,m in structure:
            ua = u[:, offset:offset+r*m]
            true_projectors.append(ua@ua.conj().T)
            offset += r*m
        weights = []
        for r,s,ua in learned:
            ambient_projector_on_K = Q@ua@ua.conj().T@Q.conj().T
            overlap = [np.trace(ambient_projector_on_K@p).real for p in true_projectors]
            index = int(np.argmax(overlap))
            rt, m = structure[index]
            assert rt == r
            w = np.linalg.norm(ua.conj().T@Q.conj().T@seeds, 'fro')**2
            mhat = s if s < q*r else w/(q*r)
            if s < q*r:
                assert mhat == m
            weights.append({'r':r,'m':m,'s':s,'resolved':s<q*r,
                            'mhat':float(mhat),'relative_error':float(abs(mhat/m-1))})
        rows.append({'n':n,'q':q,'k':expected_k,'calls':calls,
                     'learned_structure':observed,'invariance_residual':float(invariance),
                     'weights':weights,
                     'all_PSD_relative_error':max(w['relative_error'] for w in weights)})

    # Directly test simultaneous gamma confidence intervals at multiple shapes.
    # This is numerical evidence only; the proof is algebraic/Chernoff.
    t = np.log(200.0)
    interval_rows=[]
    for shape in [1, 2, 4, 10, 100, 10000]:
        w = rng.gamma(shape=shape, size=100000)
        lo = np.maximum(0, np.sqrt(np.maximum(w-t/2,0))-np.sqrt(t/2))**2
        hi = (np.sqrt(w+t/2)+np.sqrt(t/2))**2
        failure = np.mean((shape<lo)|(shape>hi))
        interval_rows.append({'shape':shape,'observed_failure':float(failure),
                              'proved_upper_bound':float(2*np.exp(-t))})
    report={'module_checks':rows,'gamma_interval_checks':interval_rows}
    out=Path(__file__).with_name('trace_checks.json')
    out.write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    run()
