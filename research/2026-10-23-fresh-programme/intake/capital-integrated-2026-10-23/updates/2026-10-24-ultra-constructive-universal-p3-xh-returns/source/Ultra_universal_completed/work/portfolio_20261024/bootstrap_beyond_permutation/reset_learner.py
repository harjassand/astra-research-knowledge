#!/usr/bin/env python3
"""Count-only rank-two reset acquisition. No private plant import or probability oracle.

Inputs are integer Bernoulli counts and a supplied full-Hankel rank bound.
All fitting/certification arithmetic is rational. The actual reset weight is
a B-bit dyadic, so selection uses a fixed number of fresh fair bits.
"""
import argparse
import json
from fractions import Fraction
from pathlib import Path


def ratio(value):
    return {"numerator": value.numerator, "denominator": value.denominator,
            "decimal": float(value)}


def acquire(data, bits=16, tolerance=Fraction(1, 20)):
    if set(data) != {"interface", "calibration"}:
        raise ValueError("Pass the whitelisted learner_input.json, without source/audit metadata")
    interface = data["interface"]
    if set(interface) != {"full_controlled_hankel_rank_upper_bound", "reset_control_durations"}:
        raise ValueError("Unexpected metadata in the learner interface")
    if interface["full_controlled_hankel_rank_upper_bound"] != 2:
        raise ValueError("This certificate requires the supplied full rank bound two")
    if bits < 1 or bits > 64:
        raise ValueError("Supported fixed sampling precision is 1..64 bits")
    if interface["reset_control_durations"] != {"a": 1, "b": 1}:
        raise ValueError("Equal-duration physical control contract is required")
    cal = data["calibration"]
    if set(cal) != {"samples_per_setting", "error_width", "settings"}:
        raise ValueError("Cost/provenance metadata belongs outside learner input")
    if cal["samples_per_setting"] != 50_000 or cal["error_width"] != [1, 100]:
        raise ValueError("This executable uses the fixed prospectively declared count budget")
    settings = cal["settings"]
    expected = {(prep, macro) for prep in ("initial", "a", "b")
                for macro in ("none", "a", "b")}
    cells = {}
    for cell in settings:
        if set(cell) != {"preparation", "macro", "trials", "ones"}:
            raise ValueError("Unexpected metadata in count cell")
        key = (cell["preparation"], cell["macro"])
        if key in cells or key not in expected:
            raise ValueError("Duplicate or undeclared experiment cell")
        n, ones = cell["trials"], cell["ones"]
        if n != 50_000 or not (0 <= ones <= n):
            raise ValueError("Invalid integer counts")
        cells[key] = Fraction(ones, n)
    if set(cells) != expected:
        raise ValueError("The simultaneous event requires all nine cells")
    # e > 27/10, from its positive Taylor series. Hence 18*e^-10 is
    # rigorously upper bounded by this rational (rather than a float exp).
    alpha_upper = 18 * Fraction(10, 27) ** 10
    w = Fraction(1, 100)
    prep0 = "initial"
    prep1 = max(("a", "b"),
                key=lambda name: (abs(cells[name, "none"] - cells[prep0, "none"]), name))
    gap_hat = cells[prep1, "none"] - cells[prep0, "none"]
    gap_lower = abs(gap_hat) - 2*w
    result = {"status": "UNKNOWN", "supplied_rank_bound": 2,
              "basis_preparations": [prep0, prep1],
              "basis_gap_estimate": ratio(gap_hat),
              "basis_gap_lower": ratio(gap_lower),
              "simultaneous_calibration_failure_upper": ratio(alpha_upper),
              "confidence_event_cell_count": len(cells),
              "precision_bits_per_reset": bits,
              "requested_reset_tolerance": ratio(tolerance),
              "target_contract": "new physical preparation S(rho0); not original rho0",
              "record_contract": "fresh private fixed-bit selection; word/key/reset outcomes withheld; done at time one"}
    if gap_lower <= 0:
        result["reason"] = "No certified complete rank-two basis"
        return result
    contrast = {u: cells[prep1, u]-cells[prep0, u] for u in ("a", "b")}
    da, db = contrast["a"], contrast["b"]
    if da == db:
        result["reason"] = "No distinct control contrasts in this library"
        return result
    exact_weight = -db/(da-db)
    if not 0 <= exact_weight <= 1:
        result["reason"] = "Observed zero contrast outside positive control hull"
        return result
    denominator = 1 << bits
    scaled = exact_weight * denominator
    # Round nearest; exact half goes upward. No floating arithmetic in fit.
    numerator = (2*scaled.numerator + scaled.denominator)//(2*scaled.denominator)
    weight = Fraction(numerator, denominator)
    residual = abs(weight*da+(1-weight)*db)
    epsilon = min(Fraction(1), (residual+2*w)/(gap_lower*gap_lower))
    result.update({"status": "CERTIFIED" if epsilon <= tolerance else "UNKNOWN",
                   "reason": "Acquired positive fixed-duration nonselective preparation"
                             if epsilon <= tolerance else "Uniform certificate above requested tolerance",
                   "observed_control_contrasts": {u: ratio(d) for u, d in contrast.items()},
                   "zero_contrast_rational_weight_a": ratio(exact_weight),
                   "implemented_weight_a": ratio(weight),
                   "dyadic_selection": {"a_threshold": numerator, "range_size": denominator},
                   "implemented_empirical_contrast_residual": ratio(residual),
                   "uniform_all_future_tv_diameter_certificate": ratio(epsilon),
                   "rational_storage_max_integer_bits": max(
                       v.bit_length() for f in (gap_lower, exact_weight, weight, residual, epsilon)
                       for v in (abs(f.numerator), f.denominator))})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("counts", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--bits", type=int, default=16)
    args = parser.parse_args()
    result = acquire(json.loads(args.counts.read_text()), bits=args.bits)
    args.out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "basis": result["basis_preparations"],
                      "epsilon": result.get("uniform_all_future_tv_diameter_certificate"),
                      "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
