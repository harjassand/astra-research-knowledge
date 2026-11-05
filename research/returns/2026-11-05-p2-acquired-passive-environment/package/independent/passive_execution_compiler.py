#!/usr/bin/env python3
"""Finite rational compiler and verifier for a learned positive memory model.

Emits a piecewise-linear rational path.  Every accepted segment has a rigorous
L-infinity residual certificate for the exact finite exponential kernel.
The scalar endpoint equation is solved by interval bisection, never a floating
nonlinear solve. Coefficients and modal histories have outward rational bounds.

The concrete potential is V'(y)=a*y+b*y^3, a>0, b>=0. Inputs are rational
piecewise-affine forces. The accompanying theorem explains the extension to
other known potentials/forces with paid enclosing evaluation algorithms.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
import json
from math import ceil
from pathlib import Path
from time import perf_counter

Interval = tuple[Q, Q]


def pow2(k: int) -> Q:
    return Q(1 << k) if k >= 0 else Q(1, 1 << (-k))


def ceil_log2(q: Q) -> int:
    assert q > 0
    k = q.numerator.bit_length() - q.denominator.bit_length()
    while pow2(k) < q:
        k += 1
    while pow2(k - 1) >= q:
        k -= 1
    return k


def floor_dyadic(q: Q, bits: int) -> Q:
    d = 1 << bits
    return Q((q.numerator * d) // q.denominator, d)


def ceil_dyadic(q: Q, bits: int) -> Q:
    return -floor_dyadic(-q, bits)


def nearest_dyadic(q: Q, bits: int) -> Q:
    return floor_dyadic(q + pow2(-bits - 1), bits)


def add(a: Interval, b: Interval) -> Interval:
    return a[0] + b[0], a[1] + b[1]


def scale(a: Interval, s: Q) -> Interval:
    x, y = a[0] * s, a[1] * s
    return min(x, y), max(x, y)


def multiply(a: Interval, b: Interval) -> Interval:
    values = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return min(values), max(values)


def maxabs(a: Interval) -> Q:
    return max(abs(a[0]), abs(a[1]))


def rational_payload_bits(q: Q) -> int:
    return q.numerator.bit_length() + q.denominator.bit_length()


def interval_payload_bits(states: list[Interval]) -> int:
    return sum(rational_payload_bits(q) for interval in states for q in interval)


def outward(a: Interval, bits: int, low: Q | None = None,
            high: Q | None = None) -> Interval:
    lo, hi = floor_dyadic(a[0], bits), ceil_dyadic(a[1], bits)
    if low is not None:
        lo = max(lo, low)
    if high is not None:
        hi = min(hi, high)
    assert lo <= hi
    return lo, hi


def exp_neg_bounds(x: Q, bits: int) -> Interval:
    assert x >= 0
    if x == 0:
        return Q(1), Q(1)
    if x >= bits + 2:
        return Q(0), pow2(-bits - 2)
    s = max(0, ceil_log2(x))
    u = x / pow2(s)
    term, total = Q(1), Q(1)
    target = pow2(-bits - s - 3)
    n = 0
    while True:
        n += 1
        previous = total
        term *= u / n
        total += (-term if n % 2 else term)
        lo, hi = (total, previous) if n % 2 else (previous, total)
        if term <= target:
            break
    for _ in range(s):
        lo, hi = lo * lo, hi * hi
    assert 0 <= lo <= hi <= 1 and hi - lo <= pow2(-bits)
    return lo, hi


def psi_bounds(x: Q, bits: int) -> Interval:
    """Bounds for (1-exp(-x))/x, continuously defined as 1 at zero."""
    assert x >= 0
    if x == 0:
        return Q(1), Q(1)
    if x > 1:
        lo, hi = exp_neg_bounds(x, bits)
        return (1 - hi) / x, (1 - lo) / x
    term, total = Q(1), Q(1)
    n = 0
    while True:
        n += 1
        previous = total
        term *= x / (n + 1)
        total += (-term if n % 2 else term)
        lo, hi = (total, previous) if n % 2 else (previous, total)
        if term <= pow2(-bits):
            assert 0 <= lo <= hi <= 1
            return lo, hi


def coefficients(rate: Q, h: Q, bits: int) -> tuple[Interval, Interval]:
    if rate == 0:
        return (Q(1), Q(1)), (Q(1), Q(1))
    x = rate * h
    return (outward(exp_neg_bounds(x, bits + 4), bits, Q(0), Q(1)),
            outward(psi_bounds(x, bits + 4), bits, Q(0), Q(1)))


@dataclass(frozen=True)
class Potential:
    linear: Q
    cubic: Q

    def __post_init__(self):
        assert self.linear > 0 and self.cubic >= 0

    @property
    def mu(self) -> Q:
        return self.linear

    def prime(self, y: Q) -> Q:
        return self.linear * y + self.cubic * y * y * y

    def lipschitz(self, lo: Q, hi: Q) -> Q:
        return self.linear + 3 * self.cubic * max(abs(lo), abs(hi)) ** 2


@dataclass(frozen=True)
class ForcePiece:
    start: Q
    end: Q
    initial: Q
    slope: Q

    def value(self, t: Q) -> Q:
        assert self.start <= t <= self.end
        return self.initial + self.slope * (t - self.start)

    def amplitude(self) -> Q:
        return max(abs(self.initial), abs(self.value(self.end)))


def make_plan(model: list[tuple[Q, Q]], potential: Potential,
              force: list[ForcePiece], x_ref: Q, c: Q,
              force_budget: Q, target: Q) -> dict:
    assert target > 0 and force_budget >= 0
    assert all(rate >= 0 and weight > 0 for rate, weight in model)
    assert force and force[0].start == 0
    assert all(piece.end > piece.start and piece.amplitude() <= force_budget
               for piece in force)
    assert all(force[i].end == force[i + 1].start for i in range(len(force) - 1))
    B = sum((weight for _, weight in model), Q(0))
    C = sum((rate * weight for rate, weight in model), Q(0))
    A0 = abs(potential.prime(x_ref) - c)
    R = (force_budget + A0 + target) / potential.mu
    lo, hi = x_ref - R, x_ref + R
    L = potential.lipschitz(lo, hi)
    tau = target / 4
    U = force_budget + A0 + (L + 2 * B) * R + tau
    Lf = max(abs(piece.slope) for piece in force)
    variation = (L + B) * U + Lf + 2 * R * C
    hmax = target / (2 * variation) if variation else force[-1].end
    levels = [max(0, ceil_log2((piece.end - piece.start) / hmax))
              for piece in force]
    maximum_steps = sum(1 << k for k in levels)
    if B:
        eta_coefficient = tau / (256 * B * R * maximum_steps)
        eta_round = tau / (64 * B * maximum_steps)
        coefficient_bits = max(1, ceil_log2(4 / eta_coefficient))
        state_bits = max(1, ceil_log2(2 / eta_round))
    else:
        eta_coefficient = eta_round = Q(1)
        coefficient_bits = state_bits = 4
    return dict(B=B, C=C, A0=A0, R=R, low=lo, high=hi, L=L, tau=tau,
                U=U, Lf=Lf, variation=variation, hmax=hmax, levels=levels,
                maximum_steps=maximum_steps, eta_coefficient=eta_coefficient,
                eta_round=eta_round, coefficient_bits=coefficient_bits,
                state_bits=state_bits, target=target)


def endpoint_bisection(y0: Q, h: Q, states: list[Interval],
                       coeffs: list[tuple[Interval, Interval]],
                       model: list[tuple[Q, Q]], potential: Potential,
                       f_end: Q, c: Q, plan: dict) -> tuple[Q, int, Q, int]:
    # These two sums are the only mode-dependent work inside the scalar solve.
    history, psi_sum = (Q(0), Q(0)), (Q(0), Q(0))
    for (_, w), q, (a, psi) in zip(model, states, coeffs):
        history = add(history, scale(multiply(a, q), w))
        psi_sum = add(psi_sum, scale(psi, w))
    lo, hi = plan["low"], plan["high"]
    Ch = 1 / h + plan["L"] + plan["B"]
    max_iterations = max(1, ceil_log2(8 * plan["R"] * Ch / plan["tau"])) + 3
    largest_residual_payload = 0
    for iteration in range(1, max_iterations + 1):
        y1 = (lo + hi) / 2
        dy = y1 - y0
        memory = add(history, scale(psi_sum, dy))
        base = dy / h + potential.prime(y1) - f_end - c
        g = base + memory[0], base + memory[1]
        largest_residual_payload = max(largest_residual_payload,
                                       rational_payload_bits(g[0]),
                                       rational_payload_bits(g[1]))
        assert g[1] - g[0] <= plan["tau"] / 8
        if maxabs(g) <= plan["tau"] / 2:
            return y1, iteration, maxabs(g), largest_residual_payload
        if g[0] > 0:
            hi = y1
        elif g[1] < 0:
            lo = y1
        else:
            raise AssertionError("Narrow interval straddles zero but was not accepted")
    raise AssertionError("Proved bisection bound exceeded")


def update_states(y0: Q, y1: Q, x_ref: Q, states: list[Interval],
                  coeffs: list[tuple[Interval, Interval]],
                  model: list[tuple[Q, Q]], bits: int, R: Q) -> list[Interval]:
    out = []
    for (rate, _), old, (a, psi) in zip(model, states, coeffs):
        if rate == 0:
            out.append((y1 - x_ref, y1 - x_ref))
        else:
            q = add(multiply(a, old), scale(psi, y1 - y0))
            out.append(outward(q, bits, -2 * R, 2 * R))
    return out


def segment_certificate(y0: Q, y1: Q, h: Q, old: list[Interval],
                        new: list[Interval], model: list[tuple[Q, Q]],
                        potential: Potential, f_end: Q, c: Q,
                        L: Q, Lf: Q) -> tuple[Q, Q]:
    v = (y1 - y0) / h
    base = v + potential.prime(y1) - f_end - c
    endpoint = Q(base), Q(base)
    memory_variation = Q(0)
    for (_, w), q0, q1 in zip(model, old, new):
        endpoint = add(endpoint, scale(q1, w))
        # Each exact mode is monotone during a constant-slope segment.
        change = q1[0] - q0[1], q1[1] - q0[0]
        memory_variation += w * maxabs(change)
    ep = maxabs(endpoint)
    total = ep + L * abs(y1 - y0) + Lf * h + memory_variation
    return total, ep


def compile_path(model: list[tuple[Q, Q]], potential: Potential,
                 force: list[ForcePiece], x_ref: Q, c: Q,
                 force_budget: Q, target: Q) -> tuple[dict, list[tuple[Q, Q]]]:
    started = perf_counter()
    plan = make_plan(model, potential, force, x_ref, c, force_budget, target)
    states = [(Q(0), Q(0)) for _ in model]
    knots = [(Q(0), x_ref)]
    cache = {}
    attempts = rejections = bisections = 0
    coefficient_batches = 0
    maximum_state_payload = interval_payload_bits(states)
    maximum_coefficient_payload = maximum_bisection_payload = 0
    maximum_residual = maximum_endpoint = maximum_speed = Q(0)
    max_state_width = Q(0)
    for piece_index, piece in enumerate(force):
        t = piece.start
        level = 0
        while t < piece.end:
            h = (piece.end - piece.start) / (1 << level)
            assert h <= piece.end - t
            if h not in cache:
                # Old dyadic levels will not be used again within this piece.
                # Retain only the current coefficient bank for O(m) workspace.
                cache.clear()
                cache[h] = [coefficients(rate, h, plan["coefficient_bits"])
                            for rate, _ in model]
                coefficient_batches += 1
                maximum_coefficient_payload = max(maximum_coefficient_payload,
                    sum(interval_payload_bits([a, psi]) for a, psi in cache[h]))
                for a, psi in cache[h]:
                    assert a[1] - a[0] <= 2 * plan["eta_coefficient"]
                    assert psi[1] - psi[0] <= 2 * plan["eta_coefficient"]
            coeffs = cache[h]
            y0 = knots[-1][1]
            y1, iterations, _, scalar_payload = endpoint_bisection(
                y0, h, states, coeffs, model, potential, piece.value(t + h), c, plan)
            new = update_states(y0, y1, x_ref, states, coeffs, model,
                                plan["state_bits"], plan["R"])
            bound, ep = segment_certificate(y0, y1, h, states, new, model,
                                            potential, piece.value(t + h), c,
                                            plan["L"], abs(piece.slope))
            attempts += 1
            bisections += iterations
            maximum_bisection_payload = max(maximum_bisection_payload, scalar_payload)
            if bound > target:
                rejections += 1
                level += 1
                assert level <= plan["levels"][piece_index], "Finite step guarantee failed"
                continue
            v = abs((y1 - y0) / h)
            assert v <= plan["U"]
            assert plan["low"] <= y1 <= plan["high"]
            states = new
            maximum_state_payload = max(maximum_state_payload, interval_payload_bits(states))
            t += h
            knots.append((t, y1))
            maximum_residual = max(maximum_residual, bound)
            maximum_endpoint = max(maximum_endpoint, ep)
            maximum_speed = max(maximum_speed, v)
            max_state_width = max([max_state_width] + [hi - lo for lo, hi in states])
            if plan["B"]:
                assert max_state_width <= plan["tau"] / (16 * plan["B"])
    assert len(knots) - 1 <= plan["maximum_steps"]
    result = {
        "plan": {k: str(v) if isinstance(v, Q) else v for k, v in plan.items()},
        "accepted_steps": len(knots) - 1, "attempted_steps": attempts,
        "rejected_steps": rejections, "bisection_iterations": bisections,
        "coefficient_step_sizes": coefficient_batches,
        "mode_loop_visits_for_sums_updates_certificates": 3 * len(model) * attempts,
        "computed_coefficient_pairs": len(model) * coefficient_batches,
        "maximum_online_modal_interval_integer_payload_bits": maximum_state_payload,
        "maximum_current_coefficient_bank_integer_payload_bits": maximum_coefficient_payload,
        "maximum_single_bisection_residual_rational_payload_bits": maximum_bisection_payload,
        "compiler_residual_bound_exact": str(maximum_residual),
        "compiler_residual_bound": float(maximum_residual),
        "compiler_endpoint_bound_exact": str(maximum_endpoint),
        "actual_maximum_speed_exact": str(maximum_speed),
        "actual_maximum_speed": float(maximum_speed),
        "maximum_modal_interval_width_exact": str(max_state_width),
        "runtime_seconds": perf_counter() - started,
        "all_knots_in_protected_interval": True,
    }
    return result, knots


def verify_path(knots: list[tuple[Q, Q]], model: list[tuple[Q, Q]],
                potential: Potential, force: list[ForcePiece], x_ref: Q, c: Q,
                plan: dict) -> dict:
    """Fresh pass from emitted knots only; none of the compiler states are used."""
    started = perf_counter()
    states = [(Q(0), Q(0)) for _ in model]
    cache = {}
    coefficient_batches = 0
    maximum_state_payload = interval_payload_bits(states)
    maximum_residual = maximum_endpoint = maximum_speed = Q(0)
    piece_index = 0
    assert knots[0] == (Q(0), x_ref)
    assert knots[-1][0] == force[-1].end
    for (t0, y0), (t1, y1) in zip(knots[:-1], knots[1:]):
        while t0 >= force[piece_index].end:
            piece_index += 1
        piece = force[piece_index]
        assert piece.start <= t0 < t1 <= piece.end
        assert plan["low"] <= y0 <= plan["high"]
        assert plan["low"] <= y1 <= plan["high"]
        h = t1 - t0
        if h not in cache:
            cache.clear()
            cache[h] = [coefficients(rate, h, plan["coefficient_bits"] + 8)
                        for rate, _ in model]
            coefficient_batches += 1
        new = update_states(y0, y1, x_ref, states, cache[h], model,
                            plan["state_bits"] + 8, plan["R"])
        bound, ep = segment_certificate(y0, y1, h, states, new, model,
                                        potential, piece.value(t1), c,
                                        plan["L"], abs(piece.slope))
        assert bound <= plan["target"], "Emitted path failed independent residual verification"
        states = new
        maximum_state_payload = max(maximum_state_payload, interval_payload_bits(states))
        maximum_residual = max(maximum_residual, bound)
        maximum_endpoint = max(maximum_endpoint, ep)
        maximum_speed = max(maximum_speed, abs((y1 - y0) / h))
    return {
        "verified_from_emitted_knots": True,
        "verified_residual_Linfinity_exact": str(maximum_residual),
        "verified_residual_Linfinity": float(maximum_residual),
        "verified_endpoint_bound_exact": str(maximum_endpoint),
        "verified_actual_speed_exact": str(maximum_speed),
        "verified_actual_speed": float(maximum_speed),
        "verification_seconds": perf_counter() - started,
        "verification_coefficient_bits": plan["coefficient_bits"] + 8,
        "verification_state_bits": plan["state_bits"] + 8,
        "mode_loop_visits_for_updates_certificates": 2 * len(model) * (len(knots) - 1),
        "computed_coefficient_pairs": len(model) * coefficient_batches,
        "maximum_online_modal_interval_integer_payload_bits": maximum_state_payload,
    }


def ceil_decimal(q: Q, digits: int) -> Q:
    scale10 = 10 ** digits
    return Q(ceil(q * scale10), scale10)


def main():
    parser = argparse.ArgumentParser()
    here = Path(__file__).resolve().parent
    parser.add_argument("--source", default=str(here.parent / "bridge" / "physical_bridge_results.json"))
    parser.add_argument("--target", default="1/1000")
    parser.add_argument("--output", default=str(here / "passive_compiler_results.json"))
    parser.add_argument("--path-output", default=str(here / "passive_compiler_path.json"))
    args = parser.parse_args()
    raw = Path(args.source).read_bytes()
    source = json.loads(raw, parse_float=Q)
    # This main() is a named fixture adapter, not a parser for arbitrary physical
    # source schemas. The general compile_path interface takes its inputs
    # explicitly. This source's fitted poles/weights already use B=T=1 units.
    assert source["declared_B"] == 1
    assert source["horizon"] == 1
    assert source["mu"] == 1
    assert source["deployment"]["force_amplitude_bound"] == Q(2, 5)
    # Only the already learned model and declared interface receipts enter.
    model = [(Q(m["pole"]), Q(m["weight"])) for m in source["fit"]["model"]]
    assert sum((weight for _, weight in model), Q(0)) <= 1
    potential = Potential(Q(1), Q(3, 20))
    measured_c = source["initialization"]["measured_bath_force"]
    c = nearest_dyadic(measured_c, 40)
    c_rounding_error = abs(c - measured_c)
    horizon = Q(source["horizon"])
    force = [ForcePiece(Q(0), horizon, Q(7, 20), Q(0))]
    x_ref, F, target = Q(0), Q(2, 5), Q(args.target)
    compiled, knots = compile_path(model, potential, force, x_ref, c, F, target)
    plan = make_plan(model, potential, force, x_ref, c, F, target)
    path_payload = {
        "meaning": "rational knots defining the emitted continuous piecewise-linear path",
        "knots": [[str(t), str(y)] for t, y in knots],
        "x_ref": str(x_ref), "encoded_bath_force": str(c),
        "potential_derivative": {"linear": "1", "cubic": "3/20"},
        "force_pieces": [{"start": str(p.start), "end": str(p.end),
                          "initial": str(p.initial), "slope": str(p.slope)} for p in force],
        "model": [{"pole": str(rate), "weight": str(w)} for rate, w in model],
    }
    # Write and reload before the independent verification, to check the actual
    # finite output rather than an in-memory solver state.
    path_file = Path(args.path_output)
    path_file.write_text(json.dumps(path_payload, indent=2) + "\n")
    emitted = json.loads(path_file.read_text())
    reloaded_knots = [(Q(t), Q(y)) for t, y in emitted["knots"]]
    verified = verify_path(reloaded_knots, model, potential, force, x_ref, c, plan)
    zeta = Q(source["fit"]["certified_L1_bound_exact"]) + source["smoothing_budget"]
    gamma_original = source["initialization"]["force_forecast_error_bound"]
    gamma = ceil_decimal(gamma_original, 12) + c_rounding_error
    # Deployment starts after the finite trap release/drive rise.  The hold's
    # tracking tube is not its initial-coordinate guarantee.
    initial_delta = ceil_decimal(
        source["initialization"]["deployment_initial_coordinate_bound"], 12)
    velocity = Q(verified["verified_actual_speed_exact"])
    residual = Q(verified["verified_residual_Linfinity_exact"])
    final_bound = max(initial_delta, (zeta * velocity + gamma + residual) / potential.mu)
    knot_integer_bits = sum(t.numerator.bit_length() + t.denominator.bit_length()
                            + y.numerator.bit_length() + y.denominator.bit_length()
                            for t, y in reloaded_knots)
    report = {
        "source_path": str(Path(args.source).resolve()),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "fixture_adapter": {
            "name": "root physical_bridge_results B=T=mu=1 fixture",
            "asserted_declared_B": "1", "asserted_T": "1", "asserted_mu": "1",
            "asserted_force_budget": "2/5",
            "supplied_reference_coordinate": "0",
            "supplied_potential_derivative": "x + (3/20)*x^3",
            "scope": "The source JSON does not encode an arbitrary potential; this adapter supplies and labels the fixed physical-fixture potential.",
            "initial_coordinate_bound_source": "initialization.deployment_initial_coordinate_bound (after finite release)",
        },
        "learned_modes": len(model), "horizon_exact": str(horizon),
        "encoded_bath_force_exact": str(c),
        "bath_force_encoding_error_exact": str(c_rounding_error),
        "force_budget_exact": str(F), "queried_force_exact": "7/20",
        "numerical_target_exact": str(target),
        "compiler": compiled, "independent_verifier": verified,
        "physical_join": {
            "conditional_on_supplied_acquisition_and_initialization_event": True,
            "kernel_L1_exact": str(zeta),
            "initial_force_error_with_encoding_exact": str(gamma),
            "physical_initial_coordinate_error_exact": str(initial_delta),
            "actual_numerical_path_speed_exact": str(velocity),
            "numerical_residual_exact": str(residual),
            "trajectory_sup_error_exact": str(final_bound),
            "trajectory_sup_error": float(final_bound),
            "mu_exact": str(potential.mu),
        },
        "output_path": str(path_file.resolve()),
        "output_sha256": hashlib.sha256(path_file.read_bytes()).hexdigest(),
        "output_knots": len(reloaded_knots),
        "output_integer_payload_bits": knot_integer_bits,
        "output_JSON_bytes": path_file.stat().st_size,
        "arithmetic": "exact rational bisection, outward exponential/psi intervals, finite dyadic state intervals",
        "residual_convention": "rho = y_prime + V_prime(y) + Khat*y_prime - f - c",
        "limitations": [
            "Physical-source acquisition assumptions and its supplied bounds are consumed, not re-proved by this compiler.",
            "No microscopic source modes, BDF trajectory, or source simulation state enters compile_path or verify_path.",
            "The proof covers this emitted piecewise-linear path; exact exponentials are enclosed rather than replaced by unverified floating values.",
            "Stored full path has O(number_of_steps) knots; online model-state memory is O(number_of_modes) at the charged precision.",
        ],
    }
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "modes": len(model), "accepted_steps": compiled["accepted_steps"],
        "rejected_steps": compiled["rejected_steps"],
        "residual": verified["verified_residual_Linfinity"],
        "speed": verified["verified_actual_speed"],
        "physical_sup_bound": float(final_bound),
        "compile_seconds": compiled["runtime_seconds"],
        "verify_seconds": verified["verification_seconds"],
        "path_bytes": path_file.stat().st_size,
    }))


if __name__ == "__main__":
    main()
