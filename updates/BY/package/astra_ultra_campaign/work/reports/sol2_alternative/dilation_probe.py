import math
import numpy as np


def g(r):
    if r <= 0:
        return 0.0
    return (r + 1) * math.log1p(r) - r * math.log(r)


def invg(s):
    low, high = 0.0, math.exp(s) + 1
    for _ in range(90):
        mid = (low + high) / 2
        if g(mid) < s:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def entropy(p):
    pos = p > 0
    return -float(np.dot(p[pos], np.log(p[pos])))


def thermal(r, length):
    m = np.arange(length)
    return np.exp(-math.log1p(r) + m * math.log(r / (r + 1)))


def rates(p):
    k = np.arange(len(p) - 1) + 1
    ratio = np.log(p[:-1] / p[1:])
    minus = float(np.dot(k * p[1:], -ratio))
    plus = float(np.dot(k * p[:-1], ratio))
    return minus, plus


def dilation_fock(k, t, length):
    a = (t - 1) / (t + 1)
    out = np.zeros(length)
    for m in range(length):
        if m > k + 50 and a < 1e-3:
            continue
        terms = []
        for j in range(min(k, m) + 1):
            power = k + m - 2 * j
            if power == 0:
                term = math.comb(k, j) * math.comb(k + m - j, k)
            else:
                logterm = (
                    math.lgamma(k + 1) - math.lgamma(j + 1) - math.lgamma(k - j + 1)
                    + math.lgamma(k + m - j + 1) - math.lgamma(k + 1) - math.lgamma(m - j + 1)
                    + power * math.log(a)
                )
                term = math.exp(logterm) if logterm > -745 else 0.0
            terms.append(((-1) ** (k - j)) * term)
        out[m] = 2 / (t + 1) * math.fsum(terms)
    return out


def build(pfinite, eps=0.01, r=100, length=8000):
    p = eps * thermal(r, length)
    p[:len(pfinite)] += (1 - eps) * np.array(pfinite)
    return p


def check(pfinite, eps, r, t, length=8000):
    p = build(pfinite, eps, r, length)
    q = eps * thermal(t * (r + 0.5) - 0.5, length)
    for k, pk in enumerate(pfinite):
        if pk:
            q += (1 - eps) * pk * dilation_fock(k, t, length)
    sin = entropy(p)
    sout = entropy(q)
    n = invg(sin)
    nout = invg(sout)
    minus, plus = rates(p)
    deriv = (plus - minus) / 2
    target_deriv = (n + 0.5) * math.log1p(1 / n)
    return {
        'finite': pfinite, 'eps': eps, 'r': r, 't': t,
        'sin': sin, 'sout': sout, 'n': n, 'nout': nout,
        'desired': t * (n + 0.5) - 0.5,
        'n_defect': nout - (t * (n + 0.5) - 0.5),
        'minq': float(np.min(q)), 'sumq': float(np.sum(q)),
        'dilation_rate': deriv, 'target_rate': target_deriv,
        'rate_defect': deriv - target_deriv,
        'first20q': q[:20].tolist(),
    }


if __name__ == '__main__':
    for k in [1, 2, 5, 10, 20, 50, 100]:
        pfinite = [0.0] * k + [1.0]
        for eps in [0.1, 0.01, 0.001]:
            result = check(pfinite, eps, 100, 1 + eps / 10000)
            if result['rate_defect'] < 0:
                print(result)
