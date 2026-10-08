#!/usr/bin/env python3
"""Reproduce the JUN/FOS-subfamily double-mutant nomination from GEO GSE245326.

This is a processed-score analysis only. It intentionally does not refit the
input/output count likelihood or impute pairs rejected by the source QC rule.
"""

from __future__ import annotations

import csv
import gzip
import math
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "GSE245326_Supplementary_Data_3.txt.gz"
TARGETS = {"FOS", "FOSB", "FOSL1", "FOSL2"}
VARIANTS = ("1eA", "4aR")


def load_rows():
    with gzip.open(DATA, "rt", newline="") as handle:
        yield from csv.DictReader(handle, delimiter="\t")


def as_float(row, key):
    value = row[key]
    if value in ("", "NA", "NaN"):
        raise ValueError(f"missing {key}")
    return float(value)


def stable_fraction_bound(z):
    z = max(-700.0, min(700.0, z))
    return 1.0 / (1.0 + math.exp(z))


def fit_source_link(rows):
    """Fit shared ref_dG, scale and offset to source-published MoCHI means.

    The official analysis code uses A/(1+exp(mult*(ref_dG+ddG_mut+ddG_bZ)))+B.
    Per-partner `dG_mult` and exported energy terms are taken from Data 3.
    Refitting only the three shared mapping parameters gives a reproducible
    approximation to the source model's exported `mean` column.
    """

    def evaluate(ref):
        xs = [
            stable_fraction_bound(
                row["dG_mult"] * (ref + row["ddG_mut"] + row["ddG_bZ"])
            )
            for row in rows
        ]
        ys = [row["mean"] for row in rows]
        mx = sum(xs) / len(xs)
        my = sum(ys) / len(ys)
        variance = sum((x - mx) ** 2 for x in xs)
        scale = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / variance
        offset = my - scale * mx
        sse = sum(
            (y - (scale * x + offset)) ** 2 for x, y in zip(xs, ys)
        )
        return sse, scale, offset

    coarse = [(-10.0 + i * 0.2, evaluate(-10.0 + i * 0.2)[0]) for i in range(101)]
    center = min(coarse, key=lambda item: item[1])[0]
    left, right = center - 0.2, center + 0.2
    phi = (math.sqrt(5.0) - 1.0) / 2.0
    x1 = right - phi * (right - left)
    x2 = left + phi * (right - left)
    f1, f2 = evaluate(x1)[0], evaluate(x2)[0]
    for _ in range(80):
        if f1 < f2:
            right, x2, f2 = x2, x1, f1
            x1 = right - phi * (right - left)
            f1 = evaluate(x1)[0]
        else:
            left, x1, f1 = x1, x2, f2
            x2 = left + phi * (right - left)
            f2 = evaluate(x2)[0]
    ref = (left + right) / 2.0
    sse, scale, offset = evaluate(ref)
    return ref, scale, offset, math.sqrt(sse / len(rows))


def score_metrics(profile, targets=TARGETS):
    target_scores = [profile[name] for name in sorted(targets)]
    off_target, off_name = max(
        (score, name) for name, score in profile.items() if name not in targets
    )
    mean_target = sum(target_scores) / len(target_scores)
    return {
        "target_mean": mean_target,
        "target_min": min(target_scores),
        "max_off_target": off_target,
        "max_off_name": off_name,
        "margin": mean_target - off_target,
    }


def main():
    numeric_keys = (
        "fitness",
        "sigma",
        "wt_fitness_sigma",
        "mean",
        "ddG_mut",
        "ddG_bZ",
        "dG_mult",
    )
    all_count = 0
    flag_count = Counter()
    usable = []
    hamming_by_id = {}
    wt_sequence = None
    partner_set_all = set()

    for row in load_rows():
        all_count += 1
        flag_count[row["filt"]] += 1
        partner_set_all.add(row["bZ"])
        if row["id"] == "0xx" and row["bZ"] == "FOS":
            # Data 3's `aa_seq` appends a 51-position one-hot partner code after
            # the 65-residue JUN sequence; compare only the JUN sequence.
            wt_sequence = row["aa_seq"][:65]
        if row["filt"] != "FALSE":
            continue
        item = {key: as_float(row, key) for key in numeric_keys}
        item.update(
            id=row["id"],
            bZ=row["bZ"],
            aa_seq=row["aa_seq"],
        )
        usable.append(item)

    if wt_sequence is None:
        raise RuntimeError("WT JUN × FOS row was not found")

    by_variant = {}
    for row in usable:
        by_variant.setdefault(row["id"], {})[row["bZ"]] = row
        hamming_by_id[row["id"]] = sum(
            ref != alt for ref, alt in zip(wt_sequence, row["aa_seq"][:65])
        )

    if len(partner_set_all) != 52:
        raise AssertionError(f"expected 52 partner names, found {len(partner_set_all)}")
    if max(hamming_by_id.values()) != 1:
        raise AssertionError("the accepted JUN sequences include a multi-mutant")

    partners = sorted(by_variant["0xx"])
    for variant in ("0xx", *VARIANTS):
        if set(by_variant[variant]) != set(partners):
            raise AssertionError(f"{variant} does not have a complete partner profile")

    ref, scale, offset, fit_rmse = fit_source_link(usable)

    def global_prediction(row, ddg_mut):
        fraction = stable_fraction_bound(
            row["dG_mult"] * (ref + ddg_mut + row["ddG_bZ"])
        )
        return scale * fraction + offset

    def observed_single(variant):
        return {
            partner: by_variant[variant][partner]["fitness"]
            - by_variant["0xx"][partner]["fitness"]
            for partner in partners
        }

    def predicted_double(variants):
        total_ddg = sum(by_variant[v]["FOS"]["ddG_mut"] for v in variants)
        profile = {}
        for partner in partners:
            wt_row = by_variant["0xx"][partner]
            value = global_prediction(wt_row, total_ddg) - global_prediction(
                wt_row, 0.0
            )
            for variant in variants:
                row = by_variant[variant][partner]
                value += row["fitness"] - global_prediction(row, row["ddG_mut"])
            wt_residual = wt_row["fitness"] - global_prediction(wt_row, 0.0)
            # Residuals are assumed additive as deviations from WT.  Subtract
            # the WT residual once per mutation so the formula recovers the
            # observed single-mutant relative profile when the other allele is WT.
            value -= 2.0 * wt_residual
            profile[partner] = value
        return profile

    def global_only_double(variants):
        total_ddg = sum(by_variant[v]["FOS"]["ddG_mut"] for v in variants)
        profile = {}
        for partner in partners:
            wt_row = by_variant["0xx"][partner]
            profile[partner] = global_prediction(wt_row, total_ddg) - global_prediction(
                wt_row, 0.0
            )
        return profile

    def raw_score_addition(variants):
        profile = {partner: 0.0 for partner in partners}
        for variant in variants:
            single = observed_single(variant)
            profile = {
                partner: profile[partner] + single[partner] for partner in partners
            }
        return profile

    print(f"source_file_bytes={DATA.stat().st_size}")
    print(f"rows_all={all_count}; filt_FALSE={flag_count['FALSE']}; filt_TRUE={flag_count['TRUE']}")
    print(
        f"valid_unique_variants={len(by_variant)}; valid_partner_names={len(partners)}; "
        f"max_JUN_Hamming_from_WT={max(hamming_by_id.values())}"
    )
    print(
        f"MoCHI-link fit to exported means: n={len(usable)}, ref_dG={ref:.6f}, "
        f"scale={scale:.6f}, offset={offset:.6f}, RMSE={fit_rmse:.6f}"
    )
    print("\nprofile summaries; scores are relative assay enrichment units")
    profiles = {
        "observed 1eA": observed_single("1eA"),
        "observed 4aR": observed_single("4aR"),
        "double, raw score-additive sensitivity": raw_score_addition(VARIANTS),
        "double, nonlinear global-energy only": global_only_double(VARIANTS),
        "double, nonlinear MoCHI + additive single residuals": predicted_double(VARIANTS),
    }
    for label, profile in profiles.items():
        metrics = score_metrics(profile)
        print(
            f"{label}: FOS-family mean={metrics['target_mean']:.3f}; "
            f"family min={metrics['target_min']:.3f}; "
            f"max off-target={metrics['max_off_target']:.3f} "
            f"({metrics['max_off_name']}); margin={metrics['margin']:.3f}"
        )
    print("\nnonlinear-plus-residual predicted family profile")
    pair = profiles["double, nonlinear MoCHI + additive single residuals"]
    for partner in sorted(TARGETS):
        print(f"{partner}\t{pair[partner]:.6f}")
    print("\ntop predicted non-FOS partners")
    for score, partner in sorted(
        (score, partner)
        for partner, score in pair.items()
        if partner not in TARGETS
    )[::-1][:8]:
        print(f"{partner}\t{score:.6f}")

    print("\nsource single-score uncertainty (quadrature of mutant and WT sigma)")
    for variant, off_target in (("1eA", "ATF4"), ("4aR", "XBP1")):
        for partner in (*sorted(TARGETS), off_target):
            row = by_variant[variant][partner]
            wt = by_variant["0xx"][partner]
            relative = row["fitness"] - wt["fitness"]
            combined_sigma = math.hypot(row["sigma"], wt["sigma"])
            print(f"{variant}\t{partner}\trel={relative:.6f}\tsigma={combined_sigma:.6f}")

    # Exploratory, first-order candidate scan over single mutants with a
    # complete 52-partner profile. These thresholds are screening choices, not
    # biological standards; the double-mutant profile remains unmeasured.
    complete_singles = sorted(
        variant
        for variant, profile in by_variant.items()
        if variant != "0xx"
        and len(profile) == len(partners)
        and re.fullmatch(r"[1-5][a-g][A-Z]", variant)
    )
    eligible_pairs = []
    for index, first in enumerate(complete_singles):
        for second in complete_singles[index + 1 :]:
            if first[:2] == second[:2]:
                continue
            candidate_profile = predicted_double((first, second))
            metrics = score_metrics(candidate_profile)
            if metrics["target_mean"] >= 0.30 and metrics["target_min"] >= 0.15:
                eligible_pairs.append((metrics["margin"], first, second, metrics))
    eligible_pairs.sort(key=lambda item: item[0], reverse=True)
    print(
        f"\nexploratory_pair_scan: complete_single_profiles={len(complete_singles)}; "
        f"eligible_pairs={len(eligible_pairs)}; ranking=family_mean_minus_max_offtarget"
    )
    for margin, first, second, metrics in eligible_pairs[:5]:
        strict_gap = metrics["target_min"] - metrics["max_off_target"]
        print(
            f"{first}+{second}\tmean={metrics['target_mean']:.6f}\t"
            f"min={metrics['target_min']:.6f}\tmax_off="
            f"{metrics['max_off_target']:.6f}:{metrics['max_off_name']}\t"
            f"mean_margin={margin:.6f}\tmin_minus_maxoff={strict_gap:.6f}"
        )


if __name__ == "__main__":
    main()
