"""Conservative calibration under a KNOWN affine iid-innovation promise.

No optional stopping, source truth verification, clock inference, or quantum
simulation is implemented. Integer labels use coordinate zero as the low bit.
All N transitions, including self loops, must be supplied. Errors in the known
mechanism/transcript format raise ValueError; a statistically valid but too
large bound yields ABORT. An accepted rare misleading transcript is possible.
"""
from fractions import Fraction
from collections import Counter


def rational(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, str, Fraction)):
        raise ValueError(name + ' must be exact int, rational string or Fraction')
    try:
        return Fraction(x)
    except (ValueError, ZeroDivisionError):
        raise ValueError(name + ' is not a finite rational') from None


def matrix(a, name, rows=None, cols=None):
    if not isinstance(a, (list, tuple)) or not a:
        raise ValueError(name + ' must have nonempty rows')
    if any(not isinstance(r, (list, tuple)) for r in a):
        raise ValueError(name + ' must be a matrix')
    width = len(a[0])
    if not width or any(len(r) != width for r in a):
        raise ValueError(name + ' must be rectangular and nonempty')
    if rows is not None and len(a) != rows or cols is not None and width != cols:
        raise ValueError(name + ' has incorrect dimensions')
    if any(type(v) is not int or v not in (0, 1) for r in a for v in r):
        raise ValueError(name + ' entries must be integer bits')
    return [list(r) for r in a]


def rank(a):
    a = [r[:] for r in a]
    row = 0
    for col in range(len(a[0])):
        pivot = next((j for j in range(row, len(a)) if a[j][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        for j in range(row + 1, len(a)):
            if a[j][col]:
                a[j] = [x ^ y for x, y in zip(a[j], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def product(a, b):
    return [[sum(a[i][h] * b[h][j] for h in range(len(b))) % 2
             for j in range(len(b[0]))] for i in range(len(a))]


def matvec(a, x):
    return sum((sum(v * ((x >> j) & 1) for j, v in enumerate(row)) % 2) << i
               for i, row in enumerate(a))


def label(x, n, name):
    if type(x) is not int or not 0 <= x < (1 << n):
        raise ValueError(name + ' must be an n-bit integer')
    return x


def mechanism(F, G, beta):
    F = matrix(F, 'F')
    n = len(F)
    if len(F[0]) != n or rank(F) != n:
        raise ValueError('F must be square and invertible')
    G = matrix(G, 'G', rows=n)
    k = len(G[0])
    if k > n or rank(G) != k:
        raise ValueError('G must be injective')
    label(beta, n, 'beta')
    block, reach = G, [[] for _ in range(n)]
    for m in range(1, n + 1):
        reach = [a + b for a, b in zip(reach, block)]
        if rank(reach) == n:
            return F, G, beta, n, k, m
        block = product(F, block)
    raise ValueError('(F,G) must be controllable')


def recover(G, v):
    n, k = len(G), len(G[0])
    a = [row[:] + [(v >> i) & 1] for i, row in enumerate(G)]
    row = 0
    for col in range(k):
        pivot = next(j for j in range(row, n) if a[j][col])
        a[row], a[pivot] = a[pivot], a[row]
        for j in range(n):
            if j != row and a[j][col]:
                a[j] = [x ^ y for x, y in zip(a[j], a[row])]
        row += 1
    if any(not any(r[:k]) and r[k] for r in a):
        raise ValueError('transition residual is outside im(G)')
    return sum(a[j][k] << j for j in range(k))


def dyadic_confidence_exponent(delta):
    """Smallest nonnegative j with 2^-j <= delta, using integers only."""
    j = max(0, delta.denominator.bit_length() - delta.numerator.bit_length())
    while delta.numerator * (1 << j) < delta.denominator:
        j += 1
    while j and delta.numerator * (1 << (j - 1)) >= delta.denominator:
        j -= 1
    return j


def calibrate(F, G, beta, transitions, *, N, radius, delta, b, T,
              p_slots, epsilon_model):
    F, G, beta, n, k, m = mechanism(F, G, beta)
    if type(N) is not int or N < 1:
        raise ValueError('N must be a precommitted positive integer')
    if type(p_slots) is not int or p_slots < 0:
        raise ValueError('p_slots must be a nonnegative integer')
    radius, delta = rational(radius, 'radius'), rational(delta, 'delta')
    b, T = rational(b, 'b'), rational(T, 'T')
    epsilon_model = rational(epsilon_model, 'epsilon_model')
    if radius <= 0 or not 0 < delta < 1 or b < 0 or T < 0 or epsilon_model <= 0:
        raise ValueError('invalid numerical budget')
    D, j = 1 << k, dyadic_confidence_exponent(delta)
    # 2^D exp(-N radius^2/2) <= 2^(D-floor(N radius^2/2)) <= delta.
    if N * radius * radius < 2 * (D + j):
        raise ValueError('insufficient fixed N for this radius and confidence')
    if not isinstance(transitions, (list, tuple)) or len(transitions) != N:
        raise ValueError('exactly N complete transition pairs required')
    counts = Counter()
    for pair in transitions:
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError('each record must be a transition pair')
        x, y = label(pair[0], n, 'x'), label(pair[1], n, 'y')
        counts[recover(G, y ^ matvec(F, x) ^ beta)] += 1
    # Sparse histogram; missing symbols each contribute 1/D.
    eta_hat = sum((abs(Fraction(c, N) - Fraction(1, D))
                   for c in counts.values()), Fraction(0)) + Fraction(D-len(counts), D)
    upper = min(Fraction(2), eta_hat + radius)
    C = 72 * (p_slots + 1) * m + 4096 * b * b * m * m * T
    target = min(Fraction(1, 4*m), epsilon_model / C)
    passed = upper <= target
    return {'status': 'PASS' if passed else 'ABORT', 'n': n, 'k': k, 'm': m,
            'N': N, 'delta': str(delta), 'confidence_exponent': j,
            'radius': str(radius), 'eta_hat': str(eta_hat),
            'eta_upper': str(upper), 'eta_target': str(target),
            'model_error_upper_if_good': str(C * upper) if passed else None,
            'false_pass_scope': 'unconditional training probability, not posterior',
            'model_promise_verified': False}


def trajectory_pairs(states):
    """Caller guarantees states contains EVERY clock event, including self loops."""
    if not isinstance(states, (list, tuple)) or len(states) < 2:
        raise ValueError('at least two observed states required')
    return list(zip(states[:-1], states[1:]))
