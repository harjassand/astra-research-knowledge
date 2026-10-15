#!/usr/bin/env python3
"""Independent exact finite checks for the accompanying analytic note.

These checks do not execute or import the incoming structural verifier, and do
not replace the dimension-uniform proofs or provide external validation.
"""
import hashlib
import json
from itertools import combinations, combinations_with_replacement, permutations
from pathlib import Path

import sympy as s
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parent


def qmons(v):
    return [v[i] * v[j] for i, j in combinations_with_replacement(range(len(v)), 2)]


def coefficient_matrix(polys, variables, monomials=None):
    p = [s.Poly(s.expand(f), *variables) for f in polys]
    if monomials is None:
        monomials = sorted({e for f in p for e, _ in f.terms()})
    return s.Matrix([[f.coeff_monomial(e) for f in p] for e in monomials])


def rank(q):
    return DomainMatrix.from_Matrix(q).convert_to(s.QQ).rank()


def planar_checks(m):
    aa = s.symbols(f'a0:{m}')
    xi, eta = s.symbols('xi eta')
    X = s.symbols(f'X0:{m}')
    Y = s.symbols(f'Y0:{m}')
    Z = s.symbols(f'Z0:{m}')
    h = X + Y + Z
    symbol = tuple(a * xi**2 for a in aa) + tuple(a * xi * eta for a in aa) + tuple(a * eta**2 for a in aa)
    SM = coefficient_matrix(qmons(symbol), aa + (xi, eta))
    U = X + Y
    V = Y + Z
    minors = [U[i] * V[j] - U[j] * V[i] for i, j in combinations(range(2*m), 2)]
    # Use exactly the same quadratic-Hessian monomial ordering as SM.
    hmons = [s.Poly(f, *h).monoms()[0] for f in qmons(h)]
    PM = coefficient_matrix(minors, h, hmons)
    assert SM.cols == 3*m*(3*m+1)//2
    assert SM.rows == 5*m*(m+1)//2
    assert rank(SM) == SM.rows
    assert rank(PM) == m*(2*m-1)
    assert SM * PM == s.zeros(SM.rows, PM.cols)
    assert SM.cols - rank(SM) == rank(PM)

    # The extreme third jets detect T = d omega. The S_j = u^j_xxx
    # coefficients are T(p_i,p_j,V); W_j = u^j_yyy coefficients are
    # T(q_i,U,q_j). Their linear map is injective on all 3-forms.
    triples = list(combinations(range(2*m), 3))
    tid = {t: i for i, t in enumerate(triples)}
    rows = []
    for i in range(m):
        for j in range(m):
            for k in range(2*m):
                for triple in [(i, j, k), (m+i, k, m+j)]:
                    row = [0] * len(triples)
                    if len(set(triple)) == 3:
                        inversions = sum(triple[a] > triple[b] for a in range(3) for b in range(a+1, 3))
                        row[tid[tuple(sorted(triple))]] = (-1)**inversions
                    rows.append(row)
    CM = s.Matrix(rows) if triples else s.zeros(2*m*m*2*m, 0)
    assert rank(CM) == len(triples)
    return dict(output_dimension=m, jet_dimension=3*m,
                symbol_rank=rank(SM), symbol_kernel=rank(PM),
                two_form_dimension=m*(2*m-1),
                closedness_test_rank=rank(CM), three_form_dimension=len(triples))


def symbol_span(n, m):
    pairs = list(combinations_with_replacement(range(n), 2))
    cols = []
    for a in range(m):
        directions = [s.eye(n)[:, i] for i in range(n)]
        directions += [s.eye(n)[:, i] + s.eye(n)[:, j] for i, j in combinations(range(n), 2)]
        for v in directions:
            cols.append(s.Matrix([v[i]*v[j] if out == a else 0 for out in range(m) for i, j in pairs]))
    q = s.Matrix.hstack(*cols)
    assert rank(q) == m*n*(n+1)//2
    return dict(spatial_dimension=n, output_dimension=m, pure_jet_span_rank=rank(q))


def output_generator_examples():
    a, b, c, d = s.symbols('a b c d')
    A = s.Matrix([a, b, c, d])  # row-major matrix entries
    HF = s.hessian(a**4, A)
    bg = {a: 1, b: 0, c: 0, d: 0}
    values = []
    for name, M, target in [
        ('symmetric_positive', s.Matrix([[1, s.Rational(1,2)], [s.Rational(1,2), 1]]), s.Matrix([1, -4])),
        ('nonsymmetric_strong_parabolic', s.Matrix([[1, -1], [1, 1]]), s.Matrix([1, 2])),
    ]:
        Bx = s.Matrix([target[0], 0, target[1], 0])
        K = s.kronecker_product(M, s.eye(2))
        heat = (Bx.T * HF.subs(bg) * K * Bx)[0]
        assert heat == -12
        symM = (M + M.T)/2
        assert symM[0, 0] > 0 and symM.det() > 0
        values.append(dict(name=name, matrix=[[str(v) for v in row] for row in M.tolist()],
                           target=[str(v) for v in target], negative_dissipation=str(heat)))
    return values


def spatial_dimension_boundary():
    h11, h12, h13, h22, h23, h33 = s.symbols('h11 h12 h13 h22 h23 h33')
    p1, p2, p3 = s.symbols('p1 p2 p3')
    H = s.Matrix([[h11,h12,h13],[h12,h22,h23],[h13,h23,h33]])
    U,V,W = H[:,0],H[:,1],H[:,2]
    def wedge(v, w, i, j):
        return v[i]*w[j]-v[j]*w[i]
    gauge = wedge(U,V,0,2)-wedge(U,W,0,1)
    assert s.expand(gauge) == 0
    nonclosed_density = p3*wedge(U,V,0,1)
    closed_replacement = p3*wedge(U,V,0,1)+p2*wedge(U,V,0,2)-p2*wedge(U,W,0,1)
    assert s.expand(nonclosed_density-closed_replacement) == 0
    return dict(nonzero_pair_form_gauge_identically_zero=True,
                nonclosed_representative_has_closed_replacement=True)


def non_peano_example():
    p,q = s.symbols('p q', real=True)
    r = s.sqrt(p*p+q*q)
    f = p*r
    HF = s.hessian(f, (p,q))
    assert s.simplify(HF[0,0]-(3*p/r-p**3/r**3)) == 0
    assert s.simplify(HF[0,1]-q**3/r**3) == 0
    assert s.simplify(HF[1,1]-p**3/r**3) == 0
    assert f.subs({p:1,q:0}) == 1
    assert f.subs({p:-1,q:0}) == -1
    X,Y,Z = s.symbols('X Y Z', real=True)
    # The two elementary determinant bounds give |det H| <= |H|_F^2/2.
    assert s.expand((X*X+2*Y*Y+Z*Z)/2-(X*Z-Y*Y)-(X-Z)**2/2-2*Y*Y) == 0
    assert s.expand((X*X+2*Y*Y+Z*Z)/2+(X*Z-Y*Y)-(X+Z)**2/2) == 0
    return dict(coefficients='p sqrt(p^2+q^2)', regularity='C1,1; no quadratic Peano jet',
                corrected_density_lower_bound='(7/2)|A|^2 |H|_F^2',
                does_not_separate_polynomial_and_nonsmooth_cones=True)


def main():
    result = {
        'status':'EXACT_FINITE_CHECK_PASS',
        'planar_dimension_checks':[planar_checks(m) for m in range(1,7)],
        'general_symbol_span_checks':[symbol_span(n,m) for n,m in [(1,1),(2,1),(2,3),(3,2),(4,2),(5,3)]],
        'output_generator_counterexamples':output_generator_examples(),
        'higher_spatial_dimension_boundary':spatial_dimension_boundary(),
        'regularity_boundary':non_peano_example(),
        'scope':'Independent exact algebra only. Dimension-uniform analytic proofs are in REPORT.md. No external review, novelty, PDE existence, or physical capability is certified.',
    }
    result['checks_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (ROOT/'CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
