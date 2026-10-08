#!/usr/bin/env python3
"""Checks the composition identity used in the iteration-barrier note.
Shares only basis/Choi utility functions with the main diagnostic. These
small-dimensional fixtures are NOT examples of the large-dimension theorem.
"""
from __future__ import annotations
import json, math
from pathlib import Path
from fractions import Fraction
import numpy as np
from verify_gaussian_construction import basis_sym0, map_from_choi

ROOT=Path(__file__).resolve().parents[1]
rng=np.random.default_rng(2026100804)
rows=[]; worst=0.0; hs_worst=0.0
for d in [2,3,4,5,6,8]:
    s=basis_sym0(d); h=len(s)
    for trial in range(4):
        g=rng.normal(size=(h,h))
        G=np.einsum('ab,aij,bkl->ikjl',g,s,s,optimize=True).reshape(d*d,d*d)/d
        choi=(np.eye(d*d)+G/6)/d
        composed=np.zeros_like(choi)
        for i in range(d):
            for j in range(d):
                e=np.zeros((d,d));e[i,j]=1
                composed[i*d:(i+1)*d,j*d:(j+1)*d]=map_from_choi(choi,map_from_choi(choi,e,d),d)
        E=np.einsum('ab,aij,bkl->ikjl',g@g,s,s,optimize=True).reshape(d*d,d*d)/(36*d**3)
        err=float(np.linalg.norm(d*composed-np.eye(d*d)-E))
        hs_err=float(abs(np.linalg.norm(E)-np.linalg.norm(g@g)/(36*d**3)))
        worst=max(worst,err);hs_worst=max(hs_worst,hs_err)
        assert err<1e-12 and hs_err<1e-12
        rows.append({'d':d,'trial':trial,'composition_residual':err,
          'E_Frobenius':float(np.linalg.norm(E)),
          'crude_Frobenius_bound':float(np.linalg.norm(g,2)*np.linalg.norm(g)/(36*d**3)),
          'scope':'Identity diagnostic only; no claim of uniform Schmidt bound.'})
assert Fraction(8,36)==Fraction(2,9)
assert Fraction(1,4)-Fraction(9,32)*Fraction(7,10)>Fraction(1,20)
for d in range(2,101):
    h=d*(d+1)//2-1
    assert 4*h<=3*d*d
result={'status':'Internal algebraic diagnostics; the universal claims are analytic',
 'seed':2026100804,'count':len(rows),'max_composition_residual':worst,
 'max_HS_identity_residual':hs_worst,'checks':rows,
 'imported_criterion':'Gurvits-Barnum 2002 Theorem 1, unnormalized identity HS ball radius one'}
(ROOT/'results'/'iteration_barrier_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
