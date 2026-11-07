"""Exact Fraction checks for the X-noise, biased-qubit and native-menu cases.

These are exact arithmetic witnesses, distinct from the binary64 emitter.
All times/rates are dimensionless declared model units; no calibration run.
"""
from fractions import Fraction as F
import json
from pathlib import Path


def certificates():
    p=F(1,5);lam=F(1)
    k=lam/(p*(1-p))
    # Weighted rank-one Choi condition: k^2 p(1-p)-k lambda >= 0.
    determinant=k*k*p*(1-p)-k*lam
    diag0=k*(1-p)-lam;diag1=k*p-lam
    assert determinant==0 and diag0>0 and diag1>0
    # Exact LDL for CP-part subtraction, basis 00,01,10,11.
    # M=diag(k(1-p), k(1-p)-lam, kp-lam, kp), M[01,10]=-lam.
    d0=k*(1-p);d1=diag0;d2=diag1-lam*lam/diag0;d3=k*p
    assert (d0,d1,d2,d3)==(F(5),F(4),F(0),F(5,4))
    # A negative determinant at any 0<k'<k gives the exact lower witness.
    below=k-F(1,100)
    negative_det=below*below*p*(1-p)-below*lam
    assert negative_det<0
    # Native menu: D[Y], D[Z], D[|0><1|], D[|1><0|].
    kn=F(10); y=lam; z=kn/4; down=(1-p)*kn-2*lam; up=p*kn-2*lam
    assert y==1 and z==F(5,2) and down==6 and up==0
    assert 2*lam+2*y+down+up==kn
    assert 2*y+(down+up)/2+2*z==kn
    assert 2*lam+(down+up)/2+2*z==kn
    assert down-up==kn*(1-2*p)
    # Stationarity alone: downward=3, no other added jumps.
    ds=lam*(1-2*p)/p
    assert ds==3 and (lam+ds)*p==lam*(1-p)
    # With downward cap 2, all nonnegative y/up violate stationarity:
    # down = 3 + 3*y + 4*up >= 3 > 2.
    return {
        "arithmetic":"fractions.Fraction; all assertions exact",
        "p":str(p),"noise_lambda":str(lam),"reset_embedding_optimum":str(k),
        "choi_block_diagonal":[str(diag0),str(diag1)],
        "choi_block_offdiagonal":str(-lam),"determinant_at_optimum":str(determinant),
        "exact_ldl_diagonal":[str(d0),str(d1),str(d2),str(d3)],
        "ldl_nontrivial_lower_entry":str(-lam/diag0),
        "rate_below_optimum":str(below),"negative_determinant":str(negative_det),
        "native_reset_optimum":str(kn),
        "native_control_rates":{"Y":str(y),"Z":str(z),"down":str(down),"up":str(up)},
        "native_reset_infeasibility_cap5":"Reset identities force y=1, up=kappa/5-2>=0, kappa>=10, down=4*kappa/5-2>=6>5.",
        "stationarity_with_cap5":{"down":str(ds),"others":"0"},
        "stationarity_infeasibility_cap2":"Stationarity forces down=3+3*y+4*up>=3>2.",
        "scope":"Exact declared qubit model and finite native menu; no physical device or process tomography performed."
    }


if __name__=="__main__":
    out=certificates()
    Path(__file__).with_name("EXACT_RATIONAL_CERTIFICATES.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
