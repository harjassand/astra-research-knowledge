#!/usr/bin/env python3
"""Exact symbolic CPV source/mapped-block replay, not a finite grid.

Dependency: SymPy. Imported source: arXiv2110.03521, Eq18.
Physical map: sol_semiclassical_memory/wall_su3/MISSING_LABEL_MAPPING.txt.
No eigenvalue computation, solver status or external validation inferred.
"""
import sympy as sp

N, k = sp.symbols('N k', positive=True, integer=True)
c = sp.symbols('c', positive=True)
C2 = (N + 1)**2 / 3
C3 = (N - 2) * (N + 1) * (N + 4) / 9
alpha = C3 / C2


def cpv(xi, lam, size):
    """Literal source Eq18 with xi_b=0 for these physical blocks."""
    X, Y = sp.zeros(size), sp.zeros(size)
    lp = lam / 2 + sum(xi) / 6
    lm = -lam / 2 + sum(xi) / 6
    for j in range(1, size + 1):
        e = {r: sum((z - j + sp.Rational(1, 2))**r for z in xi)
             for r in (1, 2, 3, 4)}
        X[j-1, j-1] = sp.expand(
            -(sp.Rational(7, 2)*e[1]**3 - 18*e[1]*e[2] + 18*e[3])/108
            - e[1]*(lam**2+2)/24)
        Y[j-1, j-1] = sp.expand(
            (sp.Rational(5, 2)*e[1]**4 + 32*e[1]*e[3]
             + 6*(e[2]**2 - 3*e[1]**2*e[2] - 4*e[4])
             + 6*e[2]*(lam**2+2) - 3*e[1]**2*(lam**2-2)
             - sp.Rational(3, 2)*lam**4 + 6*lam**2 - 36)/288)
        if j < size:
            X[j-1, j] = sp.prod(j-z for z in xi[:3])
            X[j, j-1] = sp.prod(j-z for z in xi[3:])
            Y[j-1, j] = X[j-1, j] * (j-lm)
            Y[j, j-1] = X[j, j-1] * (j-lp)
    return X, Y


def mapped(xi, lam, size, casimir):
    X, Y = cpv(xi, lam, size)
    I = sp.eye(size)
    Q = (X + (2*C3/3-alpha*casimir)*I)/N
    LS = (-Y-casimir**2*I/12
          + (C2/3+sp.Rational(1, 4)-alpha**2)*casimir*I
          - 2*alpha*N*Q)/N**2
    return Q, LS


def equal(x, y):
    assert sp.cancel(x-y) == 0, sp.factor(x-y)


diag_c = k*(k+2)
Q, LS = mapped([N+1-k, sp.Integer(2), sp.Integer(2),
                1-k, 1-k, sp.Integer(0)], N+k+3, 2, diag_c)
A = N**4+4*N**3-66*N**2-140*N+1225
B = (24*N**6+144*N**5+504*N**4+1056*N**3
     -504*N**2-2736*N-1560)
trq = -2*(N+1)/N+6*c/(N*(N+1))
detq = -c*((1-36/(N+1)**2)*c+24)/(4*N**2)
trls = (4*N**4+16*N**3+(N**2+2*N+37)*c-32*N-20)/(2*N**2*(N+1)**2)
detls = c*(B+A*c)/(16*N**4*(N+1)**4)
mixed = 3*c*(3*N**4+12*N**3-18*N**2-60*N-33
             -(N**2+2*N-35)*c)/(2*N**3*(N+1)**3)
for lhs, rhs in ((sp.trace(Q), trq), (Q.det(), detq),
                 (sp.trace(LS), trls), (LS.det(), detls),
                 (sp.trace(LS)*sp.trace(Q)-sp.trace(LS*Q), mixed)):
    equal(lhs, rhs.subs(c, diag_c))

off_c = (k+2)*(k+3)
Qoff, LSoff = mapped([N-k-1, sp.Integer(2), sp.Integer(1),
                     -k, -k-1, sp.Integer(0)], N+k+5, 1, off_c)
equal(Qoff[0, 0], -2*(N+1)/N+3*off_c/(N*(N+1)))
equal(LSoff[0, 0], (8*N**4+32*N**3-64*N-40
                    -(N**2+2*N-35)*off_c)/(4*N**2*(N+1)**2))
# The conjugate offdiagonal swaps xi4,xi5 and leaves both diagonal sums.
Qbar, LSbar = mapped([N-k-1, sp.Integer(2), sp.Integer(1),
                     -k-1, -k, sp.Integer(0)], N+k+5, 1, off_c)
equal(Qbar[0, 0], Qoff[0, 0])
equal(LSbar[0, 0], LSoff[0, 0])

Qtop, LStop = mapped([sp.Integer(1), sp.Integer(2), sp.Integer(2),
                     1-N, 1-N, sp.Integer(0)], 2*N+3, 1, N*(N+2))
equal(Qtop[0, 0], -(N-1)*(N-2)*(N+2)/(2*N*(N+1)))

# Exact whole-character dimension sum; symbolic finite-sum identity.
j = sp.symbols('j', nonnegative=True, integer=True)
total = (1+2*sp.summation((j+1)**3, (j, 1, N-1))+(N+1)**3
         + sp.summation((j+4)*(j+1)*(2*j+5), (j, 0, N-2)))
equal(total, (N*(N+2))**2)

print('PASS: exact symbolic CPV diagonal/offdiagonal/top blocks and dimension sum')
print('Scope: algebra replay only; physical metric, analytic PSD/count and actual Choi proof are in WALL_B1_ACTUAL_COMPATIBILITY_PROOF.txt')
