"""Acquire robust rational Foster functions through three catalytic layers.

Rate intervals are fixed rational input. The worst-generator verifier chooses
the adversarial endpoint for EACH RAW REACTION according to its actual jump
of V. It therefore checks every point of each rate box at the sampled state.
The infinite-lattice guarantee is proved separately in robust_three_layer.txt.
"""
from fractions import Fraction as F
from itertools import product
import json
import pathlib
import time


def interval(value):
    if (not isinstance(value, (list, tuple)) or len(value) != 2
            or any(isinstance(z, bool) or not isinstance(z, (str, int)) for z in value)):
        raise ValueError("Use two exact rational strings or integers per interval")
    lo, hi = (F(str(z)) for z in value)
    if not 0 < lo <= hi:
        raise ValueError("Rates need positive ordered rational bounds")
    return lo, hi


def ceil_rat(value):
    return -((-value.numerator) // value.denominator)


def acquire(spec):
    if not isinstance(spec, dict) or set(spec) != {"roots", "middle", "leaves"}:
        raise ValueError("Complete three-layer syntax required; unknown fields rejected")
    roots, middle, leaves = (spec[k] for k in ("roots", "middle", "leaves"))
    if any(not isinstance(z, list) for z in (roots, middle, leaves)):
        raise ValueError("Species groups must be lists")
    for group, keys in ((roots, {"name", "birth", "death"}),
                        (middle, {"name", "parents"}),
                        (leaves, {"name", "parent", "birth", "death"})):
        if any(not isinstance(z, dict) or set(z) != keys for z in group):
            raise ValueError("Unknown or missing species fields")
    names = [z["name"] for group in (roots, middle, leaves) for z in group]
    if (not roots or any(not isinstance(z, str) or not z for z in names)
            or len(set(names)) != len(names)):
        raise ValueError("Nonempty roots, distinct species required")
    rn = {z["name"] for z in roots}
    mn = {z["name"] for z in middle}
    root_rates = {z["name"]: (interval(z["birth"]), interval(z["death"]))
                  for z in roots}
    mid_edges = {}
    mid_data = {}
    for z in middle:
        j = z["name"]
        if (not isinstance(z["parents"], dict) or not z["parents"]
                or not set(z["parents"]) <= rn):
            raise ValueError("Middle species need nonempty root-only parent sets")
        if any(not isinstance(v, dict) or set(v) != {"birth", "death"}
               for v in z["parents"].values()):
            raise ValueError("Unknown or missing catalytic rate fields")
        mid_edges[j] = {i: (interval(v["birth"]), interval(v["death"]))
                        for i, v in z["parents"].items()}
        parents = mid_edges[j]
        b_lo = sum(root_rates[i][0][0] for i in parents)
        d_hi = max(root_rates[i][1][1] for i in parents)
        beta_lo = min(v[1][0] for v in parents.values())
        alpha_lo = min(v[0][0] for v in parents.values())
        beta_hi = max(v[1][1] for v in parents.values())
        c = min(F(1), beta_lo / d_hi)
        gamma = min(c * b_lo / 2, beta_lo / 2)
        mid_data[j] = {"B_lo": b_lo, "D_hi": d_hi,
                       "alpha_lo": alpha_lo, "beta_hi": beta_hi,
                       "c": c, "gamma": gamma}
    leaf_data = {}
    for z in leaves:
        k, j = z["name"], z["parent"]
        if j not in mn:
            raise ValueError("Leaves need exactly one middle parent")
        alpha, beta = interval(z["birth"]), interval(z["death"])
        d = mid_data[j]
        shift = 1 + 4 * d["D_hi"] / d["alpha_lo"]
        c = min(F(1), beta[0] / (d["D_hi"] / shift + d["beta_hi"]))
        gamma = min(c * d["B_lo"] / (shift * (shift + 1)),
                    c * d["alpha_lo"] / (4 * (shift + 1)), beta[0] / 2)
        leaf_data[k] = {"parent": j, "alpha": alpha, "beta": beta,
                        "s": shift, "c": c, "gamma": gamma}
    mid_weight = {j: (1 + sum((1 + z["c"] / z["s"]) * z["alpha"][1]
                              for z in leaf_data.values() if z["parent"] == j))
                       / d["gamma"]
                  for j, d in mid_data.items()}
    root_weight = {i: (1 + sum(mid_weight[j] * (1 + mid_data[j]["c"])
                               * mid_edges[j][i][0][1]
                               for j in mid_edges if i in mid_edges[j]))
                         / root_rates[i][1][0]
                   for i in rn}
    constant = sum(root_weight[i] * root_rates[i][0][1] for i in rn)
    decay = min([1 / z for z in root_weight.values()]
                + [1 / (mid_weight[j] * (1 + z["c"]))
                   for j, z in mid_data.items()]
                + [z["gamma"] / (1 + z["c"] / z["s"])
                   for z in leaf_data.values()])
    gamma_min = min([F(1), *[z["gamma"] for z in leaf_data.values()]])
    min_weight = min([F(1), *root_weight.values(), *mid_weight.values()])
    radius = max(1, ceil_rat((constant + 1) / gamma_min))
    return {"spec": spec, "names": names, "root_rates": root_rates,
            "mid_edges": mid_edges, "mid_data": mid_data,
            "leaf_data": leaf_data, "mid_weight": mid_weight,
            "root_weight": root_weight, "C": constant, "lambda": decay,
            "min_weight": min_weight, "core_radius": radius}


def acquire_from_reactions(species, reactions):
    """Acquire the partition from a COMPLETE integer source/target CRN table.

    Parallel identical reactions are aggregated by adding their interval
    endpoints. Every input record is consumed; unknown fields, unpaired edges,
    conversions, self-catalysis, bursts, unused species and deeper layers reject.
    """
    if (not isinstance(species, list) or not species
            or any(not isinstance(z, str) or not z for z in species)
            or len(set(species)) != len(species)
            or not isinstance(reactions, list)):
        raise ValueError("Explicit distinct species and complete reaction list required")
    buckets = {}
    for reaction in reactions:
        if not isinstance(reaction, dict) or set(reaction) != {"source", "target", "rate"}:
            raise ValueError("Raw reactions require exactly source/target/rate")
        source, target = reaction["source"], reaction["target"]
        if (not isinstance(source, (list, tuple)) or not isinstance(target, (list, tuple))
                or len(source) != len(species) or len(target) != len(species)
                or any(isinstance(z, bool) or not isinstance(z, int) or z < 0
                       for z in (*source, *target))):
            raise ValueError("Integer source/target vectors required")
        drift = [z - y for y, z in zip(source, target)]
        changed = [i for i, v in enumerate(drift) if v]
        if len(changed) != 1 or abs(drift[changed[0]]) != 1:
            raise ValueError("Only unit production/degradation of one species admitted")
        j = changed[0]
        sign = drift[j]
        residual = source if sign > 0 else target
        if sum(residual) not in (0, 1):
            raise ValueError("Only zero or one unchanged catalyst admitted")
        parent = None if sum(residual) == 0 else residual.index(1)
        if parent == j:
            raise ValueError("Self-catalysis outside three-layer class")
        bounds = interval(reaction["rate"])
        key = (j, parent, sign)
        old = buckets.get(key, (F(0), F(0)))
        buckets[key] = (old[0] + bounds[0], old[1] + bounds[1])
    pairs = {(j, i) for j, i, _ in buckets}
    if any((j, i, 1) not in buckets or (j, i, -1) not in buckets for j, i in pairs):
        raise ValueError("Every specified channel must have both positive directions")
    roots = {j for j, i in pairs if i is None}
    parents = {j: {i for jj, i in pairs if jj == j and i is not None}
               for j in range(len(species))}
    if not roots or any(parents[j] for j in roots):
        raise ValueError("Roots require only direct immigration/death")
    nonroots = set(range(len(species))) - roots
    if any(not parents[j] for j in nonroots):
        raise ValueError("Unused or unactivated species outside promise")
    middle = {j for j in nonroots if parents[j] <= roots}
    leaves = nonroots - middle
    if any(len(parents[j]) != 1 or not parents[j] <= middle for j in leaves):
        raise ValueError("Each third-layer leaf needs one middle parent")
    def rates(j, i):
        return {"birth": [str(z) for z in buckets[(j, i, 1)]],
                "death": [str(z) for z in buckets[(j, i, -1)]]}
    specialized = {
        "roots": [{"name": species[j], **rates(j, None)} for j in sorted(roots)],
        "middle": [{"name": species[j], "parents": {
            species[i]: rates(j, i) for i in sorted(parents[j])}}
                   for j in sorted(middle)],
        "leaves": [{"name": species[j], "parent": species[next(iter(parents[j]))],
                    **rates(j, next(iter(parents[j])))} for j in sorted(leaves)]}
    return acquire(specialized)


def potential(cert, state):
    x = dict(zip(cert["names"], state))
    result = sum(w * x[i] for i, w in cert["root_weight"].items())
    for j, d in cert["mid_data"].items():
        s = sum(x[i] for i in cert["mid_edges"][j])
        result += cert["mid_weight"][j] * (1 + d["c"] / (s + 1)) * x[j]
    for k, d in cert["leaf_data"].items():
        j = d["parent"]
        s = sum(x[i] for i in cert["mid_edges"][j])
        result += (1 + d["c"] / ((s + d["s"]) * (x[j] + 1))) * x[k]
    return result


def raw_reactions(cert):
    names = cert["names"]
    result = []
    def pair(i, j, birth, death):
        source = [0] * len(names)
        if i is not None:
            source[names.index(i)] = 1
        target = source.copy()
        target[names.index(j)] = 1
        result.append((tuple(source), tuple(target), birth))
        result.append((tuple(target), tuple(source), death))
    for i, (birth, death) in cert["root_rates"].items():
        pair(None, i, birth, death)
    for j, parents in cert["mid_edges"].items():
        for i, (birth, death) in parents.items():
            pair(i, j, birth, death)
    for k, d in cert["leaf_data"].items():
        pair(d["parent"], k, d["alpha"], d["beta"])
    return result


def raw_worst_generator(cert, state):
    value = potential(cert, state)
    result = F(0)
    endpoint_policy = []
    for source, target, bounds in raw_reactions(cert):
        ff = 1
        for n, deg in zip(state, source):
            for shift in range(deg):
                ff *= max(0, n - shift)
        if not ff:
            continue
        new = tuple(n + z - y for n, y, z in zip(state, source, target))
        jump = potential(cert, new) - value
        endpoint = bounds[1] if jump >= 0 else bounds[0]
        result += endpoint * ff * jump
        endpoint_policy.append(str(endpoint))
    return result, endpoint_policy


def serialized(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: serialized(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [serialized(v) for v in value]
    return value


def verify():
    one = ["1", "1"]
    fixtures = [
        {"roots": [{"name": "A", "birth": ["1/2", "2"],
                    "death": ["1/3", "3"]}],
         "middle": [{"name": "B", "parents": {
             "A": {"birth": ["1/5", "5"], "death": ["1/7", "7"]}}}],
         "leaves": []},
        {"roots": [{"name": "A", "birth": one, "death": one}],
         "middle": [{"name": "B", "parents": {
             "A": {"birth": one, "death": one}}}],
         "leaves": [{"name": "C", "parent": "B", "birth": one, "death": one}]},
        {"roots": [{"name": "A", "birth": ["1/2", "2"],
                    "death": ["1/3", "3"]},
                   {"name": "D", "birth": ["3/2", "3"],
                    "death": ["2/3", "4"]}],
         "middle": [{"name": "B", "parents": {
             "A": {"birth": ["1/5", "5"], "death": ["1/7", "7"]},
             "D": {"birth": ["2/5", "6"], "death": ["2/7", "8"]}}}],
         "leaves": [{"name": "C", "parent": "B",
                     "birth": ["1/11", "11"], "death": ["1/13", "13"]}]},
    ]
    count = 0
    boundary_count = 0
    smallest_slack = None
    certs = []
    for spec in fixtures:
        cert = acquire(spec)
        certs.append(cert)
        raw = [{"source": list(y), "target": list(z),
                "rate": [str(k) for k in bounds]}
               for y, z, bounds in raw_reactions(cert)]
        recovered = acquire_from_reactions(cert["names"], raw)
        assert recovered["root_weight"] == cert["root_weight"]
        assert recovered["mid_weight"] == cert["mid_weight"]
        assert recovered["leaf_data"] == cert["leaf_data"]
        assert recovered["C"] == cert["C"]
        assert recovered["lambda"] == cert["lambda"]
        for state in product(range(6), repeat=len(cert["names"])):
            x = dict(zip(cert["names"], state))
            h = (sum(x[i] for i in cert["root_weight"])
                 + sum(x[j] for j in cert["mid_weight"])
                 + sum(d["gamma"] * x[k] for k, d in cert["leaf_data"].items()))
            lv, _ = raw_worst_generator(cert, state)
            slack = cert["C"] - h - lv
            assert slack >= 0, (state, lv, cert["C"] - h)
            assert lv <= cert["C"] - cert["lambda"] * potential(cert, state)
            count += 1
            if all(x[i] == 0 for i in cert["root_weight"]):
                boundary_count += 1
            smallest_slack = (slack if smallest_slack is None
                              else min(slack, smallest_slack))
    # Large downstream population at two consecutive empty catalyst gates.
    chain = certs[1]
    boundary = raw_worst_generator(chain, (0, 0, 6000))[0]
    assert boundary < 0
    # A second catalyst generation cannot be passed as a middle parent.
    invalid = {"roots": fixtures[1]["roots"], "middle": [
        *fixtures[1]["middle"], {"name": "D", "parents": {
            "B": {"birth": one, "death": one}}}], "leaves": []}
    try:
        acquire(invalid)
    except ValueError:
        rejected = True
    else:
        raise AssertionError("Outside-scope fourth layer admitted")
    bad_raw = [{"source": list(y), "target": list(z),
                "rate": [str(k) for k in bounds]}
               for y, z, bounds in raw_reactions(chain)]
    bad_raw.append({"source": [0, 0, 0], "target": [0, 0, 2], "rate": one})
    try:
        acquire_from_reactions(chain["names"], bad_raw)
    except ValueError:
        extra_reaction_rejected = True
    else:
        raise AssertionError("Unaccounted burst reaction admitted")
    try:
        acquire({**fixtures[1], "other_reactions": []})
    except ValueError:
        extra_field_rejected = True
    else:
        raise AssertionError("Unaccounted syntax field admitted")
    return {"status": "EXACT_FINITE_RATE_BOX_DIAGNOSTIC_PASSED",
            "checked_states": count, "zero_root_states": boundary_count,
            "smallest_slack": smallest_slack,
            "double_empty_gate_LV_at_0_0_6000": boundary,
            "out_of_class_rejected": rejected,
            "complete_raw_reaction_recovery_checked": len(fixtures),
            "extra_raw_reaction_rejected": extra_reaction_rejected,
            "extra_syntax_field_rejected": extra_field_rejected,
            "certificates": certs}


if __name__ == "__main__":
    started = time.monotonic()
    report = verify()
    report["elapsed_seconds"] = time.monotonic() - started
    path = pathlib.Path(__file__).with_name("robust_three_layer_checks.json")
    path.write_text(json.dumps(serialized(report), indent=2) + "\n")
    print(json.dumps(serialized({k: v for k, v in report.items()
                                  if k != "certificates"}), indent=2))
