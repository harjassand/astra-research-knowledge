"""Exact rational verification of a nonperturbative environment-uniform bound.
Requires SymPy. No floating-point eigenvalue is accepted as a certificate.
"""
from __future__ import annotations
import json,time
from pathlib import Path
import sympy as sp
from experiment import heisenberg,local_pair

def exact_matrix(M):return sp.Matrix([[sp.Rational(float(x)).limit_denominator(10**8) for x in row] for row in M])

def partial_singlet(H,r=4):
    s=sp.Matrix([0,1/sp.sqrt(2),-1/sp.sqrt(2),0])
    W=sp.kronecker_product(s,sp.eye(r));return W.T*H*W

if __name__=='__main__':
    started=time.perf_counter()
    edges=[(0,1,1),(0,2,1),(1,3,1)]
    h0=exact_matrix(heisenberg(4,edges).toarray())
    h1=h0+exact_matrix(heisenberg(4,[(0,1,1)]).toarray())
    s=sp.Matrix([0,1/sp.sqrt(2),-1/sp.sqrt(2),0]);Ps=s*s.T;Pt=sp.eye(4)-Ps;q=sp.Rational(1,2)
    K=Ps+q*Pt;KR=sp.kronecker_product(K,sp.eye(4))
    image=KR*h1*KR+(1-q*q)*sp.kronecker_product(Pt,partial_singlet(h1))
    R=sp.simplify(h0-image)
    ev=R.eigenvals()
    lower=(5-sp.sqrt(13))/8
    assert all(sp.simplify(v-lower).is_nonnegative for v in ev)
    assert K*K+(1-q*q)*Pt==sp.eye(4)
    out={'motif':'central antiferromagnetic pair with one independent spin-1/2 neighbor per endpoint; all three initial exchanges equal 1',
         'change':'central exchange 1 to 2',
         'q':'1/2','spectrum':{str(k):v for k,v in ev.items()},
         'certified_difference_lower':'-3/4','certified_difference_upper':str(-lower),
         'upper_decimal':float(-lower),'seconds':time.perf_counter()-started}
    root=Path(__file__).parent
    (root/'exact_amplitude_certificate.json').write_text(json.dumps(out,indent=2))
    (root/'exact_amplitude_residual.json').write_text(json.dumps([[str(x) for x in row] for row in R.tolist()]))
    print(json.dumps(out,indent=2))
