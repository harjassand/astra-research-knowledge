"""Ordinary SGD indexed by actual active pairs on root's identical PacketPort.

No source reconstruction, hardware change, hidden reset, rail change, horizon
change, outcome deletion, or importance weighting. Inactive windows really
elapse. The controller's certificates use only bounded ADC reports and guards.

The fixed calendar checkpoints are declared before execution. Conditional on
the independent complete activity schedule, their active-index horizons are
deterministic. Thus root's fixed-horizon certificates apply with p=w=1 and
their original failure allocation; future signs/dithers remain fresh.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
sys.path.insert(0, str(ROOT))
from check_bounded_task_learning import (
    PacketPort, CEXP, observed_noise_radius, worst_rail_noise_radius,
    ball, optimum_for_audit,
)

INPUTS = [
    'check_bounded_task_learning.py',
    'BOUNDED_TASK_LEARNING_WITH_PERSISTENT_MEMORY.md',
    'OBSERVED_VARIANCE_FOR_BOUNDED_PHYSICAL_GRADIENTS.md',
    'BOUNDED_TASK_CHECK_RESULTS.json',
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(rounds=262144):
    input_pins = {name: sha(ROOT/name) for name in INPUTS}
    # These are exactly the root fixture, source seed, controller seed and
    # schedule. No outcome-dependent tuning or additional RNG consumption.
    port = PacketPort(2026103014)
    rng = np.random.default_rng(1401)
    U, lam, kappa, levels, alpha = .7, .5, .5, 257, .05
    target = np.array([.32, -.24])
    Ry = 4*U
    rmax = Ry*np.sqrt(2)+np.linalg.norm(target)
    V = kappa*rmax
    Rz = 4*(U+V)
    dy, dz = 2*Ry/(levels-1), 2*Rz/(levels-1)
    assert Ry > 3*U+2*dy and Rz > 3*(U+V)+2*dz
    CF = 2*U+2*rmax

    u = np.zeros(2)
    sumu = np.zeros(2)
    sumg = np.zeros(2)
    squares = np.zeros(2)
    flag_debit = 0.
    active = flag_y = flag_z = 0
    expected_active = 0.
    checkpoints, records, adc_codes, clipping_audit = [], [], [], []
    # Auditor-only evaluation. These do not enter commands or certificates.
    A = port.oracle_matrix()
    ustar, multiplier = optimum_for_audit(A, target, lam, U)
    objective = lambda v: float((np.linalg.norm(A@v-target)**2+lam*(v@v))/2)
    Fstar = objective(ustar)

    for i in range(1, rounds+1):
        bits = (((i-1).bit_length())+2)//3
        p = 2.**(-bits)
        on = bool(rng.integers(0, 1 << bits) == 0)
        expected_active += p
        if on:
            active += 1
            # u is the pre-pair command; only an active pair changes it.
            sigma = float(rng.choice([-1, 1]))
            before_clips = port.clipped_coefficients
            qy = port.read(sigma*u, Ry, levels)
            clip_y = port.clipped_coefficients-before_clips
            residual = sigma*qy-target
            tau = float(rng.choice([-1, 1]))  # Drawn after the first ADC.
            before_clips = port.clipped_coefficients
            qz = port.read(kappa*tau*residual, Rz, levels)
            clip_z = port.clipped_coefficients-before_clips

            signal = tau*qz/kappa   # No activity importance weight.
            g = lam*u+signal
            fy = (np.abs(qy) >= Ry-2*U-dy).astype(int)
            fz = (np.abs(qz) >= Rz-2*(U+V)-dz).astype(int)
            at_y_rail = (np.abs(qy) >= Ry-1e-12).astype(int)
            at_z_rail = (np.abs(qz) >= Rz-1e-12).astype(int)
            debit = U*np.sum(fy)+rmax*np.sum(fz)
            flag_debit += debit
            flag_y += int(np.sum(fy))
            flag_z += int(np.sum(fz))
            squares += signal**2
            # Predeclared uniform averages of all active pre-update u/g.
            sumu += u
            sumg += g
            records.append(np.r_[i, active, p, sigma, tau, u, qy, qz,
                                 fy, fz, at_y_rail, at_z_rail, g])
            adc_codes.append(np.r_[np.rint((qy+Ry)/dy),
                                   np.rint((qz+Rz)/dz)].astype(np.int16))
            # An auditor can distinguish actual clipping from a rounded rail
            # code. The learner receives only the rail codes/guards above.
            clipping_audit.append([i, active, clip_y, clip_z])
            u = ball(u-2*g/(lam*(active+1)), U)
        else:
            port.idle()
            port.idle()

        if i >= 64 and i & (i-1) == 0:
            j = i.bit_length()-1
            av, gg = sumu/active, sumg/active
            aj = 6*alpha/(np.pi**2*(j+1)**2)
            delta = aj/3
            # Active-index fixed horizon k, p_k=w_k=1, a_k=1.
            drift = (flag_debit+CF*np.log(1/delta))/CEXP
            Hobs, vhat, gridK = observed_noise_radius(
                squares, active, 1., Rz, kappa, delta, delta)
            Hrail = worst_rail_noise_radius(
                active, 1., Rz, kappa, 2, delta)
            eobs = (Hobs+drift)/active
            erail = (Hrail+drift)/active
            eta = 1/(1+lam)
            mapping = np.linalg.norm(av-ball(av-eta*gg, U))/(eta*lam)
            trueg = A.T@(A@av-target)+lam*av
            checkpoints.append(dict(
                calendar_pairs=i, active_index_horizon=active,
                physical_windows=port.calls,
                paid_zero_input_windows=2*(i-active),
                averaging='Uniform over every active pre-update command and gradient',
                observed_guard_counts=[flag_y, flag_z],
                observed_guard_debit=float(flag_debit),
                observed_gradient_square_sums=squares.tolist(),
                observed_predictable_second_moment_upper=vhat.tolist(),
                mean_gradient_radius_observed_squares=float(eobs),
                mean_gradient_radius_worst_rail=float(erail),
                clipping_debit_per_active_pair=float(drift/active),
                noise_radius_per_active_pair=float(Hobs/active),
                fixed_point_residual_component=float(mapping),
                optimum_distance_certificate_observed=float(mapping+eobs/lam),
                optimum_distance_certificate_worst_rail=float(mapping+erail/lam),
                actual_gradient_error_audit_only=float(np.linalg.norm(gg-trueg)),
                actual_optimum_distance_audit_only=float(np.linalg.norm(av-ustar)),
                objective_excess_audit_only=objective(av)-Fstar,
                variance_grid_levels=gridK+1,
                checkpoint_allocated_failure=float(aj),
                audited_stored_energy=port.energy(),
            ))

    av = sumu/active
    record_path = OUT/'ACTIVE_PAIR_LEARNING_RECORD.npz'
    columns = ['calendar_pair', 'active_index', 'activity_probability', 'sigma', 'tau',
               'u0', 'u1', 'yhat0', 'yhat1', 'zhat0', 'zhat1',
               'guard_y0', 'guard_y1', 'guard_z0', 'guard_z1',
               'rail_y0', 'rail_y1', 'rail_z0', 'rail_z1', 'g0', 'g1']
    np.savez_compressed(record_path, active_record=np.asarray(records),
        columns=np.asarray(columns), finite_adc_codes=np.asarray(adc_codes),
        target=target, learned_waveform=av, mean_gradient=sumg/active,
        U=np.array(U), regularization=np.array(lam), kappa=np.array(kappa),
        rails=np.array([Ry, Rz]), adc_levels=np.array(levels),
        calendar_pairs=np.array(rounds))
    audit_path = OUT/'ACTIVE_PAIR_CLIPPING_AUDIT.json'
    audit_path.write_text(json.dumps(dict(
        scope='Population auditor only; no exact clipping bit supplied to learner.',
        columns=['calendar_pair','active_index','clipped_forward_coefficients',
                 'clipped_reverse_coefficients'],
        active_pair_clipping_counts=clipping_audit), indent=2)+'\n')

    conservation = port.energy()+port.total_out-port.initial_energy-port.total_in
    assert abs(conservation) < 1e-7
    assert port.max_balance < 1e-9
    assert port.dark == 3.
    assert port.maximum_input_norm <= max(U, V)+1e-10
    assert port.adc_reads == 2*active
    assert port.calls == 2*rounds
    assert port.clipped_coefficients > 0 and flag_y+flag_z > 0
    assert np.max(adc_codes) < levels and np.min(adc_codes) >= 0

    root_result = json.loads((ROOT/'BOUNDED_TASK_CHECK_RESULTS.json').read_text())
    incumbent = root_result['persistent_run']
    root_record = np.load(ROOT/'BOUNDED_TASK_ACTIVE_RECORD.npz')['active_record']
    active_record = np.asarray(records)
    # The common keys and calendar schedule really match the prior run.
    assert np.array_equal(root_record[:,0], active_record[:,0])
    assert np.array_equal(root_record[:,1], active_record[:,2])
    assert np.array_equal(root_record[:,2:4], active_record[:,3:5])
    assert active == incumbent['active_pairs']
    assert input_pins == {name: sha(ROOT/name) for name in INPUTS}

    run = dict(
        scope='One persistent population simulation; no hardware or empirical-coverage claim.',
        source='Unmodified PacketPort imported from the pinned root source',
        calendar_pairs=rounds, physical_windows=port.calls,
        physical_time_in_fixed_packet_window_units=port.calls,
        active_pairs=active, active_physical_windows=2*active,
        paid_zero_input_windows=2*(rounds-active),
        adc_vector_reads=port.adc_reads, adc_scalar_reports=2*port.adc_reads,
        fixed_adc_levels=levels, fixed_adc_bits_per_coordinate=9,
        first_rail=Ry, second_rail=Rz, first_step=dy, second_step=dz,
        forward_input_norm_cap=U, replay_input_norm_cap=float(V),
        maximum_actual_input_norm=float(port.maximum_input_norm),
        initializations=1, hidden_resets=0, initial_energy=port.initial_energy,
        final_energy=port.energy(), frozen_dark_energy=9.,
        slow_observable_retention_per_window=.999999,
        actual_clipped_scalar_reports_audit_only=port.clipped_coefficients,
        first_guard_flags=flag_y, second_guard_flags=flag_z,
        observed_forward_rail_codes=int(np.sum(active_record[:,15:17])),
        observed_reverse_rail_codes=int(np.sum(active_record[:,17:19])),
        actual_saturation_records_excluded=0,
        total_incident_energy=float(port.total_in),
        total_outgoing_energy=float(port.total_out),
        maximum_raw_output_norm_auditor_only=float(port.maximum_raw_norm),
        sufficient_uniform_external_norm_rating=float(
            np.sqrt(port.initial_energy)+3*max(U,V)*np.sqrt(2)),
        complete_energy_identity_error=float(conservation),
        maximum_call_energy_error=float(port.max_balance),
        expected_active_pairs=float(expected_active),
        total_declared_checkpoint_failure_probability=alpha,
        feasible_set_diameter=2*U, oracle_constraint_multiplier=float(multiplier),
        learned_waveform=av.tolist(), mean_gradient=(sumg/active).tolist(),
        checkpoints=checkpoints, record_file=record_path.name,
        record_sha256=sha(record_path), clipping_audit_file=audit_path.name,
        clipping_audit_sha256=sha(audit_path),
    )
    comparison = dict(
        same_calendar_horizon=True, same_source_and_limits=True,
        same_activity_sequence_and_signs=True, same_ADC_dither_stream=True,
        incumbent_updates='Calendar index, importance-weighted signal, weights i',
        current_updates='Active index only, unweighted signal, uniform active average',
        incumbent_final=incumbent['checkpoints'][-1],
        current_final=checkpoints[-1],
        incumbent_total_incident_energy=incumbent['total_incident_energy'],
        current_total_incident_energy=run['total_incident_energy'],
        incumbent_actual_clipped_scalar_reports=incumbent['actual_clipped_scalar_reports'],
        current_actual_clipped_scalar_reports=port.clipped_coefficients,
        no_uniform_superiority_claim=True,
    )
    result = dict(script_sha256=sha(Path(__file__)), input_sha256=input_pins,
        persistent_run=run, matched_comparison=comparison,
        binding_scope=[
            'ADC conditional mean holds given all pre-read physical/instrument history and current commands/signs; dither is fresh.',
            'Conditioning on the independent whole activity schedule leaves signs/dithers fresh; fixed calendar checkpoints then have deterministic active-index horizons.',
            'There is no importance weighting, inactive update, hidden reset, saturation deletion or hidden-matrix learner input.',
            'Every inactive pair consists of two real fixed-duration matched windows.',
            'Actual clipping counts are population audits, separate from the learner-visible rail codes and guards.',
            'Bounded commands do not remove calibration, actuation-resolution, timing, sensing, randomness or arithmetic costs.',
            'The source has no uncharged ongoing native bath-energy injection.',
            'One trajectory cannot establish confidence coverage or a universal optimizer advantage.',
        ])
    result_path = OUT/'ACTIVE_PAIR_LEARNING_CHECKS.json'
    result_path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in run.items() if k!='checkpoints'}), flush=True)
    print(json.dumps({'matched_final_comparison':comparison}), flush=True)


if __name__ == '__main__':
    main()
