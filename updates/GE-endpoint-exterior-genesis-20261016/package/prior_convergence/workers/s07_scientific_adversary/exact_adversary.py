"""Exact finite-frequency tests for selective-sink inversion boundaries."""

import sympy as sp


def signal(A, b, D, u, s):
    n = A.rows
    return sp.factor(1 - s * (sp.ones(1, n) * (s * sp.eye(n) - A + u * D).inv() * b)[0])


def invert_two_dose(table, b, ss, us):
    n = len(table)
    u1, u2 = us
    F = sp.zeros(n, n)
    H = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            p1, p2 = table[i][0][j], table[i][1][j]
            q1, q2 = p1 / u1, p2 / u2
            F[i, j] = sp.factor((u2-u1)*q1*q2/(u2*q2-u1*q1))
            H[i, j] = sp.factor((q1-q2)/(u2*q2-u1*q1))
    w = F.T.inv() * sp.Matrix([1/s for s in ss])
    X = sp.diag(*w) * F
    Ahat = sp.simplify((X * sp.diag(*ss) - b * sp.ones(1, n)) * X.inv())
    khat = sp.diag(*[1/x for x in w])
    return F, H, Ahat, khat


def main():
    A = sp.Matrix([[-2, 3], [2, -3]])
    b = sp.Matrix([1, 0])
    ss = [sp.Integer(1), sp.Integer(2)]
    us = [sp.Integer(1), sp.Integer(2)]
    eps = sp.Rational(1, 4)
    D = [sp.diag(1, 0), sp.diag(eps, 1)]
    table = [[[signal(A, b, D[i], u, s) for s in ss] for u in us]
             for i in range(2)]
    F, H, Ahat, khat = invert_two_dose(table, b, ss, us)
    residuals = [[[sp.factor(signal(Ahat, b, khat[i, i] * sp.eye(2)[:, i] * sp.eye(2)[i, :], u, s)
                              - table[i][k][j]) for j, s in enumerate(ss)]
                  for k, u in enumerate(us)] for i in range(2)]
    print('A=', A.tolist())
    print('D=', [d.tolist() for d in D])
    print('F=', F.tolist())
    print('H=', H.tolist())
    print('Ahat=', Ahat.tolist())
    print('khat=', khat.diagonal())
    print('residuals=', residuals)
    print('Ahat offdiagonal positive=', Ahat[1, 0] > 0 and Ahat[0, 1] > 0)
    print('khat positive=', all(x > 0 for x in khat.diagonal()))
    assert Ahat[1, 0] > 0 and Ahat[0, 1] > 0
    assert all(x > 0 for x in khat.diagonal())
    assert any(x != 0 for site in residuals for dose in site for x in dose)

    s = sp.Integer(1)
    q = [sp.factor(signal(A, b, D[1], u, s)/u) for u in (1, 2, 3)]
    print('mixed sink 1/q at doses 1,2,3=', [sp.factor(1/x) for x in q])
    print('reciprocal second difference=', sp.factor(1/q[2] - 2/q[1] + 1/q[0]))
    assert sp.factor(1/q[2] - 2/q[1] + 1/q[0]) == -sp.Rational(8, 455)
    print('false inferred target-2 hitting values=',
          [sp.factor(F[1, j]/H[1, j]) for j in range(2)],
          'true=', [sp.Rational(2, 1)/(s+2) for s in ss])

    B = sp.Matrix([[-2, 1, 1], [1, -1, 0], [1, 0, -1]])
    e1 = sp.Matrix([1, 0, 0])
    T = []
    for s in (sp.Integer(1), sp.Integer(2)):
        p = [signal(B, e1, 3*sp.eye(3)[:, 1]*sp.eye(3)[1, :], u, s) for u in us]
        q1, q2 = p[0]/us[0], p[1]/us[1]
        inferred = sp.factor((us[1]-us[0])*q1*q2/(q1-q2))
        G = (s*sp.eye(3)-B).inv()
        expected = sp.factor((G*e1)[1]/G[1, 1])
        assert inferred == expected
        T.append((s, inferred))
    print('first hitting T to branch state 2=', T)
    assert T == [(1, sp.Rational(2, 5)), (2, sp.Rational(3, 11))]
    assert sp.Matrix.hstack(e1, B*e1, B**2*e1).det() == 0

    # A graph-reachable hidden-state refinement is exactly invisible if only
    # the target compartment can be selectively perturbed.  The two hidden
    # states are lumpable for every target dose, despite positive interchange.
    a, out, exchange = sp.Integer(2), sp.Integer(3), sp.Integer(4)
    coarse = sp.Matrix([[-a, out], [a, -out]])
    refined = sp.Matrix([[-a, out, out],
                         [a/2, -out-exchange, exchange],
                         [a/2, exchange, -out-exchange]])
    s, u = sp.symbols('s u', positive=True)
    y2 = (sp.ones(1, 2) * (s*sp.eye(2)-coarse+u*sp.diag(1, 0)).inv()
          * sp.Matrix([1, 0]))[0]
    y3 = (sp.ones(1, 3) * (s*sp.eye(3)-refined+u*sp.diag(1, 0, 0)).inv()
          * sp.Matrix([1, 0, 0]))[0]
    assert sp.cancel(y2-y3) == 0
    print('2-state and reachable 3-state target-only survival:', sp.factor(y2))


if __name__ == '__main__':
    main()
