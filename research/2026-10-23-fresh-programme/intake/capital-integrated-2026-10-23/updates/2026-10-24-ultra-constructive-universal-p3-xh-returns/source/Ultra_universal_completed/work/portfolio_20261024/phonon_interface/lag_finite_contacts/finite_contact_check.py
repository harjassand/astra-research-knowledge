#!/usr/bin/env python3
"""Finite-chain two-mass phonon contact check; NumPy only.

Uses the dimensionless optimum parameters and theta=1/2 Bose factor from
PHONON_OPTIMUM.md. Integrates the real semi-infinite-lead scattering problem,
not an absorbing-boundary approximation.
"""

import numpy as np


C = 4.25987400929229248434
K = (C * C - 3.0) / 4.0
M = 4.0 - 12.0 / (C * C)
M_BACKBONE = 1.0
M_SIDE = M - M_BACKBONE
K_SIDE = 4.0 * M_SIDE / M
OMEGA_LEAD = 2.0 * np.sqrt(K / M)
J_BULK_OPTIMUM = 1.133319342823405


def integrate_device(ncells, k_contact=None, with_side_resonators=True, nq=80001):
    """Return dimensionless Landauer integral and transmission on q-grid.

    The lead atoms have mass M and nearest-neighbor spring K. Device backbone
    sites have mass 1, adjacent backbone links K, and (optionally) one side
    mass M_SIDE attached by K_SIDE. Contact springs K_CONTACT connect the
    device end backbones to the lead end atoms. The semi-infinite leads are
    eliminated using their exact Bloch surface self-energy.
    """
    if k_contact is None:
        k_contact = K
    if nq < 3 or nq % 2 == 0:
        raise ValueError("Composite Simpson integration requires odd nq >= 3")

    q = np.linspace(0.0, np.pi, nq)
    omega = OMEGA_LEAD * np.sin(q / 2.0)

    # The physical lead end atom has diagonal K+k_contact: one bulk spring K
    # and the actual contact spring. Its exact surface Green function is
    # g_s=[k_contact-K+K exp(-iq)]^-1, so Sigma=k_contact^2 g_s. The simpler
    # (k_contact^2/K) exp(iq) applies only when k_contact=K.
    sigma = k_contact * k_contact / (k_contact - K + K * np.exp(-1j * q))
    gamma = 2.0 * np.imag(sigma)

    # Physical spring diagonals before eliminating either lead. For a one-cell
    # device the backbone has two contact springs and no internal links.
    spring_diag = np.full(ncells, 2.0 * K)
    if ncells == 1:
        spring_diag[0] = 2.0 * k_contact
    else:
        spring_diag[0] = K + k_contact
        spring_diag[-1] = K + k_contact

    if with_side_resonators:
        # Schur complement of each physical side-mass coordinate. At its
        # isolated resonance this expression has a pole; the transmission
        # there is zero and the isolated point has no effect on the integral.
        with np.errstate(divide="ignore", invalid="ignore"):
            local_dynamic = spring_diag[None, :] - omega[:, None] ** 2 * (
                M_BACKBONE
                + K_SIDE * M_SIDE / (K_SIDE - M_SIDE * omega[:, None] ** 2)
            )
    else:
        local_dynamic = spring_diag[None, :] - omega[:, None] ** 2 * M

    effective = local_dynamic.astype(complex)
    if ncells == 1:
        effective[:, 0] -= 2.0 * sigma
    else:
        effective[:, 0] -= sigma
        effective[:, -1] -= sigma

    # Determinant of the effective tridiagonal N-cell operator by continuants.
    p_nm2 = np.ones(nq, dtype=complex)
    p_nm1 = effective[:, 0].copy()
    for j in range(1, ncells):
        p_n = effective[:, j] * p_nm1 - K * K * p_nm2
        p_nm2, p_nm1 = p_nm1, p_n
    det = p_nm1

    # The endpoint cofactor is K^(N-1), so this is Gamma_L Gamma_R |G_1N|^2.
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        transmission = gamma * gamma * K ** (2 * (ncells - 1)) / np.abs(det) ** 2
    transmission = np.nan_to_num(transmission, nan=0.0, posinf=0.0, neginf=0.0)

    # At q=0 the exact acoustic limiting transmission is one, while direct
    # evaluation has a 0/0 form. The upper lead edge has zero measure and zero
    # d omega/dq, so its value does not affect the integral.
    transmission[0] = 1.0
    bose = np.ones_like(omega)
    bose[1:] = (omega[1:] / np.sinh(omega[1:])) ** 2
    jacobian = (OMEGA_LEAD / 2.0) * np.cos(q / 2.0)
    integrand = bose * transmission * jacobian
    integrand[0] = OMEGA_LEAD / 2.0

    # Composite Simpson rule in q, where omega=2 sqrt(K/M) sin(q/2).
    h = np.pi / (nq - 1)
    j_value = h / 3.0 * (
        integrand[0]
        + integrand[-1]
        + 4.0 * np.sum(integrand[1:-1:2])
        + 2.0 * np.sum(integrand[2:-1:2])
    )
    return float(j_value), transmission


def point_transmission(ncells, k_contact, with_side_resonators, q):
    """Evaluate the scattering formula at one nonzero lead wave number."""
    omega = OMEGA_LEAD * np.sin(q / 2.0)
    sigma = k_contact * k_contact / (k_contact - K + K * np.exp(-1j * q))
    gamma = 2.0 * np.imag(sigma)
    spring_diag = np.full(ncells, 2.0 * K)
    if ncells == 1:
        spring_diag[0] = 2.0 * k_contact
    else:
        spring_diag[0] = spring_diag[-1] = K + k_contact
    if with_side_resonators:
        local_dynamic = spring_diag.astype(complex) - omega**2 * (
            M_BACKBONE + K_SIDE * M_SIDE / (K_SIDE - M_SIDE * omega**2)
        )
    else:
        local_dynamic = spring_diag.astype(complex) - omega**2 * M
    if ncells == 1:
        local_dynamic[0] -= 2.0 * sigma
    else:
        local_dynamic[0] -= sigma
        local_dynamic[-1] -= sigma
    p_nm2 = 1.0 + 0.0j
    p_nm1 = local_dynamic[0]
    for j in range(1, ncells):
        p_nm2, p_nm1 = p_nm1, local_dynamic[j] * p_nm1 - K * K * p_nm2
    return float(gamma * gamma * K ** (2 * (ncells - 1)) / abs(p_nm1) ** 2)


def main():
    print(f"K={K:.12f} M={M:.12f} m_side={M_SIDE:.12f} k_side={K_SIDE:.12f}")
    print(f"lead cutoff={OMEGA_LEAD:.12f}; side resonance={np.sqrt(K_SIDE/M_SIDE):.12f}")
    print("N  J_side  J_rigid  side/rigid  side/bulk_ideal  rigid_max_abs_error")
    for n in (1, 2, 4, 8, 16):
        js, _ = integrate_device(n, with_side_resonators=True)
        jr, tr = integrate_device(n, with_side_resonators=False)
        print(
            f"{n:2d} {js:.12f} {jr:.12f} {js/jr:.9f} "
            f"{js/J_BULK_OPTIMUM:.9f} {np.max(np.abs(tr[1:-1]-1.0)):.3g}"
        )

    print("N=8, physical contact-spring sweep (same contact for side and rigid devices)")
    for ratio in (0.5, 0.75, 1.0, 1.5, 2.0):
        kc = ratio * K
        js, _ = integrate_device(8, k_contact=kc, with_side_resonators=True)
        jr, _ = integrate_device(8, k_contact=kc, with_side_resonators=False)
        print(f"Kc/K={ratio:.2f} J_side={js:.12f} J_rigid={jr:.12f} ratio={js/jr:.9f}")

    print("N=8 low-frequency transmission; q=0.01, 0.001, 0.0001")
    for ratio in (0.5, 1.0, 2.0):
        kc = ratio * K
        for q0 in (1e-2, 1e-3, 1e-4):
            ts = point_transmission(8, kc, True, q0)
            tr = point_transmission(8, kc, False, q0)
            print(f"Kc/K={ratio:.2f} q={q0:.0e} T_side={ts:.12f} T_rigid={tr:.12f}")

    print("N=16 quadrature convergence")
    for nq in (20001, 80001, 320001):
        js, _ = integrate_device(16, with_side_resonators=True, nq=nq)
        print(f"nq={nq} J_side={js:.12f}")


if __name__ == "__main__":
    main()
