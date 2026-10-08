"""Independent finite normalization diagnostics; not a proof of the theorem."""
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
import json
import numpy as np


I = np.eye(2, dtype=complex)
P = [np.array([[0, 1], [1, 0]], complex),
     np.array([[0, -1j], [1j, 0]], complex),
     np.diag([1, -1]).astype(complex)]


def kron_all(items):
    answer = np.array([[1]], complex)
    for item in items:
        answer = np.kron(answer, item)
    return answer


def reduction(rho, n, r):
    return np.einsum("abcb->ac", rho.reshape(2**r, 2**(n-r), 2**r, 2**(n-r)))


def white_top_twisted(n):
    spins = [sum(kron_all([pauli if site == index else I for site in range(n)])
                 for index in range(n)) / 2 for pauli in P]
    j2 = sum(spin @ spin for spin in spins)
    eigenvalues, eigenvectors = np.linalg.eigh(j2)
    rho = np.zeros_like(j2)
    for spin_twice in range(n, -1, -2):
        j = spin_twice / 2
        mask = np.isclose(eigenvalues, j * (j + 1), atol=1e-8)
        sector = eigenvectors[:, mask] @ eigenvectors[:, mask].conj().T
        magnetic = np.diag(np.isclose(np.diag(spins[2]).real, j).astype(float))
        rho += (spin_twice + 1) / 2**n * sector @ magnetic
    assert abs(np.trace(rho) - 1) < 1e-10
    values, vectors = np.linalg.eigh(spins[0] @ spins[0])
    twist = (vectors * np.exp(-0.19j * values)) @ vectors.conj().T
    return twist @ rho @ twist.conj().T


matrix_results = []
for n in [4, 6]:
    rho_n = white_top_twisted(n)
    tau = reduction(rho_n, n, 1)
    b = np.array([np.trace(tau @ pauli).real for pauli in P])
    centered = [I] + [P[a] - b[a] * I for a in range(3)]
    gram = np.array([[np.trace(tau @ left.conj().T @ right)
                      for right in centered] for left in centered])
    assert np.max(abs(gram[0, 1:])) < 1e-10
    for r in [2, 3]:
        rho = reduction(rho_n, n, r)
        reference = kron_all([tau] * r)
        delta = rho - reference
        direct = np.trace(rho @ rho @ np.linalg.inv(reference)).real - 1
        words = [kron_all([centered[a] for a in axes])
                 for axes in product(range(4), repeat=r)]
        coefficients = np.array([np.trace(word.conj().T @ delta) for word in words])
        gram_full = kron_all([gram] * r)
        parsed = (coefficients.conj() @ np.linalg.solve(gram_full, coefficients)).real
        assert abs(direct - parsed) < 1e-9
        eigenvalues = np.linalg.eigvalsh(rho)
        positive = eigenvalues[eigenvalues > 1e-14]
        ref_values, ref_vectors = np.linalg.eigh(reference)
        log_ref = (ref_vectors * np.log(ref_values)) @ ref_vectors.conj().T
        entropy = np.sum(positive * np.log(positive)) - np.trace(rho @ log_ref).real
        assert entropy <= np.log1p(direct) + 1e-10
        commutator = np.linalg.norm(rho @ reference - reference @ rho)
        assert commutator > 1e-8  # The normalization check really is noncommutative.
        matrix_results.append({"N": n, "r": r, "weighted_chi2": direct,
                               "Gram_error": abs(direct - parsed),
                               "relative_entropy": float(entropy),
                               "commutator_norm": float(commutator)})


def e_coefficients(n, magnetization, maximum):
    answer = [Fraction(1)]
    if maximum:
        answer.append(Fraction(magnetization))
    for degree in range(1, maximum):
        answer.append((magnetization * answer[degree]
                       - (n-degree+1) * answer[degree-1]) / (degree+1))
    return answer


exact_checks = 0
for n in range(1, 65):
    maximum = min(n, 8)
    beta = Fraction(1, n)
    coefficients = {m: e_coefficients(n, m, maximum)
                    for m in range(-n, n+1, 2)}
    for degree in range(1, maximum+1):
        direct = Fraction(0)
        for count in range(n+1):
            magnetization = 2*count-n
            shifted = sum(Fraction(comb(degree, lower), comb(n, lower))
                          * (-beta)**(degree-lower) * coefficients[magnetization][lower]
                          for lower in range(degree+1))
            direct += Fraction(comb(n, count), 2**n) * shifted**2
        expanded = sum(Fraction(comb(degree, lower)**2, comb(n, lower))
                       * beta**(2*(degree-lower)) for lower in range(degree+1))
        assert direct == expanded
        assert direct <= Fraction(4**degree, comb(n, degree))
        exact_checks += 2

derivative_bound = (Fraction(10) + Fraction(135, 256)) * Fraction(128, 119)**5
assert derivative_bound == Fraction(7381975040, 487010951)
assert derivative_bound < 16
assert 1728 * Fraction(9, 2)**2 == 34992
exact_checks += 3
result = {"exact_checks": exact_checks,
          "matrix_checks": matrix_results,
          "scope": "Finite normalization diagnostics, not theorem validation"}
Path(__file__).with_name("verification_results.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
