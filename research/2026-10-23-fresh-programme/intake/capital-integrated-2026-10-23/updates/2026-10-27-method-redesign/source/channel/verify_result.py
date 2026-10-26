#!/usr/local/bin/python3
"""Independent rational recheck: verify_result.py INPUT.json OUTPUT.json."""
from pathlib import Path
import sys,json,importlib.util,time,math
_START=time.perf_counter()
p=Path(__file__).resolve().parent/'selected'/'verify.py'
spec=importlib.util.spec_from_file_location('t31_selected_exact_verifier',p)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
inp=json.loads(Path(sys.argv[1]).read_text());out=json.loads(Path(sys.argv[2]).read_text())
if 'cases' in inp:
    assert len(inp['cases'])==len(out['results'])
    checks=[]
    for c,r in zip(inp['cases'],out['results']):
        assert c.get('id')==r.get('id')
        checks.append({'id':c.get('id'),**v.verify(c,r)})
else:checks=[{'id':inp.get('id'),**v.verify(inp,out)}]
def json_numbers(value):
    if isinstance(value,float) and not math.isfinite(value):return None
    if isinstance(value,dict):return {k:json_numbers(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [json_numbers(v) for v in value]
    return value
print(json.dumps(json_numbers({'checks':checks,'verification_process_seconds_including_imports':time.perf_counter()-_START}),indent=2,allow_nan=False))
