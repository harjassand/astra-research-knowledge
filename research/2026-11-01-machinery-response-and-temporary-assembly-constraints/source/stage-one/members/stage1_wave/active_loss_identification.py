"""Conventional active controller with no coordinate input and no reset.

This is a discriminating algorithm check in a dilute-inclusion model, not an
experimental reproduction or a claim of general response programmability.
The physical model uses three harmonic Dirichlet modes on a disk. The material
state is a small cylindrical inclusion; only its 3x3 port response is exposed.
The controller actively identifies the current loss-rate quadratic, not a full
mobility-weighted response operator. It is never given the hidden position,
force law, mobility, temperature, or polarizability.
"""
from pathlib import Path
import json
import numpy as np


def response(q):
    x, y = q
    fields = np.array([[1.0, 0.0, x], [0.0, 1.0, -y]])
    return np.diag([np.pi, np.pi, np.pi / 2]) + 0.2 * fields.T @ fields


class InclusionPlant:
    def __init__(self, initial):
        self._q = np.array(initial, dtype=float)
        self.measurements = 0
        self.pulses = 0
        self.integrated_voltage_squared = 0.0

    def measure(self):
        self.measurements += 1
        return response(self._q)

    def pulse(self, voltage, duration):
        u = np.asarray(voltage)
        assert np.linalg.norm(u) <= 1 + 1e-12
        x, y = self._q
        # Positive input-conductance convention, dimensionless mobility*kappa=1.
        force = 0.4 * u[2] * np.array([u[0] + u[2]*x, -u[1] + u[2]*y])
        self._q += duration * force
        self.pulses += 1
        self.integrated_voltage_squared += duration * float(u @ u)


def terminal_only_controller(measure, pulse, target, probe_time, max_cycles=500):
    """Only actuator and terminal-measurement callbacks enter this routine."""
    def loss(matrix):
        return 0.5 * float(np.linalg.norm(matrix - target)**2)

    n = target.shape[0]
    eye = np.eye(n)
    initial_loss = loss(measure())
    history = [initial_loss]
    last_matrix = None
    for cycle in range(max_cycles):
        A = np.zeros((n, n))
        # Positive finite pulses at sequential, non-reset material states.
        # Bias from these different states vanishes with total calibration motion.
        for i in range(n):
            before = loss(measure())
            pulse(eye[i], probe_time)
            after = loss(measure())
            A[i, i] = (after - before) / probe_time
        for i in range(n):
            for j in range(i + 1, n):
                before = loss(measure())
                pulse((eye[i] + eye[j]) / np.sqrt(2), probe_time)
                after = loss(measure())
                measured = (after - before) / probe_time
                A[i, j] = A[j, i] = measured - 0.5*(A[i, i] + A[j, j])
        values, vectors = np.linalg.eigh(A)
        if values[0] < -1e-12:
            pulse(vectors[:, 0], 0.03)
        last_matrix = measure()
        current_loss = loss(last_matrix)
        history.append(current_loss)
        if current_loss < 1e-10:
            break
    return {
        "initial_loss": initial_loss,
        "final_loss": history[-1],
        "cycles": len(history)-1,
        "full_response_frobenius_error": float(np.linalg.norm(last_matrix-target)),
        "probe_duration": probe_time,
        "loss_samples": [history[i] for i in range(0, len(history), 25)],
        "returned_response": last_matrix.tolist(),
    }


def run():
    target = response(np.array([-0.2, 0.3]))
    results = []
    for dt in (1e-4, 1e-3):
        plant = InclusionPlant([0.5, -0.4])
        result = terminal_only_controller(plant.measure, plant.pulse, target, dt)
        result.update({
            "physical_pulses": plant.pulses,
            "terminal_matrix_measurements": plant.measurements,
            "integrated_voltage_squared": plant.integrated_voltage_squared,
            "hidden_final_position_for_validation_only": plant._q.tolist(),
            "position_given_to_controller": False,
            "reset_operations": 0,
        })
        results.append(result)
    # Entire response targets need not belong to the material's response manifold.
    # G11=pi+0.2 at every position; changing just that target entry by .1 cannot
    # be repaired by moving this sphere, regardless of sensing or control method.
    unreachable_target = target.copy()
    unreachable_target[0, 0] += 0.1
    result = {
        "scope": "Noiseless dilute-inclusion model with ideal instantaneous 3-mode readout; conventional active task-gradient identification",
        "finite_readout_and_noise_earned": False,
        "cases": results,
        "unreachable_target_exact_loss_lower_bound": 0.5 * 0.1**2,
        "unreachable_reason": "First diagonal response is position independent; no controller can change it by rearranging this inclusion",
    }
    assert all(r["final_loss"] < r["initial_loss"] / 1000 for r in results)
    Path(__file__).with_name("active_loss_identification_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
