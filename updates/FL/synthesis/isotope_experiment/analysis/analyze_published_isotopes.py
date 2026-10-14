#!/usr/bin/env python3
"""Reproduce bounded arithmetic from Liu et al. (2023) supporting information.

The reported C3+ entries are fitted fragment-mixture estimates, not raw
whole-molecule C4 isotope counts. This script preserves that boundary.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "reported_isotope_analysis.json"

TABLE_S1 = {
    "1.25_min": {
        "p": [0.33, 0.41, 0.23, 0.03],
        "half_width": [0.06, 0.07, 0.06, 0.06],
        "interval_s": 75,
    },
    "3.75_min": {
        "p": [0.81, 0.17, 0.02, 0.0],
        "half_width": [0.06, 0.06, 0.05, 0.0],
        "interval_s": 225,
    },
}


def component_box_vertices(ranges: list[tuple[float, float]]) -> list[tuple[float, ...]]:
    """Vertices of a box intersected with sum(p)=1, by choosing one dependent p."""
    vertices: set[tuple[float, ...]] = set()
    n = len(ranges)
    for dependent in range(n):
        independent = [i for i in range(n) if i != dependent]
        for endpoints in itertools.product((0, 1), repeat=n - 1):
            p: list[float | None] = [None] * n
            for index, endpoint in zip(independent, endpoints):
                p[index] = ranges[index][endpoint]
            p[dependent] = 1.0 - sum(float(p[i]) for i in independent)
            low, high = ranges[dependent]
            if low - 1e-12 <= float(p[dependent]) <= high + 1e-12:
                vertices.add(tuple(float(x) for x in p))
    return sorted(vertices)


rows: dict[str, dict[str, object]] = {}
for interval, record in TABLE_S1.items():
    p = record["p"]
    half = record["half_width"]
    assert abs(sum(p) - 1.0) < 1e-12
    heavy_fraction = (p[1] + 2 * p[2] + 3 * p[3]) / 3
    parity = p[0] - p[1] + p[2] - p[3]
    binomial_parity = (1 - 2 * heavy_fraction) ** 3
    ranges = [
        (max(0.0, pi - hi), min(1.0, pi + hi))
        for pi, hi in zip(p, half)
    ]
    vertices = component_box_vertices(ranges)
    q_values = [v[0] - v[1] + v[2] - v[3] for v in vertices]
    x_values = [(v[1] + 2 * v[2] + 3 * v[3]) / 3 for v in vertices]
    rows[interval] = {
        "reported_p0_to_p3": p,
        "reported_component_95pct_half_widths": half,
        "heavy_atom_fraction_point": heavy_fraction,
        "parity_point": parity,
        "independent_binomial_parity_at_same_heavy_fraction": binomial_parity,
        "point_residual_from_independent_binomial": parity - binomial_parity,
        "component_interval_box_envelope_not_joint_ci": {
            "parity": [min(q_values), max(q_values)],
            "heavy_atom_fraction": [min(x_values), max(x_values)],
        },
        "component_interval_box_ranges": ranges,
        "interval_seconds": record["interval_s"],
        "warning": (
            "C3+ fitted fragment mixture; componentwise 95% intervals have no published "
            "covariance and do not define a joint confidence interval."
        ),
    }

# Table S2's integrated carbon flow for butylenes and butanes; dividing by four
# converts C-moles into molecule-moles for each pooled C4 product class, not into
# detector counts.
avogadro = 6.02214076e23
c4_carbon_umol = {
    "butylenes": {"3.75_min": 0.529, "1.25_min": 0.479},
    "butanes": {"3.75_min": 1.733, "1.25_min": 1.805},
}
c4_output = {}
for product_class, intervals in c4_carbon_umol.items():
    for interval, carbon_umol in intervals.items():
        molecule_umol = carbon_umol / 4
        c4_output[f"{product_class}_{interval}"] = {
            "product_class": product_class,
            "integrated_product_carbon_umol": carbon_umol,
            "C4_molecule_equivalent_umol": molecule_umol,
            "C4_molecule_equivalent_count": molecule_umol * 1e-6 * avogadro,
            "warning": "Carbon-balance output equivalent only; not ion counts or detected molecules.",
        }

# Conditional planning calculation using the source report's synthetic E/O
# contrast at r*tau=2. It is not transferred to H-ZSM-5.
synthetic_delta = (1 - math.exp(-4)) ** 4 / 8
nominal_a = 0.98
z_values = {"95pct_two_sided_normal": 1.96, "99pct_two_sided_normal": 2.576}
ideal_sample_counts = {
    label: math.ceil(2 * z * z / (nominal_a**8 * synthetic_delta**2))
    for label, z in z_values.items()
}

result = {
    "source": {
        "article_doi": "10.1021/acscatal.3c00168",
        "si_doi": "10.1021/acscatal.3c00168.s001",
        "si_table_s1": "fitted average C3 isotope composition, p0..p3, first response peak",
        "si_table_s2": "integrated carbon flow (mu0) of pooled butanes",
    },
    "table_s1_analysis": rows,
    "table_s2_C4_product_output": c4_output,
    "startup_observation_reported_in_article": {
        "pre_switch_13C_pulses": 5,
        "carbon_per_pulse_umol": 7.6,
        "pre_switch_13C_carbon_umol": 38.0,
        "first_12C_pulse_fully_13C_aromatic_carbon_fraction_reported": 0.15,
        "first_12C_pulse_fully_12C_aromatic_carbon_fraction_reported": 0.48,
        "first_12C_pulse_total_13C_aromatic_carbon_fraction_reported": 0.29,
        "warning": "Reported aromatic response, not C4 output or total catalyst inventory.",
    },
    "illustrative_ideal_count_budget": {
        "synthetic_E_O_delta_Q_at_r_tau_2": synthetic_delta,
        "nominal_label_contrast_a": nominal_a,
        "independent_effective_product_observations_per_mechanism": ideal_sample_counts,
        "assumptions": [
            "Two independent hypotheses with equal effective product sample sizes.",
            "Product parity is a bounded +/-1 observation with worst-case variance 1.",
            "Known constant isotope contrast a=0.98 and independent products.",
            "Synthetic E/O construction only; no H-ZSM-5 effect size is inferred.",
        ],
        "excluded": [
            "Detector sensitivity, sampling fraction, covariance, catalyst variability, startup bias, and code-waveform error.",
            "The output count is not a laboratory acquisition plan or instrument guarantee.",
        ],
    },
}

OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
