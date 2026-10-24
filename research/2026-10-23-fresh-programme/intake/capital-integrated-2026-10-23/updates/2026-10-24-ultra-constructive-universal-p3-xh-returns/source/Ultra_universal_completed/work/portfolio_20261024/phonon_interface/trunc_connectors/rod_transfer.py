"""Full longitudinal-rod transfer check for a counted intercell connector.

The scalar continuum rod is exact within the declared 1D model.  NumPy is the
only dependency.  The script reports (i) ideal-matched-lead passband integrals
and (ii) a separate N-cell finite segment between identical bare-rod leads.
It does not write files or claim a 3D material result.
"""

from __future__ import annotations

import math
import numpy as np


# Dimensionless optimum copied from PHONON_OPTIMUM.md.
ROOT = 4.259874009292292484341159056875
KAPPA = (ROOT * ROOT - 3.0) / 4.0
MASS = 4.0 - 12.0 / (ROOT * ROOT)
SIDE0 = MASS - 1.0
KINT = 4.0 * SIDE0 / MASS
THETA = 0.5
OMEGA_CUT = 20.0
GL_X, GL_W = np.polynomial.legendre.leggauss(256)


def bose_weight(w: float | np.ndarray) -> float | np.ndarray:
    """The dimensionless theta=1/2 weight (w/sinh(w))^2."""
    x = np.asarray(w, dtype=float)
    out = np.ones_like(x)
    nz = x != 0.0
    out[nz] = (x[nz] / np.sinh(x[nz])) ** 2
    return float(out) if out.ndim == 0 else out


def parameters(a_m: float, c_l: float = 5000.0) -> tuple[float, float, float]:
    """Return r=omega_u*a/c, rod mass ratio mu, and remaining side mass."""
    omega_u = 2.0 * math.pi * 1.0e9
    r = omega_u * a_m / c_l
    mu = KAPPA * r * r
    side = SIDE0 - mu
    if side <= 0.0:
        raise ValueError("counted rod mass leaves no positive side mass")
    return r, mu, side


def delta(w: float | np.ndarray, r: float, mu: float, mode: str) -> float | np.ndarray:
    """Half-trace of the exact unit-cell transfer, dimensionless frequency."""
    x = np.asarray(w, dtype=float)
    th = r * x
    sinc = np.ones_like(x)
    nz = th != 0.0
    sinc[nz] = np.sin(th[nz]) / th[nz]
    if mode == "resonator":
        side = SIDE0 - mu
        den = KINT - side * x * x
        with np.errstate(divide="ignore", invalid="ignore"):
            meff = 1.0 + KINT * side / den
    elif mode == "rigid":
        meff = np.full_like(x, MASS - mu)
    else:
        raise ValueError(mode)
    out = np.cos(th) - (x * x / (2.0 * KAPPA)) * meff * sinc
    return float(out) if out.ndim == 0 else out


def bisect_edge(mode: str, r: float, mu: float, edge: int,
                lo: float, hi: float) -> float:
    """Bisection on a sign-changing bracket for delta(w)-edge."""
    f_lo = float(delta(lo, r, mu, mode)) - edge
    f_hi = float(delta(hi, r, mu, mode)) - edge
    if f_lo == 0.0:
        return lo
    if f_hi == 0.0:
        return hi
    if f_lo * f_hi > 0.0:
        raise ValueError("root bracket does not change sign")
    for _ in range(72):
        mid = 0.5 * (lo + hi)
        f_mid = float(delta(mid, r, mu, mode)) - edge
        if f_lo * f_mid <= 0.0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return 0.5 * (lo + hi)


def bands_below_cutoff(r: float, mu: float, mode: str,
                       cutoff: float = OMEGA_CUT) -> list[tuple[float, float]]:
    """Bracket all threshold crossings on a dense, pole-split finite window.

    This is a numerical root isolation diagnostic for the displayed fixture,
    not the global dual proof.  The Bose tail beyond `cutoff` is bounded
    analytically in the note.
    """
    breaks = [0.0, cutoff]
    if mode == "resonator":
        side = SIDE0 - mu
        pole = math.sqrt(KINT / side)
        if 0.0 < pole < cutoff:
            breaks.insert(1, pole)
    roots: list[float] = []
    mesh_per_segment = 50000
    for edge in (-1, 1):
        f = lambda x: float(delta(x, r, mu, mode)) - edge
        for left, right in zip(breaks[:-1], breaks[1:]):
            eps = 1.0e-10 * max(1.0, right - left)
            lo = left + (eps if left > 0.0 else 1.0e-12)
            hi = right - eps
            grid = np.linspace(lo, hi, mesh_per_segment + 1)
            vals = np.asarray(delta(grid, r, mu, mode)) - edge
            for j in range(mesh_per_segment):
                va, vb = vals[j], vals[j + 1]
                if np.isfinite(va) and np.isfinite(vb) and va * vb < 0.0:
                    roots.append(bisect_edge(mode, r, mu, edge,
                                             float(grid[j]), float(grid[j + 1])))
    # ω=0 is the acoustic endpoint Δ(0)=1, not found by open-interval scans.
    cuts = [0.0, cutoff] + breaks[1:-1] + roots
    cuts = sorted(cuts)
    uniq: list[float] = []
    for x in cuts:
        if not uniq or abs(x - uniq[-1]) > 2.0e-9:
            uniq.append(x)
    bands: list[tuple[float, float]] = []
    for left, right in zip(uniq[:-1], uniq[1:]):
        if right - left <= 1.0e-9:
            continue
        mid = 0.5 * (left + right)
        val = float(delta(mid, r, mu, mode))
        if abs(val) < 1.0:
            bands.append((left, right))
    return bands


def integrate_bands(bands: list[tuple[float, float]]) -> tuple[float, list[float]]:
    pieces = []
    for lo, hi in bands:
        mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
        pieces.append(half * sum(float(w) * float(bose_weight(mid + half * float(x)))
                                 for x, w in zip(GL_X, GL_W)))
    return sum(pieces), pieces


def matmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.einsum("...ij,...jk->...ik", a, b)


def finite_segment_transmission(w: np.ndarray, r: float, mu: float,
                                mode: str, cells: int) -> np.ndarray:
    """Exact transfer transmission for N cells between bare, same-material rods.

    State is (u, N/(EA*kappa)); the segment has N point modules and total rod
    length N*a, with half-rod end pieces.  The outer leads are uniform rods of
    the same E, rho, A.  Thus the sample mass is exactly N times its bulk cell
    mass, including all distributed rod inertia.
    """
    x = np.asarray(w, dtype=float)
    th = r * x
    if mode == "resonator":
        side = SIDE0 - mu
        with np.errstate(divide="ignore", invalid="ignore"):
            meff = 1.0 + KINT * side / (KINT - side * x * x)
    elif mode == "rigid":
        meff = np.full_like(x, MASS - mu)
    else:
        raise ValueError(mode)
    b = np.zeros_like(x)
    nz = th != 0.0
    b[nz] = meff[nz] * x[nz] ** 2 / (KAPPA * th[nz])
    co, si = np.cos(th), np.sin(th)
    cell = np.empty(x.shape + (2, 2), dtype=float)
    cell[..., 0, 0] = co - si * b
    cell[..., 0, 1] = si
    cell[..., 1, 0] = -si - co * b
    cell[..., 1, 1] = co
    half = np.empty_like(cell)
    ch, sh = np.cos(th / 2.0), np.sin(th / 2.0)
    half[..., 0, 0], half[..., 0, 1] = ch, sh
    half[..., 1, 0], half[..., 1, 1] = -sh, ch
    point = np.zeros_like(cell)
    point[..., 0, 0], point[..., 1, 1] = 1.0, 1.0
    point[..., 1, 0] = -b

    # cell=Trod(a)*Ppoint.  For N>=2, Cayley-Hamilton gives
    # cell^(N-1)=U_(N-2)(Delta)cell-U_(N-3)(Delta)I.
    if cells == 1:
        power = np.broadcast_to(np.eye(2), cell.shape)
    else:
        d = 0.5 * (cell[..., 0, 0] + cell[..., 1, 1])
        m = cells - 1
        u_prev = np.zeros_like(d)  # U_-1
        u_curr = np.ones_like(d)   # U_0
        u_vals = [u_curr]
        for _ in range(1, m):
            u_prev, u_curr = u_curr, 2.0 * d * u_curr - u_prev
            u_vals.append(u_curr)
        u_m1 = u_vals[m - 1]
        u_m2 = u_vals[m - 2] if m >= 2 else np.zeros_like(d)
        power = u_m1[..., None, None] * cell
        power[..., 0, 0] -= u_m2
        power[..., 1, 1] -= u_m2

    # Half rod, first point module, repeated interior rod+module, half rod.
    total = matmul(matmul(matmul(half, point), power), half)
    s22 = 0.5 * (total[..., 0, 0] + total[..., 1, 1]) \
        + 0.5j * (total[..., 1, 0] - total[..., 0, 1])
    return 1.0 / (s22.real * s22.real + s22.imag * s22.imag)


def finite_landauer(mode: str, r: float, mu: float,
                    cells: int = 10, panels: int = 500000) -> float:
    """Composite-Simpson finite-sample integral on [0,20]."""
    x = np.linspace(0.0, OMEGA_CUT, panels + 1)
    # The selected resonance is not a mesh node; physical transmission tends
    # to zero at the exact undamped side-mass pole.
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        tau = finite_segment_transmission(x, r, mu, mode, cells)
    tau = np.nan_to_num(tau, nan=0.0, posinf=0.0, neginf=0.0)
    vals = bose_weight(x) * tau
    weights = np.ones(panels + 1)
    weights[1:-1:2] = 4.0
    weights[2:-1:2] = 2.0
    return (OMEGA_CUT / panels / 3.0) * float(np.dot(weights, vals))


def main() -> None:
    # Illustrative 1D continuum parameter choice.  E and rho are not claimed
    # as sourced properties of a named material.
    E, rho = 125.0e9, 5000.0
    area, length = (30.0e-9) ** 2, 300.0e-9
    c_l = math.sqrt(E / rho)
    r, mu, side = parameters(length, c_l)
    omega_u = 2.0 * math.pi * 1.0e9
    mb_phys = (E * area / length) / (KAPPA * omega_u * omega_u)
    rod_mass = rho * area * length
    side_phys = side * mb_phys
    total_phys = MASS * mb_phys
    print(f"kappa={KAPPA:.12f}, M={MASS:.12f}, kint={KINT:.12f}")
    print(f"E={E:g} Pa, rho={rho:g} kg/m^3, A={area:.6e} m^2, a={length:.6e} m (illustrative)")
    print(f"cL={c_l:.6f} m/s, fu=1 GHz, T={6.62607015e-34*omega_u/(4*math.pi*1.380649e-23):.9f} K")
    print(f"r=omega_u*a/cL={r:.12f}, mu_rod={mu:.12f}, side/m_b={side:.12f}")
    print(f"m_b={mb_phys:.9e} kg, m_rod={rod_mass:.9e} kg, m_side={side_phys:.9e} kg, M_cell={total_phys:.9e} kg")
    print(f"K=EA/a={E*area/length:.9f} N/m, k_internal={KINT*mb_phys*omega_u**2:.9f} N/m")

    for mode in ("resonator", "rigid"):
        bands = bands_below_cutoff(r, mu, mode)
        value, pieces = integrate_bands(bands)
        print(f"{mode}: bands below {OMEGA_CUT:g}={[(round(a, 9), round(b, 9)) for a,b in bands]}")
        print(f"{mode}: band contributions={pieces}; J_[0,20]={value:.12f}")

    tail = (2.0 * OMEGA_CUT**2 + 2.0 * OMEGA_CUT + 1.0) \
        * math.exp(-2.0 * OMEGA_CUT) / (1.0 - math.exp(-2.0 * OMEGA_CUT)) ** 2
    print(f"all omitted ideal-band weight above 20 <= {tail:.3e}")
    for mode in ("resonator", "rigid"):
        for panels in (100000, 500000):
            val = finite_landauer(mode, r, mu, cells=10, panels=panels)
            print(f"N=10 bare-rod-lead {mode}, Simpson panels={panels}: J={val:.12f}")


if __name__ == "__main__":
    main()
