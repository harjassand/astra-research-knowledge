"""New construction: a certified recurrent-controller occupation kernel.

The theorem is in recurrent_commuting_event_kernel_proof.md.  This executor
checks the existing Boolean rule IR, exact commutation of the local killed
matrices, and a two-state autonomous recurrent controller.  Its numerical
local exponentials currently support binary modules.  The acquiring theorem
is broader than that numerical specialization.

The Gaussian rules are NOT accepted on floating-point accuracy alone.
Positive block-banded uniformization encloses occupation moments; an inverse
residual encloses the orthogonal polynomial coefficients; sign changes
isolate all its roots; and the Gaussian weights are enclosed from those
roots.  Ordinary numerical Decimal algebra and a float Sturm iteration supply
only guesses verified by those enclosures.  No external package is required.

No prior scientific file is overwritten.  This is new implementation, not a
reconstruction of unavailable historical helpers.  The saved object is an
actual positive rational sum of local matrices, including controller input
and output indices, not a numerical execution report alone.
"""

from dataclasses import dataclass, replace
from decimal import Decimal as D, Context, getcontext, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN
from fractions import Fraction as F
from itertools import product
from math import factorial, lcm
from pathlib import Path
import argparse
import json
import time

from source_interface_compiler import (
    Rule, Program, InitialBranch, InitialFactor, SourceError, compile_interface,
)


def precision(digits):
    global DOWN, UP, NEAR
    DOWN = Context(prec=digits, rounding=ROUND_FLOOR)
    UP = Context(prec=digits, rounding=ROUND_CEILING)
    NEAR = Context(prec=digits, rounding=ROUND_HALF_EVEN)
    getcontext().prec = digits
    getcontext().rounding = ROUND_HALF_EVEN


precision(240)


class I:
    """Outward Decimal intervals; all four arithmetic operations are enclosed."""
    __slots__ = ('lo', 'hi')

    def __init__(self, lo, hi=None):
        if isinstance(lo, I):
            self.lo, self.hi = lo.lo, lo.hi
        elif isinstance(lo, F):
            self.lo = DOWN.divide(D(lo.numerator), D(lo.denominator))
            self.hi = UP.divide(D(lo.numerator), D(lo.denominator))
        else:
            self.lo = D(lo)
            self.hi = D(lo if hi is None else hi)
        if self.lo > self.hi:
            raise ArithmeticError('Reversed interval')

    def __add__(self, other):
        other = I(other)
        return I(DOWN.add(self.lo, other.lo), UP.add(self.hi, other.hi))

    __radd__ = __add__

    def __neg__(self):
        return I(self.hi.copy_negate(), self.lo.copy_negate())

    def __sub__(self, other):
        return self + (-I(other))

    def __rsub__(self, other):
        return I(other) + (-self)

    def __mul__(self, other):
        other = I(other)
        if self.lo >= 0 and other.lo >= 0:
            return I(DOWN.multiply(self.lo, other.lo), UP.multiply(self.hi, other.hi))
        pairs = [(a, b) for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return I(min(DOWN.multiply(a, b) for a, b in pairs),
                 max(UP.multiply(a, b) for a, b in pairs))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = I(other)
        if other.lo <= 0 <= other.hi:
            raise ArithmeticError('Unresolved nonzero denominator')
        return self * I(DOWN.divide(D(1), other.hi), UP.divide(D(1), other.lo))

    def exp(self):
        if self.lo == self.hi == 0:
            return I(1)
        return I(NEAR.exp(self.lo).next_minus(DOWN), NEAR.exp(self.hi).next_plus(UP))

    def sqrt(self):
        if self.lo < 0:
            raise ArithmeticError('Unresolved positive square root')
        if self.lo == self.hi == 0:
            return I(0)
        lower = D(0) if self.lo == 0 else NEAR.sqrt(self.lo).next_minus(DOWN)
        return I(lower, NEAR.sqrt(self.hi).next_plus(UP))

    def abs_upper(self):
        return max(self.lo.copy_abs(), self.hi.copy_abs())

    def midpoint(self):
        return NEAR.divide(NEAR.add(self.lo, self.hi), D(2))


def record(value):
    value = I(value)
    return [str(value.lo), str(value.hi)]


def stored_lower(value, digits=65):
    """An exact positive rational lower endpoint with bounded decimal length."""
    return F(Context(prec=digits, rounding=ROUND_FLOOR).plus(I(value).lo))


def tv_upper(spread):
    z = I(spread).sqrt()
    return ((z - 1) / (z + 1)).hi


def integerize(values):
    values = list(map(F, values))
    denominator = lcm(*(x.denominator for x in values))
    return [x.numerator * (denominator // x.denominator) for x in values], denominator


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), 0)
             for j in range(len(b[0]))] for i in range(len(a))]


def exp2(matrix):
    """Interval exponential of a binary Metzler matrix already multiplied by t."""
    a, b, c, d = [I(z) for row in matrix for z in row]
    halftrace = (a + d) / 2
    difference = (a - d) / 2
    gap2 = difference * difference + b * c
    # In this executor the nonzero offdiagonals make this strictly positive.
    # A scalar or triangular equal-diagonal matrix is handled exactly below.
    if gap2.lo < 0 and gap2.hi >= 0:
        gap2 = I(0, gap2.hi)
    gap = gap2.sqrt()
    if gap.hi == 0:
        e = halftrace.exp()
        return [[e * (1 + difference), e * b], [e * c, e * (1 - difference)]]
    if gap.lo <= 0:
        raise ArithmeticError('Binary exponential gap needs more precision')
    slow = (halftrace + gap).exp()
    fast = (halftrace - gap).exp()
    mean = (slow + fast) / 2
    divided = (slow - fast) / (2 * gap)
    return [[mean + difference * divided, b * divided],
            [c * divided, mean - difference * divided]]


def controller_matrix(lam, mu, elapsed):
    decay = (-I((lam + mu) * elapsed)).exp()
    p01 = I(lam / (lam + mu)) * (1 - decay)
    p10 = I(mu / (lam + mu)) * (1 - decay)
    return [[1 - p01, p01], [p10, 1 - p10]]


@dataclass
class Acquired:
    interface: object
    lam: F
    mu: F
    killed: list
    support: list
    event: object
    elapsed: F


def acquire_source(source, event_mark, elapsed):
    """Exact local semantic checks precede all numerical work."""
    if elapsed <= 0:
        raise SourceError('nonpositive_lag')
    interface = compile_interface(source)
    if len(interface.controller_states) != 2:
        raise SourceError('occupation_controller', requirement='two states')
    C = interface.controller_generator
    lam, mu = C[0][1], C[1][0]
    if min(lam, mu) <= 0 or C != ((-lam, lam), (mu, -mu)):
        raise SourceError('occupation_controller', requirement='bidirectional autonomous controller')
    if any(interface.controller_killing(c) for c in (0, 1)):
        raise SourceError('occupation_executor_controller_killing', requirement='local additive event killing')
    chosen = [event for event in interface.events if event.mark == event_mark]
    # Multiple source rules can carry the same mark if they share a reset and
    # owner.  Sum their exact local hazards before applying the mark.
    if not chosen:
        raise SourceError('occupation_missing_mark', mark=event_mark)
    first = chosen[0]
    if first.owner is None:
        raise SourceError('occupation_mark_owner')
    if any((e.owner, e.controller_reset, e.component_resets) !=
           (first.owner, first.controller_reset, first.component_resets) for e in chosen):
        raise SourceError('occupation_mark_reset_branches', requirement='one shared reset branch in numerical executor')
    event = replace(first, hazards=tuple(tuple(sum((e.hazards[c][x] for e in chosen), F(0))
                                                 for x in range(len(first.hazards[c]))) for c in (0, 1)))
    killed, support = [], []
    for i, component in enumerate(interface.components):
        A = [interface.killed_generator(i, c) for c in (0, 1)]
        if matmul(A[0], A[1]) != matmul(A[1], A[0]):
            raise SourceError('occupation_noncommuting_killed_generators', component=i)
        if len(component.states) != 2:
            raise SourceError('occupation_numerical_local_dimension', component=i, allowed=2)
        # Binary support; local finite graph closure generalizes this step.
        reach = [[True, any(a[0][1] > 0 for a in A)],
                 [any(a[1][0] > 0 for a in A), True]]
        killed.append(A)
        support.append(reach)
    return Acquired(interface, lam, mu, killed, support, event, F(elapsed))


def source_bounds(spec):
    minimums = []
    contrast = F(0)
    for component, (A0, A1), reach in zip(spec.interface.components, spec.killed, spec.support):
        Q0, Q1 = component.generators
        Qbar = [[(Q0[x][y] + Q1[x][y]) / 3 for y in (0, 1)] for x in (0, 1)]
        v = max(-(1 - p) * A0[x][x] - p * A1[x][x] + Qbar[x][x]
                for x in (0, 1) for p in (F(1, 3), F(2, 3)))
        E = exp2([[I(spec.elapsed * x) for x in row] for row in Qbar])
        prefactor = (-I(v * spec.elapsed)).exp()
        lower = min(stored_lower(prefactor * E[x][y]) for x in (0, 1) for y in (0, 1) if reach[x][y])
        if lower <= 0:
            raise ArithmeticError('Local supported lower certificate unresolved')
        minimums.append(lower)
        contrast += max(sum(abs(A1[x][y] - A0[x][y]) for y in (0, 1)) for x in (0, 1))
    p = controller_matrix(spec.lam, spec.mu, spec.elapsed)
    expmin = (-I(max(spec.lam, spec.mu) * spec.elapsed)).exp()
    t = spec.elapsed
    boxes = [[I(spec.lam * spec.mu * t * t / 144) * expmin,
              I(spec.lam * t / 3) * expmin],
             [I(spec.mu * t / 3) * expmin,
              I(spec.lam * spec.mu * t * t / 144) * expmin]]
    eta = min(stored_lower(boxes[c][d] / I(p[c][d].hi)) for c in (0, 1) for d in (0, 1))
    sigma = eta
    for value in minimums:
        sigma *= value
    return contrast, sigma, {'local_supported_minimums_exact':list(map(str, minimums)),
                              'central_occupation_fraction_interval':['1/3', '2/3'],
                              'controller_bridge_central_mass_lower_exact':str(eta),
                              'relative_denominator_sigma_lower_exact':str(sigma),
                              'summed_generator_contrast_norm_exact':str(contrast)}


def gaussian_order(spec, tolerance):
    contrast, sigma, info = source_bounds(spec)
    if contrast == 0:
        return 1, F(0), info
    q = 1
    # Reserve ample room for the certified numerical quadrature evaluation.
    while True:
        delta = 4 * (spec.elapsed * contrast / 4) ** (2 * q) / (sigma * factorial(2 * q))
        if delta < tolerance:
            return q, delta, info
        q += 1
        if q > 300:
            raise RuntimeError('Declared occupation quadrature order budget exceeded')


def occupation_moments(lam, mu, elapsed, degree, digits):
    """All endpoint measures of U=S_t/t by banded positive uniformization.

    B has tC on its diagonal and E=diag(0,1) above.  B-I is a killed
    generator.  Its exp at time one gives M_j/(e*j!).  Only two initial rows
    and the block bandwidth are used; no controller trajectories are stored.
    """
    z = max(lam, mu) * elapsed + 1
    P = [[I(1 - (lam * elapsed + 1) / z), I(lam * elapsed / z)],
         [I(mu * elapsed / z), I(1 - (mu * elapsed + 1) / z)]]
    up = I(1 / z)
    vectors = [[[I(int(j == 0 and state == c)) for state in (0, 1)]
                for j in range(degree + 1)] for c in (0, 1)]
    sums = [[[I(v) for v in block] for block in row] for row in vectors]
    poisson = I(1)
    multiplier = I(1 - z).exp()
    maximum_factorial = I(factorial(degree))
    target = D('1e-' + str(digits - 35))
    for order in range(1, 10000):
        next_vectors = []
        for row in vectors:
            next_row = []
            for j in range(degree + 1):
                v0, v1 = row[j]
                n0 = v0 * P[0][0] + v1 * P[1][0]
                n1 = v0 * P[0][1] + v1 * P[1][1]
                if j:
                    n1 = n1 + row[j - 1][1] * up
                next_row.append([n0, n1])
            next_vectors.append(next_row)
        vectors = next_vectors
        poisson = poisson * I(z / order)
        for c in (0, 1):
            for j in range(degree + 1):
                for d in (0, 1):
                    sums[c][j][d] = sums[c][j][d] + poisson * vectors[c][j][d]
        if order + 2 > z:
            tail = multiplier * poisson * I(z / (order + 1)) / I(1 - z / (order + 2))
            moment_tail = tail * maximum_factorial
            if order >= degree and moment_tail.hi < target:
                break
    else:
        raise RuntimeError('Controller moment uniformization budget exceeded')
    moments = {}
    for c in (0, 1):
        for d in (0, 1):
            row = []
            for j in range(degree + 1):
                value = multiplier * sums[c][j][d] * I(factorial(j))
                row.append(I(value.lo, UP.add(value.hi, (tail * I(factorial(j))).hi)))
            moments[c, d] = row
    return moments, {'banded_dimension':2 * (degree + 1),
                     'retained_initial_controller_rows':2,
                     'positive_uniformization_terms':order + 1,
                     'maximum_moment_absolute_tail_upper':str(moment_tail.hi),
                     'precision_decimal_digits':digits}


def inverse_guess(matrix):
    """Numerical Decimal Gauss-Jordan; the returned guess is verified later."""
    n = len(matrix)
    a = [list(row) + [D(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    for k in range(n):
        pivot = max(range(k, n), key=lambda i:abs(a[i][k]))
        a[k], a[pivot] = a[pivot], a[k]
        divisor = a[k][k]
        if divisor == 0:
            raise ArithmeticError('Numerical moment inverse needs more precision')
        a[k] = [v / divisor for v in a[k]]
        for i in range(n):
            if i != k:
                multiplier = a[i][k]
                a[i] = [x - multiplier * y for x, y in zip(a[i], a[k])]
    return [row[n:] for row in a]


def verified_polynomial(moments, degree):
    """Enclose the monic orthogonal polynomial by an inverse residual.

    For any exact point matrix R and point vector c, if ||I-RH||∞=rho<1,
    then ||c_true-c||∞ <= ||R(b-Hc)||∞/(1-rho).  All products below enclose
    the actual moment matrix.  High-precision inverse guesses carry no trust.
    """
    if degree == 0:
        return [I(1)], {'inverse_residual_norm_upper':'0', 'coefficient_radius_upper':'0'}
    H = [[moments[j + k] for k in range(degree)] for j in range(degree)]
    b = [-moments[degree + j] for j in range(degree)]
    HM = [[v.midpoint() for v in row] for row in H]
    RM = inverse_guess(HM)
    CM = [sum((RM[j][k] * b[k].midpoint() for k in range(degree)), D(0)) for j in range(degree)]
    R = [[I(RM[j][k]) for k in range(degree)] for j in range(degree)]
    C = [I(CM[j]) for j in range(degree)]
    rho = D(0)
    for j in range(degree):
        rownorm = D(0)
        for k in range(degree):
            error = I(int(j == k)) - sum((R[j][l] * H[l][k] for l in range(degree)), I(0))
            rownorm = UP.add(rownorm, error.abs_upper())
        rho = max(rho, rownorm)
    if rho >= 1:
        raise ArithmeticError('Moment inverse not certified; increase precision')
    residual = [b[j] - sum((H[j][k] * C[k] for k in range(degree)), I(0)) for j in range(degree)]
    correction = [sum((R[j][k] * residual[k] for k in range(degree)), I(0)) for j in range(degree)]
    radius = (I(max(v.abs_upper() for v in correction)) / (1 - I(rho))).hi
    coefficients = [I(DOWN.subtract(v.lo, radius), UP.add(v.hi, radius)) for v in C] + [I(1)]
    return coefficients, {'inverse_residual_norm_upper':str(rho),
                          'coefficient_radius_upper':str(radius)}


def inner(a, b, moments, shift=0):
    return sum((x * y * moments[i + j + shift] for i, x in enumerate(a)
                for j, y in enumerate(b)), I(0))


def evaluate(poly, x):
    value = I(0)
    for coefficient in reversed(poly):
        value = value * x + coefficient
    return value


def gauss_guesses(moments, q):
    m = [v.midpoint() for v in moments]
    old, current, oldnorm = [], [D(1)], None
    diagonal, offdiagonal = [], []
    for k in range(q):
        norm = sum(x * y * m[i + j] for i, x in enumerate(current) for j, y in enumerate(current))
        if norm <= 0:
            raise ArithmeticError('Numerical orthogonal-polynomial guess needs more precision')
        alpha = sum(x * y * m[i + j + 1] for i, x in enumerate(current)
                    for j, y in enumerate(current)) / norm
        beta = norm / oldnorm if k else D(0)
        diagonal.append(float(alpha))
        if k:
            offdiagonal.append(float(beta.sqrt()))
        new = [D(0)] * (k + 2)
        for i, value in enumerate(current):
            new[i] -= alpha * value
            new[i + 1] += value
        for i, value in enumerate(old):
            new[i] -= beta * value
        old, current, oldnorm = current, new, norm
    def below(x):
        pivot = diagonal[0] - x
        count = int(pivot < 0)
        for i in range(1, q):
            if abs(pivot) < 1e-250:
                pivot = -1e-250
            pivot = diagonal[i] - x - offdiagonal[i - 1] ** 2 / pivot
            count += int(pivot < 0)
        return count
    guesses = []
    for j in range(q):
        lo, hi = -0.1, 1.1
        for _ in range(55):
            middle = (lo + hi) / 2
            if below(middle) <= j:
                lo = middle
            else:
                hi = middle
        guesses.append((lo + hi) / 2)
    return guesses


def certified_gauss_rule(moments, q):
    poly, info = verified_polynomial(moments, q)
    previous, previous_info = verified_polynomial(moments, q - 1)
    norm = inner(previous, previous, moments)
    if norm.lo <= 0:
        raise ArithmeticError('Orthogonal polynomial norm not resolved')
    derivative = [I(i) * poly[i] for i in range(1, q + 1)]
    pm = [v.midpoint() for v in poly]
    dm = [i * pm[i] for i in range(1, q + 1)]
    def point_eval(p, x):
        value = D(0)
        for a in reversed(p):
            value = value * x + a
        return value
    rule, last_upper = [], D(0)
    for seed in gauss_guesses(moments, q):
        root = D.from_float(seed)
        for _ in range(25):
            step = point_eval(pm, root) / point_eval(dm, root)
            root -= step
            if abs(step) < D('1e-' + str(NEAR.prec // 2)):
                break
        center = root
        width = D('1e-' + str(min(80, NEAR.prec // 3)))
        for _ in range(NEAR.prec):
            lower = DOWN.subtract(center, width)
            upper = UP.add(center, width)
            fl, fu = evaluate(poly, I(lower)), evaluate(poly, I(upper))
            if ((fl.hi < 0 < fu.lo) or (fu.hi < 0 < fl.lo)):
                break
            width = UP.multiply(width, D(10))
        else:
            raise ArithmeticError('Gaussian root not isolated')
        if not last_upper < lower < upper < 1:
            raise ArithmeticError('Gaussian roots not distinct and interior')
        node = I(lower, upper)
        denominator = evaluate(derivative, node) * evaluate(previous, node)
        if denominator.lo <= 0:
            raise ArithmeticError('Positive Gaussian weight denominator unresolved')
        weight = norm / denominator
        if weight.lo <= 0:
            raise ArithmeticError('Positive Gaussian weight unresolved')
        rule.append((node, weight))
        last_upper = upper
    # Degree q, q disjoint sign-changing intervals in (0,1): every true root
    # is isolated, even though the float guesses were not trusted.
    return rule, {'degree':q, 'polynomial':info, 'previous_polynomial':previous_info,
                   'squared_norm_interval':record(norm),
                   'all_roots_certified_distinct_interior':True,
                   'nodes_fraction_intervals':[record(x) for x, w in rule],
                   'weight_intervals':[record(w) for x, w in rule]}


def acquire_kernel(source, event_mark='reaction_0', elapsed=F(1, 2), tolerance=F(1, 10**8)):
    if not 0 < tolerance < 1:
        raise ValueError('Tolerance must be in (0,1)')
    spec = acquire_source(source, event_mark, F(elapsed))
    q, delta, bounds = gaussian_order(spec, tolerance / 2)
    digits = max(200, 5 * q + 100)
    precision(digits)
    moments, moment_info = occupation_moments(spec.lam, spec.mu, spec.elapsed, 2 * q - 1, digits)
    quadratures, terms = {}, []
    numerical_spread = D(1)
    resets = dict(spec.event.component_resets)
    for c in (0, 1):
        for d in (0, 1):
            rule, rule_info = certified_gauss_rule(moments[c, d], q)
            quadratures[f'{c},{d}'] = rule_info
            if not any(spec.event.hazards[d]):
                continue
            for node, weight in rule:
                coefficient = stored_lower(weight)
                ratio = I(weight.hi) / I(coefficient)
                matrices, denominators = [], []
                for i, ((A0, A1), reach) in enumerate(zip(spec.killed, spec.support)):
                    H = exp2([[I(spec.elapsed) * ((1 - node) * I(A0[x][y]) + node * I(A1[x][y]))
                               for y in (0, 1)] for x in (0, 1)])
                    # Preserve zeros by the exact local graph, not a numerical threshold.
                    H = [[H[x][y] if reach[x][y] else I(0) for y in (0, 1)] for x in (0, 1)]
                    if i == spec.event.owner:
                        H = [[H[x][y] * I(spec.event.hazards[d][y]) for y in (0, 1)] for x in (0, 1)]
                    if i in resets:
                        mapping = resets[i]
                        H = [[sum((H[x][z] for z in (0, 1) if mapping[z] == y), I(0))
                              for y in (0, 1)] for x in (0, 1)]
                    lower, local_ratio = [], D(1)
                    for row in H:
                        for value in row:
                            if value.hi == value.lo == 0:
                                lower.append(F(0))
                            else:
                                lo = stored_lower(value)
                                if lo <= 0:
                                    raise ArithmeticError('Positive local kernel entry not resolved')
                                lower.append(lo)
                                local_ratio = max(local_ratio, (I(value.hi) / I(lo)).hi)
                    integers, denominator = integerize(lower)
                    matrices.append([integers[:2], integers[2:]])
                    denominators.append(denominator)
                    ratio = ratio * I(local_ratio)
                numerical_spread = max(numerical_spread, ratio.hi)
                terms.append({'controller_input':c, 'controller_output':spec.event.controller_reset[d],
                              'coefficient':str(coefficient),
                              'local_integer_matrices':[[list(map(str, row)) for row in M] for M in matrices],
                              'local_denominators':list(map(str, denominators))})
    lower = 1 / (1 + delta)
    upper = F(numerical_spread) / (1 - delta)
    spread = upper / lower
    if tv_upper(spread) > I(tolerance).lo:
        raise ArithmeticError('Final combined error exceeds requested tolerance')
    source_record = {'nsites':source.nsites, 'controller':list(source.controller),
                     'rules':[{'name':r.name, 'guard':r.guard, 'update':r.update,
                               'rate':str(r.rate), 'mark':r.mark} for r in source.rules]}
    return {'scientific_object':'recurrent-controller all-input rational marked density operator',
            'new_implementation':True, 'row_convention':True,
            'source':source_record, 'elapsed_time':str(spec.elapsed), 'event_mark':event_mark,
            'controller_site':spec.interface.controller[0],
            'local_component_sites':[list(c.sites) for c in spec.interface.components],
            'operator_definition':'sum_term coefficient * E_controller_input,controller_output tensor product_i(local_integer_matrix/local_denominator)',
            'terms':terms,
            'certificate':{'lower_multiplier_exact':str(lower), 'upper_multiplier_exact':str(upper),
                           'spread_factor_upper_exact':str(spread),
                           'all_input_and_future_selection_TV_upper':str(tv_upper(spread)),
                           'quadrature_relative_error_exact':str(delta),
                           'numerical_spread_upper_exact':str(F(numerical_spread)),
                           'gaussian_nodes_per_controller_pair':q,
                           'positive_product_terms':len(terms),
                           'recurrent_controller_retained':True,
                           'local_killed_commutators_checked_exactly':True,
                           'source_bounds':bounds,
                           'moment_obtaining':moment_info,
                           'quadrature_obtaining':quadratures},
            'scope':'Fixed supplied lag and source parameters; no row normalization. Every approximate reuse pays its relative spread. Repeated mixture width can grow. Local numerical executor is binary; theorem admits finite local blocks.'}


def recurrent_clock_source(n=24, lam=F(7, 10), mu=F(11, 10), clocks=(F(1, 4), F(1))):
    rules = [Rule('controller_01', ((0, 0),), ((0, 1),), lam),
             Rule('controller_10', ((0, 1),), ((0, 0),), mu)]
    factors = []
    for i in range(n):
        site = i + 1
        alpha, beta, kappa = F(3, 5) + F(i, 100), F(2, 5) + F(i % 5, 50), F(3, 2) + F(i % 3, 10)
        for c, speed in enumerate(clocks):
            rules.extend((Rule(f'up_{i}_{c}', ((0, c), (site, 0)), ((site, 1),), speed * alpha),
                          Rule(f'down_{i}_{c}', ((0, c), (site, 1)), ((site, 0),), speed * beta),
                          Rule(f'event_{i}_{c}', ((0, c), (site, 1)), ((site, 0),), speed * kappa, f'reaction_{i}')))
        factors.append(InitialFactor((site,), (F(1, 2), F(1, 2))))
    return Program(n + 1, (0,), tuple(rules),
                   (InitialBranch(F(1), ((0, 0),), tuple(factors)),))


def full_reference(source, event_mark, elapsed, terms=150):
    """Independent small expansion, used only as a numerical semantic check."""
    states = list(product((0, 1), repeat=source.nsites))
    index = {state:i for i, state in enumerate(states)}
    dim = len(states)
    A, J = [[[F(0) for _ in states] for _ in states] for _ in range(2)]
    for x, state in enumerate(states):
        env = dict(enumerate(state))
        for rule in source.rules:
            if all(env[site] == bit for site, bit in rule.guard):
                dest = env | dict(rule.update)
                y = index[tuple(dest[i] for i in range(source.nsites))]
                if rule.mark is None:
                    if x != y:
                        A[x][y] += rule.rate
                        A[x][x] -= rule.rate
                else:
                    A[x][x] -= rule.rate
                    if rule.mark == event_mark:
                        J[x][y] += rule.rate
    rate = max(-A[x][x] for x in range(dim))
    P = [[I(int(x == y) + A[x][y] / rate) for y in range(dim)] for x in range(dim)]
    power = [[I(int(x == y)) for y in range(dim)] for x in range(dim)]
    total = [[I(v) for v in row] for row in power]
    z, weight = rate * elapsed, I(1)
    for k in range(1, terms + 1):
        power = matmul(power, P)
        weight = weight * I(z / k)
        total = [[total[x][y] + weight * power[x][y] for y in range(dim)] for x in range(dim)]
    scalar = (-I(z)).exp()
    tail = scalar * weight * I(z / (terms + 1)) / I(1 - z / (terms + 2))
    E = [[I((scalar * v).lo, UP.add((scalar * v).hi, tail.hi)) for v in row] for row in total]
    return matmul(E, [[I(v) for v in row] for row in J]), states, tail


def evaluated_entry(kernel, source_state, destination_state):
    answer = F(0)
    controller_site = kernel['controller_site']
    for term in kernel['terms']:
        if source_state[controller_site] != term['controller_input'] or destination_state[controller_site] != term['controller_output']:
            continue
        value = F(term['coefficient'])
        for i, (matrix, denominator) in enumerate(zip(term['local_integer_matrices'], term['local_denominators'])):
            site = kernel['local_component_sites'][i][0]
            value *= F(int(matrix[source_state[site]][destination_state[site]]), int(denominator))
        answer += value
    return answer


def apply_product_mixture(kernel, weights, controller_rows, local_rows):
    """Exact rational contraction on a correlated positive product mixture.

    The branch index can encode any supplied inter-module/controller
    correlation.  No separate row normalization of the event operator is
    performed.  Returned mixture normalization uses one global density.
    Its width can grow by the actual number of operator terms; no truncation
    or unproved compression occurs here.  All rows use retained local order.
    """
    weights = list(map(F, weights))
    controller_rows = [list(map(F, row)) for row in controller_rows]
    local_rows = [[list(map(F, row)) for row in branch] for branch in local_rows]
    n = len(kernel['local_component_sites'])
    if (not weights or len(weights) != len(controller_rows) or len(weights) != len(local_rows)
            or min(weights) < 0 or sum(weights, F(0)) != 1):
        raise ValueError('Invalid normalized mixture weights')
    if any(len(row) != 2 or min(row) < 0 or sum(row, F(0)) != 1 for row in controller_rows):
        raise ValueError('Invalid controller probability row')
    if any(len(branch) != n or any(len(row) != 2 or min(row) < 0 or sum(row, F(0)) != 1
                                   for row in branch) for branch in local_rows):
        raise ValueError('Invalid local probability row')
    raw_weights, controllers, leaves = [], [], []
    for w, crow, branch in zip(weights, controller_rows, local_rows):
        for term in kernel['terms']:
            scalar = w * crow[term['controller_input']] * F(term['coefficient'])
            if scalar == 0:
                continue
            output = []
            for row, matrix, denominator in zip(branch, term['local_integer_matrices'], term['local_denominators']):
                new = [sum((row[x] * F(int(matrix[x][y]), int(denominator)) for x in (0, 1)), F(0)) for y in (0, 1)]
                mass = sum(new, F(0))
                scalar *= mass
                if scalar == 0:
                    break
                output.append([v / mass for v in new])
            if scalar:
                raw_weights.append(scalar)
                controllers.append([F(int(c == term['controller_output'])) for c in (0, 1)])
                leaves.append(output)
    normalizer = sum(raw_weights, F(0))
    if normalizer == 0:
        raise ValueError('The requested event has zero density for this entrance')
    return {'weights':[w / normalizer for w in raw_weights],
            'controller_rows':controllers, 'local_rows':leaves,
            'event_density':normalizer,
            'additional_spread':F(kernel['certificate']['spread_factor_upper_exact'])}


def check_small():
    source = recurrent_clock_source(2)
    kernel = acquire_kernel(source, elapsed=F(1, 2), tolerance=F(1, 10**9))
    reference, states, tail = full_reference(source, 'reaction_0', F(1, 2))
    a = F(kernel['certificate']['lower_multiplier_exact'])
    b = F(kernel['certificate']['upper_multiplier_exact'])
    positive, zeros = 0, 0
    ratios = []
    for x, sx in enumerate(states):
        for y, sy in enumerate(states):
            value = evaluated_entry(kernel, sx, sy)
            if sy[1] == 1:
                assert value == 0 and reference[x][y].hi == 0
                zeros += 1
            else:
                lower, upper = I(a * value), I(b * value)
                assert lower.lo <= reference[x][y].lo <= reference[x][y].hi <= upper.hi
                positive += 1
                ratios.append((reference[x][y] / I(value)).midpoint())
    # A nearby source changes only killing in one phase: killed commutation
    # fails even though the original silent generators still commute.
    altered = tuple(replace(r, rate=r.rate + F(1, 7)) if r.name == 'event_0_0' else r for r in source.rules)
    try:
        acquire_source(replace(source, rules=altered), 'reaction_0', F(1, 2))
    except SourceError as error:
        assert error.category == 'occupation_noncommuting_killed_generators'
        rejection = error.category
    else:
        raise AssertionError('Noncommuting killed source was accepted')
    # Actual sequential application: arbitrary correlated entrance, two
    # recorded events, and the retained controller is NEVER reset externally.
    weights = [F(2, 5), F(3, 5)]
    controllers = [[F(1), F(0)], [F(0), F(1)]]
    leaves = [[[F(4, 5), F(1, 5)], [F(1, 3), F(2, 3)]],
              [[F(1, 4), F(3, 4)], [F(5, 6), F(1, 6)]]]
    initial = [sum((w * c[s[0]] * rows[0][s[1]] * rows[1][s[2]]
                    for w, c, rows in zip(weights, controllers, leaves)), F(0)) for s in states]
    first = apply_product_mixture(kernel, weights, controllers, leaves)
    second = apply_product_mixture(kernel, first['weights'], first['controller_rows'], first['local_rows'])
    record_density = first['event_density'] * second['event_density']
    fullrow = matmul(matmul([[I(v) for v in initial]], reference), reference)[0]
    reference_mass = sum(fullrow, I(0))
    assert I(a * a * record_density).lo <= reference_mass.lo <= reference_mass.hi <= I(b * b * record_density).hi
    final_controller_one = sum((w * c[1] for w, c in zip(second['weights'], second['controller_rows'])), F(0))
    reference_posterior = sum((value for value, s in zip(fullrow, states) if s[0]), I(0)) / reference_mass
    radius = I(tv_upper(F(kernel['certificate']['spread_factor_upper_exact']) ** 2))
    assert (I(final_controller_one) - radius).lo <= reference_posterior.lo
    assert reference_posterior.hi <= (I(final_controller_one) + radius).hi
    return {'expanded_states':len(states), 'positive_entries_contained':positive,
            'structural_zero_entries_exact':zeros, 'reference_uniformization_tail_upper':str(tail.hi),
            'ratio_midpoint_min':str(min(ratios)), 'ratio_midpoint_max':str(max(ratios)),
            'killed_not_only_silent_commutation_rejection':rejection,
            'all_controller_input_and_output_states_checked':True,
            'two_event_reuse_without_controller_reset':{
                'initial_correlated_mixture_terms':2,
                'first_output_terms':len(first['weights']),
                'second_output_terms':len(second['weights']),
                'joint_event_density_midpoint':str(I(record_density).midpoint()),
                'controller_one_posterior_midpoint':str(I(final_controller_one).midpoint()),
                'whole_posterior_TV_upper':str(radius.hi),
                'independent_full_reference_contained':True}}


def run(n=24):
    started = time.perf_counter()
    source = recurrent_clock_source(n)
    kernel = acquire_kernel(source)
    kernel_file = Path(f'recurrent_occupation_kernel_{n}sites.json')
    kernel_file.write_text(json.dumps(kernel, separators=(',', ':')))
    # Reading and exact decoding check the saved operator, rather than only
    # its transient in-memory construction.  The full certificate is retained.
    loaded = json.loads(kernel_file.read_text())
    assert evaluated_entry(loaded, (0,) * (n + 1), (0,) * (n + 1)) > 0
    small = check_small()
    result = {'new_implementation':True, 'source_rules':len(source.rules),
              'local_modules':n, 'nominal_global_configurations':str(2 ** (n + 1)),
              'operator_file':str(kernel_file),
              'positive_product_terms':kernel['certificate']['positive_product_terms'],
              'gaussian_nodes_per_controller_pair':kernel['certificate']['gaussian_nodes_per_controller_pair'],
              'all_input_and_future_selection_TV_upper':kernel['certificate']['all_input_and_future_selection_TV_upper'],
              'moment_obtaining':kernel['certificate']['moment_obtaining'],
              'small_independent_expanded_reference':small,
              'source_scope':'autonomous recurrent controller; phase clock speeds1/4 and1 scale silent and event rates; exact killed commutation; arbitrary runtime entrance law',
              'retained_controller_requires_no_external_reset':True,
              'quadrature_labels_are_not_claimed_physical_occupation_samples':True,
              'elapsed_seconds':time.perf_counter() - started}
    Path('recurrent_occupation_kernel_results.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sites', type=int, default=24)
    arguments = parser.parse_args()
    run(arguments.sites)
