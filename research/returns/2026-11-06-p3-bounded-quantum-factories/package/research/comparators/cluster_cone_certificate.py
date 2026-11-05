"""Exact-rational receipts for the uniform cluster-fabric cone theorem.

No external libraries. The all-N proof is in cluster_uniform_cone.md; the
finite-N Walsh calculation is only an independent small-instance diagnostic.
"""

from fractions import Fraction as F
import json


def uniform_constants(p=F(1, 3000), target_max=F(11, 20), root_factor=10):
    c = 1 - F(4, 3) * p
    root = root_factor * p
    tstar = target_max / (c**4 * (1 - 2 * root))
    amin = c**6
    local_min_numerator = (1 - tstar)**2 - (1 - amin)
    local_max_numerator = (1 + tstar)**2 - (1 - amin)
    ratio = local_max_numerator / local_min_numerator
    a = c**2
    alpha = (3 + a) / (4 * a)
    beta = (1 - a) / (4 * a)
    signed_ratio = beta / alpha
    zeta = 6 * signed_ratio + 9 * signed_ratio**2
    cone_bound = 1 / (4 * ratio**2 + 2 * ratio)
    kappa = 1 / (2 * ratio)
    cone_gap = kappa * (1 - kappa * ratio) - zeta * ratio * (1 + kappa)
    assert alpha - 3 * beta == 1
    assert 0 < tstar < 1
    assert local_min_numerator > 0
    assert zeta < cone_bound
    assert cone_gap > 0
    assert 7 * p + 3 * (11 * p)**2 <= 10 * p
    assert 87 * p < 1
    return {
        "p": str(p),
        "target_polarization_max": str(target_max),
        "root_BSC_bound": str(root),
        "tstar": float(tstar),
        "local_ratio_R": float(ratio),
        "signed_link_ratio_zeta": float(zeta),
        "cone_upper_bound": float(cone_bound),
        "positive_cone_gap": float(cone_gap),
        "exact_cone_gap_numerator": str(cone_gap.numerator),
        "exact_cone_gap_denominator": str(cone_gap.denominator),
        "root_parameter_contraction": float(87 * p),
        "all_exact_assertions_passed": True,
    }


def label_character_exponent(mask, n):
    # Reset, load CNOT, and H each contribute one singleton factor c per 1 bit.
    exponent = 3 * mask.bit_count()
    # First CZ matching (0,1),(2,3),...; the odd last site is an idle slot.
    for i in range(n):
        partner = i ^ 1
        own = (mask >> i) & 1
        other = (mask >> partner) & 1 if partner < n else 0
        exponent += bool(own or other)
    # Second CZ matching has completed the graph. Terminal delivery adds a
    # second identical graph-syndrome channel at every physical site.
    for i in range(n):
        own = (mask >> i) & 1
        neighbors = 0
        if i:
            neighbors ^= (mask >> (i - 1)) & 1
        if i + 1 < n:
            neighbors ^= (mask >> (i + 1)) & 1
        exponent += 2 * bool(own or neighbors)
    return exponent


def inverse_walsh(n, p, root, target=F(11, 20)):
    c = 1 - F(4, 3) * p
    values = [
        (target / (1 - 2 * root)) ** mask.bit_count()
        / c ** label_character_exponent(mask, n)
        for mask in range(1 << n)
    ]
    stride = 1
    while stride < len(values):
        for start in range(0, len(values), 2 * stride):
            for offset in range(stride):
                left = start + offset
                right = left + stride
                a, b = values[left], values[right]
                values[left], values[right] = a + b, a - b
        stride *= 2
    values = [v / (1 << n) for v in values]
    assert sum(values) == 1
    return {
        "N": n,
        "p": str(p),
        "root_BSC": str(root),
        "minimum_preimage_mass": float(min(values)),
        "negative_entries": sum(v < 0 for v in values),
        "exact_normalization": True,
    }


if __name__ == "__main__":
    report = {
        "uniform_all_N_certificate": uniform_constants(),
        "finite_N_diagnostics_not_proof": [
            inverse_walsh(7, F(1, 3000), F(1, 300)),
            inverse_walsh(8, F(1, 3000), F(1, 300)),
            inverse_walsh(8, F(1, 200), F(1, 200)),
        ],
    }
    print(json.dumps(report, indent=2))
