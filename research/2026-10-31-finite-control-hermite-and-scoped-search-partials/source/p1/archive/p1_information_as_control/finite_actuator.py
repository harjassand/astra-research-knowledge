"""A finite, power-bounded dense pattern and its paid local control traffic.

The source is still a software linear-aggregate simulator. This script makes
the actuator coefficient representation explicit; it does not build hardware.
The exact power cap is checked using integer arithmetic on the actual pattern.
"""
from pathlib import Path
import json
import math
import numpy as np
import finite_precision as fp


def pack_pattern(indices, offset=2**18, bits=20):
    unsigned = (indices + offset).astype(np.uint32)
    binary = ((unsigned[..., None] >> np.arange(bits, dtype=np.uint32)) & 1).astype(np.uint8)
    return np.packbits(binary.reshape(len(indices), -1), axis=1, bitorder="little")


def unpack_pattern(packet, m, offset=2**18, bits=20):
    binary = np.unpackbits(packet, axis=1, count=m*bits, bitorder="little").reshape(len(packet), m, bits)
    values = np.sum(binary.astype(np.int64) * (1 << np.arange(bits)), axis=-1)
    return values - offset


def pattern_bound(m):
    k = math.ceil(math.sqrt(m))
    denominator = 2**19 + k
    return denominator, (math.sqrt(m) + k) / denominator


def main():
    root = Path(__file__).resolve().parent
    impl = fp.impl
    r = 64
    m = r*(r+1)//2
    noise = 0.01
    alpha = 1/(1+noise)
    generator = np.random.default_rng(20261101+r)
    hidden = generator.uniform(0.9, 1.1, size=m)  # scorer only
    acquired = np.load(root/"learning"/"learned_cubic_model.npz")["coefficients"]
    theory, qm, am = fp.formulas(hidden, acquired, r, noise)
    denominator, direction_bound = pattern_bound(m)
    risk_bound = (math.sqrt(theory["exact_MSE_before_last_ADC"])
                  + alpha**2 * math.sqrt(theory["quantized_coefficient_second_moment"])
                  * (direction_bound + math.sqrt(am["MSE_bound"])))**2
    rng = np.random.default_rng(20261031)
    trials = 8192
    errors = []
    perturbations = []
    max_direction_error = 0.0
    max_integer_power_numerator = 0
    off = impl.layout(r)
    for start in range(0, trials, 32):
        count = min(32, trials-start)
        u = rng.normal(size=(count,r))
        v = rng.normal(size=(count,m))
        truth = np.sum(impl.features(u,off)*hidden*v,axis=1)/math.sqrt(m)
        g = (u+math.sqrt(noise)*rng.normal(size=(count,r)))/math.sqrt(1+noise)
        context = (np.sign(g)*np.minimum(np.floor(np.abs(g)/.01),600)).astype(np.int16)
        context_packet = impl.pack_control(context,600,11)
        qg = .01*impl.unpack_control(context_packet,r,600,11).astype(float)
        raw = impl.features(qg,off)*acquired/math.sqrt(m)
        norms = np.linalg.norm(raw,axis=1)
        ideal = np.divide(raw,norms[:,None],out=np.zeros_like(raw),where=norms[:,None]!=0)
        ideal[norms==0,0] = 1
        indices = np.rint(ideal*2**18).astype(np.int64)
        pattern_packet = pack_pattern(indices)
        received = unpack_pattern(pattern_packet,m)
        assert np.array_equal(received,indices)
        assert pattern_packet.shape[1] == math.ceil(20*m/8)
        # wtilde_i=2*j_i/denominator. This integer inequality verifies its
        # true rational norm cap independently of float normalization.
        numerator = 4*np.sum(received*received,axis=1,dtype=np.int64)
        assert np.all(numerator <= denominator**2)
        max_integer_power_numerator = max(max_integer_power_numerator,int(np.max(numerator)))
        actual = 2*received.astype(float)/denominator
        direction_error = np.linalg.norm(actual-ideal,axis=1)
        assert np.all(direction_error <= direction_bound+1e-12)
        max_direction_error = max(max_direction_error,float(np.max(direction_error)))
        eta = math.sqrt(noise)*rng.normal(size=count)
        analog_actual = np.sum(actual*v,axis=1)+eta
        analog_ideal = np.sum(ideal*v,axis=1)+eta
        last_indices = np.clip(np.rint(analog_actual/am["step"]),-32767,32767).astype("<i2")
        last_packet = last_indices.tobytes()
        last = np.frombuffer(last_packet,dtype="<i2").astype(float)*am["step"]
        estimate = alpha**2*norms*last
        ideal_estimate = alpha**2*norms*analog_ideal
        errors.extend((truth-estimate)**2)
        perturbations.extend((estimate-ideal_estimate)**2)
    errors = np.asarray(errors)
    measured = float(np.mean(errors))
    se = float(np.std(errors,ddof=1)/math.sqrt(trials))
    assert measured <= risk_bound+6*se

    m_large = 8256
    denominator_large, direction_large = pattern_bound(m_large)
    dq = qm["uniform_feature_mse_bound"]
    base = 1-alpha**3+alpha**3*dq
    balanced_bound = (math.sqrt(base)+alpha**2*(1+math.sqrt(dq))
                      *(direction_large+math.sqrt(am["MSE_bound"])))**2
    assert balanced_bound < .03
    result = dict(status="PASS",pattern_bits_per_weight=20,
        acquired_case=dict(r=r,M=m,trials=trials,scalar_reads=r+1,
            remote_context_control_bytes=88,local_pattern_bytes=math.ceil(20*m/8),
            final_ADC_bytes=2,pattern_denominator=denominator,
            exact_integer_power_cap_checked=True,
            maximum_power_numerator=max_integer_power_numerator,
            power_denominator_squared=denominator**2,
            uniform_direction_error_bound=direction_bound,
            largest_executed_direction_error=max_direction_error,
            predicted_MSE_upper_bound=risk_bound,measured_MSE=measured,
            MSE_standard_error=se,
            measured_output_change_MSE=float(np.mean(perturbations)),
            actuator_coefficients=m,projection_multiplications=m),
        balanced_case=dict(r=128,M=m_large,scalar_reads=129,
            first_ADC_bits=1408,remote_control_bits=1408,
            local_pattern_bits=20*m_large,local_pattern_bytes=20*m_large//8,
            final_ADC_bits=16,pattern_denominator=denominator_large,
            uniform_direction_error_bound=direction_large,
            fully_quantized_MSE_upper_bound=balanced_bound,
            all_fixed_129_read_MSE_lower_bound=1-3*alpha*129/m_large),
        scope="Finite rational actuator weights, packed20-bit local programs, packed11-bit context, packed16-bit final readout. Exact integer power caps verified. Weight-generation arithmetic is float64 and the aggregate is software simulated; no physical sensor or certified runtime advantage.")
    (root/"finite_actuator_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
