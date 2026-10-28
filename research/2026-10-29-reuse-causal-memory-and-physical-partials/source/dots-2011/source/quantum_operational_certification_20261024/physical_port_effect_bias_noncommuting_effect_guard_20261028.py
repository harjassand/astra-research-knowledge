#!/usr/bin/env python3
"""Effect mechanism with four noncommuting quantum-memory instrument effects."""
import itertools,json
from pathlib import Path
import sympy as s
I=s.eye(2)
L=[s.diag(s.Rational(3,5),s.Rational(4,5)),s.Matrix([[0,s.Rational(3,5)],[s.Rational(4,5),0]])]
D=[s.diag(s.Rational(5,13),s.Rational(12,13)),s.diag(s.Rational(12,13),s.Rational(5,13))]
R=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
K=[B*R*A for A,B in itertools.product(L,D)]
E=[A.H*A for A in K]
assert sum(E,s.zeros(2))==I
commutator=E[0]*E[2]-E[2]*E[0]
assert commutator!=s.zeros(2)
rates=[s.Rational(1,10),s.Rational(1,5),s.Rational(3,10),s.Rational(2,5)]
bad=sum((p*A for p,A in zip(rates,E)),s.zeros(2))
bias=I-2*bad;lower=s.Rational(1,5)*I
res=bias-lower
assert res==res.H and res[0,0]>=0 and res[1,1]>=0 and res.det()>=0
out={'status':'PASS_EFFECT_BIAS_MECHANISM_WITH_NONCOMMUTING_INSTRUMENT_EFFECTS',
     'source_outcomes':0,'rng_draws':0,'instrument_branches':4,
     'nonzero_effect_commutator':str(commutator),'signed_bias_effect':str(bias),
     'uniform_lower_effect':'(1/5) I','positive_residual_determinant':str(res.det())}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
