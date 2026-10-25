"""Numerical witness: one loop holonomy does not determine a 2D Chern number.

The exact argument is in outputs/l20/assessment.md.  This script uses the
Fukui-Hatsugai-Suzuki lattice formula only as a reproducibility check.
Requires NumPy.
"""

import numpy as np


def h_topological(kx: float, ky: float) -> np.ndarray:
    """Qi-Wu-Zhang two-band Bloch Hamiltonian at mass m = -1."""
    dx = np.sin(kx)
    dy = np.sin(ky)
    dz = -1.0 + np.cos(kx) + np.cos(ky)
    return np.array([[dz, dx - 1j * dy], [dx + 1j * dy, -dz]], dtype=complex)


def h_trivial(kx: float, ky: float) -> np.ndarray:
    """A ky-independent gapped model with the same ky=0 loop."""
    dx = np.sin(kx)
    dz = np.cos(kx)
    return np.array([[dz, dx], [dx, -dz]], dtype=complex)


def lower_band_vectors(hamiltonian, n: int) -> np.ndarray:
    points = 2 * np.pi * np.arange(n) / n
    vectors = np.empty((n, n, 2), dtype=complex)
    for ix, kx in enumerate(points):
        for iy, ky in enumerate(points):
            _, eigvecs = np.linalg.eigh(hamiltonian(kx, ky))
            vectors[ix, iy] = eigvecs[:, 0]
    return vectors


def unit_overlap(left: np.ndarray, right: np.ndarray) -> complex:
    overlap = np.vdot(left, right)
    return overlap / abs(overlap)


def fhs_chern(vectors: np.ndarray) -> float:
    """Discrete Berry-curvature sum on a periodic momentum grid."""
    nx, ny, _ = vectors.shape
    ux = np.empty((nx, ny), dtype=complex)
    uy = np.empty((nx, ny), dtype=complex)
    for ix in range(nx):
        for iy in range(ny):
            ux[ix, iy] = unit_overlap(vectors[ix, iy], vectors[(ix + 1) % nx, iy])
            uy[ix, iy] = unit_overlap(vectors[ix, iy], vectors[ix, (iy + 1) % ny])

    total_phase = 0.0
    for ix in range(nx):
        for iy in range(ny):
            plaquette = (
                ux[ix, iy]
                * uy[(ix + 1) % nx, iy]
                / ux[ix, (iy + 1) % ny]
                / uy[ix, iy]
            )
            total_phase += np.angle(plaquette)
    return total_phase / (2 * np.pi)


def loop_phase(vectors: np.ndarray, iy: int = 0) -> float:
    """Berry phase around kx at one fixed ky, returned in radians."""
    n = vectors.shape[0]
    holonomy = 1.0 + 0.0j
    for ix in range(n):
        holonomy *= unit_overlap(vectors[ix, iy], vectors[(ix + 1) % n, iy])
    return float(np.angle(holonomy))


def minimum_gap(hamiltonian, n: int = 201) -> float:
    points = 2 * np.pi * np.arange(n) / n
    gap = np.inf
    for kx in points:
        for ky in points:
            energies = np.linalg.eigvalsh(hamiltonian(kx, ky))
            gap = min(gap, float(energies[1] - energies[0]))
    return gap


def main() -> None:
    n = 81
    top = lower_band_vectors(h_topological, n)
    trivial = lower_band_vectors(h_trivial, n)
    kx = 2 * np.pi * np.arange(n) / n
    same_slice = all(
        np.allclose(h_topological(x, 0.0), h_trivial(x, 0.0), atol=1e-12)
        for x in kx
    )
    print(f"same Bloch Hamiltonian on ky=0: {same_slice}")
    print(f"minimum direct gap, topological model: {minimum_gap(h_topological):.6f}")
    print(f"minimum direct gap, trivial model:     {minimum_gap(h_trivial):.6f}")
    print(f"ky=0 loop phase, topological model: {loop_phase(top):+.12f} rad")
    print(f"ky=0 loop phase, trivial model:     {loop_phase(trivial):+.12f} rad")
    print(f"FHS Chern estimate, topological: {fhs_chern(top):+.12f}")
    print(f"FHS Chern estimate, trivial:     {fhs_chern(trivial):+.12f}")


if __name__ == "__main__":
    main()
