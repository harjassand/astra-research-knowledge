#!/usr/bin/env python3
"""Independent rational/interval controls for root's CP lag certificate.

The phase-clock PSD/non-CP conclusions use analytic rational certificates;
the dense matrix exponential is only a separate floating numerical control.
No native observations or preparation are performed.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import time

ROOT = Path(__file__).resolve().parent


def mm(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def exp_minus_interval(x, terms=100):
    assert x >= 0 and terms+2 > x
    term = F(1)
    lower_e = term
    for k in range(1, terms+1):
        term *= x/k
        lower_e += term
    next_term = term*x/(terms+1)
    tail = next_term/(1-x/(terms+2))
    return 1/(lower_e+tail), 1/lower_e


def log_unit_interval(x, terms=48):
    assert 1 <= x <= 2
    z = (x-1)/(x+1)
    lo = 2*sum(z**(2*k+1)/F(2*k+1) for k in range(terms))
    tail = 2*z**(2*terms+1)/(F(2*terms+1)*(1-z*z))
    return lo, lo+tail


def log_interval(x):
    assert x > 0
    if x < 1:
        lo, hi = log_interval(1/x)
        return -hi, -lo
    k = 0
    while x > 2:
        x /= 2
        k += 1
    a, b = log_unit_interval(x)
    l2, u2 = log_unit_interval(F(2))
    return a+k*l2, b+k*u2


def interval_receipt(lo, hi):
    return {'lower':str(lo), 'upper':str(hi),
            'float_lower':float(lo), 'float_upper':float(hi)}


def refresh_check():
    weights = [F(2, 5), F(3, 5)]
    laws = [[F(2, 3), F(1, 3), F(0)], [F(0), F(1, 4), F(3, 4)]]
    states = [(k, a) for k in range(2) for a in range(3) if laws[k][a]]
    mu = [weights[k]*laws[k][a] for k,a in states]
    n = len(states)
    tw = [[laws[k][b] if k == l else F(0) for l,b in states] for k,a in states]
    tg = [mu[:] for _ in states]
    assert mm(tw, tw) == tw and mm(tg, tg) == tg
    assert mm(tw, tg) == tg and mm(tg, tw) == tg
    rate, epsilon, t = F(3, 2), F(1, 7), F(2, 3)
    q = [[rate*(tw[i][j]-F(i==j))+epsilon*(tg[i][j]-F(i==j))
          for j in range(n)] for i in range(n)]
    for i in range(n):
        assert sum(q[i]) == 0
        assert -q[i][i] <= rate+epsilon
        for j in range(n):
            assert mu[i]*q[i][j] == mu[j]*q[j][i]
            if i != j:
                assert q[i][j] > 0
    c = [[sum(weights[k]*laws[k][a]*laws[k][b] for k in range(2))
          for b in range(3)] for a in range(3)]
    p = [sum(row) for row in c]
    ar, br = exp_minus_interval(rate*t)
    ae, be = exp_minus_interval(epsilon*t)
    intervals = []
    tv_hi = F(0)
    for a in range(3):
        row = []
        for b in range(3):
            diag = p[a] if a == b else F(0)
            # All coefficients are nonnegative; independent interval products
            # safely enclose their dependent true values.
            lo = ae*(ar*diag+(1-br)*c[a][b])+(1-be)*p[a]*p[b]
            hi = be*(br*diag+(1-ar)*c[a][b])+(1-ae)*p[a]*p[b]
            tv_hi += max(abs(lo-c[a][b]), abs(hi-c[a][b]))/2
            row.append([str(lo),str(hi)])
        intervals.append(row)
    assert tv_hi < ar+epsilon*t
    import numpy as np
    from scipy.linalg import expm
    qf=np.array(q,float); ef=np.zeros((n,3))
    for i,(_,a) in enumerate(states): ef[i,a]=1
    actual=ef.T@np.diag(np.array(mu,float))@expm(float(t)*qf)@ef
    formula=math.exp(-float(epsilon*t))*(math.exp(-float(rate*t))*np.diag(np.array(p,float))
              +(1-math.exp(-float(rate*t)))*np.array(c,float))
    formula+=(1-math.exp(-float(epsilon*t)))*np.outer(np.array(p,float),np.array(p,float))
    assert np.max(abs(actual-formula)) < 1e-13
    return {'states':states,'mu':[str(x) for x in mu],
            'generator':[[str(x) for x in row] for row in q],
            'supplied_CP_matrix':[[str(x) for x in row] for row in c],
            'commuting_projection_and_balance_checks':'EXACT PASS',
            'lag_formula_intervals':intervals,
            'TV_interval_upper':str(tv_hi),
            'TV_bound_lower':str(ar+epsilon*t),
            'dense_exponential_float_max_error':float(np.max(abs(actual-formula)))}


def phase_clock_check():
    n=20; a=F(n); b=F(1,1000); t=F(11,20)
    count=5*n
    def idx(pos,phase): return pos*n+phase
    q=[[F(0) for _ in range(count)] for _ in range(count)]
    for pos in range(5):
        for phase in range(n):
            i=idx(pos,phase)
            if phase+1<n: q[i][idx(pos,phase+1)]+=a
            else:
                for step in [-1,1]: q[i][idx((pos+step)%5,0)]+=a/2
            if phase>0: q[i][idx(pos,phase-1)]+=b
            else:
                for step in [-1,1]: q[i][idx((pos+step)%5,n-1)]+=b/2
            q[i][i]=-(a+b)
    reflection=[idx(pos,n-1-phase) for pos in range(5) for phase in range(n)]
    for i in range(count):
        assert sum(q[i])==0
        assert sum(q[j][i] for j in range(count))==0
        assert reflection[i]//n == i//n
        for j in range(count):
            assert q[reflection[i]][reflection[j]]==q[j][i]
            if i!=j:
                assert q[i][j]>=0
                assert (q[i][j]>0)==(q[j][i]>0)
    # All states reach all others: direct graph search, no numeric inference.
    reached={0}; todo=[0]
    while todo:
        i=todo.pop()
        for j in range(count):
            if i!=j and q[i][j] and j not in reached:
                reached.add(j); todo.append(j)
    assert len(reached)==count
    # Forward-only clock: E W=t and visible Fourier eigenvalue E c^W
    # >=1-(1-c)t. Reverse-clock insertion changes it by at most2bt.
    scale=10**12; root=math.isqrt(5*scale*scale)
    sqrt5_lo=F(root,scale); sqrt5_hi=F(root+1,scale)
    assert sqrt5_lo**2 <= 5 < sqrt5_hi**2
    transition_eigen_lower=1-t*(5+sqrt5_hi)/4-2*b*t
    joint_eigen_lower=transition_eigen_lower/5
    assert joint_eigen_lower>0
    # A forward-only visible neighbor is certain if exactly one phase wrap
    # occurs. E[W;W>=2] <= t P(Pois(nt)>=n-1).
    lam=a*t
    _, exp_hi=exp_minus_interval(lam)
    tail_hi=exp_hi*lam**(n-1)/math.factorial(n-1)/(1-lam/n)
    assert tail_hi < 1
    neighbor_lower=t*(1-tail_hi)-b*t
    gamma_lower=2*neighbor_lower-1
    assert gamma_lower>0
    sigma_lower,sigma_upper=log_interval(a/b)
    sigma_lower*=a-b; sigma_upper*=a-b
    # Non-CP witness bound is rigorously below actual entropy rate.
    witness_rate_lower=4*gamma_lower/t
    assert witness_rate_lower < sigma_lower
    import numpy as np
    from scipy.linalg import expm
    ef=np.zeros((count,5))
    for i in range(count):ef[i,i//n]=1
    c=ef.T@expm(float(t)*np.array(q,float))@ef/count
    horn=np.ones((5,5))
    for i in range(5):
        horn[i,(i+1)%5]=-1; horn[i,(i-1)%5]=-1
    gamma_float=-float(np.sum(c*horn))
    eigen_float=np.linalg.eigvalsh((c+c.T)/2)
    assert gamma_float>float(gamma_lower)
    assert min(eigen_float)>float(joint_eigen_lower)
    assert np.max(abs(c-c.T)) < 1e-13
    return {'n_phase':n,'hidden_states':count,'forward_rate':str(a),'reverse_rate':str(b),
            'lag':str(t),'departure_rate':str(a+b),'stationary_law':'uniform on100 states',
            'exact_checks':['row and column balance','reciprocal support','irreducibility',
                            'phase reflection conjugates Q to Q transpose','reflection fixes visible label'],
            'rigorous_Poisson_tail_upper':str(tail_hi),'float_tail_upper':float(tail_hi),
            'rigorous_visible_joint_eigen_lower':str(joint_eigen_lower),
            'float_joint_eigen_lower':float(joint_eigen_lower),
            'rigorous_Horn_gap_lower':str(gamma_lower),'float_Horn_gap_lower':float(gamma_lower),
            'rigorous_witness_entropy_rate_lower':str(witness_rate_lower),
            'float_witness_entropy_rate_lower':float(witness_rate_lower),
            'actual_entropy_rate_interval':interval_receipt(sigma_lower,sigma_upper),
            'floating_control_only':{'joint':c.tolist(),'eigenvalues':eigen_float.tolist(),
                                     'Horn_gap':gamma_float,'symmetry_error':float(np.max(abs(c-c.T)))},
            'no_physical_time_reversal_identification':'all-even reversal is a stated model premise'}


def scalar_path_bounds():
    rows=[]
    for h in [F(1,100),F(1,10),F(1,2),F(2)]:
        a=(1+h)**2; b=F(1); kill=(a+b)-2*(1+h)
        assert kill==h*h
        lo,hi=log_interval(a/b)
        rate_lo=(a-b)*lo
        for t in [F(1,100),F(1,10),F(1),F(10)]:
            affinity_lo,affinity_hi=exp_minus_interval(kill*t)
            assert rate_lo*t >= 4*(1-affinity_lo)
            assert rate_lo*t >= 2*kill*t
            rows.append({'h':str(h),'t':str(t),'KL_lower':str(rate_lo*t),
                         'four_deficit_upper':str(4*(1-affinity_lo)),
                         'log_affinity_bound_exact':str(2*kill*t)})
    return rows


def main():
    started=time.perf_counter()
    r={'scope':'supplied finite CTMC proof controls; no acquisition',
       'native_observations':0,'native_preparations':0,
       'CP_closure':refresh_check(), 'phase_clock':phase_clock_check(),
       'scalar_path_inequalities':scalar_path_bounds(),
       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'elapsed_seconds':time.perf_counter()-started}
    (ROOT/'COPOSITIVE_LAG_INDEPENDENT_CHECKS.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'CP_closure':r['CP_closure']['commuting_projection_and_balance_checks'],
      'phase_states':r['phase_clock']['hidden_states'],
      'joint_eigen_lower':r['phase_clock']['float_joint_eigen_lower'],
      'Horn_gap_lower':r['phase_clock']['float_Horn_gap_lower'],
      'witness_rate_lower':r['phase_clock']['float_witness_entropy_rate_lower'],
      'float_check':r['phase_clock']['floating_control_only'],
      'scalar_checks':len(r['scalar_path_inequalities']),
      'elapsed_seconds':r['elapsed_seconds']},indent=2))


if __name__=='__main__': main()
