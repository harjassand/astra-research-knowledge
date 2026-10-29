"""One-port simulated acquisition; the learner never receives hidden states/H.

Floating model diagnostic, not certified numerical or physical tomography.
All experiment durations/laws are fixed before the run. No parameter tuning.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import eig
from scipy.optimize import linear_sum_assignment


class Instrument:
    def __init__(self, hidden_matrix):
        self._H = hidden_matrix
        self._l, self._V = np.linalg.eigh(hidden_matrix)
        self.n = len(hidden_matrix)
        self.calls = self.port_reads = self.nfev = 0
        self.preparation_time = self.pulse_time = self.readout_time = 0.0
        self.max_drive_amplitude_bound = self.max_prepared_norm = 0.0

    def impulse_return(self, times):
        self.calls += 1
        self.port_reads += len(times)
        self.readout_time += float(max(times))
        return np.exp(-1j * np.outer(times, self._l)) @ self._V[0] ** 2

    def experiment(self, drive_coeff, drive_freq, prep_time, duration, times, law):
        self.calls += 1
        self.port_reads += len(times)
        self.preparation_time += prep_time
        self.pulse_time += duration
        self.readout_time += float(max(times))
        self.max_drive_amplitude_bound = max(
            self.max_drive_amplitude_bound, float(np.sum(np.abs(drive_coeff))))

        def prepare_rhs(t, x):
            u = drive_coeff @ np.exp(1j * drive_freq * (prep_time - t))
            ans = -1j * self._H @ x
            ans[0] += u
            return ans

        sol = solve_ivp(prepare_rhs, (0, prep_time), np.zeros(self.n, complex),
                        method="DOP853", rtol=2e-12, atol=2e-13, max_step=.1)
        if not sol.success:
            raise RuntimeError(sol.message)
        self.nfev += sol.nfev
        x = sol.y[:, -1]
        self.max_prepared_norm = max(self.max_prepared_norm, float(np.linalg.norm(x)))

        if law == "off":
            x = self._V @ (np.exp(-1j * self._l * duration) * (self._V.T @ x))
        else:
            def pulse_rhs(t, state):
                if law == "distributed":
                    nl = np.abs(state) ** 2 * state
                elif law == "port_only":
                    nl = np.zeros_like(state)
                    nl[0] = abs(state[0]) ** 2 * state[0]
                elif law == "isotropic":
                    nl = np.vdot(state, state).real * state
                else:
                    raise ValueError(law)
                return -1j * (self._H @ state + nl)
            sol = solve_ivp(pulse_rhs, (0, duration), x, method="DOP853",
                            rtol=2e-12, atol=2e-13)
            if not sol.success:
                raise RuntimeError(sol.message)
            self.nfev += sol.nfev
            x = sol.y[:, -1]
        # ONLY the same single complex boundary field is returned.
        return (np.exp(-1j * np.outer(times, self._l))
                @ (self._V[0] * (self._V.T @ x)))

    def costs(self):
        return {k: v for k, v in vars(self).items() if not k.startswith("_")}


def spectral_acquisition(device, n, spacing=1.0):
    samples = device.impulse_return(np.arange(2 * n) * spacing)
    H0 = np.array([[samples[i+j] for j in range(n)] for i in range(n)])
    H1 = np.array([[samples[i+j+1] for j in range(n)] for i in range(n)])
    poles = eig(H1, H0, right=False)
    freq = -np.angle(poles) / spacing
    freq.sort()
    vand = np.exp(-1j * np.outer(np.arange(n) * spacing, freq))
    weights = np.linalg.solve(vand, samples[:n])
    assert np.max(np.abs(weights.imag)) < 1e-9
    assert np.min(weights.real) > 0
    return freq, np.sqrt(weights.real), dict(
        hankel_condition=float(np.linalg.cond(H0)),
        hankel_smallest_singular=float(np.linalg.svd(H0, compute_uv=False)[-1]),
        max_pole_unit_circle_defect=float(np.max(np.abs(np.abs(poles)-1))),
        minimum_acquired_port_weight=float(np.min(weights.real)),
        acquired_minimum_frequency_gap=float(np.min(np.diff(freq))))


class Learner:
    def __init__(self, device, freq, port):
        self.device, self.freq, self.port = device, freq, port
        self.n = len(freq)
        self.prep_time = 2 * np.pi
        diff = freq[:, None] - freq[None, :]
        T = self.prep_time
        self.G = T * np.exp(-.5j * diff * T) * np.sinc(diff * T / (2*np.pi))
        self.read_times = 2*np.pi*np.arange(self.n)/self.n
        self.O = np.exp(-1j * np.outer(self.read_times, freq)) * port

    def control(self, desired):
        return np.linalg.solve(self.G, desired/self.port)

    def cubic_query(self, desired, duration):
        coeff = self.control(desired)
        nonlinear = self.device.experiment(coeff, self.freq, self.prep_time,
                                           duration, self.read_times, "distributed")
        baseline = self.device.experiment(coeff, self.freq, self.prep_time,
                                          duration, self.read_times, "off")
        return 1j * np.linalg.solve(self.O, nonlinear-baseline) / duration

    def reconstruct(self, g, duration):
        basis = np.eye(self.n)
        columns = []
        for e in basis:
            c = (self.cubic_query(g+e, duration)-self.cubic_query(g-e, duration)
                 -2*self.cubic_query(e, duration))/6
            columns.append(c)
        Mraw = np.column_stack(columns)
        M = (Mraw.real + Mraw.real.T)/2
        vals, vecs = np.linalg.eigh(M)
        rows = vecs.T
        matches = np.abs(rows @ self.port)
        distinguished = int(np.argmax(matches))
        perm = [distinguished] + [i for i in range(self.n) if i != distinguished]
        rows = rows[perm]
        if rows[0] @ self.port < 0:
            rows[0] *= -1
        recovered = (rows * self.freq) @ rows.T
        return recovered, rows, M, dict(
            pulse_duration=duration,
            slice_minimum_eigenvalue_gap=float(np.min(np.diff(vals))),
            ignored_imaginary_slice_norm=float(np.linalg.norm(Mraw.imag, 2)),
            ignored_antisymmetric_slice_norm=float(np.linalg.norm(Mraw-Mraw.T, 2)),
            distinguished_port_row_error=float(np.linalg.norm(rows[0]-self.port)))


def align_for_evaluation(recovered, rows, true_matrix, true_vectors):
    # Secret matrices are used ONLY to score, never to fit/acquire.
    ri, ci = linear_sum_assignment(-np.abs(rows @ true_vectors.T))
    assignment = ci[np.argsort(ri)]
    signs = np.sign(np.sum(rows * true_vectors[assignment], axis=1))
    target = true_matrix[np.ix_(assignment, assignment)] * signs[:, None] * signs[None, :]
    return float(np.linalg.norm(recovered-target, 2))


def main():
    start = time.perf_counter()
    n = 6
    j, k = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    V = np.sqrt(2/n)*np.cos(np.pi*(j+.5)*k/n)
    V[:, 0] = 1/np.sqrt(n)
    freq = np.arange(n)-(n-1)/2
    H = (V*freq) @ V.T
    Q = np.eye(n)
    for i, j, angle in [(1, 2, .47), (3, 5, -.31), (2, 4, .22)]:
        R = np.eye(n)
        R[i, i] = R[j, j] = np.cos(angle)
        R[i, j], R[j, i] = -np.sin(angle), np.sin(angle)
        Q = R @ Q
    matrices, vectors = [H, Q@H@Q.T], [V, Q@V]
    devices = [Instrument(A) for A in matrices]
    learned = [spectral_acquisition(d, n) for d in devices]
    learners = [Learner(d, x[0], x[1]) for d, x in zip(devices, learned)]
    # Deterministic seed is only a diagnostic choice of a contraction vector.
    rng = np.random.default_rng(2026102917)
    g = rng.normal(size=n)
    g /= np.linalg.norm(g)
    rows_out, slices, recoveries = [], [], []
    for index, learner in enumerate(learners):
        results = []
        for duration in [1e-3, 1e-4, 1e-5]:
            rec, rows, M, report = learner.reconstruct(g, duration)
            report["aligned_matrix_operator_error"] = align_for_evaluation(
                rec, rows, matrices[index], vectors[index])
            results.append(report)
        rows_out.append(rows)
        slices.append(M)
        recoveries.append(results)

    controls = {}
    for law in ["off", "port_only", "isotropic", "distributed"]:
        ys = []
        for learner in learners:
            ys.append(learner.device.experiment(learner.control(g), learner.freq,
                      learner.prep_time, .1, learner.read_times, law))
        controls[law] = float(np.max(np.abs(ys[0]-ys[1])))
    assert controls["distributed"] > 1e-5
    assert max(controls[k] for k in ["off", "port_only", "isotropic"]) < 1e-9
    out = dict(
        status="FLOATING_MODEL_CONSTRUCTION_EXECUTED",
        n=n, source="two real symmetric cyclic sources related by Q fixing port",
        frequency_diagnostics=[x[2] for x in learned],
        control_gram_conditions=[float(np.linalg.cond(x.G)) for x in learners],
        readout_conditions=[float(np.linalg.cond(x.O)) for x in learners],
        contraction_vector=g.tolist(), reconstruction=recoveries,
        nonlinear_slice_difference_norm=float(np.linalg.norm(slices[0]-slices[1], 2)),
        matched_port_only_and_isotropic_controls=controls,
        raw_acquisition_costs=[d.costs() for d in devices],
        elapsed_seconds=time.perf_counter()-start,
        current_consumer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        scope="Simulated one-port complex fields; no hidden tensor/state given to learner; no physical experiment, finite-error certification, or generic novelty claim",
    )
    here = Path(__file__).resolve().parent
    (here/"EXECUTION.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
