"""Independent, introduced resistor-grid diagnostics; no producer code or hardware.

The analytic argument is in the accompanying contracts file.  Floating tests
illustrate it; they are neither a proof by sampling nor physical qualification.
Requires only the NumPy already present in the workspace environment.
"""
import itertools
import json
import math
import os
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
import numpy as np


def path_laplacian(m):
    a = np.zeros((m, m))
    for i in range(m - 1):
        a[i, i] += 1
        a[i + 1, i + 1] += 1
        a[i, i + 1] -= 1
        a[i + 1, i] -= 1
    return a


def solve_grid(r, g):
    m, length = r.shape
    nodes = m * (length + 1)
    a = np.zeros((nodes, nodes))
    def add(u, v, c):
        a[u, u] += c
        a[v, v] += c
        a[u, v] -= c
        a[v, u] -= c
    def node(i, k):
        return i * (length + 1) + k
    for i in range(m):
        for k in range(length):
            add(node(i, k), node(i, k + 1), 1 / r[i, k])
    for i in range(m - 1):
        for k in range(length + 1):
            add(node(i, k), node(i + 1, k), g)
    q = np.zeros((nodes, m))
    for s in range(m):
        q[node(s, 0), s] = 1
        q[node(s, length), s] = -1
    v = np.zeros_like(q)
    v[:-1] = np.linalg.solve(a[:-1, :-1], q[:-1])
    currents = np.empty((m, length, m))
    for i in range(m):
        for k in range(length):
            currents[i, k] = (v[node(i, k)] - v[node(i, k + 1)]) / r[i, k]
    energy = np.diag(q.T @ v)
    return currents, energy


def dual_system(r, g):
    m, length = r.shape
    lap = path_laplacian(m)
    a = np.zeros((m * length, m * length))
    b = np.zeros((m * length, m))
    for k in range(length):
        sl = slice(m * k, m * (k + 1))
        a[sl, sl] = 2 * np.eye(m) + g * lap @ np.diag(r[:, k])
        if k:
            a[sl, slice(m * (k - 1), m * k)] = -np.eye(m)
        else:
            b[sl] += np.eye(m)
        if k + 1 < length:
            a[sl, slice(m * (k + 1), m * (k + 2))] = -np.eye(m)
        else:
            b[sl] += np.eye(m)
    j = np.linalg.solve(a, b).reshape(length, m, m).transpose(1, 0, 2)
    return j, float(np.min(a.sum(axis=0))), float(np.max(a.sum(axis=0)))


def diagnostics(r, g, rmax=2.0):
    m, length = r.shape
    j, f = solve_grid(r, g)
    jd, csmin, csmax = dual_system(r, g)
    epsilon = g * min(2, m - 1) * rmax * (length + 1) ** 2 / 8
    selected = np.asarray([j[s, :, s] for s in range(m)])
    off = j.copy()
    for s in range(m):
        off[s, :, s] = 0
    result = dict(rows=m, length=length, g=g, epsilon=epsilon,
                  min_current=float(j.min()),
                  max_current_sum_error=float(abs(j.sum(axis=0) - 1).max()),
                  selected_min=float(selected.min()),
                  nonselected_max=float(off.max()),
                  max_off_sum=float(off.sum(axis=0).max()),
                  dual_difference=float(abs(j - jd).max()),
                  dual_column_sum_min=csmin, dual_column_sum_max=csmax)
    assert j.min() > -1e-10
    assert result["dual_difference"] < 1e-9
    assert result["max_current_sum_error"] < 1e-9
    assert selected.min() >= 1 - epsilon - 1e-10
    assert off.sum(axis=0).max() <= epsilon + 1e-10
    return result, f, j


def main():
    rng = np.random.default_rng(1426)
    cases = []
    # All 2^6 introduced resistance corners of the 3-row/2-edge grid.
    for corner in itertools.product([1.0, 2.0], repeat=6):
        r = np.asarray(corner).reshape(3, 2)
        record, _, _ = diagnostics(r, 4 * .06 / (2 * 3 ** 2))
        cases.append(record)
    # Finite contrasting initial states, without assuming uniform rows.
    for m, length in [(2, 4), (3, 8), (5, 4), (5, 8)]:
        g = 4 * .06 / (2 * (length + 1) ** 2)
        patterns = [np.ones((m, length)), np.full((m, length), 2.0),
                    1.0 + np.indices((m, length)).sum(axis=0) % 2,
                    rng.uniform(1.0, 2.0, (m, length))]
        for r in patterns:
            record, _, _ = diagnostics(r, g)
            cases.append(record)

    # New limited inverse statement: only row-uniform continuous parameters.
    inverse_cases = []
    for m, length in [(2, 4), (3, 8), (5, 8)]:
        g = 4 * .06 / (2 * (length + 1) ** 2)
        target = rng.uniform(1.1, 1.9, m)
        _, ft = solve_grid(np.repeat(target[:, None], length, axis=1), g)
        r = rng.uniform(1.0, 2.0, m)
        history = [float(np.max(abs(r - target)))]
        jacobian_records = []
        for _ in range(12):
            record, f, j = diagnostics(np.repeat(r[:, None], length, axis=1), g)
            # Rows are measured energies, columns are row parameters.
            jac = (j ** 2).sum(axis=1).T
            eps = record["epsilon"]
            diag = np.diag(jac)
            offsum = jac.sum(axis=1) - diag
            contraction = np.max(np.abs(np.eye(m) - jac / length).sum(axis=1))
            assert diag.min() >= length * (1 - eps) ** 2 - 1e-10
            assert offsum.max() <= length * eps ** 2 + 1e-10
            assert contraction <= 2 * eps + 1e-10
            jacobian_records.append(dict(min_diagonal=float(diag.min()),
                                         max_offsum=float(offsum.max()),
                                         contraction_norm=float(contraction)))
            r = np.clip(r - (f - ft) / length, 1, 2)
            history.append(float(np.max(abs(r - target))))
        # Testing stops at floating precision; no bound below solver error claimed.
        inverse_cases.append(dict(rows=m, length=length, g=g,
                                  target=target.tolist(), error_history=history,
                                  jacobian_diagnostics=jacobian_records,
                                  analytic_contraction_bound=2 * eps))

    # Independent continuum two-row calculation; its read excitation differs
    # from the producer's equal-transverse-voltage-at-both-ends read witness.
    continuum = []
    for off in [.01, .03, .06, .1]:
        s = math.acosh(1 / (1 - 2 * off))
        ratio = math.tanh(s) / s
        continuum.append(dict(off_fraction=off, s=s,
                              antisymmetric_read_relative_change=1 - ratio,
                              single_row_write_power_ratio=(1 + ratio) / 2))

    # A separate common-end-voltage read.  Keep the physical conductance and
    # its state-dependent normalization distinct.  This is our declared grid,
    # not recovery or execution of the producer's unavailable model.
    common_end_read = []
    lam = 2 + 2 * math.cos(math.pi / 16)
    for length in [15, 16]:
        for boundary_rungs in [False, True]:
            states = []
            for r in [120., 240.]:
                coeff = r * lam / 270000.
                a = ((2 + coeff) * np.eye(length - 1)
                     - np.eye(length - 1, k=1) - np.eye(length - 1, k=-1))
                b = np.zeros(length - 1)
                b[0] += 1
                b[-1] += 1
                vint = np.linalg.solve(a, b)
                gread = 2 * ((1 - vint[0]) / r
                             + (lam / 270000. if boundary_rungs else 0))
                states.append(dict(horizontal_r=r, physical_modal_conductance=gread,
                                   normalized_to_2_over_Lr=gread * length * r / 2))
            common_end_read.append(dict(rows=16, length=length,
                                        boundary_rungs=boundary_rungs, states=states,
                                        physical_high_over_low=states[1]["physical_modal_conductance"] / states[0]["physical_modal_conductance"],
                                        normalized_high_over_low=states[1]["normalized_to_2_over_Lr"] / states[0]["normalized_to_2_over_Lr"]))

    # Two competing adaptive paths, introduced normalized Physarum-type law.
    # For D1+D2=1, the exact scalar equation is dx/dt=x(1-x)*delta/(x/L1+(1-x)/L2).
    # Thus the following elapsed time is analytic, not ODE solver evidence.
    route = []
    initial, final = .5, .99
    for length_gap in [1.0, .1, .01, .001]:
        l1, l2 = 1., 1. + length_gap
        aa, bb = 1 / l1, 1 / l2
        elapsed = (bb * math.log(final / initial)
                   - aa * math.log((1 - final) / (1 - initial))) / (aa - bb)
        route.append(dict(length_gap=length_gap, initial_short_path_fraction=initial,
                          final_short_path_fraction=final, normalized_time=elapsed,
                          off_drive_total_after_time_1=math.exp(-1)))

    out = dict(scope="INTRODUCED exact linear circuit and continuum/adaptation models; no hardware or novelty claim",
               current_case_count=len(cases),
               current_summary=dict(min_current=min(c["min_current"] for c in cases),
                                    max_off_sum=max(c["max_off_sum"] for c in cases),
                                    min_selected=min(c["selected_min"] for c in cases),
                                    max_dual_difference=max(c["dual_difference"] for c in cases),
                                    max_current_sum_error=max(c["max_current_sum_error"] for c in cases)),
               current_cases=cases, row_uniform_inverse_cases=inverse_cases,
               continuum_two_row_cases=continuum,
               common_end_voltage_read_cases=common_end_read,
               producer_numbers_normalization_identity=dict(
                   condition="IF the reported .205/.396 numbers use the stated reference proportional to 1/r",
                   physical_high_over_low=(.396 / .205) * (120 / 240),
                   normalized_high_over_low=.396 / .205),
               adaptive_two_parallel_path_cases=route)
    target = Path(__file__).with_suffix(".json")
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"output":str(target), "current_cases":len(cases),
                      "current_summary":out["current_summary"],
                      "inverse_final_errors":[x["error_history"][-1] for x in inverse_cases],
                      "continuum":continuum,"common_end_read":common_end_read,
                      "adaptive_paths":route}, indent=2))


if __name__ == "__main__":
    main()
