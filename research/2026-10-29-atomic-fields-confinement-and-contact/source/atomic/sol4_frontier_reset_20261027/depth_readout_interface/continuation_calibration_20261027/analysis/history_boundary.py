"""Untimed detector counts do not label endpoints under arbitrary hidden paths.

At every probe dwell compare equal exposure in native and layer15, in opposite
temporal orders. The actual multislice template count integrals are identical.
State paths/reset timing are hypothetical, not an acquired transition law.
Time-resolved or transition-aware ordinary observation can escape this boundary.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from paired_screen import load
ROOT=Path(__file__).resolve().parents[1]
ss,p,d=load('rigid256');p0=p[ss.index(0)];p1=p[ss.index(15)]
order01=.5*p0+.5*p1;order10=.5*p1+.5*p0
out={'scope':__doc__,'templates':'Frozen actual native and layer15 detector probabilities',
     'integrated_mean_max_absolute_difference':float(np.max(np.abs(order01-order10))),
     'mean_arrays_identical':bool(np.array_equal(order01,order10)),
     'equal_prior_endpoint_error_lower_bound':.5,
     'quantifier':'For a path class allowing both orders with equal occupation fractions within every retained dwell; no claim that measured CrSBr kinetics realize them.',
     'escape':'Retain sub-dwell timestamps/subframes and acquire a transition/observation law; an ordinary controller receives identical access.',
     'damage_rate_inferred':False}
(ROOT/'outputs/history_boundary.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
