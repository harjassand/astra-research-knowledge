"""Produce and read a finite calibrated record for the degree-four benchmark.

The unknown-model reconstruction reads RECORDS.json. AUDIT_TRUTH.json is
separate and is used only after reconstruction to audit the digital source.
"""
import json,time
from pathlib import Path
from fractions import Fraction as Q
from polynomial_tools import ProbeInverse,encode_polynomial,decode_polynomial
from probe_schedule import schedule
from calibrated_source import make_records,recover
from entropy_bounds import log_interval

ROOT=Path(__file__).resolve().parent


def ceilq(x): return -((-x.numerator)//x.denominator)


def acquire():
    start=time.perf_counter()
    K=4; C=Q(5,4); budget=Q(1,500); N=6
    inverse=ProbeInverse(K)
    sched=schedule(K,C,budget/inverse.condition)
    truth={(0,0,4):Q(-1),(1,0,0):Q(-1,4)}
    raw,source_cost=make_records(N,truth,inverse,sched)
    record={'contract':{'degree':K,'source_size':N,'coefficient_l1_bound':str(C),
                        'family':'distinct-site permutation-invariant Pauli polynomials'},
            'bath_nodes':[str(x) for x in inverse.nodes],
            'times':[str(x) for x in sched['nodes']],
            'record_radius':str(sched['record_radius']),
            'records':[[str(v) for v in row] for row in raw],
            'source_cost':source_cost}
    (ROOT/'RECORDS.json').write_text(json.dumps(record,indent=2)+'\n')
    (ROOT/'AUDIT_TRUTH.json').write_text(json.dumps({'polynomial':encode_polynomial(truth)},indent=2)+'\n')
    # Reconstruction is deliberately performed from the serialized record.
    read=json.loads((ROOT/'RECORDS.json').read_text())
    assert read['times']==[str(x) for x in sched['nodes']]
    recovered,nu=recover(inverse,sched,[[Q(x) for x in row] for row in read['records']])
    # A paid coefficient rounding reduces irrelevant exact-arithmetic costs.
    denominator=10**6
    rounded={a:Q((2*c.numerator*denominator+c.denominator)//(2*c.denominator),denominator)
             for a,c in recovered.items()}
    rounding=sum(abs(rounded[a]-recovered[a]) for a in recovered)
    rounded={a:c for a,c in rounded.items() if c}
    certified_error=nu+rounding
    audit=json.loads((ROOT/'AUDIT_TRUTH.json').read_text())
    truth_read=decode_polynomial(audit['polynomial'])
    actual=sum(abs(rounded.get(a,Q(0))-truth_read.get(a,Q(0))) for a in inverse.alphas)
    assert actual<=certified_error
    M=len(raw)*len(sched['nodes']); alpha=Q(1,20); gamma=sched['record_radius']
    # Each measured mean has statistical radius gamma/2 and allowed systematic
    # radius gamma/2. Hoeffding + union bound, with an outward log bound.
    logupper=log_interval(2*M/alpha)[1]
    shots=ceilq(8*logupper/gamma**2)
    evolution_time=shots*len(raw)*sum(sched['nodes'])
    result={'degree':K,'unknown_coefficients':len(inverse.alphas),'source_size':N,
            'learned_polynomial':encode_polynomial(rounded),'coefficient_l1_error':str(certified_error),
            'coefficient_l1_error_float':float(certified_error),'audit_actual_error':str(actual),
            'coefficient_rounding_error':str(rounding),'inverse_l1_condition':str(inverse.condition),
            'gradient_error':str(sched['gradient_error']),
            'interpolation_degree':sched['R'],'T':str(sched['T']),
            'derivative_weight_l1_float':float(sched['W']),
            'derivative_bias_bound_float':float(sched['bias']),
            'record_count':M,'record_radius':str(gamma),'record_radius_float':float(gamma),
            'hypothetical_physical_acquisition':{
                'failure_probability':str(alpha),'shots_per_record':str(shots),
                'fresh_N_spin_preparations':str(M*shots),'individual_spin_preparations':str(N*M*shots),
                'total_scheduled_free_evolution_time_energy_units':str(evolution_time),
                'total_free_evolution_time_float':float(evolution_time),
                'systematic_radius_per_record_at_most':str(gamma/2),
                'comment':'No physical shots were taken. Preparation, reset, timing and SPAM certification must additionally be supplied and priced.'},
            'digital_source':source_cost,'wall_seconds':time.perf_counter()-start}
    (ROOT/'ACQUISITION_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['unknown_coefficients','source_size','coefficient_l1_error_float',
                                         'audit_actual_error','record_count','record_radius_float','wall_seconds']},indent=2),flush=True)
    print('Total hypothetical physical preparations:',M*shots,flush=True)
    return result


if __name__=='__main__': acquire()
