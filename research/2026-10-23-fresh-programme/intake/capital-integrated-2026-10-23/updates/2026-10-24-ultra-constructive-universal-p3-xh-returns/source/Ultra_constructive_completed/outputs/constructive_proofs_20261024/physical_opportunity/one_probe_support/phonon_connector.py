"""Count finite midpoint-connector inertia in the optimized mass-in-mass cell."""

import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
OPTIMUM = HERE.parent / "phonon_optimum.json"
THETA = 0.5
GL_X, GL_W = np.polynomial.legendre.leggauss(240)


def bose_weight(x):
    if x < 1.0e-3:
        x2 = x * x
        return 1.0 - x2 / 12.0 + x2**2 / 240.0 - x2**3 / 6048.0
    if x > 50.0:
        return x * x * math.exp(-x)
    em1 = math.expm1(x)
    return x * x * (em1 + 1.0) / (em1 * em1)


def integral(lo, hi, theta=THETA):
    if hi <= lo:
        return 0.0
    mid = 0.5 * (lo + hi)
    half = 0.5 * (hi - lo)
    return half * sum(
        float(w) * bose_weight((mid + half * float(x)) / theta)
        for x, w in zip(GL_X, GL_W)
    )


def integral_simpson(lo, hi, theta=THETA, panels=1 << 12):
    """Composite Simpson cross-check, independent of the Gauss rule above."""
    if hi <= lo:
        return 0.0
    h = (hi - lo) / panels
    f = lambda omega: bose_weight(omega / theta)
    total = f(lo) + f(hi)
    total += 4.0 * sum(f(lo + j * h) for j in range(1, panels, 2))
    total += 2.0 * sum(f(lo + j * h) for j in range(2, panels, 2))
    return total * h / 3.0


def bands_integral_simpson(bands, theta=THETA):
    return sum(integral_simpson(lo, hi, theta) for lo, hi in bands)


def spectrum(m_backbone, delta, m_terminal, spring, intercell):
    """Return ordered q=0 and q=pi squared-frequency eigenvalues."""
    # Physical coordinates are (backbone, midpoint connector, terminal side mass).
    # Two 2k springs in series give static stiffness k.
    stiffness0 = np.array(
        [[2.0 * spring, -2.0 * spring, 0.0],
         [-2.0 * spring, 4.0 * spring, -2.0 * spring],
         [0.0, -2.0 * spring, 2.0 * spring]],
        dtype=float,
    )
    masses = np.array([m_backbone, delta, m_terminal], dtype=float)
    inv_sqrt_m = 1.0 / np.sqrt(masses)
    d0 = inv_sqrt_m[:, None] * stiffness0 * inv_sqrt_m[None, :]
    dpi = d0.copy()
    dpi[0, 0] += 4.0 * intercell
    alpha = np.linalg.eigvalsh(d0)
    beta = np.linalg.eigvalsh(dpi)
    return alpha, beta


def bands_from_endpoints(alpha, beta):
    # Rank-one interlacing: alpha_j <= beta_j <= alpha_{j+1}.
    tol = 2.0e-10
    assert abs(alpha[0]) < tol
    # Connected springs have an exact rigid-translation zero mode. Remove
    # positive eigensolver roundoff instead of treating it as a tiny gap.
    alpha[0] = 0.0
    assert alpha[0] <= beta[0] + tol
    assert beta[0] <= alpha[1] + tol
    assert alpha[1] <= beta[1] + tol
    assert beta[1] <= alpha[2] + tol
    assert alpha[2] <= beta[2] + tol
    return [(math.sqrt(max(0.0, a)), math.sqrt(max(0.0, b))) for a, b in zip(alpha, beta)]


def band_union_integral(bands, theta=THETA):
    return sum(integral(lo, hi, theta) for lo, hi in bands)


def main():
    data = json.loads(OPTIMUM.read_text())
    res = data["normalized_resources"]
    m_backbone = float(res["backbone_min_mass"])
    total_mass = float(res["total_mass"])
    side_mass = float(res["side_mass"])
    spring = float(res["internal_spring"])
    intercell = float(res["intercell_spring"])

    # The two-mass ideal optimum and rigid comparator are checked against the
    # saved parent values before connector mass is introduced.
    ideal_bands = [tuple(map(float, pair)) for pair in data["bands"]["optimal"]]
    ideal_value = band_union_integral(ideal_bands)
    rigid_cutoff = 2.0 * math.sqrt(intercell / total_mass)
    rigid_value = integral(0.0, rigid_cutoff)
    assert abs(ideal_value - float(data["bose_integrals"]["optimal"])) < 2.0e-12
    assert abs(rigid_value - float(data["bose_integrals"]["rigid"])) < 2.0e-12
    quadrature_error = max(
        abs(ideal_value - bands_integral_simpson(ideal_bands)),
        abs(rigid_value - integral_simpson(0.0, rigid_cutoff)),
    )

    print(f"theta={THETA}; m_backbone={m_backbone:.12f}, M={total_mass:.12f}, K={intercell:.12f}, k={spring:.12f}")
    print(f"ideal two-mass J={ideal_value:.12f}; rigid J={rigid_value:.12f}; rigid cutoff={rigid_cutoff:.12f}")
    print("delta/Mside  delta  terminal_mass  bands [sqrt(alpha_j),sqrt(beta_j)]  J_total  J_high_band  vs_rigid  vs_ideal")

    for frac in (0.01, 0.05, 0.10, 0.20, 0.50, 0.80):
        delta = frac * side_mass
        terminal = side_mass - delta
        assert delta > 0 and terminal > 0
        alpha, beta = spectrum(m_backbone, delta, terminal, spring, intercell)
        bands = bands_from_endpoints(alpha, beta)
        pieces = [integral(lo, hi) for lo, hi in bands]
        j3 = sum(pieces)
        quadrature_error = max(quadrature_error, abs(j3 - bands_integral_simpson(bands)))
        assert abs(m_backbone + delta + terminal - total_mass) < 2.0e-14
        btxt = " ".join(f"[{lo:.9f},{hi:.9f}]" for lo, hi in bands)
        print(f"{frac:10.2%}  {delta:.9f}  {terminal:.9f}  {btxt}  {j3:.12f}  {pieces[2]:.3e}  {j3/rigid_value:.8f}  {j3/ideal_value:.8f}")

    assert quadrature_error < 2.0e-11
    print(f"PASS: all three branches integrated; mass/interlacing checks pass; Simpson/GL max error={quadrature_error:.3e}.")


if __name__ == "__main__":
    main()
