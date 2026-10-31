"""Exact finite-contact checks of the complete-record isolation estimate.

This computes Choi trace distances (diagnostics, not diamond-norm estimates)
for the recorded instruments and verifies that the proved upper bound exceeds
them. No Monte Carlo source sampling or white-noise contact approximation.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parent
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1., -1.]).astype(complex)


def kraus(ham, duration=1.0):
    unitary = expm(-1j * duration * ham)
    sysdim = unitary.shape[0] // 2
    u = unitary.reshape(sysdim, 2, sysdim, 2)
    return [u[:, j, :, 0] for j in range(2)]


def trace_norm_herm(a):
    return float(np.abs(np.linalg.eigvalsh((a + a.conj().T) / 2)).sum())


def choi_vector(k):
    return k.reshape(-1, order="F") / np.sqrt(k.shape[0])


def test_case(omega, hopping, steps):
    dim = 6
    theta = np.array([np.pi / 12, np.pi / 4, 5 * np.pi / 12])
    nuisance = .025
    p_lo = np.maximum(0, np.sin(theta) - nuisance) ** 2
    p_hi = np.minimum(1, (np.sin(theta) + nuisance) ** 2)
    affinities = []
    for p in range(3):
        for q in range(p + 1, 3):
            assert p_hi[p] < p_lo[q]
            affinities.append(np.sqrt(p_hi[p] * p_lo[q])
                              + np.sqrt((1 - p_hi[p]) * (1 - p_lo[q])))
    c = max(affinities)
    ham0 = np.zeros((12, 12), complex)
    for q in range(3):
        he = omega * Z / 2 + (.12 + .03 * q) * X
        b = nuisance * (np.cos(q) * Z + np.sin(q) * Y)
        block = np.kron(he, I2) + np.kron(theta[q] * I2 + b, X)
        ham0[4*q:4*q+4, 4*q:4*q+4] = block
    gain = hopping * (I2 + .2 * X) / 1.2
    voff = np.zeros((dim, dim), complex)
    for q in [0, 2]:
        voff[2:4, 2*q:2*q+2] = np.sqrt(2) * gain
        voff[2*q:2*q+2, 2:4] = np.sqrt(2) * gain
    v = 4 * np.sqrt(2) * hopping
    s = v
    rem = np.expm1(s) - s
    aa = np.expm1(s)
    eta = c + aa
    assert eta < 1
    bound = .5 * (2 * eta**steps + 3*aa/(1-eta)
                    + steps * (rem + aa*aa/(1-eta)))
    actual = kraus(ham0 + np.kron(voff, I2))
    ideal = kraus(ham0)
    completeness = max(np.linalg.norm(sum(k.conj().T @ k for k in ks)-np.eye(dim), 2)
                       for ks in [actual, ideal])
    records = [(np.eye(dim, dtype=complex), np.eye(dim, dtype=complex))]
    for _ in range(steps):
        records = [(actual[j] @ ka, ideal[j] @ ki)
                   for ka, ki in records for j in range(2)]
    projectors = [np.diag(np.repeat(np.eye(3)[q], 2)).astype(complex) for q in range(3)]
    distance = 0.
    for ka, ki in records:
        va = choi_vector(ka)
        difference = np.outer(va, va.conj())
        for pq in projectors:
            vi = choi_vector(ki @ pq)
            difference -= np.outer(vi, vi.conj())
        distance += .5 * trace_norm_herm(difference)
    assert distance <= bound + 1e-9
    return dict(source_speed=omega, off_hopping=hopping, steps=steps,
                records=len(records), max_affinity=c,
                instrument_choi_trace_distance=distance,
                proved_half_diamond_upper_bound=bound,
                completeness_error=float(completeness))


def main():
    cases = [test_case(om, h, n)
             for om in [0., 5., 500., 10000.]
             for h in [0., .0005, .002]
             for n in [1, 4, 8]]
    # Phase-only count backaction: every record preserves coherence magnitude.
    # An unconditional dephasing formula would incorrectly claim contraction.
    p = .3
    kk = [np.sqrt(1-p)*np.eye(2), np.sqrt(p)*np.diag([1., -1.])]
    off = np.array([[0., 1.], [0., 0.]], complex)
    record_norm = sum(np.linalg.svd(k @ off @ k.conj().T, compute_uv=False).sum() for k in kk)
    uncond_norm = np.linalg.svd(sum(k @ off @ k.conj().T for k in kk), compute_uv=False).sum()
    assert abs(record_norm-1) < 1e-14
    assert abs(uncond_norm-.4) < 1e-14
    result = dict(description="Exact complete recorded finite-contact Choi checks; proofs are in RECORD_ASSISTED_ISOLATION.txt.",
                  cases=cases,
                  opposite_phase_counterexample=dict(recorded_offdiagonal_norm=float(record_norm),
                                                       unconditional_offdiagonal_norm=float(uncond_norm)),
                  max_completeness_error=max(x['completeness_error'] for x in cases))
    (ROOT / "record_isolation_results.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(dict(cases=len(cases), max_completeness_error=result['max_completeness_error'],
                          maximum_diagnostic_to_bound_ratio=max(x['instrument_choi_trace_distance']/x['proved_half_diamond_upper_bound'] for x in cases)), indent=2))


if __name__ == "__main__":
    main()
