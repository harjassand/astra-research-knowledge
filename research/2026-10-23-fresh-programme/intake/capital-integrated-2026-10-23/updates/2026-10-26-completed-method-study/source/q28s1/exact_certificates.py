#!/usr/local/bin/python3
"""Exact rational certificates for binary-channel quantum-conditional orders.

The scalar certificate is ordinary univariate algebra. The theorem in
binary_channel_proof.md lifts it to arbitrary finite quantum references.
"""
from fractions import Fraction as F
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(p, q):
    out = [F(0)] * max(len(p), len(q))
    for i, x in enumerate(p): out[i] += x
    for i, x in enumerate(q): out[i] += x
    return trim(out)


def scale(p, x): return trim([a * x for a in p])


def mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q): out[i + j] += x * y
    return trim(out)


def divrem(p, q):
    p, q = trim(p), trim(q)
    assert q != [0]
    out = [F(0)] * max(1, len(p) - len(q) + 1)
    while p != [0] and len(p) >= len(q):
        j = len(p) - len(q)
        x = p[-1] / q[-1]
        out[j] += x
        for i, y in enumerate(q): p[i + j] -= x * y
        p = trim(p)
    return trim(out), trim(p)


def derivative(p): return trim([F(i) * p[i] for i in range(1, len(p))] or [F(0)])


def evaluate(p, x):
    out = F(0)
    for a in reversed(p): out = out * x + a
    return out


def sturm(p):
    seq = [trim(p), derivative(p)]
    if seq[-1] == [0]: return seq[:-1]
    while True:
        _, rem = divrem(seq[-2], seq[-1])
        if rem == [0]: break
        seq.append(scale(rem, F(-1)))
    return seq


def variations(seq, t):
    signs = [1 if x > 0 else -1 for p in seq if (x := evaluate(p, t)) != 0]
    return sum(a != b for a, b in zip(signs, signs[1:]))


def rational_g(k):
    factors = [[row[1], row[0] - row[1]] for row in k]
    den = [F(1)]
    for f in factors: den = mul(den, f)
    num = [F(0)]
    for j, row in enumerate(k):
        term = [(row[0] - row[1]) ** 2]
        for i, f in enumerate(factors):
            if i != j: term = mul(term, f)
        num = add(num, term)
    return num, den


def certify(label, k, l, bound):
    nk, dk = rational_g(k)
    nl, dl = rational_g(l)
    p = add(scale(mul(nl, dk), bound), scale(mul(nk, dl), F(-1)))
    original = p
    endpoints = [0, 0]
    while len(p) > 1 and evaluate(p, F(0)) == 0:
        p, rem = divrem(p, [F(0), F(1)])
        assert rem == [0]
        endpoints[0] += 1
    while len(p) > 1 and evaluate(p, F(1)) == 0:
        # Divide by 1-t, positive on the open interval.
        p, rem = divrem(p, [F(1), F(-1)])
        assert rem == [0]
        endpoints[1] += 1
    seq = sturm(p)
    count = variations(seq, F(0)) - variations(seq, F(1))
    positive_midpoint = evaluate(p, F(1, 2)) > 0
    assert count == 0 and positive_midpoint, (label, count, positive_midpoint)
    return {'comparison': label, 'rational_bound': str(bound),
            'K': [[str(x) for x in row] for row in k],
            'L': [[str(x) for x in row] for row in l],
            'comparison_polynomial_coefficients_ascending': [str(x) for x in original],
            'positive_endpoint_factors': {'t_power': endpoints[0], 'one_minus_t_power': endpoints[1]},
            'reduced_polynomial_coefficients_ascending': [str(x) for x in p],
            'sturm_sequence': [[str(x) for x in poly] for poly in seq],
            'sturm_roots_in_open_unit_interval': count,
            'midpoint_exact_value': str(evaluate(p, F(1, 2))),
            'conclusion': 'strictly positive comparison polynomial in (0,1); all-quantum-reference bound certified by analytic theorem'}


def main():
    ident = [[F(1), F(0)], [F(0), F(1)]]
    biased = [[F(5, 8), F(1, 8)], [F(3, 8), F(7, 8)]]
    bsc = [[F(83, 100), F(17, 100)], [F(17, 100), F(83, 100)]]
    bec = [[F(18, 25), F(0)], [F(0), F(18, 25)], [F(7, 25), F(7, 25)]]
    asymmetric = [[F(31, 50), F(3, 25)], [F(23, 100), F(41, 100)], [F(3, 20), F(47, 100)]]
    results = [
        certify('biased_reset_vs_identity', biased, ident, F(137, 500)),
        certify('biased_reset_vs_BSC', biased, bsc, F(3, 4)),
        certify('asymmetric_3output_vs_BEC', asymmetric, bec, F(2, 5)),
        certify('BSC_vs_asymmetric_3output', bsc, asymmetric, F(63, 25)),
    ]
    (HERE / 'exact_certificate_results.json').write_text(json.dumps(results, indent=2) + '\n')
    lines = ['# Exact comparison certificates', '',
             'All arithmetic below is rational. Each comparison polynomial has no root in (0,1) by its saved Sturm sequence and is positive at 1/2. Its denominator is positive in that interval. The analytic binary lifting theorem supplies the dimension-uniform quantum guarantee.', '',
             '| Comparison | Exact certified bound | Interior roots |', '|---|---:|---:|']
    for row in results:
        lines.append(f"| {row['comparison']} | {row['rational_bound']} | 0 |")
    lines += ['', 'The sharp biased-reset value is separately derived analytically as `(19-sqrt(105))/32`; 137/500 is a rational upper certificate, not a claim of sharpness.', '',
              'Full channel matrices, polynomial coefficients and Sturm sequences are in `exact_certificate_results.json`.', '',
              'Run: `/usr/local/bin/python3 exact_certificates.py`', '']
    (HERE / 'EXACT_CERTIFICATES.md').write_text('\n'.join(lines))
    print('\n'.join(lines))


if __name__ == '__main__': main()
