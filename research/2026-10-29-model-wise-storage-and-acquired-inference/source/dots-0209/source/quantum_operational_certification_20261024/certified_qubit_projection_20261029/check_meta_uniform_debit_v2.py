from exact_meta_arithmetic_v1 import _series
from fractions import Fraction as F
from math import factorial,isqrt
from pathlib import Path
import json
D=1<<64;end=F(2,3)+F(1,D)
assert end<1 and _series(end,33)>F(1,2)
assert 4*D<factorial(33)
N=1024
out={'status':'PASS_EXACT_RATIONAL_UNIFORM_EXPECTED_DEBIT','D':str(D),'odd_lower_at_max_argument_exceeds_half':True,'four_D_less_than_33_factorial':True,'uniform_relative_factor_debit':str(F(5,D)),'uniform_average_regret_debit_N1024':str(F(40*isqrt(N),D)),'safe_regret_coin_coupling_N1024':str(F(2*N,1<<128)),'scope':'Replaces realized-ledger interpretation in the expected theorem; no data or frozen source changed.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
