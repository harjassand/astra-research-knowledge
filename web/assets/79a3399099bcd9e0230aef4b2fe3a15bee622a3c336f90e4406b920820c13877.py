#!/usr/bin/env python3
"""Exact local regression for canonical rational-kinetics certificates."""
from __future__ import annotations
import itertools
import json
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from recognize_reversible_modules import certify
from compile_alternative_substrates import compile_model


def load(name):
    return json.loads((ROOT / "fixtures" / name).read_text())


def parse_v(v):
    return {int(i): F(str(x)) for i, x in v.items() if F(str(x))}


def dot(a, b):
    return sum((x * b.get(i, F(0)) for i, x in a.items()), F(0))


def expanded_pairs(data):
    d = data["dimension"]
    out = []
    for i, mod in enumerate(data["modules"]):
        choices = []
        for factor in mod.get("shared_numerator_factors", []):
            terms = []
            for term in factor["terms"]:
                terms.append((parse_v(term["exp"]), F(str(term.get("coef", "1")))))
            choices.append(terms)
        for j, other in enumerate(data["modules"]):
            if i == j:
                continue
            for factor in other["denominator_factors"]:
                terms = []
                for term in factor["terms"]:
                    exp = parse_v(term["exp"])
                    terms.append((exp, F(str(term.get("coef", "1")))))
                choices.append(terms)
        tuples = itertools.product(*choices) if choices else [()]
        alpha, beta = parse_v(mod["source"]), parse_v(mod["target"])
        for tup in tuples:
            gamma, qcoef = {}, F(1)
            for exp, coef in tup:
                qcoef *= coef
                for k, x in exp.items():
                    gamma[k] = gamma.get(k, F(0)) + x
            for src, dst, rate, label in (
                (alpha, beta, F(str(mod["k_forward"])), "forward"),
                (beta, alpha, F(str(mod["k_reverse"])), "reverse"),
            ):
                shifted_src = {k: src.get(k, F(0)) + gamma.get(k, F(0)) for k in set(src) | set(gamma)}
                shifted_dst = {k: dst.get(k, F(0)) + gamma.get(k, F(0)) for k in set(dst) | set(gamma)}
                nu = {k: shifted_dst.get(k, F(0)) - shifted_src.get(k, F(0)) for k in set(shifted_src) | set(shifted_dst)}
                out.append({"name": f"{mod['name']}:{label}",
                            "source": {k: x for k, x in shifted_src.items() if x},
                            "nu": {k: x for k, x in nu.items() if x},
                            "coef": rate * qcoef})
    return out


def direct_properties(edges, w):
    active = [e for e in edges if dot(e["nu"], w)]
    if not active:
        weak_ok = True
    else:
        top = max(dot(e["source"], w) for e in active)
        weak_ok = all(dot(e["nu"], w) < 0 for e in active if dot(e["source"], w) == top)
    all_top = max((dot(e["source"], w) for e in edges), default=F(0))
    strong_ok = any(dot(e["source"], w) == all_top and dot(e["nu"], w) < 0 for e in edges) \
        if any(dot(e["nu"], w) for e in edges) else True
    return weak_ok, strong_ok


def module_denominator_height(module, w):
    total = F(0)
    for factor in module["denominator_factors"]:
        total += max(dot(parse_v(term["exp"]), w) for term in factor["terms"])
    return total


def module_numerator_height(module, w):
    total = F(0)
    for factor in module.get("shared_numerator_factors", []):
        total += max(dot(parse_v(term["exp"]), w) for term in factor["terms"])
    return total


def check_source_lift_identity(data, lifted, directions):
    for wlist in directions:
        w = {i: x for i, x in enumerate(wlist) if x}
        dh = sum((module_denominator_height(m, w) for m in data["modules"]), F(0))
        for m in data["modules"]:
            qh = module_denominator_height(m, w)
            for orient, source in (("forward", parse_v(m["source"])),
                                   ("reverse", parse_v(m["target"]))):
                original_tau = dot(source, w) + module_numerator_height(m, w) - qh
                group = [e for e in lifted if e["name"] == f"{m['name']}:{orient}"]
                lifted_height = max(dot(e["source"], w) for e in group)
                assert lifted_height == dh + original_tau


def main():
    cm = load("liebermeister_cm_AplusB_rev_2C.json")
    result = certify(cm)
    assert result["status"] == "CERTIFIED"
    assert result["strong_endotactic_status"] == "CERTIFIED"
    assert result["lifted_pair_count_upper_bound_without_expansion"] == "2"
    pairs = expanded_pairs(cm)
    assert len(pairs) == 2
    # In 3D, w not orthogonal to (-1,-1,2); test representative directions
    # with exact ties and neutral source edges retained for the strong check.
    for w in ([F(1), F(0), F(0)], [F(0), F(1), F(0)],
              [F(0), F(0), F(1)], [F(1), F(1), F(1)],
              [F(1), F(1), F(0)]):
        vec = {i: x for i, x in enumerate(w) if x}
        weak, strong = direct_properties(pairs, vec)
        assert weak and strong
    print("PASS: primary-source common-modular reversible A+B<->2C fixture receives exact weak and strong certificates")

    collision = load("cross_module_collision_bound.json")
    collision_result = certify(collision)
    assert collision_result["expanded_rate_box_for_N33"]["kappa_lower_bound"] == "1"
    assert collision_result["expanded_rate_box_for_N33"]["K_upper_bound"] == "2"
    collision_edges = expanded_pairs(collision)
    merged_coefficients = {}
    for edge in collision_edges:
        key = (tuple(sorted(parse_v(edge["source"]).items())),
               tuple(sorted(parse_v(edge["nu"]).items())))
        merged_coefficients[key] = merged_coefficients.get(key, F(0)) + F(edge["coef"])
    assert merged_coefficients[((), ((0, F(1)),))] == 2
    assert merged_coefficients[(((0, F(1)),), ((0, F(-1)),))] == 2
    assert max(merged_coefficients.values()) <= F(collision_result["expanded_rate_box_for_N33"]["K_upper_bound"])
    print("PASS: two identical unit modules aggregate to coefficient 2 and merged simple-graph K=2")

    try:
        certify(load("self_loop_rejected.json"))
    except ValueError as exc:
        assert "distinct endpoints" in str(exc)
    else:
        raise AssertionError("self-loop/rank-zero input must be rejected by the schema")
    print("PASS: nonempty schema rejects self-loops; rank zero is not an accepted case")

    try:
        certify(load("json_float_rejected.json"))
    except ValueError as exc:
        assert "JSON floats are rejected" in str(exc)
    else:
        raise AssertionError("inexact JSON floating-point coefficients must be rejected")
    try:
        certify(load("scientific_rational_rejected.json"))
    except ValueError as exc:
        assert "without exponents" in str(exc)
    else:
        raise AssertionError("scientific notation must not bypass charged rational bit length")
    print("PASS: rational input rejects JSON floats and succinct scientific-exponent strings")

    large_rational = load("large_rational_5001_digits.json")
    large_expected = large_rational["modules"][0]["k_forward"]
    large_result = certify(large_rational)
    large_bound = large_result["expanded_rate_box_for_N33"]["K_upper_bound"]
    assert len(large_expected) == 5001 and large_bound == large_expected
    assert json.loads(json.dumps(large_result))["expanded_rate_box_for_N33"]["K_upper_bound"] == large_expected
    print("PASS: 5,001-digit exact rational input and output round-trip without float or truncation")

    # Reproduce the large tuple-count case as a generated valid-schema fixture:
    # explicit factors are charged input, but no expanded product support is built.
    factor_count = 15000
    one_plus_x = {"terms": [{"exp": {}}, {"exp": {"0": "1"}}]}
    huge_count_input = {
        "schema": "paired-reversible-rational-modules-v1",
        "dimension": 2,
        "modules": [
            {"name": "many-denominator-factors", "source": {}, "target": {"0": "1"},
             "k_forward": "1", "k_reverse": "1",
             "denominator_factors": [one_plus_x for _ in range(factor_count)]},
            {"name": "second-module", "source": {"1": "1"}, "target": {},
             "k_forward": "1", "k_reverse": "1",
             "denominator_factors": [{"terms": [{"exp": {}}]}]},
        ],
    }
    huge_count_result = certify(huge_count_input)
    exact_power = 1 << factor_count
    assert huge_count_result["per_module_rate_boxes"][1]["nonexpanded_pair_tuple_upper_bound"] == str(exact_power)
    assert huge_count_result["lifted_pair_count_upper_bound_without_expansion"] == str(2 + 2 * exact_power)
    assert json.loads(json.dumps(huge_count_result))["lifted_pair_count_upper_bound_without_expansion"] == str(2 + 2 * exact_power)
    with tempfile.TemporaryDirectory(prefix="cycle10-large-count-") as tmp:
        generated_path = Path(tmp) / "large_tuple_count.json"
        generated_path.write_text(json.dumps(huge_count_input))
        cli = subprocess.run(
            [sys.executable, str(ROOT / "recognize_reversible_modules.py"), str(generated_path)],
            capture_output=True, text=True, check=False)
        assert cli.returncode == 0, cli.stderr
        cli_result = json.loads(cli.stdout)
        assert cli_result["lifted_pair_count_upper_bound_without_expansion"] == str(2 + 2 * exact_power)
        assert cli_result["per_module_rate_boxes"][1]["nonexpanded_pair_tuple_upper_bound"] == str(exact_power)
    print("PASS: generated 15,000-factor CLI input reports exact 2^15000 tuple counts without expansion")

    # A positive common activation factor with no constant term is allowed in
    # the numerator and a nonsingular factor in the denominator.
    activated = json.loads(json.dumps(cm))
    activated["modules"][0]["shared_numerator_factors"] = [
        {"terms": [{"exp": {"0": "1"}, "coef": "2"}, {"exp": {}, "coef": "1"}]}
    ]
    activated["modules"][0]["denominator_factors"].append(
        {"terms": [{"exp": {}, "coef": "1"}, {"exp": {"1": "1"}, "coef": "3"}]}
    )
    activated_result = certify(activated)
    assert activated_result["status"] == "CERTIFIED" and activated_result["strong_endotactic_status"] == "CERTIFIED"
    activated_lift = expanded_pairs(activated)
    check_source_lift_identity(
        activated, activated_lift,
        [list(map(F, vec)) for vec in itertools.product((-1, 0, 1), repeat=3)],
    )
    print("PASS: shared positive rational activation numerator/denominator factors preserve the paired certificate")

    boundary = load("weak_not_strong_distinct_linkage_spans.json")
    boundary_result = certify(boundary)
    assert boundary_result["status"] == "CERTIFIED"
    assert boundary_result["strong_endotactic_status"] == "UNKNOWN"
    lifted = expanded_pairs(boundary)
    check_source_lift_identity(
        boundary, lifted,
        [list(map(F, vec)) for vec in itertools.product((-1, 0, 1), repeat=3)],
    )
    w = {0: F(1), 2: F(-1)}
    weak, strong = direct_properties(lifted, w)
    assert weak and not strong
    print("PASS: 27 exact directions preserve source heights/ties under distinct-denominator clearing; weak but not standard-strong witness replays")

    # This stays a compact input while the conceptual common-denominator lift
    # has hundreds of millions of labelled edges; certification must not build it.
    R = 24
    stress = {"schema": "paired-reversible-rational-modules-v1", "dimension": 2*R, "modules": []}
    for i in range(R):
        stress["modules"].append({
            "name": f"S{i}<->P{i}", "source": {str(i): "1"},
            "target": {str(R+i): "1"}, "k_forward": "1", "k_reverse": "1",
            "denominator_factors": [{"terms": [
                {"exp": {}, "coef": "1"}, {"exp": {str(i): "1"}, "coef": "1"}
            ]}],
        })
    compact = certify(stress)
    expected_lift = 2 * R * (2 ** (R-1))
    assert compact["status"] == "CERTIFIED"
    assert compact["lifted_pair_count_upper_bound_without_expansion"] == str(expected_lift)
    print(f"PASS: {R}-module factorized input is certified without expansion (lift upper bound {expected_lift:,} edges)")

    alt = load("schnell_mendoza_three_alternative_substrates.json")
    network, cert, decay = compile_model(alt)
    assert cert["status"] == "REFUTED" and decay is not None
    assert [x["minimum_exponential_decay_rate"] for x in decay["substrate_bounds"]] == ["4/15", "2/5", "16/45"]
    assert [x["Eq38_enzyme_scale_ratio"] for x in decay["QSSA_regime_diagnostic"]["ratios"]] == ["1/3", "1/6", "2/9"]
    assert decay["QSSA_regime_diagnostic"]["maximum_Eq38_enzyme_scale_ratio"] == "1/3"
    assert len(network["edges"]) == 3
    r = {0: F(1)}
    active = []
    for edge in network["edges"]:
        nu, source = parse_v(edge["nu"]), parse_v(edge["source"])
        drift = dot(nu, r)
        if drift:
            active.append((edge["name"], drift, dot(source, r)))
    assert len(active) == 1 and active[0][0] == "S1->P1"
    min_score = min(row[2] for row in active)
    assert any(score == min_score and drift < 0 for _, drift, score in active)
    print("PASS: Schnell-Mendoza reduced law yields exact witness/decay bounds; synthetic fixture max Eq. 38 ratio 1/3 is not QSSA-regime evidence")


if __name__ == "__main__":
    main()
