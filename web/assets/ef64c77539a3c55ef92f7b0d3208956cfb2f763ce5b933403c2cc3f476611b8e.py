"""Exact small fixtures for RESULT; finite instances, not formal verification."""
from collections import Counter
from fractions import Fraction
import importlib.util
import json
from math import ceil, log
from pathlib import Path
import sys
import sympy as sp


def gf_degree(a):
    return a.bit_length()-1


def gf_remainder(a, p):
    while a and gf_degree(a) >= gf_degree(p):
        a ^= p << (gf_degree(a)-gf_degree(p))
    return a


def irreducible(b):
    # Only small b in the fixture; the same exhaustive method is polynomial
    # in q=2^b, which is polynomial in the number of stabilizers.
    for p in range((1 << b)+1, 1 << (b+1), 2):
        reducible = False
        for d in range(1, b//2+1):
            for f in range((1 << d)+1, 1 << (d+1), 2):
                if gf_remainder(p, f) == 0:
                    reducible = True
                    break
            if reducible:
                break
        if not reducible:
            return p
    raise AssertionError('No irreducible found')


def biased_multiset(a):
    b = (2*a-1).bit_length()
    q, p = 1 << b, irreducible(b)

    def mul(x, y):
        out = 0
        while y:
            if y & 1:
                out ^= x
            x <<= 1
            y >>= 1
        return gf_remainder(out, p)

    def trace(x):
        out, xx = 0, x
        for _ in range(b):
            out ^= xx
            xx = mul(xx, xx)
        assert out in [0, 1]
        return out

    labels = []
    for t in range(q):
        powers = [1]
        for _ in range(a-1):
            powers.append(mul(powers[-1], t))
        for x in range(q):
            labels.append(sum(trace(mul(x, tt)) << j for j, tt in enumerate(powers)))
    biases = [Fraction(sum((-1)**((z & g).bit_count() % 2) for g in labels), q*q)
              for z in range(1 << a)]
    assert biases[0] == 1
    assert all(0 <= v <= Fraction(a-1, q) <= Fraction(1, 2) for v in biases[1:])
    return q, labels, biases


def local_gate(n, target, gate):
    return sp.kronecker_product(*[gate if j == target else sp.eye(2) for j in range(n)])


def cnot(n, control, target):
    dim = 1 << n
    out = sp.zeros(dim)
    for col in range(dim):
        row = col ^ (1 << (n-1-target)) if col & (1 << (n-1-control)) else col
        out[row, col] = 1
    return out


def clifford_fixture():
    n, a = 1, 2
    nq, dim = n+a, 1 << (n+a)
    hh = sp.Matrix([[1, 1], [1, -1]])/sp.sqrt(2)
    zz = sp.diag(1, -1)
    uu = cnot(nq, 0, 1)*local_gate(nq, 1, hh)*cnot(nq, 1, 2)
    assert uu.adjoint()*uu == sp.eye(dim)
    stabilizers = [sp.simplify(uu*local_gate(nq, n+j, zz)*uu.adjoint()) for j in range(a)]
    q, labels, biases = biased_multiset(a)
    avg = sp.zeros(dim)
    for g in labels:
        ss = sp.eye(dim)
        for j in range(a):
            if (g >> j) & 1:
                ss *= stabilizers[j]
        assert all(sum(v != 0 for v in ss.row(row)) == 1 for row in range(dim))
        avg += ss
    cc = sp.simplify((sp.eye(dim)-avg/(q*q))/2)
    vv0 = sp.zeros(dim, 1 << n)
    for z in range(1 << n):
        vv0[z << a, z] = 1
    vv = uu*vv0
    pp = vv*vv.adjoint()
    assert cc*vv == sp.zeros(dim, 1 << n)
    gauge = sp.simplify(uu.adjoint()*cc*uu)
    reverse_bits = lambda z: sum(((z >> (a-1-j)) & 1) << j for j in range(a))
    assert gauge == sp.diag(*[(1-biases[reverse_bits(z)])/2 for z in range(1 << a)]*2)
    assert sp.simplify(cc-sp.Rational(1, 4)*(sp.eye(dim)-pp)).is_positive_semidefinite
    row_degree = max(sum(v != 0 for v in cc.row(row)) for row in range(dim))
    assert row_degree <= q*q+1
    return {'status': 'EXACT_CLIFFORD_ENFORCER_FIXTURE_PASSED',
            'logical_qubits': n, 'ancilla_qubits': a,
            'multiset_size': q*q, 'actual_max_row_degree': row_degree,
            'off_code_spectrum': sorted({str((1-v)/2) for v in biases[1:]}),
            'kernel_dimension': 1 << n}


def seed_row_fixture():
    target = Path(__file__).parents[1]/'games_hamiltonians/cycle2/bmvz_bjsw_seed_pair_test.py'
    spec = importlib.util.spec_from_file_location('saved_seed_checker', target)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    cphi, cpsi = mod.q3_cliffords()
    cphi = mod.append_clock_suffix(cphi)
    cpsi = mod.append_clock_suffix(cpsi)
    relative = mod.matmul(mod.conjugate_transpose_real(cphi), cpsi)
    for row in relative:
        nonzero = [v for v in row if v]
        assert len(nonzero) == 8
        assert all(mod.abs_squared(v) == Fraction(1, 8) for v in nonzero)
    preparation_product = mod.matmul(cphi, mod.conjugate_transpose_real(cpsi))
    assert all(sum(bool(v) for v in row) == 2 for row in preparation_product)
    assert all(mod.abs_squared(v) == Fraction(1, 2)
               for row in preparation_product for v in row if v)
    out = []
    for t in [1, 2, 5]:
        k, q = 16, 4
        count = q*8**t
        square = Fraction(1, k*k*8**t)
        mass = count*square
        assert mass == Fraction(q, k*k)
        out.append({'T': t, 'K': k, 'psi_tail_count': q,
                    'selected_row_nonzeros': count,
                    'entry_square': str(square), 'row_square_mass': str(mass)})
    return {'status': 'EXACT_FLAT_TAIL_ROW_FIXTURE_PASSED',
            'decoder_product': 'c_phi* c_psi: 8 entries/row, square 1/8',
            'preparation_product': 'c_phi c_psi*: 2 entries/row, square 1/2',
            'instances': out}


def arbitrary_decoder_fixture():
    # The two-dimensional active seed span can attain the 7/8 entry bound.
    c, ss = 1/sp.sqrt(8), sp.sqrt(7)/sp.sqrt(8)
    ww = sp.Matrix([[c, ss], [-ss, c]])
    assert ww*ww.adjoint() == sp.eye(2)
    pphi = sp.diag(1, 0)
    psi = sp.Matrix([c, ss])
    ppsi = psi*psi.adjoint()
    assert sp.simplify(pphi*ppsi*pphi) == pphi/8
    assert max(abs(v)**2 for v in ww.row(0)) == sp.Rational(7, 8)
    return {'status': 'EXACT_ARBITRARY_DECODER_BOUND_FIXTURE_PASSED',
            'fixed_overlap_square': '1/8',
            'largest_row_entry_square': '7/8',
            'tensor_row_maximum_square': '(7/8)^T',
            'scope': 'Tensor endpoint decoder bound; no general active workspace claim.'}


def scalar_filter_fixture():
    # Exact polynomial samples; the interval-uniform proof remains RESULT B.
    xx = sp.Symbol('x')
    checked = 0
    for gamma in [sp.Rational(1, 16), sp.Rational(1, 4), sp.Rational(1, 2)]:
        for degree in [1, 2, 4]:
            poly = sp.chebyshevt(degree, (1+gamma-2*xx)/(1-gamma))
            denom = sp.chebyshevt(degree, (1+gamma)/(1-gamma))
            assert sp.simplify(poly.subs(xx, 0)/denom) == 1
            for j in range(17):
                point = gamma+(1-gamma)*sp.Rational(j, 16)
                assert abs(poly.subs(xx, point)/denom) <= 1/denom
                checked += 1
    rows = []
    for t in [16, 64, 256, 1024, 4096]:
        k, q, rowdegree = 16*t*t, 4*t*t, 9
        denominator = log(q/2)+t*log(8)-log(rowdegree+1)
        bound = (log(8*k*k/q)*log(rowdegree+1)/(4*denominator))**2
        rows.append({'T': t, 'K': k, 'row_degree': rowdegree,
                     'gap_upper_bound': bound})
    return {'status': 'EXACT_SCALAR_FILTER_SAMPLES_PASSED', 'rational_points': checked,
            'warning': 'Gap table is numerical evaluation of an analytic bound, not a gap measurement.',
            'bound_table': rows}


def main():
    field_rows = []
    for a in range(1, 9):
        q, labels, bias = biased_multiset(a)
        field_rows.append({'stabilizers': a, 'field_size': q, 'multiset_size': len(labels),
                           'largest_nontrivial_bias': str(max(bias[1:]))})
    out = {'warning': 'Exact finite fixtures are not formal or external proof validation.',
           'flat_row': seed_row_fixture(), 'finite_field': field_rows,
           'arbitrary_decoder': arbitrary_decoder_fixture(),
           'Clifford': clifford_fixture(), 'Chebyshev': scalar_filter_fixture()}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
