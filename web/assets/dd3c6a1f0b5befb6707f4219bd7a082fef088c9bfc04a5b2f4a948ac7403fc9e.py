"""Replay immutable six physical controls without regenerating any output."""
from pathlib import Path
import hashlib
import json
import math

here=Path(__file__).resolve().parent
writer=here/"CHECK_PHYSICAL_CONTROLS.py"
data=writer.read_bytes()
assert hashlib.sha256(data).hexdigest()=="803a56bdb5fe9bd663c203e7fd8d312499f361398f32f595aec5505448cdd073"
delimiter='\nwith (HERE/"PHYSICAL_CONTROLS.json").open("x") as f:'
source=data.decode()
assert source.count(delimiter)==1
environment={"__file__":str(writer),"__name__":"__read_only_replay__"}
exec(compile(source.split(delimiter)[0],str(writer),"exec"),environment)
actual=environment["out"]
expected=json.loads((here/"PHYSICAL_CONTROLS.json").read_text())

def compare(a,b):
    if isinstance(a,dict):
        assert set(a)==set(b)
        for key in a:
            compare(a[key],b[key])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b):
            compare(x,y)
    elif isinstance(a,float):
        assert math.isclose(a,b,abs_tol=3e-10,rel_tol=3e-10),(a,b)
    else:
        assert a==b,(a,b)

compare(actual,expected)
print(json.dumps({"status":"PASS_READ_ONLY_PHYSICAL_REPLAY","case_count":actual["case_count"],"endpoint_checks":12,"writes":0}))
