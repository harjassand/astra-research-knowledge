"""Exact similarity ambiguity when the intervention may change transitions."""

import sympy as sp


def main():
    A = sp.Matrix([[-2, 3], [2, -3]])
    D = sp.diag(1, 2)
    b = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)])
    c = sp.ones(1, 2)
    T = sp.Matrix([[sp.Rational(9, 10), sp.Rational(1, 10)],
                   [sp.Rational(1, 10), sp.Rational(9, 10)]])
    A2 = T.inv()*A*T
    D2 = T.inv()*D*T
    b2 = T.inv()*b
    M2 = A2-D2
    assert c*T == c and b2 == b
    assert c*A2 == sp.zeros(1, 2)
    assert all(A2[i, j] > 0 for i, j in ((0, 1), (1, 0)))
    assert all(M2[i, j] > 0 for i, j in ((0, 1), (1, 0)))
    assert all(x < 0 for x in c*M2)
    assert D2[0, 1] != 0 and D2[1, 0] != 0
    # Similarity gives equality of every switched word, hence of every
    # on/off pulse response for all nonnegative real durations.
    for i in range(4):
        for j in range(4):
            for k in range(4):
                left = (c*(A-D)**i*A**j*(A-D)**k*b)[0]
                right = (c*M2**i*A2**j*M2**k*b2)[0]
                assert left == right
    print('A alternate=', A2.tolist())
    print('D alternate=', D2.tolist())
    print('M alternate=', M2.tolist())
    print('b alternate=', list(b2))
    print('all pulse words equal by stochastic similarity')

    # On-mode minimality is sufficient for the small Hankel construction,
    # but can fail while switching creates a full reachable/observable span.
    Az = sp.Matrix([[-2, 1], [2, -1]])
    Dz = sp.diag(1, 3)
    Mz = Az-Dz
    bz = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)])
    on_reach = sp.Matrix.hstack(bz, Mz*bz)
    switched_reach = sp.Matrix.hstack(bz, Az*bz)
    on_observe = sp.Matrix.vstack(c, c*Mz)
    assert on_reach.det() == 0
    assert switched_reach.det() == sp.Rational(1, 2)
    assert on_observe.det() == -2
    assert (c*Mz*Az*bz)[0] == -1
    print('on Hankel singular, switched reachable determinant=',
          switched_reach.det(), 'mixed word=', (c*Mz*Az*bz)[0])

    # Simple control and exact minimality do not give uniform numerical
    # recovery on a positive-time grid when transition rates are unbounded.
    r, u = sp.symbols('r u', positive=True)
    Ar = sp.Matrix([[-r, r], [r, -r]])
    Mr = Ar-u*sp.diag(1, 2)
    br = sp.Matrix([1, 0])
    Hr = sp.Matrix.vstack(c, c*Mr) * sp.Matrix.hstack(br, Mr*br)
    assert sp.factor(Hr.det()) == -u*r
    slow = -r-sp.Rational(3, 2)*u+sp.sqrt(r*r+u*u/4)
    fast = -r-sp.Rational(3, 2)*u-sp.sqrt(r*r+u*u/4)
    assert sp.simplify(slow+fast-Mr.trace()) == 0
    assert sp.simplify(slow*fast-Mr.det()) == 0
    assert sp.limit(slow, r, sp.oo) == -sp.Rational(3, 2)*u
    assert sp.limit(fast, r, sp.oo) == -sp.oo
    print('fast-mixing family det H=', sp.factor(Hr.det()),
          'slow eigenvalue limit=', sp.limit(slow, r, sp.oo),
          'fast eigenvalue limit=', sp.limit(fast, r, sp.oo))


if __name__ == '__main__':
    main()
