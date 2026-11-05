"""Exact and numerical audit for the fixed mechanical thermal-port model.

Run: python next4_physical/audit.py
No simulation or statistical tolerance stands in for an exact identity.
"""
from pathlib import Path
import json
import numpy as np
import sympy as sp
from scipy.linalg import expm, solve_continuous_lyapunov
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parent
s = sp.symbols("s", real=True)
A = sp.diag(1, 3)
c = sp.Matrix([1, 1]) / sp.sqrt(2)
v = sp.Matrix([1, -1]) / sp.sqrt(2)
Sigma = A.inv() + s * v * v.T
D = (A * Sigma + Sigma * A) / 2
Q = (A * Sigma - Sigma * A) / 2
zero = sp.zeros(2)

assert sp.simplify(A * Sigma + Sigma * A - 2 * D) == zero
assert sp.simplify(Sigma * c - A.inv() * c) == sp.zeros(2, 1)
assert sp.simplify((c.T * D * c)[0]) == 1
assert sp.simplify(sp.Matrix.hstack(c, A*c).det()) == 1
assert sp.simplify(sp.Matrix.vstack(c.T, c.T*A).det()) == 1
entropy = sp.factor(sp.trace(Sigma.inv() * Q.T * D.inv() * Q))
target = s**2 / (1 + 2*s - s**2/4)
assert sp.simplify(entropy - target) == 0
Tc = 1 + s * (1 - sp.sqrt(5)/2)
Th = 1 + s * (1 + sp.sqrt(5)/2)
heat = s / sp.sqrt(5)
assert sp.simplify(heat*(1/Tc - 1/Th) - entropy) == 0

theta = 0.5 * np.arctan2(2.0, 1.0)
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta), np.cos(theta)]])
An = np.diag([1.0, 3.0])
cn = np.array([1.0, 1.0]) / np.sqrt(2)
vn = np.array([1.0, -1.0]) / np.sqrt(2)
K = R.T @ An @ R
b = R.T @ cn
rows = []
for sn in (0.0, 1.0, 4.0, 8.0):
    S = np.linalg.inv(An) + sn * np.outer(vn, vn)
    Dn = (An @ S + S @ An)/2
    assert np.linalg.eigvalsh(Dn)[0] > 0
    solved = solve_continuous_lyapunov(An, 2*Dn)
    assert np.max(np.abs(solved-S)) < 1e-13
    T = np.diag(R.T @ Dn @ R)
    offdiag = R.T @ Dn @ R - np.diag(T)
    assert np.max(np.abs(offdiag)) < 1e-13
    Sq = R.T @ S @ R
    heat_in = T*np.diag(K) - np.diag(K @ Sq @ K)
    J = sn/np.sqrt(5)
    assert np.max(np.abs(heat_in - [-J,J])) < 1e-12
    sigma_heat = -np.sum(heat_in/T)
    Qn = (An @ S - S @ An)/2
    sigma_current = np.trace(np.linalg.inv(S) @ Qn.T @ np.linalg.inv(Dn) @ Qn)
    expected = sn**2/(1+2*sn-sn**2/4)
    assert abs(sigma_heat - expected) < 1e-10
    assert abs(sigma_current - expected) < 1e-10
    cov_error = max(abs(cn @ expm(-An*t) @ S @ cn
                        -.5*(np.exp(-t)+np.exp(-3*t)/3))
                    for t in np.linspace(0, 10, 101))
    assert cov_error < 1e-13
    tr = np.log(3)/2
    reset_cov = S - expm(-An*tr) @ S @ expm(-An*tr)
    reset_variance = cn @ reset_cov @ cn
    assert abs(reset_variance - (40/81 - sn/27)) < 1e-13
    rows.append(dict(s=sn, temperatures=T.tolist(),
                     minimum_diffusion_eigenvalue=float(np.linalg.eigvalsh(Dn)[0]),
                     heat_into_cold=float(heat_in[0]),
                     heat_into_hot=float(heat_in[1]),
                     entropy_current=float(sigma_current),
                     entropy_heat=float(sigma_heat),
                     scalar_covariance_max_error=float(cov_error),
                     known_full_reset_variance_at_log3_over2=float(reset_variance)))

# Smooth finite-slew cyclic forcing, independently integrate mean and variance.
# State per lambda: z, w, direct_mean, energy_integral, covariance_variance.
F, duration = 0.7, 2.0
def drive(t):
    return F*np.sin(np.pi*t/duration)**2
def slew(t):
    return F*np.pi/duration*np.sin(2*np.pi*t/duration)
def rhs(t, state):
    result = []
    for j, lam in enumerate((1., 3.)):
        z, w, mdirect, energy, variance = state[5*j:5*j+5]
        u, du = drive(t), slew(t)
        dz = -lam*z+u
        result.extend([dz, -lam*w+du, -.5*du*z,
                       .5*dz**2, du*w/lam])
    return result
sol = solve_ivp(rhs, (0, duration), np.zeros(10), rtol=2e-12, atol=2e-14)
assert sol.success
workrows = []
for j, lam in enumerate((1., 3.)):
    z, w, direct, energy, variance = sol.y[5*j:5*j+5, -1]
    positive_form = energy + lam*z*z/4
    assert abs(direct-positive_form) < 1e-11
    assert abs(variance-2*direct) < 1e-11
    assert direct > 0
    workrows.append(dict(rate=lam, mean_direct=float(direct),
                         mean_positive_form=float(positive_form),
                         variance_covariance_integral=float(variance)))
mean = sum(r["mean_direct"] for r in workrows)
variance = sum(r["variance_covariance_integral"] for r in workrows)
assert abs(np.exp(-mean+.5*variance)-1) < 1e-11

output = {
    "status": "all exact identities and numerical checks passed",
    "corpus_revision": "fef3640a8b1dc5475674a006de417f652f3baf3c",
    "scope": "mathematical model audit, not laboratory validation or novelty certification",
    "exact_entropy_expression": str(entropy),
    "fixed_spring_matrix": K.tolist(),
    "fixed_mechanical_port": b.tolist(),
    "models": rows,
    "smooth_work_protocol": {
        "peak_force": F, "duration": duration,
        "maximum_slew": F*np.pi/duration,
        "modes": workrows, "mean": mean, "variance": variance,
        "exponential_work_expectation": float(np.exp(-mean+.5*variance))
    }
}
(ROOT/"audit_results.json").write_text(json.dumps(output, indent=2)+"\n")
print(json.dumps(output, indent=2))
