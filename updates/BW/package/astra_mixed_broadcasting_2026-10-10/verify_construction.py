#!/usr/bin/env python3
"""Internal checks for a finite-dimensional approximate-broadcasting counterexample.

The analytic argument is in RESEARCH_PROOF.md. These checks are not an
all-dimension proof, an optimization over all EB channels, or external validation.
Requires Python 3.10+, numpy, and sympy. Run from any directory. The receipt is
written next to this script. Explicit exceptions remain active under python -O.
"""
from __future__ import annotations

import itertools
import json
import math
import platform
from fractions import Fraction
from pathlib import Path
from typing import Iterable

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
TOL = 2e-10
RNG = np.random.default_rng(20261010)
checks: list[dict] = []


def check(name: str, residual: float, tolerance: float = TOL, **scope) -> None:
    if not math.isfinite(residual) or residual > tolerance:
        raise ArithmeticError(f"{name}: residual {residual} > {tolerance}")
    checks.append({"name": name, "status": "pass", "residual": residual,
                   "tolerance": tolerance, "scope": scope})


def exact_check(name: str, condition: bool, **scope) -> None:
    if not condition:
        raise ArithmeticError(f"Exact check failed: {name}")
    checks.append({"name": name, "status": "pass", "arithmetic": "exact",
                   "scope": scope})


def occupations(k: int, d: int) -> list[tuple[int, ...]]:
    if k < 0 or d < 1:
        raise ValueError("k must be nonnegative and d positive")
    if d == 1:
        return [(k,)]
    return [(a,) + rest for a in range(k + 1)
            for rest in occupations(k - a, d - 1)]


def multinomial(a: Iterable[int]) -> int:
    aa = tuple(a)
    return math.factorial(sum(aa)) // math.prod(math.factorial(x) for x in aa)


def coherent(psi: np.ndarray, k: int) -> np.ndarray:
    return np.array([math.sqrt(multinomial(a)) * np.prod(psi ** np.array(a))
                     for a in occupations(k, len(psi))], dtype=complex)


def tensor_power(x: np.ndarray, n: int) -> np.ndarray:
    out = np.array([1.0], dtype=complex)
    for _ in range(n):
        out = np.kron(out, x)
    return out


def split_isometry(k: int, d: int, m: int) -> np.ndarray:
    if k % m:
        raise ValueError("k must be divisible by m")
    inp = occupations(k, d)
    small = occupations(k // m, d)
    lookup = {a: j for j, a in enumerate(inp)}
    v = np.zeros((len(small) ** m, len(inp)), dtype=complex)
    for row, groups in enumerate(itertools.product(small, repeat=m)):
        total = tuple(sum(b[j] for b in groups) for j in range(d))
        v[row, lookup[total]] = math.sqrt(
            math.prod(multinomial(b) for b in groups) / multinomial(total))
    return v


def trace_distance(a: np.ndarray, b: np.ndarray) -> float:
    h = (a - b + (a - b).conj().T) / 2
    return float(np.sum(np.abs(np.linalg.eigvalsh(h))) / 2)


def partial_trace_one(x: np.ndarray, dim: int, m: int, keep: int) -> np.ndarray:
    if x.shape != (dim ** m, dim ** m):
        raise ValueError("Incorrect tensor matrix size")
    tensor = x.reshape([dim] * (2 * m))
    sites = list(range(m))
    for site in reversed(range(m)):
        if site == keep:
            continue
        pos = sites.index(site)
        tensor = np.trace(tensor, axis1=pos, axis2=pos + len(sites))
        sites.pop(pos)
    return tensor.reshape(dim, dim)


def decoder_kraus(d: int, counts: list[int], offsets: list[int]) -> list[np.ndarray]:
    total = offsets[-1]
    maps = []
    for level, k in enumerate(counts):
        inp = occupations(k, d)
        for beta in occupations(k - 1, d):
            a = np.zeros((d, total), dtype=complex)
            for col, alpha in enumerate(inp):
                for j in range(d):
                    reduced = list(alpha)
                    reduced[j] -= 1
                    if tuple(reduced) == beta:
                        a[j, offsets[level] + col] = math.sqrt(alpha[j] / k)
            maps.append(a)
    return maps


def channel_fixture(d: int, m: int, length: int, trials: int = 4) -> None:
    counts = [m ** r for r in range(length + 1)]
    sizes = [math.comb(d + k - 1, k) for k in counts]
    offsets = [0] + [int(x) for x in np.cumsum(sizes)]
    total = offsets[-1]
    kraus = []
    for r in range(1, length + 1):
        v = split_isometry(counts[r], d, m)
        check(f"isometry_d{d}_m{m}_L{length}_r{r}",
              float(np.max(np.abs(v.conj().T @ v - np.eye(sizes[r])))))
        out = np.zeros((total ** m, total), dtype=complex)
        rows = [np.ravel_multi_index(tuple(offsets[r-1] + j for j in tup),
                                     (total,) * m)
                for tup in itertools.product(range(sizes[r-1]), repeat=m)]
        out[np.ix_(rows, range(offsets[r], offsets[r+1]))] = v
        kraus.append(out)
    # Full-domain extension on the unused bottom block; also symmetric in outputs.
    for col in range(sizes[0]):
        a = np.zeros((total ** m, total), dtype=complex)
        a[0, col] = 1
        kraus.append(a)
    check(f"Kraus_completeness_d{d}_m{m}_L{length}",
          float(np.max(np.abs(sum(a.conj().T @ a for a in kraus) - np.eye(total)))),
          dimension=total, output_dimension=total ** m)
    dec = decoder_kraus(d, counts, offsets)
    check(f"decoder_completeness_d{d}_m{m}_L{length}",
          float(np.max(np.abs(sum(a.conj().T @ a for a in dec) - np.eye(total)))))
    for trial in range(trials):
        psi = RNG.normal(size=d) + 1j * RNG.normal(size=d)
        psi /= np.linalg.norm(psi)
        rho = np.zeros((total, total), dtype=complex)
        shifted = np.zeros_like(rho)
        for r, k in enumerate(counts):
            z = coherent(psi, k)
            if r:
                rho[offsets[r]:offsets[r+1], offsets[r]:offsets[r+1]] = np.outer(z,z.conj()) / length
            if r < length:
                shifted[offsets[r]:offsets[r+1], offsets[r]:offsets[r+1]] = np.outer(z,z.conj()) / length
        out = sum(a @ rho @ a.conj().T for a in kraus)
        product_target = np.array([[1.0]], dtype=complex)
        for _ in range(m):
            product_target = np.kron(product_target, rho)
        check(f"exact_GLOBAL_cloning_failure_d{d}_m{m}_L{length}_trial{trial}",
              abs(trace_distance(out,product_target)-(1-(length-1)/length**m)))
        residual = 0.0
        for j in range(m):
            marginal = partial_trace_one(out, total, m, j)
            residual = max(residual, float(np.max(np.abs(marginal-shifted))),
                           abs(trace_distance(marginal,rho) - 1/length))
        check(f"broadcast_and_exact_error_d{d}_m{m}_L{length}_trial{trial}", residual)
        decoded = sum(a @ rho @ a.conj().T for a in dec)
        check(f"decoded_pure_state_d{d}_m{m}_L{length}_trial{trial}",
              float(np.max(np.abs(decoded-np.outer(psi,psi.conj())))))
        eig = np.linalg.eigvalsh(rho)
        expected = np.array([0.] * (total-length) + [1/length] * length)
        check(f"rank_and_spectrum_d{d}_m{m}_L{length}_trial{trial}",
              float(np.max(np.abs(eig-expected))))
    # A generic input with cross-block coherences tests the full-domain channel,
    # rather than just its promised-family restriction.
    z = RNG.normal(size=total) + 1j * RNG.normal(size=total)
    z /= np.linalg.norm(z)
    generic = np.outer(z,z.conj())
    out = sum(a @ generic @ a.conj().T for a in kraus)
    marginals = [partial_trace_one(out,total,m,j) for j in range(m)]
    check(f"generic_trace_and_equal_marginals_d{d}_m{m}_L{length}",
          max(abs(float(np.trace(out).real)-1),
              max(float(np.max(np.abs(a-marginals[0]))) for a in marginals)))
    if length >= 2:
        # Phi and Phi^2 have orthogonal output levels on the second level.
        psi = np.zeros(d); psi[0] = 1
        zz = coherent(psi,counts[2])
        state = np.zeros((total,total),dtype=complex)
        state[offsets[2]:offsets[3], offsets[2]:offsets[3]] = np.outer(zz,zz.conj())
        once = partial_trace_one(sum(a @ state @ a.conj().T for a in kraus),total,m,0)
        twice = partial_trace_one(sum(a @ once @ a.conj().T for a in kraus),total,m,0)
        check(f"NOT_global_near_idempotence_d{d}_m{m}_L{length}",
              abs(trace_distance(once,twice)-1), tested_half_trace_distance=1)


def symmetric_projector_exact(n: int, d: int) -> sp.Matrix:
    words = list(itertools.product(range(d), repeat=n))
    out = sp.zeros(d ** n)
    counts = [tuple(w.count(j) for j in range(d)) for w in words]
    for i, a in enumerate(counts):
        for j, b in enumerate(counts):
            if a == b:
                out[i,j] = sp.Rational(1,multinomial(a))
    return out


def exact_moments() -> None:
    i = sp.I
    paulis = [sp.Matrix([[0,1],[1,0]]), sp.Matrix([[0,-i],[i,0]]),
              sp.Matrix([[1,0],[0,-1]])]
    states = [(sp.eye(2) + sign*s) / 2 for s in paulis for sign in (-1,1)]
    for n in range(1,4):
        moment = sum((sp.kronecker_product(*([p]*n)) for p in states), sp.zeros(2**n)) / 6
        target = symmetric_projector_exact(n,2) / (n+1)
        exact_check(f"Pauli_six_state_projective_moment_order_{n}", moment == target,
                    dimension=2, ensemble_size=6)
    # Critical negative control: the same ensemble is NOT a fourth design.
    moment4 = sum((sp.kronecker_product(*([p]*4)) for p in states),sp.zeros(16))/6
    target4 = symmetric_projector_exact(4,2)/5
    exact_check("Pauli_ensemble_NOT_a_fourth_design", moment4 != target4,
                message="Do not use a low-order design for the commuting-family proof")
    p3 = symmetric_projector_exact(3,2)
    support = sp.kronecker_product(symmetric_projector_exact(2,2),sp.eye(2))
    exact_check("symmetric_projector_support_nesting", support*p3 == p3 and p3*support == p3)
    complement = support-p3
    exact_check("state_estimation_dual_gap_is_a_projection", complement*complement == complement
                and complement == complement.conjugate().T)
    exact_check("dimension_ratio_k2_d2", sp.Rational(3,4) ==
                sp.Rational(math.comb(3,2),math.comb(4,3)))


def exact_parameter_bounds() -> list[dict]:
    records=[]
    for length in (2,4,8,10,16,32,100):
        k=2**length; d=4*k*k
        a=sum((Fraction(2**r+1,2**r+d) for r in range(1,length+1)), Fraction(0))/length
        easy=Fraction(2*k-2+length, length*d)
        exact_check(f"exact_estimation_bound_L{length}", 0<a<=easy<1)
        ratio = Fraction(2*k,d)
        exact_check(f"commuting_SECOND_moment_ratio_bound_L{length}",
                    ratio <= Fraction(1,4) and ratio**2/(1-ratio) <= Fraction(1,k*k),
                    implication="sum_r D_kr/D_2kr <= ratio^2/(1-ratio) <= 1/K^2")
        records.append({"L":length,"m":2,"K":str(k),"d":str(d),
                        "constructed_broadcast_error":f"1/{length}",
                        "a_exact_fraction":str(a),"a_upper_fraction":str(easy),
                        "EB_error_lower_float":float(1-a),
                        "commuting_error_lower_fraction":str(Fraction(k-1,k)),
                        "cq_classical_error_lower_expression":f"1-2^(-{length}/2)",
                        "floating_limit_warning":"A displayed 1.0 is rounding, not exact equality."})
    return records


def occupation_identity_exact() -> None:
    for d,m,j in ((2,2,1),(2,2,2),(3,2,2),(2,3,2)):
        small=occupations(j,d)
        accum={a:0 for a in occupations(m*j,d)}
        for groups in itertools.product(small,repeat=m):
            total=tuple(sum(b[q] for b in groups) for q in range(d))
            accum[total]+=math.prod(multinomial(b) for b in groups)
        exact_check(f"multinomial_isometry_d{d}_m{m}_j{j}",
                    all(v==multinomial(a) for a,v in accum.items()))


def main() -> None:
    occupation_identity_exact()
    exact_moments()
    for args in ((2,2,2),(2,2,3),(3,2,2),(2,3,1)):
        channel_fixture(*args)
    parameters=exact_parameter_bounds()
    receipt={"status":"all_executed_checks_passed", "check_count":len(checks),
             "random_seed":20261010,
             "environment":{"python":platform.python_version(),"numpy":np.__version__,
                            "sympy":sp.__version__,"platform":platform.platform()},
             "scope":"Exact finite identities and floating finite full-domain channel fixtures; not external or formal validation.",
             "checks":checks,"parameter_examples":parameters}
    (HERE/'verification_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({"status":receipt['status'],"check_count":len(checks),
                      "max_floating_residual":max([c.get('residual',0) for c in checks]),
                      "receipt":str(HERE/'verification_receipt.json')},indent=2))

if __name__=='__main__':
    main()
