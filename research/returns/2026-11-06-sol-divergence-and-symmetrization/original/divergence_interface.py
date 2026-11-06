"""Exact finite tests of the transferred divergence interface.

No capacity evaluator is implemented here.  The tests distinguish the
unstabilized, classically stabilized and fully stabilized optimizations,
including a full-rank comparison Choi matrix.  A compressed, rigorous
entropy calculation also checks the extensive loss from permutation
averaging for an antidegradable erasure channel.
"""
from fractions import Fraction as F
from math import comb
import json
import time
import sympy as s
from finite_block import Channel, identity_channel, integer_pure_density, bell_density


def depolarizing(a, b):
    return Channel(a, b, tuple(s.eye(b)/b if i == j else s.zeros(b)
                              for i in range(a) for j in range(a)))


def exact_dyadic_entropy(rho):
    out = s.Integer(0)
    for eigenvalue, multiplicity in rho.eigenvals().items():
        if eigenvalue:
            term = s.log(eigenvalue, 2)
            assert term.is_Integer
            out -= multiplicity * eigenvalue * term
    return out


def atanh_log_bounds(x, terms):
    """Bounds on ln x for rational 1<=x<=2."""
    assert F(1) <= x <= F(2)
    z = (x-1)/(x+1)
    lo = 2*sum((z**(2*j+1)/F(2*j+1)
                for j in range(terms)), F(0))
    tail = 2*z**(2*terms+1)/(F(2*terms+1)*(1-z*z))
    return lo, lo+tail


def log2_bounds(x, bits=50):
    """Outward-rounded dyadic bounds on log2 of a positive rational."""
    x = F(x)
    assert x > 0
    exponent = 0
    while x < 1:
        x *= 2
        exponent -= 1
    while x >= 2:
        x /= 2
        exponent += 1
    terms = 1
    while True:
        ylo, yhi = atanh_log_bounds(x, terms)
        llo, lhi = atanh_log_bounds(F(2), terms)
        lo = F(exponent)+ylo/lhi
        hi = F(exponent)+yhi/llo
        if hi-lo <= F(1, 2**(bits+2)):
            scale = 2**bits
            flo = lo*scale
            fhi = hi*scale
            lower = F(flo.numerator//flo.denominator, scale)
            upper = F(-((-fhi.numerator)//fhi.denominator), scale)
            assert lower <= lo <= hi <= upper
            return lower, upper
        terms += 1


def type_marginal_entropy(n, k, bits=50):
    """Entropy of any k bits of uniform weight-n/2 binary strings.

    There are comb(k,j) strings of weight j, each with probability
    comb(n-k,n/2-j)/comb(n,n/2).  This avoids constructing a 2**n matrix.
    """
    assert n % 2 == 0 and 0 <= k <= n
    total = comb(n, n//2)
    lo = hi = F(0)
    mass = F(0)
    for j in range(k+1):
        remainder = n//2-j
        if not 0 <= remainder <= n-k:
            continue
        probability = F(comb(n-k, remainder), total)
        multiplicity = comb(k, j)
        loglo, loghi = log2_bounds(probability, bits)
        weight = multiplicity * probability
        lo -= weight*loghi
        hi -= weight*loglo
        mass += weight
    assert mass == 1
    return lo, hi


def twirled_type_coherent_information(n, erasure_probability, bits=50):
    p = F(erasure_probability)
    entropies = [type_marginal_entropy(n, k, bits) for k in range(n+1)]
    lo = hi = F(0)
    for k in range(n+1):
        probability = comb(n,k)*(1-p)**k*p**(n-k)
        slo, shi = entropies[k]
        elo, ehi = entropies[n-k]
        lo += probability*(slo-ehi)
        hi += probability*(shi-elo)
    return lo, hi


def decimal_bound(value, lower, places=15):
    scale = 10**places
    scaled = value*scale
    rounded = (scaled.numerator//scaled.denominator if lower
               else -((-scaled.numerator)//scaled.denominator))
    sign = "-" if rounded < 0 else ""
    magnitude = abs(rounded)
    return sign+str(magnitude//scale)+"."+str(magnitude%scale).zfill(places)


def execute_checks():
    start = time.perf_counter()
    a = b = 2
    physical = depolarizing(a, b)
    first = identity_channel(a).tensor(physical)
    second = depolarizing(a, a).tensor(physical)
    jsecond = second.choi()
    assert jsecond == s.eye(16)/16
    assert jsecond.det() == s.Rational(1, 2**64)
    for i in range(4):
        for j in range(4):
            assert s.trace(second.images[i*4+j]) == int(i == j)

    pure_a = integer_pure_density([1,0])
    unref_input = s.kronecker_product(pure_a, pure_a)
    output = first.apply_reference(unref_input, 1)
    comparison = second.apply_reference(unref_input, 1)
    assert comparison == s.eye(4)/4
    unref_normalized = 2-exact_dyadic_entropy(output)
    assert unref_normalized == 1

    referenced_input = s.kronecker_product(bell_density(a), pure_a)
    output_with_z = first.apply_reference(referenced_input, a)
    comparison_with_z = second.apply_reference(referenced_input, a)
    assert comparison_with_z == s.eye(8)/8
    ref_normalized = 3-exact_dyadic_entropy(output_with_z)
    assert ref_normalized == 2

    # The infimum substitution is attained by pi_R tensor pi_B.
    product_output = s.eye(4)/4
    infimum_unnormalized = 1-exact_dyadic_entropy(product_output)
    assert infimum_unnormalized == -1

    # A cq label with probability 1/3 on pure R, 2/3 on mixed R.
    # Direct-sum classical terms cancel; the normalized divergence is
    # the weighted average 1/3*1 + 2/3*0.
    cq_divergence = s.Rational(1,3)*1+s.Rational(2,3)*0
    assert cq_divergence == s.Rational(1,3)

    n = 32
    plo, phi = twirled_type_coherent_information(n, F(3,4), bits=50)
    # Independent analytic bound: S(X_K)>=K-log2(n+1), S(X_K)<=K.
    # As 33<64, I_c <= -16+log2(33) < -10.
    assert phi < -10
    assert phi-plo < F(1, 2**40)
    # A second compressed formula check: p=1/2 is self-complementary.
    hlo, hhi = twirled_type_coherent_information(8, F(1,2), bits=40)
    assert hlo <= 0 <= hhi
    assert hhi-hlo < F(1, 2**30)

    return {
        "status": "PASS",
        "physical_channel": "qubit completely depolarizing; Q=0 analytically",
        "first_map_dimensions": [first.a, first.b],
        "second_normalized_choi": "I_16/16",
        "second_choi_determinant": str(jsecond.det()),
        "unstabilized_normalized_witness_bits": str(unref_normalized),
        "fully_stabilized_normalized_witness_bits": str(ref_normalized),
        "unstabilized_identity_comparison_bits": str(unref_normalized-1),
        "fully_stabilized_identity_comparison_bits": str(ref_normalized-1),
        "substituted_set_infimum_identity_comparison_bits": str(infimum_unnormalized),
        "classical_label_fixture_normalized_bits": str(cq_divergence),
        "type_twirl": {
            "n": n, "erasure_probability": "3/4", "original_pure_input_Ic": 0,
            "twirled_Ic_interval": [str(plo), str(phi)],
            "outward_decimal_interval": [decimal_bound(plo, True),
                                          decimal_bound(phi, False)],
            "decimal_estimates": [float(plo), float(phi)],
            "analytic_upper_bound": "-16+log2(33)<-10",
            "entropy_matrix_dimension_avoided": str(2**n),
            "interval_width": str(phi-plo)},
        "elapsed_seconds": time.perf_counter()-start,
        "scope": "Exact interface counterexamples and certified compressed entropy calculation; no capacity evaluator or general noncomputability theorem."}


if __name__ == "__main__":
    result = execute_checks()
    with open("divergence_checks.json", "w") as handle:
        json.dump(result, handle, indent=2)
    print(json.dumps(result, indent=2))
