from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json
N=24
def lower(x):return sum((x**k/F(factorial(k))for k in range(N+1)),F())
def upper(x):return lower(x)+x**(N+1)/F(factorial(N+1))/(1-x/F(N+2))
assert upper(F(5,8))<2
assert lower(F(81,32))>12
assert lower(F(9,2))>64
assert F(7,20)-F(16,189)>F(1,4)
assert F(1,4)**4==F(1,256)
report={'status':'PASS','series_convention':'No alternating sign: sum exp(-(2k+1)^2 pi^2 t/8) cos((2k+1)pi u/2)','exp_upper_5_8':str(upper(F(5,8))),'exp_lower_81_32':str(lower(F(81,32))),'exp_lower_9_2':str(lower(F(9,2))),'kernel_lower':'1/4','integrated_three_kernel_lower':'1/256'};Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS')
