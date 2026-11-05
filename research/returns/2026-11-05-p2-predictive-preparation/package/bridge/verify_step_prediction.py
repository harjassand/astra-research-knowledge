"""Independent exact verification by degree-five Boole quadrature.

The verifier reloads emitted rational polynomials. Seven interior rational
points determine each degree-six polynomial; breakpoints are checked against
the full table/ramp partition. The target is evaluated by exact Newton-Cotes
quadrature, not the compiler's polynomial antiderivative implementation.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import time

HERE=Path(__file__).resolve().parent


def pval(cs,t):
    value=F(0)
    for c in cs[::-1]:
        value=value*t+c
    return value


def boole_response(times,values,t,start,h):
    tau=t-start
    if tau<=0:
        return F(0),0
    total=F(0)
    boxes=0
    for i in range(len(times)-1):
        left=max(F(0),tau-times[i+1])
        right=min(h,tau-times[i])
        if right<=left:
            continue
        boxes+=1
        weighted=F(0)
        for j,w in enumerate((7,32,12,32,7)):
            s=left+(right-left)*F(j,4)
            lag=tau-s
            interp=(values[i]*(times[i+1]-lag)+values[i+1]*(lag-times[i]))/(times[i+1]-times[i])
            u=s/h
            density=30*u*u*(1-u)*(1-u)/h
            weighted+=w*interp*density
        total+=(right-left)*weighted/90
    return total,boxes


def main():
    begin=time.perf_counter()
    tp=HERE/"acquired_step_response.json"
    pp=HERE/"exact_prediction_path.json"
    table=json.loads(tp.read_text())
    path=json.loads(pp.read_text())
    assert hashlib.sha256(tp.read_bytes()).hexdigest()==path["acquired_table_sha256"]
    times=[F(t) for t in table["times_exact"]]
    values=[F(x) for x in table["values_exact"]]
    baseline=F(table["deployment_baseline_exact"])
    T=F(table["horizon_exact"])
    assert len(times)==len(values) and times[0]==0 and times[-1]==T
    assert all(b>a for a,b in zip(times,times[1:]))
    assert values[0]==0
    ramps=[(F(r["start_exact"]),F(r["ramp_exact"]),F(r["increment_exact"])) for r in path["force_program"]]
    expected={F(0),T}
    for start,h,c in ramps:
        assert start>=0 and h>0
        for t in times:
            for b in (start+t,start+h+t):
                if 0<b<T: expected.add(b)
    expected=sorted(expected)
    segs=path["segments"]
    assert len(segs)==len(expected)-1
    samples=boxes=0
    last_end=None
    for i,seg in enumerate(segs):
        left,right=F(seg["left_exact"]),F(seg["right_exact"])
        assert (left,right)==(expected[i],expected[i+1])
        coeff=[F(c) for c in seg["coefficients_exact"]]
        assert 1<=len(coeff)<=7
        if last_end is not None: assert pval(coeff,left)==last_end
        for j in range(1,8):
            t=left+(right-left)*F(j,8)
            target=baseline
            for start,h,c in ramps:
                value,n=boole_response(times,values,t,start,h)
                target+=c*value
                boxes+=n
            assert pval(coeff,t)==target
            samples+=1
        last_end=pval(coeff,right)
    assert pval([F(c) for c in segs[0]["coefficients_exact"]],F(0))==baseline
    variation=sum(abs(c) for start,h,c in ramps)
    bound=(F(table["readiness_error_exact"])+variation*F(table["response_error_exact"])
           +F(table.get("delivery_error_exact","0")))
    assert bound==F(path["uniform_physical_error_bound_exact"])
    out={"verified":True,"method":"Exact Boole quadrature at seven points on each complete degree-six partition cell, exact continuity, exact error composition.",
         "path_sha256":hashlib.sha256(pp.read_bytes()).hexdigest(),
         "table_sha256":hashlib.sha256(tp.read_bytes()).hexdigest(),
         "segments":len(segs),"identity_points":samples,"degree_five_quadrature_boxes":boxes,
         "uniform_physical_error_bound_exact":str(bound),"uniform_physical_error_bound":float(bound),
         "elapsed_seconds":time.perf_counter()-begin,
         "scope":"The path implements the acquired-table predictor exactly; physical confidence remains conditional on the acquisition and initialization contracts."}
    (HERE/"exact_prediction_verifier_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
