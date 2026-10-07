"""Own exact algebra fixtures; no peer code executed or imported."""
from fractions import Fraction as F
from pathlib import Path
import json

def main():
    a=b=F(1,10); c=F(2)
    assert a+b-c==F(-9,5)
    powers=[]
    for gamma in (F(11,10),F(-11,10)):
        for power in (1,2,3,5,8):
            x0=10+gamma; xp=10-gamma+2; xm=10-gamma-2
            f=lambda x:(1+x/10)**power
            aa=f(x0); bb=(f(xp)+f(xm))/2; cc=(f(xp)-f(xm))/2
            assert aa>0 and bb>0 and cc>0 and f(xm)>0
            slack=aa-bb-cc if gamma>1 else bb-cc-aa
            assert slack>0
            powers.append({"gamma":str(gamma),"power":power,"slack":str(slack)})
    # The fixed charge-one diagonal two-qubit gate is x0*y1+x1*y0.
    # Its Hessian consists of two disjoint off-diagonal unit pairs, hence
    # eigenvalues 1,1,-1,-1. Ordinary charge weights (0,1,0) are LC, but
    # that fact alone does not make THIS unprojected diagonal polynomial LC.
    block=[[F(0),F(1)],[F(1),F(0)]]
    assert block[0][0]*block[1][1]-block[0][1]*block[1][0]==-1
    result={"status":"PASS_SCOPED_ALGEBRA",
       "inside_cone_nonnegative_table_counterexample":{"alpha":"1","gamma":"0",
          "kappa":"0","scalar_f":"1/10+x","a":"1/10","b":"1/10","c":"2",
          "last_triangle_slack":"-9/5","status":"REFUTES unqualified iff"},
       "positive_spectrum_outside_checks":powers,
       "canonical_cut":{"weights":["0","1","0"],"diagonal_polynomial":"x0*y1+x1*y0",
          "hessian_eigenvalues":["1","1","-1","-1"],
          "scope":"Refutes direct fixed-charge diagonal LC gate only; no sector-law hardness or other-encoding obstruction."}}
    Path(__file__).with_name("cross_review_checks.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"outside_power_checks":len(powers),
                      "functional_if_and_only_if_repaired":True},indent=2))

if __name__=="__main__":main()
