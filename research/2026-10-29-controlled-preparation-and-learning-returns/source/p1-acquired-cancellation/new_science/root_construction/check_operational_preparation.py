#!/usr/bin/env python3
"""Exact acquired-quotient reset example with permanently frozen hidden memory."""
from pathlib import Path
from fractions import Fraction as F
import contextlib,io,json,math,runpy
import numpy as np
with contextlib.redirect_stdout(io.StringIO()):
    b=runpy.run_path(str(Path(__file__).with_name('check_pulse_closure.py')))
Q=b['Qd']; Phi=b['F8']; eye=b['eye']; zero=b['zero']; inv=b['inv']
Qf=np.kron(Q,eye(2)); one=b['ones'](8)
frozen=b['mat']([[1],[-1],[1],[-1],[1],[-1],[1],[-1]])
assert zero(Qf@frozen) and zero(Qf@one)
G=Phi.T@Phi/F(8); A=inv(G)@(Phi.T@Qf@Phi/F(8))
assert zero(Qf@Phi-Phi@A)
# Q on the first factor is 16(J/4-I)+(1/4) vv^T, ||v||^2=6.
# Its centered eigenvalues are -16,-16,-29/2; hidden full generator has TWO zeros.
v=b['mat']([[-2],[0],[1],[1]])
assert (v.T@v)[0,0]==6 and zero(Q@v+F(29,2)*v)
J=b['ones'](4)@b['ones'](4).T/F(4)
assert zero((Q+16*(eye(4)-J))@v-F(3,2)*v)
gap=F(29,2)
g=1/max(sum(abs(x) for x in row) for row in inv(G))
c2=F(4)/g
c=math.isqrt(c2.numerator//c2.denominator)
if F(c*c)<c2:c+=1
target=F(1,100)
t=0
while True:
    power=(gap*t).numerator//(gap*t).denominator
    upper=F(c,2)*F(1,2**power) # exp(-gap*t)<=2^(-floor(gap*t))
    if upper<=target:break
    t+=1
assert zero(Qf@frozen)
out={'result':'PASS','native_states':8,'controlled_predictive_rank':4,
 'hidden_zero_eigenvectors':['constant','frozen spectator bit'],
 'microscopic_global_gap':0,'acquired_operational_gap':str(gap),
 'certified_gram_floor':str(g),'pointwise_feature_norm_ceiling':c,
 'reset':'Actual baseline generator for a fixed deterministic duration; no reset path readout retained.',
 'duration':t,'future_record_TV_upper':str(upper),'target':str(target),
 'scope':'Exact closed representation and population moments. Not a finite-data universal reset or cold-start preparation certificate.'}
p=Path(__file__).with_name('OPERATIONAL_PREPARATION_EXACT_RESULTS.json')
p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'result':'PASS','hidden_global_gap':0,'operational_gap':float(gap),
 'reset_duration':t,'future_record_TV_upper':float(upper),'output':str(p)},indent=2))
