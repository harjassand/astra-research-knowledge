"""Small diagnostics for c09_s02; proofs are in INITIAL.txt, not in this file.

No dependencies. Gaussian curve rank checks are floating diagnostics.
The truncated exponential quantities are explicit closed-form evaluations.
"""
import json
import math
import time
from pathlib import Path


def curve(q, theta):
    scale = 1 / math.sqrt(sum(k*k for k in range(1, q+1)))
    return [z for k in range(1, q+1)
            for z in (scale*math.cos(k*theta), scale*math.sin(k*theta))]


def det(matrix):
    a = [row[:] for row in matrix]
    value = 1.0
    for i in range(len(a)):
        pivot = max(range(i, len(a)), key=lambda j: abs(a[j][i]))
        if not a[pivot][i]:
            return 0.0
        if pivot != i:
            a[pivot], a[i] = a[i], a[pivot]
            value = -value
        p = a[i][i]
        value *= p
        for j in range(i+1, len(a)):
            r = a[j][i]/p
            for k in range(i+1, len(a)):
                a[j][k] -= r*a[i][k]
    return value


def entropy_binary(delta):
    return -delta*math.log(delta) - (1-delta)*math.log1p(-delta)


def exp_record(R):
    Z = -math.expm1(-R)
    e = math.exp(-R)
    variance = 1-R*R*e/(Z*Z)
    poincare = 1/(0.25 + (math.pi/R)**2)
    uniform_kl = R/2+math.log(Z)-math.log(R)
    delta = R**-0.5
    mixed_kl_lower = delta*uniform_kl-entropy_binary(delta)
    mixed_energy_upper = delta/4
    affinity = 2*(1-math.exp(-R/2))/math.sqrt(R*Z)
    lmax = 1-delta+delta*Z*math.exp(R)/R
    p = 1/(2*lmax)
    return dict(R=R, covariance=variance, poincare=poincare,
                uniform_kl=uniform_kl, uniform_sqrt_energy=0.25,
                uniform_affinity=affinity, delta=delta,
                mixed_kl_lower=mixed_kl_lower,
                mixed_sqrt_energy_upper=mixed_energy_upper,
                mixed_tv_upper=delta, mixed_H2_upper=2*delta,
                binary_event_probability=p,
                binary_information_lower=p*mixed_kl_lower,
                binary_average_sqrt_energy_upper=p*delta/2,
                binary_I_over_P_energy_lower=2*(uniform_kl-entropy_binary(delta)/delta)/poincare)


def main():
    start = time.perf_counter()
    ranks = []
    for q in range(1, 7):
        d = 2*q
        means = [curve(q, j/d) for j in range(d+1)]
        a = [[x-y for x,y in zip(row, means[0])] for row in means[1:]]
        determinant = det(a)
        speed_residual = max(abs(sum((k/math.sqrt(sum(j*j for j in range(1,q+1))))**2
                                       *(math.sin(k*t)**2+math.cos(k*t)**2)
                                       for k in range(1,q+1))-1)
                             for t in (0,0.125,0.5,1))
        assert speed_residual < 1e-14
        assert determinant != 0.0
        ranks.append(dict(q=q, ambient_dimension=d, fisher_residual=speed_residual,
                          affine_determinant=determinant,
                          curve_memory_prelog=q, line_memory_prelog=0.5,
                          scope='Floating diagnostic; exact rank follows from polynomial root count.'))
    exponentials = [exp_record(R) for R in (8,16,32,64,128,256)]
    for r in exponentials:
        # The strictly positive exact correction can round away at large R.
        assert 0 < r['covariance'] <= 1
        assert 0 < r['poincare'] < 4
        assert r['mixed_kl_lower'] > 0
        assert abs(r['binary_event_probability']* (1-r['delta']+r['delta']*(-math.expm1(-r['R']))*math.exp(r['R'])/r['R']) - 0.5) < 1e-14
    result = dict(status='PASS', curve_fixtures=ranks,
                  truncated_exponential_fixtures=exponentials,
                  elapsed_seconds=time.perf_counter()-start,
                  limitations=['No physical quantum-memory execution.',
                               'No certified Gaussian CDF/inverse-CDF compiler.',
                               'No numerical value certifies asymptotic proof or novelty.',
                               'Binary-channel obstruction is not the special N75 Gaussian covariance channel.'])
    out = Path(__file__).with_name('analytic_checks.json')
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status':result['status'],'curve_fixtures':len(ranks),
                      'exponential_fixtures':len(exponentials),
                      'seconds':result['elapsed_seconds'],'output':str(out)}))


if __name__ == '__main__':
    main()
