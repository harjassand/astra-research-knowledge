#!/usr/bin/env python3
"""Independent exact audits of the hidden-field compiler interface.

The generator algorithm sees only an abstract F2 algebra, not its defining
polynomial. Brute field enumeration is used only in separately labelled
finite validation. This is not a Lauder--Wan implementation or speed test.
"""
from itertools import combinations, product
import json
from pathlib import Path
import random


def rank(vectors):
    pivots = {}
    for v in vectors:
        while v:
            k = v.bit_length() - 1
            if k in pivots:
                v ^= pivots[k]
            else:
                pivots[k] = v
                break
    return len(pivots)


def linear_apply(columns, x):
    out = 0
    while x:
        bit = x & -x
        out ^= columns[bit.bit_length()-1]
        x ^= bit
    return out


def kernel(columns):
    pivots, out = {}, []
    for i, v in enumerate(columns):
        rel = 1 << i
        while v:
            k = v.bit_length() - 1
            if k in pivots:
                w, s = pivots[k]
                v ^= w
                rel ^= s
            else:
                pivots[k] = (v, rel)
                break
        if not v:
            out.append(rel)
    return out


def solve(columns, target):
    pivots = {}
    for i, v in enumerate(columns):
        rel = 1 << i
        while v:
            k = v.bit_length() - 1
            if k in pivots:
                w, s = pivots[k]
                v ^= w
                rel ^= s
            else:
                pivots[k] = (v, rel)
                break
    rel = 0
    while target:
        k = target.bit_length() - 1
        if k not in pivots:
            return None
        w, s = pivots[k]
        target ^= w
        rel ^= s
    return rel


class BinaryField:
    def __init__(self, degree, modulus):
        self.d, self.modulus = degree, modulus
        self.q = 1 << degree

    def mul(self, a, b):
        out = 0
        while b:
            if b & 1:
                out ^= a
            a <<= 1
            if a & self.q:
                a ^= self.modulus
            b >>= 1
        return out

    def pow(self, a, e):
        out = 1
        while e:
            if e & 1:
                out = self.mul(out, a)
            a = self.mul(a, a)
            e >>= 1
        return out

    def trace(self, a):
        out = 0
        for _ in range(self.d):
            out ^= a
            a = self.mul(a, a)
        assert out in (0, 1)
        return out


def polynomial_gcd(a, b):
    while b:
        c = a
        while c and c.bit_length() >= b.bit_length():
            c ^= b << (c.bit_length()-b.bit_length())
        a, b = b, c
    return a


def prime_powers(d):
    out, ell = [], 2
    while ell * ell <= d:
        if d % ell == 0:
            power = 1
            while d % ell == 0:
                power *= ell
                d //= ell
            out.append((ell, power))
        ell += 1
    if d > 1:
        out.append((d, d))
    return out


def irreducible(degree, modulus):
    f = BinaryField(degree, modulus)
    x = 2 if degree > 1 else 0
    if f.pow(x, 1 << degree) != x:
        return False
    return all(polynomial_gcd(f.pow(x, 1 << (degree//ell)) ^ x, modulus) == 1
               for ell, _ in prime_powers(degree))


def fixture_field(d):
    # Explicit construction of small TEST INPUTS; not the acquired generator.
    if d == 1:
        return BinaryField(1, 3)
    for tail in range(1, 1 << d, 2):
        modulus = (1 << d) | tail
        if irreducible(d, modulus):
            return BinaryField(d, modulus)
    raise AssertionError("irreducible polynomial missing")


class AbstractAlgebra:
    """A disguised multiplication table; the acquisition only uses mul/one."""
    def __init__(self, field, rng):
        self.d = field.d
        columns = [1 << i for i in range(self.d)]
        for _ in range(20*self.d):
            if self.d > 1:
                a, b = rng.sample(range(self.d), 2)
                columns[a] ^= columns[b]
        self.table = [[solve(columns, field.mul(a,b)) for b in columns]
                      for a in columns]
        self.one = solve(columns, 1)
        self.fixture_columns = columns

    def mul(self, a, b):
        out = 0
        for i in range(self.d):
            if a >> i & 1:
                for j in range(self.d):
                    if b >> j & 1:
                        out ^= self.table[i][j]
        return out

    def frobenius(self, a, iterations=1):
        for _ in range(iterations):
            a = self.mul(a, a)
        return a


class TruncatedRing:
    """Finite test input F_{2^a}[epsilon]/(epsilon^height)."""
    def __init__(self, field, height):
        self.field, self.height = field, height
        self.d = field.d*height

    def mul(self, a, b):
        width = self.field.d
        mask = (1<<width)-1
        out = [0]*self.height
        for i in range(self.height):
            for j in range(self.height-i):
                out[i+j] ^= self.field.mul((a>>(i*width))&mask,(b>>(j*width))&mask)
        return sum(c<<(i*width) for i,c in enumerate(out))


def acquire_reduced_field(algebra):
    """Extract the canonical coefficient field of a connected algebra."""
    d = algebra.d
    assert len(kernel([algebra.frobenius(1<<i)^(1<<i) for i in range(d)])) == 1
    image = [1<<i for i in range(d)]
    iterations = 0
    while True:
        squared = [algebra.frobenius(x) for x in image]
        basis = []
        for x in squared:
            if rank(basis+[x]) > len(basis):
                basis.append(x)
        iterations += 1
        if len(basis) == len(image):
            image = basis
            break
        image = basis
    field = AbstractAlgebra.__new__(AbstractAlgebra)
    field.d = len(image)
    field.table = [[solve(image,algebra.mul(a,b)) for b in image] for a in image]
    field.one = solve(image,algebra.one)
    assert field.one is not None
    assert all(c is not None for row in field.table for c in row)
    return field,image,iterations


def acquire_generator(algebra):
    """Deterministic polynomial algorithm, without enumerating the field."""
    d = algebra.d
    alpha = 0
    parts = []
    for ell, power in prime_powers(d):
        fixed = kernel([algebra.frobenius(1 << i, power) ^ (1 << i)
                        for i in range(d)])
        assert len(fixed) == power
        gamma = next(v for v in fixed
                     if algebra.frobenius(v, power//ell) != v)
        alpha ^= gamma
        parts.append({"prime":ell,"degree":power,"element":gamma})
    if d == 1:
        alpha = algebra.one
    powers, a = [], algebra.one
    for _ in range(d):
        powers.append(a)
        a = algebra.mul(a, alpha)
    assert rank(powers) == d
    coefficients = solve(powers, a)
    minimal_polynomial = (1 << d) | coefficients
    assert irreducible(d, minimal_polynomial)
    return {"degree":d,"generator":alpha,"components":parts,
            "minimal_polynomial":minimal_polynomial}


def candidates(b, D):
    atoms = [(i, 1 << j) for i in range(b)
             for j in range(D.bit_length()) if (1 << j) <= D]
    out = {(0,)*b}
    for length in (1,2,3):
        for indices in combinations(range(len(atoms)+length-1), length):
            # Standard stars-and-bars enumeration of nondecreasing atom tuples.
            positions = [indices[t]-t for t in range(length)]
            exponent = [0]*b
            for pos in positions:
                i, e = atoms[pos]
                exponent[i] += e
            if sum(exponent) <= D:
                out.add(tuple(exponent))
    return sorted(out)


def field_monomial(field, values, exponent):
    out = 1
    for value, power in zip(values, exponent):
        out = field.mul(out, field.pow(value, power))
    return out


def binary_values(x, b, d):
    mask = (1 << d)-1
    return [(x >> (i*d)) & mask for i in range(b)]


def evaluation_vector(field, b, exponent, coefficient, inputs):
    return sum(field.trace(field.mul(coefficient,
                    field_monomial(field,binary_values(x,b,field.d),exponent))) << t
               for t,x in enumerate(inputs))


def full_anf(values, n):
    coeffs = list(values)
    for i in range(n):
        for x in range(1 << n):
            if x >> i & 1:
                coeffs[x] ^= coeffs[x ^ (1 << i)]
    return [mask for mask,c in enumerate(coeffs) if c]


def random_invertible_field_matrix(field, b, rng):
    matrix = [[int(i==j) for j in range(b)] for i in range(b)]
    for _ in range(10*b):
        if b > 1:
            a,c = rng.sample(range(b),2)
            scale = rng.randrange(1,field.q)
            matrix[a] = [u ^ field.mul(scale,v)
                         for u,v in zip(matrix[a],matrix[c])]
    return matrix


def fit_affine_fixture(field, b, D, rng):
    n = b * field.d
    exponents = candidates(b,D)
    coefficients = [rng.randrange(field.q) for _ in exponents]
    M = random_invertible_field_matrix(field,b,rng)
    shift = [rng.randrange(field.q) for _ in range(b)]

    def target(x):
        X = binary_values(x,b,field.d)
        Y = [shift[i] ^ sum_xor(field.mul(M[i][j],X[j]) for j in range(b))
             for i in range(b)]
        return field.trace(sum_xor(field.mul(c,field_monomial(field,Y,e))
                                  for c,e in zip(coefficients,exponents)))

    sparse_inputs = [mask for mask in range(1<<n) if mask.bit_count() <= 3]
    columns = [evaluation_vector(field,b,e,1<<j,sparse_inputs)
               for e in exponents for j in range(field.d)]
    target_vector = sum(target(x)<<t for t,x in enumerate(sparse_inputs))
    solution = solve(columns,target_vector)
    assert solution is not None
    recovered = [sum(((solution >> (i*field.d+j))&1)<<j
                     for j in range(field.d)) for i in range(len(exponents))]
    truth = []
    for x in range(1<<n):
        X = binary_values(x,b,field.d)
        out = field.trace(sum_xor(field.mul(c,field_monomial(field,X,e))
                                 for c,e in zip(recovered,exponents)))
        expected = target(x)
        assert out == expected
        truth.append(out)
    anf = full_anf(truth,n)
    assert max((mask.bit_count() for mask in anf),default=0) <= 3
    return {"field_degree":field.d,"field_variables":b,"inputs":n,
            "ordinary_degree_cap":D,"candidate_monomials":len(exponents),
            "coefficient_columns":len(columns),"fit_rows":len(sparse_inputs),
            "truth_table_checks":1<<n,"anf_terms":len(anf),
            "exact_zero_count":truth.count(0),"image_dimension":rank(columns)}


def sum_xor(values):
    out = 0
    for v in values:
        out ^= v
    return out


def run():
    rng = random.Random(20261027031)
    generators = []
    for d in [1,2,3,4,5,6,8,9,10,12,15,18]:
        field = fixture_field(d)
        for _ in range(3):
            algebra = AbstractAlgebra(field,rng)
            result = acquire_generator(algebra)
            result["input_modulus"] = field.modulus
            generators.append(result)
    local_rings = []
    for a,height in [(2,2),(3,3),(4,4),(6,2)]:
        ring = TruncatedRing(fixture_field(a),height)
        for _ in range(3):
            algebra = AbstractAlgebra(ring,rng)
            field,embedding,steps = acquire_reduced_field(algebra)
            assert field.d == a
            result = acquire_generator(field)
            local_rings.append({"algebra_dimension":algebra.d,"nilpotent_height":height,
                                "residue_field_degree":a,"frobenius_image_steps":steps,
                                "minimal_polynomial":result["minimal_polynomial"]})
    fits = [fit_affine_fixture(fixture_field(d),b,D,rng)
            for d,b,D in [(2,3,3),(3,3,3),(3,3,5),(4,2,9),(5,2,17)]]
    return {"status":"all exact assertions passed",
            "abstract_algebra_generator_cases":len(generators),
            "generator_algorithm_enumerates_field":False,
            "generator_records":generators,"affine_field_fit_records":fits,
            "nonsemisimple_centroid_cases":len(local_rings),"local_ring_records":local_rings,
            "full_truth_checks":sum(r["truth_table_checks"] for r in fits),
            "point_count_backend_executed":False,"speed_claim":False}


if __name__ == "__main__":
    result = run()
    Path(__file__).with_name("field_acquisition_audit_results.json").write_text(
        json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if not k.endswith("records")},indent=2))
