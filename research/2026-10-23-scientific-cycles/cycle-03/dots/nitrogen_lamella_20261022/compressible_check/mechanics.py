"""Staggered Lagrangian slab mechanics; no trajectory integrator.

mu: fixed cell mass/area [kg/m2]; width [m]; velocity at N+1 nodes [m/s].
Cell normal compression stress is pstar = pressure - eta_longitudinal*du/width.
Thermal/species fluxes are handled by the receiving caller, not this helper.
"""
import numpy as np


def nodal_masses(mu):
    mu = np.asarray(mu, dtype=float)
    if mu.ndim != 1 or not mu.size or not np.isfinite(mu).all() or np.any(mu <= 0):
        raise ValueError('Cell masses must be finite, positive and one-dimensional')
    mass = np.empty(mu.size + 1)
    mass[0] = mu[0]/2
    mass[-1] = mu[-1]/2
    mass[1:-1] = (mu[:-1] + mu[1:])/2
    return mass


def mechanical_rhs(mu, width, velocity, pressure, eta_longitudinal,
                   exterior_left, exterior_right):
    mu = np.asarray(mu, dtype=float)
    mass = nodal_masses(mu)
    n = mu.size
    width, pressure, eta = [np.asarray(a, dtype=float) for a in
                            (width, pressure, eta_longitudinal)]
    velocity = np.asarray(velocity, dtype=float)
    if any(a.shape != (n,) for a in (width, pressure, eta)) or velocity.shape != (n+1,):
        raise ValueError('Wrong cell or node array shape')
    if not all(np.isfinite(a).all() for a in (width, pressure, eta, velocity)):
        raise ValueError('Nonfinite state')
    if np.any(width <= 0) or np.any(pressure <= 0) or np.any(eta < 0):
        raise ValueError('Require positive widths/pressures and nonnegative viscosity')
    if not np.isfinite([exterior_left, exterior_right]).all():
        raise ValueError('Nonfinite exterior load')
    du = np.diff(velocity)
    tau = eta*du/width
    pstar = pressure-tau
    force = np.r_[exterior_left-pstar[0], pstar[:-1]-pstar[1:],
                  pstar[-1]-exterior_right]
    return {
        'node_mass': mass,
        'node_acceleration': force/mass,
        'node_force': force,
        'width_rate': du,
        'normal_viscous_stress': tau,
        'compression_stress': pstar,
        'cell_internal_mechanical_power': -pstar*du,
        'cell_viscous_heating_power': tau*du,
        'total_kinetic_energy': np.dot(mass, velocity**2)/2,
        'total_kinetic_power': np.dot(velocity, force),
        'external_mechanical_power': exterior_left*velocity[0]-exterior_right*velocity[-1],
    }
