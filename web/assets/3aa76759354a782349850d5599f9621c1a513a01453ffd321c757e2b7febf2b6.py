"""Independently verify ONLY completed N170 from a retained INCOMPLETE source.

The original requested range/status/failure are retained. This wrapper does not
promote the failed N171..199 run to PASS and never admits its missing cases.
The frozen owned integer checker acquires its own positive-Taylor exp inputs.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,time
from optimal_prefix_independent_integer_verifier import Checker,DN,DD

OWN=Path(__file__).parent
FROZEN_CHECKER_SHA256='19b91b7cc16fb349ba0306a57b9d803e575f797b32b0479513171a873262c502'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True)
    ap.add_argument('--wall-limit',type=float,required=True)
    ap.add_argument('--guard',type=int,default=64)
    args=ap.parse_args()
    assert 0<args.wall_limit<=60 and args.guard>=32
    source=Path(args.source)
    outpath=OWN/(source.stem+f'_completed_N170_independent_integer_G{args.guard}.json')
    if outpath.exists():raise SystemExit('Preserving the earlier partial-source verification receipt.')
    started=time.perf_counter();deadline=started+args.wall_limit
    receipt={'status':'RUNNING','source':str(source),
             'declared_total_wall_cap_seconds':args.wall_limit,'guard_bits':args.guard,
             'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'accepted_source_cases':[170],'completed_cases':[],
             'input_algorithm':'positive directed Taylor exp(+y), y<=1/16, geometric tail, reciprocal, guarded squaring',
             'operation_algorithm':'independent outward INTEGER recurrence and exact cross-multiplication LDL division checks',
             'disposition':'N170 alone from retained INCOMPLETE N170..199 source; N171..199 not admitted here'}
    checker=None
    try:
        frozen=OWN/'optimal_prefix_independent_integer_verifier.py'
        assert hashlib.sha256(frozen.read_bytes()).hexdigest()==FROZEN_CHECKER_SHA256
        data=json.loads(source.read_text())
        assert data['status']=='INCOMPLETE'
        assert data['requested_N_range']==[170,199]
        assert [c['N'] for c in data['cases']]==[170]
        assert data['delta']==f'{DN}/{DD}'
        assert data['precision_bits']==1024
        assert int(data['denominator'])==1<<1024
        assert 'uncertified pivot N=171' in data['failure']
        receipt['source_file_status']=data['status']
        receipt['source_requested_N_range']=data['requested_N_range']
        receipt['source_failure_preserved']=data['failure']
        checker=Checker(1024,args.guard,deadline)
        checker.case(data['cases'][0]);receipt['completed_cases'].append(170)
        receipt['status']='PASS independent exact inputs/congruences/LDL for completed N170 only'
        receipt['requested_N_range']=[170,170];receipt['precision_bits']=1024
    except Exception as e:
        receipt['status']='INCOMPLETE';receipt['failure']=repr(e)
        receipt['failure_stage']=checker.stage if checker else 'load/admission'
    receipt['wall_seconds']=time.perf_counter()-started
    receipt['verified_counts']=checker.counts if checker else None
    receipt['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    receipt['checker_sha256']=FROZEN_CHECKER_SHA256
    receipt['partial_wrapper_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    outpath.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('completed_cases','source_failure_preserved')},indent=2))
    if receipt['status']=='INCOMPLETE':raise SystemExit(1)

if __name__=='__main__':main()
