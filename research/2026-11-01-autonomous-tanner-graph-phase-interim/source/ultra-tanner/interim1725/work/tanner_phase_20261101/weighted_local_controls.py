"""Exact locality identity for a weighted local generator, with common bath.

Includes a signed difference of dissipators: individual perturbations need
not be CP. The actual perturbed jump J+E is a valid physical jump.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/tanner_global_phase_20261101'
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)


def ten(*args):return s.kronecker_product(*args)


def diss_adj(J,A):
    D=J.conjugate().T*J
    return J.conjugate().T*A*J-(D*A+A*D)/2


def main():
    # Four commuting local checks, including both Pauli types and far
    # factors overlapping the near ones. Last tensor factor is ONE bath.
    checks=[ten(Z,Z,I,I,I),ten(I,Z,Z,I,I),ten(X,X,X,I,I),ten(I,I,I,Z,I)]
    D=32;ident=s.eye(D)
    assert all(A*B==B*A for A,B in itertools.product(checks,repeat=2))
    plus=[(ident+C)/2 for C in checks];minus=[(ident-C)/2 for C in checks]
    near=[0,2];far=[1,3]
    def product(factors):
        out=ident
        for A in factors:out=out*A
        return out
    sqrtF=product(plus[i]+2*minus[i] for i in range(4))
    invF=product(plus[i]+s.Rational(1,2)*minus[i] for i in range(4))
    sqrtNear=product(plus[i]+2*minus[i] for i in near)
    invNear=product(plus[i]+s.Rational(1,2)*minus[i] for i in near)
    P=s.zeros(D)
    for bits in itertools.product(range(2),repeat=4):
        if sum(bits)<=1:P+=product((minus[i] if b else plus[i]) for i,b in enumerate(bits))
    assert P*P==P and sqrtF*invF==ident
    # Both ideal and perturbed jumps act on data qubit 0 and this same bath.
    J=ten(X,I,I,I,X)/4
    E=ten(Z,I,I,I,Z)/32
    H=ten(X,I,I,I,(I+Z)/2)/64
    def Vstar(A):return diss_adj(J+E,A)-diss_adj(J,A)+s.I*(H*A-A*H)
    full=invF*Vstar(sqrtF*P*sqrtF)*invF
    local=invNear*Vstar(sqrtNear*P*sqrtNear)*invNear
    assert full==local
    delta=s.Rational(1,32)+s.Rational(17,512)
    assert delta==s.Rational(33,512)
    # F_near=4^(u0+u2) has norm 16 and minimum >=1.
    bound=16*delta
    compressed=P*full*P
    residual=np.array(compressed-bound*P,complex)
    maximum=float(np.linalg.eigvalsh((residual+residual.conj().T)/2)[-1])
    assert maximum<1e-11
    # A truly non-CP signed perturbation appears in the proof interface;
    # setting the correction jump to J+E keeps the total generator GKSL.
    out=dict(exact_far_factor_cancellation=True,local_checks=4,near_checks=near,
             far_checks=far,projector_rank=int(s.trace(P)),
             perturbation_diamond_upper=str(delta),relative_compressed_upper=str(bound),
             largest_upper_residual_preview=maximum,
             actual_perturbed_jump='J+E',bath_dimension=2,
             scope='Exact weighted locality/compression identity plus finite floating positivity control; not a scalable code instance')
    out['program_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'weighted_local_controls.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(output=str(OUT/'weighted_local_controls.json'),checks=list(out))))


if __name__=='__main__':main()
