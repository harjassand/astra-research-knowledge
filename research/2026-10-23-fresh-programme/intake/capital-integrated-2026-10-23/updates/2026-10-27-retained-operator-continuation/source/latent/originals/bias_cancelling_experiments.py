"""Native fixed-dose, nonnegative self-calibration of a rank-one posterior.
Separate from the initial exact calibrated observation required for saturation.
"""
import json
from pathlib import Path
import sympy as sp
from acquired_latent_controller_compiler import (S,SL,e0,e1,e2,R,t,frac)

true_t=R(7,4)
S_true=S.subs(t,true_t)
eta=R(1,100)


def check_mixture(q):
    assert sum(q)==1 and all(z>=0 for z in q)
    assert (q.T*q)[0]<=1


def main():
    bias=sp.Matrix([R(1,10),-R(1,5),R(3,10)])
    q0=e0; q1=e2
    check_mixture(q0);check_mixture(q1)
    # Exact fixed offset across both experiments, not available beforehand.
    z0=S_true*q0+bias
    z1=S_true*q1+bias
    c=(e2.T*(q1-q0))[0]
    recovered_t=1+(e2.T*(z1-z0-SL*(q1-q0)))[0]/c
    assert recovered_t==true_t
    recovered_bias=z0-S_true*q0
    assert recovered_bias==bias
    # Two readings under independently bounded Euclidean sensor errors.
    n0=eta*e2/2
    n1=-eta*e2/4
    w0=z0+n0;w1=z1+n1
    center=1+(e2.T*(w1-w0-SL*(q1-q0)))[0]/c
    certified_range=[center-2*eta/abs(c),center+2*eta/abs(c)]
    assert certified_range[0]<=true_t<=certified_range[1]
    # General indistinguishability for every allowed mixture q on the simplex.
    # Two latent values t0+-2eta and different fixed biases can be hidden by
    # two adversarial errors of norm at most eta for every possible query.
    tplus=true_t+2*eta; tminus=true_t-2*eta
    bplus=bias-eta*e2
    bminus=bias+eta*e2
    # For any allowed mixture c=q[2] in [0,1], the two ideal biased outputs
    # differ by 4eta*c v -2eta v; magnitude <=2eta.
    for a in range(9):
        for b in range(9-a):
            q=sp.Matrix([R(a,8),R(b,8),R(8-a-b,8)])
            check_mixture(q)
            diff=S.subs(t,tplus)*q+bplus-(S.subs(t,tminus)*q+bminus)
            assert diff==2*eta*(2*q[2]-1)*e2
            assert (diff.T*diff)[0]<=4*eta**2
    out=dict(source_contract='One exact earlier source action establishes rank-one posterior; later biased sensor outputs y(q)=S(t)q+b+e with the SAME unknown b for all calls.',
             native_input_contract='q_i>=0, sum_i q_i=1, ||q||<=1',
             exact_two_probe_reconstruction=dict(inputs=[[frac(z) for z in q0],[frac(z) for z in q1]],
                    actual_readings=[[frac(z) for z in z0],[frac(z) for z in z1]],
                    recovered_latent=frac(recovered_t),recovered_unknown_bias=[frac(z) for z in recovered_bias],
                    additional_biased_native_calls=2),
             bounded_sensor_variant=dict(sensor_error_norm_bound=frac(eta),actual_noise_vectors=[[frac(z) for z in n0],[frac(z) for z in n1]],
                    certified_latent_interval=[frac(z) for z in certified_range],
                    universally_guaranteed_latent_radius=frac(2*eta)),
             one_call_impossibility='With unbounded unknown b, any one reported vector is compatible with every t in [1,3] by changing b.',
             adversarial_many_call_lower_bound=dict(source_latents=[frac(tminus),frac(tplus)],
                    distinct_fixed_biases=[[frac(z) for z in bminus],[frac(z) for z in bplus]],
                    worst_case_minimax_latent_error_at_least=frac(2*eta),
                    reason='For any allowable q, the two noiseless biased outputs differ by at most 2eta, so a shared reported vector can lie within eta of each. Repeating queries does not remove adversarial error.'),
             warning='If bias changes between the two measurements without a declared drift bound, exact reconstruction no longer follows.')
    file=Path(__file__).with_name('bias_cancelling_experiments_results.json')
    file.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print('PASSED exact self-calibration and noisy minimax lower bound:',out['bounded_sensor_variant']['certified_latent_interval'])

if __name__=='__main__':main()
