"""Scoped numeric falsification checks for support-coded covariance discovery.

Population exact arithmetic is NOT claimed: these are floating-point fixtures.
The accompanying report contains the algebraic proofs and the prior-art downgrade.
"""
from pathlib import Path
import itertools
import json
import numpy as np

RNG = np.random.default_rng(20261007)


def code(d):
    m = max(1, int(np.ceil(8 * np.log(max(2, d * (d - 1))))))
    trials = 0
    while True:
        trials += 1
        bits = RNG.integers(0, 2, (m, d))
        distances = np.sum(bits[:, :, None] != bits[:, None, :], axis=0)
        np.fill_diagonal(distances, m)
        if distances.min() >= m / 4:
            return np.concatenate([bits, 1 - bits]), float(distances.min() / m), trials


def model(d, masks):
    b = RNG.normal(0, .07, (d, d))
    np.fill_diagonal(b, 0)
    b *= .5 / max(.5, np.linalg.norm(b, 2))
    a = np.eye(d) - b
    mixing = np.linalg.inv(a)
    u = RNG.normal(size=(d, d))
    omega = np.eye(d) + u @ u.T / d
    baseline = mixing @ omega @ mixing.T
    covs, interventions = [], []
    for mask in masks:
        active = np.flatnonzero(mask)
        k = np.zeros((d, d))
        if len(active):
            v = RNG.normal(size=(len(active), len(active)))
            block = np.eye(len(active)) + v @ v.T / max(1, len(active))
            k[np.ix_(active, active)] = block
        interventions.append(k)
        covs.append(baseline + mixing @ k @ mixing.T)
    return a, mixing, baseline, covs, interventions


def decode(baseline, covs, masks):
    d, e = len(baseline), len(covs)
    out, gaps, nulls = np.zeros((d, d)), [], []
    for i in range(d):
        chosen = np.flatnonzero(masks[:, i] == 0)
        if not len(chosen):
            raise ValueError("No excluded-target environments")
        s = sum(covs[l] - baseline for l in chosen) / len(chosen)
        vals, vecs = np.linalg.eigh(s)
        q = vecs[:, 0]
        out[i] = q / q[i]
        gaps.append(float(vals[1]))
        nulls.append(float(abs(vals[0])))
    return out, gaps, nulls


def cov_support_fit(a, baseline, covs, masks, tolerance=2e-7):
    fitted = []
    for l, (cov, mask) in enumerate(zip(covs, masks)):
        k = a @ (cov - baseline) @ a.T
        off = k.copy()
        active = np.flatnonzero(mask)
        off[np.ix_(active, active)] = 0
        support_error = np.linalg.norm(off, 2)
        min_active = np.linalg.eigvalsh(k[np.ix_(active, active)]).min() if len(active) else 1.
        if support_error < tolerance and min_active > tolerance:
            fitted.append(l)
    return fitted


def robust_population_decode(baseline, covs, masks, k):
    e, d = masks.shape
    tried = 0
    for bad in itertools.combinations(range(e), k):
        tried += 1
        keep = [l for l in range(e) if l not in bad]
        candidates, ok = np.zeros((d, d)), True
        for i in range(d):
            inactive = [l for l in keep if masks[l, i] == 0]
            s = sum(covs[l] - baseline for l in inactive)
            vals, vectors = np.linalg.eigh(s)
            q = vectors[:, 0]
            if abs(vals[0]) > 2e-7 or vals[1] < 2e-7 or abs(q[i]) < 2e-7:
                ok = False
                break
            candidates[i] = q / q[i]
        if ok and abs(np.linalg.det(candidates)) > 1e-7:
            fit = cov_support_fit(candidates, baseline, covs, masks)
            if len(fit) >= e - k:
                return candidates, tried, fit
    raise ValueError("No valid candidate found")


def sharp_ambiguity(masks, i, j):
    e, d = masks.shape
    sep = np.flatnonzero((masks[:, j] == 1) & (masks[:, i] == 0)).tolist()
    k = int(np.ceil(len(sep) / 2))
    a0 = np.eye(d)
    a1 = np.eye(d)
    a1[i, j] = -.2
    mixing1 = np.linalg.inv(a1)
    baseline = np.eye(d)
    covs = []
    left = set(sep[:k])
    for l, mask in enumerate(masks):
        diagonal = np.diag(mask)
        # Nonseparating masks are compatible with both models. At separating
        # masks, use model 0 on one half and model 1 on the other half.
        change = diagonal if l not in sep or l in left else mixing1 @ diagonal @ mixing1.T
        covs.append(baseline + change)
    fits0 = cov_support_fit(a0, baseline, covs, masks)
    fits1 = cov_support_fit(a1, baseline, covs, masks)
    assert e - len(fits0) <= k and e - len(fits1) <= k
    return {"separating_contexts": len(sep), "k": k,
            "model_0_bad": e - len(fits0), "model_1_bad": e - len(fits1),
            "matrix_distance": float(np.linalg.norm(a0 - a1))}


def calibrated_decode(baseline, calibration, covs, masks, k):
    e, d = masks.shape
    vals, vectors = np.linalg.eigh(calibration - baseline)
    w = (vectors / np.sqrt(vals)) @ vectors.T
    projectors = []
    for cov in covs:
        p = w @ (cov - baseline) @ w
        values, basis = np.linalg.eigh(p)
        positive = basis[:, values > 1e-7]
        projectors.append(positive @ positive.T)
    tried = 0
    for bad in itertools.combinations(range(e), k):
        tried += 1
        keep = [l for l in range(e) if l not in bad]
        a, ok = np.zeros((d, d)), True
        for i in range(d):
            h = sum((np.eye(d) - projectors[l]) if masks[l, i] else projectors[l] for l in keep)
            values, basis = np.linalg.eigh(h)
            if abs(values[0]) > 1e-7 or values[1] < 1e-7:
                ok = False
                break
            row = basis[:, 0] @ w
            if abs(row[i]) < 1e-7:
                ok = False
                break
            a[i] = row / row[i]
        if ok:
            calibrated = a @ (calibration - baseline) @ a.T
            residual = calibrated - np.diag(np.diag(calibrated))
            fit = cov_support_fit(a, baseline, covs, masks)
            if np.linalg.norm(residual, 2) < 1e-7 and len(fit) >= e - k:
                return a, tried, fit
    raise ValueError("No calibrated candidate")


def calibrated_ambiguity(masks, i, j):
    e, d = masks.shape
    sep = np.flatnonzero(masks[:, i] != masks[:, j]).tolist()
    k = int(np.ceil(len(sep) / 2))
    rotation = np.eye(d)
    theta = .15
    c, s = np.cos(theta), np.sin(theta)
    rotation[np.ix_([i, j], [i, j])] = [[c, -s], [s, c]]
    a0 = np.eye(d)
    a1 = rotation.T / np.diag(rotation.T)[:, None]
    baseline, calibration = np.eye(d), 2 * np.eye(d)
    observed, left = [], set(sep[:k])
    for l, mask in enumerate(masks):
        diagonal = np.diag(mask)
        observed.append(baseline + (diagonal if l not in sep or l in left else rotation @ diagonal @ rotation.T))
    fits0 = cov_support_fit(a0, baseline, observed, masks)
    fits1 = cov_support_fit(a1, baseline, observed, masks)
    cal1 = a1 @ (calibration - baseline) @ a1.T
    assert np.linalg.norm(cal1 - np.diag(np.diag(cal1))) < 1e-10
    assert e - len(fits0) <= k and e - len(fits1) <= k
    return {"hamming_separating_contexts": len(sep), "k": k,
            "model_0_bad": e - len(fits0), "model_1_bad": e - len(fits1),
            "all_on_diagonal_residual": float(np.linalg.norm(cal1 - np.diag(np.diag(cal1)))),
            "matrix_distance": float(np.linalg.norm(a0 - a1))}


def rank_one_failure():
    d = 8
    bits = np.array([[(j >> b) & 1 for j in range(d)] for b in range(3)])
    masks = np.concatenate([bits, 1 - bits])
    directions = []
    covs = []
    for mask in masks:
        v = mask * RNG.uniform(.5, 1.5, d)
        directions.append(v)
        covs.append(np.eye(d) + np.outer(v, v))
    # Every response row has only three homogeneous constraints on seven
    # off-diagonal entries. Find an explicit alternate row perturbation.
    a1 = np.eye(d)
    i = 0
    cols = [j for j in range(d) if j != i]
    constraints = np.array([directions[l][cols] for l in range(len(masks)) if masks[l, i] == 0])
    _, _, vh = np.linalg.svd(constraints, full_matrices=True)
    w = vh[-1]
    a1[i, cols] += .02 * w
    mismatches = []
    active_min = []
    for cov, mask in zip(covs, masks):
        k = a1 @ (cov - np.eye(d)) @ a1.T
        inactive = np.flatnonzero(mask == 0)
        mismatches.append(float(np.linalg.norm(k[inactive], 2)))
        active_min.append(int(np.linalg.matrix_rank(k, tol=1e-7)))
    assert max(mismatches) < 1e-10
    return {"d": d, "environments": len(masks), "alternative_matrix_distance": float(np.linalg.norm(a1 - np.eye(d))),
            "max_off_support_residual": max(mismatches), "intervention_ranks": active_min}


def sample_cov(cov, n):
    data = RNG.normal(size=(n, len(cov))) @ np.linalg.cholesky(cov).T
    return data.T @ data / n


def main():
    result = {"seed": 20261007, "arithmetic": "numpy float64", "population_checks": []}
    for d in [3, 8, 16]:
        masks, distance, trials = code(d)
        for repetition in range(3):
            a, mixing, baseline, covs, ks = model(d, masks)
            estimated, gaps, nulls = decode(baseline, covs, masks)
            err = float(np.max(np.linalg.norm(estimated - a, axis=1)))
            gap_lower = distance * np.linalg.svd(mixing, compute_uv=False).min() ** 2
            assert err < 1e-10 and min(gaps) >= gap_lower - 1e-10
            result["population_checks"].append({"d": d, "repetition": repetition,
                "environments": len(masks), "relative_bit_distance": distance,
                "code_rejection_trials": trials, "max_row_error": err,
                "minimum_gap": min(gaps), "proved_gap_lower": float(gap_lower),
                "largest_null_eigenvalue": max(nulls)})
    base_bits = np.array([[0, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 0]])
    repeated = np.repeat(base_bits, 3, axis=0)
    masks = np.concatenate([repeated, 1 - repeated])
    a, mixing, baseline, covs, ks = model(4, masks)
    observed = [x.copy() for x in covs]
    for l in [2, 14]:
        v = RNG.normal(size=(4, 4))
        observed[l] = baseline + .3 * np.eye(4) + v @ v.T
    estimated, tried, fit = robust_population_decode(baseline, observed, masks, 2)
    result["corrupt_population_check"] = {"environments": len(masks), "k": 2,
        "ordered_separation_min": 6, "subsets_tried": tried, "contexts_fit": len(fit),
        "max_row_error": float(np.max(np.linalg.norm(estimated - a, axis=1)))}
    assert result["corrupt_population_check"]["max_row_error"] < 1e-10
    result["sharp_ambiguity"] = sharp_ambiguity(masks, 0, 1)
    a, mixing, baseline, covs, ks = model(4, repeated)
    actuation = np.diag(RNG.uniform(.7, 1.5, 4))
    calibration = baseline + mixing @ actuation @ mixing.T
    observed = [x.copy() for x in covs]
    for l in [1, 7]:
        v = RNG.normal(size=(4, 4))
        observed[l] = baseline + .4 * np.eye(4) + v @ v.T
    estimated, tried, fit = calibrated_decode(baseline, calibration, observed, repeated, 2)
    result["calibrated_corrupt_population_check"] = {"environments": len(repeated), "k": 2,
        "hamming_separation_min": 6, "subsets_tried": tried, "contexts_fit": len(fit),
        "max_row_error": float(np.max(np.linalg.norm(estimated - a, axis=1)))}
    assert result["calibrated_corrupt_population_check"]["max_row_error"] < 1e-10
    result["calibrated_sharp_ambiguity"] = calibrated_ambiguity(repeated, 0, 1)
    result["rank_one_failure"] = rank_one_failure()
    masks, distance, trials = code(8)
    a, mixing, baseline, covs, ks = model(8, masks)
    m = len(masks) // 2
    result["sample_checks"] = []
    for n_anchor in [2500, 10000, 40000]:
        n_mask = int(np.ceil(n_anchor / m))
        base_est = sample_cov(baseline, n_anchor)
        mask_est = [sample_cov(c, n_mask) for c in covs]
        estimated, gaps, nulls = decode(base_est, mask_est, masks)
        result["sample_checks"].append({"d": 8, "environments": len(masks),
            "n_baseline": n_anchor, "n_per_mask": n_mask,
            "total_samples": n_anchor + len(masks) * n_mask,
            "max_row_error": float(np.max(np.linalg.norm(estimated - a, axis=1))),
            "mean_row_error": float(np.mean(np.linalg.norm(estimated - a, axis=1))),
            "min_empirical_second_eigenvalue": min(gaps)})
    target = Path(__file__).with_name("causal_discovery_check.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
