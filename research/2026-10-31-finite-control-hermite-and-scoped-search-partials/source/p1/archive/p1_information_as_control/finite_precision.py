"""Finite input/control/output messages for the cubic sensing construction.

This is a new root-owned extension. It leaves every earlier campaign and the
agent's learned model unchanged. Sensor and pattern arithmetic remain float64;
we quantify input/output digitization, not a hardware implementation error.
"""
from pathlib import Path
import importlib.util
import json
import math
import numpy as np
from scipy.special import ndtr

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "cubic_impl", ROOT / "learning" / "learn_quantized_cubic.py")
impl = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = impl
spec.loader.exec_module(impl)


def adc_moments(noise=0.01, limit=8.0, largest_index=32767):
    """Exact Gaussian-bin first/cross/second moments for a nearest ADC.

    The support is {-32767,...,32767} times step: 65535 levels, one
    unused int16 code. Use positive bins and symmetry to avoid lower-tail
    CDF cancellation. The tail in the last bin extends to infinity.
    """
    sd = math.sqrt(1 + noise)
    step = limit / largest_index
    j = np.arange(1, largest_index + 1, dtype=float)
    lo = (j - 0.5) * step / sd
    hi = (j + 0.5) * step / sd
    hi[-1] = np.inf
    mass = ndtr(-lo) - ndtr(-hi)
    density_lo = np.exp(-lo * lo / 2) / math.sqrt(2 * math.pi)
    density_hi = np.exp(-hi * hi / 2) / math.sqrt(2 * math.pi)
    first = sd * (density_lo - density_hi)
    values = j * step
    cross = float(2 * np.dot(values, first))
    second = float(2 * np.dot(values * values, mass))
    error = 1 + noise - 2 * cross + second
    a = limit / sd
    tail_second = 2 * sd * sd * (
        a * math.exp(-a * a / 2) / math.sqrt(2 * math.pi) + ndtr(-a))
    error_bound = step * step / 4 + tail_second
    assert error >= -1e-12 and error <= error_bound + 1e-12
    return dict(step=step, limit=limit, bits=16, levels=65535,
                gaussian_cross_moment=cross, gaussian_second_moment=second,
                exact_gaussian_MSE=max(0.0, error), MSE_bound=error_bound)


def coefficient_moments(c, acquired, r, moments):
    """E[true coefficient dot implemented coefficient] and squared norm / M."""
    diag_second = (moments["q4"] - 2 * moments["q2"] + 1) / 2
    diag_cross = (moments["g2q2"] - moments["q2"]) / 2
    off_second = moments["q2"] ** 2
    off_cross = moments["gq"] ** 2
    cross = (np.dot(c[:r], acquired[:r]) * diag_cross
             + np.dot(c[r:], acquired[r:]) * off_cross) / len(c)
    second = (np.dot(acquired[:r], acquired[:r]) * diag_second
              + np.dot(acquired[r:], acquired[r:]) * off_second) / len(c)
    return float(cross), float(second)


def formulas(c, acquired, r, noise=0.01):
    alpha = 1 / (1 + noise)
    qm = impl.quantizer_moments(0.01, 6.0)
    am = adc_moments(noise)
    cross, second = coefficient_moments(c, acquired, r, qm)
    variance = float(np.mean(c * c))
    before_adc = variance + alpha**3 * (second - 2 * cross)
    after_adc = (variance - 2 * alpha**4 * cross * am["gaussian_cross_moment"]
                 + alpha**4 * second * am["gaussian_second_moment"])
    triangle_bound = (math.sqrt(before_adc)
                      + alpha**2 * math.sqrt(second * am["MSE_bound"]))**2
    assert after_adc <= triangle_bound + 1e-12
    return dict(target_variance=variance,
                exact_MSE_before_last_ADC=before_adc,
                exact_MSE_with_last_ADC=after_adc,
                last_ADC_MSE_upper_bound=triangle_bound,
                quantized_coefficient_second_moment=second), qm, am


def main():
    noise = 0.01
    alpha = 1 / (1 + noise)
    # Restore exactly the separately acquired r=64 model and its scorer-only
    # hidden coefficients. Repeat real calibration calls to verify provenance.
    r = 64
    m = r * (r + 1) // 2
    calibration_rng = np.random.default_rng(20261101 + r)
    hidden = calibration_rng.uniform(0.9, 1.1, size=m)
    oracle = impl.FunctionOracle(r, hidden)
    acquired = impl.acquire(oracle, 1e-7, calibration_rng)
    retained = np.load(ROOT / "learning" / "learned_cubic_model.npz")
    assert np.array_equal(acquired, retained["coefficients"])
    predicted, qm, am = formulas(hidden, acquired, r, noise)
    trials = 8192
    rng = np.random.default_rng(20261030)
    errors = []
    differences = []
    saturations = 0
    off = impl.layout(r)
    for start in range(0, trials, 256):
        count = min(256, trials - start)
        u = rng.normal(size=(count, r))
        v = rng.normal(size=(count, m))
        truth = np.sum(impl.features(u, off) * hidden * v, axis=1) / math.sqrt(m)
        analog_context = (u + math.sqrt(noise) * rng.normal(size=(count, r))) / math.sqrt(1 + noise)
        indices = (np.sign(analog_context) * np.minimum(
            np.floor(np.abs(analog_context) / 0.01), qm["levels"])).astype(np.int16)
        # Both first-read digitization and controller-to-actuator control use
        # the actual packed bytes. No precise analog context enters prediction.
        packet = impl.pack_control(indices, qm["levels"], qm["bits_per_coordinate"])
        decoded = impl.unpack_control(packet, r, qm["levels"], qm["bits_per_coordinate"])
        assert np.array_equal(indices, decoded)
        qg = decoded.astype(float) * 0.01
        raw = impl.features(qg, off) * acquired / math.sqrt(m)
        norms = np.linalg.norm(raw, axis=1)
        unit = np.divide(raw, norms[:, None], out=np.zeros_like(raw), where=norms[:, None] != 0)
        zero = norms == 0
        if np.any(zero):
            unit[zero, 0] = 1.0  # fixed unit fallback; amplitude is zero
        last = np.sum(unit * v, axis=1) + math.sqrt(noise) * rng.normal(size=count)
        last_indices = np.clip(np.rint(last / am["step"]), -32767, 32767).astype("<i2")
        last_packet = last_indices.tobytes()
        decoded_last = np.frombuffer(last_packet, dtype="<i2").astype(float) * am["step"]
        assert len(last_packet) == 2 * count
        pred = alpha**2 * norms * decoded_last
        pred_analog = alpha**2 * norms * last
        errors.extend((truth - pred)**2)
        differences.extend((pred - pred_analog)**2)
        saturations += int(np.count_nonzero(np.abs(last) > 8.0))
    errors = np.asarray(errors)
    empirical = float(np.mean(errors))
    se = float(np.std(errors, ddof=1) / math.sqrt(trials))
    assert abs(empirical - predicted["exact_MSE_with_last_ADC"]) <= 6 * se

    # A separate balanced, normalized mathematical instance. Do not confuse
    # these constants with the acquired coefficients above.
    r_large = 128
    m_large = r_large * (r_large + 1) // 2
    balanced, _, _ = formulas(np.ones(m_large), np.ones(m_large), r_large, noise)
    q_error_bound = qm["uniform_feature_mse_bound"]
    risk_uniform = 1 - alpha**3 + alpha**3 * q_error_bound
    norm_bound = (1 + math.sqrt(q_error_bound))**2
    finite_bound = (math.sqrt(risk_uniform)
                    + alpha**2 * math.sqrt(norm_bound * am["MSE_bound"]))**2
    fixed_lower = 1 - 3 * alpha * (r_large + 1) / m_large
    fixed_necessary = math.ceil(0.97 * m_large / (3 * alpha))
    assert finite_bound < 0.03
    balanced.update(r=r_large, M=m_large, scalar_reads=r_large + 1,
                    context_ADC_bits=11 * r_large, control_bits=11 * r_large,
                    final_ADC_bits=16,
                    uniform_analytic_finite_precision_MSE_bound=finite_bound,
                    every_fixed_same_count_MSE_lower_bound=fixed_lower,
                    necessary_fixed_reads_for_MSE_at_most_0_03=fixed_necessary,
                    full_coordinate_noisy_reads=r_large + m_large,
                    full_coordinate_noisy_MSE=1 - alpha**3)

    result = dict(status="PASS", noise_variance=noise, final_ADC=am,
                  acquired_case=dict(r=r, M=m, trials=trials,
                    calibration_calls_for_provenance=oracle.calls,
                    calibration_feature_entries=oracle.feature_entries,
                    calibration_dense_target_products=oracle.target_products,
                    scalar_reads=r+1, context_ADC_bytes=88,
                    controller_to_actuator_bytes=88, final_ADC_bytes=2,
                    model_bytes=int(acquired.nbytes), actuator_weights=m,
                    projection_multiplications=m,
                    measured_MSE=empirical, MSE_standard_error=se,
                    measured_output_digitization_squared_error=float(np.mean(differences)),
                    final_ADC_clipping_events=saturations, **predicted),
                  balanced_case=balanced,
                  scope="First context and final readout are digitized and actually serialized. Dense pattern arithmetic and source projections are float64 software operations, not a certified physical actuator. No runtime speedup claimed.")
    (ROOT / "finite_precision_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
