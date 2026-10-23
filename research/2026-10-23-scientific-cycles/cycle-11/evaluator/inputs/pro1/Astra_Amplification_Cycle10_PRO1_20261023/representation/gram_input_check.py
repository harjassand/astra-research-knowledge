"""Bounded check of the new actual input; not an all-length proof or code compiler.

The original token construction of 2H is copied unchanged in inherited_h_operator.py.
All color-count sectors are included, with their exact sigma weights.
"""
from pathlib import Path
import argparse, hashlib, json, math, resource, time
import numpy as np
from inherited_h_operator import matrix


def check(k):
    ell = math.log(2)
    gamma = ell / 4
    b = 1 / (256 * k)
    r = b * k
    sectors = []
    v = 0.0
    dim = 0
    for n0 in range(k + 1):
        q = k - n0
        for n1 in range(q + 1):
            hh, words = matrix(k, n0, n1)
            h = hh.toarray() / 2
            sw = 2.0 ** (-k - q)
            v += sw * np.sum(h * h.T)
            sectors.append((q, h, words, sw))
            dim += len(words)
    assert dim == 3 ** k
    m = 3 * ell * v / 32
    trace = charge = entropy = repair2 = x2 = y2 = chi2 = 0.0
    min_eig = 1.0
    max_pinching = max_noncommutation = 0.0
    rank = 0
    for q, h, words, sw in sectors:
        d = len(words)
        eye = np.eye(d)
        x = -gamma * b * h
        c = eye + x / 2
        c2 = c @ c
        patterns = [tuple(int(a != 0) for a in w) for w in words]
        same = np.array([[u == v for v in patterns] for u in patterns])
        normalizer = c2 * same
        ev, vec = np.linalg.eigh(normalizer)
        assert np.min(ev) > 0
        invsqrt = (vec * (ev ** -0.5)) @ vec.T
        f = invsqrt @ c2 @ invsqrt
        tilt = 1 + (4 * m / k) * b * b * (q - k / 2)
        assert tilt > 0
        rho_eigs = sw * tilt * np.linalg.eigvalsh(f)
        assert np.min(rho_eigs) >= -1e-14
        min_eig = min(min_eig, float(np.min(rho_eigs)))
        rank += int(np.sum(rho_eigs > 1e-14))
        positive = rho_eigs[rho_eigs > 0]
        entropy -= float(np.sum(positive * np.log2(positive)))
        trace += sw * tilt * np.trace(f)
        charge += sw * tilt * (q - k / 2) * np.trace(f)
        repair = f - eye - x
        y = tilt * (f - eye) - x
        repair2 += sw * np.sum(repair * repair.T)
        x2 += sw * np.sum(x * x.T)
        y2 += sw * np.sum(y * y.T)
        z = tilt * f - eye
        chi2 += sw * np.sum(z * z.T)
        max_pinching = max(max_pinching, float(np.max(np.abs(f * same - eye))))
        max_noncommutation = max(max_noncommutation, float(np.linalg.norm(normalizer @ h - h @ normalizer, ord='fro')))
    budget = ell * v * b * b
    assert abs(trace - 1) < 2e-12
    assert abs(charge - m * b * b) < 2e-12
    assert max_pinching < 2e-12
    assert math.sqrt(repair2) <= 3 * gamma * gamma * r * r + 2e-13
    assert math.sqrt(y2) <= 4 * gamma * gamma * r * r + 2e-13
    assert entropy - 1.5 * k >= budget / 64 - 2e-12
    assert entropy - 1.5 * k >= charge - chi2 / ell - 2e-12
    # Analytic operator lower margin, not numerical evaluation of the full bath map.
    a = 1 - b
    margin = a * budget * (1 / 16 - 2 * r) - 2 * r * math.sqrt(y2)
    assert margin >= a * budget / 128
    return dict(k=k, b=b, beta=math.sqrt(b), r=r, dimension=dim,
                numeric_rank=rank, v=v, trace=trace, charge=charge,
                target_charge=m*b*b, entropy=entropy,
                entropy_excess=entropy-1.5*k, proved_entropy_floor=budget/64,
                repair_weighted_l2=math.sqrt(repair2),
                offdiagonal_correction_l2=math.sqrt(y2),
                charge_pinching_error=max_pinching,
                normalizer_h_commutator_frobenius=max_noncommutation,
                analytic_drift_margin=margin, required_drift= a*budget/128,
                minimum_density_eigenvalue=min_eig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--kmax', type=int, default=7)
    args = parser.parse_args()
    assert 4 <= args.kmax <= 8
    start = time.perf_counter()
    rows = [check(k) for k in range(4, args.kmax + 1)]
    result = dict(status='PASS', rows=rows, wall_seconds=time.perf_counter()-start,
                  peak_rss_kib_linux=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  inherited_h_code_sha256=hashlib.sha256(Path(__file__).with_name('inherited_h_operator.py').read_bytes()).hexdigest(),
                  scope='Floating diagnostics of actual small input matrices and analytic margins; no finite check proves the all-length theorem, evaluates capacity, or compiles a code.')
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
