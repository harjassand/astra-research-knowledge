"""Complex passband transfer for a 50-ohm line with shorted quarter-wave stubs.

This is a lossless single-TEM transmission-line circuit model.  It charges each
line section's distributed C and L, but treats the T junction as an ideal
shunt node and does not model conductor loss or 3-D junction parasitics.
Requires NumPy.
"""

from __future__ import annotations

import math
import numpy as np


Z_PORT = 50.0
Z_STUB = 60.0
F_C = 6.0e9
HALF_BAND = 100.0e6
TAU_MAIN = 95.6302e-12
TAU_Q = 1.0 / (4.0 * F_C)
C_BUDGET = 5.73781e-12
L_BUDGET = 33.8362e-9


def _line(f: np.ndarray, delay: float, z: float) -> np.ndarray:
    """ABCD matrix of a lossless matched TEM line, e^(+i omega t) convention."""
    phase = 2.0 * np.pi * f * delay
    c, s = np.cos(phase), np.sin(phase)
    out = np.zeros((f.size, 2, 2), dtype=complex)
    out[:, 0, 0] = out[:, 1, 1] = c
    out[:, 0, 1] = 1j * z * s
    out[:, 1, 0] = 1j * s / z
    return out


def _stub(f: np.ndarray) -> np.ndarray:
    """ABCD of a shorted shunt stub: C=Y_in, Y_in=-i*cot(omega*tau_q)/Zs."""
    phase = 2.0 * np.pi * f * TAU_Q
    y = -1j / Z_STUB / np.tan(phase)
    out = np.zeros((f.size, 2, 2), dtype=complex)
    out[:, 0, 0] = out[:, 1, 1] = 1.0
    out[:, 1, 0] = y
    return out


def _matmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.einsum("nij,njk->nik", a, b)


def transfer(nstub: int, f: np.ndarray) -> np.ndarray:
    """S21 for half-feed, N stubs, quarter-wave spacers, half-feed."""
    if nstub not in (1, 2, 3):
        raise ValueError("nstub must be 1, 2, or 3")
    total = _line(f, TAU_MAIN / 2.0, Z_PORT)
    stub = _stub(f)
    spacer = _line(f, TAU_Q, Z_PORT)
    for j in range(nstub):
        total = _matmul(total, stub)
        if j + 1 < nstub:
            total = _matmul(total, spacer)
    total = _matmul(total, _line(f, TAU_MAIN / 2.0, Z_PORT))
    denominator = (total[:, 0, 0] + total[:, 0, 1] / Z_PORT
                   + total[:, 1, 0] * Z_PORT + total[:, 1, 1])
    return 2.0 / denominator


def analytic_transfer(nstub: int, f: np.ndarray) -> np.ndarray:
    """Closed forms after removing the fixed main-feed phase."""
    q = Z_PORT / Z_STUB
    delta = (np.pi / 2.0) * (f - F_C) / F_C
    t = np.tan(delta)
    if nstub == 1:
        d = 2.0 + 1j * q * t
    elif nstub == 2:
        s = np.cos(delta)
        d = s * (-2.0 * (1.0 + q) * t
                 + 1j * (2.0 - q * (q + 2.0) * t * t))
    elif nstub == 3:
        d = -((1.0 + 1j * (1.0 + q) * t)
              * (2.0 - q * (q + 3.0) * t * t
                 + 1j * (q + 2.0) * t)) / (1.0 + t * t)
    else:
        raise ValueError("nstub must be 1, 2, or 3")
    # D already includes the center phase of every inter-stub line.
    return np.exp(-2j * np.pi * f * TAU_MAIN) * 2.0 / d


def fit_delay(nstub: int) -> tuple[float, float]:
    """Carrier phase and exact phase-tangent group delay."""
    q = Z_PORT / Z_STUB
    slope_coeff = {
        1: q / 2.0,
        2: 1.0 + q,
        3: (4.0 + 3.0 * q) / 2.0,
    }[nstub]
    phase = (-2.0 * np.pi * F_C * TAU_MAIN
             - (nstub - 1) * np.pi / 2.0)
    delay = TAU_MAIN + slope_coeff * TAU_Q
    return phase, delay


def analytic_error_bound(nstub: int) -> tuple[float, float, float]:
    """Whole-band lower power and upper complex-error bounds.

    The error is relative to the single phase/group-delay tangent at 6 GHz.
    Bounds use |atan(x)-x| <= |x|^3/3 and tan(d)-d >= 0 for d >= 0.
    """
    q = Z_PORT / Z_STUB
    d = (np.pi / 2.0) * HALF_BAND / F_C
    t = math.tan(d)
    if nstub == 1:
        eps = q * q * t * t / 4.0
        a = q / 2.0
        phase_rem = a * (t - d) + (a * t) ** 3 / 3.0
    elif nstub == 2:
        A = q * (q + 2.0)
        eps = A * A * t ** 4 / 4.0  # drop a denominator >= 1
        a = 1.0 + q
        h = A / 2.0
        v = a * t / (1.0 - h * t * t)
        phase_rem = (a * (t - d)
                     + a * t * (h * t * t) / (1.0 - h * t * t)
                     + v ** 3 / 3.0)
    elif nstub == 3:
        eps = q * q * t * t / 4.0
        a1 = 1.0 + q
        a2 = (q + 2.0) / 2.0
        h = q * (q + 3.0) / 2.0
        v2 = a2 * t / (1.0 - h * t * t)
        phase_rem = (a1 * (t - d) + (a1 * t) ** 3 / 3.0
                     + a2 * (t - d)
                     + a2 * t * (h * t * t) / (1.0 - h * t * t)
                     + v2 ** 3 / 3.0)
    else:
        raise ValueError("nstub must be 1, 2, or 3")
    power_floor = 1.0 / (1.0 + eps)
    amplitude_defect = 1.0 - 1.0 / math.sqrt(1.0 + eps)
    complex_error = amplitude_defect + phase_rem
    return power_floor, phase_rem, complex_error


def resources(nstub: int) -> tuple[float, float, float, float]:
    """Total line C, L, main-path delay, and all-segment delay."""
    c = (TAU_MAIN / Z_PORT + (nstub - 1) * TAU_Q / Z_PORT
         + nstub * TAU_Q / Z_STUB)
    ell = (Z_PORT * TAU_MAIN + (nstub - 1) * Z_PORT * TAU_Q
           + nstub * Z_STUB * TAU_Q)
    main_path = TAU_MAIN + (nstub - 1) * TAU_Q
    all_line_delays = main_path + nstub * TAU_Q
    return c, ell, main_path, all_line_delays


def main() -> None:
    f = np.linspace(F_C - HALF_BAND, F_C + HALF_BAND, 20001)
    omega = 2.0 * np.pi * f
    omega_c = 2.0 * np.pi * F_C
    q = Z_PORT / Z_STUB
    print(f"port={Z_PORT:g} ohm, stub={Z_STUB:g} ohm, q={q:.12g}")
    print(f"center={F_C/1e9:g} GHz, half-band={HALF_BAND/1e6:g} MHz, "
          f"quarterwave delay={TAU_Q*1e12:.9f} ps")
    print("N  C[pF]  L[nH]  path-delay[ps]  all-line-delay[ps]  "
          "center-fit-delay[ps]  sampled-min-power  sampled-error  "
          "analytic-power-floor  analytic-error-bound")
    for n in (1, 2, 3):
        s21 = transfer(n, f)
        s21_closed = analytic_transfer(n, f)
        if not np.allclose(s21, s21_closed, rtol=2e-12, atol=2e-12):
            raise AssertionError(f"ABCD and closed form disagree for N={n}")
        phase_c, delay = fit_delay(n)
        error = np.max(np.abs(np.exp(1j * (omega - omega_c) * delay) * s21
                              - np.exp(1j * phase_c)))
        power = np.abs(s21) ** 2
        c, ell, path, all_delay = resources(n)
        p_floor, _, e_bound = analytic_error_bound(n)
        print(f"{n}  {c*1e12:.9f}  {ell*1e9:.9f}  {path*1e12:.9f}  "
              f"{all_delay*1e12:.9f}  {delay*1e12:.9f}  {power.min():.12f}  "
              f"{error:.12g}  {p_floor:.12f}  {e_bound:.12g}")
    print(f"budgets: C={C_BUDGET*1e12:.5f} pF, L={L_BUDGET*1e9:.5f} nH")


if __name__ == "__main__":
    main()
