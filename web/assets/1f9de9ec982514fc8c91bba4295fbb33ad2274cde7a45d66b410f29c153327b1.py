"""Exact rational three-orbit EB selector for the promised spin-2 class.

Run with four rational sector eigenvalues, for example:
  python3 SPIN2_SELECTOR.py 7/12 7/12 7/12 7/12

The theorem's covariance and actual compatibility promises are SUPPLIED;
this routine does not certify them or acquire eigenvalues from samples.
For certified |lambda_est-lambda_true|<=epsilon, pass epsilon as optional
fifth argument. It selects using lower eigenvalue bounds and returns the
charged relaxed-comparison allowance 4epsilon, as proved in SPIN2_PROOF.
Requires Python standard library only.
"""
from fractions import Fraction as Q
from itertools import combinations
import json, sys

VERTICES=((Q(2,3),Q(2,7),Q(1,14),Q(1,126)),
          (Q(0),Q(2,7),Q(0),Q(2,7)),
          (Q(0),Q(0),Q(5,14),Q(1,6)))

def select(lambda_est,epsilon=Q(0)):
    assert len(lambda_est)==4 and epsilon>=0
    u=[max(Q(0),2*(v-epsilon)-1) for v in lambda_est]
    # Lines A*a+B*b=C. Their ordered intersections give a deterministic
    # selector, including lower-dimensional boundary polytopes.
    lines=((Q(1),Q(0),Q(0)),(Q(0),Q(1),Q(0)),
           (Q(1),Q(1),Q(1)),(Q(1),Q(0),Q(3,2)*u[0]),
           (Q(1),Q(1),Q(7,2)*u[1]),
           (Q(4),Q(5),5-14*u[2]),
           (Q(20),Q(-15),21-126*u[3]))
    for i,j in combinations(range(7),2):
        A,B,C=lines[i];D,E,F=lines[j];det=A*E-B*D
        if det==0:continue
        a=(C*E-B*F)/det;b=(A*F-C*D)/det;c=1-a-b
        if min(a,b,c)<0:continue
        mu=tuple(a*VERTICES[0][k]+b*VERTICES[1][k]+c*VERTICES[2][k] for k in range(4))
        if any(v<uk for v,uk in zip(mu,u)):continue
        assert sum((2*k+3)*v for k,v in enumerate(mu))==4
        # Exact algebraic guarantee when the supplied estimates have the
        # stated error; no true native lambda values are inferred here.
        return {'weights':(a,b,c),'mu':mu,'selected_lines':(i,j),
                'relaxed_dirichlet_allowance':4*epsilon,'outcomes_at_most':1215}
    raise ValueError('No feasible three-orbit selector; supplied class/compatibility/error promises need verification.')

def strings(value):
    if isinstance(value,Q):return str(value)
    if isinstance(value,dict):return {k:strings(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [strings(v) for v in value]
    return value

if __name__=='__main__':
    if len(sys.argv) not in (5,6):
        raise SystemExit('Provide four rational eigenvalues and optionally a certified epsilon.')
    vals=[Q(v) for v in sys.argv[1:5]];eps=Q(sys.argv[5]) if len(sys.argv)==6 else Q(0)
    print(json.dumps(strings(select(vals,eps)),indent=2))
