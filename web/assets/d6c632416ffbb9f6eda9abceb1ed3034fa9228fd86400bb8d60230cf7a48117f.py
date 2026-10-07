"""Finite exact checks of the similarity readout lemma; not theorem certification."""
from fractions import Fraction as Q
import json
import random
from pathlib import Path


def eye(d):
    return [[Q(i == j) for j in range(d)] for i in range(d)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def neg(a):
    return [[-x for x in row] for row in a]


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def inv(a):
    d = len(a)
    aug = [a[i][:] + eye(d)[i] for i in range(d)]
    for j in range(d):
        pivot = next((i for i in range(j, d) if aug[i][j]), None)
        if pivot is None:
            raise ValueError("undefined original inverse occurrence")
        aug[j], aug[pivot] = aug[pivot], aug[j]
        scale = aug[j][j]
        aug[j] = [x / scale for x in aug[j]]
        for i in range(d):
            if i != j:
                scale = aug[i][j]
                aug[i] = [x - scale * y for x, y in zip(aug[i], aug[j])]
    return [row[d:] for row in aug]


def rational_expression(x, y):
    # This expression is undefined at x=0, so the test also exercises the
    # arbitrary-expression similarity interface instead of a zero-block lift.
    d = len(x)
    return add(add(inv(x), add(mul(x, y), neg(mul(y, x)))),
               [[7 * z for z in row] for row in eye(d)])


def conj(a, p):
    return mul(mul(inv(p), a), p)


def scalar_service(x, y):
    return rational_expression(x, y)[0][0]


def reconstruct(x, y):
    d = len(x)
    diagonals = []
    permutations = []
    calls = 0
    for i in range(d):
        order = [i] + [j for j in range(d) if j != i]
        p = [[Q(k == order[j]) for j in range(d)] for k in range(d)]
        permutations.append(p)
        diagonals.append(scalar_service(conj(x, p), conj(y, p)))
        calls += 1
    result = [[Q(0) for _ in range(d)] for _ in range(d)]
    for i in range(d):
        result[i][i] = diagonals[i]
        for j in range(d):
            if i == j:
                continue
            shear = eye(d)
            shear[j][i] += 1
            # First shear at original i; then permutation moves i to first.
            p = mul(shear, permutations[i])
            result[i][j] = scalar_service(conj(x, p), conj(y, p)) - diagonals[i]
            calls += 1
    return result, calls


def test_invertible_detection(m):
    d = len(m)
    inv(m)
    values = [m[0][0]]
    for j in range(1, d):
        p = eye(d)
        p[j][0] += 1
        values.append(conj(m, p)[0][0])
    assert any(values)
    return len(values)


def main():
    rng = random.Random(20261007)
    details = []
    for d in range(1, 7):
        for repetition in range(3):
            x = [[Q(rng.randrange(-3, 4), rng.randrange(1, 5))
                  if i < j else Q(i == j) for j in range(d)] for i in range(d)]
            y = [[Q(rng.randrange(-3, 4), rng.randrange(1, 5))
                  for _ in range(d)] for _ in range(d)]
            expected = rational_expression(x, y)
            result, calls = reconstruct(x, y)
            assert result == expected
            assert calls == d * d
            # A permutation matrix has invertible output and can have every
            # diagonal zero: it is a useful adversary for identity-only readout.
            m = [[Q(j == (i + 1) % d) for j in range(d)] for i in range(d)]
            detection_calls = test_invertible_detection(m)
            details.append({"dimension": d, "repetition": repetition,
                            "reconstruction_calls": calls,
                            "invertible_detection_calls": detection_calls})
    report = {"status": "PASS", "scope": "18 exact rational fixtures",
              "claim_limit": "finite checks are not proof certification",
              "fixtures": details}
    destination = Path(__file__).with_name("DIAGONAL_READOUT_CHECK.json")
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "fixtures"}))


if __name__ == "__main__":
    main()
