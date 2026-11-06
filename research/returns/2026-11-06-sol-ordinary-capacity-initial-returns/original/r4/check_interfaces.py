"""Finite exact checks against analytically known channel-state fixtures."""
import json
import math
import random
import time
from fractions import Fraction as F
from pathlib import Path

from finite_block import (
    G, ONE, ZERO, affine_choi_projection, choi_from_kraus, coherent_information_interval,
    entropy_interval, finite_block_interval, projector, tensor_choi,
    verify_normalized_choi, zeros, is_psd,
)


def as_text(interval):
    return {"lower": str(interval[0]), "upper": str(interval[1]),
            "lower_float": float(interval[0]), "upper_float": float(interval[1])}


def run():
    started = time.monotonic()
    id_J, a, b = choi_from_kraus([[[1, 0], [0, 1]]])
    dep = []
    # Two exact rational copies of each of the four matrix units: sum K* K=I.
    for i in range(2):
        for j in range(2):
            for _ in range(2):
                K = zeros(2)
                K[i][j] = G(F(1, 2))
                dep.append(K)
    dep_J, _, _ = choi_from_kraus(dep)
    erase = []
    # Two copies of I/2 successful, two copies of each |e><j|/2 erased.
    for _ in range(2):
        erase.append([[F(1, 2), 0], [0, F(1, 2)], [0, 0]])
    for j in range(2):
        for _ in range(2):
            K = zeros(3, 2)
            K[2][j] = G(F(1, 2))
            erase.append(K)
    erase_J, _, _ = choi_from_kraus(erase)
    cases = []
    for name, J, b, truth in [
        ("identity_Bell", id_J, 2, F(1)),
        ("depolarizing_Bell", dep_J, 2, F(-1)),
        ("half_erasure_Bell", erase_J, 3, F(0)),
    ]:
        verify_normalized_choi(J, 2, b)
        interval = coherent_information_interval(J, 2, b, [1, 0, 0, 1], F(1, 16))
        assert interval[0] <= truth <= interval[1]
        cases.append({"name": name, "analytic_value": str(truth), **as_text(interval)})
    for name, J, b in [("identity_pure", id_J, 2), ("depolarizing_pure", dep_J, 2),
                       ("half_erasure_pure", erase_J, 3)]:
        interval = coherent_information_interval(J, 2, b, [1, 0, 0, 0], F(1, 16))
        assert interval[0] <= 0 <= interval[1]
        cases.append({"name": name, "analytic_value": "0", **as_text(interval)})

    # A genuinely complex rational projector, with known spectrum {1,0,0}.
    complex_entropy = entropy_interval(projector([1, G(0, 1), G(1, 1)]), F(1, 100))
    assert complex_entropy == (F(0), F(0))

    # The two-use Choi ordering must equal the Choi of I_4, exactly.
    tensor_J, A, B = tensor_choi(id_J, 2, 2, 2)
    direct_J, _, _ = choi_from_kraus([[[int(i == j) for j in range(4)] for i in range(4)]])
    assert tensor_J == direct_J and (A, B) == (4, 4)

    # Singular and indefinite PSD cases, with genuinely complex entries.
    assert is_psd(projector([1, G(0, 1), G(1, 1)]))
    assert is_psd(zeros(3))
    assert not is_psd([[G(0), G(1)], [G(1), G(0)]])
    assert not is_psd([[G(1), G(2)], [G(2), G(1)]])
    # Boundary channel -> interior -> grid rounding -> exact affine slice.
    delta, a, b = F(1, 8), 2, 2
    D, tau = a*b, delta/8
    M = math.ceil(32*a*D*D/delta)
    interior = [[(1-tau)*id_J[i][j]+G(tau/D if i == j else 0)
                 for j in range(D)] for i in range(D)]
    rounded = [[G(F(round(z.re*M), M), F(round(z.im*M), M)) for z in row]
               for row in interior]
    candidate = affine_choi_projection(rounded, a, b)
    assert is_psd(candidate)
    verify_normalized_choi(candidate, a, b)
    # Exact entrywise error implies the advertised operator/dimension bound.
    assert all(abs(candidate[i][j].re-interior[i][j].re) <= F(2*D, M)
               and abs(candidate[i][j].im-interior[i][j].im) <= F(2*D, M)
               for i in range(D) for j in range(D))

    # Operational guard must expose refusal instead of mislabelling a sample as max.
    guarded = False
    try:
        finite_block_interval(id_J, 2, 2, 1, F(1, 4), max_points=10)
    except RuntimeError as exc:
        guarded = "grid" in str(exc)
    assert guarded

    # Independently check the geometric mesh inequality with floating points.
    rng = random.Random(65731)
    mesh_tests, largest_ratio = 0, 0.0
    for dim in [2, 4, 9, 16]:
        delta = 0.1
        M = math.ceil(math.sqrt(2*dim)/delta)
        for _ in range(100):
            v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(dim)]
            norm = math.sqrt(sum(abs(z)**2 for z in v))
            v = [z/norm for z in v]
            q = [complex(round(z.real*M)/M, round(z.imag*M)/M) for z in v]
            qn = math.sqrt(sum(abs(z)**2 for z in q))
            q = [z/qn for z in q]
            overlap = sum(x.conjugate()*y for x, y in zip(v, q))
            td = math.sqrt(max(0, 1-abs(overlap)**2))
            assert td <= delta+1e-12
            largest_ratio = max(largest_ratio, td/delta)
            mesh_tests += 1
    result = {
        "status": "finite_interface_checks_passed",
        "ordinary_capacity_question": "UNRESOLVED",
        "full_general_grid_executed": False,
        "fixtures": cases,
        "complex_rank_one_entropy": as_text(complex_entropy),
        "tensor_choi_grouping": "exact_pass",
        "PSD_and_affine_channel_mesh": "exact_pass",
        "mesh_samples": mesh_tests,
        "largest_observed_trace_distance_over_delta": largest_ratio,
        "guarded_full_search_refusal": guarded,
        "elapsed_seconds": time.monotonic()-started,
    }
    path = Path(__file__).resolve().parent/"CHECK_RESULTS.json"
    path.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: v for k, v in result.items() if k != "fixtures"}, indent=2))


if __name__ == "__main__":
    run()
