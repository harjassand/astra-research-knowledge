#!/usr/bin/env python3
"""Exact supply-driven saturation obstruction and a costed attenuation repair.

Local scientific computation only. The first-tranche artifacts are read, never
changed; all new outputs go beside this script.
"""
from pathlib import Path
import json
import math
import numpy as np

OUT=Path(__file__).resolve().parent


def codes(y, word, M=1., K=128, words=65536):
    z=np.clip(y,-M,M)
    t=np.abs(z)*K/M
    lo=np.floor(t)
    return (np.sign(z)*(lo+((word+.5)/words<t-lo))).astype(np.int16)


def repair_certificate(N,U,P,*,E0=16.,d=1,m=1,M=1.,K=128,
                       words=65536,failure=.01):
    assert N%d==0
    V=E0+N*(U*U+P)
    analog_range=math.sqrt(V)
    gain=M/analog_range
    original_step=analog_range/K
    ep=1/(2*words)
    T=(V+original_step*(1+2*ep)*math.sqrt(m*N*V)
       +ep*N*m*original_step*original_step)
    noise=math.sqrt(T/failure)/(N/d*U)
    bias=math.sqrt(d*m)*ep*original_step/U
    return dict(N=N,d=d,m=m,input_amplitude=U,supply_energy_per_window=P,
                initial_energy_bound=E0,total_energy_bound=V,
                maximum_warranted_analogue_range=analog_range,
                pre_ADC_gain=gain,ADC_levels=2*K+1,
                ADC_range=[-M,M],ADC_spacing=M/K,
                reconstructed_grid_spacing=original_step,
                dither_bits=int(math.log2(words)),
                operator_radius=noise+bias,noise_radius=noise,
                finite_dither_bias_radius=bias,failure_probability=failure,
                controlled_input_energy=N*U*U,external_supply_energy=N*P)


def stats(v):
    return dict(min=float(np.min(v)),median=float(np.median(v)),
                max=float(np.max(v)),mean=float(np.mean(v)))


def main():
    first=json.loads((OUT.parent/'RESULTS.json').read_text())
    old_U=first['declared_design']['amplitude']
    old_radius=first['declared_design']['operator_radius']
    old_task_radius=first['execution']['ridge_task_certificate_radius']
    N=65536; paths=256; U=.7; M=1.; K=128; words=65536
    lam=.5; b=.4; a=math.sqrt(lam); c=math.sqrt(1-lam)
    W=2.2; P=W*W; h=c*W; dark_energy=9.
    optimum=b/(2*math.sqrt(lam))
    cert=repair_certificate(N,U,P)
    gain=cert['pre_ADC_gain']
    rng_s=np.random.default_rng(7201030)
    rng_w=np.random.default_rng(7201031)
    rng_q=np.random.default_rng(7201032)
    rng_oldq=np.random.default_rng(7201033)
    signed_a=np.array([a,-a])[:,None]
    S=np.array([[[a,c],[c,-a]],[[-a,c],[c,a]]])
    orthogonality=float(np.max(np.abs(np.swapaxes(S,1,2)@S-np.eye(2))))
    assert orthogonality<1e-14
    # Exhaust all relevant affine extrema and a dense command grid.
    grid=np.linspace(-U,U,10001)
    saturation_margin=float(np.min(np.abs(
        signed_a[:,:,None]*grid[None,None,:]
        +np.array([-h,h])[None,:,None]))-M)
    assert saturation_margin>0
    # Strongest ordinary comparator when the explicitly given pair is known:
    # a larger calibrated gain, using its actual analogue range, identifies
    # the member in one read for every possible finite dither word.
    pair_gain=M/(h+a*U)
    exhaustive_word=np.arange(words)
    pair_ambiguities=0
    for command_sign in [-1.,1.]:
        qp=[codes(pair_gain*(a*command_sign*U+bath_sign*h),
                  exhaustive_word,M,K,words) for bath_sign in [-1.,1.]]
        qm=[codes(pair_gain*(-a*command_sign*U+bath_sign*h),
                  exhaustive_word,M,K,words) for bath_sign in [-1.,1.]]
        pair_ambiguities+=sum(int(np.sum(vp==vm)) for vp in qp for vm in qm)
    assert pair_ambiguities==0
    atten_sums=np.zeros((2,paths)); fixed_sums=atten_sums.copy()
    full_sums=atten_sums.copy(); output_energy=atten_sums.copy()
    energy_residual=0.; fixed_disagreements=0; atten_disagreements=0
    atten_saturation_count=0
    eliminated=np.full((2,paths),N+1,dtype=np.int64)
    # The first-tranche protocol, applied outside its admitted class, is
    # evaluated on a 2D embedding with A=diag(+/-sqrt(lambda),1).
    old_sums=np.zeros((paths,2,2))
    old_saturation_count=0
    for t in range(N):
        # Uncontrolled field exists before the fresh controlled-input sign.
        v=rng_w.choice(np.array([-1.,1.]),size=paths)
        s=rng_s.choice(np.array([-1.,1.]),size=paths)
        x=U*s
        w=W*v
        y=signed_a*x[None,:]+c*w[None,:]
        inaccessible=c*x[None,:]-signed_a*w[None,:]
        energy_residual=max(energy_residual,float(np.max(np.abs(
            y*y+inaccessible*inaccessible-(U*U+P)))))
        output_energy+=y*y
        word=rng_q.integers(0,words,size=paths)
        qfixed=codes(y,word[None,:],M,K,words)
        fixed_disagreements+=int(np.sum(qfixed[0]!=qfixed[1]))
        assert np.all(qfixed==K*v[None,:])
        qatten=codes(gain*y,word[None,:],M,K,words)
        atten_disagreements+=int(np.sum(qatten[0]!=qatten[1]))
        atten_saturation_count+=int(np.sum(np.abs(gain*y)>M))
        reconstructed=qatten*(M/K/gain)
        atten_sums+=s[None,:]*reconstructed
        fixed_sums+=s[None,:]*qfixed*(M/K)
        full_sums+=s[None,:]*y
        # An ordinary consistency decoder knows the explicitly given pair,
        # sees the same dither word, and allows either unobserved bath sign.
        for actual in range(2):
            rival=1-actual
            rival_plus=codes(gain*(signed_a[rival,0]*x+h),word,M,K,words)
            rival_minus=codes(gain*(signed_a[rival,0]*x-h),word,M,K,words)
            incompatible=(qatten[actual]!=rival_plus)&(qatten[actual]!=rival_minus)
            newly=incompatible&(eliminated[actual]==N+1)
            eliminated[actual,newly]=t+1
        # Same fixed ADC law, same dither precision and public constants as
        # phase 1, but the external supply invalidates its no-supply premise.
        j=t%2
        old_primary=M*v
        old_secondary=(old_U*s if j==1 else np.zeros(paths))
        old_secondary_q=codes(old_secondary,
            rng_oldq.integers(0,words,size=paths),M,K,words)*(M/K)
        old_sums[:,0,j]+=s*old_primary
        old_sums[:,1,j]+=s*old_secondary_q
        old_saturation_count+=paths
    assert fixed_disagreements==0
    assert atten_saturation_count==0
    Ahat=atten_sums/(N*U)
    Ahat_fixed=fixed_sums/(N*U)
    Ahat_full=full_sums/(N*U)
    # Conventional least squares on precisely these same reconstructed reads.
    ordinary_OLS=(U*atten_sums)/(N*U*U)
    ordinary_difference=float(np.max(np.abs(Ahat-ordinary_OLS)))
    assert ordinary_difference<1e-14
    true=np.broadcast_to(signed_a,Ahat.shape)
    errors=np.abs(Ahat-true)
    repaired_u=b*Ahat/(Ahat*Ahat+lam)
    true_u=np.broadcast_to(np.array([optimum,-optimum])[:,None],Ahat.shape)
    task_errors=np.abs(repaired_u-true_u)
    assert np.max(task_errors-(b/lam)*errors)<1e-12
    legacy_A=old_sums/(N/2*old_U)
    legacy_true=np.zeros((2,paths,2,2))
    legacy_true[:,:,0,0]=signed_a
    legacy_true[:,:,1,1]=1.
    legacy_errors=np.linalg.norm(legacy_A[None,:,:,:]-legacy_true,axis=(2,3))
    legacy_b=np.broadcast_to(np.array([b,0.]),(paths,2))
    legacy_lhs=np.einsum('pki,pkj->pij',legacy_A,legacy_A)+lam*np.eye(2)
    legacy_rhs=np.einsum('pki,pk->pi',legacy_A,legacy_b)
    legacy_u=np.linalg.solve(legacy_lhs,legacy_rhs[...,None])[...,0]
    legacy_target=np.zeros((2,paths,2)); legacy_target[:,:,0]=true_u
    legacy_task_errors=np.linalg.norm(legacy_u[None,:,:]-legacy_target,axis=2)
    assert np.min(np.max(legacy_task_errors,axis=0))>=optimum-1e-12
    curves=[]
    for count in [4096,16384,65536,262144,1048576]:
        row=repair_certificate(count,U,P)
        row['ridge_task_radius']=b/lam*row['operator_radius']
        curves.append(row)
    sensor_energy=gain*gain*output_energy
    lost_energy=(1-gain*gain)*output_energy
    results=dict(
        obstruction=dict(control_bound=U,ADC_bound=M,ridge_lambda=lam,
            target_b=b,incremental_gains=[a,-a],bath_coupling=c,
            supply_amplitude=W,supply_energy_per_window=P,
            supply_law='independent equiprobable signs, zero mean, before input sign',
            primary_field_magnitude=h,minimum_saturation_margin=saturation_margin,
            hard_clipping_sufficient_power_threshold=(M+a*U)**2/(1-lam),
            two_optimal_commands=[optimum,-optimum],
            minimax_absolute_radius=optimum,
            minimax_expected_squared_command_error=optimum*optimum,
            minimax_expected_excess_objective=b*b/4,
            any_uniform_radius_below_minimax_has_success_at_most_one_half=True,
            forward_and_adjoint_same_symmetric_lossless_two_port=True,
            unchanged_dark_state_energy=dark_energy,
            inaccessible_port_is_not_observed=True,
            no_claim_for_Gaussian_equilibrium_bath=True),
        executed_checks=dict(paired_paths=paths,windows_each=N,
            unitary_matrix_residual=orthogonality,
            maximum_per_window_energy_residual=energy_residual,
            fixed_ADC_transcript_disagreements=fixed_disagreements,
            attenuated_ADC_transcript_disagreements=atten_disagreements,
            attenuated_ADC_saturations=atten_saturation_count,
            original_ADC_every_read_saturated=True),
        failed_extension_of_phase1=dict(
            warning='This deliberately violates phase 1 no-supply premise; it is not a counterexample to that theorem.',
            dimension=2,first_protocol_amplitude=old_U,
            incorrectly_reused_operator_radius=old_radius,
            incorrectly_reused_task_radius=old_task_radius,
            operator_errors=stats(legacy_errors),
            fraction_violating_inapplicable_operator_radius=float(np.mean(legacy_errors>old_radius)),
            task_errors=stats(legacy_task_errors),
            fraction_violating_inapplicable_task_radius=float(np.mean(legacy_task_errors>old_task_radius)),
            saturated_scalar_reports_per_specimen=N),
        repair=dict(certificate=cert,
            operator_errors=stats(errors),
            task_errors=stats(task_errors),
            task_certificate_radius=b/lam*cert['operator_radius'],
            zero_command_radius=optimum,
            operator_certificate_violations=int(np.sum(errors>cert['operator_radius'])),
            ordinary_least_squares_max_difference=ordinary_difference,
            full_signed_read_operator_errors=stats(np.abs(Ahat_full-true)),
            known_pair_consistency_decoder_reads=stats(eliminated),
            known_pair_decoder_unresolved=int(np.sum(eliminated>N)),
            known_pair_decoder_uses_extra_model_structure=True,
            known_pair_best_gain=pair_gain,
            known_pair_best_one_read_decoder_ambiguities=pair_ambiguities,
            known_pair_best_one_read_decoder_exhausts_all_16bit_words=True,
            measured_output_energy=stats(output_energy),
            energy_delivered_to_ADC=stats(sensor_energy),
            energy_lost_at_attenuator=stats(lost_energy)),
        resources_per_repaired_specimen=dict(
            physical_windows=N,active_windows=N,scalar_reads=N,
            resets=0,idle_windows=0,adjoint_operations=0,
            calibrated_gain_settings=1,
            fixed_report_bits=N*9,ADC_random_bits=N*16,
            controlled_input_energy=N*U*U,external_supply_energy=N*P,
            gain_calibration='exact mathematical operation; no hardware qualification',
            apparatus_control_and_cooling_work='unmeasured',
            counterfactual_interfaces_are_not_free_simultaneous_reads=True),
        theorem_budget_curve=curves)
    (OUT/'RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    np.savez_compressed(OUT/'NUMERICAL_RECORD.npz',Ahat=Ahat,
        fixed_ADC_Ahat=Ahat_fixed,full_read_Ahat=Ahat_full,
        legacy_Ahat=legacy_A,legacy_commands=legacy_u,
        known_pair_first_elimination=eliminated,
        output_energy=output_energy,attenuator_loss_energy=lost_energy)
    print(json.dumps(dict(obstruction=results['obstruction'],
        executed_checks=results['executed_checks'],
        failed_extension=results['failed_extension_of_phase1'],
        repair=results['repair']),indent=2))


if __name__=='__main__':
    main()
