"""Independent floating-point residue identity check for a two-mode plant."""
import json
from pathlib import Path

import numpy as np


OUT = Path(__file__).resolve().parent
theta = 0.37
U = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta), np.cos(theta)]])
lam = np.array([1.0, 2.25])
gamma = 0.35
alpha = np.array([0.23, 0.41])
K = (U * lam) @ U.T
a = U[0, :]
s, t = 0.8j, 0.6j
c = (s - t) / 2


def q(z):
    return np.linalg.solve((z * z + gamma * z) * np.eye(2) + K, np.array([1.0, 0.0]))


def F(R):
    return np.sum(alpha * q(s) * q(t) * q(R + c) * q(-R + c))


omega = np.sqrt(lam - gamma**2 / 4)
p = np.r_[-gamma / 2 + 1j * omega, -gamma / 2 - 1j * omega]
z = np.r_[p - c, c - p]
nu = np.array([0.43, 0.71, 1.13, 1.57, 2.02, 2.49, 2.93, 3.41])
R = 1j * nu
C = 1 / (R[:, None] - z[None, :])
f = np.array([F(r) for r in R])
residues = np.linalg.solve(C, f)
c4 = np.sum(residues * z**3)
c8 = np.sum(residues * z**7)

d = 2 * c + gamma
e = c * c + gamma * c
m1 = np.dot(a**2, lam)
m2 = np.dot(a**2, lam**2)
p8 = d**4 - 4 * d**2 * (e + m1) + 3 * e**2 + 6 * m1 * e + m1**2 + 2 * m2
B_residue = c8 - p8 * c4
k = K[:, 0]
B_direct = alpha[1] * k[1] ** 2 * q(s)[1] * q(t)[1]

result = {
    "disclosure": __doc__.strip(),
    "n": 2,
    "number_of_port_H3_samples": len(R),
    "c4_from_residues": [c4.real, c4.imag],
    "c8_minus_p8_c4": [B_residue.real, B_residue.imag],
    "direct_hidden_contraction": [B_direct.real, B_direct.imag],
    "absolute_residue_identity_error": float(abs(B_residue - B_direct)),
    "Cauchy_condition_number": float(np.linalg.cond(C)),
    "sample_R_are_pure_imaginary": bool(np.allclose(R.real, 0)),
}
(OUT / "residue_identity_results.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
