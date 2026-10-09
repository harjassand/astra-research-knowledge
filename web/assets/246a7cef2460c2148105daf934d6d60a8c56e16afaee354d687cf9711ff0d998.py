"""Independent direct Kraus marginal calculation, including disconnected G."""
from pathlib import Path
import hashlib
import json
import sympy as s

OWN = Path(__file__).resolve().parent

def simple(x):
    return s.simplify(x)

def add(out, key, value):
    out[key] = out.get(key, s.S.Zero) + value

fixtures = [
    ("K2", 2, [(0, 1)], s.sqrt(2)),
    ("2K2", 4, [(0, 1), (2, 3)], s.sqrt(2)),
    ("K222", 6, [(i, j) for i in range(6) for j in range(i + 1, 6)
                  if i // 2 != j // 2], 1 + s.sqrt(13)),
]
records = []
for name, d, edges, lam in fixtures:
    adjacency = s.zeros(d)
    for i, j in edges:
        adjacency[i, j] = adjacency[j, i] = 1
    r = sum(adjacency[0, j] for j in range(d))
    assert all(sum(adjacency[i, j] for j in range(d)) == r for i in range(d))
    resolvent = (lam * s.eye(d) - adjacency).inv().applyfunc(simple)
    square = (resolvent * resolvent).applyfunc(simple)
    diagonal = resolvent[0, 0]
    q = square[0, 0]
    n0 = simple(2 * q - diagonal ** 2)
    assert n0.is_positive
    assert all(simple(lam * resolvent[i, i] - 2) == 0 for i in range(d))
    assert all(simple(square[i, i] - q) == 0 for i in range(d))

    # Unnormalized Kraus columns, with the same common factor 1/sqrt(n0).
    columns = []
    for k in range(d):
        operator = []
        for i in range(d):
            operator.append({(k, k): resolvent[k, k]} if i == k else
                            {(i, k): resolvent[i, k], (k, i): resolvent[i, k]})
        columns.append(operator)

    # Each direct partial trace is compared to the analytic population/coherence
    # formula. This checks the whole matrix-space action, rather than just TP.
    superoperator = s.zeros(d * d)
    for i in range(d):
        for j in range(d):
            marginal_b, marginal_c = {}, {}
            gram = s.S.Zero
            for operator in columns:
                for (b, c), x in operator[i].items():
                    for (bb, cc), y in operator[j].items():
                        if c == cc:
                            add(marginal_b, (b, bb), x * y / n0)
                        if b == bb:
                            add(marginal_c, (c, cc), x * y / n0)
                        if (b, c) == (bb, cc):
                            gram += x * y / n0
            assert simple(gram - int(i == j)) == 0
            for b in range(d):
                for bb in range(d):
                    actual = simple(marginal_b.get((b, bb), 0))
                    assert simple(actual - marginal_c.get((b, bb), 0)) == 0
                    if i != j:
                        expected = square[i, j] / n0 if (b, bb) == (i, j) else 0
                    elif b == bb:
                        expected = q / n0 if b == i else resolvent[b, i] ** 2 / n0
                    else:
                        expected = 0
                    assert simple(actual - expected) == 0
                    superoperator[b * d + bb, i * d + j] = actual

    # E_ij is an orthonormal complex HS basis. Real symmetric superoperator
    # certifies adjointness on all matrices, hence all Hermitian observables.
    assert superoperator == superoperator.T
    population = s.Matrix(d, d, lambda b, i: superoperator[b * d + b, i * d + i])
    assert population == population.T
    assert all(simple(sum(population[b, i] for b in range(d)) - 1) == 0
               for i in range(d))
    assert all(simple(sum(population[b, i] for i in range(d)) - 1) == 0
               for b in range(d))

    vectors = []
    for k in range(d):
        vector = {(i, b, c): x for i, col in enumerate(columns[k])
                  for (b, c), x in col.items()}
        assert simple(sum(x * x for x in vector.values()) - n0) == 0
        acted = {}
        for (a, b, c), x in vector.items():
            if a == b:
                for aa in range(d):
                    if adjacency[a, aa]:
                        add(acted, (aa, aa, c), 2 * x)
            if a == c:
                for aa in range(d):
                    if adjacency[a, aa]:
                        add(acted, (aa, b, aa), 2 * x)
        assert all(simple(acted.get(key, 0) - 2 * lam * vector.get(key, 0)) == 0
                   for key in set(acted) | set(vector))
        vectors.append(vector)

    records.append({"graph": name, "d": d, "r": int(r), "lambda": str(lam),
                    "n0": str(n0), "all_matrix_units_directly_checked": True,
                    "population_symmetric_doubly_stochastic": True,
                    "HS_adjoint": True, "equal_marginals": True,
                    "Kraus_TP": True, "star_eigenvectors": True,
                    "disconnected": name == "2K2"})

proof = OWN / "THEOREM_FIRST_BASELINE.txt"
result = {"status": "ALL_EXACT_ASSERTIONS_PASSED", "fixtures": records,
          "scope": "three fixed legality controls; the general result is analytic",
          "blind_proof_sha256": hashlib.sha256(proof.read_bytes()).hexdigest()}
(OWN / "BROADCASTER_LEGALITY_REPLAY.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
