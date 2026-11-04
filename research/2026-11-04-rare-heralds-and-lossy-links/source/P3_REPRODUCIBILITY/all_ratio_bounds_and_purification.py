"""Evaluate proved analytic bounds; this is not an interval proof of all parameters."""
import math
import json
from collections import Counter

S, Q = 0.2, 0.5
R_BOUND = S/2 + math.expm1(0.001)*(1+1/(2*S)) + 0.04*math.exp(0.001)
Z_BOUND = 0.02
SUCCESS_FACTOR = (1-Z_BOUND)**2
FIDELITY_BOUND = SUCCESS_FACTOR/(SUCCESS_FACTOR+(math.sqrt(R_BOUND)+Z_BOUND)**2)

def entropy2(e):
    return -e*math.log2(e)-(1-e)*math.log2(1-e)

def source_bounds(rho, eta=1.0, gamma=1.0):
    if not (rho > 0 and 0 < eta <= 1 and gamma > 0):
        raise ValueError('rho, gamma must be positive, and 0 < eta <= 1')
    mu = min(0.001, 1/rho)
    theta = rho*mu
    T = mu/gamma
    N = math.ceil(5+2*max(0, -math.log(rho))/math.log(1000))
    D_lower = theta*theta/24
    p0_lower = math.exp(-mu)*S*Q*eta*mu*D_lower
    log_ratio = (N-1)*math.log(eta)+N*math.log(mu)-math.lgamma(N+1)
    log_ratio -= -mu+math.log(S*Q*mu*D_lower)
    assert log_ratio <= math.log(1e-4)+1e-10
    y = 1-entropy2(1-FIDELITY_BOUND)-(1-FIDELITY_BOUND)*math.log2(3)
    return dict(rho=rho, eta=eta, gamma=gamma, mu=mu, T=T, theta=theta,
        receiver_dimension=N, mode_contrast_lower=D_lower,
        scalar_coupling_amplitude_bound=8/math.sqrt(T),
        scalar_coupling_slew_bound=270/T**1.5,
        photon_tail_to_p0_bound=math.exp(log_ratio), good_Bell_weight_lower=p0_lower,
        raw_success_lower=SUCCESS_FACTOR*p0_lower, raw_fidelity_lower=FIDELITY_BOUND,
        Q2_lower_per_window=SUCCESS_FACTOR*p0_lower*y,
        Q2_upper_per_window=min(1, math.log2(1+6*(-math.expm1(-eta*mu)))))

def purification_step(e):
    u, x = 1-e, e/3
    accepted = u**5+30*x**3*u*u+15*x**4*u+18*x**5
    return (30*x**3*u*u+18*x**5)/accepted, accepted

def purification_budget(e, levels, raw_success):
    pairs = 1.0
    out = []
    for k in range(1, levels+1):
        e, a = purification_step(e)
        pairs *= 5/a
        out.append(dict(level=k, Bell_error_bound=e, block_acceptance=a,
            expected_raw_accepted_pairs=pairs, expected_source_windows=pairs/raw_success))
    return out

def code_enumerators():
    def pauli(word):
        x=z=0
        for k, a in enumerate(word):
            if a in 'XY': x |= 1 << k
            if a in 'ZY': z |= 1 << k
        return x, z
    generators = list(map(pauli, ['XZZXI','IXZZX','XIXZZ','ZXIXZ']))
    stabilizer = set()
    for mask in range(16):
        x=z=0
        for k, (gx,gz) in enumerate(generators):
            if mask >> k & 1: x ^= gx; z ^= gz
        stabilizer.add((x,z))
    normalizer = set()
    for x in range(32):
        for z in range(32):
            if all(((x&gz).bit_count()+(z&gx).bit_count()) % 2 == 0 for gx,gz in generators):
                normalizer.add((x,z))
    weight = lambda points: dict(sorted(Counter((x|z).bit_count() for x,z in points).items()))
    result = dict(stabilizer=weight(stabilizer), normalizer=weight(normalizer),
                  logical_nonidentity=weight(normalizer-stabilizer))
    assert result['stabilizer'] == {0:1,4:15}
    assert result['normalizer'] == {0:1,3:30,4:15,5:18}
    return result

if __name__ == '__main__':
    print(json.dumps(dict(error_ratio=R_BOUND, success_factor=SUCCESS_FACTOR,
                         fidelity=FIDELITY_BOUND, code=code_enumerators())))
    for rho in [1e-12,1e-6,0.01,1.0,100.0,1e6]:
        print(json.dumps(source_bounds(rho,eta=0.01)))
    print(json.dumps(dict(finite_cavity_purification=purification_budget(
        1-0.8942083147562617, 3, 5.000022157216882e-6))))
