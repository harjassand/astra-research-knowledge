#!/usr/bin/env python3
"""Exact counterexample: true residual contracts but block comparison refuses."""
from pathlib import Path
import hashlib,json,math,sys
import sympy as s
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent.parent/'robust_operator_reuse_20261031'/'finite_observation'))
from robust_replay import psd
R=s.Rational


def run():
    A=s.Matrix([[0,1,1,0,0,0],[0,2,0,0,0,0],[0,1,0,0,0,1],
                [0,1,0,0,0,1],[1,0,0,0,0,1],[0,2,0,0,0,0]])/2
    P=s.diag(s.ones(3)/3,s.ones(3)/3);Q=s.eye(6)-P;F=Q*A*Q
    assert min(A)>=0 and A*s.ones(6,1)==s.ones(6,1)
    assert psd(R(15,16)**2*s.eye(6)-F.T*F)
    # A lower bound suffices to falsify this sufficient geometry. No random
    # probes or floating SVD are needed in the exact receiving test.
    vectors=[s.Matrix(x) for x in [(0,1,-1),(1,-1,0),(1,0,-1),(1,1,-2),(1,-2,1),(-2,1,1)]]
    lower=s.zeros(2);witnesses=[];S=1<<20
    for g in range(2):
        for h in range(2):
            B=F[3*g:3*g+3,3*h:3*h+3]
            ratios=[(B*x).dot(B*x)/x.dot(x) for x in vectors]
            i=max(range(len(vectors)),key=lambda j:ratios[j]);v=ratios[i]
            z=math.isqrt(int(v.p)*S*S//int(v.q));lower[g,h]=R(z,S)
            assert lower[g,h]**2<=v
            witnesses.append({'g':g,'h':h,'vector':list(map(int,vectors[i])),'squared_norm_ratio':str(v),'norm_lower':str(lower[g,h])})
    probes=[s.Matrix([a,b]) for a in range(1,9) for b in range(1,9)]
    v=max(probes,key=lambda z:(lower*z).dot(lower*z)/z.dot(z))
    ratio=(lower*v).dot(lower*v)/v.dot(v)
    assert ratio>1
    return {'status':'PASS_EXACT_SUFFICIENT_CERTIFICATE_FAILURE','checks':7,
      'true_residual_norm_upper':'15/16','comparison_norm_squared_lower':str(ratio),
      'comparison_test_vector':list(map(int,v)),'block_norm_lower_witnesses':witnesses,
      'stochastic_matrix':[[str(x) for x in A.row(i)] for i in range(6)],
      'scope':'Even one stochastic action contracts on the complement but the norm of its exact block-norm comparison exceeds one. No claim that its leakage/task certificate would otherwise admit.',
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    out=run();(ROOT/'comparison_failure_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
