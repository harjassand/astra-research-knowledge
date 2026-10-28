"""Numerical diagnostics for finite-excursion SLD truncation.

These checks illustrate a proved bound; floating-point checks are not proofs.
Only numpy is needed. Run from this directory to regenerate diagnostics.json.
"""
from pathlib import Path
import json
import numpy as np


def herm(x):
    return (x + x.conj().T) / 2


def state(rng, d, rank=None):
    k = d if rank is None else rank
    z = rng.normal(size=(d, k)) + 1j * rng.normal(size=(d, k))
    x = z @ z.conj().T
    return x / np.trace(x).real


def norm1(x):
    return float(np.abs(np.linalg.eigvalsh(herm(x))).sum())


def score(alpha, beta, excursion=1.0):
    rho = (alpha + beta) / 2
    tangent = (alpha - beta) / (2 * excursion)
    lam, v = np.linalg.eigh(herm(rho))
    lam = np.maximum(lam, 0)
    hv = v.conj().T @ tangent @ v
    den = lam[:, None] + lam[None, :]
    lv = np.divide(2 * hv, den, out=np.zeros_like(hv), where=den > 1e-13)
    sl = herm(v @ lv @ v.conj().T)
    return float(np.trace(tangent @ sl).real), float(np.max(np.abs(np.linalg.eigvalsh(sl))))


def random_channel(rng, din=2, dout=2, env=3):
    z = rng.normal(size=(dout * env, din)) + 1j * rng.normal(size=(dout * env, din))
    v, _ = np.linalg.qr(z)
    return [v[i * dout:(i + 1) * dout] for i in range(env)]


def apply_channel(x, kraus, refdim):
    ans = np.zeros((kraus[0].shape[0] * refdim,) * 2, dtype=complex)
    for k in kraus:
        kr = np.kron(k, np.eye(refdim))
        ans += kr @ x @ kr.conj().T
    return herm(ans)


def compress_ref(x, da, dr, cut):
    """Keep levels 0,...,cut-1 and reset all higher levels to level 0."""
    t = x.reshape(da, dr, da, dr)
    y = t[:, :cut, :, :cut].copy()
    for r in range(cut, dr):
        y[:, 0, :, 0] += t[:, r, :, r]
    return herm(y.reshape(da * cut, da * cut))


def embed_ref(x, da, dr, cut):
    z = np.zeros((da, dr, da, dr), dtype=complex)
    z[:, :cut, :, :cut] = x.reshape(da, cut, da, cut)
    return z.reshape(da * dr, da * dr)


def energy_and_tail(x, da, dr, cut):
    diag = np.diag(x).real.reshape(da, dr).sum(axis=0)
    return float(diag @ np.arange(dr)), float(diag[cut:].sum())


def tilted_state(rng, da, dr, decay):
    x = state(rng, da * dr, rank=rng.integers(1, da * dr + 1))
    filt = np.tile(np.exp(-decay * np.arange(dr) / 2), da)
    x = filt[:, None] * x * filt[None, :]
    return herm(x / np.trace(x).real)


def main():
    rng = np.random.default_rng(675281026)
    checks = []
    max_norm = 0.0
    max_ratio = 0.0
    max_linear_ratio = 0.0
    for case in range(240):
        da, dr = 2, int(rng.integers(3, 9))
        cut = int(rng.integers(1, dr))
        decay = float(rng.uniform(0, 4))
        excursion = float(10 ** rng.uniform(-1, 1))
        alpha = tilted_state(rng, da, dr, decay)
        beta = tilted_state(rng, da, dr, decay)
        ca = compress_ref(alpha, da, dr, cut)
        cb = compress_ref(beta, da, dr, cut)
        ea, pa = energy_and_tail(alpha, da, dr, cut)
        eb, pb = energy_and_tail(beta, da, dr, cut)
        tail = max(pa, pb)
        endpoint_error = max(norm1(alpha - embed_ref(ca, da, dr, cut)),
                             norm1(beta - embed_ref(cb, da, dr, cut)))
        assert endpoint_error <= 2 * np.sqrt(tail) + tail + 2e-10
        channels = [random_channel(rng), random_channel(rng)]
        full, low = [], []
        for ks in channels:
            gf, lf = score(apply_channel(alpha, ks, dr), apply_channel(beta, ks, dr), excursion)
            gl, ll = score(apply_channel(ca, ks, cut), apply_channel(cb, ks, cut), excursion)
            max_norm = max(max_norm, excursion * lf, excursion * ll)
            assert max(excursion * lf, excursion * ll) <= 1 + 2e-7
            assert gl <= gf + 2e-9 / excursion**2
            bound_one = (norm1(alpha - embed_ref(ca, da, dr, cut)) +
                         norm1(beta - embed_ref(cb, da, dr, cut))) / excursion**2
            assert abs(gf - gl) <= bound_one + 2e-9 / excursion**2
            full.append(gf)
            low.append(gl)
            if tail > 1e-12:
                max_linear_ratio = max(max_linear_ratio, (gf - gl) * excursion**2 / tail)
        error = abs((full[1] - full[0]) - (low[1] - low[0]))
        bound = 4 * (2 * np.sqrt(tail) + tail) / excursion**2
        assert error <= bound + 2e-9 / excursion**2
        max_ratio = max(max_ratio, error / bound if bound else 0)
        checks.append({"case": case, "reference_dimension": dr, "retained_dimension": cut,
                       "excursion": excursion, "endpoint_energy_bound": max(ea, eb),
                       "tail_bound": tail, "score_difference_error": error,
                       "proved_bound": bound})

    # Exact scalar witness of rare-sector dilution: rho=I/2 and H=diag(1,-1)/2.
    # Identity versus total erasure has score gap one. Embedding with probability p
    # at reference energy L gives gap p and energy pL. No positive p changes sign.
    diluted = []
    for level in [1, 10, 100, 1000]:
        p = 0.25 / level
        r = np.diag([0.5 * (1 - p), 0.5 * p, 0.5 * (1 - p), 0.5 * p])
        h = np.diag([0, 0.5 * p, 0, -0.5 * p])
        g, l = score(r + h, r - h)
        assert abs(g - p) < 1e-12
        diluted.append({"reference_excited_energy": level, "weight": p,
                        "mean_energy": p * level, "sld_gap": g,
                        "max_sld_eigenvalue": l})

    out = {"status": "240 floating-point diagnostics pass; ordinary proof is separate",
           "seed": 675281026, "max_scaled_sld_norm": max_norm,
           "max_observed_error_to_proved_bound": max_ratio,
           "max_observed_single_channel_loss_over_tail": max_linear_ratio,
           "linear_tail_bound": "not claimed; diagnostic ratio is not a proof",
           "rare_sector_dilution": diluted, "checks": checks}
    Path(__file__).with_name("diagnostics.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "checks"}, indent=2))


if __name__ == "__main__":
    main()
