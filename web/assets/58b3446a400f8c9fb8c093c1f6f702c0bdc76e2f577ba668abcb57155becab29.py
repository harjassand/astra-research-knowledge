"""Independent exact/dense metric checks and actual compressed posterior certs."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import signal
import time

from axial_acquisition import (sector_matrix, matvec, spin_dimensions, total_variation,
                                choose)
from filtered_sector import (filtered_sector_columns, filtered_isotropic_target,
                             backconvert_filtered_weights, filtered_posterior,
                             scaled_filter_values, direct_filtered_branch_data,
                             conditional_max_shift_probabilities)
from check_axial_acquisition import zeros, identity, scale, add, mm, tr, spin_projectors


def main():
    def wall_limit(signum, frame):
        raise TimeoutError("declared30second filtered-sector fixture wall cap exceeded")
    signal.signal(signal.SIGALRM, wall_limit)
    signal.alarm(30)
    started = time.perf_counter()
    assertions = 0
    def check(condition):
        nonlocal assertions
        assertions += 1
        assert condition
    dense_cases = 0
    for N in range(1, 5):
        d = 1 << N
        P = spin_projectors(N)
        dims = spin_dimensions(N)
        f = [F((t + 1) * (N + 2 - t), (N + 2) ** 2) for t in range(N + 1)]
        A = sector_matrix(N)
        x = [F(b + 1, sum(range(1, len(P) + 1))) for b in range(len(P))]
        y = list(reversed(x))
        C, c, Z = filtered_sector_columns(N, f)
        Qx = [v * cb / sum(a * z for a, z in zip(x, c)) for v, cb in zip(x, c)]
        Qy = [v * cb / sum(a * z for a, z in zip(y, c)) for v, cb in zip(y, c)]
        states = []
        for weights in [x, y]:
            G = zeros(d)
            for q, dim, projector in zip(weights, dims, P):
                G = add(G, scale(q / dim, projector))
            filtered = zeros(d)
            for i in range(d):
                for j in range(d):
                    if i.bit_count() == j.bit_count():
                        filtered[i][j] = G[i][j] * f[i.bit_count()]
                    else:
                        check(G[i][j] == 0)
            states.append(scale(1 / tr(filtered), filtered))
        sign_operator = zeros(d)
        for b, projector in enumerate(P):
            q_difference = Qx[b] - Qy[b]
            sign = 1 if q_difference > 0 else -1 if q_difference < 0 else 0
            sign_operator = add(sign_operator, scale(F(sign), projector))
            check(tr(mm(P[b], states[0])) == Qx[b])
            check(tr(mm(P[b], states[1])) == Qy[b])
        difference = add(states[0], scale(F(-1), states[1]))
        # Signs are constant in each positive conditional block, so this is
        # the exact physical trace norm witness, not a numeric eigenvalue call.
        metric = tr(mm(sign_operator, difference)) / 2
        check(metric == total_variation(Qx, Qy))
        v = [F(k + 1, choose(N + 2, 2)) for k in range(N + 1)]
        w = backconvert_filtered_weights(v, Z)
        model_prior = matvec(A, w)
        beta = sum(q * z for q, z in zip(model_prior, c))
        model_sector = [q * z / beta for q, z in zip(model_prior, c)]
        check(model_sector == matvec(C, v))
        dense_cases += 1
    compressed_cases = 0
    for N in [8, 16, 32, 64]:
        f = [F(t + 1, N + 1) for t in range(N + 1)]
        C, c, Z = filtered_sector_columns(N, f)
        check(len(C) == N // 2 + 1 and len(Z) == N + 1)
        for k in range(N + 1):
            check(sum(C[b][k] for b in range(len(C))) == 1)
            R = sum(F(choose(N - k, u), (k + 1) * (1 << (N - k)))
                    * sum(f[u:u + k + 1]) for u in range(N - k + 1))
            check(R == Z[k])
        compressed_cases += 1
    # Coupling-independent floors and clipped conditional acquisition.
    huge = F(1 << 256)
    huge_records = []
    for h in [huge, -huge]:
        N, eps = 16, F(1, 1024)
        values, intervals = scaled_filter_values(N, F(1), h, 64)
        C, c, Z = filtered_sector_columns(N, values)
        aligned = N if h > 0 else 0
        check(values[aligned] > F(1, 1 << N))
        check(min(Z) > F(1, 1 << (2 * N)))
        qhat = filtered_isotropic_target(N, huge, values, 64)
        check(qhat[0] == 1)
        v = [F(int(k == 0)) for k in range(N + 1)]
        posterior = filtered_posterior(N, huge, F(1), h, 64,
                                      direct_filtered_weights=v)
        check(posterior["TV_upper"] < eps)
        branches, data = direct_filtered_branch_data(N, F(1), h, v, eps)
        check(sum(b["probability"] for b in branches) == 1)
        check(data["zero_global_slices"] > 0)
        for branch in branches:
            p, meta = conditional_max_shift_probabilities(N, branch["k"], branch["u"], F(1), h, eps)
            check(min(p) >= 0 and sum(p) == 1)
            check(meta["normalizer_at_least_one"])
            check(meta["scalar_bits"] < 40)
        huge_records.append({"h_sign": int(h > 0), "N": N,
                             "magnitude_bits": 257,
                             "posterior_upper": str(posterior["TV_upper"]),
                             "global_zero_slices": data["zero_global_slices"]})
    # Independently validate actual peer-proposed rational weights against TRUE
    # filter intervals.  This is a model metric, not the complete sampler cert.
    peer_records = []
    for N in [8, 16]:
        path = Path(f'work/cycle6/c03_s01/implementation/filtered_N{N}.json')
        raw = path.read_bytes()
        model = json.loads(raw)["model"]
        def frac(record):
            return F(int(record["numerator"]), int(record["denominator"]))
        alpha, delta, h = [frac(model[name]) for name in ["alpha", "delta", "h"]]
        w = [frac(v) for v in model["isotropic_weights"]]
        check(len(w) == N + 1 and sum(w) == 1 and min(w) >= 0)
        result = filtered_posterior(N, alpha, delta, h, 96, isotropic_weights=w)
        check(result["TV_upper"] < F(1, 1000000))
        # The deliberately wrong K0 candidate must fail this same tight claim.
        bad = [F(int(k == 0)) for k in range(N + 1)]
        rejected = filtered_posterior(N, alpha, delta, h, 96, isotropic_weights=bad)
        check(rejected["TV_upper"] > F(1, 100))
        peer_records.append({"N": N, "alpha": str(alpha), "delta": str(delta),
                             "h": str(h), "source": str(path),
                             "source_sha256": hashlib.sha256(raw).hexdigest(),
                             "own_true_filter_model_TV_upper": str(result["TV_upper"]),
                             "own_true_filter_model_TV_upper_float": float(result["TV_upper"]),
                             "wrong_K0_upper": float(rejected["TV_upper"]),
                             "sampler_block_phase_and_local_errors_included": False})
    # Explicit API rejection controls.
    for call in [lambda: filtered_posterior(2, F(1), F(1), F(0), 64,
                                          isotropic_weights=[F(-1), F(1), F(1)]),
                 lambda: filtered_sector_columns(2, [F(0)] * 3),
                 lambda: filtered_posterior(2, F(1), F(1), F(0), 64)]:
        try:
            call()
        except ValueError:
            check(True)
        else:
            check(False)
    result = {"status": "PASS", "assertions": assertions,
              "elapsed_seconds_shared_machine": time.perf_counter() - started,
              "exact_dense_metric_cases": dense_cases,
              "exact_compressed_cases": compressed_cases,
              "binary_magnitude_cases": huge_records,
              "independent_actual_peer_model_certificates": peer_records,
              "evidence_scope": "exact algebra plus outward physical model trace certificates; candidate LP and generic iid backends not executed; sampler certificates remain separate",
              "hardware_preparation": "NOT_EXECUTED"}
    signal.alarm(0)
    Path(__file__).with_name('filtered_sector_checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
