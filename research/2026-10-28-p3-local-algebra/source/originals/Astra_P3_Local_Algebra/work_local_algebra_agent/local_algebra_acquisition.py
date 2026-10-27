#!/usr/bin/env python3
"""Exact chain-algebra acquisition from raw Boolean cubic ANF.

No field, ring, hidden coordinates, or decomposition are supplied. This is
representation acquisition, not a counting backend. Ring elements are packed
in d-bit field coefficients, low power of the uniformizer first.
"""
from itertools import combinations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"work_field_root"))
from field_descent import (bits, linear_apply, compose, flat, unflat, span,
                          solve, kernel_columns, centroid, tensor_value,
                          polynomial_value, prime_powers)
from field_kloosterman import gf_mul, gf_trace


def independent(columns):
    return [v for v, _ in span(columns).values()]


class Solver:
    def __init__(self, columns):
        self.pivots = span(columns)

    def __call__(self, target):
        answer = 0
        while target:
            p = (target & -target).bit_length()-1
            if p not in self.pivots:
                return None
            v, c = self.pivots[p]
            target ^= v
            answer ^= c
        return answer


class ChainRing:
    def __init__(self, modulus, length):
        if length < 1:
            raise ValueError("chain length must be positive")
        self.h = modulus
        self.d = modulus.bit_length()-1
        self.e = length
        self.m = self.d*self.e
        self.mask = (1 << self.d)-1

    def mul(self, a, b):
        result = 0
        for i in range(self.e):
            ai = (a >> (self.d*i)) & self.mask
            if not ai:
                continue
            for j in range(self.e-i):
                bj = (b >> (self.d*j)) & self.mask
                if bj:
                    result ^= gf_mul(ai, bj, self.h) << (self.d*(i+j))
        return result

    def functional(self, a):
        return gf_trace((a >> (self.d*(self.e-1))) & self.mask, self.h)

    def gram(self):
        return [sum(self.functional(self.mul(1 << i, 1 << j)) << i
                    for i in range(self.m)) for j in range(self.m)]


def acquire_chain_algebra(algebra, n, *, require_free=True):
    """Recognize a matrix algebra as F_(2^d)[pi]/pi^e and acquire coordinates.

    The production entry point obtains this algebra from a radical-free tensor.
    This function also verifies identity, closure and commutation.
    """
    m = len(algebra)
    if not m or any(len(A) != n for A in algebra):
        raise ValueError("invalid matrix algebra dimensions")
    if require_free and (m > n or n % m):
        raise ValueError("algebra dimension is incompatible with a free module")
    af = [flat(A, n) for A in algebra]
    solver = Solver(af)
    if len(solver.pivots) != m:
        raise ValueError("algebra basis is dependent")
    one = solver(flat([1 << i for i in range(n)], n))
    if one is None:
        raise ValueError("algebra has no identity")
    table = []
    for A in algebra:
        row = []
        for B in algebra:
            AB = compose(A, B)
            if AB != compose(B, A):
                raise ValueError("matrix algebra is not commutative")
            c = solver(flat(AB, n))
            if c is None:
                raise ValueError("matrix algebra is not closed")
            row.append(c)
        table.append(row)

    def multiply(a, b):
        out = 0
        for i in bits(a):
            for j in bits(b):
                out ^= table[i][j]
        return out

    def operator(a):
        return unflat(linear_apply(af, a), n)

    frob = [table[i][i] for i in range(m)]
    fixed = kernel_columns([x ^ (1 << i) for i, x in enumerate(frob)])
    if len(fixed) != 1:
        raise ValueError("product algebra: primitive idempotent splitting required")
    power = [1 << i for i in range(m)]
    frobenius_steps = 0
    while True:
        nxt = [linear_apply(frob, x) for x in power]
        frobenius_steps += 1
        if len(span(nxt)) == len(span(power)):
            power = nxt
            break
        power = nxt
    field_basis = independent(power)
    radical = kernel_columns(power)
    d = len(field_basis)
    if m % d:
        raise AssertionError("residue degree does not divide algebra dimension")
    e = m//d
    square_radical = independent([multiply(a, b) for a in radical for b in radical])
    if e == 1:
        pi = 0
        if radical:
            raise AssertionError("field has nonzero radical")
    else:
        if len(radical)-len(square_radical) != d:
            raise ValueError("local algebra is not a chain ring")
        pi = next(a for a in radical if solve(square_radical, a) is None)

    field_solver = Solver(field_basis)
    field_frob = [field_solver(linear_apply(frob, a)) for a in field_basis]
    if any(x is None for x in field_frob):
        raise AssertionError("coefficient field is not Frobenius stable")

    def minpoly(a):
        powers = []
        value = one
        for degree in range(d+1):
            relation = solve(powers, value)
            if relation is not None:
                return relation | (1 << degree), powers
            powers.append(value)
            value = multiply(value, a)
        raise AssertionError("field element has no dependence")

    alpha = None
    for candidate in field_basis:
        h, fpowers = minpoly(candidate)
        if h.bit_length()-1 == d:
            alpha = candidate
            break
    if alpha is None:
        def iterate(x, times):
            for _ in range(times):
                x = linear_apply(field_frob, x)
            return x
        alpha_coordinate = 0
        for prime, prime_power in prime_powers(d):
            fixed_subfield = kernel_columns([
                iterate(1 << j, prime_power) ^ (1 << j) for j in range(d)])
            gamma = next(x for x in fixed_subfield
                         if iterate(x, prime_power//prime) != x)
            alpha_coordinate ^= gamma
        alpha = linear_apply(field_basis, alpha_coordinate)
        h, fpowers = minpoly(alpha)
    if h.bit_length()-1 != d:
        raise AssertionError("coefficient field generator has wrong degree")

    ring_basis = []
    pipower = one
    for j in range(e):
        ring_basis.extend(multiply(pipower, a) for a in fpowers)
        pipower = multiply(pipower, pi)
    if pipower or len(span(ring_basis)) != m:
        raise AssertionError("uniformizer did not certify the chain presentation")
    ring = ChainRing(h, e)
    acquired_operators = [operator(a) for a in ring_basis]
    ring_solver = Solver(ring_basis)
    for i in range(m):
        for j in range(m):
            if ring_solver(multiply(ring_basis[i], ring_basis[j])) != ring.mul(1 << i, 1 << j):
                raise AssertionError("acquired ring multiplication mismatch")

    pi_operator = operator(pi)
    pi_kernel_dimension = n-len(span(pi_operator))
    free = n % m == 0 and e*pi_kernel_dimension == n
    result = dict(n=n, algebra_dimension=m, field_degree=d, chain_length=e,
                  field_modulus=h, h=h, d=d, e=e,
                  algebra_coordinates=ring_basis,
                  ring_operators=acquired_operators, uniformizer_operator=pi_operator,
                  frobenius_steps=frobenius_steps, radical_dimension=len(radical),
                  radical_square_dimension=len(square_radical), free_module=free,
                  pi_kernel_dimension=pi_kernel_dimension)
    if not free:
        if require_free:
            raise ValueError("centroid chain ring acts on a nonfree module")
        return result
    current = independent(pi_operator)
    module_basis = []
    for i in range(n):
        v = 1 << i
        if solve(current, v) is not None:
            continue
        module_basis.append(v)
        current.extend(linear_apply(acquired_operators[t], v) for t in range(d))
    columns = [linear_apply(A, v) for v in module_basis for A in acquired_operators]
    if len(columns) != n or len(span(columns)) != n:
        raise AssertionError("Nakayama module basis failed")
    result.update(module_dimension=len(module_basis), module_basis=module_basis,
                  coordinate_columns=columns)
    return result


def acquire_raw_chain_cubic(poly, n, *, verify_cubic_coefficients=False):
    """Exact raw cubic -> chain ring, coordinates, cubic and quadratic remainder."""
    if n <= 0 or any(mask < 0 or mask >> n or mask.bit_count() > 3 for mask in poly):
        raise ValueError("requires an explicit Boolean ANF of degree at most three")
    algebra, pair, trail = centroid(poly, n)
    acquired = acquire_chain_algebra(algebra, n)
    d, e, b = (acquired[k] for k in ("field_degree", "chain_length", "module_dimension"))
    ring = ChainRing(acquired["field_modulus"], e)
    m = d*e
    columns = acquired["coordinate_columns"]
    gram_solver = Solver(ring.gram())
    if len(gram_solver.pivots) != m:
        raise AssertionError("chain ring Frobenius pairing is degenerate")
    cubic = {}
    for i, j, k in combinations(range(b), 3):
        evaluations = sum(tensor_value(pair, columns[m*i+t], columns[m*j], columns[m*k]) << t
                          for t in range(m))
        c = gram_solver(evaluations)
        if c is None:
            raise AssertionError("Frobenius lift has no coefficient")
        if c:
            cubic[i, j, k] = c

    def base_value(y):
        values = [(y >> (m*i)) & ((1 << m)-1) for i in range(b)]
        value = 0
        for (i, j, k), c in cubic.items():
            value ^= ring.mul(c, ring.mul(values[i], ring.mul(values[j], values[k])))
        return ring.functional(value)

    differences = {}
    def difference(y):
        if y not in differences:
            differences[y] = polynomial_value(poly, linear_apply(columns, y)) ^ base_value(y)
        return differences[y]

    constant = difference(0)
    unary = [difference(1 << i) ^ constant for i in range(n)]
    remainder = set([0]) if constant else set()
    remainder.update(1 << i for i, value in enumerate(unary) if value)
    for i, j in combinations(range(n), 2):
        if difference((1 << i) ^ (1 << j)) ^ constant ^ unary[i] ^ unary[j]:
            remainder.add((1 << i) ^ (1 << j))
    if verify_cubic_coefficients:
        for i, j, k in combinations(range(n), 3):
            mask = (1 << i) ^ (1 << j) ^ (1 << k)
            delta = 0
            sub = mask
            while True:
                delta ^= difference(sub)
                if sub == 0:
                    break
                sub = (sub-1) & mask
            if delta:
                raise AssertionError("acquired cubic leaves a nonquadratic remainder")
    acquired.update(cubic=[dict(indices=list(indices), coefficient=c) for indices, c in cubic.items()],
                    quadratic_remainder=sorted(remainder), centroid_dimension_trail=trail,
                    cubic_coefficients_explicitly_checked=verify_cubic_coefficients)
    return acquired


acquire_chain = acquire_raw_chain_cubic


def reconstructed_value(acquired, y):
    ring = ChainRing(acquired["field_modulus"], acquired["chain_length"])
    m = ring.m
    mask = (1 << m)-1
    values = [(y >> (m*i)) & mask for i in range(acquired["module_dimension"])]
    value = 0
    for item in acquired["cubic"]:
        i, j, k = item["indices"]
        value ^= ring.mul(item["coefficient"], ring.mul(values[i], ring.mul(values[j], values[k])))
    return ring.functional(value) ^ polynomial_value(acquired["quadratic_remainder"], y)


def split_local_matrix_algebras(algebra, n):
    """Acquire all primitive idempotent components without enumerating elements.

    The algebra must already be a unital commutative matrix algebra, as a
    radical-free tensor centroid is. Each returned inclusion is into the
    original n-bit space, and each restricted algebra acts faithfully there.
    """
    af = [flat(A, n) for A in algebra]
    solver = Solver(af)
    one = solver(flat([1 << i for i in range(n)], n))
    if one is None:
        raise ValueError("algebra identity is missing")
    frob = [solver(flat(compose(A, A), n)) for A in algebra]
    if any(x is None for x in frob):
        raise ValueError("algebra is not closed under squaring")
    fixed = kernel_columns([a ^ (1 << i) for i, a in enumerate(frob)])
    if len(fixed) == 1:
        return [dict(inclusion_columns=[1 << i for i in range(n)],
                     dimension=n, algebra=algebra)]
    idempotent = next(x for x in fixed if x not in (0, one))
    P = unflat(linear_apply(af, idempotent), n)
    if compose(P, P) != P:
        raise AssertionError("Frobenius-fixed element is not idempotent")
    out = []
    for projection in (P, [P[i] ^ (1 << i) for i in range(n)]):
        columns = independent(projection)
        k = len(columns)
        if not k or k == n:
            raise AssertionError("nontrivial idempotent did not split the module")
        inclusion_solver = Solver(columns)
        restricted = []
        for A in algebra:
            image = [inclusion_solver(linear_apply(A, v)) for v in columns]
            if any(x is None for x in image):
                raise AssertionError("central idempotent image is not invariant")
            restricted.append(flat(image, k))
        basis = [unflat(x, k) for x in independent(restricted)]
        for component in split_local_matrix_algebras(basis, k):
            component["inclusion_columns"] = [linear_apply(columns, v)
                                                for v in component["inclusion_columns"]]
            out.append(component)
    return out


def acquire_product_chain_cubic(poly, n, *, verify_cubic_coefficients=False):
    """Acquire a product of free chain-ring modules plus its exact quadratic glue.

    Returns no count. Arbitrary cross-component quadratic interactions remain
    visible in quadratic_remainder, so no independence is silently assumed.
    """
    if n <= 0 or any(mask < 0 or mask >> n or mask.bit_count() > 3 for mask in poly):
        raise ValueError("requires an explicit Boolean ANF of degree at most three")
    algebra, pair, trail = centroid(poly, n)
    components = []
    all_columns = []
    bit_offset = 0
    for part in split_local_matrix_algebras(algebra, n):
        acquired = acquire_chain_algebra(part["algebra"], part["dimension"])
        local_columns = acquired["coordinate_columns"]
        global_columns = [linear_apply(part["inclusion_columns"], v) for v in local_columns]
        ring = ChainRing(acquired["h"], acquired["e"])
        m, b = ring.m, acquired["module_dimension"]
        gram_solver = Solver(ring.gram())
        cubic = []
        for i, j, k in combinations(range(b), 3):
            rhs = sum(tensor_value(pair, global_columns[m*i+t], global_columns[m*j],
                                   global_columns[m*k]) << t for t in range(m))
            c = gram_solver(rhs)
            if c is None:
                raise AssertionError("component Frobenius lift failed")
            if c:
                cubic.append(dict(indices=[i, j, k], coefficient=c))
        acquired.update(cubic=cubic, quadratic_remainder=[], bit_offset=bit_offset,
                        global_coordinate_columns=global_columns)
        components.append(acquired)
        all_columns.extend(global_columns)
        bit_offset += part["dimension"]
    if len(all_columns) != n or len(span(all_columns)) != n:
        raise AssertionError("primitive components do not reconstruct original input space")

    def base_value(y):
        out = 0
        for component in components:
            local = (y >> component["bit_offset"]) & ((1 << component["n"])-1)
            out ^= reconstructed_value(component, local)
        return out
    differences = {}
    def difference(y):
        if y not in differences:
            differences[y] = polynomial_value(poly, linear_apply(all_columns, y)) ^ base_value(y)
        return differences[y]
    constant = difference(0)
    unary = [difference(1 << i) ^ constant for i in range(n)]
    remainder = set([0]) if constant else set()
    remainder.update(1 << i for i, value in enumerate(unary) if value)
    for i, j in combinations(range(n), 2):
        if difference((1 << i) ^ (1 << j)) ^ constant ^ unary[i] ^ unary[j]:
            remainder.add((1 << i) ^ (1 << j))
    if verify_cubic_coefficients:
        for i, j, k in combinations(range(n), 3):
            mask = (1 << i) | (1 << j) | (1 << k)
            delta = 0
            sub = mask
            while True:
                delta ^= difference(sub)
                if not sub:
                    break
                sub = (sub-1) & mask
            if delta:
                raise AssertionError("component construction left a cubic cross interaction")
    for index, component in enumerate(components):
        offset, width = component["bit_offset"], component["n"]
        support = ((1 << width)-1) << offset
        component["local_quadratic_remainder"] = sorted(
            mask >> offset for mask in remainder
            if (mask and not (mask & ~support)) or (mask == 0 and index == 0))
    return dict(n=n, components=components, coordinate_columns=all_columns,
                quadratic_remainder=sorted(remainder), centroid_dimension=len(algebra),
                centroid_dimension_trail=trail,
                cubic_coefficients_explicitly_checked=verify_cubic_coefficients)


def reconstructed_product_value(acquired, y):
    out = polynomial_value(acquired["quadratic_remainder"], y)
    for component in acquired["components"]:
        local = (y >> component["bit_offset"]) & ((1 << component["n"])-1)
        out ^= reconstructed_value(component, local)
    return out


acquire_product_chain = acquire_product_chain_cubic
