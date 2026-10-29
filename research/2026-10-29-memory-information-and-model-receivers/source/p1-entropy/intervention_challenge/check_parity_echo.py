#!/usr/bin/env python3
"""Exact algebra and analytic CTMC certificate for the parity echo.

The non-CP echo is certified by a closed-form no-flip CTMC and a coupling
bound, not by trusting a matrix exponential. No native pulse is executed.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math

from check_copositive_lag import mm, exp_minus_interval, log_interval

HERE = Path(__file__).resolve().parent


def transpose(a):
    return [list(row) for row in zip(*a)]


def zeros(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]


def rounded_receipt(lo, hi, places=20):
    scale = 10**places
    low = F(lo.numerator*scale//lo.denominator, scale)
    high = F(-((-hi.numerator*scale)//hi.denominator), scale)
    assert low <= lo <= hi <= high
    return {'lower':str(low),'upper':str(high),
            'decimal_lower':float(low),'decimal_upper':float(high)}


def path_factor(q, pi, halves):
    """Return prefactor and exponent for a marked-pulse path density."""
    first = halves[0][0][0]
    prefactor, exponent = pi[first], F(0)
    for half in halves:
        for x, duration in half:
            exponent += q[x][x]*duration
        for (x,_),(y,_) in zip(half,half[1:]):
            prefactor *= q[x][y]
    return prefactor, exponent


def exact_control():
    a, b, c = F(1), F(1,100), F(1,100000)
    h, t = F(12,5), F(24,5)
    n = 6
    q, theta, e = zeros(n), zeros(n), zeros(n,3)
    reflect = [i ^ 1 for i in range(n)]
    for pos in range(3):
        for velocity in range(2):
            x = 2*pos+velocity
            theta[x][reflect[x]] = 1
            e[x][pos] = 1
            step = 1 if velocity == 0 else -1
            q[x][2*((pos+step)%3)+velocity] = a if velocity == 0 else b
            q[x][reflect[x]] = c
            q[x][x] = -sum(q[x])
    pi = [F(1,n)]*n
    r = mm(mm(theta,transpose(q)),theta)
    s = zeros(n)
    for i in range(n):
        assert sum(q[i]) == 0
        assert sum(q[j][i] for j in range(n)) == 0
        for j in range(n):
            if i == j:
                s[i][j] = (q[i][i]+r[i][i])/2
            elif j == reflect[i]:
                s[i][j] = c
            elif q[i][j]:
                s[i][j] = F(1,10)
            assert i == j or s[i][j]**2 == q[i][j]*r[i][j]
    assert mm(theta,e) == e
    assert transpose(s) == mm(mm(theta,s),theta)
    assert any(q[i][i] != r[i][i] for i in range(n))
    assert all(sum(row) == -F(81,200) for row in s)
    reached, todo = {0}, [0]
    while todo:
        x = todo.pop()
        for y in range(n):
            if x != y and q[x][y] and y not in reached:
                reached.add(y); todo.append(y)
    assert len(reached) == n

    # A marked-pulse path and its physical reversal: holding exponents,
    # jump products, and midpoint pulse compatibility all check exactly.
    duration = h/3
    halves = [[(0,duration),(2,duration),(3,duration)],
              [(2,duration),(4,duration),(5,duration)]]
    reversed_halves = [[(reflect[x],d) for x,d in reversed(half)]
                       for half in reversed(halves)]
    assert halves[1][0][0] == reflect[halves[0][-1][0]]
    assert reversed_halves[1][0][0] == reflect[reversed_halves[0][-1][0]]
    assert path_factor(q,pi,reversed_halves) == path_factor(r,pi,halves)
    pq, eq = path_factor(q,pi,halves)
    pr, er = path_factor(r,pi,halves)
    ps, es = path_factor(s,pi,halves)
    assert ps*ps == pq*pr and 2*es == eq+er

    # At c=0, the visible echo has the exact Fourier eigenvalue
    # exp(-A)*exp(i B), A=909/250, B=(297/250)*sqrt(3).
    # H=zz^T, z=(1,-1,0), gives gamma0=-(2/3)exp(-A)cos(B).
    exponent = F(3,2)*(a+b)*h
    angle_factor = (a-b)*h/2
    assert exponent == F(909,250) < 4
    assert angle_factor == F(297,250)
    assert (2/angle_factor)**2 < 3 < (3/angle_factor)**2
    # Thus 2<B<3<pi. The alternating cosine series gives this upper bound.
    cosine_upper_at_two = sum((-1)**k*F(2)**(2*k)/math.factorial(2*k) for k in range(5))
    assert cosine_upper_at_two == -F(131,315)
    # e < sum_{k=0}^4 1/k! + (1/5!)/(1-1/6) < 68/25,
    # and (68/25)^4<55. Hence exp(-A)>1/55.
    e_upper = sum(F(1,math.factorial(k)) for k in range(5))+F(1,120)/(1-F(1,6))
    assert e_upper == F(1631,600) < F(68,25)
    assert F(68,25)**4 < 55
    gamma_zero_lower = F(2,3)*F(1,55)*F(131,315)
    assert gamma_zero_lower == F(262,51975)
    # Internal velocity flips have constant rate c. Couple to c=0 until
    # the first flip: endpoint TV <=1-exp(-ct)<=ct. Score oscillation=2.
    gamma_lower = gamma_zero_lower-2*c*t
    assert gamma_lower == F(321263,64968750) > 0

    log_lo, log_hi = log_interval(a/b)
    sigma_lo, sigma_hi = (a-b)*log_lo/2, (a-b)*log_hi/2
    affinity_lo, affinity_hi = exp_minus_interval(F(81,200)*t)
    assert sigma_lo*t > 4*(1-affinity_lo)
    assert sigma_lo > 4*gamma_lower/t

    eta, eps0, eps1 = F(1,1000), F(1,10000), F(1,10000)
    reset = [[F(j == 0) for j in range(n)] for _ in range(n)]
    kick = [[(1-eta)*theta[i][j]+eta*reset[i][j] for j in range(n)] for i in range(n)]
    row_errors = [sum(abs(kick[i][j]-theta[i][j]) for j in range(n))/2 for i in range(n)]
    assert max(row_errors) == eta
    average_error = sum(pi[i]*row_errors[i] for i in range(n))
    assert average_error == eta*F(5,6)
    assert [sum(pi[i]*kick[i][j] for i in range(n)) for j in range(n)] != pi
    calibration_budget = eta+eps0+eps1
    assert calibration_budget == F(3,2500)
    # Worst-case measured population gamma loses L*nu, then the robust
    # certificate subtracts a further L*nu; it still stays positive.
    robust_population_margin = gamma_lower-4*calibration_budget
    assert robust_population_margin == F(9413,64968750) > 0

    # An exact generalized-equilibrium control with both speeds equal.
    qeq = [row[:] for row in q]
    for pos in range(3):
        x = 2*pos+1
        qeq[x][2*((pos-1)%3)+1] = a
        qeq[x][x] = -(a+c)
    assert qeq == mm(mm(theta,transpose(qeq)),theta)

    return {
        'states':n,'stationary_distribution':[str(x) for x in pi],
        'generator':[[str(x) for x in row] for row in q],
        'physical_involution':reflect,'even_observation':'position modulo 3',
        'clockwise_plus_rate':str(a),'counterclockwise_minus_rate':str(b),
        'velocity_flip_rate':str(c),'total_free_evolution_time':str(t),
        'exact_stationarity_irreducibility_and_twisted_adjoint':'PASS',
        'unequal_theta_partner_holding_rates':'YES; averaged geometric diagonal required',
        'exact_marked_path_reversal_and_geometric_density':'PASS',
        'generalized_equilibrium_control':'PASS: equal velocity speeds',
        'copositive_witness':'H=zz^T, z=(1,-1,0); h_minus=1, oscillation=2',
        'analytic_echo_gamma_lower':str(gamma_lower),
        'analytic_echo_gamma_lower_decimal':float(gamma_lower),
        'analytic_entropy_rate_certificate':str(4*gamma_lower/t),
        'sigma_Theta':rounded_receipt(sigma_lo,sigma_hi),
        'geometric_echo_affinity':rounded_receipt(affinity_lo,affinity_hi),
        'intrinsic_entropy_vs_four_affinity_deficit':'RATIONAL INTERVAL PASS',
        'kick_uniform_row_TV':str(eta),'kick_stationary_average_TV':str(average_error),
        'combined_pulse_sensor_endpoint_TV_budget':str(calibration_budget),
        'guaranteed_robust_population_score_margin':str(robust_population_margin),
        'guaranteed_robust_population_rate_bound':str(4*robust_population_margin/t),
        'finite_sample_confidence':'Not performed; population theorem/control only.',
        'native_measurements':0,'native_parity_operations':0,
        'matrix_exponential_interval_test':'Not performed; the certificate is analytic.',
        'earlier_completed_float_expm_control':{
            'scope':'Numerical corroboration executed before the brief transport outage, not the certificate.',
            'gamma':0.00821771950791518,
            'symmetric_joint_minimum_eigenvalue':-0.004108859753957614,
            'sigma_Theta':2.2795592420641055}}


def main():
    result = exact_control()
    result['code_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['helper_sha256'] = hashlib.sha256((HERE/'check_copositive_lag.py').read_bytes()).hexdigest()
    (HERE/'PARITY_ECHO_EXACT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ['states','analytic_echo_gamma_lower',
        'analytic_echo_gamma_lower_decimal','sigma_Theta','guaranteed_robust_population_score_margin',
        'exact_marked_path_reversal_and_geometric_density','native_measurements','native_parity_operations']},indent=2))


if __name__ == '__main__':
    main()
