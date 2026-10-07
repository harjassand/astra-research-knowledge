"""Exact acquired Foster certificates for two-layer catalytic birth/death.

Only standard-library rational arithmetic is used. The verifier computes the
generator from raw reaction vectors, independently of the displayed bound.
This is a specialized complete recognizer, not a generic CRN synthesizer.
"""
from fractions import Fraction as F
from itertools import product
import json
import pathlib
import time


def rat(value):
    return F(str(value))


def ceil_rat(value):
    return -((-value.numerator) // value.denominator)


def acquire(spec):
    roots = spec["roots"]
    children = spec["children"]
    names = [r["name"] for r in roots] + [j["name"] for j in children]
    if not roots or len(set(names)) != len(names):
        raise ValueError("Nonempty roots and unique disjoint species required")
    root_names = {r["name"] for r in roots}
    b = {r["name"]: rat(r["birth"]) for r in roots}
    delta = {r["name"]: rat(r["death"]) for r in roots}
    if any(v <= 0 for v in [*b.values(), *delta.values()]):
        raise ValueError("Every root needs positive immigration and death")
    c, gamma, edges = {}, {}, {}
    for child in children:
        name = child["name"]
        parents = child["parents"]
        if not parents or not set(parents) <= root_names:
            raise ValueError("Every child needs a nonempty subset of roots")
        edges[name] = {i: (rat(k["birth"]), rat(k["death"]))
                       for i, k in parents.items()}
        if any(v <= 0 for pair in edges[name].values() for v in pair):
            raise ValueError("Every catalytic channel must have both positive rates")
        beta_min = min(pair[1] for pair in edges[name].values())
        delta_max = max(delta[i] for i in parents)
        c[name] = min(F(1), beta_min / delta_max)
        gamma[name] = min(c[name] * sum(b[i] for i in parents) / 2,
                          beta_min / 2)
    w = {i: (1 + sum((1 + c[j]) * edges[j][i][0]
                      for j in edges if i in edges[j])) / delta[i]
         for i in root_names}
    constant = sum(w[i] * b[i] for i in root_names)
    decay = min([1 / w[i] for i in root_names]
                + [gamma[j] / (1 + c[j]) for j in edges])
    gamma_min = min([F(1), *gamma.values()])
    core_radius = max(1, ceil_rat((constant + 1) / gamma_min))
    stationary_upper_means = {i: b[i] / delta[i] for i in root_names}
    stationary_upper_means.update(
        {j: max(a / z for a, z in edges[j].values()) for j in edges})
    killing_rates = {j: sum(b[i] * z / (delta[i] + z)
                            for i, (_, z) in edges[j].items())
                     for j in edges}
    return {"spec": spec, "names": names, "b": b, "delta": delta,
            "edges": edges, "c": c, "gamma": gamma, "w": w,
            "C": constant, "lambda": decay, "core_radius": core_radius,
            "stationary_upper_means": stationary_upper_means,
            "killing_rates": killing_rates}


def potential(cert, state):
    x = dict(zip(cert["names"], state))
    answer = sum(cert["w"][i] * x[i] for i in cert["w"])
    for j, parents in cert["edges"].items():
        s = sum(x[i] for i in parents)
        answer += (1 + cert["c"][j] / (s + 1)) * x[j]
    return answer


def raw_reactions(cert):
    names = cert["names"]
    out = []
    for i in cert["w"]:
        source = [0] * len(names)
        target = source.copy()
        target[names.index(i)] = 1
        out.append((tuple(source), tuple(target), cert["b"][i]))
        out.append((tuple(target), tuple(source), cert["delta"][i]))
    for j, parents in cert["edges"].items():
        for i, (alpha, beta) in parents.items():
            source = [0] * len(names)
            source[names.index(i)] = 1
            target = source.copy()
            target[names.index(j)] = 1
            out.append((tuple(source), tuple(target), alpha))
            out.append((tuple(target), tuple(source), beta))
    return out


def falling_factorial(state, source):
    answer = 1
    for n, degree in zip(state, source):
        for shift in range(degree):
            answer *= max(0, n - shift)
    return answer


def raw_generator(cert, state):
    value = potential(cert, state)
    result = F(0)
    for source, target, rate in raw_reactions(cert):
        propensity = rate * falling_factorial(state, source)
        if propensity:
            new = tuple(n + z - y for n, y, z in zip(state, source, target))
            result += propensity * (potential(cert, new) - value)
    return result


def serialized(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {k: serialized(v) for k, v in obj.items()}
    if isinstance(obj, (tuple, list)):
        return [serialized(v) for v in obj]
    return obj


def verify():
    fixtures = [
        {"roots": [{"name": "A", "birth": "1", "death": "1"}],
         "children": [{"name": "B", "parents": {
             "A": {"birth": "1", "death": "1"}}}]},
        # Different ratios 1 and 2 force absence of complex balance.
        {"roots": [{"name": "A", "birth": "1", "death": "1"},
                   {"name": "C", "birth": "1", "death": "1"}],
         "children": [{"name": "B", "parents": {
             "A": {"birth": "1", "death": "1"},
             "C": {"birth": "2", "death": "1"}}}]},
        {"roots": [{"name": "A", "birth": "1/7", "death": "13/3"},
                   {"name": "C", "birth": "11/5", "death": "2/9"}],
         "children": [{"name": "B", "parents": {
             "A": {"birth": "1/17", "death": "1/19"},
             "C": {"birth": "7/3", "death": "2/11"}}},
                      {"name": "D", "parents": {
             "C": {"birth": "23/5", "death": "5/29"}}}]},
    ]
    checked = 0
    zero_catalyst_checks = 0
    smallest_slack = None
    certificates = []
    for spec in fixtures:
        cert = acquire(spec)
        certificates.append(cert)
        for state in product(range(6), repeat=len(cert["names"])):
            lv = raw_generator(cert, state)
            v = potential(cert, state)
            x = dict(zip(cert["names"], state))
            h = (sum(x[i] for i in cert["w"])
                 + sum(cert["gamma"][j] * x[j] for j in cert["edges"]))
            slack = cert["C"] - h - lv
            assert slack >= 0, (state, lv, cert["C"] - h)
            assert lv <= cert["C"] - cert["lambda"] * v
            checked += 1
            if all(x[i] == 0 for i in cert["w"]):
                zero_catalyst_checks += 1
            smallest_slack = (slack if smallest_slack is None
                              else min(slack, smallest_slack))
    simple = certificates[0]
    # A nonzero rational state on the gate face has negative drift for large B.
    boundary_lv = raw_generator(simple, (0, 60))
    assert boundary_lv == -27
    # Exponentiating this rational V is an invalid shortcut. At (1,60),
    # theta=2 log 2 makes all four jump multipliers rational.
    exponential_drift_ratio = (F(2**54) - 1 + F(1, 2**14) - 1
                               + F(8) - 1 + 60 * (F(1, 8) - 1))
    assert exponential_drift_ratio > 0
    # Syntax rejection: a downstream catalyst is outside the two-layer promise.
    invalid = {"roots": fixtures[0]["roots"], "children": [
        *fixtures[0]["children"],
        {"name": "C", "parents": {"B": {"birth": "1", "death": "1"}}}]}
    try:
        acquire(invalid)
    except ValueError:
        rejected = True
    else:
        raise AssertionError("Invalid second-layer catalyst was admitted")
    return {"status": "EXACT_FINITE_DIAGNOSTIC_PASSED",
            "checked_states": checked,
            "zero_catalyst_states": zero_catalyst_checks,
            "smallest_slack": smallest_slack,
            "boundary_example_LV_at_0_60": boundary_lv,
            "exponential_V_counterexample_drift_ratio": exponential_drift_ratio,
            "out_of_class_rejected": rejected,
            "certificates": certificates}


if __name__ == "__main__":
    started = time.monotonic()
    report = verify()
    report["elapsed_seconds"] = time.monotonic() - started
    destination = pathlib.Path(__file__).with_name("certificate_checks.json")
    destination.write_text(json.dumps(serialized(report), indent=2) + "\n")
    print(json.dumps(serialized({k: v for k, v in report.items()
                                  if k != "certificates"}), indent=2))
