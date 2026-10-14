"""Exact finite checks for the torsion-safe sparse constant floor.

The universal theorem is proved in RESULT.txt. The finite checks here include
integer-lattice certificates over all abelian groups at n=3, not only scans
over fixed cyclic moduli. No environment changes or network calls are made.
"""
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import time

from sympy import Matrix, eye
from sympy.matrices.normalforms import hermite_normal_form


ROOT = Path(__file__).resolve().parent


def beta(s):
    assert s >= 1
    return 1 << (s.bit_length() - 1)


class Group:
    def __init__(self, moduli):
        self.moduli = tuple(moduli)
        self.elements = list(product(*(range(q) for q in self.moduli)))
        self.zero = (0,) * len(self.moduli)
        self.nonzero = [a for a in self.elements if a != self.zero]

    def add(self, a, b):
        return tuple((x + y) % q for x, y, q in zip(a, b, self.moduli))

    def neg(self, a):
        return tuple(-x % q for x, q in zip(a, self.moduli))


def zeta(coefficients, n, G):
    values = list(coefficients)
    for i in range(n):
        bit = 1 << i
        for x in range(1 << n):
            if x & bit:
                values[x] = G.add(values[x], values[x ^ bit])
    return values


def product_form(coefficients, n, G):
    c0 = coefficients[0]
    if c0 == G.zero:
        return False
    T = [a for a, c in enumerate(coefficients) if c != G.zero]
    D = 0
    for a in T:
        D |= a
    for a in range(1 << n):
        expected = G.zero
        if a & D == a:
            expected = G.neg(c0) if a.bit_count() & 1 else c0
        if coefficients[a] != expected:
            return False
    return True


def constant_arrays(n, G, sparse_cap=None):
    """Every coefficient vector in the named finite family, exactly once."""
    size = 1 << n
    if sparse_cap is None:
        for c0 in G.nonzero:
            for rest in product(G.elements, repeat=size - 1):
                yield (c0,) + rest
        return
    for m in range(1, min(sparse_cap, size) + 1):
        for positive_terms in combinations(range(1, size), m - 1):
            for coeffs in product(G.nonzero, repeat=m):
                c = [G.zero] * size
                c[0] = coeffs[0]
                for a, value in zip(positive_terms, coeffs[1:]):
                    c[a] = value
                yield c


def scan_constant(n, moduli, sparse_cap=None):
    G = Group(moduli)
    checked = equalities = 0
    per_m = {}
    for coefficients in constant_arrays(n, G, sparse_cap):
        values = zeta(coefficients, n, G)
        m = sum(c != G.zero for c in coefficients)
        k = sum(v != G.zero for v in values)
        assert k * beta(m) >= 1 << n, (n, moduli, coefficients, values)
        assert k * m >= 1 << n
        equality = k * m == 1 << n
        assert equality == product_form(coefficients, n, G)
        equalities += equality
        checked += 1
        row = per_m.setdefault(m, dict(count=0, min_k=k, equality_count=0))
        row['count'] += 1
        row['min_k'] = min(row['min_k'], k)
        row['equality_count'] += equality
    return dict(n=n, group_moduli=moduli, sparse_cap=sparse_cap,
                checked=checked, reciprocal_equalities=equalities,
                per_actual_m=per_m)


def structural_factor(T):
    detail = {}
    for a in T:
        above = [b for b in T if a & b == a]
        s = len(above)
        d = max((b ^ a).bit_count() for b in above)
        detail[a] = dict(s=s, d=d, rho=min(beta(s), 1 << d))
    return detail


def check_all_term_structure(n, moduli):
    G = Group(moduli)
    checked = 0
    for coefficients in product(G.elements, repeat=1 << n):
        T = [a for a, c in enumerate(coefficients) if c != G.zero]
        if not T:
            continue
        values = zeta(coefficients, n, G)
        k = sum(v != G.zero for v in values)
        m = len(T)
        union = sum(any(a & x == a for a in T) for x in range(1 << n))
        W_all = sum(1 << (n - a.bit_count()) for a in T)
        detail = structural_factor(T)
        D_all = sum(row['s'] for row in detail.values())
        D_dyad = sum(row['rho'] for row in detail.values())
        minima = [a for a in T if not any(b != a and a & b == b for b in T)]
        W_min = sum(1 << (n - a.bit_count()) for a in minima)
        D_min = sum(detail[a]['rho'] for a in minima)
        assert union <= m * k
        assert W_all <= D_dyad * k <= D_all * k
        assert D_all <= m * (m + 1) // 2 <= m * m
        assert W_min <= D_min * k
        checked += 1
    return dict(n=n, group_moduli=moduli, checked=checked,
                statements=['union<=m*k', 'W_all<=D_dyad*k<=D_all*k',
                            'D_all<=m(m+1)/2<=m^2', 'W_min<=D_min*k'])


def product_mass(values, probabilities, G):
    n = len(probabilities)
    q = Fraction(0)
    for x, value in enumerate(values):
        if value == G.zero:
            continue
        mass = Fraction(1)
        for i in range(n):
            p = probabilities[i]
            mass *= p if x & (1 << i) else 1 - p
        q += mass
    return q


def biased_checks():
    families = [(3, [2]), (2, [6]), (2, [2, 4])]
    biases = [Fraction(0), Fraction(1, 4), Fraction(1, 2)]
    output = []
    for n, moduli in families:
        G = Group(moduli)
        checked = equalities = 0
        for coefficients in constant_arrays(n, G):
            values = zeta(coefficients, n, G)
            T = [a for a, c in enumerate(coefficients) if c != G.zero]
            m = len(T)
            detail = structural_factor(T)
            D_all = sum(row['rho'] for row in detail.values())
            form = product_form(coefficients, n, G)
            used = 0
            for a in T:
                used |= a
            for probabilities in product(biases, repeat=n):
                q = product_mass(values, probabilities, G)
                assert q * beta(m) >= 1
                equality = q * m == 1
                expected_equality = form and all(
                    probabilities[i] == Fraction(1, 2)
                    for i in range(n) if used & (1 << i))
                assert equality == expected_equality
                weights = {}
                for a in T:
                    w = Fraction(1)
                    for i in range(n):
                        if a & (1 << i):
                            w *= probabilities[i]
                    weights[a] = w
                    assert w <= detail[a]['rho'] * q
                assert sum(weights.values()) <= D_all * q
                checked += 1
                equalities += equality
        output.append(dict(n=n, group_moduli=moduli,
                           biases=[str(x) for x in biases], checked=checked,
                           reciprocal_equalities=equalities))
    return output


def lattice_coordinates(H, v):
    """Return integral coordinates, or None; never replace by rational span."""
    if not H.cols:
        return [] if not any(v) else None
    pivots = list(H.T.rref()[1])
    square = H.extract(pivots, range(H.cols))
    z = square.inv() * Matrix([v[i] for i in pivots])
    if not all(x.q == 1 for x in z) or H * z != v:
        return None
    return [int(x) for x in z]


def zero_row_HNF(n, T, N):
    zero = [x for x in range(1 << n) if x not in N]
    rows = (Matrix([[int(b & x == b) for b in T] for x in zero])
            if zero else Matrix.zeros(0, len(T)))
    return hermite_normal_form(rows.T)


def all_group_lattice_gate(n=3):
    """e_empty is forced for every maximal strict dyadic violation pattern."""
    size = 1 << n
    certificates = []
    by_m = {}
    for m in range(1, size + 1):
        kmax = (size - 1) // beta(m)
        if kmax < 1:
            continue  # c_empty=F(0)!=0 already forbids empty N.
        count = 0
        for tail in combinations(range(1, size), m - 1):
            T = [0] + list(tail)
            e0 = eye(m).col(0)
            for other_N in combinations(range(1, size), kmax - 1):
                N = [0] + list(other_N)
                H = zero_row_HNF(n, T, N)
                coordinates = lattice_coordinates(H, e0)
                assert coordinates is not None, (n, T, N)
                certificates.append(dict(T=T, allowed_N=N,
                    zero_row_HNF=[[int(z) for z in row] for row in H.tolist()],
                    e_empty_integer_HNF_coordinates=coordinates))
                count += 1
        by_m[m] = dict(kmax=kmax, patterns=count)
    path = ROOT / 'all_group_lattice_certificates.json'
    path.write_text(json.dumps(certificates, indent=2) + '\n')
    return dict(n=n, status='ALL_INTEGER_CONSTANT_UNITS_FORCED',
                patterns=len(certificates), by_actual_m=by_m,
                certificate_file=path.name,
                certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def equality_lattice_gate(n=3):
    size = 1 << n
    checked = forced = 0
    face_cases = []
    excluded = []
    for m in [1 << j for j in range(n + 1)]:
        k = size // m
        for tail in combinations(range(1, size), m - 1):
            T = [0] + list(tail)
            e0 = eye(m).col(0)
            for other_N in combinations(range(1, size), k - 1):
                N = [0] + list(other_N)
                H = zero_row_HNF(n, T, N)
                coordinates = lattice_coordinates(H, e0)
                D = 0
                for b in T:
                    D |= b
                face_T = [b for b in range(size) if b & D == b]
                face_N = [x for x in range(size) if x & D == 0]
                is_face = T == face_T and N == face_N
                if is_face:
                    assert coordinates is None
                    relations = []
                    for j, b in enumerate(T[1:], 1):
                        v = eye(m).col(j) - ((-1) ** b.bit_count()) * e0
                        relations.append(v)
                        assert lattice_coordinates(H, v) is not None
                    R = Matrix.hstack(*relations) if relations else Matrix.zeros(m, 0)
                    assert H == hermite_normal_form(R)
                    face_cases.append(dict(T=T, N=N, D=D,
                        coefficient_relations='c_B=(-1)^|B| c_empty',
                        quotient='free cyclic; no torsion relation on c_empty'))
                else:
                    assert coordinates is not None, (T, N)
                    forced += 1
                    excluded.append(dict(T=T, allowed_N=N,
                        zero_row_HNF=[[int(z) for z in row] for row in H.tolist()],
                        e_empty_integer_HNF_coordinates=coordinates))
                checked += 1
    path = ROOT / 'equality_lattice_certificates.json'
    path.write_text(json.dumps(dict(face_cases=face_cases, excluded=excluded), indent=2) + '\n')
    return dict(n=n, checked_patterns=checked, forced_zero_constant_patterns=forced,
                exact_face_patterns=face_cases, certificate_file=path.name,
                certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def constructed_sharp_examples():
    rows = []
    for moduli in [[2], [4], [6], [2, 4]]:
        G = Group(moduli)
        for g in G.nonzero:
            for d in range(7):
                n = d + 1
                D = (1 << d) - 1
                c = [G.zero] * (1 << n)
                for a in range(1 << n):
                    if a & D == a:
                        c[a] = G.neg(g) if a.bit_count() & 1 else g
                values = zeta(c, n, G)
                m = sum(v != G.zero for v in c)
                k = sum(v != G.zero for v in values)
                assert (m, k) == (1 << d, 2)
                assert product_form(c, n, G)
                rows.append(dict(group_moduli=moduli, g=g, n=n, d=d, m=m, k=k))
    return rows


def boundary_cases():
    G = Group([4])
    g = (1,)
    # The no-constant GF2 ZERO-event corollary is false over Z4.
    linear = [G.zero] * 8
    for a in [1, 2, 4]:
        linear[a] = g
    values = zeta(linear, 3, G)
    zeros = [x for x, v in enumerate(values) if v == G.zero]
    assert zeros == [0]
    rows = [dict(name='GF2_even_corollary_does_not_extend_to_Z4',
        n=3, group_moduli=[4], T=[1, 2, 4], coefficient=1,
        actual_m=3, zero_inputs=zeros, zero_probability='1/8',
        refuted_bound='Pr(F=0)>=1/(m+1)=1/4',
        does_not_refute='Nonzero-constant NONZERO-event sparse floor')]
    # Removing the constant hypothesis admits a one-term needle.
    needle = [G.zero] * 32
    needle[31] = g
    nonzero = [x for x, v in enumerate(zeta(needle, 5, G)) if v != G.zero]
    assert nonzero == [31]
    rows.append(dict(name='nonzero_constant_is_necessary', n=5,
        group_moduli=[4], T=[31], coefficient=1, actual_m=1,
        nonzero_inputs=nonzero, nonzero_probability='1/32'))
    # Product bias p>1/2 can violate the two-term reciprocal bound.
    c = [g, G.neg(g)]
    q = product_mass(zeta(c, 1, G), [Fraction(3, 4)], G)
    assert q == Fraction(1, 4)
    rows.append(dict(name='p_at_most_half_is_necessary', n=1,
        group_moduli=[4], polynomial='1-x1', actual_m=2,
        probability_x1_one='3/4', nonzero_probability=str(q)))
    # Fair marginals do not replace coordinate independence.
    c = [g, G.neg(g), G.neg(g), g]
    values = zeta(c, 2, G)
    dependent_law = {1: Fraction(1, 2), 2: Fraction(1, 2)}
    q = sum(mass for x, mass in dependent_law.items() if values[x] != G.zero)
    assert q == 0
    rows.append(dict(name='independence_is_necessary', n=2,
        group_moduli=[4], polynomial='(1-x1)(1-x2)', actual_m=4,
        law='uniform on {01,10}; both one-bit marginals fair',
        nonzero_probability='0'))
    return rows


def main():
    start = time.monotonic()
    constant_families = [
        (3, [2], None), (3, [3], None), (3, [4], None),
        (3, [2, 2], None), (3, [6], 4), (3, [2, 4], 4),
        (4, [6], 3), (4, [2, 4], 3),
    ]
    constant = [scan_constant(*row) for row in constant_families]
    all_terms = [check_all_term_structure(2, moduli)
                 for moduli in [[2], [3], [4], [6], [2, 4]]]
    all_terms += [check_all_term_structure(3, [2])]
    biased = biased_checks()
    lattice = all_group_lattice_gate()
    equality = equality_lattice_gate()
    sharp = constructed_sharp_examples()
    boundaries = boundary_cases()
    output = dict(status='PASS',
        theorem_scope='Universal statements proved in RESULT.txt; finite checks are supporting evidence only.',
        constant_coefficient_scans=constant,
        total_constant_arrays=sum(row['checked'] for row in constant),
        all_term_structure_scans=all_terms,
        total_all_term_arrays=sum(row['checked'] for row in all_terms),
        product_bias_scans=biased,
        total_biased_laws=sum(row['checked'] for row in biased),
        all_abelian_n3_lattice_gate=lattice,
        all_abelian_n3_equality_gate=equality,
        constructed_sharp_examples=sharp,
        explicit_scope_boundary_cases=boundaries,
        elapsed_seconds=round(time.monotonic() - start, 6),
        costs='All listed coefficient arrays, cube evaluations, rational product masses, and integer HNF operations executed locally; no sampling-runtime claim.')
    path = ROOT / 'floor_gate_receipt.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({key: output[key] for key in ['status', 'total_constant_arrays',
        'total_all_term_arrays', 'total_biased_laws', 'elapsed_seconds']}, indent=2))
    print(json.dumps(dict(all_group_lattice=lattice, equality_lattice=dict(
        checked_patterns=equality['checked_patterns'],
        forced_zero_constant_patterns=equality['forced_zero_constant_patterns'],
        exact_face_patterns=len(equality['exact_face_patterns']))), indent=2))


if __name__ == '__main__':
    main()
