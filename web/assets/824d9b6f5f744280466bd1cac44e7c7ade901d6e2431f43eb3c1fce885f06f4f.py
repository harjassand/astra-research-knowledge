"""Acquired blind archive for a known finite-digital weak-interaction model.

No partition table, peer code, float exp, reference sampler, or unknown-v input.
Rational probability arithmetic; Random is a reproducible diagnostic bit source.
Full proof and exact interface are in DIGITAL_GIBBS_REPAIR.txt.
"""
from fractions import Fraction as F
from pathlib import Path
import math
import json
import random
import time


def ceil_fraction(x):
    x = F(x)
    return -(-x.numerator // x.denominator)


def ceil_sqrt_fraction(x):
    x = F(x)
    if x < 0:
        raise ValueError('nonnegative value required')
    n = math.isqrt(x.numerator // x.denominator)
    return n if n*n >= x else n+1


def node(j, J):
    if not 0 <= j <= J:
        raise ValueError('invalid node')
    return F(-1) + F(6*j*j, J*J) - F(4*j*j*j, J*J*J)


def point(k, p):
    if not 0 <= k < (1 << p):
        raise ValueError('invalid grid point')
    return F(2*k+1-(1 << p), 1 << p)


def hat(t, j, J):
    t = F(t)
    a = node(j, J)
    if t == a:
        return F(1)
    if t < a and j > 0:
        left = node(j-1, J)
        return (t-left)/(a-left) if t > left else F(0)
    if t > a and j < J:
        right = node(j+1, J)
        return (right-t)/(right-a) if t < right else F(0)
    return F(0)


def support_grid(j, J, p):
    N = 1 << p
    a = node(max(0, j-1), J)
    b = node(min(J, j+1), J)
    lo = max(0, ceil_fraction((a+1)*N/2-F(1, 2)))
    hi = min(N-1, ((b+1)*N/2-F(1, 2)).numerator // ((b+1)*N/2-F(1, 2)).denominator)
    if lo > hi:
        raise ValueError('hat contains no grid point; acquire adequate p')
    return lo, hi


class RandomnessCap(Exception):
    pass


class BitSource:
    def __init__(self, seed, max_attempts=None):
        self.generator = random.Random(seed)
        self.max_attempts = max_attempts
        self.bits = 0
        self.rejected_uniform_draws = 0
        self.max_coin_bits = 0
        self.cap_failures = 0

    def below(self, n):
        if n < 1:
            raise ValueError('invalid uniform integer range')
        if n == 1:
            return 0
        b = (n-1).bit_length()
        attempts = 0
        while self.max_attempts is None or attempts < self.max_attempts:
            attempts += 1
            self.bits += b
            k = self.generator.getrandbits(b)
            if k < n:
                return k
            self.rejected_uniform_draws += 1
        self.cap_failures += 1
        raise RandomnessCap('uniform integer rejection cutoff reached')

    def coin(self, prob):
        prob = F(prob)
        if not 0 <= prob <= 1:
            raise ValueError('invalid exact Bernoulli probability')
        self.max_coin_bits = max(self.max_coin_bits, prob.denominator.bit_length())
        return self.below(prob.denominator) < prob.numerator


def adjacency(d, edges):
    a = [[] for _ in range(d)]
    seen = set()
    for i, j, lam in edges:
        lam = F(lam)
        if not 0 <= i < j < d or lam < 0 or (i, j) in seen:
            raise ValueError('simple graph with nonnegative weights required')
        seen.add((i, j))
        a[i].append((j, lam))
        a[j].append((i, lam))
    return a


def taylor_degree(W, eta):
    W, eta = F(W), F(eta)
    if not W >= 0 or eta <= 0:
        raise ValueError('invalid remainder parameters')
    r = 0
    remainder = W
    while remainder > eta:
        r += 1
        remainder *= W / (r+1)
    return r, remainder


def exp_minus_rational(u, degree):
    u = F(u)
    if u < 0:
        raise ValueError('nonnegative exponent required')
    term = F(1)
    val = F(1)
    for k in range(1, degree+1):
        term *= -u/k
        val += term
    return max(F(0), min(F(1), val))


def plan(spectrum, edges, rho, epsilon):
    s = list(map(F, spectrum))
    eps, rho = F(epsilon), F(rho)
    if not s or min(s) < 0 or not 0 <= rho < 1 or not 0 < eps < 1 or sum(x*x for x in s) > rho*rho:
        raise ValueError('invalid model range/precision')
    d = len(s)
    a = adjacency(d, edges)
    W = max(sum((lam for _, lam in row), F(0)) for row in a)
    if W >= 4:
        raise ValueError('Dobrushin regime W<4 required')
    L = 2*W
    C = 12+324*L
    m = 0
    tail2 = sum(x*x for x in s)
    while tail2 > eps*eps/64:
        tail2 -= s[m]*s[m]
        m += 1
    M = ceil_sqrt_fraction(max(1, m))
    J0 = max(3, ceil_fraction(6*L))
    Js = [max(J0, ceil_sqrt_fraction(4*C*M*x/eps)) for x in s[:m]]
    Jmax = max(Js, default=3)
    p = 0
    while (1 << p) < 16*Jmax*Jmax or F(1 << p) < 264/eps:
        p += 1
    alpha = W/4
    contraction = 1-(1-alpha)/d
    T = 1
    mixing = d*contraction
    while mixing > eps/8:
        T += 1
        mixing *= contraction
    delta_step = eps/(8*T)
    exp_lower = F(1, 3**ceil_fraction(W))
    eta = exp_lower*delta_step/2
    degree, remainder = taylor_degree(W, eta)
    D = math.prod(J+1 for J in Js)
    # Bound every rejection loop and charge their extra total-TV error.
    proposal_cap = 1
    proposal_failure = T*(1-exp_lower/8)
    while proposal_failure > eps/8:
        proposal_cap += 1
        proposal_failure *= 1-exp_lower/8
    uniform_calls_upper = m+T*(2*proposal_cap+1)
    uniform_attempt_cap = 0
    while F(uniform_calls_upper, 1 << uniform_attempt_cap) > eps/8:
        uniform_attempt_cap += 1
    qmax = max((math.lcm(*(lam.denominator for _, lam in row)) for row in a), default=1)
    N = 1 << p
    denominator_upper = N*(2*Jmax**3)*(qmax*N**4)**degree*math.factorial(degree)
    random_operand_bits_upper = max(p, (d-1).bit_length(), denominator_upper.bit_length())
    allocation2 = C*C*sum((s[i]*s[i]/Js[i]**4 for i in range(m)), F(0))
    digitization = 33*rho*F(2, 1 << p)
    # Rational prerequisites imply ideal TV<=3eps/8 and total<=5eps/8.
    assert allocation2 <= eps*eps/16
    assert digitization <= eps/4
    assert tail2 <= eps*eps/64
    assert remainder <= eta
    return {'d': d, 'm': m, 'J': Js, 'p': p, 'D': D,
            'archive_bits': (D-1).bit_length(), 'input_output_bits': d*p,
            'W': str(W), 'L': str(L), 'C': str(C), 'alpha': str(alpha),
            'rho': str(rho), 'epsilon': str(eps), 'mixing_steps': T,
            'mixing_upper': str(mixing), 'local_kernel_TV_budget': str(delta_step),
            'exp_absolute_error_target': str(eta), 'exp_degree': degree,
            'exp_remainder_upper': str(remainder),
            'expected_proposals_upper': str(8*T/exp_lower),
            'allocation_squared_density_error': str(allocation2),
            'digitization_density_error': str(digitization), 'tail_squared_norm': str(tail2),
            'ideal_TV_upper': str(3*eps/8), 'uncapped_TV_upper': str(5*eps/8),
            'total_TV_upper': str(7*eps/8),
            'proposals_per_update_cap': proposal_cap,
            'total_proposals_hard_cap': T*proposal_cap,
            'proposal_cutoff_failure_upper': str(proposal_failure),
            'uniform_integer_attempt_cap': uniform_attempt_cap,
            'uniform_integer_calls_hard_cap': uniform_calls_upper,
            'uniform_integer_cutoff_failure_upper': str(F(uniform_calls_upper, 1 << uniform_attempt_cap)),
            'random_integer_operand_bits_hard_cap': random_operand_bits_upper,
            'total_random_bits_hard_cap': uniform_calls_upper*uniform_attempt_cap*random_operand_bits_upper,
            'all_model_acquisition': 'supplied known graph/couplings/spectrum/rho; no discovery claim',
            'precision_scope': 'digital midpoint-weight model, not quantized continuous Gibbs law'}


def _encode(grid_input, specification, bits):
    d, m, Js, p = [specification[k] for k in ['d', 'm', 'J', 'p']]
    if len(grid_input) != d:
        raise ValueError('full input required')
    if any(not isinstance(k, int) or not 0 <= k < (1 << p) for k in grid_input):
        raise ValueError('legal digital input required')
    labels = []
    for i in range(m):
        t = point(grid_input[i], p)
        J = Js[i]
        lo, hi = 0, J-1
        while lo < hi:
            mid = (lo+hi+1)//2
            if node(mid, J) <= t:
                lo = mid
            else:
                hi = mid-1
        frac = (t-node(lo, J))/(node(lo+1, J)-node(lo, J))
        labels.append(lo+1 if bits.coin(frac) else lo)
    # Every random label is in this single counted mixed-radix record.
    packed = 0
    for label, J in zip(labels, Js):
        packed = packed*(J+1)+label
    assert 0 <= packed < specification['D']
    return packed


def encode(grid_input, specification, bits):
    try:
        return _encode(grid_input, specification, bits)
    except RandomnessCap:
        return 0  # A legal archive; cutoff contribution is charged in the plan.


def unpack(packed, Js):
    if not 0 <= packed < math.prod(J+1 for J in Js):
        raise ValueError('invalid archive')
    labels = []
    for J in reversed(Js):
        packed, label = divmod(packed, J+1)
        labels.append(label)
    return list(reversed(labels))


def decode(packed, specification, edges, bits):
    d, m, Js, p = [specification[k] for k in ['d', 'm', 'J', 'p']]
    labels = unpack(packed, Js)
    a = adjacency(d, edges)
    ranges = [support_grid(labels[i], Js[i], p) if i < m else (0, (1 << p)-1) for i in range(d)]
    # Initialize inside each support; endpoints with zero hat are excluded here.
    x = []
    for i, (lo, hi) in enumerate(ranges):
        k = (lo+hi)//2
        if i < m:
            assert hat(point(k, p), labels[i], Js[i]) > 0
        x.append(k)
    proposals = 0
    neighbor_reads = 0
    max_probability_bits = 0
    proposal_cutoffs = 0
    randomness_cutoff = False
    updates_completed = 0
    T = specification['mixing_steps']
    degree = specification['exp_degree']
    try:
        for _ in range(T):
            i = bits.below(d)
            beta = sum((lam*point(x[j], p)**2 for j, lam in a[i]), F(0))
            neighbor_reads += len(a[i])
            lo, hi = ranges[i]
            for attempt in range(specification['proposals_per_update_cap']):
                proposals += 1
                k = lo+bits.below(hi-lo+1)
                t = point(k, p)
                phi = hat(t, labels[i], Js[i]) if i < m else F(1)
                probability = phi*exp_minus_rational(beta*(1-t*t), degree)
                max_probability_bits = max(max_probability_bits,
                                           probability.numerator.bit_length(), probability.denominator.bit_length())
                if bits.coin(probability):
                    x[i] = k
                    break
            else:
                proposal_cutoffs += 1  # Leave this coordinate unchanged.
            updates_completed += 1
    except RandomnessCap:
        randomness_cutoff = True  # Return the existing legal state.
    assert proposals <= specification['total_proposals_hard_cap']
    return x, {'planned_local_updates': T, 'completed_local_updates': updates_completed, 'proposals': proposals,
               'neighbor_values_read': neighbor_reads,
               'max_rational_probability_bits': max_probability_bits,
               'random_bits_requested': bits.bits,
               'rejected_uniform_integer_draws': bits.rejected_uniform_draws,
               'maximum_coin_denominator_bits': bits.max_coin_bits,
               'proposal_cutoffs': proposal_cutoffs, 'randomness_cutoff': randomness_cutoff}


def finite_checks():
    # Exact linear reproduction and partition of unity on several finite grids.
    hat_checks = 0
    for J in [3, 4, 7, 12]:
        for p in [3, 4, 6]:
            for k in range(1 << p):
                t = point(k, p)
                hs = [hat(t, j, J) for j in range(J+1)]
                assert min(hs) >= 0 and sum(hs) == 1
                assert sum(node(j, J)*hs[j] for j in range(J+1)) == t
                hat_checks += 1
    mass_checks = 0
    for J in [3, 4, 7, 12]:
        p = (16*J*J-1).bit_length()
        for j in range(J+1):
            lo, hi = support_grid(j, J, p)
            avg = sum((hat(point(k, p), j, J) for k in range(lo, hi+1)), F(0))/(hi-lo+1)
            assert avg >= F(1, 4)
            mass_checks += 1
    exp_checks = []
    for W in [F(0), F(1, 2), F(1), F(3), F(399, 100)]:
        degree, remainder = taylor_degree(W, F(1, 2**20))
        assert remainder <= F(1, 2**20)
        # Clipping interval and exact polynomial arithmetic are checked;
        # the mathematical Lagrange remainder supplies the exp enclosure.
        for u in [F(0), W/3, W]:
            assert 0 <= exp_minus_rational(u, degree) <= 1
        exp_checks.append({'W': str(W), 'degree': degree, 'remainder': str(remainder)})
    return {'exact_hat_partition_and_reproduction_checks': hat_checks,
            'exact_discrete_hat_mass_checks': mass_checks,
            'rational_exponential_remainder_plans': exp_checks}


def main():
    start = time.perf_counter()
    checks = finite_checks()
    s = [F(1, 16), F(1, 32), F(1, 64), F(1, 128)]
    edges = [(0, 1, F(1, 2)), (1, 2, F(1, 2)), (2, 3, F(1, 2)), (0, 3, F(1, 2))]
    specification = plan(s, edges, F(1, 2), F(1, 10))
    p = specification['p']
    N = 1 << p
    runs = []
    for seed, supplied_observation in enumerate([[N//8, N//3, N//2, 7*N//8], [N//2]*4, [0, N-1, N//4, 3*N//4]]):
        encoder_bits = BitSource(seed+101, specification['uniform_integer_attempt_cap'])
        packed = encode(supplied_observation, specification, encoder_bits)
        decoder_bits = BitSource(seed+201, specification['uniform_integer_attempt_cap'])
        output, stats = decode(packed, specification, edges, decoder_bits)
        assert all(0 <= k < N for k in output)
        assert encoder_bits.bits+decoder_bits.bits <= specification['total_random_bits_hard_cap']
        assert decoder_bits.max_coin_bits <= specification['random_integer_operand_bits_hard_cap']
        runs.append({'seed': seed, 'input_grid_indices': supplied_observation,
                     'archive_integer': packed, 'labels': unpack(packed, specification['J']),
                     'output_grid_indices': output, 'encoder_random_bits': encoder_bits.bits,
                     'decoder_costs': stats,
                     'scope': 'Execution on supplied legal observations; no claim these test inputs were sampled from P_v or that empirical TV was estimated.'})
    forced_encoder = BitSource(900, 0)
    assert encode([N//2]*4, specification, forced_encoder) == 0 and forced_encoder.cap_failures == 1
    forced_decoder = BitSource(901, 0)
    fallback, fallback_stats = decode(0, specification, edges, forced_decoder)
    assert fallback_stats['randomness_cutoff'] and all(0 <= k < N for k in fallback)
    no_interaction = plan([F(1, 1000)], [], F(1, 2), F(1, 10))
    assert no_interaction['m'] == 0 and no_interaction['D'] == 1
    xb = BitSource(303, no_interaction['uniform_integer_attempt_cap'])
    y, st = decode(0, no_interaction, [], xb)
    assert len(y) == 1
    result = {'known_cycle_plan': specification, 'checks': checks, 'actual_digital_decoder_runs': runs,
              'forced_cutoff_path_checks': 2,
              'empty_archive_plan': no_interaction, 'empty_archive_decoder': {'output': y, 'costs': st},
              'elapsed_seconds': time.perf_counter()-start,
              'status': 'SCOPED_KNOWN_DIGITAL_MODEL_CONDITIONAL_SAMPLER_ACQUIRED',
              'limits': ['All graph/spectrum data supplied; not learned.', 'Unbiased iid bit source assumed by theorem; seeded PRNG is reproducibility only.',
                         'No continuous-output TV claim.', 'Finite checks are not external theorem validation.']}
    out = Path(__file__).with_name('digital_gibbs_checks.json')
    out.write_text(json.dumps(result, indent=2)+'\n')
    display_plan = {k:specification[k] for k in ['d','m','J','p','archive_bits','input_output_bits','mixing_steps','exp_degree','total_proposals_hard_cap','total_random_bits_hard_cap','total_TV_upper']}
    print(json.dumps({'plan': display_plan, 'exact_hat_checks': checks['exact_hat_partition_and_reproduction_checks'],
                      'decoder_proposals': [r['decoder_costs']['proposals'] for r in runs],
                      'seconds': result['elapsed_seconds'], 'output': str(out)}, indent=2))

if __name__ == '__main__':
    main()
