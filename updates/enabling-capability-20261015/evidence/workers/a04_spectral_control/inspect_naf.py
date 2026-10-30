"""Inspect the acquired NaF archive and profile a deliberately restricted model.

No downloaded Python is executed. Zip members are read in memory. The lifetime
fit is a processed-data diagnostic, not a physical model comparison or CI.
Run with python3 inspect_naf.py; NumPy/SciPy are shared local dependencies.
"""
from pathlib import Path
from collections import defaultdict
import hashlib
import io
import json
import re
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "measurement_search" / "deps"))
import numpy as np
from scipy.optimize import minimize
from scipy.stats import exponnorm, norm


def inventory():
    result = {}
    for path in sorted((ROOT / "data").glob("*.zip")):
        with zipfile.ZipFile(path) as archive:
            members = [i for i in archive.infolist() if not i.is_dir()]
            groups = defaultdict(lambda: defaultdict(set))
            examples = []
            for member in members:
                match = re.search(
                    r"([^/]*FWM)(_BKG_)?step(\d+)_iter(\d+)\.txt$",
                    member.filename,
                )
                if match:
                    folder = member.filename.rsplit("/", 1)[0]
                    key = folder + ":" + match.group(1)
                    role = "background" if match.group(2) else "signal"
                    groups[key][f"{role}:iteration:{int(match.group(4)):02}"] .add(
                        int(match.group(3))
                    )
                elif "CrossCorr_FWM_iter00" in member.filename:
                    raw = archive.read(member)
                    array = np.loadtxt(io.BytesIO(raw))
                    examples.append({
                        "name": member.filename,
                        "shape": list(array.shape),
                        "header": [x for x in raw.decode().splitlines()
                                   if x.startswith("#")],
                    })
            result[path.name] = {
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "file_count": len(members),
                "uncompressed_bytes": sum(i.file_size for i in members),
                "groups": {
                    k: {r: {"count": len(s), "minimum_step": min(s),
                            "maximum_step": max(s)}
                        for r, s in sorted(v.items())}
                    for k, v in groups.items()
                },
                "calibration_examples": examples,
            }
    return result


def load_processed():
    with zipfile.ZipFile(ROOT / "data" / "Processed.zip") as archive:
        return {Path(name).name: np.load(io.BytesIO(archive.read(name)))
                for name in archive.namelist() if name.endswith(".npy")}


def profile_line(t, y, taus):
    """Gaussian instrument response convolved with exponential of mean tau.

    t0, Gaussian width, amplitude and constant baseline are re-fitted at every
    tau. tau=0 is evaluated as an exact Gaussian, avoiding singular rate fits.
    Unweighted SSE is used because processed arrays have no covariance model.
    """
    yscale = max(np.ptp(y), 1e-12)
    yy = y / yscale

    def solve(tau):
        def residual(par, details=False):
            center, log_sigma = par
            sigma = np.exp(log_sigma)
            response = (norm.pdf(t, loc=center, scale=sigma) if tau == 0 else
                        exponnorm.pdf(t, tau/sigma, loc=center, scale=sigma))
            design = np.column_stack([response, np.ones_like(t)])
            coeff, *_ = np.linalg.lstsq(design, yy, rcond=None)
            err = yy - design @ coeff
            if details:
                return dict(tau_fs=float(tau), sse=float(err @ err),
                            center_fs=float(center),
                            gaussian_fwhm_fs=float(2*np.sqrt(2*np.log(2))*sigma),
                            amplitude=float(coeff[0]*yscale),
                            baseline=float(coeff[1]*yscale))
            return float(err @ err)

        starts = [(t[np.argmax(y)]-tau, np.log(s)) for s in (2.0, 3.5, 5.0)]
        fitted = [minimize(residual, p, method="L-BFGS-B",
                           bounds=[(-25, 25), (np.log(.25), np.log(15))],
                           options={"ftol": 1e-13, "gtol": 1e-9})
                  for p in starts]
        best = min(fitted, key=lambda fit: fit.fun)
        out = residual(best.x, details=True)
        out["optimizer_success"] = bool(best.success)
        return out

    return [solve(tau) for tau in taus]


def profile_processed(data):
    output = {}
    taus = np.r_[0.0, .025, .05, .1, .2, .3, .5, .75, 1., 1.5, 2., 3., 5., 8.]
    # Exact windows and offsets used by deposited Make_Figures.py. The source
    # crops the first 331 pixels, then selects these channel centers.
    for label, centers, offset in [
        ("Bright", (752, 808), 3.),
        ("Dark", (749, 802), -1.),
    ]:
        array = data[f"Processed {label}.npy"][:, 331:]
        t = data[f"TimeAxis{label}.npy"][2:] + offset
        for index, center in enumerate(centers, 1):
            y = -array[2:, center-15:center+15].sum(axis=1)
            fitted = profile_line(t, y, taus)
            null = fitted[0]
            best = min(fitted, key=lambda f: f["sse"])
            output[f"{label}_X{index}"] = {
                "n_points": len(t),
                "time_min_fs": float(t.min()),
                "time_max_fs": float(t.max()),
                "original_pixel_window": [center+331-15, center+331+15],
                "tau_zero": null,
                "best_grid": best,
                "relative_sse_reduction_vs_zero":
                    (null["sse"] - best["sse"]) / null["sse"],
                "profile": fitted,
            }
    return output


if __name__ == "__main__":
    start = time.perf_counter()
    inv = inventory()
    (ROOT / "ARCHIVE_SCHEMA.json").write_text(json.dumps(inv, indent=2)+"\n")
    data = load_processed()
    profiles = profile_processed(data)
    output = {
        "scope": "Restricted processed-data profile; no physical lifetime CI, "
                 "no raw-heldout fit and no exclusion of competing Hamiltonians.",
        "model": "Gaussian IRF convolved with exponential; constant baseline; "
                 "center and width are independently refitted at each lifetime.",
        "observation_noise_covariance": "NOT_ACQUIRED",
        "profiles": profiles,
        "wall_seconds_measured": time.perf_counter()-start,
        "model_inference_tokens": "UNAVAILABLE",
        "physical_experiment_performed": False,
    }
    (ROOT / "LIFETIME_PROFILE.json").write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps({"wall_seconds_measured": output["wall_seconds_measured"],
                      "profiles": {k: {f: v[f] for f in (
                          "tau_zero", "best_grid", "relative_sse_reduction_vs_zero")}
                                   for k, v in profiles.items()}}, indent=2))
