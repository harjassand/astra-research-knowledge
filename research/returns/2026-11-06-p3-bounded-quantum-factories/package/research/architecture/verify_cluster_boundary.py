"""Exact rational boundary for one noisy six-layer cluster fabric.

This is an architectural counterexample, not general sampling hardness or a
general impossibility theorem for bounded factories. No experimental data.
"""
from fractions import Fraction as F


def character_count(n, mask):
    count = 0
    for i in range(n):
        site = 1 << i
        partner = ((1 << (i + 1)) if i % 2 == 0 and i + 1 < n
                   else ((1 << (i - 1)) if i % 2 else 0))
        neighbors = ((1 << (i - 1)) if i else 0)
        neighbors |= ((1 << (i + 1)) if i + 1 < n else 0)
        # Reset, load-CNOT, H, CZ first matching, CZ second matching,
        # terminal delivery. Each pair is the X and Z syndrome translation;
        # Y is their XOR. Noise occurs at idle slots too.
        for x, z in [(site, 0), (site, 0), (0, site),
                     (partner, site), (neighbors, site), (neighbors, site)]:
            count += bool(((mask & x).bit_count() & 1)
                          or ((mask & z).bit_count() & 1))
    return count


def inverse_distribution(n, t, p):
    values = [(t / (1 - 2*p)) ** mask.bit_count()
              / (1 - F(4, 3)*p) ** character_count(n, mask)
              for mask in range(1 << n)]
    step = 1
    while step < len(values):
        for start in range(0, len(values), 2*step):
            for offset in range(step):
                a, b = values[start+offset], values[start+offset+step]
                values[start+offset] = a+b
                values[start+offset+step] = a-b
        step *= 2
    return [x / (1 << n) for x in values]


if __name__ == "__main__":
    n, t, p = 8, F(11, 20), F(1, 200)
    values = inverse_distribution(n, t, p)
    smallest = min(range(len(values)), key=lambda x: values[x])
    assert sum(values) == 1
    assert smallest == (1 << n)-1
    assert values[smallest] < 0
    print(f"N={n}; thermal bias={t}; Pauli total p={p}; root BSC p={p}")
    print(f"Negative preimage at {smallest:0{n}b}: {values[smallest]}")
    print(f"Approximate value: {float(values[smallest]):.16g}")
    print(f"Negative entries: {sum(x<0 for x in values)}")
