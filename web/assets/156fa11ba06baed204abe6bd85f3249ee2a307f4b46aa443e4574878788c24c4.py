"""Finite diagnostics for the compact cocycle notes; not a general proof."""
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


def multiply_words(u, v):
    out = list(u)
    for x in v:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)


def star_words(u):
    return tuple(-x for x in reversed(u))


def ring_multiply(p, q):
    out = {}
    for u, a in p.items():
        for v, b in q.items():
            word = multiply_words(u, v)
            out[word] = out.get(word, 0) + a * b
    return {word: c for word, c in out.items() if c}


def ring_add(p, q):
    out = dict(p)
    for word, c in q.items():
        out[word] = out.get(word, 0) + c
    return {word: c for word, c in out.items() if c}


def scale(p, c):
    return {word: c * v for word, v in p.items() if c * v}


def kesten_moment(k, exponent):
    dp = {0: 1}
    for _ in range(exponent):
        nxt = {}
        for radius, number in dp.items():
            if radius:
                nxt[radius - 1] = nxt.get(radius - 1, 0) + number
            nxt[radius + 1] = nxt.get(radius + 1, 0) + number * (k if radius == 0 else k - 1)
        dp = nxt
    return dp.get(0, 0)


def check_codes():
    records = []
    for m in (2, 3, 4, 8):
        r = math.ceil(math.log2(m))
        codes = list(itertools.product((2, 3), repeat=r))[:m]
        bases = [code + code for code in codes]
        signed = {j + 1: word for j, word in enumerate(bases)}
        signed.update({-j: star_words(word) for j, word in list(signed.items())})
        checked = 0
        smallest_core = None
        letters = list(signed)
        for size in range(1, 5):
            for abstract in itertools.product(letters, repeat=size):
                if any(a == -b for a, b in zip(abstract, abstract[1:])):
                    continue
                concrete = ()
                for letter in abstract:
                    concrete = multiply_words(concrete, signed[letter])
                assert concrete, (m, abstract)
                checked += 1
                smallest_core = len(concrete) if smallest_core is None else min(smallest_core, len(concrete))
        records.append({"m": m, "r": r, "reduced_abstract_words_checked": checked,
                        "minimum_reduced_length": smallest_core,
                        "w_length": m * (2 * r + 1) + 1})
    return records


def check_moments():
    records = []
    for m in range(1, 5):
        t = {(): 1, **{(j,): 1 for j in range(1, m + 1)}}
        tstar = {star_words(word): c for word, c in t.items()}
        q = ring_multiply(t, tstar)
        power = {(): 1}
        moments = []
        for exponent in range(1, 5):
            power = ring_multiply(power, q)
            moment = power.get((), 0)
            assert moment == kesten_moment(m + 1, 2 * exponent)
            moments.append(moment)
        records.append({"m": m, "Q_moments_1_through_4": moments})
    return records


def check_finite_polynomial():
    m = 2
    t = {(): Fraction(1), **{(j,): Fraction(1) for j in range(1, m + 1)}}
    tstar = {star_words(word): c for word, c in t.items()}
    q = ring_multiply(t, tstar)
    c = 4 * m + 1
    transition = ring_add({(): Fraction(1 - 1 / c)}, scale(q, Fraction(-1, c)))
    # Replace the floating 1-1/c above by an exact fraction.
    transition[()] = Fraction(1) - Fraction(1, c) - q.get((), 0) / c
    power = {(): Fraction(1)}
    polynomial = {}
    records = []
    for degree in range(7):
        polynomial = ring_add(polynomial, scale(power, Fraction(1, c)))
        h = ring_multiply(tstar, polynomial)
        error = ring_add(ring_multiply(t, h), {(): Fraction(-1)})
        hn = sum(a * a for a in h.values())
        en = sum(a * a for a in error.values())
        total = hn + en
        exact_infinite_minimum = 4 / (1 + 3 * math.sqrt(9))
        assert float(total) + 1e-14 >= exact_infinite_minimum
        assert all(isinstance(a, Fraction) for a in h.values())
        records.append({"m": m, "degree": degree, "expanded_support": len(h),
                        "norm_squared": float(hn), "residual_squared": float(en),
                        "norm_plus_residual_squared": float(total),
                        "resolvent_limit": exact_infinite_minimum})
        power = ring_multiply(power, transition)
    return records


def simpson(function, pieces=20000):
    step = math.pi / (2 * pieces)
    value = function(0.0) + function(math.pi / 2)
    for index in range(1, pieces):
        value += (4 if index % 2 else 2) * function(index * step)
    return value * step / 3


def check_integrals():
    records = []
    for m in (1, 2, 3, 10, 100, 1000):
        def density(theta):
            if m == 1:
                return 2 / math.pi
            sine, cosine = math.sin(theta), math.cos(theta)
            return 4 * m * (m + 1) * cosine * cosine / (math.pi * ((m + 1) ** 2 - 4 * m * sine * sine))
        def qvalue(theta):
            return 4 * m * math.sin(theta) ** 2
        mass = simpson(density)
        trace = simpson(lambda theta: density(theta) * qvalue(theta))
        residual = simpson(lambda theta: density(theta) / (qvalue(theta) + 1) ** 2)
        hnorm = simpson(lambda theta: density(theta) * qvalue(theta) / (qvalue(theta) + 1) ** 2)
        resolvent = 2 * m / (m - 1 + (m + 1) * math.sqrt(1 + 4 * m))
        assert abs(mass - 1) < 1e-10
        assert abs(trace - (m + 1)) < 1e-8
        assert abs(residual + hnorm - resolvent) < 1e-10
        records.append({"m": m, "mass": mass, "mean": trace,
                        "norm_squared": hnorm, "residual_squared": residual,
                        "R_m_1": resolvent})
    return records


def check_exact_radial_polynomials():
    def padd(a, b):
        result = [Fraction(0)] * max(len(a), len(b))
        for i, value in enumerate(a):
            result[i] += value
        for i, value in enumerate(b):
            result[i] += value
        return result
    records = []
    for m in (1, 2, 3, 4):
        d = m + 1
        t = {(): Fraction(1), **{(j,): Fraction(1) for j in range(1, m + 1)}}
        tstar = {star_words(word): c for word, c in t.items()}
        q = ring_multiply(t, tstar)
        fs = [[Fraction(1)], [Fraction(0), Fraction(1)],
              [Fraction(-d), Fraction(0), Fraction(1)]]
        for index in range(3, 9):
            fs.append(padd([Fraction(0)] + fs[-1], [-m * value for value in fs[-2]]))
        for radius in range(1, 5):
            kr = Fraction(m + radius * d, m)
            qp = [Fraction(1)]
            for index in range(1, radius + 1):
                assert all(value == 0 for value in fs[2 * index][1::2])
                even = fs[2 * index][::2]
                qp = padd(qp, [Fraction((-1) ** index, m ** index) * value for value in even])
            qp = [value / kr for value in qp]
            assert qp[0] == 1
            hp = [-value for value in qp[1:]]
            power = {(): Fraction(1)}
            polynomial = {}
            for value in hp:
                polynomial = ring_add(polynomial, scale(power, value))
                power = ring_multiply(power, q)
            h = ring_multiply(tstar, polynomial)
            error = ring_add(ring_multiply(t, h), {(): Fraction(-1)})
            hn = sum(value * value for value in h.values())
            en = sum(value * value for value in error.values())
            assert en == Fraction(m, m + radius * d)
            assert hn == Fraction(d * radius * (radius + 1) * (2 * radius + 1),
                                  6 * (m + radius * d) ** 2)
            records.append({"m": m, "r": radius, "expanded_h_support": len(h),
                            "norm_squared_exact": str(hn), "residual_squared_exact": str(en)})
    return records


if __name__ == "__main__":
    results = {"scope": "Finite exact word and rational-coefficient diagnostics plus quadrature; not proof certification.",
               "codes": check_codes(), "moments": check_moments(),
               "finite_polynomial": check_finite_polynomial(), "integrals": check_integrals(),
               "exact_radial_polynomials": check_exact_radial_polynomials()}
    output = Path(__file__).with_name("diagnostics.json")
    output.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"status": "passed", "output": str(output.resolve()),
                      "code_words_checked": sum(row["reduced_abstract_words_checked"] for row in results["codes"]),
                      "moment_fixtures": 16, "polynomial_fixtures": 7, "quadrature_cases": 6,
                      "exact_radial_polynomial_fixtures": 16}))
