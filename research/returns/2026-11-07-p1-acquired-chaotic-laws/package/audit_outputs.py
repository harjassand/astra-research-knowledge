"""Independent output checks: direct cyclic defects and count recurrence.

Does not run or import the source generator or the address contraction loop.
Uses the delivered surrogate representation and claimed point coordinates.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from exact_core import GridResidual, matvec

ROOT=Path(__file__).resolve().parent


def main():
    cert=json.loads((ROOT/"EXECUTED_CERTIFICATE.json").read_text())
    s=np.load(ROOT/"surrogate.npz")
    a=s["A"].tolist()
    Q=int(s["Q"])
    b=[F(int(z),Q) for z in s["b"]]
    residual=GridResidual(s["residual"],Q)
    c=F(cert["constants"]["C"]["rational"])
    lhat=F(cert["constants"]["ell_hat"]["rational"])
    D=F(cert["constants"]["orbit_correspondence_D"]["rational"])
    # The independently derived trace recurrence t_m=3t_(m-1)-t_(m-2).
    traces=[2,3]
    for _ in range(2,101):
        traces.append(3*traces[-1]-traces[-2])
    for m,n in cert["fixed_point_counts"].items():
        assert n==(traces[int(m)]-2)**2
    orbits=json.loads((ROOT/"PERIODIC_ORBITS.json").read_text())
    checked=[]
    for entry in orbits:
        pts=[[F(z) for z in row] for row in entry["points"]]
        defect=F(0)
        for i,x in enumerate(pts):
            fx=[u+v+w for u,v,w in zip(matvec(a,x),b,residual(x))]
            nxt=pts[(i+1)%len(pts)]
            for expected,actual in zip(fx,nxt):
                diff=actual-expected
                nearest=(diff+F(1,2)).numerator//(diff+F(1,2)).denominator
                defect=max(defect,abs(diff-nearest))
        # sqrt(d)=2. This certificate comes directly from the cyclic equations.
        bound=2*c*defect/(1-c*lhat)
        assert bound<F(1,10**11)
        checked.append({"period":len(pts),"max_coordinate_dynamical_defect":str(defect),
                        "independent_surrogate_orbit_error_bound":str(bound),
                        "independent_surrogate_orbit_error_decimal":float(bound),
                        "independent_source_orbit_error_bound":str(D+bound)})
    ent=cert["entropy"]
    assert F(ent["rational_upper"])-F(ent["rational_lower"])<F(1,10**34)
    output={"count_recurrence_matches_all_reported_counts":True,
            "entropy_interval_width_below_1e_minus_34":True,
            "direct_cyclic_defect_certificates":checked,
            "meaning":"Finite execution checks only; all-period correctness follows from the report's theorem."}
    (ROOT/"INDEPENDENT_AUDIT.json").write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({"count_recurrence":"passed","orbit_defects":"passed",
                      "max_independent_surrogate_error":max(x["independent_surrogate_orbit_error_decimal"] for x in checked)}))


if __name__=="__main__":
    main()
