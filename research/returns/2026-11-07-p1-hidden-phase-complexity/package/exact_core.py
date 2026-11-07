"""Rational construction and certified branch compiler.

No source experiments, hidden-state oracle, floating arithmetic or optimization
oracle are used by this module. See RESEARCH_REPORT.txt for the full proof and
the input/channel distinction. Python 3.10+ standard library only.
"""
from fractions import Fraction as F
from math import isqrt


def ceil_sqrt(n):
    assert isinstance(n, int) and n >= 1
    r = isqrt(n)
    return r if r * r == n else r + 1


def ceil_log2_fraction(x):
    x = F(x)
    if x <= 1:
        return 0
    k = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    if F(1 << k) < x:
        k += 1
    return k


def coupling(n):
    return F(1, 10 * ceil_sqrt(n))


def zero_matrix(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def graph_laplacian(n, edges, scale=F(1)):
    L = zero_matrix(n)
    seen = set()
    for i, j in edges:
        assert 0 <= i < j < n and (i, j) not in seen
        seen.add((i, j))
        L[i][i] += scale
        L[j][j] += scale
        L[i][j] -= scale
        L[j][i] -= scale
    return L


def partition_laplacian(groups):
    assert groups and all(isinstance(m, int) and m > 0 for m in groups)
    n = sum(groups)
    L = zero_matrix(n)
    off = 0
    for m in groups:
        for i in range(off, off + m):
            for j in range(off, off + m):
                L[i][j] = 3 * (F(i == j) - F(1, m))
        off += m
    return L


def source_matrix(L):
    n = len(L)
    a = coupling(n)
    K = zero_matrix(n + 1)
    K[0][0] = F(4)
    for i in range(n):
        K[0][i + 1] = K[i + 1][0] = -a
        for j in range(n):
            K[i + 1][j + 1] = L[i][j] + F(i == j)
    return K


def check_laplacian(L, weak=False):
    n = len(L)
    assert all(len(row) == n for row in L)
    assert all(isinstance(v, (int, F)) for row in L for v in row)
    for i in range(n):
        assert sum(L[i]) == 0
        for j in range(n):
            assert L[i][j] == L[j][i]
            if i != j:
                assert L[i][j] <= 0
        if weak:
            assert L[i][i] <= F(1, 100)
    return True


def check_quotient(L):
    """Exact rational K T = T R, with T=(e0, hidden ones)."""
    check_laplacian(L)
    n = len(L)
    a = coupling(n)
    K = source_matrix(L)
    T = [[F(1), F(0)]] + [[F(0), F(1)] for _ in range(n)]
    R = [[F(4), -a * n], [-a, F(1)]]
    for i in range(n + 1):
        for b in range(2):
            assert sum(K[i][j] * T[j][b] for j in range(n + 1)) == sum(
                T[i][c] * R[c][b] for c in range(2)
            )
    assert a * a * n <= F(1, 100)
    return R


def bisect_root(t, R, tolerance):
    """Inverse of 2z+z^3; every comparison is exact."""
    lo, hi = -R, R
    assert 2 * lo + lo**3 <= t <= 2 * hi + hi**3
    steps = 0
    while hi - lo > 2 * tolerance:
        mid = (lo + hi) / 2
        if 2 * mid + mid**3 < t:
            lo = mid
        else:
            hi = mid
        steps += 1
    return (lo + hi) / 2, steps


def bisect_branch(t, label, tolerance):
    """Inverse branch of x^3-x on I_-, I_0, or I_+."""
    assert label in (-1, 0, 1)
    lo, hi = F(10 * label - 1, 10), F(10 * label + 1, 10)
    increasing = label != 0
    flo, fhi = lo**3 - lo, hi**3 - hi
    assert min(flo, fhi) <= t <= max(flo, fhi)
    steps = 0
    while hi - lo > 2 * tolerance:
        mid = (lo + hi) / 2
        fm = mid**3 - mid
        if (fm < t) == increasing:
            lo = mid
        else:
            hi = mid
        steps += 1
    return (lo + hi) / 2, steps


def compile_phase(labels, epsilon, *, L=None, groups=None, expand_physical=False):
    """Compute a specified stationary phase, with a rational norm-error bound.

    Weak case: supply the full rational Laplacian L with weighted degree <= .01.
    Partition case: supply positive group sizes; labels has one entry per group.
    A zero label names the middle branch (a saddle direction), not a minimum.
    A binary group-size input is returned compactly unless expand_physical=True.
    Full expansion costs at least sum(groups)+1 output entries and is charged
    separately. Weak-graph inputs already give all n coordinates explicitly.
    """
    labels = tuple(labels)
    epsilon = F(epsilon)
    assert 0 < epsilon <= F(1, 100)
    assert labels and all(s in (-1, 0, 1) for s in labels)
    if groups is not None:
        assert L is None
        weights = tuple(groups)
        assert len(weights) == len(labels) and all(isinstance(m, int) and m >= 1 for m in weights)
        A = zero_matrix(len(labels))
    else:
        assert L is not None and len(L) == len(labels)
        check_laplacian(L, weak=True)
        weights = (1,) * len(labels)
        A = L
    n = sum(weights)
    a = coupling(n)
    R = F(11, 20) * a * n
    delta = epsilon / (32 * (n + 1))
    steps = ceil_log2_fraction(1 / delta)
    x = list(map(F, labels))
    bisections = 0
    for _ in range(steps):
        z, used = bisect_root(a * sum(m * b for m, b in zip(weights, x)), R, delta)
        bisections += used
        new_x = []
        for i, label in enumerate(labels):
            t = a * z - sum(A[i][j] * x[j] for j in range(len(x)))
            v, used = bisect_branch(t, label, delta)
            bisections += used
            new_x.append(v)
        x = new_x
    z, used = bisect_root(a * sum(m * b for m, b in zip(weights, x)), R, delta)
    bisections += used
    q = F(1, 32)
    leaf_error = F(1, 5) * q**steps + 2 * delta / (1 - q)
    root_error = a * n * leaf_error / 2 + delta
    norm_error = n * leaf_error + root_error
    assert norm_error <= epsilon
    physical = None
    if groups is None or expand_physical:
        physical = [z]
        for m, v in zip(weights, x):
            physical.extend([v] * m)
    return {
        'X': physical, 'root': z, 'group_values': x, 'multiplicities': weights,
        'norm_error_bound': norm_error,
        'leaf_infinity_error_bound': leaf_error, 'outer_iterations': steps,
        'scalar_bisection_steps': bisections, 'delta': delta,
        'morse_index': sum(s == 0 for s in labels),
    }


def energy_and_gradient(X, L):
    z, x = X[0], X[1:]
    n = len(x)
    a = coupling(n)
    Lx = [sum(L[i][j] * x[j] for j in range(n)) for i in range(n)]
    E = z*z + z**4/4 + sum(v**4/4 - v*v/2 for v in x)
    E += sum(x[i] * Lx[i] for i in range(n))/2 - a*z*sum(x)
    grad = [2*z + z**3 - a*sum(x)]
    grad.extend(x[i]**3 - x[i] + Lx[i] - a*z for i in range(n))
    return E, grad


def minimum_certificate(X, L, labels):
    """Residual certificate; existence/uniqueness is supplied by the theorem."""
    assert len(X) == len(labels) + 1
    assert all(s in (-1, 1) for s in labels)
    assert all(F(9, 10) <= s*x <= F(11, 10) for s, x in zip(labels, X[1:]))
    E, grad = energy_and_gradient(X, L)
    l1 = sum(abs(g) for g in grad)
    radius = F(5, 7) * l1
    # Strong convexity yields E(X)-E(X*) <= ||grad||_2^2/(2m).
    gap = F(5, 14) * sum(g*g for g in grad)
    return {'distance_bound': radius, 'energy': E, 'energy_gap_bound': gap}


def cut_size(edges, labels):
    return sum(labels[i] != labels[j] for i, j in edges)


def fixed_mean_bounds(n, edges, bisection):
    assert n % 2 == 0 and n >= 2
    degrees = [0] * n
    for i, j in edges:
        degrees[i] += 1
        degrees[j] += 1
    Delta = max(degrees, default=0)
    lam = F(1, 64*n**4)
    correction = 4 * lam**2 * n * Delta**2
    upper = 2 * lam * bisection
    assert correction <= lam/F(16*n)
    return {'lambda': lam, 'Delta': Delta, 'lower': upper-correction,
            'upper': upper, 'approximation_tolerance': lam/4,
            'cut_recovery_margin': F(1, 2) - (correction + lam/4)/(2*lam)}
