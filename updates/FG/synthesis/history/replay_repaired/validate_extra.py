"""Negative controls for the proposed operation. These are simulations, not data."""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm


def phase_parts(U, labels):
    labels = np.asarray(labels, dtype=int)
    diff = labels[:, None] - labels[None, :]
    return {int(m): np.where(diff == m, U, 0) for m in np.unique(diff)}


def harmonic_map(K, parts, ell, q, s):
    out = np.zeros_like(K)
    for m, A in parts.items():
        n = m - ell
        if n in parts:
            out += np.exp(1j * (m + n) * q * s / 2) * A @ K @ parts[n].conj().T
    return out


s = .702
# A three-band ladder with adjacent-band dipole couplings and a finite detuning.
# Its two-photon processes violate the two-band closure hypothesis.
H = np.array([[0, 1.3, 0], [1.3, .25, 1.05], [0, 1.05, .8]], complex)
parts = phase_parts(expm(-1j * H), [0, 1, 2])
rho = np.diag([1., 0., 0.]).astype(complex)

def signal(q2):
    K = rho.copy()
    for ell, q in zip([-1, 1, 1, -1], [1, q2, 1, 1]):
        K = harmonic_map(K, parts, ell, q, s)
    return np.trace(K)

residual = signal(1) + signal(-1) - 2*np.cos(s/2)*signal(0)
assert abs(residual) > 1e-4, 'Chosen counterexample unexpectedly obeys the two-band consistency test.'

# A common (equal-history) channel conserves the ancilla coherence even if the
# molecule is driven strongly and undergoes amplitude relaxation. No recoil here.
rng = np.random.default_rng(427)
for _ in range(20):
    K = np.diag([.4, .3, .3]).astype(complex)
    for phi in rng.uniform(0, 2*np.pi, size=4):
        U = sum(np.exp(1j*m*phi)*A for m, A in parts.items())
        K = U @ K @ U.conj().T
    # Decay of both upper states into the lowest one; fully trace preserving.
    p = .8
    E0 = np.diag([1., np.sqrt(1-p), np.sqrt(1-p)])
    E1 = np.zeros((3,3)); E1[0,1] = np.sqrt(p)
    E2 = np.zeros((3,3)); E2[0,2] = np.sqrt(p)
    K = sum(E @ K @ E.conj().T for E in [E0, E1, E2])
    assert abs(np.trace(K)-1) < 1e-12

report = {
    'status': 'ideal algebraic tests; no experimental validation',
    'three_band_consistency_residual': [float(residual.real), float(residual.imag)],
    'three_band_residual_magnitude': float(abs(residual)),
    'interpretation': 'Two-band inversion does not generally extend to a three-band ladder. A zero residual is necessary in the ideal two-band model, not a sufficient proof of no leakage.',
    'equal_history_with_common_relaxation': 'passed',
    'exclusions': 'Branch-dependent recoil, state-dependent trap forces, route-dependent pulse mismatch, preparation and ancilla readout errors are not removed by the common-channel identity.'
}
Path('extra_validation_results.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
