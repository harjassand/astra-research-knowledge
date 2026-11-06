"""Sharp inference on cooperative networks, with rational certificates.

All model envelopes and certificate inequalities use fractions.Fraction.
The ordered-source reduction uses ordinary comparison theory; the numerical
error analysis uses the classical logarithmic-norm residual inequality.
"""
from fractions import Fraction as Q


class InconsistentData(ValueError):
    pass


def require(condition, message='Invalid model or certificate'):
    if not condition:
        raise ValueError(message)


def ceil_int(x):
    return -((-x.numerator)//x.denominator)


def ceil_log2(x):
    x = Q(x)
    if x <= 1:
        return 0
    k = max(0, x.numerator.bit_length()-x.denominator.bit_length())
    while Q(1 << k) < x:
        k += 1
    return k


def round_dyadic(x, bits):
    scale = 1 << bits
    return Q(int(x*scale), scale)


def round_up(x, bits):
    scale = 1 << bits
    return Q(ceil_int(x*scale), scale)


def supnorm(x):
    return max(map(abs, x), default=Q(0))


class Envelope:
    def __init__(self, lower_slope, upper_slope, samples, endpoint):
        self.lower_slope, self.upper_slope = Q(lower_slope), Q(upper_slope)
        require(self.lower_slope <= self.upper_slope, 'Reversed slope interval')
        require(endpoint in ('lower', 'upper'), 'Unknown envelope endpoint')
        self.endpoint = endpoint
        self.samples = [tuple(map(Q, row)) for row in samples]
        require(self.samples and all(lo <= hi for _, lo, hi in self.samples),
                'Each source requires nonempty valid interval data')
        self.A = self.upper_slope-self.lower_slope
        self.lo = [(x, lo-self.lower_slope*x) for x, lo, _ in self.samples]
        self.hi = [(x, hi-self.lower_slope*x) for x, _, hi in self.samples]
        for x, _, hi in self.samples:
            if self.value(x, 'lower') > hi:
                raise InconsistentData('Inconsistent source and measurement bounds')

    def value(self, x, endpoint=None):
        x = Q(x)
        endpoint = endpoint or self.endpoint
        require(endpoint in ('lower', 'upper'), 'Unknown envelope endpoint')
        if endpoint == 'lower':
            return self.lower_slope*x+max(
                lo-self.A*max(z-x, Q(0)) for z, lo in self.lo)
        return self.lower_slope*x+min(
            hi+self.A*max(x-z, Q(0)) for z, hi in self.hi)

    def document(self):
        return {'lower_slope': str(self.lower_slope),
                'upper_slope': str(self.upper_slope),
                'samples': [[str(x) for x in row] for row in self.samples],
                'endpoint': self.endpoint}


class Network:
    def __init__(self, rows, sources, forcing):
        self.n = len(sources)
        self.rows = [[(int(j), Q(v)) for j, v in row if Q(v)] for row in rows]
        self.sources = sources
        self.forcing = list(map(Q, forcing))
        require(self.n > 0 and len(rows) == len(forcing) == self.n, 'Dimension mismatch')
        require(all(0 <= j < self.n for row in self.rows for j, _ in row),
                'Invalid matrix column')
        require(all(v >= 0 for i, row in enumerate(self.rows) for j, v in row if j != i),
                'The network must have nonnegative off-diagonal coupling')
        self.diagonal = [sum((v for j, v in row if j == i), Q(0))
                         for i, row in enumerate(self.rows)]
        self.lipschitz = max(
            sum((abs(v) for _, v in row), Q(0))+
            max(abs(g.lower_slope), abs(g.upper_slope))
            for row, g in zip(self.rows, sources))
        self.gamma = max(sum((v for _, v in row), Q(0))-g.lower_slope
                         for row, g in zip(self.rows, sources))

    def rhs(self, x):
        require(len(x) == self.n, 'State dimension mismatch')
        return [sum((v*x[j] for j, v in row), Q(0))
                -g.value(x[i])+self.forcing[i]
                for i, (row, g) in enumerate(zip(self.rows, self.sources))]

    def document(self):
        return {
            'rows': [[[j, str(v)] for j, v in row] for row in self.rows],
            'sources': [g.document() for g in self.sources],
            'forcing': list(map(str, self.forcing)),
            'lipschitz': str(self.lipschitz), 'gamma': str(self.gamma)}


def trajectory_at_grid(model, initial, horizon, steps, tolerance, keep_trace=True):
    initial = list(map(Q, initial))
    horizon, tolerance = Q(horizon), Q(tolerance)
    require(len(initial) == model.n, 'Initial dimension mismatch')
    require(horizon >= 0 and 0 < tolerance <= 1 and isinstance(steps, int) and steps >= 1)
    h = horizon/steps
    if model.gamma > 0:
        require(model.gamma*h <= Q(1, 2), 'Step too large')
    growth = Q(1 << ceil_int(4*max(model.gamma, Q(0))*horizon))
    bits = max(24, ceil_log2(32*(steps+1)*growth/tolerance))
    q = 1/(1-model.gamma*h)
    local_factor = max(Q(1), q)
    x = [round_dyadic(v, bits) for v in initial]
    radius = round_up(supnorm([a-b for a, b in zip(x, initial)]), bits)
    trace = [{'x': list(map(str, x)), 'radius': str(radius)}] if keep_trace else None
    max_speed = Q(0)
    for _ in range(steps):
        f = model.rhs(x)
        speed = supnorm(f)
        max_speed = max(max_speed, speed)
        exact_euler = [a+h*b for a, b in zip(x, f)]
        next_x = [round_dyadic(v, bits) for v in exact_euler]
        jump = supnorm([a-b for a, b in zip(next_x, exact_euler)])
        local_defect = local_factor*model.lipschitz*speed*h*h/2
        radius = round_up(q*radius+local_defect+jump, bits)
        x = next_x
        if keep_trace:
            trace.append({'x': list(map(str, x)), 'radius': str(radius)})
    return {
        'initial': list(map(str, initial)), 'horizon': str(horizon),
        'steps': steps, 'step': str(h), 'precision_bits': bits,
        'state': list(map(str, x)), 'radius': str(radius),
        'maximum_candidate_speed': str(max_speed),
        'trace': trace}


def certified_trajectory(model, initial, horizon, tolerance):
    horizon, tolerance = Q(horizon), min(Q(tolerance), Q(1))
    require(horizon >= 0 and tolerance > 0)
    n = max(8, ceil_int(2*max(Q(0), model.gamma)*horizon))
    # Dyadic step counts make the complete cost of failed refinements explicit.
    n = 1 << ceil_log2(n)
    attempts = []
    while True:
        result = trajectory_at_grid(model, initial, horizon, n, tolerance, True)
        attempts.append({'steps': n, 'radius': result['radius']})
        if Q(result['radius']) <= tolerance:
            result['attempts'] = attempts
            result['total_steps_including_refinements'] = sum(x['steps'] for x in attempts)
            return result
        n *= 2


def verify_trajectory(model, certificate):
    """Check a numerical path independently of its rounding implementation."""
    trace = certificate['trace']
    steps = certificate['steps']
    h = Q(certificate['step'])
    require(isinstance(steps, int) and steps >= 1 and h >= 0)
    require(len(trace) == steps+1 and h*steps == Q(certificate['horizon']))
    require(model.gamma*h < 1)
    q = 1/(1-model.gamma*h)
    local_factor = max(Q(1), q)
    old = list(map(Q, trace[0]['x']))
    radius = Q(trace[0]['radius'])
    initial = list(map(Q, certificate['initial']))
    require(len(old) == len(initial) == model.n)
    require(radius >= supnorm([a-b for a, b in zip(old, initial)]))
    for item in trace[1:]:
        f = model.rhs(old)
        new = list(map(Q, item['x']))
        require(len(new) == model.n)
        jump = supnorm([b-a-h*c for a, b, c in zip(old, new, f)])
        required = q*radius+local_factor*model.lipschitz*supnorm(f)*h*h/2+jump
        new_radius = Q(item['radius'])
        require(new_radius >= required, 'Insufficient trajectory error radius')
        old, radius = new, new_radius
    require(list(map(str, old)) == certificate['state'])
    require(radius == Q(certificate['radius']))
    return True


def certified_equilibrium(model, tolerance):
    tolerance = Q(tolerance)
    require(tolerance > 0 and model.gamma < 0, 'A negative logarithmic norm is required')
    alpha = -model.gamma
    diagonal_scale = max(Q(0), max(
        g.upper_slope-a for g, a in zip(model.sources, model.diagonal)))
    h = 1/(1+diagonal_scale)
    q = 1-alpha*h
    require(0 <= q < 1)
    bits = max(24, ceil_log2(32*max(Q(1), model.lipschitz)/(alpha*alpha*h*tolerance)))
    x = [Q(0)]*model.n
    d0 = supnorm(model.rhs(x))
    log_bound = max(1, ceil_log2(
        16*(1+model.lipschitz)*(1+d0)/(alpha*alpha*tolerance)))
    limit = ceil_int(Q(log_bound)/(alpha*h))+4
    for iteration in range(limit+1):
        f = model.rhs(x)
        radius = supnorm(f)/alpha
        if radius <= tolerance:
            return {'state': list(map(str, x)), 'radius': str(radius),
                    'residual': list(map(str, f)),
                    'alpha': str(alpha), 'step': str(h),
                    'precision_bits': bits, 'iterations': iteration,
                    'proved_iteration_limit': limit}
        x = [round_dyadic(a+h*b, bits) for a, b in zip(x, f)]
    raise AssertionError('The proved equilibrium convergence budget was not met')


def verify_equilibrium(model, certificate):
    require(model.gamma < 0)
    x = list(map(Q, certificate['state']))
    require(len(x) == model.n)
    residual = model.rhs(x)
    radius = supnorm(residual)/(-model.gamma)
    require(list(map(str, residual)) == certificate['residual'])
    require(radius == Q(certificate['radius']))
    require(Q(certificate['alpha']) == -model.gamma)
    return True


def contraction_scaling(model):
    """Construct a positive diagonal change of coordinates when possible.

    For M=A-diag(lower_slopes), solve (-M)w=1 exactly. For a Metzler M,
    a positive solution exists iff M is Hurwitz. The returned rational w
    is a directly checkable stability certificate, not a spectral oracle.
    A None result only says this uniform matrix test failed.
    """
    from interpolation import solve_unique
    if model.gamma < 0:
        return [Q(1)]*model.n, model
    matrix = [[Q(0)]*model.n for _ in range(model.n)]
    for i, (row, g) in enumerate(zip(model.rows, model.sources)):
        matrix[i][i] = g.lower_slope
        for j, value in row:
            matrix[i][j] -= value
    weights = solve_unique(matrix, [Q(1)]*model.n)
    if weights is None or min(weights) <= 0:
        return None
    rows = [[(j, value*weights[j]/weights[i]) for j, value in row]
            for i, row in enumerate(model.rows)]
    sources = [Envelope(g.lower_slope, g.upper_slope,
                        [(x/w, lo/w, hi/w) for x, lo, hi in g.samples], g.endpoint)
               for g, w in zip(model.sources, weights)]
    scaled = Network(rows, sources, [u/w for u, w in zip(model.forcing, weights)])
    require(scaled.gamma < 0, 'Invalid positive scaling certificate')
    return weights, scaled
