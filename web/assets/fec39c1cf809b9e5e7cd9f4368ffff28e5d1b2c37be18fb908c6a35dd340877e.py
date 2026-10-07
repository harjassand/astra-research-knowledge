"""Verify reusable whole-Gibbs models after JSON roundtrip and count fair bits."""
from copy import deepcopy
import json
from pathlib import Path
import random
import resource
import platform
import time
from whole_gibbs_compiler import compile_whole_gibbs,verify_whole_model,sample_whole_gibbs

HERE=Path(__file__).resolve().parent


class CountedRandom(random.Random):
    def __init__(self,seed):
        super().__init__(seed)
        self.bits=0
    def getrandbits(self,k):
        self.bits+=k
        return super().getrandbits(k)


def run():
    start=time.perf_counter()
    records=[]
    examples=[]
    for N,alpha,epsilon in [(1,'0','1e-12'),(2,'1/2','1e-12'),(3,'3','1e-40')]:
        model=compile_whole_gibbs(N,alpha,'1','1/3',epsilon)
        restored=json.loads(json.dumps(model))
        assert verify_whole_model(restored)
        rng=CountedRandom(20261008)
        samples=[]
        for j in range(24):
            before=rng.bits
            sample=sample_whole_gibbs(restored,rng)
            assert rng.bits-before==model['predetermined_random_bits_per_sample']
            assert sample['random_bits_consumed']==model['predetermined_random_bits_per_sample']
            assert len(sample['local_density_matrices'])==N
            if j<2:
                samples.append(sample)
        records.append({'N':N,'alpha':alpha,'delta':'1','h':'1/3','epsilon':epsilon,
                        'compile_seconds':model['compile_seconds'],
                        'total_target_trace_distance_upper':model['total_target_trace_distance_upper'],
                        'json_roundtrip_certificate_verified':True,
                        'draws_checked':24,'predetermined_fair_bits_per_draw':model['predetermined_random_bits_per_sample']})
        examples.append({'model':model,'samples':samples})
    target=examples[-1]['model']
    corruptions=[]
    for label,mutate in [
        ('false_zero_matrix_error',lambda m:m['full_matrix_trace_distance_upper'].update(numerator='0')),
        ('branch_normalization_wrong',lambda m:m['branches'][0]['probability'].update(numerator='1',denominator='1')),
        ('subblock_parameter_wrong',lambda m:m['Dicke_models'][-1]['h'].update(numerator='0')),
    ]:
        bad=deepcopy(target)
        mutate(bad)
        try:
            verify_whole_model(bad)
        except (AssertionError,ValueError,ArithmeticError):
            corruptions.append({'name':label,'status':'REJECTED'})
        else:
            raise AssertionError('whole-model corruption accepted: '+label)
    result={'status':'PASS','models':3,'draws_checked':72,'records':records,
            'corruption_controls':corruptions,'examples':examples,
            'elapsed_seconds':time.perf_counter()-start,
            'process_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if platform.system()=='Darwin' else 1024),
            'scope':'Reusable bounded whole-Gibbs API; N<=3, scalar inputs known; exact posterior full-matrix certification'}
    text=json.dumps(result,indent=2)+'\n'
    (HERE/'whole_api_checks.json').write_text(text)
    print(json.dumps({'status':'PASS','models':3,'draws_checked':72,
                      'elapsed_seconds':result['elapsed_seconds'],'output_bytes':len(text.encode())}),flush=True)


if __name__=='__main__':
    run()
