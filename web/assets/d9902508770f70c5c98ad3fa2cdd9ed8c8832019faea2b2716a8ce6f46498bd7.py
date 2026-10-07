"""Small independent exact fixtures and floating 2x2 divergence diagnostics."""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import time

started = time.perf_counter()

# The proper-loss normalization and regret are checked on their legal interval.
s = F(1, 4)
for i in range(17):
    p = (1 - s) / 2 + s * F(i, 16)
    potential = (p - F(1, 2)) ** 2 / s
    slope = (2 * p - 1) / s
    loss0 = p * slope - potential + F(1, 2) - s / 4
    loss1 = (p - 1) * slope - potential + F(1, 2) - s / 4
    assert 0 <= loss0 <= 1 and 0 <= loss1 <= 1
    for j in range(17):
        q = (1 - s) / 2 + s * F(j, 16)
        f_q = (q - F(1, 2)) ** 2 / s
        regret = potential - f_q - (2 * q - 1) * (p - q) / s
        assert regret == (p - q) ** 2 / s

# Exact three-node quadrature moments without floating algebraic nodes.
def uniform_moment(r):
    return F(0) if r % 2 else F(1, r + 1)

def gauss3_moment(r):
    if r == 0:
        return F(1)
    return F(0) if r % 2 else F(5, 9) * F(3, 5) ** (r // 2)

for a in range(6):
    for b in range(6 - a):
        assert uniform_moment(a) * uniform_moment(b) == gauss3_moment(a) * gauss3_moment(b)
tau = F(1, 8)
correct_second = 2 * tau**4 * uniform_moment(4)
wrong_second = tau**4 * uniform_moment(4)
assert correct_second == 2 * wrong_second and correct_second != wrong_second
assert gauss3_moment(6) != uniform_moment(6)
q = F(1, 7)
series_bound = q * (1 + 11*q + 11*q*q + q**3) / (1-q)**5
assert series_bound == F(70, 81) < 1
assert sum((F(2)**k / math.factorial(k) for k in range(6)), F(0)) > 7
assert F(3025, 588 * 72**2) == F(3025, 3048192) < F(1, 1000)

I = ((1.0, 0.0), (0.0, 1.0))
def add(A,B): return tuple(tuple(A[i][j]+B[i][j] for j in range(2)) for i in range(2))
def scale(a,A): return tuple(tuple(a*A[i][j] for j in range(2)) for i in range(2))
def mul(A,B): return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def trace(A): return A[0][0]+A[1][1]
def eig(A):
    h=(A[0][0]+A[1][1])/2
    r=math.hypot((A[0][0]-A[1][1])/2,(A[0][1]+A[1][0])/2)
    return max(0.0,h-r),h+r
def function(A,f):
    x,y=eig(A)
    if abs(y-x)<1e-14:
        return scale(f((x+y)/2),I)
    a=(f(y)-f(x))/(y-x)
    b=(y*f(x)-x*f(y))/(y-x)
    return add(scale(a,A),scale(b,I))
def phi(A):
    return sum(x*math.log(x) if x>0 else 0.0 for x in eig(A))
def relative_entropy(A,B):
    return phi(A)-trace(mul(A,function(B,math.log)))-trace(A)+trace(B)
def covariance(A,T,L):
    if L is None:return add(I,scale(T,A))
    return add(I,function(A,lambda x:(T*x)/(1+T*x/L)))
def stable_remainder(x):
    assert x > -1
    if abs(x)<.05:return sum(((-1)**k)*x**k/k for k in range(2,15))
    return x-math.log1p(x)
def gaussian_kl(CA,CB):
    R=function(CB,lambda x:1/math.sqrt(x))
    S=mul(mul(R,CA),R)
    u,v,w=S[0][0]-1,S[1][1]-1,(S[0][1]+S[1][0])/2
    h=(u+v)/2;r=math.hypot((u-v)/2,w)
    return .5*(stable_remainder(h-r)+stable_remainder(h+r))
def integrate(A,B,L):
    n,left,right=2000,-18.0,18.0
    step=(right-left)/n
    def f(u):
        T=math.exp(u)
        return gaussian_kl(covariance(A,T,L),covariance(B,T,L))*math.exp(-u)
    return step/3*(f(left)+f(right)+sum((4 if i%2 else 2)*f(left+i*step) for i in range(1,n)))
fixtures=[
    (((1.0,0.0),(0.0,4.0)),((2.0,0.0),(0.0,3.0))),
    (((0.0,0.0),(0.0,4.0)),((2.0,1.0),(1.0,2.0))),
    (((3.0,1.0),(1.0,2.0)),((1.5,-.5),(-.5,2.5))),
]
records=[]
for A,B in fixtures:
    D=relative_entropy(A,B)
    exact=integrate(A,B,None)
    assert abs(exact-D/2)<2e-5*(1+D)
    caps=[]
    for L in (1.0,8.0,256.0):
        v=integrate(A,B,L)
        assert -1e-8 <= v <= D/2+2e-5
        caps.append({'L':L,'KL_integral_approx':v})
    records.append({'A':A,'B':B,'matrix_relative_entropy':D,'uncapped_integral_approx':exact,
                    'uncapped_residual':abs(exact-D/2),'caps':caps})
output=Path(__file__).with_name('phase2_audit_checks.json')
assert not output.exists()
report={'status':'PASS','exact_scope':{'proper_loss_actions':17,'regret_pairs':289,
        'tensor_quadrature_moments':21,'finite_jet_factorial_repair':True,
        'series_bound_70_over_81':True,'periodic_codec_J72':True},
        'matrix_scope':'FLOATING_DIAGNOSTICS_ONLY; NOT_A_THEOREM_OR_MI_EVALUATION',
        'matrix_records':records,'local_seconds':time.perf_counter()-started,'backend_energy':'UNKNOWN'}
output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','exact_scope':report['exact_scope'],
    'max_uncapped_residual':max(r['uncapped_residual'] for r in records),
    'local_seconds':report['local_seconds']},indent=2))
