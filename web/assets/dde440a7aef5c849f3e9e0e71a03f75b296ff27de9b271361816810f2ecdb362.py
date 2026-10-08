#!/usr/bin/env python3
"""Compile a shared-enzyme alternative-substrate MM/QSSA module exactly.

The source law is v_i = kcat_i E_total (S_i/Km_i) /
(1 + sum_j S_j/Km_j), with paired flux -v_i on S_i and +v_i on P_i.
The compiler emits the sparse positive-rational interface used by
recognize_common_factor.py, together with a closed-form exact refutation
witness and a model-level substrate-extinction bound.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
from typing import Any


def q(raw: Any, label: str) -> F:
    if isinstance(raw, bool):
        raise ValueError(f"{label}: Boolean is not a rational")
    try:
        return F(str(raw))
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{label}: expected an exact rational, got {raw!r}") from exc


def text(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def compile_model(model: Any):
    if not isinstance(model, dict) or model.get("schema") != "alternative-substrates-qssa-v1":
        raise ValueError("schema must be alternative-substrates-qssa-v1")
    enzyme_total = q(model.get("enzyme_total"), "enzyme_total")
    if enzyme_total <= 0:
        raise ValueError("enzyme_total must be strictly positive")
    channels = model.get("channels")
    if not isinstance(channels, list) or not channels:
        raise ValueError("channels must be a nonempty list")
    names = []
    for i, item in enumerate(channels):
        if not isinstance(item, dict):
            raise ValueError(f"channels[{i}] must be an object")
        s, p = item.get("substrate"), item.get("product")
        if not isinstance(s, str) or not s or not isinstance(p, str) or not p:
            raise ValueError(f"channels[{i}] requires nonempty substrate and product names")
        if s == p:
            raise ValueError(f"channels[{i}] substrate and product must differ")
        names.extend((s, p))
        km, kcat = q(item.get("Km"), f"channels[{i}].Km"), q(item.get("kcat"), f"channels[{i}].kcat")
        if km <= 0 or kcat <= 0:
            raise ValueError(f"channels[{i}] Km and kcat must be strictly positive")
        item["_Km"] = km
        item["_kcat"] = kcat
    if len(set(names)) != len(names):
        raise ValueError("each substrate/product name must occur in exactly one channel")
    substrates = [item["substrate"] for item in channels]
    products = [item["product"] for item in channels]
    species = substrates + products
    index = {name: i for i, name in enumerate(species)}
    d = len(species)
    q_terms = [{"exp": {}, "coef": "1"}]
    edges = []
    for i, item in enumerate(channels):
        s_i, p_i = index[item["substrate"]], index[item["product"]]
        q_terms.append({"exp": {str(s_i): "1"}, "coef": text(1 / item["_Km"])})
        edges.append({
            "name": f"{item['substrate']}->{item['product']}",
            "nu": {str(s_i): "-1", str(p_i): "1"},
            "source": {str(s_i): "1"},
            "coef": text(enzyme_total * item["_kcat"] / item["_Km"]),
        })
    network = {
        "dimension": d,
        "species_order": species,
        "rate_semantics": "rho_i = kcat_i*enzyme_total*(S_i/Km_i)/(1+sum_j S_j/Km_j)",
        "common_multiplier": {"denominator_factors": [{"terms": q_terms}]},
        "edges": edges,
    }
    init = model.get("initial_state")
    bound = None
    if init is not None:
        if not isinstance(init, dict):
            raise ValueError("initial_state must map every species name to a positive rational")
        vals = {}
        for name in species:
            if name not in init:
                raise ValueError(f"initial_state missing {name}")
            value = q(init[name], f"initial_state.{name}")
            if value <= 0:
                raise ValueError(f"initial_state.{name} must be positive")
            vals[name] = value
        occupancy_at_initial_state = F(1) + sum(
            (vals[item["substrate"]] / item["_Km"] for item in channels), F(0))
        qssa_ratios = [
            {
                "channel": item["substrate"],
                "Eq38_enzyme_scale_ratio": text(
                    enzyme_total / (item["_Km"] * occupancy_at_initial_state)),
            }
            for item in channels
        ]
        max_qssa_ratio = max(
            (F(row["Eq38_enzyme_scale_ratio"]) for row in qssa_ratios), default=F(0))
        qmax = F(1)
        for item in channels:
            total = vals[item["substrate"]] + vals[item["product"]]
            qmax += total / item["_Km"]
        decays = []
        for item in channels:
            rate = enzyme_total * item["_kcat"] / item["_Km"] / qmax
            decays.append({
                "substrate": item["substrate"],
                "initial": text(vals[item["substrate"]]),
                "total_pair": text(vals[item["substrate"]] + vals[item["product"]]),
                "minimum_exponential_decay_rate": text(rate),
                "bound": f"{text(vals[item['substrate']])}*exp(-({text(rate)})*t)",
            })
        bound = {
            "Q_upper_bound": text(qmax),
            "pair_totals_invariant": True,
            "substrate_bounds": decays,
            "QSSA_regime_diagnostic": {
                "ratios": qssa_ratios,
                "maximum_Eq38_enzyme_scale_ratio": text(max_qssa_ratio),
                "interpretation": (
                    "This is a diagnostic of the Eq. 38 enzyme-to-scaled-substrate smallness term at the supplied initial state, not a complete QSSA validity certificate. A value not much smaller than 1 is no evidence for the QSSA regime."
                ),
            },
            "proof": "Q(t)<=Qmax by S_i+P_i conservation and nonnegativity; dS_i/dt=-(kcat_i*E_total/Km_i)S_i/Q(t)<=-lambda_i*S_i, then Gronwall.",
        }
    # Remove parser-only cached Fraction fields so the original object stays JSON-safe.
    for item in channels:
        item.pop("_Km", None)
        item.pop("_kcat", None)
    witness_r = ["0"] * d
    witness_r[0] = "1"
    certificate = {
        "status": "REFUTED",
        "property": "weak essential-source/endotactic condition",
        "direction_r_min_orientation": witness_r,
        "direction_w_max_orientation": [text(-q(x, "witness")) for x in witness_r],
        "active_channels": [edges[0]["name"]],
        "active_projected_jump": "-1",
        "active_source_score": "1",
        "proof": "Choose r with r_S1=1 and all other coordinates 0 (equivalently w=-r). Only the first irreversible substrate-transfer channel is active; it is negative in the minimum-source orientation and is therefore a violating top channel. This is independent of all strictly positive coefficients and of the shared positive denominator.",
    }
    return network, certificate, bound


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path)
    ap.add_argument("--output", type=Path, default=None, help="write compiled network JSON")
    args = ap.parse_args(argv)
    try:
        model = json.loads(args.input.read_text())
        network, certificate, bound = compile_model(model)
    except (OSError, json.JSONDecodeError, TypeError, ValueError, ZeroDivisionError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "reason": str(exc)}, indent=2))
        return 2
    if args.output:
        args.output.write_text(json.dumps(network, indent=2, sort_keys=True) + "\n")
    result = {
        "status": certificate["status"],
        "source_model": str(args.input),
        "channels": len(network["edges"]),
        "dimension": network["dimension"],
        "compiled_network": str(args.output) if args.output else None,
        "certificate": certificate,
        "model_extinction_bound": bound,
        "scope": "exact for the stated positive-rational shared-enzyme QSSA law; biological applicability inherits the source QSSA condition and is not a claim about the unreduced enzyme-complex ODE",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
