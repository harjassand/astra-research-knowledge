"""Bounded full test grid; independent decimal population reconstruction."""
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import platform
import random
import resource
import time

import mpmath as mp
from dicke_compiler import (compile_state, from_record, recovered_populations,
                            sample_product, verify_model, target_intervals,
                            finite_local_density)

HERE = Path(__file__).resolve().parent


def independent_population_error(model):
    """Do not reuse acquired moments, eigenvalues, or certificate exp engine."""
    n,bits = model['n'],model['node_weight_bits']
    delta,h = from_record(model['delta']),from_record(model['h'])
    with mp.workdps(100):
        xs = [mp.mpf(int(x))/(1 << bits) for x in model['node_integers']]
        ws = [mp.mpf(int(w))/(1 << bits) for w in model['weight_integers']]
        md,mh = mp.mpf(delta.numerator)/delta.denominator,mp.mpf(h.numerator)/h.denominator
        target_logs = [-(md/n)*(mp.mpf(k)-mp.mpf(n)/2)**2+mh*(mp.mpf(k)-mp.mpf(n)/2)
                       if n else mp.mpf(0) for k in range(n+1)]
        peak = max(target_logs)
        target = [mp.exp(v-peak) for v in target_logs]
        Z = mp.fsum(target)
        target = [v/Z for v in target]
        q = [math.comb(n,k)*mp.fsum(w*x**k*(1-x)**(n-k) for x,w in zip(xs,ws))
             for k in range(n+1)]
        maxerr = max(abs(x-y) for x,y in zip(q,target))
        td = mp.fsum(abs(x-y) for x,y in zip(q,target))/2
        bound = from_record(model['certificate']['target_trace_distance_upper'])
        mpbound = mp.mpf(bound.numerator)/bound.denominator
        assert td <= mpbound+mp.mpf('1e-95')
        return {'max_population_error':mp.nstr(maxerr,14),
                'trace_distance':mp.nstr(td,14),
                'status':'INDEPENDENT_FLOATING_DIAGNOSTIC_ONLY; exact verifier also passed'}


def run():
    start = time.perf_counter()
    grid = [(n,d,h) for n in [2,3,8,15,16,31,32]
            for d in ['0','1/4','1/2'] for h in ['0','1/3','-2/5']]
    extra = [(0,'1/2','1/3'),(1,'1/2','1/3'),(64,'1/2','1/3'),
             (32,'1/2','60'),(31,'1/2','-60'),
             (64,'1/2','100000000000000000000'),
             (64,'1/2','-100000000000000000000')]
    models,records = [],[]
    rng = random.Random(20261008)
    for index,(n,d,h) in enumerate(grid+extra):
        model = compile_state(n,d,h,epsilon='1e-20')
        assert verify_model(model)
        diagnostic = independent_population_error(model)
        sample = sample_product(model,rng)
        density = sample['finite_product_local_density']
        diag = [from_record(x) for x in density['diagonal']]
        re,im = from_record(density['upper_right_real']),from_record(density['upper_right_imag'])
        assert sum(diag)==1 and min(diag)>=0 and re*re+im*im <= diag[0]*diag[1]
        assert sample['phase_index'] < n+1
        assert sample['random_bits_consumed'] == model['predetermined_random_bits_per_sample']
        record = {'n':n,'delta':d,'h':h,'certificate_verified':True,
                  'compile_seconds':model['compile_seconds'],
                  'node_count':len(model['node_integers']),
                  'phase_count':model['phase_modulus'],
                  'exact_recipe_component_count':model['component_count'],
                  'node_weight_bits':model['node_weight_bits'],
                  'density_bits':model['density_bits'],
                  'total_trace_distance_upper':model['total_output_trace_distance_upper'],
                  'numeric_population_diagnostic':diagnostic,
                  'density_PSD_exact':True,
                  'predetermined_random_bits_per_sample':model['predetermined_random_bits_per_sample'],
                  'attempt_count':len(model['acquisition_attempts']),
                  'certificate_kind':model['certificate']['kind']}
        models.append(model)
        records.append(record)
        if index%9 == 8 or index==len(grid+extra)-1:
            print(json.dumps({'completed':index+1,'total':len(grid+extra),
                              'last_n':n,'elapsed_seconds':time.perf_counter()-start}),flush=True)
    # Deterministic draw law and every phase of a representative measure.
    representative = next(m for m in models if m['n']==8 and from_record(m['delta'])==F(1,2)
                          and from_record(m['h'])==F(1,3))
    phase_density_checks = 0
    for node in representative['node_integers']:
        x = F(int(node),1 << representative['node_weight_bits'])
        for j in range(representative['phase_modulus']):
            finite_local_density(x,j,representative['phase_modulus'],representative['density_bits'])
            phase_density_checks += 1
    # Budget exhaustion returns failure, not unverified output.
    failure_preserved = False
    try:
        compile_state(8,'1/2','1/3',epsilon='1e-30',bits=2,density_bits=2,max_attempts=1)
    except ArithmeticError:
        failure_preserved = True
    assert failure_preserved
    output = {'models':models}
    text = json.dumps(output,indent=2)+'\n'
    (HERE/'certified_models.json').write_text(text)
    # A real sampler export with compact local density and exact phase label.
    sample_model = next(m for m in models if m['n']==32 and from_record(m['delta'])==F(1,2)
                       and from_record(m['h'])==F(1,3))
    sample_output = {'model':sample_model,'samples':[sample_product(sample_model,rng) for _ in range(4)]}
    sample_text = json.dumps(sample_output,indent=2)+'\n'
    (HERE/'sampler_examples.json').write_text(sample_text)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_bytes = rss if platform.system()=='Darwin' else rss*1024
    summary = {'status':'PASS','utc_note':'wall timestamps in implementation start/end metadata',
               'cases':len(records),'requested_grid_cases':len(grid),'extra_cases':len(extra),
               'records':records,'phase_density_checks':phase_density_checks,
               'insufficient_precision_failure_preserved':failure_preserved,
               'elapsed_seconds':time.perf_counter()-start,
               'process_peak_rss_bytes':peak_bytes,
               'rss_scope':'current Python process including interpreter/mpmath/test suite; OS peak RSS',
               'certified_models_output_bytes':len(text.encode()),
               'sampler_examples_output_bytes':len(sample_text.encode()),
               'BLAS_threads':1,'mpmath_version':mp.__version__,
               'python_version':platform.python_version(),
               'platform':platform.platform(),
               'no_physical_device_preparation_claim':True,
               'quantum_accuracy':'trace distance = half trace norm',
               'certification':'exact rational certificates, recomputed; floating acquisition and independent mp diagnostics separately labelled'}
    (HERE/'checks.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['status','cases','elapsed_seconds','process_peak_rss_bytes',
                                           'certified_models_output_bytes','sampler_examples_output_bytes']}),flush=True)


if __name__=='__main__':
    run()
