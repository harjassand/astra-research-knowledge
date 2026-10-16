"""Retrospective diagnostics on actual NIST measured data, never synthetic labels.

All spectra are supplied up front to spectral arms. Their acquisition is charged
separately. Computational partitions are not expert phase labels. No causal or
external-transfer conclusion follows from this one-library exercise.
"""
from pathlib import Path
import argparse
import hashlib
import json
import time
import warnings

import numpy as np
from scipy.io import loadmat
from scipy.linalg import cho_factor, cho_solve
from scipy.spatial.distance import cdist
from scipy.special import ndtr
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from threadpoolctl import threadpool_limits

BASE = Path(__file__).resolve().parent


def load():
    data = loadmat(BASE / "data/FeCoNi_benchmark_dataset_220501a.mat")
    c = data["C"] / data["C"].sum(axis=1, keepdims=True)
    raw = data["XRD"]
    bg = np.quantile(raw, .1, axis=1, keepdims=True)
    positive = np.maximum(raw - bg, 0)
    shape = positive / positive.sum(axis=1, keepdims=True)
    pc = PCA(n_components=8, svd_solver="full").fit_transform(shape)
    labels = KMeans(n_clusters=5, n_init=20, random_state=62026).fit_predict(pc)
    tth = data["TTH"].ravel()
    centroid = shape @ tth
    width = np.sqrt(np.sum(shape * (tth[None, :] - centroid[:, None])**2, axis=1))
    y = {"Coer": data["Coer"].ravel(), "Kerr": data["Kerr"].ravel()}
    return c, shape, pc, labels, y, centroid, width, positive.sum(axis=1)


def kernels(c, pc, labels):
    d = cdist(c, c)
    s = cdist(pc, pc)
    s /= np.median(s[s > 0])
    same = labels[:, None] == labels[None, :]
    names, mats = [], []
    for length in [.05, .1, .2, .4, .8]:
        z = np.sqrt(3) * d / length
        km = (1 + z) * np.exp(-z)
        names.append(f"composition_matern32_l{length}")
        mats.append(km)
    base_ids = list(range(len(mats)))
    for i in base_ids:
        for spec_length in [.4, 1.2]:
            ks = np.exp(-.5 * (s / spec_length)**2)
            names.append(names[i] + f"_plus_spectral_l{spec_length}")
            mats.append(.5 * mats[i] + .5 * ks)
        names.append(names[i] + "_partition")
        # Common residual retains some covariance across computational partitions.
        mats.append(mats[i] * (.1 + .9 * same))
    return names, np.asarray(mats), {
        "composition": list(range(5)),
        "continuous_spectra": [i for i, n in enumerate(names) if "spectral" in n],
        "partition": [i for i, n in enumerate(names) if "partition" in n],
        "equally_informed_union": list(range(len(names))),
    }


def posterior(K, observed, y, predict, noise):
    mean = float(np.mean(y[observed]))
    scale = max(float(np.std(y[observed])), .01)
    ys = (y[observed] - mean) / scale
    A = K[np.ix_(observed, observed)] + noise * np.eye(len(observed))
    factor = cho_factor(A, lower=True, check_finite=False)
    alpha = cho_solve(factor, ys, check_finite=False)
    B = K[np.ix_(observed, predict)]
    mu = mean + scale * (B.T @ alpha)
    variance = np.maximum(1 - np.sum(B * cho_solve(factor, B, check_finite=False), axis=0), 1e-12)
    mll = -.5 * ys @ alpha - np.log(np.diag(factor[0])).sum() - .5 * len(observed) * np.log(2*np.pi)
    return mu, scale*np.sqrt(variance), float(mll)


def fit_select(Ks, ids, train, y, test, validation=None):
    best = None
    for i in ids:
        for noise in [.001, .01, .1]:
            mu, sigma, mll = posterior(Ks[i], train, y, test if validation is None else validation, noise)
            score = mll if validation is None else -float(np.mean((mu-y[validation])**2))
            if best is None or score > best[0]:
                best = (score, i, noise, mu, sigma)
    if validation is not None:
        joint = np.r_[train, validation]
        mu, sigma, _ = posterior(Ks[best[1]], joint, y, test, best[2])
        return mu, sigma, best[1], best[2]
    return best[3], best[4], best[1], best[2]


def prediction(c, Ks, arms, outputs):
    # Whole composition regions are held out; this is spatial interpolation/
    # extrapolation, still not a separately fabricated material validation batch.
    regions = KMeans(n_clusters=6, random_state=92026, n_init=20).fit_predict(c)
    runs = []
    for split_type in ["random", "composition_region"]:
        for fold in range(6):
            rng = np.random.default_rng(20261015 + fold)
            test = np.where(regions == fold)[0] if split_type == "composition_region" else rng.choice(len(c), 154, replace=False)
            pool = np.setdiff1d(np.arange(len(c)), test)
            observed = rng.choice(pool, 128, replace=False)
            train, val = observed[:96], observed[96:]
            for output, y in outputs.items():
                for arm, ids in arms.items():
                    mu, sd, ki, noise = fit_select(Ks, ids, train, y, test, val)
                    err = mu-y[test]
                    runs.append({"split": split_type, "fold": fold, "output": output,
                                 "arm": arm, "train_indices_0based": observed.tolist(),
                                 "test_indices_0based": test.tolist(), "kernel_index": ki,
                                 "noise": noise, "rmse": float(np.sqrt(np.mean(err**2))),
                                 "mae": float(np.mean(abs(err))),
                                 "latent_95_interval_coverage": float(np.mean(abs(err) <= 1.96*sd)),
                                 "predictions": mu.tolist(), "source_observations": y[test].tolist()})
    return runs


def acquisition(Ks, arms, outputs, seeds=12, budget=80):
    n = Ks.shape[1]
    runs = []
    for output, y in outputs.items():
        for seed in range(seeds):
            rng = np.random.default_rng(730000 + seed)
            initial = rng.choice(n, 8, replace=False).tolist()
            for arm, ids in arms.items():
                observed = initial.copy()
                choices = []
                start = time.perf_counter()
                for step in range(len(observed), budget):
                    candidates = np.setdiff1d(np.arange(n), observed)
                    mu, sd, ki, noise = fit_select(Ks, ids, np.asarray(observed), y, candidates)
                    delta = mu - np.max(y[observed])
                    z = delta/sd
                    ei = delta*ndtr(z) + sd*np.exp(-.5*z*z)/np.sqrt(2*np.pi)
                    index = int(candidates[np.argmax(ei)])
                    observed.append(index)
                    choices.append({"step": step+1, "kernel_index": ki, "noise": noise})
                best = np.maximum.accumulate(y[observed])
                runs.append({"output": output, "seed": seed, "arm": arm,
                             "indices_0based": observed, "observed_values": y[observed].tolist(),
                             "best_values": best.tolist(), "regret": (y.max()-best).tolist(),
                             "selection_models": choices, "wall_seconds": time.perf_counter()-start,
                             "first_hit": {str(level): (int(np.where(best>=level*y.max())[0][0])+1 if np.any(best>=level*y.max()) else None)
                                           for level in [.9, .95, .999, 1.0]}})
            # Preserve random order. setdiff1d is used only to form the pool;
            # it sorts, so it must never define the random trajectory itself.
            pool = np.setdiff1d(np.arange(n), initial)
            observed = np.r_[initial, rng.choice(pool, budget-8, replace=False)]
            best = np.maximum.accumulate(y[observed])
            runs.append({"output": output,"seed":seed,"arm":"random","indices_0based":observed.tolist(),
                         "observed_values":y[observed].tolist(),"best_values":best.tolist(),"regret":(y.max()-best).tolist(),
                         "first_hit":{str(level):(int(np.where(best>=level*y.max())[0][0])+1 if np.any(best>=level*y.max()) else None)
                                      for level in [.9,.95,.999,1.0]}})
            print(output, seed, "completed", flush=True)
    return runs


def structural_audit(c, shape, labels, outputs, centroid, width, area):
    out = {"composition_order": "C1,C2,C3; public file description does not state element ordering",
           "n_unique_compositions": len(np.unique(c, axis=0)), "n_rows": len(c),
           "XRD_range_2theta_deg": [42.6,47.0], "XRD_bins": shape.shape[1],
           "independent_synthesis_batches_in_acquired_data": None,
           "repeated_measurements_in_acquired_data": None, "calibration_in_acquired_data": None}
    distance = cdist(shape, shape, metric="cosine")
    np.fill_diagonal(distance, np.inf)
    nearest = distance.argmin(axis=1)
    for key,y in outputs.items():
        ranking = np.argsort(y)[::-1]
        out[key] = {"max": float(y.max()), "min":float(y.min()),
                    "top_10": [{"row_1based":int(i)+1,"C_percent":(100*c[i]).tolist(),"value":float(y[i]),
                                "partition":int(labels[i]),"XRD_centroid":float(centroid[i]),"XRD_width":float(width[i])}
                               for i in ranking[:10]],
                    "top_two_gap":float(y[ranking[0]]-y[ranking[1]]),
                    "symmetric_per_specimen_error_needed_to_reverse_top_two":float((y[ranking[0]]-y[ranking[1]])/2),
                    "within_max_fraction":{str(level):int(np.sum(y>=level*y.max())) for level in [.9,.95,.99,.999]},
                    "partitions": []}
        for label in np.unique(labels):
            ix=np.where(labels==label)[0]
            out[key]["partitions"].append({"partition":int(label),"n":len(ix),"min":float(y[ix].min()),"max":float(y[ix].max()),"sd":float(y[ix].std()),"mean":float(y[ix].mean())})
        diffs=abs(y-y[nearest]); order=np.argsort(diffs)[::-1]
        out[key]["spectral_nearest_neighbor_contrasts"]=[{
            "rows_1based":[int(i)+1,int(nearest[i])+1],"cosine_distance":float(distance[i,nearest[i]]),
            "values":[float(y[i]),float(y[nearest[i]])],"absolute_difference":float(diffs[i]),
            "composition_distance_fraction":float(np.linalg.norm(c[i]-c[nearest[i]]))}
            for i in order[:20]]
    return out


def summarize(pred, searches):
    out={"prediction":[],"acquisition":[]}
    for output in ["Coer","Kerr"]:
        for split in ["random","composition_region"]:
            for arm in sorted({r["arm"] for r in pred}):
                rows=[r for r in pred if r["output"]==output and r["split"]==split and r["arm"]==arm]
                out["prediction"].append({"output":output,"split":split,"arm":arm,
                    "mean_rmse":float(np.mean([r["rmse"] for r in rows])),
                    "mean_mae":float(np.mean([r["mae"] for r in rows])),
                    "mean_latent_95_coverage":float(np.mean([r["latent_95_interval_coverage"] for r in rows]))})
        for arm in sorted({r["arm"] for r in searches}):
            rows=[r for r in searches if r["output"]==output and r["arm"]==arm]
            hits={str(level):[r["first_hit"][str(level)] for r in rows] for level in [.9,.95,.999,1.0]}
            out["acquisition"].append({"output":output,"arm":arm,"n_runs":len(rows),
                "mean_regret_at":{str(n):float(np.mean([r["regret"][n-1] for r in rows])) for n in [16,32,64,80]},
                "first_hit":{level:{"successes_within_80":sum(v is not None for v in vals),
                     "median_censored_81":float(np.median([81 if v is None else v for v in vals])),"counts":vals}
                     for level,vals in hits.items()}})
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--seeds",type=int,default=12)
    parser.add_argument("--skip-search",action="store_true")
    parser.add_argument("--output",default="results_v2")
    args=parser.parse_args()
    output_path=BASE/args.output
    if output_path.exists() and any(output_path.iterdir()):
        parser.error("output already contains artifacts; select a fresh --output path")
    output_path.mkdir(parents=True,exist_ok=True)
    started=time.perf_counter()
    with threadpool_limits(limits=1):
        c,shape,pc,labels,outputs,centroid,width,area=load()
        names,Ks,arms=kernels(c,pc,labels)
        (output_path/"KERNELS.json").write_text(json.dumps({"names":names,"arms":arms},indent=2)+"\n")
        audit=structural_audit(c,shape,labels,outputs,centroid,width,area)
        (output_path/"STRUCTURAL_TARGET_AUDIT.json").write_text(json.dumps(audit,indent=2)+"\n")
        pred=prediction(c,Ks,arms,outputs)
        (output_path/"PREDICTION_RUNS.json").write_text(json.dumps(pred,indent=2)+"\n")
        searches=[] if args.skip_search else acquisition(Ks,arms,outputs,args.seeds)
        (output_path/"ACQUISITION_RUNS.json").write_text(json.dumps(searches,indent=2)+"\n")
        summary=summarize(pred,searches)
        summary["code_wall_seconds"]=time.perf_counter()-started
        summary["scope"]="retrospective_actual_measured_labels_one_library_not_new_physical_experiment"
        summary["all_spectra_cost_per_spectral_arm"]="921 XRD acquisitions plus calibration, analysis and stage motion"
        summary["physical_costs_unknown"]=True
        summary["inference_tokens"]=None;summary["inference_energy"]=None;summary["inference_cost"]=None
        (output_path/"DIAGNOSTIC_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n")
        print(json.dumps(summary,indent=2))


if __name__=="__main__":main()
