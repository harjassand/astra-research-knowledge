#!/usr/bin/env python3
"""Exact polynomial identity + positive two-quantum on-shell weight."""
import json
from pathlib import Path
import sympy as sp
import mpmath as mp

P=Path(__file__).resolve().parent
w=sp.symbols('w',real=True)
sminus=lambda x:(1-x)**2*(2-x)**2/(6*(x*x+2)*(1+x*x)**2)
amplitude=1/(1-w)+1/(w-2)
raw=sminus(w)*sminus(3-w)*amplitude**2
simple=(w-1)**2*(w-2)**2/(36*(w*w+2)*(1+w*w)**2*((3-w)**2+2)*(1+(3-w)**2)**2)
assert sp.cancel(raw-simple)==0
assert sp.cancel(1/(1-w)+1/(w-1))==0
mp.mp.dps=60
f=sp.lambdify(w,simple,'mpmath')
full=mp.quad(f,[0,1,2,3])
window=mp.quad(f,[mp.mpf(1)/4,mp.mpf(3)/4])
assert full>window>0
out={'scope':'On-shell two-quantum spectral weight, alpha=1; fixed positive rate prefactor omitted. Not a lifetime theorem.',
     'exact_integrand_identity':'PASS','equal_spaced_cancelled_example':'PASS (rejected)',
     'full_integral_0_3':str(full),'restricted_integral_1_4_to_3_4':str(window)}
(P/'results/two_quantum_obstruction.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
