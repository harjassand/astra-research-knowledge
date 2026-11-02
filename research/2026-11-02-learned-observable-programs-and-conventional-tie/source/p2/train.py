"""First stage: freeze records and acquired code; do not read heldout questions."""
import json,hashlib
from pathlib import Path
from source_device import BATHS,MeasuredDevice
from synthesize import compile_all
from execute import programs_growth,model_error_envelope

ROOT=Path(__file__).parent
if __name__=='__main__':
    device=MeasuredDevice(BATHS,seed=3457)
    records,programs=compile_all(device,exposure=2_000_000,desired_local_residual=.015)
    assert all(p['local_residual_bound']<=.015 for p in programs.values())
    result={'kind':'acquired-local-observable-programs-v1','source_interface':'eight pinned neighbourhood Poisson clock counts per mode',
      'assumptions':['local single-spin flip rates depend only on three spin sites',
       'stationary mode-local rate table is unchanged across lattice size and site',
       'individual site modes independently addressable, no cross-talk',
       'Poisson exposure counts conditionally unbiased with mean rate*exposure',
       'initial state independent product preparation with supplied marginals',
       'open-loop time/spatial mode schedules only'],
      'confidence_joint':'at least 1 - 32 exp(-22) (>0.99999999) for the sixteen Poisson rate tables',
      'acquisition_cost':{'physical_exposure_units':device.exposures,'scalar_calls':device.calls,
                           'reported_event_count':device.reported_events,'candidate_site_codes':4,
                           'source_model_bits':'two rate configurations, eight spin triples per mode'},
      'programs':programs,'growth':programs_growth(programs),
      'model_error_one_spin_T1.2':model_error_envelope(programs,1.2,1)}
    path=ROOT/'frozen_programs.json'
    path.write_text(json.dumps(result,indent=2,sort_keys=True))
    rp=ROOT/'frozen_measurements.json'
    rp.write_text(json.dumps({k:v.to_json() for k,v in records.items()},indent=2,sort_keys=True))
    blob=path.read_bytes()
    print('FROZEN',path,'sha256',hashlib.sha256(blob).hexdigest())
    for name,prog in programs.items():
        print(name,'language=',prog['encoding'],'rules=',[(v['offsets'],v['rate']) for v in prog['jumps']],
              'kill=',prog['kill'],'local residual=',prog['local_residual_bound'])
    print('cost=',result['acquisition_cost'])
