#!/usr/bin/env python3
"""Fail-closed isotope-inventory certificate for a CO-dimer alternative.

This checker consumes measured confidence bounds; it never supplies chemistry
parameters, detection limits, isotope fractions, or missing pool estimates.
All quantities use mol of molecules or mol of carbon atoms as named in the
input schema. One labeled carbon atom can contribute to at most one final
acetate molecule, so the molar inequality is dimensionally consistent.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


BOUND_FIELDS = (
    "old_13c_non_ch2_co_eligible_atoms_upper_mol",
    "old_13c_ch2_to_reactive_co_atoms_upper_mol",
    "13c_feed_or_impurity_atoms_upper_mol",
    "background_and_cross_talk_atoms_upper_mol",
)
REQUIRED_VALIDATIONS = (
    "co_accessible_bound_complete",
    "ch2_isotope_assignment_validated",
    "ketene_label_followthrough_validated",
    "other_pre_reduced_c1_sources_bounded",
)


def _number(value: Any, name: str) -> Decimal:
    if value is None or isinstance(value, bool):
        raise ValueError(f"missing numeric measurement bound: {name}")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"invalid decimal measurement bound: {name}") from exc
    if not result.is_finite() or result < 0:
        raise ValueError(f"bound must be finite and nonnegative: {name}")
    return result


def assess(data: dict[str, Any]) -> dict[str, Any]:
    """Return a conservative decision from measured interval endpoints."""
    validations = data.get("validation", {})
    missing_validations = [
        field for field in REQUIRED_VALIDATIONS if validations.get(field) is not True
    ]

    try:
        if data.get("units") != "mol":
            raise ValueError("units must be 'mol' for both molecule and atom amounts")
        observation = data.get("observed", {})
        y_lower = _number(
            observation.get("methyl_13c_acetate_lower_mol"),
            "methyl_13c_acetate_lower_mol",
        )
        bounds = data.get("upper_bounds", {})
        values = {field: _number(bounds.get(field), field) for field in BOUND_FIELDS}
    except ValueError as exc:
        return {
            "decision": "UNKNOWN",
            "reason": str(exc),
            "missing_validation_flags": missing_validations,
        }

    if validations.get("co_accessible_bound_complete") is not True:
        return {
            "decision": "UNKNOWN",
            "reason": "the upper bound must include every unique old-label atom that could enter active CO during the collection window",
            "missing_validation_flags": missing_validations,
        }

    dimer_budget = sum(values.values(), Decimal(0))
    if y_lower <= dimer_budget:
        return {
            "decision": "NO_SEPARATION",
            "reason": "the measured labeled-acetate lower bound does not exceed the conservative all-CO label budget; this does not establish the dimer route",
            "methyl_13c_acetate_lower_mol": str(y_lower),
            "all_co_label_budget_upper_mol": str(dimer_budget),
            "budget_terms_mol": {key: str(value) for key, value in values.items()},
            "missing_validation_flags": missing_validations,
        }

    if missing_validations:
        return {
            "decision": "DIMER_ONLY_REFUTED_OTHER_ROUTE_UNRESOLVED",
            "reason": "the label mass balance excludes a CO-CO-only C-C step, but the route-specific CH2-to-ketene link or alternative C1 pools are not fully validated",
            "methyl_13c_acetate_lower_mol": str(y_lower),
            "all_co_label_budget_upper_mol": str(dimer_budget),
            "budget_terms_mol": {key: str(value) for key, value in values.items()},
            "missing_validation_flags": missing_validations,
        }

    return {
        "decision": "DIRECT_CH2_SUPPORTED_WITHIN_REGISTERED_NETWORK",
        "reason": "the measured product label exceeds the complete CO-accessible label budget, and CH2-to-ketene follow-through is validated with other reduced-C1 sources bounded",
        "methyl_13c_acetate_lower_mol": str(y_lower),
        "all_co_label_budget_upper_mol": str(dimer_budget),
        "budget_terms_mol": {key: str(value) for key, value in values.items()},
        "missing_validation_flags": [],
        "scope": "conditional on the registered candidate network and validity of supplied measurement bounds",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path, help="measured interval bounds in the documented schema")
    args = parser.parse_args()
    try:
        data = json.loads(args.input_json.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"decision": "UNKNOWN", "reason": str(exc)}, indent=2))
        raise SystemExit(2)
    result = assess(data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
