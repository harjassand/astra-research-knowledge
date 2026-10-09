"""Exact finite diagnostics for the pendant-pair reduction; not a proof."""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
from random import Random

rng = Random(271828)
checks = instances = weighted_checks = 0
for n in (2, 4, 6, 8):
    pairs = list(combinations(range(n), 2))
    masks = (range(1 << len(pairs)) if n <= 4 else
             [rng.getrandbits(len(pairs)) for _ in range(60)])
    for mask in masks:
        adjacency = [[0] * n for _ in range(n)]
        edges = []
        for k, (i, j) in enumerate(pairs):
            if mask >> k & 1:
                adjacency[i][j] = adjacency[j][i] = 1
                edges.append((i, j))

        @lru_cache(None)
        def pm(vertices):
            if not vertices:
                return 1
            i = vertices[0]
            return sum(adjacency[i][j] * pm(tuple(x for x in vertices[1:] if x != j))
                       for j in vertices[1:])

        z = pm(tuple(range(n)))
        if not z:
            continue
        instances += 1
        sums = [Fraction(0) for _ in range(n)]
        for u, v in edges:
            zr = pm(tuple(x for x in range(n) if x not in (u, v)))
            sums[u] += Fraction(zr, z)
            sums[v] += Fraction(zr, z)
            augmented = [row + [0, 0] for row in adjacency] + [[0] * (n + 2) for _ in range(2)]
            augmented[u][n] = augmented[n][u] = 1
            augmented[v][n + 1] = augmented[n + 1][v] = 1

            @lru_cache(None)
            def repeated_haf(counts):
                if sum(counts) == 0:
                    return 1
                if sum(counts) % 2:
                    return 0
                i = next(k for k, x in enumerate(counts) if x)
                rest = list(counts)
                rest[i] -= 1
                result = 0
                for j, multiplicity in enumerate(rest):
                    if multiplicity and augmented[i][j]:
                        nxt = rest.copy()
                        nxt[j] -= 1
                        result += multiplicity * repeated_haf(tuple(nxt))
                return result

            for na, nb in product(range(4), repeat=2):
                observed = repeated_haf((1,) * n + (na, nb))
                expected = z if (na, nb) == (0, 0) else zr if (na, nb) == (1, 1) else 0
                assert observed == expected
                checks += 1

            # Weighted amplitudes use the same matching decomposition, with
            # t on original edges and lambda on the two pendant edges.
            t = Fraction(1, 4 * n)
            for halving in range(n.bit_length() + 1):
                lam = Fraction(1, 4 * 2**halving)
                amp00 = t**(n // 2) * z
                amp11 = lam**2 * t**(n // 2 - 1) * zr
                q = amp11**2 / (amp00**2 + amp11**2)
                p = Fraction(zr, z)
                odds = (lam**2 / t)**2 * p**2
                assert q == odds / (1 + odds)
                weighted_checks += 1
        assert all(x == 1 for x in sums)

# Exact worst-case constants for noisy edge selection and calibration.
assert Fraction(1, 17) - Fraction(1, 64) > Fraction(1, 32)
assert Fraction(63, 1103) > Fraction(1, 32)
assert Fraction(2048, 63) < 64

report = (
    f"PASS: {instances} positive-perfect-matching graph instances; "
    f"{checks} exact repeated-hafnian leaf-occupation identities; "
    f"{weighted_checks} weighted odds identities; all incident marginal sums equal 1.\n"
    "Exhaustive simple graphs through 4 vertices, 60 seeded graphs each at 6 and 8 vertices; "
    "leaves tested at occupations 0,1,2,3. Seed 271828.\n"
    "Finite diagnostic only; proof is in REDUCTION_AUDIT.md.\n"
)
Path(__file__).with_name("reduction_finite_check.txt").write_text(report)
print(report, end="")
