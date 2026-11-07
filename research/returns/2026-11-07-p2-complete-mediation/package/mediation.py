"""Fixed-budget rational classical trajectories; see REPORT.md for the error contract."""
from fractions import Fraction

def compiler_budget(n, trace_R, local_h_bound, time, epsilon):
    """Exact conservative bound for an exactly factored feasible generator.

    Allocates epsilon/2 to time discretization; the other half is available
    for finite arithmetic/local-channel compilation. No fast-forwarding claim.
    """
    K = 3 * n
    tr, H, t, e = map(Fraction, [trace_R, local_h_bound, time, epsilon])
    if n < 1 or tr < 0 or H < 0 or (t < 0) or (not 0 < e < 1):
        raise ValueError('Invalid contract')
    W = 8 + 8 * K * (1 + tr) + 2 * H
    ceil = lambda z: (z.numerator + z.denominator - 1) // z.denominator
    m = max(1, ceil(32 * W * W * t), ceil(8192 * W ** 4 * t * t / e))
    return {'W': str(W), 'steps': m, 'time_step': str(t / m), 'discretization_bound': str(4096 * W ** 4 * t * t / m), 'weak_measurements': K * m, 'shared_random_bits': K * m, 'broadcast_outcome_bits': K * m, 'broadcast_shared_random_bits': K * m, 'point_to_point_delivered_bits_bound': 2 * n * K * m}

def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), Fraction(0))

def cross(x, y):
    return [x[1] * y[2] - x[2] * y[1], x[2] * y[0] - x[0] * y[2], x[0] * y[1] - x[1] * y[0]]

def round_bloch(r, p):
    """Rational PSD-preserving rounding; trace error at most 5*2**(-p)."""
    scale = 1 << p
    v = [Fraction(x.numerator * scale // x.denominator, scale) for x in r]
    return [x / Fraction(scale + 3, scale) for x in v]

def cayley_bloch(r, y, s):
    denom = 1 + s * s * dot(y, y) / 4
    a = (1 - s * s * dot(y, y) / 4) / denom
    c = [s * x / denom for x in y]
    cr = cross(c, r)
    d = dot(c, r)
    return [(a * a - dot(c, c)) * r[i] + 2 * c[i] * d - 2 * a * cr[i] for i in range(3)]

def binary_measure_bloch(r, b, s, p, rng):
    """One exact-form rational instrument with a p-bit outcome coin.

    The only approximation here is flooring the outcome probability; the
    subsequent state is the exact Born update for the chosen outcome, then
    PSD-preserving rounded. Fixed-budget probability error <=2**(-p).
    """
    b2 = dot(b, b)
    br = dot(b, r)
    pplus = (1 + s * s * b2 + 2 * s * br) / (2 * (1 + s * s * b2))
    scale = 1 << p
    threshold = pplus.numerator * scale // pplus.denominator
    xi = 1 if rng.getrandbits(p) < threshold else -1
    denom = 1 + s * s * b2 + 2 * s * xi * br
    if denom <= 0:
        raise ValueError('Step too large or invalid input state')
    out = [((1 - s * s * b2) * r[i] + 2 * s * xi * b[i] + 2 * s * s * br * b[i]) / denom for i in range(3)]
    return (xi, round_bloch(out, p))

def trajectory_z_sample(V, F, G, n, states, local_fields, s, steps, p, rng):
    """Fixed-budget rational trajectory, followed by all-site Z readout.

    V is block diagonal with exactly three columns/site. F has 3n columns;
    G has any explicitly listed number. All scalar inputs are Fractions.
    The caller supplies the certified steps/precision from REPORT.md; this
    routine never claims an error bound merely from running a short demo.
    """
    K = 3 * n
    V, F, G = [[[Fraction(z) for z in row] for row in M] for M in [V, F, G]]
    states = [[Fraction(z) for z in r] for r in states]
    fields = [[Fraction(z) for z in r] for r in local_fields]
    s = Fraction(s)
    h = s * s
    if any((dot(r, r) > 1 for r in states)):
        raise ValueError('Bloch vector outside the unit ball')
    if any((V[a][k] for a in range(K) for k in range(K) if a // 3 != k // 3)):
        raise ValueError('Measurement columns are not local')
    for _ in range(steps):
        xi = []
        for k in range(K):
            i = k // 3
            b = [V[3 * i + a][k] for a in range(3)]
            sign, states[i] = binary_measure_bloch(states[i], b, s, p, rng)
            xi.append(sign)
        eta = [2 * rng.getrandbits(1) - 1 for _ in range(len(G[0]))]
        y = [sum((F[a][j] * xi[j] for j in range(K))) + sum((G[a][j] * eta[j] for j in range(len(eta)))) for a in range(K)]
        for i in range(n):
            states[i] = round_bloch(cayley_bloch(states[i], y[3 * i:3 * i + 3], s), p)
            if any(fields[i]):
                states[i] = round_bloch(cayley_bloch(states[i], fields[i], -h), p)
    out = []
    scale = 1 << p
    for r in states:
        pp = (1 + r[2]) / 2
        threshold = pp.numerator * scale // pp.denominator
        out.append(0 if rng.getrandbits(p) < threshold else 1)
    return (out, states)
