"""Exact scalar-echo compiler. No hidden dimension/rank enters this API.

Native source: self-adjoint contractions in one Hilbert metric, reset/read
vector b, simultaneous scalar word intervals. Numerical maps are untrusted
proposals; Fraction arithmetic validates their measured residuals.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt

def canonical(word):
    w = tuple(word)
    return min(w, w[::-1])

def echo_word(left, middle, right):
    return canonical(tuple(right)+tuple(middle)+tuple(left)[::-1])

def add_term(expr, word, coeff):
    if coeff:
        w = canonical(word)
        expr[w] = expr.get(w, F(0))+coeff
        if not expr[w]:
            del expr[w]

def add_expr(target, source, scale=F(1)):
    for w, c in source.items():
        add_term(target, w, scale*c)
    return target

def bilinear_expr(dictionary, left, middle, right):
    out = {}
    for j, x in enumerate(left):
        if x:
            for k, y in enumerate(right):
                if y:
                    add_term(out, echo_word(dictionary[j], middle, dictionary[k]), x*y)
    return out

def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))

def matvec(a, x):
    return [dot(row, x) for row in a]

def sqrt_upper(x, bits=72):
    if x < 0:
        raise ValueError('Negative residual upper bound contradicts source/instrument premises')
    if not x:
        return F(0)
    scale = 1 << bits
    k = isqrt((x.numerator*scale*scale)//x.denominator)
    q = F(k, scale)
    if q*q < x:
        q = F(k+1, scale)
    assert q*q >= x
    return q

@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F
    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError('Inverted interval')
    @property
    def center(self):
        return (self.lo+self.hi)/2
    @property
    def radius(self):
        return (self.hi-self.lo)/2
    def contains(self, x):
        return self.lo <= x <= self.hi

def interval_expr(expr, records):
    lo, hi = F(0), F(0)
    for w, c in expr.items():
        q = records[w]
        if c >= 0:
            lo += c*q.lo
            hi += c*q.hi
        else:
            lo += c*q.hi
            hi += c*q.lo
    return Interval(lo, hi)

class EchoCompiler:
    def __init__(self, dictionary, alphabet_size, records, maps):
        self.dictionary = [tuple(w) for w in dictionary]
        self.q = alphabet_size
        self.r = len(dictionary)
        if self.dictionary[0] != ():
            raise ValueError('Dictionary must start with reset vector')
        self.records = {canonical(w): v for w, v in records.items()}
        self.maps = maps
        self.initial = [F(1)]+[F(0)]*(self.r-1)
        missing = self.required_words(self.dictionary, self.q)-self.records.keys()
        if missing:
            raise ValueError(f'Missing {len(missing)} echo intervals')

    @staticmethod
    def required_words(dictionary, alphabet_size):
        words = set()
        for j in range(len(dictionary)):
            for k in range(j, len(dictionary)):
                words.add(echo_word(dictionary[j], (), dictionary[k]))
                for i in range(alphabet_size):
                    words.add(echo_word(dictionary[j], (i,), dictionary[k]))
                    words.add(echo_word(dictionary[j], (i, i), dictionary[k]))
        return words

    def gram_centers(self, middle=()):
        return [[self.records[echo_word(a, middle, b)].center
                 for b in self.dictionary] for a in self.dictionary]

    def defect_expr(self, i, left, right):
        out = bilinear_expr(self.dictionary, left, (i,), right)
        return add_expr(out, bilinear_expr(self.dictionary, left, (),
                                           matvec(self.maps[i], right)), F(-1))

    def residual_sq_expr(self, i, x):
        tx = matvec(self.maps[i], x)
        out = bilinear_expr(self.dictionary, x, (i, i), x)
        add_expr(out, bilinear_expr(self.dictionary, x, (i,), tx), F(-2))
        add_expr(out, bilinear_expr(self.dictionary, tx, (), tx))
        return out

    def residual_expr(self, i, left, right):
        tl = matvec(self.maps[i], left)
        tr = matvec(self.maps[i], right)
        out = bilinear_expr(self.dictionary, left, (i, i), right)
        add_expr(out, bilinear_expr(self.dictionary, left, (i,), tr), F(-1))
        add_expr(out, bilinear_expr(self.dictionary, tl, (i,), right), F(-1))
        add_expr(out, bilinear_expr(self.dictionary, tl, (), tr))
        return out

    def certificate(self, word, sqrt_bits=72):
        w = tuple(word)
        h = len(w)
        forward = [self.initial]
        for i in w:
            forward.append(matvec(self.maps[i], forward[-1]))
        backward = [None]*(h+1)
        backward[h] = self.initial
        for s in range(h-1, -1, -1):
            backward[s] = matvec(self.maps[w[s]], backward[s+1])
        prediction = bilinear_expr(self.dictionary, self.initial, (), forward[h])
        uncorrected = interval_expr(prediction, self.records)
        correction = {}
        a, b = [], []
        first_order_radius = F(0)
        for s, i in enumerate(w):
            expr = self.defect_expr(i, backward[s+1], forward[s])
            add_expr(correction, expr)
            first = interval_expr(expr, self.records)
            first_order_radius += max(abs(first.lo), abs(first.hi))
            af = interval_expr(self.residual_sq_expr(i, forward[s]), self.records)
            ab = interval_expr(self.residual_sq_expr(i, backward[s+1]), self.records)
            a.append(sqrt_upper(af.hi, sqrt_bits))
            b.append(sqrt_upper(ab.hi, sqrt_bits))
        add_expr(prediction, correction)
        corrected = interval_expr(prediction, self.records)
        remainder, accumulated = F(0), F(0)
        for s in range(h):
            remainder += accumulated*b[s]
            accumulated += a[s]
        raw = Interval(corrected.lo-remainder, corrected.hi+remainder)
        norm_hi = self.records[()].hi
        final = Interval(max(raw.lo, -norm_hi), min(raw.hi, norm_hi))
        old = Interval(uncorrected.lo-first_order_radius-remainder,
                       uncorrected.hi+first_order_radius+remainder)
        return {'interval': final, 'raw_interval': raw,
                'uncorrected_prediction': uncorrected,
                'corrected_prediction': corrected,
                'uncorrected_absolute_defect_interval': old,
                'remainder': remainder,
                'first_order_absolute_bound': first_order_radius,
                'native_coefficient_l1': sum(map(abs, prediction.values()), F(0)),
                'native_records_used': len(prediction),
                'max_coefficient_bits': max((max(x.numerator.bit_length(),
                    x.denominator.bit_length()) for vec in forward+backward
                    for x in vec), default=1),
                'forward_residual_upper': a, 'backward_residual_upper': b}

def propose_maps(dictionary, q, records, quantum=10**8, ridge=0.0, shrink=1.0):
    import numpy as np
    r = len(dictionary)
    g = np.array([[float(records[echo_word(a, (), b)].center)
                   for b in dictionary] for a in dictionary])
    maps = []
    for i in range(q):
        m = np.array([[float(records[echo_word(a, (i,), b)].center)
                       for b in dictionary] for a in dictionary])
        try:
            t = shrink*np.linalg.solve(g+ridge*np.eye(r), m)
            if not np.all(np.isfinite(t)):
                raise ValueError('Nonfinite proposal')
        except (np.linalg.LinAlgError, ValueError):
            t = np.zeros((r, r))
        maps.append([[F(int(round(float(v)*quantum)), quantum) for v in row]
                     for row in t])
    return maps
