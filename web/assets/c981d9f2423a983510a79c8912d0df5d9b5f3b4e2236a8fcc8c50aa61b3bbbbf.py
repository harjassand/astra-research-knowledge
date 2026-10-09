#!/usr/bin/env python3
"""Exact-rational interval certificate for the 30-state reversible-output clock.

Only Python's standard library is used.  All inequalities establishing the
base Horn and PSD margins are checked with fractions.Fraction; the nonzero
reverse and sheet-switch rates are handled by an explicit coupling bound.
"""
from fractions import Fraction as F
from math import factorial
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
import json


def exp_minus_rate_interval(rate, order=30, tail_start=30):
    # e^rate = sum_{j=0}^order rate^j/j! + positive remainder.
    partial = sum((rate**j / factorial(j) for j in range(order + 1)), F(0))
    first_omitted = rate ** (order + 1) / factorial(order + 1)
    ratio = rate / (order + 2)
    remainder_upper = first_omitted / (1 - ratio)
    e2_lo, e2_hi = partial, partial + remainder_upper
    e_minus_two = (1 / e2_hi, 1 / e2_lo)

    # The Poisson tail from n=tail_start is bounded by a geometric series.
    tail_first = rate**tail_start / factorial(tail_start)  # e^-rate < 1
    tail_ratio = rate / (tail_start + 1)
    poisson_tail = tail_first / (1 - tail_ratio)
    return e_minus_two, poisson_tail


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def neg(x):
    return (-x[1], -x[0])


def sub(x, y):
    return add(x, neg(y))


def scale(c, x):
    if c >= 0:
        return (c * x[0], c * x[1])
    return (c * x[1], c * x[0])


def mul(x, y):
    vals = (x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1])
    return (min(vals), max(vals))


def decimal_endpoint(x, digits=18, rounding=ROUND_FLOOR):
    with localcontext() as ctx:
        ctx.prec = digits + 8
        ctx.rounding = rounding
        d = Decimal(x.numerator) / Decimal(x.denominator)
        return format(d, f".{digits}f")


def interval_text(x):
    return (f"[{decimal_endpoint(x[0], rounding=ROUND_FLOOR)}, "
            f"{decimal_endpoint(x[1], rounding=ROUND_CEILING)}]")


def poisson_output_intervals(rate, e_interval, tail, cutoff=30):
    # For N=3m+s and uniform starting phase r in {0,1,2},
    # floor((r+N)/3) is m/m+1 with weights (1,0), (2/3,1/3),
    # or (1/3,2/3), respectively.
    coeff = [F(0) for _ in range(5)]
    for n in range(cutoff):
        m, s = divmod(n, 3)
        c = rate**n / factorial(n)
        j = m % 5
        if s == 0:
            coeff[j] += c
        elif s == 1:
            coeff[j] += F(2, 3) * c
            coeff[(j + 1) % 5] += F(1, 3) * c
        else:
            coeff[j] += F(1, 3) * c
            coeff[(j + 1) % 5] += F(2, 3) * c
    return [(coeff[j] * e_interval[0], coeff[j] * e_interval[1] + tail)
            for j in range(5)]


def sqrt5_interval():
    # Both endpoints are rational; the integer square checks certify them.
    den = 10**15
    lo = F(2236067977499789, den)
    hi = F(2236067977499790, den)
    assert lo * lo < 5 < hi * hi
    return (lo, hi)


def check_ctmc(rate, reverse, switch):
    states = [(sheet, n) for sheet in (0, 1) for n in range(15)]
    index = {state: j for j, state in enumerate(states)}
    size = len(states)
    Q = [[F(0) for _ in range(size)] for _ in range(size)]
    for sheet, n in states:
        i = index[(sheet, n)]
        along = rate if sheet == 0 else reverse
        against = reverse if sheet == 0 else rate
        Q[i][index[(sheet, (n + 1) % 15)]] += along
        Q[i][index[(sheet, (n - 1) % 15)]] += against
        Q[i][index[(1 - sheet, n)]] += switch
        Q[i][i] = -sum(Q[i])

    # Uniform pi is stationary iff every column sum is zero.
    assert all(sum(Q[i][j] for i in range(size)) == 0 for j in range(size))
    J = [index[(1 - sheet, n)] for sheet, n in states]
    for i in range(size):
        for j in range(size):
            assert Q[j][i] == Q[J[i]][J[j]]
    # Strong connectivity, hence irreducibility, is checked on positive rates.
    reached, frontier = {0}, [0]
    while frontier:
        i = frontier.pop()
        for j, value in enumerate(Q[i]):
            if value > 0 and j not in reached:
                reached.add(j)
                frontier.append(j)
    assert len(reached) == size
    # Output labels floor(n/3) are fixed by the sheet-swap involution.
    observed = lambda state: state[1] // 3
    assert all(observed(states[i]) == observed(states[J[i]])
               for i in range(size))
    return size


def main():
    rate = F(15, 8)
    e_interval, tail = exp_minus_rate_interval(rate)
    q = poisson_output_intervals(rate, e_interval, tail)

    # The opposite-orientation sheet transposes the directed pair table.
    # Therefore the two-sheet pair table uses qsym=(q_d+q_-d)/2.
    q0 = q[0]
    q14 = add(q[1], q[4])
    q23 = add(q[2], q[3])
    horn = add(sub(q0, q14), q23)

    root5 = sqrt5_interval()
    c72 = (F(root5[0] - 1, 4), F(root5[1] - 1, 4))
    c144 = (F(-(root5[1] + 1), 4), F(-(root5[0] + 1), 4))
    # Fourier coefficients of the symmetric circulant displacement law.
    mu1 = add(add(q0, mul(c72, q14)), mul(c144, q23))
    mu2 = add(add(q0, mul(c144, q14)), mul(c72, q23))

    # These intentionally loose rational thresholds leave ample room for
    # finite reverse rates and the irreducibility links.
    assert horn[1] < F(-13, 1000), f"Horn upper bound too weak: {interval_text(horn)}"
    assert mu1[0] > F(54, 100), f"mu1 lower bound too weak: {interval_text(mu1)}"
    assert mu2[0] > F(43, 1000), f"mu2 lower bound too weak: {interval_text(mu2)}"

    # Actual irreducible model: A=15/8, reverse rate b, sheet-switch rate d.
    b = d = F(1, 10**8)
    state_count = check_ctmc(rate, b, d)
    pair_l1_perturbation = 2 * (b + d)
    base_psd_eigenvalue_lower = min(F(1, 5), mu1[0] / 5, mu2[0] / 5)
    actual_psd_lower = base_psd_eigenvalue_lower - pair_l1_perturbation
    actual_horn_upper = horn[1] + pair_l1_perturbation
    assert actual_psd_lower > F(8, 1000), actual_psd_lower
    assert actual_horn_upper < F(-12, 1000), actual_horn_upper

    out = {
        "scope": "Exact-rational interval proof for base table plus explicit CTMC coupling perturbation bound",
        "hidden_states": state_count,
        "output_alphabet": 5,
        "phases_per_output": 3,
        "lag": 1,
        "clockwise_rate": str(rate),
        "reverse_rate": "1/100000000",
        "sheet_switch_rate": "1/100000000",
        "e_minus_clockwise_rate_interval": [str(e_interval[0]), str(e_interval[1])],
        "poisson_tail_n_ge_30_upper": str(tail),
        "directed_output_displacement_intervals": [
            [str(x[0]), str(x[1])] for x in q
        ],
        "horn_pairing_base_interval": [str(horn[0]), str(horn[1])],
        "horn_pairing_base_decimal_outward": interval_text(horn),
        "fourier_mu1_base_interval": [str(mu1[0]), str(mu1[1])],
        "fourier_mu1_base_decimal_outward": interval_text(mu1),
        "fourier_mu2_base_interval": [str(mu2[0]), str(mu2[1])],
        "fourier_mu2_base_decimal_outward": interval_text(mu2),
        "pair_table_l1_perturbation_upper": str(pair_l1_perturbation),
        "actual_min_eigenvalue_lower": str(actual_psd_lower),
        "actual_min_eigenvalue_decimal_floor": decimal_endpoint(actual_psd_lower),
        "actual_horn_pairing_upper": str(actual_horn_upper),
        "actual_horn_pairing_decimal_ceiling": decimal_endpoint(actual_horn_upper, rounding=ROUND_CEILING),
        "local_detailed_balance": "equal state energies; the two sheets use opposite chemical affinities +/-ln((15/8)/b) per oriented edge; sheet switches are work-free",
        "entropy_production_rate_nats_per_time": "(15/8-b)*ln((15/8)/b)",
        "uniform_stationarity_j_conjugacy_irreducibility": "PASS exact rational checks",
        "hidden_time_reversal_parity": "all states even; sheet swap is a generator symmetry, not physical odd parity",
        "assertions": "PASS"
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
