#!/usr/bin/env python3
"""Exact expansion-free certifier for paired reversible rational modules.

Module r has endpoints alpha_r <-> beta_r, positive channel coefficients
c+ and c-, and shared positive numerator factors A_r and denominator Q_r for
both directions. Q_r is a product of sparse positive polynomial factors
(constant terms required); A_r is another positive factor product and may
have no constant term. Different modules may have different factors.

The product D=prod_r Q_r is never expanded. The proof pairs each term of
D/Q_r with its forward and reverse reaction, making the conceptual lifted
diagram weakly reversible. See COMMON_FACTOR_PROOF.md.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

_INTEGER_TEXT = re.compile(r"[+-]?[0-9]+\Z")
_DECIMAL_TEXT = re.compile(r"[+-]?(?:[0-9]+\.[0-9]+|\.[0-9]+)\Z")


# This CLI consumes explicitly supplied exact rational strings and reports
# exact decimal summaries. Python 3.11+ otherwise rejects conversions beyond
# a process-wide 4,300-digit default. The input itself charges these digits;
# keep the arithmetic exact instead of truncating or round-tripping through
# floating point. This is a standalone local compiler, not an exposed service.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def frac(raw: Any, label: str) -> F:
    if isinstance(raw, bool):
        raise ValueError(f"{label}: Boolean is not a rational")
    if isinstance(raw, int):
        return F(raw)
    if not isinstance(raw, str):
        raise ValueError(f"{label}: use an exact JSON integer or rational string; JSON floats are rejected")
    if "/" in raw:
        parts = raw.split("/")
        valid = len(parts) == 2 and all(_INTEGER_TEXT.fullmatch(part) for part in parts)
    else:
        valid = bool(_INTEGER_TEXT.fullmatch(raw) or _DECIMAL_TEXT.fullmatch(raw))
    if not valid:
        raise ValueError(
            f"{label}: exact rational strings must be integers, integer ratios, or finite decimals without exponents"
        )
    try:
        return F(raw)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{label}: expected exact rational, got {raw!r}") from exc


def qstr(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


Vector = dict[int, F]


def parse_vector(raw: Any, dimension: int, label: str) -> Vector:
    if not isinstance(raw, dict):
        raise ValueError(f"{label} must be a sparse coordinate:value object")
    out: Vector = {}
    for key, value in raw.items():
        try:
            i = int(key)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{label} coordinate index must be an integer") from exc
        if str(i) != str(key) or not 0 <= i < dimension:
            raise ValueError(f"{label} coordinate {key!r} is not canonical in [0,{dimension})")
        x = frac(value, f"{label}[{i}]")
        if x:
            out[i] = out.get(i, F(0)) + x
    return {i: x for i, x in out.items() if x}


def parse_factors(raw: Any, dimension: int, label: str, *, require_constant: bool):
    if not isinstance(raw, list):
        raise ValueError(f"{label} must be a list of positive polynomial factors")
    if require_constant and not raw:
        raise ValueError(f"{label} must contain at least one denominator factor")
    parsed = []
    constant = True
    factor_min_product = F(1)
    factor_sum_product = F(1)
    term_tuple_count = 1
    for k, factor in enumerate(raw):
        if not isinstance(factor, dict) or not isinstance(factor.get("terms"), list) or not factor["terms"]:
            raise ValueError(f"{label}[{k}].terms must be a nonempty list")
        terms = []
        for j, item in enumerate(factor["terms"]):
            if not isinstance(item, dict) or "exp" not in item:
                raise ValueError(f"{label}[{k}].terms[{j}] needs exp and optional coef")
            exponent = parse_vector(item["exp"], dimension, f"{label}[{k}].terms[{j}].exp")
            if any(a < 0 for a in exponent.values()):
                raise ValueError(f"{label} exponents must be nonnegative")
            coefficient = frac(item.get("coef", "1"), f"{label}[{k}].terms[{j}].coef")
            if coefficient <= 0:
                raise ValueError(f"{label} coefficients must be strictly positive")
            terms.append((exponent, coefficient))
        factor_has_constant = any(not exponent for exponent, _ in terms)
        constant = constant and factor_has_constant
        coeffs = [coefficient for _, coefficient in terms]
        factor_min_product *= min(coeffs)
        factor_sum_product *= sum(coeffs, F(0))
        term_tuple_count *= len(terms)
        parsed.append(terms)
    if require_constant and not constant:
        raise ValueError(f"{label} must have a positive constant term (all factors need one)")
    return parsed, factor_min_product, factor_sum_product, term_tuple_count


def rank_at_most_one(vectors: list[Vector]) -> bool:
    pivot = next((v for v in vectors if v), None)
    if pivot is None:
        return True
    p = min(pivot)
    pv = pivot[p]
    for v in vectors:
        if not v:
            continue
        # v = lambda*pivot, with lambda fixed by coordinate p; check without
        # constructing lambda*pivot over absent sparse coordinates.
        vv = v.get(p, F(0))
        for i in set(pivot) | set(v):
            if v.get(i, F(0)) * pv != vv * pivot.get(i, F(0)):
                return False
    return True


def parse_network(data: Any):
    if not isinstance(data, dict) or data.get("schema") != "paired-reversible-rational-modules-v1":
        raise ValueError("schema must be paired-reversible-rational-modules-v1")
    dimension = data.get("dimension")
    if not isinstance(dimension, int) or isinstance(dimension, bool) or dimension < 1:
        raise ValueError("dimension must be a positive integer")
    raw_modules = data.get("modules")
    if not isinstance(raw_modules, list) or not raw_modules:
        raise ValueError("modules must be a nonempty list")
    modules = []
    for i, raw in enumerate(raw_modules):
        if not isinstance(raw, dict):
            raise ValueError(f"modules[{i}] must be an object")
        name = str(raw.get("name", f"module{i}"))
        source = parse_vector(raw.get("source"), dimension, f"{name}.source")
        target = parse_vector(raw.get("target"), dimension, f"{name}.target")
        if any(x < 0 for x in source.values()) or any(x < 0 for x in target.values()):
            raise ValueError(f"{name}: endpoints must be nonnegative complexes")
        if source == target:
            raise ValueError(f"{name}: reversible module must have distinct endpoints")
        kf = frac(raw.get("k_forward"), f"{name}.k_forward")
        kr = frac(raw.get("k_reverse"), f"{name}.k_reverse")
        if kf <= 0 or kr <= 0:
            raise ValueError(f"{name}: both directional coefficients must be positive")
        factors, fmin, fsum, tuples = parse_factors(
            raw.get("denominator_factors"), dimension, f"{name}.denominator_factors",
            require_constant=True)
        numerator_factors, amin, asum, a_tuples = parse_factors(
            raw.get("shared_numerator_factors", []), dimension,
            f"{name}.shared_numerator_factors", require_constant=False)
        nu = {}
        for coord in set(source) | set(target):
            z = target.get(coord, F(0)) - source.get(coord, F(0))
            if z:
                nu[coord] = z
        modules.append({"name": name, "source": source, "target": target,
                        "kf": kf, "kr": kr, "fmin": fmin, "fsum": fsum,
                        "tuple_count": tuples, "nu": nu, "factors": factors,
                        "numerator_factors": numerator_factors,
                        "amin": amin, "asum": asum, "a_tuples": a_tuples})
    return dimension, modules


def denominator_token_count(module) -> int:
    return sum(len(factor) for factor in module["factors"])


def certify(data: Any):
    dimension, modules = parse_network(data)
    nus = [m["nu"] for m in modules]
    # The parser requires a nonempty module list and distinct endpoints, so
    # every accepted module jump is nonzero and the total rank is at least 1.
    # The helper remains defined on all-zero lists, but that case is outside
    # this schema and cannot trigger a certificate here.
    if not nus or any(not nu for nu in nus):
        raise AssertionError("parser invariant broken: expected nonempty non-self-loop modules")
    rank_one = rank_at_most_one(nus)
    lifted_pair_upper = 0
    global_kappa = None
    global_K = F(0)
    module_support_bounds = []
    for i, module in enumerate(modules):
        others_min = F(1)
        others_sum = F(1)
        pair_count = module["a_tuples"]
        for j, other in enumerate(modules):
            if i == j:
                continue
            others_min *= other["fmin"]
            others_sum *= other["fsum"]
            pair_count *= other["tuple_count"]
        lifted_pair_upper += 2 * pair_count
        local_min = min(module["kf"], module["kr"]) * module["amin"] * others_min
        local_max = max(module["kf"], module["kr"]) * module["asum"] * others_sum
        global_kappa = local_min if global_kappa is None else min(global_kappa, local_min)
        # Each local_max bounds the sum of all tuple coefficients contributed
        # by this module to any one directed edge. Add across modules because
        # the public simple-graph convention merges coincident directions.
        global_K += local_max
        module_support_bounds.append({
            "module": module["name"],
            "nonexpanded_pair_tuple_upper_bound": str(pair_count),
            "module_directional_edge_contribution_lower_bound": qstr(local_min),
            "module_directional_edge_contribution_upper_bound": qstr(local_max),
        })
    rank = "exactly_one" if rank_one else "greater_than_one"
    return {
        "status": "CERTIFIED",
        "property": "ordinary essential-source endotacticity",
        "dimension": dimension,
        "module_count": len(modules),
        "input_denominator_term_count": sum(denominator_token_count(m) for m in modules),
        "input_shared_numerator_term_count": sum(
            sum(len(factor) for factor in m["numerator_factors"]) for m in modules),
        "lifted_pair_count_upper_bound_without_expansion": str(lifted_pair_upper),
        "decision_method": "paired reverse-edge proof; no direction LPs, fan cells, denominator products, or support Minkowski sums are built",
        "endotactic_proof": "For each denominator-term tuple and each reversible module, clearing the other denominators creates two opposite edges with the same shift. If an active edge at an essential maximum pointed outward, its paired reverse edge would have strictly higher source score; hence every active top edge points inward. Neutral pairs are both removed, and tied top edges are checked individually.",
        "strong_endotactic_status": "CERTIFIED" if rank_one else "UNKNOWN",
        "stoichiometric_rank_gate": rank,
        "strong_proof_or_reason": (
            "The accepted schema has nonempty modules and rejects self-loops, so its stoichiometric rank is at least one. Since the exact rank gate passes, every lifted reaction vector lies on one line; for w not orthogonal to it, a globally maximal endpoint has a reverse-paired edge pointing inward."
            if rank_one else
            "Weak reversibility alone does not imply strong endotacticity for several linkage classes with different stoichiometric spans. No strong verdict is inferred."
        ),
        "expanded_rate_box_for_N33": {
            "kappa_lower_bound": qstr(global_kappa),
            "K_upper_bound": qstr(global_K),
            "coefficient_convention": "simple directed reactions; coincident same-direction labeled term edges are summed",
            "proof": "For each module r, the product of its shared-numerator factor sums and every other denominator's factor sums bounds above the total tuple coefficient contributed by r to any one directed edge. Summing these modulewise bounds covers collisions across modules. The global lower bound is safe because every merged edge contains at least one tuple contribution.",
            "gate": "CONDITIONAL_ON_N33_CANDIDATE",
            "meaning": "The N33 permanence candidate applies to the finite lifted endotactic power-law diagram with these fixed coefficients, if its source theorem and common-class hypotheses are validated. It is not a new proof of N33."
        },
        "strong_permanence_gate": (
            "PRIOR_STRONG_ENDOTACTIC_PERMANENCE_AFTER_TIME_CHANGE"
            if rank_one else "NOT_ESTABLISHED_BY_THIS_STRONG_GATE"
        ),
        "time_change": "F(x)=G(x)/D(x), D=product_r Q_r>0. If the G-trajectory is y(s), the original clock is t(s)=integral_0^s D(y(u))du. On the eventual compact positive set supplied by a permanence theorem, D has positive finite bounds, so t(s) tends to infinity and permanence transfers.",
        "per_module_rate_boxes": module_support_bounds,
        "cost": {
            "input": "L bits across sparse endpoints, positive factor supports, and rational coefficients",
            "recognition": "polynomial in L; sparse exact arithmetic and a collinearity check",
            "expanded_lift_size": "may be exponential and is reported only by an exact tuple-count upper bound",
            "acquisition": "all support factors and positivity promises are supplied; no experimental parameter acquisition is inferred",
        },
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path)
    ap.add_argument("--property", choices=("endotactic", "strong"), default="endotactic")
    args = ap.parse_args(argv)
    try:
        data = json.loads(args.input.read_text())
        result = certify(data)
    except (OSError, json.JSONDecodeError, TypeError, ValueError, ZeroDivisionError, RecursionError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "reason": str(exc)}, indent=2))
        return 2
    if args.property == "strong" and result["strong_endotactic_status"] != "CERTIFIED":
        result["status"] = "UNKNOWN"
        result["property"] = "standard strong endotacticity (global all-source maximum, neutral edges retained)"
    result["input"] = str(args.input)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] == "CERTIFIED":
        return 0
    if result["status"] == "UNKNOWN":
        return 3
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
