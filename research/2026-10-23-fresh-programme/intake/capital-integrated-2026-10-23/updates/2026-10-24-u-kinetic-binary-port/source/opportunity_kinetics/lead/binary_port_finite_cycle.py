"""Finite binary-port CTMC cycle, with an a posteriori interval sign check.

Probability columns; work positive ON. The interval proof certifies a
piecewise-linear periodic probability profile, not the RK4 algorithm.
All physical parameters in the interval stage are exact rationals.
"""

import argparse
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from mpmath import iv


QRAW = [[-3120, 480, 3], [3000, -483, 10], [120, 3, -13]]
QBASE = np.array(QRAW, dtype=float) / 3000
PI = np.array([2083, 13400, 22320], dtype=float) / 37803
PORT = np.array([1.0, 0.0, 0.0])


def rational_solve(matrix, rhs):
    a = [list(row) + [v] for row, v in zip(matrix, rhs)]
    n = len(a)
    for j in range(n):
        pivot = next(k for k in range(j, n) if a[k][j])
        a[j], a[pivot] = a[pivot], a[j]
        d = a[j][j]
        a[j] = [v / d for v in a[j]]
        for k in range(n):
            if k != j:
                d = a[k][j]
                a[k] = [v - d * w for v, w in zip(a[k], a[j])]
    return [row[-1] for row in a]


def exact_friction():
    q = [[F(v, 3000) for v in row] for row in QRAW]
    pi = [F(v, 37803) for v in (2083, 13400, 22320)]
    f = [F(1), F(0), F(0)]
    assert all(sum(q[i][j] for i in range(3)) == 0 for j in range(3))
    assert all(sum(q[i][j] * pi[j] for j in range(3)) == 0 for i in range(3))
    b = [-sum((q[i][j] * pi[j] + pi[i] * q[j][i]) * f[j]
              for j in range(3)) / 2 for i in range(3)]
    invertible = [[q[i][j] + pi[i] for j in range(3)] for i in range(3)]
    first = rational_solve(invertible, b)
    second = rational_solve(invertible, first)
    zeta = sum(f[i] * second[i] for i in range(3))
    assert zeta == -F(29239948720000, 54023012580627)
    return str(zeta)


def generator(h, clock=False):
    if clock:
        # E_i=-h*f_i; source-clock q_ij=q0_ij exp(E_j).
        q = QBASE * np.exp(-h * PORT)[None, :]
        return q
    q = QBASE * np.exp(h * (PORT[:, None] - PORT[None, :]) / 2)
    np.fill_diagonal(q, 0)
    q[np.diag_indices(3)] = -q.sum(axis=0)
    return q


def numeric_profile(steps, amplitude, frequency, clock):
    tau = 2 * math.pi / frequency
    dt = tau / steps
    times = np.linspace(0.0, tau, 2 * steps + 1)
    qs = np.stack([generator(amplitude * math.cos(frequency * t), clock)
                   for t in times])

    def advance(p, k):
        q0, qm, q1 = qs[2 * k:2 * k + 3]
        k1 = q0 @ p
        p2 = p + dt * k1 / 2
        k2 = qm @ p2
        p3 = p + dt * k2 / 2
        k3 = qm @ p3
        p4 = p + dt * k3
        k4 = q1 @ p4
        return p + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6, (p, p2, p3, p4)

    phi = np.eye(3)
    for k in range(steps):
        phi, _ = advance(phi, k)
    p0 = np.linalg.solve(phi - np.eye(3) + np.ones((3, 3)) / 3,
                         np.ones(3) / 3)
    p0 /= p0.sum()
    p = p0.copy()
    profile = [p.copy()]
    ledger = np.zeros(4)
    max_energy_balance = 0.0

    def observables(t, q, state):
        h = amplitude * math.cos(frequency * t)
        dh = -amplitude * frequency * math.sin(frequency * t)
        energies = -h * PORT
        work = -dh * (PORT @ state)
        chem = heat = entropy_prod = 0.0
        for j in range(3):
            for i in range(j + 1, 3):
                current = q[i, j] * state[j] - q[j, i] * state[i]
                fuel = math.log(QBASE[i, j] / QBASE[j, i])
                chem += current * fuel
                heat += current * (energies[i] - energies[j] - fuel)
                entropy_prod += current * math.log(q[i, j] * state[j] /
                                                  (q[j, i] * state[i]))
        de = work + energies @ (q @ state)
        return np.array([work, chem, heat, entropy_prod]), abs(de - work - chem - heat)

    for k in range(steps):
        pnew, stages = advance(p, k)
        weights = (1, 2, 2, 1)
        indices = (2 * k, 2 * k + 1, 2 * k + 1, 2 * k + 2)
        for w, index, state in zip(weights, indices, stages):
            vals, balance = observables(times[index], qs[index], state)
            ledger += dt * w * vals / 6
            max_energy_balance = max(max_energy_balance, balance)
        p = pnew
        profile.append(p.copy())
    closure = float(np.max(np.abs(p - p0)))
    # The proof below uses these fixed floats as exact dyadic numbers.
    # Enforce normalization and exact periodicity of the proposed profile.
    profile = np.array(profile)
    profile[:, 2] = 1.0 - profile[:, 0] - profile[:, 1]
    profile[-1] = profile[0]
    return profile, {
        "model": "source_clock" if clock else "geometric",
        "amplitude": amplitude, "frequency": frequency, "period": tau,
        "steps": steps, "periodic_initial_probability": p0.tolist(),
        "period_closure_max": closure,
        "work_on": float(ledger[0]), "chemical_work_in": float(ledger[1]),
        "heat_in": float(ledger[2]), "entropy_production": float(ledger[3]),
        "cycle_energy_residual": float(sum(ledger[:3])),
        "entropy_heat_residual": float(ledger[2] + ledger[3]),
        "pointwise_energy_residual": max_energy_balance,
        "output_per_fuel": float(-ledger[0] / ledger[1]),
        "finite_generator_scope": "state-energy work only; kinetic actuator cost is not modeled",
    }


def interval_certificate(profile, amplitude_text, frequency_text):
    """Residual/contraction proof of the exact periodic cycle work sign.

    For periodic ptilde with sum 1 and residual r=ptilde'-Q ptilde,
    uniform off-diagonal q>=m implies exact periodic p has
    sup ||p-ptilde||_1 <= sup||r||_1/(3m). Thus |W-Wtilde|
    <= 4A sup||r||_1/(3m). Residual Taylor bounds are rigorous intervals.
    """
    iv.dps = 45
    a, nu = iv.mpf(amplitude_text), iv.mpf(frequency_text)
    n = len(profile) - 1
    dt = 2 * iv.pi / (nu * n)
    half = dt / 2
    dtheta = nu * dt
    expmax = iv.exp(a / 2)
    exitmax = iv.mpf(26) / 25 * expmax
    q1_bound = exitmax * a * nu
    q2_bound = exitmax * nu ** 2 * (a + a ** 2 / 2)
    contraction = iv.mpf(3) / 1000 / expmax

    def upper(x):
        return math.nextafter(float(x.b), math.inf)

    def multiply(matrix, vector):
        return [sum((matrix[i][j] * vector[j] for j in range(3)), iv.mpf(0))
                for i in range(3)]

    def l1(vector):
        return sum((abs(x) for x in vector), iv.mpf(0))

    def interval_matrix(theta):
        h = a * iv.cos(theta)
        dh = -a * nu * iv.sin(theta)
        ep, em = iv.exp(h / 2), iv.exp(-h / 2)
        plus = [[iv.mpf(0), iv.mpf(4) / 25, iv.mpf(1) / 1000],
                [iv.mpf(0)] * 3, [iv.mpf(0)] * 3]
        minus = [[iv.mpf(0)] * 3,
                 [iv.mpf(1), iv.mpf(0), iv.mpf(0)],
                 [iv.mpf(1) / 25, iv.mpf(0), iv.mpf(0)]]
        const = [[iv.mpf(0)] * 3,
                 [iv.mpf(0), iv.mpf(0), iv.mpf(1) / 300],
                 [iv.mpf(0), iv.mpf(1) / 1000, iv.mpf(0)]]
        q = [[plus[i][j] * ep + minus[i][j] * em + const[i][j]
              for j in range(3)] for i in range(3)]
        dq = [[dh / 2 * (plus[i][j] * ep - minus[i][j] * em)
               for j in range(3)] for i in range(3)]
        for j in range(3):
            q[j][j] = -sum(q[i][j] for i in range(3) if i != j)
            dq[j][j] = -sum(dq[i][j] for i in range(3) if i != j)
        return q, dq

    max_r0 = max_r1 = max_s = max_residual = 0.0
    wtilde = iv.mpf(0)
    sinhalf, coshalf = iv.sin(dtheta / 2), iv.cos(dtheta / 2)
    for k in range(n):
        # Third coordinate is formed as an EXACT interval arithmetic
        # complement, not independently rounded input; sum equals 1.
        left = [iv.mpf(float(profile[k, 0])), iv.mpf(float(profile[k, 1]))]
        left.append(1 - left[0] - left[1])
        right = [iv.mpf(float(profile[k + 1, 0])), iv.mpf(float(profile[k + 1, 1]))]
        right.append(1 - right[0] - right[1])
        assert all(float(x.a) > 0 for x in left + right)
        pmid = [(x + y) / 2 for x, y in zip(left, right)]
        slope = [(y - x) / dt for x, y in zip(left, right)]
        theta = 2 * iv.pi * (2 * k + 1) / (2 * n)
        q, dq = interval_matrix(theta)
        qp = multiply(q, pmid)
        dqp = multiply(dq, pmid)
        qs = multiply(q, slope)
        r0 = l1([slope[i] - qp[i] for i in range(3)])
        r1 = l1([-dqp[i] - qs[i] for i in range(3)])
        s_norm = l1(slope)
        bound = r0 + half * r1 + half ** 2 / 2 * (q2_bound + 2 * q1_bound * s_norm)
        max_r0 = max(max_r0, upper(r0))
        max_r1 = max(max_r1, upper(r1))
        max_s = max(max_s, upper(s_norm))
        max_residual = max(max_residual, upper(bound))
        # Exact integral of A sin(theta) * ptilde_0(theta).
        wtilde += 2 * a * (pmid[0] * iv.sin(theta) * sinhalf +
                           slope[0] * iv.cos(theta) * (-half * coshalf + sinhalf / nu))

    state_bound = iv.mpf(max_residual) / contraction
    work_bound = 4 * a * state_bound
    wtrue = wtilde + iv.mpf([-1, 1]) * work_bound
    assert float(wtrue.b) < 0, "Finite interval proof did not establish negative work"
    return {
        "proof": "interval residual + uniform CTMC total variation contraction",
        "interval_decimal_precision": 45,
        "amplitude_exact": amplitude_text, "frequency_exact": frequency_text,
        "proposed_profile_intervals": n,
        "uniform_contraction_rate_lower": str(contraction),
        "max_midpoint_residual_l1_upper": max_r0,
        "max_midpoint_residual_derivative_l1_upper": max_r1,
        "max_profile_slope_l1_upper": max_s,
        "global_residual_l1_upper": max_residual,
        "exact_periodic_probability_error_l1_upper": str(state_bound),
        "profile_work_on_interval": str(wtilde),
        "work_error_upper": str(work_bound),
        "exact_periodic_work_on_enclosure": str(wtrue),
        "certified_negative_work_on": True,
        "scope": "stipulated finite CTMC geometric actuator and periodic law; no hardware claim",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=8192)
    parser.add_argument("--amplitude", default="0.3")
    parser.add_argument("--frequency", default="0.01")
    parser.add_argument("--clock", action="store_true")
    parser.add_argument("--certify", action="store_true")
    parser.add_argument("--verify-profile", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.verify_profile:
        payload_bytes = args.verify_profile.read_bytes()
        payload = json.loads(payload_bytes)
        args.amplitude = payload["amplitude_exact"]
        args.frequency = payload["frequency_exact"]
        profile = np.array([[float.fromhex(x), float.fromhex(y), 0.0]
                            for x, y in payload["first_two_probability_coordinates_hex"]])
        assert np.array_equal(profile[0], profile[-1])
        data = {"verification_input": str(args.verify_profile),
                "profile_sha256": hashlib.sha256(payload_bytes).hexdigest()}
        data["interval_certificate"] = interval_certificate(profile, args.amplitude, args.frequency)
        args.output.write_text(json.dumps(data, indent=2) + "\n")
        print(json.dumps(data, indent=2))
        return
    profile, data = numeric_profile(args.steps, float(args.amplitude),
                                    float(args.frequency), args.clock)
    data["exact_geometric_low_frequency_friction"] = exact_friction()
    if args.certify:
        assert not args.clock
        payload = {
            "meaning": "exact dyadic candidate, with third coordinate exactly one minus first two",
            "amplitude_exact": args.amplitude, "frequency_exact": args.frequency,
            "first_two_probability_coordinates_hex": [[float(x).hex(), float(y).hex()]
                                                       for x, y in profile[:, :2]],
        }
        payload_bytes = (json.dumps(payload, separators=(",", ":")) + "\n").encode()
        profile_path = args.output.with_suffix(".profile.json")
        profile_path.write_bytes(payload_bytes)
        data["profile_file"] = str(profile_path)
        data["profile_sha256"] = hashlib.sha256(payload_bytes).hexdigest()
        data["interval_certificate"] = interval_certificate(profile, args.amplitude, args.frequency)
    args.output.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
