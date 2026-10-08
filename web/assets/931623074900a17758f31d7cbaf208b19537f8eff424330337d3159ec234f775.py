#!/usr/bin/env python3
"""Small independent checker for certificate_compiler.py output.

This file deliberately contains no Fourier--Motzkin/LP code. It rebuilds the
original rational rows from the input JSON and checks only the claimed
witness or Gordan multiplier identities.
"""

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


def rational(value, where):
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError(f"{where}: expected integer or rational string")
    try:
        return Fraction(str(value))
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{where}: invalid rational") from exc


def qstr(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def interval(value, where):
    if isinstance(value, list):
        if len(value) != 2:
            raise ValueError(f"{where}: interval must have two endpoints")
        lo, hi = rational(value[0], where + ".lo"), rational(value[1], where + ".hi")
    else:
        lo = hi = rational(value, where)
    if lo <= 0 or lo > hi:
        raise ValueError(f"{where}: require 0 < lower <= upper")
    return lo, hi


def make_rows(raw):
    if not isinstance(raw, dict):
        raise ValueError("input root must be an object")
    k = raw.get("k")
    if not isinstance(k, list) or not k or not isinstance(k[0], list) or not k[0]:
        raise ValueError("k must be a nonempty matrix")
    r, s = len(k), len(k[0])
    for j, row in enumerate(k):
        if not isinstance(row, list) or len(row) != s:
            raise ValueError("k must be rectangular")
        if any(isinstance(v, bool) or not isinstance(v, int) or v < 1 for v in row):
            raise ValueError(f"k[{j}] must contain integers >= 1")
    rates = raw.get("rates")
    if not isinstance(rates, dict) or set(rates) != {"alpha", "delta", "p", "q", "u", "v"}:
        raise ValueError("rates must contain exactly alpha, delta, p, q, u, v")

    def vec(name):
        arr = rates[name]
        if not isinstance(arr, list) or len(arr) != r:
            raise ValueError(f"rates.{name} must have length {r}")
        return [interval(x, f"rates.{name}[{j}]") for j, x in enumerate(arr)]

    def mat(name):
        arr = rates[name]
        if not isinstance(arr, list) or len(arr) != r:
            raise ValueError(f"rates.{name} must be {r}x{s}")
        out = []
        for j, row in enumerate(arr):
            if not isinstance(row, list) or len(row) != s:
                raise ValueError(f"rates.{name}[{j}] must have length {s}")
            out.append([interval(x, f"rates.{name}[{j}][{i}]") for i, x in enumerate(row)])
        return out

    alpha, delta = vec("alpha"), vec("delta")
    p, q, u, v = mat("p"), mat("q"), mat("u"), mat("v")
    n = r + s
    names, rows = [], []

    def add(name, terms):
        row = [Fraction(0) for _ in range(n)]
        for index, value in terms.items():
            row[index] += value
        names.append(name)
        rows.append(tuple(row))

    for j in range(r):
        add(f"lambda_positive[{j}]", {j: Fraction(1)})
    for i in range(s):
        add(f"w_positive[{i}]", {r + i: Fraction(1)})
    for j in range(r):
        terms = {j: delta[j][0]}
        for i in range(s):
            terms[r + i] = -p[j][i][1]
        add(f"gamma[{j}]", terms)
    for j in range(r):
        for i in range(s):
            add(f"eta[{j},{i}]", {j: -k[j][i] * u[j][i][1], r + i: q[j][i][0]})
    return r, s, alpha, names, rows


def verify(raw, cert):
    r, s, alpha, names, rows = make_rows(raw)
    canonical = json.dumps(raw, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    if cert.get("format") != "reaction-dynamics-foster-lp-certificate-v1":
        raise ValueError("unknown certificate format")
    if cert.get("input_sha256_canonical_json") != digest:
        raise ValueError("certificate input hash mismatch")
    if cert.get("dimensions") != {"r": r, "s": s, "variables": r + s, "strict_rows": len(rows)}:
        raise ValueError("certificate dimensions mismatch")

    if cert.get("status") == "feasible":
        witness = cert.get("witness")
        if not isinstance(witness, dict):
            raise ValueError("missing witness")
        lam = [rational(x, "lambda") for x in witness.get("lambda", [])]
        w = [rational(x, "w") for x in witness.get("w", [])]
        if len(lam) != r or len(w) != s:
            raise ValueError("witness dimension mismatch")
        z = lam + w
        vals = [sum((a * x for a, x in zip(row, z)), Fraction(0)) for row in rows]
        if any(value <= 0 for value in vals):
            raise ValueError("strict LP inequality failed")
        recomputed_slacks = [{"name": name, "slack": qstr(value)} for name, value in zip(names, vals)]
        if cert.get("strict_slacks") != recomputed_slacks:
            raise ValueError("strict slack listing mismatch")
        K, rho = rational(witness.get("K"), "K"), rational(witness.get("rho"), "rho")
        if rho <= 0 or any(K <= x for x in lam):
            raise ValueError("K>max(lambda) and rho>0 are required")
        weighted_low = sum((a[0] * (K - x) for a, x in zip(alpha, lam)), Fraction(0))
        if weighted_low <= rho:
            raise ValueError("robust boundary inequality fails")
        boundary = {
            "K_minus_lambda": [qstr(K - x) for x in lam],
            "uniform_lower_bound_sum_alpha_times_K_minus_lambda": qstr(weighted_low),
            "rho": qstr(rho),
            "uniform_strict_margin": qstr(weighted_low - rho),
        }
        if cert.get("boundary_check") != boundary:
            raise ValueError("boundary check listing mismatch")
        return {"verified": True, "status": "feasible", "strict_rows_checked": len(rows),
                "K": qstr(K), "rho": qstr(rho)}

    if cert.get("status") == "infeasible":
        proof = cert.get("gordan_farkas")
        if not isinstance(proof, dict) or not isinstance(proof.get("multipliers"), dict):
            raise ValueError("missing Farkas multiplier map")
        multipliers = proof["multipliers"]
        if set(multipliers) != set(names):
            raise ValueError("multiplier labels mismatch")
        y = [rational(multipliers[name], "multiplier") for name in names]
        if any(x < 0 for x in y) or not any(x > 0 for x in y):
            raise ValueError("multipliers must be nonnegative and nonzero")
        n = r + s
        residual = [sum((y[t] * rows[t][j] for t in range(len(rows))), Fraction(0)) for j in range(n)]
        if any(x != 0 for x in residual):
            raise ValueError("Farkas normals do not cancel")
        total = sum(y, Fraction(0))
        if rational(proof.get("sum_multipliers"), "sum_multipliers") != total:
            raise ValueError("multiplier total mismatch")
        return {"verified": True, "status": "infeasible", "strict_rows_checked": len(rows),
                "nonzero_multipliers": sum(x > 0 for x in y), "sum_multipliers": qstr(total)}
    raise ValueError("certificate status must be feasible or infeasible")


def main(argv):
    if len(argv) != 3:
        print("usage: verify_certificate.py INPUT.json CERTIFICATE.json", file=sys.stderr)
        return 2
    try:
        raw = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        cert = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
        print(json.dumps(verify(raw, cert), sort_keys=True))
        return 0
    except Exception as exc:
        print(f"verify_certificate: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
