#!/usr/bin/env python3
"""Exact calculations for the local lift criterion and its sharp obstruction.

No producer imports, SDP solver, floating point premises, or network.
Requires SymPy. Run with python3 -B lift_criterion.py.
"""
from itertools import product
from pathlib import Path
import json
import sympy as s


def zero(mat):
    return all(s.expand(v) == 0 for v in mat)


def pd(mat):
    return all(s.factor(mat[:j, :j].det()) > 0
               for j in range(1, mat.rows + 1))


def integrate_radially(p, variables, extra_weight=False):
    """Integral p(t*y) dt, optionally with weight (1-t)."""
    poly = s.Poly(s.expand(p), *variables)
    out = 0
    for powers, coeff in poly.terms():
        degree = sum(powers)
        den = (degree + 1) * (degree + 2) if extra_weight else degree + 1
        out += coeff * s.prod(y**j for y, j in zip(variables, powers)) / den
    return s.expand(out)


def taylor_lift(C, variables, corank, tangent_gram=None):
    """Construct C=D.T*M*D with D=diag(y tensor I_corank,I).

    Input finite jet conditions are checked exactly. A supplied Gram is
    checked against the tangent Schur form, not taken on trust.
    """
    n, k, d = C.rows, corank, len(variables)
    r = n - k
    at0 = {y: 0 for y in variables}
    A, B, H = C[:k, :k], C[:k, k:], C[k:, k:]
    assert zero(C - C.T)
    assert zero(A.subs(at0)) and zero(B.subs(at0))
    assert all(zero(A.diff(y).subs(at0)) for y in variables)
    H0 = H.subs(at0)
    assert r == 0 or pd(H0)
    G = s.zeros(d*k)
    R = s.zeros(d*k, r)
    for i, yi in enumerate(variables):
        for a in range(k):
            for c in range(r):
                R[i*k+a, c] = integrate_radially(s.diff(B[a, c], yi), variables)
            for j, yj in enumerate(variables):
                for b in range(k):
                    G[i*k+a, j*k+b] = integrate_radially(
                        s.diff(A[a, b], yi, yj), variables, extra_weight=True)
    E = s.Matrix.vstack(*(y*s.eye(k) for y in variables))
    R0, G0 = R.subs(at0), G.subs(at0)
    S0 = G0 - R0*H0.inv()*R0.T if r else G0
    P = S0 if tangent_gram is None else tangent_gram
    assert zero(E.T*(P-S0)*E)
    G += P-S0
    M = G.row_join(R).col_join(R.T.row_join(H))
    D = s.zeros(d*k+r, n)
    D[:d*k, :k] = E
    D[d*k:, k:] = s.eye(r)
    assert zero(D.T*M*D-C)
    assert zero(M-M.T)
    return D, M, P


def bernstein_matrices(M, variables, box):
    """Direct tensor Bernstein coefficients on a rational rectangle."""
    d = len(variables)
    degree = tuple(max(s.Poly(v, *variables).degree(y)
                       for v in M) for y in variables)
    degree = tuple(max(0, j) for j in degree)
    u = s.symbols('u0:'+str(d))
    affine = {y: lo+(hi-lo)*ui
              for y, ui, (lo, hi) in zip(variables, u, box)}
    powers = {}
    for a in range(M.rows):
        for b in range(a, M.cols):
            powers[a, b] = s.Poly(s.expand(M[a, b].subs(affine, simultaneous=True)), *u)
    ans = []
    for index in product(*(range(n+1) for n in degree)):
        B = s.zeros(M.rows)
        for (a, b), poly in powers.items():
            value = 0
            for exponent, coeff in poly.terms():
                if all(e <= i for e, i in zip(exponent, index)):
                    value += coeff*s.prod(s.binomial(i, e)/s.binomial(n, e)
                                         for i, e, n in zip(index, exponent, degree))
            B[a, b] = B[b, a] = s.factor(value)
        ans.append(B)
    return ans


def check_constructive_example():
    x, y = s.symbols('x y', real=True)
    ell = s.Matrix([x+y+x*x, 2*x-y+x*y])
    schur = (x+x*y)**2 + 3*y*y + (x*x+y*y)**2
    C = s.Matrix([[schur+(ell.T*ell)[0], ell[0], ell[1]],
                  [ell[0], 1, 0], [ell[1], 0, 1]])
    D, M, P = taylor_lift(C, (x, y), 1)
    assert P == s.diag(1, 3) and pd(P)
    assert pd(M.subs({x:0, y:0}))
    for power in range(1, 15):
        h = s.Rational(1, 2**power)
        coeffs = bernstein_matrices(M, (x, y), ((-h, h), (-h, h)))
        if all(pd(B) for B in coeffs):
            break
    else:
        raise AssertionError('No positive Bernstein box found')
    # A controlled failed quadratic-vanishing hypothesis. The original C
    # remains PSD, while the canonical first-order lift has singular Schur jet.
    bad = s.Matrix([[x**4+y**4+(ell.T*ell)[0], ell[0], ell[1]],
                    [ell[0], 1, 0], [ell[1], 0, 1]])
    _, badM, badP = taylor_lift(bad, (x, y), 1)
    assert zero(badP) and badM.subs({x:0, y:0}).det() == 0
    return (x, y), C, D, M, P, h, len(coeffs)


def check_choi_family():
    x = s.symbols('x1:4', real=True)
    v = s.symbols('v1:4', real=True)
    e, a, b = s.symbols('epsilon a b', real=True)
    x1, x2, x3 = x
    C0 = s.Matrix([[x1*x1+2*x3*x3, -x1*x2, -x1*x3],
                   [-x1*x2, x2*x2+2*x1*x1, -x2*x3],
                   [-x1*x3, -x2*x3, x3*x3+2*x2*x2]])
    expected_det = 4*(x1**4*x2**2+x2**4*x3**2+x3**4*x1**2+x1*x1*x2*x2*x3*x3)
    assert s.expand(C0.det()-expected_det) == 0
    # All seven principal minors are polynomials in squares with nonnegative
    # coefficients. This proves C0>=0 for every real x, without grid sampling.
    minors = []
    for size in range(1,4):
        from itertools import combinations
        for I in combinations(range(3), size):
            p = s.Poly(s.expand(C0.extract(I,I).det()), *x)
            assert all(c >= 0 and all(j % 2 == 0 for j in powers)
                       for powers, c in p.terms())
            minors.append(p.as_expr())
    C = C0+e*sum(t*t for t in x)*s.eye(3)
    q = s.expand((s.Matrix(v).T*C*s.Matrix(v))[0])
    Avars = s.symbols('A11 A12 A13 A21 A22 A23 A31 A32 A33', real=True)
    A = s.Matrix(3,3,Avars)
    G = (sum(A[i,i]**2 for i in range(3))
         -2*sum(A[i,i]*A[j,j] for i in range(3) for j in range(i+1,3))
         +2*(A[0,2]**2+A[1,0]**2+A[2,1]**2)
         +e*sum(z*z for z in Avars))
    rankone = {A[i,j]:v[i]*x[j] for i in range(3) for j in range(3)}
    assert s.expand(G.subs(rankone, simultaneous=True)-q) == 0
    # Full Gram construction, with no symmetry assumption in the necessity proof.
    W = s.zeros(9)
    diag = (0,4,8)
    for i in range(3):
        W[diag[i],diag[i]] = 1+e
        for j in range(i+1,3):
            W[diag[i],diag[j]] = W[diag[j],diag[i]] = -a
    for positive, reverse in ((2,6),(3,1),(7,5)):
        W[positive,positive] = 2+e
        W[reverse,reverse] = e
        W[positive,reverse] = W[reverse,positive] = -b
    av = s.Matrix(Avars)
    H = s.expand((av.T*W*av)[0])
    principal_minors = sum(A[i,i]*A[j,j]-A[i,j]*A[j,i]
                           for i in range(3) for j in range(i+1,3))
    assert s.expand((G-H+2*b*principal_minors).subs(b,1-a)) == 0
    boundary_W = W.subs({a:(1+e)/2,b:(1-e)/2})
    # The diagonal 3x3 block has eigenvalues 0 and 3(1+e)/2 twice.
    Q = boundary_W.extract(diag,diag)
    assert zero(Q-s.Rational(1,2)*(1+e)*(3*s.eye(3)-s.ones(3)))
    pair_det = s.factor(boundary_W.extract((2,6),(2,6)).det())
    assert s.expand(pair_det-(3*e*e+10*e-1)/4) == 0
    threshold = (2*s.sqrt(7)-5)/3
    assert s.simplify((3*e*e+10*e-1).subs(e,threshold)) == 0
    # Arbitrary-Gram necessity: if q is a bilinear SOS, coefficient vectors
    # d_i,o_ij imply 0 <= ||sum d_i||^2 <= -3+3e+6sqrt(e(2+e)).
    # For the exact rational choice below this upper bound is strictly negative.
    eps = s.Rational(1,16)
    assert 0 < eps < 1
    separation = s.factor((1-eps)**2-4*eps*(2+eps))
    assert separation == s.Rational(93,256) and separation > 0
    # Construct an honest strictly positive canonical lift on the other side.
    positive = W.subs({e:s.Rational(1,10),a:s.Rational(109,200),b:s.Rational(91,200)})
    assert pd(positive)
    E = s.Matrix.vstack(*(t*s.eye(3) for t in x))
    # W uses row-major v_i*x_j; E*v uses column-major x_j*v_i.
    perm = [3*i+j for j in range(3) for i in range(3)]
    canonical_gram = positive.extract(perm,perm)
    assert zero(E.T*canonical_gram*E-C.subs(e,s.Rational(1,10)))
    return C0, expected_det, threshold, eps, separation, pair_det, positive


def case_zero_geometry():
    case = Path(__file__).resolve().parents[2] / 'cases' / 'angular'
    # Read only the supplied case; do not import or execute its acquisition code.
    data = json.loads((case/'seed_299_301.json').read_text())
    b,d = s.symbols('b d', real=True)
    def literal(rows):
        return sum(s.Rational(n,m)*b**i*d**j for i,j,n,m in rows)
    w,g = literal(data['w']),literal(data['g'])
    # det d(w,g)/d(b,d) = 2b*g'(d). Nonzero if g is square-free and
    # its roots do not meet b=0 on w=0. Both tests are exact resultants.
    disc = s.discriminant(g,d)
    resultant = s.resultant(g,w.subs(b,0),d)
    assert disc != 0 and resultant != 0
    assert s.expand(s.det(s.Matrix([[s.diff(w,b),s.diff(w,d)],
                                    [s.diff(g,b),s.diff(g,d)]]))-2*b*s.diff(g,d)) == 0
    return disc,resultant


def main():
    variables,C,D,M,P,h,count = check_constructive_example()
    C0,det0,threshold,eps,separation,pair_det,positive = check_choi_family()
    disc,resultant = case_zero_geometry()
    lines = [
        'EXACT SCIENTIFIC CALCULATIONS',
        '',
        'Constructive corank-one example:',
        'C = '+str(C),
        'D = '+str(D),
        'M = '+str(M),
        'Tangent Schur Gram = '+str(P),
        'Identity C=D^T M D: exact.',
        'All '+str(count)+' tensor Bernstein coefficient matrices are positive definite on [-'+str(h)+','+str(h)+']^2.',
        'Degenerate control: replacing the Schur function by x^4+y^4 makes the canonical central lift singular.',
        '',
        'Choi-type family:',
        'C0 = '+str(C0),
        'det C0 = '+str(det0),
        'All seven principal minors have nonnegative coefficients in even powers.',
        'For epsilon>0, C_epsilon >= epsilon |x|^2 I.',
        'Bilinear SOS / quadratic polyconvexity threshold = '+str(threshold),
        'The boundary Gram pair determinant is '+str(pair_det)+'.',
        'At epsilon='+str(eps)+', (1-epsilon)^2-4 epsilon(2+epsilon) = '+str(separation)+' > 0: no bilinear SOS.',
        'Consequently no analytic D^T M D with M(0)>0 can represent C_(1/16) near 0.',
        'At epsilon=1/10, a=109/200 and b=91/200 give a positive definite 9x9 Gram and an exact canonical lift.',
        '',
        'Supplied B1 zero geometry:',
        'discriminant_d(g) = '+str(disc),
        'resultant_d(g,w(0,d)) = '+str(resultant),
        'Both are nonzero, so the (w,g) zero coordinates are simple.',
        '',
        'The general mathematical implications and their scope are proved in FINDING.txt.',
    ]
    output='\n'.join(lines)+'\n'
    (Path(__file__).resolve().parent/'EXACT_RESULTS.txt').write_text(output)
    print(output)


if __name__ == '__main__':
    main()
