#!/usr/bin/env python3
"""Interface-faithful diagnostic for the active acquisition theorem.

Synthetic data validate an implementation and cost ledger, not the physical
closure assumptions or historical novelty. The learner sees only declared
bounds, bit readings after finite holds, and priced prepared first-exit dwells.
Ground-truth parameters are accessed only inside the oracle and final audit.
"""
from dataclasses import dataclass, asdict
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
SEED = 407031
ETA, RHO = 0.04, 0.1
DELTA_E, DELTA_Q, DELTA_PREP = 0.02, 0.02, 0.01
B0, RCAL, RMIN, RMAX = 30.0, 0.5, 0.5, 2.0
SLEW_SPEED, PIN_SECONDS, CONTEXT_SECONDS, READ_SECONDS = 5.0, 0.005, 0.1, 1e-5
N = 4
EDGES = [(0, 1), (1, 2), (2, 3), (0, 3)]
NEIGHBORS = [sorted(j if i == k else k for k, j in EDGES if i in (k, j)) for i in range(N)]
MENU = {"baseline": np.zeros(N), "protective": np.full(N, -3.0)}


def sig(z):
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


@dataclass
class Ledger:
    local_bit_reads: int = 0
    energy_hold_seconds: float = 0.0
    operating_dwell_seconds: float = 0.0
    forced_preparations: int = 0
    prepared_event_contexts: int = 0
    context_settings: int = 0
    field_commands: int = 0
    commanded_field_travel: float = 0.0
    realized_field_travel: float = 0.0
    commanded_max_amplitude: float = 0.0
    realized_max_amplitude: float = 0.0
    max_dwell: float = 0.0


class LocalOracle:
    """Only this class owns the hidden h,J and field-dependent clock."""
    def __init__(self):
        self._h = np.full(N, -28.0)
        self._J = {e: 8.0 for e in EDGES}
        self._rng = np.random.default_rng(SEED)
        self._state = 0  # arbitrary state; never an equilibrium reset
        self._field = 0.0
        self._realized_field = 0.0
        self.ledger = Ledger()

    def _ell(self, i, context):
        return self._h[i] + sum(self._J[tuple(sorted((i, j)))] * b for j, b in zip(NEIGHBORS[i], context))

    def _clock(self, i, context, field):
        # Explicitly varies across neighbor contexts AND applied fields.
        return 0.8 + 0.1 * i + 0.08 * sum(context) + 0.2 * math.sin(field) ** 2 + 0.03 * abs(field) / (1 + abs(field))

    def set_context(self, i, context):
        self.ledger.context_settings += 1
        self._i, self._context = i, tuple(context)

    def set_bias(self, command):
        self.ledger.field_commands += 1
        self.ledger.commanded_field_travel += abs(command - self._field)
        self._field = float(command)
        self.ledger.commanded_max_amplitude = max(self.ledger.commanded_max_amplitude, abs(command))
        # Unknown, stable readback error bounded by 0.001 < ETA/16.
        error = 0.001 * math.sin(1 + self._i + 2 * sum(self._context))
        realized = self._field + error
        self.ledger.realized_field_travel += abs(realized - self._realized_field)
        self._realized_field = realized
        self.ledger.realized_max_amplitude = max(self.ledger.realized_max_amplitude, abs(self._realized_field))

    def held_readings_mean(self, n, spacing):
        q = sig(self._ell(self._i, self._context) + self._realized_field)
        a = self._clock(self._i, self._context, self._realized_field)
        retain = math.exp(-a * (spacing + READ_SECONDS))
        total = 0
        # Exact 2-state transition kernel: retain previous state, or refresh.
        # Batched last-refresh indices preserve all within-block dependence.
        left = n
        while left:
            size = min(left, 500_000)
            refresh = self._rng.random(size) >= retain
            fresh = (self._rng.random(size) < q).astype(np.uint8)
            indices = np.maximum.accumulate(np.where(refresh, np.arange(size), -1))
            values = np.concatenate((np.array([self._state], dtype=np.uint8), fresh))
            observed = values[indices + 1]
            total += int(observed.sum())
            self._state = int(observed[-1])
            left -= size
        self.ledger.local_bit_reads += n
        self.ledger.energy_hold_seconds += n * spacing
        return total / n

    def prepared_first_exit_sum(self, i, context, u, initial_bit, k, tick, cap):
        self.set_context(i, context)
        self.ledger.prepared_event_contexts += 1
        self.ledger.field_commands += 1
        self.ledger.commanded_field_travel += abs(u - self._field)
        self.ledger.realized_field_travel += abs(u - self._realized_field)
        self._field = self._realized_field = u
        # Operating command is exactly calibrated in this diagnostic.
        rate = self._clock(i, context, u) * sig((1 - 2 * initial_bit) * (self._ell(i, context) + u))
        dwells = self._rng.exponential(1 / rate, k)
        self.ledger.forced_preparations += k
        self.ledger.operating_dwell_seconds += float(dwells.sum())
        self.ledger.max_dwell = max(self.ledger.max_dwell, float(dwells.max()))
        if np.any(dwells > cap):
            raise RuntimeError("Capped dwell: certificate correctly aborts")
        ticks = np.rint(dwells / float(tick)).astype(np.int64)
        return int(ticks.sum()) * tick

    def audit(self, learned_h, learned_J, learned_rates, learned_probabilities):
        # Called only after inference. No truth is passed to the learner.
        h_error = max(abs(learned_h[i] - self._h[i]) for i in range(N))
        j_error = max(abs(learned_J[e] - self._J[e]) for e in EDGES)
        ell_error = 0.0
        rate_error, p_true = {}, {}
        for name, u in MENU.items():
            worst = 0.0
            for i in range(N):
                for context in product((0, 1), repeat=len(NEIGHBORS[i])):
                    ell_hat = learned_h[i] + sum(learned_J[tuple(sorted((i, j)))] * b for j, b in zip(NEIGHBORS[i], context))
                    ell_error = max(ell_error, abs(ell_hat - self._ell(i, context)))
                    for bit in (0, 1):
                        rate = self._clock(i, context, u[i]) * sig((1 - 2 * bit) * (self._ell(i, context) + u[i]))
                        hat = learned_rates[(name, i, context, bit)]
                        worst = max(worst, abs(math.log(float(hat) / rate)))
            rate_error[name] = worst
            p_true[name] = enumerate_failure_probability(self._h + u, self._J)
        return {"max_node_log_factor_error": h_error,
                "max_pair_log_factor_error": j_error,
                "max_conditional_logit_error": ell_error,
                "max_rate_log_errors": rate_error,
                "true_failure_probabilities": p_true,
                "log_probability_errors": {name: abs(math.log(learned_probabilities[name] / p_true[name])) for name in MENU},
                "baseline_independent_isolated_approximation": sig(-28.0) ** N,
                "baseline_correlation_multiplier_over_isolated_independence": p_true["baseline"] / (sig(-28.0) ** N)}


def enumerate_failure_probability(h, J):
    logs = []
    for x in product((0, 1), repeat=N):
        logs.append(sum(h[i] * x[i] for i in range(N)) + sum(j * x[i] * x[k] for (i, k), j in J.items()))
    # Visible network has four parallel edges, so disconnection is all ones.
    peak = max(logs)
    return math.exp(logs[-1] - peak) / sum(math.exp(z - peak) for z in logs)


def factor_from_estimate(value):
    # Exact binary representation of the floating exp approximation, recorded
    # as a rational factor. This diagnostic is not an interval-arithmetic proof.
    return Fraction.from_float(math.exp(value))


def main():
    oracle = LocalOracle()
    D, d = N + 2 * len(EDGES), max(map(len, NEIGHBORS))
    j0 = math.ceil(math.log2(max(2, 2 * B0))) + 1
    n0 = math.ceil(512 * math.log(4 * D * j0 / DELTA_E))
    nf = math.ceil(512 * ETA ** -2 * math.log(4 * D / DELTA_E))
    s0, sf = math.log(32) / RCAL, math.log(32 / ETA) / RCAL
    estimates, calibration_rows = {}, []
    for i in range(N):
        contexts = [(0,) * len(NEIGHBORS[i])]
        contexts += [tuple(int(j == k) for j in range(len(NEIGHBORS[i]))) for k in range(len(NEIGHBORS[i]))]
        for context in contexts:
            oracle.set_context(i, context)
            lo, hi, stages = -B0, B0, 0
            while hi - lo > 1:
                mid = (lo + hi) / 2
                oracle.set_bias(-mid)
                qbar = oracle.held_readings_mean(n0, s0)
                stages += 1
                if qbar < 3 / 8:
                    hi = mid
                elif qbar > 5 / 8:
                    lo = mid
                else:
                    break
            else:
                mid = (lo + hi) / 2
                oracle.set_bias(-mid)
            qbar = oracle.held_readings_mean(nf, sf)
            ell = math.log(qbar / (1 - qbar)) + mid
            estimates[(i, context)] = ell
            calibration_rows.append({"node": i, "context": list(context), "stages": stages, "compensating_command": -mid,
                                     "final_observed_fraction": qbar, "estimated_logit": ell})
    node_factors = [factor_from_estimate(estimates[(i, (0,) * len(NEIGHBORS[i]))]) for i in range(N)]
    pair_factors = {}
    for i, j in EDGES:
        ci = tuple(int(n == j) for n in NEIGHBORS[i])
        cj = tuple(int(n == i) for n in NEIGHBORS[j])
        ji = estimates[(i, ci)] - estimates[(i, (0,) * len(NEIGHBORS[i]))]
        jj = estimates[(j, cj)] - estimates[(j, (0,) * len(NEIGHBORS[j]))]
        pair_factors[(i, j)] = factor_from_estimate((ji + jj) / 2)
    h_hat = np.array([math.log(float(f)) for f in node_factors])
    J_hat = {e: math.log(float(f)) for e, f in pair_factors.items()}
    E, a, b = D * ETA, (1 + 2 * d) * ETA, RHO + (1 + 2 * d) * ETA
    C = len(MENU) * sum(2 ** len(s) for s in NEIGHBORS)
    k = math.ceil(256 * RHO ** -2 * math.log(8 * C / DELTA_Q))
    cap = 3 / RMIN * math.log(4 * C * k / DELTA_Q)
    tick = Fraction.from_float(RHO / (128 * RMAX))
    rates = {}
    for name, u in MENU.items():
        for i in range(N):
            for context in product((0, 1), repeat=len(NEIGHBORS[i])):
                odds = node_factors[i] * factor_from_estimate(u[i])
                for j, active in zip(NEIGHBORS[i], context):
                    if active:
                        odds *= pair_factors[tuple(sorted((i, j)))]
                initial = 0 if odds >= 1 else 1
                total = oracle.prepared_first_exit_sum(i, context, u[i], initial, k, tick, cap)
                lam = Fraction(k, 1) / total
                rates[(name, i, context, initial)] = lam
                rates[(name, i, context, 1 - initial)] = lam / odds if initial == 0 else lam * odds
    risk_hat = {name: enumerate_failure_probability(h_hat + u, J_hat) for name, u in MENU.items()}
    checks = {}
    for name, u in MENU.items():
        row_bounds, contrast_checks = [], []
        lower_clock, upper_clock = math.inf, []
        max_logit = 0.0
        for i in range(N):
            logits = {context: h_hat[i] + u[i] + sum(J_hat[tuple(sorted((i, j)))] * x for j, x in zip(NEIGHBORS[i], context))
                      for context in product((0, 1), repeat=len(NEIGHBORS[i]))}
            row = 0.0
            for index, j in enumerate(NEIGHBORS[i]):
                influence = 0.0
                for context in logits:
                    other = list(context)
                    other[index] = 1 - other[index]
                    influence = max(influence, abs(sig(logits[context]) - sig(logits[tuple(other)])))
                row += influence + a / 2
            row_bounds.append(row)
            lo, hi = min(logits.values()) - a, max(logits.values()) + a
            max_logit = max(max_logit, abs(lo), abs(hi))
            contrast_checks.append(math.log(sig(lo)) >= 3 * math.log(sig(hi)))
            clocks = [float(rates[(name, i, s, 0)] + rates[(name, i, s, 1)]) for s in logits]
            lower_clock = min(lower_clock, min(clocks) * math.exp(-b))
            upper_clock.append(max(clocks) * math.exp(b))
        alpha = 1 - max(row_bounds)
        gamma = alpha * lower_clock
        zeta = 0.01
        prep_time = (1.5 * N * (max_logit + math.log(2)) + math.log(1 / zeta)) / gamma
        prep_cap = math.ceil(math.log(1 / DELTA_PREP) / math.log(8 / 5))
        risk_interval = [risk_hat[name] * math.exp(-2 * E), risk_hat[name] * math.exp(2 * E)]
        checks[name] = {"Dobrushin_row_upper_bounds": row_bounds, "alpha_lower_bound": alpha,
                        "fixed_log_contrast_c": 3, "contrast_passes": all(contrast_checks),
                        "clock_lower_bound": lower_clock, "gap_lower_bound": gamma,
                        "uniformization_rate": 2 * sum(upper_clock), "safe_mass_check": risk_interval[1] <= 0.5,
                        "static_failure_interval": risk_interval, "prep_zeta": zeta,
                        "prep_hold_seconds": prep_time, "prep_attempt_cap": prep_cap,
                        "prep_inspection_seconds_per_attempt": N * READ_SECONDS,
                        "prep_max_elapsed_seconds": prep_cap * (prep_time + N * READ_SECONDS),
                        "CDF_model_log_distortion_bound": 6 * E + b}
    audit = oracle.audit(h_hat, J_hat, rates, risk_hat)
    assert audit["max_node_log_factor_error"] <= ETA
    assert audit["max_pair_log_factor_error"] <= 2 * ETA
    assert audit["max_conditional_logit_error"] <= a
    assert all(v <= b for v in audit["max_rate_log_errors"].values())
    assert all(v <= 2 * E for v in audit["log_probability_errors"].values())
    assert all(v["contrast_passes"] and v["alpha_lower_bound"] > 0 and v["safe_mass_check"] for v in checks.values())
    selected = min(checks, key=lambda name: checks[name]["static_failure_interval"][1])
    assert checks["protective"]["static_failure_interval"][1] < checks["baseline"]["static_failure_interval"][0]
    ledger = asdict(oracle.ledger)
    ledger["pin_elapsed_seconds"] = ledger["forced_preparations"] * PIN_SECONDS
    ledger["context_elapsed_seconds"] = ledger["context_settings"] * CONTEXT_SECONDS
    ledger["available_constant_speed_slew_seconds"] = ledger["realized_field_travel"] / SLEW_SPEED
    ledger["event_detector_processing_seconds"] = ledger["forced_preparations"] * READ_SECONDS
    ledger["local_read_seconds"] = ledger["local_bit_reads"] * READ_SECONDS
    ledger["summed_nominal_experiment_seconds"] = sum(ledger[key] for key in (
        "energy_hold_seconds", "operating_dwell_seconds", "pin_elapsed_seconds", "context_elapsed_seconds", "available_constant_speed_slew_seconds", "local_read_seconds", "event_detector_processing_seconds"))
    result = {"description": "Synthetic interface diagnostic; no actual physical experiment; no rare global-event observations used.",
              "seed": SEED, "N": N, "pair_interactions": len(EDGES), "degree": d, "energy_contexts": D,
              "kinetic_contexts": C, "eta": ETA, "rho": RHO, "coarse_reads_per_stage": n0,
              "fine_reads_per_context": nf, "dwells_per_kinetic_context": k, "dwell_cap_seconds": cap,
              "factor_log_error_budget": E, "conditional_logit_error_budget": a, "rate_log_error_budget": b,
              "ledger": ledger,
              "selected_preparation_planned_budget_seconds": checks[selected]["prep_max_elapsed_seconds"],
              "selected_preparation_executed": False,
              "learned_node_parameters": h_hat.tolist(),
              "learned_pair_parameters": {str(e): j for e, j in J_hat.items()},
              "calibration": calibration_rows, "learned_failure_probabilities": risk_hat,
              "certification_diagnostics": checks, "selected_static_action": selected, "audit": audit,
              "limitations": ["Floating arithmetic checks are diagnostics, not certified interval arithmetic.",
                              "The accepted rare-CDF solver is not reimplemented or benchmarked here.",
                              "No claim that sample constants or elapsed acquisition time are practical.",
                              "Physical cell/clamp faithfulness, rate lower bounds and sensor correctness remain assumptions.",
                              "Cell construction, instrument calibration, full menu environment setup, deployment slew and actuator work are unpriced in this synthetic example and must be added to its specified-component time ledger.",
                              "The whole-system preparation budget is calculated, not physically executed.",
                              "Nonconstant context clocks are not assumed attractive; no monotone preparation-exposure bound is invoked."]}
    (ROOT / "diagnostic_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"selected": selected, "true_risks": audit["true_failure_probabilities"],
                      "static_intervals": {name: checks[name]["static_failure_interval"] for name in checks},
                      "ledger": ledger, "audited_max_errors": {key: audit[key] for key in (
                          "max_node_log_factor_error", "max_pair_log_factor_error", "max_conditional_logit_error", "max_rate_log_errors")}}, indent=2))


if __name__ == "__main__":
    main()
