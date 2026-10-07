"""Exact arithmetic supporting the fresh C07_S02 half-floor audit."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib,json

checks={}
def test(name,val):
    assert val,name
    checks[name]=True
test("tangent_endpoint",F(606,389)<F(8,5))
test("logcos_endpoint",F(389,720)*(1+F(2,3)+F(2,9)+F(4,81))>1)
test("phase_cubic",F(2,5)*F(8,5)**2/24==F(16,375))
test("phase_gaussian_coefficient",F(15,32)*F(16,375)**2==F(8,9375))
test("phase_loss_endpoint",F(2187,9375)*F(25,27)==F(27,125))
test("exp6_partial_lower",sum(F(6**j,factorial(j)) for j in range(8))>250)
test("sqrt18_ge4",18>=4**2)
test("vertical_exponent",-2+F(25,72)+F(10,9)==-F(13,24))
test("sqrt2_ge7_over5",F(7,5)**2<2)
test("vertical_exp_lower",sum(F(13,8)**j/factorial(j) for j in range(5))>F(100,21))
test("density_floor",1-F(27,125)-F(1,1000)-F(1,4)==F(533,1000)>F(1,2))
test("exp4_partial_lower",sum(F(4**j,factorial(j)) for j in range(7))>48)
test("correction_exp_lower",1+F(23,24)+F(23,24)**2/2==F(2785,1152))
test("correction_bound",F(1344,2785)<F(1,2))
test("real_N_derivative_upper",F(1,6)+1-F(15,8)<0)
source=Path('work/cycle6/c07_s02/phase2/AXIAL_HALF_EXTENSION.txt')
out={'status':'EXACT_CONSTANT_CHECKS_PASS','source_path':str(source),
     'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
     'checks':checks,'scope':'Supporting arithmetic; the saved audit supplies the all-N analytic reconstruction.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
