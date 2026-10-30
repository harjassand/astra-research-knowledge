#!/usr/bin/env python3
"""Reproduce three independent population-model checks for the root theorem.

Checks: actual interacting carrier cell (including real work), nonlinear
exclusion action contraction, and delayed feedback on real lattice carriers.
This is not a finite-data confidence certificate or a numerical proof of an LDP.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar


def carrier_cell_check() -> dict:
    rng = np.random.default_rng(910031)
    R, N, g, bath = 5, 13.0, 0.9, 0.35
    h, beta = np.pi / (2 * g), 2 / g + bath
    coeff = rng.uniform(0.2, 3.0, (R, R))
    coeff = (coeff + coeff.T) / 2
    np.fill_diagonal(coeff, 0.0)
    max_current_error = max_momentum_error = max_work_error = 0.0
    omitted_endpoint_terms = []
    for strength in (0.1, 2.0, 17.0):
        X = rng.uniform(0, N, R)
        V, Y = rng.normal(size=R), rng.normal(size=R)
        delayed_J, cumulative_J = 0.0, 0.0
        actual_work = corrected_work = momentum_term = 0.0
        for k in range(24):
            F = -0.18 * np.sign(delayed_J) if k > 1 else 0.0
            old_delayed = cumulative_J
            P0, Y0, X0 = V.sum(), Y.sum(), X.copy()

            def grad(x):
                angles = 2 * np.pi * (x[:, None] - x[None, :]) / N
                return strength * (2 * np.pi / N) * (coeff * np.sin(angles)).sum(axis=1)

            def transport(_t, z):
                x, v, y = z[:R], z[R:2 * R], z[2 * R:]
                return np.concatenate((v, -grad(x) - g * y + F, g * v))

            sol = solve_ivp(transport, (0, h), np.concatenate((X, V, Y)),
                            rtol=2e-11, atol=1e-12)
            assert sol.success
            X, V, Y = np.split(sol.y[:, -1], 3)
            incoming = rng.normal(size=R)

            def bath_rhs(_t, z):
                x, v = z[:R], z[R:]
                return np.concatenate((v, -grad(x) + F))

            sol = solve_ivp(bath_rhs, (0, bath), np.concatenate((X, V)),
                            rtol=2e-11, atol=1e-12)
            assert sol.success
            X, V = np.split(sol.y[:, -1], 2)
            # An exact finite-frequency quarter rotation swaps in this source.
            Y = incoming
            dJ, dP = float((X - X0).sum()), float(V.sum() - P0)
            predicted_corrected = -beta * Y0 + R * beta**2 * F / 2
            predicted_P = -Y0 + R * F * (1 / g + bath)
            max_current_error = max(max_current_error,
                                    abs(dJ + dP / g - predicted_corrected))
            max_momentum_error = max(max_momentum_error, abs(V.sum() - predicted_P))
            actual_work += F * dJ
            corrected_work += F * predicted_corrected
            momentum_term += F * dP / g
            cumulative_J += dJ
            delayed_J = old_delayed
        max_work_error = max(max_work_error,
                             abs(actual_work - (corrected_work - momentum_term)))
        omitted_endpoint_terms.append(float(momentum_term))
    assert max_current_error < 2e-8
    assert max_momentum_error < 2e-8
    assert max_work_error < 2e-8
    assert max(abs(v) for v in omitted_endpoint_terms) > 1e-3
    return {"unknown_interaction_strengths": [0.1, 2.0, 17.0],
            "periods_per_strength": 24,
            "max_true_current_identity_error": max_current_error,
            "max_momentum_identity_error": max_momentum_error,
            "max_actual_work_identity_error": max_work_error,
            "work_terms_that_would_be_lost_by_dropping_momentum": omitted_endpoint_terms,
            "scope": "ODE population identity, not a built thermal preparation or sensor"}


def action_check() -> dict:
    x = (np.arange(8192) + 0.5) / 8192
    D = np.array([0.7, 1.4])
    means, amps, speeds = np.array([0.3, 0.57]), np.array([0.12, 0.09]), np.array([0.8, -0.45])
    t, common_current = 0.37, 0.21
    phase = 2 * np.pi * (x[None, :] - speeds[:, None] * t)
    rho = means[:, None] + amps[:, None] * np.cos(phase)
    grad = -2 * np.pi * amps[:, None] * np.sin(phase)
    nonconstant_j = speeds[:, None] * (rho - means[:, None])
    mobility = D[:, None] * rho * (1 - rho)
    a = nonconstant_j + common_current + D[:, None] * grad
    r = (1 / mobility).mean(axis=1)
    ell = (a / mobility).mean(axis=1)
    u = -(ell[0] - ell[1]) / r.sum()
    predicted = 0.25 * ((a * a / mobility).mean(axis=1).sum() - (ell[0] - ell[1])**2 / r.sum())

    def native_preimage_cost(shift):
        shifted = a + np.array([shift, -shift])[:, None]
        return 0.25 * (shifted**2 / mobility).mean(axis=1).sum()

    numerical = minimize_scalar(native_preimage_cost, bracket=(u - 1, u + 1))
    assert numerical.success
    error = abs(predicted - numerical.fun)
    assert error < 2e-12
    # Compare complete density-history costs, optimizing the remaining mean.
    a0 = nonconstant_j + D[:, None] * grad
    d = (a0 / mobility).mean(axis=1)
    c = (a0**2 / mobility).mean(axis=1).sum()
    native_density_cost = 0.25 * (c - np.sum(d**2 / r))
    passive_common_cost = 0.25 * (c - d.sum()**2 / r.sum())
    native_optimal_means = -d / r
    optimal_output_mean = native_optimal_means.mean()
    aa = a0 + optimal_output_mean
    ll = (aa / mobility).mean(axis=1)
    active_density_cost = 0.25 * ((aa**2 / mobility).mean(axis=1).sum()
                                 - (ll[0] - ll[1])**2 / r.sum())
    assert abs(active_density_cost - native_density_cost) < 2e-12
    assert passive_common_cost - native_density_cost > 1e-5
    return {"spatial_grid": len(x), "nonflat_profile_min": float(rho.min()),
            "nonflat_profile_max": float(rho.max()),
            "analytic_action": float(predicted), "direct_minimized_action": float(numerical.fun),
            "minimization_error": float(error), "analytic_eliminated_current": float(u),
            "native_density_history_cost": float(native_density_cost),
            "active_density_history_cost": float(active_density_cost),
            "passively_restricted_common_current_cost": float(passive_common_cost),
            "passive_density_cost_increase": float(passive_common_cost - native_density_cost),
            "scope": "exact quadratic minimization on a nonlinear mobility profile; spatial quadrature"}


def native_exclusion_events(N, horizon, D, fields, occupancies, seed):
    rng = np.random.default_rng(seed)
    q = len(D)
    state = np.zeros((q, N), dtype=np.int64)
    for a, density in enumerate(occupancies):
        state[a, rng.choice(N, round(density * N), replace=False)] = 1
    initial = state.copy()
    rates = np.array([[D[a] * np.exp(fields[a] / (2 * N)),
                       D[a] * np.exp(-fields[a] / (2 * N))] for a in range(q)])
    total = N * rates.sum()
    probs = rates.ravel() / rates.sum()
    cumulative = np.cumsum(probs)
    now, events, proposals = 0.0, [], 0
    while True:
        now += rng.exponential(1 / total)
        if now > horizon:
            break
        proposals += 1
        event = int(np.searchsorted(cumulative, rng.random(), side="right"))
        a, direction = divmod(event, 2)
        edge = int(rng.integers(N))
        right = (edge + 1) % N
        src, dst, sign = (edge, right, 1) if direction == 0 else (right, edge, -1)
        if state[a, src] and not state[a, dst]:
            state[a, src], state[a, dst] = 0, 1
            events.append((now, a, edge, sign))
    return initial, events, proposals


def carrier_deployment(N, R, horizon, initial_native, events, program, seed,
                       amplitude=0.45, trigger_factor=0.25, macro_scale=0.3):
    """Exact event-driven independent-walker model, with one-epoch-delayed counts.

    The controller receives events only when executed, although the proof/test
    couples the native path across programs. No controller can inspect its future.
    """
    rng = np.random.default_rng(seed)
    q = initial_native.shape[0]
    native = initial_native.copy()
    positions = rng.integers(N, size=(q, R))
    aux_initial = np.array([np.bincount(p, minlength=N) for p in positions])
    clocks = rng.uniform(0.6, 1.4, (q, R))  # Never passed to the controller.
    J_native = np.zeros((q, N), dtype=np.int64)
    J_aux = np.zeros((q, N), dtype=np.int64)
    forces = np.zeros(q)
    epoch = N / 4  # Fixed finite local signal speed; total delay is O(N).
    threshold = trigger_factor * N**1.5 * np.log(2 + N)
    previous_error = np.zeros(q)
    armed = False
    arm_time = None
    t = 0.0
    native_index = 0
    actual_work = 0.0
    work_compensator = 0.0
    max_spatial_error = 0.0
    max_continuity_error = 0
    max_tracking_error = 0.0
    traces, auxiliary_events = [], []

    def target(B, now):
        h = B / N**2
        if program == "projection":
            mapped = np.repeat(h.mean(), q)
        elif program == "nonlinear_rectifier":
            mapped = macro_scale * h**2 / (macro_scale**2 + h**2)
        elif program == "cancel":
            mapped = np.zeros(q)
        elif program == "zero_drive":
            mapped = h
        else:
            raise ValueError(program)
        return N**2 * (mapped - h)

    boundary = 0.0
    while boundary < horizon:
        end = min(boundary + epoch, horizon)
        # Use only the snapshot from one completed epoch ago.
        if program != "zero_drive" and np.max(np.abs(previous_error)) >= threshold:
            armed = True
            if arm_time is None:
                arm_time = boundary
        if armed:
            forces = -amplitude * np.sign(previous_error)
        B_at_boundary = J_native.sum(axis=1).astype(float)
        A_at_boundary = J_aux.sum(axis=1).astype(float)
        next_error = A_at_boundary - target(B_at_boundary, boundary)
        step_rates = np.stack((clocks * np.exp(forces[:, None] / 2),
                               clocks * np.exp(-forces[:, None] / 2)), axis=2)
        aux_total = step_rates.sum()
        cumulative = np.cumsum(step_rates.ravel()) / aux_total
        next_aux = boundary + rng.exponential(1 / aux_total)
        interval = end - boundary
        work_compensator += interval * np.sum(forces[:, None] *
                                               (step_rates[:, :, 0] - step_rates[:, :, 1]))
        while True:
            next_native = events[native_index][0] if native_index < len(events) else np.inf
            next_event = min(next_aux, next_native)
            if next_event >= end:
                break
            t = next_event
            if next_native <= next_aux:
                _, a, edge, sign = events[native_index]
                native_index += 1
                right = (edge + 1) % N
                src, dst = (edge, right) if sign == 1 else (right, edge)
                assert native[a, src] == 1 and native[a, dst] == 0
                native[a, src], native[a, dst] = 0, 1
                J_native[a, edge] += sign
            else:
                flat = int(np.searchsorted(cumulative, rng.random(), side="right"))
                a, l, direction = np.unravel_index(flat, step_rates.shape)
                sign = 1 if direction == 0 else -1
                old = positions[a, l]
                edge = old if sign == 1 else (old - 1) % N
                positions[a, l] = (old + sign) % N
                J_aux[a, edge] += sign
                actual_work += forces[a] * sign
                auxiliary_events.append((float(t), int(a), int(l), int(sign)))
                next_aux = t + rng.exponential(1 / aux_total)
        t = end
        B, A = J_native.sum(axis=1), J_aux.sum(axis=1)
        aux = np.array([np.bincount(p, minlength=N) for p in positions])
        native_error = native - initial_native - (np.roll(J_native, 1, axis=1) - J_native)
        auxiliary_error = aux - aux_initial - (np.roll(J_aux, 1, axis=1) - J_aux)
        max_continuity_error = max(max_continuity_error,
                                   int(np.max(np.abs(native_error))), int(np.max(np.abs(auxiliary_error))))
        centered = J_aux / N - A[:, None] / N**2
        max_spatial_error = max(max_spatial_error, float(np.max(np.abs(centered))))
        err = (A - target(B.astype(float), t)) / N**2
        max_tracking_error = max(max_tracking_error, float(np.max(np.abs(err))))
        traces.append({"physical_time": t, "background_harmonic": (B / N**2).tolist(),
                       "auxiliary_harmonic": (A / N**2).tolist(),
                       "actual_total_harmonic": ((B + A) / N**2).tolist(),
                       "target_harmonic": ((B + target(B.astype(float), t)) / N**2).tolist(),
                       "forces": forces.tolist(), "armed": armed})
        previous_error = next_error
        boundary = end
    assert max_continuity_error == 0
    assert max_spatial_error <= 2 * R / N + 1e-12
    digest = hashlib.sha256(json.dumps(auxiliary_events, separators=(",", ":")).encode()).hexdigest()
    return {"program": program, "R_per_lane": R, "carrier_clock_range": [float(clocks.min()), float(clocks.max())],
            "force_cap": amplitude, "epoch_length": epoch, "trigger_counter": threshold,
            "arm_time": arm_time, "native_events_executed": native_index,
            "auxiliary_events_executed": len(auxiliary_events), "auxiliary_event_sha256": digest,
            "exact_integer_continuity_residual": max_continuity_error,
            "largest_nonconstant_auxiliary_current": max_spatial_error,
            "deterministic_bound": 2 * R / N,
            "max_sampled_macroscopic_tracking_error": max_tracking_error,
            "actual_stochastic_force_work": float(actual_work),
            "force_work_compensator_on_this_trajectory": float(work_compensator),
            "final": traces[-1], "trace": traces}


def jump_checks() -> dict:
    N, R, T = 48, 6, 0.8
    horizon = N**2 * T
    initial, events, proposals = native_exclusion_events(
        N, horizon, [0.7, 1.4], [3.0, -1.0], [0.3, 0.57], seed=910032)
    loaded = [carrier_deployment(N, R, horizon, initial, events, p, seed=910033)
              for p in ("zero_drive", "projection", "nonlinear_rectifier")]
    # All programs execute exactly the same actual background path.
    assert len({r["native_events_executed"] for r in loaded}) == 1
    assert len({tuple(r["final"]["background_harmonic"]) for r in loaded}) == 1
    # At zero force the seed produces no arm; complete auxiliary paths then agree.
    init0, events0, prop0 = native_exclusion_events(
        N, horizon, [0.7], [0.0], [0.3], seed=910034)
    ref = carrier_deployment(N, R, horizon, init0, events0, "zero_drive", seed=910035,
                             trigger_factor=1.0)
    arm = carrier_deployment(N, R, horizon, init0, events0, "cancel", seed=910035,
                             trigger_factor=1.0)
    assert arm["arm_time"] is None
    assert arm["auxiliary_event_sha256"] == ref["auxiliary_event_sha256"]
    return {"N": N, "macroscopic_horizon": T, "native_proposals_loaded": proposals,
            "native_proposals_unforced": prop0, "loaded_deployments": loaded,
            "unforced_coupling": {"armed": False,
                                  "identical_auxiliary_event_hash": arm["auxiliary_event_sha256"],
                                  "native_events": len(events0),
                                  "auxiliary_events": arm["auxiliary_events_executed"]},
            "scope": "single-seed exact event-driven population executions; no sampling confidence or asymptotic tail fit"}


def main():
    result = {"schema": "astra_p1.circulation_operation_checks.v1",
              "carrier_cell": carrier_cell_check(), "nonlinear_action": action_check(),
              "actual_jump_carriers": jump_checks(),
              "not_established": ["manufactured apparatus", "acquired detector/clock/reliability budget",
                                  "finite-data confidence", "large-deviation asymptotics from simulation",
                                  "practical efficiency or historical priority"]}
    output = Path(__file__).with_name("CIRCULATION_OPERATION_CHECK_RESULTS.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    brief = {"output": str(output), "carrier_cell": result["carrier_cell"],
             "nonlinear_action": result["nonlinear_action"],
             "loaded_current_examples": [{k: r[k] for k in ("program", "arm_time", "final",
                                          "max_sampled_macroscopic_tracking_error",
                                          "actual_stochastic_force_work")}
                                         for r in result["actual_jump_carriers"]["loaded_deployments"]],
             "unforced_coupling": result["actual_jump_carriers"]["unforced_coupling"]}
    print(json.dumps(brief, indent=2))


if __name__ == "__main__":
    main()
