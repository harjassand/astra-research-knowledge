"""Independent exact physical one-magnon obstruction to the small collar."""
from pathlib import Path
from fractions import Fraction as Q
import json
import time
import math
import sympy as s

ROOT=Path(__file__).resolve().parent


def main():
    started=time.monotonic()
    t=s.symbols('t',positive=True)
    v=s.Matrix([[4,0,0,0],[0,2,2,0],[0,2,2,0],[0,0,0,4]])
    # Literal h01+h23 in the four-site physical one-magnon sector.
    w=s.Matrix([[6,2,0,0],[2,6,0,0],[0,0,6,2],[0,0,2,6]])
    p4=v/4;p0=s.eye(4)-p4
    assert p4*p4==p4 and p0*p4==s.zeros(4)
    c=p0+t**-2*p4;ci=p0+t**2*p4
    assert s.simplify(c*ci)==s.eye(4)
    e=(w-c*w*ci)/2
    herm=(e+e.T)/2
    assert s.simplify(herm[1,0]+(t*t+t**-2-2)/4)==0
    # A positive Taylor lower bound for sinh(3/2) uses exact rational terms.
    z=Q(3,2)
    lower=sum((z**k/math.factorial(k) for k in range(1,30,2)),Q(0))
    lower_n256=64*(lower/4-Q(3,8))
    assert lower_n256>Q(1006847,100000)
    result={'status':'INDEPENDENT_EXACT_ONE_MAGNON_SMALL_COLLAR_OBSTRUCTION_PASS',
            'Hermitian_residual_entry':'-(t²+t^(-2)-2)/4, t=exp(s)',
            'ring256_integrated_residual_lower_bound_exact':str(lower_n256),
            'ring256_integrated_residual_lower_bound_decimal':float(lower_n256),
            'ring512_integrated_residual_lower_bound_exact':str(2*lower_n256),
            'accepted_log_purity_residual_budget_upper':'1/10000000',
            'seconds':time.monotonic()-started,
            'scope':'Disjoint block4/collar1 amplitude cannot satisfy the all-Schatten residual certificate at beta3/4. Does not lower-bound its actual Gibbs purity error or rule out other amplitudes.'}
    (ROOT/'SMALL_COLLAR_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
