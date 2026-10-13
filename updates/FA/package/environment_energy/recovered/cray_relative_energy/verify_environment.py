"""Exact rational energy enclosure for an explicit near-extremal environment."""
from __future__ import annotations
from pathlib import Path
import json, time
import numpy as np
import sympy as s
from scipy.linalg import eigh
from rational_verify import exact_pd,ratmatrix
from experiment import heisenberg

def bound_ground(H):
    e,v=eigh(np.array(H,dtype=float));q=ratmatrix(v[:,0,None]);upper=(q.T*H*q)[0]/(q.T*q)[0]
    lower=s.Rational(int(np.floor(e[0]*10**9))-5,10**9)
    exact_pd(H-lower*s.eye(H.rows))
    assert upper>=lower
    return lower,s.cancel(upper),q

if __name__=='__main__':
    start=time.perf_counter();root=Path(__file__).parent
    h0=ratmatrix(heisenberg(4,[(0,1,1),(0,2,1),(1,3,1)]).toarray())
    h1=h0+ratmatrix(heisenberg(4,[(0,1,1)]).toarray());t=s.Rational(-59307,100000)
    env=t*ratmatrix(heisenberg(4,[(2,3,1)]).toarray())
    l0,u0,v0=bound_ground(h0+env);l1,u1,v1=bound_ground(h1+env)
    # Round enclosure outward using exact rational arithmetic.
    lo=s.floor((l1-u0)*10**8)/10**8;hi=s.ceiling((u1-l0)*10**8)/10**8
    data={'environment_exchange':str(t),'weak_interval_decimal':[float(l0),float(u0)],'strong_interval_decimal':[float(l1),float(u1)],'difference_interval_exact':[str(lo),str(hi)],'difference_interval_decimal':[float(lo),float(hi)],'verification':'Exact rational positive-definite shifts and Rayleigh quotients','seconds':time.perf_counter()-start}
    (root/'rational_environment_verification.json').write_text(json.dumps(data,indent=2))
    # Exact rational vectors permit independent upper-bound verification.
    fixture={'t':str(t),'weak_rayleigh_vector':[str(x) for x in v0],'strong_rayleigh_vector':[str(x) for x in v1],'weak_lower':str(l0),'strong_lower':str(l1)}
    (root/'rational_environment_fixture.json').write_text(json.dumps(fixture,indent=2));print(json.dumps(data,indent=2))
