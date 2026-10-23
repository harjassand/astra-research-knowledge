"""Independent 16-mask check of the omitted pair-support premise.
No inherited representation import; exact raw prepend/pop device calls.
This finite counterexample is not an all-length proof.
"""
from itertools import product
from pathlib import Path
import json,time,resource

def history(word,bath,stays):
    out=list(word); stack=list(bath)
    for i,stay in enumerate(stays):
        if stay:
            continue
        if out[i]==0:
            assert stack, "The witness must not encounter the root."
            out[i]=stack.pop(0)
        else:
            stack.insert(0,out[i])
            out[i]=0
    return tuple(out),tuple(stack)

def main():
    start=time.perf_counter()
    x=(0,1,0,1); y=(1,0,1,0); bath=(1,2,1,1)
    entries=[]
    coefficient=0
    for stays_x in product((0,1),repeat=4):
        stays_y=tuple(1-s for s in stays_x)
        ox,bx=history(x,bath,stays_x)
        oy,by=history(y,bath,stays_y)
        if (ox,bx)!=(oy,by):
            continue
        sign=(-1)**sum(stays_x)
        delta=len(bx)-len(bath)
        coefficient+=sign*delta
        entries.append({"x_stay_mask":stays_x,"y_stay_mask":stays_y,
                        "output":ox,"bath":bx,"sign":sign,
                        "depth_increment":delta,"signed_increment":sign*delta})
    assert coefficient==1
    result={
        "input_x":x,"input_y":y,"initial_bath":bath,
        "matrix_element":"<x,bath|G(b)|y,bath> = b^2 (1-b)^2",
        "coefficient":coefficient,
        "matching_histories":entries,
        "matching_count":len(entries),
        "weighted_H_contraction_at_this_bath":"b^2 (1-b)^2 / 32 for K=|x><y|+|y><x|",
        "scope":"Exact finite omitted-pair-support counterexample; root not visited; no all-length extrapolation.",
        "runtime_seconds":time.perf_counter()-start,
        "peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()

