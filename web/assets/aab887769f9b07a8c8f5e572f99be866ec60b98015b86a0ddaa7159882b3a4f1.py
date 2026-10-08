#!/usr/bin/env python3
"""Count-level reanalysis of JUN x bZIP DMS with zero outputs retained.

For each JUN variant / wild-type bZIP pair, condition on the two output counts
(variant, WT JUN) within each biological replicate. Under a common sequencing
and selection-depth nuisance factor, this is a binomial model whose log-odds
offset is the ratio of matched input counts. The fitted parameter is the
variant's log relative enrichment versus WT JUN for the same partner. Zero
outputs are retained as valid likelihood observations; replicate input zero
is omitted because that replicate gives no input-offset information.

This is a diagnostic count model, not the published MoCHI fit and not a
biophysical binding-energy model. Its profile intervals condition on observed
input counts and do not model between-replicate overdispersion.
"""
from __future__ import annotations

import csv
import gzip
import json
import math
import os
from collections import defaultdict


ROOT = os.path.dirname(__file__)
DATA = os.path.join(
    ROOT,
    "../children/released_data/data/GSE245326_Supplementary_Data_3.txt.gz",
)
DATA = os.path.abspath(DATA)
OUT = ROOT
CHI2_95_HALF = 1.920729410347062
TARGET = {"FOS", "FOSB", "FOSL1", "FOSL2"}


def read_table(path: str):
    rows = {}
    with gzip.open(path, "rt") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            row["filt"] = row["filt"] == "TRUE"
            rows[(row["id"], row["bZ"])] = row
    return rows


def logistic(logit: float) -> float:
    if logit >= 0:
        return 1.0 / (1.0 + math.exp(-logit))
    e = math.exp(logit)
    return e / (1.0 + e)


def log_likelihood(delta: float, obs) -> float:
    ans = 0.0
    for i, iw, o, ow in obs:
        p = logistic(delta + math.log(i) - math.log(iw))
        total = o + ow
        if o:
            ans += o * math.log(p)
        if ow:
            ans += ow * math.log1p(-p)
    return ans


def score(delta: float, obs):
    grad = hess = 0.0
    for i, iw, o, ow in obs:
        p = logistic(delta + math.log(i) - math.log(iw))
        total = o + ow
        grad += o - total * p
        hess -= total * p * (1.0 - p)
    return grad, hess


def make_observations(row, wt, min_input=1):
    obs = []
    for r in range(1, 7):
        i = int(row[f"count_e{r}_s0"])
        iw = int(wt[f"count_e{r}_s0"])
        o = int(row[f"count_e{r}_s1"])
        ow = int(wt[f"count_e{r}_s1"])
        if i >= min_input and iw > 0 and (o + ow) > 0:
            obs.append((i, iw, o, ow))
    return obs


def fit_profile(row, wt, min_input=1, lr_half=CHI2_95_HALF):
    """MLE and 95% profile-likelihood interval for one variant/partner.

    Infinite MLEs are retained as one-sided confidence bounds. A row with no
    informative biological replicate returns None.
    """
    obs = make_observations(row, wt, min_input=min_input)
    if not obs:
        return None
    lo, hi = -40.0, 40.0
    glo, _ = score(lo, obs)
    ghi, _ = score(hi, obs)
    if glo <= 0:
        # Every informative output count favors the WT comparator.
        d_hat = -math.inf
        ll_max = log_likelihood(lo, obs)
    elif ghi >= 0:
        d_hat = math.inf
        ll_max = log_likelihood(hi, obs)
    else:
        d_hat = 0.0
        for _ in range(150):
            g, h = score(d_hat, obs)
            if abs(g) < 1e-10:
                break
            candidate = d_hat - g / h if h else (lo + hi) / 2
            if not lo < candidate < hi:
                candidate = (lo + hi) / 2
            if g > 0:
                lo = d_hat
            else:
                hi = d_hat
            d_hat = candidate
        ll_max = log_likelihood(d_hat, obs)

    threshold = ll_max - lr_half

    def bisect_crossing(a, b):
        # Return the profile-likelihood boundary between one inside and one
        # outside endpoint, regardless of which side contains the MLE.
        inside_a = log_likelihood(a, obs) >= threshold
        for _ in range(100):
            mid = (a + b) / 2
            inside = log_likelihood(mid, obs) >= threshold
            if inside == inside_a:
                a = mid
            else:
                b = mid
        return (a + b) / 2

    if d_hat == -math.inf:
        lower = -math.inf
        upper = bisect_crossing(-40.0, 40.0)
    elif d_hat == math.inf:
        lower = bisect_crossing(-40.0, 40.0)
        upper = math.inf
    else:
        step = 1.0
        a = d_hat - step
        while log_likelihood(a, obs) >= threshold and a > -100:
            step *= 2
            a = d_hat - step
        lower = bisect_crossing(a, d_hat)
        step = 1.0
        b = d_hat + step
        while log_likelihood(b, obs) >= threshold and b < 100:
            step *= 2
            b = d_hat + step
        upper = bisect_crossing(d_hat, b)
    return {"estimate": d_hat, "lower95": lower, "upper95": upper,
            "n_reps": len(obs), "loglik": ll_max}


def pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    xx = sum((x - mx) ** 2 for x in xs)
    yy = sum((y - my) ** 2 for y in ys)
    xy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return xy / math.sqrt(xx * yy)


def normal_cdf(z):
    return 0.5 * math.erfc(-z / math.sqrt(2.0))


def normal_quantile(p):
    lo, hi = -10.0, 10.0
    for _ in range(100):
        mid = (lo + hi) / 2.0
        if normal_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def json_number(x):
    return x if math.isfinite(x) else str(x)


def main():
    rows = read_table(DATA)
    wt = {partner: row for (variant, partner), row in rows.items()
          if variant == "0xx"}
    estimates = {}
    accepted_pairs = []
    count_stats = {"all_rows": len(rows), "source_qc_pass": 0,
                   "source_qc_fail": 0, "zero_output_rows": 0,
                   "input_low_rows": 0, "retained_zero_output_rows": 0,
                   "estimable_with_any_positive_input": 0,
                   "estimable_with_4plus_replicates": 0}
    for (variant, partner), row in rows.items():
        if variant == "0xx":
            continue
        count_stats["source_qc_fail" if row["filt"] else "source_qc_pass"] += 1
        counts_i = [int(row[f"count_e{r}_s0"]) for r in range(1, 7)]
        counts_o = [int(row[f"count_e{r}_s1"]) for r in range(1, 7)]
        zero_o = any(x == 0 for x in counts_o)
        low_i = any(x <= 10 for x in counts_i)
        count_stats["zero_output_rows"] += int(zero_o)
        count_stats["input_low_rows"] += int(low_i)
        count_stats["retained_zero_output_rows"] += int(zero_o and not row["filt"])
        est = fit_profile(row, wt[partner], min_input=1)
        if est:
            count_stats["estimable_with_any_positive_input"] += 1
            count_stats["estimable_with_4plus_replicates"] += int(est["n_reps"] >= 4)
            estimates[(variant, partner)] = est
            if not row["filt"] and math.isfinite(est["estimate"]):
                published = row["rel"]
                if published not in ("", "NA"):
                    accepted_pairs.append((est["estimate"], float(published)))

    xs = [x for x, y in accepted_pairs]
    ys = [y for x, y in accepted_pairs]
    slope = sum(x * y for x, y in accepted_pairs) / sum(x * x for x, y in accepted_pairs)
    fitted = [slope * x for x in xs]
    rmse = math.sqrt(sum((p - y) ** 2 for p, y in zip(fitted, ys)) / len(ys))
    calibration = {"n_accepted_finite_pairs": len(xs),
                   "pearson_count_logodds_vs_published_rel": pearson(xs, ys),
                   "zero_intercept_scale_published_score_per_logodds": slope,
                   "rmse_after_scale": rmse}

    partners = sorted(wt)
    variants = sorted({v for v, p in rows if v != "0xx"})
    ranking = []
    for variant in variants:
        all_est = [estimates.get((variant, p)) for p in partners]
        if sum(e is not None and e["n_reps"] >= 4 and math.isfinite(e["estimate"])
               for e in all_est) < 48:
            continue
        by_partner = {p: estimates.get((variant, p)) for p in partners}
        target = [by_partner[p]["estimate"] for p in sorted(TARGET)
                  if p in by_partner and by_partner[p] and math.isfinite(by_partner[p]["estimate"])]
        off = [by_partner[p]["estimate"] for p in partners if p not in TARGET
               and by_partner[p] and math.isfinite(by_partner[p]["estimate"])]
        if len(target) != len(TARGET) or len(off) < 40:
            continue
        mean_t = sum(target) / len(target)
        max_off = max(off)
        ranking.append({"variant": variant, "target_mean_logodds": mean_t,
                        "target_min_logodds": min(target),
                        "max_offtarget_logodds": max_off,
                        "mean_minus_maxoff_logodds": mean_t - max_off,
                        "source_qc_filtered_target_pairs": sum(rows[(variant,p)]["filt"] for p in TARGET if (variant,p) in rows),
                        "source_qc_filtered_offtarget_pairs": sum(rows[(variant,p)]["filt"] for p in partners if p not in TARGET and (variant,p) in rows)})
    ranking.sort(key=lambda x: x["mean_minus_maxoff_logodds"], reverse=True)

    # Conservative simultaneous profile-likelihood screening: one two-sided
    # interval per partner with Bonferroni alpha=0.05/52. This is still
    # conditional on inputs and does not correct for biological overdispersion.
    simultaneous_z = normal_quantile(1.0 - 0.05 / (2.0 * len(partners)))
    simultaneous_lr_half = simultaneous_z * simultaneous_z / 2.0
    robust_ranking = []
    source_qc_complete_ranking = []
    for variant in variants:
        per_partner = {}
        all_source_pass = True
        all_profiles = True
        for p in partners:
            row = rows.get((variant, p))
            if row is None:
                all_source_pass = False
                all_profiles = False
                continue
            all_source_pass = all_source_pass and not row["filt"]
            est = fit_profile(row, wt[p], min_input=1, lr_half=simultaneous_lr_half)
            per_partner[p] = est
            if est is None or est["n_reps"] < 4:
                all_profiles = False
        if all_source_pass:
            measured = {p: rows[(variant, p)]["rel"] for p in partners}
            if all(v not in ("", "NA") for v in measured.values()):
                target_s = [float(measured[p]) for p in TARGET]
                off_s = [float(measured[p]) for p in partners if p not in TARGET]
                source_qc_complete_ranking.append({"variant": variant,
                    "target_mean_score": sum(target_s)/len(target_s),
                    "target_min_score": min(target_s),
                    "max_offtarget_score": max(off_s),
                    "target_mean_minus_maxoff_score": sum(target_s)/len(target_s)-max(off_s)})
        if not all_profiles:
            continue
        if any(per_partner[p]["lower95"] == -math.inf for p in TARGET):
            target_lower = -math.inf
        else:
            target_lower = sum(per_partner[p]["lower95"] for p in TARGET)/len(TARGET)
        off_upper = max(per_partner[p]["upper95"] for p in partners if p not in TARGET)
        point_target = sum(per_partner[p]["estimate"] for p in TARGET)/len(TARGET)
        point_off = max(per_partner[p]["estimate"] for p in partners if p not in TARGET)
        robust_ranking.append({"variant": variant,
            "count_target_mean_score": json_number(point_target * slope),
            "count_target_min_score": json_number(min(per_partner[p]["estimate"] for p in TARGET) * slope),
            "count_max_offtarget_score": json_number(point_off * slope),
            "count_target_mean_minus_maxoff_score": json_number((point_target-point_off)*slope),
            "simultaneous_target_mean_lower95_score": target_lower*slope if math.isfinite(target_lower) else str(target_lower),
            "simultaneous_max_offtarget_upper95_score": off_upper*slope if math.isfinite(off_upper) else str(off_upper),
            "simultaneous_margin_lower95_score": (target_lower-off_upper)*slope if math.isfinite(target_lower) and math.isfinite(off_upper) else "-inf",
            "source_qc_filtered_pairs": sum(rows[(variant,p)]["filt"] for p in partners)})
    robust_ranking.sort(key=lambda x: x["simultaneous_margin_lower95_score"]
                        if isinstance(x["simultaneous_margin_lower95_score"], (int,float)) else -math.inf,
                        reverse=True)
    source_qc_complete_ranking.sort(key=lambda x: x["target_mean_minus_maxoff_score"], reverse=True)

    candidate_rows = []
    for variant in ("1eA", "4aR"):
        for partner in partners:
            row = rows.get((variant, partner))
            est = estimates.get((variant, partner))
            if row and est:
                candidate_rows.append({"variant": variant, "partner": partner,
                    "source_filt": row["filt"], "source_rel": row["rel"],
                    "count_logodds": est["estimate"],
                    "lower95": est["lower95"] if math.isfinite(est["lower95"]) else str(est["lower95"]),
                    "upper95": est["upper95"] if math.isfinite(est["upper95"]) else str(est["upper95"]), "n_reps": est["n_reps"],
                    "input_counts": [int(row[f"count_e{r}_s0"]) for r in range(1,7)],
                    "output_counts": [int(row[f"count_e{r}_s1"]) for r in range(1,7)]})

    output = {"interface": {
        "model": "conditional binomial output-count likelihood; matched input count is log-odds offset; WT-JUN x same partner is comparator",
        "zero_outputs": "retained as observed binomial outcomes, not pseudocounts",
        "input_zero": "replicate omitted because its input offset is undefined",
        "interval": "95% one-parameter profile likelihood conditional on observed inputs; no between-replicate random effect",
        "scope": "diagnostic reanalysis of released processed counts, not an experimental result or calibrated thermodynamic-energy model"},
        "count_stats": count_stats, "calibration_on_source_qc_pass": calibration,
        "top_20_single_mutants_by_count_level_target_margin": ranking[:20],
        "simultaneous_95_bonferroni_count_margin_top_20": robust_ranking[:20],
        "source_qc_complete_profile_margin_top_20": source_qc_complete_ranking[:20],
        "simultaneous_95_bonferroni": {"family": "all 52 bZIP partners for a given single mutant",
            "z_critical": simultaneous_z, "profile_loglik_half_threshold": simultaneous_lr_half,
            "scope": "conditional-input likelihood only; no replicate random effect"},
        "target_candidates": [x for x in ranking if x["variant"] in ("1eA", "4aR")],
        "candidate_partner_counts": candidate_rows}
    with open(os.path.join(OUT,"count_censor_results.json"),"w") as f:
        json.dump(output,f,indent=2,allow_nan=False)
    with open(os.path.join(OUT,"count_censor_results.json"),"a") as f:
        f.write("\n")
    print(json.dumps({"count_stats": count_stats, "calibration": calibration,
                      "top": ranking[:12], "target_candidates": [x for x in ranking if x['variant'] in ('1eA','4aR')]},
                     indent=2,allow_nan=False))


if __name__ == "__main__":
    main()
