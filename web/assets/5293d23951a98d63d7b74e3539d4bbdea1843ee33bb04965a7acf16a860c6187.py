#!/usr/bin/env python3
"""Exact bounded recognizer for positive sparse rational-rate endotacticity.

The search is formulated directly in sparse support data. It never expands a
common denominator or a Minkowski sum. For each candidate outward channel e,
Z3 decides the existential QF-LRA formula

    w.nu_e > 0 and, for every f, w.nu_f != 0 -> tau_e(w) >= tau_f(w),

where tau_f = max_{a in P_f} w.a - max_{b in Q_f} w.b. The formula keeps all
exact ties and removes neutral channels before the comparison. SAT models are
rechecked with Python Fraction arithmetic. UNSAT is exact for Z3's rational
linear-arithmetic decision procedure; the solver/version is included in the
output. A wall-clock or check budget yields UNKNOWN, never CERTIFIED.

Input JSON:
  {"edges":[{"name":"e","nu":["1","0"],
    "P":[{"exp":["0","0"],"coef":"2"}],
    "Q":[{"exp":["0","0"],"coef":"1"}]}]}

For convenience, a support term may be given as just an exponent vector; its
coefficient is then 1. Exponents and jumps are exact rational strings. All
coefficients must be positive rationals. Real/rational exponents are accepted
because x^alpha is positive and well-defined for x>0.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
from typing import Any, Sequence

try:
    import z3
except ImportError:  # pragma: no cover - exercised on minimal installations
    z3 = None


Vector = tuple[F, ...]


@dataclass(frozen=True)
class Term:
    exponent: Vector
    coefficient: F


@dataclass(frozen=True)
class Edge:
    name: str
    nu: Vector
    P: tuple[Term, ...]
    Q: tuple[Term, ...]


def frac(raw: Any) -> F:
    if isinstance(raw, bool):
        raise ValueError("booleans are not rational numbers")
    return F(str(raw))


def parse_vector(raw: Any, where: str) -> Vector:
    if not isinstance(raw, list) or not raw:
        raise ValueError(f"{where} must be a nonempty vector")
    return tuple(frac(x) for x in raw)


def parse_terms(raw: Any, where: str) -> tuple[Term, ...]:
    if not isinstance(raw, list) or not raw:
        raise ValueError(f"{where} support must be a nonempty list")
    terms: list[Term] = []
    for j, item in enumerate(raw):
        if isinstance(item, dict):
            if "exp" not in item:
                raise ValueError(f"{where}[{j}] is missing exp")
            exponent = parse_vector(item["exp"], f"{where}[{j}].exp")
            coefficient = frac(item.get("coef", "1"))
        else:
            exponent = parse_vector(item, f"{where}[{j}]")
            coefficient = F(1)
        if coefficient <= 0:
            raise ValueError(f"{where}[{j}] coefficient must be strictly positive")
        terms.append(Term(exponent, coefficient))
    dims = {len(t.exponent) for t in terms}
    if len(dims) != 1:
        raise ValueError(f"{where} has inconsistent exponent dimensions")
    # Aggregate repeated support points. Positivity makes their sum nonzero.
    aggregate: dict[Vector, F] = {}
    for t in terms:
        aggregate[t.exponent] = aggregate.get(t.exponent, F(0)) + t.coefficient
    return tuple(Term(exp, coefficient) for exp, coefficient in sorted(aggregate.items()))


def parse_network(data: Any) -> tuple[list[Edge], int]:
    if not isinstance(data, dict) or not isinstance(data.get("edges"), list) or not data["edges"]:
        raise ValueError("input must contain a nonempty edges list")
    edges: list[Edge] = []
    for j, raw in enumerate(data["edges"]):
        if not isinstance(raw, dict):
            raise ValueError(f"edges[{j}] must be an object")
        name = str(raw.get("name", f"e{j}"))
        nu = parse_vector(raw.get("nu"), f"{name}.nu")
        P = parse_terms(raw.get("P"), f"{name}.P")
        Q = parse_terms(raw.get("Q"), f"{name}.Q")
        if any(len(t.exponent) != len(nu) for t in (*P, *Q)):
            raise ValueError(f"{name}: jump and support dimensions differ")
        edges.append(Edge(name, nu, P, Q))
    d = len(edges[0].nu)
    if any(len(e.nu) != d for e in edges):
        raise ValueError("all reaction vectors must have the same dimension")
    return edges, d


def dot_fraction(a: Sequence[F], b: Sequence[F]) -> F:
    return sum((x * y for x, y in zip(a, b)), F(0))


def exact_failure(edges: Sequence[Edge], w: Vector) -> dict[str, Any] | None:
    """Return a verified outward top-tie witness, or None."""
    rows: list[dict[str, Any]] = []
    for edge in edges:
        drift = dot_fraction(edge.nu, w)
        if drift == 0:
            continue  # neutral channels are excluded before finding the top
        hp = max(dot_fraction(t.exponent, w) for t in edge.P)
        hq = max(dot_fraction(t.exponent, w) for t in edge.Q)
        rows.append({"name": edge.name, "drift": drift, "tau": hp - hq})
    if not rows:
        return None
    top = max(row["tau"] for row in rows)
    bad = [row["name"] for row in rows if row["tau"] == top and row["drift"] > 0]
    if not bad:
        return None
    return {
        "direction": [str(x) for x in w],
        "top_tau": str(top),
        "outward_top_ties": bad,
        "active": [
            {"name": row["name"], "w_dot_nu": str(row["drift"]),
             "tau": str(row["tau"]), "top_tied": row["tau"] == top}
            for row in rows
        ],
    }


def exact_strong_failure(edges: Sequence[Edge], w: Vector) -> dict[str, Any] | None:
    """Check failure of the strong inward-at-global-source-maximum clause."""
    rows = []
    for edge in edges:
        drift = dot_fraction(edge.nu, w)
        hp = max(dot_fraction(t.exponent, w) for t in edge.P)
        hq = max(dot_fraction(t.exponent, w) for t in edge.Q)
        rows.append({"name": edge.name, "drift": drift, "tau": hp - hq})
    if not any(row["drift"] != 0 for row in rows):
        return None
    top = max(row["tau"] for row in rows)  # neutral channels are included here
    top_rows = [row for row in rows if row["tau"] == top]
    if any(row["drift"] < 0 for row in top_rows):
        return None
    return {
        "direction": [str(x) for x in w],
        "top_all_source_tau": str(top),
        "top_channels": [
            {"name": row["name"], "w_dot_nu": str(row["drift"]),
             "neutral": row["drift"] == 0}
            for row in top_rows
        ],
        "active_channel_count": sum(row["drift"] != 0 for row in rows),
    }


def z3_rational(x: F):
    return z3.RealVal(f"{x.numerator}/{x.denominator}")


def z3_dot(vector: Sequence[F], variables: Sequence[Any]):
    return z3.Sum([z3_rational(a) * v for a, v in zip(vector, variables)])


def z3_max(expressions: Sequence[Any]):
    out = expressions[0]
    for expression in expressions[1:]:
        out = z3.If(out >= expression, out, expression)
    return out


def model_fraction(value: Any) -> F:
    value = z3.simplify(value)
    if not z3.is_rational_value(value):
        raise ValueError(f"solver returned a non-rational Real model value: {value}")
    return F(value.numerator_as_long(), value.denominator_as_long())


def formula_for_outward_edge(edges: Sequence[Edge], dimension: int, bad_index: int):
    w = [z3.Real(f"w_{i}") for i in range(dimension)]
    projected = [z3_dot(edge.nu, w) for edge in edges]
    tau = []
    for edge in edges:
        hp = z3_max([z3_dot(term.exponent, w) for term in edge.P])
        hq = z3_max([z3_dot(term.exponent, w) for term in edge.Q])
        tau.append(hp - hq)
    constraints = [projected[bad_index] > 0]
    for j in range(len(edges)):
        constraints.append(z3.Implies(projected[j] != 0, tau[bad_index] >= tau[j]))
    return w, z3.And(*constraints)


def formula_for_strong_failure(edges: Sequence[Edge], dimension: int):
    """A direction with an active edge but no inward edge at global max source."""
    w = [z3.Real(f"sw_{i}") for i in range(dimension)]
    projected = [z3_dot(edge.nu, w) for edge in edges]
    tau = []
    for edge in edges:
        hp = z3_max([z3_dot(term.exponent, w) for term in edge.P])
        hq = z3_max([z3_dot(term.exponent, w) for term in edge.Q])
        tau.append(hp - hq)
    top_all = z3_max(tau)
    constraints = [z3.Or(*[value != 0 for value in projected])]
    constraints.extend(z3.Implies(tau[i] == top_all, projected[i] >= 0)
                       for i in range(len(edges)))
    return w, z3.And(*constraints)


def recognize(edges: Sequence[Edge], dimension: int, *, property_name: str,
              timeout_ms: int | None, max_checks: int | None,
              rlimit: int | None) -> dict[str, Any]:
    if z3 is None:
        return {"status": "UNKNOWN", "reason": "z3-solver Python package is unavailable",
                "checks_completed": 0}
    started = time.monotonic()
    unsat_edges: list[str] = []
    checks = 0
    for i, edge in enumerate(edges):
        if max_checks is not None and checks >= max_checks:
            return {"status": "UNKNOWN", "reason": "check budget exhausted",
                    "checks_completed": checks, "unsat_candidates": unsat_edges,
                    "requested_property": property_name}
        remaining_ms = None
        if timeout_ms is not None:
            remaining_ms = timeout_ms - int(1000 * (time.monotonic() - started))
            if remaining_ms <= 0:
                return {"status": "UNKNOWN", "reason": "wall-clock budget exhausted",
                        "checks_completed": checks, "unsat_candidates": unsat_edges,
                        "requested_property": property_name}
        w, formula = formula_for_outward_edge(edges, dimension, i)
        solver = z3.Solver()
        if remaining_ms is not None:
            solver.set(timeout=remaining_ms)
        if rlimit is not None:
            solver.set(rlimit=rlimit)
        solver.add(formula)
        result = solver.check()
        checks += 1
        if result == z3.sat:
            model = solver.model()
            try:
                witness = tuple(model_fraction(model.eval(variable, model_completion=True))
                                for variable in w)
            except ValueError as exc:
                return {"status": "UNKNOWN", "reason": str(exc),
                        "checks_completed": checks, "candidate_edge": edge.name,
                        "requested_property": property_name}
            verified = exact_failure(edges, witness)
            if verified is None:
                return {"status": "UNKNOWN",
                        "reason": "SAT model failed independent exact Fraction validation",
                        "checks_completed": checks, "candidate_edge": edge.name,
                        "requested_property": property_name,
                        "candidate_direction": [str(x) for x in witness]}
            return {"status": "REFUTED", "checks_completed": checks,
                    "candidate_edge": edge.name, "witness": verified,
                    "requested_property": property_name,
                    "reason": "an outward channel is tied at the maximum active source score"}
        if result == z3.unknown:
            return {"status": "UNKNOWN", "reason": solver.reason_unknown(),
                    "checks_completed": checks, "unsat_candidates": unsat_edges,
                    "requested_property": property_name}
        unsat_edges.append(edge.name)

    # Endotacticity is one clause of strong endotacticity. Only after it passes
    # do we ask whether every non-orthogonal direction has an inward arrow at
    # the global (all-channel, including neutral) source maximum.
    if property_name == "strong":
        if max_checks is not None and checks >= max_checks:
            return {"status": "UNKNOWN", "reason": "check budget exhausted before strong-source query",
                    "checks_completed": checks, "unsat_candidates": unsat_edges,
                    "requested_property": property_name}
        remaining_ms = None
        if timeout_ms is not None:
            remaining_ms = timeout_ms - int(1000 * (time.monotonic() - started))
            if remaining_ms <= 0:
                return {"status": "UNKNOWN", "reason": "wall-clock budget exhausted before strong-source query",
                        "checks_completed": checks, "unsat_candidates": unsat_edges,
                        "requested_property": property_name}
        w, formula = formula_for_strong_failure(edges, dimension)
        solver = z3.Solver()
        if remaining_ms is not None:
            solver.set(timeout=remaining_ms)
        if rlimit is not None:
            solver.set(rlimit=rlimit)
        solver.add(formula)
        result = solver.check()
        checks += 1
        if result == z3.sat:
            model = solver.model()
            try:
                witness = tuple(model_fraction(model.eval(variable, model_completion=True))
                                for variable in w)
            except ValueError as exc:
                return {"status": "UNKNOWN", "reason": str(exc),
                        "checks_completed": checks, "requested_property": property_name}
            verified = exact_strong_failure(edges, witness)
            if verified is None:
                return {"status": "UNKNOWN",
                        "reason": "strong SAT model failed independent exact Fraction validation",
                        "checks_completed": checks, "requested_property": property_name,
                        "candidate_direction": [str(x) for x in witness]}
            return {"status": "REFUTED", "checks_completed": checks,
                    "requested_property": property_name,
                    "reason": "no inward channel is present at the global all-source maximum",
                    "witness": verified}
        if result == z3.unknown:
            return {"status": "UNKNOWN", "reason": solver.reason_unknown(),
                    "checks_completed": checks, "unsat_candidates": unsat_edges,
                    "requested_property": property_name}
        return {"status": "CERTIFIED", "checks_completed": checks,
                "requested_property": property_name,
                "solver": f"Z3 {z3.get_version_string()}",
                "exact_theory": "quantifier-free linear real arithmetic with exact rationals and ITE",
                "trust_basis": "exact Z3 UNSAT answers; no separately checked proof object is emitted",
                "unsat_candidates": unsat_edges,
                "meaning": "endotacticity holds and every non-orthogonal direction has an inward arrow at its global all-source maximum"}
    return {"status": "CERTIFIED", "checks_completed": checks,
            "requested_property": property_name,
            "solver": f"Z3 {z3.get_version_string()}",
            "exact_theory": "quantifier-free linear real arithmetic with exact rationals and ITE",
            "trust_basis": "exact Z3 UNSAT answers; no separately checked proof object is emitted",
            "unsat_candidates": unsat_edges,
            "meaning": "no direction has an outward active channel tied at the maximum active tropical order"}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--property", choices=("endotactic", "strong"), default="endotactic",
                        help="check essential-source endotacticity or standard strong endotacticity of the positive lift")
    parser.add_argument("--timeout-ms", type=int, default=None,
                        help="total wall-clock budget across channel queries; expiration returns UNKNOWN")
    parser.add_argument("--max-checks", type=int, default=None,
                        help="maximum per-channel exact solver queries; exhaustion returns UNKNOWN")
    parser.add_argument("--rlimit", type=int, default=None,
                        help="Z3 resource limit for each query; exhaustion returns UNKNOWN")
    args = parser.parse_args(argv[1:])
    if args.timeout_ms is not None and args.timeout_ms < 0:
        parser.error("--timeout-ms must be nonnegative")
    if args.max_checks is not None and args.max_checks < 0:
        parser.error("--max-checks must be nonnegative")
    if args.rlimit is not None and args.rlimit < 0:
        parser.error("--rlimit must be nonnegative")
    try:
        data = json.loads(args.input.read_text())
        edges, dimension = parse_network(data)
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "reason": str(exc)}, indent=2))
        return 2
    result = recognize(edges, dimension, property_name=args.property,
                       timeout_ms=args.timeout_ms,
                       max_checks=args.max_checks, rlimit=args.rlimit)
    result["input"] = str(args.input)
    result["dimension"] = dimension
    result["channels"] = len(edges)
    result["support_terms"] = sum(len(e.P) + len(e.Q) for e in edges)
    print(json.dumps(result, indent=2, sort_keys=True))
    return {"CERTIFIED": 0, "REFUTED": 1, "UNKNOWN": 3}.get(result["status"], 2)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
