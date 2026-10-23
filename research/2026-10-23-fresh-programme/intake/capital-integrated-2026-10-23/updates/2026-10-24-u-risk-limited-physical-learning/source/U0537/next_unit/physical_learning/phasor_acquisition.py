"""Three-epoch virtual acquisition on the fixed reciprocal RC fixture.

The plant solver returns voltages, never an internal gradient to the learner.
The adjoint/finite-difference derivatives below are independent validation.
This is model replay; no physical electronics or noisy readout was acquired.
"""
from pathlib import Path
import json
import numpy as np

G0 = np.array([1.0, 2.0, 0.5])
B = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, -1.0]])
C = np.diag([0.25, 1.0])
OMEGA = 4.0
INPUT = np.array([1.0, 0.0], dtype=complex)
TARGET = complex(0.1, -0.05)
KAPPA_T = 1.0
EPSILON = 0.2
ETA = 1.0
SAMPLES_PER_PERIOD = 4096


def plant(g, current):
    # Simulated physical response. Only output voltages are returned.
    a = B.T @ np.diag(g) @ B
    return np.linalg.solve(a + 1j * OMEGA * C, current)


def loss(g):
    error = plant(g, INPUT)[1] - TARGET
    return 0.5 * abs(error)**2


def squared_voltage_second_harmonic(edge_phasors):
    phase = np.arange(SAMPLES_PER_PERIOD) * 2 * np.pi / SAMPLES_PER_PERIOD
    real_voltages = np.real(edge_phasors[:, None] * np.exp(1j * phase))
    return 4 * np.mean(real_voltages**2 * np.cos(2 * phase), axis=1)


def pairs(z):
    return [[float(x.real), float(x.imag)] for x in np.asarray(z)]


def main():
    # Epoch 1: the teacher obtains only the free output error, then holds it.
    free = plant(G0, INPUT)
    error = free[1] - TARGET
    held_teacher = np.array([0, KAPPA_T * error.conjugate()])

    # Epochs 2 and 3: local detectors see only their own real branch waveform.
    plus_current = INPUT + EPSILON * held_teacher
    minus_current = INPUT - EPSILON * held_teacher
    plus = plant(G0, plus_current)
    minus = plant(G0, minus_current)
    qplus = squared_voltage_second_harmonic(B @ plus)
    qminus = squared_voltage_second_harmonic(B @ minus)
    acquired_gradient = -(qplus - qminus) / (4 * EPSILON * KAPPA_T)

    # These computations validate the acquisition; the learner did not use H.
    a = B.T @ np.diag(G0) @ B
    h = np.linalg.inv(a + 1j * OMEGA * C)
    adjoint = h.conjugate().T @ np.array([0, error])
    exact_gradient = -np.real(np.conjugate(B @ adjoint) * (B @ free))
    finite_difference = []
    for j in range(len(G0)):
        perturbation = np.zeros_like(G0)
        perturbation[j] = 1e-6
        finite_difference.append((loss(G0 + perturbation) - loss(G0 - perturbation)) / 2e-6)
    finite_difference = np.array(finite_difference)
    assert np.max(np.abs(acquired_gradient - exact_gradient)) < 1e-13
    assert np.max(np.abs(acquired_gradient - finite_difference)) < 1e-10

    # One retained programming step, not continuous adjustment during probing.
    trained = np.clip(G0 - ETA * acquired_gradient, 0.1, 4.0)
    old_loss, new_loss = loss(G0), loss(trained)
    assert new_loss < old_loss

    # Strong implementation falsifier: a DC square detector gets a different
    # complex product even though the same forward measurements are used.
    wrong_dc = -(np.abs(B @ plus)**2 - np.abs(B @ minus)**2) / (4 * EPSILON * KAPPA_T)

    # Steady integration loss only. Actual settling and active circuitry are
    # deliberately not silently assigned zero cost.
    gstar, cstar, vstar = 1e-3, 1e-6, 1.0
    omega_physical = OMEGA * gstar / cstar
    duration = 32 * 2 * np.pi / omega_physical
    voltages = [free, plus, minus]
    steady_powers = [0.5 * np.sum(G0 * np.abs(B @ x)**2) * gstar * vstar**2
                     for x in voltages]
    verified_state = plant(trained, INPUT)
    verify_power = 0.5 * np.sum(trained * np.abs(B @ verified_state)**2) * gstar * vstar**2
    result = {
        "status": "synthetic linear reciprocal RC replay; no acquired hardware or advantage",
        "fixture_normalized": {"g_shunt1_shunt2_link": G0.tolist(),
                               "capacitance_diagonal": np.diag(C).tolist(),
                               "omega": OMEGA, "target_real_imag": [TARGET.real, TARGET.imag],
                               "teacher_transconductance": KAPPA_T, "probe_epsilon": EPSILON},
        "free_voltages_real_imag": pairs(free),
        "held_teacher_current_real_imag": pairs(held_teacher),
        "acquired_gradient": acquired_gradient.tolist(),
        "exact_gradient_validation": exact_gradient.tolist(),
        "finite_difference_validation": finite_difference.tolist(),
        "dc_square_wrong_product": wrong_dc.tolist(),
        "programmed_g": trained.tolist(),
        "free_loss_before": old_loss,
        "free_loss_after": new_loss,
        "relative_loss_decrease": 1 - new_loss / old_loss,
        "resource_record": {
            "forward_epochs_to_produce_update": 3,
            "additional_held_loss_verification_epochs": 1,
            "local_samples_per_edge_per_probe_period": SAMPLES_PER_PERIOD,
            "local_detector_quantity": "4 mean(real_voltage^2 cos(2 omega t))",
            "local_stored_contrasts": len(G0),
            "conductance_programs": len(G0),
            "physical_Gstar_S": gstar, "physical_Cstar_F": cstar, "physical_Vstar_V": vstar,
            "carrier_frequency_Hz": omega_physical / (2 * np.pi),
            "assumed_integration_periods_per_epoch": 32,
            "steady_integration_time_per_epoch_s": duration,
            "mesh_steady_power_free_plus_minus_W": [float(p) for p in steady_powers],
            "mesh_steady_integration_update_J": float(sum(steady_powers) * duration),
            "mesh_held_loss_verification_power_W": float(verify_power),
            "mesh_steady_integration_with_verification_J": float((sum(steady_powers) + verify_power) * duration),
            "excluded_unacquired_costs": ["settling transients", "I/Q teacher and sample/hold",
                "local squarer/mixer/integrator", "clock and bias rails",
                "programming and retention", "detector noise and calibration", "reset"]
        }
    }
    output = Path(__file__).with_name("phasor_acquisition_results.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
