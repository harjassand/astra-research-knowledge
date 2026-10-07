"""Finite diagnostics for the written robust-numerics derivations.

The assertions verify conventions and finite formulas, not universal theorems.
Requires NumPy. Outputs only this scout's JSON artifact.
"""
from pathlib import Path
import json
import math
import numpy as np


def annihilators(n):
    result = []
    for j in range(n):
        a = np.zeros((2**n, 2**n), complex)
        for z in range(2**n):
            if (z >> j) & 1:
                sign = (-1) ** ((z & ((1 << j) - 1)).bit_count())
                a[z ^ (1 << j), z] = sign
        result.append(a)
    return result


def quadratic(a, cs):
    result = np.zeros_like(cs[0])
    for i in range(len(cs)):
        for j in range(len(cs)):
            result += a[i, j] * cs[i].conj().T @ cs[j]
    return result


def density(cov, cs):
    eig, basis = np.linalg.eigh(cov)
    k = (basis * np.log((1 - eig) / eig)) @ basis.conj().T
    eig_h, basis_h = np.linalg.eigh(quadratic(k, cs))
    weights = np.exp(-eig_h - np.max(-eig_h))
    weights /= weights.sum()
    return (basis_h * weights) @ basis_h.conj().T


def grid_boundary(n):
    edges = []
    for y in range(n + 1):
        for x in range(n):
            edges.append(((x, y), (x + 1, y)))
    for y in range(n):
        for x in range(n + 1):
            edges.append(((x, y), (x, y + 1)))
    lookup = {e: i for i, e in enumerate(edges)}
    boundary = np.zeros((n * n, len(edges)))
    for y in range(n):
        for x in range(n):
            row = y * n + x
            for e, s in [(((x, y), (x + 1, y)), 1),
                         (((x + 1, y), (x + 1, y + 1)), 1),
                         (((x, y + 1), (x + 1, y + 1)), -1),
                         (((x, y), (x, y + 1)), -1)]:
                boundary[row, lookup[e]] = s
    return boundary


def coherent_loop(n, t, phases):
    # One additional mode is an untouched phase reference.
    state = np.zeros(n + 1, complex)
    state[0] = state[n] = 1 / math.sqrt(2)
    a = -2 * np.arctanh(2 * t) / t
    tau = math.pi / (2 * abs(a) * t)
    for i in range(n):
        j = (i + 1) % n
        k = np.zeros((n + 1, n + 1), complex)
        k[i, j] = a * t * np.exp(1j * phases[i])
        k[j, i] = k[i, j].conjugate()
        vals, vecs = np.linalg.eigh(k)
        u = (vecs * np.exp(-1j * tau * vals)) @ vecs.conj().T
        state = u @ state
    predicted = (1j ** n) * np.exp(-1j * sum(phases))
    return max(abs(state[0] / state[n] - predicted),
               np.linalg.norm(state[1:n]))


def run():
    cs = annihilators(4)
    number = sum(c.conj().T @ c for c in cs)
    errors = {"mean": 0.0, "second_moment": 0.0, "probabilities": 0.0}
    cases = 0
    for t in [0.01, 0.03, 0.1, 0.12]:
        a = -2 * np.arctanh(2 * t) / t
        for phi in [-math.pi, -math.pi/2, -0.2, 0, 0.2, math.pi/2, math.pi]:
            c = 0.5 * np.eye(4, dtype=complex)
            for i, j in [(0, 1), (1, 2), (2, 3)]:
                c[i, j] = c[j, i] = t
            c[3, 0] = t * np.exp(1j * phi)
            c[0, 3] = c[3, 0].conjugate()
            rho = density(c, cs)
            h23 = np.zeros((4, 4), complex)
            h34 = np.zeros((4, 4), complex)
            h23[1, 2] = h23[2, 1] = a*t
            h34[2, 3] = h34[3, 2] = a*t
            q23, q34 = quadratic(h23, cs), quadratic(h34, cs)
            observable = 1j * (number - 2*np.eye(16)) @ (q23 @ q34 - q34 @ q23)
            b = a*a*t*t
            mean = np.trace(rho @ observable).real
            second = np.trace(rho @ observable @ observable).real
            q = 0.25 - 8*t**4*(1 - math.cos(phi))
            errors["mean"] = max(errors["mean"], abs(mean - 2*a*a*t**4*math.sin(phi)))
            errors["second_moment"] = max(errors["second_moment"], abs(second - b*b*q))
            vals, vecs = np.linalg.eigh(observable / b)
            diag = np.diag(vecs.conj().T @ rho @ vecs).real
            probs = [diag[np.abs(vals-z) < 1e-7].sum() for z in [-1, 0, 1]]
            expected = [q/2-t*t*math.sin(phi), 1-q, q/2+t*t*math.sin(phi)]
            errors["probabilities"] = max(errors["probabilities"], max(abs(np.array(probs)-expected)))
            cases += 1
    grid_errors = []
    for n in [1, 2, 3, 5, 8]:
        b = grid_boundary(n)
        sigma = np.linalg.svd(b, compute_uv=False)[-1]
        expected = 2*math.sqrt(2)*math.sin(math.pi/(2*(n+1)))
        grid_errors.append({"side_cells": n, "sigma_min": float(sigma),
                            "residual": float(abs(sigma-expected))})
    rng = np.random.default_rng(74012)
    coherent_errors = []
    for n in [3, 4, 6, 9, 12]:
        residual = coherent_loop(n, 0.05, rng.uniform(-math.pi, math.pi, n))
        coherent_errors.append({"cycle_length": n, "residual": float(residual)})
    assert max(errors.values()) < 1e-10
    assert max(x["residual"] for x in grid_errors) < 1e-10
    assert max(x["residual"] for x in coherent_errors) < 1e-10
    result = {"scope": "finite convention checks only", "four_site_cases": cases,
              "four_site_residuals": errors, "grid_singular_values": grid_errors,
              "coherent_loop_checks": coherent_errors}
    out = Path(__file__).with_name("robust_numerics_checks.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
