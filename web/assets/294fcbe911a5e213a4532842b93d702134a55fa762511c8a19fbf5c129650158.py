"""Tiny exact audit of the XXZ field-lift off-diagonal rank correction."""
from fractions import Fraction as F
from itertools import product

# One field gate: A = I + X, so I + sA = [[1+s, s], [s, 1+s]].
# The lift uses r=b=1,c=0, giving d=s and u=v=1+s.
s = F(1, 3)
d = s
u = 1 + s
v = 1 + s

# Each term is (row exponent x, complemented-column exponent y,
# dummy subset, coefficient) in q1_tilde.
terms = [
    (0, 0, frozenset({0, 1}), d),
    (1, 0, frozenset({0}), u / 2),
    (1, 0, frozenset({1}), u / 2),
    (0, 1, frozenset({0}), v / 2),
    (0, 1, frozenset({1}), v / 2),
    (1, 1, frozenset(), d),
]

def local_terms(row, col):
    """Terms whose x=row and y=1-col reproduce one gate entry."""
    return [term for term in terms if term[0] == row and term[1] == 1 - col]

def open_entry_by_lift(a, b):
    delta = a - b
    f = 2
    p_dummy_rank = f - delta
    q_dummy_rank = f + delta
    assert 0 <= p_dummy_rank <= 2 * f
    assert 0 <= q_dummy_rank <= 2 * f
    assert p_dummy_rank + q_dummy_rank == 2 * f
    total = F(0)
    # Matrix product F F: t is the internal wire bit. Complementing the
    # first gate's column means (1-t)+t=1, exactly the wire constraint.
    for t in (0, 1):
        for _, _, d1, c1 in local_terms(a, t):
            for _, _, d2, c2 in local_terms(t, b):
                selected_dummies = d1 | frozenset(2 + j for j in d2)
                if len(selected_dummies) != p_dummy_rank:
                    continue
                # The partner factor has e_(f+delta) on four dummy variables;
                # its complement to the P dummy set has exactly this rank.
                assert 4 - len(selected_dummies) == q_dummy_rank
                total += c1 * c2
    return total

def direct_entry(a, b):
    # F = [[v,d],[d,u]].
    mat = ((v, d), (d, u))
    return sum(mat[a][t] * mat[t][b] for t in (0, 1))

results = {}
for a, b in product((0, 1), repeat=2):
    lifted = open_entry_by_lift(a, b)
    direct = direct_entry(a, b)
    assert lifted == direct, (a, b, lifted, direct)
    results[f"{a}{b}"] = str(lifted)

# The nonzero charge-changing example is the decisive check: delta=1, so the
# partner rank is f+delta=3, not the trace rank f=2.
assert open_entry_by_lift(1, 0) == F(8, 9)
assert 2 + (1 - 0) == 3
print({"s": str(s), "F_squared_entries": results,
       "offdiagonal_10": results["10"], "partner_dummy_rank_for_10": 3,
       "status": "PASS exact fractions"})
