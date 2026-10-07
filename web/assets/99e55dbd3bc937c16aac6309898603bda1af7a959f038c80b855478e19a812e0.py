"""Exact arithmetic supporting the delta<=5/4,N>=64 analytic tail."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json
checks={}
def test(name,v):
    assert v,name
    checks[name]=True
z=F(6,5)
Cupper=1-z**2/2+z**4/24;Clower=Cupper-z**6/720
test('correlated_lemma_condition',2*(1-Cupper**2)>F(165,128))
test('strip_logsec',Clower*sum(F(21,20)**j/factorial(j) for j in range(6))>1)
test('vertical_barrier',F(144,125)-F(33,32)*F(21,20)==F(1107,16000))
test('vertical_prefactor',F(5,12)<F(2,3)**2)
test('vertical_ratio',F(11,96)<F(1,8))
test('core_phase_cubic',F(2,5)*F(8,7)**2/24==F(16,735))
test('core_g_factor',1-5*F(33,32)/7==F(59,224))
test('core_sqrt_bound',F(51,100)**2<F(59,224))
phase=60*F(16,735)**2*F(125,64)*F(1089,65536)/(F(59,224)**3*F(51,100))
test('core_phase_bound',phase==F(2420000,24440101)<F(1,10))
test('exp2_gt7',sum(F(2**j,factorial(j)) for j in range(6))>7)
test('exp4_gt48',sum(F(4**j,factorial(j)) for j in range(7))>48)
test('outside_endpoint_barrier',F(1,5)-F(33,224)==F(59,1120)<F(1107,16000))
test('sqrt15_gt15_over4',15>F(15,4)**2)
test('outside_prefactor',F(112,1)/(5*F(15,4))<6)
test('outside_exp',sum(F(118,35)**j/factorial(j) for j in range(7))>24)
test('density_margin',1-F(1,10)-F(1,1000)-F(1,4)-F(1,8)==F(131,250)>F(1,2))
test('full_tail_prefactor',F(5,3)<F(4,3)**2)
test('log2_lt_point7',sum(F(7,10)**j/factorial(j) for j in range(4))>2)
test('correction_derivative',F(7,10)<F(144,125)-F(5,16))
test('correction_N64_exponent',-F(279,2000)*64+F(67,20)+F(5,256)==-F(177871,32000)<0)
test('correction_N64_ratio',F(5,72)<F(1,2))
out={'status':'EXACT_ANALYTIC_CONSTANT_CHECKS_PASS','delta_exact':'5/4',
     'analytic_range':'all N>=64','checks':checks,'phase_upper':str(phase),
     'scope':'Analytic tail only; finite prefix and fresh audit are separate requirements.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
