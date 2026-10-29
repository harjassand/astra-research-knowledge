#!/usr/bin/env python3
"""Exact synthetic conventional behavioral-control fixture; no apparatus data.

Only input/output arrays reach learn_and_design(). Hidden matrices are confined
to the simulator and independent verification. All identities/certificates use
Fraction; QR pivoting only selects a measured square submatrix.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import random
import numpy as np
from scipy.linalg import qr

HERE = Path(__file__).resolve().parent


def transpose(a):
    return [list(x) for x in zip(*a)]


def mm(a, b):
    bt = transpose(b)
    return [[sum((x*y for x, y in zip(ar, bc)), F(0)) for bc in bt] for ar in a]


def mv(a, x):
    return [sum((p*q for p, q in zip(row, x)), F(0)) for row in a]


def inv(a):
    n = len(a)
    v = [list(row) + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if v[i][j]), None)
        if pivot is None:
            raise ValueError("singular")
        v[j], v[pivot] = v[pivot], v[j]
        d = v[j][j]
        v[j] = [x/d for x in v[j]]
        for i in range(n):
            if i != j:
                d = v[i][j]
                v[i] = [x-d*y for x, y in zip(v[i], v[j])]
    return [row[n:] for row in v]


def rank(a):
    v = [list(row) for row in a]
    i = 0
    for j in range(len(v[0])):
        pivot = next((p for p in range(i, len(v)) if v[p][j]), None)
        if pivot is None:
            continue
        v[i], v[pivot] = v[pivot], v[i]
        z = v[i][j]
        v[i] = [x/z for x in v[i]]
        for p in range(i+1, len(v)):
            z = v[p][j]
            v[p] = [x-z*y for x, y in zip(v[p], v[i])]
        i += 1
        if i == len(v):
            break
    return i


def minf(a):
    return max(sum(map(abs, row), F(0)) for row in a)


def vinf(x):
    return max(map(abs, x), default=F(0))


def hankel(x, length):
    return [[x[j+i] for j in range(len(x)-length+1)] for i in range(length)]


def columns(a, indices):
    return [[row[j] for j in indices] for row in a]


def data_blocks(inputs, outputs, lag, horizon):
    u = hankel(inputs, lag+horizon)
    y = hankel(outputs, lag+horizon)
    return u[:lag] + y[:lag] + u[lag:], y[lag:]


def cost(y, u, target, penalty):
    return sum(((x-target)**2 for x in y), F(0)) + penalty*sum((x*x for x in u), F(0))


def learn_and_design(inputs, observed_outputs, lag, horizon, epsilon, target, penalty):
    dmat, yf = data_blocks(inputs, observed_outputs, lag, horizon)
    d = 2*lag+horizon
    _, _, piv = qr(np.array(dmat, dtype=float), pivoting=True)
    indices = [int(j) for j in piv[:d]]
    square = columns(dmat, indices)
    square_inv = inv(square)
    model = mm(columns(yf, indices), square_inv)
    kappa = minf(square_inv)
    radius = d*epsilon*kappa
    assert radius < 1
    model_error = d*epsilon*(1+minf(model))*kappa/(1-radius)
    past = list(inputs[-lag:]) + list(observed_outputs[-lag:])
    f = mv([row[:2*lag] for row in model], past)
    response = [row[2*lag:] for row in model]
    rt = transpose(response)
    h = mm(rt, response)
    h = [[x + (penalty if i == j else 0) for j, x in enumerate(row)] for i, row in enumerate(h)]
    rhs = mv(rt, [target-z for z in f])
    optimum = mv(inv(h), rhs)
    assert vinf(optimum) < 1  # Therefore also the exact box-constrained optimum.
    # Execute a literal finite-resolution waveform, rather than the huge rational
    # minimizer. The input interface is assumed exact on this declared grid.
    control = [F(round(u*2**16), 2**16) for u in optimum]
    assert vinf([u-v for u,v in zip(control, optimum)]) <= F(1,2**17)
    prediction = [x+y for x,y in zip(f, mv(response, control))]
    zmax = max(F(1), vinf(past))
    output_error = model_error*zmax + (minf(model)+model_error)*epsilon
    # Task-specific bound, avoiding a loose uniform prediction-magnitude bound.
    candidate_cost_error = 2*output_error*sum((abs(y-target) for y in prediction), F(0)) + horizon*output_error**2
    baseline_cost_error = 2*output_error*sum((abs(y-target) for y in f), F(0)) + horizon*output_error**2
    return {
        "selected_columns": indices, "square_inverse_norm": kappa,
        "neumann_radius": radius, "model": model, "model_error": model_error,
        "control": control, "unrounded_optimum": optimum,
        "prediction": prediction, "baseline_prediction": f,
        "output_error": output_error,
        "predicted_cost": cost(prediction, control, target, penalty),
        "predicted_baseline_cost": cost(f, [F(0)]*horizon, target, penalty),
        "candidate_cost_error": candidate_cost_error,
        "baseline_cost_error": baseline_cost_error,
    }


def simulate(x, controls):
    a = [[F(3,4), F(1,8)], [F(1,8), F(1,2)]]
    b = [F(1,4), F(0)]
    out = []
    for u in controls:
        x = [v+w*u for v,w in zip(mv(a, x), b)]
        out.append(x[0])  # Read only first temperature, after the physical call.
    return x, out


def numeric(x):
    if isinstance(x, F):
        return float(x)
    if isinstance(x, list):
        return [numeric(v) for v in x]
    if isinstance(x, dict):
        return {k:numeric(v) for k,v in x.items()}
    return x


def rational(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, list):
        return [rational(v) for v in x]
    if isinstance(x, dict):
        return {k:rational(v) for k,v in x.items()}
    return x


def main():
    lag, horizon, ncal = 2, 6, 40
    rng = random.Random(20261029)
    inputs = [F(rng.choice([-1,1])) for _ in range(ncal)]
    initial = [F(1,3), F(-1,4)]
    current, outputs = simulate(initial, inputs)
    epsilon, target, penalty = F(1,10**6), F(2,5), F(1,20)
    noise = [epsilon*F(rng.choice([-1,0,1])) for _ in outputs]
    measured = [y+e for y,e in zip(outputs, noise)]
    clean = learn_and_design(inputs, outputs, lag, horizon, F(0), target, penalty)
    fitted = learn_and_design(inputs, measured, lag, horizon, epsilon, target, penalty)
    true_d, true_yf = data_blocks(inputs, outputs, lag, horizon)
    assert rank(hankel(inputs, 2*lag+horizon)) == 2*lag+horizon
    assert rank(true_d) == 2*lag+horizon
    assert mm(clean["model"], true_d) == true_yf
    _, true_clean = simulate(current, clean["control"])
    assert true_clean == clean["prediction"]
    _, true_fitted = simulate(current, fitted["control"])
    _, true_base = simulate(current, [F(0)]*horizon)
    actual_model_error = minf([[x-y for x,y in zip(a,b)] for a,b in zip(clean["model"], fitted["model"])])
    actual_output_error = vinf([x-y for x,y in zip(true_fitted, fitted["prediction"])])
    assert actual_model_error <= fitted["model_error"]
    assert actual_output_error <= fitted["output_error"]
    true_cost = cost(true_fitted, fitted["control"], target, penalty)
    true_base_cost = cost(true_base, [F(0)]*horizon, target, penalty)
    cert_improvement = fitted["predicted_baseline_cost"]-fitted["baseline_cost_error"]-fitted["predicted_cost"]-fitted["candidate_cost_error"]
    assert cert_improvement > 0
    assert true_base_cost-true_cost >= cert_improvement
    assert all(u not in inputs for u in fitted["control"])
    raw = {
        "kind": "synthetic rational trajectory; not experimental measurements",
        "input": inputs, "true_readout_for_verification_only": outputs,
        "observed_readout": measured, "bounded_sensor_error": noise,
        "lag": lag, "horizon": horizon, "sensor_error_bound": epsilon,
        "target": target, "input_quadratic_penalty": penalty,
        "no_hidden_state_or_matrices_given_to_designer": True,
        "data_selected_control": fitted["control"],
        "actuator_grid_denominator": 2**16,
    }
    raw_path = HERE/"BEHAVIORAL_CONTROL_SYNTHETIC_READOUTS.json"
    raw_path.write_text(json.dumps(rational(raw), indent=2)+"\n")
    # Passive hidden-delay pair: y_t = +/-rho u_{t-L}; any prefix t<L is identical.
    delay, gain = ncal+1, F(3,4)
    delay_tests = 0
    for seed in range(16):
        probe = random.Random(seed)
        sequence = [F(probe.choice([-1,0,1])) for _ in range(2*delay+3)]
        plus = [gain*(sequence[t-delay] if t >= delay else 0) for t in range(len(sequence))]
        minus = [-x for x in plus]
        assert plus[:ncal] == minus[:ncal] == [F(0)]*ncal
        assert sum((y*y for y in plus), F(0)) <= sum((u*u for u in sequence), F(0))
        delay_tests += 1
    report = {
        "status": "all exact rational checks passed",
        "calibration_calls": ncal, "calibration_visible_reads": ncal,
        "hidden_state_reset_count": 0, "future_calls": horizon,
        "behavioral_lag": lag, "pe_order_and_rank": 2*lag+horizon,
        "selected_columns": fitted["selected_columns"],
        "sensor_error_bound": epsilon,
        "square_inverse_infinity_norm": fitted["square_inverse_norm"],
        "neumann_radius": fitted["neumann_radius"],
        "certified_predictor_infinity_error": fitted["model_error"],
        "actual_predictor_infinity_error": actual_model_error,
        "certified_future_output_max_error": fitted["output_error"],
        "actual_future_output_max_error": actual_output_error,
        "designed_control": fitted["control"],
        "actuator_grid_denominator": 2**16,
        "true_future_output": true_fitted,
        "predicted_cost": fitted["predicted_cost"],
        "true_cost": true_cost,
        "true_zero_input_baseline_cost": true_base_cost,
        "certified_cost_improvement": cert_improvement,
        "actual_cost_improvement": true_base_cost-true_cost,
        "designed_each_amplitude_abs_below_one": True,
        "designed_each_amplitude_absent_from_calibration": True,
        "passive_delay_pair_exact_checks": delay_tests,
        "synthetic_readouts_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
        "limitations": ["known exact LTI port class and lag are premises", "bounded sensor error is a premise, not acquired here", "no process noise or actuator error in this fixture", "no closed-loop infinite-time guarantee"],
    }
    (HERE/"BEHAVIORAL_CONTROL_CHECKS.json").write_text(json.dumps(numeric(report), indent=2)+"\n")
    print(json.dumps(numeric(report), indent=2))


if __name__ == "__main__":
    main()
