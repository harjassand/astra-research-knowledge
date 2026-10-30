#!/usr/bin/env python3
"""Dense, low-amplitude identification of a passive specimen with a fixed ADC.

The controller's certificate uses only declared interface constants. The hidden
state and true response appear exclusively in numerical audit checks. No files
outside this script's directory are written.
"""
from pathlib import Path
import json
import math
import numpy as np

OUT = Path(__file__).resolve().parent


def certificate(N, U, *, d=2, m=2, E0=16., M=1., K=128,
                failure=.01, dither_words=65536):
    assert N % d == 0 and 0 < U < M
    n = N // d
    step = M / K
    ep = 1 / (2 * dither_words)
    incident = N * U * U
    total = E0 + incident
    # Finite random-word correction, not exact-unbiased continuous dither.
    T = (total + step * (1 + 2 * ep) * math.sqrt(m * N * total)
         + ep * N * m * step * step)
    H = (math.sqrt(total) + math.sqrt(incident)) ** 2
    noise = math.sqrt(T / failure) / (n * U)
    clipping = H / (n * (M - U) ** 2)
    dither_bias = math.sqrt(d * m) * ep * step / U
    return dict(N=N, amplitude=U, operator_radius=noise+clipping+dither_bias,
                noise_radius=noise, clipping_radius=clipping,
                finite_dither_bias_radius=dither_bias,
                total_incident_energy=incident, total_energy_bound=total,
                ADC_levels=2*K+1, ADC_range=[-M,M], ADC_spacing=step,
                dither_bits=round(math.log2(dither_words)),
                failure_probability=failure)


def design(N, **kwargs):
    # Optimize a theorem bound, before any plant or measurement is drawn.
    candidates = np.geomspace(.001, .7, 8192)
    return min((certificate(N, float(U), **kwargs) for U in candidates),
               key=lambda r: r['operator_radius'])


def rotation(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.stack([np.stack([c,-s],axis=-1),
                     np.stack([s,c],axis=-1)],axis=-2)


def quantize(y, uniform_word, M=1., K=128, words=65536):
    z = np.clip(y, -M, M)
    mag = np.abs(z) * K / M
    lo = np.floor(mag)
    fraction = mag - lo
    fresh_uniform = (uniform_word + .5) / words
    q = np.sign(z) * (lo + (fresh_uniform < fraction)) * M / K
    return q, np.abs(y) > M


def main():
    d=m=2; E0=16.; M=1.; K=128; failure=.01; words=65536
    bnorm=.4; ridge=.5; command_radius=.7
    N=65536; paths=256
    cert = design(N,d=d,m=m,E0=E0,M=M,K=K,failure=failure,
                  dither_words=words)
    U=cert['amplitude']
    rng = np.random.default_rng(701030)
    rng_sign = np.random.default_rng(701031)
    rng_adc = np.random.default_rng(701032)
    # Distinct passive all-pass cascades. Unknown relaxation spans 10^2 to
    # 10^12 windows, together with a perfectly dark, nondecaying coordinate.
    fast = rng.uniform(.1,.9,size=(paths,2))
    slow_exponents = rng.integers(2,13,size=(paths,2))
    slow = 1. - 10.**(-slow_exponents)
    cf = np.sqrt((1-fast)*(1+fast))
    cs = np.sqrt((1-slow)*(1+slow))
    left = rotation(rng.uniform(-math.pi,math.pi,size=paths))
    right = rotation(rng.uniform(-math.pi,math.pi,size=paths))
    # All initial energy is charged. Nine units remain forever in the dark.
    visible = rng.normal(size=(paths,4))
    visible *= math.sqrt(E0-9.) / np.linalg.norm(visible,axis=1)[:,None]
    zf,zs = visible[:,:2].copy(),visible[:,2:].copy()
    dark = np.full(paths,3.)
    A = np.einsum('pik,pk,pkj->pij',right,fast*slow,left)
    initial_energy = np.sum(zf*zf+zs*zs,axis=1)+dark*dark
    sums = np.zeros((paths,m,d)); full_sums=sums.copy()
    ordinary_sums=sums.copy()
    output_energy=np.zeros(paths); old_energy=np.zeros(paths)
    saturations=np.zeros(paths,dtype=np.int64)
    clipping_bias_sum=np.zeros((paths,m,d))
    saturated_read_record=[]
    max_balance_error=0.; max_response_error=0.
    step=M/K
    for t in range(N):
        j=t%d
        sign = rng_sign.choice(np.array([-1.,1.]),size=paths)
        x=np.zeros((paths,d)); x[:,j]=U*sign
        drive=np.einsum('pij,pj->pi',left,x)
        h=np.einsum('pij,pj->pi',right,-cs*zs-slow*cf*zf)
        old_energy += np.sum(h*h,axis=1)
        # Each stage is a real orthogonal two-port scattering operation.
        vf=-cf*zf+fast*drive
        n_zf=fast*zf+cf*drive
        vs=-cs*zs+slow*vf
        n_zs=slow*zs+cs*vf
        y=np.einsum('pij,pj->pi',right,vs)
        pred=np.einsum('pij,pj->pi',A,x)+h
        max_response_error=max(max_response_error,float(np.max(np.abs(pred-y))))
        energy_before=np.sum(zf*zf+zs*zs,axis=1)+dark*dark
        energy_after=np.sum(n_zf*n_zf+n_zs*n_zs,axis=1)+dark*dark
        balance=energy_after+np.sum(y*y,axis=1)-energy_before-U*U
        max_balance_error=max(max_balance_error,float(np.max(np.abs(balance))))
        output_energy+=np.sum(y*y,axis=1)
        # Exact two-sign clipping attenuation, using hidden h only as an audit.
        a=A[:,:,j]
        mu=(np.clip(h+U*a,-M,M)-np.clip(h-U*a,-M,M))/(2*U)
        clipping_bias_sum[:,:,j]+=mu-a
        dither_word=rng_adc.integers(0,words,size=(paths,m))
        q,warning=quantize(y,dither_word,M,K,words)
        for specimen in np.flatnonzero(np.any(warning,axis=1)):
            saturated_read_record.append(dict(
                window=t+1,specimen=int(specimen),coordinate=j,
                input_sign=int(sign[specimen]),ADC_report=q[specimen].tolist(),
                saturation_flags=warning[specimen].tolist(),
                dither_word=dither_word[specimen].tolist()))
        assert np.max(np.abs(q)) <= M+1e-12
        saturations += np.sum(warning,axis=1)
        sums[:,:,j] += sign[:,None]*q
        full_sums[:,:,j] += sign[:,None]*y
        # Equally informed conventional instrumental-variable identification
        # uses exactly the same sufficient statistic and operations.
        ordinary_sums[:,:,j] += sign[:,None]*q
        zf,zs=n_zf,n_zs
    n=N//d
    Ahat=sums/(n*U)
    ordinary=ordinary_sums/(n*U)
    Ahat_full=full_sums/(n*U)
    assert np.array_equal(Ahat,ordinary)
    err=np.linalg.norm(Ahat-A,axis=(1,2))
    full_err=np.linalg.norm(Ahat_full-A,axis=(1,2))
    final_energy=np.sum(zf*zf+zs*zs,axis=1)+dark*dark
    budget=E0+N*U*U
    assert np.max(output_energy+final_energy-budget)<1e-8
    H=(math.sqrt(budget)+math.sqrt(N*U*U))**2
    assert np.max(old_energy)<=H+1e-8
    actual_clip=np.linalg.norm(clipping_bias_sum/n,axis=(1,2))
    assert np.max(actual_clip) <= cert['clipping_radius']+1e-9
    # Tasks are selected after acquiring the record; operator confidence is
    # simultaneous for every b in the declared ball.
    task_b=bnorm*np.linalg.svd(Ahat,full_matrices=False)[0][:,:,0]
    def solve(B):
        lhs=np.einsum('pki,pkj->pij',B,B)+ridge*np.eye(d)[None,:,:]
        rhs=np.einsum('pki,pk->pi',B,task_b)
        return np.linalg.solve(lhs,rhs[...,None])[...,0]
    u=solve(Ahat); target=solve(A)
    task_error=np.linalg.norm(u-target,axis=1)
    assert np.max(np.linalg.norm(u,axis=1))<=bnorm/(2*math.sqrt(ridge))+1e-12
    assert np.max(task_error-bnorm/ridge*err)<1e-10
    task_radius=bnorm/ridge*cert['operator_radius']
    zero_radius=bnorm/(2*math.sqrt(ridge))
    # First failed representation: stochastic rounding of log amplitude.
    # sqrt(1*4)=2 has logarithmic fraction 1/2, so decoding has mean 2.5.
    log_failure=dict(lower=1.,upper=4.,amplitude=2.,
                     log_coordinate_round_up_probability=.5,
                     decoded_expected_amplitude=2.5,
                     persistent_bias=.5,
                     amplitude_coordinate_round_up_probability=1/3,
                     repaired_expected_amplitude=2.)
    curves=[]
    for count in [4096,16384,32768,65536,262144,1048576]:
        row=design(count,d=d,m=m,E0=E0,M=M,K=K,failure=failure,
                   dither_words=words)
        row['ridge_task_radius']=bnorm/ridge*row['operator_radius']
        curves.append(row)
    def stats(v):
        return dict(min=float(np.min(v)),median=float(np.median(v)),
                    max=float(np.max(v)),mean=float(np.mean(v)))
    result=dict(
        assumptions=dict(state_space='unknown contractive scattering colligation',
                         d=d,m=m,initial_energy_upper_bound=E0,
                         continuing_bath_energy=0,passivity='pathwise',
                         fixed_incremental_operator=True,
                         actuator_and_threshold_calibration='exact in simulation; not hardware qualified'),
        declared_design=cert,
        resources_per_specimen=dict(physical_windows=N,active_windows=N,
            idle_windows=0,vector_reads=N,scalar_reads=m*N,
            hidden_state_resets=0,forward_operations=N,adjoint_operations=0,
            input_sign_bits=N,ADC_random_bits=m*N*16,
            scalar_report_fixed_width_bits=9,
            ADC_report_bits=m*N*9,
            incident_energy=N*U*U,ADC_saturation_policy='all reports retained'),
        execution=dict(specimens=paths,
            nominal_relaxation_windows=[100,1000000000000],
            exactly_nondecaying_dark_energy=9.,
            max_incremental_response_identity_error=max_response_error,
            max_single_window_energy_balance_error=max_balance_error,
            final_energy=stats(final_energy),output_energy=stats(output_energy),
            old_field_energy=stats(old_energy),
            saturated_scalar_reports_per_specimen=stats(saturations),
            max_actual_conditional_clipping_bias=float(np.max(actual_clip)),
            bounded_ADC_operator_errors=stats(err),
            full_read_operator_errors=stats(full_err),
            bounded_ADC_operator_certificate_violations=int(np.sum(err>cert['operator_radius'])),
            ordinary_instrumental_variable_identification_equal=True,
            receiving_task_selection='dominant left singular vector of acquired Ahat; norm .4',
            audited_ridge_task_errors=stats(task_error),
            ridge_task_certificate_radius=task_radius,
            zero_experiment_task_radius=zero_radius,
            all_commands_within_declared_radius=bool(np.all(np.linalg.norm(u,axis=1)<=command_radius)),
            operator_bound_is_from_public_interface_constants=True,
            empirical_coverage_is_not_a_proof=True),
        failed_log_representation=log_failure,
        theorem_budget_curve=curves)
    (OUT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'SATURATED_READS.json').write_text(json.dumps(saturated_read_record,indent=2)+'\n')
    np.savez_compressed(OUT/'SIMULATION_RECORD.npz',A=A,Ahat=Ahat,
        Ahat_full=Ahat_full,task_b=task_b,command=u,target=target,
        output_energy=output_energy,final_energy=final_energy,
        old_field_energy=old_energy,saturated_scalar_reports=saturations)
    print(json.dumps(dict(design=cert,execution=result['execution']),indent=2))


if __name__ == '__main__':
    main()
