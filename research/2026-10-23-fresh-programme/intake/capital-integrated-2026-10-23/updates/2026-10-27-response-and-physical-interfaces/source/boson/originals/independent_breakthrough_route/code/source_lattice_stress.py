#!/usr/bin/env python3
"""Sampling diagnostic on the source's full 3x3 triangular lattice.

No accuracy or convergence claim is made from this diagnostic. In particular,
an empirical effective sample size can miss unsampled rare events.
"""
import json
import time
from pathlib import Path

import numpy as np

from canonical_bafqmc import field_evaluate


def main():
    m, n, beta, steps, samples, batch = 9, 9, 1., 20, 65536, 512
    k = np.zeros((m, m))
    coords = [(x, y) for x in range(3) for y in range(3)]
    index = {r: i for i, r in enumerate(coords)}
    for i, (x, y) in enumerate(coords):
        for dx, dy in [(1, 0), (0, 1), (1, -1)]:
            j = index[((x+dx) % 3, (y+dy) % 3)]
            k[i, j] += 1
            k[j, i] += 1
    phase = np.array([4*np.pi*x/3+2*np.pi*y/3 for x, y in coords])
    sf = np.cos(phase[:, None]-phase[None, :])/m**2
    result = {"status": "sampling stress only; no exact thermodynamics acquired",
              "lattice": "source 3x3 periodic triangular, t=1",
              "single_particle_eigenvalues": np.linalg.eigvalsh(k).tolist(),
              "n_per_flavor": n, "beta": beta, "steps": steps,
              "samples_per_setting": samples, "runs": []}
    for u2 in [0., -.05]:
        rng = np.random.default_rng(202610274)
        sums = np.zeros(4)
        cross = np.zeros((4, 4))
        largest = 0.
        start = time.perf_counter()
        for _ in range(samples//batch):
            fields = rng.standard_normal((batch, steps, 2, m))
            values, logpre = field_evaluate(fields, n=n, beta=beta, u1=1.,
                                            u2=u2, k=k, sf=sf)
            sums += values.sum(axis=0)
            cross += values.T@values
            largest = max(largest, float(values[:, 0].max()))
        mean = sums/samples
        cov = (cross-samples*np.outer(mean, mean))/(samples-1)
        energy = mean[1]/mean[0]
        energy_error = np.sqrt(max(0., cov[1, 1]-2*energy*cov[0, 1]+
                                   energy*energy*cov[0, 0])/samples)/mean[0]
        run = {"u1": 1., "u2": u2, "seed": 202610274,
               "uniform_fields_integrated": True,
               "weight_cv_squared_empirical": float(cov[0, 0]/mean[0]**2),
               "weight_ess_diagnostic": float(sums[0]**2/cross[0, 0]),
               "largest_weight_fraction_of_sum": float(largest/sums[0]),
               "energy_ratio_diagnostic": float(energy),
               "energy_delta_method_error_diagnostic": float(energy_error),
               "seconds": time.perf_counter()-start,
               "accuracy": "UNKNOWN; no ED or other matched thermal reference"}
        result["runs"].append(run)
        print(json.dumps(run), flush=True)
    Path(__file__).resolve().parents[1].joinpath("source_lattice_stress.json").write_text(
        json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
