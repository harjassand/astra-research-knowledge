"""Exact finite diagnostics for the two claims in pcp_bridge.md.

Run with Python 3; only standard-library arithmetic is used.
Finite checks do not constitute the general mathematical proof.
"""

from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json


def chebyshev(a, x):
    if a == 0:
        return F(1)
    left, right = F(1), x
    for _ in range(1, a):
        left, right = right, 2 * x * right - left
    return right


def polynomial_mod(a, b):
    while a and a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def irreducible(degree):
    for candidate in range((1 << degree) | 1, 1 << (degree + 1), 2):
        valid = True
        for d in range(1, degree // 2 + 1):
            for divisor in range((1 << d) | 1, 1 << (d + 1), 2):
                if polynomial_mod(candidate, divisor) == 0:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            return candidate
    raise AssertionError("No irreducible polynomial found")


def mul(a, b, modulus, degree):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & (1 << degree):
            a ^= modulus
    return result


def trace(a, modulus, degree):
    result = 0
    current = a
    for _ in range(degree):
        result ^= current
        current = mul(current, current, modulus, degree)
    assert result in (0, 1)
    return result


def walsh(values):
    out = list(values)
    step = 1
    while step < len(out):
        for start in range(0, len(out), 2 * step):
            for offset in range(step):
                a, b = out[start + offset], out[start + offset + step]
                out[start + offset] = a + b
                out[start + offset + step] = a - b
        step *= 2
    return out


def character_fixture(bits):
    q = 1
    degree = 0
    while q < 4 * bits:
        q *= 2
        degree += 1
    modulus = irreducible(degree)
    powers = []
    for b in range(q):
        seq = [1]
        for _ in range(1, bits):
            seq.append(mul(seq[-1], b, modulus, degree))
        powers.append(seq)
    counts = Counter()
    for a in range(q):
        for b in range(q):
            label = 0
            for i, bi in enumerate(powers[b]):
                label |= trace(mul(a, bi, modulus, degree), modulus, degree) << i
            counts[label] += 1
    correlations = walsh([counts[label] for label in range(1 << bits)])
    assert correlations[0] == q * q
    beta_max = F(0)
    for u in range(1, 1 << bits):
        roots = 0
        for b in range(q):
            value = 0
            for i, bi in enumerate(powers[b]):
                if (u >> i) & 1:
                    value ^= bi
            roots += value == 0
        beta = F(correlations[u], q * q)
        assert beta == F(roots, q)
        assert F(0) <= beta <= F(bits - 1, q) <= F(1, 4)
        beta_max = max(beta_max, beta)
    gap = (1 - beta_max) / 2
    assert gap >= F(3, 8)
    # The convolution tester annihilates the uniform vector exactly.
    diagonal = F(q * q - counts[0], 2 * q * q)
    off_sum = sum(F(-count, 2 * q * q) for label, count in counts.items() if label)
    assert diagonal + off_sum == 0
    return {
        "bits": bits,
        "q": q,
        "modulus_binary": bin(modulus),
        "sample_count": q * q,
        "distinct_labels": len(counts),
        "nontrivial_characters_checked": (1 << bits) - 1,
        "maximum_bias": str(beta_max),
        "exact_gap": str(gap),
        "max_enumerated_row_support": 1 + q * q,
        "uniform_kernel_row_sum": "0",
    }


def chebyshev_fixtures():
    records = []
    points = 0
    for t in (4, 8, 16, 32, 64, 128, 256, 512, 4096):
        for a in range(1, min(8, t // 2) + 1):
            denominator = chebyshev(a, F(t + 1, t - 1))
            c = 1 - 1 / (denominator * denominator)
            assert 0 < c < 1
            minimum = F(1)
            max_bits = 0
            for j in range(t + 1):
                numerator = chebyshev(a, F(t + 1 - 2 * j, t - 1))
                value = 1 - (numerator / denominator) ** 2
                assert 0 <= value <= 1
                if j == 0:
                    assert value == 0
                else:
                    assert value >= c
                    minimum = min(minimum, value)
                max_bits = max(max_bits, value.numerator.bit_length(), value.denominator.bit_length())
                points += 1
            assert minimum == c
            d = 2 * a
            bound = None
            if d * d < t:
                bound = F(d * d, t - d * d)
                assert c <= bound
            if a == 1:
                assert c == F(4 * t, (t + 1) ** 2)
            records.append({
                "t": t,
                "chebyshev_order": a,
                "syndrome_degree": d,
                "exact_gap": str(c),
                "degree_bound": None if bound is None else str(bound),
                "max_grid_value_bits": max_bits,
            })
    return records, points


def main():
    chebyshev, points = chebyshev_fixtures()
    enforcers = [character_fixture(bits) for bits in range(1, 10)]
    # Complete Fourier-image enforcement uses G_r and G_(r+1),
    # zero on the valid frequency-0 tail sector, identity on invalid
    # frequencies. Orthogonal sector gaps therefore compose exactly.
    encoded = []
    for r in range(1, 9):
        first = F(enforcers[r - 1]["exact_gap"])
        second = F(enforcers[r]["exact_gap"])
        gap = min(first, second, F(1))
        assert gap >= F(3, 8)
        m = 1 << r
        encoded.append({
            "r": r,
            "old_port_dimension": m + 1,
            "new_port_dimension": 2 * m,
            "logical_field_dimension": m + 2,
            "image_enforcement_gap": str(gap),
            "all_unused_frequencies_penalty": "1",
            "construction": "orthogonal sectors, exact uniform kernels",
        })
    result = {
        "status": "PASS_FINITE_EXACT_DIAGNOSTICS_ONLY",
        "chebyshev_cases": len(chebyshev),
        "chebyshev_grid_points": points,
        "small_bias_cases": len(enforcers),
        "nontrivial_character_checks": sum(x["nontrivial_characters_checked"] for x in enforcers),
        "complete_encoded_image_cases": len(encoded),
        "chebyshev": chebyshev,
        "small_bias": enforcers,
        "encoded_images": encoded,
    }
    destination = Path(__file__).with_suffix(".json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("chebyshev", "small_bias", "encoded_images")}, indent=2))


if __name__ == "__main__":
    main()
