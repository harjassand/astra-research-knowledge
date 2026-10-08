"""Small-dimension Choi SDPs for pair broadcasting and EB reconstruction.

Ordering conventions and validity boundaries are documented in
small_dimension_sdp.txt. Requires cvxpy plus Clarabel/SCS. The d=2 PPT
program is exact by 2x2 PPT=separability; for d=3 PPT and symmetric-extension
programs are outer relaxations for the EB minimum and hence only lower bounds.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import cvxpy as cp
import numpy as np


def solve_problem(problem: cp.Problem, solver: str):
    if solver.upper() == "SCS":
        return problem.solve(solver="SCS", eps=1e-7, max_iters=200_000,
                             verbose=False)
    return problem.solve(solver=solver, tol_gap_abs=1e-7, tol_feas=1e-7,
                         tol_gap_rel=1e-7, max_iter=2000, verbose=False)


def pure_state(vector: list[complex]) -> np.ndarray:
    v = np.asarray(vector, dtype=complex)
    v = v / np.linalg.norm(v)
    return np.outer(v, v.conj())


def prime_mub_states(d: int) -> list[np.ndarray]:
    """Complete prime-dimensional MUBs for d=2 or 3."""
    if d not in (2, 3):
        raise ValueError("this fixture generator supports prime d=2,3")
    states = []
    for a in range(d):
        e = np.zeros(d, dtype=complex)
        e[a] = 1
        states.append(pure_state(e))
    if d == 2:
        states += [pure_state([1, 1]), pure_state([1, -1]),
                   pure_state([1, 1j]), pure_state([1, -1j])]
        return states
    w = np.exp(2j * np.pi / d)
    for b in range(d):
        for a in range(d):
            v = np.asarray([w ** ((b * x * x + a * x) % d) for x in range(d)])
            states.append(pure_state(v))
    return states


def rational_gaussian_state(vector: list[complex]) -> np.ndarray:
    """Pure projector from Gaussian-integer amplitudes; entries are rational Gaussian."""
    v = np.asarray(vector, dtype=complex)
    norm2 = int(round(float(np.vdot(v, v).real)))
    if norm2 <= 0 or abs(np.vdot(v, v).real - norm2) > 1e-10:
        raise ValueError("vector must have integer squared norm")
    return np.outer(v, v.conj()) / norm2


def idx2(a: int, i: int, din: int) -> int:
    return a * din + i


def idx3(a: int, b: int, i: int, d: int) -> int:
    return (a * d + b) * d + i


def partial_output_from_broadcaster(J, rho: np.ndarray, d: int):
    """Marginal output map from J[(A,B),input] in row-major tensor order."""
    rows = []
    for a in range(d):
        row = []
        for ap in range(d):
            terms = [
                J[idx3(a, b, i, d), idx3(ap, b, ip, d)] * rho[i, ip]
                for b in range(d)
                for i in range(d)
                for ip in range(d)
            ]
            row.append(sum(terms))
        rows.append(row)
    return cp.bmat(rows)


def partial_output_from_channel(J, rho: np.ndarray, d: int):
    """Channel output from J[output,input], with Lambda(rho)=Tr_in J(I tensor rho^T)."""
    rows = []
    for a in range(d):
        row = []
        for ap in range(d):
            terms = [J[idx2(a, i, d), idx2(ap, ip, d)] * rho[i, ip]
                     for i in range(d) for ip in range(d)]
            row.append(sum(terms))
        rows.append(row)
    return cp.bmat(rows)


def trace_norm_epigraph(delta, t, constraints, d: int, tag: str):
    p = cp.Variable((d, d), hermitian=True, name=f"P_{tag}")
    q = cp.Variable((d, d), hermitian=True, name=f"Q_{tag}")
    constraints += [p >> 0, q >> 0, delta == p - q, cp.real(cp.trace(p + q)) <= 2 * t]


def broadcast_sdp(states: list[np.ndarray], solver: str = "CLARABEL") -> dict:
    """Exact convex program for min worst marginal trace distance over a physical pair broadcaster.

    Output swap symmetry is WLOG: averaging any broadcaster with its output swap
    makes equal marginals, and convexity of trace distance cannot increase the
    worst error when the target is the same on both outputs.
    """
    d = states[0].shape[0]
    J = cp.Variable((d**3, d**3), hermitian=True, name="J_broadcast")
    t = cp.Variable(nonneg=True, name="broadcast_error")
    constraints = [J >> 0]

    # Swap the two output tensor factors in (out1,out2,input) ordering.
    P = np.zeros((d**3, d**3))
    for a in range(d):
        for b in range(d):
            for i in range(d):
                P[idx3(b, a, i, d), idx3(a, b, i, d)] = 1
    constraints += [P @ J @ P.T == J]

    # Trace preservation: Tr_out1,out2 J = I_input.
    for i in range(d):
        for ip in range(d):
            terms = [J[idx3(a, b, i, d), idx3(a, b, ip, d)]
                     for a in range(d) for b in range(d)]
            constraints += [sum(terms) == (1 if i == ip else 0)]

    for r, rho in enumerate(states):
        out = partial_output_from_broadcaster(J, rho, d)
        trace_norm_epigraph(out - rho, t, constraints, d, f"b{r}")

    problem = cp.Problem(cp.Minimize(t), constraints)
    value = solve_problem(problem, solver)
    return {"status": problem.status, "value": float(value), "solver": solver,
            "primal_residual": getattr(problem.solver_stats, "extra_stats", None)}


def partial_transpose_output(J, d: int):
    rows = []
    for a in range(d):
        for i in range(d):
            row = []
            for ap in range(d):
                for ip in range(d):
                    row.append(J[idx2(ap, i, d), idx2(a, ip, d)])
            rows.append(row)
    return cp.bmat(rows)


def eb_ppt_sdp(states: list[np.ndarray], solver: str = "CLARABEL") -> dict:
    """PPT-Choi outer relaxation for the minimum full-domain EB error.

    Exact for d=2. For d=3 the optimum is a lower bound on e_EB, since PPT
    need not imply separability on 3x3.
    """
    d = states[0].shape[0]
    J = cp.Variable((d**2, d**2), hermitian=True, name="J_EB_relaxation")
    t = cp.Variable(nonneg=True, name="eb_error")
    constraints = [J >> 0, partial_transpose_output(J, d) >> 0]
    for i in range(d):
        for ip in range(d):
            constraints += [sum(J[idx2(a, i, d), idx2(a, ip, d)]
                                 for a in range(d)) == (1 if i == ip else 0)]
    for r, rho in enumerate(states):
        out = partial_output_from_channel(J, rho, d)
        trace_norm_epigraph(out - rho, t, constraints, d, f"e{r}")
    problem = cp.Problem(cp.Minimize(t), constraints)
    value = solve_problem(problem, solver)
    return {"status": problem.status, "value": float(value), "solver": solver,
            "interpretation": "exact e_EB for d=2; PPT lower bound for d=3",
            "primal_residual": getattr(problem.solver_stats, "extra_stats", None)}


def eb_fixed_povm_sdp(states: list[np.ndarray], effects: list[np.ndarray],
                      solver: str = "CLARABEL") -> dict:
    """Exact SDP over preparations for one supplied POVM; every feasible map is EB.

    This is a full-domain EB decoder, but it is only an upper bound on e_EB
    unless a separate argument proves the POVM is globally optimal.
    """
    d = states[0].shape[0]
    if not np.allclose(sum(effects), np.eye(d), atol=1e-9):
        raise ValueError("effects must sum to the identity")
    preparations = [cp.Variable((d, d), hermitian=True, name=f"sigma_{y}")
                    for y in range(len(effects))]
    t = cp.Variable(nonneg=True, name="fixed_povm_eb_error")
    constraints = []
    for sigma in preparations:
        constraints += [sigma >> 0, cp.real(cp.trace(sigma)) == 1]
    for r, rho in enumerate(states):
        out = cp.bmat([
            [sum(float(np.trace(effect @ rho).real) * sigma[a, ap]
                 for effect, sigma in zip(effects, preparations))
             for ap in range(d)]
            for a in range(d)
        ])
        trace_norm_epigraph(out - rho, t, constraints, d, f"fixed{r}")
    problem = cp.Problem(cp.Minimize(t), constraints)
    value = solve_problem(problem, solver)
    return {"status": problem.status, "value": float(value), "solver": solver,
            "interpretation": "feasible full-domain EB decoder from a fixed POVM; upper bound on e_EB"}


def random_gaussian_projectors(d: int, count: int, seed: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    states = []
    seen = set()
    while len(states) < count:
        re = rng.integers(-1, 2, size=d)
        im = rng.integers(-1, 2, size=d)
        v = re + 1j * im
        if np.all(v == 0):
            continue
        key = tuple(np.round((np.outer(v, v.conj()) / np.vdot(v, v)).reshape(-1), 10))
        if key in seen:
            continue
        seen.add(key)
        states.append(rational_gaussian_state(list(v)))
    return states


def traceless_affine_rank(states: list[np.ndarray]) -> int:
    d = states[0].shape[0]
    rows = [rho - np.eye(d) / d for rho in states]
    real_features = np.asarray([np.concatenate([x.real.ravel(), x.imag.ravel()]) for x in rows])
    return int(np.linalg.matrix_rank(real_features, tol=1e-9))


def exact_binary_pair_receipt() -> dict:
    """Algebraic bounds for rho0=|0><0| and rho1=|10,1><10,1|."""
    S = 1 / math.sqrt(101)
    C = 10 / math.sqrt(101)
    eb_lower = (13 - math.sqrt(110)) / (2 * math.sqrt(1010))
    eb_upper = S / 2  # dephase in the bisector basis and prepare its eigenstates
    broadcast_upper = 0.5 * math.sqrt(
        (1 - 1 / math.sqrt(2)) ** 2 * S**2 + 0.25 * (1 - C) ** 2
    )  # symmetric one-excitation isometry, after a unitary rotation
    return {
        "states_exact": ["[[1,0],[0,0]]", "[[100/101,10/101],[10/101,1/101]]"],
        "eb_lower_exact": "(13-sqrt(110))/(2*sqrt(1010))",
        "eb_upper_exact": "1/(2*sqrt(101))",
        "broadcast_upper_exact": "sqrt((1-1/sqrt(2))^2/(4*101) + (1-10/sqrt(101))^2/16)",
        "eb_lower_numeric": eb_lower,
        "eb_upper_numeric": eb_upper,
        "broadcast_upper_numeric": broadcast_upper,
        "certified_separation": "e_EB > 39/1000 > 31/1000 > 2*b_2",
        "scope": "fixed d=2 finite-family counterexample to the proposed linear bound e_EB<=2*b_2; both errors still vanish in the coalescing-state limit",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", action="store_true", help="run small random rational-state screens")
    parser.add_argument("--solver", default="CLARABEL")
    args = parser.parse_args()
    results = {"runtime": {"cvxpy": cp.__version__, "numpy": np.__version__,
                           "solver": args.solver},
               "fixtures": {}, "binary_pair_exact": exact_binary_pair_receipt(),
               "search": []}
    for d in (2, 3):
        states = prime_mub_states(d)
        effects = [rho / (d + 1) for rho in states]
        results["fixtures"][str(d)] = {
            "state_count": len(states),
            "exact_b2": f"{d-1}/{2*(d+1)}",
            "exact_e_EB": f"{d-1}/{d+1}",
            "broadcast": broadcast_sdp(states, args.solver),
            "eb_ppt": eb_ppt_sdp(states, args.solver),
            "eb_fixed_mub_povm": eb_fixed_povm_sdp(states, effects, args.solver),
        }
    if args.search:
        for p, q in ((10, 1), (4, 1), (2, 1), (1, 1), (1, 2), (1, 4), (1, 10)):
            states = [rational_gaussian_state([1, 0]),
                      rational_gaussian_state([p, q])]
            b = broadcast_sdp(states, args.solver)
            e = eb_ppt_sdp(states, args.solver)
            results["search"].append({
                "kind": "qubit-two-state-rational-sweep", "d": 2,
                "pair": [p, q], "b2": b, "eb_exact": e,
                "ratio_eb_over_b2": e["value"] / b["value"] if b["value"] > 1e-9 else None,
                "states": [[[[float(x.real), float(x.imag)] for x in row]
                            for row in rho] for rho in states],
            })
        for d, count, seed_count in ((2, 5, 5), (2, 7, 5), (3, 5, 5), (3, 10, 3)):
            for seed in range(seed_count):
                states = random_gaussian_projectors(d, count, seed + 100 * d)
                b = broadcast_sdp(states, args.solver)
                e = eb_ppt_sdp(states, args.solver)
                effects = [rho / (d + 1) for rho in prime_mub_states(d)]
                e_upper = eb_fixed_povm_sdp(states, effects, args.solver)
                results["search"].append({
                    "d": d, "count": count, "seed": seed + 100 * d,
                    "traceless_affine_rank": traceless_affine_rank(states),
                    "b2": b, "eb_ppt_lower": e,
                    "eb_mub_povm_upper": e_upper,
                    "ratio_lower": e["value"] / b["value"] if b["value"] > 1e-9 else None,
                    "states": [[[[float(x.real), float(x.imag)] for x in row]
                                for row in rho] for rho in states],
                })
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
