"""Find numerical trials, then export rational witnesses for independent verification."""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction
import json,time,platform
import numpy as np
import sympy as sp
import scipy
from fast import dual_context_setup, dual_context_eval, fast_primal
from verify import verify_lower,verify_upper,verify_file

root=Path(__file__).parent
scale=2**40
start=time.perf_counter();data=dual_context_setup(6)
basis,N,outer,G,valid,pop=data
setup_seconds=time.perf_counter()-start
if any(value.q!=1 for value in N):raise RuntimeError('Nonintegral nullspace basis requires an explicit denominator.')
Nint=np.asarray(N,dtype=np.int64)
results=[]
for p in [Fraction(1,2),Fraction(4,5),Fraction(19,20)]:
    started=time.perf_counter()
    lo,z=dual_context_eval(data,float(p))
    # All rounding occurs in free coordinates, so exact constraints survive.
    zi=[int(round(float(x)*scale)) for x in z]
    coeff=[sum(int(Nint[i,j])*zi[j] for j in range(len(zi))) for i in range(len(basis))]
    hi,pbasis,pz,V,t,details=fast_primal(10,float(p))
    pcoeff=[int(round(float(x)*scale)) for x in pz]
    witness={'model':'Bertini-Toninelli 1D; exchange rate 1-eta[x-1]*eta[x+2]',
             'density':str(p),'scale':scale,
             'dual':{'r':6,'outer':list(outer),'terms':[{'shape':sorted(a),'numerator':c} for a,c in zip(basis,coeff) if c]},
             'primal':{'m':10,'basis':'centered occupation products','terms':[{'shape':sorted(a),'numerator':c} for a,c in zip(pbasis,pcoeff) if c]}}
    exact_lo=verify_lower(witness);exact_hi=verify_upper(witness)
    assert abs(float(exact_lo)-lo)<1e-9,(p,lo,float(exact_lo))
    assert abs(float(exact_hi)-hi)<1e-9,(p,hi,float(exact_hi))
    witness.update(lower_fraction=str(exact_lo),upper_fraction=str(exact_hi))
    name=f'certificate_{p.numerator}_{p.denominator}.json'
    path=root/name;path.write_text(json.dumps(witness,indent=2)+'\n')
    result=verify_file(path);result.update(file=name,generation_seconds=time.perf_counter()-started,
        dual_local_configurations=len(G),dual_legal_configurations=int(valid.sum()),dual_trial_dimension=N.cols,
        dual_monomial_columns=len(basis),primal_trial_columns=len(pbasis),primal_lsqr_iterations=details[1],
        max_abs_free_dual_coefficient=float(np.max(np.abs(z))),max_abs_primal_coefficient=float(np.max(np.abs(pz))))
    results.append(result)
    print(json.dumps({k:v for k,v in result.items() if not k.endswith('_fraction')},indent=2),flush=True)
metadata={'setup_seconds':setup_seconds,'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__},'results':results}
(root/'certified_results.json').write_text(json.dumps(metadata,indent=2)+'\n')
