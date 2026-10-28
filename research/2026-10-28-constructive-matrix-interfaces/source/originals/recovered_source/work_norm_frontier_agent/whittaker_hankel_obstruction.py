#!/usr/bin/env python3
"""Exact Hankel tests for the profile functional and its full Gaussian convolution.

This is a research oracle, not the proposed production counter.  It deliberately
enumerates partitions to test the rank lower bound for compositional linear
summaries.  The proof is in HALL_LINEAR_SUMMARY_OBSTRUCTION.tex.
"""
from functools import lru_cache
from math import comb, factorial
from pathlib import Path
import json
import time


@lru_cache(None)
def partitions(n, maximum=None):
    if n == 0:
        return ((),)
    if maximum is None:
        maximum = n
    return tuple((k,) + p for k in range(min(n, maximum), 0, -1)
                 for p in partitions(n-k, k))


@lru_cache(None)
def gaussian_binomial(n, k, q):
    if k < 0 or k > n:
        return 0
    if not k or k == n:
        return 1
    return gaussian_binomial(n-1, k-1, q) + q**k*gaussian_binomial(n-1, k, q)


def dominates(lam, alpha):
    left = right = 0
    for i in range(max(len(lam), len(alpha))):
        if i < len(lam):
            left += lam[i]
        if i < len(alpha):
            right += alpha[i]
        if left < right:
            return False
    return True


@lru_cache(None)
def horizontal_removals(lam, size, q):
    """One-variable q-Whittaker branching; coefficients are Gaussian products."""
    tail = lam[1:] + (0,)
    drops = tuple(a-b for a, b in zip(lam, tail))
    result = []
    def rec(i, remaining, nu, coefficient):
        if i == len(lam):
            if not remaining:
                result.append((tuple(x for x in nu if x), coefficient))
            return
        for d in range(min(drops[i], remaining)+1):
            rec(i+1, remaining-d, nu+[lam[i]-d],
                coefficient*gaussian_binomial(drops[i], d, q))
    rec(0, size, [], 1)
    return tuple(result)


@lru_cache(None)
def whittaker_monomial_coefficient(lam, alpha, q):
    if not alpha:
        return int(not lam)
    if sum(lam) != sum(alpha) or not dominates(lam, alpha):
        return 0
    return sum(c*whittaker_monomial_coefficient(nu, alpha[:-1], q)
               for nu, c in horizontal_removals(lam, alpha[-1], q))


def multiply_power_monomial(r, mu):
    out = {}
    for a in set(mu):
        nu = list(mu)
        nu.remove(a)
        nu.append(a+r)
        nu.sort(reverse=True)
        nu = tuple(nu)
        out[nu] = out.get(nu, 0) + nu.count(a+r)
    nu = tuple(sorted(mu+(r,), reverse=True))
    out[nu] = out.get(nu, 0) + nu.count(r)
    return out


@lru_cache(None)
def power_monomial_expansion(rho):
    out = {(): 1}
    for r in rho:
        new = {}
        for mu, c in out.items():
            for nu, d in multiply_power_monomial(r, mu).items():
                new[nu] = new.get(nu, 0) + c*d
        out = new
    return tuple(out.items())


class Functional:
    def __init__(self, q, ambient_t):
        self.q, self.t = q, ambient_t
        self.monomial = {(): 1}
        self.power = {(): 1}

    def acquire_degree(self, d):
        shapes = sorted(partitions(d))
        for lam in shapes:
            value = (-1)**d
            for i in range(lam[0]):
                # The original product is 1-u*q**(-i), u=q**t.
                value *= 1-self.q**(self.t-i)
            for mu in shapes:
                if mu >= lam:
                    break
                c = whittaker_monomial_coefficient(lam, mu, self.q)
                value -= c*self.monomial[mu]
            if whittaker_monomial_coefficient(lam, lam, self.q) != 1:
                raise AssertionError('monic triangular basis')
            self.monomial[lam] = value
        for rho in shapes:
            self.power[rho] = sum(c*self.monomial[mu]
                                  for mu, c in power_monomial_expansion(rho))

    def theta_power(self, rho):
        """Normalized full beta!=0,p=0 functional, even extension degree.

        Theta_t(f)=sum_b g_b L_(q**t)([z**b] f[X+z]), with
        g_(2v)=q**v, g_(4v+1)=q**(2v+1), g_(4v+3)=0.
        """
        values = sorted(set(rho))
        out = 0
        def rec(i, retained, removed_degree, multiplicity):
            nonlocal out
            if i == len(values):
                b = removed_degree
                g = 0 if b % 4 == 3 else self.q**((b+1)//2)
                out += multiplicity*g*self.power[tuple(sorted(retained, reverse=True))]
                return
            r = values[i]
            m = rho.count(r)
            for removed in range(m+1):
                rec(i+1, retained+[r]*(m-removed), removed_degree+r*removed,
                    multiplicity*comb(m, removed))
        rec(0, [], 0, 1)
        return out


def determinant(matrix):
    A = [row[:] for row in matrix]
    previous = 1
    sign = 1
    if not A:
        return 1
    for k in range(len(A)-1):
        if not A[k][k]:
            pivot = next((i for i in range(k+1, len(A)) if A[i][k]), None)
            if pivot is None:
                return 0
            A[k], A[pivot] = A[pivot], A[k]
            sign = -sign
        pivot = A[k][k]
        for i in range(k+1, len(A)):
            for j in range(k+1, len(A)):
                numerator = A[i][j]*pivot-A[i][k]*A[k][j]
                value, remainder = divmod(numerator, previous)
                if remainder:
                    raise AssertionError('Bareiss exact division')
                A[i][j] = value
        previous = pivot
    return sign*A[-1][-1]


def gaussian_moment(m, mean, variance):
    a, b = 1, mean
    if not m:
        return a
    for j in range(2, m+1):
        a, b = b, mean*b+(j-1)*variance*a
    return b


def limiting_power_moment(rho):
    value = 1
    for r in set(rho):
        value *= gaussian_moment(rho.count(r), r % 2, r)
    return value


def z_partition(rho):
    out = 1
    for r in set(rho):
        out *= r**rho.count(r)*factorial(rho.count(r))
    return out


def main():
    begun = time.perf_counter()
    rows = []
    for n in range(1, 7):
        shapes = partitions(n)
        change_determinant_squared = 1
        for p in shapes:
            change_determinant_squared *= z_partition(p)
        for q in (0, 2, 4):
            functional = Functional(q, 2*n)
            for d in range(1, 2*n+1):
                functional.acquire_degree(d)
            if q == 0:
                for rho, value in functional.power.items():
                    assert value == (-1)**sum(rho)*limiting_power_moment(rho)
            plain = [[functional.power[tuple(sorted(lam+mu, reverse=True))]
                      for mu in shapes] for lam in shapes]
            full = [[functional.theta_power(tuple(sorted(lam+mu, reverse=True)))
                     for mu in shapes] for lam in shapes]
            d_plain = determinant(plain)
            d_full = determinant(full)
            assert d_plain and d_full
            assert d_plain % change_determinant_squared == 0
            assert d_full % change_determinant_squared == 0
            if q == 0:
                assert d_plain == d_full > 0
            rows.append(dict(half_degree=n, ambient_t=2*n, q=q,
                state_rank=len(shapes), plain_schur_determinant=str(d_plain//change_determinant_squared),
                full_gaussian_schur_determinant=str(d_full//change_determinant_squared)))
            print(n, q, len(shapes), 'full rank', flush=True)
    result = dict(cases=rows, seconds=time.perf_counter()-begun,
        scope='Exact rank evidence, not a general polynomial counter; theorem is generic-q linear-summary lower bound')
    path = Path(__file__).with_name('whittaker_hankel_obstruction_results.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    print('saved', path, result['seconds'], flush=True)


if __name__ == '__main__':
    main()
