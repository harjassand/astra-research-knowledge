"""Exact 6x6 partial-transpose and projection checks, using installed SymPy."""
import sympy as s

e=s.symbols('epsilon',positive=True)
v=s.zeros(6,1)
v[0]=v[3]=1/s.sqrt(2)
u=s.eye(6)[:,4]
P=v*v.T
sigma=P+e*s.eye(6)
H=v*u.T+u*v.T

def partial_trace_A(M):
    return sum([M[2*a:2*a+2,2*a:2*a+2] for a in range(3)],s.zeros(2))

def partial_transpose_A(M):
    result=s.zeros(6)
    for a in range(3):
        for b in range(3):
            result[2*a:2*a+2,2*b:2*b+2]=M[2*b:2*b+2,2*a:2*a+2]
    return result

def W(M):
    return (s.kronecker_product(s.eye(3),partial_trace_A(M))-partial_transpose_A(M))/2

assert partial_trace_A(H)==s.zeros(2)
N_sigma=W(sigma)
N_H=W(H)
singlet=s.Matrix([0,1/s.sqrt(2),-1/s.sqrt(2),0])
Q=singlet*singlet.T
assert N_sigma[:4,:4]==Q/2+e*s.eye(4)
assert N_sigma[4:,4:]==(s.Rational(1,4)+e)*s.eye(2)
assert N_sigma[:4,4:]==s.zeros(4,2)
Y=N_H[:4,4:]
expected=s.zeros(4,2)
expected[0,0]=expected[2,1]=-1/(2*s.sqrt(2))
assert Y==expected
norm2=lambda X:s.simplify(s.trace(X.T*X))
assert norm2(Y)==s.Rational(1,4)
assert norm2(Q*Y)==s.Rational(1,16)
assert norm2((s.eye(4)-Q)*Y)==s.Rational(3,16)
assert s.simplify(sigma*v-(1+e)*v)==s.zeros(6,1)
assert s.simplify(sigma*u-e*u)==s.zeros(6,1)
print('Exact partial-transpose and BKM projection checks passed.')
print('Output tangent block Y =',Y)
print('Squared norms: total 1/4, singlet 1/16, complement 3/16.')

# Independent interval check of the baseline's remaining entropy slack.
import mpmath as m
import json
from pathlib import Path
m.iv.dps=60
iv=m.iv
eps=iv.mpf(1)/100
Z=1+6*eps
entropy=lambda values:-sum(x*iv.ln(x) for x in values)
baseline_gap=(2*entropy([(iv.mpf(1)/2+eps)/Z]+[eps/Z]*3+[(iv.mpf(1)/4+eps)/Z]*2)
              -entropy([(1+eps)/Z]+[eps/Z]*5)-iv.ln(2)-iv.ln(3))
assert baseline_gap.a>0
receipt={'exact_matrix_checks':'passed','epsilon':'1/100',
         'baseline_gap_above_log3':str(baseline_gap),
         'scope':'A pinching-mechanism obstruction, not an entropy-target violation.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(receipt,indent=2))
print(json.dumps(receipt,indent=2))
