"""Verify and replay the frozen entropy/p scripts without their writers."""
from pathlib import Path
import hashlib
import json
import math

HERE=Path(__file__).resolve().parent
CASES=[("CHECK_FORWARD_ENTROPY_CONTROLS.py","FORWARD_ENTROPY_CONTROLS.json",
        "53129c08d408a834b04a50a5c2dc8d1035bb24d976ecffe0b774fd18fcbe83db",
        "80aceecef698010f8d8707e5bbcb79292642d2f440b5d4455c9b472fcb427d70"),
       ("CHECK_NONKMS_FINITE_P_CONTROLS.py","NONKMS_FINITE_P_CONTROLS.json",
        "548aac4924e95cfd405422f083781e6497808ee5dbebcdfc861b5403551f2902",
        "415813ff6a0f56f409871fa78900a1549cb7bd196f25a0f6fc61f7dce1d837d1")]


def cmp(a,b,path="root"):
    if isinstance(a,dict):
        assert isinstance(b,dict) and a.keys()==b.keys(),path
        for k in a:
            cmp(a[k],b[k],path+"."+str(k))
    elif isinstance(a,list):
        assert isinstance(b,list) and len(a)==len(b),path
        for i,(u,v) in enumerate(zip(a,b)):
            cmp(u,v,path+"["+str(i)+"]")
    elif isinstance(a,float):
        assert isinstance(b,(int,float)) and math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-11),(path,a,b)
    else:
        assert a==b,(path,a,b)


out=[]
for writer,stored,ws,js in CASES:
    code=(HERE/writer).read_bytes()
    data=(HERE/stored).read_bytes()
    assert hashlib.sha256(code).hexdigest()==ws,writer
    assert hashlib.sha256(data).hexdigest()==js,stored
    marker='\nwith (HERE/"'+stored+'").open("x") as f:\n'
    parts=code.decode().split(marker)
    assert len(parts)==2
    namespace={"__file__":str(HERE/writer),"__name__":"frozen_prefix_read_only_replay"}
    exec(compile(parts[0],str(HERE/writer),"exec"),namespace)
    cmp(namespace["out"],json.loads(data))
    assert (HERE/writer).read_bytes()==code and (HERE/stored).read_bytes()==data
    out.append({"writer":writer,"output":stored,"status":"MATCH_READ_ONLY"})
print(json.dumps({"status":"PASS_READ_ONLY_REPLAY","replays":out}))
