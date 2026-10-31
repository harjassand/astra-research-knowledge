"""Exact orthogonal acquisition of an unknown binary quadratic energy.

The learner accesses only experiment.n, experiment.sigma, experiment.costs(),
and experiment.measure_many(X, repetitions=1).  A measure(x, shots=1) fallback
supports the same scalar interface. Every raw repeat is actually requested.

The design uses the classical BCH/orthogonal-array construction, proved in
latent_contraction_comparators.txt: labels (1,a,a**3) over a binary finite field
make all constant, unary, and pair Walsh characters distinct. Integer FWHT
reconstructs their coefficients. No matrix, latent partition, or optimizer is
read from the experiment.

Reference for conventional strength-four array machinery:
Carlet, Kiss, Nagy, doi:10.1007/s10623-022-01105-4, Remark 5 and Lemma 6.
"""
from __future__ import annotations

import math
from fractions import Fraction

import numpy as np


def _fraction(value):
    if isinstance(value, Fraction):
        return value
    if isinstance(value, (int, np.integer)):
        return Fraction(int(value))
    if isinstance(value, (float, np.floating)):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("Non-finite source report or parameter")
        return Fraction.from_float(number)
    return Fraction(value)


def _round_ratio_even(numerator, denominator):
    """Round a signed rational to its nearest integer, ties to even."""
    floor, remainder = divmod(int(numerator), int(denominator))
    if 2*remainder > denominator or (2*remainder == denominator and floor % 2):
        floor += 1
    return floor


def _poly_mod(a, modulus):
    degree = modulus.bit_length()-1
    while a and a.bit_length()-1 >= degree:
        a ^= modulus << (a.bit_length()-1-degree)
    return a


def _poly_gcd(a, b):
    while b:
        a, b = b, _poly_mod(a, b)
    return a


def _field_multiply(a, b, modulus):
    """Polynomial-basis multiplication in F_2[x]/modulus."""
    degree = modulus.bit_length()-1
    a = _poly_mod(a, modulus)
    value = 0
    while b:
        if b & 1:
            value ^= a
        b >>= 1
        a <<= 1
        if a & (1 << degree):
            a ^= modulus
    return value


def _irreducible(modulus, degree):
    # Any reducible degree-m polynomial has an irreducible factor of degree
    # at most m/2. Such a factor divides x^(2^j)-x at its own degree j.
    x = _poly_mod(2, modulus)
    power = x
    for j in range(1, degree+1):
        power = _field_multiply(power, power, modulus)
        if j <= degree//2 and _poly_gcd(power ^ x, modulus) != 1:
            return False
    return power == x


def _find_irreducible(degree):
    if degree < 1:
        raise ValueError("The finite-field degree must be positive")
    tried = 0
    for modulus in range((1 << degree) | 1, 1 << (degree+1), 2):
        tried += 1
        if _irreducible(modulus, degree):
            return modulus, tried
    raise ArithmeticError("No irreducible binary polynomial found")


def quadratic_character_design(n):
    """Return the unary/pair character labels and exact design metadata."""
    if isinstance(n, bool) or int(n) != n or n < 1:
        raise ValueError("n must be a positive integer")
    n = int(n)
    if n == 1:
        degree, modulus, tried, labels, dimension = 0, 0, 0, [1], 1
    else:
        degree = (n-1).bit_length()
        modulus, tried = _find_irreducible(degree)
        labels = []
        for a in range(n):
            square = _field_multiply(a, a, modulus)
            cube = _field_multiply(square, a, modulus)
            labels.append((1 << (2*degree)) | (a << degree) | cube)
        dimension = 1+2*degree
    pairs = [(i, j, labels[i] ^ labels[j])
             for i in range(n) for j in range(i+1, n)]
    all_labels = [0]+labels+[label for _, _, label in pairs]
    if len(set(all_labels)) != len(all_labels):
        raise ArithmeticError("The quadratic character labels are not distinct")
    return labels, pairs, {
        "n": n, "field_degree": degree,
        "irreducible_polynomial_bits": modulus,
        "irreducible_candidates_tested": tried,
        "character_dimension": dimension,
        "design_rows": 1 << dimension,
        "coefficient_count_including_constant": len(all_labels),
        "distinct_quadratic_character_labels": True,
        "exact_feature_gram_diagonal": 1 << dimension,
    }


def _configuration_block(labels, start, stop):
    return np.asarray([[1-2*((t & label).bit_count() & 1) for label in labels]
                       for t in range(start, stop)], dtype=np.int8)


def integer_fwht(values):
    """Unnormalized Walsh transform using arbitrary-precision integers."""
    values = [int(value) for value in values]
    length = len(values)
    if length < 1 or length & (length-1):
        raise ValueError("Walsh length must be a positive power of two")
    step = 1
    while step < length:
        for start in range(0, length, 2*step):
            for j in range(start, start+step):
                left, right = values[j], values[j+step]
                values[j], values[j+step] = left+right, left-right
        step *= 2
    return values


def _ceil_log2_fraction(value):
    """Smallest integer k such that value <= 2**k, for value >= 1."""
    value = _fraction(value)
    if value < 1:
        raise ValueError("Expected a rational at least one")
    numerator, denominator = value.numerator, value.denominator
    k = max(0, numerator.bit_length()-denominator.bit_length())
    if numerator > denominator << k:
        k += 1
    return k


def _sqrt_upper(value, bits=80):
    """An exact outward dyadic square-root bound, with no float decisions."""
    value = _fraction(value)
    if value < 0:
        raise ValueError("Negative radicand")
    scale = 1 << bits
    numerator = value.numerator*scale*scale
    denominator = value.denominator
    root = math.isqrt(numerator//denominator)
    if root*root*denominator < numerator:
        root += 1
    return Fraction(root, scale)


def _float_upper(value):
    value = _fraction(value)
    try:
        result = float(value)
    except OverflowError:
        return math.inf
    if not math.isfinite(result):
        return result
    if Fraction.from_float(result) < value:
        result = math.nextafter(result, math.inf)
    return result


def _zigzag_leb128_bits(value):
    value = int(value)
    unsigned = 2*value if value >= 0 else -2*value-1
    return 8*max(1, (unsigned.bit_length()+6)//7)


def _input_report_bits(value):
    if isinstance(value, (float, np.floating)):
        # The interface accepts binary64 reports (not arbitrary np.longdouble).
        if isinstance(value, np.floating) and value.dtype.itemsize > 8:
            raise TypeError("Use binary64 or exact rational source reports")
        return 64
    rational = _fraction(value)
    return (_zigzag_leb128_bits(rational.numerator)
            + _zigzag_leb128_bits(rational.denominator))


def _costs(experiment):
    public = getattr(experiment, "costs", None)
    values = public() if callable(public) else public
    if values is None:
        return {}
    return {str(key): (value.item() if isinstance(value, np.generic) else value)
            for key, value in dict(values).items()}


def acquire_orthogonal_quadratic(experiment, n, global_failure=.05,
                                 replicates=1, grid_bits=30,
                                 report_rounding_radius=0):
    """Return (full_model, acquisition_record) from public scalar reports.

    full_model contains integers only (apart from lists and dict keys):
      A_units, b_units, constant_units, denominator, n.
    It represents constant + .5*x.T*A*x + b*x, with A*1=0 exactly.

    record['source_regret_bound'] is an EXACT rational string. With probability
    at least 1-global_failure it bounds the true-energy regret added by using
    an exact optimizer of this acquired energy, uniformly over every future
    additive field. A further surrogate-optimization error can simply be added.

    report_rounding_radius bounds instrument/transport error per raw report
    relative to an ideal conditionally sigma-subgaussian report. Internal
    dyadic report rounding and coefficient rounding are separately charged.
    No claim that a finite float computation models a physical instrument's
    unreported rounding is made.
    """
    labels, pairs, metadata = quadratic_character_design(n)
    n = metadata["n"]
    if int(getattr(experiment, "n", n)) != n:
        raise ValueError("Experiment dimension differs from n")
    if isinstance(replicates, bool) or int(replicates) != replicates or replicates < 1:
        raise ValueError("replicates must be a positive integer")
    if isinstance(grid_bits, bool) or int(grid_bits) != grid_bits or grid_bits < 0:
        raise ValueError("grid_bits must be a nonnegative integer")
    replicates, grid_bits = int(replicates), int(grid_bits)
    failure, sigma = _fraction(global_failure), _fraction(experiment.sigma)
    instrument_radius = _fraction(report_rounding_radius)
    if not 0 < failure < 1 or sigma < 0 or instrument_radius < 0:
        raise ValueError("Invalid confidence, noise, or rounding parameter")
    N, D = metadata["design_rows"], metadata["coefficient_count_including_constant"]
    M, denominator = N*replicates, 1 << grid_bits
    row_sums = [0]*N
    received_bits = 0
    quantized_bits = _zigzag_leb128_bits(grid_bits)
    max_report_units_bits = 0
    before = _costs(experiment)
    measure_many = getattr(experiment, "measure_many", None)
    measure_one = getattr(experiment, "measure", None)
    if not callable(measure_many) and not callable(measure_one):
        raise TypeError("Experiment needs a public scalar measurement interface")
    # All raw observations are requested. Public batch means at repetitions>1
    # are deliberately not substituted for raw repeats or their bit accounting.
    for start in range(0, N, 256):
        stop = min(N, start+256)
        configurations = _configuration_block(labels, start, stop)
        for _ in range(replicates):
            if callable(measure_many):
                reports = measure_many(configurations, repetitions=1)
            else:
                reports = [measure_one(x, shots=1) for x in configurations]
            reports = list(reports)
            if len(reports) != stop-start:
                raise ValueError("Source returned the wrong number of raw reports")
            for row, report in enumerate(reports, start=start):
                received_bits += _input_report_bits(report)
                rational = _fraction(report)
                units = _round_ratio_even(rational.numerator*denominator,
                                          rational.denominator)
                row_sums[row] += units
                quantized_bits += _zigzag_leb128_bits(units)
                max_report_units_bits = max(max_report_units_bits, abs(units).bit_length()+1)
    transformed = integer_fwht(row_sums)
    coefficient_units = lambda label: _round_ratio_even(transformed[label], M)
    b = [coefficient_units(label) for label in labels]
    A = [[0]*n for _ in range(n)]
    off_diagonal_sum = 0
    for i, j, label in pairs:
        units = coefficient_units(label)
        A[i][j] = A[j][i] = units
        off_diagonal_sum += units
    for i in range(n):
        A[i][i] = -sum(A[i])
    walsh_constant = coefficient_units(0)
    full = {"A_units": A, "b_units": b, "denominator": denominator,
            "constant_units": walsh_constant+off_diagonal_sum, "n": n}

    # Exact upper bound on n*ln2+ln(2/failure). ln2<7/10 follows, for
    # example, by truncating exp(7/10) after its positive fourth-order term.
    logarithm_upper = Fraction(7, 10)*(n+_ceil_log2_fraction(2/failure))
    radicand = 2*D*sigma*sigma*logarithm_upper/M
    outward_bits = max(80, grid_bits+40)
    statistical = _sqrt_upper(radicand, outward_bits)
    internal_report_radius = Fraction(1, 2*denominator)
    total_report_radius = instrument_radius+internal_report_radius
    source_digitization = _sqrt_upper(D, outward_bits)*total_report_radius
    coefficient_digitization = Fraction(D, 2*denominator)
    prediction_bound = statistical+source_digitization+coefficient_digitization
    regret_bound = 2*prediction_bound
    after = _costs(experiment)
    record = {
        "method": "exact_binary_orthogonal_array_and_integer_walsh_transform",
        **metadata,
        "replicates": replicates, "raw_source_reports": M,
        "source_shots_requested": M,
        "public_measurement_repetitions_argument": 1,
        "configuration_bits_requested": n*M,
        "received_report_bits": received_bits,
        "received_report_encoding": "binary64=64 bits; exact rationals use two ZigZag LEB128 integers",
        "quantized_report_encoding_bits": quantized_bits,
        "quantized_report_encoding": "ZigZag LEB128 per raw quantized report plus common grid exponent",
        "maximum_quantized_report_integer_bits": max_report_units_bits,
        "integer_fwht_additions": N*metadata["character_dimension"],
        "integer_fwht_maximum_output_bits": max(abs(value).bit_length()+1 for value in transformed),
        "grid_bits": grid_bits,
        "global_failure": str(failure),
        "sigma": str(sigma),
        "instrument_report_rounding_radius": str(instrument_radius),
        "internal_report_rounding_radius": str(internal_report_radius),
        "total_report_rounding_radius": str(total_report_radius),
        "statistical_logarithm_exact_upper": str(logarithm_upper),
        "statistical_radius_squared_upper": str(radicand),
        "statistical_prediction_radius": str(statistical),
        "source_digitization_prediction_radius": str(source_digitization),
        "coefficient_digitization_prediction_radius": str(coefficient_digitization),
        "prediction_error_bound": str(prediction_bound),
        "source_regret_bound": str(regret_bound),
        "objective_oscillation_error_bound": str(regret_bound),
        "source_regret_bound_float_upper": _float_upper(regret_bound),
        "source_costs_before": before,
        "source": after,
    }
    return full, record
