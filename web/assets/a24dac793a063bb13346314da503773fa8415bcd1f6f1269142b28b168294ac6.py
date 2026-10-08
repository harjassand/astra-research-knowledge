#!/usr/bin/env python3
"""Exact rational certificate compiler/checker for the multi-catalyst Foster LP.

The LP rows are strict homogeneous inequalities in lambda_j,w_i. Rate cells
are either a rational string (singleton) or [lower, upper]. All calculations
use fractions.Fraction; no floating-point decisions are made.

Usage:
  python3 certificate_compiler.py solve INPUT.json -o CERTIFICATE.json
  python3 certificate_compiler.py verify INPUT.json CERTIFICATE.json

The solver uses Fourier--Motzkin elimination with exact nonnegative row
combinations. It is complete as a finite mathematical algorithm, but has
exponential worst-case row/memory growth. The independent verifier does not
rerun elimination: it checks a strict rational witness or a Gordan/Farkas
multiplier vector against rows rebuilt from INPUT.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


Q = Fraction


def qstr(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def parse_q(x: Any, where: str) -> Fraction:
    if isinstance(x, bool) or not isinstance(x, (str, int)):
        raise ValueError(f"{where}: expected integer or rational string, got {x!r}")
    try:
        return Fraction(str(x))
    except (ValueError, ZeroDivisionError) as e:
        raise ValueError(f"{where}: invalid rational {x!r}") from e


def parse_interval(x: Any, where: str) -> tuple[Fraction, Fraction]:
    if isinstance(x, list):
        if len(x) != 2:
            raise ValueError(f"{where}: interval must have exactly [lower, upper]")
        lo, hi = parse_q(x[0], where + ".lo"), parse_q(x[1], where + ".hi")
    else:
        lo = hi = parse_q(x, where)
    if not (0 < lo <= hi):
        raise ValueError(f"{where}: require 0 < lower <= upper")
    return lo, hi


def canonical_input(raw: dict[str, Any]) -> str:
    return json.dumps(raw, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def interval_vector(x: Any, r: int, name: str) -> list[tuple[Fraction, Fraction]]:
    if not isinstance(x, list) or len(x) != r:
        raise ValueError(f"rates.{name}: expected vector of length {r}")
    return [parse_interval(v, f"rates.{name}[{i}]") for i, v in enumerate(x)]


def interval_matrix(x: Any, r: int, s: int, name: str) -> list[list[tuple[Fraction, Fraction]]]:
    if not isinstance(x, list) or len(x) != r:
        raise ValueError(f"rates.{name}: expected {r}x{s} matrix")
    out = []
    for j, row in enumerate(x):
        if not isinstance(row, list) or len(row) != s:
            raise ValueError(f"rates.{name}[{j}]: expected row of length {s}")
        out.append([parse_interval(v, f"rates.{name}[{j}][{i}]") for i, v in enumerate(row)])
    return out


@dataclass(frozen=True)
class Row:
    name: str
    a: tuple[Fraction, ...]
    y: tuple[Fraction, ...]  # nonnegative combination of original rows


def parse_problem(raw: dict[str, Any]) -> tuple[int, int, list[list[int]], dict[str, Any], list[Row], list[str], Fraction]:
    if not isinstance(raw, dict):
        raise ValueError("input root must be a JSON object")
    k = raw.get("k")
    if not isinstance(k, list) or not k or not isinstance(k[0], list) or not k[0]:
        raise ValueError("k must be a nonempty rectangular integer matrix")
    r, s = len(k), len(k[0])
    kk: list[list[int]] = []
    for j, row in enumerate(k):
        if not isinstance(row, list) or len(row) != s:
            raise ValueError("k must be rectangular")
        clean = []
        for i, entry in enumerate(row):
            if isinstance(entry, bool) or not isinstance(entry, int) or entry < 1:
                raise ValueError(f"k[{j}][{i}] must be an integer >= 1")
            clean.append(entry)
        kk.append(clean)

    rates = raw.get("rates")
    if not isinstance(rates, dict):
        raise ValueError("rates must be an object")
    required = {"alpha", "delta", "p", "q", "u", "v"}
    missing = required - rates.keys()
    extra = rates.keys() - required
    if missing or extra:
        raise ValueError(f"rates keys mismatch; missing={sorted(missing)}, extra={sorted(extra)}")
    rr: dict[str, Any] = {
        "alpha": interval_vector(rates["alpha"], r, "alpha"),
        "delta": interval_vector(rates["delta"], r, "delta"),
        "p": interval_matrix(rates["p"], r, s, "p"),
        "q": interval_matrix(rates["q"], r, s, "q"),
        "u": interval_matrix(rates["u"], r, s, "u"),
        "v": interval_matrix(rates["v"], r, s, "v"),
    }

    n = r + s
    names: list[str] = []
    coeffs: list[tuple[Fraction, ...]] = []

    def add(name: str, entries: dict[int, Fraction]) -> None:
        row = [Q(0) for _ in range(n)]
        for index, value in entries.items():
            row[index] += value
        names.append(name)
        coeffs.append(tuple(row))

    for j in range(r):
        add(f"lambda_positive[{j}]", {j: Q(1)})
    for i in range(s):
        add(f"w_positive[{i}]", {r + i: Q(1)})
    # Robust box endpoints are exact because all lambda_j,w_i are positive.
    for j in range(r):
        entries: dict[int, Fraction] = {j: rr["delta"][j][0]}
        for i in range(s):
            entries[r + i] = -rr["p"][j][i][1]
        add(f"gamma[{j}]", entries)
    for j in range(r):
        for i in range(s):
            add(f"eta[{j},{i}]", {j: -Q(kk[j][i]) * rr["u"][j][i][1],
                                    r + i: rr["q"][j][i][0]})
    m = len(names)
    rows = [Row(name, coeffs[t], tuple(Q(int(t == z)) for z in range(m))) for t, name in enumerate(names)]
    return r, s, kk, rr, rows, names, Q(n)


def normalize(row: Row) -> Row:
    first = next((x for x in row.a if x), None)
    if first is None:
        return row
    scale = abs(first)
    return Row(row.name, tuple(x / scale for x in row.a), tuple(x / scale for x in row.y))


def deduplicate(rows: Iterable[Row]) -> list[Row]:
    """Equivalent homogeneous strict rows have identical normalized normals."""
    result: dict[tuple[Fraction, ...], Row] = {}
    for row in rows:
        if not any(row.a):
            # For a homogeneous strict system, 0>0 is immediate infeasibility.
            result[tuple() + (Q(0),)] = row
            continue
        nr = normalize(row)
        old = result.get(nr.a)
        if old is None:
            result[nr.a] = nr
    return list(result.values())


def first_zero_row(rows: Iterable[Row]) -> Row | None:
    return next((row for row in rows if not any(row.a)), None)


def eliminate(rows: list[Row], variable: int) -> list[Row]:
    pos = [row for row in rows if row.a[variable] > 0]
    neg = [row for row in rows if row.a[variable] < 0]
    zero = [row for row in rows if row.a[variable] == 0]
    out = list(zero)
    for p in pos:
        for n in neg:
            cp, cn = p.a[variable], n.a[variable]
            wp, wn = -cn, cp
            a = tuple(wp * ap + wn * an for ap, an in zip(p.a, n.a))
            assert a[variable] == 0
            y = tuple(wp * yp + wn * yn for yp, yn in zip(p.y, n.y))
            out.append(Row(f"fm[{variable}]", a, y))
    out = deduplicate(out)
    contradiction = first_zero_row(out)
    if contradiction is not None:
        return [contradiction]
    return out


def choose_witness(rows: list[Row], stages: list[list[Row]], nvars: int) -> tuple[Fraction, ...]:
    x = [Q(0) for _ in range(nvars)]
    for variable in range(nvars - 1, -1, -1):
        lower: Fraction | None = None
        upper: Fraction | None = None
        for row in stages[variable]:
            c = row.a[variable]
            tail = sum((row.a[j] * x[j] for j in range(variable + 1, nvars)), Q(0))
            if c == 0:
                if not tail > 0:
                    raise ArithmeticError("back-substitution found an unsatisfied projected row")
                continue
            bound = -tail / c
            if c > 0:
                lower = bound if lower is None or bound > lower else lower
            else:
                upper = bound if upper is None or bound < upper else upper
        if lower is not None and upper is not None:
            if not lower < upper:
                raise ArithmeticError("Fourier--Motzkin projection did not leave an open interval")
            x[variable] = (lower + upper) / 2
        elif lower is not None:
            x[variable] = lower + 1
        elif upper is not None:
            x[variable] = upper - 1
        else:
            x[variable] = Q(0)
    if any(sum((a * b for a, b in zip(row.a, x)), Q(0)) <= 0 for row in rows):
        raise ArithmeticError("constructed witness failed original strict rows")
    return tuple(x)


def solve(rows: list[Row], nvars: int) -> tuple[str, tuple[Fraction, ...] | tuple[Fraction, ...], list[int]]:
    active = deduplicate(rows)
    stages: list[list[Row]] = []
    counts = [len(active)]
    contradiction = first_zero_row(active)
    if contradiction is not None:
        return "infeasible", contradiction.y, counts
    for j in range(nvars):
        stages.append(active)
        active = eliminate(active, j)
        counts.append(len(active))
        contradiction = first_zero_row(active)
        if contradiction is not None:
            return "infeasible", contradiction.y, counts
    return "feasible", choose_witness(rows, stages, nvars), counts


def slacks(rows: list[Row], x: tuple[Fraction, ...]) -> list[dict[str, str]]:
    # Rows are originals, so the names are one-hot multipliers.
    names = [row.name for row in rows]
    return [{"name": name, "slack": qstr(sum((a * b for a, b in zip(row.a, x)), Q(0)))}
            for name, row in zip(names, rows)]


def build_certificate(raw: dict[str, Any], input_bytes: bytes) -> tuple[dict[str, Any], list[int]]:
    r, s, _k, rates, rows, _names, _ = parse_problem(raw)
    status, data, counts = solve(rows, r + s)
    digest = hashlib.sha256(canonical_input(raw).encode("utf-8")).hexdigest()
    cert: dict[str, Any] = {
        "format": "reaction-dynamics-foster-lp-certificate-v1",
        "input_sha256_canonical_json": digest,
        "status": status,
        "dimensions": {"r": r, "s": s, "variables": r + s, "strict_rows": len(rows)},
        "fourier_motzkin_rows_per_stage": counts,
    }
    if status == "feasible":
        x = data  # type: ignore[assignment]
        lam, w = x[:r], x[r:]
        K = max(lam) + 1
        alpha_lo_sum = sum((a[0] for a in rates["alpha"]), Q(0))
        rho = alpha_lo_sum / 2
        # K-lambda_j >= 1; for every alpha in its interval box,
        # sum alpha_j(K-lambda_j) >= sum alpha_j^- > rho.
        cert["witness"] = {
            "lambda": [qstr(xj) for xj in lam],
            "w": [qstr(xi) for xi in w],
            "K": qstr(K),
            "rho": qstr(rho),
        }
        cert["strict_slacks"] = slacks(rows, x)
        cert["boundary_check"] = {
            "K_minus_lambda": [qstr(K - xj) for xj in lam],
            "uniform_lower_bound_sum_alpha_times_K_minus_lambda": qstr(
                sum((a[0] * (K - xj) for a, xj in zip(rates["alpha"], lam)), Q(0))),
            "rho": qstr(rho),
            "uniform_strict_margin": qstr(
                sum((a[0] * (K - xj) for a, xj in zip(rates["alpha"], lam)), Q(0)) - rho),
        }
    else:
        y = data  # type: ignore[assignment]
        cert["gordan_farkas"] = {
            "multipliers": {row.name: qstr(yi) for row, yi in zip(rows, y)},
            "sum_multipliers": qstr(sum(y, Q(0))),
            "claim": "nonnegative nonzero combination of all strict row normals equals zero",
        }
    return cert, counts


def verify_certificate(raw: dict[str, Any], cert: dict[str, Any]) -> dict[str, Any]:
    r, s, _k, rates, rows, names, _ = parse_problem(raw)
    expected_hash = hashlib.sha256(canonical_input(raw).encode("utf-8")).hexdigest()
    if cert.get("format") != "reaction-dynamics-foster-lp-certificate-v1":
        raise ValueError("unknown certificate format")
    if cert.get("input_sha256_canonical_json") != expected_hash:
        raise ValueError("certificate is bound to different input JSON")
    if cert.get("dimensions") != {"r": r, "s": s, "variables": r + s, "strict_rows": len(rows)}:
        raise ValueError("dimension metadata mismatch")
    status = cert.get("status")
    if status == "feasible":
        wit = cert.get("witness")
        if not isinstance(wit, dict):
            raise ValueError("missing witness")
        lam = [parse_q(x, "witness.lambda") for x in wit.get("lambda", [])]
        w = [parse_q(x, "witness.w") for x in wit.get("w", [])]
        if len(lam) != r or len(w) != s:
            raise ValueError("witness dimension mismatch")
        x = tuple(lam + w)
        computed_slacks = slacks(rows, x)
        if any(Q(item["slack"]) <= 0 for item in computed_slacks):
            raise ValueError("witness does not satisfy all strict robust LP rows")
        K = parse_q(wit.get("K"), "witness.K")
        rho = parse_q(wit.get("rho"), "witness.rho")
        if rho <= 0 or any(K <= xj for xj in lam):
            raise ValueError("K or rho does not satisfy positivity/boundary condition")
        alpha_lo_sum = sum((a[0] for a in rates["alpha"]), Q(0))
        boundary_margin = sum((a[0] * (K - xj) for a, xj in zip(rates["alpha"], lam)), Q(0)) - rho
        if boundary_margin <= 0:
            raise ValueError("uniform boundary condition K alpha_sum > H+rho not verified")
        recorded = cert.get("strict_slacks")
        if recorded != computed_slacks:
            raise ValueError("recorded strict slacks do not match independently recomputed values")
        boundary = cert.get("boundary_check")
        alpha_low_weighted = sum((a[0] * (K - xj) for a, xj in zip(rates["alpha"], lam)), Q(0))
        expected_boundary = {
            "K_minus_lambda": [qstr(K - xj) for xj in lam],
            "uniform_lower_bound_sum_alpha_times_K_minus_lambda": qstr(alpha_low_weighted),
            "rho": qstr(rho),
            "uniform_strict_margin": qstr(alpha_low_weighted - rho),
        }
        if boundary != expected_boundary:
            raise ValueError("recorded boundary check does not match recomputation")
        return {"verified": True, "status": status, "strict_rows_checked": len(rows),
                "K": qstr(K), "rho": qstr(rho)}
    if status == "infeasible":
        data = cert.get("gordan_farkas")
        if not isinstance(data, dict) or not isinstance(data.get("multipliers"), dict):
            raise ValueError("missing Gordan/Farkas multiplier map")
        mult = data["multipliers"]
        if set(mult) != set(names):
            raise ValueError("Farkas multiplier labels do not match the LP rows")
        y = [parse_q(mult[name], f"multiplier.{name}") for name in names]
        if any(value < 0 for value in y) or not any(value > 0 for value in y):
            raise ValueError("Farkas multipliers must be nonnegative and nonzero")
        n = r + s
        at_y = [sum((y[t] * rows[t].a[j] for t in range(len(rows))), Q(0)) for j in range(n)]
        if any(value != 0 for value in at_y):
            raise ValueError("Farkas combination does not cancel every variable coefficient")
        if parse_q(data.get("sum_multipliers"), "sum_multipliers") != sum(y, Q(0)):
            raise ValueError("recorded multiplier sum mismatch")
        return {"verified": True, "status": status, "strict_rows_checked": len(rows),
                "nonzero_multipliers": sum(value > 0 for value in y),
                "sum_multipliers": qstr(sum(y, Q(0)))}
    raise ValueError(f"unsupported status {status!r}")


def read_json(path: str) -> tuple[dict[str, Any], bytes]:
    data = Path(path).read_bytes()
    obj = json.loads(data)
    if not isinstance(obj, dict):
        raise ValueError("JSON root must be an object")
    return obj, data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    solve_p = sub.add_parser("solve", help="compile a witness or exact Farkas certificate")
    solve_p.add_argument("input")
    solve_p.add_argument("-o", "--output", default="-")
    verify_p = sub.add_parser("verify", help="independently verify a certificate")
    verify_p.add_argument("input")
    verify_p.add_argument("certificate")
    args = parser.parse_args(argv)
    try:
        raw, input_bytes = read_json(args.input)
        if args.command == "solve":
            cert, counts = build_certificate(raw, input_bytes)
            rendered = json.dumps(cert, indent=2, sort_keys=True) + "\n"
            if args.output == "-":
                sys.stdout.write(rendered)
            else:
                Path(args.output).write_text(rendered, encoding="utf-8")
            print(f"compiled {cert['status']} certificate; FM rows/stage={counts}", file=sys.stderr)
            return 0
        cert_obj = json.loads(Path(args.certificate).read_text(encoding="utf-8"))
        result = verify_certificate(raw, cert_obj)
        print(json.dumps(result, sort_keys=True))
        return 0
    except Exception as exc:
        print(f"certificate_compiler: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
