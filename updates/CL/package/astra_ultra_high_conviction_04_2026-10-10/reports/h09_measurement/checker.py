"""Exact check of the frozen one-port quadratic-response witness."""
import sympy as sp

sqrt2 = sp.sqrt(2)
K = sp.Matrix([[4, 1, 0], [1, 3, 0], [0, 0, 5]])
Q = sp.Matrix([[1, 0, 0], [0, 1 / sqrt2, -1 / sqrt2],
                [0, 1 / sqrt2, 1 / sqrt2]])
Kp = sp.simplify(Q * K * Q.T)
e = sp.Matrix([1, 0, 0])
s = sp.symbols("s")

assert sp.simplify(Q * Q.T - sp.eye(3)) == sp.zeros(3)
assert Q * e == e
assert all(v > 0 for v in [4, 11, 55])  # leading principal minors of K
assert sp.simplify(Kp - sp.Matrix([
    [4, sqrt2 / 2, sqrt2 / 2],
    [sqrt2 / 2, 4, -1],
    [sqrt2 / 2, -1, 4],
])) == sp.zeros(3)

H = sp.simplify((e.T * (s * sp.eye(3) + K).inv() * e)[0])
Hp = sp.simplify((e.T * (s * sp.eye(3) + Kp).inv() * e)[0])
assert sp.simplify(H - Hp) == 0

v = sp.simplify(K.inv() * e)
vp = sp.simplify(Kp.inv() * e)
c2 = sp.simplify(sum(z**3 for z in v))
c2p = sp.simplify(sum(z**3 for z in vp))
gap = sp.simplify(c2p - c2)
assert v == sp.Matrix([sp.Rational(3, 11), -sp.Rational(1, 11), 0])
assert c2 == sp.Rational(26, 1331)
assert c2p == sp.Rational(27, 1331) - sqrt2 / 2662
assert gap == (2 - sqrt2) / 2662
print("linear transfer:", H)
print("K quadratic coefficient:", c2)
print("K' quadratic coefficient:", c2p)
print("positive separation:", gap, "=", sp.N(gap, 12))
