"""Exact accounting and diagnostic calculations for the conventional comparator.

These are not wet-lab results and not a kinetic model of whole ribosome assembly.
Only the RsmB affinity numbers are data-derived; illustrative identifiability
examples are explicitly labeled. Python standard library only.
"""

import json
import math
from pathlib import Path


def static_binding_tradeoff(k_substrate, k_product):
    """Best equal capture/mature-occupancy error at one free enzyme level.

    p_s=c/(K_s+c), p_p=c/(K_p+c). Equating 1-p_s=p_p gives
    c=sqrt(K_s*K_p). This applies to two equilibrated binding states ONLY.
    The measured substrate state is a C375A mimic; do not apply the theorem to
    the catalytic WT reaction or claim it limits driven release.
    """
    c = math.sqrt(k_substrate * k_product)
    capture = c / (k_substrate + c)
    product = c / (k_product + c)
    return {
        "best_free_enzyme_nM": c,
        "capture_fraction": capture,
        "product_occupancy_fraction": product,
        "affinity_ratio": k_product / k_substrate,
        "ratio_needed_for_90pct_capture_10pct_product_occupancy": 81.0,
        "supports_90_10_static_window": k_product / k_substrate >= 81,
    }


def exact_native_scaffold_conservation():
    """Integer stoichiometric proof on the earned native-RNA assembly network.

    Species: native23S, immatureRNP, active50S, 70S, degraded_native23S.
    All states retain exactly one native23S token. Degradation is included as
    a counted sink, preventing disappearance from being mistaken for synthesis.
    IVT23S->active50S is absent because the all-recombinant complete service has
    not been earned for it in the retrieved primary constructions.
    """
    species = ["native23S", "immatureRNP", "active50S", "70S", "degraded_native23S"]
    reactions = {
        "early_assembly": [-1, 1, 0, 0, 0],
        "maturation": [0, -1, 1, 0, 0],
        "join_30S": [0, 0, -1, 1, 0],
        "split_70S": [0, 0, 1, -1, 0],
        "disassemble": [1, 0, -1, 0, 0],
        "damage": [0, 0, -1, 0, 1],
        "repair_proteins": [0, 0, 0, 0, 0],
    }
    left_null_residual = {k: sum(v) for k, v in reactions.items()}
    assert all(v == 0 for v in left_null_residual.values())
    return {
        "species": species,
        "reactions": reactions,
        "left_null_vector": [1] * len(species),
        "left_null_residual": left_null_residual,
        "bound": "active50S + 70S <= initial native23S tokens + imported native23S tokens",
        "scope": "earned native-RNA construction, not a physical impossibility theorem for synthetic rRNA",
    }


def activity_nonidentifiability():
    """Two physically distinct populations produce the same scalar activity.

    Output per input RNA = active fraction * turnover * reporter success.
    End-point fluorescence alone cannot separate the three factors.
    The examples below are mathematical witnesses, not estimates for Aoyama.
    """
    rows = [
        {"active_fraction": 0.2, "turnover": 1.0, "reporter_success": 1.0},
        {"active_fraction": 1.0, "turnover": 0.2, "reporter_success": 1.0},
        {"active_fraction": 1.0, "turnover": 1.0, "reporter_success": 0.2},
    ]
    for row in rows:
        row["normalized_output"] = math.prod(row.values())
    assert all(abs(row["normalized_output"] - 0.2) < 1e-12 for row in rows)
    return rows


def main():
    measured = static_binding_tradeoff(15.4, 249.0)
    edge_low = static_binding_tradeoff(17.0, 232.7)
    edge_high = static_binding_tradeoff(13.8, 265.3)
    data = {
        "nature_of_result": "accounting, exact algebra, and reported-data calculation; no laboratory execution",
        "aoyama_input_accounting": {
            "native_23S_pmol": 240,
            "native_5S_pmol": 240,
            "each_32_single_copy_LSU_protein_pmol_nominal": 270,
            "bL12_pmol_nominal": 1080,
            "protein_equivalents_per_rRNA": 270 / 240,
            "native23S_upper_bound_on_new_LSU_pmol": 240,
            "assembly_incubation_minutes_excluding_preparation_and_exchange": 20 + 90,
            "reference": "Aoyama et al., 10.1093/jb/mvab121",
            "note": "protein concentrations inferred from paper's stated mixture equivalents; actual recovery and active yield not supplied here",
        },
        "rsmb_reported_binding_state_tradeoff": measured,
        "rsmb_reported_error_bar_corner_range_not_CI": {
            "best_static_capture_low": edge_low["capture_fraction"],
            "best_static_capture_high": edge_high["capture_fraction"],
        },
        "rsmb_scope": {
            "reference": "Wei and Woodson, 10.1126/sciadv.aef7741",
            "substrate_mimic": "RsmB C375A + unmethylated 16S 3-prime domain + SAM",
            "product_state": "RsmB C375A + methylated 16S 3-prime domain + SAM",
            "buffer": "200 mM KCl, 10 mM MgCl2",
            "warning": "This does not estimate a WT catalytic release rate or disprove a driven protocol.",
        },
        "native_scaffold_conservation": exact_native_scaffold_conservation(),
        "fluorescence_activity_nonidentifiability_illustration": activity_nonidentifiability(),
        "performance_claims_not_available": [
            "active-particle yield of all-recombinant 70S",
            "codon-resolved error spectrum of all-recombinant 70S",
            "usable lifetime after removal of assembly chemicals",
            "purified 33P + entirely synthetic 23S full-translation service",
        ],
    }
    out = Path(__file__).parent / "comparison_results.json"
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
