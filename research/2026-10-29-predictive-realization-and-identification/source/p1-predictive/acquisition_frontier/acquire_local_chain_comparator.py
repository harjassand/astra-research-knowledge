#!/usr/bin/env python3
"""Actual streamed local coins; conventional positive birth-death mean consumer.

No physical process was operated. A marked unit-attempt clock and exact state
reset access are supplied. Integer thresholds implement dyadic source coins.
"""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter
import hashlib,json,math
import numpy as np

HERE=Path(__file__).resolve().parent

def ratio(x):return {'numerator':str(x.numerator),'denominator':str(x.denominator),'display':float(x)}
def mean_to_right(p):
    """Positive O(N) conventional recurrence, avoids a nearly singular solve."""
    previous=F(0); total=F(0)
    for i,pi in enumerate(p[:-1]):
        previous=(1+(1-pi)*previous)/pi if i else 1/pi
        total+=previous
    return total

def acquire():
    nstates=33; n=2**22; chunk=2**18
    private_nums=[64+((7*i+3)%8) for i in range(nstates)]
    rng=np.random.default_rng(202610290314)
    counts=[]; hashes=[]; start=perf_counter()
    for threshold in private_nums:
        count=0; digest=hashlib.sha256()
        for _ in range(n//chunk):
            outcomes=rng.integers(0,256,size=chunk,dtype=np.uint8)<threshold
            count+=int(outcomes.sum())
            digest.update(np.packbits(outcomes,bitorder='little').tobytes())
        counts.append(count); hashes.append(digest.hexdigest())
    elapsed=perf_counter()-start
    record={'known_states':nstates,'known_graph':'nearest-neighbour path 0..32; reflected attempts at endpoints','known_clock':'unit-rate marked attempt clock','supplied_parameter_range':["1/4","3/4"],'outcomes_per_state':n,'right_counts':counts,'packed_outcome_sha256':hashes,'statistical_radius':"1/800",'confidence_failure_bound':"1/4096",'charged_scalar_outcomes':nstates*n,'charged_fresh_state_preparations':nstates*n,'charged_expected_native_attempt_waiting':nstates*n,'instrument_error':'zero in exact integer-threshold software source; not a physical calibration claim','acquisition_wall_seconds':elapsed,'sample_semantics':'actually generated streamed elementary binary outcomes, not aggregate Binomial draws; raw stream hashes and sufficient counts retained'}
    payload=json.dumps(record,indent=2)+'\n'
    (HERE/'LOCAL_CHAIN_ACQUIRED_RECORD.json').write_text(payload)
    frozen_hash=hashlib.sha256(payload.encode()).hexdigest()
    return record,private_nums,frozen_hash

def consume(record):
    """No private source parameters or normalizer arguments accepted."""
    n=record['outcomes_per_state']; radius=F(record['statistical_radius'])
    p=[max(F(1,4),min(F(3,4),F(c,n))) for c in record['right_counts']]
    lows=[max(F(1,4),F(c,n)-radius) for c in record['right_counts']]
    ups=[min(F(3,4),F(c,n)+radius) for c in record['right_counts']]
    k=max(max(u/pp,pp/l,(1-l)/(1-pp),(1-pp)/(1-u)) for pp,l,u in zip(p,lows,ups))
    exponent=2*(record['known_states']-1)-1
    estimate=mean_to_right(p)
    factor=k**exponent
    # Stronger equally-informed path monotonicity: T decreases in every p_i.
    strong_lower=mean_to_right(ups); strong_upper=mean_to_right(lows)
    # Exact elementary exponential bound for 2*M*exp(-2*n*r^2)<1/4096.
    assert 2*n*radius**2>=13
    exp13_lower=sum((F(13**j,math.factorial(j)) for j in range(48)),F(0))
    assert exp13_lower>2*record['known_states']*4096
    return {'proposal_mean':ratio(estimate),'uniform_local_rate_factor':ratio(k),'all_target_forest_point_factor':ratio(factor),'all_target_forest_interval_factor':ratio(factor**2),'selected_target_general_interval':[ratio(estimate/factor),ratio(estimate*factor)],'strong_conventional_positive_recurrence_interval':[ratio(strong_lower),ratio(strong_upper)],'strong_conventional_interval_factor':ratio(strong_upper/strong_lower),'confidence_inequality_proved_exactly':True,'all_target_statement':'for every nonempty target subset, every initial state outside it, and fixed nonnegative occupation reward; compute each query with its killed inverse and the uniform factor','selected_target':32,'initial_state':0,'consumer_private_parameters_read':False,'new_observations_after_freeze':0},(lows,ups)

def main():
    # Preserve an already acquired record: a consumer repair must not redraw data.
    record_path=HERE/'LOCAL_CHAIN_ACQUIRED_RECORD.json'
    if record_path.exists():
        payload=record_path.read_text()
        record=json.loads(payload)
        private=[64+((7*i+3)%8) for i in range(record['known_states'])]
        frozen_hash=hashlib.sha256(payload.encode()).hexdigest()
    else:
        record,private,frozen_hash=acquire()
    start=perf_counter(); result,intervals=consume(record)
    result['consumer_wall_seconds']=perf_counter()-start
    # Private truth checks are performed only after counts and consumer freeze.
    truth=[F(x,256) for x in private]
    true_mean=mean_to_right(truth)
    assert all(lo<=p<=hi for lo,p,hi in zip(intervals[0],truth,intervals[1]))
    lo=F(int(result['strong_conventional_positive_recurrence_interval'][0]['numerator']),int(result['strong_conventional_positive_recurrence_interval'][0]['denominator']))
    hi=F(int(result['strong_conventional_positive_recurrence_interval'][1]['numerator']),int(result['strong_conventional_positive_recurrence_interval'][1]['denominator']))
    assert lo<=true_mean<=hi
    result.update({'acquired_record_sha256':frozen_hash,'private_truth_interval_check':True,'source_hardware_operation':False,'interpretation':'large rare mean is not an information-time lower bound under supplied complete-state local reset access; conventional positive recurrence is strongest tested consumer','acquisition_cost_not_just_record_size':record['charged_scalar_outcomes']})
    (HERE/'LOCAL_CHAIN_PRIVATE_SOURCE.json').write_text(json.dumps({'right_probability_numerators':private,'denominator':256,'true_selected_mean':ratio(true_mean),'mean_to_paid_outcome_ratio_display':float(true_mean/record['charged_scalar_outcomes']),'role':'producer and post-freeze diagnostic only'},indent=2)+'\n')
    (HERE/'LOCAL_CHAIN_ACQUISITION_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','actual_streamed_outcomes':record['charged_scalar_outcomes'],'source_states':record['known_states'],'acquisition_wall_seconds':record['acquisition_wall_seconds'],'true_mean_display':float(true_mean),'forest_interval_factor_display':result['all_target_forest_interval_factor']['display'],'stronger_same_data_interval_factor_display':result['strong_conventional_interval_factor']['display'],'confidence_failure_bound':'1/4096'}))

if __name__=='__main__':main()
