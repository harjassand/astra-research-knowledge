"""Actual transition, current, and work checks for the round-11 comparators.

This is an algebra/population-model check, not acquisition or a fabricated
apparatus. No empirical rare-tail fit is used.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import quad
from scipy.special import i0
from scipy.linalg import solve_discrete_lyapunov

ROOT = Path(__file__).resolve().parent
STATES = [(0, 1), (0, 2), (1, 2), (1, 0), (2, 0), (2, 1)]
INDEX = {s: i for i, s in enumerate(STATES)}
REL = np.array([-1, -2, -1, -2, -1, -2])
MOVES = []
for i, state in enumerate(STATES):
    hole = next(x for x in range(3) if x not in state)
    for species in range(2):
        delta = 1 if (state[species] + 1) % 3 == hole else -1
        target = list(state)
        target[species] = hole
        j = INDEX[tuple(target)]
        assert j in ((i + 1) % 6, (i - 1) % 6)
        assert delta == (1 if j == (i + 1) % 6 else -1)
        carrier_difference = delta * (1 if species == 0 else -1)
        assert carrier_difference == REL[j] - REL[i]
        MOVES.append((i, j, species, delta))
assert len(MOVES) == 12


def generator(clocks, forces, common_tilt=0.0):
    mat = np.zeros((6, 6))
    current = np.zeros((6, 2))
    for i, j, species, delta in MOVES:
        edge = i if delta == 1 else j
        rate = clocks[edge] * np.exp(delta * forces[species] / 2)
        mat[i, j] += rate * np.exp(common_tilt * delta / 2)
        mat[i, i] -= rate
        current[i, species] += rate * delta
    return mat, current


def stationary(mat):
    lhs = mat.T.copy()
    rhs = np.zeros(6)
    lhs[-1] = 1
    rhs[-1] = 1
    law = np.linalg.solve(lhs, rhs)
    assert np.min(law) > 0
    return law


def eigenvalue(clocks, forces, tilt):
    mat, _ = generator(clocks, forces, tilt)
    vals = np.linalg.eigvals(mat)
    val = vals[np.argmax(vals.real)]
    assert abs(val.imag) < 1e-10
    return float(val.real)


clocks = np.array([0.4, 1.8, 0.7, 2.1, 1.2, 0.5])
mobility = 3 / (2 * np.sum(1 / clocks))
force_cases = [(0.2, -0.08), (0.2, -0.2), (0.08, -0.2)]
cell_cases = []
for forces in force_cases:
    mat, current = generator(clocks, forces)
    pi = stationary(mat)
    v = pi @ current
    assert abs(v[0] - v[1]) < 2e-13
    if sum(forces):
        assert v[0] * sum(forces) > 0
    else:
        expected = np.exp(forces[0] * REL)
        expected /= expected.sum()
        assert np.max(abs(pi - expected)) < 2e-13
        assert np.max(abs(v)) < 2e-13
    cell_cases.append({
        "forces": forces,
        "velocities": v.tolist(),
        "input_power": float(forces[0] * v[0]),
        "output_power": float(-forces[1] * v[1]),
        "stationary_residual": float(np.max(abs(pi @ mat))),
    })

eps = 2e-5
v_plus = stationary(generator(clocks, (eps, 0))[0]) @ generator(clocks, (eps, 0))[1]
v_minus = stationary(generator(clocks, (-eps, 0))[0]) @ generator(clocks, (-eps, 0))[1]
mobility_fd = float((v_plus[0] - v_minus[0]) / (2 * eps))
q = 2e-4
diffusion_fd = (eigenvalue(clocks, (0, 0), q) + eigenvalue(clocks, (0, 0), -q)
                - 2 * eigenvalue(clocks, (0, 0), 0)) / (2 * q * q)
assert abs(mobility_fd - mobility) < 1e-8
assert abs(diffusion_fd - mobility) < 2e-7

# Unknown unequal physical mobilities: exact biased-periodic-diffusion mean.
d1, d2 = 0.7, 1.3
f1, f2 = 0.04, -0.02
a = d1 + d2
m = d1 * d2 / a
relative_force = (d1 * f1 - d2 * f2) / a
continuous_cases = []
for kappa in (0, 1, 2, 4, 6):
    denominator = quad(
        lambda y: np.exp(relative_force * y) * i0(2 * kappa * np.sin(y / 2)),
        0, 2 * np.pi, epsabs=1e-10, epsrel=1e-12,
    )[0]
    relative_velocity = a * np.expm1(2 * np.pi * relative_force) / denominator
    common_velocity = m * (f1 + f2)
    velocities = [common_velocity + d1 / a * relative_velocity,
                  common_velocity - d2 / a * relative_velocity]
    if kappa == 0:
        assert np.max(abs(np.array(velocities) - [d1 * f1, d2 * f2])) < 1e-13
    zero_force_denominator = quad(
        lambda y: i0(2 * kappa * np.sin(y / 2)), 0, 2 * np.pi,
        epsabs=1e-10, epsrel=1e-12,
    )[0]
    relative_diffusion = a / i0(kappa)**2
    assert abs(a * 2 * np.pi / zero_force_denominator - relative_diffusion) < 1e-12
    continuous_cases.append({
        "kappa": kappa,
        "relative_diffusion": float(relative_diffusion),
        "common_mobility": m,
        "velocities": velocities,
        "input_power": f1 * velocities[0],
        "output_power": -f2 * velocities[1],
        "operating_efficiency": -f2 * velocities[1] / (f1 * velocities[0]),
    })

# The delayed linear governor's noise prefactor: exact stationary covariance
# of the declared Gaussian comparison, not a physical initialization claim.
delay_cases = []
for h in (0.005, 0.04, 0.10):
    mat = np.array([[1.0, -h], [1.0, 0.0]])
    cov = solve_discrete_lyapunov(mat, np.diag([1.0, 0.0]))
    variance_formula = (1 + h) / (h * (2 - h - h*h))
    assert abs(cov[0, 0] - variance_formula) < 1e-9
    delay_cases.append({
        "h": h,
        "stationary_error_variance_per_innovation_variance": float(cov[0, 0]),
        "formula_residual": float(abs(cov[0, 0] - variance_formula)),
    })

result = {
    "scope": "Exact graph and population-model algebra; no empirical rare-tail fit or apparatus claim",
    "enumerated_physical_moves": len(MOVES),
    "maximum_pathwise_single_cell_current_difference": 1,
    "unknown_clock_example": clocks.tolist(),
    "mobility_exact": float(mobility),
    "mobility_centered_difference": mobility_fd,
    "diffusion_from_tilted_generator": diffusion_fd,
    "cell_force_and_work_cases": cell_cases,
    "periodic_gear_cases": continuous_cases,
    "delayed_governor_covariance_checks": delay_cases,
    "all_checks_passed": True,
}
out = ROOT / "NATIVE_GEAR_CHECKS.json"
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: result[k] for k in (
    "enumerated_physical_moves", "mobility_exact", "mobility_centered_difference",
    "diffusion_from_tilted_generator", "all_checks_passed")}, indent=2))
