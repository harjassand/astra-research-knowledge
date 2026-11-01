"""Checks for cold-output thermal/phase tradeoff and native-output escape.

Finite passive-collision model follows warm_bus_observation_probe.py. All
checks are mathematical, not experimental. No network or fitted data.
"""
import json
import numpy as np
from scipy.integrate import cumulative_trapezoid, simpson


def collision_model(n_steps=80, duration=2.0, hot_rate=0.3, cold_rate=1.0, phase=0.1):
    dt = duration / n_steps
    ch = np.exp(-hot_rate * dt / 2)
    sh = np.sqrt(1 - ch * ch)
    cc = np.exp(-cold_rate * dt / 2)
    sc = np.sqrt(1 - cc * cc)
    decay = ch * cc
    modes = 1 + 2 * n_steps
    passive = np.eye(modes)
    displacement = np.zeros(modes, complex)
    phi, energy = 0.0, 0.0
    prescribed = (np.exp(2j * np.pi * np.arange(n_steps + 1) / n_steps) - 1) * np.sqrt(phase / (2 * np.pi))
    for step in range(n_steps):
        kick = prescribed[step + 1] - decay * prescribed[step]
        phi += np.imag(kick * np.conj(displacement[0]))
        displacement[0] += kick
        energy += abs(kick) ** 2 / dt
        for mode, cosine, sine in ((1 + 2 * step, ch, sh), (2 + 2 * step, cc, sc)):
            old_bus, old_mode = passive[0].copy(), passive[mode].copy()
            passive[0] = cosine * old_bus + sine * old_mode
            passive[mode] = -sine * old_bus + cosine * old_mode
            bus_d, mode_d = displacement[0], displacement[mode]
            displacement[0] = cosine * bus_d + sine * mode_d
            displacement[mode] = -sine * bus_d + cosine * mode_d
    hot = np.zeros(modes)
    hot[0] = 1
    hot[1::2] = 1
    hot_projector = passive @ np.diag(hot) @ passive.T
    lvec = np.column_stack((np.sqrt(2) * displacement.imag, -np.sqrt(2) * displacement.real)).reshape(-1)
    omega = np.kron(np.eye(modes), np.array([[0, 1], [-1, 0]]))
    cold_indices = np.ravel(np.column_stack((2 * np.arange(2, modes, 2), 2 * np.arange(2, modes, 2) + 1)))
    cold_selection = np.eye(2 * modes)[cold_indices]
    return hot_projector, lvec, omega, cold_selection, float(phi), float(energy), displacement


def cold_constrained_check(n_steps):
    hot, lvec, omega, select, phi, energy, displacement = collision_model(n_steps)
    hot_quad = np.kron(hot, np.eye(2))
    q = select @ hot_quad @ select.T
    g = select @ hot_quad @ lvec
    c = select @ omega.T @ lvec
    k0 = np.linalg.solve(q, g)
    qc = np.linalg.solve(q, c)
    # Preserve the original phase exactly.
    gain = k0 - qc * (c @ k0) / (c @ qc)
    residual = lvec - select.T @ gain
    coefficient = float(residual @ hot_quad @ residual)
    benchmark = 2 * 0.3 * phi ** 2 / energy
    return {"steps": n_steps, "phase": phi, "E": energy,
            "leading_hot_coefficient": coefficient,
            "continuum_lower_bound": benchmark,
            "ratio": coefficient / benchmark,
            "unconstrained_phase_after_feedback": float(phi - 0.5 * c @ k0)}


def smooth_continuum_saturation():
    duration, kh, kc, target = 2.0, 0.3, 1.0, 0.1
    kappa = kh + kc
    t = np.linspace(0, duration, 20001)
    carrier = 2 * np.pi / duration
    p = np.pi / duration
    envelope = np.sin(p * t) ** 2
    envelope_d = p * np.sin(2 * p * t)
    envelope_dd = 2 * p ** 2 * np.cos(2 * p * t)
    amplitude = np.sqrt(target / (carrier * 3 * duration / 8))
    rotating = np.exp(1j * carrier * t)
    alpha = amplitude * envelope * rotating
    alpha_d = amplitude * (envelope_d + 1j * carrier * envelope) * rotating
    alpha_dd = amplitude * (envelope_dd + 2j * carrier * envelope_d - carrier ** 2 * envelope) * rotating
    force = 1j * (alpha_d + kappa * alpha / 2)
    force_d = 1j * (alpha_dd + kappa * alpha_d / 2)
    energy = float(simpson(abs(force) ** 2, x=t))
    phi = float(simpson(np.imag(alpha.conj() * alpha_d), x=t))

    def future_convolution(values):
        cumulative = cumulative_trapezoid(np.exp(-kappa * t / 2) * values, t, initial=0)
        return np.exp(kappa * t / 2) * (cumulative[-1] - cumulative)

    rows = []
    u = future_convolution(force)
    for desired in [0.0, 0.05, 0.1]:
        residual = 1j * desired / energy * force
        residual_d = 1j * desired / energy * force_d
        filter_kernel = (force - kappa * residual / 2 + residual_d) / np.sqrt(kc)
        rebuilt = u - np.sqrt(kc) * future_convolution(filter_kernel)
        actual_phase = phi + np.sqrt(kc) * np.real(simpson(alpha.conj() * filter_kernel, x=t))
        hot_coefficient = float(2 * (abs(residual[0]) ** 2 + kh * simpson(abs(residual) ** 2, x=t)))
        cold_vacuum = float(simpson(abs(np.sqrt(kc) * residual + filter_kernel) ** 2, x=t))
        assert abs(actual_phase - desired) < 1e-10
        assert abs(hot_coefficient - 2 * kh * desired ** 2 / energy) < 1e-10
        assert max(abs(rebuilt - residual)) < 1e-7
        rows.append({"desired_phase": desired, "actual_phase": float(actual_phase),
                     "leading_hot_coefficient": hot_coefficient,
                     "homodyne_cold_vacuum_variance": cold_vacuum,
                     "filter_squared_norm": float(simpson(abs(filter_kernel) ** 2, x=t)),
                     "convolution_identity_error": float(max(abs(rebuilt - residual)))})
    return {"original_phase": phi, "E": energy, "rows": rows}


def native_output_check():
    hot, lvec, omega, _, phi, _, displacement = collision_model(80)
    modes = len(displacement)
    rows, efficiencies, norms = [], [], []
    for mode in range(1, modes):
        pair = lvec[2 * mode:2 * mode + 2]
        norm = np.linalg.norm(pair)
        if norm < 1e-14:
            continue
        eta = 0.4 if mode % 2 else 0.7
        row = np.zeros_like(lvec)
        row[2 * mode:2 * mode + 2] = np.sqrt(eta) * pair / norm
        rows.append(row)
        efficiencies.append(eta)
        norms.append(norm)
    measure = np.stack(rows)
    efficiencies = np.array(efficiencies)
    gain = np.array(norms) / np.sqrt(efficiencies)
    seed = np.diag((1 - efficiencies) / 2)
    c = measure @ omega.T @ lvec
    residual = lvec - measure.T @ gain
    reports = []
    for population in [0.0, 10.0, 1e6]:
        covariance = np.kron(0.5 * np.eye(modes) + population * hot, np.eye(2))
        variance = residual @ covariance @ residual + gain @ seed @ gain
        reports.append({"hot_population": population, "variance": float(variance),
                        "surviving_phase": float(phi - 0.5 * c @ gain)})
    assert max(abs(c)) < 1e-14
    assert np.linalg.norm(residual) < 1e-14
    assert max(x["variance"] for x in reports) - min(x["variance"] for x in reports) < 1e-10
    # A fixed multiplicative calibration mismatch restores a hot term.
    mismatch = 1e-3
    wrong_residual = lvec - measure.T @ ((1 + mismatch) * gain)
    hot_quad = np.kron(hot, np.eye(2))
    return {"rows": reports, "phase_backaction_vector_max": float(max(abs(c))),
            "residual_norm": float(np.linalg.norm(residual)),
            "gain_mismatch": mismatch,
            "mismatch_leading_hot_coefficient": float(wrong_residual @ hot_quad @ wrong_residual)}


def main():
    result = {"cold_port_constrained_continuum_limit": [cold_constrained_check(n) for n in [20, 40, 80, 160, 320]],
              "finite_gain_smooth_saturation": smooth_continuum_saturation(),
              "native_hot_output_escape": native_output_check()}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
