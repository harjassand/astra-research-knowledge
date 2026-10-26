#!/usr/local/bin/python3
"""T31 completion executable: evaluate.py INPUT.json OUTPUT.json.

Uses the selected denominator-only covariance construction. Original independent
worker sources and the lead Gram-SDP alternative remain preserved unchanged.
"""
import time
_START=time.perf_counter()
from pathlib import Path
import sys,json,importlib.util,math
_WORKER=Path(__file__).resolve().parent/'selected'
sys.path.insert(0,str(_WORKER))
_spec=importlib.util.spec_from_file_location('t31_selected_evaluator',_WORKER/'evaluator.py')
_primary=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_primary)
def json_numbers(value):
    if isinstance(value,float) and not math.isfinite(value):return None
    if isinstance(value,dict):return {k:json_numbers(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [json_numbers(v) for v in value]
    return value

def evaluate(case):
    # Exact rational endpoints and certificate fields are unchanged. Extremely
    # large finite coefficients can overflow optional binary64 diagnostics.
    return json_numbers(_primary.evaluate(case))

if __name__=='__main__':
    inp=json.loads(Path(sys.argv[1]).read_text())
    if 'cases' in inp:
        out={'results':[evaluate(c) for c in inp['cases']]}
    else:out=evaluate(inp)
    out['process_seconds_including_imports']=time.perf_counter()-_START
    out['construction']='T31 denominator-only covariance and exact rational SOS/vertex certificates'
    if len(sys.argv)>2:Path(sys.argv[2]).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    if 'results' in out:
        print(json.dumps({'results':[{k:r[k] for k in ['id','lower_float','upper_float','width']} for r in out['results']],
                          'process_seconds_including_imports':out['process_seconds_including_imports']},indent=2,allow_nan=False))
    else:print(json.dumps({k:out[k] for k in ['id','lower_float','upper_float','width','process_seconds_including_imports']},indent=2,allow_nan=False))
