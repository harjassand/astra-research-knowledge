"""Reproduce the executed experimental-design result and its certificates.

Usage: python3 run.py [--check-only]
Uses only the Python standard library. No CAD implementation or external
solver is called. Files are written beside this script only in build mode.
"""
import argparse
import copy
import json
import platform
import time
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

from experiments import (ExperimentGame,verify_game,normalize,root_range,
                         envelope,potential,require)
from programme_models import (loop_machine,delayed_halt_machine,
                              coefficient_interval,evaluate,common_report)

HERE=Path(__file__).resolve().parent


def dump(name,obj):
    (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')


def fixture():
    return {'slopes':['1','3'],'physical_error':'1/32','forcing':'1',
            'budget':2,'prior_data':[['0','0','0']],
            'experiments':[{'x':x,'precision_bits':4,'cost':1}
                           for x in ['1/4','1/2','3/4','1']]}


def machine_checks():
    out=[]
    cases=[('invariant-state loop',loop_machine(),Q(1,2))]
    for t in [0,1,8,32,64]:
        cases.append((f'halts at {t}',delayed_halt_machine(t),
                      Q(1,2)+Q(1,1<<(t+2))))
    for label,machine,truth in cases:
        rows=[]
        for p in [0,1,4,8,16,32,64]:
            lo,hi=coefficient_interval(machine,p)
            require(lo<=truth<=hi and hi-lo<=Q(1,1<<p))
            rows.append({'precision_bits':p,'interval':[str(lo),str(hi)]})
            for x in [Q(-7,3),Q(0),Q(11,7)]:
                for quantity in ['potential','gradient','equilibrium']:
                    target={'potential':x*x/2+truth*x,
                            'gradient':x+truth,'equilibrium':-truth}[quantity]
                    a,b=evaluate(machine,1,x,p,quantity)
                    require(a<=target<=b and b-a<=Q(1,1<<p))
        out.append({'case':label,'known_coefficient':str(truth),'evaluations':rows})
    # Direct checks of the common-report construction. These are finite
    # controls for the formula; they do not prove the general bit bound.
    common_checks=0
    for B in range(4,11):
        beta=Q(1,1<<(2*B+3))
        for denominator in [1,3,5,7,11]:
            for numerator in range(-denominator,denominator+1):
                x=Q(numerator,denominator)
                if x.denominator.bit_length()>B:
                    continue
                for p in range(B+1):
                    y=common_report(x,p,beta)
                    require(y is not None)
                    q=Q(1,1<<p);eta=Q(1,4)+q/2
                    require(abs(y-x)<=eta and abs(y-(x+Q(1,2)+beta))<=eta)
                    common_checks+=1
    return {'bounded_simulation_fixtures':out,
            'common_report_checks':common_checks,
            'nonhalting_status':'Only the specified invariant-state loop is proved nonhalting; no general nonhalting test was run.'}


def verify(spec,cert,schedules):
    result=verify_game(spec,cert)
    game=ExperimentGame(spec)
    expected=[]
    for k in range(3):
        for schedule in product(range(len(game.actions)),repeat=k):
            expected.append({'actions':list(schedule),
                             'risk':str(game.fixed_schedule_value(schedule))})
    require(schedules==expected,'Fixed-schedule enumeration mismatch')
    best_fixed=min(Q(row['risk']) for row in schedules)
    zero_value=Q(schedules[0]['risk'])
    one_value=min(Q(row['risk']) for row in schedules if len(row['actions'])==1)
    require(Q(cert['value'])==Q(1,12) and best_fixed==Q(5,48))
    require(zero_value==Q(1,3) and one_value==Q(5,32))
    require(result['verified_nodes']==len(cert['nodes']))
    edges=sum(len(a['children']) for n in cert['nodes'] for a in n['actions'])
    require(cert['counts']=={'unique_states':len(cert['nodes']),
                            'stored_response_edges':edges})
    data=normalize(cert['worst_case_witness']['shared_data'])
    roots=list(map(Q,cert['worst_case_witness']['root_values']))
    source_checks=[]
    for endpoint,r in zip(['upper','lower'],roots):
        require(envelope(game.m,game.L,data,r,endpoint)==game.forcing)
        for x,lo,hi in data:
            value=envelope(game.m,game.L,data,x,endpoint)
            require(lo<=value<=hi)
        source_checks.append({'source':endpoint+' envelope',
                              'equilibrium':str(r),
                              'potential_at_equilibrium':str(potential(game.m,game.L,data,r,endpoint))})
    # An all-future continuum ambiguity witness for the same prior, with
    # refinable quantization and observation region [0,1].
    m,L=game.m,game.L;u=game.forcing;delta=game.delta
    amplitude=min(2*delta,u*(1-m/L));cut=amplitude/(L-m)
    low_root=u/m;high_force_root=(u-amplitude)/m
    require(high_force_root>=cut)
    require(m*high_force_root+amplitude==u)
    continuum={'lower_force':'g(x)=m*x',
               'higher_force':'f(x)=m*x+(L-m)*min(max(x,0),cut)',
               'cut':str(cut),'uniform_force_difference':str(amplitude),
               'equilibria':[str(high_force_root),str(low_root)],
               'optimal_unlimited_finite_experiment_risk':str(amplitude/(2*m))}
    # Controls target proof-relevant omissions and arithmetic corruption.
    bad=copy.deepcopy(cert);bad['nodes'][bad['root']]['value']='0'
    rejected_value=False
    try:verify_game(spec,bad)
    except ValueError:rejected_value=True
    bad=copy.deepcopy(cert);bad['nodes'][bad['root']]['actions'].pop()
    rejected_action=False
    try:verify_game(spec,bad)
    except ValueError:rejected_action=True
    bad=copy.deepcopy(cert);bad['nodes'][bad['root']]['actions'][0]['children'].pop()
    rejected_response=False
    try:verify_game(spec,bad)
    except ValueError:rejected_response=True
    require(rejected_value and rejected_action and rejected_response)
    result.update({'response_edges':edges,'fixed_schedules_checked':len(schedules),
                   'no_measurement_value':str(zero_value),
                   'best_one_measurement_value':str(one_value),
                   'best_fixed_value':str(best_fixed),
                   'source_checks':source_checks,'continuum_witness':continuum,
                   'corrupted_value_rejected':rejected_value,
                   'missing_action_rejected':rejected_action,
                   'missing_response_rejected':rejected_response})
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only',action='store_true')
    args=parser.parse_args();start=time.monotonic()
    if args.check_only:
        spec=json.loads((HERE/'EXPERIMENT_INPUT.json').read_text())
        cert=json.loads((HERE/'EXPERIMENT_CERTIFICATE.json').read_text())
        schedules=json.loads((HERE/'FIXED_SCHEDULES.json').read_text())
    else:
        spec=fixture();game=ExperimentGame(spec);cert=game.solve()
        schedules=[]
        for k in range(3):
            for schedule in product(range(len(game.actions)),repeat=k):
                schedules.append({'actions':list(schedule),
                                  'risk':str(game.fixed_schedule_value(schedule))})
        dump('EXPERIMENT_INPUT.json',spec)
        # Compact storage preserves all nodes, actions and reports.
        (HERE/'EXPERIMENT_CERTIFICATE.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
        dump('FIXED_SCHEDULES.json',schedules)
    checked=verify(spec,cert,schedules);machines=machine_checks()
    root=cert['nodes'][cert['root']]
    chosen=next(b for b in root['actions'] if b['action']==root['chosen_action'])
    policy=[{'first_report':e['report'],
             'next_action':cert['nodes'][e['child']]['chosen_action'],
             'remaining_risk':cert['nodes'][e['child']]['value']}
            for e in chosen['children']]
    report={'status':'PASS','python_version':platform.python_version(),
            'checks':checked,'machine_common_report_checks':machines['common_report_checks'],
            'elapsed_seconds':time.monotonic()-start,
            'general_CAD_executed':False,
            'independent_or_formal_verification':False}
    if not args.check_only:
        dump('VERIFICATION.json',report)
        dump('PROGRAMME_MODEL_CHECKS.json',machines)
        dump('OPTIMAL_POLICY.json',{
            'first_query':spec['experiments'][root['chosen_action']],
            'conditional_second_query':policy,
            'estimator':'At a stopping leaf, return the midpoint of its exact root_interval.',
            'action_index':spec['experiments']})
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
