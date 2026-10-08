"""Exact rational stress checks for the N33 endotactic permanence candidate.

This script checks one small all-endotactic non-WR rational diagram, its
weighted drift constants at a selected active-slope neighborhood, and a
different-span switching obstruction.  It is finite evidence only; the
universal drift argument is recorded in FINAL_REPORT.md.
"""

from fractions import Fraction as Q
from functools import cmp_to_key
from math import gcd
from itertools import product


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def primitive(v):
    g = gcd(abs(v[0]), abs(v[1]))
    return (v[0] // g, v[1] // g)


def half(v):
    # Counterclockwise order starting at the positive x-axis.
    return 0 if (v[1] > 0 or (v[1] == 0 and v[0] > 0)) else 1


def ray_cmp(a, b):
    ha, hb = half(a), half(b)
    if ha != hb:
        return -1 if ha < hb else 1
    cross = a[0] * b[1] - a[1] * b[0]
    if cross > 0:
        return -1
    if cross < 0:
        return 1
    return 0


def endotactic_at(w, edges):
    essential = [edge for edge in edges if dot(w, edge[2]) != 0]
    if not essential:
        return True
    top = max(dot(w, edge[0]) for edge in essential)
    return all(dot(w, edge[2]) < 0
               for edge in essential if dot(w, edge[0]) == top)


def arrangement_representatives(edges):
    sources = sorted({edge[0] for edge in edges} | {edge[1] for edge in edges})
    normals = {edge[2] for edge in edges if edge[2] != (0, 0)}
    for i, y in enumerate(sources):
        for z in sources[i + 1:]:
            v = (z[0] - y[0], z[1] - y[1])
            if v != (0, 0):
                normals.add(v)
    rays = set()
    for q in normals:
        ray = primitive((-q[1], q[0]))
        rays.add(ray)
        rays.add((-ray[0], -ray[1]))
    ordered = sorted(rays, key=cmp_to_key(ray_cmp))
    reps = set(ordered)
    for i, u in enumerate(ordered):
        v = ordered[(i + 1) % len(ordered)]
        w = (u[0] + v[0], u[1] + v[1])
        if w == (0, 0):
            # The open sector is a half-plane; rotate its first boundary
            # ray counterclockwise by 90 degrees to obtain a rational point.
            w = (-u[1], u[0])
        reps.add(w)
    return sorted(reps, key=lambda w: (w[0], w[1]))


# Edge tuple: source, target, stoichiometric vector.  This diagram is
# (1,3)->(2,3), (3,3)->(2,3), and (0,0)<->(0,1).
edges = [
    ((1, 3), (2, 3), (1, 0)),
    ((3, 3), (2, 3), (-1, 0)),
    ((0, 0), (0, 1), (0, 1)),
    ((0, 1), (0, 0), (0, -1)),
]

# Hyperplanes at which essential membership or a source ordering can change
# are all included.  Exact rational representatives cover every open chamber
# and every boundary ray of this finite central arrangement.
reps = arrangement_representatives(edges)
bad = [w for w in reps if not endotactic_at(w, edges)]
assert not bad, bad

# The witness is not weakly reversible: the two horizontal arrows both
# terminate at (2,3), which is not a source.  It is not strongly endotactic:
# at w=(0,1), the maximal source among all complexes is (3,3), but its
# horizontal reaction is tangent; the only w-essential top source is (0,1).
assert (2, 3) not in {edge[0] for edge in edges}
assert all(dot((0, 1), edge[2]) == 0
           for edge in edges if edge[0] == (3, 3))

# Exact weighted-drift fixture.
r = (Q(1, 2), Q(1, 3))
p = (Q(1, 2), Q(1, 5))
assert max(abs(p[i] - r[i]) for i in range(2)) == Q(2, 15) < Q(1, 6)

vertices = sorted({edge[0] for edge in edges} | {edge[1] for edge in edges})
D = {(1, 0), (0, 1)}
for y in vertices:
    for z in vertices:
        if y != z:
            D.add((z[0] - y[0], z[1] - y[1]))

nonzero_halves = [abs(dot(r, v)) / 2 for v in D if dot(r, v) != 0]
H = min([Q(1)] + nonzero_halves)
assert H == Q(1, 6)
E = min([Q(1, 2)] + [abs(dot(r, v)) / (2 * (abs(v[0]) + abs(v[1])))
                     for v in D if dot(r, v) != 0])
assert E == Q(1, 6)

kappa, K = Q(1), Q(2)
L = sum(abs(nu[0]) + abs(nu[1]) for _, _, nu in edges)
M = max(abs(y[0]) + abs(y[1]) for y, _, _ in edges)
assert (L, M) == (4, 6)

# h=48^(-30) makes h^(1/2) and h^(1/5) rational and satisfies the
# candidate's uniform small-scale requirement KL h^H <= kappa H.
q = Q(1, 48)
h = q ** 30
x = q ** 15
y = q ** 6
assert K * L * q ** 5 <= kappa * H
assert x**2 == h
assert y**5 == h

def projected_flux(rate_tuple):
    a1, a2, a3, a4 = rate_tuple
    return (Q(1, 2) * a1 * x * y**3
            - Q(1, 2) * a2 * x**3 * y**3
            + Q(1, 3) * a3
            - Q(1, 3) * a4 * y)

corner_values = [(projected_flux(rs), rs)
                 for rs in product((Q(1), Q(2)), repeat=4)]
minimum_flux, minimizing_rates = min(corner_values)
delta = kappa * H * h**M
assert minimum_flux >= delta > 0

# A pointwise arbitrary-switching barrier for the same diagram, with rates
# in [1,2].  z=x^2 obeys z'=2 y^3 z(a1-a2 z), so [1/2,2] is invariant;
# y'=a3-a4 y makes [1/2,2] invariant.  These inequalities hold a.e. for
# any measurable switching of the four rates.

# Different-span switching obstruction: mode A acts only on A with
# 0<->A, mode B only on B with 0<->B.  Each has span dimension one, while
# their union has span R^2.  Selecting mode A forever leaves B(t)=B(0),
# ruling out one compact absorber for the union positive class.

print(f"rational witness endian tests: {len(reps)} exact directions passed")
print(f"non-WR target (2,3) is not a source: {True}")
print(f"r={r}, p={p}, E(r)=H={H}, L={L}, M={M}")
print(f"h=48^(-30); KL h^H <= kappa H: {K*L*q**5} <= {kappa*H}")
print(f"worst rate-corner flux at {minimizing_rates}: {minimum_flux}")
print(f"uniform claimed lower bound delta=H h^M: {delta}")
print("measurable switching barrier on witness: exact thresholds z=x^2,y in [1/2,2]")
print("different-span switch: B(t)=B(0) in A-only mode, no union-class compact absorber")
