"""Exact finite-depth obstruction in a connected interacting fermion chain.

This is a counterexample to a restricted information interface, not a physical
data set or a lower bound for algorithms allowed to inspect all coefficients.
All exact moment tests use Python integers on 16*(H-E_seed I).
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json
import math
import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh, expm_multiply

BASE = Path(__file__).resolve().parent


def build(sites=12, particles=4, trap_first=8, eps_units=1, scale=16,
          hopping=1, repulsion=1, left_depth=10, trap_depth=11):
    states = [sum(1 << i for i in occ) for occ in combinations(range(sites), particles)]
    index = {state: k for k, state in enumerate(states)}
    seed = index[(1 << particles) - 1]
    e_seed = -left_depth * particles + repulsion * (particles - 1)
    matrices = []
    integer_rows = []
    for with_trap in [False, True]:
        rows = [[] for _ in states]
        for i, state in enumerate(states):
            occ = [(state >> j) & 1 for j in range(sites)]
            energy = -left_depth * sum(occ[:particles])
            energy += repulsion * sum(occ[j] * occ[j + 1] for j in range(sites - 1))
            if with_trap:
                energy -= trap_depth * sum(occ[trap_first:])
            diag = scale * (energy - e_seed)
            if diag:
                rows[i].append((i, diag))
            for j in range(sites - 1):
                if occ[j] != occ[j + 1]:
                    target = state ^ (1 << j) ^ (1 << (j + 1))
                    value = -eps_units if j == particles - 1 else -scale * hopping
                    rows[index[target]].append((i, value))
        rr, cc, vv = [], [], []
        for i, row in enumerate(rows):
            for j, value in row:
                rr.append(i)
                cc.append(j)
                vv.append(value / scale)
        matrices.append(sparse.csr_matrix((vv, (rr, cc)), shape=(len(states), len(states))))
        integer_rows.append(rows)
    return states, seed, e_seed, matrices, integer_rows


def integer_matvec(rows, vector):
    return [sum(value * vector[j] for j, value in row) for row in rows]


def main():
    start = time.perf_counter()
    sites, particles, trap_first, scale = 12, 4, 8, 16
    eps = Fraction(1, scale)
    states, seed, e_seed, matrices, integer_rows = build(sites, particles, trap_first)
    d = (trap_first + 1) - particles
    vectors = [[int(i == seed) for i in range(len(states))] for _ in range(2)]
    moment_rows = []
    for k in range(2 * d + 2):
        difference = Fraction(vectors[1][seed] - vectors[0][seed], scale ** k)
        moment_rows.append({
            "degree": k,
            "compressed_moment_difference_exact": str(difference),
            "full_krylov_vectors_equal_exactly": vectors[0] == vectors[1],
        })
        vectors = [integer_matvec(rows, vector) for rows, vector in zip(integer_rows, vectors)]
    assert all(row["compressed_moment_difference_exact"] == "0" for row in moment_rows[:2*d+1])
    assert all(row["full_krylov_vectors_equal_exactly"] for row in moment_rows[:d+1])
    assert moment_rows[d+1]["full_krylov_vectors_equal_exactly"] is False
    assert Fraction(moment_rows[-1]["compressed_moment_difference_exact"]) == -11 * eps**2
    basis = np.zeros(len(states)); basis[seed] = 1
    numerical = []
    for label, matrix in zip(["H0_no_remote_trap", "H1_remote_trap"], matrices):
        begin = time.perf_counter()
        ev, vec = eigsh(matrix, k=2, which="SA", tol=1e-12, v0=np.ones(len(states)))
        numerical.append({
            "label": label,
            "two_lowest_energies_float_diagnostic": (ev + e_seed).tolist(),
            "ground_seed_overlap_squared_float_diagnostic": float(vec[seed, 0]**2),
            "seed_residual_norm": float(np.linalg.norm(matrix @ basis)),
            "eigensolve_seconds": time.perf_counter() - begin,
        })
    # V-2U-4t is a proved form bound, not an exact spectral gap.
    kappa = 10 - 2 * 1 - 4 * 1
    g = kappa - float(eps)
    delta = 2 * float(eps)**2 / (math.sqrt(g*g + 4*float(eps)**2) + g)
    # A direct finite-time signal test supplements, but does not prove, the
    # independent analytic epsilon^2 T^2 bound in THEORY.txt.
    signals = []
    for duration in [0.1, 1.0, 10.0]:
        amps = []
        for matrix in matrices:
            state = expm_multiply((-1j*duration) * matrix, basis, traceA=(-1j*duration)*matrix.diagonal().sum())
            amps.append(state[seed])
        signals.append({"time": duration, "survival_amplitude_difference_float": float(abs(amps[0]-amps[1])),
                        "proved_epsilon_squared_t_squared_bound": float(eps)**2 * duration**2})
    result = {
        "status": "restricted_interface_no_go; numerical eigensolves are diagnostics only",
        "model": "connected spinless extended Hubbard path, fixed particle number; genuinely nonzero nearest-neighbor interaction",
        "sites": sites, "particles": particles, "sector_dimension": len(states),
        "trap_first_site_one_based": trap_first+1, "hopping_t": 1, "interaction_U": 1,
        "left_well_depth_V": 10, "remote_well_depth_M": 11,
        "weak_link_epsilon_exact": str(eps), "seed_energy_exact": e_seed,
        "distance_to_remote_trap": d,
        "exact_moment_tests": moment_rows,
        "analytic_certificate": {
            "kappa": kappa, "complement_floor_above_seed": g,
            "H0_energy_lower_analytic_float_evaluation": e_seed-delta,
            "H0_energy_upper_exact": e_seed,
            "H1_energy_upper_from_remote_determinant_exact": e_seed-particles,
            "energy_separation_lower_analytic_float_evaluation": particles-delta,
            "formula_delta": "2 epsilon^2 / (sqrt(g^2+4epsilon^2)+g), g=V-2U-4t-epsilon",
            "note": "Proof is exact; displayed irrational endpoints are ordinary float evaluations, not outward-rounded numerical certificates."
        },
        "numerical_diagnostics": numerical,
        "finite_time_signal_diagnostics": signals,
        "elapsed_code_seconds": time.perf_counter()-start,
        "not_claimed": ["molecular experimental data", "novel theorem in the literature", "impossibility for algorithms inspecting full Hamiltonian coefficients", "physical many-body speedup"]
    }
    (BASE/'LOCAL_COUNTEREXAMPLE.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
