"""Exact rational certificates for a cloud-only intermediate-oracle bound."""
from pathlib import Path
from fractions import Fraction
import importlib.util
import math
import csv

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('rigidity_exact', ROOT.parent/'round2_positive'/'check_shift_rigidity.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
rows=[]
lines=['CLOUD-ONLY NONLINEAR ACQUISITION OBSTRUCTION']
for j in (2,4,8,12,16):
    kappa=Fraction(1,2**j)
    # A floating logarithm proposes the integer; exact arithmetic certifies it.
    proposed=1/(2*float(kappa)**2*math.log(12/float(kappa)))
    n0=math.floor(proposed)
    x=1/(2*n0*kappa*kappa)
    lo,hi,terms,squares=module.exp_negative_interval(x,192)
    assert hi<kappa/12
    rows.append([str(kappa),str(kappa/32),n0,n0+1,str(hi),str(kappa/12)])
    lines.append(f'kappa={kappa}, epsilon<={kappa/32}: at most {n0} observations impossible; at least {n0+1} required.')
lines += ['Decisive attenuation bounds and comparisons are exact rational arithmetic.',
          'Source values used: zero. Not a lower bound for the original N687 oracle.']
with (ROOT/'cloud_only_count_bounds.csv').open('w',newline='') as f:
    writer=csv.writer(f)
    writer.writerow(['kappa','maximum_target_tv','impossible_count','required_count','attenuation_upper','threshold'])
    writer.writerows(rows)
text='\n'.join(lines)+'\n'
(ROOT/'CLOUD_ONLY_BOUND_RESULTS.txt').write_text(text)
print(text)
