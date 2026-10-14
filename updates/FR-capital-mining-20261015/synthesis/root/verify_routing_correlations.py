"""Finite corroboration of the analytic routing theorem, not hardware evidence."""
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path
import json
import numpy as np


def partial_trace(rho, dims, keep):
    rest = tuple(i for i in range(len(dims)) if i not in keep)
    order = tuple(keep) + rest
    dk = int(np.prod([dims[i] for i in keep]))
    dr = int(np.prod([dims[i] for i in rest]))
    a = rho.reshape(dims + dims).transpose(order + tuple(i+len(dims) for i in order))
    return np.trace(a.reshape(dk, dr, dk, dr), axis1=1, axis2=3)


def entropy(rho):
    ev = np.linalg.eigvalsh((rho+rho.conj().T)/2)
    ev = ev[ev > 1e-14]
    return float(-np.dot(ev, np.log(ev)))


def run():
    cases = 0
    for n in range(1, 6):
        assignments = list(product((0, 1), repeat=n))
        for pi in permutations(range(n)):
            for mask in range(1 << n):
                keep = [i for i in range(n) if mask >> i & 1]
                donors = {pi[i] for i in keep}
                m = len(donors.intersection(keep))
                ea = Fraction(sum(sum(z[pi[i]] for i in keep) for z in assignments), 2**n)
                eb = Fraction(sum(sum(z[i] for i in keep) for z in assignments), 2**n)
                eab = Fraction(sum(sum(z[pi[i]] for i in keep)*sum(z[i] for i in keep)
                                   for z in assignments), 2**n)
                assert eab-ea*eb == Fraction(m, 4)
                assert m >= max(0, 2*len(keep)-n)
                cases += 1

    rng = np.random.default_rng(20261015)
    a = rng.normal(size=(4, 4))+1j*rng.normal(size=(4, 4))
    rho = a@a.conj().T
    rho /= np.trace(rho)
    rx = partial_trace(rho, (2, 2), (0,))
    re = partial_trace(rho, (2, 2), (1,))
    mutual = entropy(rx)+entropy(re)-entropy(rho)
    max_error = 0.0
    quantum_cases = 0
    for n, pi in ((2, (1, 0)), (3, (1, 2, 0)), (4, (1, 0, 3, 2)), (3, (0, 2, 1))):
        full = np.array([[1.+0j]])
        for _ in range(n):
            full = np.kron(full, rho)
        for mask in range(1, 1 << n):
            keep = [i for i in range(n) if mask >> i & 1]
            k = len(keep)
            dims = (2, 2)*n
            indices = tuple(j for i in keep for j in (2*pi[i], 2*i+1))
            out = partial_trace(full, dims, indices)
            m = len(set(keep).intersection(pi[i] for i in keep))
            f = sum(pi[i] == i for i in keep)
            sx = entropy(partial_trace(out, (2, 2)*k, tuple(range(0, 2*k, 2))))
            se = entropy(partial_trace(out, (2, 2)*k, tuple(range(1, 2*k, 2))))
            cross = sx+se-entropy(out)
            local_sum = sum(entropy(partial_trace(out, (2, 2)*k, (2*j, 2*j+1))) for j in range(k))
            total = local_sum-entropy(out)
            errors = (abs(cross-m*mutual), abs(total-(m-f)*mutual))
            max_error = max(max_error, *errors)
            assert max(errors) < 3e-12, (n, pi, keep, errors)
            quantum_cases += 1
    return {"status": "passed", "classical_exhaustive_cases": cases,
            "classical_scope": "all permutations and retained subsets, N=1..5, iid fair bits; exact Fraction covariance",
            "quantum_cases": quantum_cases, "quantum_maximum_entropy_identity_error": max_error,
            "quantum_scope": "selected N=2..4 permutations and all nonempty subsets, one seeded mixed qubit-pair state",
            "evidence_limit": "finite mathematical checks only; analytic theorem proved in ROUTING_CORRELATION_THEOREM.md; no physical or novelty validation"}


if __name__ == "__main__":
    result = run()
    target = Path(__file__).with_name("ROUTING_CORRELATION_CHECK.json")
    target.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
