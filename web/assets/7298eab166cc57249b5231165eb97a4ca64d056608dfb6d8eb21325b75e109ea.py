"""Exact rational Foster and boundary-recovery compiler for an admitted class.

No floating point solver, stationary oracle, imported CAD, or trajectory simulation.
All scientific conclusions and general complexity bounds are in INITIAL.txt.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, product
from math import ceil, prod
from pathlib import Path
import hashlib
import json
import time


@dataclass(frozen=True)
class Reaction:
    y: tuple
    yp: tuple
    lo: F
    hi: F
    name: str

    @property
    def nu(self):
        return tuple(b-a for a, b in zip(self.y, self.yp))


def reaction(y, yp, lo=1, hi=None, name=""):
    return Reaction(tuple(y), tuple(yp), F(lo), F(lo if hi is None else hi), name)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def falling(x, y):
    if any(a < b for a, b in zip(x, y)):
        return 0
    return prod(prod(range(a-b+1, a+1)) for a, b in zip(x, y))


def check_weak_reversibility(rs):
    nodes = {r.y for r in rs} | {r.yp for r in rs}
    graph = {y: [] for y in nodes}
    for r in rs:
        graph[r.y].append(r.yp)
    def reachable(a, b):
        seen, stack = {a}, [a]
        while stack:
            z = stack.pop()
            if z == b:
                return True
            for zz in graph[z]:
                if zz not in seen:
                    seen.add(zz)
                    stack.append(zz)
        return False
    return all(reachable(r.yp, r.y) for r in rs)


def acquire_drain_paths(rs, d):
    """Each chosen edge is one molecule -> one molecule or zero."""
    edges = []
    for k, r in enumerate(rs):
        if sum(r.y) == 1 and sum(r.yp) <= 1:
            i = r.y.index(1)
            j = -1 if sum(r.yp) == 0 else r.yp.index(1)
            edges.append((i, j, k))
    distance = {-1: 0}
    successor = {}
    for _ in range(d):
        changed = False
        for i, j, k in edges:
            if i not in distance and j in distance:
                distance[i] = distance[j]+1
                successor[i] = (j, k)
                changed = True
        if not changed:
            break
    if any(i not in distance for i in range(d)):
        return None
    paths = {}
    for i in range(d):
        j, p = i, []
        while j != -1:
            j, k = successor[j]
            p.append(k)
        paths[i] = p
    return paths


def acquire_production_recipes(rs, d):
    """An acyclic recipe recursively manufactures extra reactants then fires."""
    recipes, order = {}, []
    for _ in range(d):
        changed = False
        for k, r in enumerate(rs):
            if all(r.y[i] == 0 or i in recipes for i in range(d)):
                for j in range(d):
                    if r.yp[j] > 0 and j not in recipes:
                        recipes[j] = k
                        order.append(j)
                        changed = True
        if not changed:
            break
    if len(recipes) != d:
        return None
    def word(i):
        r = rs[recipes[i]]
        result = []
        for j, count in enumerate(r.y):
            for _ in range(count):
                result.extend(word(j))
        result.append(recipes[i])
        return result
    words = {i: word(i) for i in range(d)}
    return {"order": order, "recipes": recipes, "words": words}


def grouped(rs):
    groups = {}
    for r in rs:
        groups.setdefault(r.y, []).append(r)
    return groups


def source_vertices(group, d):
    if not group:
        return [tuple(F(0) for _ in range(d))]
    vertices = set()
    for ks in product(*(sorted({r.lo, r.hi}) for r in group)):
        vertices.add(tuple(sum((k*r.nu[i] for k, r in zip(ks, group)), F(0))
                           for i in range(d)))
    return sorted(vertices)


def constraints(rs, d, quadratic_species):
    groups = grouped(rs)
    rows = []
    for i in range(d):
        rows.append((tuple(F(-1 if i == j else 0) for j in range(d)), F(-1)))
    for i in range(d):
        yi = tuple(int(j == i) for j in range(d))
        if i not in quadratic_species:
            rows.extend((a, F(-1)) for a in source_vertices(groups.get(yi, []), d))
        y2 = tuple(2*int(j == i) for j in range(d))
        rows.extend((a, F(-1 if i in quadratic_species else 0))
                    for a in source_vertices(groups.get(y2, []), d))
    for y, group in groups.items():
        if sum(y) == 2 and max(y) == 1:
            rows.extend((a, F(0)) for a in source_vertices(group, d))
    return sorted(set(rows))


def solve_equalities(rows, d):
    a = [list(coeff)+[rhs] for coeff, rhs in rows]
    for col in range(d):
        pivot = next((i for i in range(col, d) if a[i][col]), None)
        if pivot is None:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [v/scale for v in a[col]]
        for i in range(d):
            if i != col and a[i][col]:
                factor = a[i][col]
                a[i] = [v-factor*u for v, u in zip(a[i], a[col])]
    return tuple(a[i][-1] for i in range(d))


def feasible(w, rows):
    return all(dot(a, w) <= b for a, b in rows)


def synthesize_weight(rs, d, linear_only=False):
    stats = {"partitions_considered": 0, "bases_solved": 0}
    masks = [0] if linear_only else range(2**d)
    for mask in masks:
        s = {i for i in range(d) if mask & (1 << i)}
        rows = constraints(rs, d, s)
        stats["partitions_considered"] += 1
        if any(not any(a) and b < 0 for a, b in rows):
            continue
        ones = tuple(F(1) for _ in range(d))
        if feasible(ones, rows):
            return ones, s, rows, stats
        for indices in combinations(range(len(rows)), d):
            stats["bases_solved"] += 1
            w = solve_equalities([rows[j] for j in indices], d)
            if w is not None and feasible(w, rows):
                return w, s, rows, stats
    return None, None, None, stats


def source_worst(group, w):
    return sum((max(r.lo*dot(w, r.nu), r.hi*dot(w, r.nu))
                for r in group), F(0))


def compile_certificate(rs, q=2, linear_only=False):
    if not rs or not isinstance(q, int) or q < 1:
        return {"status": "REJECTED_INPUT"}
    d = len(rs[0].y)
    if d < 1 or not all(len(r.y) == d == len(r.yp)
               and all(isinstance(v, int) and v >= 0 for v in r.y+r.yp)
               and sum(r.y) <= 2 and sum(r.yp) <= 2
               and 0 < r.lo <= r.hi for r in rs):
        return {"status": "REJECTED_INPUT"}
    if not check_weak_reversibility(rs):
        return {"status": "REJECTED_NOT_WEAKLY_REVERSIBLE"}
    drain = acquire_drain_paths(rs, d)
    production = acquire_production_recipes(rs, d)
    if drain is None or production is None:
        return {"status": "REJECTED_BOUNDARY_CLASS"}
    w, s, rows, stats = synthesize_weight(rs, d, linear_only)
    if w is None:
        return {"status": "NO_CERTIFICATE_IN_ADMITTED_FOSTER_CLASS", "search": stats}
    groups = grouped(rs)
    zero = tuple(0 for _ in range(d))
    b0 = source_worst(groups.get(zero, []), w)
    correction = {}
    for i in sorted(s):
        y = tuple(int(j == i) for j in range(d))
        ci = source_worst(groups.get(y, []), w)
        correction[i] = max(F(0), ci+2)
    b = b0+sum((v*v/4 for v in correction.values()), F(0))
    radius_w = 2*max(w)*(b+1)
    radius_n = ceil(radius_w)
    cover = [k for i in range(d) for _ in range(q) for k in production["words"][i]]
    production_length = len(cover)
    h = d*radius_n+production_length
    count_cap = max(radius_n, 2*production_length)
    u = sum((r.hi for r in rs), F(0))
    total_rate_cap = u*(count_cap+1)**2
    alpha = min(r.lo for r in rs)/(2*total_rate_cap)
    p = alpha**h
    t0 = F(h)/total_rate_cap
    recovery_constant = (radius_w+(b+1)*t0)/p
    return {"status": "CERTIFIED", "dimension": d, "weight": w,
            "quadratic_species": sorted(s), "constraint_count": len(rows),
            "search": stats, "B0": b0, "quadratic_linear_corrections": correction,
            "B": b, "weighted_core_radius": radius_w, "count_core_radius": radius_n,
            "drain_paths": drain, "production": production, "cover_word": cover,
            "q": q, "attempt_steps": h, "path_count_cap": count_cap,
            "total_rate_cap": total_rate_cap, "one_step_probability": alpha,
            "attempt_success_probability": p, "attempt_duration": t0,
            "recovery_constant": recovery_constant,
            "recovery_constant_bit_length": max(recovery_constant.numerator.bit_length(),
                                                recovery_constant.denominator.bit_length())}


def fire(x, r):
    if not falling(x, r.y):
        raise AssertionError(("disabled", x, r))
    return tuple(a+b for a, b in zip(x, r.nu))


def apply_word(x, rs, word):
    cap = sum(x)
    for k in word:
        x = fire(x, rs[k])
        cap = max(cap, sum(x))
    return x, cap


def drain_word(x, rs, paths):
    current, word = tuple(x), []
    while any(current):
        i = next(j for j, n in enumerate(current) if n)
        for k in paths[i]:
            current = fire(current, rs[k])
            word.append(k)
    return word


def exact_diagnostics(rs, cert, extent=7):
    d, w, b = cert["dimension"], cert["weight"], cert["B"]
    counts = {"global_drift_states_checked": 0, "rate_vertex_states_checked": 0,
              "drain_paths_checked": 0, "production_dominance_checked": 0}
    for x in product(range(extent+1), repeat=d):
        # Directly maximize the full enabled generator, independently of source constraints.
        direct = sum((falling(x, r.y)*max(r.lo*dot(w, r.nu), r.hi*dot(w, r.nu))
                      for r in rs), F(0))
        assert direct <= b-sum(x), (x, direct, b)
        counts["global_drift_states_checked"] += 1
    for x in product(range(3), repeat=d):
        for rates in product(*(sorted({r.lo, r.hi}) for r in rs)):
            generator = sum((k*falling(x, r.y)*dot(w, r.nu)
                             for k, r in zip(rates, rs)), F(0))
            assert generator <= b-sum(x)
            counts["rate_vertex_states_checked"] += 1
        word = drain_word(x, rs, cert["drain_paths"])
        terminal, cap = apply_word(x, rs, word)
        assert terminal == (0,)*d and len(word) <= d*sum(x) and cap <= sum(x)
        counts["drain_paths_checked"] += 1
        terminal, cap = apply_word(x, rs, cert["cover_word"])
        assert all(a >= z+cert["q"] for a, z in zip(terminal, x))
        assert cap <= sum(x)+2*len(cert["cover_word"])
        counts["production_dominance_checked"] += 1
    return counts


def serialize(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serialize(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [serialize(v) for v in value]
    return value


def fixtures():
    linear = [reaction((0,0,0),(1,0,0),1,2,"0->A"),
              reaction((1,0,0),(0,0,0),8,10,"A->0"),
              reaction((1,0,0),(0,1,0),1,2,"A->B"),
              reaction((0,1,0),(1,0,0),1,2,"B->A"),
              reaction((1,0,0),(1,1,0),1,2,"A->A+B"),
              reaction((1,1,0),(0,0,1),1,2,"A+B->C"),
              reaction((0,0,1),(1,0,0),1,2,"C->A")]
    autocatalytic = [reaction((0,),(1,),1,name="0->A"),
                    reaction((1,),(0,),1,name="A->0"),
                    reaction((1,),(2,),2,name="A->2A"),
                    reaction((2,),(1,),1,name="2A->A")]
    balanced_cross = [reaction((0,0),(1,0),name="0->A"),
                      reaction((1,0),(0,0),name="A->0"),
                      reaction((0,0),(0,1),name="0->B"),
                      reaction((0,1),(0,0),name="B->0"),
                      reaction((1,0),(1,1),name="A->A+B"),
                      reaction((1,1),(1,0),name="A+B->A"),
                      reaction((0,1),(1,1),name="B->A+B"),
                      reaction((1,1),(0,1),name="A+B->B")]
    return {"nonlinear_assembly": linear, "autocatalytic": autocatalytic,
            "balanced_cross_rejection": balanced_cross}


if __name__ == "__main__":
    start = time.perf_counter()
    output = {"method": "Fraction exact vertex enumeration and constructive boundary words",
              "scope": "finite diagnostics support the derivation; no trajectory or general-corpus run",
              "fixtures": {}}
    for name, rs in fixtures().items():
        cert = compile_certificate(rs)
        entry = {"reactions": [{"source": r.y, "product": r.yp, "lo": r.lo,
                                  "hi": r.hi, "name": r.name} for r in rs],
                 "certificate": cert}
        if cert["status"] == "CERTIFIED":
            entry["exact_diagnostics"] = exact_diagnostics(rs, cert,
                                                           extent=12 if len(rs[0].y)==1 else 7)
        if name == "autocatalytic":
            entry["linear_only_search"] = compile_certificate(rs, linear_only=True)
            assert entry["linear_only_search"]["status"] == "NO_CERTIFICATE_IN_ADMITTED_FOSTER_CLASS"
        output["fixtures"][name] = entry
    assert output["fixtures"]["nonlinear_assembly"]["certificate"]["status"] == "CERTIFIED"
    assert output["fixtures"]["autocatalytic"]["certificate"]["status"] == "CERTIFIED"
    assert output["fixtures"]["balanced_cross_rejection"]["certificate"]["status"] == "NO_CERTIFICATE_IN_ADMITTED_FOSTER_CLASS"
    output["wall_seconds"] = time.perf_counter()-start
    output["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    dest = Path(__file__).with_name("checks.json")
    dest.write_text(json.dumps(serialize(output), indent=2)+"\n")
    print(json.dumps({"result": str(dest), "wall_seconds": output["wall_seconds"],
                      "statuses": {n: e["certificate"]["status"] for n,e in output["fixtures"].items()},
                      "checks": {n: e.get("exact_diagnostics") for n,e in output["fixtures"].items()}}, indent=2))
