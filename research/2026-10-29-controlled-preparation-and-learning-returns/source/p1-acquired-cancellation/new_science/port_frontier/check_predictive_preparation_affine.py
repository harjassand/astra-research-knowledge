#!/usr/bin/env python3
"""Exact finite illustration: acquired reset need not preserve baseline pi.

Four hidden states consist of a visible bit and a frozen hidden spectator.
The acquired two-coordinate service algebra is exact. No physical data are
sampled; this checks the affine preparation algebra and its explicit scope.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json


def mm(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def main():
    W=[[F(9,10),F(1,10)],[F(2,5),F(3,5)]]
    pi=[F(1,2),F(1,2)]
    prepared=[F(4,5),F(1,5)]
    assert mm([pi],W)[0]!=pi
    assert mm([prepared],W)[0]==prepared
    assert prepared[0]*W[0][1]==prepared[1]*W[1][0]
    e=[[F(1)],[F(-1)]]
    We=mm(W,e)
    b=(We[0][0]+We[1][0])/2
    kappa=(We[0][0]-We[1][0])/2
    assert b==F(3,10) and kappa==F(1,2)
    prepared_prediction=[F(1,2)+b/(2*(1-kappa)),F(1,2)-b/(2*(1-kappa))]
    assert prepared_prediction==prepared

    # Tensor identity on a hidden spectator: its value never resets.
    W4=[[W[i//2][j//2] if i%2==j%2 else F(0) for j in range(4)] for i in range(4)]
    assert all(W4[i][j]==0 for i in range(4) for j in range(4) if i%2!=j%2)
    P=[[F(1),F(0)],[F(0),F(1)]]
    rows=[]
    for m in range(21):
        gap=max(sum(abs(P[i][j]-prepared[j]) for j in range(2))/2 for i in range(2))
        exact=F(4,5)*kappa**m
        theorem=F(1,2)*(2+b/(1-kappa))*kappa**m
        assert gap==exact and gap<=theorem
        rows.append({'m':m,'actual_uniform_visible_tv':str(gap),
                     'theorem_tv_upper':str(min(F(1),theorem))})
        P=mm(P,W)
    proof=Path(__file__).with_name('PREDICTIVE_PREPARATION_WITHOUT_HIDDEN_STATIONARITY.md')
    out={'status':'PASS','scope':'Exact algebraic illustration, no physical acquisition.',
         'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),
         'baseline_pi':list(map(str,pi)),'prepared_law':list(map(str,prepared)),
         'W':[[str(x) for x in row] for row in W],
         'W_does_not_preserve_baseline_pi':True,'hidden_spectator_frozen':True,
         'centered_contraction':str(kappa),'acquired_centered_bias':str(b),
         'checks':rows}
    p=Path(__file__).with_name('PREDICTIVE_PREPARATION_AFFINE_EXACT_CHECKS.json')
    p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','prepared_law','centered_contraction',
                                      'acquired_centered_bias','hidden_spectator_frozen']},indent=2))


if __name__=='__main__':
    main()
