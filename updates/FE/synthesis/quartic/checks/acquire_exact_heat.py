#!/usr/bin/env python3
"""Acquire a rational closed heat certificate near a retained numerical point.

All mathematical acceptance checks are exact; rounded floating values choose
only free variables in an exact affine solution. Acquisition is not required
to verify the resulting portable JSON certificate.
"""
from pathlib import Path
import json
import runpy
import time
import numpy as np
import sympy as S

OUT=Path(__file__).parent
tick=time.monotonic()
# Reconstruct the exact polynomial interface; the bounded exploration is cheap.
ns=runpy.run_path(str(OUT/'search_closed_heat.py'))
O=ns['O'];N=ns['N'];D=S.Matrix.hstack(*(O*N).T.nullspace()).T
bmon=ns['bmon'];ij=ns['ij'];coeff=ns['coeff'];n=ns['n']
P=S.Matrix.hstack(*[coeff(bmon[i]*bmon[j])*(1 if i==j else 2) for i,j in zip(*ij)])
Ef=coeff(ns['diss'](ns['F']));Ed=coeff(ns['diss'](ns['q']**2))
T=(D*P).row_join(D*Ed);rhs=D*Ef
rref,pivots=T.row_join(rhs).rref()
assert len(pivots)==T.rows and all(p<T.cols for p in pivots)
free=[j for j in range(T.cols) if j not in pivots]
print('exact affine rank',len(pivots),'free',len(free),flush=True)
candidate=np.load(OUT/'heat_candidate_0.npz')
floating=np.r_[candidate['gram'][ij],candidate['gamma']]
for denominator in [1000,10000,100000]:
    vals=S.zeros(T.cols,1)
    for j in free: vals[j]=S.Rational(round(floating[j]*denominator),denominator)
    for i,j in enumerate(pivots): vals[j]=rref[i,-1]-sum(rref[i,k]*vals[k] for k in free)
    assert T*vals==rhs
    QQ=S.zeros(n)
    for k,(i,j) in enumerate(zip(*ij)):QQ[i,j]=vals[k];QQ[j,i]=vals[k]
    gamma=vals[-1]
    try:
        LL,DD=QQ.LDLdecomposition(hermitian=False)
    except Exception:
        continue
    diag=list(DD.diagonal())
    if gamma<0 or not all(v>0 for v in diag):continue
    gap=P*vals[:-1,0]+gamma*Ed-Ef
    omega=(O*N).gauss_jordan_solve(gap)[0]
    fullomega=N*omega
    assert O*fullomega==gap
    assert ns['C']*fullomega==S.zeros(16,1)
    assert LL*DD*LL.T==QQ
    cert={'schema':'astra-exact-quartic-closed-heat/1',
          'scope':'Fstar only; identity diffusion; closed homogeneous-quadratic 2-form; exact rational bilinear Gram',
          'matrix_entry_order':['a','b','c','d'],
          'jet_order':['phi1_xx','phi1_xy','phi1_yy','phi2_xx','phi2_xy','phi2_yy'],
          'bilinear_order':'A outer jet, row major',
          'omega_pair_order':ns['formpairs'],
          'quadratic_coefficient_order':ns['xpairs'],
          'gamma':str(gamma),
          'gram':[[str(v) for v in row] for row in QQ.tolist()],
          'omega_coefficients':[[str(v) for v in fullomega[10*i:10*i+10,0]] for i in range(6)],
          'ldl_diagonal':[str(v) for v in diag],
          'acceptance':'exact polynomial identity, exact closedness, exact rational positive LDL diagonal',
          'free_variable_rounding_denominator':denominator,
          'historical_novelty':'UNKNOWN',
          'external_review':'UNKNOWN'}
    (OUT/'FSTAR_CLOSED_HEAT_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps({'status':'EXACT_PASS','gamma':str(gamma),'rounding_denominator':denominator,'ldl_pivots':len(diag),'min_float_eigenvalue':float(np.linalg.eigvalsh(np.array(QQ,float))[0]),'seconds':time.monotonic()-tick}),flush=True)
    break
else:raise ArithmeticError('No exact positive certificate acquired from bounded rationalization.')
