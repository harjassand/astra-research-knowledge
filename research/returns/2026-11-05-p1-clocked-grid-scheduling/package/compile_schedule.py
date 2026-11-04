"""Exact finite scheduler and interval certificate; does not operate hardware.

Usage: python compile_schedule.py fleet_input.json schedule_output.json
All decimals are parsed as rational numbers. Endpoint timer phases are exact
integer ticks. Hardware waveform, clock, membership and actuator contracts
must be independently supplied and verified before physical use.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import json, sys
from reproduce import midpoint_phases, nearest_tick, discrepancy_certificate

def ceil_fraction(v):return -(-v.numerator//v.denominator)

def compile_fleet(config):
    period=F(str(config['period_s']))
    tick=F(str(config['timer_tick_s']))
    clock=F(str(config['per_event_timing_error_s']))
    if period<=0 or tick<=0 or clock<0 or (period/tick).denominator!=1:
        raise ValueError('Invalid period, tick, or timing budget.')
    devices=config['devices']
    ids=[d['id'] for d in devices]
    if len(set(ids))!=len(ids):raise ValueError('Duplicate device identifiers.')
    classes=defaultdict(list)
    for d in devices:
        d=dict(d)
        for name in ['absolute_event_energy_J','repeatable_waveform_L1_error_J','minimum_interval_s','maximum_interval_s']:
            d[name]=F(str(d[name]))
        if 'old_nominal_phase_s' not in d:
            raise ValueError('Supply the old nominal phase explicitly for '+d['id'])
        d['old_nominal_phase_s']=F(str(d['old_nominal_phase_s']))%period
        if (d['old_nominal_phase_s']/tick).denominator!=1:
            raise ValueError('The old nominal phase must be represented on the declared timer grid.')
        if d['absolute_event_energy_J']<=0 or d['repeatable_waveform_L1_error_J']<0:
            raise ValueError('Energy weight/error sign invalid.')
        if d['minimum_interval_s']<0 or d['maximum_interval_s']<d['minimum_interval_s']:
            raise ValueError('Invalid diagnostic interval contract.')
        if not (period-2*clock>=d['minimum_interval_s'] and period+2*clock<=d['maximum_interval_s']):
            raise ValueError('Cadence cannot tolerate the declared clock error for '+d['id'])
        classes[d['waveform_class']].append(d)
    phase_records=[];class_records=[];B=F(0);total_energy=F(0);total_mismatch=F(0)
    for label,group in classes.items():
        weights=[d['absolute_event_energy_J'] for d in group]
        ideal=midpoint_phases(weights,period)
        phase=[nearest_tick(p,tick,period) for p in ideal]
        cert=discrepancy_certificate(weights,phase,period)
        nominal=F(cert['span_exact']);energy=sum(weights)
        mismatch=sum(d['repeatable_waveform_L1_error_J'] for d in group)
        bound=nominal+2*energy*clock/period+(1+2*clock/period)*mismatch
        B+=bound;total_energy+=energy;total_mismatch+=mismatch
        class_records.append({'class':label,'device_count':len(group),
            'nominal_event_span_J_exact':str(nominal),
            'certified_primitive_span_J_exact':str(bound),
            'certified_primitive_span_J':float(bound)})
        for d,phi in zip(group,phase):
            old_phase=d['old_nominal_phase_s']
            advance=(old_phase-phi)%period
            max_step_ticks=(period-d['minimum_interval_s']-2*clock)//tick
            max_step=max_step_ticks*tick
            if advance>0 and max_step<=0:
                raise ValueError('No allowed phase-migration slack for '+d['id'])
            advances=[];remain=advance
            while remain>0:
                step=min(remain,max_step);advances.append(step);remain-=step
            intervals=[period-step for step in advances]
            if not intervals:intervals=[period]
            assert min(intervals)-2*clock>=d['minimum_interval_s']
            assert max(intervals)+2*clock<=d['maximum_interval_s']
            assert ((old_phase+sum(intervals))%period)==phi
            phase_records.append({'id':d['id'],'class':label,
                'phase_seconds_exact':str(phi),'phase_tick':int(phi/tick),
                'old_nominal_phase_s_exact':str(old_phase),
                'commissioning_nominal_intervals_s_exact':[str(x) for x in intervals],
                'subsequent_nominal_interval_s_exact':str(period),
                'actual_interval_min_s':float(min(intervals)-2*clock),
                'actual_interval_max_s':float(period+2*clock),
                'maximum_nominal_advanced_extra_executions':int(advance>0),
                'transient_timing_reserve_required':True})
    return {'status':'MATHEMATICAL_CERTIFICATE_ONLY_NO_HARDWARE_COMMANDS',
        'period_s':float(period),'timer_tick_s':float(tick),'per_event_timing_error_s':float(clock),
        'total_absolute_event_energy_J':float(total_energy),
        'primitive_span_budget_J_exact':str(B),'primitive_span_budget_J':float(B),
        'first_order_frequency_bound':'B/M Hz only for supplied valid M*f_dot+D*f=-u model; no grid inertia inferred.',
        'general_frequency_bound':'B/2 * (|g(0)|+Var(g)), plus initial and uncontrolled background response.',
        'classes':class_records,'devices':phase_records,
        'assumptions':['Each diagnostic can be shifted without changing its function or calibrated waveform.',
            'Every nominal event occurs exactly once; no automatic burst replay of missed tests.',
            'Timing error is an absolute bound relative to the commissioned nominal event stream.',
            'Per-device residual waveform repeats and has the supplied per-event L1 bound.',
            'Membership and waveform class remain fixed; failed or rebooted devices need explicit handling.',
            'Persistent phase and last-event state survive reboot; minimum recovery and maximum deadline are supplied.',
            'The commissioning bridge starts after a test with the supplied old nominal phase (zero only when explicitly appropriate).',
            'Startup energy/power, missing events, unstable plant response and per-cycle bias drift are outside this certificate.']}

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit(__doc__)
    config=json.loads(Path(sys.argv[1]).read_text(),parse_float=str)
    result=compile_fleet(config)
    Path(sys.argv[2]).write_text(json.dumps(result,indent=2))
    print(json.dumps({'budget_J':result['primitive_span_budget_J'],
                      'phases_s':[r['phase_seconds_exact'] for r in result['devices']]}))
