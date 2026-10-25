"""High precision arithmetic; the rows are not independent observations.

Original rows: Alpha Fig3 and measurement publications/CODATA2022.
Updated rows: arXiv2505.21476v3 Sec7 (reprocessed inputs, not new recoil data).
Pull means (candidate - row central value)/row quoted standard uncertainty.
No combined significance or probability-of-coincidence is computed.
"""
from decimal import Decimal as D, localcontext
import json


with localcontext() as ctx:
    ctx.prec = 75
    r = (D(79)+D(48)*D(2).sqrt()+D(42)*D(3).sqrt()+D(3)*D(6).sqrt())/D(31104)
    inverse = 1/r
    rows = [
        ("CODATA2022", "137.035999177", "0.000000021", "joint adjusted recommendation; uncertainty expansion applied"),
        ("electron_QED2023", "137.035999166", "0.000000015", "original printed theory-dependent inversion"),
        ("Rb_original2020", "137.035999206", "0.000000011", "original published recoil inference"),
        ("Cs_original2018", "137.035999046", "0.000000027", "original published recoil inference"),
        ("electron_QED2025", "137.035999163", "0.000000015", "updated theory-dependent inversion of same measured moment"),
        ("Rb_reprocessed2025", "137.0359992052", "0.0000000097", "reprocessed mass inputs; same recoil observation"),
        ("Cs_reprocessed2025", "137.035999045", "0.000000027", "reprocessed mass inputs; same recoil observation"),
    ]
    result = {"alpha_candidate":str(r),"inverse_candidate":str(inverse),"rows":[]}
    for name, value, uncertainty, scope in rows:
        result["rows"].append({"row":name,"inverse":value,"standard_uncertainty":uncertainty,
            "descriptive_pull":str((inverse-D(value))/D(uncertainty)),"scope":scope})
    assert abs(inverse-D("137.0359991895661550291837440208667995664")) < D("1e-36")
    result["boundary"]="No covariance matrix is estimated; no joint evidence multiplier, meta-analysis, p-value or coincidence probability is claimed."
    print(json.dumps(result, indent=2))
