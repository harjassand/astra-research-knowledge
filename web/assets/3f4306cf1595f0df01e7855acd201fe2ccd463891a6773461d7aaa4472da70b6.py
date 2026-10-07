"""Small, bounded diagnostic of the explicit permutation-commutant SDP.

The compiler representation never enumerates physical basis vectors.  This
fixture DOES enumerate at d=2,N<=3, and d=3,N=2 solely to check the formulas.
Its Newton/log-det solver is floating point and is NOT a certified Turing SDP
implementation.  The proof imports that implementation separately.
Run with OPENBLAS_NUM_THREADS=1; owned JSON output only.
"""
from __future__ import annotations

import itertools
import json
import math
import pathlib
import time

import numpy as np


def compositions(n: int, q: int):
    if q == 1:
        yield (n,)
        return
    for k in range(n + 1):
        for tail in compositions(n - k, q - 1):
            yield (k,) + tail


class OrbitAlgebra:
    def __init__(self, d: int, n: int):
        self.d, self.n = d, n
        self.ms = list(compositions(n, d * d))
        self.index = {m: i for i, m in enumerate(self.ms)}
        self.dim = len(self.ms)
        fact = [math.factorial(i) for i in range(n + 1)]
        self.gram = np.array(
            [fact[n] // math.prod(fact[k] for k in m) for m in self.ms],
            dtype=np.float64,
        )
        self.trace = np.zeros(self.dim)
        self.unit = np.zeros(self.dim, dtype=np.complex128)
        for j, m in enumerate(self.ms):
            if all(m[a * d + b] == 0 for a in range(d) for b in range(d) if a != b):
                self.trace[j] = self.gram[j]
                self.unit[j] = 1

        # All structure constants are acquired by triple counts, not by
        # permutations or a matrix of dimension d**n.
        self.left = np.zeros((self.dim, self.dim, self.dim), dtype=np.int64)
        for t in compositions(n, d**3):
            m, k, p = [0] * (d * d), [0] * (d * d), [0] * (d * d)
            for a, b, c in itertools.product(range(d), repeat=3):
                v = t[(a * d + b) * d + c]
                m[a * d + b] += v
                k[b * d + c] += v
                p[a * d + c] += v
            numerator = math.prod(fact[v] for v in p)
            denominator = math.prod(fact[v] for v in t)
            assert numerator % denominator == 0
            self.left[self.index[tuple(m)], self.index[tuple(p)], self.index[tuple(k)]] += numerator // denominator

        h = []
        seen = set()
        for j, m in enumerate(self.ms):
            if j in seen:
                continue
            mt = tuple(m[b * d + a] for a in range(d) for b in range(d))
            k = self.index[mt]
            seen.update((j, k))
            re = np.zeros(self.dim, dtype=np.complex128)
            re[j] = 1
            if j == k:
                h.append(re)
            else:
                re[k] = 1
                im = np.zeros(self.dim, dtype=np.complex128)
                im[j], im[k] = 1j, -1j
                h.extend((re, im))
        self.hermitian_coordinates = np.array(h)
        assert len(h) == self.dim
        self.hermitian_left = np.array([self.regular(c) for c in h])
        self.hermitian_trace = np.real(self.hermitian_coordinates @ self.trace)

    def left_matrix(self, coefficients):
        return np.einsum("m,mpq->pq", coefficients, self.left, optimize=True)

    def regular(self, coefficients):
        # Square roots occur ONLY in the numerical fixture.  The rational
        # theorem uses G L_X >=0, with diagonal integer G instead.
        l = self.left_matrix(coefficients)
        return l * np.sqrt(self.gram[:, None] / self.gram[None, :])

    def collective_coefficients(self, t):
        d = self.d
        ans = np.zeros(self.dim, dtype=np.complex128)
        for j, m in enumerate(self.ms):
            off = [(a, b, m[a * d + b]) for a in range(d) for b in range(d) if a != b and m[a * d + b]]
            if not off:
                ans[j] = sum(m[a * d + a] * t[a, a] for a in range(d))
            elif len(off) == 1 and off[0][2] == 1:
                a, b, _ = off[0]
                ans[j] = t[a, b]
        return ans

    def product_coefficients(self, state):
        entries = np.asarray(state).reshape(-1)
        return np.array([math.prod(entries[a] ** m[a] for a in range(self.d**2)) for m in self.ms])

    def gibbs_coefficients(self, k):
        khat = self.regular(k)
        assert np.max(np.abs(khat - khat.conj().T)) < 2e-12
        values, vectors = np.linalg.eigh(khat)
        scaled = vectors @ ((np.exp(values - values.max()))[:, None] * vectors.conj().T)
        coef = (scaled @ (np.sqrt(self.gram) * self.unit)) / np.sqrt(self.gram)
        return coef / np.dot(self.trace, coef)

    def tiny_physical_basis(self):
        # Verification only.  Forbidden as the scalable compiler method.
        words = list(itertools.product(range(self.d), repeat=self.n))
        result = np.zeros((self.dim, len(words), len(words)), dtype=np.int64)
        for a, u in enumerate(words):
            for b, v in enumerate(words):
                m = [0] * (self.d**2)
                for x, y in zip(u, v):
                    m[x * self.d + y] += 1
                result[self.index[tuple(m)], a, b] = 1
        return result


def trace_distance(x, y):
    return float(np.abs(np.linalg.eigvalsh((x - y + (x - y).conj().T) / 2)).sum() / 2)


def newton_sdp(algebra, target, nodes, final_mu=1e-6):
    """Solve the actual orbit-algebra trace-norm SDP by a small log barrier.

    P=Q+target-sum_j w_j S_j, Q>=0, P>=0, w simplex.
    Since all states have trace one, objective is the PHYSICAL trace(Q).
    """
    D, M = algebra.dim, len(nodes)
    hs = algebra.hermitian_left
    node_coef = np.array([algebra.product_coefficients(x) for x in nodes])
    ss = np.array([algebra.regular(c) for c in node_coef])
    rr = algebra.regular(target)
    nv = D + M - 1
    aq = np.zeros((nv, D, D), dtype=np.complex128)
    ap = np.zeros_like(aq)
    aq[:D] = hs
    ap[:D] = hs
    ap[D:] = -(ss[:-1] - ss[-1])
    c = np.concatenate((algebra.hermitian_trace, np.zeros(M - 1)))
    jac = np.concatenate((np.eye(M - 1), -np.ones((1, M - 1))), axis=0)
    weights = np.full(M, 1 / M)
    delta = target - weights @ node_coef
    qcoef = 2 * algebra.unit - delta / 2
    qx = np.linalg.solve(algebra.hermitian_coordinates.T, qcoef).real
    x = np.concatenate((qx, weights[:-1]))
    iterations = 0
    mus = [10.0**(-j) for j in range(7)]
    mus = [z for z in mus if z >= final_mu]
    if mus[-1] != final_mu:
        mus.append(final_mu)

    def evaluate(z, mu, derivatives=False):
        w = np.concatenate((z[D:], [1 - z[D:].sum()]))
        if w.min() <= 0:
            return None
        q = np.einsum("a,aij->ij", z[:D], hs)
        p = q + rr - np.einsum("a,aij->ij", w, ss)
        q = (q + q.conj().T) / 2
        p = (p + p.conj().T) / 2
        try:
            cq, cp = np.linalg.cholesky(q), np.linalg.cholesky(p)
        except np.linalg.LinAlgError:
            return None
        logs = 2 * np.log(np.diag(cq).real).sum() + 2 * np.log(np.diag(cp).real).sum() + np.log(w).sum()
        f = float(c @ z - mu * logs)
        if not derivatives:
            return f
        qi, pi = np.linalg.inv(q), np.linalg.inv(p)
        vq = np.einsum("ij,ajk->aik", qi, aq)
        vp = np.einsum("ij,ajk->aik", pi, ap)
        grad = c - mu * (np.trace(vq, axis1=1, axis2=2).real + np.trace(vp, axis1=1, axis2=2).real)
        grad[D:] -= mu * (jac.T @ (1 / w))
        hess = mu * (np.einsum("aij,bji->ab", vq, vq).real + np.einsum("aij,bji->ab", vp, vp).real)
        hess[D:, D:] += mu * (jac.T @ ((1 / w**2)[:, None] * jac))
        return f, grad, (hess + hess.T) / 2

    for mu in mus:
        for _ in range(70):
            iterations += 1
            f, grad, hess = evaluate(x, mu, True)
            try:
                step = -np.linalg.solve(hess, grad)
            except np.linalg.LinAlgError:
                step = -np.linalg.lstsq(hess, grad, rcond=1e-14)[0]
            decrement = -float(grad @ step)
            if decrement < 2e-11:
                break
            rate = 1.0
            accepted = False
            for _ in range(65):
                candidate = x + rate * step
                fc = evaluate(candidate, mu)
                if fc is not None and fc <= f + 0.02 * rate * float(grad @ step):
                    x, accepted = candidate, True
                    break
                rate /= 2
            if not accepted:
                break
    w = np.concatenate((x[D:], [1 - x[D:].sum()]))
    qcoef = x[:D] @ algebra.hermitian_coordinates
    pcoef = qcoef + target - w @ node_coef
    f, grad, _ = evaluate(x, mus[-1], True)
    return {
        "weights": w,
        "mixture_coefficients": w @ node_coef,
        "objective": float(c @ x),
        "minimum_regular_P_eigenvalue": float(np.linalg.eigvalsh(algebra.regular(pcoef)).min()),
        "minimum_regular_Q_eigenvalue": float(np.linalg.eigvalsh(algebra.regular(qcoef)).min()),
        "final_mu": mus[-1],
        "nominal_barrier_gap": (2 * D + M) * mus[-1],
        "stationarity_norm": float(np.linalg.norm(grad)),
        "iterations": iterations,
        "floating_point_only": True,
    }


def algebra_checks(d, n):
    a = OrbitAlgebra(d, n)
    bs = a.tiny_physical_basis()
    pairs = 0
    for m in range(a.dim):
        for k in range(a.dim):
            actual = bs[m] @ bs[k]
            predicted = np.einsum("p,pij->ij", a.left[m, :, k], bs)
            assert np.array_equal(actual, predicted)
            pairs += 1
    traces = np.trace(bs, axis1=1, axis2=2)
    grams = np.einsum("mij,mij->m", bs, bs)
    assert np.array_equal(traces, a.trace)
    assert np.array_equal(grams, a.gram)
    rng = np.random.default_rng(771 + d + n)
    worst = 0.0
    for _ in range(8):
        coeff = rng.normal(size=a.dim) @ a.hermitian_coordinates
        x = np.einsum("m,mij->ij", coeff, bs)
        physical_min = np.linalg.eigvalsh(x).min()
        regular_min = np.linalg.eigvalsh(a.regular(coeff)).min()
        worst = max(worst, abs(physical_min - regular_min))
        assert abs(physical_min - regular_min) < 3e-12
    collective_error = 0.0
    for row, col in itertools.product(range(d), repeat=2):
        t = np.zeros((d, d), dtype=np.complex128)
        t[row, col] = 1
        lt = a.left_matrix(a.collective_coefficients(t))
        explicit = np.zeros_like(lt)
        for j, m in enumerate(a.ms):
            if row == col:
                explicit[j, j] = sum(m[row * d + z] for z in range(d))
            else:
                for z in range(d):
                    if m[col * d + z]:
                        p = list(m)
                        p[col * d + z] -= 1
                        p[row * d + z] += 1
                        explicit[a.index[tuple(p)], j] += m[row * d + z] + 1
        collective_error = max(collective_error, float(np.abs(lt - explicit).max()))
    assert collective_error == 0
    return {
        "d": d, "N": n, "commutant_dimension": a.dim,
        "expected_dimension": math.comb(n + d * d - 1, d * d - 1),
        "exact_integer_product_pairs": pairs,
        "exact_trace_and_gram": True,
        "minimum_eigenvalue_worst_error": worst,
        "collective_action_exact_error": collective_error,
    }


def spin_fixture(sign):
    a = OrbitAlgebra(2, 3)
    bs = a.tiny_physical_basis()
    paulis = [np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.diag([1, -1])]
    js = [a.collective_coefficients(p / 2) for p in paulis]
    k = sum(a.left_matrix(j) @ j for j in js) * sign / 3
    target = a.gibbs_coefficients(k)
    kphys = np.einsum("m,mij->ij", k, bs)
    val, vec = np.linalg.eigh(kphys)
    target_physical = vec @ ((np.exp(val) / np.exp(val).sum())[:, None] * vec.conj().T)
    represented = np.einsum("m,mij->ij", target, bs)
    assert np.abs(represented - target_physical).max() < 2e-13
    half = np.eye(2) / 2
    nodes = [half] + [(np.eye(2) + s * p) / 2 for p in paulis for s in [-1, 1]]
    result = newton_sdp(a, target, nodes)
    mix = np.einsum("m,mij->ij", result.pop("mixture_coefficients"), bs)
    error = trace_distance(target_physical, mix)
    weights = result.pop("weights")
    if sign > 0:
        exact_optimum = 0.0
        p = (math.e - 1) / (math.e + 1)
        exact_weights = np.array([1 - p] + [p / 6] * 6)
    else:
        exact_optimum = (math.e - 1) / (2 * (math.e + 1))
        exact_weights = np.array([1.0] + [0.0] * 6)
    exact_mix = np.einsum("m,mij->ij", exact_weights @ np.array([a.product_coefficients(s) for s in nodes]), bs)
    assert abs(trace_distance(target_physical, exact_mix) - exact_optimum) < 3e-13
    assert result["minimum_regular_P_eigenvalue"] > -1e-9
    assert result["minimum_regular_Q_eigenvalue"] > -1e-9
    assert weights.min() > -1e-12 and abs(weights.sum() - 1) < 1e-12
    assert abs(error - exact_optimum) < 3e-4
    assert result["objective"] + 1e-9 >= error
    assert abs(result["objective"] - exact_optimum) < 3e-4
    result.update({
        "d": 2, "N": 3, "beta_sign": sign,
        "commutant_dimension": a.dim,
        "physical_dimension_in_verifier_only": 8,
        "nodes": "I/2 and the six pure Pauli eigenstates",
        "weights": weights.tolist(),
        "physical_trace_distance": error,
        "analytically_proved_optimum": exact_optimum,
        "analytic_weights_max_error": float(np.abs(weights - exact_weights).max()),
        "gibbs_compressed_vs_tiny_physical_error": float(np.abs(represented - target_physical).max()),
        "isotropic_ferromagnet_source_admitted": sign > 0,
        "antiferromagnetic_negative_control": sign < 0,
    })
    return result


def main():
    start = time.monotonic()
    checks = [algebra_checks(2, 2), algebra_checks(2, 3), algebra_checks(3, 2)]
    fixtures = [spin_fixture(1), spin_fixture(-1)]
    result = {
        "status": "PASS",
        "scope": "exact small orbit structure/trace checks and floating SDP fixtures; no general certified solver or physical preparation execution",
        "algebra_checks": checks,
        "SDP_fixtures": fixtures,
        "elapsed_seconds": time.monotonic() - start,
        "numpy_version": np.__version__,
    }
    output = pathlib.Path(__file__).with_name("commutant_compiler_checks.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "elapsed_seconds": result["elapsed_seconds"], "exact_product_pairs": sum(c["exact_integer_product_pairs"] for c in checks), "fixture_errors": [f["physical_trace_distance"] for f in fixtures], "owned_output": str(output)}, indent=2))


if __name__ == "__main__":
    main()
