#!/usr/bin/env python3
"""Exact scope obstruction: block-history != microscopic-state control."""
from pathlib import Path
import itertools,json,hashlib
import sympy as s
ROOT=Path(__file__).resolve().parent;R=s.Rational


def run():
    d=R(1,10);p=s.Matrix([1,1,-1,-1])/2;q=s.Matrix([1,-1,1,-1])/2
    A=[s.ones(4)/4+sign*d*(p*q.T+q*p.T) for sign in [1,-1]]
    P=s.diag(s.ones(2)/2,s.ones(2)/2);Q=s.eye(4)-P
    b=s.Matrix([1,1,0,0]);ell=b/2;checks=0;block=[]
    for M in A:assert min(M)>=0 and M*s.ones(4,1)==s.ones(4,1);checks+=1
    for policy in itertools.product(range(2),repeat=2):
        M=s.Matrix.vstack(A[policy[0]][:2,:],A[policy[1]][2:,:])
        value=(ell.T*M*b)[0];assert value==R(1,2);checks+=1
        assert Q*M*Q==s.zeros(4);checks+=1;block.append(str(value))
    v=[M*b for M in A];best=s.Matrix([max(x[i] for x in v) for i in range(4)])
    microscopic=(ell.T*best)[0];assert microscopic==R(1,2)+d/2;checks+=1
    return {'status':'PASS_EXACT_MICROSCOPIC_SCOPE_LIMIT','checks':checks,'delta':str(d),
      'every_one_step_block_history_value':'1/2','microscopic_optimum':str(microscopic),
      'strict_gap':str(d/2),'one_step_block_model_error':'0',
      'scope':'No history exists beyond the initial block at horizon1. Thus even exact block-history value agreement cannot imply optimality against microscopic-state feedback. This is an information/class restriction, not an optimal-planning hardness claim.',
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    out=run();(ROOT/'microscopic_limit_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
