"""Independent finite-matrix checks for the finite-interval sensing audit.

Python >=3.10; numpy/scipy. No sampling, no fitting.
"""

import json
import numpy as np
from scipy.linalg import expm

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
XI = np.kron(X, I)
ZI = np.kron(Z, I)
PE = np.diag([1, 0, 0, 1]).astype(complex)
PO = np.eye(4) - PE
RHO01 = np.zeros((4, 4), dtype=complex)
RHO01[0, 3] = 1


def instrument_exact(gamma, omega, theta, delta):
    h = omega * ZI / 2
    j = np.kron(np.cos(theta) * X + np.sin(theta) * Y, I)
    # Column-major vectorization.
    generator = -1j * (np.kron(np.eye(4), h) - np.kron(h.T, np.eye(4)))
    generator += gamma * (np.kron(j.conj(), j) - np.eye(16))
    out = (expm(delta * generator) @ RHO01.reshape(-1, order="F")).reshape((4, 4), order="F")
    even = PE @ out @ PE
    odd = XI @ PO @ out @ PO @ XI
    return even[0, 3], odd[0, 3]


def instrument_formula(gamma, omega, theta, delta):
    d = np.sqrt(complex(gamma * gamma - omega * omega))
    sh = delta if abs(d) < 1e-12 else np.sinh(d * delta) / d
    common = np.exp(-gamma * delta)
    fe = common * (np.cosh(d * delta) - 1j * omega * sh)
    fo = common * gamma * sh * np.exp(2j * theta)
    return fe, fo


def full_isometry_null(gamma, omega, theta, dt):
    p = gamma * dt
    u = expm(-1j * omega * Z * dt / 2)
    j = np.cos(theta) * X + np.sin(theta) * Y
    dj = -np.sin(theta) * X + np.cos(theta) * Y
    du = -1j * gamma * dt * Z @ u
    v = np.vstack([np.sqrt(1-p) * u, np.sqrt(p) * j @ u])
    dv = np.vstack([np.sqrt(1-p) * du, np.sqrt(p) * (dj @ u + j @ du)])
    return float(np.linalg.norm(v.conj().T @ dv)), float(np.linalg.norm(dv.conj().T @ dv - p*(1-p)*I))


def record_coherence(g1, g2, d1, d2, theta, omega, n, e1, e2):
    factors = []
    for g, dt, evens in [(g1, d1, e1), (g2, d2, e2)]:
        qe = (1 + np.exp(-2*g*dt))/2
        qo = 1 - qe
        fe, fo = instrument_exact(g, omega, theta, dt)
        factors.append((fe/qe)**evens * (fo/qo)**n)
    return factors[0].conjugate() * factors[1]


def main():
    errors = []
    for gamma in (0.3, 1.0, 2.7):
        for omega in (0.0, 0.4, 1.0, 3.5):
            for theta in (0.0, 0.37, 1.19):
                for delta in (0.08, 0.7, 2.1):
                    a = instrument_exact(gamma, omega, theta, delta)
                    b = instrument_formula(gamma, omega, theta, delta)
                    errors.append(max(abs(a[i]-b[i]) for i in (0, 1)))
    echo = [record_coherence(0.4, 1.7, 0.2, 0.3, theta, 0.6, 3, 7, 4)
            for theta in (0.0, 0.17, 0.8, 1.33)]
    echo_error = max(abs(z-echo[0]) for z in echo)
    g1, g2, d1, d2, n, e1, e2 = 0.4, 1.7, 0.2, 0.3, 3, 7, 4
    h = 1e-6
    derivative = (record_coherence(g1,g2,d1,d2,.71,h,n,e1,e2)
                  - record_coherence(g1,g2,d1,d2,.71,-h,n,e1,e2))/(2*h)
    b = e2*np.tanh(g2*d2)/g2 - e1*np.tanh(g1*d1)/g1
    null_errors = full_isometry_null(0.7, 0.43, 0.87, 0.031)
    report = {
        "finite_interval_cases": len(errors),
        "max_exact_liouvillian_vs_formula_error": float(max(errors)),
        "theta_echo_max_change": float(echo_error),
        "local_derivative_error": float(abs(derivative+1j*b)),
        "full_bath_null_beta_error": null_errors[0],
        "full_bath_null_alpha_error": null_errors[1],
    }
    report["passed"] = max(v for k,v in report.items() if k not in ("finite_interval_cases",)) < 1e-8
    print(json.dumps(report, indent=2))
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
