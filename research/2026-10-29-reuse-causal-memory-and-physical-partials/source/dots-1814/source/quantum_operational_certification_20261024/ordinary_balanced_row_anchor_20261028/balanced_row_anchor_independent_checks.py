"""Independent finite checks for the frozen balanced-anchor acquisition theorem.

No source, tomography circuit, or generic SDP solver is executed. The grouped
pilot simulation samples exactly the classical joint law specified in the proof.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'BALANCED_RANK_ONE_ROW_ANCHOR_ACQUISITION.md'
FROZEN = '421f3fdabfaff88e924346795f7d7aa63014549cb335db4b1c884abfdfe97083'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == FROZEN
rng = np.random.default_rng(202610281602)

# The 24 equiprobable slots, not a sampled approximation to Haar measure.
slots = []
for j in range(4):
    x = [F(i == j) for i in range(4)]
    slots += [x, x]
for signs in itertools.product([-1, 1], repeat=4):
    slots.append([F(s, 2) for s in signs])
assert len(slots) == 24
moment_checks = 0
for idx in itertools.product(range(4), repeat=2):
    i, j = idx
    assert sum(x[i]*x[j] for x in slots)/24 == F(i == j, 4)
    moment_checks += 1
for i,j,l,t in itertools.product(range(4), repeat=4):
    wanted = F((i == j)*(l == t)+(i == l)*(j == t)+(i == t)*(j == l),24)
    assert sum(x[i]*x[j]*x[l]*x[t] for x in slots)/24 == wanted
    moment_checks += 1

# Exact clipped-ratio checks include zero candidate denominator and sign flips.
def rational_circle(t):
    return (F(1-t*t,1+t*t), F(2*t,1+t*t), F(0), F(0))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
anchor = (F(1), F(0), F(0), F(0))
ratios = 0
clipped = 0
for aparam in [F(j,7) for j in range(-20,21) if abs(j) != 7]:
    u = rational_circle(aparam)
    a = u[0]
    for fraction in [F(1),F(1,2),F(1,100)]:
        kappa = a*a*fraction
        for bparam in [F(j,5) for j in range(-20,21)]:
            v = rational_circle(bparam)
            e = 1-dot(u,v)**2
            b = v[0]
            if b*b >= kappa/4:
                s = tuple(z/b for z in v)
            else:
                s = anchor
                clipped += 1
                assert e >= kappa/8
            true_s = tuple(z/a for z in u)
            difference = sub(s,true_s)
            lhs = a*a*dot(difference,difference)
            assert lhs <= 32*e/kappa
            assert dot(s,anchor) == 1
            assert dot(s,s) <= 4/kappa
            ratios += 1

# Count and perturbation constants, checked independently of any random records.
assert F(1,3)-math.sqrt(3)/8 > F(1,12)
max_t = math.sqrt(3)/16
bernstein_exponent_multiple = 3/(2*(F(1,4)+max_t/3))
assert bernstein_exponent_multiple > 1
vector_bound_constant = (math.sqrt(3)/(1/3-max_t)+.01)**2
assert vector_bound_constant < 256
assert 9/64 < 1  # d*(8e^-L+e^-L), with e^-L <= beta/(64d).
count_envelopes = 0
L = 19
N = 10**9
for mu in [F(0), F(1,100), F(8*L)-F(1,100), F(8*L), F(512*L), F(10**6)]:
    lam = 4*mu/N
    if mu < 8*L:
        assert lam <= F(32*L,N)
    else:
        for n in [math.ceil(mu/2), math.ceil(mu), math.ceil(2*mu)]:
            e = F(1) if n <= 256*L else min(F(1),F(256*L,n))
            assert lam*e <= F(2048*L,N)
            count_envelopes += 1

# Realized-count simulation using aggregate multinomials. There are zero rows,
# repeated directions, and masses down to about 5e-13; no expected-count shortcut.
H = np.array([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]],float)/2
base = np.vstack([np.eye(4),H])
split = np.array([1,1e-1,1e-2,1e-4,1e-6,1e-9,1e-12,0.0])
split /= split.sum()
us = np.repeat(base,len(split),axis=0)
lam = np.tile(split,len(base))/2
d = len(lam)
x0 = np.array([1,2,2,4],float)/5
kappa = .01
assert np.linalg.norm(np.einsum('i,ij,ik->jk',lam,us,us)-np.eye(4)) < 1e-14
assert abs(lam.sum()-4) < 1e-14
assert np.min((us@x0)**2) >= kappa-1e-14
X = np.array(slots,float)
conditional = (X@us.T)**2/6
assert np.max(abs(conditional.sum(axis=0)-1)) < 1e-14
trials = 120
max_weighted_ratio = 0.0
max_uniform_ratio = 0.0
missing_nonzero = 0
high_count_rows = 0
for trial in range(trials):
    counts = rng.multinomial(N,lam/4)
    estimated = []
    errors = []
    for i,n in enumerate(counts):
        if n <= 256*L:
            estimated.append(x0)
            errors.append(1.0)
            missing_nonzero += int(n == 0 and lam[i] > 0)
            continue
        high_count_rows += 1
        records = rng.multinomial(n,conditional[:,i])
        M = np.einsum('i,ij,ik->jk',records,X,X)/n
        vals,vecs = np.linalg.eigh(M)
        assert vals[-1]-vals[-2] >= 1/12
        v = vecs[:,-1]
        err = max(0.0,1-(v@us[i])**2)
        assert err <= 256*L/n
        errors.append(err)
        b = v@x0
        estimated.append(v/b if b*b >= kappa/4 else x0)
    errors = np.array(errors)
    estimated = np.array(estimated)
    weighted = lam@errors
    max_weighted_ratio = max(max_weighted_ratio,weighted/(4096*d*L/N))
    assert weighted <= 4096*d*L/N
    true_s = us/(us@x0)[:,None]
    w = lam*(us@x0)**2
    row_norm = np.einsum('i,ij,ij->',w,estimated-true_s,estimated-true_s)
    assert row_norm <= 32*weighted/kappa + 1e-12
    max_uniform_ratio = max(max_uniform_ratio,row_norm/(2**17*d*L/(kappa*N)))
assert missing_nonzero > 0 and high_count_rows > 0

# Physical nonzero-comparator fixture: E_x = W_x o dephase_p, p=1/5.
# W_x is an actual known-control family of output isometries. Its receiver rows
# use the coordinate/Hadamard directions above. Exact primal/dual certificates
# give full-CPTP optimum Bell loss p, whereas measuring the output row gives 1/2.
HH = sp.Matrix([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])/2
I2 = sp.eye(2)
P0 = sp.diag(1,0)
phase = sp.diag(1,-1)
p = sp.Rational(1,5)
def vec(M): return sp.Matrix([M[i,j] for i in range(M.rows) for j in range(M.cols)])
def make_W(x):
    z = HH*x
    return sp.Matrix([[x[s] if l == 0 and a == 0 else z[s] if l == 1 and a == 1 else 0
                       for a in range(2)] for s in range(4) for l in range(2)])
def make_T(W):
    w,z = vec(W),vec(W*phase)
    J = ((1-p)*w*w.T+p*z*z.T)/2
    return (sp.kronecker_product(W*W.T,I2)-J)/3,J
x0s = sp.Matrix([1,2,2,4])/5
T0,_ = make_T(make_W(x0s))
physical_cases = 0
min_dual_slack = 1.0
for x in [x0s,sp.Matrix([1,0,0,0]),sp.Matrix([1,1,1,1])/2,sp.Matrix([2,1,-2,4])/5]:
    W = make_W(x)
    assert W.T*W == I2
    T,J = make_T(W)
    w = vec(W)
    C = w*w.T+sp.kronecker_product(sp.eye(8)-W*W.T,P0)
    for i,j in itertools.product(range(8),repeat=2):
        assert sum(C[2*i+a,2*j+a] for a in range(2)) == int(i == j)
    ell = sp.Rational(3,2)*sp.trace(C.T*T)
    Y = (1-p)*W*W.T/2
    slack = sp.kronecker_product(Y,I2)-J.T/2
    assert ell == p
    assert sp.trace(Y) == 1-p
    bell_minus = sp.Matrix([1,0,0,-1])
    logical_slack = (1-2*p)*bell_minus*bell_minus.T/4+(1-p)*sp.diag(0,1,1,0)/2
    embed = sp.kronecker_product(W,I2)
    assert slack == embed*logical_slack*embed.T  # Exact nonnegative sum of squares.
    min_dual_slack = min(min_dual_slack,float(np.linalg.eigvalsh(np.array(slack,float)).min()))
    assert min_dual_slack > -1e-13
    ss = [sp.eye(4)[s,:] if l == 0 else HH[s,:] for s in range(4) for l in range(2) for a in range(2)]
    rr = [(u*x)[0]/(u*x0s)[0] for u in ss]
    RR = sp.diag(*rr)
    assert T == RR*T0*RR
    measured = sp.diag(*[J[i,i] for i in range(16)])
    Cmeasure = sp.diag(*[int(a == (b % 2)) for b in range(8) for a in range(2)])
    assert 1-sp.trace(Cmeasure.T*measured)/2 == sp.Rational(1,2)
    assert T.trace() == 1
    assert T.rank() <= 6
    physical_cases += 1

# Exact chosen budgets and nonzero-comparator scalar risk transfer.
budget_checks = 0
nonzero_comparator_checks = 0
for gamma,eps,kap,dim in itertools.product([F(1),F(1,7),F(1,101)], [F(1),F(1,13),F(1,1000)], [F(1,4),F(1,10000)], [4,16,64]):
    raw = 2**32*dim*L/(kap*gamma*eps)
    NN = math.ceil(raw)
    E = F(2**17*dim*L,1)/(kap*NN)
    m = kap*gamma*eps/2**20
    assert 6*E+48*m/kap <= gamma*eps/4096
    assert F(27,4096)+F(1,128) < F(1,64)
    assert 2*F(1,64)+F(1,2) < 1
    for optimum in [F(0),F(1,10000),F(1,5),F(1,2),F(3,4)]:
        risk = (math.sqrt(float(optimum))+3*math.sqrt(float(gamma*eps/4096)))**2
        rhs = float((1+gamma/2)*optimum+F(27,4096)*eps)
        assert risk <= rhs+1e-13
        nonzero_comparator_checks += int(optimum > 0)
    budget_checks += 1

out = {
    'status':'PASS independent algebra, statistics, physical comparator, and budget checks',
    'source_sha256':FROZEN,
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'exact_design_moment_checks':moment_checks,
    'exact_clipped_ratio_checks':ratios,
    'exact_fallback_cases':clipped,
    'count_envelope_cases':count_envelopes,
    'conditional_bernstein_exponent_at_threshold_in_L':bernstein_exponent_multiple,
    'finite_vector_error_coefficient_bound':vector_bound_constant,
    'aggregate_pilot_trials':trials,
    'simulated_raw_calls_per_trial':N,
    'nonzero_missing_rows_over_trials':missing_nonzero,
    'observed_high_count_rows_over_trials':high_count_rows,
    'maximum_weighted_error_divided_by_claimed_bound':max_weighted_ratio,
    'maximum_row_norm_error_divided_by_claimed_bound':max_uniform_ratio,
    'exact_nonzero_optimum_physical_primal_dual_fixtures':physical_cases,
    'physical_optimal_bell_loss':'1/5',
    'physical_coordinate_measuring_bell_loss':'1/2',
    'minimum_numerical_dual_slack_eigenvalue':min_dual_slack,
    'exact_budget_cases':budget_checks,
    'nonzero_comparator_scalar_checks':nonzero_comparator_checks,
    'actual_source_calls':0,
    'limits':['No imported quantum tomography circuit or gate compiler was re-audited or executed.',
              'Aggregate pilots simulate the exact classical law, not quantum acquisition hardware.',
              'Physical fixtures use explicit certificates, not a generic SDP implementation.',
              'No test certifies rank-one structure or the supplied calibrated anchor from noisy data.']
}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
