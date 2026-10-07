#!/usr/bin/env python3
"""Exact, dependency-free bounded PL mass-action certificate checker.

This is a deliberately small reference implementation, not an efficient solver.
Every numerical quantity used for acceptance is a fractions.Fraction. Rational
powers use outward dyadic bounds obtained by integer comparisons. A bounded
run may return UNKNOWN. REFUTED requires an exact or rigorous interval witness.
The report explains the theorem proved by a CERTIFIED result.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import argparse
import copy
import json
import time


def q(x):
    if isinstance(x, float):
        raise ValueError("Supply rationals as integers or strings, never floats")
    return Q(x)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def rref(matrix):
    a = [list(row) for row in matrix]
    if not a:
        return a, []
    rows, cols = len(a), len(a[0])
    pivots, k = [], 0
    for j in range(cols):
        pivot = next((i for i in range(k, rows) if a[i][j]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        scale = a[k][j]
        a[k] = [z / scale for z in a[k]]
        for i in range(rows):
            if i != k and a[i][j]:
                scale = a[i][j]
                a[i] = [z - scale * w for z, w in zip(a[i], a[k])]
        pivots.append(j)
        k += 1
        if k == rows:
            break
    return a, pivots


def solve_unique(matrix, rhs, n):
    """Return unique rational solution of a possibly overdetermined system."""
    aug = [list(row) + [b] for row, b in zip(matrix, rhs)]
    reduced, pivots = rref(aug)
    if n in pivots or any(not any(row[:n]) and row[n] for row in reduced):
        return None
    if len([j for j in pivots if j < n]) != n:
        return None
    ans = [Q(0)] * n
    for row, pivot in zip(reduced, pivots):
        if pivot < n:
            ans[pivot] = row[n]
    return tuple(ans)


def nullspace(matrix, d):
    reduced, pivots = rref(matrix)
    basis = []
    for free in (j for j in range(d) if j not in pivots):
        v = [Q(0)] * d
        v[free] = Q(1)
        for row, pivot in zip(reduced, pivots):
            v[pivot] = -row[free]
        basis.append(tuple(v))
    return basis


def box_inequalities(box):
    d = len(box)
    out = []
    for i, (lo, hi) in enumerate(box):
        a = [Q(0)] * d
        a[i] = Q(1)
        out.append((tuple(a), -lo))
        a = [Q(0)] * d
        a[i] = Q(-1)
        out.append((tuple(a), hi))
    return out


def vertices(equations, rhs, inequalities, box):
    """Exact vertices of a bounded polyhedron, including lower-dimensional ones.

    Inequalities are a.x+b >= 0. Boundedness is supplied by box. Enumerating
    all bases is expensive but complete; an empty vertex list means empty.
    """
    d = len(box)
    inequalities = list(inequalities) + box_inequalities(box)
    dim = d - len(equations)
    points = set()
    for basis in combinations(range(len(inequalities)), dim):
        a = list(equations) + [inequalities[i][0] for i in basis]
        b = list(rhs) + [-inequalities[i][1] for i in basis]
        v = solve_unique(a, b, d)
        if v is not None and all(dot(normal, v) + offset >= 0
                                 for normal, offset in inequalities):
            points.add(v)
    return sorted(points)


def conic_witness(inequalities, equations, rhs, target):
    """Farkas witness target = sum nonnegative inequality/equality columns.

    Columns are (a,b) for inequalities, both signs of (E,-rhs) for equalities,
    and (0,1). The last column permits a nonnegative constant residual.
    """
    d = len(target) - 1
    columns = [tuple(a) + (b,) for a, b in inequalities]
    names = ["inequality:" + str(i) for i in range(len(inequalities))]
    for i, (a, b) in enumerate(zip(equations, rhs)):
        columns += [tuple(a) + (-b,), tuple(-z for z in a) + (b,)]
        names += ["equation:+" + str(i), "equation:-" + str(i)]
    columns.append(tuple([Q(0)] * d + [Q(1)]))
    names.append("constant")
    if not any(target):
        return []
    for size in range(1, min(d + 1, len(columns)) + 1):
        for chosen in combinations(range(len(columns)), size):
            matrix = [[columns[j][i] for j in chosen] for i in range(d + 1)]
            weights = solve_unique(matrix, target, size)
            if weights is not None and all(z >= 0 for z in weights):
                return [{"column": names[j], "vector": columns[j], "weight": w}
                        for j, w in zip(chosen, weights) if w]
    return None


def verify_conic(witness, target):
    if witness is None or any(row["weight"] < 0 for row in witness):
        return False
    return all(sum((row["weight"] * row["vector"][i] for row in witness), Q(0))
               == target[i] for i in range(len(target)))


def power_bounds(base, exponent, bits):
    """Rigorous rational bounds for base**exponent, base >= 0, exponent >= 0."""
    if base < 0 or exponent < 0:
        raise ValueError("The checker supports nonnegative complexes and boxes")
    p, n = exponent.numerator, exponent.denominator
    if not p:
        return Q(1), Q(1)
    if n == 1:
        value = base ** p
        return value, value
    value, scale = base ** p, 1 << bits
    target = value.numerator * scale ** n
    denom = value.denominator
    lo, hi = 0, 1
    while hi ** n * denom <= target:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** n * denom <= target:
            lo = mid
        else:
            hi = mid
    lower = Q(lo, scale)
    upper = lower if lo ** n * denom == target else Q(hi, scale)
    return lower, upper


def monomial_bounds(box, source, bits):
    lo = hi = Q(1)
    for (left, right), exponent in zip(box, source):
        left_bound, _ = power_bounds(left, exponent, bits)
        _, right_bound = power_bounds(right, exponent, bits)
        lo *= left_bound
        hi *= right_bound
    return lo, hi


def derivative_bounds(normal, reactions, kappa, cap, box, bits):
    """Minimize each independent rate exactly before interval bounding in x."""
    lower = upper = Q(0)
    rates = []
    for source, nu in reactions:
        signed = dot(normal, nu)
        rate = kappa if signed >= 0 else cap
        rates.append(rate)
        coeff = signed * rate
        mlo, mhi = monomial_bounds(box, source, bits)
        if coeff >= 0:
            lower += coeff * mlo
            upper += coeff * mhi
        else:
            lower += coeff * mhi
            upper += coeff * mlo
    return lower, upper, rates


def parse(spec):
    c = tuple(map(q, spec["c"]))
    d = len(c)
    if not d or min(c) <= 0:
        raise ValueError("c must be a positive rational vector")
    kappa, cap, delta = map(q, (spec["kappa"], spec["K"], spec["delta"]))
    if not 0 < kappa <= cap or delta <= 0:
        raise ValueError("Require 0 < kappa <= K and delta > 0")
    reactions = []
    for edge in spec["reactions"]:
        y, target = tuple(map(q, edge["source"])), tuple(map(q, edge["target"]))
        if len(y) != d or len(target) != d or min(y + target) < 0:
            raise ValueError("Complexes must be nonnegative rational d-vectors")
        reactions.append((y, tuple(z - w for z, w in zip(target, y))))
    labels = [(tuple(map(q, row["normal"])), q(row["offset"]))
              for row in spec["labels"]]
    if any(len(a) != d for a, _ in labels):
        raise ValueError("Wrong label dimension")
    if (tuple([Q(0)] * d), Q(0)) not in labels:
        raise ValueError("Include the constant zero plateau label")
    outer = tuple(tuple(map(q, row)) for row in spec["outer_box"])
    inner = tuple(tuple(map(q, row)) for row in spec["inner_box"])
    margin = q(spec["containment_margin"])
    if len(inner) != d or len(outer) != d or margin <= 0:
        raise ValueError("Boxes and containment margin malformed")
    for (ol, oh), (il, ih) in zip(outer, inner):
        if not 0 <= ol < il < ih < oh or il <= 0 or il + margin >= ih - margin:
            raise ValueError("Inner positive box must lie strictly inside outer box")
    equations = nullspace([nu for _, nu in reactions], d)
    rhs = [dot(row, c) for row in equations]
    return c, reactions, labels, outer, inner, margin, equations, rhs, kappa, cap, delta


def check(spec, maxdepth=8, bits=32):
    started = time.perf_counter()
    (c, reactions, labels, outer, inner, margin, equations, rhs,
     kappa, cap, delta) = parse(spec)
    d = len(c)
    if any(dot(a, c) + b < 0 for a, b in labels):
        return {"status": "REFUTED", "reason": "c is outside plateau"}
    result = {"status": "CERTIFIED", "scope": "invariant_and_box_conditional_entry",
              "equations": equations, "rhs": rhs, "delta": delta,
              "containment": [], "active_cells": [], "stats": {"nodes": 0}}
    for i, (il, ih) in enumerate(inner):
        for sign, bound in ((1, -(il + margin)), (-1, ih - margin)):
            a = tuple(Q(sign) if j == i else Q(0) for j in range(d))
            target = a + (bound,)
            witness = conic_witness(labels, equations, rhs, target)
            if not verify_conic(witness, target):
                return {"status": "UNKNOWN", "reason": "No inner-box containment witness"}
            result["containment"].append({"target": target, "witness": witness})

    def recurse(normal, cell_inequalities, box, depth):
        result["stats"]["nodes"] += 1
        points = vertices(equations, rhs, cell_inequalities, box)
        if not points:
            return {"kind": "empty", "box": box}
        hull = tuple((min(v[i] for v in points), max(v[i] for v in points))
                     for i in range(d))
        lower, upper, rates = derivative_bounds(normal, reactions, kappa, cap,
                                                hull, bits + 2 * depth)
        if lower >= delta:
            return {"kind": "positive", "box": box, "hull": hull,
                    "lower_bound": lower, "vertices": points}
        # Any rigorous upper bound below delta at an active rational point
        # refutes this particular candidate, not the network's permanence.
        for point in points:
            pbox = tuple((v, v) for v in point)
            plo, phi, prates = derivative_bounds(normal, reactions, kappa, cap,
                                                 pbox, bits + 2 * depth)
            if phi < delta:
                return {"kind": "refuted", "point": point,
                        "derivative_interval": (plo, phi), "rates": prates}
        if depth >= maxdepth:
            return {"kind": "unknown", "box": hull, "lower_bound": lower,
                    "upper_bound": upper, "reason": "Subdivision/precision budget"}
        widths = [hi - lo for lo, hi in hull]
        coordinate = max(range(d), key=lambda i: widths[i])
        if not widths[coordinate]:
            return recurse(normal, cell_inequalities, hull, depth + 1)
        mid = sum(hull[coordinate], Q(0)) / 2
        left, right = list(hull), list(hull)
        left[coordinate] = (hull[coordinate][0], mid)
        right[coordinate] = (mid, hull[coordinate][1])
        children = [recurse(normal, cell_inequalities, tuple(part), depth + 1)
                    for part in (left, right)]
        return {"kind": "split", "box": box, "coordinate": coordinate,
                "midpoint": mid, "children": children}

    def tree_status(tree):
        if tree["kind"] == "split":
            statuses = [tree_status(child) for child in tree["children"]]
            return "REFUTED" if "REFUTED" in statuses else (
                "UNKNOWN" if "UNKNOWN" in statuses else "CERTIFIED")
        return {"empty": "CERTIFIED", "positive": "CERTIFIED",
                "refuted": "REFUTED", "unknown": "UNKNOWN"}[tree["kind"]]

    for i, (normal, offset) in enumerate(labels):
        if all(dot(normal, nu) == 0 for _, nu in reactions):
            # This affine value is constant on P and >= 0 at c; hence it
            # cannot be active where F < 0. Its derivative is exactly zero.
            result["active_cells"].append({"label": i, "kind": "S_perp"})
            continue
        cell = [(tuple(v - u for u, v in zip(normal, a)), b - offset)
                for a, b in labels]
        tree = recurse(normal, cell, outer, 0)
        result["active_cells"].append({"label": i, "tree": tree})
        status = tree_status(tree)
        if status == "REFUTED" or result["status"] == "CERTIFIED":
            result["status"] = status

    # Optional finite proof that the entire nonnegative class is in outer.
    # This converts conditional entry to GLOBAL entry when finite positivity
    # follows from y_i >= 1 for every reaction that consumes species i.
    if result["status"] == "CERTIFIED" and spec.get("global_bounded_class"):
        nonnegative = []
        for i in range(d):
            a = tuple(Q(1) if j == i else Q(0) for j in range(d))
            nonnegative.append((a, Q(0)))
        witnesses = []
        for a, b in box_inequalities(outer):
            target = a + (b,)
            witness = conic_witness(nonnegative, equations, rhs, target)
            if not verify_conic(witness, target):
                result["status"] = "UNKNOWN"
                result["reason"] = "The entire class was not proved bounded by outer"
                break
            witnesses.append({"target": target, "witness": witness})
        dominance = all(y[i] >= 1 for y, nu in reactions for i in range(d)
                        if nu[i] < 0)
        if result["status"] == "CERTIFIED" and not dominance:
            result["status"] = "UNKNOWN"
            result["reason"] = "Finite positive-time boundary avoidance not certified"
        if result["status"] == "CERTIFIED":
            points = vertices(equations, rhs, nonnegative, outer)
            fmin = min(dot(a, v) + b for a, b in labels for v in points)
            result["scope"] = "global_invariant_absorber_on_this_bounded_class"
            result["class_containment"] = witnesses
            result["uniform_entry_time_upper_bound"] = -fmin / delta
    result["stats"]["elapsed_seconds_diagnostic"] = time.perf_counter() - started
    return result


def stringify(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {k: stringify(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [stringify(v) for v in value]
    return value


def sample():
    return {"c": ["1/2", "1/2"], "kappa": 1, "K": 4, "delta": "5/16",
            "reactions": [{"source": [2, 0], "target": [1, 1]},
                          {"source": [0, 2], "target": [1, 1]}],
            "labels": [{"normal": [0, 0], "offset": 0},
                       {"normal": [1, 0], "offset": "-1/4"},
                       {"normal": [-1, 0], "offset": "3/4"}],
            "outer_box": [[0, 1], [0, 1]],
            "inner_box": [["1/8", "7/8"], ["1/8", "7/8"]],
            "containment_margin": "1/16", "global_bounded_class": True}


def enumerate_local_candidates(network, initial_vertices=(), maxheight=None):
    """Exhaustive rational candidate stream; extremely expensive on purpose.

    This is an implementable search specification, not a useful performance
    claim. Height simultaneously dovetails box index, label count, rational
    coefficient heights, positivity margin, root precision, and subdivision.
    For any one strict rational certificate in this box family, some later
    finite height includes its data and enough verification resources.
    """
    d = len(network["c"])
    c = tuple(map(q, network["c"]))
    initial_vertices = [tuple(map(q, v)) for v in initial_vertices]
    if any(len(v) != d for v in initial_vertices):
        raise ValueError("Initial vertices have the wrong dimension")
    stoichiometry = [tuple(q(v) - q(u) for u, v in zip(edge["source"], edge["target"]))
                     for edge in network["reactions"]]
    equations = nullspace(stoichiometry, d)
    rhs = [dot(row, c) for row in equations]
    if any(min(v) <= 0 or any(dot(a, v) != b for a, b in zip(equations, rhs))
           for v in initial_vertices):
        raise ValueError("Initial vertices must be positive and in P")
    height = 4
    while maxheight is None or height <= maxheight:
        rationals = sorted({Q(p, den) for den in range(1, height + 1)
                            for p in range(-height, height + 1)})
        # This retained pool itself has exponential dependence on dimension.
        pool = [(tuple(row[:d]), row[d]) for row in product(rationals, repeat=d + 1)
                if any(row[:d]) or row[d] != 0]
        pool = [(a, b) for a, b in pool
                if all(dot(a, v) + b >= 0 for v in [c] + initial_vertices)]
        for n in range(4, height + 1):
            if not all(Q(1, n) < v < n for v in c):
                continue
            for count in range(1, height + 1):
                for chosen in combinations(pool, count):
                    spec = copy.deepcopy(network)
                    spec.update({"delta": str(Q(1, height)),
                                 "outer_box": [[str(Q(1, n)), n] for _ in range(d)],
                                 "inner_box": [[str(Q(2, n)), str(Q(n, 2))]
                                               for _ in range(d)],
                                 "containment_margin": str(Q(1, height)),
                                 "global_bounded_class": False,
                                 "labels": [{"normal": [0] * d, "offset": 0}] +
                                           [{"normal": [str(z) for z in a],
                                             "offset": str(b)} for a, b in chosen]})
                    # At a small height the requested margin might leave no
                    # inner interval; skip it instead of throwing on parsing.
                    if Q(2, n) + Q(1, height) >= Q(n, 2) - Q(1, height):
                        continue
                    yield height, spec
        height += 1


def search_local(network, initial_vertices=(), maxheight=None, max_candidates=None):
    """Dovetailed local safety/box-entry compiler. Total only with existence."""
    count = 0
    for height, spec in enumerate_local_candidates(network, initial_vertices, maxheight):
        count += 1
        result = check(spec, maxdepth=height, bits=height)
        if result["status"] == "CERTIFIED":
            return {"status": "CERTIFIED", "candidate": spec, "certificate": result,
                    "search_candidates": count, "height": height}
        if max_candidates is not None and count >= max_candidates:
            break
    return {"status": "UNKNOWN", "reason": "Finite search budget", "search_candidates": count}


def interval_family_search(network, maxn=20):
    """Small actual acquisition search over two-species conservative intervals.

    This restricted family has no advertised completeness for other networks.
    It supplies a candidate rather than taking the interval endpoints as input.
    """
    if len(network["c"]) != 2:
        raise ValueError("Restricted search expects two species")
    mass = sum(map(q, network["c"]), Q(0))
    attempts = []
    for n in range(3, maxn + 1):
        lower = mass / n
        spec = copy.deepcopy(network)
        spec.update({"delta": str(Q(1, n)), "global_bounded_class": True,
                     "labels": [{"normal": [0, 0], "offset": 0},
                                {"normal": [1, 0], "offset": str(-lower)},
                                {"normal": [-1, 0], "offset": str(mass - lower)}],
                     "outer_box": [[0, str(mass)], [0, str(mass)]],
                     "inner_box": [[str(lower / 2), str(mass - lower / 2)]] * 2,
                     "containment_margin": str(lower / 4)})
        result = check(spec)
        attempts.append({"n": n, "status": result["status"]})
        if result["status"] == "CERTIFIED":
            return {"status": "CERTIFIED", "candidate": spec,
                    "certificate": result, "attempts": attempts}
    return {"status": "UNKNOWN", "attempts": attempts, "reason": "Finite search budget"}


def check_chain(specifications, initial_vertices, transition_margin, maxdepth=8, bits=32):
    """Finite GLOBAL absorption certificate for the supplied compact initial set.

    Q_0 contains A=conv(initial_vertices), every Q_j is invariant, and Q_j is
    strictly inside the next certificate's box. This does not assert that one
    finite chain covers every initial point of an unbounded class.
    """
    if not specifications:
        raise ValueError("A chain must be nonempty")
    parsed = [parse(spec) for spec in specifications]
    initial_vertices = [tuple(map(q, v)) for v in initial_vertices]
    margin = q(transition_margin)
    if margin <= 0 or not initial_vertices:
        raise ValueError("Supply a positive transition margin and initial vertices")
    first = parsed[0]
    c, reactions, labels, _, _, _, equations, rhs, kappa, cap, _ = first
    for data in parsed[1:]:
        if data[0] != c or data[1] != reactions or data[8:10] != (kappa, cap):
            raise ValueError("All chain entries must describe the same class and kinetics")
    for v in initial_vertices:
        if len(v) != len(c) or min(v) <= 0 or any(dot(a, v) != b for a, b in zip(equations, rhs)):
            raise ValueError("Initial polytope vertices must be positive and in P")
        if any(dot(a, v) + b < 0 for a, b in labels):
            return {"status": "REFUTED", "reason": "Initial set not inside Q_0", "point": v}
    local = [check(spec, maxdepth, bits) for spec in specifications]
    if any(row["status"] != "CERTIFIED" for row in local):
        return {"status": "UNKNOWN", "reason": "Some local chain member was not certified",
                "local_certificates": local}
    transitions, total_time = [], Q(0)
    for j in range(len(parsed) - 1):
        previous, nxt = parsed[j], parsed[j + 1]
        prev_labels, prev_outer = previous[2], previous[3]
        next_labels, next_outer, next_delta = nxt[2], nxt[3], nxt[10]
        witnesses = []
        for a, b in box_inequalities(next_outer):
            target = a + (b - margin,)
            witness = conic_witness(prev_labels, equations, rhs, target)
            if not verify_conic(witness, target):
                return {"status": "UNKNOWN", "reason": "Missing box transition containment"}
            witnesses.append({"target": target, "witness": witness})
        points = vertices(equations, rhs, prev_labels, prev_outer)
        fmin = min(dot(a, v) + b for a, b in next_labels for v in points)
        entry_time = -fmin / next_delta
        total_time += entry_time
        transitions.append({"from": j, "to": j + 1, "containment": witnesses,
                            "entry_time_upper_bound": entry_time})
    return {"status": "CERTIFIED", "scope": "global_absorption_for_supplied_initial_polytope",
            "local_certificates": local, "transitions": transitions,
            "entry_time_upper_bound": total_time}


def demo(directory):
    directory.mkdir(parents=True, exist_ok=True)
    spec = sample()
    (directory / "example.json").write_text(json.dumps(spec, indent=2) + "\n")
    result = check(spec)
    (directory / "example_certificate.json").write_text(
        json.dumps(stringify(result), indent=2) + "\n")
    wider = copy.deepcopy(spec)
    wider["K"] = 16
    bad = check(wider)
    (directory / "failed_wider_rates.json").write_text(
        json.dumps(stringify(bad), indent=2) + "\n")
    # Exercise genuine noninteger-complex rational power bounds without
    # pretending that this diagnostic proves a general theorem.
    fractional = copy.deepcopy(spec)
    fractional["reactions"] = [
        {"source": ["3/2", 0], "target": ["1/2", 1]},
        {"source": [0, "3/2"], "target": [1, "1/2"]}]
    fractional["K"] = 2
    fractional["delta"] = "1/4"
    fractional_result = check(fractional)
    (directory / "fractional_example.json").write_text(
        json.dumps(fractional, indent=2) + "\n")
    (directory / "fractional_certificate.json").write_text(
        json.dumps(stringify(fractional_result), indent=2) + "\n")
    acquired = interval_family_search({k: spec[k] for k in ("c", "kappa", "K", "reactions")})
    (directory / "acquired_interval.json").write_text(
        json.dumps(stringify(acquired), indent=2) + "\n")
    wide_plateau = copy.deepcopy(spec)
    wide_plateau.update({"global_bounded_class": False, "delta": "3/4",
                         "labels": [{"normal": [0, 0], "offset": 0},
                                    {"normal": [1, 0], "offset": "-1/16"},
                                    {"normal": [-1, 0], "offset": "15/16"}],
                         "inner_box": [["1/32", "31/32"]] * 2,
                         "containment_margin": "1/64"})
    final_plateau = copy.deepcopy(spec)
    final_plateau.update({"global_bounded_class": False,
                          "outer_box": [["1/32", "31/32"]] * 2})
    initial_vertices = [["1/16", "15/16"], ["15/16", "1/16"]]
    chain = check_chain([wide_plateau, final_plateau], initial_vertices, "1/64")
    (directory / "finite_chain.json").write_text(
        json.dumps(stringify(chain), indent=2) + "\n")
    return {"integer_example": result["status"], "integer_scope": result["scope"],
            "entry_time": result.get("uniform_entry_time_upper_bound"),
            "wider_rate_candidate": bad["status"],
            "fractional_example": fractional_result["status"],
            "fractional_scope": fractional_result["scope"],
            "acquisition_search": acquired["status"], "search_attempts": acquired["attempts"],
            "finite_chain": chain["status"], "chain_scope": chain.get("scope"),
            "chain_entry_time": chain.get("entry_time_upper_bound")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument("--demo", type=Path)
    parser.add_argument("--maxdepth", type=int, default=8)
    parser.add_argument("--bits", type=int, default=32)
    args = parser.parse_args()
    if args.demo:
        result = demo(args.demo)
    elif args.input:
        result = check(json.loads(args.input.read_text()), args.maxdepth, args.bits)
    else:
        parser.error("Supply a JSON candidate or --demo DIRECTORY")
    print(json.dumps(stringify(result), indent=2))
