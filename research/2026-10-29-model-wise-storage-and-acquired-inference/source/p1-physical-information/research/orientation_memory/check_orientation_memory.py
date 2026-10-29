#!/usr/bin/env python3
"""Exact control for the orientation-memory and constant-clock lifts.

No trajectories are sampled. Generator algebra uses Fraction throughout.
Log identities are checked by exact rational coefficients of logarithms of
primes. Numerical displays are outward-rounded certified rational intervals.
"""

from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
from math import factorial
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def transpose(a):
    return list(map(list, zip(*a)))


def mm(a, b):
    bt = transpose(b)
    return [[sum((x*y for x, y in zip(row, col)), F(0))
             for col in bt] for row in a]


def mv(a, x):
    return [sum((v*w for v, w in zip(row, x)), F(0)) for row in a]


def stationary(q, pi):
    return all(sum((pi[i]*q[i][j] for i in range(len(q))), F(0)) == 0
               for j in range(len(q)))


def verify_generator(q, pi):
    n = len(q)
    require(all(len(row) == n for row in q), "generator not square")
    require(all(sum(row) == 0 for row in q), "nonzero generator row sum")
    require(all(q[i][j] >= 0 for i in range(n) for j in range(n) if i != j),
            "negative off-diagonal rate")
    require(sum(pi) == 1 and min(pi) > 0, "invalid positive stationary law")
    require(stationary(q, pi), "stationarity failure")
    reached = {0}
    for _ in range(n):
        reached |= {j for i in reached for j in range(n) if i != j and q[i][j] > 0}
    require(len(reached) == n, "generator not irreducible")


def adjoint(q, pi):
    n = len(q)
    return [[pi[j]*q[j][i]/pi[i] for j in range(n)] for i in range(n)]


def physical_reverse(q, pi, theta):
    star = adjoint(q, pi)
    n = len(q)
    require(sorted(theta) == list(range(n)), "Theta not a permutation")
    require(all(theta[theta[i]] == i for i in range(n)), "Theta not involutive")
    rev = [[star[theta[i]][theta[j]] for j in range(n)] for i in range(n)]
    reverse_pi = [pi[theta[i]] for i in range(n)]
    require(stationary(rev, reverse_pi), "reversed process stationary law failure")
    for i in range(n):
        for j in range(n):
            if i != j and q[i][j] > 0:
                require(q[theta[j]][theta[i]] > 0, "unpaired physical edge support")
                require(rev[i][j] > 0, "undefined finite path likelihood")
    return rev, reverse_pi


@lru_cache(None)
def factors(n):
    require(n >= 1, "prime factorization requires positive integer")
    result = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            result[p] = result.get(p, 0) + 1
            n //= p
        p = 3 if p == 2 else p + 2
    if n > 1:
        result[n] = result.get(n, 0) + 1
    return result


def add_log(record, coefficient, argument):
    """Add coefficient * log(argument), exactly in the prime-log basis."""
    coefficient, argument = F(coefficient), F(argument)
    require(argument > 0, "nonpositive log argument")
    for sign, value in [(1, argument.numerator), (-1, argument.denominator)]:
        for prime, exponent in factors(value).items():
            record[prime] = record.get(prime, F(0)) + sign*exponent*coefficient
            if record[prime] == 0:
                del record[prime]


def path_kl_decomposition(q, pi, theta):
    """D(P[0,T] || physical reversal P[0,T]) = B + T*(J + H)."""
    rev, reverse_pi = physical_reverse(q, pi, theta)
    boundary, jumps = {}, {}
    holding = F(0)
    for i in range(len(q)):
        add_log(boundary, pi[i], pi[i]/reverse_pi[i])
        holding += pi[i]*(q[i][i]-rev[i][i])
        for j in range(len(q)):
            if i != j and q[i][j] > 0:
                add_log(jumps, pi[i]*q[i][j], q[i][j]/rev[i][j])
    return {"boundary": boundary, "jumps": jumps, "holding": holding,
            "reverse_generator": rev, "reverse_pi": reverse_pi}


def orientation_lift(q, pi, epsilon, kappa):
    n = len(q)
    star = adjoint(q, pi)
    a, b = kappa*epsilon, kappa*(1-epsilon)
    lifted = [[F(0) for _ in range(2*n)] for _ in range(2*n)]
    for orientation, base, switch in [(0, q, a), (1, star, b)]:
        for x in range(n):
            z = orientation*n+x
            for y in range(n):
                if x != y:
                    lifted[z][orientation*n+y] = base[x][y]
            lifted[z][(1-orientation)*n+x] = switch
            lifted[z][z] = -sum(lifted[z])
    weights = [(1-epsilon)*p for p in pi] + [epsilon*p for p in pi]
    theta = [(1-o)*n+x for o in range(2) for x in range(n)]
    return lifted, weights, theta


def clock_lift(q, pi, theta, clock):
    n = len(q)
    lifted = [[F(0) for _ in range(2*n)] for _ in range(2*n)]
    for z in range(n):
        invisible = clock+q[z][z]
        require(invisible > 0, "invisible bit toggle is not strictly positive")
        for bit in range(2):
            i = 2*z+bit
            for w in range(n):
                if z != w:
                    lifted[i][2*w+bit] = q[z][w]
            lifted[i][2*z+(1-bit)] = invisible
            lifted[i][i] = -clock
    weights = [pi[z]/2 for z in range(n) for _ in range(2)]
    flip = [2*theta[z]+bit for z in range(n) for bit in range(2)]
    projection = [[F(z == w) for w in range(n)] for z in range(n) for _ in range(2)]
    require(mm(lifted, projection) == mm(projection, q),
            "strong lumpability generator intertwining failure")
    aggregate = [sum(weights[2*z:2*z+2]) for z in range(n)]
    require(aggregate == pi, "initial-law projection failure")
    return lifted, weights, flip


def log_core_interval(x, terms=36):
    """Exact interval for log(x), for 1<=x<=2."""
    require(1 <= x <= 2, "log range-reduction failure")
    z = (x-1)/(x+1)
    power = z
    lower = F(0)
    for j in range(terms):
        lower += 2*power/(2*j+1)
        power *= z*z
    upper = lower + 2*power/((2*terms+1)*(1-z*z))
    return lower, upper


@lru_cache(None)
def log_interval(x):
    x = F(x)
    require(x > 0, "nonpositive log interval input")
    k = 0
    while x >= 2:
        x /= 2
        k += 1
    while x < 1:
        x *= 2
        k -= 1
    lo, hi = log_core_interval(x)
    lo2, hi2 = log_core_interval(F(2))
    if k >= 0:
        return lo+k*lo2, hi+k*hi2
    return lo+k*hi2, hi+k*lo2


def log_sum_interval(coefficients, constant=F(0)):
    lower = upper = F(constant)
    for prime, coefficient in coefficients.items():
        lo, hi = log_interval(F(prime))
        if coefficient >= 0:
            lower += coefficient*lo
            upper += coefficient*hi
        else:
            lower += coefficient*hi
            upper += coefficient*lo
    return lower, upper


def exp_minus_interval(x, degree=40):
    require(x >= 0 and degree % 2 == 0, "invalid exponential interval inputs")
    term = total = F(1)
    for j in range(1, degree+1):
        term *= -x/j
        total += term
    error = x**(degree+1)/factorial(degree+1)
    return max(F(0), total-error), min(F(1), total)


def decimal_outward(x, rounding):
    with localcontext() as context:
        context.prec = 26
        context.rounding = rounding
        return str(Decimal(x.numerator)/Decimal(x.denominator))


def display_interval(interval):
    lo, hi = interval
    require(lo <= hi, "reversed interval")
    return {"lower": decimal_outward(lo, ROUND_FLOOR),
            "upper": decimal_outward(hi, ROUND_CEILING)}


def serialize_logs(coefficients):
    return {str(p): str(c) for p, c in sorted(coefficients.items())}


def serialize_matrix(q):
    return [[str(v) for v in row] for row in q]


def main():
    # Unequal stationary masses and unequal escape rates; all three net
    # cycle fluxes are 1/12 and all clockwise/counterclockwise ratios are 2.
    pi = [F(1,2), F(1,3), F(1,6)]
    q = [
        [F(-1,2), F(1,3), F(1,6)],
        [F(1,4), F(-3,4), F(1,2)],
        [F(1), F(1,2), F(-3,2)],
    ]
    verify_generator(q, pi)
    original = path_kl_decomposition(q, pi, list(range(3)))
    require(original["boundary"] == {} and original["holding"] == 0,
            "ordinary stationary reversal decomposition failure")
    require(original["jumps"] == {2: F(1,4)}, "baseline not the intended nonequilibrium chain")
    exits = [-q[x][x] for x in range(3)]
    clock = max(exits)+1
    c = [clock-rate for rate in exits]
    require(min(c) >= 1, "clock reserve below one")
    cases = []
    full_generators = []
    for value in [F(1,4), F(1,16), F(1,64)]:
        epsilon = kappa = value
        u, d = 1-epsilon, 1-2*epsilon
        a, b = kappa*epsilon, kappa*u
        base, mu, theta = orientation_lift(q, pi, epsilon, kappa)
        verify_generator(base, mu)
        base_kl = path_kl_decomposition(base, mu, theta)
        expected_boundary = {}
        add_log(expected_boundary, d, u/epsilon)
        require(base_kl["boundary"] == expected_boundary,
                "orientation preparation divergence formula failure")
        require(base_kl["jumps"] == {}, "orientation switch log terms do not cancel")
        require(base_kl["holding"] == kappa*d*d,
                "orientation intrinsic rate formula failure")
        require(mu != [mu[theta[z]] for z in range(len(mu))],
                "test accidentally removed preparation asymmetry")

        fixed, nu, theta_fixed = clock_lift(base, mu, theta, clock)
        verify_generator(fixed, nu)
        require(all(-fixed[z][z] == clock for z in range(len(fixed))),
                "microscopic escape clocks differ")
        fixed_kl = path_kl_decomposition(fixed, nu, theta_fixed)
        require(fixed_kl["boundary"] == expected_boundary,
                "clock lift changed preparation divergence")
        require(fixed_kl["holding"] == 0, "constant clocks left a holding contribution")
        expected_clock_logs = {}
        for p, reserve in zip(pi, c):
            add_log(expected_clock_logs, p*d*reserve,
                    (reserve-kappa*epsilon)/(reserve-kappa*u))
        require(fixed_kl["jumps"] == expected_clock_logs,
                "constant-clock intrinsic log-coefficient formula failure")
        sigma_interval = log_sum_interval(expected_clock_logs)
        sigma_base = kappa*d*d
        upper_bound = kappa*d*d/(1-kappa)
        require(sigma_interval[0] >= sigma_base,
                "certified clock rate below analytic orientation rate")
        require(sigma_interval[1] <= upper_bound,
                "certified clock rate exceeds claimed bound")
        boundary_interval = log_sum_interval(expected_boundary)

        # The exact orientation eigenmode survives the bit lift.
        mode_base = [epsilon]*3 + [-u]*3
        require(mv(base, mode_base) == [-kappa*x for x in mode_base],
                "base orientation relaxation mode failure")
        mode_fixed = [x for x in mode_base for _ in range(2)]
        require(mv(fixed, mode_fixed) == [-kappa*x for x in mode_fixed],
                "clock lift changed orientation relaxation mode")

        # These are the exact ingredients of the analytic path coupling.
        require(sum(mu[3:]) == epsilon, "incorrect initial wrong-orientation mass")
        for z in range(3):
            require(sum(base[z][3:]) == a, "plus escape-to-minus rate not constant")
        for z in range(6):
            if z//2 < 3:
                require(sum(fixed[z][6:]) == a,
                        "clock lift changed plus escape-to-minus rate")
        tv_bounds = {}
        full_kl = {}
        for horizon in [F(1), F(10)]:
            e_lo, e_hi = exp_minus_interval(a*horizon)
            tv_bounds[str(horizon)] = display_interval((1-u*e_hi, 1-u*e_lo))
            full_kl[str(horizon)] = display_interval((
                boundary_interval[0]+horizon*sigma_interval[0],
                boundary_interval[1]+horizon*sigma_interval[1]))

        cases.append({
            "epsilon": str(epsilon), "kappa": str(kappa),
            "states_orientation": len(base), "states_constant_clock": len(fixed),
            "clock": str(clock), "a": str(a), "b": str(b),
            "orientation_intrinsic_rate": str(sigma_base),
            "constant_clock_intrinsic_rate_interval": display_interval(sigma_interval),
            "constant_clock_rate_upper_bound": str(upper_bound),
            "boundary_divergence_interval": display_interval(boundary_interval),
            "boundary_prime_log_coefficients": serialize_logs(expected_boundary),
            "clock_rate_prime_log_coefficients": serialize_logs(expected_clock_logs),
            "orientation_relaxation_time": str(1/kappa),
            "mean_plus_orientation_sojourn": str(1/a),
            "analytic_visible_path_TV_upper_bound_intervals": tv_bounds,
            "full_clock_lift_reversal_KL_intervals": full_kl,
            "checks": "all exact generator, stationarity, support, clock, lumpability, eigenmode, and log-identity checks passed"
        })
        full_generators.append({
            "epsilon": str(epsilon), "kappa": str(kappa),
            "orientation_generator": serialize_matrix(base),
            "orientation_stationary": list(map(str,mu)), "orientation_theta": theta,
            "clock_generator": serialize_matrix(fixed),
            "clock_stationary": list(map(str,nu)), "clock_theta": theta_fixed
        })

    record = {
        "status": "all scoped exact checks passed",
        "arithmetic": "Fraction algebra; exact prime-log identities; rational log and exponential intervals with outward Decimal display",
        "no_sampling": True,
        "baseline": {
            "generator": serialize_matrix(q), "stationary": list(map(str,pi)),
            "escape_rates": list(map(str,exits)),
            "ordinary_entropy_rate": "(1/4) log 2",
            "ordinary_entropy_rate_interval": display_interval(log_sum_interval({2:F(1,4)})),
            "constant_clock": str(clock), "reserves": list(map(str,c))
        },
        "cases": cases,
        "analytic_claims_used": [
            "finite-state generator intertwining implies the semigroup identity for every time by its power series",
            "physical path reversal KL equals initial parity KL plus duration times jump-log and holding-rate contributions",
            "couple on the plus orientation until its first minus switch; observation and bit projection contract TV",
            "log(1+x)<=x and c_x>=1 give sigma_clock<=kappa(1-2epsilon)^2/(1-kappa)"
        ],
        "scope": [
            "sustained reversal-divergence rate can vanish while full finite-window KL does not",
            "stationary lifted distribution is not Theta-invariant; the boundary B is essential",
            "state count and microscopic escape clock remain fixed within this parameter family",
            "orientation memory, preparation asymmetry, and sampling/mixing requirements are not free",
            "no native physical implementation, thermodynamic work cost, or empirical measurement is claimed"
        ]
    }
    (HERE/"ORIENTATION_MEMORY_EXACT_CHECKS.json").write_text(json.dumps(record,indent=2)+"\n")
    (HERE/"ORIENTATION_MEMORY_EXACT_GENERATORS.json").write_text(
        json.dumps(full_generators,indent=2)+"\n")
    print(json.dumps(record,indent=2))


if __name__ == "__main__":
    main()
