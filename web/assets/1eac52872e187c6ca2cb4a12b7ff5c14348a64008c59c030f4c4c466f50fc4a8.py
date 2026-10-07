"""Exact bracket checks for the equality-frame reconstruction.

This checks only the finite-dimensional Lie-algebra identifications and the
contact/closed one-form split.  It does not verify the entropy argument or
integrate the frame on a manifold.
"""

import sympy as sp


H, r, c = sp.symbols("H r c", nonzero=True, real=True)
zero = sp.zeros(3, 1)
x = sp.Matrix([1, 0, 0])
u = sp.Matrix([0, 1, 0])
v = sp.Matrix([0, 0, 1])


def bracket(a, b):
    """Bilinear bracket in basis (X, U+, U-)."""
    ax, au, av = a
    bx, bu, bv = b
    return sp.simplify(
        ax * bu * (-H * u)
        + au * bx * (H * u)
        + ax * bv * (H * v)
        + av * bx * (-H * v)
        + au * bv * (c * x)
        + av * bu * (-c * x)
    )


def is_zero(vector):
    return all(sp.simplify(entry) == 0 for entry in vector)


assert is_zero(bracket(x, bracket(u, v))
               + bracket(u, bracket(v, x))
               + bracket(v, bracket(x, u)))

# For c != 0, this is the standard split sl_2 basis:
# [h,E]=2E, [h,F]=-2F, [E,F]=h.
h = -2 * x / H
E = u
F = -2 * v / (c * H)
assert is_zero(bracket(h, E) - 2 * E)
assert is_zero(bracket(h, F) + 2 * F)
assert is_zero(bracket(E, F) - h)

# In the orthonormal frame (e=X/r,U+,U-), the structure constants are
# a=H/r and beta=c*r.  The dual form alpha=e^flat has d alpha(U+,U-)=-beta.
e = x / r
a = H / r
beta = c * r
assert is_zero(bracket(e, u) + a * u)
assert is_zero(bracket(e, v) - a * v)
assert is_zero(bracket(u, v) - beta * e)
alpha_on_x = r  # alpha=e^flat, with e=X/r
assert sp.simplify(-alpha_on_x * bracket(e, u)[0]) == 0
assert sp.simplify(-alpha_on_x * bracket(e, v)[0]) == 0
d_alpha_uv = sp.simplify(-alpha_on_x * bracket(u, v)[0])
assert sp.simplify(d_alpha_uv + beta) == 0
assert sp.simplify(d_alpha_uv.subs(c, 0)) == 0

print({
    "status": "PASS",
    "checks": [
        "Jacobi identity for the equality-frame brackets",
        "nonzero-c branch rescales to sl_2(R)",
        "orthonormal frame has rates H/r and c*r",
        "dual flow form is contact iff c != 0 and closed iff c == 0",
    ],
    "scope": "Exact symbolic bracket algebra only; no dynamical or global proof.",
})
