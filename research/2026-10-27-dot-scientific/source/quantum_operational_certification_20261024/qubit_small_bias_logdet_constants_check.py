from fractions import Fraction as F
from pathlib import Path
import json
assert 3-2*F(13,12)==F(5,6)
assert 1+F(5,6)/2==F(17,12)
assert 1-2*(F(12,17)**2)==F(1,289)
assert F(1,289)/4==F(1,1156)
assert F(1,1156)/2==F(1,2312)
report={'status':'PASS','physical_bias_upper':'13/12','relative_head_order':'17/12','noncommutative_Hessian_margin':'1/289','coherence_logdet_margin':'1/2312','scope':'qubit reference, pointwise logdet only; not inverse-trace sign'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
