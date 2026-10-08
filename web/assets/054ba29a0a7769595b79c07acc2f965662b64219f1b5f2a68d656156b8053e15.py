#!/usr/bin/env python3
"""Reproducible count/score audit of GSE315318 and the public DENet tables.

Run from the workspace root with Python 3 and NumPy installed. This script does
not retrain DENet. It checks what the released time-course tables can validate,
then tests whether within-lineage temporal forecasting beats chronology and
sequence-label shuffles for predicting the final abundance snapshot.
"""
from __future__ import annotations

import csv
import gzip
import glob
import math
import os
from pathlib import Path

import numpy as np

ROOT = Path("work/agents/c9_protein_evolvability/sources")
OUT = Path("work/agents/c9_protein_evolvability/children/design_representation/denet_metrics.txt")


def read_rows(path: Path, compressed: bool = False):
    opener = gzip.open if compressed else open
    with opener(path, "rt", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def counts_map(path: Path):
    with open(path, newline="") as f:
        rr = csv.reader(f, delimiter="\t")
        fields = [x.strip() for x in next(rr)]
        key = "mutation" if "mutation" in fields else "mutant"
        i, j = fields.index(key), fields.index("counts")
        out = {}
        for row in rr:
            row = [x.strip() for x in row]
            out[row[i]] = int(row[j])
    return out


def rankdata(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    out = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and xs[order[j]] == xs[order[i]]:
            j += 1
        rank = (i + j - 1) / 2 + 1
        for q in order[i:j]:
            out[q] = rank
        i = j
    return np.asarray(out, dtype=float)


def corr(x, y, rank=False):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if rank:
        x, y = rankdata(x), rankdata(y)
    if len(x) < 2 or np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def describe_forecast(protein, day_labels, maps, seeds=100):
    times = np.asarray([int(x) for x in day_labels], dtype=float)
    input_times, target_time = times[:-1], times[-1]
    input_maps, target_map = maps[:-1], maps[-1]
    all_names = set().union(*(d.keys() for d in maps))
    n_all = len(all_names)
    names = sorted(target_map)
    orders = np.asarray([0 if x == "origin" else len(x.split(";")) for x in names])
    # Read-count fractions remove cross-library sequencing-depth differences.
    # A fixed half-read pseudocount handles undetected genotypes.
    in_total = [sum(d.values()) for d in input_maps]
    out_total = sum(target_map.values())
    counts_in = np.asarray([[d.get(name, 0) for name in names] for d in input_maps], dtype=float).T
    X = np.log10((counts_in + .5) / (np.asarray(in_total)[None, :] + .5 * n_all))
    counts_out = np.asarray([target_map[name] for name in names], dtype=float)
    y = np.log10((counts_out + .5) / (out_total + .5 * n_all))
    # Persistence is the latest observed abundance; linear trend uses every
    # pre-terminal sample and extrapolates to the final assay day.
    persist = X[:, -1]
    tc = input_times - np.mean(input_times)
    pred = X.mean(axis=1) + (X @ tc) / (tc @ tc) * (target_time - np.mean(input_times))
    lines = []
    lines.append(f"{protein} terminal abundance forecast (N={len(names)} terminal genotypes)")
    for label, p in [("persistence", persist), ("linear-time trend", pred)]:
        mae = float(np.mean(np.abs(p - y)))
        lines.append(f"  {label}: Pearson={corr(p,y):.4f}; Spearman={corr(p,y,True):.4f}; log-frequency MAE={mae:.4f}")
    # Negative control 1: shuffle the three chronological labels but preserve
    # the same measured input snapshots and per-timepoint count distributions.
    # Six permutations are exhaustive; no random seed is involved.
    import itertools
    null_time = []
    for perm in itertools.permutations(range(len(input_maps))):
        # Keep each measured snapshot column fixed and reassign its date label.
        xp = X
        tp = times[list(perm)]
        tc_p = tp - np.mean(tp)
        pp = xp.mean(axis=1) + (xp @ tc_p) / (tc_p @ tc_p) * (target_time - np.mean(tp))
        null_time.append(corr(pp, y, True))
    lines.append("  chronology-label permutation Spearman (six input-date permutations): " +
                 ", ".join(f"{v:.4f}" for v in null_time))
    # Negative control 2: shuffle whole input histories across genotypes within
    # mutation order, preserving each order class and the temporal autocorrelation.
    rng = np.random.default_rng(1707)
    null_seq = []
    for _ in range(seeds):
        xp = X.copy()
        for order in np.unique(orders):
            ix = np.flatnonzero(orders == order)
            xp[ix] = xp[rng.permutation(ix)]
        pp = xp.mean(axis=1) + (xp @ tc) / (tc @ tc) * (target_time - np.mean(input_times))
        null_seq.append(corr(pp, y, True))
    lines.append(f"  order-matched whole-history shuffle Spearman: mean={np.mean(null_seq):.4f}, "
                 f"95% interval=[{np.quantile(null_seq,.025):.4f},{np.quantile(null_seq,.975):.4f}]")
    # Negative control 3: thin each observed input count to 20% to mimic lower
    # sequencing depth; assess prediction-rank stability against the unthinned target.
    stable = []
    # Vectorized binomial thinning of the measured input read counts.
    for _ in range(seeds):
        xthin_counts = rng.binomial(counts_in.astype(np.int64), .2)
        xthin = np.log10((xthin_counts + .5) / (.2 * np.asarray(in_total)[None, :] + .5 * n_all))
        pp = xthin.mean(axis=1) + (xthin @ tc) / (tc @ tc) * (target_time - np.mean(input_times))
        stable.append(corr(pp, y, True))
    lines.append(f"  20%-depth read thinning trend Spearman vs full-depth target: "
                 f"mean={np.mean(stable):.4f}, 95% interval=[{np.quantile(stable,.025):.4f},{np.quantile(stable,.975):.4f}]")
    return lines


def high_order_score_forecast(maps, score_rows, day_labels, repeats=100):
    """Use count trajectories to predict KRAS score labels on held-out 3+ mutants.

    This is a small linear stress test, not a DENet reproduction. Training is
    restricted to single/double mutants; all 3+ mutation labels are held out.
    """
    names = [r["mutant"] for r in score_rows]
    y = np.asarray([float(r["score"]) for r in score_rows])
    order = np.asarray([len(name.split(";")) for name in names], dtype=int)
    union = set().union(*(d.keys() for d in maps))
    xcount = []
    for d in maps:
        den = sum(d.values()) + .5 * len(union)
        xcount.append([math.log10((d.get(name, 0) + .5) / den) for name in names])
    xcount = np.asarray(xcount, dtype=float).T
    # Training/test partition is fixed by mutation order; no high-order score
    # enters model fitting or tuning.
    train = np.flatnonzero(order <= 2)
    test = np.flatnonzero(order >= 3)
    if not len(test):
        return []

    def fit_pred(F, tr, te):
        mu = F[tr].mean(axis=0)
        sd = F[tr].std(axis=0)
        sd[sd == 0] = 1
        A = (F - mu) / sd
        ymu = y[tr].mean()
        yc = y[tr] - ymu
        # Small ridge penalty stabilizes the few-feature fit; intercept is
        # unpenalized by centering.
        beta = np.linalg.solve(A[tr].T @ A[tr] + np.eye(A.shape[1]), A[tr].T @ yc)
        return ymu + A[te] @ beta

    features = {
        "mutation count only": order[:, None].astype(float),
        "terminal frequency + mutation count": np.column_stack([xcount[:, -1], order]),
        "all four trajectory frequencies": xcount,
        "all four trajectory frequencies + mutation count": np.column_stack([xcount, order]),
    }
    lines = [f"KRAS score forecasting on held-out 3+ mutants (train singles+doubles n={len(train)}, test n={len(test)})"]
    for label, F in features.items():
        pred = fit_pred(F, train, test)
        lines.append(f"  {label}: Pearson={corr(pred,y[test]):.4f}; Spearman={corr(pred,y[test],True):.4f}")
    # Descriptive full-table fit diagnoses whether the supplied score itself is
    # almost algebraically recoverable from the observed selected-population
    # trajectory. This is not a held-out generalization claim.
    Ffull = np.column_stack([np.ones(len(y)), xcount, order])
    beta, *_ = np.linalg.lstsq(Ffull, y, rcond=None)
    fit = Ffull @ beta
    r2 = 1 - float(np.sum((y - fit) ** 2) / np.sum((y - y.mean()) ** 2))
    lines.append("  descriptive all-row OLS R2 from [intercept, log-frequency day5/9/12/14, order]="
                 f"{r2:.6f}; coefficients=" + ",".join(f"{b:.4g}" for b in beta))
    # Negative control: shuffle whole trajectory feature vectors within each
    # mutation-order class, separately inside training and test, preserving the
    # burden and marginal count distributions while breaking genotype identity.
    rng = np.random.default_rng(3501)
    F = features["all four trajectory frequencies + mutation count"]
    null = []
    for _ in range(repeats):
        Fs = F.copy()
        for ix in (train, test):
            for k in np.unique(order[ix]):
                group = ix[order[ix] == k]
                Fs[group, :-1] = F[rng.permutation(group), :-1]
        pred = fit_pred(Fs, train, test)
        null.append(corr(pred, y[test], True))
    lines.append(f"  identity-shuffled trajectories within order: Spearman mean={np.mean(null):.4f}, "
                 f"95% interval=[{np.quantile(null,.025):.4f},{np.quantile(null,.975):.4f}]")
    return lines


def main():
    lines = ["GSE315318 / DENet count-target audit", ""]
    specs = {
        "KRAS": (["5", "9", "12", "14"], ["day5", "day9", "day12", "day14"]),
        # GEO says day15. The public DENet code repository calls that exact
        # terminal table Day20; the crosswalk below checks values, not filename.
        "MEK1": (["5", "7", "10", "15"], ["Day5", "Day7", "Day10", "Day20"]),
    }
    for protein, (days, repo_days) in specs.items():
        maps = [counts_map(ROOT / "DENet_paper/Data/DE_experiments" / protein / f"{d}.tsv") for d in repo_days]
        lines.append(f"{protein} snapshots: " + "; ".join(
            f"day{day}: {len(m)} genotypes, {sum(m.values()):,} listed reads" for day, m in zip(days, maps)))
        # Crosswalk GEO supplementary matrices to repository integer counts.
        geo_files = sorted(glob.glob(str(ROOT / "GSE315318" / f"*_{protein}_*.tsv.gz")),
                           key=lambda s: int(s.rsplit("_d", 1)[1].split(".")[0]))
        for day, repo, gf in zip(days, maps, geo_files):
            rows = read_rows(Path(gf), compressed=True)
            gkey = {r["mutation"]: float(r["score"]) for r in rows}
            common = set(gkey) & set(repo)
            if protein == "MEK1":
                exact = sum(gkey[k] == repo[k] for k in common)
                lines.append(f"  GEO day{day} vs repository {os.path.basename(gf)}: {len(common)}/{len(repo)} genotypes; "
                             f"integer count matches={exact}/{len(common)}")
            else:
                ratios = [repo[k] / gkey[k] for k in common if gkey[k] > 0]
                lines.append(f"  GEO day{day} vs repository {os.path.basename(gf)}: {len(common)}/{len(repo)} genotypes; "
                             f"count/score scale range={min(ratios):.3f}..{max(ratios):.3f}")
        lines.extend(describe_forecast(protein, days, maps))
        # Supervised-score crosswalk.
        score_rows = read_rows(ROOT / f"DENet_paper/Data/Protein_Info/score/{protein}_DE.tsv")
        score_key = "mutant"
        labels = {r[score_key]: float(r["score"]) for r in score_rows}
        last = maps[-1]
        overlap = set(labels) & set(last)
        orders = {}
        for name in labels:
            o = 0 if name == "origin" else len(name.split(";"))
            orders.setdefault(o, []).append(name)
        lines.append(f"{protein} score table: {len(labels)} variants, terminal overlap {len(overlap)}/{len(labels)}")
        if protein == "MEK1":
            exact = sum(abs(labels[k] - math.log10(last[k])) < 1e-12 for k in overlap)
            lines.append(f"  score == log10(day15 terminal count) for {exact}/{len(overlap)} overlapping variants; "
                         f"the score table is the terminal count target transformed, not a separate function assay")
        else:
            start = maps[0]
            ratio_names = [k for k in overlap if k in start and k in last and start[k] > 0 and last[k] > 0]
            offsets = [labels[k] - math.log10(last[k] / start[k]) for k in ratio_names]
            offset_min, offset_max = min(offsets), max(offsets)
            lines.append(f"  exact target identity: score = log10(day14_count/day5_count) + c; "
                         f"n={len(ratio_names)}/{len(labels)}, c range=[{offset_min:.15f},{offset_max:.15f}]")
            for day, m in zip(days, maps):
                ov = set(labels) & set(m)
                xs = [math.log10(m[k] + 1) for k in ov]
                ys = [labels[k] for k in ov]
                lines.append(f"  KRAS score vs log10(count+1) at day{day}: n={len(ov)}, "
                             f"Spearman={corr(xs,ys,True):.4f}, Pearson={corr(xs,ys):.4f}")
            high = [k for k in overlap if len(k.split(";")) >= 3]
            lines.append(f"  higher-order score variants (3+ substitutions) overlapping terminal selected population: {len(high)}")
            lines.extend(high_order_score_forecast(maps, score_rows, days))
        lines.append("")
    OUT.write_text("\n".join(lines) + "\n")
    print(OUT)
    print(OUT.read_text())


if __name__ == "__main__":
    main()
