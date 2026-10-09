"""Replay both frozen finite diagnostics without invoking their writers."""
from pathlib import Path
import hashlib
import json
import math

HERE=Path(__file__).resolve().parent
PAIRS=[
    ("CHECK_ALL_P_PHYSICAL_CONTROLS.py","ALL_P_PHYSICAL_CONTROLS.json",
     "fa46b05c354be1b46ac8c6a2a2f85347b0e4617decfcb5976c74a8cec11aa610",
     "a67058732c95dba43b1d5a904f4909126cbf106bbb16fc052eec9e756ef5f596"),
    ("CHECK_EXPOSED_SIGNED_POLAR.py","EXPOSED_SIGNED_POLAR_CONTROLS.json",
     "25d1ac623ed6469e4761df028f3cd1b215c4d232021aca311318afc1b2f60f57",
     "e4c5129821fb67ea735c793ae3d1c74bdace934d8f4e02805e6b85c63fde589a")]


def compare(a,b,path="root"):
    if isinstance(a,dict):
        assert isinstance(b,dict) and a.keys()==b.keys(),path
        for k in a:
            compare(a[k],b[k],path+"."+str(k))
    elif isinstance(a,list):
        assert isinstance(b,list) and len(a)==len(b),path
        for i,(u,v) in enumerate(zip(a,b)):
            compare(u,v,path+"["+str(i)+"]")
    elif isinstance(a,float):
        assert isinstance(b,(float,int)) and math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-11),(path,a,b)
    else:
        assert a==b,(path,a,b)


rows=[]
for writer,output,writer_sha,output_sha in PAIRS:
    source=(HERE/writer).read_bytes()
    stored=(HERE/output).read_bytes()
    assert hashlib.sha256(source).hexdigest()==writer_sha,writer
    assert hashlib.sha256(stored).hexdigest()==output_sha,output
    marker='\nwith (HERE/"'+output+'").open("x") as f:\n'
    chunks=source.decode().split(marker)
    assert len(chunks)==2,writer
    namespace={"__file__":str(HERE/writer),"__name__":"frozen_read_only_replay"}
    exec(compile(chunks[0],str(HERE/writer),"exec"),namespace)
    compare(namespace["out"],json.loads(stored))
    assert (HERE/writer).read_bytes()==source and (HERE/output).read_bytes()==stored
    rows.append({"writer":writer,"stored_output":output,"status":"MATCH_READ_ONLY"})
print(json.dumps({"status":"PASS_READ_ONLY_REPLAY","replays":rows}))
