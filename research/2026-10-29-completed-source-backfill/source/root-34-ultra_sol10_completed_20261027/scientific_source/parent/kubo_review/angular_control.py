"""Independent coupled-spin control of the actual 25-state Kubo source.
Uses root's scalar enclosure only, no producer matrix/projector imports.
"""
from fractions import Fraction as F
from pathlib import Path
import importlib.util,json
OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('root_trace',OUT.parent/'validated_twist_trace/certify.py')
rt=importlib.util.module_from_spec(spec);spec.loader.exec_module(rt)
def exponential(x):
    low,high=rt.exp_interval(F(x));return F(low,rt.S),F(high,rt.S)
terms=[(F(-4,3),18),(F(2,3),15),(F(25,9),9),(F(31,2),-12)]
low=high=F(133,18)
for coefficient,power in terms:
    a,b=exponential(power)
    low+=coefficient*(a if coefficient>=0 else b)
    high+=coefficient*(b if coefficient>=0 else a)
raw=json.loads((OUT.parents[1]/'validated_kubo/KUBO_CERTIFICATE.json').read_text())
physical=raw['correlations']['left,right']['physical']
assert F(physical['lower'])<=low<=high<=F(physical['upper'])
projector=raw['correlations']['left,right']['exact_projector_comparator']
assert max(low,F(projector['lower']))<=min(high,F(projector['upper']))
zlo=zhi=F(7)
for coefficient,power in [(1,18),(3,15),(5,9),(9,-12)]:
    a,b=exponential(power);zlo+=coefficient*a;zhi+=coefficient*b
assert F(raw['partition_trace']['lower'])<=zlo<=zhi<=F(raw['partition_trace']['upper'])
weights=[];previous=F(0)
for J in range(5):
    total=F((2*J+1)*(24-J*(J+1)),3)
    if J<4:
        following=total-previous;weights.append(following);previous=following
    else:assert total==previous
assert weights==[8,14,16,12]
result={'status':'ROOT_ANGULAR_MOMENTUM_SOURCE_CONTROL_PASS',
        'adjacent_Dz_transition_weights':list(map(str,weights)),
        'C_LR_formula':'-4/3 exp18+2/3 exp15+25/9 exp9+133/18+31/2 exp(-12)',
        'lower':str(low),'upper':str(high),'width':str(high-low),
        'display_only_value':float((low+high)/2),'display_only_width':float(high-low),
        'generic_certificate_contains_control':True,'exact_projector_control_overlaps':True,
        'scope':'Independent source-level control at H=3 S1 dot S2,beta1; generic Kubo error theorem is separately reviewed.'}
(OUT/'ANGULAR_CONTROL.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','display_only_value','display_only_width']},indent=2))
