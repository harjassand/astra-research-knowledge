from fractions import Fraction as F
from unittest.mock import patch
from sampler import *

def reference(x):
    t=s=F(1);lo=F(0);hi=F(1)
    for j in range(1,101):
        t*=-x/j;s+=t
        if j%2:lo=s
        else:hi=s
    return lo,hi
for x in [F(0),F(1,1000),F(3,10),F(1)]:
    lo,hi=expneg(x);rl,rh=reference(x)
    assert F(lo,S)<=rl<=rh<=F(hi,S)
m=prepare()
for i in [0,19,399]:
    for u in [F(1,1<<65),F(1,2),F((1<<65)-1,1<<65)]:
        t,f=inverse_time(m['lam'][i],m['ps'][i],u)
        assert 0<=t<=T
        with patch('sampler.math.log1p',return_value=0.0):
            t,f=inverse_time(m['lam'][i],m['ps'][i],u)
            assert 0<=t<=T
# Explicit rational inequalities used in the finite-error contract.
assert 200/F(S)+F(3,400)**41/math.factorial(41)<F(1,1<<240)
assert m['C']*(200/F(S)+F(3,10)**41/math.factorial(41))<F(1,1<<200)
assert F(2*(m['k']-1),m['n'])*sum(m['lam'])*T<F(3,10)
print('PASS: Taylor brackets, edge uniforms, forced fallback, global precision inequalities')
