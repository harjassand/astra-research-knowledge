"""Independent exact scalar/finite-command intake; no producer imports or flow.

Consumes the retained source-qualified certificate and the NEW UNEXECUTED
finite bootstrap command. It does not reconstruct frames, simulate an ODE,
validate a physical calibration, or transfer stored numerical data to a new
protocol. The exact-flow comparison is the mathematical contract in REVIEW.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import time


def bound(d, end="upper"):
    return F(*d[end])


def save(x):
    return {"numerator": x.numerator, "denominator": x.denominator,
            "display": float(x)}


def complex_q(entry):
    return F(*entry[0]), F(*entry[1])


def main():
    start = time.perf_counter()
    here = Path(__file__).resolve().parent
    source = here.parent.parent / "t_nonlinear_port"
    bridge = source / "calibration_bridge"
    cert = json.loads((bridge / "CERTIFICATE.json").read_text())
    command = json.loads((bridge / "COMMAND.json").read_text())
    old = json.loads((source / "ENERGY_CERTIFICATE.json").read_text())
    assert cert["proper_protocol_rank_or_actual_error_from_old_arrays"].startswith("NOT_QUALIFIED")
    assert cert["no_source_or_science_flow_rerun"]

    # Exact norms of the finite, executed-compiler output command. Arb's
    # norm routine uses upper majorants; its lower endpoint is not claimed
    # to be a lower bound on the true command norm.
    v = [complex_q(row[0]) for row in command["bootstrap_command"]]
    assert len(v) == 32
    assert all((x * (1 << 48)).denominator == 1 for pair in v for x in pair)
    norm2 = sum(x*x+y*y for x, y in v)
    power = norm2 / 2
    assert power <= bound(cert["cost"]["integrated_squared_drive_bound"])
    peak_bound = bound(cert["cost"]["peak_drive_bound"])
    assert all(x*x+y*y <= peak_bound**2 for x, y in v)
    assert power < F(13647, 10**6) and peak_bound < F(56901, 10**6)
    feedback = command["science_feedback_matrix"]
    assert len(feedback) == 32 and all(len(row) == 32 for row in feedback)
    assert all((x * (1 << 48)).denominator == 1
               for row in feedback for z in row for x in complex_q(z))

    # An independent, deliberately enlarged scalar receiver for the new
    # exact-flow controller. Its constants use only supplied outward upper
    # bounds, with rational square-root/exponential overpays.
    assert bound(cert["steering_sigma_lower"], "lower") > F(142, 1000)
    assert bound(cert["readout_sigma_lower"], "lower") > F(291, 1000)
    dK, de = bound(cert["dK"]), bound(cert["de"])
    history = de/5 + F(321, 50)*dK
    assert history < F(8153, 10**15)
    initial = bound(cert["reset_residual_general_bound"])
    assert initial < F(2176, 10**14)
    alpha = bound(cert["science_reset_gain_general_bound"])
    gain = bound(cert["post_reset_noise_gain_bound"])
    rounding = bound(cert["finite_output_command_rounding_state_error"])
    assert alpha < F(675, 10**12)
    root32 = F(5656854249492381, 10**15)
    assert root32**2 > 32
    eta = F(1, 10**9)
    target = F(1500001, 10**6)
    # The positive terms in producer alpha also bound its eb <= alpha.
    rbar = F(205, 10**10)
    assert initial <= rbar
    next_r = alpha*(rbar+(1+alpha)*target+rounding) + gain*root32*eta + rounding
    assert next_r < rbar
    assert rbar+(1+alpha)*target+rounding < F(8, 5)

    exponent = 3*F(7,20)*F(8,5)**2*F(13,10)
    # For x>=0, sum through term n plus a geometric upper bound on the
    # remaining Taylor terms is an elementary rational exp upper bound.
    term, partial, n = F(1), F(1), 80
    for k in range(1, n+1):
        term *= exponent/k
        partial += term
    next_term = term*exponent/(n+1)
    exp_upper = partial+next_term/(1-exponent/F(n+2))
    assert exp_upper < 33
    q = 33*alpha
    assert q < F(223, 10**10) < 1
    floor_same = 2*rounding/(1-q)
    floor_different = (2*gain*root32*eta+2*rounding)/(1-q)
    assert floor_same < F(804, 10**16)
    assert floor_different < F(3883, 10**11)

    # A coarse independent reconstruction of the OLD, source-qualified
    # stored-data receiver; no NPZ, left inverse, source matrix, or solver.
    s = bound(old["design_sigma_min_certified_lower"], "lower")
    residual = bound(old["source_truth_residual"])+bound(old["fitted_residual"])
    stored_error_bound = residual/s
    assert stored_error_bound < F(258, 10**7)
    assert bound(old["actual_tensor_coefficient_error"]) < stored_error_bound

    originals = []
    for binding in cert["unchanged_original_bindings"]:
        raw = (source / binding["path"]).read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        assert digest == binding["sha256"] and len(raw) == binding["bytes"]
        originals.append({"path": binding["path"], "sha256": digest})
    inputs = []
    for path in (bridge / "COMMAND.json", bridge / "CERTIFICATE.json", source / "ENERGY_CERTIFICATE.json"):
        inputs.append({"path": str(path.relative_to(source)),
                       "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    result = {
        "status": "PASS_INDEPENDENT_EXACT_SCALAR_AND_FINITE_COMMAND_CONSUMER",
        "no_producer_imports": True,
        "no_frame_or_flow_or_source_run": True,
        "inputs": inputs,
        "finite_command_squared_norm": save(norm2),
        "finite_command_integrated_squared_drive": save(power),
        "source_qualified_calibration_history_bound": save(history),
        "independent_absolute_post_reset_cap": save(rbar),
        "independent_exact_cycle_contraction_bound": save(q),
        "same_word_rounding_floor_bound": save(floor_same),
        "different_word_floor_bound": save(floor_different),
        "stored_data_tensor_error_coarse_bound": save(stored_error_bound),
        "old_flow_error": "UNKNOWN: conservation defect is not trajectory error",
        "new_proper_protocol_rank": "NOT_QUALIFIED",
        "original_files_unchanged": originals,
        "seconds": time.perf_counter()-start,
    }
    (here / "SCALAR_CONSUMER.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("original_files_unchanged",)}, indent=2))


if __name__ == "__main__":
    main()
