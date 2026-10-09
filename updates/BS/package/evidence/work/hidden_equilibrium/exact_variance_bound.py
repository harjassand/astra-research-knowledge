"""Exact rational coefficient checks and conservative finite-sample power bound.

The probability reasoning is in RESULT.md. This checks only finite arithmetic;
the inherited universal mean inequality remains a source-dependent premise.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parent

def matrix(x):
    return [[F(a) for a in row] for row in x]

def mul(A,z):
    return [sum(a*b for a,b in zip(row,z)) for row in A]

def sq(v):
    return sum(x*x for x in v)

def run():
    seed=json.loads((ROOT/'certificate.txt').read_text())
    wit=json.loads((ROOT/'witness.txt').read_text())
    Q=matrix(seed['Q']); C=matrix(wit['feature_matrix'])
    D=matrix(wit['facet_residual_matrix']); K=matrix(wit['K'])
    h=F(wit['constants']['h']); tau=F(wit['constants']['tau'])
    Lam=F(wit['constants']['Lambda']); Mu=F(wit['constants']['Mu'])
    checks={}
    checks['Q_exit_rate_at_most_one']=all(-Q[i][i]<=1 for i in range(10))
    checks['Q_uniform_stationary']=all(sum(Q[i][j] for i in range(10))==0 for j in range(10))
    checks['Q_rows_zero']=all(sum(row)==0 for row in Q)
    checks['Q_offdiagonal_nonnegative']=all(Q[i][j]>=0 for i in range(10) for j in range(10) if i!=j)
    checks['K_Frobenius_squared_below_nine']=sum(sq(row) for row in K)<9
    checks['quadratic_coefficients_below_one_tenth']=all(abs(F(a))<F(1,10) for a in wit['quadratic_coefficients'])
    for c in range(6):
        for f in range(6):
            z=[F(0) for _ in range(11)]
            z[0]=F(c==0)
            if c==0 and f>0:z[f]=F(1)
            if c>0:z[c+5]=F(1)
            fv,dv=mul(C,z),mul(D,z)
            event=(c==0 and f>0)
            checks[f'F_squared_{c}_{f}']=sq(fv)<=(100/h**2 if event else 3)
            checks[f'D_squared_{c}_{f}']=sq(dv)<=(1 if event else h**2)
    if not all(checks.values()):
        raise AssertionError([k for k,v in checks.items() if not v])
    # Target conditional second-moment estimates, for both Q and Q*:
    f2=F(103)/h
    d2=h+h*h
    g2=20*f2
    # Minkowski L2 bound for the entire raw observable W.
    # ||Sq||_2 <= 41/h follows from coefficient bounds and h<=1.
    bound=(41/h+72*(1+f2)+(45000*h+tau)*(1+f2)+tau+Lam*d2+Mu*g2)
    variance_bound=bound*bound
    n=2*10**64; alpha=0.05; eta=0.025; delta=1e-6
    range_bound=1.2e40
    lp=math.log(1/eta); ls=math.log(2/alpha)
    v=float(variance_bound)
    deviation=math.sqrt(2*v*lp/n)+range_bound*lp/(3*n)
    sample_sd_bound=math.sqrt(v)+range_bound*math.sqrt(2*lp/(n-1))
    radius=math.sqrt(2*ls/n)*sample_sd_bound+7*range_bound*ls/(3*(n-1))
    # The final decimal check is a numerical convenience; proof uses log(40)<4
    # and the exact rational inequalities v<4.105e50, range<=1.2e40.
    checks['rational_variance_bound_below_4_105e50']=variance_bound<F(4105)*10**47
    checks['chosen_n_exact']=n==2*10**64
    assert all(checks.values()), [k for k,v in checks.items() if not v]
    results={
      'status':'EXACT_FINITE_COEFFICIENT_CHECKS_PLUS_ANALYTIC_BOUND',
      'all_checks_pass':all(checks.values()),'checks':checks,
      'L2_bound_decimal':str(float(bound)),
      'variance_upper_bound_decimal':str(v),
      'variance_upper_bound_simple':'4.105e50',
      'iid_stationary_windows':n,'null_type_I_error_at_most':alpha,
      'target_power_at_least':1-2*eta,
      'raw_gap_inherited_from_source':delta,
      'source_range_bound':'1.2e40',
      'power_budget_left_side_numerical':deviation+radius,
      'proof_note':'Use log(40)<4: square-root total <8.105e-7; all range/n terms <1e-22; sum<1e-6.',
      'limitations':['Requires inherited universal witness inequality and target gap.',
                    'No external proof verification.',
                    'Independent stationary windows and 1e-12 resolution required.',
                    'The enormous sample budget is not practical and is not a lower bound.']
    }
    (ROOT/'exact_variance_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k!='checks'},indent=2))

if __name__=='__main__':run()
