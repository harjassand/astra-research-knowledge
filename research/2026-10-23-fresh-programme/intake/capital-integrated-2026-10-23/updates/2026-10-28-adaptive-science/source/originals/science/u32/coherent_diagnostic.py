"""Finite response/rank diagnostic; analytical obstruction is in the proof."""
import json
import math
from fractions import Fraction
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
theta=math.pi*math.sqrt(2)
c,s=math.cos(2*theta),math.sin(2*theta)
R=np.array([[1,0,0],[0,c,s],[0,-s,c]])
M0=np.array([[.5,0,.5],[0,0,0],[.5,0,.5]])
M1=np.array([[.5,0,-.5],[0,0,0],[-.5,0,.5]])
initial=np.array([1.,0,1.]);trace=np.array([1.,0,0])
preps=np.column_stack([np.linalg.matrix_power(R,j)@initial for j in range(3)])
tests=np.vstack([trace,trace@M0,trace@M0@R])
H=tests@preps
assert abs(np.linalg.det(H))>1e-4
assert np.max(abs(trace@(M0+M1)-trace))<1e-12

# Rational phase-cycle competitors receive the same exact theta for this
# representation-only comparison. These are not learned from count data.
out={'theta_over_pi':'sqrt(2)','rank_three_core_det':float(np.linalg.det(H)),
     'rank_three_core_singular_values':np.linalg.svd(H,compute_uv=False).tolist(),
     'horizon':100000,'representation_only_phase_cycles':[]}
nn=np.arange(100001)
p=(1+np.cos(2*nn*theta))/2
for max_q in [8,32,128,512]:
    rational=Fraction(math.sqrt(2)).limit_denominator(max_q)
    phase=math.pi*float(rational)
    approx=(1+np.cos(2*nn*phase))/2
    errors=abs(p-approx)
    out['representation_only_phase_cycles'].append({
        'phase_over_pi':str(rational),'classical_phase_states':rational.denominator,
        'max_error_first_10':float(errors[:11].max()),
        'max_error_first_1000':float(errors[:1001].max()),
        'max_error_first_100000':float(errors.max())})
(ROOT/'coherent_diagnostic.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
