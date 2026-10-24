#!/usr/bin/env python3
"""Finite positive quantum-record recursion: exact arithmetic V2 certificate.

This is a NEW certificate, not a relabeling of the eta=1/2 V1 outputs.
It verifies finite transition primitives and evaluates complete analytic
allowances. It does not execute the millions/billions of actions in a full
certified forecast. Independent uniform random bits remain a supplied input.

Concrete model: two modes, cross Kerr |g|<=1, Pauli-axis hopping ||h||<=1,
kappa=nu=c=1, eta=1. Coordinates are INTERLEAVED (Re z1,Im z1,Re z2,Im z2).
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import comb, factorial, isqrt
from pathlib import Path
import hashlib
import json

BITS = 256
SCALE = 1 << BITS
STATE_BITS = 80
DELTA = F(1, 1 << STATE_BITS)
RADIUS = F(12)
RANDOM_BITS = 128
POISSON_K = 63
POISSON_DEGREE = 65


def ceildiv(a, b):
    assert b > 0
    return -((-a)//b)


@dataclass(frozen=True)
class I:
    lo: int
    hi: int

    def __post_init__(self):
        assert self.lo <= self.hi

    @staticmethod
    def of(x):
        if isinstance(x, I):
            return x
        x = F(x)
        return I(x.numerator*SCALE//x.denominator,
                 ceildiv(x.numerator*SCALE, x.denominator))

    def __add__(self, y):
        y = I.of(y)
        return I(self.lo+y.lo, self.hi+y.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, y):
        return self+-I.of(y)

    def __rsub__(self, y):
        return I.of(y)+-self

    def __mul__(self, y):
        y = I.of(y)
        v = (self.lo*y.lo, self.lo*y.hi,
             self.hi*y.lo, self.hi*y.hi)
        return I(min(v)//SCALE, ceildiv(max(v), SCALE))

    __rmul__ = __mul__

    def reciprocal(self):
        assert self.lo > 0
        return I(SCALE*SCALE//self.hi,
                 ceildiv(SCALE*SCALE, self.lo))

    def __truediv__(self, y):
        return self*I.of(y).reciprocal()

    def sqrt(self):
        assert self.lo >= 0
        a = isqrt(self.lo*SCALE)
        n = self.hi*SCALE
        b = isqrt(n)
        if b*b < n:
            b += 1
        return I(a, b)

    def widen(self, r):
        u = I.of(r).hi
        return I(self.lo-u, self.hi+u)

    def width(self):
        return F(self.hi-self.lo, SCALE)


def sqrt_upper(x, bits=128):
    x = F(x)
    q = 1 << bits
    n = ceildiv(x.numerator*q*q, x.denominator)
    k = isqrt(n)
    if k*k < n:
        k += 1
    out = F(k, q)
    assert out*out >= x
    return out


def dyadic_upper(x, bits=128):
    x = F(x)
    return F(ceildiv(x.numerator*(1 << bits), x.denominator), 1 << bits)


def pack_upper(x):
    z = dyadic_upper(x)
    return {'rational_upper': str(z), 'decimal_upper_display': float(z)}


def sin_cos(t):
    """Degree 17/16 series, exact small rational angle, outward dyadics."""
    t = F(t)
    assert abs(t) <= F(1, 1 << 12)
    x = I.of(t*t)
    co = I.of(F(1, factorial(16)))
    si = I.of(F(1, factorial(17)))
    for k in range(7, -1, -1):
        co = co*x+F((-1)**k, factorial(2*k))
        si = si*x+F((-1)**k, factorial(2*k+1))
    co = co.widen(abs(t)**18/factorial(18))
    si = (si*t).widen(abs(t)**19/factorial(19))
    return si, co


def covariance_root(x, theta, g=F(1)):
    """Stable exact-algebraic 4x4 principal root, interval enclosed."""
    x = tuple(map(F, x))
    a, b, c, d = x
    i1, i2 = a*a+b*b, c*c+d*d
    s = i1+i2
    bound = 2/theta  # eta=kappa=nu=|g|max=1
    chi = min(F(1), bound/s) if s else F(1)
    aa = chi*theta*g
    p, q = a*c-b*d, a*d+b*c
    er = [[F(0), F(0), aa*q/2, -aa*p/2],
          [F(0), F(0), -aa*p/2, -aa*q/2],
          [aa*q/2, -aa*p/2, F(0), F(0)],
          [-aa*p/2, -aa*q/2, F(0), F(0)]]
    e2 = aa*aa*i1*i2/4
    rad = F(1, 4)-e2
    assert rad >= 0
    u = ((I.of(rad).sqrt()+F(1, 2))*F(1, 2)).sqrt()
    assert u.lo >= SCALE//2
    root = [[I.of(er[j][k])/(2*u)+(u if j == k else 0)
             for k in range(4)] for j in range(4)]
    # Exact finite rational checks of the structural square-root identity.
    for j in range(4):
        for k in range(4):
            assert sum(er[j][l]*er[l][k] for l in range(4)) == (e2 if j == k else 0)
    return root, {'S': s, 'chi': chi, 'radicand': rad}


def contractive_round(endpoint):
    """Quantize certified endpoint toward zero, then apply the radius cap."""
    grid = 1 << STATE_BITS
    out = []
    err2 = F(0)
    for y in endpoint:
        lo, hi = F(y.lo, SCALE), F(y.hi, SCALE)
        assert y.width() <= F(1, 1 << 100)
        if lo >= 0:
            v = F((lo*grid).numerator//(lo*grid).denominator, grid)
            assert 0 <= v <= lo
        elif hi <= 0:
            h = hi*grid
            v = F(ceildiv(h.numerator, h.denominator), grid)
            assert hi <= v <= 0
        else:
            v = F(0)
        err2 += max(abs(lo-v), abs(hi-v))**2
        out.append(v)
    assert err2 <= (4*DELTA)**2
    # The radius test is on the ACTUAL rounded candidate, at EVERY attempt.
    reset = sum(y*y for y in out) > RADIUS*RADIUS
    return (tuple(F(0) for _ in out) if reset else tuple(out)), {
        'reset_on_rounded_candidate': reset,
        'width_upper': max(y.width() for y in endpoint),
        'endpoint_squared_error_upper_before_reset': err2,
    }


def endpoints(x, theta, exponent=20, g=F(1), hopping_axis='x', hopping_sign=1):
    """Eleven internal transitions, each evaluated in outward intervals."""
    x = tuple(map(F, x))
    assert sum(y*y for y in x) <= RADIUS*RADIUS
    assert exponent >= 20 and exponent % 2 == 0
    eps = F(1, 1 << (exponent//2))
    tau = F(1, 1 << exponent)
    root, meta = covariance_root(x, theta, g)
    out = {}
    for k in range(4):
        for sign in [-1, 1]:
            out[f'noise_{k}_{sign:+d}'] = tuple(I.of(x[j])+sign*eps*root[j][k]
                                               for j in range(4))
    sn, cs = sin_cos(tau)
    a, b, c, d = map(I.of, x)
    if hopping_axis == 'x':
        hp = (cs*a+hopping_sign*sn*d, cs*b-hopping_sign*sn*c,
              cs*c+hopping_sign*sn*b, cs*d-hopping_sign*sn*a)
    elif hopping_axis == 'y':
        hp = (cs*a-hopping_sign*sn*c, cs*b-hopping_sign*sn*d,
              cs*c+hopping_sign*sn*a, cs*d+hopping_sign*sn*b)
    elif hopping_axis == 'z':
        hp = (cs*a+hopping_sign*sn*b, cs*b-hopping_sign*sn*a,
              cs*c-hopping_sign*sn*d, cs*d+hopping_sign*sn*c)
    elif hopping_axis == 'zero':
        hp = tuple(map(I.of, x))
    else:
        raise ValueError(hopping_axis)
    out['hop'] = hp
    i1, i2 = x[0]*x[0]+x[1]*x[1], x[2]*x[2]+x[3]*x[3]
    s1, c1 = sin_cos(tau*g*i2)
    s2, c2 = sin_cos(tau*g*i1)
    out['phase'] = (c1*a+s1*b, c1*b-s1*a, c2*c+s2*d, c2*d-s2*c)
    out['damp'] = tuple(I.of(v*(1-tau/2)) for v in x)
    rounded = {}
    diagnostics = []
    for name, ep in out.items():
        rounded[name], check = contractive_round(ep)
        diagnostics.append({'category': name, **check})
    return rounded, meta, diagnostics


def port_rates(x, axis):
    a, b, c, d = map(F, x)
    s = a*a+b*b+c*c+d*d
    r = {'x': 2*(a*c+b*d), 'y': 2*(a*d-b*c),
         'z': a*a+b*b-c*c-d*d}[axis]
    out = ((s+r)/2, (s-r)/2)
    assert min(out) >= 0 and sum(out) == s
    return out


def proposal_row(x, exponent, axis='x', latch=0):
    rate = (1 << exponent)
    internal = 7*rate
    uniform_rate = internal+RADIUS*RADIUS
    cats = [f'noise_{k}_{s:+d}' for k in range(4) for s in [-1, 1]]
    weights = [F(rate, 2)]*8
    cats += ['hop', 'phase', 'damp']
    weights += [F(rate)]*3
    lp, lm = port_rates(x, axis) if latch == 0 else (F(0), F(0))
    cats += ['port_plus', 'port_minus', 'self']
    weights += [lp, lm, uniform_rate-internal-lp-lm]
    weights = [v/uniform_rate for v in weights]
    assert all(v >= 0 for v in weights) and sum(weights) == 1
    return cats, weights


def dyadic_row(weights, bits=RANDOM_BITS):
    """All but final category rounded down; leftover to final category."""
    q = 1 << bits
    masses = [(F(w)*q).numerator//(F(w)*q).denominator for w in weights[:-1]]
    masses += [q-sum(masses)]
    assert min(masses) >= 0 and sum(masses) == q
    return masses


def pick_dyadic(masses, word):
    assert 0 <= word < sum(masses)
    c = 0
    for n, v in enumerate(masses):
        c += v
        if word < c:
            return n
    raise AssertionError('positive categorical row did not cover word')


def small_poisson_row(v, bits=RANDOM_BITS):
    """Support 0..63, overflow maps to 64; a positive dyadic row."""
    v = F(v)
    assert 0 <= v <= 1
    term = total = F(1)
    for k in range(1, POISSON_DEGREE+1):
        term *= -v/k
        total += term
    assert POISSON_DEGREE % 2 == 1 and total >= 0
    lower = total
    scale = 1 << bits
    term = lower
    masses = []
    for n in range(POISSON_K+1):
        if n:
            term *= v/n
        masses.append((term*scale).numerator//(term*scale).denominator)
    masses += [scale-sum(masses)]
    assert min(masses) >= 0 and sum(masses) == scale
    # Degree 65 alternating-series error <=v^66/66!.
    eta0 = v**66/factorial(66)
    error = F(2, factorial(64))+3*eta0+F(64, scale)
    return masses, error


def finite_poisson(mu, randbits, bits=RANDOM_BITS, cap_bits=128):
    """Executable bounded sampler; not invoked for giant default means."""
    mu = F(mu)
    if not mu:
        return 0, False
    m = ceildiv(mu.numerator, mu.denominator)
    row, _ = small_poisson_row(mu/m, bits)
    cap = 2*m+cap_bits
    count = 0
    for _ in range(m):
        count += pick_dyadic(row, randbits(bits))
        if count >= cap:
            return 0, True  # declared fallback
    return count, False


def simulate_bins(initial_point, theta, exponent, bins, policy, randbits):
    """Complete finite recursion; caller supplies independent uniform words.

    policy(record) -> {g, hopping_axis, hopping_sign, port_axis}.
    Bin durations are rational. Physical feedback acts ONLY at boundaries.
    This function is supplied, not run in full by the certificate command.
    """
    x = tuple(map(F, initial_point))
    if sum(v*v for v in x) > RADIUS*RADIUS:
        x = (F(0),)*4
    record = []
    uniform_rate = 7*(1 << exponent)+RADIUS*RADIUS
    for duration in bins:
        control = policy(tuple(record))
        n, count_cap = finite_poisson(uniform_rate*F(duration), randbits)
        latch = 0
        if count_cap:
            x = (F(0),)*4
            record.append(0)
            continue
        for _ in range(n):
            names, weights = proposal_row(x, exponent, control['port_axis'], latch)
            category = names[pick_dyadic(dyadic_row(weights), randbits(RANDOM_BITS))]
            if category == 'self':
                continue
            if category in ('port_plus', 'port_minus'):
                latch = 1 if category == 'port_plus' else -1
                continue
            # Simple reference implementation evaluates all eleven endpoints.
            # An optimized implementation may evaluate only the chosen one.
            candidates, _, _ = endpoints(x, theta, exponent,
                F(control['g']), control['hopping_axis'], control['hopping_sign'])
            x = candidates[category]
        record.append(latch)
    return tuple(record), x


def ap(p, r):
    return sum(comb(p, r+s)*comb(r+s, 2*s)*4**s
               for s in range(min(r, p-r)+1))


def coefficients(p, eps2):
    # m=2,kappa=nu=Dmax=1, eta=1.
    return [F(0), F(p*(p+1))]+[
        F(2*ap(p, r))*eps2**(r-1) for r in range(2, p+1)]


def moments(max_order, eps2):
    rho = 1-eps2/2
    out = [F(1)]
    for p in range(1, max_order+1):
        coeff = coefficients(p, eps2)
        kp = (1-rho**(2*p))/eps2
        out.append(sum(coeff[r]*out[p-r] for r in range(1, p+1))/kp)
        assert out[-1] >= factorial(p+1)
    return out


def exit_allowance(eps2, horizon=F(2), p=48):
    rho = 1-eps2/2
    kp = (1-rho**(2*p))/eps2
    a = coefficients(p, eps2)
    sstar = F(p+2)
    assert sum(a[r]/sstar**r for r in range(1, p+1)) <= kp
    c = sum(a[r]*sstar**(p-r) for r in range(1, p+1))
    return (F(factorial(p+1))+horizon*c)/RADIUS**(2*p), {
        'p': p, 's_star': str(sstar), 'radius': str(RADIUS),
        'drift_inequality_checked_exactly': True}


def analytic_cases():
    horizon = F(2)
    bins = [F(1), F(1, 2), F(1, 2)]
    c2 = 2+2*sqrt_upper(3)
    c4 = F(70)
    cases = []
    for exponent in [20, 24, 28]:
        eps2 = F(1, 1 << exponent)
        u = moments(40, eps2)
        internal = 7*(1 << exponent)
        uniform_rate = F(internal)+RADIUS**2
        exit_error, exit_meta = exit_allowance(eps2)
        poisson_error = F(0)
        row_error = F(0)
        proposals_cap = 0
        small_draws = 0
        for dt in bins:
            mu = uniform_rate*dt
            m = ceildiv(mu.numerator, mu.denominator)
            _, small_error = small_poisson_row(mu/m)
            cap = 2*m+128
            poisson_error += m*small_error+F(1, 1 << 128)
            row_error += cap*F(14, 1 << RANDOM_BITS)
            small_draws += m
            proposals_cap += cap
        for theta in [F(1, 4), F(1, 8), F(1, 16)]:
            b = 2/theta
            tails = [(horizon*F(1, 2)*F((p-1)**(p-1), p**p)*u[p]/b**(p-1), p)
                     for p in range(2, len(u))]
            tail, chosen_p = min(tails)
            noise = horizon*c4*eps2*2/(48*theta*theta)
            ham = horizon*eps2/4*(c2*(u[1]+u[3])/theta+
                   2*(sqrt_upper(u[1])+sqrt_upper(u[2]*u[3]))*sqrt_upper(1/theta))
            damp = horizon*c2*eps2*u[1]/(16*theta)
            rounding = horizon*internal*(4*DELTA)*sqrt_upper(1/theta)
            # Lower-quantile initializer, supplied by companion standalone code.
            # Each real coordinate is N(0,1/2), cap R0=8, B0=128, grid 2^-60.
            init = 4*F(3, 8)**64+(32*F(1, 1 << 128)+F(4, 1 << 60))*sqrt_upper(1/theta)
            pieces = {'quantum_clipping': tail, 'noise_jump': noise,
                      'Hamiltonian_jumps': ham, 'rational_damping': damp,
                      'endpoint_rounding': rounding, 'finite_thermal_initialization': init,
                      'radius_exit': exit_error, 'finite_Poisson_and_count_caps': poisson_error,
                      'finite_proposal_uniforms': row_error}
            total = sum(pieces.values())
            cases.append({
                'theta': str(theta), 'thermal_mean_photons_per_mode': int(1/theta),
                'epsilon_squared_tau_tau_d': str(eps2), 'eta': 1, 'B': str(b),
                'chosen_moment_order': chosen_p,
                'U1_upper': pack_upper(u[1]), 'U2_upper': pack_upper(u[2]),
                'U3_upper': pack_upper(u[3]),
                'allowances_TV': {k: pack_upper(v) for k, v in pieces.items()},
                'complete_quantum_record_TV_upper': pack_upper(total),
                'expected_internal_actions_exact_ideal_sampler': int(horizon*internal),
                'expected_uniformization_proposals_exact_ideal_sampler': int(horizon*uniform_rate),
                'small_Poisson_draws_deterministic_upper': small_draws,
                'categorical_proposals_cap_total': proposals_cap,
                'random_bits_upper_without_initialization': RANDOM_BITS*(small_draws+proposals_cap),
                'initialization_uniform_bits': 4*(128+1),
                'state_coordinate_grid_bits': STATE_BITS,
                'signed_coordinate_bits_sufficient': STATE_BITS+5,
                'working_interval_precision_bits': BITS,
                'radius_certificate': exit_meta,
                'statistical_forecast_error': 'Not included: no full trajectory ensemble was run.'})
    return cases


def primitive_checks():
    tests = []
    max_width = F(0)
    max_error2 = F(0)
    resets = 0
    endpoint_count = 0
    row_count = 0
    for theta, boundary in [(F(1, 4), (2, 0, 2, 0)),
                            (F(1, 8), (2, 2, 2, 2)),
                            (F(1, 16), (4, 0, 4, 0))]:
        points = [(0, 0, 0, 0), (1, F(1, 2), F(-3, 4), 2), boundary,
                  (5, 0, 4, 0), (12, 0, 0, 0), (6, 2, 1, -3)]
        for exponent in [20, 24, 28]:
            for ix, x in enumerate(points):
                for axis, sign, g in [('x', 1, F(1)), ('y', -1, F(-1)), ('z', 1, F(1))]:
                    result, meta, checks = endpoints(x, theta, exponent, g, axis, sign)
                    for check in checks:
                        max_width = max(max_width, check['width_upper'])
                        max_error2 = max(max_error2, check['endpoint_squared_error_upper_before_reset'])
                        resets += int(check['reset_on_rounded_candidate'])
                    endpoint_count += len(checks)
                    if ix == 2:
                        assert meta['radicand'] == 0
                    for port_axis in ['x', 'y', 'z']:
                        for latch in [0, 1]:
                            _, weights = proposal_row(tuple(map(F, x)), exponent, port_axis, latch)
                            masses = dyadic_row(weights)
                            for word in [0, 1, (1 << 127), (1 << 128)-1]:
                                assert 0 <= pick_dyadic(masses, word) < len(masses)
                            row_count += 1
                tests.append({'theta': str(theta), 'exponent': exponent, 'point': list(map(str, x)),
                              'exact_boundary': ix == 2})
    for v in [F(0), F(1, 3), F(1, 2), F(1)]:
        masses, bound = small_poisson_row(v)
        assert len(masses) == 65 and sum(masses) == 1 << RANDOM_BITS
        assert bound >= 0
    # Exact combinatoric check independent of the moment recurrence.
    for p in range(2, 13):
        s, eps, sig = F(9), F(1, 7), F(2, 5)
        a, b = 2*eps*3*sig, eps*eps*sig*sig
        direct = ((s+a+b)**p+(s-a+b)**p-2*s**p)/(2*eps*eps)
        grouped = sum(F(ap(p, r))*eps**(2*r-2)*s**(p-r)*sig**(2*r)
                      for r in range(1, p+1))
        assert direct == grouped
    return {'endpoint_enclosures_checked': endpoint_count,
            'rational_proposal_rows_checked': row_count,
            'observed_radius_resets_in_primitive_checks': resets,
            'maximum_observed_endpoint_interval_width': pack_upper(max_width),
            'maximum_observed_endpoint_squared_rounding_error': pack_upper(max_error2),
            'all_widths_below_2_power_minus_100': max_width <= F(1, 1 << 100),
            'all_contractivity_and_distance_assertions_passed': True,
            'small_Poisson_rows_checked': ['0', '1/3', '1/2', '1'],
            'moment_combinatoric_orders_checked': list(range(2, 13)),
            'test_inputs': tests,
            'scope': 'Finite primitive executions and exact algebraic bound evaluations, not a full forecast.'}


def main():
    checks = primitive_checks()
    cases = analytic_cases()
    source = Path(__file__)
    out = {
        'status': 'Private research. Complete analytic finite-model allowance plus executed finite primitives. No full quantum-record Monte Carlo forecast.',
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'model': {'m': 2, 'kappa': 1, 'nu': 1, 'G_max': 1, 'H_max': 1,
                  'c_max': 1, 'horizon': 2, 'bins': ['1', '1/2', '1/2'],
                  'eta': 1, 'preparation': 'Supplied product thermal coherent mixture, with finite-bit contractive initializer allowance.',
                  'controls': 'Supplied feedback table among Pauli hopping axes/signs, cross-Kerr signs, Pauli readout axes; tables frozen inside each bin.',
                  'instrument_access': 'Specified passive loss subchannels; theta*c <= d=1+1/theta.',
                  'randomness': 'Independent uniform 128-bit words are a supplied computational input.'},
        'implementation': {'interval_bits': BITS, 'state_grid_bits': STATE_BITS,
                           'Poisson_small_count_cutoff': POISSON_K,
                           'Poisson_exponential_odd_degree': POISSON_DEGREE,
                           'rounding': 'Contractive coordinate endpoint enclosure, radius reset at every rounded attempted exit.',
                           'uniformization': 'No waiting times. Finite Poisson count and positive categorical transitions per fixed-control bin.',
                           'thermal_initializer': 'Companion exact interval inverse-erf implementation; no Gaussian oracle is claimed.'},
        'executed_primitive_checks': checks, 'cases': cases,
        'not_claimed': ['Practical speed advantage', 'Executed certified forecast ensemble',
                        'Acquired physical measurement', 'Economical posterior after a rare supplied record',
                        'Free preparation or instrument calibration', 'A first phase-space or positive-diffusion method']}
    target = source.with_name('POSITIVE_JUMP_PREDICTOR_V2_CERTIFICATE.json')
    target.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: checks[k] for k in ['endpoint_enclosures_checked', 'rational_proposal_rows_checked',
         'maximum_observed_endpoint_interval_width', 'all_contractivity_and_distance_assertions_passed']}, indent=2))
    for row in cases:
        print(json.dumps({k: row[k] for k in ['theta', 'epsilon_squared_tau_tau_d',
            'chosen_moment_order', 'complete_quantum_record_TV_upper',
            'expected_internal_actions_exact_ideal_sampler']}))
    print(target)


if __name__ == '__main__':
    main()
