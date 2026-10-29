"""Exact final comparison; no Hamiltonian/trajectory/source rerun."""
import hashlib
import json
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent


def outward(x,upper=False):
    with localcontext() as c:
        c.prec=25;c.rounding=ROUND_CEILING if upper else ROUND_FLOOR
        return str(Decimal(x.numerator)/Decimal(x.denominator))


def main():
    p=json.loads((HERE/'PREDICTION.json').read_text())
    l=json.loads((HERE/'LINEAR_COMPARISON.json').read_text())
    v=F.from_float(p['observables']['density_excess_at_source'])
    e=F(p['qualification']['density_total_error_upper']['upper_fraction'])
    w=F.from_float(l['linear_density_excess'])
    assert l['linear_numerical_error_upper']<1e-9
    f=F(1,10**9)
    separation=(v-e)-(w+f)
    assert separation>F(84303,10**7)
    assert e<F(453,10**6)
    assert v-e>F(-287100,10**6) and v+e<F(-286193,10**6)
    result=dict(status='PASS final rational interval composition, no new source run',
          physical_density_excess_interval=[outward(v-e),outward(v+e,True)],
          exact_error_upper=str(e),
          linear_response_interval=[outward(w-f),outward(w+f,True)],
          signed_nonlinear_minus_linear_interval=[outward((v-e)-(w+f)),outward((v+e)-(w-f),True)],
          rigorous_rounded_separation_lower='0.0084303',
          scope='ideal eta-coherent or phase-averaged eta-ensemble Hubbard input; binary64 arithmetic contract; no generic state/physical acquisition/ordinary-method advantage',
          input_sha256={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest()
                        for n in ['PREDICTION.json','LINEAR_COMPARISON.json','native.py','compare_linear.py']})
    (HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
