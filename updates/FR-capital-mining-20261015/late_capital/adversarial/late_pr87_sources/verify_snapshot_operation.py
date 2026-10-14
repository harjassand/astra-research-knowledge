#!/usr/bin/env python3
"""Exact rational finite certificates; no simulation or empirical claim."""
from dataclasses import dataclass
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from math import factorial, ceil, log
from pathlib import Path
import hashlib
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F

    def __post_init__(self):
        need(self.lo <= self.hi, "reversed interval")

    @staticmethod
    def point(value):
        return Interval(F(value), F(value))

    def __add__(self, other):
        other = other if isinstance(other, Interval) else Interval.point(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Interval) else -F(other))

    def __mul__(self, other):
        other = other if isinstance(other, Interval) else Interval.point(other)
        products = [a*b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return Interval(min(products), max(products))

    __rmul__ = __mul__


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def multiply(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def exp_negative(x, terms=30):
    need(0 <= x <= 1, "alternating-series range")
    term, partial = F(1), F(1)
    for k in range(1, terms+1):
        term *= -x/F(k)
        partial += term
    next_term = term*(-x)/F(terms+1)
    return Interval(min(partial, partial+next_term), max(partial, partial+next_term))


def transition(q, t, terms=24):
    n = len(q)
    need(all(sum(row) == 0 for row in q), "generator rows")
    need(all(q[i][j] >= 0 for i in range(n) for j in range(n) if i != j), "rates")
    rate = max(-q[i][i] for i in range(n))
    need(rate > 0, "positive uniformization rate")
    a = [[F(i == j)+q[i][j]/rate for j in range(n)] for i in range(n)]
    need(all(v >= 0 for row in a for v in row), "stochastic uniformizer")
    x = rate*t
    e = exp_negative(x)
    power, weight = eye(n), F(1)
    partial = eye(n)
    for k in range(1, terms+1):
        power = multiply(power, a)
        weight *= x/F(k)
        partial = [[partial[i][j]+weight*power[i][j] for j in range(n)] for i in range(n)]
    tail = x**(terms+1)/F(factorial(terms+1))/(1-x/F(terms+2))
    return [[Interval(e.lo*partial[i][j], e.hi*partial[i][j]+tail)
             for j in range(n)] for i in range(n)]


def average_transition(q, gaps):
    result = None
    for probability, t in gaps:
        current = transition(q, t)
        if result is None:
            result = [[Interval.point(0) for _ in row] for row in current]
        result = [[result[i][j]+probability*current[i][j]
                   for j in range(len(q))] for i in range(len(q))]
    need(sum(probability for probability, _ in gaps) == 1, "clock normalization")
    return result


def negative_log_one_minus(x, terms=60):
    need(0 <= x.lo <= x.hi < 1, "log certificate domain")
    lower = sum(x.lo**k/F(k) for k in range(1, terms+1))
    upper = sum(x.hi**k/F(k) for k in range(1, terms+1))
    upper += x.hi**(terms+1)/(F(terms+1)*(1-x.hi))
    return Interval(lower, upper)


def decimal(value, rounding=ROUND_FLOOR):
    with localcontext() as ctx:
        ctx.prec = 48
        ctx.rounding = rounding
        return str(Decimal(value.numerator)/Decimal(value.denominator))


def show(interval):
    return {"lower_decimal": decimal(interval.lo, ROUND_FLOOR),
            "upper_decimal": decimal(interval.hi, ROUND_CEILING)}


def certificate(q, pi, b, r, gaps):
    p = average_transition(q, gaps)
    mean = sum(pi[i]*p[i][j]*p[j][k]*b[j]*(b[i]-r)*(b[k]-r)
               for i in range(len(q)) for j in range(len(q)) for k in range(len(q)))
    duration = sum(probability*t for probability, t in gaps)
    d = -mean
    result = {"mean_score": show(mean), "D": show(d), "mean_gap": str(duration),
              "clock": [[str(probability), str(t)] for probability, t in gaps],
              "predeclared_r": str(r), "binary_emission_probabilities": list(map(str, b))}
    if d.lo > 0:
        c = r*(1-r)
        bound = negative_log_one_minus(d*(1/c))*(1/duration)
        result["certified_floor"] = show(bound)
        result["floor_above_17_over_100"] = bound.lo > F(17,100)
        result["iid_windows_for_half_expected_margin_at_alpha_0_05_planning_only"] = ceil(
            float(max(r, 1-r))**2*log(20)/(2*(float(d.lo)/2)**2))
        return result, bound, p
    result["certified_floor"] = None
    return result, None, p


def verify_odd_lift(q, pi):
    n = len(q)
    reverse = [[pi[j]*q[j][i]/pi[i] for j in range(n)] for i in range(n)]
    lift = [[F(0) for _ in range(2*n)] for _ in range(2*n)]
    for branch, generator in enumerate((q, reverse)):
        for i in range(n):
            for j in range(n):
                lift[branch*n+i][branch*n+j] = generator[i][j]
    epsilon = F(1,7)
    lift[0][n] = lift[n][0] = epsilon
    lift[0][0] -= epsilon
    lift[n][n] -= epsilon
    stationary = [v/2 for v in pi]+[v/2 for v in pi]
    theta = lambda i: (i+n) % (2*n)
    need(all(sum(row) == 0 for row in lift), "lift generator")
    need(all(sum(stationary[i]*lift[i][j] for i in range(2*n)) == 0
             for j in range(2*n)), "lift stationarity")
    need(all(stationary[i]*lift[i][j] == stationary[theta(j)]*lift[theta(j)][theta(i)]
             for i in range(2*n) for j in range(2*n)), "parity detailed balance")
    need(all(lift[i][i] == lift[theta(i)][theta(i)] for i in range(2*n)), "holding parity")
    # Exact finite check of phase-type density derivatives; the all-time identity is analytic.
    derivatives = []
    for generator in (q, reverse):
        alpha = [[generator[0][j]/(-generator[0][0]) for j in range(1,n)]]
        block = [[generator[i][j] for j in range(1,n)] for i in range(1,n)]
        exits = [[generator[i][0]] for i in range(1,n)]
        values = []
        for _ in range(10):
            values.append(multiply(alpha, exits)[0][0])
            alpha = multiply(alpha, block)
        derivatives.append(values)
    need(derivatives[0] == derivatives[1], "PH reverse finite checks")
    return {"states": 2*n, "reset_flip_rate": str(epsilon),
            "stationarity_and_generalized_balance": "exact rational PASS",
            "B_dwell_first_10_density_derivatives": list(map(str, derivatives[0])),
            "theta_path_EP": "exactly 0 under the formal parity reversal",
            "physical_realization": "NOT_ESTABLISHED",
            "full_observed_law_identity": "analytic proof; finite checks are not the proof"}


def main():
    qrate = F(1,20)
    q = [[-(1+qrate),F(1),qrate],[qrate,-(1+qrate),F(1)],[F(1),qrate,-(1+qrate)]]
    pi, b, r = [F(1,3)]*3, [F(0),F(1),F(1)], F(9,10)
    fixed, lower, p = certificate(q,pi,b,r,[(F(1),F(3,10))])
    need(lower is not None and lower.lo > F(17,100), "strict rational floor >0.17")
    clock, _, _ = certificate(q,pi,b,r,[(F(1,2),F(1,5)),(F(1,2),F(2,5))])
    noisy, _, _ = certificate(q,pi,[F(1,20),F(19,20),F(19,20)],F(43,50),[(F(1),F(3,10))])
    equilibrium_q = [[F(-1),F(1,2),F(1,2)],[F(1,2),F(-1),F(1,2)],[F(1,2),F(1,2),F(-1)]]
    equilibrium, null_bound, _ = certificate(equilibrium_q,pi,b,r,[(F(1),F(3,10))])
    need(null_bound is None and F(equilibrium["mean_score"]["lower_decimal"]) > 0,
         "equilibrium control must not generate positive floor")
    # Matching gap marginals without independence is insufficient, even at equilibrium.
    eq2 = [[F(-1),F(1)],[F(1),F(-1)]]
    short, long = transition(eq2,F(1,10)), transition(eq2,F(1))
    r_bad, b2 = F(3,4), [F(0),F(1)]
    bad_score = sum(F(1,2)*short[i][j]*long[j][k]*b2[j]*(b2[i]-r_bad)*(b2[k]-r_bad)
                    for i in range(2) for j in range(2) for k in range(2))
    need(bad_score.hi < 0, "correlated-clock equilibrium falsifier")
    triple = {}
    for x in (0,1):
        for y in (0,1):
            for z in (0,1):
                value = sum(pi[i]*p[i][j]*p[j][k] for i in range(3)
                            for j in range(3) for k in range(3)
                            if (int(b[i]),int(b[j]),int(b[k])) == (x,y,z))
                triple[f"{x}{y}{z}"] = show(value)
    result = {"schema":"astra.operational-closure.exact-snapshot-check.v1",
              "scope":"supplied finite mathematical fixtures and rational enclosures; no experiment",
              "fixed_gap":fixed,"iid_matched_two_point_clock":clock,
              "independent_memoryless_5_percent_readout_noise":noisy,
              "equilibrium_negative_control":equilibrium,"observable_triple_probabilities":triple,
              "correlated_or_unmatched_clock_false_positive_control":{
                  "equilibrium_generator":[["-1","1"],["1","-1"]],
                  "gap_pairs":[["1/10","1"],["1","1/10"]],
                  "pair_probabilities":["1/2","1/2"],"r":"3/4",
                  "negative_score_despite_zero_EP":show(bad_score),
                  "lesson":"identical gap marginals and exchangeability do not replace independence"},
              "odd_parity_countermodel":verify_odd_lift(q,pi),
              "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "status":"PASS", "novelty":"UNKNOWN"}
    output = Path(__file__).with_name("SNAPSHOT_EXACT_RESULTS.json")
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"PASS","fixed_gap_floor":fixed["certified_floor"],
                      "iid_clock_floor":clock["certified_floor"],"output":str(output)},indent=2))


if __name__ == "__main__":
    main()
