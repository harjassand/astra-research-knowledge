"""Small independent normalization controls; never imports archived programs."""
from fractions import Fraction as F
import json
from pathlib import Path


def mul(a, b, modulus):
    out = 0
    degree = modulus.bit_length() - 1
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        if a >> degree:
            a ^= modulus
        b >>= 1
    return out


def power(a, n, modulus):
    out = 1
    while n:
        if n & 1:
            out = mul(out, a, modulus)
        a = mul(a, a, modulus)
        n >>= 1
    return out


def determinant(matrix):
    a = [[F(x) for x in row] for row in matrix]
    answer = F(1)
    for i in range(len(a)):
        j = next(j for j in range(i, len(a)) if a[j][i])
        if j != i:
            a[i], a[j] = a[j], a[i]
            answer = -answer
        pivot = a[i][i]
        answer *= pivot
        for j in range(i + 1, len(a)):
            ratio = a[j][i] / pivot
            for k in range(i, len(a)):
                a[j][k] -= ratio * a[i][k]
    return answer


def controls():
    checks = []
    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)
    indices = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1)]
    for d in range(1, 6):
        q, epsilon = 1 << d, (-1) ** d
        nodes = [(-q, epsilon*q), (q, epsilon*q)] + [(x, y) for amplitude, y in ((2*q,-2*epsilon*q),(4*q,4*epsilon*q)) for x in (-amplitude,0,amplitude)]
        matrix = [[x**i * y**j for x,y in nodes] for i,j in indices]
        check('eight-state-determinant-d%d' % d, abs(determinant(matrix)) == 2**15 * 3**7 * q**14)
    check('empty-pair-factor-is-one', 0**0 == 1)
    # Ordinary F4 cubic z^3 is not the Boolean polynomial z. Count all 16
    # (z,w) pairs only; these are controls of the cardinality conversion.
    q, modulus = 4, 0b111
    points = sum(mul(w,w,modulus) ^ w ^ power(z,3,modulus) == 0 for z in range(q) for w in range(q))
    boolean_reduced = sum(mul(w,w,modulus) ^ w ^ z == 0 for z in range(q) for w in range(q))
    check('AS-cardinality-minus-q-not-twice-cardinality', points == 8 and points - q == 4 and 2*points-q != 4)
    check('ordinary-field-cube-is-not-Boolean-idempotence', boolean_reduced == 4 and points != boolean_reduced)
    # Independently verify the actual F8 critical-chart extractors.
    modulus, alpha = 0b1011, 2
    for a in (0,1):
        for b in (0,1):
            y = (alpha if a else 0) ^ (power(alpha,2,modulus) if b else 0)
            x = mul(y,y,modulus)
            check('F8-critical-equation-%d%d' % (a,b), power(y,4,modulus) ^ power(y,2,modulus) ^ y == 0)
            check('F8-linear-bit-extractor-%d%d' % (a,b), mul(power(alpha,2,modulus),x,modulus) ^ mul(power(alpha,4,modulus),y,modulus) == a)
    for n in (2,4):
        r = n + 1
        # Source polynomial includes a constant, and a cubic when n=4.
        def p(x):
            return 1 ^ ((x & 1) * ((x >> 1) & 1) * ((x >> 2) & 1) if n == 4 else (x & 1) * ((x >> 1) & 1))
        zp = sum((-1)**p(x) for x in range(1 << n))
        s0 = (-1)**p(0)
        total, weighted = 0, 0
        for a in range(1 << r):
            if a.bit_count() & 1:
                continue
            for b in range(1 << r):
                if b.bit_count() & 1 or (a & b).bit_count() & 1:
                    continue
                total += 1
                weighted += (-1)**p(a & ((1 << n)-1))
        expected = (1 << (n-1))*((1 << n)+1)
        check('F8-chart-multiplicity-N%d' % n, total == expected and weighted == (1 << (n-1))*(zp+s0))
        za = 8**(2*n+3)*(1+3*total+4*weighted)
        recovered = F(za,8**(2*n+3))-1-3*expected
        recovered = recovered/F(4*(1 << (n-1))) - s0
        check('F8-affine-signed-count-recovery-N%d' % n, recovered == zp)
    return {'scope':'Exact independent finite controls of determinant, ordinary-field/AS conversion and F8 normalization. Not a raw acquisition replay, generic point-count implementation, full ring truth table, benchmark or new measurement.', 'checks':checks, 'result':'passed'}


if __name__ == '__main__':
    value = controls()
    target = Path(__file__).with_name('DERIVED_MATH_CONTROLS.json')
    target.write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({'result':value['result'],'controls':len(value['checks'])}))
