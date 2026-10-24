"""Exact small-algebra checks for NONFLAT_CYCLIC_CLOCK_COMPILER.txt.

Standard library only. This checks identities with formal involution F,
rational coefficients, and arbitrary-d normalized permutation traces. It
does not replace the endpoint/code argument or the product-clock proof.
"""

from fractions import Fraction as F
from itertools import product


def mat(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


Z = mat([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
I = mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
X = mat([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
C = mat([[0, 0, 1], [0, 0, 1], [1, 1, 0]])


def add(a, b):
    return tuple(tuple(x + y for x, y in zip(ar, br)) for ar, br in zip(a, b))


def scale(a, c):
    return tuple(tuple(c * x for x in row) for row in a)


def mul(a, b):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n))
                       for j in range(n)) for i in range(n))


# A pair (a,b) represents a + b F, where F^2=I and F commutes with clocks.
def p_add(p, q):
    return add(p[0], q[0]), add(p[1], q[1])


def p_scale(p, c):
    return scale(p[0], c), scale(p[1], c)


def p_mul(p, q):
    return (add(mul(p[0], q[0]), mul(p[1], q[1])),
            add(mul(p[0], q[1]), mul(p[1], q[0])))


h0 = (C, X)
h02 = p_mul(h0, h0)
h03 = p_mul(h02, h0)
assert h02 == p_add((scale(I, 2), Z), (X, C))  # F h0 + 2I
assert h03 == p_add(p_scale(h0, 3), (Z, scale(I, 2)))

lam = F(1, 4)
h = (C, add(X, scale(I, lam)))
h2 = p_mul(h, h)
h3 = p_mul(h2, h)
assert h2 == (add(scale(I, 2 + lam * lam), scale(X, 1 + 2 * lam)),
              scale(C, 1 + 2 * lam))
assert h3 == (scale(C, 3 * (1 + lam + lam * lam)),
              add(scale(X, 3 * (1 + lam + lam * lam)),
                  scale(I, 2 + 6 * lam + lam ** 3)))

# After K1 and K2: E X=-lambda, E C=0, E I=1.
variance_scalar = 2 + lam * lam - lam * (1 + 2 * lam)
cubic_swap = 2 + 6 * lam + lam ** 3 - 3 * lam * (1 + lam + lam * lam)
assert variance_scalar == F(27, 16)
assert cubic_swap == (1 - lam) * (2 * lam + 1) * (lam + 2) == F(81, 32)

# Exact isolated revival. At t0=2pi/(3g), energies in units g are:
spectra = {1: (F(9, 4), F(-3, 4), F(-3, 4)),
           -1: (F(3, 4), F(3, 4), F(-9, 4))}
phase_of_minus_i_pi_over_2 = {0: 1, 1: -1j, 2: -1, 3: 1j}
for s, energies in spectra.items():
    phases = []
    for energy in energies:
        multiplier = F(4, 3) * energy  # t0 E = (pi/2) multiplier
        assert multiplier.denominator == 1
        phases.append(phase_of_minus_i_pi_over_2[int(multiplier) % 4])
    assert phases == [1j * s] * 3
assert max(abs(e) for es in spectra.values() for e in es) == F(9, 4)


def compose(p, q):
    """Permutation p after q."""
    return tuple(p[q[i]] for i in range(len(p)))


def transposition(n, a, b):
    p = list(range(n))
    p[a], p[b] = p[b], p[a]
    return tuple(p)


def cycle_count(p):
    seen = set()
    cycles = 0
    for start in range(len(p)):
        if start not in seen:
            cycles += 1
            j = start
            while j not in seen:
                seen.add(j)
                j = p[j]
    return cycles


# For arbitrary local dimension d, normalized trace of a register
# permutation p is d^(cycles(p)-n). Work in Laurent polynomials in d.
def poly_add(*polys):
    out = {}
    for poly in polys:
        for power, coefficient in poly.items():
            out[power] = out.get(power, F(0)) + coefficient
    return {power: c for power, c in out.items() if c}


def trace_poly(p, coefficient=F(1), extra_power=0):
    return {cycle_count(p) - len(p) + extra_power: coefficient}


n = 4  # Union of any two edges has at most four registers; spectators cancel.
all_edges = [(a, b) for a in range(n) for b in range(a + 1, n)]
for e, f in product(all_edges, repeat=2):
    se, sf = transposition(n, *e), transposition(n, *f)
    # T_e = SWAP_e - I/d. Orthogonality is an identity for ALL d.
    gram = poly_add(trace_poly(compose(se, sf)),
                    trace_poly(se, -1, -1),
                    trace_poly(sf, -1, -1), {-2: F(1)})
    assert gram == ({0: F(1), -2: F(-1)} if e == f else {})

# Adjacent SWAPs genuinely fail to commute for every d>=2:
# normalized ||[S,T]||_HS^2 = 2 - 2/d^2 > 0.
s, t = transposition(3, 0, 1), transposition(3, 1, 2)
st, ts = compose(s, t), compose(t, s)
commutator_norm = poly_add({0: F(2)},
                          trace_poly(compose(st, st), -1),
                          trace_poly(compose(ts, ts), -1))
assert commutator_norm == {0: F(2), -2: F(-2)}

# Original/transformed offsets are disjoint for every N>=4: any putative
# modular coincidence would require N to divide one of the nonzero
# integers below, whose absolute values are all at most three.
offset_differences = {a - b for a in (0, -1) for b in (-2, -3)}
assert offset_differences == {1, 2, 3}

# The only index multiplicity patterns for three factors are (3),
# (2,1), (1,1,1). In the last two there is a singleton clock, so the
# product-clock bimodule expectation kills that word once E h_e=0.
patterns = set()
for word in product(range(3), repeat=3):
    counts = tuple(sorted((word.count(e) for e in set(word)), reverse=True))
    patterns.add(counts)
assert patterns == {(3,), (2, 1), (1, 1, 1)}
assert all(1 in pattern for pattern in patterns if pattern != (3,))

print("PASS: exact rational clock identities and isolated +/-i times SWAP revival")
print("PASS: variance=27/16, unavoidable cubic SWAP coefficient=81/32")
print("PASS: arbitrary-d edge Gram = delta_ef (1-d^-2), adjacent commutator=2-2d^-2")
print("PASS: all N>=4 offset separation and cubic singleton-clock combinatorics")
print("Scope: endpoint symmetry and product-clock bimodule argument are mathematical imports,")
print("not numerical claims; within-cell entangled clock pairs remain outside this theorem.")
