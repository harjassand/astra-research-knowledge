#!/usr/bin/env python3
"""Tagwise phase contrasts for two barcoded-HAC lines in GSE287042.

The previous implementation pooled D1/D2 counts before taking H3K9me3:CENP-A
odds. That statistic does not cancel within-domain copy weights. This version
first forms a phase/reference fold for each position code, then contrasts the
mean log fold over D1 and D2. Stable tag-specific copy number and sequencing
bias cancel tagwise; marker/phase-wide scale factors cancel because the D1 and
D2 coefficients sum to zero. The retained tags are single-hit only in the
available *partial* supplementary assembly, so all biological interpretations
remain conditional on phase-invariant structure and stable population mixture.

Run from repository root:
  python3 work/agents/c8_genome_engineering/code/phase_allocation_metric.py
"""
from __future__ import annotations

import csv
import gzip
import glob
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path("work/agents/c8_genome_engineering")
RAW = ROOT / "sources/raw/GSE287042"
MAP = ROOT / "sources/derived/assembled_pc_positions.tsv"
OUT = ROOT / "sources/derived"
LN2 = math.log(2.0)


def read_counts(hac: str, condition: str, marker: str) -> dict[str, int]:
    matches = glob.glob(str(RAW / f"*{hac}_ChIP_{condition}_{marker}.txt.gz"))
    if len(matches) != 1:
        raise ValueError(f"Expected one file for {hac}/{condition}/{marker}, found {matches}")
    counts: dict[str, int] = {}
    with gzip.open(matches[0], "rt") as fh:
        for line in fh:
            fields = line.rstrip("\n").split("\t")
            if fields[0].startswith("T"):
                counts[fields[0]] = int(fields[2])
    return counts


def log2_fold(x: int, ref: int) -> float:
    if x <= 0 or ref <= 0:
        raise ValueError("Selected single-hit tags must have positive counts in all phases")
    return math.log2(x / ref)


def domain_interaction(
    phase_counts: dict[str, int],
    ref_counts: dict[str, int],
    d1: list[str],
    d2: list[str],
) -> tuple[float, float, list[dict[str, float | str]]]:
    """Return D1-D2 mean log2 fold and Poisson read-sampling SE.

    Coefficients are +1/|D1| on D1, -1/|D2| on D2. For independent Poisson
    read counts (or the multinomial delta approximation; coefficients sum to
    zero), Var(log2 fold) is sum_i a_i^2(1/x_i+1/x0_i)/(ln 2)^2. This is only
    technical count uncertainty, not biological-replicate uncertainty.
    """
    coeff = {code: 1.0 / len(d1) for code in d1}
    coeff.update({code: -1.0 / len(d2) for code in d2})
    by_code = []
    estimate = 0.0
    var = 0.0
    for code, a in coeff.items():
        x, x0 = phase_counts.get(code, 0), ref_counts.get(code, 0)
        fold = log2_fold(x, x0)
        estimate += a * fold
        var += a * a * (1.0 / x + 1.0 / x0) / LN2**2
        by_code.append({"code": code, "log2_fold": fold, "coefficient": a})
    return estimate, math.sqrt(var), by_code


def pooled_naive_phi(
    phase: str,
    counts: dict[tuple[str, str], dict[str, int]],
    d1: list[str],
    d2: list[str],
) -> float:
    """Reproduce the old raw-sum statistic, explicitly for audit only."""
    def odds(marker: str, condition: str) -> float:
        c = counts[(marker, condition)]
        return sum(c[x] for x in d1) / sum(c[x] for x in d2)

    h = odds("K9T", phase) / odds("K9T", "THYM")
    ca = odds("CA", phase) / odds("CA", "THYM")
    return h / ca


def log2_phi_for_sets(
    phase: str,
    counts: dict[tuple[str, str], dict[str, int]],
    d1: list[str],
    d2: list[str],
) -> float:
    ca, _, _ = domain_interaction(counts[("CA", phase)], counts[("CA", "THYM")], d1, d2)
    h, _, _ = domain_interaction(counts[("K9T", phase)], counts[("K9T", "THYM")], d1, d2)
    return h - ca


def copy_weight_counterexample(epsilon: float = 0.001) -> dict[str, float]:
    # Two D1 tags have true copy weights (1,10), with per-copy H/C
    # occupancies reversed. D2 is a one-tag reference with all values 1.
    copies = (1.0, 10.0)
    c_occ = (1.0, epsilon)
    h_occ = (epsilon, 1.0)
    raw_h = sum(c * z for c, z in zip(copies, h_occ))
    raw_c = sum(c * z for c, z in zip(copies, c_occ))
    raw_phi = (raw_h / raw_c) / (1.0 / 1.0)
    per_copy_h = sum(z for z in h_occ) / len(h_occ)
    per_copy_c = sum(z for z in c_occ) / len(c_occ)
    corrected_phi = (per_copy_h / per_copy_c) / (1.0 / 1.0)
    return {
        "epsilon": epsilon,
        "raw_sum_phi": raw_phi,
        "per_copy_mean_occupancy_phi": corrected_phi,
    }


def main() -> None:
    pos = list(csv.DictReader(MAP.open(), delimiter="\t"))
    # Source-defined intervals from main Fig. 3B/Fig. 5C and Supplementary
    # Fig. S3/S5. Codes seen more than once in the partial assembly are dropped.
    domain_specs = {
        "HAC120": {
            "a": "D1", "codes_a": list(range(69, 85)),
            "b": "D2", "codes_b": list(range(110, 126)),
            "map_source": "main Fig. 3B and Fig. 5C",
        },
        "HAC465": {
            "a": "D3", "codes_a": [*range(25, 52), 90, 91, 92, 93],
            "b": "D4", "codes_b": [87, 69, 70, 71, 73, 74, 75, 76, 77, 78, 79],
            "map_source": "Supplementary Fig. S3 and S5",
        },
    }
    phases = ("THYM", "COL", "CR3")
    markers = ("CA", "K9T")

    summaries = []
    tag_rows = []
    domain_summary = {}
    for hac, spec in domain_specs.items():
        hits = Counter(row["code"] for row in pos if row["hac"] == hac)
        da = [f"T{i:03d}" for i in spec["codes_a"] if hits[f"T{i:03d}"] == 1]
        db = [f"T{i:03d}" for i in spec["codes_b"] if hits[f"T{i:03d}"] == 1]
        if len(da) < 2 or len(db) < 2:
            raise ValueError(f"Need at least two singleton tags in each domain for {hac}")
        counts = {(m, p): read_counts(hac, p, m) for m in markers for p in phases}
        domain_summary[hac] = {
            f"{spec['a']}_single_hit_assembled_tags": da,
            f"{spec['b']}_single_hit_assembled_tags": db,
            "source_domain_map": spec["map_source"],
        }
        for phase in ("COL", "CR3"):
            effects = {}
            for marker in markers:
                effect, se, details = domain_interaction(
                    counts[(marker, phase)], counts[(marker, "THYM")], da, db
                )
                effects[marker] = (effect, se)
                for item in details:
                    code = str(item["code"])
                    tag_rows.append({
                        "HAC": hac,
                        "condition_vs_THYM": phase,
                        "marker": "CENP-A" if marker == "CA" else "H3K9me3",
                        "code": code,
                        "domain": spec["a"] if code in da else spec["b"],
                        "mapped_reads_phase": counts[(marker, phase)][code],
                        "mapped_reads_THYM": counts[(marker, "THYM")][code],
                        "log2_tagwise_fold": f"{float(item['log2_fold']):.10g}",
                        "domain_contrast_coefficient": f"{float(item['coefficient']):.10g}",
                    })
            # Phi is an interaction of tagwise domain contrasts. It is a
            # compositional shape statistic, not an occupancy ratio or stability.
            log2_phi = effects["K9T"][0] - effects["CA"][0]
            se_log2_phi = math.sqrt(effects["K9T"][1] ** 2 + effects["CA"][1] ** 2)
            lo = 2 ** (log2_phi - 1.96 * se_log2_phi)
            hi = 2 ** (log2_phi + 1.96 * se_log2_phi)
            loo = []
            for domain, tags in ((spec["a"], da), (spec["b"], db)):
                for tag in tags:
                    da_minus, db_minus = da.copy(), db.copy()
                    (da_minus if domain == spec["a"] else db_minus).remove(tag)
                    loo.append({
                        "removed_domain": domain,
                        "removed_code": tag,
                        "log2_Phi": log2_phi_for_sets(phase, counts, da_minus, db_minus),
                    })
            loo_values = [float(x["log2_Phi"]) for x in loo]
            lower95_log2_phi = log2_phi - 1.96 * se_log2_phi
            summaries.append({
                "HAC": hac,
                "domain_a": spec["a"],
                "domain_b": spec["b"],
                "condition_vs_THYM": phase,
                "CENP_A_domain_a_minus_b_log2_fold": effects["CA"][0],
                "CENP_A_read_count_only_SE_log2": effects["CA"][1],
                "H3K9me3_domain_a_minus_b_log2_fold": effects["K9T"][0],
                "H3K9me3_read_count_only_SE_log2": effects["K9T"][1],
                "log2_Phi_tagwise_interaction": log2_phi,
                "Phi_tagwise_interaction": 2**log2_phi,
                "Phi_read_count_only_95pct_interval": [lo, hi],
                "read_count_only_95pct_interval_scope": "Poisson/delta read-sampling only; not biological replicate uncertainty",
                "old_pooled_raw_sum_Phi_invalid_for_copy_cancellation": pooled_naive_phi(phase, counts, da, db),
                "leave_one_tag_out_log2_Phi_range": [min(loo_values), max(loo_values)],
                "leave_one_tag_out": loo,
                "conditional_copy_mismatch_bound": {
                    "assumption": "for every retained tag, |log2(copy_ratio_H3K9me3/copy_ratio_CENP-A)| <= epsilon between phase aliquot and THYM aliquot",
                    "bias_bound_abs_log2_Phi": "2*epsilon",
                    "epsilon_max_for_positive_point_estimate_log2": log2_phi / 2,
                    "epsilon_max_for_positive_read_count_only_95pct_lower_limit_log2": lower95_log2_phi / 2,
                    "max_per_tag_marker_mismatch_fold_point": 2 ** (log2_phi / 2),
                    "max_per_tag_marker_mismatch_fold_read_count_only_95pct": 2 ** (lower95_log2_phi / 2),
                    "status": "sensitivity threshold only; no source assay bounds epsilon",
                },
            })

    # An audit witness requested by the reviewer: unequal copy weights alone
    # can create an apparent tenfold pooled contrast although mean per-copy
    # H/C occupancy is exactly 1.
    counter = copy_weight_counterexample()
    assert abs(counter["per_copy_mean_occupancy_phi"] - 1.0) < 1e-12
    assert counter["raw_sum_phi"] > 9.0

    summary = {
        "source": {
            "paper": "Ohzeki et al., Nucleic Acids Research 54(12), gkag597 (2026)",
            "doi": "10.1093/nar/gkag597",
            "data": "GEO GSE287040/GSE287042; HAC120 and HAC465 PC ChIP idxstats tables",
        },
        "domains": domain_summary,
        "tagwise_phase_contrasts": summaries,
        "counterexample_to_pooled_copy_cancellation": counter,
        "interpretation": {
            "valid_invariant": "For each tag i, log(Y_m,p,i/Y_m,0,i) cancels stable b_mi and stable copy c_i. The D1-minus-D2 mean cancels each marker/phase-wide multiplicative factor because coefficients sum to zero. A H3K9me3-minus-CENP-A interaction then cancels common tagwise copy changes if both marker aliquots represent the same phase/reference copy mixture.",
            "unestablished_assumptions": [
                "Position-code copy number and physical structure are invariant across the compared phase aliquots, or copy shifts are the same for both marker aliquots.",
                "Each tag mapped once in partial supplementary contigs is truly single-copy in the complete HAC; omitted or unresolved repeat copies do not contribute.",
                "Condition aliquots contain comparable HAC-bearing clone mixtures; phase-specific selection or cell-mixture shifts do not alter per-tag copy-weighted state.",
                "Per-tag library/antibody/fragment-recovery bias is stable across compared phases within marker; marker-specific global recovery may vary but cancels in D1-D2.",
            ],
            "not_identified": [
                "absolute per-cell CENP-A or H3K9me3 occupancy (GEO PC tables omit qPCR recovery multiplier)",
                "same-cell joint CENP-A/H3K9 state, local replication time, causal invasion/reload rates, lineages, functional kinetochore multiplicity, structural loss, or long-term retention hazard",
            ],
        },
    }
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "tagwise_phase_effects.tsv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(tag_rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(tag_rows)
    (OUT / "spatial_phase_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    # Keep a plain TSV of inferentially useful summaries; columns explicitly
    # separate read-count uncertainty from biological uncertainty.
    with (OUT / "spatial_phase_contrasts.tsv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summaries[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(summaries)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
