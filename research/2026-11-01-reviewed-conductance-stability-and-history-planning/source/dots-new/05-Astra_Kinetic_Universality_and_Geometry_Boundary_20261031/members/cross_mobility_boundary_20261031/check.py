#!/usr/bin/env python3
"""Exact algebra/adversarial receiver checks and finite executed certificates."""
from copy import deepcopy
from fractions import Fraction as Q
import json
from pathlib import Path
from receive import receive, strict_json_loads, SCHEMA

ROOT = Path(__file__).resolve().parent


def source(k, n, d):
    return {"schema": SCHEMA, "k": k, "epsilon": {"numerator": n, "denominator": d}}


def q(item):
    return Q(int(item["numerator"]), int(item["denominator"]))


def main():
    total = 0
    for y in [Q(i, 8) for i in range(-24, 25)]:
        v = 1 + (1 - y*y)**2
        assert v >= 1
        assert v - y**4/2 == (y*y-2)**2/2
        assert 6*y**4-8*y*y+4 == 6*(y*y-Q(2,3))**2+Q(4,3)
        if abs(y) <= Q(1, 2):
            assert Q(25,16) <= v <= 2
        if Q(1,2) <= abs(y) <= 1:
            assert v <= Q(25,16)
        total += 1
    # Exact quadratic energy identities at rational test points. The algebraic
    # coefficient equalities below additionally check the entire a,b polynomial.
    for eps in [Q(1, 1000000), Q(1, 4), Q(1, 2), Q(99, 100)]:
        for k in [1, 2, 7, 64]:
            gamma = Q(k*k)/(1-eps)
            alpha = (1-eps)/k
            assert 1-2*k*alpha+gamma*alpha*alpha == eps
            assert 2-2*k*alpha == 2*eps
            assert gamma-k*k > 0
            for a in [Q(-6), Q(0), Q(3, 2), Q(6)]:
                for b in [Q(-24), Q(0), Q(5, 2), Q(24)]:
                    p, r = a+b, -alpha*a
                    energy = p*p+2*k*p*r+gamma*r*r
                    assert energy == eps*a*a+2*eps*a*b+b*b
                    assert energy == eps*(a+b)**2+(1-eps)*b*b
                    assert energy <= 900
                    assert energy == eps*p*p+gamma*(r+alpha*p)**2
                    assert energy == (p+k*r)**2+(gamma-k*k)*r*r
                    total += 1
    bad = []
    base = source(16, 1, 100)
    for k in [0, -1, True, 1.0, "16"]:
        x = deepcopy(base); x["k"] = k; bad.append(x)
    for n, d in [(0,1),(-1,2),(1,1),(2,1),(2,4),(1,-2),(1,0),(True,2),(1,2.0)]:
        bad.append(source(16,n,d))
    x=deepcopy(base); x["extra"]=1; bad.append(x)
    x=deepcopy(base); x["schema"]="arbitrary_potential"; bad.append(x)
    x=deepcopy(base); x["epsilon"]["extra"]=1; bad.append(x)
    bad.extend([None, [], {}, "model"])
    for item in bad:
        try:
            receive(item)
        except (ValueError, TypeError):
            pass
        else:
            raise AssertionError(f"bad input accepted: {item!r}")
    for raw in [
        '{"schema":"x","schema":"y"}',
        '{"epsilon":{"numerator":1,"numerator":2,"denominator":3}}',
    ]:
        try:
            strict_json_loads(raw)
        except ValueError:
            pass
        else:
            raise AssertionError("duplicate raw JSON key accepted")
    try:
        receive(source(10**20, 1, 2))
    except ValueError as error:
        assert "resource_budget" in str(error)
    else:
        raise AssertionError("resource budget not enforced before huge power allocation")
    certificates = []
    summary = []
    for exponent in [2, 4, 6, 8]:
        item = source(16*exponent, 1, 10**exponent)
        cert = receive(item)
        lo, hi = (q(cert["capacity_normalized"][key]) for key in ["lower", "upper"])
        conductance = q(cert["capacity_over_basin_mass"]["upper"])
        assert 0 < lo <= hi and conductance == 4*hi
        assert q(cert["model"]["longitudinal_schur_complement"]) == Q(1,10**exponent)
        certificates.append(cert)
        summary.append({
            "k": item["k"], "epsilon": f"1/{10**exponent}",
            "capacity_lower_float_diagnostic": float(lo),
            "capacity_upper_float_diagnostic": float(hi),
            "conductance_upper_float_diagnostic": float(conductance),
            "condition_number_lower_float_diagnostic": float(q(cert["eigenvalue_condition_number"]["lower"])),
        })
    result = {
        "status": "PASS", "exact_identity_grid_checks": total,
        "adversarial_rejections": len(bad), "duplicate_key_rejections": 2, "resource_budget_rejections": 1, "finite_certificates": len(certificates),
        "summary": summary,
        "warning": "Float summaries are diagnostics; exact guarantees are the rational certificate objects. Checks complement rather than replace PROOF.md."
    }
    (ROOT/"certificates.json").write_text(json.dumps(certificates, indent=2, sort_keys=True)+"\n")
    (ROOT/"check_results.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
